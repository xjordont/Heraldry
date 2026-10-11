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
