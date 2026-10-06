# Heraldry publication state

Status: IN PRODUCTION — complete art-light book builds; figures integration, all-page visual QA and packaging in progress.

Canonical source: source/Heraldry_RC484.md — SHA-256 2744833106569e6b20f6913340de5d80c7869782556e23b8f738a0407e4f16f3 (verified by preflight and every parse).
Branch: claude/heraldry-rc484-build

## Milestones (evidence)
- M0 preflight baseline PASS (production/preflight.json). Toolchain: Python 3.13, typst (python) 0.15.0, PyMuPDF 1.28.2, markdown-it-py 4.2.0, fonttools 4.66.1 (requirements.lock). Fonts: Source Serif 4, Source Sans 3, Cinzel (OFL, fonts/licences).
- M1 inventory: production/inventory/ (833 headings, 332 tables, 7,743 paragraphs, 4,185 list items, 18 <br>, 1 quote, 42 hr).
- M2/M3 full conversion: ~419 pages; reconciliation PASS (8,426 blocks in order, 10,341 table cells, 22,796 bold + 449 italic runs); layout detectors 0 flags; inkjet checker PASS (cream).
- M5 navigation: generated TOC, 551 bookmarks (3 levels), 1,262 internal links resolve, curated index (228 entries from the C.11 glossary + named-entry groups).
- Covers, calibration sheet, print instructions, art manifest (route C) written.

## Next exact actions
1. Integrate figures from figures/ (rules-illustrator output): `python3 figures/src/make_figures.py`.
2. Full build: `make all` (parse → figures → balanced book → white/digital variants → covers/calibration → specimen).
3. `make verify` (writes production/qa/STATUS.json; must be PASS).
4. All-page visual review in 24-page batches → production/qa/visual-review.json; repair, rebuild, re-verify.
5. `make package` → dist/Heraldry_RC484_release.zip with SHA256SUMS; commit + push.

## Resume
`python3 tools/preflight.py --report production/preflight.json` (no --baseline), then `make all verify`.
