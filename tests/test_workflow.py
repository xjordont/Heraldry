"""Regression tests for revision safety and failure/currency gates."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from manuscript import ROOT, check, source_path
from revise_manuscript import revise
from figure_dependencies import hashes
from verify import run


class Revisions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in ("source", "config", "editorial"):
            shutil.copytree(ROOT / name, self.root / name)
        self.patch = self.root / "proposal.json"
        self.batch = {"patches": [{"id": "TEST-01", "status": "approved", "find": "A competitive GM-less PvPvE fantasy tabletop miniature skirmish game", "replace": "A competitive GM-less PvPvE fantasy tabletop miniature skirmish game for testing", "expected_count": 1}]}
        self.patch.write_text(json.dumps(self.batch))

    def tearDown(self):
        self.tmp.cleanup()

    def do_revision(self):
        return revise(self.root, self.patch, "Test batch", "Test owner instruction")

    def test_advances_once_and_preserves_every_previous_snapshot(self):
        before = {p.name: p.read_bytes() for p in (self.root / "source").glob("*.md")}
        n = check(self.root)["number"]
        r = self.do_revision()
        self.assertEqual(r["number"], n + 1)
        self.assertEqual(check(self.root), r)
        for name, data in before.items():
            self.assertEqual((self.root / "source" / name).read_bytes(), data)

    def test_rejects_replay_of_archived_batch(self):
        self.do_revision()
        with self.assertRaises(ValueError):
            self.do_revision()

    def test_artwork_changes_do_not_advance_manuscript(self):
        before = check(self.root)
        (self.root / "artwork.svg").write_text("new asset")
        self.assertEqual(check(self.root), before)

    def test_rejects_unversioned_text_edit(self):
        p = source_path(self.root)
        p.write_bytes(p.read_bytes() + b"\nText edit\n")
        with self.assertRaises(ValueError):
            check(self.root)

    def test_rejects_original_snapshot_tamper(self):
        (self.root / "source/Heraldry_RC484.md").write_text("altered")
        with self.assertRaises(ValueError):
            self.do_revision()

    def test_rejects_unapproved_and_noop_and_wrong_match_without_writes(self):
        for change in ({"status": "proposed"}, {"replace": self.batch["patches"][0]["find"]}, {"expected_count": 2}, {"find": "absent phrase"}):
            with self.subTest(change=change):
                b = json.loads(json.dumps(self.batch)); b["patches"][0].update(change)
                self.patch.write_text(json.dumps(b))
                before = check(self.root)
                with self.assertRaises(ValueError):
                    self.do_revision()
                self.assertEqual(check(self.root), before)

    def test_rejects_number_reuse(self):
        n = check(self.root)["number"] + 1
        (self.root / f"source/Heraldry_RC{n}.md").write_text("existing")
        with self.assertRaises(ValueError):
            self.do_revision()

    def test_rejects_patch_evidence_tamper(self):
        r = self.do_revision()
        (self.root / r["patch_file"]).write_text("tampered")
        with self.assertRaises(ValueError):
            check(self.root)

    def test_figure_dependency_hashes_ignore_version_marker_and_follow_relevant_rules(self):
        initial = hashes(self.root)
        self.do_revision()  # subtitle only; outside figure dependencies
        self.assertEqual(hashes(self.root), initial)
        p = source_path(self.root)
        p.write_text(p.read_text().replace("## 3.1 Overview of a Round", "## 3.1 Overview of a Changed Round"))
        self.assertNotEqual(hashes(self.root)["FIG-01"], initial["FIG-01"])
        self.assertEqual(hashes(self.root)["FIG-19"], initial["FIG-19"])


class GateExecution(unittest.TestCase):
    def test_old_pass_report_cannot_mask_crash(self):
        with tempfile.TemporaryDirectory() as d:
            report = Path(d) / "result.json"
            report.write_text('{"status":"PASS"}')
            result = type("Result", (), {"returncode": 1, "stdout": "", "stderr": "crash"})()
            with patch("verify.subprocess.run", return_value=result):
                self.assertEqual(run(["check.py"], report)[0], "FAIL")

    def test_missing_report_cannot_pass(self):
        result = type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        with tempfile.TemporaryDirectory() as d, patch("verify.subprocess.run", return_value=result):
            self.assertEqual(run(["check.py"], Path(d) / "missing.json")[0], "FAIL")

class VisualCurrency(unittest.TestCase):
    def test_rejects_stale_pdf_and_incomplete_page_coverage(self):
        from visual_review_gate import check as visual_check
        from manuscript import sha256
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            q = root / "production/qa"; q.mkdir(parents=True)
            pdf = root / "test.pdf"; pdf.write_bytes(b"current PDF")
            record = {"status": "PASS", "sha256": sha256(pdf), "pages": 2,
                      "pages_reviewed": [1, 2], "reviewer": "test", "reviewed_at": "today"}
            path = q / "visual-review.json"; path.write_text(json.dumps(record))
            visual_check(pdf, 2, root)
            record["pages_reviewed"] = [1]; path.write_text(json.dumps(record))
            with self.assertRaises(ValueError): visual_check(pdf, 2, root)
            record["pages_reviewed"] = [1, 2]; path.write_text(json.dumps(record))
            pdf.write_bytes(b"new PDF")
            with self.assertRaises(ValueError): visual_check(pdf, 2, root)


if __name__ == "__main__":
    unittest.main()
