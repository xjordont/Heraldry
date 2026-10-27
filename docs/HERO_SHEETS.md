# Expanded Hero records

Owner direction, 2026-10-22: use one consistent expanded record, always one US Letter sheet printed front and back. The owner rejected the preceding mixed one-/two-side draft and its detached headings and writing lines. That version is superseded.

Latest direction: finish the blank record before adapting Basic Mode Heroes. The blank now imports the book's type and marks directly, removes nested frames and grey writing fields, merges equipped and carried possessions into one Inventory, and removes reminders. Basic Mode PDFs and their template remain at the preceding checkpoint.

## Current outputs

| File | Printed format |
| --- | --- |
| `hero-sheet-<paper>.pdf` | Blank expanded Hero record, exactly 2 populated sides |
| `hero-<name>-<paper>.pdf` | Each of the 24 Basic Mode Heroes, exactly 2 populated sides |
| `basic-heroes-<paper>.pdf` | All 24 Heroes, exactly 48 populated pages / 24 duplex sheets |
| `party-ledger-<paper>.pdf` | Existing 2-side party ledger, unchanged in this iteration |

`<paper>` is `white` or `cream`. Local PDFs are in ignored `build/heroes/`. There is no current compact one-side output and no padding with empty backs. The retired compact sources have been removed. Print actual size / 100%, Letter portrait, duplex, flipping on the long edge.

## Blank record visual system

`typst/heroes/blank-record.typ` imports `typst/aids/kit.typ` and the main rulebook's `typst/templates/system.typ`. Grenze Gotisch headings, Source Serif 4 resource headings, Source Sans 3 labels, the approved signature, shield marks, lozenges, and deterministic brush rules use the book's existing sources. There is no substitute font system or new artwork.

Identity occupies a compact three-row field grid beside an empty portrait arch. There is no default portrait, crest, or label inside that arch. The book signature appears only in the title. Attribute shields retain legible sans-serif abbreviations; Initiative, Speed, Size, HP, NRG, Luck, and AP use open writing lines. Current, maximum, and Temporary HP remain distinct.

Ornament stays at section boundaries. Black title bands with reversed blackletter and black attribute-shield chiefs restore visual weight, following the owner's feedback that the black boxes were aesthetic. Open ledger rules separate entries without an outer panel, inner frame, tinted label band, or grey-filled writing cell. Coins, Adventures, and Fate remain on white writing surfaces beside the black bands. All writing capacities and row pitches are unchanged. All printed type is at least 9 pt. Cream and white exports have identical text and geometry.

## Blank record

The front contains identity, attributes, resources, Chest and Shield armour parameters, Wounds and lingering injuries, 3 weapon rows at 26 pt, and 12 Inventory rows at 18 pt. The Inventory records quantity, item, equipped status/location, and notes in one list. Coins use a small writing line in the section heading rather than a separate box.

The reverse devotes the full page width to 7 Power entries at 38 pt and 7 talent/special-ability entries at 32 pt. Each entry has a name column and a broad description column with two writing lines. Hero Details provides two additional full-width lines, with small Adventures and Fate fields. These are writing capacities, not mechanical limits.

The duplicated ancestry/background rules panel, separate equipped-slot list, Party Leader checkbox, boxed Carried Coins field, weapon/armour reminders, and entire advancement reference have been removed from the blank. Ancestry and Background remain once in identity; their abilities can be recorded with the other special abilities. Permanent item details can be recorded in Inventory notes. No manuscript or game rule changed.

## Pre-generated Heroes - adaptation deferred

The following describes the previous expanded design. It has not been restyled during the blank-only pass. `typst/heroes/expanded.typ`, the approved portraits, and all 50 individual/pack PDFs retain their previous hashes.

Every front contains identity and portrait, statistics and trackers, every equipment entry, full shared Basic Mode Hands and 0 HP rules, active Hands fields, carried coins, and a bounded carried-item/change area.

Every reverse contains ancestry traits, the background rule, talents, Powers, special rules, weapon trait rules, applicable Senses reminders, and a bounded Notes area. Dense Heroes receive less space on the reverse and retain the front writing area. Both sides are populated for every Hero, including the shortest profiles.

The renderer retains every B.4 word and emphasis run through the exact extractor in `tools/hero_cards.py`. A long sub-paragraph can continue at a sentence boundary between columns. Its existing text runs are sliced without rewording; the complete original paragraph must remain present in the extracted PDF text. Headings stay with their first entry.

## Reproduction and checks

```text
python tools/hero_cards.py check
python tools/hero_cards.py render --paper both --only hero-sheet
python tools/hero_sheet_qa.py --only-blank --render-review
```

The render command rejects anything other than 2 pages for an individual Hero and 48 pages for the full set, and rejects compiler warnings. It audits all profile text, sub-items, statistics, shared notes, front equipment, footer clearance, and the reverse Notes boundary.

Blank-only QA checks Letter geometry, exactly two pages, minimum type size, essential text safety, font embedding, searchable text, simulated 1.03 overscan text clipping, and cream/white geometry. It compares the 50 Basic Mode PDFs against their preceding hashes, without rebuilding them or replacing their review images. The four blank sides are rendered by Poppler. The scoped receipt is `build/hero-redesign/blank/qa.json`; author observations and exact hashes are in `production/qa/blank-hero-sheet-design-review.json`. Use the commands without `--only`/`--only-blank` for a separately authorized complete Hero-set pass.

`tests/test_hero_cards.py` verifies source extraction, required blank fields, absence of redundant sections and grey-filled inner cells, the empty portrait area, exact two-side output, populated pack versos, and complete profile coverage. Run `python tools/dev.py check` before pushing sources.

## Review status

Author review and automated checks do not establish owner aesthetic approval. This iteration remains subject to owner review. Physical printing, handwriting, erasing, and duplex registration are **NOT TESTED**. The current manuscript remains RC513; the published book release remains RC492-build-37. This work does not rebuild or release the book.

## Illustrated Hero record (2026-10-26)

`assets/hero-record/` holds the illustrated Hero record (front and reverse) and its single generator, `assets/hero-record/sheet.py`, which builds both the blank sides and the 24 populated Basic Mode Heroes from one geometry spec (see `assets/hero-record/README.md`). It uses the repository's fonts, signature mark and ink art, keeps all printed type at 9 pt or larger, and does not replace the Typst blank above. Populated PDFs are build products and are not committed; the on-demand **Build Hero records** workflow publishes both PDFs as a pre-release (tag `RC###-hero-records-N`). Owner approval of this version and physical printing are **NOT TESTED**.
