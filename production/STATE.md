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
