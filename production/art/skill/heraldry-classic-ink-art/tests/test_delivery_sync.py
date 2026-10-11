"""delivery_guard.ship in a long unattended run: the intake bot commits to main after every
delivery, so the next ship must fast-forward safely (disjoint paths) and stop on any overlap or
divergence. Real git against a local bare remote; JPEG images avoid needing an LFS server."""
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
        (seed / '.gitattributes').write_text('assets/art/incoming/*.png filter=lfs diff=lfs merge=lfs -text\n')
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


if __name__ == '__main__':
    unittest.main()


@unittest.skipUnless(HAVE, 'git required')
class PerImageCadence(unittest.TestCase):
    """push_every 1: deliver after each image; drift review only every review_every images."""
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

    def queue(self, review_every):
        (self.repo / 'production/art/gpt/QUEUE.json').write_text(json.dumps(
            {'schema': 2, 'phase': 'batch', 'count': 4, 'push_every': 1, 'review_every': review_every,
             'generated_at': '2026-10-11T00:00:00+00:00', 'items': self.items}))

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
