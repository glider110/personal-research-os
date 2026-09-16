"""Cross-topic identity, revision, conflict and migration behavior."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '90-system/03-scripts'))
import test_research as base
from shared_library import rebuild


class SharedLibraryTests(unittest.TestCase):
    setUp = base.PipelineTests.setUp
    tearDown = base.PipelineTests.tearDown
    save = base.PipelineTests.save
    def other_topic(self):
        self.p['id'] = 'package.other.v1'
        self.p['topic'] = dict(id='topic.consumption', slug='consumption', name='消费', scope='测试范围')
        self.save()
        self.store.import_package(self.path)

    def test_shared_definition_across_topics_preserves_usages(self):
        self.store.import_package(self.path)
        self.other_topic()
        db = self.store.db
        self.assertEqual(db.execute("SELECT count(*) FROM shared_object WHERE kind='metric'").fetchone()[0],1)
        self.assertEqual(db.execute("SELECT count(*) FROM shared_object WHERE kind='factor'").fetchone()[0],1)
        self.assertEqual(db.execute("SELECT count(DISTINCT topic_id) FROM shared_usage WHERE kind='metric'").fetchone()[0],2)
        self.assertEqual(len(list((self.root/'02-sources').rglob('source.txt'))),1)
        rebuild(self.store)
        self.assertTrue((self.root/'04-research/consumption.md').exists())

    def test_same_name_different_methodology_is_not_merged(self):
        self.store.import_package(self.path)
        self.p['metrics'][0]['methodology'] = 'different population'
        self.other_topic()
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM shared_object WHERE kind='metric'").fetchone()[0],2)

    def test_explicit_identity_preserves_definition_versions(self):
        self.p['metrics'][0]['shared_id']='shared.income'
        self.save()
        self.store.import_package(self.path)
        self.p['metrics'][0]['methodology']='revised definition'
        self.other_topic()
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM shared_revision WHERE object_id='shared.income'").fetchone()[0],2)

    def test_cross_kind_identity_conflict_rolls_back_package(self):
        self.p['metrics'][0]['shared_id']='shared.collision'
        self.p['analysis']['factors'][0]['shared_id']='shared.collision'
        self.save()
        with self.assertRaisesRegex(ValueError,'another object kind'):
            self.store.import_package(self.path)
        self.assertEqual(self.store.status()['processing_package'],0)
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM shared_object').fetchone()[0],0)
        self.assertEqual(list((self.root/'02-sources').rglob('*.txt')),[])

    def test_support_and_refutation_are_explicit_and_versioned(self):
        self.store.import_package(self.path)
        db=self.store.db
        ev=db.execute("SELECT revision_id FROM shared_usage WHERE kind='evidence'").fetchone()[0]
        factor=db.execute("SELECT revision_id FROM shared_usage WHERE kind='factor'").fetchone()[0]
        folder=self.root/'03-library/05-relations/assertions'
        folder.mkdir(parents=True)
        d=dict(id='assertion.test.v1',from_revision=ev,relation='supports',to_revision=factor,status='pending',rationale='synthetic claim')
        first=folder/'support.json'
        first.write_text(json.dumps(d))
        d.update(id='assertion.test.v2',relation='refutes')
        (folder/'refute.json').write_text(json.dumps(d))
        rebuild(self.store)
        text=(self.root/'04-research/01-pending.md').read_text()
        self.assertIn('同时存在支持与反驳',text)
        self.assertIn(factor,text)
        self.assertEqual(db.execute("SELECT review_status FROM evidence").fetchone()[0],'verified')
        d.update(id='assertion.test.v1',rationale='changed')
        first.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'reused with different content'):
            rebuild(self.store)

    def test_same_period_conflicting_values_are_visible(self):
        self.store.import_package(self.path)
        self.p['id']='package.test.v2'
        self.p['sources'][0]['sha256']=__import__('hashlib').sha256(b'value 20\n').hexdigest()
        (self.input/'source.txt').write_bytes(b'value 20\n')
        self.p['evidence'][0]['excerpt']='value 20'
        self.p['evidence'][0]['claim']='value is 20'
        self.p['metrics'][0].update(value=20,value_text='20')
        self.save()
        self.store.import_package(self.path)
        rebuild(self.store)
        text=(self.root/'04-research/01-pending.md').read_text()
        self.assertIn('10，批次 package.test.v1',text)
        self.assertIn('20，批次 package.test.v2',text)

    def test_changed_assessment_keeps_shared_factor_definition(self):
        self.store.import_package(self.path)
        self.p['analysis']['factors'][0]['confidence']='high'
        self.other_topic()
        db=self.store.db
        self.assertEqual(db.execute("SELECT count(*) FROM shared_object WHERE kind='factor'").fetchone()[0],1)
        self.assertEqual(db.execute("SELECT count(*) FROM shared_usage WHERE kind='factor'").fetchone()[0],2)

    def test_legacy_path_resolution(self):
        from test_research import r
        self.assertEqual(r.artifact(self.root,'raw/a/b.txt'),self.root.resolve()/'02-sources/a/b.txt')
        self.assertEqual(r.artifact(self.root,'data/normalized/a/package.json'),self.root.resolve()/'03-library/08-packages/a/package.json')
        with self.assertRaisesRegex(ValueError,'unsafe path'):
            r.artifact(self.root,'raw/../secret.txt')


if __name__ == '__main__':
    unittest.main()
