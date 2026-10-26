# Hero Record (illustrated blank, two sides)

Owner-reviewed design, 2026-10-26. One US Letter sheet printed front and back, 816 x 1056 CSS px (8.5 x 11 in).

| File | Purpose |
|---|---|
| `hero-record-front.html` | Front: identity, attributes, resources, Armour, Wounds, Weapons, Inventory, Coins |
| `hero-record-reverse.html` | Reverse: Powers (14 rows) and Talents & Special Abilities (14 rows) |
| `art/` | Ink art and traced ornaments (SVG; the three illustrations are 4x upscaled PNGs, about 490 to 540 ppi at print size) |
| `render.py` | Renders both sides to 2550 x 3300 PNG (300 dpi) in `previews/`; `--pdf OUT.pdf` also writes the two-page print PDF |
| `previews/` | 300 dpi page renders |
| `populate.py` | Fills the record for the 24 Basic Mode Heroes from `typst/heroes/basic-heroes.json` (B.4) into `build/hero-records/` (never committed); `--pdf FILE` writes one duplex-ready PDF |

Type follows `config/design_tokens.json`: Grenze Gotisch (titles and banners), Source Serif 4 Bold (product line and resource headings), Source Sans 3 (labels). Fonts load from `fonts/static/`. Every printed label is 9 pt or larger. All values are blank by design.

Print actual size (100%), Letter portrait, duplex, flip on the long edge. Do not commit PDFs; publish through a GitHub Release. Physical print, handwriting, and duplex registration are **NOT TESTED**.

## Populated Basic Mode Heroes

`python3 assets/hero-record/populate.py --pdf build/hero-records/basic-heroes.pdf` writes a front and reverse for each Hero, in B.4 order, then any reference cards, so duplex pairs stay aligned.

- Front: name, class, ancestry, background, Level 1, portrait (`assets/art/ink/<art>.png`, masked to the shield with `art/hr-shield5-mask.png`), ability scores, INIT (INT + SPI, as the earlier pre-generated records), SPD, Size, and the maximum HP, NRG, and Luck. Current values, Wounds, and Coins stay blank for play. Armour, weapons, and other items are parsed from Equipment and Items; P/O marks the first weapon Primary and a second one-handed melee weapon Off-Hand only when no shield is listed.
- Reverse: every word of each ancestry trait, background rule, talent, Power, and special rule in 9 pt, two text lines per ruled row, with rules drawn between entries. Powers (anything that costs NRG) show Tier, Cost, and Range. Owner decision 2026-10-26: weapon trait rules print where room remains, and the Weapons table always names every trait. If the Talents table overflows, a Senses reminder keeps its name only, then an ability with an AP cost moves into spare Powers rows.
- Mossgrave's Wild Shape Form Rules and four Novice Beast Forms print on a separate one-third-page Wild Shape card (owner decision 2026-10-26); his sheet keeps the Wild Shape text and points to the card.
- The script fails if any text overflows its cell, falls below 9 pt, or if any B.4 rules or item text is missing from a Hero's pages.

