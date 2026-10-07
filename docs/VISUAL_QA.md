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

## Specimen decision gate

Build the 8–12-page actual-content specimen specified in DESIGN_SPEC.md. Include one chapter opener and enough ordinary, dense and continuation pages to expose monotony, weak hierarchy and table failure. Do not use marketing mockups or invented rules to pass this gate. A two-column page must read down the left column then down the right; full-width components should have an obvious sequence.

Record in `production/design-decisions.md`:

1. The frozen substrate/font/spacing/rule tokens and any justified optical changes from `config/design_tokens.json`.
2. Reference lesson, exact PDF viewer page, abstract principle, original Heraldry implementation, and viewed specimen filename/page.
3. Findings by component, repairs, and evidence after rebuild. Keep visual-review status separate from successful compilation.
4. Final-size image/diagram crops and left/right normal-page evidence, plus the 1.03-scale cropped stress images.
5. Whether available artwork passes the anchor or the clean art-light route is being used.

The independent auditor reviews without relying on the designer's assertions. Assess hierarchy, flow, table craft, originality/coherence, art construction, and print behaviour. Mark each PASS/FAIL with evidence; numerical aesthetic scores are optional and cannot override a defect. Any failed essential component receives repair before bulk layout. Bounded repairs should preserve a coherent complete book rather than trigger repeated wholesale redesigns.

## Art-light acceptance

The twelve atmospheric masters are now supplied. The earlier art-light review is historical; the requested illustrated edition needs final-size placement review on cream and white. Do not fill missing illustrations with repeated generic silhouettes, decorative clip art, fake signatures, or prompts rendered as reader-facing placeholders. Keep the missing atmospheric suite visibly incomplete in the production report, while finishing the rest of the publication.

## Owner-requested refinement, 2026-10-07

Apply DESIGN_REFINEMENT.md before treating the requested visual iteration as complete. An art-light/geometry PASS remains a scoped historical result; it does not satisfy the owner's request for a less plain illustrated product.

Review every major-section/scenario start, short fit-capable table and table/entry continuation. Headings need meaningful following content; short subsections should move together where they fit. Tables require attached caption, intact rows, repeat headers and identifying continuation. Inspect wide components with the prose above/below them and reject avoidable isolated rows, detached setup/maps and unexplained lone-column voids. Keep detailed evidence for T004 and T327 and the Whispering Grove scenario. Do not classify genuinely over-height tables or deliberate section-start whitespace as failures simply because they span pages or leave space.

The requested design/pagination repairs are PENDING until implemented, rendered, reconciled and reviewed. Existing detector reports do not certify those new requirements. Record automated geometry, aesthetic review, artwork completeness and physical proof as separate statuses.
