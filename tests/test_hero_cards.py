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
                      "Chest", "Shield", "AD", "AV", "Wounds", "Lingering Injuries", "Known Powers",
                      "Talents and Special Abilities", "Equipped Items", "Carried Items", "Coins", "Fate"):
            self.assertIn(label.casefold(), text)

    def test_field_labels_are_inside_attached_bands(self):
        import pymupdf
        pdf = pymupdf.open(str(self.compile("sheet.typ", "label-bands")))
        page = pdf[0]
        bands = [d["rect"] for d in page.get_drawings()
                 if d.get("fill") is not None and sum(d["fill"]) / len(d["fill"]) < 0.98
                 and d["rect"].get_area() < 6500]
        spans = [s for b in page.get_text("dict")["blocks"] for line in b.get("lines", []) for s in line["spans"]]
        for label in ("Name", "Class", "Ancestry", "Background", "Level", "Casting", "Senses",
                      "Current", "Max", "Temp", "Allowance", "Carried Coins", "Party Leader"):
            matches = [s for s in spans if s["text"].strip() == label]
            self.assertTrue(matches, label)
            for span in matches:
                r = pymupdf.Rect(span["bbox"])
                centre = pymupdf.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
                self.assertTrue(any(centre in band for band in bands), f"Detached field label: {label}")

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
