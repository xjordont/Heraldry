import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from make_index import filing_key  # noqa: E402


class FilingOrder(unittest.TestCase):
    def test_a_leading_the_is_ignored_when_filing(self):
        names = ["Swamp Troll", "The Ancient Void Dragon", "Bandit", "The Voice Beneath the Bells", "Theurgist"]
        self.assertEqual(sorted(names, key=filing_key),
                         ["The Ancient Void Dragon", "Bandit", "Swamp Troll", "Theurgist", "The Voice Beneath the Bells"])

    def test_punctuation_and_case_do_not_move_an_entry(self):
        self.assertEqual(filing_key("Swim (X\")"), filing_key("swim x"))
        self.assertLess(filing_key("Heal / Healing"), filing_key("Heard the Song"))


if __name__ == "__main__":
    unittest.main()
