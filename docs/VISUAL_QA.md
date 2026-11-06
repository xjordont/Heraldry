# Visual acceptance: an authored dark-fantasy book

This is a design review rubric, not a detector of image provenance. Generated assets may pass or fail on their visible quality; do not claim a work was hand-drawn or promise that AI provenance is undetectable. The aim is specific, coherent editorial design rather than generic fantasy decoration.

Review the digital PDF: portrait Letter pages on a light cream page colour, with the front and back covers inside it.

## The intended character

Darkness comes from subject matter, ink silhouettes, and restrained heraldic vocabulary. The page remains light and quiet. The marks are the owner-approved armoury in `docs/DESIGN.md` section 12 (the castle logo, the chapter arms, the engraved shields, and the other approved marks), used at boundaries only and at most two on an ordinary page. They are decoration, never rules icons. Do not frame ordinary pages or decorate every subsection. If a setting-specific emblem is justified by the source, document its meaning before adding it.

The warm substrate, serif prose, compact sans-serif data, sparse display headings, and original ink work must look like decisions made for this manuscript. A cream background plus Cinzel and a skull is not an adequate identity. Craft is demonstrated in ordinary pages, consistent baseline/spacing, meaningful examples, well-designed long tables, and graceful continuation pages.

## Review each component

| Area | Required evidence | Reject/repair |
|---|---|---|
| Substrate | One flat almost-white cream, edge to edge; clean text | Brown wash, noisy parchment scan, burnt edges, fixed vignette, watermark crest, visible texture tiling or faint grid |
| Type | Optical hierarchy at actual size; real weights; stable spacing; correct glyphs | Heading font on body prose, arbitrary all-caps hierarchy, excessive tracking, faux bold, crushed leading, inconsistent quote/number forms |
| Page composition | Calm normal pages with an intentional reading path; relevant art; coherent left/right furniture | Every paragraph in a rounded card, symmetric poster layouts, heavy frame, giant badge/folio, decorative voids, token art filling gaps |
| Tables | Width follows information; headers and notes attach; continuations preserve row identities | Full dark slabs on every table, pale type on tint, 12 squeezed columns, missing cells, noisy grids, ornament inside data |
| Examples/scenarios | Explicit example label, subtle rule, canonical headings; setup diagram near setup | Permanent dark sidebar, invented callout taxonomy, colour-only labels, relabelled mechanics, diagrams far from their rule |
| Line artwork | Distinct purposeful subjects, plausible anatomy/construction, coherent ink method, open negative space | Generic hooded skull figure on every chapter, copied composition, random spikes/runes, fused hands/weapons, impossible straps/masonry, over-rendered digital shine |
| Artwork integration | Native masters and final-size crops; matte edges/transparent assets matching the substrate | White rectangles on cream, bright edge halo, doubled texture, muddy hatch blocks, inconsistent contour weight, art behind prose |
| Diagrams | Exact source semantics; visible line types/labels at final size; key geometry stays safe | Atmospheric hatching that obscures measurements, bitmap text, ambiguous arrowheads, false scale, colour-only party/terrain distinctions |
| Page geometry | Exact portrait Letter pages; essential content inside the 0.375 in safe area | Landscape fallback, edge-hugging folios, text or art past the safe edge, forced grayscale losing the cream |

## Specimen

Try design changes on actual-content pages before applying them across the book (`docs/DESIGN.md` section 15): the template specimens or a local proof with a chapter opener and enough ordinary, dense, and continuation pages to expose monotony, weak hierarchy, and table failure. Use real content, never marketing mockups or invented rules. A two-column page reads down the left column, then down the right; full-width components need an obvious sequence. Record frozen token changes and the reference lessons behind them as `docs/DESIGN.md` section 15 says. Assess hierarchy, flow, table craft, originality and coherence, art construction, and legibility at actual size; repair a failed essential component before bulk layout, with bounded repairs rather than repeated wholesale redesigns.

Never fill a missing illustration with repeated generic silhouettes, decorative clip art, fake signatures, or prompts rendered as reader-facing placeholders.

## Pagination review

Apply the pagination policy in `docs/DESIGN.md` (sections 8 and 13). Review every major-section and scenario start, short fit-capable table, and table or entry continuation. Headings need meaningful following content; short subsections move together where they fit. Tables need an attached caption, intact rows, repeated headers, and an identifying continuation. Inspect wide components with the prose above and below them and reject avoidable isolated rows, detached setups or maps, and unexplained lone-column voids. Genuinely over-height tables and deliberate section-start whitespace are not failures just because they span pages or leave space.

**One-page keeps:** apply the rule in `docs/PROJECT_CONTRACT.md` ("Pagination: the one-page keep rule"); the build's keep audit fails on an avoidable split.

**Pointers from the flow report:** `production/qa/layout.json` (`flow`) lists the pages to look at first. Interior voids should be none; check each one. Keep gaps are named by what was carried; check that the whole unit was worth the space. Low right-column starts and uneven chapter ends are also listed. They point to pages, they are not verdicts. The layout gate fails on a composition hairline drawn through text; never accept one.
