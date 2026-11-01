# Design audit and production plan: non-illustrative graphic design

Date: 2026-11-01, updated the same day for RC527-build-40 (see the update section). Status: **audit and plan only; no design files changed; nothing built.** The original evidence is RC522-build-39 (618 interior pages, cream PDF SHA-256 `ead73ce9…`), inspected through its committed review images (`production/qa/review/`: 26 all-page contact sheets at 34 dpi, 29 detail pages at 100 dpi, both covers, calibration), its QA ledgers (`production/qa/*.json`), and the current source files (RC527 manuscript, `typst/`, `tools/`, `config/`). Limits: no local PDF was built, art masters are Git LFS stubs in this container, and the review images are not glyph-level evidence. Physical printing remains NOT TESTED.

Scope follows the owner brief: typography, grid, layout, hierarchy, spacing, contrast, tables, stat blocks, figures and captions, callouts, headers and footers, page furniture, contents and index, cross-references, consistency, and print and digital production. Illustrations, lore, prose, and rules are out of scope and untouched.

---

## Update 2026-11-01: RC527-build-40 (the tailpiece build)

The owner built and released RC527-build-40 (618 pages, cream PDF SHA-256 `88942e53…`) with all 47 section-end tailpieces placed. Two composer fixes went in with it: end art now also follows one-column units, and a wide piece whose full height is under the 1.6 in minimum prints at full size. The new release's review images and ledgers were pulled and compared page by page with RC522-build-39.

**What improved.** 51 pages changed their vertical fill by five points or more; on the 47 tailpiece pages the average fill rose from 51% to 70%, and every numbered section in Chapters 1 to 11 now closes on a relevant image. The count of non-opener pages under 55% vertical fill fell from 77 to 62. Text did not move, so every other finding in this report stands unchanged.

**What did not.** The tailpieces are placed at their family print width (`config/art_style.json`: world 3.3 in, item and tradition 2.6 in, and so on), while the approved masters are 1536 × 1024 px, which allows about 5.1 in at 300 ppi. The width cap is therefore a family setting, not the resolution floor, and on a page that was mostly empty a 2.6 in vignette fills about a third of the gap. Sixteen tailpiece pages are still under 62% vertical fill: 26, 53, 94, 111, 112, 135, 146, 201, 222, 228, 243, 244, 355, 363, 489, 510. Pages 222 (Divine Prayers), 243 (9.2), 355 (Reading a Scenario), and 112 (Random Class Table) remain more than half empty. The art also sits directly under the last line with a 16 pt gap, so the remaining white space collects at the foot of the page rather than framing the piece.

**Revised recommendations for D-02 (added as items f and g, both within the keep contract and without new art):**

- **D-02 f, size tailpieces to the gap.** In `load_end_art` and `endart`, pass the art's 300 ppi maximum width alongside the family width, and let the piece grow to the lesser of the 300 ppi maximum, a design cap of about 4.6 in (63% of the frame), and the height left on the page. `tools/check_art_ppi.py` already gates every raster at 300 ppi or more, so the floor is enforced automatically. Small gaps keep the family width; large gaps get a full tailpiece.
- **D-02 g, anchor tailpieces to the foot.** When the gap is taller than the piece plus a page's worth of breathing room (about 60 pt), place the tailpiece at the foot of the text frame instead of under the last line, so the page reads as text, air, tailpiece: the traditional book composition. The zero-height probe in `endart` already knows the remaining height; this is a placement change only.
- Keep D-02 a to e as written. Items b and c (opener composition and Appendix C run-on) still need the owner's decision and remain the only way to recover the pages that have no tailpiece: the stranded-introduction pages (147, 153, 163) and the short Appendix C sections.

**Other changes in this build.** The digital PDF grew from 157 MB to 177 MB with the 47 new rasters, which raises the priority of P-03. `production/RELEASE_STATUS.md` still carries the heading "RC527 source / RC522-build-39 delivery" although the README and `dist/RELEASE.json` record RC527-build-40; that is a ledger inconsistency for the next status update, not a design issue.

---

## Implementation record 2026-11-01 (owner: "Approve everything")

Everything in Phases 0 to 2 was implemented in one pass, then built and inspected locally six times and once as a GitHub candidate; the evidence is the local proof (625 interior pages) and the composition gates. Items marked "follow-up" are open.

| Item | Done | Where | Notes |
|---|---|---|---|
| P-04 density metric and sparse-page report | yes | `tools/layout_diagnostics.py`, `tools/layout_qa.py` | Drawings count as content only when at least half their width lies inside the frame; `sparse_pages` by chapter in `production/qa/layout.json`; the near-empty detector's strip is the outer margin plus the tab halo and its line filter overlaps the frame instead of requiring an inset start |
| D-07 tokens and one component source | yes | `config/design_tokens.json`, `typst/templates/system.typ`, `typst/heraldry.typ`, `typst/frontmatter.typ` | Inks, tints, rule weights, the remaining sizes, ornament budget, tailpiece limits, and the composition policy are tokens; the specimen components read them. The specimens, aids, and Hero records still import `system.typ`, which now shares the book's values (full unification is a follow-up) |
| D-03 quiet separator | yes | `heraldry.typ hr-ornament` | Hairline and lozenge at 40% of the measure; the castle flourish stays at chapter and front-matter boundaries |
| D-05 tab halo | yes | `system.typ thumb-tab` | 3 pt paper halo (token `ornament.tab_halo_pt`) |
| D-08 identity dedupe across a run-in label | yes | `build_book.py chapter_items` | |
| D-09 "Chapter One" | yes | `heraldry.typ opener-display` | The source token "1." stays in the text layer as transparent glyphs |
| D-10 version line and back-cover facts | yes | `frontmatter.typ`, `cover.typ` | Serif small caps; facts ragged left in a 4.8 in measure under a short brush |
| P-02 calibration samples | yes | `calibration.typ` | Tinted hairlines at 24, 30, and 40% and the 5, 6, 9, and 12% tints |
| P-03 screen companion | yes | `tools/digital_compact.py`, `Makefile`, `tools/provenance.py`, `tools/check_art_ppi.py`, print instructions | 175 MB to 62 MB at 150 ppi; pages, bookmarks, links, and attachments verified equal |
| D-01 full-width section heads | yes | `build_book.py flat_parts/emit_x`, `heraldry.typ section-head` | A page-fit section carries the head as its first full-width part; an over-height section emits it in the outer flow, sticky to its columns; a column-fit section becomes a page unit so its head still spans |
| D-04 hierarchy | yes | tokens `type_pt.subsection 13`, `type_pt.minor 13` | |
| D-02 b opener sharing | yes | `build_book.py opener_shares`, `heraldry.typ opener-body` | Measured in the measurement pass (probe `opener:<chapter>`); shares when more than 35% of the frame is free and a page-fit first section fits (Chapters 2 and 4 and Appendix C in the proof) |
| D-02 c Appendix C runs on | yes | tokens `layout.run_on_chapters`, `build_book.py` | Page-fit sections move whole; an over-height section opens as a sticky band plus standfirst and runs on when the next piece is prose or a unit no taller than half a frame; otherwise it starts a fresh page |
| D-02 d tail pull-back | yes | token `layout.tiny_tail_pt 250` | |
| D-02 f and g tailpieces | yes | `build_book.py load_end_art`, `heraldry.typ endart` | Grow to the gap up to the 300 ppi maximum and 4.6 in; foot-anchored when more than 60 pt would remain beneath |
| D-06 reference band and role tags | yes | `heraldry.typ` level-2 and level-3/4 show rules | Brackets kept as transparent glyphs in the text layer |
| D-02 a end art on tails without a tailpiece, D-11 mini contents, D-12 side-by-side portraits, D-06 steps 3 and 4 (item and power name line, scenario dossier), P-01 physical proof | follow-up | | Need art, an owner choice, or a physical print |

**Faults found in the local proofs and fixed.** A unit ending in a full-width element flushed only zero-size end markers; any block wrapper after a page-filling element opened a blank page (pages 24 and 53 of the first proof), so the composer now emits such markers raw. A run-on reference head followed by a column segment with 66 to 102 pt of room ran its introduction off the frame (page 602); the band-plus-standfirst opening replaced the position probe, which Typst could not converge, and Typst's `layout` callback reports the full region height rather than the remaining room, so no in-layout guard can decide such cases. The keep audit now sets the opener probes aside before its source-coverage check. The first GitHub candidate showed the Chapter 5 opener top-aligned above an empty half page (Typst's balanced grid moved 5.1 to the next page although the flow fits): a shared first section's first segment now flows naturally and the opener centres itself from the actual layout. Three tailpieces (2.1, 7.17, 8.4) are omitted because their sections' last pages no longer leave a 1.6 in full-width band; column-aware placement is a follow-up.

**Measured outcome of the local proof.** 625 pages (618 before): full-width heads cost about a head's height of column text per section start; opener sharing and the run-on appendix give some back. Sparse pages by the corrected metric: 73, all in the documented categories (scenario and section tails, introductions before full-page tables, short Learn-to-Play and Basic Mode sections on fresh pages, Chapter 6 portrait pages); none new. Gates: keep audit 0 avoidable splits with full coverage, layout detectors clean after the filter fix, tables 333/333, cross-references and index unchanged. The candidate build and all-page review follow through the repository's release chain.

---

## 1. Pipeline reconnaissance

| Stage | What it is | Evidence |
|---|---|---|
| Source | One immutable Markdown snapshot per revision; active RC527 (1.54 MB, 18,549 lines, 254k words). 846 headings (1 title, 15 chapter, 134 section, 415 subsection, 281 minor), 333 tables (max 12 columns), 4,393 list items, 24,741 bold runs, 42 horizontal rules. | `source/versions.json`, `source/Heraldry_RC527.md`, `production/inventory/summary.json` |
| Parse | markdown-it-py to a block model with stable ids (`B00001`, `h-…`); index targets; cover data. | `tools/parse_source.py`, `tools/make_index.py`, `tools/build_extras.py` |
| Compose | `tools/build_book.py` (69 KB) walks chapters, classifies every unit as keep-col, keep-page, or over-height from measured Typst heights (`munit`), chooses table representation and widths (`tools/tables.py`: cell-aware allocator, families per H3), balances two-column tails (`bal`, `flowtail`), and emits `typst/content.typ` (generated, not committed). Eight layout passes for convergence, then white and digital variants. | `tools/build_book.py` lines 318–1120, `tools/tables.py`, `tools/measure_units.py` |
| Templates | `typst/heraldry.typ` (book: furniture, headings, components, pagination machinery), `typst/templates/system.typ` (design system v4/v5 used by specimens, player aids, and Hero records; partly adopted by the book), `typst/frontmatter.typ`, `typst/cover.typ`, `typst/calibration.typ`, `typst/aids/`, `typst/heroes/`. | file list above |
| Tokens | `config/design_tokens.json` v2 is the sole geometry, type, and spacing authority; mirrored in `config/production.json`; validated by `tools/layout_profile.py`. Colours, ornament sizes, and several type sizes are not tokenized (see D-07). | `config/design_tokens.json` |
| Fonts | Source Serif 4, Source Sans 3, Grenze Gotisch, IM FELL English (OFL, licences bundled); Cinzel still shipped but retired. | `fonts/static/`, `fonts/licences/` |
| Marks | Fifteen chapter arms, coin, logo, as SVG per substrate. | `typst/templates/marks/{cream,white}/` |
| Figures | 77 deterministic SVGs (19 rules diagrams, 38 maps, 20 section-end figures), placements by block id, semantic review ledger. | `figures/out/`, `figures/placements.json` |
| Art | 347 ink derivatives (LFS) placed by catalogue and selection; `endart` fills unit ends; 47 tailpieces queued. | `assets/art/ink/`, `production/art/SPOT_CATALOG.json`, `production/art/SELECTIONS.json` |
| Build | `make clean all verify package`; CI: `build-candidate.yml` (pre-release plus review aids) → hash-bound visual review → `rebuild-delivery.yml` (GitHub Release). Local full run about 13 min with a 12 GB swap file; CI timeout 60 min. Measurement cache in `.cache/layout-measurements/`. | `Makefile`, `.github/workflows/`, `docs/BUILD_AUTOMATION.md`, `production/STATE.md` |
| Gates | `tools/verify.py` mandatory checks: reconciliation (every word and cell), keep audit (2,831 units, 0 avoidable splits), table audit (333/333), page-map accuracy, print geometry (cream and white identical), index (234 entries), cross-references (768 citations, 0 unresolved), figure gate (77/77), inkjet preflight, art ppi, visual-review currency. | `production/qa/STATUS.json` and sibling ledgers |
| Outputs | Cream and white borderless Letter interiors, digital edition with covers and links, cover sheets, calibration sheet, ten player aids, Hero records, specimen, release ZIP. Digital PDF 157 MB, interiors 152 MB (289 rasters at 300 ppi or more). | `dist/RELEASE.json`, `BUILD.md` |

The pipeline is deterministic, reproducible, and heavily gated. Design work therefore happens in exactly three places: `config/design_tokens.json`, the Typst components, and the composer's unit and part logic in `build_book.py`. Everything else follows.

---

## 2. Design audit

### Strengths

- **A real, coherent identity.** Four intentional type roles (serif rules, sans data, blackletter display, IM FELL flavour), black-only ink, engraved shields, brush rules, chapter arms, thumb tabs, and framed openers read as one authored system. The ordinary page (for example detail page 50, 3.2 Initiative Phase) is calm, justified, well hyphenated, and dense without crowding. Loose lines fell from 430 to 83 after the 2026-10-30 justification change.
- **Tables are a genuine ledger grammar.** Black header band with reversed small caps, 9 pt tabular sans, 5% bands, 24% hairlines, no vertical rules, cell-aware width allocation shared across table families, repeated headers with "(continued)", first and last three rows travelling together, and the coin mark for "c". Detail page 144 (four d100 treasure tables) and page 344 (full-width random monster tables) are strong reference pages.
- **Stat blocks and bestiary.** The stat strip (band, 12 pt values, brush close) and the two-creatures-per-page bestiary (page 294) are clear and scannable.
- **Navigation is complete and verified.** Running heads (chapter on verso, section or scenario "(continued)" on recto), shield folios, fifteen-slot thumb tabs, a two-level linked contents with arms, 564 bookmarks, a curated 234-entry index, and 768 resolved cross-references.
- **Pagination integrity.** The mandatory one-page keep contract is enforced by a hash-bound audit; no fit-capable unit splits. Figures weld to their captions; scenario maps sit beside setup text (page 394).
- **Print discipline.** 27 pt safe frame measured by glyph outlines, cream and white variants proven geometrically identical, every raster at 300 ppi or more, a calibration sheet, and honest NOT TESTED status.

### Weaknesses

1. **Section heads are column-width, not full-width.** Every numbered section (all 193 H3 placements: 122 "column", 71 "keep-page") sets its shield, 21 pt blackletter, and brush rule inside the left column, so the right column's body text starts level with, or above, the section rule (pages 50, 100, 25). The design plan (BOOK_DESIGN_PLAN 6.6) specifies a full-width section title. This is the single largest gap between the intended page architecture and the printed one.
2. **Empty space is the book's dominant visual flaw.** Causes, in order: scenario and section tails that overflow by a few lines onto a page that then starts a fresh section (page 444: 14 lines then nothing; page 395); a section introduction stranded alone because its full-page table moves whole to the next page (pages 147, 153, 163, 385); half-empty columns where a column-keep unit did not fit (pages 100, 111, 277); and short appendix sections each on a fresh page (pages 579, 580, 585, 592). The ledger counts 97 pages with at least 250 pt empty at the foot, and that count is a floor because the density metric is truncated by the thumb tab (see P-04). 71 non-opener pages carry fewer than 35 body lines where a full page holds about 96. The owner's keep contract and fresh-page policy are the root; the section-end art program (20 figures placed, 47 tailpieces queued) is the owner's chosen remedy and is in progress. Design can still reduce the waste without touching the contract (see D-02).
3. **Ornament budget is exceeded in Chapter 7.** Each source horizontal rule becomes the brush-castle-brush flourish; thirty of the 42 rules sit in 7.17 Permanent Special Items, so pages 193 to 200 show three or four castle marks each, against the token `maximum_marks_per_ordinary_page: 2`.
4. **Heading hierarchy inverts at the bottom.** Minor headings (manuscript H5) are Grenze Gotisch 14.5 pt and read larger and louder than their parents, the serif bold 12.5 pt subsections (page 494: "Step 3: Journey Home" and "Climate 1: Greenmark Journey Table" sit under 11.2.x).
5. **The thumb tab crosses the opener frame.** The tab occupies 0 to 39 pt from the trim; the frame's double rule sits at 30.2 and 33.7 pt, so the black pennant cuts through the rules and corner flourish on every opener (pages 7, 24, 353).
6. **Planned entry grammars were never adopted.** The specimen system defines the Appendix C reference band, monster role tags, the power and item entry (shield numeral, name, cost tag, field strip), the scenario setup dossier and outcome frame, numbered procedure shields, tradition tier bands, and gazetteer heads. The generated book uses none of them; items and powers are bold run-in paragraphs with pipe separators (page 150), scenario setup is run-in labels, Appendix C sections look like any other. The specimens therefore show a richer book than the one printed.

### Inconsistencies

- **Two component libraries drift apart.** `system.typ` (specimens, aids, Hero records) and `heraldry.typ` (book) each define section headings (24 pt versus the 21 pt token), panels (unbreakable with a tag versus breakable without), figure blocks (number and title band versus number only), and tables (brush above and below with a tinted roll column versus bottom brush only). The 2026-10-16 density review already flagged "competing style definitions"; it still holds.
- **Tokens and Typst disagree on ink.** `ink.secondary_text_gray 0.2` versus `ink2 = luma(16%)`; `rule_gray 0.35` versus hairlines at 24% alpha; `band_gray 0.94` versus 5% alpha tints. Minor heading 14.5 pt, subsection number 9.5 pt, stat value 12 pt, and several 6.8 to 7.4 pt specimen labels are literals outside the token file.
- **Table identity repeats the heading when a label intervenes.** The duplicate-title suppression only looks one item back, so "The Mire Random Monster Table" prints as heading, then "APL 1–2 (d10)", then the same title again as the table identity (page 344). This pattern recurs across the six climate monster tables and similar label-plus-table pairs.
- **Chapter label carries the source period:** "CHAPTER 1." (the heading token "1." rendered verbatim). The spelled-out `words` list in `heraldry.typ` exists but is unused.
- **Version line** on the title page and back cover is 9 pt bold sans ("Release Candidate 522 (RC522)"), the only sans-bold line on otherwise serif pages, and reads like a build stamp.
- **Specimens use RC492 excerpts** and the unadopted components, so the design evidence does not describe the book.

---

## 3. Prioritized issue list

Severity: **High** affects every reader on most pages or blocks release quality; **Medium** affects a page type or chapter; **Low** is polish. Risk is the chance the change disturbs pagination, reconciliation, or gates.

| ID | Sev | Issue | Evidence | Recommendation | Expected impact | Risk |
|---|---|---|---|---|---|---|
| D-01 | High | Section heads set at column width; right column starts beside the rule | Pages 25, 50, 100; `production/mappings/blocks.json` (193 H3 placements, none full width); `typst/heraldry.typ` level-2 show rule inside `columns(2)`; plan 6.6 | Emit the H3 heading as a full-width opening part: composer marks the section head as kind `f` in `flat_parts`, `keeppage` takes a leading `f` part, `full-opening` carries heading plus any leading wide element; keep shield, 21 pt title, and brush across the 525 pt frame | Clear section architecture on every section page; removes the "text above the rule" anomaly; stronger scanning | Medium: repaginates (estimate 0 to +1% pages), measurement cache invalidates once, `test_layout_emitter` fixtures need updating; needs a full build and all-page review |
| D-02 | High | Near-empty pages: tails, stranded introductions, half columns, short appendix sections (partly mitigated by the RC527-build-40 tailpieces; see the update above for items f and g) | Pages 444, 395, 147, 153, 163, 111, 580, 585; ledger floor of 97 pages ≥ 250 pt foot void; 71 non-opener pages < 35 lines | (a) Extend `endart` to scenario tails and stranded-intro pages (art placement, no rule change); (b) compose the first numbered section on the opener page when the opener leaves more than 40% of the frame (the refinement policy table already allows "chapter opener plus first section as one opening composition"); (c) let Appendix C sections run on (reference density); (d) tail pull-back: when a unit's last page holds fewer than about 20 lines, prefer the balancing plan that keeps the tail at least a third of a page; (e) fix the density metric (P-04) so the program is measurable | Fewer wasted sheets and a steadier rhythm; most visible quality gain after D-01 | (b) and (c) are owner decisions against the 2026-10-12 fresh-page instruction; (a) and (d) are within policy; all need a build |
| D-03 | Medium | Castle flourish on every source rule; 3 to 4 per page in 7.17 | Sheet 09 pages 193–200; `heraldry.typ:567 hr-ornament`; 30 of 42 rules in Chapter 7; token `maximum_marks_per_ordinary_page: 2` | Make `hr-ornament` a quiet in-column separator (0.6 pt rule at 40% measure with a 4 pt lozenge, 10 pt above and below); keep the castle flourish for chapter and front-matter boundaries only | Chapter 7 item pages calm down; ornament budget honoured | Low: furniture only, no text layer change |
| D-04 | Medium | Minor headings (blackletter 14.5 pt) outrank subsections (serif bold 12.5 pt) | Page 494; `heraldry.typ:271,276` | Tokenize: subsection 13 pt serif bold with 10/4 pt spacing; minor 13 pt Grenze Gotisch with 8/3 pt; render one specimen page and confirm optically | Correct visual rank order through four levels | Low: a few points of height per heading, small repagination |
| D-05 | Medium | Thumb tab cuts through the opener frame | Pages 7, 24, 353; `system.typ thumb-tab` width `m-out − 3 pt`; `opener-frame` inset 0.42 in | Draw the tab with a 1.6 pt paper halo on framed pages, or notch the frame where the tab passes; keep the tab on top | Clean opener edge | Low: background only |
| D-06 | Medium | Planned component grammars unadopted (reference band, role tag, power/item entry, dossier, procedure, tier head) | `system.typ` versus emitted signatures in `build_book.py`; page 150 items as pipe-separated bold lines | Adopt in order: Appendix C band on C.x sections (after D-01); monster role tag from the "[Elite]" suffix as a typographic mapping (brackets kept in the text layer in transparent ink, like the coin); item and power name line with a cost tag; scenario dossier last | Reference pages identifiable; entries scannable; book matches its design evidence | Medium: each mapping must keep reconciliation exact; do one at a time with the table and keep audits |
| D-07 | Medium | Two component libraries and token drift; literals outside tokens | `system.typ` versus `heraldry.typ`; `design_tokens.json ink.*` versus Typst colours | Make `heraldry.typ` the only component source (specimens, aids, Hero records import it); bind `ink2`, `ink3`, `hair`, `tint`, `tint2`, rule weights, and all type sizes to tokens; add tokens `type_pt.minor`, `type_pt.stat_value`, `type_pt.label_min`, `type_pt.toc_entry`, `type_pt.index`, `line_pt.section_brush`, `line_pt.hairline`, `ink.hairline_alpha`, `ink.band_alpha` | Single source of truth; specimens become real evidence; future changes are one-line | Low to medium: refactor without visual change first, verified by identical page geometry |
| D-08 | Medium | Table identity repeats a visible heading across an intervening run-in label | Page 344; `build_book.py chapter_items duplicate_title` | Look back past one short run-in label when deciding `initial-title: false` | About thirty tables lose a redundant line | Low |
| D-09 | Low | "CHAPTER 1." label with source period; `words` list unused | Page 7; `heraldry.typ chapter-opener` | Render "CHAPTER ONE" (or the numeral without the period, keeping the period as a transparent glyph for reconciliation) | Cleaner opener | Low |
| D-10 | Low | Version line in 9 pt bold sans on title page and back cover; back-cover facts centred ragged | Page 1, back cover | Set the version in tracked serif small caps at 9.5 pt; set back-cover facts ragged left in a 4.8 in measure under a short rule | Front and back matter read as one voice | Low |
| D-11 | Low | Contents is two levels; bestiary and scenario entries are reachable only through bookmarks and the index | `frontmatter.typ toc-page depth: 2` | Optional: a generated one-column mini contents at the head of Chapters 9 and 10 (furniture, not manuscript), or depth 3 for those two chapters only | Faster table lookup in the two longest chapters (112 and 137 pages) | Low; adds about two pages; owner choice |
| D-12 | Low | Ancestry and background portraits stacked above the flavour leave half-empty columns | Pages 100, 111; plan 6.12 wanted the portrait beside the head | Measure a side-by-side variant (portrait 2.15 in in the outer column, facts beside) for ancestries and backgrounds; keep whichever packs two per page more often | Fuller Chapter 6 pages | Medium: art placement and keep classes change |
| P-01 | High | Physical proof NOT TESTED; binding unknown; 45 pt inside margin for a 618-page block | `config/production.json printer.*` all null | Owner decision on printing and binding; print the calibration sheet plus a 16-page mixed spread on the actual device and stock before any margin change; keep NOT TESTED as a release qualifier | Unblocks the margin, hairline, and tint decisions below | None until decided |
| P-02 | Medium | 0.35 pt hairlines at 24% alpha and 5% tints are below reliable home-inkjet thresholds; calibration tests black rules only | `heraldry.typ hair/tint`; `calibration.typ` | Add tinted hairline samples (0.3 to 0.6 pt at 24%, 30%, 40%) and the 5% and 9% tints to the calibration sheet; pre-set a fallback of 0.4 pt at 30% and 6% bands behind a token | Rows and bands survive on real paper | Low |
| P-03 | Medium | Digital edition is 177 MB after the tailpieces (157 MB before); no screen-optimised variant | `dist/RELEASE.json` | Add a post-export pass for the digital PDF only: downsample rasters to 150 ppi with pymupdf, keep text, links, and bookmarks; verify page count and links; deliver as a separate, clearly labelled asset | Roughly 30 to 45 MB; usable on tablets | Low: print PDFs untouched; add one minute to the build |
| P-04 | Medium | Density triage counts the thumb tab as content, so foot-void values cap at the tab (27 Scenarios pages at exactly 250.4 pt, 21 Appendix C pages at 62.1 pt, 21 Basic Mode pages at 109.2 pt) | `production/qa/layout.json`; `tools/layout_qa.py` | Exclude page-background furniture from the vertical union; add a `sparse_page` diagnostic (body lines, columns, largest band) and report it per chapter | The void program becomes measurable and reviewable | Low: diagnostic only |
| P-05 | Low | Eight-pass composition at about 13 minutes with a 12 GB swap; D-01 invalidates the measurement cache once | `production/STATE.md` | Accept; batch D-01, D-04, and D-08 into one build so the cache misses once | Build time unchanged | None |

---

## 4. Implementation plan

Branch policy: `CLAUDE.md` (owner, 2026-10-31) requires commits straight to `main` with no pull requests. Each phase below lands as one or two verified commits on `main`; a build and all-page review follow only on the owner's build request.

### Phase 0: groundwork (no visual change, no build)

1. P-04: fix the density metric and add the sparse-page diagnostic; re-run it against the RC522 ledger for a baseline table by chapter.
2. D-07 part 1: add the new tokens; bind existing Typst literals and colours to them with values that reproduce today's geometry exactly; `layout_profile.validate()` and the fixture tests prove no drift.
3. D-07 part 2: make `heraldry.typ` the single component source and have `specimens.typ`, `aids/kit.typ`, and `heroes/*.typ` import it; re-render specimens and aids as PNG evidence (`tools/render_template_specimens.py --sheet`).
4. Update `docs/BOOK_DESIGN_PLAN.md` section 10 to record what is adopted and what is not.

### Phase 1: quick wins (one build)

D-03 separator, D-05 tab halo, D-08 identity dedupe, D-09 chapter label, D-10 version line and back-cover facts, P-02 calibration additions, P-03 digital variant. All are furniture or export changes with no text-layer effect except D-09 (handled as a transparent-glyph mapping). Run `python tools/dev.py check`, then request the build and review every opener, Chapter 7 item pages, the climate tables, title page, and back cover at 100 dpi.

### Phase 2: structural fixes (one build, after owner answers Q2 to Q4)

1. D-01 full-width section heads (composer parts plus Typst), with D-04 hierarchy sizes in the same build so the measurement cache misses once.
2. D-02 (a) and (d): `endart` for scenario tails and stranded-intro pages; tail pull-back threshold in `compute_balance`.
3. D-02 (b) opener-plus-first-section composition and (c) Appendix C run-on, if approved.
4. D-06 step 1: Appendix C reference band on the now full-width C.x heads; D-06 step 2: monster role tag.
5. Verify: keep audit (0 avoidable splits, coverage 100%), table audit 333/333, page-map accuracy, print geometry identical cream and white, layout QA 0 flags, sparse-page report compared with the Phase 0 baseline, all-page contact-sheet review, and 100 dpi review of every section start in two chapters plus every scenario tail.

### Phase 3: production readiness and optional grammars

1. P-01 physical proof on the owner's device and stock; then settle hairline and tint tokens and the inside margin.
2. D-06 steps 3 and 4 (item and power name line with cost tag; scenario dossier) as typographic mappings, one per build, each with reconciliation evidence.
3. D-11 mini contents for Chapters 9 and 10, and D-12 side-by-side ancestry layout, if wanted.

---

## 5. Production specs

Values marked "current" are in force today; "proposed" are the changes above. Everything lives in `config/design_tokens.json` unless stated.

### 5.1 Page and grid (current, retain)

- Trim 612 × 792 pt portrait, borderless; cream `#FCFAF5` and white `#FFFFFF` companions with identical geometry.
- Margins inside 45, outside 42, top 45, bottom 45 pt; frame 525 × 702 pt; two columns of 254.4 pt with a 16.2 pt gutter; essential content at least 27 pt from the trim; thumb tabs stop 3 pt short of the frame.
- Full-width regions: chapter openers, section heads (proposed), wide tables and figures, scenario heads, chapter introductions at the 82% measure.
- Column regions: prose, lists, examples and notes, monster entries, powers, items, column figures (243 pt).

### 5.2 Type scale (pt, with leading as baseline pitch)

| Role | Face | Current | Proposed |
|---|---|---|---|
| Chapter title | Grenze Gotisch 600 | 50 | same |
| Section (x.y) | Grenze Gotisch 600 in a 25 or 30 pt shield | 21, column width | 21, full width, brush 2.2 pt across the frame |
| Subsection (x.y.z) | Source Serif 4 Bold, sans number 9.5 at 42% | 12.5 | 13, space before 10, after 4 |
| Minor heading | Grenze Gotisch 600 | 14.5 | 13, space before 8, after 3 |
| Run-in label | Source Serif 4 Semibold (bold delta 200) | body | same |
| Body | Source Serif 4 | 10.5 / 13.9 justified, en-CA hyphenation, limits 85–140% space, ±2% tracking | same |
| Flavour and leads | IM FELL English | 10.5 / 14.3, 84% black, 82% measure for leads | same |
| Table | Source Sans 3, tabular lining | 9 / 11.85; header 9 bold reversed small caps | same |
| Caption and figure label | Source Sans 3 | 9 | same |
| Running head | Source Sans 3 Semibold small caps +0.12 em | 9 | same |
| Folio | Source Sans 3 Bold reversed in a 23 pt shield | 9 | same |
| Tab keyword | Grenze Gotisch 700 reversed | 9 | same |
| Contents | chapter row Grenze 14, line serif 9.5, page sans 9.5 | current | same |
| Index | Source Sans 3 9.5, letter heads Grenze 13 reversed | current | same |
| Stat strip | labels 9 reversed, values Source Sans 3 Semibold 12 | current | tokenize as `type_pt.stat_value` |
| Version and imprint lines | Source Sans 3 Bold 9 | current | serif small caps 9.5, +0.1 em |
| Floor | any essential text | 9 | same |

### 5.3 Spacing (pt; unit 3)

Paragraph after 4.5; list item 2.8; section before 12, after 7; subsection 9/4 (proposed 10/4); minor 8/3; table above 6, below 8 (+4 after the brush); panel 7/8 with 8 × 6 inset; figure 10/12; lead block 5/8; flavour paragraph after 6; separator (new) 10/10; chapter opener below 14.

### 5.4 Rules, tints, and ornament

- Section brush 2.2 pt (deterministic taper); table close brush 2.2 pt, zero height; stat brush 2.0 pt; running-head pair 1.1 + 0.35 pt; figure close 0.6 pt; panel spine 2.6 pt; frame 1.4 + 0.4 pt.
- Hairlines 0.35 pt at 24% black (current); fallback after proof 0.4 pt at 30%. Bands 5%, roll column 9%, panels 5% (current); fallback bands 6%.
- Ornament budget: at most two marks on an ordinary page. Castle flourish only at chapter and front-matter boundaries; in-column separators are a 0.6 pt rule at 40% of the measure with a 4 pt lozenge (proposed).
- Ornament never sits inside a table cell, behind text, or behind art.

### 5.5 Tables

- One grammar: optional identity line (9 pt sans bold, suppressed when the visible heading or heading-plus-label already names it, always shown with "(continued)" on later pages); black header band; key column bold left; text left; short values centred; die column centred; 2.2 pt vertical and 4 pt horizontal inset; 5% bands on even rows; 24% hairlines; bottom brush.
- Width: cell-aware allocator against the column (254.4 pt) first, full frame (525 pt) when any column would be skinny; families share widths within an H3; reviewed overrides by heading path and header cells only (`layout.table_scope_policies`).
- Keeps: a table of five rows or fewer never splits; longer tables carry their first and last three rows together; header repeats; a table that fits a column but not beside its heading starts only where both columns of one page can hold the pair.
- Transformations: single-row stat tables become stat strips (short cells) or stat cards (formula cells); prose-heavy tables of six or more columns become labelled entries with every header kept as a field label in source order. Every transformation is recorded in `production/mappings/tables.json`.
- Coin mark replaces "c" typographically; the letter stays in the text layer.

### 5.6 Figures and captions

- Column figures 243 pt wide, height at most about 260 pt; full-width figures 504 pt. Figure, caption band, caption, and closing rule are one unbreakable unit placed after the block they illustrate; FIG-20 floats.
- Caption band: black, 9 pt bold reversed, printed figure number in book order; caption 9 pt sans ragged, at most three sentences, ending with the section reference; 0.6 pt close.
- Diagram text 9 pt or more, grayscale only, strokes 0.5 pt or more (enforced by `make_figures.py`).

### 5.7 Callouts

- Example and rules-note panel: 5% field, 2.6 pt black spine, 8 × 6 pt inset, body size, justified; the source's own label ("Example:") leads in bold; breakable, with list items unbreakable. No invented labels or taxonomy.

### 5.8 Stat blocks and entries

- Monster: heading (name, role in brackets; proposed role tag), IM FELL flavour, stat strip (HP, AV, SPD, LVL, CV, Sz), run-in labelled lists (AI Steps, Attacks, Special Abilities) in source order; one column per creature, two per page, full width only when over-height.
- Scenario: fresh page; title and number; flavour at 82%; setup fields as run-in labels (proposed dossier later); map beside setup; "(continued)" running head until the next scenario.
- Item and power: name line bold with source metadata (proposed cost tag mapping); flavour; "Effect:" paragraph.
- Hero profiles (Basic Mode): identification lines keep with the name; portrait placed as end art.

### 5.9 Furniture, contents, index, cross-references

- Verso head: arms, chapter name; recto head: section or scenario name with "(continued)". Suppressed on openers and front matter.
- Folio: reversed shield at the outer foot with a 40 pt brush toward the gutter; centred in the frame on openers.
- Tabs: fifteen fixed slots; black pennant with engraved inner line; keyword rotated along the edge; paper halo on framed pages (proposed).
- Contents: two columns, chapter rows with arms and rule, dotted leaders; depth two (optional depth three for Chapters 9 and 10).
- Index: three balanced columns, reversed letter heads, hanging entries, sub-entries indented 9 pt, locators linked in the digital edition.
- Cross-references: bare bold numbers in the text; clickable in the digital edition; audited by `tools/xref_audit.py`.

---

## 6. Implementation checklist and definition of done

Per change:

- [ ] Tokens first: any new size, weight, colour, or spacing lives in `config/design_tokens.json` and is read by Typst and `tools/layout_profile.py`.
- [ ] Text layer unchanged: a typographic mapping keeps the source glyphs (transparent or hidden where visually replaced) and is recorded for reconciliation.
- [ ] Fixture test added or updated in `tests/test_layout_components.py` or `tests/test_design_review_fixes.py` for each new rule (identity dedupe, separator, tab halo, section part kind, hierarchy sizes).
- [ ] `python tools/dev.py check` and `make test` pass (note: the Hero-card test needs LFS image bytes).
- [ ] Specimen PNGs re-rendered for the affected page types and inspected at 100%.
- [ ] Owner build request, then `make clean all verify package`; cache miss accepted once for D-01.
- [ ] Gates green: keep audit (0 avoidable splits, full coverage), table audit 333/333, page map, print geometry identical cream and white, inkjet preflight, art ppi, index, cross-references, figure gate.
- [ ] Sparse-page report compared with the Phase 0 baseline; every remaining sparse page is a documented over-height continuation, a fresh-page start, or carries end art.
- [ ] All-page contact-sheet review plus 100 dpi review of every changed page type; findings recorded in `production/qa/visual-review.json` by the named reviewer.
- [ ] `production/STATE.md`, `production/RELEASE_STATUS.md`, and `docs/BOOK_DESIGN_PLAN.md` updated; physical print status stays honest.

Definition of done for this programme: section heads full width on every section page; no ordinary page with more than two ornament marks; heading sizes in rank order through four levels; tabs clear of frames; identity lines never duplicate a visible title; tokens the only source of sizes and inks; specimens rendered from the book's own components; a measurable sparse-page report with no undocumented sparse page; a verified build released through the existing chain; physical proof either tested or still marked NOT TESTED.

---

## 7. Decisions needed from the owner

1. **Printing and binding.** What device, stock, and binding will the physical book use? This decides the inside margin, hairline, and tint questions (P-01, P-02).
2. **Full-width section heads (D-01).** Approve the repagination (estimate 0 to +1% pages) and the one-time cache miss?
3. **Opener plus first section (D-02 b).** May the first numbered section start on the chapter-opener page when the opener leaves more than 40% of the frame empty? The refinement policy already allows this composition; the 2026-10-12 fresh-page instruction is read as keeping fresh pages elsewhere.
4. **Appendix C density (D-02 c).** May C.x reference sections run on instead of each starting a fresh page?
5. **Digital variant (P-03).** Is a downsampled digital PDF wanted as an additional release asset?

Assumptions used if unanswered: the keep contract and fresh-page policy stand unchanged; home inkjet borderless Letter remains the target; the branch policy in `CLAUDE.md` (main only, no pull requests) governs implementation.
