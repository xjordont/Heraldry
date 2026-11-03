# Design history

This is the dated record behind `docs/DESIGN.md`: owner requests in their own words, design states that were later superseded, adoption and specimen steps that are complete, and inspection logs of old releases. It is a record, not guidance. Where it disagrees with `docs/DESIGN.md`, the design document is current.

Until 2026-11-03 this material lived in three overlapping files: `docs/DESIGN_SPEC.md`, `docs/BOOK_DESIGN_PLAN.md`, and `docs/DESIGN_REFINEMENT.md`. The owner approved merging them on 2026-11-03: "one current design document with the same requirements; the dated history moves to docs/history/." The excerpts below are quoted from those files as they stood that day, with their headings demoted; the section headings and short introductions are new. Paths in backticks inside the excerpts are updated to where the files now live: on 2026-11-03 `docs/design/REFERENCE_STUDY.md`, `production/design-decisions.md`, `docs/REFERENCE_ANALYSIS.md`, `MASTER_PROMPT.md`, and the `reports/` files moved to `docs/history/`, and `MASTER_PROMPT.md` was retired there as history. Other names are as the old files had them, and some no longer exist: the tracked `references/` folder was deleted on 2026-11-02, and the InDesign export and the print editions were removed the same day.

## Old citations

| Old citation | Now |
|---|---|
| `BOOK_DESIGN_PLAN.md` sections 1 to 13, including 6.19 and section 13's rule 9 | The same numbers in `docs/DESIGN.md` |
| `BOOK_DESIGN_PLAN.md` sections 10 and 11 (adoption steps, decisions recorded) | `docs/DESIGN.md` sections 10 and 11 (current state); the steps and decisions are quoted below |
| `DESIGN_REFINEMENT.md` pagination policy, measurement, and release audit | The keep rule, its measurement, and its audit: `docs/PROJECT_CONTRACT.md` ("Pagination: the one-page keep rule"); the page policy and how the composer applies the rule: `docs/DESIGN.md` 8.1 to 8.5 |
| `DESIGN_REFINEMENT.md` dated entries (2026-10-29 to 2026-11-01) | Their live rules are in `docs/DESIGN.md` where each applies; the entries are quoted below |
| `DESIGN_SPEC.md` 1 (identity) and 2 (grid) | `docs/DESIGN.md` sections 1, 2, and 4 |
| `DESIGN_SPEC.md` 3 (type) and 4 (reading flow) | `docs/DESIGN.md` sections 3, 8, and 13 |
| `DESIGN_SPEC.md` 5 (tables) and 6 (entries and scenarios) | `docs/DESIGN.md` 6.10, the section 6 introduction, 6.15, and 6.16 |
| `DESIGN_SPEC.md` 7 (graphics and art) | `docs/DESIGN.md` section 7, 6.8, and section 12 |
| `DESIGN_SPEC.md` 8 to 10 (navigation, specimen, delivery) | `docs/DESIGN.md` sections 5, 15, and 16; the specimen gate is quoted below |

## Before 2026-10-12: the first implementation brief (`DESIGN_SPEC.md`)

The first design brief, distilled from the reference books. Its visual identity was superseded by the design plan on 2026-10-12 and its starting values by the compact profile; its grid, table, and graphics rules that were still current are in `docs/DESIGN.md`. Its two banner notes and status line:

> **2026-10-16 compact approval, implemented from 2026-10-20:** 10.5 pt body, 9 pt tables, narrower margins, and the approved refinement report supersede earlier size/geometry proposals. The effective profile is `config/design_tokens.json`, shared by Typst and `tools/layout_profile.py`. Complete-unit keeps and source fidelity remain mandatory.

> **2026-10-12:** `docs/BOOK_DESIGN_PLAN.md` (design system v2, "Ink and Iron") supersedes this document's visual identity: display face, heading, furniture and component styling, and the page-type templates. Grid, page, source-fidelity and pagination rules here and in DESIGN_REFINEMENT.md remain in force.

Status: implementation brief, distilled from the ten owner-selected visual references. `docs/DESIGN_REFINEMENT.md` supplies the latest owner-requested iteration and overrides the earlier specimen freeze. These specifications guide the first stress specimen. Tune optical details once after rendering, then apply the resulting system consistently. MASTER_PROMPT.md governs source preservation and completion. The manuscript governs all mechanics and terminology.

Its reference assignments (section 1):

Reference assignments: BlackDeathCity and Deth Wizards for atmosphere and vignette placement; Mythras for calm grayscale prose; Hametsu and Five Leagues for tables, examples, and navigation; Hellcrawl for keyed entries. The Village Hunt informs silhouette/open-space integration; Dread Nights informs hierarchy and labelled entries; TNA Ultimate and TES: Call to Arms inform nearby exact instructional diagrams. Use only the ten titles recorded in `references/sample_pdfs.json`. Do not clone a page, extract source art into the book, or import reference mechanics.

Its starting type specification (section 3) and shared table grammar (section 5), later replaced by the compact profile and the ledger:

Four intentional roles are Source Serif 4 rules, Source Sans 3 data/navigation, Grenze Gotisch display, and IM FELL English roman flavour. Verify licensing, available weights, embedding, and glyph coverage. Bundle approved files and licences.

| Role | Starting specification | Behaviour |
|---|---|---|
| Body | Serif 10.5 pt / about 13.925 pt baseline pitch | Justified within limits; 4.5 pt paragraph spacing |
| Chapter title | Display 50 pt | Original ornament/art may accompany it; preserve canonical numbering |
| Major section | Display 21 pt | Keep with meaningful following content |
| Subsection | Serif bold 13 pt (12.5 pt before the 2026-11-01 audit) | Clear vertical separation; no gratuitous box |
| Minor heading | Body-sized bold | Run-in only where source structure permits |
| Table body | Sans 9 pt / about 11.85 pt | Minimum 9 pt essential text; bold headers |
| Example | Body family, 10–10.5 pt | Explicit title; subtle outline/left rule; clean substrate |
| Diagram label/caption | Sans 9–10 pt | Legible at placed size; no downscaling below minimum |
| Index | Sans or serif 9–9.5 pt | Hanging indent; two or three columns after legibility testing |

These are targets, not measurements copied from the books. Optical adjustment is permitted after the actual-content specimen. Do not globally shrink content to fit. Preserve semantic bold and the user's typography lock, including ASCII quotes/apostrophes, numeric-range en dashes, ×, and −.

Shared grammar: bold headers, modest cell padding (4 pt horizontal and 2.2 pt vertical), useful column width, consistent alignment, light rules, optional grayscale bands on the chosen clean substrate. Start rules around 0.5–0.7 pt and verify at actual size. Start bands around 6% black but treat shading as optional; labels/rules must work without it.

Its reference handling (section 8), from before the `references/` folder was deleted:

Each adopted reference lesson appears in `docs/history/design-decisions.md` as reference ID/page, abstract principle, Heraldry implementation, and specimen evidence. Reference rules never enter the editorial patch ledger as an authority.

Missing optional references do not block production. Read the analysis/specification once; pass implementation decisions, not the entire PDF collection, to workers. Primary inspection is a bounded design task, not a repeated assignment throughout the build.

Its stress specimen and freeze gate (section 9), completed before the first full book:

### 9. Stress specimen and freeze gate

Produce an 8–12-page actual-content specimen, allowing an extra page only if needed for a genuine high-risk component. Include:

- Chapter opening and ordinary facing pages.
- Normal two-column rules, a sustained procedure, and a worked example.
- Short random-result table, numeric table, longest prose row, and widest source table.
- Monster profile, scenario with its canonical scaling fields, and an appendix reference.
- A vector diagram, ink art treatment or clearly identified production-only art reservation, and index slice.

Inspect at actual size and enlarged detail. Use a contact sheet only for page rhythm. Confirm hierarchy, optical type size, column balance, table relationships, note attachment, gutter clearance, grayscale diagram distinctions, and art/prose separation. Apply the component rubric in VISUAL_QA.md. Revise the system once, record it, then produce the full book.

No PASS based solely on an attractive cover, chapter opening, or successful compilation. The final design gate is usable ordinary pages plus complete source reconciliation and all exceptional table/diagram checks required by MASTER_PROMPT.md.

## 2026-10-07: the design refinement request (`DESIGN_REFINEMENT.md`)

Status: standing refinement requirements with the approved compact implementation in progress. No new release is implied. This document overrides the old specimen freeze where they conflict. Resolve the active manuscript through `source/versions.json` and preserve its bytes. Work on main and retain all existing figures and content checks. Read REFERENCE_ANALYSIS.md, DESIGN_SPEC.md and VISUAL_QA.md with this brief.

### Historical evidence and diagnosis - 2026-10-07

Inspected the latest verified delivery from GitHub Actions run 37537036480 (build input 75c430e0033f66eca34b31383491de6fd41a3366): digital PDF 453 pages, interiors 450 pages. Digital SHA-256: 68bc90e062cf7f01ef438e720fba0c8d9ee46b5f6f2ce54134a4803ded6ad0e7. Reviewed 13 representative digital pages at page-composition scale, plus detailed pages 23 and 427; this is not a new all-page approval. Inspected 23 selected pages across all ten owner-selected reference PDFs; page numbers in the reference analysis are 1-based PDF viewer numbers.

The draft has readable type and faithful data, but much of its identity is one ring, Cinzel titles and cream paper. Chapter openers lack atmospheric art. Dense entry pages have little differentiation between entry title, metadata and explanatory prose. Scenarios flow into one another mid-page. Column/full-width transitions sometimes produce a tall lone column and a disproportionately empty neighbour. Automated geometry checks passing is insufficient evidence of editorial finish.

Concrete regression examples in the inspected digital PDF:

| Target | Observed issue | Required repair |
|---|---|---|
| Chapter openers, PDF pp9,19,36 | Small motif and title with no atmospheric image; limited contrast with ordinary pages | Compose source-specific ink art, chapter number/title and lead as a deliberate opening; resume readable rules below |
| Size and Footprints, T004, PDF pp23–24; interior pp21–22, folios15–16 | Four-row table leaves Huge alone on the following page | Move the complete table and its caption/intro together when they fit an empty column |
| Artifact entries, PDF p141 | Long sequence of similarly weighted labels and prose | Stable entry title, compact metadata line and quieter descriptive prose; preserve source order and every field |
| Whispering Grove, PDF pp295–297 | Scenario starts partway down a page, setup/map/special rules dispersed, next scenario starts mid-page | Start each named scenario on a fresh page; compose setup, deployment map and key instructions as a coherent opening unit |
| C.5 Reactions Summary, T327, PDF pp426–427; interior pp424–425, folios418–419 | Long single-column introduction with empty adjacent column, then one table row before a continuation | Reflow introduction across the useful width; measure the complete table before choosing a whole-table move or controlled continuation |

The table audit lists 64 multi-page tables or transformed entry sets. That count is a review queue, not proof that all 64 are defective: many genuinely exceed a page. Current htable uses breakable:true for its wrapper and breakable:false for cells. It prevents row splitting but does not prevent avoidable splitting of a short table. Current layout_qa.py recognizes heading-looking text only near the page bottom; it does not track complete subsections, table fragments, column transitions or continuation identity. Fix the architecture and add targeted evidence, rather than weakening reconciliation or stamping another visual PASS.

### Page treatments to implement

Retain portrait Letter, a flat #FCFAF5 cream page, safe margins, four intentional licensed font roles and readable body/table sizes. Distinguish pages through information architecture and composition, not more texture or decorative borders.

1. Chapter opener: one source-specific horizontal ink scene, substantial title with clear chapter number, short lead and a clean transition into rules. Target roughly one third of the page for art when available. Make the scene asymmetrical and leave useful negative space. No generic hooded skull repeated eleven times. Use ART_MANIFEST subject plans and check each against current source lore.
2. Ordinary rules: calm two-column prose with clearly different major, subsection and run-in treatments. Use larger major headings when full width allows them; nested headings remain serif. Keep existing emphasis rather than making all text heavier. Use a consistent rhythm of spacing and a small number of horizontal rules.
3. Examples: source example label and modest inset/left rule or light grayscale field, attached to the relevant procedure. Use the clarity of Hametsu's dedicated examples without its dark sidebar or narrow permanent third column.
4. Tables: family-specific widths and alignment, strong header separation, generous descriptive column and restrained alternating bands. Selective dark header treatment may help a small lookup table, but large tables remain light. Every continuation repeats the correct column headers and identifies its source table.
5. Reference entries: stable title → source metadata/stat strip → description → abilities/procedure anatomy. Short entries stay together when they fit; long entries continue with a repeated identifying name. Separate neighbouring entries through spacing and a fine rule, not a box around every paragraph.
6. Scenarios: fresh page at each named scenario; clear scenario title and source flavour; canonical setup fields in a predictable arrangement; deployment map beside or directly after its setup. Continue into special rules, scoring and aftermath using the exact source headings. A multi-page scenario is acceptable; a split opening with detached deployment instructions is not.
7. Atmospheric spot art: after the twelve required masters are complete, add a bounded set of source-specific creatures, equipment or architecture at natural transitions after review of the required suite. Use rectangular/open placements with clean negative space, never text over artwork or art filling a known pagination defect. Keep deployment figures as precise editable vectors.

### Acceptance and execution

First render an actual-content stress specimen covering opener, ordinary facing pages, nested short subsection, example, T004, long repeated-header table, transformed entry, monster and the Whispering Grove setup, plus C.5 reactions. Include the preceding/following pages for each pagination case. Compare before/after at readable size; freeze refined tokens only after these cases work. A specimen is a milestone, then apply the components across the entire book.

Extend the layout audit to record semantic heading starts and their following content, page/column breaks inside short fit-capable tables/subsections, continuation titles/headers, figure/setup distance, row orphans, and unexplained large voids. Persist findings and reviewed exceptions by stable source IDs and current hashes. Hard failures: stranded headings/captions, missing repeat headers, avoidable split of a fit-capable short table, content overlap/overflow, missing or duplicate text/cells. Subjective whitespace flags need actual inspection, not a universal ban on blank space. Caption and entry-name continuations are publication furniture, not manuscript patches.

Inspect all revised pages at contact-sheet scale for rhythm, every continuation/table exception and all scenario openings at readable size. Reconcile all text/cells, rebuild navigation and package from the same final input hashes. Record the current design outcome separately from historical geometry PASS.

### Sources consulted 2026-10-07

These support the pagination/API/export methods. Numerical keep thresholds and Heraldry component choices above are our production decisions, not standards mandated by the sources.

- Butterick, headings and keeps: https://practicaltypography.com/keep-with-next-paragraph.html
- Butterick, style-based page starts: https://practicaltypography.com/page-break-before.html
- Butterick, widow/orphan tradeoffs: https://practicaltypography.com/widow-and-orphan-control.html
- Adobe, paragraph keep options: https://helpx.adobe.com/incopy/desktop/format-text/paragraph-formatting/formatting-paragraphs.html
- Typst, sticky/unbreakable blocks: https://typst.app/docs/reference/layout/block/
- Typst, table continuations: https://typst.app/docs/guides/tables/

### Owner clarification: mandatory one-page units — 2026-10-07 UTC

**Mandatory one-page keeps:** Every complete scenario, section/subsection, table, example, procedure, stat profile or reference entry that fits within one empty usable page at its approved layout width must occupy exactly one page. Include its heading, all nested content belonging to that unit, caption, legend/deployment diagram and necessary notes in the measured group. If insufficient space remains, move the entire unit to the next page; do not split it across pages merely to fill space or balance columns. A column limitation is not proof that a unit cannot fit a page: use the approved full-width layout where appropriate. Preserve legible type, spacing and all content.

Measure rendered height, not manuscript length or character counts. A section extends from its heading to the next heading of equal or higher rank; a scenario extends to the next scenario or enclosing-section boundary. Nested fit-capable groups remain protected inside longer parents. Fit uses the empty usable content frame, after margins, running furniture and required spacing, with a small conservative tolerance. Test both facing-page positions. Artwork must not displace or fragment a fit-capable rules unit; reposition decorative art instead.

Only genuinely over-height units may continue to another page, with repeat table headers or identifying continuation and intact smaller child units. Record their source IDs, measured dimensions and reason. Never shrink type, omit notes/maps, clip content or artificially enlarge a unit to evade the keep rule. Intentional whitespace left by moving a complete unit is acceptable.

Required release evidence: a current input/PDF-hash-bound audit covering every applicable stable source ID, its measured height and frame width/height, fit classification and actual PDF page set. Any fit-capable unit appearing on more than one page is a hard failure; missing audit coverage also fails the gate. Inspect boundary cases and actual pages, not just metadata. Implement this check in the renderer/layout audit and mandatory verification gate before the next illustrated release.

## 2026-10-12 and 2026-10-13: the design plan, v2 to v4 (`BOOK_DESIGN_PLAN.md`)

The plan began on 2026-10-12 as design system v2, "Ink and Iron"; v3 and v4 ("Grim Heraldry") followed the same day, and the marks were approved on 2026-10-13. Its decisions as recorded (section 11):

- **Claude Code, 2026-10-12, within the owner's request for a design plan:**
  - display faces: Grenze Gotisch (titles and names) and IM FELL italic (flavour) replace Cinzel;
  - ragged-right body (superseded the same day: the owner asked whether all body text should be justified, and a side-by-side on the 2.6 and Fighter pages showed justified-within-limits sets evenly and saves lines; body is now justified, and the owner then locked it at 11 pt);
  - black-bar table headers;
  - one monster per column;
  - caption bars.
- **Owner, 2026-10-12:**
  1. Keep the thumb tabs, "or something more artful that serves the same purpose"; then (later the same day) "the pennants should have the name of the chapter in a word for easy reference ... written 90 degrees to run along the page edge; use a keyword for the chapter for long chapter names": section 5.
  2. Chapters whose art is not yet approved use the typographic opener (a 1.2 in drop, type alone), so layout never waits for art.
  3. C.13, the single-sheet rules summary, is also produced as a separate one-page play aid. It is built from the same source and template as the C.13 page, as its own file, whenever the book is built; no PDF is produced before a build is requested.
  4. "Add some more flavour than the plain layout ... better graphic design to the tables and elsewhere", then "add much more character and rebuild the whole graphic design moving in a more ornate grim dark direction while focusing on clarity and ease of uses. Ensure the tables are not only beautiful but also very easy to read": sections 3, 4, 6.10 and 12 (design system v3).
  5. v4 (later 2026-10-12): bolder, centred blackletter tab keywords; ledger tables with centred values and the coin mark for "c"; skulls replaced by chapter arms and the broken crown; calmer rules; narrower margins; IM FELL roman for flavour; the typesetting policy of section 13.

Owner wording the plan quoted where it applied:

- Tables: Owner 2026-10-12: "The tables look amateur. We should be centring values in cells ... changing (c) to a symbol for a coin."
- Banner tags: "The black tags should consistently be aligned to the top left of the text they reference; not centred above it".
- Ornament: the skulls of v3 retired ("a bit cheesy"); the v3 thorn rules retired ("some of the rule lines are crowded").
- The armoury: The owner directed on 2026-10-12: "take it further ... more decorations, symbols, ornaments but keep it tasteful without distracting from the text or art ... the skulls are a bit cheesy ... design something better grim dark medieval heraldry that's not so on the nose ... some of the rule lines are crowded."
- Typesetting: Owner 2026-10-12: "We should be very careful of how we set up policy and procedure for typesetting and text layout to be easy to read, avoid page bloat, and avoid having to read sections/paragraphs across pages."
- Page starts: "Keep the page breaks so each section starts on a fresh page" (2026-10-12).
- Section-end fill: "fill in the white space with either art, diagrams, further figures" (2026-10-30).

The flavour comparison and the marks' provenance, as the plan recorded them:

**One treatment for flavour (owner 2026-10-12, revised the same day):** all flavour text is IM FELL roman at the running body size (10.5 pt; see below), justified and hyphenated, with 6 pt of space between paragraphs (no first-line indents). Justification uses Typst `justification-limits` (word space 90–140%, letter spacing −0.5% to +2% of the em) so even the 3.5 in monster columns set without rivers. Section-level flavour (chapter leads, the flavour under a section title, place lore, scenario flavour) is the `lead-block` component: a centred measure 82% of the frame wide, with the text justified inside it. Entry flavour inside a column (monsters, classes, backgrounds) is the `flavour` component: the same face, size, colour and spacing at full column width. Justified was chosen over centred after a side-by-side on the Deepwarden page: centred multi-paragraph lore leaves ragged edges on both sides; justified reads as one quiet block. The specimen renderer can still show the centred variant with `tools/render_template_specimens.py --lead center` for comparison.

| Mark | Form | Where |
|---|---|---|
| **Chapter arms** | Owner-approved 2026-10-13 ("Approved. Make sure they are big enough to see."), chosen over five Nano Banana 2.1 rounds (`production/art/marks/APPROVED.json`). Flat black ink on a plain field, with bold interior detail and no grey. Each charge is set by `tools/prepare_marks.py` inside one shared double-rimmed heater shield (the Mechanics candidate's rim) and traced to vector SVG on the cream page colour. World/Lore: raven on a crown broken in two. Mechanics: die. Round: hourglass. Actions: three arrows points down. Combat: bearded axe and notched sword. Party: tattered banner. Equipment: great helm. Powers: open hand with an eye. Monsters: horned wyvern's head. Scenarios: ruined arch. Campaign: war pavilion. Learn: key. Basic: lantern. Reference: open book. Index: quill and ink pot | Chapter opener (52 pt, about 0.72 in), contents rows (22 pt), running head (15 pt), armoury sheet (52 pt). Never below 15 pt |
| **Logo / signature mark** | Owner-approved 2026-10-13: a broken heater shield bearing a three-towered castle, cracked through its portcullis gate, with fragments falling away; "the arms of a fallen realm". It replaces the six earlier signature candidates, which are retired | Opener-frame head (30 pt), flourish centre (22 pt), title page, back cover, armoury sheet (92 pt) |
| **Coin** | Owner-approved 2026-10-13 ("Yes to v2 but take the notch out of the border"): a hammered medieval long-cross penny in heavy black ink, with a bold rim, a beaded border, a solid cross and four pellets in each quarter. It is heavy enough to match bold figures at text size. Generated with Nano Banana 2.1, the notch closed by an image edit, and traced by `tools/prepare_marks.py`. `coin-reversed.svg` (ink in paper colour) serves black header bands. It sits on the baseline beside its figures | Stands for the source's "c" in tables and stat bars |

## 2026-10-16 to 2026-10-20: the compact profile

The owner approved the layout review on 2026-10-16; implementation resumed on 2026-10-20. As the plan and the refinement recorded it:

Status: compact v5 implements the owner's 2026-10-16 approval of the layout review, explicitly allowing **10.5 pt body**, **9 pt tables**, narrower margins, and more assertive refinement. The owner resumed this implementation on 2026-10-20. This supersedes the earlier 11 pt lock and conservative trial values. `config/design_tokens.json` is the single effective geometry/type/spacing authority; Typst imports it and Python uses `tools/layout_profile.py`. `config/production.json` mirrors public format values and is checked for agreement.

The original v4 reference study and component rationale below remain useful where the v5 profile does not supersede them. Ordinary rules use two columns. Chapter/section opening flavour has an explicit, inset single-column region; wide tables and diagrams retain deliberate spanning roles. Fit-capable complete source units, source order, readable figures, the accepted blank verso, and independent visual review remain mandatory. Local specimens and measured builds are evidence of their stated scope, not a new release approval.

The evidence is in `docs/history/REFERENCE_STUDY.md`: all ten reference books were mapped page by page, and about 90 pages were inspected closely.

This plan supersedes the visual identity sections of `DESIGN_SPEC.md` (display face, heading styles, furniture, component styling). The pagination contract in `DESIGN_REFINEMENT.md` stays in force without change. That contract covers fresh-page starts, mandatory one-page keeps and continuation rules.

The decorative pennant occupies the outer margin. Its 9 pt keyword sits on the inner face, with actual rotated glyph bounds checked against the 27 pt safe line and the body frame. Initial 36 pt outer and 40.5 pt top margins failed this check; 42 pt outer and 45 pt top margins preserve clearance.

### Compact profile approval - 2026-10-16; implementation resumed 2026-10-20

The owner approved the complete layout review and explicitly authorized 10.5 pt body text, 9 pt tables, narrower margins, and more assertive refinement. This supersedes earlier 11 pt and unchanged-margin trial proposals. Use the effective profile in `config/design_tokens.json` through Typst and `tools/layout_profile.py`; the production format record is a checked mirror. Four font roles remain intentional. Ordinary rules use two columns; opening flavour uses a distinct inset single-column region. Preserve manuscript bytes, complete fit-capable units, source order, all source-bound figures, deliberate wide objects, and the accepted blank verso.

Measured furniture safety takes priority over the smallest margin: the initial outside 36 pt/top 40.5 pt/bottom 40.5 pt trial left rotated navigation, running heads, and folios outside the 27 pt safe line. The corrected profile is inside/outside/top/bottom 45/42/45/45 pt, with a 16.2 pt column gap. Page savings and full-book acceptance must come from the actual same-source builds and their recorded review, not these token changes alone.

## 2026-10-29 and 2026-10-30: design review repairs, imprint, polish, and section-end fill

The bestiary note the plan carried (6.15):

- **2026-10-29:** 100 approved Monster portraits (and 24 other pieces) had silently dropped out after a pronoun normalisation changed their catalogue specs; they were reviewed, re-bound, and restored. `tools/check_art.py` now fails on an approval bound to an outdated spec, and the composer refuses a stale flavour-block anchor.
- **Effect:** this replaces today's half-empty bestiary pages with full ones.

### Design review repairs - 2026-10-29

Owner instruction after the RC522 design review: "Fix everything to the best of your ability using your best judgment and best design layout principles." Layout and art repairs only; no manuscript text changed.

- Thumb tabs end 3 pt short of the text frame (`thumb_tab_clearance_pt`). Rotated keywords sit with their glyph ink between the 27 pt safe line and the tab's engraved inner line; layout QA and the tests measure rotated keywords by glyph outlines because Grenze Gotisch's 1.1 em ascender metric is far taller than its letters.
- Tables: a hidden duplicate title no longer leaves a blank line under its heading; `Cost (c)` keeps its coin on one line; numeric ranges never break after the en dash; the closing brush takes no height, so it cannot fall alone onto the next page; column widths go where they remove the most wrapped lines (scope decisions keep the reviewed proportional rule).
- Basic Mode profiles: a run-in label merged with its list no longer glues the following piece, so profile subsections balance as separate pieces instead of one block. A long profile keeps its name, identification lines ("Class: ... | Level: 1"), and first subsection together, so it never opens at a column foot with only its name and stats.
- Short chapter introductions (one to three plain paragraphs, at most 700 characters, before the first section) are set as one standfirst at the opener's 82% measure.
- Balanced tails: a complete column unit that opens with its heading (an ancestry, a Monster, an item) is a whole balancing piece. Only a bare heading travels with the next piece. Treating whole units as bare headings had merged every unit of a tail into one piece and walked the tail back to the segment start, which stranded the 6.9 Ancestries introduction alone on its page.
- A table that fits a column but not beside its heading starts only where both columns of one page can hold the pair, then continues under its repeated header into the second column. Kept whole, Typst's sticky heading skipped a column and left the Climate 5 journey-table heading alone on its page.
- A short last page (about a dozen lines in one column, or half that already balanced over two) pulls back the piece from the foot of the previous page; the run then fits that page or gives the last page a fuller close. A tail that keeps moving to new plans is refining; only a return to an earlier plan counts as oscillation.
- Front matter: the colophon and How to Use name the current manuscript automatically. The stale RC484 text, the art-light statement, and the retired Cinzel credit are gone; the illustration credit is left to the owner with the other held credits.
- Index: the last index page is balanced into three whole-entry columns of near-equal height; a column never starts with a sub-entry or ends with a letter head.
- Back cover: the approved ART-COVER-002 party scene sits between the blurb and the game facts; the crest flourish under the frame's own crest is omitted, and the blurb is set at 4.8 in for an even rag.
- Fresh pages for numbered sections are kept, as the owner instructed on 2026-10-12. The Bestiary keeps one Monster per column (BOOK_DESIGN_PLAN 6.15); its half-empty columns came mainly from missing portraits, now restored.

### Imprint, opener spreads, and companion outputs - 2026-10-29

Owner instruction: version is the manuscript version; author Jordon; publisher Escutcheon Press; no ISBN; no illustration credits; player aids and Basic Mode Hero records current and to the book's standard; all art at 300 ppi or more.

- Title page: title, subtitle, and the author's name as a tracked byline in the title's serif; at the foot, the castle mark, the publisher's imprint, and the manuscript version. The colophon carries the author, publisher, copyright, and the type credits; the back cover carries the imprint.
- Opener spreads: a chapter whose introduction cannot share its opener page opens on a display page (art, arms, number, and title, centred) with the whole introduction on the facing page. A zero-height probe after the opening flavour decides it from the first layout iteration; Chapters 8 and 11 use it.
- Back cover: an edition blurb replaces the repeated Chapter 1 lead, set to end on a full line.
- Typography: smart quotes are off in every Typst document, and the player aids and Hero records use the manuscript's hyphen-minus for negatives and empty cells.
- Art: every placed raster is 300 ppi or more at its placed size; `tools/check_art_ppi.py` gates each release PDF.

### Design review polish and publisher device - 2026-10-30

Owner instructions: "Fix all the issues and add all the polish in the rc522 design review" and "Also incorporate the attached image in the colophon as the Escutcheon Press company logo. We could also put the logo on the back cover." Layout and front matter only; no manuscript text changed.

- Justification: interword spacing may stretch to 140% and shrink to 85% of normal, with letter spacing adjusted by at most 2% either way, before Typst accepts a loose line. The wider range lets the paragraph builder choose better breaks; book-wide loose lines (a gap over 1.6 times the line's normal space) fell from 430 to 83, and the book is 9 pages shorter.
- Chapter openers: a short opening flavour that shares its page with nothing else (the first section starts on a fresh page, or the opener page holds no section heading) is optically centred, with slightly more space below than above. Openers followed by their first section on the same page keep the top-aligned layout; opener spreads stay as they were.
- Publisher device: the owner's Escutcheon Press logo is set as ink on the paper (`tools/brand_ink.py` lifts the scanned paper to transparency and keeps the engraved ink). It sits at the foot of the title page (0.95 in, above the version line, in place of the publisher line), heads the colophon (1.3 in), and replaces the castle mark and publisher line at the foot of the back cover (1.15 in). The castle mark stays the book's own device at the head of the title page and on the player aids and Hero records.

### Section-end fill - 2026-10-30

Owner: keep fresh section pages and whole Monster entries, and fill the white space with art, diagrams, and figures.

- Figures: twenty full-width rules figures close short sections in Chapters 1 to 7, each sized to the space the section's last page leaves (BOOK_DESIGN_PLAN rule 9).
- `endart`: approved art set below a unit's text only where the next heading already starts a later page; it scales to the space and is omitted below 1.6 in, so it never moves text. Basic Mode Hero portraits use it now; the 47 queued tailpieces will use it once approved.
- Figure numbers print in book order.

## 2026-11-01: the design audit

The audit and plan are in `docs/history/Design audit and production plan.md`. The plan's adoption record and its adoption steps (section 10), and the refinement's implementation record:

**Adoption record, 2026-11-01 (design audit, owner approval "Approve everything"):** section heads span the frame; subsection 13 pt and minor 13 pt; the reference band heads Appendix C; bracketed roles and kickers are banner tags; the source's horizontal rules are quiet separators; the first numbered section may share the opener page; Appendix C runs on; tailpieces grow to their gap and sit at the foot; the thumb tab wears a paper halo; the opener label reads "Chapter One"; the version line is serif small caps. Still not adopted (remaining work): the power and item entry grammar (6.13, 6.14), the scenario setup dossier and outcome frame (6.16), the numbered procedure shields (6.9), the gazetteer head (6.11), and the character-entry head (6.12); the book sets those structures as run-in labels and headings. The rationale and evidence are in `docs/history/Design audit and production plan.md` and `docs/DESIGN_REFINEMENT.md`.

The generator (`tools/build_book.py`) already emits semantic component calls (`chapter-opener`, `htable`, `statstrip`, `statcard`, `cards`, `example`, `note-box`, `figure-block`, `spotart`, `flavour`). Adoption is mostly a reskin of those components, plus a few new wrappers that group entries the generator already recognizes.

1. **Tokens and furniture:**
   - Add IM FELL to the font set (done: `fonts/static/IMFe*.ttf`, `fonts/licences/OFL-imfell.txt`).
   - Port the geometry, running heads, folios and thumb tabs into `heraldry.typ`.
   - Record the v2 tokens in `config/design_tokens.json`.
2. **Reskin existing components** with the v2 versions from `system.typ`. Signatures are kept, and the pagination machinery (`pm`, `bal`, `keeppage`, `munit`, `tmark`) is untouched:
   - `chapter-opener`;
   - section headings (level 2);
   - `htable` (black header grammar, roll and spanning-row options);
   - `statstrip` (stat bar);
   - `statcard`;
   - `example`;
   - `note-box`;
   - `figure-block` (caption bar).
3. **New wrappers in the generator.** The source structures are already detected for keeps; the wrappers change presentation only:
   - `monster` entry grouping and portrait lookup by ART ID;
   - `character-entry`;
   - `power` entry parsing of "Name **[cost]**" lines;
   - `gazetteer`;
   - scenario dossier grouping of the labelled setup fields;
   - the contents and index renderers.
4. **Gates** (all existing):
   - reconciliation (every word and cell);
   - the mandatory one-page-unit audit;
   - layout QA;
   - visual review of every page type at readable size;
   - specimen pages are re-rendered at each step.
5. **Release:** `make clean all verify package` and the visual ledger, as BUILD.md describes.

### Design audit implementation - 2026-11-01

Owner instruction on the design audit and plan (`docs/history/Design audit and production plan.md`): "Approve everything." Layout, furniture, tooling, and export changes only; no manuscript text, illustration, or rules change. The tokens in `config/design_tokens.json` carry every value.

- **Section heads span the frame (D-01).** The composer emits every numbered section head (manuscript H3) as a full-width opening part: inside a page-fit unit as its first part, otherwise in the outer flow ahead of the columns, sticky to them (`section-head`). The shield, the 21 pt title, and the brush rule now run across the 525 pt frame, and the two columns start together beneath it.
- **Hierarchy (D-04).** Subsections 13 pt serif bold with 10 pt above; minor headings 13 pt Grenze Gotisch. The lower rank no longer reads larger than its parent.
- **Opener composition (D-02 b).** After a chapter's introduction, the first numbered section starts on the opener page when the measured opener and introduction leave more than 35% of the frame free (the illustrated openers leave 36 to 42%), otherwise on a fresh page as before, with the opener centred. The composer decides this from the measurement pass, never from a position read during layout, which Typst's introspection could not stabilise. The shared section's first column segment flows naturally instead of as a balanced grid (the grid's fixed height is decided from a position that lags one iteration, and its fixed point put the whole of 5.1 on the page after the Chapter 5 opener while the flow fits), and the opener's centring is decided from the actual layout (`intro-end(solo: "auto")`), so an opener never prints top-aligned above an empty half page. The refinement policy table already allowed "the chapter opener plus first section as one opening composition"; this makes it the rule.
- **Appendix C runs on (D-02 c).** Reference sections no longer start a fresh page each (`layout.run_on_chapters`). A fit-capable section is still one unbreakable page unit and moves whole when it does not fit. An over-height section that opens with a short introduction (at most 800 characters) opens as one unbreakable, sticky full-width composition: the reference band and the introduction set as a standfirst at the opener's measure (`full-opening`). It runs on only when the piece after the introduction is prose or a measured unit no taller than half a frame, which always fits under a fresh-page opening; being sticky (run-on openings only; ordinary section openings keep their place, since moving them cost four pages in a local proof), the opening moves with its columns when they cannot start on the page, so it never strands at a page foot. A taller first unit, or a section that opens with a table or list, starts a fresh page (with the same opening when it has an introduction). Measured in the first local build: a sticky band followed by a column segment with 66 to 102 pt of room left the band at the page foot and ran the introduction off the frame (page 602), and Typst's `layout` callback reports the full region height rather than the remaining room, so no in-layout guard can decide this.
- **Marker-only tails.** A unit that ends in a full-width element leaves only zero-size end markers to flush; emitted inside a column segment or any block wrapper after an element that fills the page, they opened a blank page before the next fresh start (pages 24 and 53 of the first local build). The composer now emits them as raw markers, which attach to the page they follow.
- **Tail pull-back (D-02 d).** A last page shorter than 250 pt (was 180 pt) pulls back the previous piece.
- **Tailpieces (D-02 f and g).** A tailpiece grows to the gap it closes, up to its 300 ppi maximum and a 4.6 in cap, and sits at the foot of the frame when more than 60 pt would otherwise be left beneath it. Hero portraits keep their family width. Known limit: a tailpiece needs a full-width band at the foot of its section's last page; where the new composition leaves that page with a full left column and a short right column (8.4 Divine Prayers) or under 1.6 in of band (2.1 Core Terms, 7.17 Permanent Special Items), the piece is omitted rather than moving text, so 44 of the 47 print in the candidate of 2026-11-01 against 47 in RC527-build-40. Column-aware placement of a tailpiece in a short right column is a follow-up.
- **Reference band and role tags (D-06).** Appendix C heads are set as the iron reference band of BOOK_DESIGN_PLAN 6.19. A bracketed role or kicker closing an entry heading ("[Elite]", "[2/5 Complexity]", "[Intro]") is set as the banner tag; the brackets stay in the text layer as transparent glyphs inside the tag and the role is small caps, so the extracted heading still reads exactly as the source.
- **Quiet separator (D-03).** The source's horizontal rules are a short hairline with a lozenge; the castle flourish stays at chapter and front-matter boundaries, so an ordinary page carries at most two marks.
- **Furniture (D-05, D-09, D-10).** The thumb tab wears a paper halo so the opener frame never runs into it; the opener label reads "Chapter One" with the source's "1." kept as transparent glyphs on the same line; the version line on the title page and back cover is serif small caps; the back-cover facts are ragged left in a 4.8 in measure under a short brush.
- **Tables (D-08).** The identity line stays hidden when the visible heading names the table across a short run-in label such as "APL 1–2 (d10)".
- **Tokens (D-07).** Inks, tints, rule weights, the remaining type sizes, the ornament budget, the tailpiece limits, and the composition policy are tokens; Typst reads them, and the specimen components use the same values.
- **Production (P-03, P-04).** `tools/digital_compact.py` writes `Heraldry_RC###_digital-compact.pdf`, the screen companion with rasters at 150 ppi (skipped by the 300 ppi gate by name); the density diagnostic no longer counts the thumb tab as content and reports sparse pages by chapter.

The book has since become digital-only, which retires P-01 (printing and binding) and the P-02 calibration samples.

## 2026-11-02: digital only, and review by the maker

- **Digital only.** The owner removed every workflow and reference to InDesign and to physical printing (`production/STATE.md`, 2026-11-02). That retired the audit's P-01 (printing and binding) and P-02 (calibration samples), the cream and white print editions, the calibration sheet, and the print checks. The old design files' print-era guidance is not carried into `docs/DESIGN.md`.
- **Review.** The independent-review rule was removed the same day: whoever makes a piece of work may review and approve it after looking at it. The plan's status line had said that "independent visual review" remained mandatory; that clause is dropped.
- **References.** The tracked `references/` folder, with its manifests, was deleted. The ten books are now cited only as the owner's reference books.

## 2026-11-03: the merge

The three files were merged into `docs/DESIGN.md`. Where they disagreed with each other, or with `config/design_tokens.json` and the Typst source, the merge kept the value below and why.

| Topic | The old files said | Kept |
|---|---|---|
| Version name | "design system v2, 'Ink and Iron'" (spec), "v4 'Grim Heraldry'" (Typst headers), "compact design system v5" (plan) | "Grim Heraldry" (compact design system v5), the plan's name |
| Justification | Word space 90 to 140%, letter spacing −0.5 to +2% (plan 3 and 13) | 85 to 140% and ±2%, as Typst sets it and the 2026-10-30 polish recorded |
| Hyphenation | "Discouraged but allowed" (plan 3) | Normal cost, 100% (Typst; the plan's rule 1 already said so) |
| Column width in rule 1 | 3.48 in | 254.4 pt (tokens) |
| Chapter lead | 12.4 pt IM FELL (plan 6.5) | 10.5 pt: Typst sets all flavour at the body size, as plan 3 says |
| Chapter art size | Full frame width and about 45% of the page (plan 6.5 and 7); about a third (refinement); about two fifths (spec) | The family print width, at most 84% of the frame and native 300 ppi (Typst); target at most two fifths (`art.chapter_opening_target_max_area_fraction`) |
| Art-light opener drop | 1.2 in (plan 6.5 and 11) | 0.9 in (Typst) |
| Thumb tab | 0.32 in wide; keyword auto-fitted up to 12 pt (plan 5) | 39 pt wide (the outer margin less the 3 pt clearance) and a fixed 9 pt keyword (Typst; plan 3 already said 9 pt) |
| Running heads | Also suppressed on scenario openers (plan 5) | Suppressed on chapter openers, the index opener, and front matter only (Typst) |
| Contents | Arms 22 pt; sans section numbers (plan 5 and 12) | Arms 20 pt; number and title in the serif (Typst) |
| Index | Grey page numbers; engraved letter blocks (plan 5) | Plain numbers and a plain black letter block in the book; the specimen shows the grey, engraved version |
| Stat-bar values | 11.5 pt (plan 6.15) | 12 pt (`type_pt.stat_value`) |
| Appendix C tables | 8.8 pt (plan 6.10 family table) | 9 pt (plan 6.19; the 9 pt floor; Typst) |
| Example panel | 5.5% tint, 2.4 pt spine, an EXAMPLE tag (plan 6.7) | 5% tint and 2.6 pt spine (tokens); the book leads with the source's own bold label, and the tag is specimen-only |
| Scenario dossier | A 5.5% panel under a 1.5 pt rule (plan 6.16) | A 5% panel with corner flourishes (the specimen in Typst) |
| Figure caption band | Number and title in reversed capitals, closed by a hairline (plan 6.8) | The book's band carries the printed number only, and the caption closes with a 0.6 pt rule (Typst, `line_pt.figure_close`); the title in the band is specimen-only |
| Place names | 28 pt (plan 3 and 6.11) | 30 pt (the gazetteer specimen in Typst) |
| Gazetteer lore | Source Serif 4 Italic in a 78% measure (plan 6.11) | IM FELL roman as a lead block (plan 3's one flavour treatment; the specimen), with rule 12a's balanced columns for lore too long for a lead block |
| Scenario flavour | "Display italic" (plan 6.16) | IM FELL roman lead block (plan 3) |
| Monster portrait | A fixed 2.55 in box (plan 6.15 and 7) | The specimen's box is 2.5 in (Typst); the book places the portrait at the monster family width above the flavour |
| Scenario art | 1.7 in at the right of the head (plan 6.16 and 7) | The specimen centres it above the title; the book places it at the scenario family width above the flavour |
| Hero portraits | 2.15 in, backgrounds 1.6 in (plan 7) | Kept as the specimen's character-entry design; the book uses the family widths in `config/art_style.json` |
| Title page | 72 pt blackletter "Heraldry", 30 pt "Skirmish", a strapline, ART-COVER-002 at full frame width, a release line (plan 6.2) | The page Typst sets: castle logo, serif title, IM FELL subtitle, byline, device, and version (refinement, 2026-10-29 and 2026-10-30) |
| Colophon | Sans 8.5 pt, three typefaces, an art provenance statement (plan 6.3) | 9 pt, four typefaces, no illustration credit or provenance line (Typst; `editorial/how_to_use.json`; owner, 2026-10-29) |
| Back cover | A flourish, an italic line from the opening, one creature vignette, and the wordmark (plan 6.1); a 4.8 in blurb (refinement, 2026-10-29) | The blurb in a 5.2 in measure, the party scene, the facts in a 4.8 in measure, and the device (Typst; refinement, 2026-11-01, D-10) |
| Opener spread | The introduction on "the facing page" (refinement, 2026-10-29) | "The next page": chapters start on either side, so it faces the display page only when the display is a verso |
| Reversed labels | At least 6.6 pt (plan 12, restraint rule 4) | The 9 pt floor (plan 3; `type_pt.minimum_essential`) |
| Minor headings | Body-sized bold (spec 3); "nested headings remain serif" (refinement); 14.5 pt blackletter (plan, before 2026-11-01) | 13 pt Grenze Gotisch (tokens; audit D-04) |
| Display lettering | Only on chapter and major titles (spec 10) | The plan's roles, which superseded the spec's visual identity on 2026-10-12 |
| Black header bands | Reserved for selected components (spec 5); dark headers for small tables only (refinement) | Every table, with a light body (plan 6.10, owner 2026-10-12) |
| Table rules and bands | Start at 0.5 to 0.7 pt rules and about 6% bands (spec 5) | 0.35 pt hairlines at 24% and 5% bands (tokens) |
| Other starting values | Example 10 to 10.5 pt; captions 9 to 10 pt; index serif or sans, two or three columns (spec 3) | 10.5 pt; 9 pt; sans 9.5 pt in three columns |
| Ornament motif | One broken-ring and tapered-rule motif (spec 7; `VISUAL_QA.md`) | The armoury of plan 12 (castle logo, arms, and shields), approved 2026-10-13 |
| Section page starts | Every numbered section on a fresh page (plan 6.6 and rule 8; refinement policy and 2026-10-29) | Fresh pages, except the first section sharing the opener page and Appendix C running on (2026-11-01) |
| Navigation rail | "Avoid a permanent navigation rail" (spec 2) | No rail or sidebar column in the text frame; the approved thumb tabs live in the margin |
| Specimen numbers | Gazetteer 11, reference 12, index 13, back cover 14 (plan 6) | 10b, 11, 12, and 13, as `typst/templates/specimens.typ` numbers them |

Two other moves in the merge:

- The one-page keep rule, with its measurement and audit, is stated once in `docs/PROJECT_CONTRACT.md` ("Pagination: the one-page keep rule"). `docs/DESIGN.md` 8.4 adds only how the composer applies it, and the owner's original 2026-10-07 wording is quoted above.
- The old files told agents to record each adopted reference lesson and frozen token change in `production/design-decisions.md`. That log moved to `docs/history/design-decisions.md` the same day as a closed record, so new lessons are recorded in the section of `docs/DESIGN.md` they change and noted in `production/STATE.md`.
