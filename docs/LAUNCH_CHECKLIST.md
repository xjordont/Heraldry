# Launch readiness and visual references

Resume the current project from `CLAUDE.md`, `AGENTS.md`, and `production/STATE.md`. `MASTER_PROMPT.md` is the standing production contract, not a request to restart completed work.

## Routine readiness

1. Inspect local work and the current main head. Fast-forward a clean checkout with `git pull --ff-only origin main`; preserve unrelated edits and inspect divergence.
2. Run `python tools/dev.py check` for exact dependencies, baseline contracts, immutable source history, whitespace, and tests. Local reports belong in ignored `build/checks/`.
3. Read `production/RELEASE_STATUS.md`, `production/RELEASE_RESULT.json`, and `dist/RELEASE.json` to identify the last requested delivery and its limits. A passing local check does not certify current PDF bytes.

## Requested publication

Only an owner request for a build, PDF, or layout pass starts publication. Follow `docs/BUILD_AUTOMATION.md` and the current `production/codex-build/CODEX_BUILD_CARD.md`: request a GitHub candidate, inspect every listed review image, bind the exact PDF, and verify the delivery result. Diagnose failures within the primary-developer role; never weaken a review gate or invent observations.

Required release evidence includes source/table reconciliation, figure semantic currency, navigation checks, all-page visual coverage, package checksums, and the exact input/PDF hashes. PDFs and ZIPs are GitHub Release assets, not Git commits.

The publication target is the digital PDF, `Heraldry_RC###_digital.pdf`: portrait US Letter pages on a warm cream page colour, with the front and back covers inside it, plus the screen companion `Heraldry_RC###_digital-compact.pdf`. See `docs/VISUAL_QA.md`.

## Reference and artwork inputs

Use only the ten owner-selected titles in `references/sample_pdfs.json`, under `references/README.md`. Fetch and inspect only the relevant selected pages. Their private PDF bytes and images never enter publication packages.

Current illustration approvals come from `production/art/SELECTIONS.json`; native-master provenance comes from `production/art/ART_MANIFEST.json`. The old `production/art/HANDOFF.md` describes the original twelve-master delivery. Current cover, layout, and release decisions come from the latest state, not that historical task list. Atmospheric artwork never establishes rules or deployment geometry.
