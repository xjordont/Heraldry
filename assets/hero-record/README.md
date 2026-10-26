# Hero Record (illustrated blank, two sides)

Owner-reviewed design, 2026-10-26. One US Letter sheet printed front and back, 816 x 1056 CSS px (8.5 x 11 in).

| File | Purpose |
|---|---|
| `hero-record-front.html` | Front: identity, attributes, resources, Armour, Wounds, Weapons, Inventory, Coins |
| `hero-record-reverse.html` | Reverse: Powers (14 rows) and Talents & Special Abilities (14 rows) |
| `art/` | Ink art and traced ornaments (SVG; the three illustrations are 4x upscaled PNGs, about 490 to 540 ppi at print size) |
| `render.py` | Renders both sides to 2550 x 3300 PNG (300 dpi) in `previews/`; `--pdf OUT.pdf` also writes the two-page print PDF |
| `previews/` | 300 dpi page renders |

Type follows `config/design_tokens.json`: Grenze Gotisch (titles and banners), Source Serif 4 Bold (product line and resource headings), Source Sans 3 (labels). Fonts load from `fonts/static/`. Every printed label is 9 pt or larger. All values are blank by design.

Print actual size (100%), Letter portrait, duplex, flip on the long edge. Do not commit PDFs; publish through a GitHub Release. Physical print, handwriting, and duplex registration are **NOT TESTED**.
