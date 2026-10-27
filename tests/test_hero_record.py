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
                self.assertEqual(eff_dex, base_dex + sum(a["pen"] for a in (chest, shield) if a))
                self.assertLessEqual(eff_spd, base_spd)

    def test_effective_values_add_pens_and_follow_the_lowest_max_speed(self):
        h = next(x for x in sheet.DATA["heroes"] if x["name"] == "Hearthbell")
        chest, shield, _w, _i = sheet.parse_equipment(h)
        # DEX -2; Ring Shirt -2 and Heater Shield -1 add to -3; SPD 4" under Max Speed 5" and 6"
        self.assertEqual(sheet.effective(h, chest, shield), (-2, -3, -5, 4, 4))
        self.assertEqual((chest["spd"], shield["spd"]), (5, 6))

    def test_martial_heroes_have_no_powers_and_traits_are_not_repeated(self):
        for h in sheet.DATA["heroes"]:
            powers, talents = sheet.parse_rules(h)
            if h["archetype"] == "Martial":
                self.assertEqual(powers, [], h["name"])
            self.assertFalse([t for t in talents if t["type"] == "Weapon trait"], h["name"])


def _active_manuscript():
    import json
    v = json.loads((ROOT / "source/versions.json").read_text(encoding="utf-8"))
    rev = next(r for r in v["revisions"] if r["number"] == v["current"])
    return (ROOT / rev["path"]).read_text(encoding="utf-8").split("\n")


def _table(lines, first_header):
    import re
    i = next(k for k, l in enumerate(lines) if l.startswith(first_header))
    hdr = [c.strip() for c in lines[i].strip("|").split("|")]
    rows, j = {}, i + 2
    while j < len(lines) and lines[j].startswith("|"):
        r = dict(zip(hdr, [c.strip() for c in lines[j].strip("|").split("|")]))
        rows[re.sub(r"\s*\(.*\)", "", r[hdr[0]]).strip()] = r
        j += 1
    return rows


class B4GearMatchesTheEquipmentTables(unittest.TestCase):
    """A B.4 profile is used in isolation, so its gear must agree with 7.8-7.12 (Hands, damage die,
    traits, AD, DEX Pen, Max Speed), and every item a Hero can use must meet its requirements."""

    @classmethod
    def setUpClass(cls):
        lines = _active_manuscript()
        cls.weapons = {**_table(lines, "| Weapon | Cost (c) | Hands | STR Req | DEX Req | Damage"),
                       **_table(lines, "| Weapon | Cost (c) | Hands | Range")}
        cls.armour = _table(lines, "| Armour | Cost (c) | AD")
        cls.shields = _table(lines, "| Shield | Cost (c) | AD")

    def weapon(self, name):
        import re
        base = re.sub(r"^(Elven|Masterwork) ", "", re.sub(r" \(\d+\)$", "", name))
        return self.weapons.get(base) or next(v for k, v in self.weapons.items() if k.startswith(base) or base.startswith(k))

    def test_weapons_armour_and_shields(self):
        import re
        req = lambda v: None if v in ("-", "") else int(v)
        for h in sheet.DATA["heroes"]:
            sc = {k: int(v) for k, v in h["scores"].items()}
            chest, shield, weapons, _inv = sheet.parse_equipment(h)
            for w in weapons:
                with self.subTest(hero=h["name"], weapon=w["name"]):
                    t = self.weapon(w["name"])
                    self.assertEqual(w["hands"], t["Hands"], "Hands")
                    self.assertEqual(w["damage"].split(" ")[0], t["Damage"].split(" ")[0], "damage die")
                    listed = {x.strip() for x in w["traits"].split(",") if x.strip() and not x.startswith("Carried")}
                    table = set(re.findall(r"\*\*(\w+)\*\*", t["Traits"])) - {"Ranged"}
                    if listed:
                        self.assertEqual(listed - {"Elven", "Masterwork"}, table, "traits")
                    if not w["traits"].startswith("Carried"):
                        s, d = req(t.get("STR Req", "-")), req(t.get("DEX Req", "-"))
                        if d is not None and w["name"].startswith("Elven "):
                            d = d - 1 if d > 1 else None
                        self.assertTrue((s is None or sc["STR"] >= s) and (d is None or sc["DEX"] >= d), "requirements")
            for a, tab in ((chest, self.armour), (shield, self.shields)):
                if a:
                    with self.subTest(hero=h["name"], armour=a["name"]):
                        t = tab[a["name"]]
                        self.assertEqual((a["ad"], a["pen"], f'{a["spd"]}"'), (t["AD"], int(t["DEX Pen"]), t["Max Speed"]))
                        s = req(t["STR Req"])
                        self.assertTrue(s is None or sc["STR"] >= s, "STR requirement")


if __name__ == "__main__":
    unittest.main()
