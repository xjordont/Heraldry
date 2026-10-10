# Production state — RC487, main

Updated 2026-10-10. Working/delivery branch: **main**.

## Active manuscript

`source/versions.json` identifies `source/Heraldry_RC487.md`, SHA-256 `d77a72f9030061f76ea61e947bf520dcc81628bd653f61ba144f2a474a088254`. RC487 applies one owner-authorized batch of 48 exact repairs archived in `editorial/history/RC487.json`. RC484–RC486 and their archived history remain unchanged. Future text edits follow `docs/WORKFLOW.md` and promote a new snapshot; artwork/figure/layout edits use Git commits without an RC bump.

## Current delivery and verification

RC487 digital: 600 pages; cream and white interiors: 597 pages each. All 597 cream interior pages were inspected on contact sheets, with nineteen detailed pages, both cover variants, calibration and an overscan specimen. Visual/figure ledgers describe the actual review scope and current hashes. Current figure review is by the repair author; historical independent findings are retained.

17 regression tests and 8 source preflight checks pass. Reconciliation preserves 8,429 text blocks in order and all 332 tables / 10,315 current cells. All 835 printed item Cost/Value cells are unchanged; development price multipliers/formulas and quality-table Value columns are removed. All 50 special weapon base profiles resolve. 1,539 fit-capable units have no avoidable splits or missing coverage. All 57 figures pass the current source-bound review gate. The 19-check release gate and package audit are recorded in `production/qa/STATUS.json` and `production/qa/package-audit.json`.

The contradiction audit is closed for F01–F21 and U01–U06 in `production/qa/manuscript-contradiction-resolution.md`; the original RC486 audit remains historical evidence. Owner-authorized completions and new illustrative dice results are explicit in the closure record. Exact reconstruction and immutable hashes are verified by `production/qa/manuscript-repair-verification.json`.

## Remaining inputs

The original workflow email's three annotation texts remain unavailable through the plugin; cancelled browser sign-in supplied no further evidence. No conjectural mapping of annotations is claimed. Pen-and-ink candidate approval and physical inkjet proof remain separate outstanding work; no new artwork is approved by this manuscript repair. Physical proof: NOT TESTED. Author/publisher/copyright/ISBN details remain unset. Commercial wrap/PDF-X: NOT APPLICABLE.

GitHub delivery rebuilding verifies the committed visual ledger before committing generated PDFs to main. Do not force-push or re-promote RC487. Historical checkpoints below retain their original scope.

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

## Automated pen-and-ink art pipeline — 2026-10-08
- Owner instruction: "I want to automate the entire process with as little effort as possible. While the existing art assets can serve as a generate inspiration I think it would be best to replace them as well to ensure consistency." Route changed from ChatGPT Work to the Gemini image API (CLAUDE.md, docs/ART_AUTOMATION.md).
- Built: tools/art_catalog.py (275 entries), config/art_style.json (style bible, $150 cap), tools/art_generate.py (anchors → approval → batch, automated judge, budget ledger), tools/art_ink.py (pure ink on transparent), the `Generate pen-and-ink artwork` workflow, and layout slots (spot art above flavour text inside keep units; cover and chapter fall back to the original masters).
- Layout test with four stand-in images: clean build PASS on all checks except the expected visual ledger; test art removed.
- BLOCKED on the owner: repository secret GEMINI_API_KEY is not set (first anchors run failed at the key check; $0 spent). Next: run anchors, review and approve anchors, run batch, review contact sheets and placed pages, rebuild and update the visual ledger.
- 2026-10-08 style definition: owner supplied four samples and asked to define the style ("Dark Souls inspiration as well"). Three samples are stored as generation references in assets/art/style/ (original JPEG bytes as plain git blobs, because this cloud session cannot upload LFS; excluded from packages and provenance); the old CH01 master is recorded as the density counter-example. config/art_style.json was rewritten: one illustrator, figure and scene registers, classic RPG interior ink, withered-beauty mood. The anchors phase now uses the owner samples; the batch uses the approved anchors plus the samples. Still waiting on the GEMINI_API_KEY secret.

## Manuscript contradiction audit — 2026-10-09

- Audit completed across all chapters and Appendices A–C of active RC486. Semantic clearance: OPEN FINDINGS. Evidence: [report](qa/manuscript-contradiction-audit.md), [findings](qa/manuscript-contradiction-audit.json), [reproducible verification](qa/manuscript-contradiction-verification.json).
- 21 open findings, 6 explicitly isolated uncertainties; stale Spot/DEX Pen/terrain/allegiance/AI references, enhanced-value differences, incomplete equipment/AI procedures, scenario deployment/objective/ending gaps, two teaching-example errors, and combined Basic Mode variants. No unverified behaviour or unseen dice results asserted.
- Exact candidate batch: `editorial/proposals/rc487-contradiction-audit.json`, 13 proposed replacements (9 summary/name repairs; 4 whole-table replacements for 15 value cells). Uniform market/treasure valuation remains an intent question. All entries are `proposed`; substantive decisions and example rolls are excluded.
- Verified: 15/15 tests; 8/8 preflight; all 274 recognizable enhanced-quality rows; 93 direct die-range tables without gaps/overlaps; 633 section references; 1,898 bestiary mentions; 86 evidence anchors; all 13 unique patch matches; exact P-01–P-12 reconstruction and immutable snapshot hashes.
- RC484–RC486, registry/history and existing PDFs are unchanged. This evidence update does not grant a semantic release PASS, reapprove artwork/layout, or substitute for physical proof. The original GitHub email's three annotation texts remain unavailable; no conjectural mapping is claimed.
- Next manuscript work: decide open mechanics/placement/timing questions, author complete corrected teaching ledgers, approve an exact patch batch and promote RC487 once, then reconcile/rebuild and review affected figures/PDFs.
- 2026-10-10 unique illustration plan (owner: "Ensure unique art planned for every illustration... Include planned prompts"): production/art/SUBJECT_PLAN.json adds 11 fresh chapter subjects and concrete direction for 78 entries. Named bosses are a separate `boss` family; scenarios show place with creatures small; backgrounds are still lifes. tools/art_catalog.py gained a uniqueness gate. production/art/ILLUSTRATION_LIST.md (tools/art_list.py) lists all 275 entries with exact prompts. The six anchors are unchanged and still valid.
- 2026-10-10 prompts v2 and ChatGPT Work route (owner: "considering" switching to ChatGPT Work for subscription use and better GPT Image results; supplied a Greythorn prompt and render). The prompt template now follows the owner's Greythorn structure; OWNER_PROMPTS.json holds that prompt verbatim. Two Sonnet workers wrote 274 manuscript-based briefs (production/art/briefs/), with orchestrator fixes (Six Climates scope, Warden size, chapter 9 duplicate, Orc weapon). tools/art_gpt_pack.py writes production/art/gpt/ (INSTRUCTIONS, QUEUE, prompts); tools/art_intake.py plus the 'Intake ChatGPT artwork' workflow ink-prepare committed images (the owner Greythorn render has been received). Art-relevant manuscript notes are in production/art/SOURCE_NOTES.md. The route switch is NOT yet recorded in CLAUDE.md, pending owner confirmation; the Gemini route is unchanged.

## RC488 owner refinements and ChatGPT Work art route — 2026-10-10
- Owner instruction: "Yes make the chat gpt work the official image generation pathway." CLAUDE.md and docs/ART_AUTOMATION.md now name ChatGPT Work (queue, then ChatGPT Work commits, then the intake workflow, then orchestrator approval) as official. The Gemini pipeline is retired as a fallback; its six test drawings are superseded.
- Owner-instructed manuscript batch promoted as RC488 (13 patches, editorial/history/RC488.json):
  - Undead Champion: War Maul.
  - Stone Sentinel: stone greatsword in the text; Stone Greatsword attack at 1d12 slashing, the Claymore's damage.
  - Orc: Battleaxe plus Shield Wall.
  - White Court Guard: Court Longsword plus Shield Wall.
  - Giant Scorpion: "size of a man".
  - Frost Giant: "towering over humans, orcs, and ogres alike".
  - Noxcloth: size M.
  - The Mire 2: Swamp Goblins replace Troglodytes.
  - The Mire 5: summons Zombies, not Troglodytes.
- Basilisk/Medusa cone Gaze: not applied. Both already have Petrifying Gaze (AI Step 1); owner decision 2026-10-10 "Leave them as they are." Their briefs were corrected to show the gaze.
- Figures: FIG-52 redrawn (Swamp Goblins; labels clear of all lines); 1,056 figure line citations remapped to RC488. An independent re-review gives gate PASS 57/57, 0 open.
- Briefs, prompts, queue and ILLUSTRATION_LIST updated for the changed entries.
- Clean build: 597 interior pages, identical pagination; 11 pages differ from RC487, all inspected. 19/19 checks PASS; release ZIP built. The RC486/RC487 dist PDFs are retired from dist/. Physical proof NOT TESTED.
- Next: owner starts ChatGPT Work on production/art/gpt/INSTRUCTIONS.md (anchors queue: 5 items; Greythorn already received).
