# Heraldry publication state

Status: ART-LIGHT RELEASE BUILT AND VERIFIED (release gate PASS). Atmospheric illustration suite BLOCKED (no authorised image route). Physical print proof NOT TESTED.

Canonical source: source/Heraldry_RC484.md — SHA-256 2744833106569e6b20f6913340de5d80c7869782556e23b8f738a0407e4f16f3.
Branch: claude/heraldry-rc484-build. See production/RELEASE_STATUS.md for per-area statuses.

## Deliverables (dist/)
Heraldry_RC484_digital.pdf (437 pp), Heraldry_RC484_inkjet-borderless.pdf and -white.pdf (435 pp each, identical), covers (cream/white), calibration sheet, PRINT_INSTRUCTIONS.md, specimen/, Heraldry_RC484_release.zip + SHA256SUMS.txt.

## Resume / rebuild
1. `python3 tools/preflight.py --report production/preflight.json`
2. `make all && make verify && make package`
3. After adding art to assets/art/incoming/ (names in production/art/ART_MANIFEST.json): rebuild, re-verify, redo the contact-sheet visual review (pagination changes).

## Open items (external inputs)
- Original illustrations (12 mandatory assets) — needs an authorised image service or supplied files.
- Physical proof on the user's printer/paper.
- Author/publisher/copyright metadata if a commercial edition is wanted.
