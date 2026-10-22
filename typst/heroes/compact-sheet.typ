#import "compact.typ": *

#record-page("Compact Hero Sheet / one side", {
  // A working record, with the full progression lookup retained in sheet.typ.
  grid(columns: (1fr, auto), column-gutter: 10pt, align: horizon,
    text(font: goth, size: 27pt, weight: 700, "Hero Record"), arms(6, w: 27pt))
  v(2pt)
  grid(columns: (2fr, 1fr, 1fr, 1fr), column-gutter: 10pt,
    write-field("Name", h: 30pt), write-field("Ancestry", h: 30pt),
    write-field("Background", h: 30pt), write-field("Class", h: 30pt))
  v(6pt)
  grid(columns: (40pt, 1fr, 1fr, 1fr, 1fr), column-gutter: 10pt,
    write-field("Level"), write-field("Archetype"), write-field("Casting Score"),
    write-field("HP per Level"), write-field("Senses"))
  v(7pt)
  attribute-strip(none)
  v(6pt)
  resource-strip(none)
  v(4pt)
  grid(columns: (1fr, 145pt), column-gutter: 12pt,
    {
      section("Armour")
      record-table(("Slot", "Item", "AD", "AV", "DEX Pen", "Max SPD"),
        (36pt, 1fr, 29pt, 29pt, 45pt, 47pt), 2, row: 19pt, first: ("Chest", "Shield"))
      v(3pt)
      text(size: 9pt, "Shield AD and AV only through Block. Use only the worse DEX Pen.")
    },
    {
      section("Wounds and Injuries")
      ticks(3, s: 13pt, gap: 7pt)
      v(4pt)
      write-field("Lingering Injuries", h: 34pt)
    })
  section("Weapons")
  record-table(("P/O", "Weapon", "Hands", "Damage and Type", "Range", "Traits"),
    (27pt, 1.2fr, 37pt, 1.2fr, 39pt, 1.5fr), 3, row: 19pt)
  v(3pt)
  text(size: 9pt, "P = Primary. O = Off-Hand: exactly 1 base damage die. See 6.13.")
  section("Known Powers")
  record-table(("Power / Tradition", "Tier", "AP", "NRG", "Range", "Target / Effect / Duration / Reference"),
    (1.3fr, 29pt, 25pt, 31pt, 39pt, 2.8fr), 4, row: 20pt)
  grid(columns: (1fr, 1fr), column-gutter: 12pt,
    {
      section("Talents and Special Abilities")
      record-table(("General / Class / Special", "Effect / Reference"), (1fr, 1.6fr), 4, row: 20pt)
    },
    {
      section("Equipped and Carried")
      grid(columns: (1fr, 1fr, 1fr), column-gutter: 7pt,
        ..("Chest", "Head", "Back", "Neck", "Waist", "Arms", "Feet", "Ring", "Ring", "Hand", "Hand", "Coins").map(s => write-field(s, h: 23pt)))
      v(3pt)
      write-field("Other Carried Items", h: 25pt)
    })
  v(4pt)
  grid(columns: (1fr, 1fr), column-gutter: 12pt,
    {
      sheet-label("Permanent Special Items "); ticks(5, s: 9pt, gap: 3pt)
      v(4pt)
      write-field("Adventures / Fate", h: 24pt)
    },
    {
      sheet-label("Party Leader "); check(s: 10pt)
      v(4pt)
      text(size: 9pt, "Progression: 6.13 and 6.16. Fates: 11.1.5.")
    })
})
