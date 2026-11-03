# Hero records

The Hero record that ships is the illustrated two-sided record in `assets/hero-record/` (owner-directed design, 2026-10-26), built by its one generator, `assets/hero-record/sheet.py`. Its layout, fields, typography, commands, and checks are in [assets/hero-record/README.md](../assets/hero-record/README.md).

## Outputs

| Release file | Content |
| --- | --- |
| `Heraldry_RC###_hero-record-blank.pdf` | The blank record: front and reverse |
| `Heraldry_RC###_basic-heroes.pdf` | The 24 Basic Mode Heroes of Appendix B.4, each front paired with its reverse, then the reference cards (Mossgrave's Wild Shape card) |

Every verified book release builds both (`Rebuild verified delivery`); there is no separate Hero-record workflow. Built PDFs are never committed.

## Source data

`typst/heroes/basic-heroes.json` holds B.4 of the active manuscript, extracted without rewording by `python tools/hero_cards.py extract`. `python tools/hero_cards.py check` proves that the JSON matches the manuscript and reproduces every profile line for line; run `extract` again after any RC that changes B.4. `tests/test_hero_record.py` checks every Hero's weapons, armour, and shields against the 7.8 to 7.12 tables.

The earlier Typst Hero records (2026-10-22) were removed on 2026-11-03; their research and design record is in `docs/history/HERO_SHEET_RESEARCH.md`.
