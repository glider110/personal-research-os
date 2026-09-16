"""Shared, versioned identities and reproducible human-readable research views."""
import hashlib
import json
import os
from pathlib import Path
import re


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def register_package(store, package, manifest):
    """Runs inside the caller's transaction; never replaces a historical assessment."""
    db = store.db
    refs = {}
    archives = {s['source_id']: s for s in manifest}
    sources = {s['id']: s for s in package['sources']}

    def register(kind, item, definition, identity=None):
        oid = identity or item.get('shared_id') or ('shared.' + kind + '.' + fingerprint(definition))
        existing = db.execute('SELECT kind FROM shared_object WHERE id=?', (oid,)).fetchone()
        require(existing is None or existing['kind'] == kind, 'shared ID reused for another object kind')
        rid = 'revision.' + fingerprint({'id': oid, 'definition': definition})
        db.execute('INSERT OR IGNORE INTO shared_object VALUES (?,?)', (oid, kind))
        db.execute('INSERT OR IGNORE INTO shared_revision VALUES (?,?,?)', (rid, oid, encode(definition)))
        payload = dict(item)
        if kind == 'source':
            payload['archive'] = archives[item['id']]['storage_uri']
        values = (package['id'], kind, item['id'], rid, package['topic']['id'], encode(payload))
        old = db.execute('SELECT * FROM shared_usage WHERE package_id=? AND kind=? AND local_id=?', values[:3]).fetchone()
        require(old is None or tuple(old) == values, 'immutable shared usage conflict')
        db.execute('INSERT OR IGNORE INTO shared_usage VALUES (?,?,?,?,?,?)', values)
        refs[(kind, item['id'])] = rid
        return rid

    def relation(a, rel, b):
        payload = [a, rel, b, package['id'], 'reference', '结构引用；不自动证明支持或因果成立']
        db.execute('INSERT OR IGNORE INTO shared_relation VALUES (?,?,?,?,?,?,?)',
                   ('relation.' + fingerprint(payload), *payload))

    for s in package['sources']:
        register('source', s, {k: s[k] for k in ('title', 'canonical_uri', 'sha256')}, s['id'])
    for e in package['evidence']:
        s = sources[e['source_id']]
        definition = {k: e[k] for k in ('claim', 'excerpt', 'locator', 'kind')}
        definition.update(source_id=s['id'], source_sha256=s['sha256'])
        rid = register('evidence', e, definition)
        relation(rid, 'extracted_from', refs['source', e['source_id']])
    for m in package['metrics']:
        definition = {k: m[k] for k in ('name', 'unit', 'frequency', 'geography', 'methodology')}
        rid = register('metric', m, definition)
        relation(rid, 'measured_by', refs['evidence', m['evidence_id']])
    for f in package['analysis']['factors']:
        definition = {k: f[k] for k in ('name', 'mechanism')}
        definition['scope'] = package['topic']['scope']
        rid = register('factor', f, definition)
        for eid in f['evidence_ids']:
            relation(rid, 'uses_evidence', refs['evidence', eid])
        for mid in f['metric_ids']:
            relation(rid, 'uses_metric', refs['metric', mid])
    for edge in package['analysis']['causal_edges']:
        definition = {k: edge[k] for k in ('outcome', 'sign', 'mechanism', 'lag', 'scope', 'falsifier')}
        definition['from_factor_revision'] = refs['factor', edge['from_factor_id']]
        rid = register('hypothesis', edge, definition)
        for eid in edge['evidence_ids']:
            relation(rid, 'uses_evidence', refs['evidence', eid])


def load_relations(store):
    """Explicit supports/refutes files are append-only by relation ID."""
    folder = store.root / '03-library/05-relations/assertions'
    for file in sorted(folder.glob('*.json')):
        d = json.loads(file.read_text())
        keys = {'id', 'from_revision', 'relation', 'to_revision', 'status', 'rationale'}
        require(set(d) == keys, f'invalid relation fields: {file.name}')
        require(all(isinstance(v, str) and v.strip() for v in d.values()), 'relation fields must be nonempty strings')
        require(re.fullmatch(r'[a-z0-9][a-z0-9._-]*', d['id']), 'invalid relation ID')
        require(d['relation'] in ('supports', 'refutes') and d['status'] in ('pending', 'reviewed'), 'invalid assertion state')
        kinds = []
        for field in ('from_revision', 'to_revision'):
            row = store.db.execute('SELECT o.kind FROM shared_revision r JOIN shared_object o ON o.id=r.object_id WHERE r.id=?', (d[field],)).fetchone()
            require(row is not None, f'unknown relation revision: {d[field]}')
            kinds.append(row['kind'])
        require(kinds[0] == 'evidence' and kinds[1] in ('factor', 'hypothesis'), 'assertions must link evidence to factor/hypothesis')
        values = (d['id'], d['from_revision'], d['relation'], d['to_revision'], None, d['status'], d['rationale'])
        old = store.db.execute('SELECT * FROM shared_relation WHERE id=?', (d['id'],)).fetchone()
        require(old is None or tuple(old) == values, 'relation ID reused with different content')
        store.db.execute('INSERT OR IGNORE INTO shared_relation VALUES (?,?,?,?,?,?,?)', values)


def rebuild(store):
    packages = []
    # Verify ALL packages and archived inputs before touching shared records/views.
    for row in store.db.execute('SELECT id FROM processing_package ORDER BY id').fetchall():
        p, catalog = store.read_package(row['id'])
        packages.append((p, catalog))
    with store.db:
        for p, catalog in packages:
            register_package(store, p, catalog['sources'])
        load_relations(store)
    render(store, packages)
    return {'status': 'rebuilt', 'objects': store.db.execute('SELECT count(*) FROM shared_object').fetchone()[0],
            'revisions': store.db.execute('SELECT count(*) FROM shared_revision').fetchone()[0],
            'usages': store.db.execute('SELECT count(*) FROM shared_usage').fetchone()[0],
            'entry': str(store.root / '03-library/README.md')}


def render(store, packages):
    # Relative imports avoid coupling to the executable's module name in tests.
    mapping = json.loads((Path(__file__).resolve().parents[1] / '05-config/legacy-paths.json').read_text())
    def current(relative):
        for old, new in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
            if relative.startswith(old + '/'):
                return new + relative[len(old):]
        return relative
    def link(label, target, page):
        relative = os.path.relpath(store.root / current(target), (store.root / page).parent)
        return f'[{label.replace("[", "（").replace("]", "）")}]({relative})'
    def write(path, text):
        dst = store.root / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_suffix(dst.suffix + '.tmp')
        tmp.write_text(text, encoding='utf-8')
        tmp.replace(dst)
    def cell(text):
        return str(text).replace('|', r'\|').replace('\n', ' ')

    dirs = {'source': '01-sources', 'evidence': '02-evidence', 'metric': '03-metrics', 'factor': '04-factors', 'hypothesis': '05-relations'}
    names = {'source':'来源', 'evidence':'证据', 'metric':'指标', 'factor':'因子', 'hypothesis':'因果假设'}
    filenames = {'source': 'sources.md', 'evidence': 'evidence.md', 'metric': 'metrics.md',
                 'factor': 'factors.md', 'hypothesis': 'hypotheses.md'}
    pages = {k: f'03-library/{v}/{filenames[k]}' for k, v in dirs.items()}
    # README files are maintained documentation, never regenerated from research data.
    template_root = Path(__file__).resolve().parents[2]
    for relative in ['03-library/README.md'] + [f'03-library/{d}/README.md' for d in dirs.values()]:
        if not (store.root / relative).exists():
            write(relative, (template_root / relative).read_text())
    all_rows = store.db.execute('SELECT r.*, o.kind FROM shared_revision r JOIN shared_object o ON o.id=r.object_id ORDER BY o.kind,o.id,r.id').fetchall()
    def objlink(rid, page):
        row = next(r for r in all_rows if r['id'] == rid)
        d = json.loads(row['definition_json'])
        label = d.get('name') or d.get('title') or d.get('claim') or d.get('outcome')
        return link(label, pages[row['kind']], page)[:-1] + '#' + rid + ')'
    labels = {'name':'名称', 'title':'标题', 'canonical_uri':'原始地址', 'sha256':'文件指纹',
              'unit':'单位', 'frequency':'频率', 'geography':'地区', 'methodology':'统计口径',
              'claim':'说法', 'excerpt':'原文摘录', 'locator':'原文定位', 'kind':'类别',
              'source_id':'来源 ID', 'source_sha256':'来源指纹', 'mechanism':'机制', 'scope':'适用范围',
              'outcome':'影响结果', 'sign':'作用方向', 'lag':'时滞', 'falsifier':'反证条件',
              'from_factor_revision':'起点因子版本'}
    relation_labels = {'extracted_from':'摘录自', 'measured_by':'指标依据', 'uses_evidence':'引用证据',
                       'uses_metric':'引用指标', 'supports':'支持', 'refutes':'反驳'}
    for kind, page in pages.items():
        out = [f'# 共享{names[kind]}数据', '', '由结果包生成；不要手工修改。跨主题引用同一对象，评估状态和数值保留在各次使用记录中。', '', '[目录说明](README.md) · [数据概览](../overview.md)', '']
        rows = [r for r in all_rows if r['kind'] == kind]
        headers = {
            'source':['来源','类别','覆盖范围','归档原文'],
            'evidence':['证据','审核状态','原文定位','引用来源'],
            'metric':['指标','期间','数值','单位','地区','口径'],
            'factor':['因子','评估日期','方向','置信度','研究','审核状态'],
            'hypothesis':['因果假设','作用方向','机制','时滞','反证条件','审核状态']}
        out += ['## 数据总表', '', '| '+' | '.join(headers[kind])+' |', '| '+' | '.join(['---']*len(headers[kind]))+' |']
        for row in rows:
            definition = json.loads(row['definition_json'])
            for u in store.db.execute('SELECT * FROM shared_usage WHERE revision_id=? ORDER BY package_id,local_id',(row['id'],)):
                item = json.loads(u['payload_json'])
                package = next(p for p,c in packages if p['id']==u['package_id'])
                name = objlink(row['id'],page)
                if kind=='source':
                    values=[name,item['source_class'],item['coverage'],link('原文',item['archive'],page)]
                elif kind=='evidence':
                    values=[name,item['status'],item['locator'],item['source_id']]
                elif kind=='metric':
                    values=[name,item['period_start']+' 至 '+item['period_end'],item['value'],item['unit'],item['geography'],item['methodology']]
                elif kind=='factor':
                    values=[name,package['analysis']['as_of_date'],item['direction'],item['confidence'],package['topic']['name'],'待人工审核']
                else:
                    values=[name,item['sign'],item['mechanism'],item['lag'],item['falsifier'],'待验证假设']
                out.append('| '+' | '.join(cell(v) for v in values)+' |')
        out.append('')
        for row in rows:
            d = json.loads(row['definition_json'])
            title = d.get('name') or d.get('title') or d.get('claim') or d.get('outcome')
            out += [f'<a id="{row["id"]}"></a>', f'## {title}', '', '| 字段 | 内容 |', '|---|---|']
            for key,value in d.items():
                if key not in ('sha256','source_sha256','source_id','from_factor_revision'):
                    out.append('| '+labels.get(key,key)+' | '+cell(value)+' |')
            out += ['', '<details>', '<summary>追溯标识</summary>', '', '| 标识 | 值 |', '|---|---|',
                    f'| 共享 ID | `{row["object_id"]}` |', f'| 定义版本 | `{row["id"]}` |']
            for key in ('sha256','source_sha256','source_id','from_factor_revision'):
                if key in d: out.append('| '+labels[key]+' | `'+d[key]+'` |')
            out += ['', '</details>', '', '### 使用与评估', '', '| 研究 | 来源批次 | 本次记录 |', '|---|---|---|']
            for u in store.db.execute('SELECT * FROM shared_usage WHERE revision_id=? ORDER BY topic_id,package_id,local_id', (row['id'],)):
                payload = json.loads(u['payload_json'])
                p = next(p for p,c in packages if p['id'] == u['package_id'])
                research = link(p['topic']['name'], f'04-research/{p["topic"]["slug"]}.md', page)
                package_link = link(u['package_id'], f'03-library/08-packages/{p["topic"]["slug"]}/{p["id"]}/package.json', page)
                detail = payload.get('status', '')
                if kind == 'metric':
                    detail = f'{payload["period_start"]} 至 {payload["period_end"]}：{payload["value"]} {payload["unit"]}'
                elif kind == 'factor':
                    detail = f'{p["analysis"]["as_of_date"]}：{payload["direction"]} / {payload["confidence"]}（待人工审核）'
                elif kind == 'source':
                    detail = link('归档原文', payload['archive'], page) + ' / ' + payload['coverage'] + ' / ' + payload['source_class']
                out.append('| '+' | '.join(cell(v) for v in [research,package_link,detail])+' |')
            relations = store.db.execute('SELECT * FROM shared_relation WHERE from_revision=? OR to_revision=? ORDER BY id', (row['id'],row['id'])).fetchall()
            out += ['', '### 关联与交叉核验', '', '| 起点 | 关系 | 终点 | 状态 | 解释 |', '|---|---|---|---|---|']
            for rel in relations:
                values=[objlink(rel['from_revision'],page),relation_labels[rel['relation']],objlink(rel['to_revision'],page),rel['status'],rel['rationale']]
                out.append('| '+' | '.join(cell(v) for v in values)+' |')
            if not relations:
                out.append('| — | — | — | 尚无记录 | 不自动补出支持或反驳 |')
            out.append('')
        if not rows:
            out.append('暂无对象。')
        write(page, '\n'.join(out).rstrip()+'\n')
    index = ['# 共享研究库数据概览', '', '先找对象，再查看它在哪些研究中被使用。主题不拥有数据，批次不切割知识。', '', '| 入口 | 定义版本数 |', '|---|---:|']
    for kind, page in pages.items():
        index.append(f'| {link(names[kind], page, "03-library/overview.md")} | {sum(r["kind"] == kind for r in all_rows)} |')
    index += ['', '[研究问题与待核验事项](../04-research/README.md)', '', '修改结果应创建新版结果包，然后执行 `python3 90-system/03-scripts/research.py library` 刷新这些视图。', '', '同名不自动合并；共同引用不等于独立验证。支持/反驳必须登记在 `05-relations/assertions/` 的版本化 JSON 文件中。', '']
    write('03-library/overview.md','\n'.join(index))
    topic_ids = sorted({p['topic']['id'] for p,c in packages})
    overview = ['# 研究问题与待核验事项', '', '每项研究引用共享库，下面是自动生成的视图，不再复制因子定义。', '']
    pending = ['# 待核验与冲突', '', '本页列出实际缺口；不会自动把不同时间、不同口径的数值判为冲突。', '']
    for topic in topic_ids:
        group = [p for p,c in packages if p['topic']['id'] == topic]
        page = f'04-research/{group[0]["topic"]["slug"]}.md'
        overview.append('- ' + link(group[0]['topic']['name'], page, '04-research/README.md'))
        out = ['# '+group[0]['topic']['name'], '', '[共享研究库](../03-library/README.md) · [待核验](01-pending.md)', '']
        for p in group:
            out += ['## '+p['analysis']['question'], '', f'追溯批次：`{p["id"]}`；截止日：{p["analysis"]["as_of_date"]}；分析待人工审核。', '', '### 引用对象', '']
            for u in store.db.execute('SELECT * FROM shared_usage WHERE package_id=? ORDER BY kind,local_id',(p['id'],)):
                out.append('- '+names[u['kind']]+'：'+objlink(u['revision_id'],page))
            out += ['', '### 条件性情景（本研究草稿）', '']
            for s in p['analysis']['scenarios']:
                out += [f'- **{s["name"]}**：条件：'+ '；'.join(s['assumptions'])+'。反证：'+'；'.join(s['falsifiers'])]
            out += ['', '### 审核缺口', ''] + ['- '+x for x in p['analysis']['limitations']]
            pending += ['## '+p['id'], '']
            for e in p['evidence']:
                if e['status'] == 'pending':
                    u = store.db.execute('SELECT revision_id FROM shared_usage WHERE package_id=? AND kind=? AND local_id=?',(p['id'],'evidence',e['id'])).fetchone()
                    pending.append('- '+objlink(u['revision_id'],'04-research/01-pending.md'))
            pending += ['- '+x for x in p['analysis']['limitations']] + ['']
        write(page,'\n'.join(out)+'\n')
    overview += ['', '[待核验与冲突](01-pending.md)', '', '## 历史运行（当前路径阅读副本）', '']
    for row in store.db.execute('SELECT id FROM run_snapshot ORDER BY id').fetchall():
        run = store.read_run(row['id'])
        original = store.root / '05-runs' / (row['id']+'.md')
        text = original.read_text()
        # Resolve only local Markdown links. Preserve original hashed Markdown.
        page = '04-research/02-history/'+original.name
        def rewrite(m):
            target=m[2]
            if target.startswith('../'):
                return link(m[1],current(target[3:]),page)
            return m[0]
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',rewrite,text)
        write(page,'> 当前路径阅读副本，原始快照内容保持不变。\n\n'+text)
        overview.append('- '+link(row['id'],page,'04-research/README.md'))
    comparable = {}
    for u in store.db.execute("SELECT * FROM shared_usage WHERE kind='metric'"):
        m = json.loads(u['payload_json'])
        key = (u['revision_id'], m['period_start'], m['period_end'])
        comparable.setdefault(key, []).append((m['value'], u['package_id']))
    pending += ['## 同口径、同期间的观测值冲突', '']
    numeric_conflicts = [(key, values) for key, values in comparable.items() if len({v for v,p in values}) > 1]
    for (rid, start, end), values in numeric_conflicts:
        pending.append('- ' + objlink(rid, '04-research/01-pending.md') + f'（{start} 至 {end}）：' +
                       '；'.join(f'{v}，批次 {p}' for v,p in sorted(set(values))))
    if not numeric_conflicts:
        pending.append('暂无同一定义版本、同期间的数值冲突；不同统计口径不自动比较。')
    conflicts = store.db.execute("SELECT to_revision FROM shared_relation WHERE relation IN ('supports','refutes') GROUP BY to_revision HAVING count(DISTINCT relation)=2").fetchall()
    pending += ['## 同时存在支持与反驳的对象', '']
    pending += ['- '+objlink(r[0],'04-research/01-pending.md') for r in conflicts] or ['暂无已登记的双向证据关系；不代表不存在争议。']
    write('04-research/01-pending.md','\n'.join(pending)+'\n')
    write('04-research/README.md','\n'.join(overview)+'\n')
