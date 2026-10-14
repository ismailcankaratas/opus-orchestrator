import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'plugins/opus-orchestrator/scripts/validate_plan.py'
SPEC = importlib.util.spec_from_file_location('validate_plan', SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def valid():
    return json.loads((ROOT/'plugins/opus-orchestrator/examples/plan.example.json').read_text())


class PlanValidationTests(unittest.TestCase):
    def test_valid_example(self):
        self.assertEqual(MOD.validate_plan(valid()), [])

    def test_duplicate_ids(self):
        plan=valid()
        plan['tasks'][1]['id']=plan['tasks'][0]['id']
        self.assertTrue(any('duplicate' in e for e in MOD.validate_plan(plan)))

    def test_missing_dependency(self):
        plan=valid()
        plan['tasks'][1]['depends_on']=['MISSING']
        self.assertTrue(any('missing dependency' in e for e in MOD.validate_plan(plan)))

    def test_self_dependency(self):
        plan=valid()
        plan['tasks'][1]['depends_on']=['T02']
        self.assertTrue(any('cannot depend on itself' in e for e in MOD.validate_plan(plan)))

    def test_dependency_cycle(self):
        plan=valid()
        plan['tasks'][0]['depends_on']=['T04']
        self.assertTrue(any('cycle' in e.lower() for e in MOD.validate_plan(plan)))

    def test_overlapping_file_ownership(self):
        plan=valid()
        plan['tasks'][2]['files_owned']=['apps/web/src/pages/settings/index.tsx']
        self.assertTrue(any('overlaps' in e for e in MOD.validate_plan(plan)))

    def test_identical_file_ownership(self):
        plan=valid()
        plan['tasks'][1]['files_owned']=['apps/api/test/settings.test.ts']
        self.assertTrue(any('overlaps' in e for e in MOD.validate_plan(plan)))

    def test_dependencies_cannot_share_parallel_group(self):
        plan=valid()
        plan['tasks'][2]['depends_on']=['T02']
        self.assertTrue(any('same parallel group' in e for e in MOD.validate_plan(plan)))

    def test_paths_must_be_relative(self):
        plan=valid()
        plan['tasks'][1]['files_owned']=['../secrets.env']
        self.assertTrue(any('invalid path' in e for e in MOD.validate_plan(plan)))

    def test_high_risk_requires_user_approval(self):
        plan=valid()
        plan['tasks'][1]['risk']='high'
        plan['tasks'][1]['approval_required']=False
        self.assertTrue(any('must require approval' in e for e in MOD.validate_plan(plan)))

    def test_read_only_agent_tasks_can_have_no_paths(self):
        plan=valid()
        self.assertEqual(MOD.validate_plan(plan), [])
        self.assertEqual(plan['tasks'][0]['files_owned'], [])

    def test_empty_plan(self):
        self.assertTrue(MOD.validate_plan({'goal':'x','tasks':[]}))

    def test_malformed_plan_not_crash(self):
        plan=valid()
        plan['tasks'][0]['depends_on']=None
        plan['tasks'][1]['files_owned']=None
        errs=MOD.validate_plan(plan)
        self.assertTrue(errs)

    def test_disjoint_parallel_dir_ownership(self):
        plan=valid()
        self.assertEqual(MOD.validate_plan(plan), [])


if __name__=='__main__':
    unittest.main()
