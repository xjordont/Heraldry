# Hero sheets, party ledger, and Basic Mode hero cards

Owner request, 2026-10-22: a blank, pencil-friendly hero sheet that holds everything the hero creation and campaign chapters ask a player to record, and then the 24 Basic Mode heroes on the same sheet, one hero per printed sheet, with their full rules, room to write, and the book's design.

The sheets belong to the player-aid family ([PLAYER_AIDS.md](PLAYER_AIDS.md)): iron band with chapter arms, Grim Heraldry type, black ink and 5 % tints, the footer with the logo and the rules RC stamp, cream or white US Letter, nothing essential within 27 pt of the trim. Inspiration came from how printed warband and character records are organised (Mordheim's warband roster, Frostgrave's wizard sheet, and hand-drawn Mörk Borg sheets): big boxes for numbers that change, a tick track for advancement, and ruled space for everything else.

## What is printed

All three are two-sided: print duplex, flipping on the long edge.

| File | Side 1 | Side 2 |
| --- | --- | --- |
| Blank hero sheet (`typst/heroes/sheet.typ`) | Name, Senses, Ancestry, Background, Class, Level, Archetype, Primary Casting Score, Max HP per Level, Party Leader, portrait frame; STR, DEX, INT, SPI shields and Initiative Bonus; HP (current, max, Temporary HP), NRG, Luck, SPD, Sz, AP; Chest armour and shield (AD, AV, DEX Pen, Max SPD); 3 Wounds and lingering injuries; weapons (Primary and Off-Hand); the eleven equip slots and the 5 Permanent Special Items | Known Powers; General Talents, Class Talents, and Special Abilities by the level that grants them; the Level 1–10 track with each level's Universal Class Progression gain, Training Cost, and Retirement Payout; carried items, Carried Coins, adventures, and Fate |
| Party ledger (`typst/heroes/ledger.typ`) | Party, Party Leader, campaign type; Roster of 8 with Wounds and Active marks; Hirelings and Animal Companions; the ten Stronghold Components with their Legendary Veterans; Hero deaths and Triumph | Campaign log and Treasury; Storage |
| Basic Mode hero card (`typst/heroes/cards.typ`, 24 of them) | The hero sheet's side 1, filled in from the hero's B.4 profile, its equipment verbatim, the active-Hands rule, the Basic Mode 0 HP rule, and notes | Every other profile rule verbatim (ancestry traits, background rule, talents, Powers, special rules, weapon trait rules, and the Darkvision reminder when the hero has it), then ruled notes |

Sources for side text and sheet labels: § 6.4 (fields), § 6.13 (progression, archetype abilities, Primary and Off-Hand Weapons), § 6.16 (training), § 7.2 and § 7.10 (equip limits, Hands, DEX Pen, shields), § 5.8 (Wounds), § 11.1–11.4 (Roster, Treasury, Storage, Fates, payouts, Hirelings, Stronghold, Legendary Veterans), § 11.5 (solo and cooperative deaths and Triumph), and Appendix B (Basic Mode).

## Fidelity: the cards never retype a rule

`tools/hero_cards.py extract` parses B.4 of the current manuscript into `typst/heroes/basic-heroes.json`. Rules are stored as runs of plain and bold text, exactly as printed. The extractor refuses markup it cannot carry and proves itself: rebuilding Markdown from the JSON reproduces every profile line for line. Archetype, Max HP per Level, and Primary Casting Score come from the class entries in § 6.13. The only computed value is Initiative Bonus (INT + SPI, § 6.4). Senses shows "—" when a profile lists none.

- `python tools/hero_cards.py` (check) fails when the committed JSON no longer matches the manuscript. A revision that changes B.4, the Basic Mode 0 HP paragraph, or a class entry needs `extract` and a look at the affected cards in the same commit. Other revisions leave the JSON unchanged.
- `python tools/hero_cards.py render --paper both [--png]` writes every file to ignored `build/heroes/`, including the 48-page `basic-heroes-<paper>.pdf`. It fails a file that is not exactly two sides per hero. It also fails a card whose PDF text is missing any rule item, sub-item, reminder, or printed statistic, or whose text runs into a ruled notes space.
- `tests/test_hero_cards.py` runs the same checks in `make test`.

## Art

The 24 hero portraits (ART-HER-*) are all rejected in `production/art/SELECTIONS.json`, so each card uses its class's approved ink (ART-CLA-*) in the portrait frame. When hero portraits are approved, change `art` in `tools/hero_cards.py` and re-extract. The blank sheet leaves the frame empty for a sketch or arms.

## Measured (2026-10-22)

52 PDF pages per paper (2 + 2 + 48), all exactly two-sided; smallest text 9 pt; nearest text to the trim 32 pt. The pages were inspected at preview resolution on cream, with spot checks on white. Physical print **NOT TESTED**: check pencil take-up and erasing on the chosen paper, and duplex registration.
