# Heraldry publication design specification

> **2026-10-16 compact approval, implemented from 2026-10-20:** 10.5 pt body, 9 pt tables, narrower margins, and the approved refinement report supersede earlier size/geometry proposals. The effective profile is `config/design_tokens.json`, shared by Typst and `tools/layout_profile.py`. Complete-unit keeps and source fidelity remain mandatory.

> **2026-10-12:** `docs/BOOK_DESIGN_PLAN.md` (design system v2, "Ink and Iron") supersedes this document's visual identity: display face, heading, furniture and component styling, and the page-type templates. Grid, page, source-fidelity and pagination rules here and in DESIGN_REFINEMENT.md remain in force.

Status: implementation brief, distilled from the ten owner-selected visual references. `docs/DESIGN_REFINEMENT.md` supplies the latest owner-requested iteration and overrides the earlier specimen freeze. These specifications guide the first stress specimen. Tune optical details once after rendering, then apply the resulting system consistently. MASTER_PROMPT.md governs source preservation and completion. The manuscript governs all mechanics and terminology.

## 1. Visual identity

Build an original dark medieval fantasy reference book with a light, clean reading field: almost-white cream/parchment tone, black ink, readable serif prose, practical sans-serif tables, restrained display headings, sparse original heraldic ornament, economical ink vignettes, and crisp vector diagrams. The book is a digital PDF of portrait US Letter pages. Implement starting values from `config/design_tokens.json` and acceptance checks from `docs/VISUAL_QA.md`; refine once on real content, then freeze. High production quality must show in ordinary reference pages, not just a decorative cover.

Reference assignments: BlackDeathCity and Deth Wizards for atmosphere and vignette placement; Mythras for calm grayscale prose; Hametsu and Five Leagues for tables, examples, and navigation; Hellcrawl for keyed entries. The Village Hunt informs silhouette/open-space integration; Dread Nights informs hierarchy and labelled entries; TNA Ultimate and TES: Call to Arms inform nearby exact instructional diagrams. Use only the ten titles recorded in `references/sample_pdfs.json`. Do not clone a page, extract source art into the book, or import reference mechanics.

Substrate: flat `#FCFAF5` warm cream from edge to edge. Parchment here means a very light restrained tone, not distressed texture. No scanned paper stains, burned edges, gritty noise, repeated texture, decorative watermark, distressed body font, heavy perimeter frame, colour-only coding, or dark ordinary-page background. Use an opaque page background independent of body margins; never place a white rectangle behind every paragraph/table.

## 2. Page grid

Every primary page is 8.5 × 11 inches (612 × 792 pt), portrait, single pages with facing-page furniture. No landscape fallback or imposed spreads. Use inside 45 pt, outside 42 pt, top 45 pt, and bottom 45 pt. The 525 × 702 pt frame keeps the wider inside margin and measured safe navigation.

Two columns with a 16.2 pt (0.225-inch) gap for ordinary rules and reference entries; each column is 254.4 pt wide. Permit one continuous full-width region for wide tables/diagrams; avoid repeated full-width islands separated by tiny two-column fragments. Opening chapter/section flavour uses an inset single-column region; substantive scenario/procedure prose follows the same two-column grammar.

Running heads identify chapter and major section, 9 pt. Folios sit at lower outer corners. All essential furniture stays at least 0.375 inch from every page edge. A background that reaches the page edge does not remove text margins. Major chapter titles may occupy more space; normal running navigation stays quiet. Avoid a permanent navigation rail.

## 3. Type hierarchy

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

## 4. Reading flow

Apply the explicit fresh-page and conditional-keep policy in DESIGN_REFINEMENT.md. Chapters, major numbered sections and named scenarios start on fresh pages, with the first section composed with its chapter opener. Nested headings keep meaningful opening content; all complete fit-capable sections, subsections, scenarios, tables and entries must stay on a single page and move whole when remaining space is insufficient, including their headings and necessary associated content. Keep definition, procedure, exceptions, and interpretive table notes together where practical. Keep headings with at least a meaningful paragraph or two complete list items. Prevent single-line widows/orphans without forcing large gaps. Keep ordinary table rows intact; handle over-height rows explicitly.

Use bounded justification, Canadian English hyphenation, and inspect spacing/rivers. Prevent breaks within short dice notation, bracketed costs, modifiers, and values with units, using layout semantics rather than changing canonical text.

Examples attach to their subject rule; art attaches to a relevant entry or chapter transition. Do not use arbitrary art to hide a pagination defect. Do not wrap text tightly around irregular illustration contours in dense rules sections.

## 5. Table components

Shared grammar: bold headers, modest cell padding (4 pt horizontal and 2.2 pt vertical), useful column width, consistent alignment, light rules, optional grayscale bands on the chosen clean substrate. Start rules around 0.5–0.7 pt and verify at actual size. Start bands around 6% black but treat shading as optional; labels/rules must work without it.

| Component | Layout |
|---|---|
| Roll/result | Narrow centred range column; wide left-aligned result; no decorative full grid |
| Numeric/equipment | Left-aligned names, aligned compact numeric fields, generous descriptive column |
| Long prose | Full-width table or labelled entry transformation with complete source mapping |
| Monster | Name; HP, AV, SPD, LVL, CV, Sz; AI Steps; Attacks; Special Abilities |
| Powers/items | Stable name/metadata/body anatomy; only actual source fields |
| Scenario/scaling | Exact canonical field labels, readable groups, full-width where needed |
| Appendix/reference | Compact hierarchy, sensible group spacing, explicit continuations |

Full-width tables take priority over narrow prose columns. Solve overflow with width/padding adjustment, full-width placement, natural row-group continuation, faithful entry transformation, then keyed portrait continuation panels or faithful entries. Preserve every cell and repeat unique row keys when column groups continue. Landscape pages are excluded from this edition. Do not reduce essential text below 9 pt. Do not create long skinny rules columns to preserve a spreadsheet silhouette.

Repeat headers and a continued marker on subsequent pages. Preserve notes, ranges, row keys, and source relationships. A changed representation requires a machine-readable source-cell-to-output-field mapping. Use tabular numerals. Avoid vertical rules unless a matrix needs them. Reserve black header bands for selected reference components, not every table.

## 6. Entry and scenario anatomy

Use recurring entry templates rather than a unique box for every named ability. Fields stay in source order except an explicitly documented mechanically neutral layout mapping. Do not invent missing metadata. Keep the five traditions visually identifiable using canonical text labels rather than a new rules icon taxonomy.

Monster anatomy follows the canonical order and contains no invented abilities or resources. Scenario pages retain canonical headers and scaling fields. Use repeatable spacing to make setup, timing, special rules, scoring, and source-provided aftermath easy to find without relabelling them.

A scenario may occupy several pages only when its complete measured unit cannot fit one usable page at the approved width. A fit-capable scenario, including its heading, deployment map, setup, rules, scoring and notes, must occupy one page. Keep fit-capable child units intact in longer scenarios. Do not force a one-page format by omitting rules. Stronghold/campaign entries may use light cards when the source structure supports them; keep card contents fully reconciled.

## 7. Original graphics and artwork

One small original ornament family, drawn as editable vectors. Thin rules, one original broken-ring/tapered-rule motif, and sparse chapter marks are sufficient. At most two small marks on an ordinary page; use the same line vocabulary throughout. Motifs have no rules meaning. Skip ornament where it weakens alignment or reading flow. Do not trace reference logos, borders, emblems, or proprietary icons.

Atmospheric art: follow ART_DIRECTION.md. Cover/chapter compositions and relevant black-and-white ink vignettes supply the visual character. No illustration underneath rules text. Keep adequate open negative space and test hatching at placed size. Blend transparent/matted vignette edges into the actual cream substrate; reject white rectangles, halos, and duplicated paper texture. Ordinary-page spot art should normally occupy no more than one quarter of the page, chapter art about two fifths; these are composition targets, not a source-layout constraint. No full-page artwork interludes by default. Preserve the existing fallback to a fully typeset art-light edition when original illustration assets are unavailable.

Rules graphics: editable vectors, clean substrate, consistent base symbols, patterned terrain, solid/dashed lines, numbered callouts, and readable legends. Differentiate allegiance and geometry redundantly. Use metric-perfect dimensions only when the source supports them and the drawing is actually scaled; otherwise label the diagram schematic. Explain Tabletop first and Grid second where rules differ.

Create AI/phase diagrams only from source-supported branches. Avoid a single giant flowchart. Separate one decision topic per figure; use compact multi-panel spatial diagrams for local edge cases. All captions and worked arithmetic need semantic verification against the manuscript.

## 8. Navigation and evidence

Real linked TOC; PDF bookmarks; useful semantic index; reliable page references after pagination freezes. Running navigation uses chapter and section names. Alphabetical entry pages have clear group headings and sensible hanging indents.

Each adopted reference lesson appears in `production/design-decisions.md` as reference ID/page, abstract principle, Heraldry implementation, and specimen evidence. Reference rules never enter the editorial patch ledger as an authority.

Missing optional references do not block production. Read the analysis/specification once; pass implementation decisions, not the entire PDF collection, to workers. Primary inspection is a bounded design task, not a repeated assignment throughout the build.

## 9. Stress specimen and freeze gate

Produce an 8–12-page actual-content specimen, allowing an extra page only if needed for a genuine high-risk component. Include:

- Chapter opening and ordinary facing pages.
- Normal two-column rules, a sustained procedure, and a worked example.
- Short random-result table, numeric table, longest prose row, and widest source table.
- Monster profile, scenario with its canonical scaling fields, and an appendix reference.
- A vector diagram, ink art treatment or clearly identified production-only art reservation, and index slice.

Inspect at actual size and enlarged detail. Use a contact sheet only for page rhythm. Confirm hierarchy, optical type size, column balance, table relationships, note attachment, gutter clearance, grayscale diagram distinctions, and art/prose separation. Apply the component rubric in VISUAL_QA.md. Revise the system once, record it, then produce the full book.

No PASS based solely on an attractive cover, chapter opening, or successful compilation. The final design gate is usable ordinary pages plus complete source reconciliation and all exceptional table/diagram checks required by MASTER_PROMPT.md.

## 10. Authored finish and delivery

Use the type/spacing/rule/palette tokens as one system. Display lettering appears on chapter/major titles, not every subheading. No generic shield badge on every entry, random flourish, ubiquitous skull, imitation occult lettering, dashboard cards, drop shadows, polished fantasy gradient, or busy symmetrical frame. Keep body ink strong and ornaments subordinate. Atmosphere follows specific manuscript subjects and materially convincing ink drawing.

Deliver the digital PDF, with its front and back covers inside it, and the screen companion `Heraldry_RC###_digital-compact.pdf`, which keeps the same pages, bookmarks, and links; navigation destinations must resolve in both. Do not add a texture generator as a substitute for editorial craft. A clean art-light edition uses typography, sparse original marks and accurate diagrams; it never claims missing atmospheric illustrations are complete.
