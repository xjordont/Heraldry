// Expanded record: the one-side operational sheet plus a campaign supplement.
#import "compact.typ": *
#import "hero.typ": GAINS, TRAIN, PAYOUT
#include "compact-sheet.typ"
#record-page("Hero Sheet / campaign reverse", {
  text(font: goth, size: 26pt, weight: 700, "Powers and Progress")
  v(5pt)
  grid(columns: (1fr, 1fr), column-gutter: 12pt,
    write-field("Hero Name", h: 26pt), write-field("Current Level / Adventures", h: 26pt))
  section("Known Powers / continued")
  record-table(("Power / Tradition", "Tier", "AP", "NRG", "Range", "Target / Effect / Duration / Reference"),
    (1.3fr, 29pt, 25pt, 31pt, 39pt, 2.8fr), 3, row: 24pt)
  section("General Talents, Class Talents, and Special Abilities / continued")
  record-table(("Type / Level", "Name", "Effect / Duration / Reference"), (70pt, 1fr, 2fr), 11, row: 18pt)
  section("Advancement Reference / 6.13 and 6.16")
  table(columns: (35pt, 1fr, 50pt, 50pt), inset: (x: 4pt, y: 3pt),
    stroke: (bottom: 0.4pt + pen), align: left + horizon,
    ..("Level", "Gain", "Train", "Retire").map(sheet-label),
    ..range(10).map(i => (str(i + 1), GAINS.at(i), TRAIN.at(i), PAYOUT.at(i))).flatten())
  v(4pt)
  text(size: 9pt)[*Each level:* add Max HP per Level, gain its benefits, learn any class Power, and recalculate Initiative Bonus and Max NRG. Train [1 TAP] in the Town Phase.]
  v(3pt)
  text(size: 9pt)[*Archetype Abilities 1 and 2:* Martial: Martial Supremacy and Sunder. Hybrid: Martial Supremacy and +1 Primary Casting Score. Caster: Caster Supremacy and +4 Max NRG.]
  section("Fate / 11.1.5")
  grid(columns: (1fr, 1fr, 1fr, 1.6fr), column-gutter: 9pt,
    [#check(s: 10pt) Died], [#check(s: 10pt) Retired], [#check(s: 10pt) Triumph], [#check(s: 10pt) Legendary Veteran])
})
