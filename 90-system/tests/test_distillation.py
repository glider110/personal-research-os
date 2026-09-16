"""Protect the simpler workflow, historical observations and cross-topic reuse."""
import copy
import subprocess
import sys
import unittest
import test_research as base
from shared_library import rebuild


def simplify(p):
    p['schema_version']='2.0'
    p['analysis']={k:v for k,v in p['analysis'].items() if k in ('question','as_of_date','mode','factors','limitations')}
    for f in p['analysis']['factors']:
        for k in ('direction','confidence','reversal_conditions'): f.pop(k, None)
        f.update(selection_reason='merge repeated information',independence_note='not statistically verified')
    for m in p['metrics']:
        m['features']=dict(relevance='test topic', timing=dict(type='unknown',relative_to='test outcome',rationale='insufficient observations'),popularity=dict(type='unknown',rationale='not measured'),corroborating=[],counter=[],gaps=[])
    return p


class DistillationTests(unittest.TestCase):
    setUp=base.PipelineTests.setUp
    tearDown=base.PipelineTests.tearDown
    save=base.PipelineTests.save

    def test_one_command_accepts_metrics_without_factors_and_no_run(self):
        simplify(self.p)['analysis']['factors']=[]
        self.save()
        command=[sys.executable,str(base.r.CODE_ROOT/'90-system/scripts/research.py'),'--root',str(self.root),'distill',str(self.path)]
        for _ in range(2):
            result=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(self.store.status()['processing_package'],1)
        self.assertEqual(self.store.status()['run_snapshot'],0)
        self.assertIn('暂不提炼因子',(self.root/'04-research/real-estate.md').read_text())
        self.assertFalse(hasattr(self.store, 'run'))

    def test_duplicate_imports_do_not_duplicate_observations_but_keep_periods(self):
        simplify(self.p);self.save();self.store.import_package(self.path)
        self.p['id']='package.test.v2';self.save();self.store.import_package(self.path)
        self.p['id']='package.test.v3'
        self.p['metrics'][0]['period_start']='2020-01-01'
        self.p['metrics'][0]['period_end']='2020-12-31'
        self.save();self.store.import_package(self.path);rebuild(self.store)
        text=(self.root/'03-library/metrics.md').read_text()
        self.assertEqual(text.count('2021-01-01～2021-12-31'),1)
        self.assertEqual(text.count('2020-01-01～2020-12-31'),1)
        self.assertEqual(self.store.status()['processing_package'],3)

    def test_shared_observation_still_appears_in_both_topics(self):
        simplify(self.p);self.save();self.store.import_package(self.path)
        self.p['id']='package.other.v1'
        self.p['topic']=dict(id='topic.other',slug='other',name='Other',scope='测试范围')
        self.save();self.store.import_package(self.path);rebuild(self.store)
        for slug in ('real-estate','other'):
            text=(self.root/f'04-research/{slug}.md').read_text()
            self.assertIn('10 unit',text)
        text=(self.root/'03-library/metrics.md').read_text()
        self.assertEqual(text.count('2021-01-01～2021-12-31'),1)

    def test_unknown_relation_or_future_data_rejected(self):
        simplify(self.p)
        self.p['metrics'][0]['features']['counter']=[dict(metric_id='absent',claim='claim',rationale='reason')]
        self.save()
        with self.assertRaisesRegex(ValueError,'feature metric'): base.r.validate(self.path)
        self.p['metrics'][0]['features']['counter']=[]
        self.p['analysis']['as_of_date']='2021-12-31';self.save()
        with self.assertRaisesRegex(ValueError,'as-of'): base.r.validate(self.path)

    def test_simple_contract_does_not_require_or_accept_scenarios(self):
        simplify(self.p);self.save();base.r.validate(self.path)
        self.p['analysis']['scenarios']=[];self.save()
        with self.assertRaisesRegex(ValueError,'unknown fields'):base.r.validate(self.path)

    def test_same_information_group_cannot_count_level_and_growth_twice(self):
        simplify(self.p)
        m=self.p['metrics'][0]
        m['features']['information_group']='same.measurement'
        other=copy.deepcopy(m);other['id']='metric.derived'
        self.p['metrics'].append(other)
        self.p['analysis']['factors'][0]['metric_ids'].append(other['id'])
        self.save()
        with self.assertRaisesRegex(ValueError,'redundant factor representatives'):
            base.r.validate(self.path)
        f=self.p['analysis']['factors'][0]
        f['metric_ids'].remove(other['id'])
        f['excluded_metrics']=[dict(metric_id=other['id'],reason='same information')]
        self.save();base.r.validate(self.path)

    def test_filter_cannot_hide_an_included_metric_as_excluded(self):
        simplify(self.p)
        self.p['analysis']['factors'][0]['excluded_metrics']=[dict(metric_id='metric.test',reason='duplicate')]
        self.save()
        with self.assertRaisesRegex(ValueError,'sets overlap'):base.r.validate(self.path)

    def test_rendering_does_not_modify_archived_sources_or_packages(self):
        simplify(self.p);self.save();self.store.import_package(self.path)
        paths=list((self.root/'02-sources').rglob('*.txt'))+list((self.root/'90-system/packages').rglob('*.json'))
        hashes={p:base.r.digest(p.read_bytes()) for p in paths}
        rebuild(self.store)
        self.assertEqual(hashes,{p:base.r.digest(p.read_bytes()) for p in paths})


if __name__=='__main__': unittest.main()
