"""The offline ChatGPT Work input package: build, verify, and the whole runner loop without Git credentials.

The images here are synthetic stand-ins drawn by the test. They exercise the mechanics (hashes, QA binding,
receipts, bundle, reviewer check) and say nothing about the image tool or artistic quality."""
import json
import unittest, os, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
import art_work_package as awp  # noqa: E402
from test_art_skill import figure_image, scene_image  # noqa: E402

SCRIPTS = awp.SCRIPTS
QUEUE = json.loads((ROOT / awp.QUEUE).read_text())


@unittest.skipUnless((ROOT / ".git").exists(), "needs the repository checkout")
class OfflineRun(unittest.TestCase):
    """Build a package, then play Work: unpack it in a folder with no Git and no credentials and run the loop."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp = Path(cls._tmp.name)
        cls.zip = cls.tmp / "input.zip"
        with open(os.devnull, "w") as null:
            import contextlib
            with contextlib.redirect_stdout(null):
                try:
                    assert awp.main(["build", "--out", str(cls.zip), "--allow-dirty"]) == 0
                except SystemExit as e:
                    # A checkout without LFS image bytes (CI) cannot build the package. Skip instead of
                    # letting SystemExit end the whole test run, as the other image-dependent tests do.
                    if "Git LFS pointer" in str(e):
                        cls._tmp.cleanup()
                        raise unittest.SkipTest(f"needs the repo images (LFS): {e}")
                    raise

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_build_is_deterministic_and_self_describing(self):
        again = self.tmp / "again.zip"
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            awp.main(["build", "--out", str(again), "--allow-dirty"])
        self.assertEqual(again.read_bytes(), self.zip.read_bytes())
        with zipfile.ZipFile(self.zip) as z:
            man = json.loads(z.read("WORK_PACKAGE.json"))
            self.assertIn("START_HERE.md", z.namelist())
        self.assertEqual(man["queue"]["ids"], [i["id"] for i in QUEUE["items"]])
        for p in man["prompts"]:
            self.assertTrue(p["verified_against_queue"])
        self.assertEqual({r["path"] for r in man["references"]}, {r for it in QUEUE["items"] for r in it["references"]})
        for r in man["references"]:
            self.assertIn(r["format"], ("JPEG", "PNG"))

    def test_package_lists_every_queue_reference_the_skill_zip_and_no_private_material(self):
        with zipfile.ZipFile(self.zip) as z:
            names = set(z.namelist())
            man = json.loads(z.read("WORK_PACKAGE.json"))
        for it in QUEUE["items"]:
            self.assertIn(it["prompt"], names)
            for r in it["references"]:
                self.assertIn(r, names)
        self.assertIn(awp.SKILL_ZIP, names)
        self.assertFalse([n for n in names if n.lower().endswith(".pdf") or n.startswith("references/")])
        self.assertFalse([n for n in names if n.startswith("assets/") and n not in {r for it in QUEUE["items"] for r in it["references"]}])
        self.assertEqual(len(man["source"]["commit"]), 40)
        self.assertEqual(man["delivery"]["route"], "bundle")

    def test_verify_passes_without_git_credentials(self):
        r = awp.verify(self.zip)
        self.assertEqual(r["status"], "PASS", json.dumps(r, indent=1))
        pre = json.loads(r["tools"]["work_preflight --offline-package --require-installed"]["stdout"])
        self.assertEqual((pre["source"]["kind"], pre["delivery"], pre["git"], pre["origin_main_access"]), ("offline_package", "bundle", False, False))
        self.assertIn("NOT_ATTEMPTED", pre["remote_access"])
        self.assertEqual(pre["image_and_reference_tool"], "UNVERIFIED")
        self.assertIn("offline Work input package", r["tools"]["delivery_guard audit (must refuse: no Git)"]["stderr"])

    def unpack(self, name):
        d = self.tmp / name
        awp.safe_extract(self.zip, d)
        home = self.tmp / (name + "-home")
        (home / "scratch").mkdir(parents=True)
        return d, home, awp.offline_env(home)

    def sh(self, pkg, env, *args):
        return subprocess.run([sys.executable, *args], cwd=pkg, env=env, capture_output=True, text=True, timeout=300)

    @unittest.skipUnless(QUEUE["items"], "the live queue is empty (all illustrations approved); this check needs queued items")
    def test_tampering_is_caught(self):
        pkg, home, env = self.unpack("tampered")
        ref = next((it["references"][-1] for it in QUEUE["items"] if it["references"]), None)   # any queue size
        if ref:              # a queue of no-reference items (owner 2026-10-31) has no reference to tamper with
            (pkg / ref).write_bytes(b"version https://git-lfs.github.com/spec/v1\noid sha256:" + b"0" * 64 + b"\nsize 1\n")
        prompt = pkg / QUEUE["items"][-1]["prompt"]
        prompt.write_text(prompt.read_text() + "extra\n")
        r = self.sh(pkg, env, f"{SCRIPTS}/work_preflight.py", "--repo", ".", "--offline-package")
        d = json.loads(r.stdout)
        self.assertEqual(d["status"], "BLOCKED")
        joined = " ".join(d["errors"])
        if ref:
            self.assertIn(ref, joined)
        self.assertIn("prompt hash mismatch", joined)

    @unittest.skipUnless(QUEUE["items"], "the live queue is empty (all illustrations approved); this check needs queued items")
    def test_five_anchors_check_save_bundle_and_review_check(self):
        pkg, home, env = self.unpack("work")
        h = f"{SCRIPTS}/heraldry_art.py"
        scratch = home / "work"
        scratch.mkdir()
        items = QUEUE["items"][:5]                               # a session's worth; the batch queue is long
        for n, it in enumerate(items):
            w, hgt = (int(x) for x in it["size"].split("x"))
            img = scratch / f"{it['id']}.png"
            im = scene_image((w, hgt)) if it["register"] == "scene" else figure_image((w, hgt), scale=0.6 + 0.03 * n)
            from PIL import ImageDraw
            ImageDraw.Draw(im).ellipse((w // 2 - 20 - 6 * n, hgt // 2 - 20, w // 2 + 20, hgt // 2 + 20 + 6 * n), outline=(0, 0, 0), width=4)
            im.save(img)                                         # each stand-in unique: the copy check is real
            r = self.sh(pkg, env, h, "check", it["id"], str(img), "--json")
            self.assertIn(json.loads(r.stdout)["result"], ("PASS", "WARN"), r.stdout + r.stderr)
            qa = scratch / f"{it['id']}.qa.json"
            refs = sum((["--reference", x] for x in it["references"]), [])
            r = self.sh(pkg, env, f"{SCRIPTS}/fidelity_gate.py", "create", it["id"], str(img), "--prompt-sha", it["prompt_sha256"], *refs, "--out", str(qa))
            self.assertEqual(r.returncode, 0, r.stderr)
            rec = json.loads(qa.read_text())
            rec.update(prompt_unchanged=True, references_attached=True, visual_review_at_print_size=True,
                       register_compared="scene" if it["register"] == "scene" else "figure")
            for k in rec["checks"]:
                rec["checks"][k] = {"pass": True, "evidence": f"synthetic test stand-in, mechanics only: {k}"}
            qa.write_text(json.dumps(rec))
            flags = sum((["--must", "test stand-in, counted as listed: " + m] for m in it["must"]), [])
            flags += ["--avoid-clear"] if it["avoid"] else []
            r = self.sh(pkg, env, h, "save", it["id"], str(img), "--qa-file", str(qa), *flags)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        whole = len(items) == len(QUEUE["items"])
        r = self.sh(pkg, env, h, "status", *([] if whole else ["--end"]))   # session end asks to deliver what is saved
        self.assertIn("BUNDLE", r.stdout)
        self.assertEqual(self.sh(pkg, env, f"{SCRIPTS}/delivery_guard.py", "audit", "--repo", ".").returncode, 2)
        sheet = scratch / "sheet.jpg"
        self.assertEqual(self.sh(pkg, env, h, "sheet", "--refs", "--out", str(sheet)).returncode, 0)
        out = self.tmp / "review.zip"
        r = self.sh(pkg, env, h, "bundle", "--out", str(out), "--evidence", str(sheet))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Nothing was pushed", r.stdout)
        r = self.sh(pkg, env, h, "status")
        if whole and QUEUE["phase"] == "anchors":
            self.assertIn("STOP", r.stdout)
            self.assertIn("anchors are done", r.stdout)
        elif not whole:
            self.assertIn("GENERATE", r.stdout)                  # the next session resumes from status
        # The package's own preflight still passes: only receipts grew, and saved images are expected extras.
        d = json.loads(self.sh(pkg, env, f"{SCRIPTS}/work_preflight.py", "--repo", ".", "--offline-package").stdout)
        self.assertEqual(d["status"], "READY", d)
        with zipfile.ZipFile(out) as z:
            names = set(z.namelist())
            man = json.loads(z.read("BUNDLE_MANIFEST.json"))
        for it in items:
            self.assertIn(f"assets/art/incoming/{it['id']}.png", names)
            self.assertIn(f"review_evidence/qa/{it['id']}.qa.json", names)
        self.assertIn("review_evidence/sheet.jpg", names)
        self.assertIs(man["pushed_to_github"], False)
        self.assertEqual(man["source"]["kind"], "offline_package")
        self.assertIn("NOT APPROVED", man["approval"])
        v = awp.verify_bundle(out)
        self.assertEqual(v["status"], "PASS", json.dumps(v, indent=1))
        # A swapped image is caught by the reviewer check.
        first = QUEUE["items"][0]
        fw, fh = (int(x) for x in first["size"].split("x"))
        swap = scratch / "swap.png"
        figure_image((fw, fh), scale=0.45).save(swap)
        bad = self.tmp / "bad.zip"
        with zipfile.ZipFile(out) as src, zipfile.ZipFile(bad, "w") as dst:
            for n in src.namelist():
                data = src.read(n)
                if n.endswith(f"{first['id']}.png"):
                    data = swap.read_bytes()
                dst.writestr(n, data)
        self.assertEqual(awp.verify_bundle(bad)["status"], "FAIL")
        # The import workflow's step, against a fresh copy of the package standing in for the repository.
        root = self.tmp / "import-root"
        awp.safe_extract(self.zip, root)
        before = (root / "production/art/gpt/RECEIPTS.jsonl").read_text()
        r = awp.import_bundle(out, root)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(r["receipts_added"], len(items))
        for it in items:
            self.assertEqual((root / f"assets/art/incoming/{it['id']}.png").read_bytes(), (pkg / f"assets/art/incoming/{it['id']}.png").read_bytes())
        self.assertTrue((root / "production/art/gpt/RECEIPTS.jsonl").read_text().startswith(before))
        self.assertEqual(awp.import_bundle(out, root)["receipts_added"], 0)          # idempotent
        self.assertEqual(awp.import_bundle(bad, root)["status"], "FAIL")

    @unittest.skipUnless(QUEUE["items"], "the live queue is empty (all illustrations approved); this check needs queued items")
    def test_bundle_refuses_a_qa_report_changed_after_save(self):
        pkg, home, env = self.unpack("qa-changed")
        it = next((i for i in QUEUE["items"] if i["register"] != "scene"), QUEUE["items"][0])
        w, hgt = (int(x) for x in it["size"].split("x"))
        img = home / "x.png"
        figure_image((w, hgt)).save(img)
        qa = home / "x.qa.json"
        self.sh(pkg, env, f"{SCRIPTS}/fidelity_gate.py", "create", it["id"], str(img), "--prompt-sha", it["prompt_sha256"],
                *sum((["--reference", x] for x in it["references"]), []), "--out", str(qa))
        rec = json.loads(qa.read_text())
        rec.update(prompt_unchanged=True, references_attached=True, visual_review_at_print_size=True, register_compared="figure")
        for k in rec["checks"]:
            rec["checks"][k] = {"pass": True, "evidence": f"synthetic test stand-in, mechanics only: {k}"}
        qa.write_text(json.dumps(rec))
        self.sh(pkg, env, f"{SCRIPTS}/heraldry_art.py", "check", it["id"], str(img))
        flags = sum((["--must", "test stand-in, counted as listed: " + m] for m in it["must"]), [])
        flags += ["--avoid-clear"] if it["avoid"] else []
        r = self.sh(pkg, env, f"{SCRIPTS}/heraldry_art.py", "save", it["id"], str(img), "--qa-file", str(qa), *flags)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        qa_copy = next((home / "scratch").rglob(f"qa/{it['id']}.qa.json"))
        qa_copy.write_text(qa_copy.read_text().replace("mechanics only", "edited later"))
        r = self.sh(pkg, env, f"{SCRIPTS}/heraldry_art.py", "bundle")
        self.assertEqual(r.returncode, 2)
        self.assertIn("changed since `save`", r.stderr)


if __name__ == "__main__":
    unittest.main()
