# Production state — RC485, main

Updated 2026-10-06. Working/delivery branch: **main**. No new branch without an explicit owner decision and recorded reason. `claude/heraldry-rc484-build` is a historical checkpoint.

## Active manuscript

`source/versions.json` identifies `source/Heraldry_RC485.md`, SHA-256 `fc6caeeedf1e8e2cce80ed469ef74fb3c196048563c6bfec65031f2b03c4bbbe`. It contains the seven previously approved clarifications P-01–P-07, plus the RC485 marker. Original RC484 is unchanged. Exact patch history is `editorial/history/RC485.json`. No build-only manuscript patch layer remains.

Future text edits follow `docs/WORKFLOW.md` and promote an approved exact patch batch with `tools/revise_manuscript.py`; the next revision is RC486. Artwork, figures and layout use Git commits without an RC bump. Only the orchestrator promotes snapshots and integrates main commits.

## Current delivery and verification

Digital PDF: 597 pages. Cream and white interiors: 594 pages each, identical pagination. Current covers, calibration, print instructions, 13-page specimen and ZIP are under dist/. The calibration ruler stays within its column. PDF timestamps are pinned to the revision date.

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

GitHub artwork transfer completed: all twelve originals were downloaded from stored LFS objects and verified by SHA256/byte count before their pointers were committed to main. The artwork-only ZIP passed native-file checks in GitHub Actions run 37555457110. Temporary transfer files are removed after the import. PDF rebuilding remains a separate gated step after placement and visual-ledger updates; instruction-only workflow edits do not trigger delivery rebuilding.

## Owner one-page keep clarification — 2026-10-07 UTC

Mandatory: every complete fit-capable scenario, section/subsection, table, procedure and entry stays on one physical page with its heading and necessary associated content; move the whole unit when remaining space is insufficient. Measure against an empty usable page at approved widths; protect nested short children even in long parents. Implement before balancing, audit every stable source ID with current input/PDF hashes, and make avoidable splits or missing coverage release failures. See DESIGN_REFINEMENT.md. This instructions-only checkpoint leaves RC485 and existing PDFs unchanged; enforcement and all-page review are required in the next build.

## Illustrated build and one-page keeps — 2026-10-07
- Art integrated: 11 chapter openers + front cover at native 300 ppi (exact px/300 in), alpha preserved; cover title remains live type.
- Pagination rebuilt around measured keep units (tools/measure_units.py → build/unit_measure.json): sections/subsections/scenarios, tables, lists, examples and figures that fit an empty usable page stay on one page (column move or whole-page composition); numbered sections and named scenarios start fresh pages; run-in labels/lead-ins stay with their lists.
- New mandatory gate check `one_page_keeps` (tools/keep_audit.py, bound to content.typ and PDF hashes): 1538 fit-capable units, 0 avoidable splits, 0 missing coverage.
- Fixed a bug from the owner's guard commit (lost tuple when appending column figures).
- Interiors grew 450 → 594 pages from fresh-page starts and whole-unit moves (intentional whitespace per DESIGN_REFINEMENT.md).
- Verified: 19/19 checks PASS; all 594 pages inspected; reconciliation unchanged (8,426 blocks, 10,341 cells). Release ZIP (156 MB) exceeds GitHub's file limit: delivered as the CI artifact, not committed.
- Not done: entry-anatomy restyle beyond existing cards, spot art; 4 scenario maps still await owner decisions. Physical proof NOT TESTED.

## Scenario diagrams unified — 2026-10-07
- All 44 setup/deployment diagrams (FIG-13-16, 18-57) drawn from one glyph registry (figures/src/scenkit.py); FIG-20 key explains all 40 glyphs; selfcheck fails on any glyph missing from the key; captions cite the key; FIG-13-16/18/19 carry compact key strips.
- Appendix A/B maps redrawn on the core map renderer. Unresolved elements (Undermarches 1, Sun-Drowned 3, The Mire 2, The Mire 5) shown with a '?' tag and note, not placed.
- Terrain types corrected to the 2.9.1 table on 24 maps, with a terrain-type selfcheck.
- Independent review: 0 open majors, gate PASS 57/57 (29 open minors, e.g. FIG-51 G1/Chest glyph touch).
- Interiors 596 pages; all inspected; 19/19 checks PASS.

## RC486 placements and figure minors — 2026-10-07
- Owner instruction 2026-10-07: "Fix the unplaced elements and minor notes to the best of your ability." RC486 created with tools/revise_manuscript.py from RC485 (P-08..P-12, editorial/proposals/rc486-scenario-placements.json): Undermarches 1 arrival point, Sun-Drowned 3 guard position, The Mire 2 and 5 escape edges, The Mire 5 Group 1 short-edge arrival.
- FIG-33, 47, 52, 55 now draw these elements; the '?' unresolved glyph was removed from the FIG-20 key and registry.
- 29 open figure minors: 25 fixed, 4 accepted with reasons in figure-semantic-review.json (FIG-19 label on ring, FIG-27 ruler over dome, FIG-29 label halo over a dashed ring, FIG-51 Group 2 logged ambiguity). Gate PASS 57/57, 0 open majors/minors.
- Clean build: interiors 596 pages, digital 599; all 596 pages inspected on contact sheets, FIG-55 at 70 dpi; 19/19 checks PASS; release ZIP built (CI artifact). Physical proof NOT TESTED.
