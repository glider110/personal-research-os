"""Behavioral checks for provenance, append-only storage and time boundaries."""
import copy
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "90-system/scripts"))

spec = importlib.util.spec_from_file_location('research', Path(__file__).resolve().parents[2] / '90-system/scripts/research.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def example():
    p = dict(schema_version='1.0', id='package.test.v1',
        topic=dict(id='topic.real-estate',slug='real-estate',name='测试主题',scope='测试范围'),
        created_at='2026-09-16T00:00:00+00:00',
        producer=dict(tool='test',model='none',prompt_version='test-v1',method='synthetic fixture; not market data'),
        sources=[dict(id='source.test',title='Synthetic',source_class='primary',type='txt',original_type='txt',
            canonical_uri='local:fixture',publisher='Test fixture',published_at='2022-01-17',
            captured_at='2026-09-16T00:00:00+00:00',file='source.txt',sha256=r.digest(b'value 10\n'),coverage='full',capture_method='fixture')],
        evidence=[dict(id='evidence.test',source_id='source.test',kind='fact',claim='value is 10',excerpt='value 10',
            locator='source.txt:L1',status='verified',review=dict(reviewer='test',reviewed_at='2026-09-16T00:00:00+00:00',method='fixture'))],
        metrics=[dict(id='metric.test',name='test',unit='unit',frequency='annual',geography='test',methodology='identity',
            period_start='2021-01-01',period_end='2021-12-31',value=10,value_text='10',value_transform='identity',evidence_id='evidence.test')],
        analysis=dict(question='Test?',as_of_date='2022-01-17',mode='historical_reconstruction',
            factors=[dict(id='factor.test',name='factor',mechanism='test only',direction='unknown',confidence='low',
                evidence_ids=['evidence.test'],metric_ids=['metric.test'],reversal_conditions='new evidence')],
            causal_edges=[dict(id='edge.test',from_factor_id='factor.test',outcome='test outcome',sign='conditional',
                mechanism='test hypothesis',lag='unknown',scope='test',evidence_ids=['evidence.test'],falsifier='opposite',status='hypothesis')],
            scenarios=[dict(id='scenario.test',name='test',type='base',assumptions=['test'],signals=['test'],falsifiers=['test'],factor_ids=['factor.test'])],
            limitations=['synthetic fixture'],next_review_date='2026-10-16'))

    p['schema_version']='2.0'
    p['analysis']={k:v for k,v in p['analysis'].items() if k in ('question','as_of_date','mode','factors','limitations')}
    for f in p['analysis']['factors']:
        for k in ('direction','confidence','reversal_conditions'): f.pop(k)
        f.update(selection_reason='merge redundant information',independence_note='not verified')
    p['metrics'][0]['features']=dict(relevance='test',timing=dict(type='unknown',relative_to='test',rationale='unknown'),popularity=dict(type='unknown',rationale='unknown'),corroborating=[],counter=[],gaps=[])
    return p


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.input = self.root / 'incoming'
        self.input.mkdir()
        (self.input / 'source.txt').write_bytes(b'value 10\n')
        self.p = example()
        self.path = self.input / 'package.json'
        self.save()
        self.store = r.Store(self.root)

    def tearDown(self):
        self.store.db.close()
        self.tmp.cleanup()

    def save(self):
        self.path.write_bytes(r.encoded(self.p))


    def test_import_is_idempotent_and_detects_archive_tampering(self):
        self.store.import_package(self.path)
        counts=self.store.status()
        self.assertEqual(self.store.import_package(self.path)['status'],'already_imported')
        self.assertEqual(self.store.status(),counts)
        _,catalog=self.store.read_package(self.p['id'])
        (self.root/catalog['sources'][0]['storage_uri']).write_text('changed')
        with self.assertRaisesRegex(ValueError,'archived source tampered'):
            self.store.read_package(self.p['id'])

    def test_snapshot_updates_and_deletes_blocked(self):
        self.store.import_package(self.path)
        for sql in ["UPDATE source_snapshot SET content_hash='changed'", 'DELETE FROM source_snapshot']:
            with self.assertRaises(sqlite3.IntegrityError):self.store.db.execute(sql)
            self.store.db.rollback()

    def test_hash_mismatch_prevents_all_inserts(self):
        (self.input / 'source.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.store.import_package(self.path)
        self.assertEqual(self.store.status()['source'], 0)
        self.assertFalse((self.root / '02-sources').exists())

    def test_ai_output_cannot_be_verified_fact(self):
        self.p['sources'][0]['source_class'] = 'ai_generated'
        self.save()
        with self.assertRaisesRegex(ValueError, 'AI/claim'):
            self.store.import_package(self.path)

    def test_pending_evidence_cannot_feed_metrics(self):
        self.p['evidence'][0]['status'] = 'pending'
        self.save()
        with self.assertRaisesRegex(ValueError, 'unverified'):
            r.validate(self.path)

    def test_metric_value_must_match_quoted_number(self):
        self.p['metrics'][0]['value'] = 100
        self.save()
        with self.assertRaisesRegex(ValueError, 'conversion mismatch'):
            r.validate(self.path)

    def test_duplicate_id_and_broken_reference_are_rejected(self):
        original = copy.deepcopy(self.p)
        self.p['sources'].append(copy.deepcopy(self.p['sources'][0]))
        self.save()
        with self.assertRaisesRegex(ValueError, 'duplicate source'):
            r.validate(self.path)
        self.p = original
        self.p['analysis']['factors'][0]['metric_ids'] = ['missing']
        self.save()
        with self.assertRaisesRegex(ValueError, 'unknown factor metrics'):
            r.validate(self.path)

    def test_paths_and_symlink_escape_are_rejected(self):
        self.p['sources'][0]['file'] = '../outside.txt'
        self.save()
        with self.assertRaisesRegex(ValueError, 'unsafe path'):
            r.validate(self.path)
        outside = self.root / 'outside.txt'
        outside.write_bytes(b'value 10\n')
        (self.input / 'link.txt').symlink_to(outside)
        self.p['sources'][0]['file'] = 'link.txt'
        self.save()
        with self.assertRaisesRegex(ValueError, 'escapes root'):
            r.validate(self.path)

    def test_same_id_different_content_cannot_overwrite(self):
        self.store.import_package(self.path)
        self.p['analysis']['question'] = 'changed question'
        self.save()
        with self.assertRaisesRegex(ValueError, 'reused'):
            self.store.import_package(self.path)
        p, _ = self.store.read_package(self.p['id'])
        self.assertEqual(p['analysis']['question'], 'Test?')




    def test_failed_import_rolls_back_database_and_new_files(self):
        original = self.store.put
        def fail(table, values):
            if table == 'metric_definition':
                raise ValueError('injected failure')
            original(table, values)
        self.store.put = fail
        with self.assertRaisesRegex(ValueError, 'injected failure'):
            self.store.import_package(self.path)
        self.assertEqual(self.store.status()['source'], 0)
        self.assertEqual(list((self.root / '02-sources').rglob('*.txt')), [])
        self.store.put = original
        self.store.import_package(self.path)

    def test_invalid_schema_does_not_enter_database(self):
        self.p['metrics'][0]['value'] = True
        self.save()
        with self.assertRaisesRegex(ValueError, 'wrong type'):
            self.store.import_package(self.path)
        self.p['metrics'][0]['value'] = 10
        self.p['analysis']['as_of_date'] = '2026-02-30'
        self.save()
        with self.assertRaises(ValueError):
            self.store.import_package(self.path)
        self.assertEqual(self.store.status()['source'], 0)


if __name__ == '__main__':
    unittest.main()
