"""A keep audit must not overwrite duplicated or invalid start/end markers."""
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import keep_audit


class KeepMarkerCoverage(unittest.TestCase):
    def run_audit(self, markers):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "build").mkdir()
            (root / "typst").mkdir()
            src = root / "typst/content.typ"
            src.write_text("fixture")
            units = {"content_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
                     "frame_fit_pt": 100,
                     "units": [{"id": "UNIT", "kind": "section", "class": "page",
                                "h1": 10, "h2": 10}]}
            (root / "build/units.json").write_text(json.dumps(units))
            units["expected_unit_ids"] = ["UNIT"]
            units["source_unit_manifest"] = [{"id": "UNIT", "kind": "section"}]
            # Test marker analysis directly. Real exact-PDF binding is covered
            # by test_pdf_position_evidence, not invalid placeholder PDF bytes.
            report = keep_audit.analyze_units(units, {"<um-pos>": markers}, 5)
            return 0 if report["status"] == "PASS" else 1, report

    def test_exact_one_start_end_passes(self):
        rc, report = self.run_audit([{"id": "UNIT", "edge": "s", "page": 3},
                                     {"id": "UNIT", "edge": "e", "page": 3}])
        self.assertEqual(rc, 0)
        self.assertEqual(report["status"], "PASS")

    def test_duplicate_start_fails(self):
        rc, report = self.run_audit([{"id": "UNIT", "edge": "s", "page": 3},
                                     {"id": "UNIT", "edge": "s", "page": 4},
                                     {"id": "UNIT", "edge": "e", "page": 4}])
        self.assertEqual(rc, 1)
        self.assertEqual(report["malformed_markers"][0]["starts"], 2)

    def test_reversed_pages_and_unexpected_unit_fail(self):
        rc, report = self.run_audit([{"id": "UNIT", "edge": "s", "page": 4},
                                     {"id": "UNIT", "edge": "e", "page": 2},
                                     {"id": "OTHER", "edge": "s", "page": 2}])
        self.assertEqual(rc, 1)
        self.assertEqual(len(report["malformed_markers"]), 2)


if __name__ == "__main__":
    unittest.main()
