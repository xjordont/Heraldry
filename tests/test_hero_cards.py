"""The Basic Mode Hero data preserves Appendix B.4 exactly."""
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import hero_cards


class HeroCardData(unittest.TestCase):
    def test_extraction_rebuilds_b4_and_matches_committed_data(self):
        rc, sha, lines = hero_cards.current_source()
        doc = hero_cards.build_doc(rc, sha, lines)
        self.assertEqual(len(doc["heroes"]), 24)
        committed = json.loads(hero_cards.DATA.read_text(encoding="utf-8"))
        self.assertEqual(doc, committed, "typst/heroes/basic-heroes.json is stale: run "
                         "`python tools/hero_cards.py extract` and review the Hero record")

    def test_parser_refuses_markup_it_cannot_carry(self):
        with self.assertRaises(ValueError):
            hero_cards.runs("an *italic* phrase")
        with self.assertRaises(ValueError):
            hero_cards.runs("an **unbalanced phrase")
        self.assertEqual(hero_cards.runs("**Mace:** Melee weapon"), [["Mace:", True], [" Melee weapon", False]])


if __name__ == "__main__":
    unittest.main()
