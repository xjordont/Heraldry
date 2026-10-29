"""The figure line-citation remapper must rewrite citations but never dates or URLs."""
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("remap", ROOT / "tools/remap_figure_lines.py")
remap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(remap)


class CitationPattern(unittest.TestCase):
    def test_citations_match(self):
        for text, expected in (("provisions of 13041.", ["13041"]), ("(11086-11088)", ["11086", "11088"]),
                               ("[11092, 11103]", ["11092", "11103"]), ("line 2026 here", ["2026"])):
            with self.subTest(text=text):
                self.assertEqual(re.findall(remap.CITE, text), expected)

    def test_dates_urls_and_decimals_are_left_alone(self):
        for text in ("http://www.w3.org/2000/svg", "pass 2026-10-06:", "size / 1000.0", "v1.2345"):
            with self.subTest(text=text):
                self.assertEqual(re.findall(remap.CITE, text), [])


if __name__ == "__main__":
    unittest.main()
