"""Cream/white geometric parity must detect layout drift without comparing ink colour."""
import sys
import io
import tempfile
import unittest
from pathlib import Path

import pymupdf
from PIL import Image

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
    def test_same_bounds_different_vector_path_is_rejected(self):
        with pymupdf.open() as a, pymupdf.open() as b:
            pa, pb = a.new_page(), b.new_page()
            pa.draw_line((100, 100), (150, 150))
            pb.draw_line((100, 150), (150, 100))
            self.assertFalse(compare_geometry(pa, pb)["vector"])

    def test_same_bounds_different_image_bytes_are_rejected(self):
        with pymupdf.open() as a, pymupdf.open() as b:
            for document, colour in ((a, "black"), (b, "white")):
                page = document.new_page()
                stream = io.BytesIO()
                Image.new("RGB", (10, 10), colour).save(stream, format="PNG")
                page.insert_image(pymupdf.Rect(100, 100, 150, 150), stream=stream.getvalue())
            self.assertFalse(compare_geometry(a[0], b[0])["raster"])

    def test_subpoint_export_noise_is_tolerated(self):
        with pymupdf.open() as a, pymupdf.open() as b:
            pa, pb = a.new_page(), b.new_page()
            pa.insert_text((72, 100), "Readable rules", fontsize=10.5)
            pb.insert_text((72.005, 100), "Readable rules", fontsize=10.5)
            self.assertTrue(compare_geometry(pa, pb)["text"])

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
