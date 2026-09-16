#!/usr/bin/env python3
"""Local, append-only research package pipeline (Python standard library only)."""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import sqlite3
import sys

CODE_ROOT = Path(__file__).resolve().parents[2]
VERSION = 'pipeline-v0.2'
LEGACY_PATHS = json.loads((CODE_ROOT / '90-system/05-config/legacy-paths.json').read_text())

def artifact(root, relative):
    # Resolve frozen paths without changing historical payloads or hashes.
    for old, new in sorted(LEGACY_PATHS.items(), key=lambda item: len(item[0]), reverse=True):
        if relative.startswith(old + '/'):
            relative = new + relative[len(old):]
            break
    return inside(root, relative)



def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError(f'duplicate JSON key: {k}')
            result[k] = v
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def require(test, message):
    if not test:
        raise ValueError(message)


def check_schema(value, schema, path='$'):
    """Validate the explicit subset used by our checked-in JSON Schema, fail closed."""
    supported = {'$schema', '$id', 'title', 'type', 'properties', 'required', 'additionalProperties',
                 'items', 'minItems', 'enum', 'minLength', 'pattern', 'format', 'anyOf'}
    require(not set(schema) - supported, f'{path}: unsupported schema keyword')
    if 'anyOf' in schema:
        for option in schema['anyOf']:
            try:
                check_schema(value, option, path)
                return
            except ValueError:
                pass
        raise ValueError(f'{path}: no matching schema alternative')
    types = schema.get('type', [])
    if isinstance(types, str):
        types = [types]
    tests = {'object': isinstance(value, dict), 'array': isinstance(value, list),
             'string': isinstance(value, str), 'null': value is None,
             'number': type(value) in (int, float) and math.isfinite(value)}
    require(not types or any(tests.get(t, False) for t in types), f'{path}: wrong type')
    if 'enum' in schema:
        require(value in schema['enum'], f'{path}: invalid enum')
    if isinstance(value, dict):
        require(set(schema.get('required', [])) <= set(value), f'{path}: missing required fields')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            require(not set(value) - set(props), f'{path}: unknown fields {set(value) - set(props)}')
        for key, child in value.items():
            if key in props:
                check_schema(child, props[key], f'{path}.{key}')
    elif isinstance(value, list):
        require(len(value) >= schema.get('minItems', 0), f'{path}: too few items')
        for i, child in enumerate(value):
            check_schema(child, schema.get('items', {}), f'{path}[{i}]')
    elif isinstance(value, str):
        require(len(value.strip()) >= schema.get('minLength', 0), f'{path}: empty string')
        if 'pattern' in schema:
            require(re.fullmatch(schema['pattern'], value) is not None, f'{path}: invalid pattern')
        if schema.get('format') == 'date':
            require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), f'{path}: invalid date')
            dt.date.fromisoformat(value)
        elif schema.get('format') == 'date-time':
            parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
            require(parsed.tzinfo is not None, f'{path}: timezone required')


def index(items, label):
    result = {item['id']: item for item in items}
    require(len(result) == len(items), f'duplicate {label} IDs')
    return result


def inside(base, relative):
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts, f'unsafe path: {relative}')
    target = (base / p).resolve()
    require(target.is_relative_to(base.resolve()), f'path escapes root: {relative}')
    return target


def validate(package_path):
    package_path = Path(package_path).resolve()
    p = load(package_path)
    check_schema(p, load(CODE_ROOT / '90-system/02-schemas/processing-package.schema.json'))
    sources = index(p['sources'], 'source')
    evidence = index(p['evidence'], 'evidence')
    metrics = index(p['metrics'], 'metric')
    factors = index(p['analysis']['factors'], 'factor')
    index(p['analysis']['scenarios'], 'scenario')
    index(p['analysis']['causal_edges'], 'causal edge')
    files = {}
    for s in sources.values():
        file = inside(package_path.parent, s['file'])
        require(file.is_file(), f'missing source file: {file}')
        content = file.read_bytes()
        require(digest(content) == s['sha256'], f'hash mismatch: {s["id"]}')
        require(s['canonical_uri'].startswith(('https://', 'http://', 'local:')), 'invalid source URI')
        files[s['id']] = content
    for e in evidence.values():
        require(e['source_id'] in sources, f'unknown evidence source: {e["id"]}')
        if e['status'] == 'verified':
            s = sources[e['source_id']]
            require(s['source_class'] != 'ai_generated' and e['kind'] == 'fact', 'AI/claim cannot be verified fact')
            require(e['review'] is not None, 'verified evidence requires review record')
            require(s['published_at'] is not None, 'verified evidence needs publication date')
            try:
                text = files[s['id']].decode('utf-8')
            except UnicodeDecodeError as exc:
                raise ValueError('verified evidence needs a text extraction source') from exc
            require(''.join(e['excerpt'].split()) in ''.join(text.split()), f'excerpt not in source: {e["id"]}')
    for m in metrics.values():
        require(m['evidence_id'] in evidence, f'unknown metric evidence: {m["id"]}')
        e = evidence[m['evidence_id']]
        require(e['status'] == 'verified', f'metric uses unverified evidence: {m["id"]}')
        token = m['value_text']
        require(re.search(r'(?<![\d.])' + re.escape(token) + r'(?![\d.])', e['excerpt']),
                f'metric value text absent from evidence: {m["id"]}')
        extracted = float(token.replace(',', ''))
        if m['value_transform'] == 'negate':
            extracted = -extracted
        require(extracted == m['value'], f'metric numeric conversion mismatch: {m["id"]}')
        require(m['period_start'] <= m['period_end'], 'invalid metric period')
    for f in factors.values():
        require(set(f['evidence_ids']) <= set(evidence), f'unknown factor evidence: {f["id"]}')
        require(set(f['metric_ids']) <= set(metrics), f'unknown factor metrics: {f["id"]}')
        for mid in f['metric_ids']:
            require(metrics[mid]['evidence_id'] in f['evidence_ids'], 'factor metric missing evidence link')
    for s in p['analysis']['scenarios']:
        require(set(s['factor_ids']) <= set(factors), 'unknown scenario factors')
    for edge in p['analysis']['causal_edges']:
        require(edge['from_factor_id'] in factors, 'unknown causal factor')
        require(set(edge['evidence_ids']) <= set(evidence), 'unknown causal evidence')
    require(p['analysis']['next_review_date'] >= p['analysis']['as_of_date'], 'review precedes as-of date')
    return p, files


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        db = artifact(self.root, '90-system/07-runtime/research.sqlite3')
        db.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(db)
        self.db.row_factory = sqlite3.Row
        self.db.executescript((CODE_ROOT / '90-system/01-db/schema.sql').read_text())

    def put(self, table, values):
        keys = list(values)
        self.db.execute(f'INSERT INTO {table} ({",".join(keys)}) VALUES ({",".join("?" for _ in keys)})', list(values.values()))

    def write(self, relative, data, created):
        path = artifact(self.root, relative)
        if path.exists():
            require(path.read_bytes() == data, f'immutable artifact conflict: {relative}')
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            created.append(path)
            stream.write(data)

    def import_package(self, path):
        p, files = validate(path)
        content_hash = digest(encoded(p))
        created = []
        try:
            self.db.execute('BEGIN IMMEDIATE')
            existing = self.db.execute('SELECT * FROM processing_package WHERE id=?', (p['id'],)).fetchone()
            if existing:
                require(existing['content_hash'] == content_hash, 'package ID reused with different content')
                self.read_package(p['id'])
                self.db.rollback()
                return {'id': p['id'], 'status': 'already_imported'}
            topic = p['topic']
            old = self.db.execute('SELECT * FROM topic WHERE id=?', (topic['id'],)).fetchone()
            if old:
                require(old['name'] == topic['name'] and old['scope'] == topic['scope'], 'topic definition conflict')
            else:
                self.put('topic', dict(id=topic['id'], name=topic['name'], kind='industry', scope=topic['scope'],
                                      status='draft', created_at=now(), updated_at=now()))
            manifest = []
            snapshot_ids = {}
            for s in p['sources']:
                snapshot = 'snapshot.' + s['id'] + '.' + digest(encoded(s))[:16]
                snapshot_ids[s['id']] = snapshot
                rel = f'02-sources/{topic["slug"]}/{s["type"]}/{s["id"]}/{snapshot}/{Path(s["file"]).name}'
                old = self.db.execute('SELECT * FROM source WHERE id=?', (s['id'],)).fetchone()
                if old:
                    require(old['canonical_uri'] == s['canonical_uri'] and old['title'] == s['title'], 'source identity conflict')
                else:
                    self.put('source', dict(id=s['id'], topic_id=topic['id'], title=s['title'], source_type=s['type'],
                                           publisher=s['publisher'], canonical_uri=s['canonical_uri'],
                                           published_at=s['published_at'], created_at=p['created_at']))
                existing_snapshot = self.db.execute('SELECT * FROM source_snapshot WHERE id=?', (snapshot,)).fetchone()
                if existing_snapshot:
                    rel = existing_snapshot['storage_uri']
                self.write(rel, files[s['id']], created)
                if not existing_snapshot:
                    self.put('source_snapshot', dict(id=snapshot, source_id=s['id'], storage_uri=rel,
                             content_hash=s['sha256'], captured_at=s['captured_at'],
                             is_official_input=int(s['source_class'] == 'primary')))
                    self.put('source_provenance', dict(source_snapshot_id=snapshot, source_class=s['source_class'],
                             original_type=s['original_type'], capture_method=s['capture_method'], coverage=s['coverage']))
                manifest.append(dict(source_id=s['id'], snapshot_id=snapshot, storage_uri=rel,
                                     sha256=s['sha256'], coverage=s['coverage'], source_class=s['source_class']))
            eid = lambda key: p['id'] + '.' + key
            evidence = index(p['evidence'], 'evidence')
            for e in p['evidence']:
                self.put('evidence', dict(id=eid(e['id']), topic_id=topic['id'], source_snapshot_id=snapshot_ids[e['source_id']],
                         evidence_type=e['kind'], claim=e['claim'], excerpt=e['excerpt'], locator=e['locator'],
                         scope=topic['scope'], review_status=e['status'], created_at=p['created_at']))
                if e['review']:
                    self.put('evidence_review', dict(evidence_id=eid(e['id']), **e['review']))
            for m in p['metrics']:
                # Definitions are versioned within each package to retain exact methodology.
                mid = eid(m['id'])
                self.put('metric_definition', dict(id=mid, topic_id=topic['id'], name=m['name'], description=m['name'],
                         unit=m['unit'], frequency=m['frequency'], geography=m['geography'],
                         methodology=m['methodology'], version=p['id'], status='verified_extraction'))
                self.put('metric_observation', dict(id='observation.' + mid, metric_id=mid, period_start=m['period_start'],
                         period_end=m['period_end'], value_numeric=m['value'], source_snapshot_id=snapshot_ids[evidence[m['evidence_id']]['source_id']],
                         observed_at=p['created_at'], quality_status='verified_extraction'))
                self.put('metric_evidence', dict(observation_id='observation.' + mid, evidence_id=eid(m['evidence_id'])))
            for f in p['analysis']['factors']:
                self.put('factor_definition', dict(id=eid(f['id']), topic_id=topic['id'], name=f['name'],
                         description=f['name'], mechanism=f['mechanism'], scope=topic['scope'],
                         assessment_method='agent_draft_human_review_required', version=p['id'], status='draft'))
            for s in p['analysis']['scenarios']:
                self.put('scenario', dict(id=eid(s['id']), topic_id=topic['id'], name=s['name'], scenario_type=s['type'],
                         assumptions_json=json.dumps(s['assumptions'], ensure_ascii=False), path_json=json.dumps(s['factor_ids']),
                         observable_signals_json=json.dumps(s['signals'], ensure_ascii=False),
                         falsifiers_json=json.dumps(s['falsifiers'], ensure_ascii=False), version=p['id'], status='draft'))
            for edge in p['analysis']['causal_edges']:
                self.put('causal_edge', dict(id=eid(edge['id']), topic_id=topic['id'],
                         from_factor_id=eid(edge['from_factor_id']), outcome_name=edge['outcome'], sign=edge['sign'],
                         mechanism=edge['mechanism'], lag_description=edge['lag'], scope=edge['scope'],
                         evidence_ids_json=json.dumps([eid(e) for e in edge['evidence_ids']]),
                         status='hypothesis', version=p['id']))
            normalized = f'03-library/08-packages/{topic["slug"]}/{p["id"]}/package.json'
            catalog = {'package_id': p['id'], 'package_sha256': content_hash, 'sources': manifest}
            self.write(normalized, encoded(p), created)
            self.write(f'03-library/06-catalog/imports/{p["id"]}.json', encoded(catalog), created)
            self.put('processing_package', dict(id=p['id'], topic_id=topic['id'], content_hash=content_hash,
                     storage_uri=normalized, producer_json=json.dumps(p['producer'], ensure_ascii=False), imported_at=now()))
            from shared_library import register_package
            register_package(self, p, manifest)
            self.db.commit()
            return {'id': p['id'], 'status': 'imported', 'sources': len(manifest), 'metrics': len(p['metrics'])}
        except Exception:
            self.db.rollback()
            for file in reversed(created):
                file.unlink()
            raise

    def read_package(self, package_id):
        row = self.db.execute('SELECT * FROM processing_package WHERE id=?', (package_id,)).fetchone()
        require(row is not None, 'package not imported')
        p = load(artifact(self.root, row['storage_uri']))
        require(digest(encoded(p)) == row['content_hash'], 'normalized package tampered')
        catalog = load(artifact(self.root, f'03-library/06-catalog/imports/{package_id}.json'))
        require(catalog['package_sha256'] == row['content_hash'], 'catalog package mismatch')
        require(len(catalog['sources']) == len(p['sources']), 'catalog source count mismatch')
        for s in p['sources']:
            matches = [item for item in catalog['sources'] if item['source_id'] == s['id']]
            require(len(matches) == 1, 'catalog source mismatch')
            item = matches[0]
            dbs = self.db.execute('SELECT * FROM source_snapshot WHERE id=?', (item['snapshot_id'],)).fetchone()
            require(dbs is not None and dbs['source_id'] == s['id'] and dbs['content_hash'] == s['sha256'], 'snapshot metadata mismatch')
            require(item['storage_uri'] == dbs['storage_uri'], 'catalog path mismatch')
            require(digest(artifact(self.root, dbs['storage_uri']).read_bytes()) == s['sha256'], 'archived source tampered')
        return p, catalog

    def run(self, package_id):
        p, catalog = self.read_package(package_id)
        analysis = p['analysis']
        sources, evidence = index(p['sources'], 'source'), index(p['evidence'], 'evidence')
        problems = list(analysis['limitations'])
        verified_ids = []
        for e in p['evidence']:
            if e['status'] == 'verified':
                pub = sources[e['source_id']]['published_at']
                require(pub <= analysis['as_of_date'], f'look-ahead source: {e["id"]} published {pub}')
                verified_ids.append(e['id'])
        for m in p['metrics']:
            require(m['period_end'] <= analysis['as_of_date'], 'look-ahead metric period')
        require(verified_ids and p['metrics'], 'run requires verified evidence and metrics')
        pending = [e['id'] for e in p['evidence'] if e['status'] == 'pending']
        partial = [s['id'] for s in p['sources'] if s['coverage'] == 'partial']
        if pending:
            problems.append(f'{len(pending)} 条说法尚未核验，不得作为正式事实。')
        if partial:
            problems.append(f'{len(partial)} 个来源仅采集到部分内容。')
        model_files = {str(f.relative_to(CODE_ROOT)): digest(f.read_bytes())
                       for f in sorted((CODE_ROOT / '03-library/07-models/topics' / p['topic']['slug']).glob('*.yaml'))}
        require(model_files, 'topic model template missing')
        rule_hash = digest(Path(__file__).read_bytes() + (CODE_ROOT / '90-system/02-schemas/processing-package.schema.json').read_bytes()
                           + (CODE_ROOT / '90-system/01-db/schema.sql').read_bytes()
                           + (Path(__file__).parent / 'shared_library.py').read_bytes())
        model_hash = digest(encoded({'analysis': analysis, 'files': model_files}))
        run_id = f'run.{p["topic"]["slug"]}.{analysis["as_of_date"]}.{catalog["package_sha256"][:8]}.{model_hash[:8]}.{rule_hash[:8]}'
        existing = self.db.execute('SELECT * FROM run_snapshot WHERE id=?', (run_id,)).fetchone()
        if existing:
            self.read_run(run_id)
            return {'id': run_id, 'status': 'already_exists'}
        run = dict(id=run_id, package_id=package_id, topic_id=p['topic']['id'], run_at=now(),
                   as_of_date=analysis['as_of_date'], mode=analysis['mode'], status='pending_human_review',
                   question=analysis['question'], data_version=catalog['package_sha256'],
                   model_version=model_hash, model_files=model_files, rule_version=VERSION + ':' + rule_hash,
                   model_contents={name: (CODE_ROOT / name).read_text() for name in model_files},
                   sources=catalog['sources'], producer=p['producer'], evidence=p['evidence'], metrics=p['metrics'],
                   factors=analysis['factors'], scenarios=analysis['scenarios'], causal_edges=analysis['causal_edges'], analysis=analysis,
                   verified_evidence_ids=verified_ids, pending_evidence_ids=pending, limitations=problems,
                   gates=[{'name':'source_integrity','status':'passed'}, {'name':'publication_cutoff','status':'passed'},
                          {'name':'factor_drafts','status':'prepared'}, {'name':'competing_scenarios','status':'prepared'},
                          {'name':'human_review','status':'pending'}, {'name':'investment_publication','status':'blocked'}],
                   judgment={'kind':'research_draft','text':'历史指标核验及条件性机制整理；不据此发布当前房价方向或资产行动。'},
                   action={'kind':'research_only','next_review_date':analysis['next_review_date'],
                           'next_steps':['人工核对因子与情景','补齐待核验说法的原始来源','用独立结果数据做后续复盘']})
        created = []
        try:
            self.db.execute('BEGIN IMMEDIATE')
            self.write(f'05-runs/{run_id}.json', encoded(run), created)
            report = render_run(run)
            self.write(f'05-runs/{run_id}.md', report.encode(), created)
            judgment = dict(run['judgment'], artifact_sha256=digest(encoded(run)), report_sha256=digest(report.encode()))
            self.put('run_snapshot', dict(id=run_id, topic_id=p['topic']['id'], run_at=run['run_at'],
                     as_of_date=run['as_of_date'], data_version=run['data_version'], model_version=model_hash,
                     rule_version=run['rule_version'], factor_states_json=json.dumps(run['factors'], ensure_ascii=False),
                     scenarios_json=json.dumps(run['scenarios'], ensure_ascii=False), judgment_json=json.dumps(judgment, ensure_ascii=False),
                     action_json=json.dumps(run['action'], ensure_ascii=False), status=run['status']))
            for f in run['factors']:
                self.put('factor_state', dict(id=run_id + '.' + f['id'], factor_id=p['id'] + '.' + f['id'],
                         as_of_date=run['as_of_date'], direction=f['direction'], confidence=f['confidence'],
                         evidence_ids_json=json.dumps([p['id'] + '.' + e for e in f['evidence_ids']]),
                         reversal_conditions=f['reversal_conditions'], assessment_method='agent_draft_human_review_required',
                         assessment_version=model_hash, created_at=run['run_at']))
            self.db.commit()
        except Exception:
            self.db.rollback()
            for file in reversed(created):
                file.unlink()
            raise
        return {'id': run_id, 'status': run['status'], 'report': str(self.root / f'05-runs/{run_id}.md')}

    def read_run(self, run_id):
        require(re.fullmatch(r'[a-z0-9][a-z0-9._-]*', run_id), 'invalid run ID')
        row = self.db.execute('SELECT * FROM run_snapshot WHERE id=?', (run_id,)).fetchone()
        require(row is not None, 'unknown run')
        run = load(artifact(self.root, f'05-runs/{run_id}.json'))
        metadata = json.loads(row['judgment_json'])
        require(digest(encoded(run)) == metadata['artifact_sha256'], 'run artifact tampered')
        report = artifact(self.root, f'05-runs/{run_id}.md').read_bytes()
        require(digest(report) == metadata['report_sha256'], 'run report tampered')
        self.read_package(run['package_id'])
        return run

    def review(self, run_id):
        run = self.read_run(run_id)
        review_id = 'review.' + run_id + '.data-audit-v1'
        if self.db.execute('SELECT 1 FROM review WHERE id=?', (review_id,)).fetchone():
            saved = load(artifact(self.root, f'06-reviews/{review_id}.json'))
            row = self.db.execute('SELECT outcome_json FROM review WHERE id=?', (review_id,)).fetchone()
            metadata = json.loads(row['outcome_json'])
            require(digest(encoded(saved)) == metadata['artifact_sha256'], 'review artifact tampered')
            require(digest(artifact(self.root, f'06-reviews/{review_id}.md').read_bytes()) == metadata['report_sha256'], 'review report tampered')
            return {'id': review_id, 'status': 'already_exists'}
        audit = dict(id=review_id, run_id=run_id, reviewed_at=now(), review_kind='data_and_process_audit',
                     outcome_status='not_evaluated', prediction_accuracy=None,
                     findings=['归档来源和运行快照哈希校验通过。',
                               '本次是数据与流程复盘，未验证未来市场结果；不能记为预测成功。'] + run['limitations'],
                     revision_actions=run['action']['next_steps'])
        report = '# 首轮数据与流程复盘\n\n' + f'运行：{run_id}\n\n市场结果：未验证。\n\n' + '\n'.join('- ' + x for x in audit['findings']) + '\n'
        created = []
        try:
            self.db.execute('BEGIN IMMEDIATE')
            self.write(f'06-reviews/{review_id}.json', encoded(audit), created)
            self.write(f'06-reviews/{review_id}.md', report.encode(), created)
            self.put('review', dict(id=review_id, run_snapshot_id=run_id, reviewed_at=audit['reviewed_at'],
                     outcome_json=json.dumps({'status':'not_evaluated','artifact_sha256':digest(encoded(audit)),
                                              'report_sha256':digest(report.encode())}), error_class='data',
                     findings=json.dumps(audit['findings'], ensure_ascii=False),
                     revision_actions_json=json.dumps(audit['revision_actions'], ensure_ascii=False)))
            self.db.commit()
        except Exception:
            self.db.rollback()
            for file in reversed(created):
                file.unlink()
            raise
        return {'id': review_id, 'status': 'data_audit_completed', 'market_outcome': 'not_evaluated'}

    def status(self):
        tables = ['source', 'source_snapshot', 'processing_package', 'evidence', 'metric_observation', 'factor_state', 'causal_edge', 'scenario', 'run_snapshot', 'review']
        return {t: self.db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in tables}


def render_run(run):
    out = ['# 立党专题：首轮研究快照' if 'real-estate' in run['topic_id'] else '# 研究快照', '',
           f'运行 ID：`{run["id"]}`', '', f'研究问题：{run["question"]}', '',
           f'数据截止：{run["as_of_date"]}；状态：待人工审核；模式：{run["mode"]}。', '',
           '## 已核对的指标', '', '| 指标 | 期间 | 值 | 单位 | 证据 |', '|---|---|---:|---|---|']
    for m in run['metrics']:
        out.append(f'| {m["name"]} | {m["period_start"]} 至 {m["period_end"]} | {m["value"]} | {m["unit"]} | {m["evidence_id"]} |')
    out += ['', '## 因子解释（草稿）', '']
    for f in run['factors']:
        out += [f'### {f["name"]}', '', f'{f["mechanism"]}', '', f'状态：{f["direction"]}；置信度：{f["confidence"]}。', '',
                '反转条件：' + f['reversal_conditions'], '']
    out += ['## 因果机制（待检验假设）', '']
    for edge in run['causal_edges']:
        out += [f'- {edge["from_factor_id"]} → {edge["outcome"]}：{edge["mechanism"]}；时滞：{edge["lag"]}；反证：{edge["falsifier"]}', '']
    out += ['## 条件性情景（草稿）', '']
    for s in run['scenarios']:
        out += [f'### {s["name"]}', '', '条件：' + '；'.join(s['assumptions']), '',
                '观察：' + '；'.join(s['signals']), '', '反证：' + '；'.join(s['falsifiers']), '']
    out += ['## 审核缺口', ''] + ['- ' + x for x in run['limitations']]
    out += ['', '## 来源与复查入口', '']
    for s in run['sources']:
        current_uri = str(artifact(CODE_ROOT, s['storage_uri']).relative_to(CODE_ROOT))
        out.append(f'- [{s["source_id"]}](../{current_uri})（{s["source_class"]}，{s["coverage"]}）')
    out += ['', '## 下一步', ''] + ['- ' + x for x in run['action']['next_steps']]
    out += ['', '本轮只完成研究整理与数据核验，尚未发布投资判断；复盘不能替代未来结果验证。', '']
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=CODE_ROOT, help='artifact/database root')
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['validate', 'import']:
        sub.add_parser(command).add_argument('package', type=Path)
    sub.add_parser('run').add_argument('package_id')
    sub.add_parser('review').add_argument('run_id')
    sub.add_parser('status')
    sub.add_parser('library', help='rebuild shared object indexes and reading views')
    args = parser.parse_args()
    store = None
    try:
        if args.command == 'validate':
            p, _ = validate(args.package)
            result = {'id':p['id'], 'status':'valid', 'sources':len(p['sources']), 'evidence':len(p['evidence']), 'metrics':len(p['metrics'])}
        else:
            store = Store(args.root)
            if args.command == 'import':
                result = store.import_package(args.package)
            elif args.command == 'run':
                result = store.run(args.package_id)
            elif args.command == 'review':
                result = store.review(args.run_id)
            elif args.command == 'library':
                from shared_library import rebuild
                result = rebuild(store)
            else:
                result = store.status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(json.dumps({'status':'error','message':str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    finally:
        if store:
            store.db.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
