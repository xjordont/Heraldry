"""Regression tests for PDF-bound Typst page-location evidence."""
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from page_map_accuracy import analyze


class PageMapAccuracy(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.pdf = Path(self.dir.name) / "fixture.pdf"
        doc = pymupdf.open()
        for _ in range(5):
            doc.new_page()
        doc.set_toc([[1, "Appendix C. Rules Reference", 1],
                     [2, "C.5 Reactions Summary", 2],
                     [2, "C.6 Critical Hits", 4]])
        doc.save(self.pdf)
        doc.close()
        self.headings = [{"id": "h-appendix-c", "title": "Appendix C. Rules Reference"},
                         {"id": "h-c5-reactions-summary", "title": "C.5 Reactions Summary"},
                         {"id": "h-c6-critical-hits", "title": "C.6 Critical Hits"}]
        self.positions = {"<hpos>": [[{"id": "h-appendix-c", "page": 1},
                                       {"id": "h-c5-reactions-summary", "page": 2},
                                       {"id": "h-c6-critical-hits", "page": 4}]],
                          "<tblpos>": [{"id": "T327", "page": 3, "edge": "s"},
                                       {"id": "T327", "page": 3, "edge": "e"}],
                          "<um-pos>": [{"id": "C.5", "page": 2, "edge": "s"}],
                          "<ixpos>": [{"id": "c5", "page": 2}]}

    def tearDown(self):
        self.dir.cleanup()

    def test_good_bookmark_positions_pass(self):
        result = analyze(self.pdf, self.headings, self.positions)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["headings_corroborated"], 3)

    def test_documented_c5_shift_is_rejected(self):
        self.positions["<hpos>"][0][1]["page"] = 4
        result = analyze(self.pdf, self.headings, self.positions)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["bookmark_page_mismatches"][0]["id"], "h-c5-reactions-summary")

    def test_out_of_range_table_page_is_rejected(self):
        self.positions["<tblpos>"][0]["page"] = 6
        result = analyze(self.pdf, self.headings, self.positions)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["page_bounds_invalid"][0]["id"], "T327")

    def test_empty_outline_is_not_silent_pass(self):
        doc = pymupdf.open(self.pdf)
        doc.set_toc([])
        doc.save(self.pdf, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
        doc.close()
        self.assertEqual(analyze(self.pdf, self.headings, self.positions)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
