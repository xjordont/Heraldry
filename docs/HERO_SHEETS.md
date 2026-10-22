# Hero sheets, party ledger, and Basic Mode hero cards

Owner request, 2026-10-22: a blank, pencil-friendly hero sheet that holds everything the hero creation and campaign chapters ask a player to record, and then the 24 Basic Mode heroes on the same sheet, one hero per printed sheet, with their full rules, room to write, and the book's design.

## Design (second version, 2026-10-22)

Owner, after the first version: "Ok I think we can do much better. Bette flat out. Better graphic design. More polished professional look. Look online at how good some character sheets look." Studied: the official D&D 2024 sheet (one family of framed panels with shaped corners, heavy outer and fine inner rules, labels set small beneath their lines, iconic circles and shields for the numbers that matter); a hand-drawn Mörk Borg sheet (illustration and blackletter carrying the mood, scroll banners for section titles); and several Shadowdark sheets (strong black title tabs, generous writing space, no clutter). Mordheim's and Frostgrave's rosters informed the party ledger.

The kit (`typst/heroes/parts.typ`) turns those lessons into the book's Grim Heraldry language:

- **Plate:** every panel is an engraved plate with a 1.5 pt outer rule, a 0.5 pt inner rule 2.8 pt inside it, concave notched corners, and a lozenge jewel at each corner.
- **Ribbon:** each plate's title sits in a swallowtail ribbon in blackletter, reversed out of black, across the plate's top edge. Grey hint text is kept to one quiet line at the foot of a plate.
- **Shields, roundels, and lozenges:** ability scores stand in heater shields with the abbreviation reversed out of a black chief. Level, Initiative, SPD, Sz, AP, and each maximum sit in double-ringed roundels. Wounds are outlined lozenges to fill.
- **Arch:** the portrait stands in a pointed gothic arch with the same double rule.
- **Fields and costs:** write-in fields put their label small beneath the line. Printed values on the cards use the book's serif with lining figures and a true minus. A rule's bracketed cost (for example "1 AP, 0 NRG") prints in a black cost tag, word for word.
- **Page:** each page opens with the chapter arms, a blackletter title, a small-caps kicker, and a brush rule, and closes with the series footer. The last plate on each side fills the remaining height with ruled lines, so every side ends cleanly at the footer.

The family otherwise matches the player aids ([PLAYER_AIDS.md](PLAYER_AIDS.md)): black ink, cream or white US Letter, and nothing within 27 pt of the trim.

## What is printed

All three are two-sided: print duplex, flipping on the long edge.

| File | Side 1 | Side 2 |
| --- | --- | --- |
| Blank hero sheet (`typst/heroes/sheet.typ`) | The Hero (Name, Senses, Ancestry, Background, Class, Level, Archetype, Primary Casting Score, Max HP per Level, Party Leader) beside the portrait arch; STR, DEX, INT, and SPI shields and the Initiative roundel; Hit Points (current, Temp, max), Energy, Luck, SPD, Sz, and AP; Armour (Chest and Shield: AD, AV, DEX Pen, and Max SPD); 3 Wounds and lingering injuries; Weapons (Primary and Off-Hand); Carried items and Coins | Known Powers; General Talents, Class Talents, and Special Abilities by the level that grants them; the Level 1–10 track with each level's gain, Training Cost, and Retirement Payout; the eleven Equipped slots with the 5 Permanent Special Items; Fate (adventures, Died, Retired, Legendary Veteran, and Triumph) |
| Party ledger (`typst/heroes/ledger.typ`) | The Party (name, Party Leader, campaign type, Hero deaths, and Triumph); Roster of 8 with Wounds and Active marks; the ten Stronghold Components with their Legendary Veterans and the unassigned Veterans; Notes | Campaign log and Treasury; 8 Hirelings and Animal Companions; Storage |
| Basic Mode hero card (`typst/heroes/cards.typ`, 24 of them) | The hero sheet's side 1, filled in, with the hero's equipment verbatim and ruled space, an Armour panel (Armour Dice, Hands, and Carried Coins), and the Basic Mode panel (active-Hands rule and 0 HP rule) above ruled space | Every other profile rule verbatim in one Rules plate (ancestry traits, background rule, talents, Powers, special rules, weapon trait rules, and the Darkvision reminder when the hero has it), then a ruled Notes plate |

Sources for side text and sheet labels: § 6.4 (fields), § 6.13 (progression, archetype abilities, Primary and Off-Hand Weapons), § 6.16 (training), § 7.2 and § 7.10 (equip limits, Hands, DEX Pen, shields), § 5.8 (Wounds), § 11.1–11.4 (Roster, Treasury, Storage, Fates, payouts, Hirelings, Stronghold, Legendary Veterans), § 11.5 (solo and cooperative deaths and Triumph), and Appendix B (Basic Mode).

## Fidelity: the cards never retype a rule

`tools/hero_cards.py extract` parses B.4 of the current manuscript into `typst/heroes/basic-heroes.json`. Rules are stored as runs of plain and bold text, exactly as printed. The extractor refuses markup it cannot carry and proves itself: rebuilding Markdown from the JSON reproduces every profile line for line. Archetype, Max HP per Level, and Primary Casting Score come from the class entries in § 6.13. The only computed value is Initiative Bonus (INT + SPI, § 6.4). Senses shows "—" when a profile lists none.

- `python tools/hero_cards.py` (check) fails when the committed JSON no longer matches the manuscript. A revision that changes B.4, the Basic Mode 0 HP paragraph, or a class entry needs `extract` and a look at the affected cards in the same commit. Other revisions leave the JSON unchanged.
- `python tools/hero_cards.py render --paper both [--png]` writes every file to ignored `build/heroes/`, including the 48-page `basic-heroes-<paper>.pdf`. It fails a file that is not exactly two sides per hero. It also fails a card whose PDF text is missing any rule item, sub-item, reminder, or printed statistic (ignoring whitespace and the square brackets that cost tags replace), any text that reaches the footer rule, or text that runs into the back's Notes space.
- `tests/test_hero_cards.py` runs the same checks in `make test`.

## Art

The 24 hero portraits (ART-HER-*) are all rejected in `production/art/SELECTIONS.json`, so each card uses its class's approved ink (ART-CLA-*) in the portrait frame. When hero portraits are approved, change `art` in `tools/hero_cards.py` and re-extract. The blank sheet leaves the frame empty for a sketch or arms.

## Measured (2026-10-22, second version)

52 PDF pages per paper (2 + 2 + 48), all exactly two-sided; smallest text 9 pt; nearest text bounding box to the trim 28.3 pt (the title's ascender box). Every side was inspected at preview resolution on cream, with spot checks on white.

Source note for the owner: Nightloom's profile prints "**2 Basic Venom** [1 AP]:" with the cost outside the bold, unlike Silkshade's "**Basic Venom [1 AP]:**". The card reproduces it as printed; a fix would need an approved RC revision. Physical print **NOT TESTED**: check pencil take-up and erasing on the chosen paper, and duplex registration.
