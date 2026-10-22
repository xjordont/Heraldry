"""Hero cards preserve Appendix B.4 and fit within one US Letter sheet per Hero."""
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

    def test_expanded_blank_has_all_required_fields(self):
        pdf = self.compile("sheet.typ", "expanded")
        reader = PdfReader(str(pdf))
        self.assertEqual(len(reader.pages), 2)
        text = "\n".join(p.extract_text() for p in reader.pages).casefold()
        for label in ("Name", "Ancestry", "Background", "Class", "Level", "STR", "DEX", "INT", "SPI",
                      "Initiative", "Current", "Max", "Temp", "NRG", "Luck", "AP", "Speed", "Size",
                      "Chest", "Shield", "AD", "AV", "Wounds", "Lingering Injuries", "Powers",
                      "Talents and Special Abilities", "Inventory", "Coins", "Fate", "Hero Details"):
            self.assertIn(label.casefold(), text)

    def test_blank_removes_redundancy_and_has_no_grey_inner_boxes(self):
        import pymupdf
        pdf = pymupdf.open(str(self.compile("sheet.typ", "open-fields")))
        self.addCleanup(pdf.close)
        text = "\n".join(p.get_text() for p in pdf)
        for removed in ("Ancestry Traits", "Background Rule", "Ancestry and Background",
                        "Equipped Items", "Carried Items", "Carried Coins", "Party Leader",
                        "Advancement Reference", "Shield AD and AV apply", "Off-Hand: exactly"):
            self.assertNotIn(removed, text)
        self.assertEqual(text.count("Inventory"), 1)
        self.assertEqual(text.count("Ancestry"), 1)
        self.assertEqual(text.count("Background"), 1)
        for page in pdf:
            for drawing in page.get_drawings():
                fill = drawing.get("fill")
                if fill is not None and drawing["rect"].get_area() < page.rect.get_area() * 0.9:
                    paper = (252 / 255, 250 / 255, 245 / 255)
                    is_paper = all(abs(a - b) < 0.002 for a, b in zip(fill, paper))
                    self.assertTrue(max(fill) < 0.01 or min(fill) > 0.99 or is_paper,
                                    "Blank writing areas must not have grey filled boxes")
        portrait = pymupdf.Rect(477, 79, 575, 165)
        self.assertEqual(pdf[0].get_textbox(portrait).strip(), "")
        self.assertFalse(any(pymupdf.Rect(img["bbox"]).intersects(portrait)
                             for img in pdf[0].get_image_info()))

    def test_compiled_set_uses_at_most_one_sheet_per_hero(self):
        reader = PdfReader(str(self.compile("cards.typ", "pack", hero="all")))
        self.assertEqual(len(reader.pages), 48)
        data = json.loads(hero_cards.DATA.read_text(encoding="utf-8"))
        for i, hero in enumerate(data["heroes"]):
            self.assertIn(hero["name"], reader.pages[2 * i].extract_text())
            back = reader.pages[2 * i + 1].extract_text().strip()
            self.assertIn(hero["name"], back, "Every Hero requires a populated reverse")

    def test_every_card_prints_its_whole_profile_clear_of_the_notes(self):
        data = json.loads(hero_cards.DATA.read_text(encoding="utf-8"))
        for hero in data["heroes"]:
            with self.subTest(hero=hero["name"]):
                pdf = self.compile("cards.typ", hero["name"], hero=hero["name"])
                self.assertEqual(hero_cards.card_problems(pdf, hero, data["reminders"], data["notes"]), [])


if __name__ == "__main__":
    unittest.main()
