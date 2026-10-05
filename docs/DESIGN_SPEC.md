# Heraldry publication design specification

Status: implementation brief, distilled from supplied visual references. These specifications guide the first stress specimen. Tune optical details once after rendering, then apply the resulting system consistently. MASTER_PROMPT.md governs source preservation, budget, and completion. The manuscript governs all mechanics and terminology.

## 1. Visual identity

Build an original monochrome medieval fantasy reference book. Use clean white reading fields, readable serif prose, practical sans-serif tables, restrained display headings, original heraldic ornament, rough ink illustrations, and crisp vector diagrams. Treat each as a separate semantic role within one system.

Reference assignments: BlackDeathCity and Deth Wizards for atmosphere and vignette placement; Mythras for calm grayscale prose; Hametsu and Five Leagues for tables, examples, and navigation; Hellcrawl for keyed entries. Secondary references address diagrams, index, and recurring entry anatomy only. Do not clone a page, extract source art into the book, or import reference mechanics.

No parchment behind text, decorative watermark, simulated paper stain, distressed body font, heavy perimeter frame, colour-only coding, or repeated dark page background. Paper colour belongs to physical production, not a painted digital substrate.

## 2. Page grid

Default trim: 8.5 × 11 inches, portrait, facing pages. Start inside margin 0.875 inch, outside 0.625 inch, top 0.65 inch, bottom 0.7 inch; reassess gutter against final binding/page count. This creates a 7-inch horizontal text frame before any adjustments.

Two columns, 0.25-inch gap, for normal short rules and reference entries. At the starting margins, each column is 3.375 inches. Permit one continuous full-width region for wide tables/diagrams; avoid repeated full-width islands separated by tiny two-column fragments. Use single-column pages for procedures/scenarios when it improves the reading path.

Running heads identify chapter and major section, 9 pt. Folios sit at lower outer corners. Neither enters the trim/binding exclusion zones. Major chapter titles may occupy more space; normal running navigation stays quiet. Avoid a permanent navigation rail.

## 3. Type hierarchy

Candidate roles: Source Serif 4, Source Sans 3, Cinzel. Verify font licensing, available weights, embedding, and glyph coverage. Bundle approved files and licences. At most three families; decorative blackletter is not an additional default family.

| Role | Starting specification | Behaviour |
|---|---|---|
| Body | Serif 10.5–11 pt / 13–14 pt leading | Ragged right initially; deliberate paragraph spacing |
| Chapter title | Display 26–32 pt | Original ornament/art may accompany it; preserve canonical numbering |
| Major section | Display or serif semibold 16–18 pt | Keep with meaningful following content |
| Subsection | Serif semibold 12.5–14 pt | Clear vertical separation; no gratuitous box |
| Minor heading | Body-sized bold | Run-in only where source structure permits |
| Table body | Sans 9.5–10 pt / about 12 pt | Minimum 9 pt essential text; real semibold headers |
| Example | Body family, 10–10.5 pt | Explicit title; subtle outline/left rule; clean substrate |
| Diagram label/caption | Sans 9–10 pt | Legible at placed size; no downscaling below minimum |
| Index | Sans or serif 9–9.5 pt | Hanging indent; two or three columns after legibility testing |

These are targets, not measurements copied from the books. Optical adjustment is permitted after the actual-content specimen. Do not globally shrink content to fit. Preserve semantic bold and the user's typography lock, including ASCII quotes/apostrophes, numeric-range en dashes, ×, and −.

## 4. Reading flow

Keep definition, procedure, exceptions, and interpretive table notes together where practical. Keep headings with at least a meaningful paragraph or two complete list items. Prevent single-line widows/orphans without forcing large gaps. Keep ordinary table rows intact; handle over-height rows explicitly.

Start with non-justified body text. If adopting justification, require Canadian English hyphenation and inspect spacing/rivers. Prevent breaks within short dice notation, bracketed costs, modifiers, and values with units, using layout semantics rather than changing canonical text.

Examples attach to their subject rule; art attaches to a relevant entry or chapter transition. Do not use arbitrary art to hide a pagination defect. Do not wrap text tightly around irregular illustration contours in dense rules sections.

## 5. Table components

Shared grammar: semibold headers, modest cell padding (start 4 pt horizontal and 3 pt vertical), useful column width, consistent alignment, light rules, optional grayscale bands. Start rules around 0.5–0.7 pt and verify at print size. Start bands around 8–12% black but treat shading as optional; labels/rules must work without it.

| Component | Layout |
|---|---|
| Roll/result | Narrow centred range column; wide left-aligned result; no decorative full grid |
| Numeric/equipment | Left-aligned names, aligned compact numeric fields, generous descriptive column |
| Long prose | Full-width table or labelled entry transformation with complete source mapping |
| Monster | Name; HP, AV, SPD, LVL, CV, Sz; AI Steps; Attacks; Special Abilities |
| Powers/items | Stable name/metadata/body anatomy; only actual source fields |
| Scenario/scaling | Exact canonical field labels, readable groups, full-width where needed |
| Appendix/reference | Compact hierarchy, sensible group spacing, explicit continuations |

Full-width tables take priority over narrow prose columns. Solve overflow with width/padding adjustment, full-width placement, natural row-group continuation, faithful entry transformation, then controlled landscape. Do not reduce essential text below 9 pt. Do not create long skinny rules columns to preserve a spreadsheet silhouette.

Repeat headers and a continued marker on subsequent pages. Preserve notes, ranges, row keys, and source relationships. A changed representation requires a machine-readable source-cell-to-output-field mapping. Use tabular numerals. Avoid vertical rules unless a matrix needs them. Reserve black header bands for selected reference components, not every table.

## 6. Entry and scenario anatomy

Use recurring entry templates rather than a unique box for every named ability. Fields stay in source order except an explicitly documented mechanically neutral layout mapping. Do not invent missing metadata. Keep the five traditions visually identifiable using canonical text labels rather than a new rules icon taxonomy.

Monster anatomy follows the canonical order and contains no invented abilities or resources. Scenario pages retain canonical headers and scaling fields. Use repeatable spacing to make setup, timing, special rules, scoring, and source-provided aftermath easy to find without relabelling them.

A scenario may occupy a spread or several pages. Keep its deployment diagram and key setup instructions together when possible. Do not force a one-page format by omitting rules. Stronghold/campaign entries may use light cards when the source structure supports them; keep card contents fully reconciled.

## 7. Original graphics and artwork

One small original ornament family, drawn as editable vectors. Thin rules, a simple original heraldic motif, and sparse chapter marks are sufficient. Do not trace reference logos, borders, emblems, or proprietary icons.

Atmospheric art: follow ART_DIRECTION.md. Cover/chapter compositions and relevant black-and-white ink vignettes supply the visual character. No illustration underneath rules text. Keep adequate open white space and test hatching at placed size. Preserve the existing fallback to a fully typeset art-light edition when original illustration assets are unavailable.

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

Inspect at actual print size and enlarged detail. Use a contact sheet only for page rhythm. Confirm hierarchy, optical type size, column balance, table relationships, note attachment, gutter clearance, grayscale diagram distinctions, and art/prose separation. Revise the system once, record it, then produce the full book.

No PASS based solely on an attractive cover, chapter opening, or successful compilation. The final design gate is usable ordinary pages plus complete source reconciliation and all exceptional table/diagram checks required by MASTER_PROMPT.md.
