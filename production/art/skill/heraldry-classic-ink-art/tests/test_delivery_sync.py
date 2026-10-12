"""delivery_guard.ship in a long unattended run: the intake bot commits to main after every
delivery, so the next ship must fast-forward safely (disjoint paths) and stop on any overlap or
divergence. Real git and Git LFS against a local bare remote."""
import hashlib, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import delivery_guard as dg
import fidelity_gate as fg

HAVE = shutil.which('git') is not None and subprocess.run(['git', 'lfs', 'version'], capture_output=True).returncode == 0


def git(cwd, *a):
    return subprocess.run(['git', '-C', str(cwd), '-c', 'user.name=t', '-c', 'user.email=t@t', *a],
                          check=True, capture_output=True, text=True).stdout


@unittest.skipUnless(HAVE, 'git and git-lfs required')
class ShipSync(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.origin = self.tmp / 'origin.git'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', str(self.origin)], check=True)
        seed = self.tmp / 'seed'
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(seed)], check=True, capture_output=True)
        ref = seed / 'assets/art/style/REF.jpg'
        ref.parent.mkdir(parents=True)
        Image.new('RGB', (64, 64), 'white').save(ref)
        (seed / 'assets/art/incoming').mkdir(parents=True)
        (seed / 'assets/art/incoming/.keep').write_text('')
        prompt = seed / 'production/art/gpt/prompts/ART-T.txt'
        prompt.parent.mkdir(parents=True)
        prompt.write_text('ink drawing\n')
        self.item = {'id': 'ART-T', 'prompt': 'production/art/gpt/prompts/ART-T.txt',
                     'prompt_sha256': hashlib.sha256(b'ink drawing').hexdigest(),
                     'references': ['assets/art/style/REF.jpg'], 'size': '1024x1024', 'register': 'creature'}
        (seed / 'production/art/gpt/QUEUE.json').write_text(json.dumps({'schema': 2, 'items': [self.item]}))
        (seed / 'production/art/gpt/RECEIPTS.jsonl').write_text('{"id": "ART-OLD"}\n')
        (seed / 'production/art/SELECTIONS.json').write_text('{}\n')
        (seed / '.gitattributes').write_text('assets/art/incoming/*.png filter=lfs diff=lfs merge=lfs -text\nassets/art/incoming/*.jpg filter=lfs diff=lfs merge=lfs -text\nassets/art/incoming/*.webp filter=lfs diff=lfs merge=lfs -text\n')
        git(seed, 'add', '-A'); git(seed, 'commit', '-qm', 'seed'); git(seed, 'push', '-q', 'origin', 'main')
        self.work = self.tmp / 'work'
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.work)], check=True, capture_output=True)
        git(self.work, 'lfs', 'install', '--local')
        git(self.work, 'config', 'user.name', 'worker')          # CI runners have no global identity
        git(self.work, 'config', 'user.email', 'worker@example.invalid')
        self.bot = self.tmp / 'bot'
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.bot)], check=True, capture_output=True)

    def deliver_locally(self):
        """What `save` leaves behind: an image plus a byte-bound receipt, uncommitted."""
        img = self.work / 'assets/art/incoming/ART-T.jpg'
        im = Image.new('RGB', (1024, 1024), 'white')
        ImageDraw.Draw(im).ellipse((200, 200, 800, 800), outline='black', width=12)
        im.save(img, quality=92)
        rec = {'id': 'ART-T', 'prompt_sha256': self.item['prompt_sha256'], 'native_sha256': dg.sha_file(img),
               'reference_shas': [dg.sha_file(self.work / 'assets/art/style/REF.jpg')],
               'qa_review': {k: {'pass': True, 'evidence': 'synthetic stand-in, mechanics only'} for k in fg.CRITERIA},
               'qa_failed_criteria': [], 'qa_unresolved': []}
        with (self.work / 'production/art/gpt/RECEIPTS.jsonl').open('a') as f:
            f.write(json.dumps(rec) + '\n')

    def bot_commits(self, path, text):
        git(self.bot, 'pull', '-q', '--ff-only', 'origin', 'main')
        (self.bot / path).write_text(text)
        git(self.bot, 'add', '-A'); git(self.bot, 'commit', '-qm', 'art: intake'); git(self.bot, 'push', '-q', 'origin', 'main')

    def test_fast_forwards_over_an_intake_commit_and_pushes(self):
        self.deliver_locally()
        self.bot_commits('production/art/SELECTIONS.json', '{"ART-X": {"status": "received"}}\n')
        out = dg.ship(self.work)
        self.assertEqual(out['status'], 'PUSHED')
        log = git(self.work, 'log', '--format=%s', 'origin/main')
        self.assertEqual(log.splitlines()[:2], ['art(gpt): ART-T .. ART-T', 'art: intake'])
        self.assertEqual(git(self.work, 'status', '--porcelain'), '')

    def test_stops_when_upstream_changed_the_same_receipts(self):
        self.deliver_locally()
        self.bot_commits('production/art/gpt/RECEIPTS.jsonl', '{"id": "ART-OLD"}\n{"id": "ART-OTHER"}\n')
        with self.assertRaisesRegex(dg.Error, 'changed the same files'):
            dg.ship(self.work)
        self.assertIn('ART-T.jpg', git(self.work, 'status', '--porcelain'))     # work preserved

    def test_stops_on_divergence(self):
        self.deliver_locally()
        (self.work / 'notes.txt').write_text('local commit')
        git(self.work, 'add', 'notes.txt'); git(self.work, 'commit', '-qm', 'local')
        self.bot_commits('production/art/SELECTIONS.json', '{}\n\n')
        with self.assertRaisesRegex(dg.Error, 'diverges'):
            dg.ship(self.work)

    def test_recovers_a_commit_that_was_never_pushed(self):
        self.deliver_locally()
        git(self.work, 'add', '-A'); git(self.work, 'commit', '-qm', 'art(gpt): ART-T .. ART-T')   # killed before push
        self.bot_commits('production/art/SELECTIONS.json', '{"ART-X": {"status": "received"}}\n')
        self.assertEqual(dg.ship(self.work)['status'], 'PUSHED')
        self.assertEqual(git(self.work, 'log', '--format=%s', 'origin/main').splitlines()[:2], ['art(gpt): ART-T .. ART-T', 'art: intake'])

    def test_a_push_that_landed_is_not_delivered_twice(self):
        self.deliver_locally()
        git(self.work, 'add', '-A'); git(self.work, 'commit', '-qm', 'art(gpt): ART-T .. ART-T')
        git(self.work, 'push', '-q', 'origin', 'main')
        git(self.work, 'reset', '-q', 'HEAD~1')          # the guard undid its commit after a push timeout
        self.bot_commits('production/art/SELECTIONS.json', '{"ART-X": {"status": "received"}}\n')
        out = dg.ship(self.work)
        self.assertEqual(out['status'], 'PUSHED')
        self.assertEqual(git(self.work, 'log', '--format=%s', 'origin/main').count('art(gpt): ART-T'), 1)
        self.assertEqual(git(self.work, 'status', '--porcelain'), '')

    def test_a_repeated_ship_after_a_landed_delivery_is_not_blocked(self):
        # Codex's tool can time out while a push lands; a second ship must not read as BLOCKED (a stop condition).
        self.deliver_locally()
        self.assertEqual(dg.ship(self.work)['status'], 'PUSHED')
        out = dg.ship(self.work)
        self.assertEqual(out['status'], 'UP-TO-DATE')
        self.assertEqual(out['commit'], git(self.work, 'rev-parse', 'origin/main').strip())
        self.assertEqual(dg.main(['ship', '--execute', '--repo', str(self.work)]), 0)
        with self.assertRaisesRegex(dg.Error, 'nothing to deliver'):
            dg.validate(self.work)                       # audit still says there is nothing to deliver

    def test_redo_in_another_format_replaces_the_old_file(self):
        self.deliver_locally()
        dg.ship(self.work)
        old = self.work / 'assets/art/incoming/ART-T.jpg'
        old.unlink()                                     # what save does when the redo is a different format
        img = self.work / 'assets/art/incoming/ART-T.webp'
        im = Image.new('RGB', (1024, 1024), 'white')
        ImageDraw.Draw(im).rectangle((250, 250, 750, 750), outline='black', width=12)
        im.save(img)
        rec = {'id': 'ART-T', 'prompt_sha256': self.item['prompt_sha256'], 'native_sha256': dg.sha_file(img),
               'reference_shas': [dg.sha_file(self.work / 'assets/art/style/REF.jpg')],
               'qa_review': {k: {'pass': True, 'evidence': 'synthetic stand-in, mechanics only'} for k in fg.CRITERIA},
               'qa_failed_criteria': [], 'qa_unresolved': []}
        with (self.work / 'production/art/gpt/RECEIPTS.jsonl').open('a') as f:
            f.write(json.dumps(rec) + '\n')
        self.assertEqual(dg.ship(self.work)['status'], 'PUSHED')
        tree = git(self.work, 'ls-tree', '-r', '--name-only', 'origin/main', 'assets/art/incoming')
        self.assertIn('ART-T.webp', tree)
        self.assertNotIn('ART-T.jpg', tree)

    def test_a_deletion_without_replacement_is_refused(self):
        self.deliver_locally()
        dg.ship(self.work)
        (self.work / 'assets/art/incoming/ART-T.jpg').unlink()
        with (self.work / 'production/art/gpt/RECEIPTS.jsonl').open('a') as f:
            f.write('{"id": "ART-T", "refused": true}\n')
        with self.assertRaisesRegex(dg.Error, 'without a replacement'):
            dg.validate(self.work, need_remote=False)

    def test_a_failed_push_leaves_a_clean_index_and_the_files(self):
        self.deliver_locally()
        hook = self.work / '.git/hooks/pre-push'
        hook.write_text('#!/bin/sh\necho "denied by policy" >&2\nexit 1\n'); hook.chmod(0o755)
        head = git(self.work, 'rev-parse', 'HEAD')
        with self.assertRaisesRegex(dg.Error, 'not a race'):
            dg.ship(self.work)
        self.assertEqual(git(self.work, 'rev-parse', 'HEAD'), head)
        self.assertEqual(git(self.work, 'diff', '--cached', '--name-only'), '')
        self.assertTrue((self.work / 'assets/art/incoming/ART-T.jpg').is_file())


    def test_next_fast_forwards_a_clean_clone_but_not_one_with_unsent_work(self):
        import heraldry_art as ha
        self.bot_commits('production/art/SELECTIONS.json', '{"ART-T": {"status": "rejected"}}\n')
        up = git(self.origin, 'rev-parse', 'main').strip()
        self.deliver_locally()                       # unsent work: never pulled over
        ha.refresh(self.work)
        self.assertNotEqual(git(self.work, 'rev-parse', 'HEAD').strip(), up)
        git(self.work, 'checkout', '-q', '--', '.'); git(self.work, 'clean', '-qfd')
        ha.refresh(self.work)                        # clean: the reviewer's rejection is seen now
        self.assertEqual(git(self.work, 'rev-parse', 'HEAD').strip(), up)


if __name__ == '__main__':
    unittest.main()


class CadenceRepo(unittest.TestCase):
    """Fixture only (no tests): a git repo with a four-item queue, for the status/cadence tests below."""
    def setUp(self):
        import heraldry_art as ha
        self.ha = ha
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.repo = self.tmp / 'repo'
        (self.repo / 'production/art/gpt/prompts').mkdir(parents=True)
        (self.repo / 'assets/art/incoming').mkdir(parents=True)
        ref = self.repo / 'assets/art/style/REF.jpg'
        ref.parent.mkdir(parents=True)
        Image.new('RGB', (64, 64), 'white').save(ref)
        self.items = []
        for n in range(4):
            iid = f'ART-T{n}'
            (self.repo / f'production/art/gpt/prompts/{iid}.txt').write_text(f'ink {n}\n')
            self.items.append({'id': iid, 'title': iid, 'family': 'monster', 'register': 'creature', 'size': '1024x1024',
                               'print_w_in': 1.9, 'max_attempts': 3, 'size_class': '', 'must': [], 'avoid': [],
                               'prompt': f'production/art/gpt/prompts/{iid}.txt',
                               'prompt_sha256': hashlib.sha256(f'ink {n}'.encode()).hexdigest(),
                               'references': ['assets/art/style/REF.jpg']})
        git(self.repo.parent, 'init', '-q', '-b', 'main', str(self.repo))

    def queue(self, review_every, receipts_base=0):
        (self.repo / 'production/art/gpt/QUEUE.json').write_text(json.dumps(
            {'schema': 2, 'phase': 'batch', 'count': 4, 'push_every': 1, 'review_every': review_every,
             'receipts_base': receipts_base, 'generated_at': '2026-10-11T00:00:00+00:00', 'items': self.items}))

    def make(self, n):
        it = self.items[n]
        im = Image.new('RGB', (1024, 1024), 'white')
        ImageDraw.Draw(im).ellipse((200 + 9 * n, 200, 800, 800 - 9 * n), outline='black', width=10)
        im.save(self.repo / f"assets/art/incoming/{it['id']}.png")
        with (self.repo / 'production/art/gpt/RECEIPTS.jsonl').open('a') as f:
            f.write(json.dumps({'id': it['id'], 'prompt_sha256': it['prompt_sha256']}) + '\n')

    def status(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.ha.main(['--repo', str(self.repo), 'status'])
        return buf.getvalue()



@unittest.skipUnless(HAVE, 'git required')
class PerImageCadence(CadenceRepo):
    """push_every 1: deliver after each image; drift review only every review_every images."""
    def test_deliver_each_image_and_review_every_third(self):
        self.queue(3)
        self.make(0); self.make(1)
        git(self.repo, 'add', '-A'); git(self.repo, 'commit', '-qm', 'two delivered')
        self.make(2)                                   # third image saved: crosses the review boundary
        self.assertIn('DRIFT REVIEW', self.status())
        git(self.repo, 'add', '-A'); git(self.repo, 'commit', '-qm', 'third delivered')
        self.make(3)                                   # fourth: plain delivery, no review
        out = self.status()
        self.assertIn('DELIVER:', out)
        self.assertNotIn('DRIFT REVIEW', out)
        self.assertEqual(self.ha.recent_ids(self.repo, self.ha.load_queue(self.repo), 2), ['ART-T2', 'ART-T3'])
        import style_audit as sa
        rep = sa.build(self.repo, recent=3)
        self.assertEqual([r['id'] for r in rep['items']], ['ART-T1', 'ART-T2', 'ART-T3'])


@unittest.skipUnless(HAVE, 'git required')
class RefusalReopens(CadenceRepo):
    """A refusal binds to the prompt it was made against; a republished prompt reopens the item."""
    def test_refusal_reopens_after_the_prompt_changes(self):
        self.queue(10)
        st = lambda: self.ha.states(self.repo, self.ha.load_queue(self.repo))['ART-T0']   # noqa: E731
        with (self.repo / 'production/art/gpt/RECEIPTS.jsonl').open('a') as f:
            f.write(json.dumps({'id': 'ART-T0', 'refused': True, 'prompt_sha256': self.items[0]['prompt_sha256']}) + '\n')
        self.assertEqual(st(), 'refused')
        (self.repo / 'production/art/gpt/prompts/ART-T0.txt').write_text('ink 0, fixed\n')
        self.items[0]['prompt_sha256'] = hashlib.sha256(b'ink 0, fixed').hexdigest()
        self.queue(10)
        self.assertEqual(st(), 'pending')

    def test_a_republished_queue_reopens_an_earlier_refusal_with_the_same_prompt(self):
        # e.g. the tool refused six references; Claude Code republishes with five and an unchanged prompt
        self.queue(10)
        st = lambda: self.ha.states(self.repo, self.ha.load_queue(self.repo))['ART-T0']   # noqa: E731
        rec = self.repo / 'production/art/gpt/RECEIPTS.jsonl'
        with rec.open('a') as f:
            f.write(json.dumps({'id': 'ART-T0', 'refused': True, 'prompt_sha256': self.items[0]['prompt_sha256']}) + '\n')
        self.assertEqual(st(), 'refused')                      # refused during this queue's run: stays refused
        lines = sum(1 for x in rec.read_text().splitlines() if x.strip())
        self.queue(10, receipts_base=lines)                    # republished after the refusal
        self.assertEqual(st(), 'pending')


@unittest.skipUnless(HAVE, 'git required')
class DriftCountIsMonotonic(CadenceRepo):
    """A rejection turns a pushed item back into a redo; that must not re-trigger the drift review."""
    def test_a_rejection_does_not_repeat_the_drift_review(self):
        self.queue(3)
        for n in range(3):
            self.make(n)
        git(self.repo, 'add', '-A'); git(self.repo, 'commit', '-qm', 'three delivered')    # review was due at 3
        (self.repo / 'production/art/SELECTIONS.json').write_text(json.dumps(
            {'ART-T0': {'status': 'rejected', 'rejected_reason': 'redo', 'master': {'sha256': None}}}))
        self.make(3)                                   # the fourth save: plain delivery, not another review
        out = self.status()
        self.assertIn('DELIVER:', out)
        self.assertNotIn('DRIFT REVIEW', out)

    def test_archive_keeps_one_local_copy_per_item_outside_the_clone(self):
        import os
        from unittest import mock
        arch = self.tmp / 'archive'
        with mock.patch.dict(os.environ, {'HERALDRY_ARCHIVE': str(arch)}):
            self.ha.archive_copy(self.repo, 'ART-T0.png', b'first')
            self.ha.archive_copy(self.repo, 'ART-T0.jpg', b'redo')         # a redo in another format replaces it
            self.assertEqual(sorted(p.name for p in arch.iterdir()), ['ART-T0.jpg'])
        with mock.patch.dict(os.environ, {'HERALDRY_ARCHIVE': str(self.repo / 'keep')}):
            with self.assertRaises(self.ha.Fatal):
                self.ha.archive_copy(self.repo, 'ART-T0.png', b'x')

    def test_receipts_from_before_the_queue_do_not_count_toward_drift_reviews(self):
        self.queue(3)
        for n in range(3):
            self.make(n)                               # three old receipts, as after a reset
        q = json.loads((self.repo / 'production/art/gpt/QUEUE.json').read_text())
        self.assertEqual(self.ha.saved_receipt_lines(self.repo, q), 3)
        q['receipts_base'] = 3                         # the queue was republished after them
        self.assertEqual(self.ha.saved_receipt_lines(self.repo, q), 0)

    def test_style_audit_skips_images_held_as_lfs_pointers(self):
        import style_audit as sa
        self.queue(10)
        self.make(0); self.make(1)
        (self.repo / 'assets/art/incoming/ART-T1.png').write_bytes(b'version https://git-lfs.github.com/spec/v1\noid sha256:' + b'a' * 64 + b'\nsize 1\n')
        rep = sa.build(self.repo, recent=10)
        self.assertEqual([r['id'] for r in rep['items']], ['ART-T0'])
        self.assertEqual(self.ha.recent_ids(self.repo, self.ha.load_queue(self.repo), 10), ['ART-T0'])


@unittest.skipUnless(HAVE, 'git required')
class AttemptNumbering(CadenceRepo):
    """Re-checking an earlier attempt (to save it) reports that attempt, not the number of images checked."""
    def test_saving_an_earlier_attempt_records_that_attempt(self):
        import os
        from unittest import mock
        with mock.patch.dict(os.environ, {'HERALDRY_SCRATCH': str(self.tmp / 'scratch')}):
            self.queue(10)
            q = self.ha.load_queue(self.repo)
            files = []
            for k in range(4):                       # budget 3, one generation too many
                f = self.tmp / f'a{k}.png'
                im = Image.new('RGB', (1024, 1024), 'white')
                ImageDraw.Draw(im).rectangle((100 + 40 * k, 100, 900, 900 - 40 * k), outline='black', width=12)
                im.save(f)
                files.append(f)
                *_, fails, warns, infos, pv, n, checked, dup = self.ha.run_check(self.repo, q, 'ART-T0', f)
                self.assertEqual((n, checked), (k + 1, k + 1))
            self.assertTrue(any('beyond the attempt budget' in x for x in fails))
            *_, fails, warns, infos, pv, n, checked, dup = self.ha.run_check(self.repo, q, 'ART-T0', files[2])
            self.assertEqual((n, checked), (3, 4))
            self.assertFalse(any('budget' in x for x in fails))
