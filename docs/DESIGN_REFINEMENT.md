# Design refinement — owner request, 2026-10-07

Status: standing refinement requirements with the approved compact implementation in progress. No new release is implied. This document overrides the old specimen freeze where they conflict. Resolve the active manuscript through `source/versions.json` and preserve its bytes. Work on main and retain all existing figures and content checks. Read REFERENCE_ANALYSIS.md, DESIGN_SPEC.md and VISUAL_QA.md with this brief.

## Compact profile approval - 2026-10-16; implementation resumed 2026-10-20

The owner approved the complete layout review and explicitly authorized 10.5 pt body text, 9 pt tables, narrower margins, and more assertive refinement. This supersedes earlier 11 pt and unchanged-margin trial proposals. Use the effective profile in `config/design_tokens.json` through Typst and `tools/layout_profile.py`; the production format record is a checked mirror. Four font roles remain intentional. Ordinary rules use two columns; opening flavour uses a distinct inset single-column region. Preserve manuscript bytes, complete fit-capable units, source order, all source-bound figures, deliberate wide objects, and the accepted blank verso.

Measured furniture safety takes priority over the smallest margin: the initial outside 36 pt/top 40.5 pt/bottom 40.5 pt trial left rotated navigation, running heads, and folios outside the 27 pt safe line. The corrected profile is inside/outside/top/bottom 45/42/45/45 pt, with a 16.2 pt column gap. A physical binding/device/media proof remains NOT TESTED. Page savings and full-book acceptance must come from the actual same-source builds and their recorded review, not these token changes alone.

## Historical evidence and diagnosis - 2026-10-07

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

## Page treatments to implement

Retain portrait Letter, flat #FCFAF5 cream/white companions, safe margins, four intentional licensed font roles and readable body/table sizes. Distinguish pages through information architecture and composition, not more texture or decorative borders.

1. Chapter opener: one source-specific horizontal ink scene, substantial title with clear chapter number, short lead and a clean transition into rules. Target roughly one third of the page for art when available. Make the scene asymmetrical and leave useful negative space. No generic hooded skull repeated eleven times. Use ART_MANIFEST subject plans and check each against current source lore.
2. Ordinary rules: calm two-column prose with clearly different major, subsection and run-in treatments. Use larger major headings when full width allows them; nested headings remain serif. Keep existing emphasis rather than making all text heavier. Use a consistent rhythm of spacing and a small number of horizontal rules.
3. Examples: source example label and modest inset/left rule or light grayscale field, attached to the relevant procedure. Use the clarity of Hametsu's dedicated examples without its dark sidebar or narrow permanent third column.
4. Tables: family-specific widths and alignment, strong header separation, generous descriptive column and restrained alternating bands. Selective dark header treatment may help a small lookup table, but large tables remain light. Every continuation repeats the correct column headers and identifies its source table.
5. Reference entries: stable title → source metadata/stat strip → description → abilities/procedure anatomy. Short entries stay together when they fit; long entries continue with a repeated identifying name. Separate neighbouring entries through spacing and a fine rule, not a box around every paragraph.
6. Scenarios: fresh page at each named scenario; clear scenario title and source flavour; canonical setup fields in a predictable arrangement; deployment map beside or directly after its setup. Continue into special rules, scoring and aftermath using the exact source headings. A multi-page scenario is acceptable; a split opening with detached deployment instructions is not.
7. Atmospheric spot art: after the twelve required masters are complete, add a bounded set of source-specific creatures, equipment or architecture at natural transitions after review of the required suite. Use rectangular/open placements with clean negative space, never text over artwork or art filling a known pagination defect. Keep deployment figures as precise editable vectors.

## Pagination policy

The owner's objective is coherent sections, with breaks before significant new headings. Implement the following defaults in renderer/style metadata, never by inserting blank lines or rewriting the immutable manuscript.

| Content | Default |
|---|---|
| Chapter/appendix | Fresh page, no forced blank verso |
| Major numbered section (source ### / Typst level2) | Fresh page; suppress a redundant break when already at page top; preserve the chapter opener plus first section as one opening composition |
| Named scenario, including those represented by a bold-only paragraph | Fresh page through a stable semantic scenario target, regardless of Markdown depth |
| Nested subsection/minor heading | Keep heading with meaningful opening content; move a short complete subsection to the next column/page when it fits there |
| Heading followed by prose | Keep at least three body lines, or the whole short opening paragraph, with the heading |
| Heading followed by list/procedure | Keep two complete short items, or the first substantive step if steps are lengthy; do not strand a step label |
| Short table/stat profile | Keep caption/header/rows/necessary note together if the measured unit fits an empty destination column/page |
| Long table | Split at row or logical group boundaries; repeat headers and identifying continuation label; avoid an isolated first/last row where feasible |
| Figure | Keep graphic, legend and caption together; keep deployment figure with the relevant setup rather than an unrelated later scenario |

Do not force every minor heading to a fresh page: it would fragment the reference material and inflate the print stack. Body paragraphs should retain natural flow with a two-line start/end target for widows/orphans. Fit-capable sections, scenarios, tables and entries are mandatory one-page keeps; genuinely over-height parents continue without breaking fit-capable children. A unit taller than the available frame must have a documented continuation path. Do not shrink essential type below 9 pt, omit content, clip a frame or use a landscape fallback.

In two-column material, a page break must occur at the outer page flow, after flushing the prior segment. Do not assume a break inside a nested columns block is equivalent to starting a fresh page. Add the policy before the existing balancer; its split candidates must respect semantic keep groups. Measure a short subsection as a complete unit at the approved destination width; allow approved full-width placement when a column is too narrow; do not split its heading, lead, table or first list group into unrelated balancing pieces. Use stable heading/block/table IDs for exceptions, not frozen PDF page numbers.

For tables, measure the actual Typst content at the selected width, including header, cell inset, wrapper spacing, caption and necessary note. Use an unbreakable wrapper only when that complete unit fits an empty frame. Preserve breakable rows/entries only for exceptional over-height content with a faithful documented representation. Estimated height from character counts is useful for choosing widths, but is not the final pagination decision. Add a modest fitting tolerance; never hide overflow with clipping. Repeated headers must be included in reconciliation's permitted repetition accounting.

Avoid a sequence of tiny two-column fragments around full-width tables. Recompose the section opener or use a sustained full-width procedure/reference region when that makes the reading path clearer. Complete the previous section before starting the next; do not place unrelated prose into a blank area simply to fill it. Deliberate whitespace from a section start is acceptable; unexplained interior voids caused by a failed balancing choice need repair.

## Acceptance and execution

First render an actual-content stress specimen covering opener, ordinary facing pages, nested short subsection, example, T004, long repeated-header table, transformed entry, monster and the Whispering Grove setup, plus C.5 reactions. Include the preceding/following pages for each pagination case. Compare before/after at readable size; freeze refined tokens only after these cases work. A specimen is a milestone, then apply the components across the entire book.

Extend the layout audit to record semantic heading starts and their following content, page/column breaks inside short fit-capable tables/subsections, continuation titles/headers, figure/setup distance, row orphans, and unexplained large voids. Persist findings and reviewed exceptions by stable source IDs and current hashes. Hard failures: stranded headings/captions, missing repeat headers, avoidable split of a fit-capable short table, content overlap/overflow, missing or duplicate text/cells. Subjective whitespace flags need actual inspection, not a universal ban on blank space. Caption and entry-name continuations are publication furniture, not manuscript patches.

Inspect all revised pages at contact-sheet scale for rhythm, every continuation/table exception and all scenario openings at readable size, then the cream/white pairing and overscan crops. Reconcile all text/cells, rebuild navigation and package from the same final input hashes. Record the current design outcome separately from historical geometry PASS. Physical printer proof remains NOT TESTED.


## Optional InDesign export - separate owner-invoked workflow

The earlier hold was superseded by the owner's explicit 2026-10-15 InDesign request. The optional export now follows `docs/INDESIGN_EXPORT.md`; it remains separate from ordinary development, this PDF refinement, and the candidate/release chain. Do not invoke it automatically. Native composition, native visual review, and physical proof require their own evidence and cannot be inferred from a structural IDML check.

## Sources consulted 2026-10-07

These support the pagination/API/export methods. Numerical keep thresholds and Heraldry component choices above are our production decisions, not standards mandated by the sources.

- Butterick, headings and keeps: https://practicaltypography.com/keep-with-next-paragraph.html
- Butterick, style-based page starts: https://practicaltypography.com/page-break-before.html
- Butterick, widow/orphan tradeoffs: https://practicaltypography.com/widow-and-orphan-control.html
- Adobe, paragraph keep options: https://helpx.adobe.com/incopy/desktop/format-text/paragraph-formatting/formatting-paragraphs.html
- Adobe, table rows/headers across frames: https://helpx.adobe.com/ca/indesign/desktop/add-tables-and-data/format-tables/break-tables-across-frames.html
- Typst, sticky/unbreakable blocks: https://typst.app/docs/reference/layout/block/
- Typst, table continuations: https://typst.app/docs/guides/tables/

## Owner clarification: mandatory one-page units — 2026-10-07 UTC

**Mandatory one-page keeps:** Every complete scenario, section/subsection, table, example, procedure, stat profile or reference entry that fits within one empty usable page at its approved layout width must occupy exactly one physical page. Include its heading, all nested content belonging to that unit, caption, legend/deployment diagram and necessary notes in the measured group. If insufficient space remains, move the entire unit to the next page; do not split it across pages merely to fill space or balance columns. A column limitation is not proof that a unit cannot fit a page: use the approved full-width layout where appropriate. Preserve legible type, spacing and all content.

Measure rendered height, not manuscript length or character counts. A section extends from its heading to the next heading of equal or higher rank; a scenario extends to the next scenario or enclosing-section boundary. Nested fit-capable groups remain protected inside longer parents. Fit uses the empty usable content frame, after margins, running furniture and required spacing, with a small conservative tolerance. Test both facing-page positions and cream/white exports. Artwork must not displace or fragment a fit-capable rules unit; reposition decorative art instead.

Only genuinely over-height units may continue to another page, with repeat table headers or identifying continuation and intact smaller child units. Record their source IDs, measured dimensions and reason. Never shrink type, omit notes/maps, clip content or artificially enlarge a unit to evade the keep rule. Intentional whitespace left by moving a complete unit is acceptable.

Required release evidence: a current input/PDF-hash-bound audit covering every applicable stable source ID, its measured height and frame width/height, fit classification and actual PDF page set. Any fit-capable unit appearing on more than one page is a hard failure; missing audit coverage also fails the gate. Inspect boundary cases and actual pages, not just metadata. Implement this check in the renderer/layout audit and mandatory verification gate before the next illustrated release.
