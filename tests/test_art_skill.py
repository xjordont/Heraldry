"""Tests for the ChatGPT Work illustration skill (production/art/skill/heraldry-classic-ink-art)."""
import contextlib, hashlib, io, json, os, shutil, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path
from unittest import mock

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "production/art/skill/heraldry-classic-ink-art"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
import heraldry_art as ha  # noqa: E402

# Legacy v4 tests below remain in source to document the former unaudited save/push interface.
# The skill requires evidence-backed --qa-file and guarded delivery; that contract is tested in
# production/art/skill/heraldry-classic-ink-art/tests/test_v5_regression.py and test_v6.py (file names kept from v6).

HAVE_GIT = shutil.which("git") is not None


def figure_image(size=(1024, 1024), scale=0.7, offset=(0, 0)):
    """Hatched black-ink standing figure on flat white paper, about as inky as the owner's figure sample."""
    w, h = size
    k = h * scale / 10
    cx, cy = w // 2 + offset[0], h // 2 + offset[1]
    layer = Image.new("L", size, 255)
    d = ImageDraw.Draw(layer)
    torso = (cx - 1.5 * k, cy - 3.6 * k, cx + 1.5 * k, cy + 1.2 * k)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse(torso, fill=255)
    hatch = Image.new("L", size, 255)
    hd = ImageDraw.Draw(hatch)
    for i in range(-h, w + h, 9):
        hd.line((i, 0, i - h // 2, h), fill=0, width=3)
    layer.paste(hatch, (0, 0), mask)
    d.ellipse(torso, outline=0, width=6)
    d.ellipse((cx - .7 * k, cy - 5 * k, cx + .7 * k, cy - 3.7 * k), outline=0, width=6)
    d.ellipse((cx - .35 * k, cy - 4.5 * k, cx - .1 * k, cy - 4.3 * k), fill=0)
    d.ellipse((cx + .1 * k, cy - 4.5 * k, cx + .35 * k, cy - 4.3 * k), fill=0)
    for dx in (-1, 1):
        d.line((cx + dx * .6 * k, cy + 1 * k, cx + dx * 1.1 * k, cy + 4.8 * k), fill=0, width=9)
        d.line((cx + dx * 1.5 * k, cy - 3 * k, cx + dx * 2.3 * k, cy - .4 * k), fill=0, width=8)
    return layer.convert("RGB")


def scene_image(size=(1536, 1024), vignette=True):
    """Dense hatched ellipse that fades to paper (vignette) or fills the frame (no vignette)."""
    im = Image.new("RGB", size, (250, 247, 238))
    d = ImageDraw.Draw(im)
    w, h = size
    box = (w * .08, h * .08, w * .92, h * .92) if vignette else (-w * .1, -h * .1, w * 1.1, h * 1.1)
    for y in range(0, h, 7):
        d.line((0, y, w, y + 40), fill=(20, 20, 20), width=2)
    for x in range(0, w, 9):
        d.line((x, 0, x - 60, h), fill=(40, 40, 40), width=2)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse(box, fill=255)
    out = Image.new("RGB", size, (250, 247, 238))
    out.paste(im, (0, 0), mask)
    return out


def make_repo(root, phase="anchors", items=None):
    for d in ("production/art/gpt/prompts", "assets/art/incoming", "assets/art/style"):
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / ".gitattributes").write_text("assets/art/incoming/*.png filter=lfs diff=lfs merge=lfs -text\nassets/art/incoming/*.jpg filter=lfs diff=lfs merge=lfs -text\nassets/art/incoming/*.webp filter=lfs diff=lfs merge=lfs -text\n")
    refs = []
    for n in range(2):
        p = f"assets/art/style/REF-{n}.jpg"
        figure_image(scale=0.6 + 0.1 * n).save(root / p, quality=80)
        refs.append(p)
    items = items or [
        {"id": "ART-T-SCENE", "family": "bastion", "register": "scene", "title": "Test Scene", "size": "1536x1024", "print_w_in": 3.3, "must": [], "avoid": ["No people."], "size_class": "", "max_attempts": 3},
        {"id": "ART-T-BEAST", "family": "monster", "register": "creature", "title": "Test Beast", "size": "1024x1024", "print_w_in": 1.9, "must": ["Exactly eight legs"], "avoid": ["No scenery."], "size_class": "Large: roughly twice a human's height or bulk", "max_attempts": 3},
        {"id": "ART-T-HERO", "family": "class", "register": "person", "title": "Test Hero", "size": "1024x1536", "print_w_in": 1.9, "must": [], "avoid": [], "size_class": "", "max_attempts": 3},
    ]
    for it in items:
        text = f"{it['title'].upper()} - PROMPT\n\nMust be shown exactly:\n" + "\n".join("* " + m for m in it["must"])
        (root / "production/art/gpt/prompts" / f"{it['id']}.txt").write_text(text + "\n")
        it.update({"prompt": f"production/art/gpt/prompts/{it['id']}.txt", "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(),
                   "references": refs[1:] if it["id"] == "ART-T-HERO" else refs[:1]})
    q = {"schema": 2, "phase": phase, "generated_at": "2026-10-10T00:00:00+00:00", "max_references": 3, "count": len(items), "items": items}
    (root / "production/art/gpt/QUEUE.json").write_text(json.dumps(q))
    return q


def run(root, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ha.main(["--repo", str(root), *args])
    return code, out.getvalue(), err.getvalue()


def queue_item(root, iid):
    return next(i for i in json.loads((Path(root) / "production/art/gpt/QUEUE.json").read_text())["items"] if i["id"] == iid)


def attest(item):
    """The statements `save` asks for: one --must per MUST line, and --avoid-clear when there is a do-not-draw list."""
    flags = []
    for m in item["must"]:
        flags += ["--must", f"{m}: checked"]
    if item["avoid"]:
        flags.append("--avoid-clear")
    return flags


def save(root, iid, path, *extra):
    return run(root, "save", iid, str(path), *attest(queue_item(root, iid)), *extra)


def git(root, *args):
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", *args], check=True, capture_output=True)


class Isolated(unittest.TestCase):
    """Each test gets its own scratch folder, so attempt counts and previews never leak between tests or into /tmp."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        patcher = mock.patch.dict(os.environ, {"HERALDRY_SCRATCH": str(self.tmp / "scratch")})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)


class Measurements(Isolated):
    def verdict(self, im, item_id, name="x.png"):
        root = self.tmp / "r"
        if not root.exists():
            make_repo(root)
        p = self.tmp / name
        im.save(p)
        with mock.patch.dict(os.environ, {"HERALDRY_SCRATCH": str(self.tmp / f"scratch-{name}-{id(im)}")}):   # one attempt per call
            code, out, err = run(root, "check", item_id, str(p), "--json")
        return json.loads(out)

    def test_calibrated_classification(self):
        good = figure_image()
        cases = {
            "good": (good, "PASS"),
            "frame": (self._frame(good), "FAIL"),
            "cropped": (figure_image(offset=(420, 0)), "FAIL"),
            "colour": (self._tint(good), "FAIL"),
            "wash": (good.filter(ImageFilter.GaussianBlur(5)), "WARN"),
            "blank": (Image.new("RGB", (1024, 1024), (250, 248, 240)), "FAIL"),
            "tiny": (figure_image(scale=0.3), "WARN"),
            "vanished": (figure_image(scale=0.1), "FAIL"),
        }
        for name, (im, expect) in cases.items():
            with self.subTest(case=name):
                got = self.verdict(im, "ART-T-BEAST")
                self.assertEqual(got["result"], expect, got)
        with self.subTest(case="wrong aspect"):
            got = self.verdict(good.crop((0, 0, 1024, 700)), "ART-T-BEAST")
            self.assertEqual(got["result"], "FAIL")
            self.assertTrue(any("aspect" in f for f in got["fails"]))
        with self.subTest(case="too small"):
            got = self.verdict(figure_image((600, 600)), "ART-T-BEAST")
            self.assertTrue(any("long side" in f for f in got["fails"]))

    def test_scene_register_wants_a_vignette(self):
        self.assertEqual(self.verdict(scene_image(), "ART-T-SCENE")["result"], "PASS")
        bleed = self.verdict(scene_image(vignette=False), "ART-T-SCENE", "bleed.png")
        self.assertEqual(bleed["result"], "FAIL")
        self.assertTrue(any("vignette" in f for f in bleed["fails"]))

    @staticmethod
    def _frame(im):
        im = im.copy()
        ImageDraw.Draw(im).rectangle((6, 6, 1017, 1017), outline=(20, 20, 20), width=8)
        return im

    @staticmethod
    def _tint(im):
        r, g, b = im.split()
        return Image.merge("RGB", (r, g.point(lambda v: int(v * .55)), b.point(lambda v: int(v * .55))))

    def test_intake_numbers_match_art_ink(self):
        """The skill reports the same colour, mid-tone and border measures the intake computes."""
        from art_ink import prep
        good = figure_image()
        images = {"good": good, "frame": self._frame(good), "tint": self._tint(good), "wash": good.filter(ImageFilter.GaussianBlur(5)),
                  "scene": scene_image()}
        for name, im in images.items():
            with self.subTest(image=name):
                src, dst = self.tmp / f"{name}.png", self.tmp / f"{name}_ink.png"
                im.save(src)
                info = prep(src, dst)
                m = ha.measure(src)
                self.assertAlmostEqual(m["colour"], info["colour_frac"], places=3)
                self.assertAlmostEqual(m["midtone"], info["midtone_frac"], places=3)
                self.assertAlmostEqual(m["intake_border_ink"], info["border_ink"], places=3)


class Runner(Isolated):
    def setUp(self):
        super().setUp()
        self.root = self.tmp / "repo"
        self.root.mkdir()
        self.q = make_repo(self.root)

    def image(self, name="gen.png", fmt="PNG", scene=False, scale=0.7):
        p = self.tmp / name
        (scene_image() if scene else figure_image(scale=scale)).save(p, format=fmt)
        return p

    def test_status_at_session_end_with_nothing_unsent_says_so(self):
        out = run(self.root, "status", "--end")[1]
        self.assertIn("SESSION END: nothing is unsent", out)
        self.assertIn("Next session: GENERATE next", out)

    def test_check_repeats_the_lists_and_names_the_helper_in_messages(self):
        code, out, err = run(self.root, "check", "ART-T-BEAST", str(self.image()))
        self.assertIn("MUST BE SHOWN (count or find it): Exactly eight legs", out)
        self.assertIn("DO NOT DRAW (confirm it is absent): No scenery.", out)
        self.assertIn("heraldry_art.py", run(self.root, "status")[1])

    def test_show_verifies_prompt_hash_and_lists_must_and_avoid(self):
        code, out, err = run(self.root, "show", "ART-T-BEAST")
        self.assertEqual(code, 0, err)
        self.assertIn("* Exactly eight legs", out)
        self.assertIn("* No scenery.", out)
        self.assertIn("Large: roughly twice", out)
        self.assertIn("IMAGE SIZE: 1024x1024 pixels (square 1:1)", out)
        self.assertIn("STATE: pending (nothing delivered yet)", out)
        (self.root / "production/art/gpt/prompts/ART-T-BEAST.txt").write_text("changed\n")
        code, out, err = run(self.root, "show", "ART-T-BEAST")
        self.assertEqual(code, 2)
        self.assertIn("does not match the queue hash", err)

    def test_old_queue_schema_is_refused_with_instructions(self):
        q = json.loads((self.root / "production/art/gpt/QUEUE.json").read_text())
        q["schema"] = 1
        (self.root / "production/art/gpt/QUEUE.json").write_text(json.dumps(q))
        code, out, err = run(self.root, "status")
        self.assertEqual(code, 2)
        self.assertIn("schema 1", err)

    def test_doctor_reports_pointer_missing_reference_and_stale_prompts(self):
        code, out, err = run(self.root, "doctor")
        self.assertEqual(code, 0, out)                                         # not a git repo: generating is fine, delivery is not
        self.assertIn("READY TO GENERATE. Delivery by git is blocked: git is not available here", out)
        self.assertIn(str(ha.scratch_dir(self.root)), out)
        (self.root / "assets/art/style/REF-0.jpg").write_bytes(b"version https://git-lfs.github.com/spec/v1\noid sha256:00\nsize 1\n")
        (self.root / "assets/art/style/REF-1.jpg").unlink()
        self.q["items"][0]["references"] = ["assets/art/style/REF-0.jpg", "assets/art/style/REF-1.jpg"]
        (self.root / "production/art/gpt/QUEUE.json").write_text(json.dumps(self.q))
        (self.root / "production/art/gpt/prompts/ART-T-HERO.txt").write_text("edited\n")
        code, out, err = run(self.root, "doctor")
        self.assertEqual(code, 1)
        self.assertIn("LFS pointers, not images", out)
        self.assertIn('git lfs pull --include="assets/art/style/REF-0.jpg"', out)
        self.assertIn("reference missing", out)
        self.assertIn("no longer match the queue hashes", out)

    def test_refusal_is_recorded_and_stays_compatible_with_the_intake_receipts(self):
        code, out, err = run(self.root, "refuse", "ART-T-BEAST", "--reason", "content policy")
        self.assertEqual(code, 0, err)
        rec = json.loads((self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()[-1])
        self.assertEqual((rec["id"], rec["refused"], rec["reason"]), ("ART-T-BEAST", True, "content policy"))
        import art_intake
        with mock.patch.object(art_intake, "RECEIPTS", self.root / "production/art/gpt/RECEIPTS.jsonl"):
            r = art_intake.receipts()["ART-T-BEAST"]
        queued = {it["id"]: it for it in json.loads((self.root / "production/art/gpt/QUEUE.json").read_text())["items"]}
        # the refusal binds to the prompt it refused, so a republished (fixed) prompt reopens the item;
        # a later real receipt for the same ID still replaces it
        self.assertEqual(r.get("prompt_sha256"), queued["ART-T-BEAST"]["prompt_sha256"])
        code, out, err = run(self.root, "check", "ART-T-BEAST", str(self.image()))
        self.assertIn("recorded as refused", out)
        code, out, err = run(self.root, "refuse", "ART-NOT-QUEUED", "--reason", "x")
        self.assertEqual(code, 2)

    def test_doctor_creates_the_scratch_folder_and_the_helper_names_the_repos_own_copy(self):
        self.assertFalse(ha.scratch_dir(self.root).exists())
        run(self.root, "doctor")
        self.assertTrue(ha.scratch_dir(self.root).is_dir())
        mine = Path(ha.__file__)
        repo_copy = self.root / ha.HELPER_IN_REPO
        repo_copy.parent.mkdir(parents=True)
        repo_copy.write_bytes(mine.read_bytes())
        out = run(self.root, "doctor")[1]
        self.assertIn("identical", out)
        self.assertIn(ha.HELPER_IN_REPO, run(self.root, "status")[1], "messages name the repo's copy")
        repo_copy.write_text(repo_copy.read_text() + "\n# newer\n")
        self.assertIn("WARNING: this helper differs from the repo's copy", run(self.root, "doctor")[1])
        self.assertIn("WARNING: this helper differs from the repo's copy", run(self.root, "status")[1])

    def test_doctor_says_not_ready_yet_for_a_fixable_pointer_and_ready_once_fixed(self):
        ref = self.root / "assets/art/style/REF-0.jpg"
        good = ref.read_bytes()
        ref.write_bytes(b"version https://git-lfs.github.com/spec/v1\noid sha256:" + b"0" * 64 + b"\nsize 1\n")
        code, out, err = run(self.root, "doctor")
        self.assertEqual(code, 1)
        self.assertIn("NOT READY YET (one step)", out)
        self.assertNotIn("NOT READY:", out)
        self.assertIn('git lfs pull --include="assets/art/style/REF-0.jpg"', out)
        ref.write_bytes(good)
        code, out, err = run(self.root, "doctor")
        self.assertEqual(code, 0, out)
        self.assertIn("READY TO GENERATE", out)

    def test_scratch_is_per_repository_and_overridable(self):
        other = self.tmp / "other"
        other.mkdir()
        self.assertNotEqual(ha.scratch_dir(self.root), ha.scratch_dir(other))
        self.assertTrue(str(ha.scratch_dir(self.root)).startswith(str(self.tmp / "scratch")))
        with mock.patch.dict(os.environ, {"HERALDRY_SCRATCH": str(self.tmp / "elsewhere")}):
            self.assertTrue(str(ha.scratch_dir(self.root)).startswith(str(self.tmp / "elsewhere")))


@unittest.skipUnless(HAVE_GIT, "git not installed")
class GitStates(Isolated):
    def make(self):
        remote, root = self.tmp / "remote.git", self.tmp / "repo"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
        root.mkdir()
        make_repo(root)
        git(root, "init", "-q", "-b", "main")
        git(root, "remote", "add", "origin", str(remote))
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "base")
        git(root, "push", "-q", "-u", "origin", "main")
        return root

    def test_status_stops_for_stray_files_and_images_without_a_receipt(self):
        root = self.make()
        stray = root / "assets/art/incoming/notes.png"
        figure_image().save(stray)
        out = run(root, "status")[1]
        self.assertIn("WARNING: not a queue item, but changed under assets/art/incoming: assets/art/incoming/notes.png", out)
        self.assertIn("NEXT ACTION: STOP. The files above are not queue items", out)
        stray.unlink()
        figure_image(scale=0.6).save(root / "assets/art/incoming/ART-T-BEAST.png")          # placed by hand: no receipt from `save`
        out = run(root, "status")[1]
        self.assertIn("ART-T-BEAST has an image but no matching receipt", out)
        self.assertIn("NEXT ACTION: STOP. ART-T-BEAST have no receipt from `save`", out)
        (root / "assets/art/incoming/ART-T-BEAST.png").unlink()
        self.assertNotIn("STOP", run(root, "status")[1])


class PointerHashes(Isolated):
    def test_an_lfs_pointer_carries_the_images_sha_so_a_skip_smudge_clone_still_knows_what_it_holds(self):
        img = self.tmp / "a.png"
        figure_image().save(img)
        digest = hashlib.sha256(img.read_bytes()).hexdigest()
        pointer = self.tmp / "pointer.png"
        pointer.write_text(f"version https://git-lfs.github.com/spec/v1\noid sha256:{digest}\nsize {img.stat().st_size}\n")
        self.assertEqual(ha.local_sha(img), digest)
        self.assertEqual(ha.local_sha(pointer), digest)
        self.assertTrue(ha.still_the_rejected_image({"master": {"sha256": digest}}, pointer))
        self.assertFalse(ha.still_the_rejected_image({"master": {"sha256": "0" * 64}}, pointer), "a different image is not the rejected one")
        self.assertTrue(ha.still_the_rejected_image({}, pointer), "no recorded hash: assume it is still the rejected image")


HAVE_IMAGES = (ROOT / "assets/art/style").is_dir()
_BUILT = {}


def built_zip():
    """The skill zip, built once per test run into a temporary folder: it is a build output, never committed."""
    if "zip" not in _BUILT:
        import art_skill_build as b
        tmp = tempfile.mkdtemp()
        _BUILT["zip"] = Path(tmp) / "skill.zip"
        _BUILT["zip"].write_bytes(b.zip_bytes())
        import atexit
        atexit.register(shutil.rmtree, tmp, True)
    return _BUILT["zip"]


class ValidatorCli(unittest.TestCase):
    SCRIPT = SKILL / "scripts/validate_skill.py"

    def run_cli(self, *args, cwd=ROOT):
        r = subprocess.run([sys.executable, str(self.SCRIPT), *args], cwd=cwd, capture_output=True, text=True)
        return r.returncode, json.loads(r.stdout)

    def test_source_folder_is_explained_not_a_wall_of_errors(self):
        code, out = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual(len(out["errors"]), 1)
        self.assertIn("skill source, not a built package", out["errors"][0])
        self.assertEqual(out["repo_checks"], "skipped: not a built package")

    @unittest.skipUnless(HAVE_IMAGES, "needs the repo images")
    def test_zip_validates_with_the_repo_found_automatically_or_skipped_outside_one(self):
        code, out = self.run_cli("--zip", str(built_zip()))
        self.assertEqual((code, out["status"], out["repo_checks"]), (0, "PASS", "done"))
        self.assertEqual(Path(out["repo"]), ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.run_cli("--zip", str(built_zip()), cwd=tmp)
            self.assertEqual((code, out["status"], out["repo"]), (0, "PASS", None))
            self.assertIn("skipped", out["repo_checks"])


class SkillSources(unittest.TestCase):
    def test_every_script_and_reference_named_in_skill_md_exists(self):
        import re
        skill = (SKILL / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\nname: heraldry-classic-ink-art\n"))
        for ref in set(re.findall(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`", skill)):
            self.assertTrue((SKILL / ref).exists(), ref)
        # every command in the helper table exists as a subcommand, and the full path in the docs is real
        for cmd in re.findall(r"^\| `([a-z]+)[ `]", skill, re.M):
            self.assertTrue(hasattr(ha, "cmd_" + cmd), cmd)
        self.assertTrue((ROOT / "production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py").is_file())
        self.assertIn("python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py", skill)


@unittest.skipUnless(HAVE_IMAGES, "a release package does not ship the owner's style samples")
class SkillPackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ZIP = built_zip()

    def test_families_table_matches_config(self):
        import art_skill_build as b
        self.assertEqual((SKILL / "references/FAMILIES.md").read_text(), b.families_markdown(), "run tools/art_skill_build.py")

    def test_zip_holds_its_sources_and_the_repo_images_and_builds_reproducibly(self):
        import art_skill_build as b
        self.assertEqual(b.zip_bytes(), self.ZIP.read_bytes(), "the skill zip build is not deterministic")
        with zipfile.ZipFile(self.ZIP) as z:
            names = set(z.namelist())
            sources = {p.relative_to(SKILL).as_posix() for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
            self.assertEqual(names, sources | set(b.IMAGES) | {"references/images/SOURCES.json", "manifest.json"})
            self.assertIn("SKILL.md", names)
            for rel in sources:
                self.assertEqual(z.read(rel), (SKILL / rel).read_bytes(), rel)
            for name, (repo_path, _role) in b.IMAGES.items():
                self.assertEqual(z.read(name), (ROOT / repo_path).read_bytes(), name)

    def test_validator_passes_the_zip_and_catches_tampering(self):
        import validate_skill as vs
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            zipfile.ZipFile(self.ZIP).extractall(base)
            errors, images = vs.check_package(base)
            self.assertEqual(errors, [])
            self.assertEqual(vs.check_repo(base, ROOT, images), [])
            (base / "SKILL.md").write_text((base / "SKILL.md").read_text() + "\nextra\n")
            self.assertTrue(any("hash mismatch: SKILL.md" in e for e in vs.check_package(base)[0]))
            (base / "references/images/STYLE-REF-03-figure-spotblack.jpg").unlink()
            self.assertTrue(any("STYLE-REF-03" in e for e in vs.check_package(base)[0]))
            fam = base / "references/FAMILIES.md"
            fam.write_text(fam.read_text().replace("| monster | creature | 1024x1024 |", "| monster | creature | 1536x1024 |"))
            self.assertTrue(any("FAMILIES.md row for monster" in e for e in vs.check_repo(base, ROOT, images)))


if __name__ == "__main__":
    unittest.main()
