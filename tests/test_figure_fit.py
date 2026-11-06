import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import pymupdf  # noqa: E402
from build_book import (BODY_BOTTOM, FIG_FIT_SPACE, FULL_W, MIN_TYPE_PT, TOP_Y,  # noqa: E402
                        compute_figfit, figure_geometry)


class FigureFit(unittest.TestCase):
    """Rulebook-layout skill 1.6: a figure carried to the next page top is set just small enough to fit
    where it began, but never so small that its labels fall under the minimum type size."""

    def proposal(self, need, previous=None):
        fid = "FIG-66"
        aspect, _ = figure_geometry(fid)
        image = aspect * FULL_W
        caption = 50.0
        room = need * image + caption + 2
        end = BODY_BOTTOM - FIG_FIT_SPACE - room
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "book.pdf"
            doc = pymupdf.open()
            first = doc.new_page(width=612, height=792)
            first.draw_rect(pymupdf.Rect(60, 100, 300, end), color=(0, 0, 0))   # the page's last content
            doc.new_page(width=612, height=792)
            doc.save(pdf)
            positions = {"<tblpos>": [{"id": fid, "edge": "s", "page": 2, "x": 45, "y": TOP_Y},
                                      {"id": fid, "edge": "e", "page": 2, "x": 45, "y": TOP_Y + image + caption}]}
            excluded = set()
            return compute_figfit(pdf, positions, previous or {}, {fid}, excluded), excluded

    def test_the_type_floor_sets_how_far_a_figure_may_shrink(self):
        # drawn with 9 pt labels on a 504 pt measure and set at 525 pt: 96% brings them to 9 pt
        _, floor = figure_geometry("FIG-66")
        self.assertAlmostEqual(floor, MIN_TYPE_PT * 504 / (FULL_W * 9), places=3)

    def test_a_figure_that_fits_just_under_full_size_is_scaled_to_fit(self):
        fit, excluded = self.proposal(0.98)
        self.assertAlmostEqual(fit["FIG-66"], 0.98, places=3)
        self.assertEqual(excluded, set())

    def test_below_the_type_floor_the_figure_keeps_its_width(self):
        fit, excluded = self.proposal(0.9)
        self.assertEqual(fit, {})
        self.assertEqual(excluded, {"FIG-66"})

    def test_a_scaled_figure_still_carried_over_goes_back_to_full_size(self):
        fit, excluded = self.proposal(0.98, previous={"FIG-66": 0.98})
        self.assertEqual(fit, {})
        self.assertEqual(excluded, {"FIG-66"})

    def test_a_figure_that_already_shares_its_page_is_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "book.pdf"
            doc = pymupdf.open()
            doc.new_page(width=612, height=792)
            doc.save(pdf)
            positions = {"<tblpos>": [{"id": "FIG-66", "edge": "s", "page": 1, "x": 45, "y": 300},
                                      {"id": "FIG-66", "edge": "e", "page": 1, "x": 45, "y": 700}]}
            self.assertEqual(compute_figfit(pdf, positions, {}, {"FIG-66"}, set()), {})


if __name__ == "__main__":
    unittest.main()
