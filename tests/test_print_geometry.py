"""Cream/white geometric parity must detect layout drift without comparing ink colour."""
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from print_checks import compare_geometry


def make_fixture(filename, *, text_x=72, shape_x=70, link_url="https://example.org"):
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((text_x, 100), "Heraldry Skirmish", fontsize=11)
    page.draw_rect(pymupdf.Rect(shape_x, 120, shape_x + 50, 150), color=(0, 0, 0))
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(70, 85, 150, 105), "uri": link_url})
    doc.save(filename)
    doc.close()


class PrintGeometry(unittest.TestCase):
    def test_matching_page_positions_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "cream.pdf", Path(tmp) / "white.pdf"
            make_fixture(a)
            make_fixture(b)
            with pymupdf.open(a) as ca, pymupdf.open(b) as wh:
                self.assertEqual(compare_geometry(ca[0], wh[0]),
                                 {"text": True, "raster": True, "vector": True, "links": True})

    def test_same_words_different_text_coordinates_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "cream.pdf", Path(tmp) / "white.pdf"
            make_fixture(a)
            make_fixture(b, text_x=90)
            with pymupdf.open(a) as ca, pymupdf.open(b) as wh:
                self.assertFalse(compare_geometry(ca[0], wh[0])["text"])

    def test_vector_and_link_drift_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "cream.pdf", Path(tmp) / "white.pdf"
            make_fixture(a)
            make_fixture(b, shape_x=80, link_url="https://different.example.org")
            with pymupdf.open(a) as ca, pymupdf.open(b) as wh:
                result = compare_geometry(ca[0], wh[0])
                self.assertTrue(result["text"])
                self.assertFalse(result["vector"])
                self.assertFalse(result["links"])


if __name__ == "__main__":
    unittest.main()
