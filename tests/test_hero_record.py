"""The illustrated Hero record generator (assets/hero-record/sheet.py).

The committed blank sides must equal the generator's output, so the blank and the populated sheets
cannot drift apart, and every B.4 Hero must parse into the sheet's fields. Rendering, fit and
fidelity checks run in `sheet.py heroes` (they need a browser)."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "assets/hero-record"
spec = importlib.util.spec_from_file_location("hero_record_sheet", HERE / "sheet.py")
sheet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sheet)


class BlankIsGenerated(unittest.TestCase):
    def test_committed_blank_sides_match_the_generator(self):
        self.assertEqual((HERE / "hero-record-front.html").read_text(),
                         sheet.page_html("Hero Record, front", sheet.front_body(), HERE),
                         "run `python3 assets/hero-record/sheet.py blank --png`")
        self.assertEqual((HERE / "hero-record-reverse.html").read_text(),
                         sheet.page_html("Hero Record, reverse", sheet.reverse_body(), HERE),
                         "run `python3 assets/hero-record/sheet.py blank --png`")

    def test_no_primary_off_hand_column(self):
        self.assertNotIn("P / O", (HERE / "hero-record-front.html").read_text())


class HeroesParse(unittest.TestCase):
    def test_every_hero_fits_the_fields(self):
        for h in sheet.DATA["heroes"]:
            with self.subTest(hero=h["name"]):
                chest, shield, weapons, inventory = sheet.parse_equipment(h)
                weapons += sheet.natural_weapons(h)
                self.assertLessEqual(len(weapons), 3)
                listed = len(sheet.section(h, "Equipment and Items"))
                self.assertEqual(listed, (chest is not None) + (shield is not None) + len(weapons)
                                 - len(sheet.natural_weapons(h)) + len(inventory), "every item has one place")
                self.assertRegex(h["stats"]["Coins"], r"^\d+c$")
                base_dex, pen, eff_dex, base_spd, eff_spd = sheet.effective(h, chest, shield)
                self.assertEqual(eff_dex, base_dex + min([a["pen"] for a in (chest, shield) if a] or [0]))
                self.assertLessEqual(eff_spd, base_spd)

    def test_effective_values_follow_the_worse_pen_and_lowest_max_speed(self):
        h = next(x for x in sheet.DATA["heroes"] if x["name"] == "Hearthbell")
        chest, shield, _w, _i = sheet.parse_equipment(h)
        # DEX -2; Ring Shirt -2 and Heater Shield -1 do not stack; SPD 4" under Max Speed 6" and 7"
        self.assertEqual(sheet.effective(h, chest, shield), (-2, -2, -4, 4, 4))

    def test_martial_heroes_have_no_powers_and_traits_are_not_repeated(self):
        for h in sheet.DATA["heroes"]:
            powers, talents = sheet.parse_rules(h)
            if h["archetype"] == "Martial":
                self.assertEqual(powers, [], h["name"])
            self.assertFalse([t for t in talents if t["type"] == "Weapon trait"], h["name"])


if __name__ == "__main__":
    unittest.main()
