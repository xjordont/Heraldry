"""Regression tests for PDF-bound Typst page-location evidence."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from page_map_accuracy import analyze
import verify


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

    def test_table_and_figure_marker_pairs_cannot_silently_miss_ends(self):
        good = [{"id": "T327", "edge": "s"}, {"id": "T327", "edge": "e"},
                {"id": "FIG-01", "edge": "s"}, {"id": "FIG-01", "edge": "e"}]
        self.assertEqual(verify.marker_pair_errors(good), {})
        bad = good + [{"id": "T327", "edge": "s"}, {"id": "FIG-02", "edge": "s"}]
        errors = verify.marker_pair_errors(bad)
        self.assertEqual(errors["T327"]["s"], 2)
        self.assertEqual(errors["FIG-02"]["e"], 0)

    def test_pdf_hash_binding_blocks_stale_query(self):
        root = Path(self.dir.name)
        (root / "build").mkdir()
        (root / "typst").mkdir()
        (root / "dist").mkdir()
        content = root / "typst/content.typ"
        content.write_text("current source")
        pdf = root / "dist/Heraldry_RC999_inkjet-borderless.pdf"
        pdf.write_bytes(b"current pdf")
        query = {"substrate": "cream", "edition": "print",
                 "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                 "content_sha256": hashlib.sha256(content.read_bytes()).hexdigest(),
                 "positions": self.positions}
        (root / "build/query.json").write_text(json.dumps(query))
        with patch.object(verify, "ROOT", root), patch.object(verify, "DIST", root / "dist"), \
             patch.object(verify, "version", return_value="RC999"), patch.object(verify, "QUERY_CACHE", None):
            # Matching hashes of a fake PDF and later query are insufficient.
            # Real serialized attachment/anchor checks have separate fixtures.
            with self.assertRaisesRegex(RuntimeError, "serialized PDF evidence"):
                verify.tquery("<tblpos>")
        pdf.write_bytes(b"different pdf")
        with patch.object(verify, "ROOT", root), patch.object(verify, "DIST", root / "dist"), \
             patch.object(verify, "version", return_value="RC999"), patch.object(verify, "QUERY_CACHE", None):
            with self.assertRaisesRegex(RuntimeError, "not bound to the exact cream PDF"):
                verify.tquery("<tblpos>")


if __name__ == "__main__":
    unittest.main()
