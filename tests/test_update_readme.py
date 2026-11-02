"""README derivation and publication against local Git repositories; no network or book build."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import update_readme as updater
from figure_dependencies import hashes_for_text

README = ('# Hand-written title\n\n<!-- BEGIN AUTO:status -->\nold\n<!-- END AUTO:status -->\n'
          '\nKeep this guidance exactly.\n\n<!-- BEGIN AUTO:recent -->\nold\n<!-- END AUTO:recent -->\n\nEnd.\n')


class ReadmeUpdate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='heraldry-readme-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.origin, self.runner, self.peer = (self.base / p for p in ('origin.git', 'runner', 'peer'))
        self.git(self.base, 'init', '--bare', '--initial-branch=main', str(self.origin))
        self.git(self.base, 'clone', str(self.origin), str(self.runner))
        self.configure(self.runner)
        self.write('README.md', README)
        source = '## 1. Rules\n\nMove 6".\n'
        svg, caption = '<svg/>\n', 'Movement example.'
        self.write('source/RC2.md', source)
        self.write('source/versions.json', {'current': 2, 'revisions': [
            {'number': 2, 'path': 'source/RC2.md', 'sha256': hashlib.sha256(source.encode()).hexdigest()}]})
        self.write('dist/RELEASE.json', {'tag': 'RC1-build-3', 'assets': [
            {'name': 'Heraldry_RC1_digital.pdf', 'sha256': 'pdf-hash'}]})
        self.write('production/RELEASE_RESULT.json', {'result': 'RELEASED'})
        self.write('production/qa/visual-review.json', {'sha256': 'pdf-hash', 'pages': 12})
        self.write('production/art/SELECTIONS.json', {'one': {'status': 'approved'}, 'two': {'status': 'delivered'}})
        self.write('production/art/gpt/QUEUE.json', {'items': ['two']})
        self.write('figures/manifest.json', {'figures': [{'id': 'FIG-01'}]})
        self.write('figures/placements.json', {'chapter': [{'id': 'FIG-01', 'caption': caption}]})
        self.write('figures/out/FIG-01.svg', svg)
        deps = {'FIG-01': ['1']}
        self.write('config/figure_dependencies.json', deps)
        self.write('production/qa/figure-semantic-review.json', {'figures': [{
            'id': 'FIG-01', 'verdict': 'PASS', 'findings': [],
            'svg_sha256': hashlib.sha256(svg.encode()).hexdigest(),
            'caption_sha256': hashlib.sha256(caption.encode()).hexdigest(),
            'rules_sha256': hashes_for_text(source, deps)['FIG-01']}]})
        self.git(self.runner, 'add', '.')
        self.git(self.runner, 'commit', '-m', 'initial <script> [link](evil) `code`')
        self.git(self.runner, 'push', 'origin', 'main')
        self.initial = self.git(self.runner, 'rev-parse', 'HEAD')
        self.git(self.base, '-c', 'core.autocrlf=false', 'clone', str(self.origin), str(self.peer))
        self.configure(self.peer)

    def git(self, cwd, *args):
        result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def configure(self, root):
        for key, value in [('user.name', 'README tests'), ('user.email', 'readme@example.invalid'),
                           ('core.autocrlf', 'false'), ('commit.gpgsign', 'false')]:
            self.git(root, 'config', key, value)

    def write(self, path, value, root=None):
        path = (root or self.runner) / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((value if isinstance(value, str) else json.dumps(value)).encode())

    def remote(self, *args):
        return self.git(self.base, f'--git-dir={self.origin}', *args)

    def publish(self, **kwargs):
        return updater.publish(self.runner, busy=lambda: False, **kwargs)

    def test_status_derives_records_without_promoting_delivery_or_art(self):
        text = updater.render(self.runner).decode()
        for expected in ('[RC2]', 'RC1-build-3', '12 pages', 'RC2 source changes await',
                         '1 approved of 2', '1 generation-queue items', '1/1 current'):
            self.assertIn(expected, text)
        self.assertNotIn('Physical printing', text)
        self.assertIn('Keep this guidance exactly.\n', text)
        self.assertTrue(text.startswith('# Hand-written title\n'))
        self.assertTrue(text.endswith('\nEnd.\n'))
        self.assertIn(r'\<script\>', text)
        self.assertIn(r'\[link\](evil)', text)

    def test_refresh_is_idempotent_and_preserves_crlf_outside_blocks(self):
        self.write('README.md', README.replace('\n', '\r\n'))
        output = updater.render(self.runner)
        self.assertIn(b'\r\nKeep this guidance exactly.\r\n', output)
        self.assertNotIn(b'\n', output.replace(b'\r\n', b''))
        (self.runner / 'README.md').write_bytes(output)
        self.assertEqual(output, updater.render(self.runner))

    def test_missing_duplicate_and_overlapping_markers_fail_without_writing(self):
        for text in (README.replace('<!-- END AUTO:status -->', ''), README + '<!-- BEGIN AUTO:recent -->',
                     README.replace('<!-- END AUTO:status -->', '').replace('End.', '<!-- END AUTO:status -->')):
            with self.subTest(text=text):
                self.write('README.md', text)
                before = (self.runner / 'README.md').read_bytes()
                with self.assertRaises(ValueError):
                    updater.render(self.runner)
                self.assertEqual(before, (self.runner / 'README.md').read_bytes())

    def test_changed_svg_marks_review_stale_and_unmatched_pdf_omits_pages(self):
        self.write('figures/out/FIG-01.svg', '<svg>changed</svg>')
        self.write('production/qa/visual-review.json', {'sha256': 'another-pdf', 'pages': 999})
        text = updater.render(self.runner).decode()
        self.assertIn('0/1 current', text)
        self.assertNotIn(', 999 pages', text)

    def test_manuscript_hash_mismatch_fails(self):
        self.write('source/RC2.md', 'unregistered source change')
        with self.assertRaisesRegex(ValueError, 'registry'):
            updater.render(self.runner)

    def test_readme_only_commit_is_excluded_from_recent_changes(self):
        self.write('README.md', README + 'manual note\n')
        self.git(self.runner, 'add', 'README.md')
        self.git(self.runner, 'commit', '-m', 'README-only sentinel')
        self.assertNotIn('README-only sentinel', updater.render(self.runner).decode())

    def test_publish_changes_only_readme_and_preserves_worktree_index_and_head(self):
        self.write('dirty.txt', 'staged')
        self.git(self.runner, 'add', 'dirty.txt')
        self.write('dirty.txt', 'unstaged')
        index = (self.runner / '.git/index').read_bytes()
        before = self.git(self.runner, 'status', '--porcelain')
        result = self.publish()
        self.assertTrue(result.startswith('UPDATED: '), result)
        self.assertEqual(self.remote('rev-parse', 'main^'), self.initial)
        self.assertEqual(self.remote('diff-tree', '--no-commit-id', '--name-only', '-r', 'main'), 'README.md')
        self.assertEqual(self.git(self.runner, 'rev-parse', 'HEAD'), self.initial)
        self.assertEqual((self.runner / '.git/index').read_bytes(), index)
        self.assertEqual(self.git(self.runner, 'status', '--porcelain'), before)
        self.assertEqual(self.publish(), 'UNCHANGED: README is current')

    def test_busy_publication_or_request_push_defers(self):
        self.assertTrue(updater.publish(self.runner, busy=lambda: True).startswith('DEFERRED:'))
        self.write('production/build-request.json', {'request_id': 'new'})
        self.git(self.runner, 'add', '.')
        self.git(self.runner, 'commit', '-m', 'request build')
        event = {'before': self.initial, 'after': self.git(self.runner, 'rev-parse', 'HEAD')}
        self.assertTrue(self.publish(event=event).startswith('DEFERRED:'))
        self.assertEqual(self.remote('rev-parse', 'main'), self.initial)

    def test_race_retries_using_fresh_parent_and_metadata(self):
        real_run, pushes = subprocess.run, []
        def race(args, **kwargs):
            if args[:3] == ['git', 'push', 'origin']:
                pushes.append(args)
                if len(pushes) == 1:
                    self.write('production/art/SELECTIONS.json', {'third': {'status': 'approved'}}, self.peer)
                    self.write('README.md', README + 'Peer guidance.\n', self.peer)
                    for command in [('add', '.'), ('commit', '-m', 'concurrent update'), ('push', 'origin', 'main')]:
                        response = real_run(['git', *command], cwd=self.peer, capture_output=True)
                        self.assertEqual(response.returncode, 0, response.stderr)
            return real_run(args, **kwargs)
        with patch.object(updater.subprocess, 'run', side_effect=race):
            self.assertTrue(self.publish().startswith('UPDATED:'))
        self.assertEqual(len(pushes), 2)
        text = self.remote('show', 'main:README.md')
        self.assertIn('1 approved of 1', text)
        self.assertIn('Peer guidance.', text)
        self.assertIn('concurrent update', text)

    def test_new_request_during_retry_defers_and_permissions_error_does_not_retry(self):
        real_run, pushes = subprocess.run, []
        def race(args, **kwargs):
            if args[:3] == ['git', 'push', 'origin']:
                pushes.append(args)
                self.write('production/build-request.json', {'request_id': 'racing'}, self.peer)
                for command in [('add', '.'), ('commit', '-m', 'request'), ('push', 'origin', 'main')]:
                    response = real_run(['git', *command], cwd=self.peer, capture_output=True)
                    self.assertEqual(response.returncode, 0, response.stderr)
            return real_run(args, **kwargs)
        with patch.object(updater.subprocess, 'run', side_effect=race):
            self.assertIn('publication inputs changed', self.publish())
        self.assertEqual(len(pushes), 1)
        pushes.clear()
        def denied(args, **kwargs):
            if args[:3] == ['git', 'push', 'origin']:
                pushes.append(args)
                return subprocess.CompletedProcess(args, 128, stdout=b'', stderr=b'permission denied')
            return real_run(args, **kwargs)
        with patch.object(updater.subprocess, 'run', side_effect=denied):
            with self.assertRaisesRegex(RuntimeError, 'push refused'):
                self.publish()
        self.assertEqual(len(pushes), 1)

    def test_polling_checks_waiting_runs_and_propagates_unknown_status_failure(self):
        queried = []
        def api(repo, endpoint, token):
            queried.append(endpoint)
            return {'total_count': int('status=waiting' in endpoint)}
        self.assertTrue(updater.publication_busy('owner/repo', 'not-a-real-token', api=api))
        self.assertTrue(any('status=waiting' in q for q in queried))
        with self.assertRaises(RuntimeError):
            updater.publication_busy('owner/repo', 'not-a-real-token', api=lambda *a: (_ for _ in ()).throw(RuntimeError('unavailable')))


class WorkflowWiring(unittest.TestCase):
    def test_all_other_workflows_have_completion_refresh_and_main_push_is_unfiltered(self):
        workflow = (ROOT / '.github/workflows/update-readme.yml').read_text()
        push = workflow.split('  push:\n', 1)[1].split('  workflow_dispatch:', 1)[0]
        self.assertIn('branches: [main]', push)
        self.assertNotIn('paths', push)
        self.assertIn('types: [completed]', workflow)
        for path in (ROOT / '.github/workflows').glob('*.yml'):
            if path.name != 'update-readme.yml':
                name = path.read_text().splitlines()[0].removeprefix('name: ')
                self.assertIn('      - ' + name + '\n', workflow, f'{path.name} needs a README completion trigger')
        self.assertEqual(workflow.count('      - Update GitHub README'), 0)

    def test_trusted_checkout_pre_push_tests_and_shared_non_cancelling_queue(self):
        workflow = (ROOT / '.github/workflows/update-readme.yml').read_text()
        for expected in ('ref: main', 'contents: write', 'actions: read', 'head_repository.full_name == github.repository',
                         "event != 'pull_request'", "event != 'pull_request_target'", 'make PY=python test'):
            self.assertIn(expected, workflow)
        self.assertLess(workflow.index('make PY=python test'), workflow.index('tools/update_readme.py --publish'))
        self.assertNotIn('download-artifact', workflow)
        for filename in ('update-readme.yml', 'build-candidate.yml', 'rebuild-delivery.yml'):
            text = (ROOT / '.github/workflows' / filename).read_text()
            self.assertIn('group: publication-main\n  cancel-in-progress: false\n  queue: max', text)


if __name__ == '__main__':
    unittest.main()
