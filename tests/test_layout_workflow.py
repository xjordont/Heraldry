"""Exercise local workflow ordering and failure handling without building a book."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import layout_workflow as workflow
import build_extras


class LocalWorkflow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.receipt = {'status': 'RUNNING', 'stages': []}

    def tearDown(self):
        self.tmp.cleanup()

    def test_local_extras_preserve_last_delivery_instructions(self):
        (self.root / 'docs').mkdir()
        (self.root / 'docs/PRINT_INSTRUCTIONS_TEMPLATE.md').write_text('Proof {{VERSION}}')
        (self.root / 'dist').mkdir()
        delivered = self.root / 'dist/PRINT_INSTRUCTIONS.md'
        delivered.write_text('Historical delivery')
        proof = self.root / 'proof/PRINT_INSTRUCTIONS.md'
        with patch.object(build_extras, 'ROOT', self.root), \
             patch.object(build_extras, 'version', return_value='RC-test'), \
             patch.object(build_extras, 'cover_data', return_value={'title': 'Test', 'version': 'RC-test'}), \
             patch.object(build_extras, 'compile_doc') as compile_doc, \
             patch.object(sys, 'argv', ['build_extras.py', '--instructions-output', str(proof)]):
            build_extras.main()
        self.assertEqual(proof.read_text(), 'Proof RC-test')
        self.assertEqual(delivered.read_text(), 'Historical delivery')
        self.assertEqual(compile_doc.call_count, 3)

    def test_existing_lock_is_preserved_and_no_stages_run(self):
        (self.root / 'build').mkdir()
        lock = self.root / 'build/layout-workflow.lock'
        lock.write_text('Another active run')
        with patch.object(workflow, 'check_source', return_value={'path': 'source', 'sha256': 'hash'}), \
             patch.object(workflow, 'execute_groups') as execute:
            self.assertEqual(workflow.run_local('check', self.root), 1)
        execute.assert_not_called()
        self.assertEqual(lock.read_text(), 'Another active run')

    def test_freeze_binds_generated_model_index_and_cover_but_allows_composition(self):
        (self.root / 'build').mkdir()
        (self.root / 'typst').mkdir()
        for name in workflow.GENERATED_INPUTS:
            path = self.root / name
            path.write_text('{}')
            before = workflow.fingerprint(self.root)
            path.write_text('{"changed":true}')
            self.assertNotEqual(before, workflow.fingerprint(self.root))
        before = workflow.fingerprint(self.root)
        (self.root / 'typst/content.typ').write_text('Generated composition')
        (self.root / 'typst/measure.typ').write_text('Generated probe')
        self.assertEqual(before, workflow.fingerprint(self.root))

    def execute(self, groups, executor, frozen=None):
        workflow.execute_groups(groups, self.root, self.root, self.receipt,
                                executor=executor, frozen=frozen)

    def test_failure_never_runs_dependent_variants_or_review(self):
        seen = []
        report = self.root / 'layout.json'
        report.write_text(json.dumps({'pdf':'old.pdf', 'pages':1, 'counts':{}, 'flags':[], 'flagged_pages':[]}))
        def fail(command, **_):
            seen.append(command[1])
            # A successful exit without a fresh report cannot reuse old output.
            self.assertFalse(report.exists())
            return subprocess.CompletedProcess(command, 0)
        groups = [[workflow.Stage('layout', ('layout',), report, 'layout')],
                  [workflow.Stage('variants', ('variants',))],
                  [workflow.Stage('review', ('review',))]]
        with self.assertRaisesRegex(ValueError, 'layout'):
            self.execute(groups, fail)
        self.assertEqual(seen, ['layout'])
        self.assertEqual(self.receipt['stages'][0]['status'], 'FAIL')
        self.assertTrue((self.root / 'run.json').exists())

    def test_flags_block_success_even_with_zero_exit(self):
        report = self.root / 'layout.json'
        def flagged(command, **_):
            report.write_text(json.dumps({'pdf':'proof.pdf','pages':2,
                'counts':{'near_empty':1},'flags':[{'page':2}],'flagged_pages':[2]}))
            return subprocess.CompletedProcess(command, 0)
        with self.assertRaisesRegex(ValueError, 'failed'):
            self.execute([[workflow.Stage('layout', ('layout',), report, 'layout')]], flagged)

    def test_independent_checks_finish_before_next_batch_and_reports_are_hashed(self):
        seen = []
        reports = {s: self.root / (s + '.json') for s in ('keeps', 'page-map')}
        def successful(command, **_):
            name = command[1]
            if name == 'variants':
                self.assertCountEqual(seen, ['keeps', 'page-map'])
            seen.append(name)
            if name in reports:
                reports[name].write_text('{"status":"PASS"}')
            return subprocess.CompletedProcess(command, 0)
        groups = [[workflow.Stage(n,(n,),p) for n,p in reports.items()],
                  [workflow.Stage('variants',('variants',))]]
        self.execute(groups, successful)
        self.assertEqual(seen[-1], 'variants')
        self.assertEqual(len(self.receipt['stages'][0]['report_sha256']), 64)

    def test_input_change_during_stage_prevents_following_stage(self):
        def success(command, **_):
            return subprocess.CompletedProcess(command, 0)
        with patch.object(workflow, 'fingerprint', side_effect=['before', 'after']):
            with self.assertRaisesRegex(ValueError, 'changed during'):
                self.execute([[workflow.Stage('cream',('cream',))],
                              [workflow.Stage('variants',('variants',))]], success, frozen='before')
        self.assertEqual(len(self.receipt['stages']), 1)

    def test_updated_manuscript_cannot_use_stale_parsed_model(self):
        (self.root / 'build').mkdir()
        (self.root / 'build/blocks.json').write_text('{"sha256":"old","source":"source/Old.md"}')
        with self.assertRaisesRegex(ValueError, 'stale'):
            workflow.assert_model_current(self.root, {'sha256':'new','path':'source/New.md'})
        workflow.assert_model_current(self.root, {'sha256':'old','path':'source/Old.md'})

    def test_plan_dependency_order_keeps_expensive_work_after_cream_checks(self):
        groups = workflow.stage_groups(self.root)
        batch_of = {s.name:i for i,g in enumerate(groups) for s in g}
        self.assertLess(batch_of['parse'], batch_of['cream'])
        self.assertLess(batch_of['figure-currency'], batch_of['cream'])
        for name in ('keeps','page-map','reconciliation','layout','inkjet-cream'):
            self.assertLess(batch_of[name], batch_of['variants'])
        self.assertLess(batch_of['variants'], batch_of['companion-geometry'])
        extras = next(s for g in groups for s in g if s.name == 'extras')
        self.assertIn(str(self.root / 'PRINT_INSTRUCTIONS.md'), extras.args)
        self.assertNotIn('tools/make_fonts.py', [s.args[0] for g in groups for s in g])

    def test_developer_front_door_plan_is_read_only(self):
        result = subprocess.run([sys.executable, str(ROOT/'tools/dev.py'), 'layout', 'plan'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Read-only plan', result.stdout)
        self.assertIn('source/Heraldry_RC', result.stdout)


if __name__ == '__main__':
    unittest.main()
