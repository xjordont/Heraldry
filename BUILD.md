# Building HERALDRY SKIRMISH RC484

Pipeline: Markdown (protected RC484 source) → markdown-it-py semantic model (`build/blocks.json`) → generated Typst (`typst/content.typ`) using the design system in `typst/heraldry.typ` → PDF (Typst via the `typst` Python package). No LLM regenerates any text; every text node is emitted as a Typst string literal.

## Requirements
* Python 3.13 (tested 3.13.16); `pip install --break-system-packages -r requirements.lock` (typst 0.15.0, PyMuPDF 1.28.2, markdown-it-py 4.2.0, fonttools 4.66.1, pypdf, Pillow).
* No system fonts are used (`ignore_system_fonts`); bundled OFL fonts in `fonts/static` (regenerate with `make fonts` from `fonts/variable`).

## One-command clean build
```sh
make clean all verify package
```
* `make all` — preflight (source hash) → parse/inventory → index → covers/calibration → figures → balanced cream interior (converging layout loop) → white + digital variants → specimen.
* `make verify` — reconciliation, layout detectors, supplied inkjet checker on cream + white, supplementary print checks, cross-reference/table/index/figure audits → `production/qa/STATUS.json`; exits non-zero on any mandatory FAIL.
* `make package` — `dist/Heraldry_RC484_release.zip` + `dist/SHA256SUMS.txt`.

## Outputs (dist/)
| File | Purpose |
|---|---|
| Heraldry_RC484_digital.pdf | digital reading edition (covers + interior, links, bookmarks) |
| Heraldry_RC484_inkjet-borderless.pdf | cream interior, borderless Letter |
| Heraldry_RC484_inkjet-borderless-white.pdf | paper-white interior, identical pagination |
| Heraldry_RC484_covers-front-back(.pdf / -white.pdf) | front/back cover sheets |
| Heraldry_RC484_inkjet-calibration.pdf | diagnostic sheet |
| PRINT_INSTRUCTIONS.md | device-aware printing guidance |
| specimen/ | production specimen (not the book) |

## Adding artwork later
Place approved masters named by `production/art/ART_MANIFEST.json` (e.g. `assets/art/incoming/ART-CH01-001.png`) and rebuild; chapter openers pick them up automatically. Re-run `make verify` and the visual review afterwards: pagination will change.
