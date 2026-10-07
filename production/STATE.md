# Production state — RC485, main

Updated 2026-10-06. Working/delivery branch: **main**. No new branch without an explicit owner decision and recorded reason. `claude/heraldry-rc484-build` is a historical checkpoint.

## Active manuscript

`source/versions.json` identifies `source/Heraldry_RC485.md`, SHA-256 `fc6caeeedf1e8e2cce80ed469ef74fb3c196048563c6bfec65031f2b03c4bbbe`. It contains the seven previously approved clarifications P-01–P-07, plus the RC485 marker. Original RC484 is unchanged. Exact patch history is `editorial/history/RC485.json`. No build-only manuscript patch layer remains.

Future text edits follow `docs/WORKFLOW.md` and promote an approved exact patch batch with `tools/revise_manuscript.py`; the next revision is RC486. Artwork, figures and layout use Git commits without an RC bump. Only the orchestrator promotes snapshots and integrates main commits.

## Current delivery and verification

Digital PDF: 453 pages. Cream and white interiors: 450 pages each, identical pagination. Current covers, calibration, print instructions, 13-page specimen and ZIP are under dist/. The calibration ruler stays within its column. PDF timestamps are pinned to the revision date.

12 regression tests PASS; 18/18 release checks PASS. 8,426 source text blocks in order; 332 tables / 10,341 cells; 57 figures with source-bound semantic reviews (current scenario-map run below). The latest visual ledger records all 450 interior pages at contact-sheet scale and selected detail reviews; exact hash/scope in the visual ledger. Not full glyph-level proofreading or a complete rules contradiction audit.

Clean repeated builds produced identical cream, white, digital and cover PDF bytes. Packaging verifies unique entries/checksums and includes all instructions, agents, reference metadata and fonts needed by a clean checkout. GitHub checks protect prior snapshots/records against the base commit. Extracted-package rebuild evidence is in production/qa/rebuild-audit.json.

## Remaining inputs and next run

Atmospheric illustrations: 12 native ChatGPT Work masters generated and reviewed; PDF integration pending. Physical inkjet proof: NOT TESTED. Full manuscript contradiction audit: NOT TESTED beyond existing triage and figure review. Commercial wrap/PDF-X: NOT APPLICABLE. Author/publisher/copyright/ISBN details were not supplied.

Resume requested component work; do not restart initial production. Run `make clean all`, inspect affected pages/repagination and update visual/figure evidence, then `make verify package`. Push verified work directly to main without force. If the platform blocks main writes, record the actual restriction and preserve work rather than silently making a branch.

## Run 2026-10-06 (scenario maps, layout)
- Art: BLOCKED — no authorized image route at that historical checkpoint. 0/12 produced then; superseded by the supplied masters below.
- Figures: FIG-20 legend, FIG-21..56 maps for all 36 Core Scenarios, FIG-57 10.1 procedural template; FIG-18/19 retained as Appendix A/B maps; FIG-14 dimension fix confirmed. Independent review: 0 open majors; gate PASS. 15 ambiguities logged for owner decision; maps with undrawn elements: Undermarches 1, Sun-Drowned 3, The Mire 2, The Mire 5.
- Layout: glossary hanging indent; formula stat profiles as key/value cards; tall legend floats (void removed).
- Manuscript: unchanged (RC485). No text patches proposed this run.
- Verified: 18/18 checks PASS; all 450 pages inspected; package rebuilt.

## Owner design review — 2026-10-07

The owner requests a less plain design, better sectional/table pagination, a GPT art route and an InDesign feasibility assessment. Read docs/DESIGN_REFINEMENT.md and docs/ART_AUTOMATION.md next. The ten correct reference books were inspected at 23 selected pages; docs/REFERENCE_ANALYSIS.md replaces the incorrect larger reference analysis and the standing brief now uses only these ten.

Representative current draft/code review found avoidable T004 splitting, awkward C.5/T327 composition, unillustrated chapter openings and dispersed scenario openings. Current automated geometry checks do not cover the new sectional/table design contract. Requested redesign status: PENDING IMPLEMENTATION AND VISUAL REVIEW. This checkpoint changes instructions/evidence only; existing dist PDFs and RC485 remain unchanged. Historical release PASS is scoped to its existing checks, not approval of the requested redesign. InDesign export is now on hold.

Next: preflight/tests; enforce fresh-page/conditional-keep policy and improve components on the specified real-content stress cases; integrate the supplied ChatGPT Work masters according to production/art/HANDOFF.md; apply across the book, inspect continuations/scenarios and all-page rhythm, reconcile, rebuild navigation and package with current hashes. Work on main. Continue through implementation, verification and packaging.

## ChatGPT Work artwork handoff — 2026-10-07 UTC

All twelve atmospheric masters are generated and visually reviewed. The exact owner-selected skeleton image was corrected to remove its third arm. Prompts, native RGBA dimensions, hashes, alpha and reduced 300ppi placement sizes are recorded under production/art/. Claude integrates these supplied assets; external image API generation is disabled. InDesign output is on hold. RC485 and all prior manuscript snapshots remain unchanged.

Preflight and all twelve workflow tests pass. Existing dist PDFs remain the previous 453-page digital / 450-page interior art-light draft. They have not been rebuilt with the new masters. The prior release ZIP and package audit are withheld pending a newly built, reconciled and visually reviewed delivery; historical PASS evidence remains scoped to the older PDF/input hashes. Read HANDOFF.md and DESIGN_REFINEMENT.md for the next run.
