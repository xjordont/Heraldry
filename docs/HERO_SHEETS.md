# Expanded Hero records

Owner direction, 2026-10-22: use one consistent expanded record, always one US Letter sheet printed front and back. The owner rejected the preceding mixed one-/two-side draft and its detached headings and writing lines. That version is superseded.

## Current outputs

| File | Printed format |
| --- | --- |
| `hero-sheet-<paper>.pdf` | Blank expanded Hero record, exactly 2 populated sides |
| `hero-<name>-<paper>.pdf` | Each of the 24 Basic Mode Heroes, exactly 2 populated sides |
| `basic-heroes-<paper>.pdf` | All 24 Heroes, exactly 48 populated pages / 24 duplex sheets |
| `party-ledger-<paper>.pdf` | Existing 2-side party ledger, unchanged in this iteration |

`<paper>` is `white` or `cream`. Local PDFs are in ignored `build/heroes/`. There is no current compact one-side output and no padding with empty backs. The retired compact sources have been removed. Print actual size / 100%, Letter portrait, duplex, flipping on the long edge.

## Visual system

`typst/heroes/expanded.typ` defines one field and panel grammar. Every writing field has a closed border, an attached tinted label band, and a dedicated writing area. Major section titles are integrated into their enclosing panels. Shared field edges, a regular 8 pt panel gutter, fixed table columns, and measured panel heights replace the detached labels and loose rules of the rejected draft.

Identity is one connected framed block, including the Hero name, role, class, ancestry, background, level, archetype, casting attribute, HP per Level, Senses, and a framed portrait. Four shield-shaped attribute cells provide the heraldic accent; Initiative, Speed, and Size use corresponding bounded statistic fields. HP, NRG, Luck, and AP have connected labelled cells. Current and maximum values are separate, with Temporary HP separate from both.

The book's existing blackletter is restricted to the Hero name and the reverse title. Source Serif prints fixed values; Source Sans prints labels and rules. Type is at least 9 pt; Basic Mode rules use 10 pt. Artwork is the owner's approved V1 portrait for each Hero, with its proportions preserved. No new art or art approval was created.

## Blank record

The front contains identity, attributes, resources, Chest and Shield armour parameters, Wounds and lingering injuries, 3 weapon rows, ancestry/background/other special ability fields, carried items, coins, and Party Leader status.

The reverse contains 6 Power rows, 11 talent/ability rows, all 11 equipped slots, 5 Permanent Special Item marks, adventures and Fate, and the complete Level 1-10 advancement lookup with gains, Training Costs, Retirement Payouts, and archetype reminders. These are writing capacities, not mechanical limits. Full Power descriptions can be referenced by section when too long for a row.

## Pre-generated Heroes

Every front contains identity and portrait, statistics and trackers, every equipment entry, full shared Basic Mode Hands and 0 HP rules, active Hands fields, carried coins, and a bounded carried-item/change area.

Every reverse contains ancestry traits, the background rule, talents, Powers, special rules, weapon trait rules, applicable Senses reminders, and a bounded Notes area. Dense Heroes receive less space on the reverse and retain the front writing area. Both sides are populated for every Hero, including the shortest profiles.

The renderer retains every B.4 word and emphasis run through the exact extractor in `tools/hero_cards.py`. A long sub-paragraph can continue at a sentence boundary between columns. Its existing text runs are sliced without rewording; the complete original paragraph must remain present in the extracted PDF text. Headings stay with their first entry.

## Reproduction and checks

```text
python tools/hero_cards.py check
python tools/hero_cards.py render --paper both
python tools/hero_sheet_qa.py --render-review
```

The render command rejects anything other than 2 pages for an individual Hero and 48 pages for the full set, and rejects compiler warnings. It audits all profile text, sub-items, statistics, shared notes, front equipment, footer clearance, and the reverse Notes boundary.

The standalone QA checks every redesigned PDF for Letter geometry, minimum type size, essential text safety, font embedding, searchable text, and simulated 1.03 overscan text clipping. It checks cream/white geometry, approved art hashes, and exact agreement between each pack pair and the corresponding individual two-page file. The blank and individual pages are rendered by Poppler for actual visual review. The current receipt is `build/hero-redesign/qa.json`; permanent author observations and exact hashes are recorded separately in `production/qa/hero-sheet-design-review.json`.

`tests/test_hero_cards.py` verifies source extraction, required blank-sheet field categories, exact two-side output, populated pack versos, and complete profile coverage. Run `python tools/dev.py check` before pushing sources.

## Review status

Author review and automated checks do not establish owner aesthetic approval. This iteration remains subject to owner review. Physical printing, handwriting, erasing, and duplex registration are **NOT TESTED**. The current manuscript remains RC513; the published book release remains RC492-build-37. This work does not rebuild or release the book.
