# Heraldry publication: reference analysis

## Recommendation

Distil the references into the repository's design specification first. Supply a small, purpose-labelled visual reference set only when useful during execution. Do not make reading every reference book a prerequisite for building Heraldry.

The production model needs concrete decisions about hierarchy, page geometry, tables, diagrams, and artwork. A pile of PDFs leaves those decisions implicit and invites incompatible design choices. A written specification alone can also leave aesthetic intent underspecified. The strongest workflow combines explicit design rules with selected visual evidence.

The updated publication kit contains the analysis, an implementation specification, a verified reference manifest, and an optional page-rendering script. It does not bundle the commercial reference PDFs or their page images. The manuscript remains the only rules authority. Reference books supply visual and instructional design observations only.

## Review method and limits

Reviewed representative rendered pages from 32 supplied PDF files, plus targeted examples of index pages, entry formats, movement diagrams, scenario pages, and AI diagrams. The files represent 29 unique byte sequences: the two Five Leagues copies, the two Hametsu copies, and the two Village Hunt copies are respectively identical by SHA-256. Retain one copy of each.

This is a comparative design reconnaissance, not an exhaustive page-by-page audit, a font-identification study, or a preflight certification of the reference books. Recommendations below are design judgements based on the inspected samples. All page references are 1-based PDF viewer pages, not printed folios. Some supplied PDFs contain two facing book pages within one PDF page; do not confuse that geometry with a single-page trim size.

## The design to build

Heraldry should read like a substantial, well-edited monochrome fantasy reference book: clear serif prose, economical sans-serif table typography, restrained medieval display lettering, clean paper-white reading fields, original rough ink illustrations, consistent small ornaments, and exact vector diagrams. Its identity should survive grayscale printing and remain usable during a game.

Use the atmospheric lessons of BlackDeathCity and Deth Wizards, the readable monochrome structure of Mythras, the table and example discipline of Hametsu and Five Leagues, and the labelled instructional graphics found in Call to Arms and TNA. Hellcrawl is useful for compact keyed content; Pathfinder supplies lessons in repeatable entry anatomy and indexing. These are separate assigned roles, not an instruction to mix their entire visual identities.

### Primary references

| Reference | Inspected PDF pages | Observable pattern | Heraldry adaptation | Limit |
|---|---|---|---|---|
| BlackDeathCity - Playtest 101 | 7, 32, 36, 74 | Monochrome art, display headings, small emblems, boxed holdings, scenario map, white central reading field | Original ink vignettes; sparse original heraldic markers; stable entry cards; scenario text paired with deployment geometry | Keep distressed lettering to display roles. Remove the mottled substrate behind rules. Do not adopt its mechanics or names. |
| Deth Wizards | 9, 27, 55, 60 | Rough ink figures, recurring profile labels, compact tabular terrain information, simple measured deployment diagram | Original ink art; reusable monster profile anatomy; direct setup diagrams; meaningful art placements beside relevant entries | Keep texture out of the reading field; its narrow single-column samples should not dictate the entire larger Heraldry book. |
| Mythras: Classic Fantasy Imperative | 7, 87, 96 | Two-column serif prose, thin running rules, restrained headings, grayscale art, full-width table beneath columns | Baseline prose rhythm and monochrome reading environment; full-width table transitions; calm running navigation | Heraldry needs a stronger distinction between examples, reference entries, and normal prose than a single dense prose template offers. |
| Hametsu, supplied second printing | 11, 29, 101, 178 | Parallel prose and examples; wide grouped equipment tables; alternating rows; section marker; alphabetical index | Inline examples beside their rule; restrained grayscale row banding; descriptive column width; intentional index hierarchy | Translate red bands into grayscale hierarchy. Do not reserve a dark example sidebar on every page. |
| Five Leagues from the Borderlands, third edition | 6, 38, 130, 138 | Section-specific running navigation, compact random tables, sequential setup instructions, diagram with keyed figures and differentiated lines | Reliable campaign-stage navigation; compact dice columns; diagrams with labelled entities and explicit legends | Translate colour cues into labels and patterns. Avoid decorative borders consuming the binding margin. |
| Hellcrawl, supplied 2026-09-13 PDF | 7, 56, 60 | Clean light substrate, compact numbered entries, small result tables, keyed ink map, strong headings | Concise keyed reference pages, map-to-entry correspondence, selective atmospheric lettering | Do not inherit its comic tone, red-dependent hierarchy, or dense text size as a default. |

### Secondary references

| Reference | Inspected PDF pages | Useful aspect | Adaptation or reason to limit |
|---|---|---|---|
| The Elder Scrolls: Call to Arms | 7, 75, 77, 95 | Clearly titled property table and AI decision branches beside explanatory prose | Use its instructional pairing of text and decision diagram; reconstruct geometry and branches entirely from Heraldry. Parchment and blue accents are unnecessary. |
| TNA Ultimate Rulebook | 6, 10, 24 | Small grid diagrams beside procedural text; explicit corner-case panels; component overview | Make Grid Mode exceptions visible near the rule. Redraw with grayscale-safe symbols and readable labels. Its supplied PDF pages are wide spreads, not a trim-size model. |
| Pathfinder 2e Player Core Remaster | 6, 17, 257, 276, 459 | Consistent entry anatomy, highly visible hierarchy, running chapter navigation, structured index | Use stable name/metadata/body order and semantic index entries. Do not borrow action glyphs, trait mechanics, or the large coloured navigation rail. |
| Relicblade: The Seekers Handbook, second edition | 12, 25, 29, 76 | Movement examples with nearby explanatory text, small scenario schematic, illustration integrated with page space | Pair each diagram panel with its own caption and keep diagrams near the relevant rule. Use original geometry, not whimsical lettering or inherited movement assumptions. |
| Lasting Tales | 7, 33, 147 | Clear chapter banner, recurring condition headings, separated flavour sidebar, compact exploration table | Use chapter recognition and distinct prose roles. Avoid boxed parchment strips and proprietary miniature photography. |
| Ker Nethalas: Carnage & Aether | 7, 39, 141 | Monochrome heading hierarchy, restrained corner ornament, consistent creature stat and attack fields | Useful profile structure and black-and-white cohesion. Avoid too many black header bands or texture beneath dense entries. |
| The Walking Dead: All Out War | 6, 29, 98 | Worked tactical diagram panel beside corresponding explanation; separate optional-play panel | Useful for diagram-caption proximity and identifying optional text. Graphic-novel lettering and colour markers are not Heraldry's prose template. |
| XCOM: The Miniatures Game | 8, 41, 152 | Visually distinct instructional callouts, recurring section architecture, separate atmospheric mission page | Use clear callout roles and phase recognition. Avoid science-fiction interface framing and faint coloured rules. |
| FINAL - GoN - Dux Disciplinam | 8, 16 | Learn-to-play sequence, short named steps, adjacent attack modifier table | Apply to Heraldry's existing teaching material without introducing a staged rules-unlock system. |
| FINAL - GoN - Tome of Knowledge | 6, 27, 42 | Annotated movement/attack examples, repeated power-entry format | Use numbered annotations keyed to short explanations. Avoid its many colour-coded categories and dense illustrated background. |
| FINAL - GoN - Scenario Book | 8, 38 | Repeated scenario fields, compact lists, special-rules placement | Make all Heraldry scenario fields consistently locatable. Retain exact canonical scaling headers and source order; do not import GoN's fields. |
| Call of Dungeons | 7, 13, 18 | Tables adjacent to actions, side-by-side rules categories, decorative chapter edge | Keep action/table adjacency. Use fewer columns on portrait pages and lighter original ornament. |
| EAHQ | 6, 27, 93 | Many small roll/result tables within a recurring reference structure | Useful for compact random tables and reference rhythm. Avoid saturated roll columns and full-page parchment. |
| Aeon Trespass: Odyssey core rulebook v1.1 | 6, 9, 46 | Components paired with labels, recurring inline symbols, art confined to available page zones | Clarify glossary-supported symbols and illustrated setup. Heraldry should not look dependent on proprietary boards, cards, or special dice. |
| Arena Contest | 6, 22, 23 | Numbered subsection hierarchy, rules beside component examples, condition list | Useful for strong subsection relationships. Colour-conditioned labels, heavy parchment, and small text are poor defaults for this book. |
| SAS rulebook | 6, 18, 23 | Visible phase sections, diagrams next to tactical instructions, compact action table | Use phase recognition and local diagrams. Avoid modern military styling, large vertical rails, and proprietary token imagery. |
| Dungeon Universalis | 10, 40, 66 | Named rules, card examples, subsection art, differentiated rules headings | Use explicit hierarchy and relevant visual examples. Avoid decorative perimeter objects, colour-heavy headers, and card dependency. |
| Dungeoneers v16 | 6, 61 | Clean two-column rules and relatively plain explanatory table | Useful evidence that rules can remain clear with little ornament. Add stronger navigational and table polish for Heraldry. |
| Nimble Core Rules | 6, 10, 32 | Compact headings, dice example beside the rule, separated short conceptual sections | Use immediate visual explanation and concise section rhythm. Do not import its retained-dice rules or adopt a tiny tightly packed body. |
| Frostgrave | 6, 45, 124 | Distinct flavour treatment, visibly separate rules callout, dedicated illustration page | Use separation of atmosphere from reference content. Avoid faux parchment notes, repeated complex corners, and full-colour painting as Heraldry's default. |
| The Village Hunt: Veil Hollow | 6, 14, 16 | Art beside gear and creature tables; consistent roll/result entry structure | Use relevant silhouettes near bestiary/gear content. Supplied pages are spreads; evaluate each half at book-page size. Avoid its saturated creature accents and text-heavy boxed grids. |
| Dread Nights | 10, 30, 71 | Forceful display lettering, clear tonal identity, visually distinct lists and feature headings | Use tonal confidence for cover/chapter lettering only. Full black/red text fields and giant distressed headings are poor defaults for hundreds of rules pages. |

## Graphic design and hierarchy

Assign each component a job. Chapter title and art set atmosphere. A section heading directs reading. A running head locates the reader. A table helps lookup. A diagram explains geometry or sequence. A callout distinguishes an example or a source-supported exception. Ornament supports identity without creating another information layer.

Use one original heraldic motif family and one rules-diagram symbol family. Repeat a small number of marks consistently rather than generating a different decorative crest for every section. Chapter recognition can use chapter number, title, and a restrained original mark; it must not depend on colour.

Atmosphere belongs mainly on the cover, chapter openings, and relevant vignettes. Ordinary rules pages should have a stable, clean substrate. Reject permanent parchment, mottled grayscale backgrounds, wide textured borders, watermark emblems behind prose, and decorative objects crossing the text frame.

## Typesetting and text flow

The suggested roles are a readable serif for prose, a practical sans-serif for dense reference matter, and a restrained medieval display face for major headings. These are project choices, not claims about the exact fonts used in the references. The existing kit's Source Serif 4, Source Sans 3, and Cinzel are starting candidates, subject to real rendered specimens and licence checks.

Use two columns for normal short rules paragraphs and reference entries. Permit full-width tables and diagrams. Use single-column pages where a sustained procedure, complex example, or scenario benefits from one continuous reading path. Avoid repeated transitions between column counts on the same page.

Preserve semantic reading order: heading, definition or lead-in, procedure, exceptions, relevant table or diagram, then following section. Do not move an exception into a separate page's sidebar because it fits there. Do not scatter one rule across unrelated floating boxes.

Start body testing at 10.5–11 pt with 13–14 pt leading. Start tables at 9.5–10 pt and do not go below the kit's 9 pt minimum for essential content. Validate the actual x-height, glyph widths, and print-size legibility. Reject automatic type reduction as a universal solution.

Use ragged-right body text initially. If justified text is chosen after specimen testing, require language-aware hyphenation and inspect rivers and word spacing. Keep short dice expressions, costs, units, and modifiers together. Preserve required terminology, bold emphasis, ASCII apostrophes/quotes, numeric-range en dashes, ×, and −. Do not let a smart-typography pass violate the project's style lock.

## Table design: the highest-value adaptation

Heraldry's 332 reconnaissance table blocks need several related templates. The reference books show the value of compact roll columns, clear repeated headers, differentiated entry roles, and width given to explanations. They do not demonstrate that every 12-column Heraldry table will fit legibly at portrait trim.

| Family | Recommended treatment | Main acceptance check |
|---|---|---|
| Random-result table | Narrow dice/range column, generous result column, light horizontal separation | Every range and result preserved; ranges remain readable and in source order |
| Equipment and numeric comparison | Stable name column, compact aligned numbers, broad special-rule column | Values retain their original row/header relationship |
| Long prose table | Full-width two/three-column layout, or faithfully labelled entries | No squeezed prose, lost qualifier, or detached note |
| Monster profile | Name, canonical stat strip, AI Steps, Attacks, Special Abilities | Required fields and canonical order preserved |
| Power, Talent, spell, prayer, ritual, Sorcery, or Psychic Ability entry | Repeated semantic entry pattern using only fields supplied by source | No guessed cost, range, tradition, duration, or restriction |
| Scenario/scaling matrix | Full width with clear groups and repeated column headers | All canonical scaling fields and dependencies remain explicit |
| Large appendix reference | Economical typography, grouping, repeating headers, clear continuation | Reliable lookup across page breaks; complete reconciliation |

Use thin horizontal rules and light grayscale banding selectively. Avoid making every table a boxed spreadsheet. Vertical rules may be useful in genuinely complex matrices but should be exceptional. Use dark headers sparingly. Tables with dense long text often need more spacing rather than more lines.

Do not substitute visual neatness for data completeness. A card layout is acceptable only with a source-to-field mapping and a verifier covering every cell. Landscape pages are a last useful option, not a failure; preserving a readable relationship is preferable to illegible portrait columns.

## Diagrams and examples

Call to Arms contributes the idea of readable AI branches beside the exact procedural explanation. TNA contributes repeated small grid examples beside local exceptions. Relicblade contributes paired movement panels and explanatory captions. Five Leagues contributes keyed entities and a line legend. Deth Wizards and BlackDeathCity contribute simple measured setup schematics.

Create original editable vectors from Heraldry alone. Use circles/base outlines, square boundaries, patterned terrain, solid/dashed lines, arrowheads, dimensions, and numbered panels consistently. Distinguish parties and permitted/blocked geometry using redundant shapes, labels, and line styles. Never rely only on colour or pale shading.

A figure must state its instructional point. Tabletop Mode and Grid Mode require separate panels when their applicable rules differ. Do not let an attractive diagram introduce a false measurement convention, to-hit roll, AP cost, Monster Reaction, deployment assumption, or line-of-sight rule.

Examples belong near their rule and must remain recognisable as examples. Use a light outlined panel, explicit title, and verified arithmetic. Full-height dark sidebars are unnecessary. If an example is longer than its parent rule, use a full-width worked example with clear steps instead of a narrow marginal strip.

## Navigation, index, and general polish

Adopt recurring entry anatomy rather than decorative variety. A reader should find the name, costs, stats, procedure, and exceptions in predictable places. Retain exact source-defined scenario headers and Monster stat order.

Running heads should identify chapter and current major section. Put folios at the outer lower corners. Use a real linked TOC and semantic index, generated after final pagination. The index should direct a player to the operative rule and useful worked example, not indiscriminately list every occurrence of a word. Use aliases only when they point to established canonical terms; do not rename the rules.

Test left/right pages and ordinary content pages, not just impressive chapter openers. Inspect at actual print size. Check table continuations, reading order, stranded headings, awkward sentence carryovers, narrow gutter content, diagram text, grayscale contrast, clipping, unintentional empty space, and art placement. A thumbnail contact sheet is useful for rhythm and inconsistent decoration; it cannot certify small text.

## Execution strategy

1. Put the updated kit's contents at the repository root.
2. Claude reads `docs/DESIGN_SPEC.md` before the design specimen. `docs/REFERENCE_ANALYSIS.md` explains the rationale and observations.
3. Build the specimen from actual Heraldry content. Include the widest table, longest description row, numeric table, monster profile, scenario, two-column rules page, worked example, diagram, chapter opening, and index slice.
4. If visual evidence is available, inspect only the primary manifest pages relevant to the design task. Record the adopted decisions once.
5. Use secondary pages only to solve a specific remaining problem: an AI branch, grid exception, movement panel, scenario structure, or index entry.
6. Freeze the design system and build the complete book. References remain optional; missing PDFs do not block production.

For optional visuals, use `tools/render_reference_pages.py` with a local directory holding the chosen PDFs. It verifies SHA-256 and page counts, renders only manifest-selected pages, and produces local reference evidence. It can run in plan mode without PDF dependencies or source files. Missing primary sources receive an explicit status; secondary books are not required.

The guide and code are suitable repository content. Whole commercial PDFs are not included. Keep any reference excerpts separate from original art and final deliverables, and include them in a shared repository only with the necessary permission. A private repository does not itself grant redistribution rights. Original Heraldry typography, ornament, diagrams, and artwork must remain independent of these page assets.

Claude Code's current official tool documentation says PDF page-range reads render selected pages using Poppler, and image reads provide visual content. That makes targeted pages practical; it does not make reading the entire collection an efficient design process. See https://code.claude.com/docs/en/tools-reference (checked 2026-10-05). Installed capabilities should still be verified at execution.

## Final recommendation

Upload the distilled project now. Optionally supply the primary reference pages privately for visual calibration. Do not upload all 32 PDFs as a mandatory reading assignment, and do not feed them into every subagent. Establish the page grammar once, then spend the remaining production budget on Heraldry's actual tables, diagrams, pagination, and verification.
