# Production state - RC512 source, main

## RC512 figures reconciled - 2026-10-21

Verification: `python tools/dev.py check` PASS (326 tests); figure generation geometry/arithmetic, glyph registry, source-citation and placement checks PASS; current semantic gate 57/57 PASS; `git diff --check` PASS.

Owner request: double-check the latest uploaded manuscript against every figure and update incorrect, unclear or outdated figures. All 57 figures were compared with RC512 and visually inspected through standalone Typst SVG specimens using the bundled fonts. Fifteen SVGs changed: Reaction declaration and commitment, AV-first mitigation, Temporary HP/PvE initiative, Knocked Out Engagement/AI, Cover, legal orthogonal Shift, step 7 zones/terrain spacing, step 11 placement, Jump versus Chasm Fall, automatic Monster Terrain Checks, automatic Entangling Roots, Basic Mode extraction and one illustrative wall arrangement. Captions, current line citations, dependency bindings, placement metadata, setup specifications and current parsed inventories were reconciled.

Per-figure observations and limits: [RC512 figure review](qa/figure-review-rc512.md). The semantic ledger binds the actual current SVG/caption/rule-section hashes and inspected render hashes; all 57 pass with no stale review or unresolved major finding. Review is by repair-author models, not independent human proof. Scenario maps were inspected on contact sheets and detailed diagrams individually. No manuscript bytes changed, no RC increment, and no full-book build/release. Current RC512 book placement and pagination await a requested build. Last delivered PDFs remain RC492-build-37; physical print **NOT TESTED**.

## Basic Mode Hero art queued - 2026-10-21

Owner request: a black-and-white, old-school, borderless pen-and-ink illustration of each of the 24 RC512 Basic Mode Heroes, alone and head to ground with no background, based on name, ancestry, class, background and equipment. Implemented through the existing GPT art workflow, with no manuscript change and no new RC: a new `hero` family (catalog entries read from B.4, 2:3 at 1.9 in, `person` register, one generation each), 24 briefs in `production/art/briefs/heroes.json`, and the regenerated queue and prompts (`production/art/gpt/QUEUE.json`, `prompts/ART-HER-*.txt`). The catalog is 299 entries; the 275 approved images keep their spec hashes and approvals. No images exist yet: generation runs in Codex on the owner's PC (or ChatGPT Work), then intake, Claude visual review and approval follow. No layout slot is wired for hero art; placement waits for a requested layout pass. The optional InDesign export refuses until every catalog entry, hero entries included, has an approved selection. Verification: 326 tests pass, 3 expected skips (`python -m unittest discover -s tests`); queue builds 24 items. No PDF build or release; physical print **NOT TESTED**.

## Automatic higher-numbered manuscript intake - 2026-10-21

Owner authorised accepting any higher numbered uploaded iteration as the newest manuscript version. The reviewed importer now selects that uploaded RC automatically, without a target flag or a separate version-jump decision. The uploaded manuscript keeps its own RC number exactly. Changed current-number or older inputs are refused rather than renumbered or overwritten; an optional target assertion must equal the uploaded number. Exact-content approval, hash-bound import evidence, immutable history, anchor checks, and transactional promotion remain in force. Focused regression coverage includes automatic jumps, exact input preservation, unchanged-number refusal and exact subsequent upload numbering, and downgrade refusal. RC512 manuscript bytes remain unchanged; no new manuscript or PDF build is part of this tooling update. Verification: `python tools/dev.py check` PASS; 326 tests, 3 expected skips; dependencies, baseline, immutable history, and whitespace PASS.

## Owner-supplied RC512 manuscript - 2026-10-21

Owner instruction: "Update the repo to have RC512 be the new working manuscript after updating the import workflow to support version jumps." The reviewed import promotes RC493 directly to RC512, retaining every earlier snapshot and exact patch archive; no RC494-RC511 snapshots are invented. `source/versions.json` and `config/production.json` identify `source/Heraldry_RC512.md`. Its SHA-256 is `816a3f9c81f91351cf24209580c18b3bd26e95ad747c9a13623304cf584ac5dd`, byte-identical to the supplied upload, with no normalisations. The manuscript includes 24 Basic Mode Hero profiles.

The import reports +1,358 / -835 text lines; all 63 publication anchors resolve after updating only FIG-07, FIG-08, and FIG-12 prefixes to the corresponding new passages. 56 figure dependencies changed (all except FIG-09); these require fresh semantic review and source-citation inspection before the next release. Existing artwork/figure approvals and hash-bound PDF evidence were not renewed. The pending Hero illustration request has not generated any images; the art queue remains empty.

Verification after promotion: `python tools/dev.py check` PASS; 324 tests, 3 expected skips, dependencies, baseline, immutable history (19 previous snapshot/evidence files), and whitespace PASS.

No PDF build or release was requested. Last delivered PDFs remain RC492-build-37; the RC493 compact local proof and existing `dist/` ledgers describe historical inputs. Physical print **NOT TESTED**.

## Explicit manuscript import targets - 2026-10-21

Owner authorised the RC493-to-RC512 import and support for version jumps. `manuscript prepare --target-rc N` binds a strictly higher target into the reviewed batch; apply retains exact candidate/base checks, immutable history, and rollback. Ordinary revisions still increment by one. Regression coverage includes exact jump promotion, invalid targets, tampered review targets, and missing jump evidence. Repository check PASS: 324 tests, 3 expected skips; baseline, dependencies, history, and whitespace PASS. No publication build. RC512 promotion follows in a separate checked transaction.

## Repeatable layout workflow - 2026-10-20, tooling only

The compact-layout pass's lessons are integrated into [the layout workflow](../docs/LAYOUT_WORKFLOW.md): exact-input, PDF-verified measurement caching shared by local and CI runs; semantic table-width policies that survive numbering changes; content-bound converged balancing hints; and a local plan/check/run front door with fail-fast stages, input freezing, timings, report hashes, and archived review substrates. Changed manuscripts receive fresh measurements and full QA. Last-delivered print instructions and release ledgers are preserved.

This iteration uses regression tests and bounded compiler fixtures, not another full-book build. The 603-page proof below remains evidence for its previous exact inputs, not certification of the updated workflow's full output. RC493 and approved art/figures are unchanged. Last delivered release remains RC492-build-37; physical print **NOT TESTED**.

Verification: focused workflow check PASS; dependency, baseline, immutable-history, and whitespace checks PASS; final `make test` runs 321 tests with 3 expected skips and no failures. The final suite includes cache invalidation/corruption/bypass, numbering-stable policies, edited-content tail rejection, and staged failure handling. No new full-book timing benchmark is claimed.

## Approved compact layout implementation - 2026-10-20, local proof reviewed

Owner authorization: all researched layout proposals accepted, with 10.5 pt body, 9 pt tables, narrower margins, and more assertive improvement; resumed by "Continue". RC493 is unchanged at SHA-256 `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`. The same-source old-layout baseline is 673 pages; the final local interiors are **603 pages**, saving **70 pages (10.40%)**. Digital: 606 pages. See [implementation and evidence](../reports/Compact%20layout%20implementation.md).

The shared compact profile controls composition, table allocation, measurement, and QA. Full-width opening flavour, two-column rules, tighter component spacing, measured table widening, substantive heading keeps, safe native list splits, real continuation identity, and Index clearance are implemented. Exact-PDF attachments replace separately recompiled position/height queries. Source keep coverage is independently enumerated and physical destinations corroborate the final attachment.

Final cream SHA-256 `bda0a463dd2c4082cfe795fc985f953dfdc7dbc80c8699c6d5a45793e79da927`. Local checks: all 8,430 source blocks and 10,315 cells reconcile in cream/digital; 2,736/2,736 keeps audited, 2,492 fit-capable, zero avoidable splits/missing coverage; 832 physical destinations agree; zero layout detector flags; cream/white inkjet checks PASS; supplementary cream/white geometry and content comparison PASS. All 57 manifest review images were actually inspected with no confirmed major finding; twelve extra integration detail renders were inspected. Residual cosmetic whitespace is documented, not claimed eliminated. Physical print and glyph-by-glyph proofreading are not certified.

`python tools/dev.py check`: 281 tests run, 3 expected skips, no failures; dependencies, baseline preflight, immutable history, and whitespace PASS. Evidence is preserved under ignored `build/checks/layout-v5/`; the original recovery stash and `resume-preserved-20261020/` remain retained. Local proof is not a published candidate or a production visual-ledger approval. No new RC, art approval, or release ledger was created. Last delivered release remains RC492-build-37; physical print **NOT TESTED**.


## Publishing integrity corrections - 2026-10-17

Scoped code-only hardening, no manuscript revision and no PDF build. CI investigation found four Windows test cleanup failures from an unclosed PyMuPDF document (fixed with a context manager), plus an obsolete preflight restriction of three font families despite the approved v4's four families (corrected). The remaining standalone query utility now reads hash-checked positions captured by the PDF compiler instead of invoking a second layout pass.

Corrections include: active v4 production/design tokens and table estimator sizes; preservation of right-aligned table cells; one true start/end marker for each stat block and figure; mandatory rejection of duplicate, orphaned, or reversed keep/table/figure markers; and cream/white comparison of word geometry, raster/vector placements, links and PDF outlines, not just extracted text. Cross-platform regression tests cover the affected cases. Old RC492 release files and historical audits were not rewritten.

Limits: the next owner-requested RC493 candidate must exercise the entire revised compiler, pagination, physical PDF location gate, marker accounting, and cream/white geometry gate on the full book. Earlier confirmed historical RC492 C.5 page-map disagreement has not been retroactively cured. Continue table/scenario naming, paragraph-tail design improvements, measurement calibration and physical printing through rendered specimens and physical proof, not unverified layout changes.


## PDF page-map gate repair - 2026-10-17

Code-only repair on main: `tools/typst_run.py` now captures all QA location queries in the same compiler process that writes the cream print PDF, recording that PDF's SHA-256 and the generated Typst source hash. `tools/verify.py` consumes only the compile-bound query; a second Typst compiler cannot silently supply uncorroborated page numbers. The new mandatory `page_map_accuracy` check independently compares uniquely named headings against physical bookmark destinations in the serialized PDF and validates the bounds of heading, table, index, and keep markers. Missing coverage, different hashes, or page disagreements block publication. Regression tests reproduce the previously reported C.5 page shift and stale hashes.

Scope: publishing-tool code and tests only. Neither the canonical RC493 manuscript nor the RC492-build-37 PDFs and their historical QA ledgers were modified. The October 16 page-map discrepancy in that historical delivery remains documented; the new gate must be exercised against the next explicitly requested full candidate build before its end-to-end behaviour can be certified. No PDF build or physical proof was performed as part of this repair.


Updated 2026-10-16. Working/delivery branch: **main**.

## PDF layout and density review - 2026-10-16

Review/proposals only: the exact RC492-build-37 cream interior (SHA-256 `10e4f8bea8cff69404a6ee1385077e0533b767ff1815714cd0b2532e245a8e78`) received an all-672-page geometry census and direct visual inspection of 25 distinct pages. All ten private reference books were hash verified and 24 selected viewer pages directly inspected. Live RC493 pipeline code and primary-source design guidance informed [the detailed report](../reports/Rulebook%20layout%20and%20density%20review.md).

Highest-priority finding: a hash-bound QA page map disagrees with the serialized PDF's C.5/T327 locations; cause unresolved, without a claim of missing content or an actual forbidden split. Proposed sequence: repair measurement/coverage, centralize intended style values, fix alignment/continuation/marker defects, then compare spacing/table-inset specimens with 11 pt body and current margins retained. Preserve complete-unit keeps and the accepted p6 blank verso. Baseline: 203 tests PASS, 3 expected skips. No manuscript/layout implementation, full PDF build, release, ledger rebinding, new visual approval, or physical proof occurred. Page savings remain unmeasured; proposals await owner review.

## README automation - 2026-10-16

Validation: baseline 190 tests and final 203 tests PASS (3 expected skips); all 13 README regressions PASS. Dependencies, baseline preflight, immutable history, and whitespace PASS. Corrected two existing Windows CI assertions to compare resolved temporary paths; both focused checks PASS. Hosted activation is checked after pushing this implementation; see GitHub's `Update GitHub README` run and its README-only bot commit for current execution evidence.

Owner request: keep the GitHub README automatically updated after changes. Generated status and recent-change blocks now derive from checked repository records and Git history; surrounding guidance remains hand-written. `tools/dev.py check` refreshes locally. A main-push/workflow-completion Actions workflow publishes README-only commits after required checks, shares the publication queue, and defers for pending builds. Review found no blocking defect; the suggested non-race retry guard was applied. Implementation and recovery details: `docs/README_AUTOMATION.md`. Hosted activation and final check results are recorded with the delivery checkpoint; no new publication build is requested.

## Active manuscript

`source/versions.json` identifies `source/Heraldry_RC493.md`, SHA-256 `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`. The owner approved all ten publication editorial replacements and five canon alignments on 2026-10-15. Exact applied evidence is `editorial/history/RC493.json`; prior snapshots and archives remain unchanged. `docs/CANON_AUTHORITY.md` records the approved working conventions.

Last PDF delivery remains **RC492-build-37**, 672 interior / 675 digital pages, and predates RC493. No RC493 PDF or full-format/physical approval is claimed. See `production/RELEASE_STATUS.md` and the latest checkpoint below.

All-figure pass completed 2026-10-16: all 57 figures freshly compared with RC493 and directly reviewed as standalone renders; 25 SVGs and 9 captions improved. The four open copy follow-ups are resolved. Current figure gate PASS 57/57, no stale entries or open findings. Actual review scope, source qualifications, and image evidence: `production/qa/figure-review-all-rc493.md`. This does not replace the last release's PDF or physical-proof evidence.

## Historical RC487 checkpoint - 2026-10-10

### Manuscript authority at that checkpoint

`source/versions.json` identifies `source/Heraldry_RC487.md`, SHA-256 `d77a72f9030061f76ea61e947bf520dcc81628bd653f61ba144f2a474a088254`. RC487 applies one owner-authorized batch of 48 exact repairs archived in `editorial/history/RC487.json`. RC484–RC486 and their archived history remain unchanged. Future text edits follow `docs/WORKFLOW.md` and promote a new snapshot; artwork/figure/layout edits use Git commits without an RC bump.

### Delivery and verification at that checkpoint

RC487 digital: 600 pages; cream and white interiors: 597 pages each. All 597 cream interior pages were inspected on contact sheets, with nineteen detailed pages, both cover variants, calibration and an overscan specimen. Visual/figure ledgers describe the actual review scope and current hashes. Current figure review is by the repair author; historical independent findings are retained.

17 regression tests and 8 source preflight checks pass. Reconciliation preserves 8,429 text blocks in order and all 332 tables / 10,315 current cells. All 835 printed item Cost/Value cells are unchanged; development price multipliers/formulas and quality-table Value columns are removed. All 50 special weapon base profiles resolve. 1,539 fit-capable units have no avoidable splits or missing coverage. All 57 figures pass the current source-bound review gate. The 19-check release gate and package audit are recorded in `production/qa/STATUS.json` and `production/qa/package-audit.json`.

The contradiction audit is closed for F01–F21 and U01–U06 in `production/qa/manuscript-contradiction-resolution.md`; the original RC486 audit remains historical evidence. Owner-authorized completions and new illustrative dice results are explicit in the closure record. Exact reconstruction and immutable hashes are verified by `production/qa/manuscript-repair-verification.json`.

### Remaining inputs at that checkpoint

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

## Independent RC488 audit resolved: RC489 and RC490 — 2026-10-10
- Owner asked to double-check the manuscript and illustration instructions. Two independent audits were archived in production/qa/rc488-audit-manuscript.json and rc488-audit-art.json.
- **RC489** (31 patches; owner: "yes but replace staff with the mundane weapon quarterstaff"):
  - Forsaken Duelist rapier.
  - Flavour/stat-block consistency for 9 monsters.
  - Elder Vrymk melee wording.
  - In-climate creatures in Pale City 3 and 13 secondary objectives.
  - Stray "None." bullets removed.
  - Deep Elf Priest and Mire 2 Scale-Shaman Quarterstaff.
- **RC490:** one corrective patch for my duplicated Tomb Guardian clause in RC489-04, found by the independent figure re-review.
- **Figures:** citations remapped with tools/remap_figure_lines.py; independent delta reviews give gate 57/57, 0 open.
- **Art:**
  - Prompt builder: "must" requirements separated from prohibitions; isolation framing kept for figure families; traditions are scene vignettes; chapter art is 4.5 in.
  - ChatGPT Work instructions: Git LFS, rebase before push, file types.
  - All 274 briefs fixed (scenery-free figures, stat-block weapons, cover party per Package A, scale figures, de-duplication) and updated to RC489 text.
- **Build:** 597 pages; every changed page inspected; 19/19 checks PASS; RC490 release ZIP built.
- **Left open, not owner-approved:** Desert Naga Hexscale gives Sleeping where the flavour says weak; Undermarches 6 allied Spectre reward; judgement-call size and trait wording (production/art/SOURCE_NOTES.md). Physical proof NOT TESTED.
- **RC491** (owner, 2026-10-10: "Change desert nagas flavour text to match. Undermarch Scenario 6 spectre reward should be changed to the closest thematic match within the undermarch bestiary. Medium is ox-sized."):
  - Desert Naga flavour now reads "hexing the strong into an unnatural sleep".
  - The Shadow Brand reward is an allied Noxcloth Summon.
  - Art size words: M runs from human-sized up to ox-sized.
  - Figure delta review recorded; gate 57/57.
  - Pages 304 and 434 inspected; 19/19 checks PASS; RC491 release ZIP built.
  - No open owner decisions remain from the RC488 audit; the judgement calls B-13..B-17 are left as written.
- **RC492** (owner, 2026-10-10: "I was wrong to say medium is an ox; please revert to previous size definitions. A briarling would be medium but a basilisk would be large. Remove the awkward ox-sized reference in the flavour text. ... We would either revert it to how it was before or rewrite it ..."):
  - The Basilisk is coded L, and its flavour drops "the size of an ox". The Briarling stays M.
  - Undermarches 6 Shadow Brand reverts to the allied Spectre Summon. The orchestrator chose the revert because the bound spirit is a spectre-like undead.
  - Art size words reverted: M is "about human-sized"; L is "roughly twice a human's height or bulk". The Basilisk brief is now Large.
  - Figure delta review recorded; gate 57/57.
  - Pages 280 and 434 inspected; 19/19 checks PASS; RC492 release ZIP built. Physical proof NOT TESTED.
- **ChatGPT Work skill v4** (artwork track; no manuscript change, so no RC increment; owner asked 2026-10-10 to review the v3.1 skill zip and produce v4):
  - Queue schema 2: each item has a register, at most three references chosen for that register, printed width, attempt budget and the brief's must and avoid lists. The old queue attached every reference to every item.
  - New: `production/art/skill/heraldry-classic-ink-art/` (SKILL.md, references, `heraldry_art.py`, `validate_skill.py`), `tools/art_skill_build.py` and `production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip`. `production/art/gpt/INSTRUCTIONS.md` rewritten to match; `docs/ART_AUTOMATION.md` updated.
  - Tests: `tests/test_art_skill.py` (helper classification calibrated on real and synthetic images, parity with `art_ink`, a real git state machine, package currency).
  - Art generation still awaits the owner running ChatGPT Work on the anchors queue. No new images exist yet.
- **Skill v6 and the offline ChatGPT Work input package** (artwork track and tooling; no manuscript change, so no RC increment; 2026-10-11):
  - Owner installed skill v6 (commit 924bb3c) as the working version. Work's first v6 test was BLOCKED before generation: shell git could not authenticate, and the connector could not fetch STYLE-REF-01/02 as binaries. No images were produced.
  - Owner request: a self-contained Work input ZIP with provenance, an offline preflight, bundle delivery with QA evidence, the ZIP attached for download, and a credential-free test. New `tools/art_work_package.py` (build / verify / check / verify-bundle). `work_preflight.py --offline-package`. Helper `bundle` now carries the QA reports, a hash manifest and `pushed_to_github: false`, after the same receipt gate as `delivery_guard.py`, which refuses in a package folder. The owner's `work-calibration-inputs` workflow uses the same builder.
  - Package: `production/art/work/Heraldry_Work_Input_anchors.zip` (built from source commit cdd189e; SHA-256 in `production/art/work/WORK_PACKAGE.json` and in the commit message). It holds the 5 anchor prompts and all 4 queue references as decodable JPEG bytes. Verified offline: READY, delivery bundle, git unused, remote NOT_ATTEMPTED. The same checks passed with no git on PATH, and the Actions export run passed too.
  - Tests: `tests/test_art_work_package.py` (end-to-end with synthetic stand-ins: five saves, bundle, reviewer check, tamper cases) and the skill's `tests/test_offline_package.py`.
  - Follow-up (2026-10-11): in a package, the scratch folder now defaults to the sibling `<package>_scratch`. START_HERE uses explicit `/mnt/data/heraldry_work` paths. Package rebuilt from commit 93d001f. A literal START_HERE rehearsal with no git on PATH ran five synthetic saves, then sheet, style audit and bundle; status then said STOP and verify-bundle PASSED. The 275-prompt audit found every prompt has shared style plus its own composition, details and mood, and 262 carry verbatim flavour. Exceptions: the cover and chapter openers have no in-world flavour passage, and six world/tradition sources are short in the manuscript. Eleven two-word mood lines were expanded (not queued).
  - Still NOT VERIFIED: in Work, image-reference attachment and native-file access (the Work smoke test). No artwork exists or is approved. Work generates the five anchors only, returns a review bundle, and stops. Claude Code runs `verify-bundle`, then visual review, then intake.
- **ChatGPT Work anchors received; visual review passed** (artwork track; no RC increment; 2026-10-11): Work returned a review bundle from package 93d001f. verify-bundle PASS; the Work smoke record attests reference attachment and native-file access. Visual review is in `production/art/review/ANCHOR_REVIEW_2026-10-11.md`: all five ANCHOR-APPROVE, with recorded notes on the Greenmark top margin and hounds, the occluded eighth tarantula leg, and two 1254 px squares. The container's network policy denies `lfs.github.com`, so the images cannot be pushed from here. The bundle is committed unchanged to `production/art/work/inbox/`, and the new `Import Work review bundle` workflow verifies it, commits the images through LFS on GitHub and runs the intake. The import workflow ran (commit 9b2baa2); the LFS images match the bundle byte for byte and intake raised no warnings. `approve-anchors` recorded six GPT anchors, including Greythorn. Placed in the book: the delivery grows to 598 pages (6.9 Ancestries +1). Changed pages 4-5, 11-14, 99-115, 265 and 277 were inspected, the visual ledger was re-signed for PDF 1cef40de, and the local `make verify` release gate PASSED. Next: publish the batch queue and its Work package.
- **Build on request only** (owner decision 2026-10-11, verbatim: "Rewrite our projects protocol to avoid recreating the entire pdf layout each time we make a change. We should only redo the layout or produce a new pdf when we specifically ask."). CLAUDE.md, docs/WORKFLOW.md, production/art/HANDOFF.md and RELEASE_STATUS now say: commit changes with `make test` and their own track's checks; run `make clean all verify package`, page inspection and the visual ledger only when the owner asks for a build, a PDF or a layout pass. `Rebuild verified delivery` is now manual (workflow_dispatch only; it no longer fires on pushes to provenance or the visual ledger). `dist/` describes the last requested build (2026-10-11, anchors placed, 598 pages), and reports must say when the source has moved past it. Rules: no RC change.
- **Hand-inked art direction; anchors back to redo** (owner, 2026-10-11, verbatim: "our proofs and test images need improvement in their artistic direction. They are all too hyper detailed, AI-like, low-resolution. I'd like them to be a notch more hand drawn and authentic human art-like. I'd like to use gpt image 2.5 sunburst if possible."). Three of the four attached examples are byte-identical (by perceptual hash) to STYLE-REF-01/02/03; the fourth, a Dying Lands map, is stored as inspiration only because it has lettering. Changes: `prompt_v2` rewritten for hand-inked line, economy of line, selective hatching and open paper, with the "exceptionally detailed / intricate / stippling" wording removed. Reference sets are now the owner's samples only, and generated images are never references. The queue size is now a minimum, so larger output at the same aspect passes (helper and delivery_guard, with tests). Preferred model: GPT Image 2.5 Sunburst if offered, with the model recorded per receipt. The five calibration anchors were rejected with the direction as the redo reason, ANCHORS.json is superseded, and the anchors queue was republished with new prompt hashes. Greythorn stays approved but is no longer a reference. Updated: docs/ART_DIRECTION.md, the skill STYLE.md and SKILL.md, INSTRUCTIONS.md and START_HERE. No build (build on request). The last build in dist/ still contains the five superseded anchors.
- **Git token route for Work: withdrawn** (2026-10-11). The owner asked for a workflow without ZIP copying. A fine-grained-token design was written, but ChatGPT refused it and flagged the pasted token as a leaked secret. The route is withdrawn: `WORK_PROMPT.md` is credential-free again, and INSTRUCTIONS.md and ART_AUTOMATION.md say never to put a credential in a Work conversation. The owner should revoke any token that was pasted. Current flow: input package to Work, review bundle back, upload to `production/art/work/inbox/` (auto-import) or attach to Claude. Claude's container can push LFS directly. Open: probe whether ChatGPT's GitHub connector can read the large references and write files.


- **ChatGPT GitHub plugin probes** (2026-10-11): Work committed a 1x1 PNG and a text file to `main` (b9eca95, d865859), so small writes work. Files pass inline only: reads up to about 0.95 MB, empty at 1.1 MB, with no sandbox transfer and no path or stream upload. The plugin cannot move artwork or the 1.6 and 2.7 MB samples. Probe files removed. The input package and review bundle stay as the transport; the only way to reduce hand-offs is larger batches per Work session and review-bundle parts that fit GitHub's 25 MB browser upload limit, both proposed to the owner and not changed.
\n
- **Codex art route** (owner, 2026-10-11: "I got codex on my windows pc working with access to my computer GitHub, git, lfs, and python. I want to continue with image generation there"; earlier "within my chat gpt plus subscription without paying more for api"). New `AGENTS.md` (Codex reads it; CLAUDE.md governs; Codex writes only incoming images and receipts through `delivery_guard ship`), `production/art/codex/CODEX_RUNBOOK.md`, `CODEX_PROMPT.md` and `PROJECT_HANDOFF.md`. CLAUDE.md and ART_AUTOMATION.md now name the Codex route, with ChatGPT Work plus the offline package as fallback. `.gitattributes` pins the art queue, prompts and skill to LF for Windows. A handoff ZIP of the project, workflow and skill was given to the owner. Open: whether Codex's in-plan image generation accepts reference images; it checks before generating.



## Local Codex and GitHub main instructions - 2026-10-11

- Owner authorization: GitHub main should be the primary workflow; "Ok apply your proposals" authorizes this documentation maintenance change outside the art worker's normal incoming-image/receipt allowlist. Production ownership and its delivery guard remain unchanged.
- Reconciled WORK_PROMPT.md, CODEX_PROMPT.md, CODEX_RUNBOOK.md, PROJECT_HANDOFF.md, and the artwork route in RELEASE_STATUS.md. GitHub main is authoritative; artwork uses guarded direct-to-main LFS delivery. ZIP input/review bundles remain fallback only.
- Preserved exact queued prompts and listed references, original native bytes, counted smoke attempts, all ten QA criteria, attempt budgets, independent review, and the stop after five anchors. Explicitly prohibited pull/rebase over unsent artwork or receipts; blocked delivery goes to bundle and maintainer reconciliation.
- Readiness-only work does not authorize generation. No artwork, production receipts, approvals, manuscript revisions, or PDFs were produced by this instruction update. Existing dist and build/visual evidence remain scoped to the last requested build.

Validation: source preflight PASS (8 checks); art preflight READY; documentation links, fenced blocks, allowlist, preserved offline procedure, and git diff --check PASS. The repository suite ran 71 tests (1 Windows helper-path failure, 23 skipped); the v6 suite ran 32 tests (1 Windows reference-path failure). Tests, helpers, queued prompts, receipts, and packaged inputs were unchanged. Local CRLF conversion was disabled after restoring unchanged text to its exact committed LF bytes. These failures remain open; no production smoke or LFS artwork push was tested.
- **Codex commit reviewed and Windows fixes** (2026-10-11). Codex's ac187ad (docs only: CODEX_PROMPT, CODEX_RUNBOOK, PROJECT_HANDOFF, WORK_PROMPT and the RELEASE_STATUS route row, made under owner authorization "Ok apply your proposals") was reviewed and fast-forwarded. It is consistent with the guarded delivery, the counted smoke gate and the stop after the anchors. The stale branch `art/upgrade-classic-ink-v6` is byte-identical to its squash merge 924bb3c, so nothing is unmerged. The two Windows test failures Codex reported are fixed. (1) `helper()` printed `os.path.relpath` backslash paths; it now prints forward slashes, which work in PowerShell. (2) `fidelity_gate.verify_record` compared reference paths separator-sensitively; both sides are now normalised, and the tests build POSIX queue paths. Also on Windows: receipts are appended with LF, `style_audit` and the save message use POSIX paths. A new test covers backslash paths. Skill ZIP and Work input package rebuilt. Not yet shown on Windows itself: Codex's next readiness run should show the full suites passing.
- **Anchors round 2 (Codex) reviewed** (2026-10-11). Codex generated the five anchors under the hand-inked direction. Its push was blocked by a delivery_guard bug (stripped porcelain status lost the first path's first letter), fixed in 3887ed6 with a test. The bundle was verified and delivered with the fixed guard (081ee0e, LFS), and intake ran (0e11e1f, no warnings). Review `production/art/review/ANCHOR_REVIEW_2026-10-11b.md`: Greenmark, Undead Champion, Fighter and Dwarf APPROVED. Giant Tarantula sent back: only seven feet are visible, the second time, against the "exactly eight legs" requirement. Its composition brief is amended (legs splayed clear, helm apart) and the anchors queue republished with the tarantula only. `approve-anchors` (the batch gate) waits for it. No build (build on request); dist/ still predates these images.
- **Batch automation and token efficiency** (owner, 2026-10-11: "fix any outstanding issues with the gpt image generation workflow ... more efficient on token usage ... streamlined and automated so once I give the go ahead all 100s of planned images can be generated all at once"). Fixed:
  - `delivery_guard ship` stopped at every second delivery because the intake bot always advances main. It now does a safe fast-forward (disjoint paths only), retries a lost push, and stops on divergence or overlap; 3 real-git tests cover this.
  - The push cadence comes from the queue (`push_every` 10).
  - New `heraldry_art.py qa` pre-filled draft; `save` uses it automatically.
  - START_HERE is phase-aware.
  - The end-to-end tests no longer assume a 5-item queue.

  Batch opened: the tarantula moved from the anchor gate into the batch as a redo, `approve-anchors` set ANCHORS approved (Greythorn plus 4), and the batch queue was published with 270 items. New `production/art/codex/BATCH_CARD.md` (the one-page contract), a short `CODEX_PROMPT.md` (one go-ahead line; resumable), a slimmer `AGENTS.md`, and `art_intake.py pending` for compact review. Not yet shown: a real unattended Codex run of the batch, the ChatGPT plan's image limits, and the Windows test run.
- **Per-image delivery** (owner, 2026-10-11: "do one image at a time then push it ... so we don't run into a block at the 5hr or weekly usage limits"). Interpreted as: deliver each image as soon as it passes Codex's checks. Claude's review stays asynchronous; waiting for Claude's approval of every image would stall the run. Changes:
  - The queue now sets `push_every: 1` and `review_every: 10`.
  - `status` says DELIVER after each save, and DRIFT REVIEW every 10th image, using the new `sheet --recent 10` and `style_audit.py --recent 10`.
  - Tests cover the cadence.
  - Fixed: the intake workflows downloaded every incoming LFS image on every run, which at one image per push would have used tens of GB of LFS bandwidth. `art_intake.py needs-pull` lists only pointers whose oid is not yet recorded, and scan skips recorded pointers (test added).
  - BATCH_CARD and CODEX_PROMPT were updated, and the batch queue was republished (270 items).

- **Gritty old-school art direction** (owner, 2026-10-11, with eleven attached examples: "I want to redo the art inspiration a bit to move our current art benchmarks and inspiration to be closer to the more old school black and white gritty style artworks such as those attached").
  - **References:** seven pure-black-ink examples became STYLE-REF-04 to STYLE-REF-10 (`assets/art/style/`, `STYLE_REFS.json`). One example was STYLE-REF-03 again (byte-identical) and stays.
  - **Mood only:** three ink-wash examples (`STYLE-INSPIRATION-wash-*`) are never attached. Grey wash cannot print in the book's pure black ink, and the pipeline still rejects it.
  - **Superseded:** STYLE-REF-01/02 (clean engraved line) stay on file but are no longer attached.
  - **Reference sets:**

    | Register | References |
    |---|---|
    | Scene | 09, 10, 07 |
    | Creature | 04, 05, 03 |
    | Person | 04, 06, 03 |
    | Still life | 04, 03 |

  - **Prompts:** `prompt_v2` (intro, style, final and reference wording) now asks for bold rough brush contours, heavy solid blacks, scratchy hatching and dry-brush with woodcut bite, high contrast and visible human marks. It still forbids grey wash, stipple fields, machine-even texture and clean vector-like line.
  - **Skill (v6, rebuilt):** `STYLE.md`, `STYLE_CONSISTENCY_V6.md`, `VISUAL_ACCEPTANCE_V6.md` and `REPAIR.md` follow the new direction. REPAIR.md has a new "too clean" correction. The ZIP now carries the new references.
  - **Updated alongside:** the Codex BATCH_CARD, runbook, WORK_PROMPT and the fallback package text.
  - **Queue:** the 270-item batch was republished with new prompt hashes. No images had been made from the old prompts.
  - **Calibration:** CODEX_PROMPT recommends a first run that stops after 5 images for review.
  - **Approved art:** Greythorn and the four hand-inked anchors remain approved; whether to redo them for consistency is for the owner to decide.
  - No manuscript change and no build. `dist/` still predates this art.
- **Reference cut** (owner, 2026-10-11, after reviewing the reference sheets: "Cut 01 town scene and use the best of the attached city scenes instead"). STYLE-REF-01 is removed; it remains in git history.
  - **Replacement:** of the four attached city scenes, two were near copies of the approved sepia Greythorn render, with grey tone, and one was very dense, close to the rejected hyper-detailed look. The chosen one is bold black-and-white with open sky and the lowest grey. It is now STYLE-REF-11.
  - **Where it is attached:** a new `family_sets` override in `gpt_reference_sets` (honoured by `tools/art_gpt_pack.py`) gives bastion and world scenes 11, 09 and 07. All other scenes keep 09, 10 and 07, so town features do not bleed into them.
  - **Owner exception:** STYLE-REF-11 looks machine-made but is attached on the owner's instruction.
  - **Queue:** republished; the reference lists of 13 items changed, and the prompt text is unchanged.
  - **Updated alongside:** the skill ZIP, the fallback package and the tests (bastion and world items, and only those, carry STYLE-REF-11).
- **References promoted** (owner, 2026-10-11: "Promote woodcut fencers and 02 city panorama"). Each item still carries at most 3 references, so:
  - **Bastion and world scenes:** STYLE-REF-11, STYLE-REF-02 and STYLE-REF-09. The panorama is a city, so it joins the town set and replaces 07 there.
  - **Persons (classes and ancestries):** STYLE-REF-04, STYLE-REF-06 and STYLE-REF-08. The woodcut fencers are full-length human figures with strong silhouettes, so they replace 03 there.
  - **STYLE-REF-03:** kept for creatures and still lifes.
  - **Queue:** republished; only reference lists changed, not prompt text.
  - **Updated alongside:** the skill ZIP, the fallback package and the tests.
- **Reference bank** (owner, 2026-10-11, sixteen examples: "Bank these example art pieces I'm going to send more"). They are stored as STYLE-REF-12 to STYLE-REF-27 in `assets/art/style/` and recorded under `banked` in `STYLE_REFS.json`, each with a category and any caveat (grey tone, screen tone, monogram or pseudo-writing).
  - **Coverage:** still lifes and equipment, non-undead beasts, cavern and swamp landscapes, interiors, and magic.
  - **Not attached yet:** no reference set, prompt or queue changed. The sets will be revised once the owner has sent the rest.
- **Reference bank, second batch** (owner, 2026-10-11, fourteen more examples). Thirteen are banked as STYLE-REF-28 to STYLE-REF-40. The fourteenth was STYLE-REF-26 again (byte-identical) and was not stored twice.
  - **Coverage:** magic in action, insect and beastfolk creatures, an adventuring-gear sheet, more items, a forest landscape and dungeon scenes.
  - **Caveats recorded:** stipple fields in 30 and 31, small images (32, 33, 35, 39, 40), a narrow image (37) and grey paper borders (33, 34).
  - **Not attached yet:** no reference set, prompt or queue changed.
- **Reference completion, mapping v7, prompt audit and skill v7** (owner, 2026-10-11: "Search the internet for example art to fulfill your request ... continue with reanalysis of all of the art to ensure optimally mapped. Check the illustrations prompts to ensure they are correct. Update the gpt skill to v7 ... prepare gpt to run the system as originally planned so we can generate all the images autonomously").
  - **Search:**
    - Wikimedia rate-limited this connection.
    - Gutenberg's Sime plates are halftone grey, and its Pyle plates carry lettering and frames.
    - From Art Institute of Chicago CC0 prints, four were added as STYLE-REF-41 to 44: two Callot beggars, Piranesi's *The Drawbridge* and Haden's *Challow Farm*. Each was levelled to black on white, with the plate number or signature painted out; provenance is in `STYLE_REFS.json` under `public_domain`.
    - Rejected: Bresdin (too dense, and black after levelling), Rembrandt's *Monk in the Cornfield* (subject unsuitable), and Doré paintings (grey).
    - No usable gritty public-domain desert, ash or snow landscape was found; this is recorded as still open.
  - **Mapping v7:** 17 reference sets, in `docs/ART_DIRECTION.md`. Five monster kinds are assigned by ID, with a coverage check; every other family has its own set. `ref_set` is recorded per item, and ten items, one per set, lead the queue.
  - **Prompt audit:** all 270 prompts linted clean. Fixed: 32 dense-stipple brief details, the Elf longbow comparison, the chapter and cover composition duplication, the title line and the reference sentence. Still lifes have their own style line.
  - **Skill v7:** see `docs/ART_AUTOMATION.md`.
  - **Checks:** `make test`, the skill suite, the package verification and CI, recorded below.
  - No manuscript change and no build; `dist/` still predates this art.
- **Second full audit and debug pass** (owner, 2026-10-11: "Double check everything again ... Ensure the repo is without bugs and fix any bugs ... Debug the codebase"). Two independent audits ran: a semantic read of all 270 prompts, and a code review of the pipeline. Every finding was verified against the text or code before it was fixed.
  - **Prompts:**
    - About 50 brief defects fixed: source contradictions, internal contradictions, scale conflicts, seven near-duplicate pose pairs, glow, ray and tone wording, garbled lines, and "Wide" in square monster prompts.
    - Two auditor claims were rejected after checking: the Chapter 4 composition was already correct, and "Shadow Caller" is the rules' own name.
  - **Code:**
    - Intake and import workflows reset to the newest main on each attempt, with no full LFS smudge; the import has its own concurrency group.
    - `delivery_guard ship`:
      - recovers an unpushed commit;
      - rolls back on any failure;
      - pushes without credential prompts and reports real push errors;
      - recognises a push that landed;
      - accepts a format-change replacement.
    - Refusals bind to the prompt hash.
    - UTF-8 reads for Windows; `doctor` checks that LFS is installed in the clone; the dead aspect check is removed; `check` caches image hashes; `save_as` is removed from the queue; the illustration list marks redos; lint is clean.
    - Repository checks skip pure image deliveries.
  - **Tests:** six new real-git regression tests. Results are below.
- **Efficiency tidy-up** (owner, 2026-10-11: "tidy everything up in the code base to ensure it is highly efficient, fast, and without redundancy"). Removed only what duplicated another check, never a safeguard:
  - **CI workflows removed:**
    - `art-skill-release.yml`: its build, validation and tests duplicated repository checks, and its auto-commit could never be needed because the tests already require a current committed ZIP.
    - `work-calibration-inputs.yml`: the committed package is checked by the tests.
  - **Repository checks:** no longer rebuild the skill ZIP before testing it (the rebuild masked a stale ZIP), and they skip pure image deliveries.
  - **Worker steps:**
    - Delivery is one `ship --execute`. The separate `audit` step repeated the validation `ship` runs anyway, and is kept for diagnosis only.
    - The drift review no longer makes a second contact sheet.
    - `status`, the batch card, the operator card, SKILL.md, the runbook and the instructions all say the same.
  - **Speed:** `work_preflight` decoded or fully read each reference once per queue item (810 times for 28 files). It now checks each file once: about 10 s down to about 0.7 s at every session start and in package verification. The repository tests drop by about 30 s.
  - **Dead code:** 23 permanently skipped v4 tests, the legacy `build_release.py` builder (duplicating `tools/art_skill_build.py`), the v4 skill ZIP, and unused imports and helpers.
- **Prime-time debug and optimisation pass** (owner, 2026-10-11: "Please debug and optimize the repo, codebase, and gpt image generation skill one more time to make sure everything is ready for prime time!"). Two independent audits ran (worker docs versus scripts, and a simulated 25-image Codex run); each finding was verified before it was fixed.
  - **Queue lead:** `gpt_lead_ids` now has seventeen items, one per reference set (it had ten, so seven sets were first seen only after the second drift review). The queue was republished; the prompts are unchanged.
  - **Worker script fixes (`heraldry_art.py`):**
    - `status` lists redos first, like `next`.
    - The drift review count is monotonic, so a rejection no longer repeats a drift review.
    - The DRIFT REVIEW message says to deliver in every case and prints the exact `style_audit` command.
    - Helper commands print the running interpreter.
    - Receipts name the real surface (Codex or ChatGPT Work).
    - `sheet --out` inside the clone is refused.
    - `check` says when an attempt was the last allowed one.
    - LFS pointer files are skipped in the recent-image list.
  - **Other scripts:**
    - `style_audit` skips LFS pointers, defaults its report to the scratch folder and prints its advisories.
    - `delivery_guard ship` no longer fetches twice per delivery.
    - `art_intake needs-pull` ignores the 12 legacy non-catalog PNGs, which it had re-downloaded (about 37 MB) on every intake run.
  - **Docs:**
    - BATCH_CARD rewritten for PowerShell, with the exact QA-draft fields and `--must` rules and the LFS-pointer fix.
    - The stale smoke-file gate, "stop after 5 anchors", `--out` and v4 ZIP wording were removed from SKILL.md, the operator card, the references, the runbook, INSTRUCTIONS, WORK_PROMPT and ART_AUTOMATION.
    - The tarantula redo reason now uses the gritty-style wording.
  - **Lint:** unused imports and dead assignments were removed across `tools/`.
  - **Tests:** new regressions for the monotonic drift count, LFS pointers in `style_audit` and legacy pointers in `needs-pull`. The duplicate inherited cadence test runs were removed.
  - **Left open at that point:** three minor items from the simulated run, all fixed in the next pass. The first real Codex delivery is still the first live test of intake.
  - No manuscript change and no build; `dist/` still describes the last requested build.
- **Remaining issues fixed** (owner, 2026-10-11: "Fix all remaining issues first").
  - **Attempt numbering:** re-checking an earlier attempt to save it now reports that attempt's own number. The receipt records `saved_attempt` beside `variants_tried`, and the "beyond the budget" tripwire applies only to an image generated past the budget. Before, saving attempt 3 after a 4th was checked recorded attempt 4 and blamed the saved image.
  - **Review-sheet growth:** the intake bot no longer commits a contact-sheet JPEG on every run (about 30 MB of history over 270 one-image pushes). `tools/art_intake.py pending --sheet` fetches only the pending ink files and writes the sheets locally to `build/art/review/` (gitignored). The three sheets already committed stay.
  - **Mid-session rejections:** `next` and `status` first fast-forward a clean clone (`git pull --ff-only`, no prompts, 120 s timeout; skipped with unsent work or in the offline package; a failure only prints a note). A redo sent back during a run now shows on the next item instead of one delivery later, or not at all at the end of the queue.
  - **Found while fixing these:**
    - JPEG and WebP deliveries would have bypassed Git LFS. `.gitattributes` now LFS-tracks every incoming image format; the older plain-git Greythorn JPEG is exempted, so it shows no change.
    - `ship` and `doctor` enforce the LFS rule for every format.
    - The intake's `needs-pull` only looked at PNGs, so a JPEG or WebP pointer would never have been fetched.
    - Intake provenance named "ChatGPT Work" for every image; it now names the surface the receipt records.
  - **Tests:** new regressions for the saved attempt number, the refresh (with and without unsent work), the WebP pointer fetch and the local review sheets. The delivery tests now use real Git LFS against a local remote.
  - No manuscript change and no build; `dist/` still describes the last requested build.
- **Large-file workflow** (owner, 2026-10-11: "Use your best judgement and set up the leanest, most efficient, most logical high quality workflow for repeatedly dealing with large files and images for our project"). The policy is in `docs/LARGE_FILES.md`.
  - **Why:** the repository had reached about 490 MB on GitHub in eleven days. Most of it was rebuilt files committed over and over: 94 PDF versions (1.46 GB uncompressed) and the skill ZIP plus Work package (61 MB per art change).
  - **Built PDFs:**
    - No longer committed. `Rebuild verified delivery` publishes each requested build as a GitHub Release (`RC###-build-N`) and commits only the ledgers and `dist/RELEASE.json` (tag, URL, asset SHA-256).
    - Its checkout is a partial clone. It pulls only the LFS art the build places (the twelve masters and the ink derivatives, not the generated natives), through an `actions/cache`.
    - The release ZIP now leaves out generated native images (their ink derivatives ship, as `masters/` already did) and refuses LFS pointers.
    - The RC492 PDFs were removed from the working tree. They remain in Git history at 3da756f, and the link is in `docs/LARGE_FILES.md`.
  - **Art ZIPs:** the skill ZIP and the offline Work package are built on request into `build/art/`:
    - with `make art-packages` (about 5 s), or
    - with the new manual `Build art packages` workflow (a 30-day download).

    The tests build fresh copies and check that they are reproducible and valid. The `check` command and the committed copies are gone.
  - **Clones:** every workflow checks out with `filter: blob:none`. The Codex runbook clones the same way. A partial clone of the old tip took 9 s and 146 MB; with this change the tip loses the PDFs and ZIPs as well.
  - **PC copy of the images:** with `HERALDRY_ARCHIVE` set (`C:\Heraldry\art-archive`), `save` keeps one copy of each delivered image outside the clone, with no download; a redo replaces it.
  - **Inbox:** the import workflow removes a Work review bundle once its images are in LFS. The already-imported anchors bundle was removed.
  - **Not exercised:** the Release step runs only with the next requested build (build on request). It is checked for YAML and command syntax only.
  - No manuscript change and no build.
- **Single branch** (owner, 2026-10-11: "Can we safely merge all branches into main? ..." then "I want a single branch at all times if possible").
  - Nothing needed merging:
    - `claude/heraldry-rc484-build` has no commits that `main` lacks. It is the RC484 checkpoint, now recorded by commit `3818324466aec2d3ab0515f48f93c7c498a0a6ab` in CLAUDE.md.
    - `art/upgrade-classic-ink-v6` ends in a tree byte-identical to `924bb3c`, its squash merge, which is already in `main` and since superseded by v7. Merging it would only re-apply v6 files.
  - Deleting both remote branches is for the owner: this session's tools refused the tag push and the branch deletion.
- **Sync and stale-file sweep; new README** (owner, 2026-10-12: "make sure everything on your side and GitHub's side are all UpToDate and in synchrony with no dead/stale files (delete if found). Then update the repo's main branch readme").
  - **Sync:** local `main` equals `origin/main`, and `main` is GitHub's only branch.
  - **Removed:**
    - the four committed review images (`production/art/review/intake-*.jpg`, `anchors-proposed.png`), superseded by local sheets;
    - `tools/art_package.py`, a separate packager for the 12 masters written while their placement in the PDF was pending; the release ZIP covers them;
    - `production/art/codex/PROJECT_HANDOFF.md`, superseded by the batch card, runbook and `docs/ART_AUTOMATION.md`;
    - `README_SETUP.md`, a stale duplicate of README and CLAUDE.md (dropped from the preflight's required list and the package list).
  - **Moved:** the dated 2026-10-06 audit to `docs/history/`.
  - **Rewritten:**
    - `docs/ART_AUTOMATION.md` describes the current state only (v4/v6 history removed; it is here and in git);
    - `README.md` covers the current state, the tracks, how to work on the project, checks, builds on request and large files.
  - A reference scan found no other unreferenced files apart from workflows, tests, revision proposals and inspection records, which are kept. `tools/contact_sheet.py` is a live review tool and is now named in the README.
- **First Codex batch round reviewed; one generation per item** (2026-10-12).
  - **Delivery:** Codex delivered 8 images, each through `ship` and the intake, then stopped on a drift review because two images had narrow margins.
  - **Review** (Claude Code, full-size natives):
    - APPROVED: Deepwarden, The Ashlands, Skeleton Warrior, Dire Wolf, Orc, Gargoyle and Ranger. All are gritty bold black ink, true to their briefs and their must and avoid lines.
    - Giant Tarantula sent back for the third time: seven feet countable plus the palps. Its brief's composition is now a high view from above, the eight legs radiating evenly, four a side, every foot on the ground. The low front view, with forelegs raised, was hiding legs.
  - **Owner decision** ("the first image generated for each prompt is far superior to any further attempts ... change our approach to a single image generation per prompt"):
    - `gpt_max_attempts` is 1 for every item. Generate once in a fresh context; never retry.
    - A hard fail is saved with `--accept-flags --notes`, and the reviewer decides on a redo. A redo gets one fresh generation with at most two correction sentences.
    - Updated: the batch card, SKILL.md, `REPAIR.md` (now corrections for redos only), the operator card, the runbook, `VISUAL_ACCEPTANCE.md` and `docs/ART_AUTOMATION.md`.
  - **Margins:** the 8% figure-margin rule was forcing retries for no layout benefit, because the ink derivative is trimmed. A hard fail is now only a cropped subject or one touching an edge; `check` reports a narrow margin as an advisory only. A drift-review stop needs a shared style drift, not margins.
  - **Queue:** republished with 263 items, the tarantula redo first. Only the tarantula prompt changed. The queue-count test now allows for batch approvals.
  - **Next session:** stop after 11 images, which covers the ten reference sets not yet tested.
  - Codex's Ranger delivery went out before its drift review; the review was done right after it and found only the margin note. No build; `dist/` still describes the RC492 build.
- **Fresh start for all artwork** (owner, 2026-10-12: "clear the previously approved images so we can start fresh from the first image on our next run"; scope chosen: all 12).
  - **Cleared:** Greythorn, the four hand-inked anchors, the seven batch images just approved, and the rejected Giant Tarantula. Their native images and ink derivatives are removed from the working tree (they stay in Git history and LFS), and their SELECTIONS entries are deleted, so every item is pending again rather than a redo.
  - **Kept:**
    - the twelve original atmospheric masters, the build's chapter and cover fallback;
    - the owner-authored Greythorn prompt (`OWNER_PROMPTS.json`), still used verbatim;
    - `RECEIPTS.jsonl`, which is append-only.
  - **Queue:** republished with all 275 items, the seventeen lead items first (one per reference set). It records `receipts_base` (19 lines), and `heraldry_art` counts drift reviews only from receipts written after that, so the first review falls at image 10 (test added).
  - **Also:**
    - the skill ZIP no longer carries the Greythorn render as a bonus reference (generated images are never references);
    - `.gitattributes` drops the Greythorn exemption;
    - `assets/art/ink/README.md` keeps the folder present for the intake's `git add`.
  - **Next Codex run:** stop after 17. No build; `dist/` still describes the RC492 build, which contains the six earlier anchors.
- **Reference bank promoted** (owner, 2026-10-12: "Promote them if there is room in their most relevant category (3 images per category)"). Every set was already full at 3, so the owner chose to raise the limit to 4 per item and include the risky pieces.
  - **One banked image joined each set it fits best:**
    - beast: 22 wolf pack;
    - vermin: 35 grub beast;
    - humanoid: 32 goat-folk;
    - classes and ancestries: 42 Callot beggar on crutches;
    - background: 39 poison flask;
    - item: 24 flanged mace;
    - tradition: 12 wizard storm;
    - climate: 17 swamp hut;
    - world: 30 forest path;
    - campaign: 23 dungeon arches;
    - scenario: 31 dungeon melee.
  - **Unchanged:** undead, magical, boss, bastion, chapter and cover had no matching banked image, so they keep 3. 190 items now carry 4 references and 85 carry 3.
  - **Still unattached:** 14, 27, 33 and 40 (still lifes, with no slot left), plus the grey-wash mood pieces and the map.
  - **Accepted risks** (recorded in `docs/ART_DIRECTION.md`):
    - screen tone, stipple and grey tone in 12, 17, 23, 30 and 31;
    - a forest scene in the beast set (22), the one exception to the figure test's no-scenery rule.
  - **Housekeeping:**
    - The queue was republished; prompts are unchanged and only reference lists changed.
    - `STYLE_REFS.json` usage fields are now generated from the config; 13 of them had wrongly said "not attached" since mapping v7.
- **References adjusted** (owner, 2026-10-12: "22 wolf pack should be removed. Add the attached files", eight images).
  - **Removed:** 22 from the beast set (it stays on file).
  - **Added:** the eight images, stored unchanged as STYLE-REF-45 to 52 (all distinct from existing references by perceptual hash) and slotted where they fit and there was room:
    - 45 cathedral facade to bastions;
    - 46 round tower to chapters;
    - 47 barrow and dolmen to the cover;
    - 49 mountain-pass swordsman to bosses;
    - 50 flame-sword elf to magical monsters;
    - 52 crowned lich and 51 bandaged mummy to undead, replacing 38 gnoll there (38 stays in beasts and humanoids).
  - **Banked:** 48 bearded warrior, a bust with a black box background that could teach a frame, and no slot left.
  - **Result:** 263 items carry 4 references and the 12 beasts carry 3. The figure test lists the new scenic references (46, 47, 49) and 22, so none can reach an isolated figure.
  - **Housekeeping:** `STYLE_REFS.json`, `docs/ART_DIRECTION.md` and `STYLE.md` updated. The queue was republished, with prompts unchanged.
- **Bastion reference** (owner, 2026-10-12: "Here's another bastion").
  - Stored unchanged as STYLE-REF-53 (frost harbour city, 1536x1024 PNG, 4.3 MB, plain Git like the other style files). It replaces 09 in the bastion set; 09 stays in scenarios and world. The bastion set is now four images used nowhere else: 11, 02, 45 and 53.
  - **Caveat recorded:** it looks machine-made and very dense, with noticeable grey (43% mid-tones). Like STYLE-REF-11, it is attached on the owner's instruction.
  - The figure test lists it as scenic. The queue was republished, with prompts unchanged.
- **Wolf pack restored** (owner, 2026-10-12: "22 wolf pack for beasts"). STYLE-REF-22 is back in the beast set, which now holds 4. All 275 items carry 4 references. The figure test records 22 as the one owner-approved exception to its no-scenery rule. The queue was republished, with prompts unchanged.
- **Item references** (owner, 2026-10-12: "40 scythe for item; 27 scroll case for item, bone cross for item (not background)").
  - The item set is now 15 sword and mace, 40 scythe, 27 scroll case and 33 bone cross. 19 and 25 left items and stay in background, which is now four images used nowhere else.
  - 24 flanged mace is unattached: the cap of 4 forced one out, and it is the cleanest still life.
  - 27 carries a pseudo-writing risk, accepted by the owner. The queue was republished, with prompts unchanged.
  - Remaining for four unique images in every set: cover, chapter and world 3 each; vermin, humanoid and magical 2 each; beast 2; scenario 1; boss 1.
- **Fourteen more owner references** (owner, 2026-10-12: fifteen images, no text; the fifteenth was STYLE-REF-53 again, byte-identical, and was skipped).
  - Stored unchanged as STYLE-REF-54 to 67, all distinct by perceptual hash. Placed toward four unique images per set:
    - humanoid: 62 ratman and 66 trolls;
    - boss: 60 skeletal standard-bearer;
    - scenario: 67 sewer ghoul;
    - world: 58 waterfall ruins and 55 siege wall-climb;
    - chapter: 65 ship and dead tree and 59 harbour wharf.
  - **Banked:** 54 dwarf, 57 swordswoman (signed), 61 herbalist, 63 wizard, 56 weapons sheet and 64 armour sheet. Their sets (person, tradition, item) are full.
  - **Caveats:** grey tone in 55, 58, 59 and 62; a dark backdrop on 62; a monogram on 65.
  - **Result:** 57 distinct images in use. Still shared: cover (29, 11, 43), chapter (43), world (44), beast (38, 16), vermin (16, 18), magical (28, 18). Eleven more images give every set four unique images.
  - Scenic references were added to the figure test. The queue was republished, with prompts unchanged.
- **Reference review** (owner, 2026-10-12: "Review every reference art piece and every reference category to ensure optimal and best assignments"). All 66 references were viewed on labelled contact sheets and checked against each set's subjects.
  - **Changes:**
    - classes and ancestries: 54 dwarf and 57 swordswoman replace 08 fencers and 42 Callot crutches;
    - spell tiers: 63 wizard casting replaces 28, which stays in magical;
    - cover: 46 tower and 65 coast replace 29 and 43;
    - climates: 47 barrow replaces 07.
  - **Kept on purpose:** vermin and magical keep 18 bear and 16 dragon-man as their weakest members, because the only alternatives (05 cave, 26 study) are scenes and must not reach isolated figures. The owner's item set (15, 40, 27, 33) is unchanged; 56 weapons sheet and 64 armour sheet are recommended alternatives.
  - **Result:** 57 distinct images in use. The queue was republished, with prompts unchanged.
- **Equipment extras** (owner, 2026-10-12: "Attach weapon and armour sheet. They can be extra"). 56 weapons sheet and 64 armour sheet join the item set as a fifth and sixth reference. The new `max_refs_by_set` setting (`item: 6`) lets that set exceed the general limit of 4, honoured by `tools/art_gpt_pack.py` and the pipeline test. Both item illustrations now carry six references, and every other set is unchanged. The queue was republished, with prompts unchanged.
- **Creature references** (owner, 2026-10-12: eleven images, no text; four repeated STYLE-REF-54, 55, 65 and 66 pixel for pixel and were skipped).
  - Seven new creature samples were stored unchanged as STYLE-REF-68 to 74 and placed by monster kind:
    - beast: 70 chimera and 74 winged reptile;
    - vermin: 72 mantis insectoid and 71 tree creature;
    - magical: 68 coiled dragon and 73 manticore.
  - **On file:** 69 hydra (no free slot) and 50 flame-sword elf.
  - **Result:** every figure set (all monster kinds, classes and ancestries, backgrounds, items) now holds images used nowhere else, 64 distinct in use. The only images still shared sit among scene sets: cover with chapter, climate and bastion; 43 between chapter and campaign; 44 between world and climate.
  - **Caveats:** 71 has grey-looking dense hatching; the composite chimera and the human-faced manticore must not be copied onto other creatures.
  - The queue was republished, with prompts unchanged.
- **Second reference review** (owner, 2026-10-12, same request again after the creature samples).
  - **Changes:**
    - humanoid: 50 flame-sword elf replaces 62 ratman, whose dark crowd backdrop sat in an isolated-figure set;
    - magical: 69 hydra replaces 28 wizard vs fiend, so no human figure is in a creature set;
    - spell tiers: 28 replaces 12 wizard storm, which had grey screen tone.
  - **Kept, with reasons recorded in `docs/ART_DIRECTION.md`:** undead 04 and 03 (bleed-list subjects, but used only for undead, and the approved Skeleton Warrior came from them); the owner's 22 wolf pack and item set.
  - **Result:** 64 distinct images in use. Every figure set is unique, and sharing remains only among scene sets.
  - **Unattached:** 07, 08, 12, 14, 24, 42, 48, 61, 62.
  - The queue was republished, with prompts unchanged.
- **Six references per set** (owner, 2026-10-12: "Are there any unused references that should be promoted? If they are high quality and match a category well we could accommodate up to 6 reference images per category").
  - `max_refs` is now 6, and the per-set override added for items is removed as redundant.
  - **Promoted:**
    - 61 herbalist to classes and ancestries (bold blacks, a quiet non-combat pose);
    - 07 dry-brush duel to scenarios (core gritty brushwork; combatants in a landscape suit scenarios, though not terrain sets).
  - **Not promoted, with reasons:** 08 and 42 (period costume bleed), 12 (screen tone), 14 (monogram, fine engraving; items full), 24 (too clean), 48 (black box frame), 62 (dark backdrop).
  - Scenarios and classes and ancestries now carry 5 references, items 6, and all others 4. The queue was republished, with prompts unchanged.
- **Skill v8** (owner, 2026-10-12: "Double check everything from these reference changes are incorporated into the plan and upgrade the gpt skill to v8 ... Then double check everything again").
  - **Reference consistency verified:**
    - all 275 queue items carry exactly their set's references (up to 6) and `ref_set`;
    - every style file is catalogued in `STYLE_REFS.json` with a correct usage field;
    - 66 distinct references are in use; `max_attempts` is 1; `receipts_base` is 19.
  - **Version 8.0.0:** `SKILL.md`, the operator card, the helper docstring, `work_preflight --require-installed` (now requires v8), `validate_skill.py`, `tools/art_skill_build.py` (`Heraldry_Classic_Ink_Art_Skill_v8_0.zip`, 43.6 MB, built on request), `tools/art_work_package.py`, INSTRUCTIONS, WORK_PROMPT, AGENTS, README, RELEASE_STATUS and ART_AUTOMATION.
  - **Records:** the skill README has a "Changes since v7" table, and `VERIFICATION_REPORT.md` is rewritten for v8.
- **Full-list run** (owner, 2026-10-12: "Codex will accept 6 reference images. I'm on chat gpt plus so the usage limit resets every 5 hours. I want the skill to run through the entire list, not just the first 17 images").
  - `CODEX_PROMPT.md` now authorizes the entire queue in one prompt; Codex stops only at NOTHING LEFT, a usage limit, a reference-attachment refusal or ship BLOCKED.
  - Drift reviews (every 10 images) are reported and the run continues; Claude Code reviews and sends redos. The "whole batch has drifted" stop is removed from `SKILL.md`, the helper message, BATCH_CARD, OPERATOR_CARD, VISUAL_ACCEPTANCE and STYLE_CONSISTENCY.
  - Usage limit: every saved image is already delivered, so the owner pastes the same prompt after the 5-hour reset and `next` resumes, redos first.
  - The six-reference limit is now owner-confirmed (`VERIFICATION_REPORT.md`). Skill suite, `make test` and preflight pass; no build was run.
- **First Codex delivery** (2026-10-12): ART-BAS-DEEPWARDEN, commit `8163bc3`; Codex then stopped after one item.
  - **Cause of the stop:** the first `ship` landed but Codex saw no output (tool timeout); the repeat reported `BLOCKED: nothing to deliver`, which the prompt treats as a stop. `ship` now reports `UP-TO-DATE` (exit 0) in that case, prints a progress line before the LFS push and flushes its result; new regression test `test_a_repeated_ship_after_a_landed_delivery_is_not_blocked`.
  - **Colour false alarm:** 14% "saturated pixels" came from near-black ink with a faint warm tint (channel spread about 5 levels). Colour now needs HSV saturation over 60 and a channel spread over 24 levels, in the helper and `tools/art_ink.py`; Deepwarden reads 0%, a red patch still fails.
  - **Double image call:** the first call showed no image but saved one; Codex called again. The card and `SKILL.md` now say to take the saved file instead. The image delivered is the first call's.
  - **Review:** Claude Code approved ART-BAS-DEEPWARDEN (closed gate, black abyss with lantern points, terraces, cranes, ore carts, chimney smoke, lantern-bearers, parapet guard; no lettering; clean vignette). Skill stays v8.0.0 (fixes only). No build was run.
- **First full Codex run reviewed** (2026-10-12): 81 deliveries, ending at ART-MON-GREEN-DRAGON (`450fe7b`); Codex stopped when the image tool refused ART-MON-HARPY (safety category "sexual").
  - **Review:** every image inspected at review size against its brief; zoomed checks on leg counts (Giant Tarantula, Basilisk), the Ranger's belt blade (a knife, not a sword) and the Dryad's torso; ink-prepared versions checked for the tinted or grey-toned images (Blood Ape, Brass Golem, Frost Giant, Green Dragon, Gloomspore Jelly, Forest Troll), all clean pure ink. Many of Codex's own flags were stricter than the briefs (1254 px squares are allowed; scale estimates on Large creatures; Sablekeep does show a terraced chapel-town).
  - **Approved: 77** (78 with Deepwarden). **Redos (3):** ART-MON-THE-LAST-COLOSSUS (about eight times a man's height; must-line says three times), ART-CLI-THE-MIRE (readable skulls and hands; brief says faint and ambiguous), ART-MON-DRYAD-GROVEWARDEN (sculpted bare breasts; brief says no nudity).
  - **Briefs recast for the image tool's safety filter:** Harpy (feather-covered, hag-like, "foul, starved and ravenous", no bare torso), Dryad ("clothed from neck to knee in overlapping leaves and bark plates"), Troglodyte ("rag loincloth" in place of "naked body"). Catalogue and queue regenerated: 197 items, redos first, `receipts_base` 101.
  - **Card:** a refused item is now explicitly not a stop (`refuse`, deliver, continue); larger-than-queue images at the same aspect are not flags. `SKILL.md` and `CODEX_PROMPT.md` match.
  - **Colour tripwire recalibrated:** tinted ink (a pixel darker than paper with channels more than 12 levels apart), warn above 3%, fail above 10%, in the helper and `tools/art_ink.py`. On the 81 deliveries: Deepwarden 1%, Blood Ape 13%, Brass Golem 10%, Green Dragon 7%.
  - **Test:** the must-line test now checks every queued item against its brief, and the catalogue (not the shrinking queue) for its minimum count.
- **Maximum output resolution** (owner, 2026-10-12: "We should be targeting the maximum output resolution for each image").
  - **Finding:** all 81 Codex deliveries already carry the same pixel budget, 1,572,864 px (1536x1024 wide, 1254x1254 square, 1024x1536 tall); the non-standard 1254x1254 shows the tool maximising pixels per aspect. At that budget every family prints at 300 ppi or more except the cover (about 260 ppi at 4.8 in).
  - **Target recorded:** `config/art_style.json` `gpt_target_pixels` 1572864; the queue carries `target_pixels`; `check` warns below 97% of it; `save` records `native_px` in each receipt; regression test `MaximumResolution`.
  - **Worker instructions:** card, `SKILL.md`, operator card, runbook, INSTRUCTIONS, WORK_PROMPT and `CODEX_PROMPT.md` say to choose the largest size and highest quality at the aspect, never the default, and to report the tool's size and quality options once per session; a larger option raises the target. No upscaling.
- **Mid-run review** (2026-10-12, Codex still running; only `SELECTIONS.json` changed, queue untouched): 48 deliveries since the queue republish.
  - **Approved: 45** (123 total), including the three earlier redos' successors The Mire and Dryad Grovewarden. Stirge leg count checked zoomed (six). Codex's flags on margins, scale of Medium or unscaled creatures, the necromancer's "visible face" (the brief asks for a withered face) and the scale figure's spear (the troll, not the figure, has no weapon) do not contradict the briefs.
  - **Redos (3):** ART-MON-THE-LAST-COLOSSUS again (about six times the man's height; reason now gives the geometry: the man's head level with its knee), ART-MON-UNDEAD-CROSSBOWMAN (crossbow on a trestle, not held with a boot in the stirrup), ART-MON-UNDEAD-WARRIOR (bare skeleton, the brief requires a half-rotted corpse). `next` serves them first mid-run.
  - **Pending:** ART-MON-HARPY was refused again by the image tool even with the feather-covered rewrite; it will be reworked when the run ends.
- **Second Codex run ended at ART-MON-VRYMK** (2026-10-12): the image call returned nothing and Codex stopped. 50 delivered in the run; 2 refusals.
  - **Reference limit:** ART-ITE-7-8-MELEE-WEAPONS was refused by the image tool itself: "referenced_image_paths must contain at most 5 paths". `max_refs` is now 5; 64 armour sheet leaves the item set (neither item, Melee Weapons nor Treasure Tables, shows armour) and stays on file. Docs that said six now say five.
  - **Refusals reopen on republish:** a refusal now binds to the queue it was made under as well as its prompt; refusals written before the current `receipts_base` reopen (republishing is Claude Code's decision to retry). Test `test_a_republished_queue_reopens_an_earlier_refusal_with_the_same_prompt`. Melee Weapons and Harpy are pending again.
  - **No-image rule:** the card now says take the saved file; if none, one more call; if that also returns nothing, `refuse` and continue. Never a stop.
  - **Harpy rewritten again** (second safety refusal): a man-sized carrion-bird monster with a vulture's body fully feathered and a withered hag-like head; "human" and "woman" are gone from the brief.
  - **Review:** approved Undead Crossbowman and Undead Warrior (both redos now match their briefs), Vault Ooze and Vaultfang (Codex's flag on its claws is within the brief's "tiny gripping claws"); 127 approved. The Last Colossus missed the three-times scale a third time; its composition is recast from a low angle (which exaggerates size) to side-on at eye level with the man's head at its knee, and it is redone first.
  - Queue republished: 148 items, `receipts_base` 155, `max_references` 5. Codex's correction on the Tomb Necromancer receipt (its face flag was wrong) is noted; the image was already approved.
- **Third run, mid-run review** (2026-10-12, Codex running): the reopened items all generated (Harpy passed the safety filter with the vulture-bodied brief; Melee Weapons with five references; Vrymk). 17 reviewed: **15 approved** (142 total). **Redos:** ART-MON-ZOMBIE (gaunt and skeletal; the brief's bloated waterlogged corpse is what separates it from the Possessed Corpse) and ART-MON-THE-LAST-COLOSSUS (side-on now, but still about five times the man's height; the reason now overshoots deliberately, the man's head at its hip, since the image model enlarges it every time).
- **Book design plan, design system v2 "Ink and Iron"** (owner, 2026-10-12: design a professional layout template for each page type from the reference books; no PDF).
  - **Reference study:** two workers mapped every page of all ten reference books on contact sheets and inspected about 90 pages closely (`docs/design/REFERENCE_STUDY.md`). The RC492 build in `dist/` was reviewed on contact sheets as the baseline: clean but monotone, half-empty bestiary pages, plain stat blocks, scenarios run on.
  - **Plan:** `docs/BOOK_DESIGN_PLAN.md` covers grid, type, ink and ornament, navigation (thumb tabs, contents, index), a catalogue of 20 page types with components, pagination, art and reference lessons, art integration, print notes and adoption steps. It supersedes DESIGN_SPEC's visual identity; the pagination policy is unchanged.
  - **Templates:** `typst/templates/system.typ` (components) and `typst/templates/specimens.typ` (14 specimen pages with real RC492 text, approved art and real figures). They render to PNG only through `tools/render_template_specimens.py` (output `build/specimens/`, not committed). The book build is unchanged until a build is requested.
  - **Fonts:** IM FELL English (roman, italic, SC) added with its OFL licence and replaces Cinzel as the display face in v2; Source Serif 4 and Source Sans 3 stay.
- **Design v2.1, heraldic graphic design** (owner, 2026-10-12: "1. Yes. Or something more artful that serves the same purpose. 2. Yes. 3. Yes. ... add some more flavour than the plain layout ... better graphic design to the tables and elsewhere").
  - **New marks:** shields (roll numbers, folios, running-head chapter mark, contents, Appendix C codes, table titles), pennant plates (section numbers, EXAMPLE tag, thumb tabs as swallowtail pennants), clipped-corner straps (table headers, stat bars, caption bars, reference heads), a fleuron terminal rule closing tables and stat bars, engraved corner brackets (rules notes, scenario dossiers) and a reversed drop capital after chapter openers. The drop capital uses droplet 0.3.1, MIT, vendored in `typst/vendor/`.
  - **Owner decisions** recorded in `docs/BOOK_DESIGN_PLAN.md` sections 11 and 12: keep the tabs, made more artful; typographic openers where chapter art is not yet approved; C.13 also as a separate one-page play aid at build time.
  - Specimens re-rendered (PNG only); no build.
- **Design system v3 "Grim Heraldry"** (owner, 2026-10-12: chapter-keyword tabs running along the edge; "add much more character and rebuild the whole graphic design moving in a more ornate grim dark direction while focusing on clarity and ease of uses. Ensure the tables are not only beautiful but also very easy to read").
  - **Tabs:** 15 pennants with a rotated keyword (World, Mechanics, Round, Actions, Combat, Party, Equipment, Powers, Monsters, Scenarios, Campaign, Learn, Basic, Reference, Index). All 15 were checked at 110 ppi to fit on one line.
  - **Type:** Grenze Gotisch (OFL, `fonts/static/`, licence added) for titles and names, never all caps, never for text or cells. IM FELL is kept for flavour italic; Source Serif 4 and Source Sans 3 are unchanged.
  - **Armoury:** briar rules, rivets, iron rules, iron bands, shields, banner tags, corner irons, skull, ornate opener frame, blackletter drop capital.
  - **Ledger tables:** black header band with rivets, bold key column, 6% banding, faint column guides, side frame, shield roll numbers, iron close.
  - **Docs:** `docs/BOOK_DESIGN_PLAN.md` sections 3, 4, 5, 6.10, 11 and 12 rewritten; specimens re-rendered (PNG only, cream and white). No build.
- **Design system v4** (owner, 2026-10-12: take it further with tasteful decoration; bolder centred tab font; tables look amateur, so centre values and use a coin for "(c)"; skulls cheesy; rules crowded; narrower margins; typesetting policy against bloat and split paragraphs; easier flavour font; polish to award-winning standard).
  - **Marks:** chapter arms (15 heraldic ordinaries), a broken crown as the signature, a brush rule, engraved shields, corner flourishes, banner tags and the coin. Skulls and thorn rules are retired.
  - **Tabs:** bold Grenze Gotisch keywords, auto-fitted, reversed and centred.
  - **Ledger tables:** values centred under centred headers, bold left key column, header band, 5% banding, hairlines, brush strokes top and bottom, no vertical rules; the coin replaces "c" (typographic mapping recorded for reconciliation).
  - **Layout:** margins 0.75 / 0.55 / 0.68 / 0.7 in (about 6% more text per page). Flavour in IM FELL roman at 84% black. Widow, orphan and runt costs set in `base`.
  - **Docs:** `docs/BOOK_DESIGN_PLAN.md` v4 rewrites sections 2 to 5, 6.10, 11 and 12, and adds section 13 (typesetting and layout policy).
  - **Specimens:** 15 pages including "The Armoury" design sheet; PNG only, no build.
- **Design v4.1** (owner, 2026-10-12: themed, more ornate arms; at least five signature options; a clearer medieval coin raised onto the baseline; keep a fresh page per section; reflow awkward typesetting such as the Deepwarden introduction).
  - **Arms:** themed chapter arms drawn as SVG by `tools/make_heraldry_marks.py` (cream and white variants in `typst/templates/marks/`). Each has hatched heraldic tinctures, an engraved double-bordered shield and a fimbriated charge.
  - **Signature:** six candidate marks (crown, pierced crown, rotting banner, broken sword, black rose, raven), shown on specimen 15; the choice is pending.
  - **Coin:** a long-cross penny sitting on the baseline.
  - **Typesetting:** balanced two-column runs at run ends; gazetteer lore in balanced full-width columns; examples unbreakable. Policy updated in BOOK_DESIGN_PLAN section 13: fresh page per numbered section kept, and balanced columns added.
- **Heraldic marks via Gemini (Nano Banana)** (owner, 2026-10-12: "Should we outsource it to nano banana with the api key we set up earlier? Please create prompts to generate these much better. I think maybe a broken shield with a castle as the heraldry on it would be most fitting overall heraldry logo. Let's draft a prompt for this and generate it in nano banana as well"). This is an explicit owner instruction to use the retired Gemini route, for these marks only.
  - **Prompts:** `production/art/marks/PROMPTS.json` covers the logo (a broken heater shield bearing a castle) and the fifteen themed chapter arms, with a shared engraving style block and a matched-series block. Campaign's charge became a war pavilion so the logo keeps the castle.
  - **Route:** `tools/mark_generate.py` reuses `art_generate.py`'s key handling, model resolution, budget cap ($150; $3.04 spent before this run) and ledger. The manual workflow `.github/workflows/generate-marks.yml` commits candidates to `assets/art/marks/candidates/` (LFS); nothing is placed until approved.
- **One flavour treatment** (owner, 2026-10-12: put the Deepwarden flavour in the same centred single column as the chapter lead, and make all section flavour the same). New `lead-block` component: centred IM FELL roman at 80% measure, used for chapter leads, section flavour, gazetteer lore and scenario flavour. Gazetteer and scenario heads are centred to match; entry flavour in columns stays left-aligned in the same face. Plan section 3 updated; specimens re-rendered.
- **Flavour and title-tag refinement** (owner, 2026-10-12: "The black flags like bastion are awkwardly positioned and should be perfectly alighted and consistently positioned relative to the subtitle or header text they are relating to. If flavour text has multiple paragraphs in a section I think it would look better to have some space between paragraphs. I wonder if justified would look better than centrered for flavour text. why not just make all falvour text 12pt for consistentcy?").
  - **Tags:** new `entry-title` component sets every title tag (monster role, BASTION, HERO CLASS, scenario number) on its own line 5 pt above the title's cap height, on the title's alignment edge. Used by monsters, classes, scenarios and gazetteer heads.
  - **Flavour:** all flavour is IM FELL roman at 12 pt, justified and hyphenated, 9 pt between paragraphs, with Typst justification limits so narrow columns set evenly. Justified was chosen over centred after a side-by-side on the Deepwarden page. `lead-block` keeps the centred 80% measure; `flavour` is full column width. `render_template_specimens.py --lead center` shows the alternative.
  - Plan section 3 updated; specimens re-rendered (cream and white, PNG only, no build). The bestiary still holds two complete monsters per page.
- **Tags top-left; justified body** (owner, 2026-10-12: "The black tags should consistently be aligned to the top left of the text they reference; not centred above it like in your example. All flavour text should be justified, it looks much better now. This begs the question should all body text everywhere be 12pt and justified for consistency?").
  - `entry-title` now pins the tag to the title's top-left corner, including over centred titles (gazetteer, scenario).
  - Rules text is now justified at 10.25 pt with the same justification limits as flavour. A side-by-side on the 2.6 and Fighter pages showed it sets evenly and saves lines. Tables, captions, stat blocks and headings stay unjustified.
  - Rules text stays 10.25 pt, not 12 pt: 12 pt would add about a third to the text pages, and the size step separates rules from flavour (plan section 3). `render_template_specimens.py --body rag` shows the ragged alternative.
- **Rules text locked at 11 pt** (owner, 2026-10-12: "Let's lock rules at 11pt"). Body 11 pt with proportional leading; examples, notes, entry anatomy and power effects 10.5 pt; dossiers 9.9 pt; flavour stays 12 pt. Hyphenation cost lowered to 100% so justified list items set evenly. `balanced` now takes exactly the room left on a near-full page instead of pushing an empty frame onto the next page (found on the chapter-opener specimen). All 15 specimens re-rendered (PNG only, no build): the opener, 2.6, the Fighter and two monsters per page still fit. Text pages are expected to grow about 15% over 10.25 pt when the book is next built.
- **One body size; rules note as a panel** (owner, 2026-10-12: "I actually think it makes more sense to set all body text (flavour and rules) to the same font size ... maybe 11pt? Also please change the ugly in line "rules note" format to be the same as example format but with a different tag. Also the tags on these should also be aligned to top left just like the rest of the tags").
  - All running text is 11 pt: rules, flavour, examples, notes, dossiers, entry text and power effects. Data text (tables, captions, stat strips, tags) keeps its own sizes.
  - Rules notes now use the example panel (`panel` component) with their own tag, set at the top left; the corner-iron note is retired.
  - Justification limits tightened (word space 90–140%, letter spacing −0.5% to +2%) after squeezed flavour lines at 11 pt.
  - List items (talents, packages, steps) are now unbreakable, after a Fighter talent split across columns.
  - Specimens re-rendered (PNG only, no build); all 15 pages fit.
- **Heraldic marks, round 2** (owner, 2026-10-12: "Rerun the chapter arms and logo through nano banana 2.1 with more clear prompting that they are heraldry inspired logos to be in the grim dark fantasy medieval style black and white ink pen only. No grey, shading, or dense lining. They will serve as icons of a sort so they symbology in the chapter arms should be simplistic iconography."). Round 1 cost $3.39 (34 images, gemini-nano-banana-2.1). PROMPTS.json was rewritten as flat icon prompts: solid black or white only, plain white field, one simple silhouette charge, the same bold double-rimmed heater shield. `mark_generate.py` saves round 2 as `<ID>-r2-v<n>.png` beside round 1, and the ledger records the round.
  - Round 2 delivered: 34 of 34 images, $3.42 (marks total $6.81). All are pure black and white: no tint, and only about 1% edge anti-aliasing. All read at icon size (44 px test). Claude Code's picks are logo v3 and arms 01 v1, 02 v1, 03 v1, 04 v1, 05 v1, 06 v2, 07 v1, 08 v2, 09 v1, 10 v1, 11 v1, 12 v2, 13 v2, 14 v1, 15 v2. The shield outlines vary slightly between images; the plan is to trace the chosen charges to SVG and set them on one shared shield so the set matches exactly. Awaiting the owner's choice.
- **Heraldic marks, round 3** (owner, 2026-10-12: "I feel like these icons could be more detailed exactly half way between the first run and second run. Run it again in nb 2.1"). The prompts keep round 2's pure black and white and plain field, and restore round 1's interior detail with bold, sparse ink lines (a solid silhouette plus interior lines, at most a few widely spaced strokes). Saved as `<ID>-r3-v<n>.png`.
  - Round 3 delivered: 34 of 34 images, $3.38 (marks total $10.19). All are black and white, with edge anti-aliasing of at most 2.5%. Claude Code's picks are logo v3 and arms 01 v2, 02 v1, 03 v2, 04 v1, 05 v2, 06 v2, 07 v1, 08 v1, 09 v2, 10 v1, 11 v1, 12 v1, 13 v2, 14 v1, 15 v1. Awaiting the owner's choice of round and picks.
- **Heraldic marks, round 4** (owner, 2026-10-12, round 3 sheet marked up: "Headed the right direction but not quite there. The world should be an abstract map. Actions should be something related to actions such three arrows pointing downwards. Equipment should be a piece of chest armour. Combat should have two different weapons crossing and a more grim dark aesthetic."). Selections are recorded in `PROMPTS.json` `selected`: 02 v1, 03 v2, 06 v2, 09 v2, 10 v1, 11 v1, 12 v1, 13 v2, 14 v1 and 15 v1, all round 3. Round 4 reruns 01 (abstract map), 04 (three arrows points down), 05 (axe and notched sword, grimmer) and 07 (breastplate), 3 variants each. Powers was rejected without a replacement, so it gets three alternative concepts with 2 variants each: 08A open hand with an eye, 08B crystal staff, 08C sigil.
  - Round 4 delivered: 18 of 18 images, $1.73 (marks total $11.91), all black and white. Claude Code's picks are 01 v2, 04 v1, 05 v2, 07 v1 and Powers 08A v1. 08B's staff thins out at icon size, and 08C's ring reads as real runic letters. Awaiting the owner.
- **Marks, round 5** (owner, 2026-10-13: "I changed my mind about world -> the map is not a good look ... alternative icon for "World" which also doubles as the "Lore" chapter ... Actions v2 is better but make the heads solid black. Combat v2 is great. Equiment i changed my mind the helmet was a better symbol. Powers v1 is very coool."). Selected: Actions r4 v2 (arrowhead facets filled solid black by a deterministic flood fill into `MARK-ARMS-04-r4-v2-solid.png`), Combat r4 v2, Equipment r3 v1 (helmet) and Powers 08A r4 v1. Fourteen of fifteen arms are now chosen. Round 5 offers World/Lore concepts, 2 variants each: 01A withered oak torn up by the roots, 01B raven on a broken crown, 01C chained tome, 01D scroll with a broken seal.
  - Round 5 delivered: 8 of 8 images, $0.73 (marks total $12.64). In review, the raven 01B v1 reads best at icon size; the oak 01A v1 is the strongest concept, though its fine branches thin out when small; the tome 01C is busy; the scroll 01D shows letter-like scribbles. Awaiting the owner.
- **Marks, round 6** (owner, 2026-10-13: "Rerun better versions of A and B to help me decide"). The oak 01A is made bold for icon size (thick trunk, few heavy branches, no twigs); the raven 01B gets a crown clearly cracked and missing a point. 3 variants each.
  - Round 6 delivered: 6 of 6 images, $0.59 (marks total $13.24). Best of each: oak 01A v3, the boldest and still readable at icon size; raven 01B v1, whose crown is cracked open with a snapped point lying beside it. Awaiting the owner's choice between them.
- **Marks, round 7** (owner, 2026-10-13: "the raven v1 is good but the crown has an extra piece and should more clearly be a crown boken into two seperate pieces"). `mark_generate.py` gained `edit_from`: the base candidate image is sent with the instruction, so Nano Banana edits it instead of redrawing it. `MARK-ARMS-01B-EDIT` keeps raven r6 v1 and its shield, and redraws only the crown as exactly two separate halves with no other fragments. 3 variants.
  - Round 7 delivered: 3 of 3 edits, $0.29 (marks total $13.52). The raven and the shield came through unchanged. v2 and v3 show exactly two crown halves with a clear gap; v1 still has a middle shard. Claude Code's pick is v2. Awaiting the owner.
- **Heraldic marks approved and placed** (owner, 2026-10-13: "Approved. Make sure they are big enough to see."). `production/art/marks/APPROVED.json` records the 15 arms and the logo (round 3 v3). The new `tools/prepare_marks.py` lifts each charge, drops fragments of its source rim, fits it into one shared shield (the Mechanics candidate's rim) and traces it to vector SVG with potrace (pure-Python `potracer`, a local tool dependency). It writes cream and white `arms-NN.svg` and `logo.svg` to `typst/templates/marks/`, 512 KB in total. The hand-drawn arms and the six signature candidates are retired; `make_heraldry_marks.py` now draws only the coin. Sizes were raised: opener arms 26 to 52 pt, contents 15 to 22 pt, running head 8.5 to 15 pt, opener-frame logo 18 to 30 pt, flourish logo 14 to 22 pt, armoury sheet 40 to 52 pt (logo 92 pt). Opener art was narrowed from 94% to 86% so the opener specimen still fits one page. All 15 specimens re-rendered (PNG only, no build); plan section 12 updated.
- **Tab arms and a new coin** (owner, 2026-10-13: "Maybe beside the keyword on the tab. Also please remake the coin to be better"). Arms can't go inside the tab: each slot is 49 pt, and the longest keywords (Equipment 50 pt, Mechanics 49.5 pt at 12 pt) already shrink to about 9 pt, so a 13 pt arm would force them to about 5.5 pt. Each thumb tab instead carries its chapter's arms as a 15 pt medallion beside the keyword, straddling the tab's inner edge, with the keyword at full length. The coin is regenerated in the arms' ink style (round 8, `MARK-COIN`, 4 variants): a hammered long-cross penny with a beaded border and pellets.
  - Coin round 8 delivered: 4 of 4 images, $0.48 (marks total $14.00). Rendered inline at 11 pt and 9.3 pt: v2 (heavy beaded border, solid cross, four pellets per quarter) is the only one dark enough to match bold figures; v1, v3 and v4 read as pale grey dots at text size. Claude Code's pick is v2. Awaiting the owner.
- **Coin v2 approved without the notch** (owner, 2026-10-13: "Yes to v2 but take the notch out of the border"). Round 9 `MARK-COIN-EDIT` edits r8 v2 in place to close the rim and the beaded border. 3 variants.
  - Coin round 9 delivered: 3 of 3 edits, $0.26 (marks total $14.26); all three closed the notch. Edit v1, the closest to r8 v2, was traced by `prepare_marks.py` into `coin.svg` and `coin-reversed.svg` (APPROVED.json `coin`). `make_heraldry_marks.py` now draws nothing. Checked inline in the bestiary CV strip and reversed in the melee-table COST header; specimens re-rendered (PNG only, no build).
- **Art review, 2026-10-13** (owner: "1", i.e. review the delivered art first). Claude Code reviewed the 42 received ChatGPT/Codex images: contact sheets, close-ups of the flagged items and ink coverage. The highest new coverage is 0.59, against 0.47 to 0.65 for approved scenes. The 36 flags are worker notes (prompt-wording conflicts such as the Trickster's rapier; missing raw vignette margins, which ink prep supplies; the Zombie's face reading skull-like) and grey-tone tripwires on the raw images; none is a visible defect. All 42 were approved, making 184 of 275. The queue was republished: 91 items, `receipts_base` 215, and 15 stale entries approved earlier were dropped.
- **Design v4 adopted into the book; build** (owner, 2026-10-13: "Sure", to step 2: bring the design into the book layout, including the build). `typst/heraldry.typ` now imports the approved specimen system (`typst/templates/system.typ`) and keeps the generator's component signatures and the pagination machinery unchanged.
  - **Furniture:** running heads with chapter arms, folio shields, thumb tabs with arms, and the opener frame with the logo, all derived from the document.
  - **Components:** section shields, ledger tables with the coin, stat strips and cards, the example/note panel, figure caption bars, IM FELL flavour, and 11 pt justified text.
  - **Front matter, covers and calibration** restyled with the logo.
  - **Geometry:** `tables.py` and the QA tools use the v4 frame (518.4 pt; column 250.5 pt; top margin 0.68 in).
  - **QA mappings** (documented in the tools): IM FELL counts as emphasis; source labels use small caps, never upper case; tracked letter-spacing is not used on source text; the coin overlays the source "c"; the thumb-tab strip is navigation furniture.
  - **Fixes from page review:** empty flow runs, the B.6 page spill (FIG-19 anchor moved after "Winning:" in `config/content_anchors.json`; placement only), table openings kept with their headings, opener art capped at native size, tab overscan.
  - **Result:** 656 interior pages (598 before), every gate PASS including the hash-bound all-page visual ledger; package PASS; `make test` PASS. Physical print NOT TESTED.
  - **Reproducibility fix:** the first release run failed only `visual_review_currency`: CI's clean build (e5dfc3c6) differs from the local incremental build (5858350d) by one balancing choice from the cached `build/balance.json`. Rebuilt with `make clean all`, reproduced twice, reviewed all 656 pages of that exact PDF again, and rebound the ledger to it. Release gate PASS; package PASS.
- **Art review, 2026-10-13 (second batch)** (owner: "Continue checking images from gpt"). Claude Code reviewed the 54 newly received Codex images: three contact sheets, close-ups of the flagged items and a colour-tint check (at most 1% of pixels, which is anti-aliasing). Of the 36 flags, none is a visible defect. The Serpent's Sunken Hoard shows a diver in a whirlpool, not a serpent. Three judgement calls are approved but noted: the Ice Wyrm's Hoard and the Cinder Lord's Obsidian Pyre show their monster more fully than the card's "partial glimpse", and the Reliquary of Broken Saints resembles a chapel interior. All 54 were approved: 238 of 275 approved. The queue was republished: 37 items, `receipts_base` 270.
- **Build timing** (owner, 2026-10-13: "[Don't] rebuild the book until all the illustrations are done"). No PDF build or `Rebuild verified delivery` run until all 275 illustrations are approved. Until then, art intake, review and approval continue; `dist/` and the RC492-build-24 release stay the last build (184 of 275 illustrations placed; 238 approved by now).
- **Tab arms removed** (owner, 2026-10-13: "Please remove the awkwardly place chapter arms icon that sits on top of the right page border chapter tab"). The arms medallion beside the thumb-tab keyword is gone; tabs carry only the bold chapter keyword again. The arms stay on the running heads, contents rows and chapter openers. Specimens re-rendered (PNG only). The change is in `typst/templates/system.typ`, which the book imports, so the published release (RC492-build-24) still shows the medallion until the next build, held until all illustrations are approved.
- **Tier 3 Druidic art rejected and redone** (owner, 2026-10-13: "The Tier 3 Druidic art is dumb with a big hole in a tree. Reject, Redo the prompt, and que our image creation pipeline in codex to retry a new better image. I'd suggest a massive epic storm pushing over a mountain as much of the tier 3 Druidic powers focus on manipulating the weather."). `ART-TRA-TIER-3-DRUIDIC-RITUALS-D20` is rejected with that reason. The brief (`production/art/briefs/figures.json`, subject plan, regenerated catalog) now shows a small druid on a ridge under a colossal storm front driving against a mountain whose flank is sliding away (Maelstrom, weather control), with an explicit "no hollow or hole in any tree or mountain" clause. The queue was republished (31 items) with the redo first; Codex picks it up on its next pull with a fresh attempt budget. Approved: 237 of 275.
- **All 275 illustrations approved** (2026-10-13; owner: "Continue" after Codex reported NOTHING LEFT). Claude Code reviewed the last 37 (contact sheets, ink and tint measurements, close-ups of CH04, CH10 and the Druidic redo) and approved them: the 20 Backgrounds (the checker's mid-tone and edge warnings are line-weight anti-aliasing on fine hatching; none is a visible defect), the Treasure Tables item, the remaining chapter second images (CH02 to CH11), and the Tier 2 and 3 tradition images. The redone Tier 3 Druidic image shows a small druid on a cliff, a tornado funnel and lightning tearing the flank off a pine-covered mountain, as the owner suggested. CH04-002 has a small distant sentinel beside the four Heroes, accepted. The queue is empty, so the owner's hold ("no rebuild until all the illustrations are done") is cleared; a build still waits for the owner's go-ahead.
  - **Tests with an empty queue:** the pipeline test now builds the full pre-approval queue (anchors only) instead of reading the live selections, which are all approved; three work-package tests that need queued items skip with a stated reason while the live queue is empty. 50 tests pass (3 skipped); they run again when a new queue exists.
- **All 20 Background illustrations rejected and redone** (owner, 2026-10-13: "Redo all background images", after Claude Code's second review found inaccurate objects and positions that defy gravity). Findings: Merchant's scale beam tilted toward the empty pan; Noble's rapier overhanging the table and star-shaped moth holes; Apprentice's coat sleeve jutting out sideways; Performer's throwing knives were kunai and the mask full-face; doubtful: the Soldier's helmet, the Artisan's hammer, the Scout's spyglass and hood, the Cultist's pentagram, and a modern-looking pen. Fixes: a shared PHYSICAL PLAUSIBILITY clause in the background framing (`config/art_style.json`: everything rests, leans or hangs from a visible support; cloth and rope hang; a scale tips toward its heavier pan; true medieval forms; no modern items or East Asian weapons), per-item corrections and extra avoid lines in `production/art/briefs/figures.json`, and a general no-floating avoid line on all 20. All 20 rejected with that reason, the catalog regenerated, and the queue republished (20 items, backgrounds only) for Codex. Approved: 255 of 275. The build hold continues until all 275 are approved again.
- **Backgrounds redone: reviewed** (owner: "Looks like it's done"). Claude Code viewed all 20 new images at about 900 px (four to a sheet) with close-ups of the scale, purse, banner and scroll. The earlier problems are fixed: the Merchant's and Alchemist's scale beams tip toward the loaded pan, the Noble's rapier lies fully on the table, the Apprentice's coat hangs down, the Performer's knives are plain and the mask half-face, the Soldier's cap sits on the chest, the Artisan's hammer lies on the anvil (now on a block), the Cultist's sigil is a ring and spiral. 18 approved. Two rejected again, both also noted by Codex's own QA: the Smuggler's purse hung from a cord attached to nothing (and the chalk route mark was missing), and the Vagabond's milestone was still a tall rounded slab like a gravestone. Their briefs were tightened (purse lying on the crate; chalk arrow and tally strokes; squat knee-high flat-topped marker, explicitly not a gravestone) and the queue republished with those two. Minor, accepted: the Apprentice's scroll scribbles read as pseudo-handwriting and its chalk circle has a star; the Scout's hood stands open on the cloak pile. Approved: 273 of 275.
- **All 275 illustrations approved again** (2026-10-13). The Smuggler and Vagabond redos were reviewed at full size and approved: the Smuggler's purse lies on the rope-bound crate and a chalk arrow with tally strokes marks the barrel; the Vagabond's milestone is a squat, flat-topped block, not a gravestone. Codex reported NOTHING LEFT (both images 1254x1254; its image tool exposes no size or quality options). The queue is empty. The owner's build hold ("no rebuild until all the illustrations are done") is cleared; the full build waits for the owner's go-ahead.
- **Backgrounds through Nano Banana 2.1 for comparison** (owner, 2026-10-13: "Let's first rebuild all 20 background art pieces through nano banana 2.1 then we will compare all versions made of each background illustration side by side and select the best"). This is an explicit owner instruction to use the Gemini route for the Backgrounds. New `tools/art_variants.py` and the manual `Generate art variants` workflow write raw 2K candidates (3 per background, the same current prompt and reference set the Codex queue uses) to `assets/art/variants/<ID>/nb-<n>.png` (Git LFS), and never touch `SELECTIONS.json`, `assets/art/incoming` or any approval. Spend shares the $150 cap and the ledger (kind "variant"). Comparison sheets will put every version of each background side by side: Codex pass 1, Codex pass 2 (currently approved) and the Nano Banana versions. A chosen Nano Banana version will be placed through a separate reviewed step. The build stays on hold until the selection is made.

## 2026-10-13: backgrounds redo with composition guides (owner decision)

Owner: keep the Codex ink style for visual cohesion, but try the Nano Banana 2.1 composition and layout. Nineteen backgrounds (all but Nomad, whose Codex image stays) are rejected back to the queue with a composition guide each (`production/art/composition/GUIDES.json`; `tools/art_composition.py build` writes `<ID>.jpg`, greyscale with the paper tone removed, from the chosen `assets/art/variants/<ID>/nb-<n>.png`). The guide is the last of the item's five references (four style references plus the guide); the prompt says to copy layout and gravity but render in the style references' ink. The previous approved Codex images stay in git history and `assets/art/incoming`/`ink` until replaced; if a guided image is not better, restore the earlier approval. One guided image per background so far. Build still on hold.

## 2026-10-14: guided backgrounds reviewed

Codex delivered 19 guided backgrounds. Full-size review: 17 approved (Alchemist, Apprentice, Artisan, Believer, Courier, Cultist, Farmer, Hermit, Merchant, Pauper, Performer, Sailor, Scholar, Shepherd, Smuggler, Soldier, Vagabond): grounded layouts, Codex ink style kept. Rejected back to the queue: Noble (rapier hilt and point overhang the table; brief now says the whole sword lies on the tabletop) and Scout (cloak read as modern camouflage; brief now says plain wool). Nomad (guide nb-2) was added after the owner noted all 20 should be redone; it is queued too. Queue: Nomad, Noble, Scout. Build still on hold.

Review 2026-10-14 (later): Nomad (felt bedroll, curved sheathed scimitar) and Scout (plain wool cloth) approved. Noble rejected a second time: the guard still overhangs the tabletop's far edge; the brief now asks for a wider table and a sword well inside it. Queue: Noble only. 19 of 20 guided backgrounds approved (Nomad, Scout included).

Review 2026-10-14 (final): Noble approved on the third try (whole table visible, rapier along the tabletop with its balance point and guard on wood; only the pommel end reaches the back edge). All 20 backgrounds are now Codex images guided by the Nano Banana compositions. All 275 illustrations are approved; the queue is empty. The build is still on hold awaiting the owner's go-ahead.

Owner decision 2026-10-14 (after the side-by-side): Believer, Merchant, Noble, Scholar, Soldier and Scout go back to their earlier Codex images (denser, richer, fuller frames than the guided versions). Their previous approvals, incoming and ink files were restored from commit 413e958; the guided images are kept as assets/art/variants/<ID>/guided-codex.png and the six guides are retired. The other 14 backgrounds use the guided Codex images. All 275 remain approved; queue empty; build still on hold.

## 2026-10-14: owner-supplied front cover

Owner supplied a finished cover picture (HERALDRY title ornament, "The PvPvE Fantasy Tabletop Skirmish Game", dragon-skeleton battle in a thorn-and-skull frame) as the book's front cover. Source: assets/art/cover/front-owner.jpg (912x1168 px). tools/prepare_cover.py converts it deterministically (3x Lanczos, paper white cut to transparent, ink pure black) to assets/art/cover/front.png; tools/build_extras.cover_art() fits it inside the 0.375 in safe edge (7.75 x 9.925 in, so native resolution is about 118 ppi) and typst/cover.typ shows it as the whole front cover (lettering is in the picture; no live type). The classic cover (castle logo, live title, ART-COVER-002 vignette) remains in cover.typ as front-cover-classic, used when front.png is absent. Back cover unchanged. Open points for the owner: the picture's title and subtitle differ from the manuscript's ("Heraldry Skirmish: The Dying Lands"), still used on the title page and back cover; and a higher-resolution original would be needed for a crisp print. Covers-only build checked (build/covers-*.pdf, not committed); no full book build.

## 2026-10-14: unattended build chain prepared (not run)

Owner asked to prepare the repo so Codex can orchestrate a full build and release overnight through GitHub. Built: `tools/build_request.py` (stdlib; check / request / wait), `.github/workflows/build-candidate.yml` (starts when `production/build-request.json` is pushed; make test clean all, verify, GitHub pre-release `<RC>-candidate-<n>`, commits `production/BUILD_STATUS.json`, also on failure), `tools/build_status.py`, `production/build/CODEX_BUILD_CARD.md` and `CODEX_BUILD_PROMPT.md`, `docs/BUILD_AUTOMATION.md`, AGENTS.md carve-out. `rebuild-delivery.yml` now also starts on a push of `production/qa/visual-review.json`, and both workflows fetch `assets/art/cover/front.png` (LFS) which the new cover needs. Limit by design: the mandatory hash-bound all-page visual review cannot be done unattended, so the unattended run ends at a pre-release candidate; Claude Code then reproduces the build, reviews every page, binds the ledger and pushes it, which starts the release. Nothing has been built or released yet; the candidate workflow has not run (YAML and tests checked only).

## 2026-10-15: RC492 release completed; primary-developer handoff

Owner handoff: Codex is now the primary developer, not only the art worker. `CLAUDE.md` governs all work. `AGENTS.md` now records the expanded role and safeguards; `docs/BUILD_AUTOMATION.md` permits repairs and re-dispatch of an already requested failed build. Main only, immutable manuscript snapshots, deterministic text conversion, owner-requested builds, real hash-bound visual review, release-only PDF/ZIP delivery, and credential protections remain in force. RC492 remains the active manuscript; this handoff changes documentation only.

Reconciled the owner's recent-work handoff with main after fast-forward sync:

- Artwork: all 275 illustrations approved; queue empty. Fourteen backgrounds use Codex images guided by Nano Banana compositions (`production/art/composition/GUIDES.json`). Believer, Merchant, Noble, Scholar, Soldier, and Scout retain their earlier Codex images; the guided alternatives remain at `assets/art/variants/<ID>/guided-codex.png`.
- Cover: the owner's entire front-cover picture is prepared by `tools/prepare_cover.py` from `assets/art/cover/`; its native 912x1168 pixels yield about 118 ppi at print size.
- Layout: `config/art_style.json` supports `art_width_overrides` (Haunted Mausoleum: 1.9 in); `typst/heraldry.typ` measures the htable opening reserve; `tools/build_book.py` keeps numbered power/entry titles with their bullet fields using `#keep`.
- Candidate `20261014T211936Z` reached CANDIDATE_READY with 672 interior pages. Commit `0546a39` bound the actual image review: all 28 contact sheets, 29 detail pages, both covers, and calibration. Review PASS at those scales, no major findings, accepted minor whitespace on pages 92, 123, 162, 187, and 249. This is not glyph-level proofreading or an independent second review.
- Run 36 reproduced the reviewed PDF and passed verification; packaging failed. Commit `5eebea0ac89a0d0f10728c8e0c19d78e6db38fe0` excluded LFS working-image directories from packaging and fetched the owner cover source in both workflows.
- Run 37 finished successfully before any handoff push. `production/RELEASE_RESULT.json` on main records RELEASED for that commit, and `dist/RELEASE.json` records [RC492-build-37](https://github.com/xjordont/Heraldry/releases/tag/RC492-build-37): six edition/cover/calibration PDFs, the specimen PDF, release ZIP, SHA256SUMS, and print instructions. All 19 release checks PASS; package audit PASS (705 entries, 704 checksums verified). Cream PDF SHA-256 `10e4f8bea8cff69404a6ee1385077e0533b767ff1815714cd0b2532e245a8e78` matches the reviewed candidate. Release ledgers landed in `16205485`; final result in `576d6214`. No rebuild was needed for this handoff.

Open owner items: decide whether the front-cover title/subtitle should match "Heraldry Skirmish: The Dying Lands" on the title page and back cover; provide a higher-resolution cover original for crisp print; examine actual printed sheets (physical proof remains **NOT TESTED**). Candidate pre-releases 1 through 4 remain optional cleanup, not deleted by this handoff.

Handoff validation: `make test` PASS (55 tests, 3 skipped because the live art queue is empty); `tools/preflight.py --baseline` PASS (8 checks); `tools/check_history.py --base 576d6214` PASS (17 previous snapshots/evidence files unchanged); `git diff --check` PASS. Release/result/source agreement, the 10 asset records, reviewed cream-PDF hash, package-audit ZIP hash, all 19 release checks, 275 approved selections, and empty queue were cross-checked from the committed ledgers. Windows checks use `PYTHONUTF8=1` and `C:/Heraldry/art-venv/Scripts/python.exe`; GNU Make 3.81 was installed under `C:/Heraldry/tools/gnuwin32` through WinGet (installer hash verified) to run the Makefile test target. These local runtime files are outside the repository.

## 2026-10-15: code debugging and regression repairs

Owner request: "Debug the repo's code base." Baseline: 55 tests ran with 3 skipped; contracts PASS. Focused audit of manuscript validation, review gates, packaging, and build/release orchestration found and repaired these defects:

- Windows default-codepage reads misdecoded UTF-8 patch archives and Python sources, falsely reporting manuscript corruption or a syntax-read failure. Manuscript authority, revision configuration, and preflight now specify UTF-8. Subprocess regressions disable UTF-8 mode and turn implicit-encoding warnings into errors; both preflight and a revision in a temporary fixture pass.
- Visual review binding ignored major findings outside contact sheets and silently treated unknown severities as minor. Findings on details, covers, and calibration now block or survive as appropriate; duplicate review entries refuse. The binder validates complete nonoverlapping page coverage and required image inventory before claiming all-page review. Refused records preserve the existing ledger.
- Figure semantic review accepted absent current and recorded manuscript-dependency hashes because both were None. Missing source bindings now fail; reviewer and date are required. Current 57-figure evidence still passes, without updating its review ledger.
- Native Windows ZIP creation failed during archive readback because Windows path separators differed from ZIP member names. Archive members, readback keys, and UTF-8 checksum paths now use forward slashes. A small isolated archive fixture reproduces the old KeyError and verifies the corrected member bytes and checksums.
- Release reporting could record RELEASED after verification-ledger persistence failed. It now requires the preceding job to succeed and reports that step's failure. The result publisher uses a temporary Git index to append only RELEASE_RESULT.json to freshly fetched main, preserving newer input files and the dirty runner checkout. It no longer rebases a pending stale verification-ledger commit during result reporting. Temporary local bare-repository tests exercise advanced-main and rejected-push races, non-race errors, and no-op publication.
- Candidate and delivery workflow reruns reused the first attempt's release tag, so publication collided after an earlier attempt had uploaded assets. Attempts after the first now append `-attempt-<attempt>`; the original tags stay unchanged. A regression executes both workflows' actual tag commands under Bash for 3 attempts and verifies distinct names.

No manuscript snapshot, art approval, PDF, release asset, or hash-bound review ledger was changed. No publication build or workflow was requested or dispatched. `dist/` and production build/QA ledgers still describe RC492-build-37, whose tooling predates these repairs. Physical proof remains **NOT TESTED**.

Validation: `make test` PASS (77 tests, 3 skipped for the empty live art queue; 22 new regressions); `tools/preflight.py --baseline` PASS (8 checks, including with `PYTHONUTF8=0`); current figure review gate PASS (57/57; report written outside the repository); `tools/check_history.py --base 56398186` PASS (17 previous snapshots/evidence files unchanged); `git diff --check` PASS. Tests exercise temporary fixtures and local bare repositories, not live release publication. Full PDF/CI build validation remains for the next owner-requested build.

## 2026-10-15: dependency installation and verification

Owner asked whether all needed dependencies are installed. Audited Python imports and external commands for publishing, Windows orchestration, and cover/mark authoring. The 7 existing locked packages matched the installed versions in `C:/Heraldry/art-venv/Scripts/python.exe` (Python 3.12.10), but cover/mark preparation also imports NumPy and `potracer` (module `potrace`), neither installed nor declared. Added `numpy==2.5.4` and `potracer==0.0.4` to `requirements.lock` and installed them in that environment. All 9 exact versions now match; `pip check` reports no broken requirements.

Runtime smoke checks PASS: Markdown parsing; Pillow/NumPy image conversion; cover-tool imports; actual Potrace tracing; native Typst query on a temporary metadata fixture; PyMuPDF text extraction/rasterisation and pypdf reading in memory; all 19 bundled static fonts readable. Git 2.55.0, Git LFS 3.7.1, GNU Make 3.81, and Git Bash 5.3.15 are installed. `BUILD.md` now gives explicit Windows environment and Make commands; bare `python` and `python3` resolve to other installations/aliases, so use the documented environment.

GitHub workflows install the same lock and use the runner's Git/LFS, Make, Bash/core utilities, and `gh`; this audit did not provision or execute a fresh GitHub runner. The Windows orchestrator does not need `gh`, and the current pipeline uses the Python Typst module rather than the standalone CLI. Pandoc, Poppler, qpdf, and Ghostscript are optional diagnostics. No manuscript, prepared artwork, font, production PDF, release asset, or review ledger was regenerated; current release evidence remains bound to RC492-build-37.

Post-install validation: `make test` PASS (77 tests, 3 skipped for the empty live art queue); baseline contract preflight PASS (8 checks); `pip check` PASS; `git diff --check` PASS. No book build or workflow dispatch.

## 2026-10-15: development and publication workflow refinement

Owner request: improve/refine/optimise the project's workflow. Kept main-only development, immutable manuscript revisioning, owner-requested builds, actual hash-bound review, GitHub-only release assets, and physical print **NOT TESTED**.

- Added the standard-library developer entry point `python tools/dev.py doctor|check|status` and equivalent Make targets. It selects the project's virtual environment, supports an explicit Python override, checks exact locked distributions/imports plus pip consistency and required executables, and runs baseline contracts, snapshot-history protection, whitespace checks, and `make test`. Reports go to ignored `build/checks/`, preserving production release evidence. Status reports local tracking refs and the last requested release without implying a new build or fetching.
- Request and review publication share `tools/git_publish.py`: require clean main equal to fetched origin/main before writing; run mandatory Make tests; recheck remote/main and exact file scope; commit only the allowed file; normally push once. Failed checks preserve files, and rejected pushes preserve the local commit without automatic pull, reset, or rebase. Local bare-repository tests cover unrelated staging, main races, failed tests, changed payloads, and interpreter paths with spaces.
- CI repository checks cover Ubuntu and Windows, cache pinned Python downloads, and cancel superseded check runs. Candidate/delivery workflows share a non-cancelling publication queue. Both check required runtime dependencies and retain allowlisted JSON diagnostics for 14 days, including on failure, without uploading private reference bytes or adding PDFs/ZIPs to Git.
- Candidate readiness now uses the same mandatory-check list as final verification. Prior STATUS is removed before verification; incomplete or inconsistent reports refuse. Every nonvisual gate must pass before review aids, and review aids must succeed before the candidate pre-release is published.
- `.gitattributes` preserves manuscript snapshots and archived patch bytes across Windows CRLF settings; a temporary-clone regression exercises `core.autocrlf=true`. No existing source or archived evidence bytes changed.
- Updated governing startup instructions, workflow/build docs, large-file routing, and the active Codex build card/prompt to the primary-developer role. Removed stop-only/Claude-only repair wording and outdated build triggers. Ordinary workflow checks do not request a build.

No manuscript, prepared artwork, font, production PDF, release asset, or actual review ledger was changed. Current delivery remains RC492-build-37; the code/workflow changes await the next owner-requested publication build. Hosted CI execution is distinct from local validation and is not claimed by this entry.

Validation: actual `python tools/dev.py check` PASS, including exact dependencies/pip consistency, baseline preflight (8 checks), prior snapshot protection against origin/main (17 files), whitespace, and `make test` (100 tests, 3 skipped for the empty art queue). Standalone artwork-skill suite PASS (54 tests, 1 skipped). `doctor`, `status`, Make's doctor target, complete candidate-report classification, and the current Windows checkout were exercised. Publication/race tests used temporary local repositories. Working source, archived patches, production release/QA ledgers, and prepared assets remain unchanged. Reports/logs are ignored or outside the checkout.

## 2026-10-15: repository cleanup

Owner request: tidy the repo and delete orphaned or unnecessary parts. Main was clean and current before edits. Recorded SHA-256, size, canonical archive path where applicable, and the recoverable base commit in `production/cleanup/2026-10-15.json` before deleting 9 tracked files:

- Seven applied proposal copies were byte-identical to their immutable RC486 through RC492 history records. Removed the duplicates; every archived record and source snapshot remains unchanged. The unique contradiction-audit proposal stays because the audit/checker still references it. `editorial/proposals/README.md` explains the canonical locations and historical path mentions.
- Removed the retired 216-line hand-drawn mark generator `tools/make_heraldry_marks.py`; it had no active caller and returned without drawing because the approved traced coin exists. Current marks continue to use `tools/prepare_marks.py` and the retained owner approvals/candidates.
- Removed `figures/src/.gitignore`, whose sole cache rule is already global. Removed 10 unused Typst definitions after searching current code/templates/config for consumers; retained the unrelated, actively used local taper function in the brush renderer. No layout was compiled for this cleanup.

Replaced obsolete launch/restart instructions with the current developer/release workflow, corrected a nonexistent figure-render command and standalone inkjet-report path, labelled the original artwork handoff as historical, and removed the incoming-art README's stale pending-integration claim. Retained all historical audits, provenance/release/QA records, art variants, style references, master images, approved derivatives, and the live vendored drop-cap code/licence. No external old checkout or art archive was touched. Existing build/release evidence remains RC492-build-37; physical print **NOT TESTED**.

Validation: `python tools/dev.py check` PASS (100 tests, 3 skipped; dependency checks, 8 baseline contracts, 17 previous snapshots/evidence files, and whitespace PASS). Each of the 9 deleted files matches the recorded base-commit hash; the 7 canonical proposal archives still match byte-for-byte. No source snapshot, archived patch, production QA/provenance/release ledger, or actual artwork bytes changed. Local bytecode-cache deletion was attempted after checks, but automatic approval review rejected both recursive and nonrecursive removal as "blocked by policy"; no cache files were deleted and no further workaround was attempted.

## 2026-10-15: reviewed full-manuscript update pathway

Owner request: ensure an efficient, well-implemented pathway for newer manuscript versions. Added `python tools/dev.py manuscript prepare|apply` and `docs/MANUSCRIPT_UPDATES.md`, linked from the governing instructions, workflow, and README. The front door selects the installed environment and needs no new dependencies.

- Preparation accepts an owner-supplied UTF-8 Markdown copy, preserves its original bytes in an ignored/external review bundle, generates exact patches plus a readable full diff/candidate, records the limited BOM/line-ending/version-marker normalisations, and checks supported Markdown, persistent content anchors, affected figure dependencies, and source-line shifts entirely in memory. Repeated text uses unambiguous exact replacement context. Matching trims unchanged document ends to keep small edits inexpensive. No active manuscript, parser inventory, figure, production review ledger, or PDF is written.
- Explicit approval requires a concrete reason and actual owner authorization, current fetched main, and unchanged base, configuration, input, diff, candidate, and proposed patches. Only the two hash-bound anchor/dependency companion configs may be modified when applying; they must be reviewed and committed with the revision. Broken bindings/unsupported Markdown block promotion. Changed figure dependencies require actual semantic review before release; citations are not automatically remapped.
- Promotion still goes through `tools/revise_manuscript.py`, creating one next immutable RC and exact patch archive while updating the source registry and production version together. Added base/candidate hash checks, stricter batch validation, an exclusive revision lock, no-clobber publication, and exact-byte rollback on ordinary write/final-check failure. Interrupted or failed rollback retains lock/recovery evidence for inspection. Existing exact-patch batches remain compatible.

The commands do not commit, push, request a build, or refresh review approvals. No actual new manuscript was supplied or promoted: current authority remains RC492, delivery remains RC492-build-37, and physical print remains **NOT TESTED**. Corrected the README's stale release/art counts against the current release records and all 275 approved selections/empty queue.

Validation: `python tools/dev.py check` PASS (140 tests, 3 skipped for the empty art queue; exact dependencies/pip consistency, 8 baseline contracts, 17 retained snapshot/evidence files, and whitespace PASS). Added 40 regressions covering isolated import round trips, no-op/version-marker handling, UTF-8/BOM/CRLF, changed/stale review refusal, companion configurations, broken anchors/dependencies, unsupported Markdown, repeated text/insertions/deletions, current-main scope, failed writes, rollback, and retained recovery locks. Real RC492 was analysed only in memory; every live anchor resolved and unrelated figure hashes stayed unchanged. No production build or actual revision promotion occurred.

## 2026-10-15: explicitly invoked editable InDesign export

Owner request: an optional workflow that creates an editable InDesign project with fonts, text flow, illustrations, editable figures, design elements and organisation. This supersedes the prior hold for this optional route; ordinary PDF production remains unchanged. Updated governing instructions and production workflow metadata accordingly.

- Added `python tools/dev.py indesign export|compose|verify`, `config/indesign.json` and `docs/INDESIGN_EXPORT.md`. Export reads the checked immutable source directly, never stale parser inventories, and creates a fresh external or ignored InDesign project. No ordinary check/Make/PDF target invokes it. The new Actions workflow has only a manual dispatch trigger, read-only permissions and a main-only job; it supplies a downloadable project artifact without committing or publishing a release.
- IDML contains native editable text, emphasis, lists, quotes and tables; measured column widths; threaded chapter stories; named paragraph/character/table/cell styles; layers, master furniture, source maps, 833 heading bookmarks and internal TOC links. Prepared illustrations, the owner cover, figure SVGs, approved mark SVGs, actual fonts and OFL licences are copied byte-for-byte. Missing approvals, stale specs/hashes, LFS pointers, escaped paths or invalid assets refuse instead of disappearing. SVG figures remain editable linked originals, not decomposed native InDesign paths; raster art retains its actual resolution.
- The packaged explicit ExtendScript finisher relinks, fits, composes/adds pages, checks fonts/links/overset, saves native INDD and round-trip IDML, and reopens the saved native document for another check. It preserves existing native outputs and unrelated open documents. Native verification requires the exact export report and compares source story text and every table cell position through the round trip, then binds output hashes. Structural, native application, visual and physical statuses remain separate. Small native edits do not update canonical Markdown or approved PDFs.
- Existing font-width measurement now closes its lazy font handles after caching advances; InDesign table allocation exposed ResourceWarnings from the old handle lifetime. Measurements and the dependency lock are unchanged.

Local full-source export and independent structural/asset verification PASS: RC492, 16 manuscript stories, 332 native tables, 10,315 cells, 343 placed graphic links and 833 bookmarks. All 274 interior illustrations, 57 figure SVGs, owner cover, 18 mark sources, 19 font files and 5 licences are packaged; only the superseded generated cover is explicitly excluded. Required ink/cover LFS bytes were fetched; no private references or generated variants were fetched or included. A complete editing package is outside the checkout at `C:/Heraldry/indesign/Heraldry_RC492-20261015`; a disposable earlier smoke export stays ignored under build. Source and cells reconcile; the packaged finishing script also passes a JavaScript syntax check.

Native InDesign composition, actual native file creation and visual inspection are **NOT TESTED**: the usual Adobe installation location and unversioned Windows InDesign COM registration were absent. The IDML contains seed pages and requires the finisher for complete composition. This is an independent native layout, not a claim of identical Typst PDF pagination, keeps or final design. No manuscript revision, production PDF build, actual semantic/page review approval or release occurred. Current authority remains RC492, delivery RC492-build-37, and physical print **NOT TESTED**.

Validation: `python tools/dev.py check` PASS (190 tests, 3 expected empty-queue skips; locked dependencies/pip consistency, 8 baseline contracts, 17 previous snapshot/evidence files and whitespace PASS). The 50 new regressions cover asset approval/spec/hash/LFS/path guards and portable copying; exact rich text, nested lists/quotes, links, native tables/cell positions and widths; deterministic IDML, missing references, broken threads, changed content/bundles, unreadable profiles, preservation of manual outputs, and refusal to substitute structural success for a matching complete native report. Full real export/verification and packaged JSX syntax PASS. External editing package: 379 files, 154,725,675 bytes; IDML 1,139,109 bytes. Hosted manual workflow and actual InDesign execution were not run.


## 2026-10-15: targeted publication improvement first pass

Owner instruction: "Continue as you suggest", following the researched proposal report. Implemented the initial calibration correction, traced authority conflicts, completed a fresh bounded source proof, and prepared executable reader/accessibility/physical-proof protocols. This authorises this first pass, not unseen manuscript changes, substantive canon decisions, a paid commission, or another book build.

- Calibration labels and samples now use the active 11 pt body, 9.3 pt table, and configured essential minimum. Table values are shared through equal-valued constants; inlining them reproduces the prior adapter exactly. A current manuscript paragraph is read verbatim with an exact-one-match assertion; the actual table-header style is shown. Both cream/white diagnostics rendered as single Letter PNGs at 144 ppi and were directly viewed by the integrating and a fresh model reviewer. No production PDF was generated.
- Five scoped brief/source conflicts are inherited from supplied RC484: 4 TAP, Druidic Rituals, Appendix C, automatic armour/no Brace, and no Monster ability Checks. The authority matrix preserves established source and records pending owner dispositions. No standing contract was silently aligned.
- A second model context read 1,517 defined source lines plus targeted checks. Seven findings cover tutorial attack control flow/rider timing, missing Search in C.13, a Parry example modifier, Block declaration timing, an unavailable reaction comparison, contextual pronouns, and optional Basic Mode components. Ten exact replacements remain proposed and unapplied, with unique matches and base hash verified. This is not human independent copyediting, a whole-source proof, or full-format PDF review.
- `docs/PUBLICATION_CHECKS.md` specifies bounded reader tasks, meaningful PDF-accessibility checks, final-format proof coverage, and physical reproduction/binding observations. Actual participants, exact delivered PDF, assistive-technology execution, and physical sheets remain required. The private release was not accessible from the unsigned browser; preserved old PDFs were hashed and rejected as current evidence because they do not match build 37. No credentials were extracted or fresh build dispatched to substitute for the missing download.

Evidence: `production/qa/publication-first-pass.md`, `publication-authority-review.md`, `independent-editorial-first-pass.md`, `calibration-source-review.md`, and `editorial/proposals/publication-first-pass.json`. Main source remains RC492 with unchanged SHA-256; all artwork/figure approvals, historical snapshots/archives, production release/visual ledgers, and released PDFs remain unchanged. Delivery remains RC492-build-37; source calibration changes await the next separately requested build. Physical print **NOT TESTED**.

Validation: baseline and post-change `python tools/dev.py check` PASS (190 tests each, 3 expected empty-queue skips; exact dependencies/pip consistency, 8 baseline contracts, 17 protected prior snapshots/evidence files, and whitespace PASS). Actual cream/white PNG compilation and scoped visual review PASS; ten proposed patches each match once and were applied only in memory to produce an ignored readable diff. No new unit tests, manuscript promotion, production PDF build, actual reader study, screen-reader session, or physical proof occurred.


## 2026-10-15: owner-approved RC493 editorial revision and canon alignment

Owner instructions: "Approve all as proposed." and "Continue". Promoted the ten exact reviewed replacements once through `tools/revise_manuscript.py`, creating RC493 and its immutable approved archive. New source SHA-256: `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`; parent RC492 and all prior snapshots/archives are unchanged. All seven findings in the approved packet are applied; no additional manuscript wording was introduced beyond those ten replacements and the revision marker.

- Applied the teaching Dire Wolf's one-Bite control flow and rider timing, C.13 Search branch, legal Shortsword Parry arithmetic, Block declaration timing, Mara's available reaction comparison, three contextual pronoun/grammar repairs, and optional Ogre component counts. Exact reconstruction matches RC493 bytes and all 332 table-cell hashes are preserved.
- Added `docs/CANON_AUTHORITY.md` and linked it from both startup contracts. Recorded the owner's five approved existing conventions: 4 TAP with Journey exceptions, Druidic Rituals, Appendix C precedence, automatic armour/no Brace with shield mitigation through Block, and no Monster ability Checks with existing exceptions. Updated authority-review dispositions without rewriting their RC492 trace evidence.
- Reparsed source/index inventories: 833 headings, 332 tables, zero ragged tables, 63 anchors resolved. Parser-generated metadata was normalised to repository LF without changing JSON values. Avoided `make parse` because its extras also build PDFs; no book or diagnostic PDF was generated.
- Actual SVG/caption/source and standalone PNG reviews covered affected FIG-06, 11, 12, 16, 18, and 19. Updated only their reviewed source bindings, retaining 51 unaffected entries and all SVG/caption bytes. Current figure gate PASS 57/57, zero stale/open majors, with four new open minor figure-copy proposals recorded separately. No minor was silently accepted or fixed as part of the approved source batch.
- Canonical approved evidence is `editorial/history/RC493.json`, SHA-256 `a9303b69f0b167350d87b83dd2ec2cb7c1baa5f8f2cb1300205dd48eaccca1dc`. Removed its applied proposal duplicate only after recording byte identity and archive hash; the earlier proposed form remains in Git history. See `production/qa/rc493-editorial-verification.json` and `rc493-editorial-application.md`.

Validation: baseline and post-integration `python tools/dev.py check` PASS (190 tests each, 3 expected empty-queue skips; exact dependencies, pip consistency, 8 baseline contracts, 17 prior protected source/archive files, and whitespace). Source reconstruction and preserved table/anchor evidence PASS; actual scoped figure review and currency gate PASS with 4 open minors. No additional unit tests, production PDF build, hosted publication run, full-format/human proof, reader study, or screen-reader session was performed. Last delivered PDFs and their release/visual/package/gate records remain RC492-build-37 and predate RC493. Physical print **NOT TESTED**.


## 2026-10-16: complete figure review and authorized repairs

Owner instruction: "Ok just review and apply the figure fixes. Review all figures to ensure they are well designed and accurate. Make changes as needed to ensure their readability, clarity, accuracy, and excellence in design." Completed a fresh semantic and rendered review of all 57 figures. Two delegated reviewers covered instructional diagrams/scenario maps; the integration owner reviewed the key/template, changed details, and every map-caption specimen. Review authorship and source limitations are explicit in `production/qa/figure-review-all-rc493.md` and its companion records.

Improved 25 SVGs and 9 captions: activation/mitigation/visibility/Aura/AI/deployment exceptions, reaction timing, typography, local keys, spatial labels/rulers, terrain layers, mixed Fen mud/pools, and paired Tabletop/Grid measurement. Removed an unsupported spatial patrol position while preserving its required setup instruction in a qualified note. All four earlier open copy findings are resolved. Expanded missing rule dependencies, bound scenario coverage to current source, and made generated line endings deterministic. No manuscript revision or mechanics changed.

Baseline and final `python tools/dev.py check` PASS: 190 tests run each, 3 expected empty-queue skips, exact dependencies, baseline contracts, immutable snapshot/history and whitespace. Full figure generation/selfchecks and the semantic gate PASS 57/57 with zero stale or open findings. Fresh scratch generation reproduces 57 SVGs and both metadata files exactly, and current inputs reproduce all 57 inspected figure PNGs; all 36 final map captions were additionally viewed at native width. Minimum essential label size remains 9 pt. Native previews are slightly smaller than the current v4 frames.

Last PDF delivery and its hash-bound visual/release/package/gate evidence remain RC492-build-37. No new book build or publication occurred. Final PDF placement/pagination and accessibility are not tested by this standalone review. Physical print **NOT TESTED**.


## 2026-10-21: player-aid design and art direction

Owner instruction: "I want there to be a consistent well thought out design and art direction across all reference sheets. Reference sheets should share a style inspired by medieval heraldic grimdark fantasy. Use mainly b&w ink penned design elements." Wrote `docs/PLAYER_AIDS.md`: the reference sheets inherit the book's Grim Heraldry system (approved marks, four type families, black ink and tints, cream and white). It defines a shared sheet anatomy (iron header band with chapter arms, footer with logo and RC stamp), one shape grammar for flowcharts, the art rule (one approved ink vignette at a boundary), a ten-sheet series PA-1 to PA-10, source-fidelity records, print and an acceptance checklist. Composed a specimen of PA-2 Monster AI (front) from the book's components with the approved Minotaur ink: `typst/aids/pa02_specimen.typ`. Its wording is abridged from RC512 §9.5 and C.8 and has not had a semantic review; no PDF is committed.

Open owner decision: the production route, either the book's Typst kit (recommended, source-bound) or Canva (asset kit, fonts and a master template first). No manuscript revision, book build or release. Physical print **NOT TESTED**.

Later 2026-10-21, owner: "I want to try both and compare." Made PA-2 Monster AI (front) in Canva from a written brief with the same approved art, arms, logo and wording, corrected six text changes and a generated dragon that Canva introduced, and compared it with the Typst specimen. Findings are in `docs/PLAYER_AIDS.md` section 10, "Route trial". The Canva draft is not saved until the owner approves it. The route decision remains open.
