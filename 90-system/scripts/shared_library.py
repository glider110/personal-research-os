"""Shared, versioned identities and reproducible human-readable research views."""
import hashlib
import json


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


def rebuild(store):
    packages = []
    # Verify ALL packages and archived inputs before touching shared records/views.
    for row in store.db.execute('SELECT id FROM processing_package ORDER BY id').fetchall():
        p, catalog = store.read_package(row['id'])
        if p['schema_version'] == '2.0':
            from distillation import validate_features
            validate_features(p)
        packages.append((p, catalog))
    with store.db:
        for p, catalog in packages:
            register_package(store, p, catalog['sources'])
    from distillation import render
    render(store, packages)
    return {'status': 'rebuilt', 'objects': store.db.execute('SELECT count(*) FROM shared_object').fetchone()[0],
            'revisions': store.db.execute('SELECT count(*) FROM shared_revision').fetchone()[0],
            'usages': store.db.execute('SELECT count(*) FROM shared_usage').fetchone()[0],
            'entry': str(store.root / 'README.md')}
