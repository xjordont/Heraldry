# Visual acceptance: an authored dark-fantasy book

This is a design review rubric, not a detector of image provenance. Generated assets may pass or fail on their visible quality; do not claim a work was hand-drawn or promise that AI provenance is undetectable. The aim is specific, coherent editorial design rather than generic fantasy decoration.

Review the borderless portrait Letter home-inkjet edition, including its light cream and paper-white variants, under the shared INKJET_PRINT.md file contract.

## The intended character

Darkness comes from subject matter, ink silhouettes, and restrained heraldic vocabulary. The page remains light and quiet. Choose one original motif: a broken ring with a short tapered rule, executed as simple editable vector strokes. Use it sparingly at chapter openings and running navigation. It is decoration, never a rules icon. Do not build a page frame or decorate every subsection. If a setting-specific emblem is justified by the source, document its meaning before adding it.

The warm substrate, serif prose, compact sans-serif data, sparse display headings, and original ink work must look like decisions made for this manuscript. A cream background plus Cinzel and a skull is not an adequate identity. Craft is demonstrated in ordinary pages, consistent baseline/spacing, meaningful examples, well-designed long tables, and graceful continuation pages.

## Review each component

| Area | Required evidence | Reject/repair |
|---|---|---|
| Substrate | One flat almost-white cream, edge to edge; white-stock variant; clean text | Brown wash, noisy parchment scan, burnt edges, fixed vignette, watermark crest, visible texture tiling or faint grid |
| Type | Optical hierarchy at actual size; real weights; stable spacing; correct glyphs | Heading font on body prose, arbitrary all-caps hierarchy, excessive tracking, faux bold, crushed leading, inconsistent quote/number forms |
| Page composition | Calm normal pages with an intentional reading path; relevant art; coherent left/right furniture | Every paragraph in a rounded card, symmetric poster layouts, heavy frame, giant badge/folio, decorative voids, token art filling gaps |
| Tables | Width follows information; headers and notes attach; continuations preserve row identities | Full dark slabs on every table, pale type on tint, 12 squeezed columns, missing cells, noisy grids, ornament inside data |
| Examples/scenarios | Explicit example label, subtle rule, canonical headings; setup diagram near setup | Permanent dark sidebar, invented callout taxonomy, colour-only labels, relabelled mechanics, diagrams far from their rule |
| Line artwork | Distinct purposeful subjects, plausible anatomy/construction, coherent ink method, open negative space | Generic hooded skull figure on every chapter, copied composition, random spikes/runes, fused hands/weapons, impossible straps/masonry, over-rendered digital shine |
| Artwork integration | Native masters and final-size crops; matte edges/transparent assets matching the substrate | White rectangles on cream, bright edge halo, doubled texture, muddy hatch blocks, inconsistent contour weight, art behind prose |
| Diagrams | Exact source semantics; visible line types/labels at final size; key geometry stays safe | Atmospheric hatching that obscures measurements, bitmap text, ambiguous arrowheads, false scale, colour-only party/terrain distinctions |
| Inkjet output | Exact portrait Letter pages; text safe zone; cropped 1.03-scale stress review | Landscape fallback, larger bleed sheet, crop marks, edge-hugging folios, forced grayscale losing the cream, untested device claims |

## Specimen

The 8–12-page actual-content specimen in DESIGN_SPEC.md (a chapter opener and enough ordinary, dense, and continuation pages to expose monotony, weak hierarchy, and table failure) is the place to try design changes before bulk layout. Use real content, never marketing mockups or invented rules. A two-column page reads down the left column, then down the right; full-width components need an obvious sequence. Record frozen token changes and the reference lessons behind them in `production/design-decisions.md`. Assess hierarchy, flow, table craft, originality and coherence, art construction, and print behaviour; repair a failed essential component before bulk layout, with bounded repairs rather than repeated wholesale redesigns.

Never fill a missing illustration with repeated generic silhouettes, decorative clip art, fake signatures, or prompts rendered as reader-facing placeholders.

## Pagination review

Apply DESIGN_REFINEMENT.md. Review every major-section and scenario start, short fit-capable table, and table or entry continuation. Headings need meaningful following content; short subsections move together where they fit. Tables need an attached caption, intact rows, repeated headers, and an identifying continuation. Inspect wide components with the prose above and below them and reject avoidable isolated rows, detached setups or maps, and unexplained lone-column voids. Genuinely over-height tables and deliberate section-start whitespace are not failures just because they span pages or leave space.

**One-page keeps:** every complete scenario, section or subsection, table, example, procedure, stat profile, or reference entry that fits within one empty usable page at its approved width occupies exactly one physical page, with its heading, nested content, caption, legend or deployment diagram, and necessary notes. If the remaining space is insufficient, move the whole unit to the next page; don't split it to fill space or balance columns. A column limit is not proof that a unit cannot fit: use the approved full-width layout where appropriate. Keep type legible and all content present. The build's keep audit checks every applicable unit (DESIGN_REFINEMENT.md) and fails on an avoidable split.
