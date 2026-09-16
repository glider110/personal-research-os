"""Three-layer reading views: sources, metric features/time series, candidate factors."""
import json
import os
from pathlib import Path

TIMING = {'leading': '领先', 'coincident': '同步', 'lagging': '滞后', 'unknown': '待判断'}
POPULARITY = {'mainstream': '大众', 'niche': '小众', 'unknown': '待判断'}
CLASSES = {'primary': '一手来源', 'secondary': '二手资料', 'ai_generated': 'AI 整理', 'user_authored': '个人记录'}
COVERAGE = {'full': '完整文件', 'article_text': '正文文本', 'partial': '部分内容'}


def validate_features(package):
    metrics = {m['id']: m for m in package['metrics']}
    evidence = {e['id']: e for e in package['evidence']}
    sources = {s['id']: s for s in package['sources']}
    cutoff = package['analysis']['as_of_date']
    for m in metrics.values():
        source = sources[evidence[m['evidence_id']]['source_id']]
        if m['period_end'] > cutoff or not source['published_at'] or source['published_at'] > cutoff:
            raise ValueError('metric unavailable at as-of date: ' + m['id'])
        for role in ('corroborating', 'counter'):
            refs = m['features'][role]
            for ref in refs:
                if ref['metric_id'] not in metrics or ref['metric_id'] == m['id']:
                    raise ValueError('unknown/self feature metric reference: ' + ref['metric_id'])
            if len({(r['metric_id'], r['claim']) for r in refs}) != len(refs):
                raise ValueError('duplicate feature relation')
    for f in package['analysis']['factors']:
        if not f['metric_ids'] or len(set(f['metric_ids'])) != len(f['metric_ids']):
            raise ValueError('candidate factor requires unique supporting metrics')
        primary = set(f['metric_ids'])
        checks = [x['metric_id'] for x in f.get('cross_checks', [])]
        excluded = [x['metric_id'] for x in f.get('excluded_metrics', [])]
        if not (primary | set(checks) | set(excluded)) <= metrics.keys():
            raise ValueError('unknown factor filter metric')
        if primary & (set(checks) | set(excluded)) or set(checks) & set(excluded):
            raise ValueError('factor representative/check/excluded sets overlap')
        if len(checks) != len(set(checks)) or len(excluded) != len(set(excluded)):
            raise ValueError('duplicate factor filter metric')
        seen = set()
        for mid in primary:
            m = metrics[mid]
            group = m['features'].get('information_group')
            if group:
                key = (group, m['geography'], m['period_start'], m['period_end'])
                if key in seen:
                    raise ValueError('redundant factor representatives in same information group/period')
                seen.add(key)
        for mid in primary | set(checks):
            e = evidence[metrics[mid]['evidence_id']]
            if e['status'] != 'verified' or e['id'] not in f['evidence_ids']:
                raise ValueError('factor filter uses unverified/unlinked evidence')



def render(store, packages):
    root = store.root
    def write(path, lines):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix('.md.tmp')
        tmp.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
        tmp.replace(target)
    def cell(value):
        return str(value).replace('|', r'\|').replace('\n', ' ')
    def table(headers, rows):
        return ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] + [
            '| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows] + ['']
    mapping = json.loads((Path(__file__).resolve().parents[1] / 'config/legacy-paths.json').read_text())
    def link(label, target, page, anchor=''):
        for old, new in sorted(mapping.items(), key=lambda x: -len(x[0])):
            if target == old or target.startswith(old + '/'):
                target = new + target[len(old):]
                break
        path = os.path.relpath(root / target, (root / page).parent)
        return '[' + str(label).replace('[', '（').replace(']', '）') + '](' + path + ('#' + anchor if anchor else '') + ')'
    pages = {'source':'03-library/sources.md', 'metric':'03-library/metrics.md',
             'factor':'03-library/factors.md', 'evidence':'90-system/evidence.md'}
    ordered = sorted((p for p, c in packages), key=lambda p: (p['created_at'], p['id']))
    usages = list(store.db.execute('SELECT * FROM shared_usage ORDER BY package_id,local_id'))
    lookup = {(u['package_id'], u['kind'], u['local_id']): u['revision_id'] for u in usages}
    catalogs = {p['id']: {s['source_id']:s for s in c['sources']} for p,c in packages}
    def rid(p, kind, item_id): return lookup[p['id'],kind,item_id]
    def ilink(p, kind, item, page): return link(item.get('name', item.get('title', item['id'])), pages[kind], page, rid(p,kind,item['id']))
    def source_of(p, m):
        e = next(e for e in p['evidence'] if e['id'] == m['evidence_id'])
        return e, next(s for s in p['sources'] if s['id'] == e['source_id'])
    def slink(p, s, page):
        return link(s['title'], catalogs[p['id']][s['id']]['storage_uri'], page)
    def truth(e, s):
        return ('摘录与数值已核对' if e['status']=='verified' else '未核对') + '；源头统计未独立审计'

    # Keep all periods, conflicting values, and independent sources; collapse repeated imports.
    metrics = {}
    sources = {}
    evidence = {}
    for p in ordered:
        for s in p['sources']: sources[rid(p,'source',s['id'])] = (p,s)
        for e in p['evidence']: evidence[rid(p,'evidence',e['id'])] = (p,e)
        for m in p['metrics']:
            key = rid(p,'metric',m['id'])
            group = metrics.setdefault(key, {'observations':{}, 'topics':{}, 'features':{}, 'p':p, 'm':m})
            e,s = source_of(p,m)
            obskey = (m['period_start'],m['period_end'],m['value'],s['id'],s['sha256'],e['locator'],e['status'])
            group['observations'][obskey] = (p,m,e,s)
            group['topics'].setdefault(p['topic']['id'], {})[obskey] = (p,m,e,s)
            group['p'],group['m'] = p,m
            # Missing metadata in a later legacy import must not erase explicit annotations.
            if 'features' in m:
                group['features'][p['topic']['id']] = (p,m)
    latest = {}
    for p in ordered: latest[p['topic']['id']] = p
    factor_groups = {}
    for p in latest.values():
        for f in p['analysis']['factors']:
            factor_groups.setdefault(rid(p,'factor',f['id']), []).append((p,f))

    page=pages['source']
    rows=[]
    for key,(p,s) in sources.items():
        rows.append([f'<a id="{key}"></a>'+slink(p,s,page), CLASSES.get(s['source_class'],s['source_class']),
                     s['published_at'] or '未知', s['type']+'（原始类型 '+s['original_type']+'）', COVERAGE[s['coverage']]])
    write(page, ['# 数据源', '', '按原文版本去重；采集到的文本不等于原视频或完整网页。', '']+table(['来源 / 原文','来源性质','发布日期','保存格式','采集范围'],rows))

    page=pages['metric']
    out=['# 指标：特征与历次数据', '', '每个指标只展示一次，历次观测保留；不同口径不合并。真实性描述的是核对范围，不是绝对保证。', '', '[主题入口](../04-research/README.md)', '']
    out += table(['指标','单位','观测记录数'], [[ilink(g['p'],'metric',g['m'],page),g['m']['unit'],len(g['observations'])] for g in metrics.values()])
    for key,g in metrics.items():
        p,m=g['p'],g['m']
        out += [f'<a id="{key}"></a>', '## '+m['name'], '']
        basic = [['名称',m['name']],['表达形式',{'level':'原始量','change_rate':'变化率（衍生表达）','composite':'综合指标','unknown':'待判断'}.get(m.get('features',{}).get('representation','unknown'))],['单位',m['unit']],['地区 / 范围',m['geography']],['统计口径',m['methodology']],['频率', {'cumulative':'累计口径（每次发布保留一期）','annual':'年度','monthly':'月度','point_in_time':'时点'}.get(m['frequency'],m['frequency'])],['数据真实性','见下表逐条核对状态；原文核对不代表源头统计审计']]
        for fp,fm in g['features'].values():
            a=fm['features']; timing=a['timing']; pop=a['popularity']
            def relations(role):
                entries=[]
                for ref in a[role]:
                    other=next(x for x in fp['metrics'] if x['id']==ref['metric_id'])
                    entries.append(ilink(fp,'metric',other,page)+'；针对“'+ref['claim']+'”：'+ref['rationale'])
                return '<br>'.join(entries) or '未登记；不代表不存在'
            out += ['### 多维特征 · '+fp['topic']['name'], '', '以下属性是分析标注，尚待复核。', '']
            out += table(['属性','内容'], basic + [['主题相关性',a['relevance']],['领先 / 同步 / 滞后',TIMING[timing['type']]+'；相对于 '+timing['relative_to']+'；'+timing['rationale']],['大众 / 小众',POPULARITY[pop['type']]+'；'+pop['rationale']],['旁证指标',relations('corroborating')],['反证指标',relations('counter')],['待补数据','；'.join(a['gaps']) or '暂无登记']])
        if not g['features']: out += table(['特征','内容'],basic) + ['其他特征尚未提取，不自动猜测领先性或大众程度。', '']
        rows=[]
        observations=sorted(g['observations'].values(), key=lambda x:(x[1]['period_end'],x[1]['period_start'],x[3]['published_at'] or '',x[1]['value']))
        for op,om,e,s in observations:
            rows.append([om['period_start']+'～'+om['period_end'],str(om['value'])+' '+om['unit'],s['published_at'] or '未知',s['captured_at'],slink(op,s,page)+'；'+e['locator'],truth(e,s)])
        out += ['### 历次观测', '']+table(['统计期间','数据','发布日期','采集时间','来源与定位','核对状态'],rows)
    write(page,out)

    page=pages['factor']
    out=['# 因子：从指标提炼的底层因素', '', '因子是尽量不重复的解释维度，目前为候选提炼；“线性无关”尚未经过统计验证。', '']
    for key,items in factor_groups.items():
        out += [f'<a id="{key}"></a>', '## '+items[0][1]['name'], '']
        for p,f in items:
            refs=[ilink(p,'metric',m,page) for m in p['metrics'] if m['id'] in f['metric_ids']]
            out += table(['属性','内容'], [['主题',p['topic']['name']],['底层含义',f['mechanism']],['代表指标','<br>'.join(dict.fromkeys(refs)) or '缺失，尚不能提炼'],['提炼 / 去重理由',f.get('selection_reason','旧版因子草稿，尚未按新定义提炼')],['独立性与重叠',f.get('independence_note','未验证；不自动视为独立因素')],['状态','候选因子，待复核']])
            cross=[]
            for check in f.get('cross_checks', []):
                m=next(m for m in p['metrics'] if m['id']==check['metric_id'])
                cross.append([{'support':'旁证','challenge':'反证','contrast':'口径对照'}[check['role']],ilink(p,'metric',m,page),check['note']])
            for excluded in f.get('excluded_metrics', []):
                m=next(m for m in p['metrics'] if m['id']==excluded['metric_id'])
                cross.append(['排除重复',ilink(p,'metric',m,page),excluded['reason']])
            out += ['### 过滤与交叉验证', '']
            out += table(['处理','指标','理由'],list(dict.fromkeys(tuple(row) for row in cross))) if cross else ['暂无额外指标用于交叉核验。', '']
            out += [f.get('validation_note','尚未登记交叉验证与去重结果；保持候选。'), '']

    if not factor_groups: out += ['尚无足够指标提炼因子。']
    write(page,out)

    page=pages['evidence']
    out=['# 原文核对记录（辅助追溯）', '', '日常阅读从指标表进入；此表只保存原文核对依据。', '']
    out += table(['摘录','来源 / 定位','状态'], [[f'<a id="{key}"></a>'+e['excerpt'],slink(p,next(s for s in p['sources'] if s['id']==e['source_id']),page)+'；'+e['locator'],e['status']] for key,(p,e) in evidence.items()])
    write(page,out)

    pending=['# 待补与待核对', '', '只列数据缺口和冲突；不是情景推演任务清单。', '']
    for p in latest.values():
        pending += ['## '+p['topic']['name'], '']+['- '+x for x in p['analysis']['limitations']]+['']
    for key,(p,e) in evidence.items():
        if e['status']=='pending': pending.append('- '+link(e['claim'],pages['evidence'],'04-research/01-pending.md',key))
    pending += ['', '## 同口径、同期间的观测值冲突', '']
    conflicts=0
    for key,g in metrics.items():
        periods={}
        for op,om,e,s in g['observations'].values(): periods.setdefault((om['period_start'],om['period_end']),[]).append((om['value'],op['id']))
        for period,values in periods.items():
            if len({v for v,pid in values})>1:
                conflicts+=1
                pending += ['- '+link(g['m']['name'],pages['metric'],'04-research/01-pending.md',key)+'（'+' 至 '.join(period)+'）：'+'；'.join(f'{v}，批次 {pid}' for v,pid in values)]
    if not conflicts: pending += ['暂无同口径、同期间的数值冲突。']
    write('04-research/01-pending.md',pending)

    topics=['# 主题数据蒸馏', '', '选择主题，按数据源 → 指标 → 因子阅读。', '']
    for topic,p in latest.items():
        page='04-research/'+p['topic']['slug']+'.md'
        topics += ['- '+link(p['topic']['name'],page,'04-research/README.md')]
        relevant={key:g for key,g in metrics.items() if topic in g['topics']}
        out=['# '+p['topic']['name']+' · 数据蒸馏', '', '**数据源 → 指标 → 因子。当前到因子层结束。**', '', f'整理截止日：{p["analysis"]["as_of_date"]}。数值所属期间见表，不代表当前市场数据。', '', '## 1. 数据源', '']
        used_sources={rid(op,'source',s['id']):(op,s) for op in ordered if op['topic']['id']==topic for s in op['sources']}
        metric_source_ids={s['id'] for g in relevant.values() for op,om,e,s in g['topics'][topic].values()}
        out += table(['指标来源','性质','内容范围'],[[slink(op,s,page),CLASSES.get(s['source_class'],s['source_class']),COVERAGE[s['coverage']]] for op,s in used_sources.values() if s['id'] in metric_source_ids])
        out += [link('全部来源（含未核对材料）',pages['source'],page), '']
        out += ['## 2. 指标', '', '点击名称查看多维特征表与历次观测；此处只列每个指标的最近统计期间。', '']
        rows=[]
        for key,g in relevant.items():
            obs=list(g['topics'][topic].values())
            end=max(o[1]['period_end'] for o in obs)
            recent=[o for o in obs if o[1]['period_end']==end]
            op,om,e,s=recent[-1]
            vals=list(dict.fromkeys(str(o[1]['value'])+' '+o[1]['unit'] for o in recent))
            rows.append([ilink(op,'metric',om,page),om['period_start']+'～'+end,' / '.join(vals), '多值，需核对' if len(vals)>1 else '原文数值已核对'])
        out += table(['指标','最近统计期间','数据','状态'],rows)
        out += ['## 3. 因子', '', '把相近指标归并成少量核心因素，避免重复计数。', '']
        rows=[]
        for f in p['analysis']['factors']:
            names=list(dict.fromkeys(m['name'] for m in p['metrics'] if m['id'] in f['metric_ids']))
            rows.append([ilink(p,'factor',f,page),f['mechanism'],'；'.join(names),f.get('validation_note',f.get('selection_reason','旧草稿待重新提炼'))])
        out += table(['候选因子','底层含义','代表指标','逻辑核验'],rows)
        if not rows: out += ['指标不足，暂不提炼因子。', '']
        out += ['## 待补', '']+['- '+x for x in p['analysis']['limitations']]+['',link('全部待核对项','04-research/01-pending.md',page),'']
        write(page,out)
    topics += ['', '[待补与待核对](01-pending.md)', '', '历史快照在 `../90-system/history/`，仅作存档。']
    write('04-research/README.md',topics)
