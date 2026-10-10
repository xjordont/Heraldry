"""Tests for the ChatGPT Work illustration skill (production/art/skill/heraldry-classic-ink-art)."""
import contextlib, hashlib, io, json, os, shutil, subprocess, sys, tempfile, unittest, warnings, zipfile
from pathlib import Path
from unittest import mock

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
                   "references": refs[1:] if it["id"] == "ART-T-HERO" else refs[:1], "save_as": f"assets/art/incoming/{it['id']}.png"})
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

    def test_save_keeps_bytes_uses_true_extension_and_writes_receipt(self):
        src = self.image("looks_like.jpg", fmt="PNG")                    # PNG content under a .jpg name
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(src), "--attempts", "2", "--model", "GPT Images 2.5", "--notes", "first pass clean",
                             "--must", "Exactly eight legs: counted 8", "--avoid-clear")
        self.assertEqual(code, 0, err + out)
        dest = self.root / "assets/art/incoming/ART-T-BEAST.png"
        self.assertEqual(dest.read_bytes(), src.read_bytes())
        rec = [json.loads(line) for line in (self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()][-1]
        item = next(i for i in self.q["items"] if i["id"] == "ART-T-BEAST")
        self.assertEqual(rec["id"], "ART-T-BEAST")
        self.assertEqual(rec["prompt_sha256"], item["prompt_sha256"])
        self.assertEqual((rec["variants_tried"], rec["model"], rec["surface"]), (2, "GPT Images 2.5", "ChatGPT Work"))
        self.assertEqual(rec["must_checked"], ["Exactly eight legs: counted 8"])
        self.assertTrue(rec["avoid_clear"])
        self.assertRegex(rec["date_utc"], r"^\d{4}-\d\d-\d\d$")
        # one file per ID: saving a JPEG replaces the PNG
        jpg = self.image("b.jpg", fmt="JPEG", scale=0.65)
        code, out, err = save(self.root, "ART-T-BEAST", jpg, "--redo")
        self.assertEqual(code, 0, err + out)
        self.assertEqual([f.name for f in (self.root / "assets/art/incoming").glob("ART-T-BEAST.*")], ["ART-T-BEAST.jpg"])

    def test_save_demands_real_statements_one_per_must_line(self):
        img = self.image()
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(img))
        self.assertEqual(code, 2)
        self.assertIn("Missing", err)
        self.assertIn("Exactly eight legs", err)
        self.assertIn("--avoid-clear", err)
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(img), "--must", "Exactly eight legs: counted 8")
        self.assertEqual(code, 2)
        self.assertIn("--avoid-clear", err)
        self.assertNotIn("exactly one --must", err)
        for bad in (["--must", ""], ["--must", "ok"], ["--must", "counted 8 legs, 4 a side", "--must", "and a second one that is not wanted"]):
            code, out, err = run(self.root, "save", "ART-T-BEAST", str(img), *bad, "--avoid-clear")
            self.assertEqual(code, 2, bad)
            self.assertIn("--must", err)
        self.assertFalse((self.root / "assets/art/incoming/ART-T-BEAST.png").exists())
        # an item with no lists needs no statements, and refuses a --must it has no line for
        hero = self.tmp / "hero.png"
        figure_image((1024, 1536)).save(hero)
        code, out, err = run(self.root, "save", "ART-T-HERO", str(hero), "--must", "counted something")
        self.assertEqual(code, 2)
        self.assertIn("no MUST lines", err)
        code, out, err = run(self.root, "save", "ART-T-HERO", str(hero))
        self.assertEqual(code, 0, err)
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(img), "--must", "counted 8 legs, 4 a side", "--avoid-clear")
        self.assertEqual(code, 0, err)

    def test_accept_flags_is_only_for_the_last_allowed_attempt_and_marks_the_receipt(self):
        imgs = [self.image(f"c{i}.png", scale=0.5 + 0.05 * i) for i in range(3)]
        run(self.root, "check", "ART-T-BEAST", str(imgs[0]))
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(imgs[0]), "--accept-flags", "--notes", "cannot be bothered")
        self.assertEqual(code, 2)
        self.assertIn("only for the last allowed attempt", err)
        self.assertIn("1 of 3", err)
        for im in imgs[1:]:
            run(self.root, "check", "ART-T-BEAST", str(im))
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(imgs[2]), "--accept-flags")
        self.assertEqual(code, 2)
        self.assertIn("needs --notes", err)
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(imgs[2]), "--accept-flags", "--notes", "legs still not countable")
        self.assertEqual(code, 0, err)
        rec = json.loads((self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()[-1])
        self.assertEqual((rec["accepted_flags"], rec["accepted_at_attempt"], rec["variants_tried"]), (True, 3, 3))

    def test_save_refuses_mechanical_failures_and_unlisted_ids(self):
        bad = self.tmp / "bad.png"
        Image.new("RGB", (1024, 1024), (250, 248, 240)).save(bad)
        code, out, err = save(self.root, "ART-T-BEAST", bad)
        self.assertEqual(code, 2)
        self.assertIn("mechanical failures", err)
        self.assertFalse((self.root / "assets/art/incoming/ART-T-BEAST.png").exists())
        for k in (1, 2):                                                       # the budget is 3 attempts
            Image.new("RGB", (1024, 1024), (250 - k, 248, 240)).save(self.tmp / f"bad{k}.png")
            run(self.root, "check", "ART-T-BEAST", str(self.tmp / f"bad{k}.png"))
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(bad), "--accept-flags", "--notes", "blank on every attempt")
        self.assertEqual(code, 0, err)
        rec = json.loads((self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()[-1])
        self.assertTrue(rec["tripwires"])
        self.assertEqual(rec["notes"], "blank on every attempt")
        code, out, err = run(self.root, "save", "ART-NOT-QUEUED", str(self.image()))
        self.assertEqual(code, 2)
        self.assertIn("never generate an ID the queue does not list", err)

    def test_attempts_are_counted_by_distinct_image_and_the_budget_is_enforced(self):
        imgs = [self.image(f"a{i}.png", scale=0.5 + 0.05 * i) for i in range(4)]
        for i in range(3):
            code, out, err = run(self.root, "check", "ART-T-BEAST", str(imgs[i]))
            self.assertEqual(code, 0, out + err)
            self.assertIn(f"attempt {i + 1} of 3", out)
        code, out, err = run(self.root, "check", "ART-T-BEAST", str(imgs[2]))          # the same image again is not a new attempt
        self.assertIn("attempt 3 of 3", out)
        self.assertEqual(len(ha.attempts_of(self.root, "ART-T-BEAST")), 3)
        self.assertIn("used so far: 3", run(self.root, "show", "ART-T-BEAST")[1])
        code, out, err = run(self.root, "check", "ART-T-BEAST", str(imgs[3]))
        self.assertEqual(code, 1)
        self.assertIn("attempt budget used up", out)
        code, out, err = save(self.root, "ART-T-BEAST", imgs[3])
        self.assertEqual(code, 2)
        code, out, err = run(self.root, "save", "ART-T-BEAST", str(imgs[3]), "--accept-flags", "--notes", "budget spent; best of four")
        self.assertEqual(code, 0, err)
        rec = json.loads((self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()[-1])
        self.assertEqual((rec["variants_tried"], rec["accepted_at_attempt"]), (4, 4))
        self.assertTrue(any("budget" in t for t in rec["tripwires"]))
        self.assertEqual(len(ha.attempts_of(self.root, "ART-T-BEAST")), 4, "a save does not forget the attempts: the round ends at delivery")

    def test_attempt_count_carries_through_a_redo_before_the_push_and_restarts_after_delivery(self):
        a, b, c = (self.image(f"{n}.png", scale=s) for n, s in (("a", 0.55), ("b", 0.6), ("c", 0.65)))
        self.assertIn("attempt 1 of 3", run(self.root, "check", "ART-T-BEAST", str(a))[1])
        self.assertEqual(save(self.root, "ART-T-BEAST", a)[0], 0)
        # a drift-review redo before the push is the same round: attempt 2, and the receipt says two generations
        self.assertIn("attempt 2 of 3", run(self.root, "check", "ART-T-BEAST", str(b))[1])
        self.assertEqual(save(self.root, "ART-T-BEAST", b)[0], 0)
        rec = json.loads((self.root / "production/art/gpt/RECEIPTS.jsonl").read_text().splitlines()[-1])
        self.assertEqual(rec["variants_tried"], 2)
        self.assertIn("used so far: 2", run(self.root, "show", "ART-T-BEAST")[1])
        # delivered (the intake recorded these bytes), then sent back: a new round
        data = (self.root / "assets/art/incoming/ART-T-BEAST.png").read_bytes()
        (self.root / "production/art").mkdir(parents=True, exist_ok=True)
        sels = {"ART-T-BEAST": {"status": "received", "master": {"sha256": hashlib.sha256(data).hexdigest()}}}
        (self.root / "production/art/SELECTIONS.json").write_text(json.dumps(sels))
        self.assertIn("used so far: 0", run(self.root, "show", "ART-T-BEAST")[1])
        sels["ART-T-BEAST"]["status"] = "rejected"
        (self.root / "production/art/SELECTIONS.json").write_text(json.dumps(sels))
        self.assertIn("attempt 1 of 3", run(self.root, "check", "ART-T-BEAST", str(c))[1])

    def test_a_copy_of_another_image_or_a_reference_is_not_a_new_generation(self):
        first = self.image("first.png")
        self.assertEqual(save(self.root, "ART-T-BEAST", first)[0], 0)
        code, out, err = run(self.root, "check", "ART-T-SCENE", str(first), "--json")
        self.assertTrue(any("byte-identical to assets/art/incoming/ART-T-BEAST.png" in f for f in json.loads(out)["fails"]))
        ref = self.root / "assets/art/style/REF-0.jpg"
        code, out, err = run(self.root, "check", "ART-T-BEAST", str(ref), "--json")
        self.assertTrue(any("byte-identical to assets/art/style/REF-0.jpg" in f for f in json.loads(out)["fails"]))

    def test_a_re_encoded_or_resized_copy_is_flagged_as_a_look_alike(self):
        import io
        first = self.image("first.png")
        self.assertEqual(save(self.root, "ART-T-BEAST", first)[0], 0)
        with Image.open(first) as im:
            buf = io.BytesIO()
            im.convert("RGB").resize((800, 800)).save(buf, "JPEG", quality=60)
        copy = self.tmp / "copy.jpg"
        copy.write_bytes(buf.getvalue())
        hero = queue_item(self.root, "ART-T-HERO")
        d, where = ha.look_alike(self.root, hero, copy)
        self.assertLessEqual(d, ha.LOOKALIKE_MAX)
        self.assertEqual(where, "assets/art/incoming/ART-T-BEAST.png")
        code, out, err = run(self.root, "check", "ART-T-HERO", str(copy), "--json")
        self.assertTrue(any("looks almost identical to assets/art/incoming/ART-T-BEAST.png" in w for w in json.loads(out)["warns"]))
        self.assertIsNone(ha.look_alike(self.root, hero, self.image("scene.png", scene=True)))
        self.assertIsNone(ha.look_alike(self.root, queue_item(self.root, "ART-T-BEAST"), copy), "an item is never its own look-alike")

    def test_status_at_session_end_with_nothing_unsent_says_so(self):
        out = run(self.root, "status", "--end")[1]
        self.assertIn("SESSION END: nothing is unsent", out)
        self.assertIn("Next session: GENERATE next", out)

    def test_bundle_carries_refusals_and_works_with_only_refusals(self):
        self.assertEqual(run(self.root, "refuse", "ART-T-HERO", "--reason", "policy")[0], 0)
        code, out, err = run(self.root, "bundle")
        self.assertEqual(code, 0, err)
        z = next((self.tmp / "scratch").rglob("batch_refusals.zip"))
        lines = zipfile.ZipFile(z).read("receipts_append.jsonl").decode().strip().splitlines()
        self.assertEqual([(json.loads(x)["id"], json.loads(x).get("refused")) for x in lines], [("ART-T-HERO", True)])
        self.assertEqual(save(self.root, "ART-T-BEAST", self.image())[0], 0)
        run(self.root, "bundle")
        z2 = next((self.tmp / "scratch").rglob("batch_ART-T-BEAST__ART-T-BEAST.zip"))
        got = {json.loads(x)["id"] for x in zipfile.ZipFile(z2).read("receipts_append.jsonl").decode().strip().splitlines()}
        self.assertEqual(got, {"ART-T-BEAST", "ART-T-HERO"})

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
        self.assertIsNone(r.get("prompt_sha256"))                # a later real receipt for the same ID replaces it
        code, out, err = run(self.root, "check", "ART-T-BEAST", str(self.image()))
        self.assertIn("recorded as refused", out)
        code, out, err = run(self.root, "refuse", "ART-NOT-QUEUED", "--reason", "x")
        self.assertEqual(code, 2)

    def test_sheet_adds_the_references_of_every_item_on_it(self):
        for iid, kw in (("ART-T-BEAST", {}), ("ART-T-SCENE", {"scene": True})):
            self.assertEqual(save(self.root, iid, self.image(f"{iid}.png", **kw))[0], 0)
        hero = self.tmp / "hero.png"
        figure_image((1024, 1536)).save(hero)
        self.assertEqual(save(self.root, "ART-T-HERO", hero)[0], 0)
        out_sheet = self.tmp / "sheet.jpg"
        code, out, err = run(self.root, "sheet", "--refs", "--out", str(out_sheet))
        self.assertEqual(code, 0, err)
        with Image.open(out_sheet) as sheet:
            # three images plus two distinct references (REF-0 for two items, REF-1 for the hero) = five cells = two rows of four
            self.assertEqual(sheet.height, 2 * (360 + 22))
        code, out, err = run(self.root, "sheet", "--out", str(out_sheet), "ART-T-BEAST")
        self.assertEqual(code, 0, err)
        # nothing saved and no IDs named
        for f in (self.root / "assets/art/incoming").glob("*"):
            f.unlink()
        code, out, err = run(self.root, "sheet")
        self.assertEqual(code, 2)
        self.assertIn("Name the IDs", err)

    def test_bundle_without_git_defaults_to_scratch_and_refuses_the_clone(self):
        for iid in ("ART-T-BEAST", "ART-T-SCENE"):
            self.assertEqual(save(self.root, iid, self.image(f"{iid}.png", scene=iid == "ART-T-SCENE"))[0], 0)
        self.assertIn("BUNDLE", run(self.root, "status", "--end")[1])
        code, out, err = run(self.root, "bundle", "--out", str(self.root / "batch.zip"))
        self.assertEqual(code, 2)
        self.assertIn("outside the repository clone", err)
        self.assertFalse((self.root / "batch.zip").exists())
        code, out, err = run(self.root, "bundle")
        self.assertEqual(code, 0, err)
        z = next((self.tmp / "scratch").rglob("batch_*.zip"))
        names = zipfile.ZipFile(z).namelist()
        self.assertIn("assets/art/incoming/ART-T-BEAST.png", names)
        lines = zipfile.ZipFile(z).read("receipts_append.jsonl").decode().strip().splitlines()
        self.assertEqual({json.loads(x)["id"] for x in lines}, {"ART-T-BEAST", "ART-T-SCENE"})

    def test_without_git_an_image_the_intake_has_recorded_counts_as_sent(self):
        code, out, err = save(self.root, "ART-T-BEAST", self.image())
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
        code, out, err = save(self.root, "ART-T-BEAST", self.image("again.png", scale=0.62))
        self.assertEqual(code, 0, err)                                      # redo needs no --redo flag

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

    def test_item_states_follow_git_history_and_next_action(self):
        root = self.make()
        q = ha.load_queue(root)
        self.assertEqual(set(ha.states(root, q).values()), {"pending"})
        ids = [i["id"] for i in q["items"]]
        for iid, scene in zip(ids, (True, False, False)):
            p = self.tmp / f"{iid}.png"
            if iid == "ART-T-HERO":
                figure_image((1024, 1536)).save(p)
            else:
                (scene_image() if scene else figure_image()).save(p)
            code, out, err = save(root, iid, p)
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
        self.assertEqual(ha.states(root, q)["ART-T-BEAST"], "redo")
        self.assertIn("ART-T-BEAST", run(root, "next")[1])
        code, out, err = save(root, "ART-T-SCENE", self.tmp / "ART-T-BEAST.png")
        self.assertEqual(code, 2, "a delivered, un-rejected item needs --redo")
        # a refusal is its own state, is not offered again, and its receipt must be pushed
        code, out, err = run(root, "refuse", "ART-T-HERO", "--reason", "policy")
        self.assertEqual(code, 0, err)
        self.assertEqual(ha.states(root, q)["ART-T-HERO"], "refused")
        status = run(root, "status")[1]
        self.assertIn("refused=1", status)
        self.assertNotIn("ART-T-HERO", run(root, "next")[1])
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "refusal")
        git(root, "push", "-q", "origin", "main")
        status = run(root, "status")[1]
        self.assertNotIn("COMMIT AND PUSH", status)
        self.assertIn("ART-T-BEAST", status)                       # still 'redo' work first
        (root / "production/art/SELECTIONS.json").write_text("{}")
        self.assertIn("STOP. The anchors are done (1 refused: ART-T-HERO", run(root, "status")[1])
        # a later save replaces the refusal
        p = self.tmp / "retry.png"
        figure_image((1024, 1536), scale=0.6).save(p)
        self.assertEqual(save(root, "ART-T-HERO", p, "--redo")[0], 0)
        self.assertEqual(ha.states(root, q)["ART-T-HERO"], "saved")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "retry")
        git(root, "push", "-q", "origin", "main")
        q2 = json.loads((root / "production/art/gpt/QUEUE.json").read_text())
        q2["phase"] = "batch"
        (root / "production/art/gpt/QUEUE.json").write_text(json.dumps(q2))
        self.assertIn("NOTHING LEFT", run(root, "status")[1])

    def test_status_waits_for_a_batch_before_asking_for_a_push(self):
        root = self.make()
        with mock.patch.object(ha, "BATCH_PUSH_AT", 2):
            self.assertEqual(save(root, "ART-T-SCENE", self._img(scene=True))[0], 0)
            one = run(root, "status")[1]
            self.assertIn("GENERATE next", one)
            self.assertIn("1 saved and not sent yet", one)
            self.assertNotIn("COMMIT AND PUSH", one)
            end = run(root, "status", "--end")[1]
            self.assertIn("DRIFT REVIEW, THEN COMMIT AND PUSH", end)
            self.assertIn("sheet --refs", end)
            self.assertIn("art(gpt): ART-T-SCENE .. ART-T-SCENE", end)
            self.assertIn("git lfs ls-files", end)
            self.assertEqual(save(root, "ART-T-BEAST", self._img())[0], 0)
            two = run(root, "status")[1]
            self.assertIn("COMMIT AND PUSH", two)
            self.assertIn("ART-T-SCENE .. ART-T-BEAST", two)

    def _img(self, scene=False):
        p = self.tmp / f"img{len(list(self.tmp.glob('img*')))}.png"
        (scene_image() if scene else figure_image(scale=0.55 + 0.02 * len(list(self.tmp.glob("img*"))))).save(p)
        return p

    def test_bundle_with_git_uses_unpushed_images(self):
        root = self.make()
        self.assertEqual(save(root, "ART-T-BEAST", self._img())[0], 0)
        code, out, err = run(root, "bundle")
        self.assertEqual(code, 0, err)
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "a")
        git(root, "push", "-q", "origin", "main")
        code, out, err = run(root, "bundle")
        self.assertEqual(code, 2)
        self.assertIn("nothing unsent", err)


class IntakeContract(Isolated):
    def test_helper_files_and_receipts_are_accepted_by_the_real_intake_without_warnings(self):
        """What `save` writes must be exactly what tools/art_intake.py scan expects: a matching prompt hash, no warnings."""
        import argparse
        import art_generate as g, art_gpt_pack as pack, art_intake
        root = self.tmp / "repo"
        (root / "assets/art/incoming").mkdir(parents=True)
        for refs in g.CFG["gpt_reference_sets"]["sets"].values():
            for cand in refs:
                if "/" in cand:
                    (root / cand).parent.mkdir(parents=True, exist_ok=True)
                    figure_image((600, 400)).save(root / cand)        # real images: the intake also processes incoming/ART-BAS-GREYTHORN.jpg
        ents = {e["id"]: e for e in g.entries()}
        queue, prompts = pack.build_queue("anchors", ents, {}, {}, root=root)
        gpt = root / "production/art/gpt"
        (gpt / "prompts").mkdir(parents=True)
        for iid, text in prompts.items():
            (gpt / "prompts" / f"{iid}.txt").write_text(text + "\n")
        (gpt / "QUEUE.json").write_text(json.dumps(queue))
        item = next(i for i in queue["items"] if i["id"] == "ART-MON-GIANT-TARANTULA")
        img = self.tmp / "tarantula.png"
        figure_image((1024, 1024)).save(img)
        code, out, err = save(root, item["id"], img, "--model", "GPT Images 2.5")
        self.assertEqual(code, 0, err + out)
        self.assertEqual(run(root, "refuse", "ART-CLA-FIGHTER", "--reason", "policy")[0], 0)
        with mock.patch.multiple(art_intake, ROOT=root, INCOMING=root / "assets/art/incoming", RECEIPTS=gpt / "RECEIPTS.jsonl",
                                 REVIEW=root / "production/art/review"), \
                mock.patch.multiple(g, INK=root / "assets/art/ink", SELECTIONS=root / "production/art/SELECTIONS.json"):
            with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
                warnings.simplefilter("ignore", ResourceWarning)           # art_intake.scan leaves its own files open
                art_intake.scan(argparse.Namespace())
            sels = g.load(g.SELECTIONS, {})
        s = sels[item["id"]]
        self.assertEqual(s["status"], "received")
        self.assertEqual(s["intake_warnings"], [], "the receipt hash and the aspect must satisfy the intake")
        self.assertEqual(s["prompt_sha256"], item["prompt_sha256"])
        self.assertEqual((s["surface"], s["model"]), ("ChatGPT Work", "GPT Images 2.5"))
        self.assertNotIn("ART-CLA-FIGHTER", sels, "a refusal line is not an image")


class ValidatorCli(unittest.TestCase):
    ZIP = ROOT / "production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip"
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

    @unittest.skipUnless(ZIP.is_file() and (ROOT / "assets/art/style").is_dir(), "needs the zip and the repo images")
    def test_zip_validates_with_the_repo_found_automatically_or_skipped_outside_one(self):
        code, out = self.run_cli("--zip", str(self.ZIP))
        self.assertEqual((code, out["status"], out["repo_checks"]), (0, "PASS", "done"))
        self.assertEqual(Path(out["repo"]), ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.run_cli("--zip", str(self.ZIP), cwd=tmp)
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
