# Hero sheets and Basic Mode Hero records

The 2026-10-22 redesign follows the owner's request for a scrutinized, research-led, compact US Letter sheet. The comparative evidence, close audit of the previous design, and page-shape decision are in [HERO_SHEET_RESEARCH.md](HERO_SHEET_RESEARCH.md). Current rules authority is RC513; no manuscript text changed.

## Choose a record

| Output | Size | Use |
| --- | --- | --- |
| `hero-sheet-compact-<paper>.pdf` | 1 portrait Letter side | Operational blank record: identity, statistics, resources, armour, weapons, Powers, abilities, equipment, Wounds, injuries, and campaign fields |
| `hero-sheet-<paper>.pdf` | 2 portrait Letter sides | Same front plus more Powers and ability space, complete Level 1-10 advancement reference, Training Costs, Retirement Payouts, and Fate |
| `hero-<name>-<paper>.pdf` | 1 or 2 portrait Letter sides | One pre-generated Basic Mode Hero with all of its B.4 rules, shared Hands/0 HP rules, sense reminder if applicable, approved V1 portrait, and writing space |
| `basic-heroes-<paper>.pdf` | 48 pages / 24 duplex sheets | Print pack. One-sided Heroes have deliberately empty versos, so every Hero begins on a new sheet |
| `party-ledger-<paper>.pdf` | 2 sides | Existing party resource record; its layout was not redesigned in this pass |

`<paper>` is `cream` or `white`. Outputs live in ignored `build/heroes/`; built PDFs are never committed. This is local player-sheet work, not a full-book build or a new published release.

The compact blank has 3 weapon rows, 4 Power rows, and 4 ability rows. The expanded reverse adds 3 Power rows and 11 ability rows, retaining the full reference that was printed in the previous sheet. The compact sheet is a finite working record, not a promise that an arbitrarily long custom spell description or inventory will fit. Use the expanded record when more space is needed. Handwriting and erasing comfort still require a physical trial.

## Design

The new `typst/heroes/compact.typ` uses the existing book fonts, selected substrates, and black ink. Blackletter and approved illustration identify the Hero; clear sans serif labels, consistent statistic order, single rules, aligned table columns, and open resource fields do the reference work. Repeated plate borders, ribbons, double roundels, and the large portrait arch are removed from these Hero records. The separate party ledger still uses the previous kit.

Current and maximum HP, NRG, and Luck are explicit. Temporary HP is separate. AP allowance and current AP are distinct. Active Hands and carried coins have write-in fields. Chest and Shield retain separate AD/AV parameters and the Block restriction. Compact blank equipment includes all eleven slots and the five Permanent Special Item marks; shared Treasury and Storage remain on the party ledger.

Pre-generated rules use 9.5 pt text with 9 pt labels, costs retain brackets, and no profile prose is summarized. The one-side fit is measured at the actual column width and font settings. If it does not fit, the renderer chooses a paragraph/item boundary across two sides. It also measures column boundaries so a sentence is not split between columns. A heading stays with its first entry. Equipment, shared Hands rules, and Basic Mode 0 HP rules stay on the front. Long profiles have substantial ruled room on both sides.

Individual files: 8 Heroes use one side, and 16 use two. One-sided: Sootfinger, Hearthbell, Starcinder, Oathscale, Dawnwarden, Thoughtwake, Ashborn, and Crowwick. A source or typography change can change this measured allocation; the renderer must fail if any Hero exceeds two sides.

## Source fidelity and art

`tools/hero_cards.py extract` deterministically parses B.4 into `typst/heroes/basic-heroes.json`, retaining every rule, value, sub-item, and bold run. Reconstructing the Markdown must reproduce each profile line for line. Archetype, HP per Level, and casting attribute come from the class entries; Initiative is INT + SPI. `check` rejects stale extracted data. Extraction writes stable LF newlines on Windows and POSIX.

The art selector now uses `ART-HER-<NAME>`, matching the owner's approved V1 selections from 2026-10-22. Original portrait proportions are preserved. No new art was generated and no approval status changed. `tools/hero_sheet_qa.py` requires each selected ink to be approved and to match its recorded SHA-256.

## Render and verify

```text
python tools/hero_cards.py check
python tools/hero_cards.py render --paper both --png
python tools/hero_sheet_qa.py --render-review
```

Use `--only hero-sheet-compact hero-sheet Crowwick Mossgrave` for a bounded specimen. `render` checks page count, refuses compiler warnings, and audits each individual Hero PDF for all rules, sub-items, values, sense reminders, and shared Basic Mode notes. It also checks the Notes boundary and footer clearance. The combined pack must contain exactly 48 pages.

`hero_sheet_qa.py` audits every individual and combined output with the existing Letter preflight: page boxes, orientation, at least 9 pt type, 27 pt essential text safety, embedded fonts, searchable text, and centred 1.03 overscan text clipping. It compares cream and white text/geometry and checks every pack front/reverse against the matching individual file, including blank versos. `--render-review` uses Poppler to produce all-page images and contact sheets in ignored `build/hero-redesign/review/`. The exact PDF and image hashes, source hash, selected art hashes, and design input hashes are recorded in `build/hero-redesign/qa.json`. This mechanical receipt does not approve visual quality.

`tests/test_hero_cards.py` checks exact profile extraction, markup refusal, all required compact-sheet categories, page limits, every profile's printed coverage, and the combined pack's Hero-to-sheet mapping. The full repository check remains required before a source push.

## Print and review limits

Print at actual size / 100%, US Letter, portrait, one PDF page per side. Use the white version for the lowest background ink. Print the 48-page pack duplex, flipping on the long edge; the intentional blank backs keep all 24 Heroes on separate sheets. Individual one-page files print one-sided. The expanded blank prints duplex, flipping on the long edge. First test the driver's duplex direction on a small batch.

Working margins are 32 pt horizontally, 40 pt at the top, and 50 pt at the bottom, with the footer in the bottom margin. Verify actual glyph bounds rather than treating those frame coordinates as evidence. A borderless driver can still enlarge a page; the overscan test is a conservative simulated crop, not a measurement of a particular printer.

The graphic review is by the same Codex author who made the changes. It is not independent player testing, comprehensive tagged-PDF accessibility testing, a full-book review, or a physical proof. Physical print remains **NOT TESTED**. Last published book PDFs remain RC492-build-37.
