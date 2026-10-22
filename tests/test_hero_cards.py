"""Hero cards stay bound to Appendix B.4, and every hero leaf prints as one duplex sheet."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

from pypdf import PdfReader
import typst

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
                         "`python tools/hero_cards.py extract` and review the hero cards")

    def test_parser_refuses_markup_it_cannot_carry(self):
        with self.assertRaises(ValueError):
            hero_cards.runs("an *italic* phrase")
        with self.assertRaises(ValueError):
            hero_cards.runs("an **unbalanced phrase")
        self.assertEqual(hero_cards.runs("**Mace:** Melee weapon"), [["Mace:", True], [" Melee weapon", False]])


class HeroLeaves(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / "build").mkdir(exist_ok=True)
        cls.tmp = tempfile.TemporaryDirectory(dir=ROOT / "build")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def compile(self, name, stem, **inputs):
        out = Path(self.tmp.name) / f"{stem}.pdf"
        typst.Compiler(str(ROOT / "typst/heroes" / name), root=str(ROOT), font_paths=[str(ROOT / "fonts/static")],
                       ignore_system_fonts=True, sys_inputs={"substrate": "cream", **inputs}).compile(output=str(out))
        return out

    def compile_pages(self, name, **inputs):
        return len(PdfReader(str(self.compile(name, "leaf", **inputs))).pages)

    def test_blank_sheet_and_ledger_are_two_sides(self):
        self.assertEqual(self.compile_pages("sheet.typ"), 2)
        self.assertEqual(self.compile_pages("ledger.typ"), 2)

    def test_every_hero_card_is_two_sides(self):
        self.assertEqual(self.compile_pages("cards.typ", hero="all"), 48)

    def test_every_card_prints_its_whole_profile_clear_of_the_notes(self):
        data = json.loads(hero_cards.DATA.read_text(encoding="utf-8"))
        for hero in data["heroes"]:
            with self.subTest(hero=hero["name"]):
                pdf = self.compile("cards.typ", hero["name"], hero=hero["name"])
                self.assertEqual(hero_cards.card_problems(pdf, hero, data["reminders"]), [])


if __name__ == "__main__":
    unittest.main()
