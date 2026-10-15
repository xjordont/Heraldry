"""A figure review needs actual source bindings and an identified reviewer."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from figure_review_gate import current_hashes, run_gate


class FigureReviewGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.dump("source/versions.json", {"revisions": [{"path": "source/test.md"}]})
        (self.root / "source/test.md").write_text("## 1.1 Test rules\n\nA rule.\n", encoding="utf-8")
        self.dump("figures/manifest.json", [{"id": "FIG-01"}])
        self.dump("figures/placements.json", {"anchor": [{"id": "FIG-01", "caption": "Test caption"}]})
        svg = self.root / "figures/out/FIG-01.svg"
        svg.parent.mkdir(parents=True)
        svg.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.dump("config/figure_dependencies.json", {"FIG-01": ["1.1"]})
        self.review = {"reviewer": "Test reviewer", "reviewed_at": "2026-10-15", "figures": [{
            "id": "FIG-01", **current_hashes(self.root)["FIG-01"], "verdict": "PASS", "findings": [],
        }]}

    def dump(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data), encoding="utf-8")

    def gate(self):
        self.dump("production/qa/figure-semantic-review.json", self.review)
        return run_gate(self.root)

    def test_complete_source_bound_review_passes(self):
        self.assertEqual(self.gate()["status"], "PASS")

    def test_missing_current_and_recorded_rules_hash_cannot_pass(self):
        self.dump("config/figure_dependencies.json", {})
        del self.review["figures"][0]["rules_sha256"]
        report = self.gate()
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("FIG-01", report["stale"])
        self.assertTrue(any("source dependency" in reason for reason in report["figures"][0]["fail_reasons"]))

    def test_reviewer_and_date_are_required(self):
        for field in ("reviewer", "reviewed_at"):
            for value in (None, "", "   "):
                with self.subTest(field=field, value=value):
                    old = self.review[field]
                    self.review[field] = value
                    self.assertEqual(self.gate()["status"], "FAIL")
                    self.review[field] = old

    def test_changed_source_invalidates_review(self):
        (self.root / "source/test.md").write_text("## 1.1 Test rules\n\nChanged rule.\n", encoding="utf-8")
        report = self.gate()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["stale"], ["FIG-01"])


if __name__ == "__main__":
    unittest.main()
