"""Tests for the ChatGPT Work illustration skill (production/art/skill/heraldry-classic-ink-art)."""
import contextlib, hashlib, io, json, shutil, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "production/art/skill/heraldry-classic-ink-art"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
import heraldry_art as ha  # noqa: E402

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
    (root / ".gitattributes").write_text("assets/art/incoming/*.png filter=lfs diff=lfs merge=lfs -text\n")
    refs = []
    for n in range(2):
        p = f"assets/art/style/REF-{n}.jpg"
        figure_image().save(root / p, quality=80)
        refs.append(p)
    items = items or [
        {"id": "ART-T-SCENE", "family": "bastion", "register": "scene", "title": "Test Scene", "size": "1536x1024", "print_w_in": 3.3, "must": [], "avoid": ["No people."], "size_class": "", "max_attempts": 3},
        {"id": "ART-T-BEAST", "family": "monster", "register": "creature", "title": "Test Beast", "size": "1024x1024", "print_w_in": 1.9, "must": ["Exactly eight legs"], "avoid": [], "size_class": "Large: roughly twice a human's height or bulk", "max_attempts": 3},
        {"id": "ART-T-HERO", "family": "class", "register": "person", "title": "Test Hero", "size": "1024x1536", "print_w_in": 1.9, "must": [], "avoid": [], "size_class": "", "max_attempts": 3},
    ]
    for it in items:
        text = f"{it['title'].upper()} - PROMPT\n\nMust be shown exactly:\n" + "\n".join("* " + m for m in it["must"])
        (root / "production/art/gpt/prompts" / f"{it['id']}.txt").write_text(text + "\n")
        it.update({"prompt": f"production/art/gpt/prompts/{it['id']}.txt", "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(),
                   "references": refs[:1], "save_as": f"assets/art/incoming/{it['id']}.png"})
    q = {"schema": 2, "phase": phase, "generated_at": "2026-10-10T00:00:00+00:00", "max_references": 3, "references": refs, "count": len(items), "items": items}
    (root / "production/art/gpt/QUEUE.json").write_text(json.dumps(q))
    return q


def run(root, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ha.main(["--repo", str(root), *args])
    return code, out.getvalue(), err.getvalue()


def git(root, *args):
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", *args], check=True, capture_output=True)


class Measurements(unittest.TestCase):
    def verdict(self, im, item_id, tmp, name="x.png"):
        root = Path(tmp)
        if not (root / "r").exists():
            make_repo(root / "r")
        p = root / name
        im.save(p)
        code, out, err = run(root / "r", "check", item_id, str(p), "--json")
        return json.loads(out)

    def test_calibrated_classification(self):
        with tempfile.TemporaryDirectory() as tmp:
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
                    got = self.verdict(im, "ART-T-BEAST", tmp)
                    self.assertEqual(got["result"], expect, got)
            with self.subTest(case="wrong aspect"):
                got = self.verdict(good.crop((0, 0, 1024, 700)), "ART-T-BEAST", tmp)
                self.assertEqual(got["result"], "FAIL")
                self.assertTrue(any("aspect" in f for f in got["fails"]))
            with self.subTest(case="too small"):
                got = self.verdict(figure_image((600, 600)), "ART-T-BEAST", tmp)
                self.assertTrue(any("long side" in f for f in got["fails"]))

    def test_scene_register_wants_a_vignette(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.verdict(scene_image(), "ART-T-SCENE", tmp)["result"], "PASS")
            bleed = self.verdict(scene_image(vignette=False), "ART-T-SCENE", tmp)
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
        with tempfile.TemporaryDirectory() as tmp:
            good = figure_image()
            images = {"good": good, "frame": self._frame(good), "tint": self._tint(good), "wash": good.filter(ImageFilter.GaussianBlur(5)),
                      "scene": scene_image()}
            for name, im in images.items():
                with self.subTest(image=name):
                    src, dst = Path(tmp) / f"{name}.png", Path(tmp) / f"{name}_ink.png"
                    im.save(src)
                    info = prep(src, dst)
                    m = ha.measure(src)
                    self.assertAlmostEqual(m["colour"], info["colour_frac"], places=3)
                    self.assertAlmostEqual(m["midtone"], info["midtone_frac"], places=3)
                    self.assertAlmostEqual(m["intake_border_ink"], info["border_ink"], places=3)


class Runner(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.root = self.tmp / "repo"
        self.root.mkdir()
        self.q = make_repo(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def image(self, name="gen.png", fmt="PNG", scene=False):
        p = self.tmp / name
        (scene_image() if scene else figure_image()).save(p, format=fmt)
        return p

    def test_save_keeps_bytes_uses_true_extension_and_writes_receipt(self):
        src = self.image("looks_like.jpg", fmt="PNG")                    # PNG content under a .jpg name
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(src), "--attempts", "2", "--model", "GPT Images 2.5", "--notes", "first pass clean")
        self.assertEqual(code, 0, err + out)
        dest = self.root / "assets/art/incoming/ART-T-BEAST.png"
        self.assertEqual(dest.read_bytes(), src.read_bytes())
        rec = [json.loads(line) for line in (self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()][-1]
        item = next(i for i in self.q["items"] if i["id"] == "ART-T-BEAST")
        self.assertEqual(rec["id"], "ART-T-BEAST")
        self.assertEqual(rec["prompt_sha256"], item["prompt_sha256"])
        self.assertEqual((rec["variants_tried"], rec["model"], rec["surface"]), (2, "GPT Images 2.5", "ChatGPT Work"))
        self.assertRegex(rec["date_utc"], r"^\d{4}-\d\d-\d\d$")
        # one file per ID: saving a JPEG replaces the PNG
        jpg = self.image("b.jpg", fmt="JPEG")
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(jpg), "--redo")
        self.assertEqual(code, 0, err + out)
        self.assertEqual([f.name for f in (self.root / "assets/art/incoming").glob("ART-T-BEAST.*")], ["ART-T-BEAST.jpg"])

    def test_save_refuses_failures_and_unlisted_ids_but_can_accept_flags(self):
        bad = self.tmp / "bad.png"
        Image.new("RGB", (1024, 1024), (250, 248, 240)).save(bad)
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(bad))
        self.assertEqual(code, 2)
        self.assertIn("mechanical failures", err)
        self.assertFalse((self.root / "assets/art/incoming/ART-T-BEAST.png").exists())
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(bad), "--accept-flags", "--attempts", "3")
        self.assertEqual(code, 0, err)
        rec = json.loads((self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()[-1])
        self.assertTrue(rec["tripwires"])
        code, out, err = run(self.root, "save", "ART-NOT-QUEUED", str(self.image()))
        self.assertEqual(code, 2)
        self.assertIn("never generate an ID the queue does not list", err)

    def test_show_verifies_prompt_hash_and_lists_must_and_avoid(self):
        code, out, err = run(self.root, "show", "ART-T-BEAST")
        self.assertEqual(code, 0, err)
        self.assertIn("* Exactly eight legs", out)
        self.assertIn("Large: roughly twice", out)
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
        (self.root / "assets/art/style/REF-0.jpg").write_bytes(b"version https://git-lfs.github.com/spec/v1\noid sha256:00\nsize 1\n")
        (self.root / "assets/art/style/REF-1.jpg").unlink()
        self.q["items"][0]["references"] = ["assets/art/style/REF-0.jpg", "assets/art/style/REF-1.jpg"]
        (self.root / "production/art/gpt/QUEUE.json").write_text(json.dumps(self.q))
        (self.root / "production/art/gpt/prompts/ART-T-HERO.txt").write_text("edited\n")
        code, out, err = run(self.root, "doctor")
        self.assertEqual(code, 1)
        self.assertIn("LFS pointer", out)
        self.assertIn("reference missing", out)
        self.assertIn("no longer match the queue hashes", out)

    def test_refusal_is_recorded_and_stays_compatible_with_the_intake_receipts(self):
        code, out, err = run(self.root, "refuse", "ART-T-BEAST", "--reason", "content policy")
        self.assertEqual(code, 0, err)
        rec = json.loads((self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()[-1])
        self.assertEqual((rec["id"], rec["refused"], rec["reason"]), ("ART-T-BEAST", True, "content policy"))
        import art_intake
        from unittest.mock import patch
        with patch.object(art_intake, "RECEIPTS", self.root / "production/art/gpt/RECEIPTS.jsonl"):
            r = art_intake.receipts()["ART-T-BEAST"]
        self.assertIsNone(r.get("prompt_sha256"))                # a later real receipt for the same ID replaces it
        code, out, err = run(self.root, "refuse", "ART-NOT-QUEUED", "--reason", "x")
        self.assertEqual(code, 2)

    def test_sheet_and_bundle(self):
        for iid, sc in (("ART-T-BEAST", False), ("ART-T-SCENE", True)):
            code, out, err = run(self.root, "save", iid, str(self.image(f"{iid}.png", scene=sc)))
            self.assertEqual(code, 0, err + out)
        out_sheet = self.tmp / "sheet.jpg"
        code, out, err = run(self.root, "sheet", "ART-T-BEAST", "ART-T-SCENE", "--refs", "--out", str(out_sheet))
        self.assertEqual(code, 0, err)
        with Image.open(out_sheet) as sheet:
            self.assertGreater(sheet.width, 600)
        z = self.tmp / "b.zip"
        for label in ("without git", "with git"):
            if label == "with git":
                if not HAVE_GIT:
                    break
                git(self.root, "init", "-q", "-b", "main")
            with self.subTest(label):
                self.assertIn("BUNDLE" if label == "without git" else "COMMIT AND PUSH", run(self.root, "status")[1])
                code, out, err = run(self.root, "bundle", "--out", str(z))
                self.assertEqual(code, 0, err + out)
                names = zipfile.ZipFile(z).namelist()
                self.assertIn("assets/art/incoming/ART-T-BEAST.png", names)
                self.assertIn("receipts_append.jsonl", names)
                lines = zipfile.ZipFile(z).read("receipts_append.jsonl").decode().strip().splitlines()
                self.assertEqual({json.loads(x)["id"] for x in lines}, {"ART-T-BEAST", "ART-T-SCENE"})

    def test_without_git_an_image_the_intake_has_recorded_counts_as_sent(self):
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(self.image()))
        self.assertEqual(code, 0, err)
        self.assertEqual(ha.states(self.root, self.q)["ART-T-BEAST"], "saved")
        data = (self.root / "assets/art/incoming/ART-T-BEAST.png").read_bytes()
        (self.root / "production/art").mkdir(parents=True, exist_ok=True)
        sels = {"ART-T-BEAST": {"status": "received", "master": {"sha256": hashlib.sha256(data).hexdigest()}}}
        (self.root / "production/art/SELECTIONS.json").write_text(json.dumps(sels))
        self.assertEqual(ha.states(self.root, self.q)["ART-T-BEAST"], "pushed")
        sels["ART-T-BEAST"]["status"] = "rejected"
        (self.root / "production/art/SELECTIONS.json").write_text(json.dumps(sels))
        self.assertEqual(ha.states(self.root, self.q)["ART-T-BEAST"], "redo")
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(self.image("again.png", scene=False)))
        self.assertEqual(code, 0, err)                                      # redo needs no --redo flag


@unittest.skipUnless(HAVE_GIT, "git not installed")
class GitStates(unittest.TestCase):
    def test_item_states_follow_git_history_and_next_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            remote, root = tmp / "remote.git", tmp / "repo"
            subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
            root.mkdir()
            make_repo(root)
            git(root, "init", "-q", "-b", "main")
            git(root, "remote", "add", "origin", str(remote))
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "base")
            git(root, "push", "-q", "-u", "origin", "main")
            q = ha.load_queue(root)
            self.assertEqual(set(ha.states(root, q).values()), {"pending"})
            ids = [i["id"] for i in q["items"]]
            # save all three
            for iid, scene in zip(ids, (True, False, False)):
                p = tmp / f"{iid}.png"
                (scene_image() if scene else figure_image()).save(p)
                if iid == "ART-T-HERO":
                    Image.new("RGB", (1024, 1536), (255, 255, 255))
                    figure_image((1024, 1536)).save(p)
                code, out, err = run(root, "save", iid, str(p))
                self.assertEqual(code, 0, err + out)
            self.assertEqual(set(ha.states(root, q).values()), {"saved"})
            self.assertIn("COMMIT AND PUSH", run(root, "status")[1])
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "art")
            self.assertEqual(set(ha.states(root, q).values()), {"saved"}, "committed but not pushed is still 'saved'")
            git(root, "push", "-q", "origin", "main")
            self.assertEqual(set(ha.states(root, q).values()), {"pushed"})
            self.assertIn("STOP. The anchors are done", run(root, "status")[1])
            # the reviewer rejects one: it becomes 'redo' until re-saved
            (root / "production/art").mkdir(exist_ok=True)
            (root / "production/art/SELECTIONS.json").write_text(json.dumps({"ART-T-BEAST": {"status": "rejected"}}))
            st = ha.states(root, q)
            self.assertEqual(st["ART-T-BEAST"], "redo")
            self.assertIn("ART-T-BEAST", run(root, "next")[1])
            code, out, err = run(root, "save", "ART-T-SCENE", str(tmp / "ART-T-BEAST.png"))
            self.assertEqual(code, 2, "a delivered, un-rejected item needs --redo")
            # a refusal is its own state, is not offered again, and its receipt must be pushed
            code, out, err = run(root, "refuse", "ART-T-HERO", "--reason", "policy")
            self.assertEqual(code, 0, err)
            self.assertEqual(ha.states(root, q)["ART-T-HERO"], "refused")
            status = run(root, "status")[1]
            self.assertIn("refused=1", status)
            self.assertIn("COMMIT AND PUSH", status)
            self.assertNotIn("ART-T-HERO", run(root, "next")[1])
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "refusal")
            git(root, "push", "-q", "origin", "main")
            status = run(root, "status")[1]
            self.assertNotIn("COMMIT AND PUSH", status)
            self.assertIn("ART-T-BEAST", status)                       # still 'redo' work first
            (root / "production/art/SELECTIONS.json").write_text("{}")
            status = run(root, "status")[1]
            self.assertIn("STOP. The anchors are done (1 refused: ART-T-HERO)", status)
            # a later save replaces the refusal
            p = tmp / "retry.png"
            figure_image((1024, 1536), scale=0.6).save(p)
            self.assertEqual(run(root, "save", "ART-T-HERO", str(p), "--redo")[0], 0)
            self.assertEqual(ha.states(root, q)["ART-T-HERO"], "saved")
            # batch phase with everything pushed
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "retry")
            git(root, "push", "-q", "origin", "main")
            q2 = json.loads((root / "production/art/gpt/QUEUE.json").read_text())
            q2["phase"] = "batch"
            (root / "production/art/gpt/QUEUE.json").write_text(json.dumps(q2))
            (root / "production/art/SELECTIONS.json").write_text("{}")
            self.assertIn("NOTHING LEFT", run(root, "status")[1])


class SkillSources(unittest.TestCase):
    def test_every_script_and_reference_named_in_skill_md_exists(self):
        import re
        skill = (SKILL / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\nname: heraldry-classic-ink-art\n"))
        for ref in set(re.findall(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`", skill)):
            self.assertTrue((SKILL / ref).exists(), ref)


@unittest.skipUnless((ROOT / "production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip").is_file() and (ROOT / "assets/art/style").is_dir(),
                     "a release package ships neither the skill zip nor the owner's style samples")
class SkillPackage(unittest.TestCase):
    ZIP = ROOT / "production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip"

    def test_families_table_matches_config(self):
        import art_skill_build as b
        self.assertEqual((SKILL / "references/FAMILIES.md").read_text(), b.families_markdown(), "run tools/art_skill_build.py")

    def test_zip_is_current_with_its_sources_and_the_repo_images(self):
        import art_skill_build as b
        self.assertTrue(self.ZIP.is_file(), "run tools/art_skill_build.py")
        with zipfile.ZipFile(self.ZIP) as z:
            names = set(z.namelist())
            sources = {p.relative_to(SKILL).as_posix() for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
            self.assertEqual(names, sources | set(b.IMAGES) | {"references/images/SOURCES.json", "manifest.json"})
            self.assertIn("SKILL.md", names)
            for rel in sources:
                self.assertEqual(z.read(rel), (SKILL / rel).read_bytes(), f"{rel} changed since the zip was built: run tools/art_skill_build.py")
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
