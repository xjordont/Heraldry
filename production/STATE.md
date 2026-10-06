# Production state — RC485, main

Updated 2026-10-06. Working/delivery branch: **main**. No new branch without an explicit owner decision and recorded reason. `claude/heraldry-rc484-build` is a historical checkpoint.

## Active manuscript

`source/versions.json` identifies `source/Heraldry_RC485.md`, SHA-256 `fc6caeeedf1e8e2cce80ed469ef74fb3c196048563c6bfec65031f2b03c4bbbe`. It contains the seven previously approved clarifications P-01–P-07, plus the RC485 marker. Original RC484 is unchanged. Exact patch history is `editorial/history/RC485.json`. No build-only manuscript patch layer remains.

Future text edits follow `docs/WORKFLOW.md` and promote an approved exact patch batch with `tools/revise_manuscript.py`; the next revision is RC486. Artwork, figures and layout use Git commits without an RC bump. Only the orchestrator promotes snapshots and integrates main commits.

## Current delivery and verification

Digital PDF: 453 pages. Cream and white interiors: 450 pages each, identical pagination. Current covers, calibration, print instructions, 13-page specimen and ZIP are under dist/. The calibration ruler stays within its column. PDF timestamps are pinned to the revision date.

12 regression tests PASS; 18/18 release checks PASS. 8,426 source text blocks in order; 332 tables / 10,341 cells; 19 figures with prior independent reviews also bound to source-rule dependencies. All 436 pages inspected as 24-dpi contact sheets, five pages at 100 dpi, covers, calibration and one 1.03 overscan page; exact hash/scope in the visual ledger. Not full glyph-level proofreading or a complete rules contradiction audit.

Clean repeated builds produced identical cream, white, digital and cover PDF bytes. Packaging verifies unique entries/checksums and includes all instructions, agents, reference metadata and fonts needed by a clean checkout. GitHub checks protect prior snapshots/records against the base commit. Extracted-package rebuild evidence is in production/qa/rebuild-audit.json.

## Remaining inputs and next run

Atmospheric illustrations: BLOCKED (12 planned pieces, no supplied art or authorized paid service). Physical inkjet proof: NOT TESTED. Full manuscript contradiction audit: NOT TESTED beyond existing triage and figure review. Commercial wrap/PDF-X: NOT APPLICABLE. Author/publisher/copyright/ISBN details were not supplied.

Resume requested component work; do not restart initial production. Read the budget ledger and live account controls before paid work; do not reset spending or assume a renewed $100. Run `make clean all`, inspect affected pages/repagination and update visual/figure evidence, then `make verify package`. Push verified work directly to main without force. If the platform blocks main writes, record the actual restriction and preserve work rather than silently making a branch.

## Run 2026-10-06 (scenario maps, layout)
- Art: BLOCKED — no authorized image route (see ART_MANIFEST route_check). 0/12 produced.
- Figures: FIG-20 legend, FIG-21..56 maps for all 36 Core Scenarios, FIG-57 10.1 procedural template; FIG-18/19 retained as Appendix A/B maps; FIG-14 dimension fix confirmed. Independent review: 0 open majors; gate PASS. 15 ambiguities logged for owner decision; maps with undrawn elements: Undermarches 1, Sun-Drowned 3, The Mire 2, The Mire 5.
- Layout: glossary hanging indent; formula stat profiles as key/value cards; tall legend floats (void removed).
- Manuscript: unchanged (RC485). No text patches proposed this run.
- Verified: 18/18 checks PASS; all 450 pages inspected; package rebuilt.
- Spend: measured $90.25 of $100; only repair/packaging remains authorized within budget.
