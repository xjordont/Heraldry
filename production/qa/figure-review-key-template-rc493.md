# RC493 figure review: shared key and setup template

Reviewed 2026-10-15 by the Codex integration owner, who also made these repairs. This is a source and rendered-figure review, not an independent second review or a book-placement proof.

Authority: `source/Heraldry_RC493.md`, SHA-256 `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`. Relevant text read directly: 2.6, including lines 594-604 and the Size table; 2.9.1 terrain types; 10.1 Setup Roll-off, Random Direction, Battlefield Edges, and all twelve Preparation Steps.

Both SVGs and their current captions were rendered through Typst directly to PNG at 504 pt width and 200 ppi, using Source Sans 3 and the production figure-caption dimensions. Both complete images were directly viewed before and after repair. The final evidence files are `build/checks/figure-review-all/FIG-20.png` and `FIG-57.png`; their hashes are recorded in `figure-semantic-review.json`.

| Figure | Actual observations and rule comparison | Disposition |
| --- | --- | --- |
| FIG-20 | All four key columns are legible. Solid/open party bands, objective/chest/marker glyphs, terrain patterns, dimensions, arrival/exit arrows, and illustrative dashes remain distinct in grayscale. Large and Huge swatches previously touched; extra row space now separates them. The key explains group/state/arrival suffixes. Measurement now gives Tabletop closest-point measurement first and Grid occupied-square/distance rules second. Footprints and default deployment dimensions match 2.6/10.1. The caption no longer claims to explain removed not-placed symbols. | PASS_WITH_NOTES; identified defects resolved. |
| FIG-57 | All twelve numbered rows read in order; terrain and deployment steps have clear emphasis. Hatch now remains visible inside deployment zones, rather than suggesting that those white areas permit major Blocking/Impassable Terrain. The text preserves the source's prohibition and scenario exception. Edge and zone clearances are explained separately. Rounded corner clearances are explicitly Tabletop schematics; the paired Grid clause directs occupied-square measurement at 1 inch orthogonally/1.5 inches diagonally under 2.6. Both boards, rulers, key, notes, and final caption are unclipped. | PASS_WITH_NOTES; identified defects resolved. |

The figures retain minimum 9 pt essential labels at the stated width. Source rules, deployment dimensions, and scenario precedence were not changed. The template's hero discs are schematic occupants, not an instruction fixing a party's Hero count.

Generator validation checks all printed distance values against their cited source lines and checks that the shared key covers every emitted setup glyph, state, and pattern. A separate font-metric boundary scan found no text outside any figure's canvas; actual image inspection remains the visual evidence.

No book PDF was built. Final placement, pagination, cream/white PDF equivalence, accessibility, and physical printing are outside this review. Physical print: **NOT TESTED**.

Integration width clarification, 2026-10-16: 504 pt and 243 pt are the native SVG preview widths. The current v4 template provides 518.4 pt full width and 250.56 pt columns; normal 100% placement enlarges the diagrams slightly. Thus native-width review is conservative for label size. Caption previews use the production 9 pt size. Final PDF placement remains untested.
