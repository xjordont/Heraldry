# Compact layout implementation - 2026-10-20

The owner approved the researched layout proposals, specified 10.5 pt body text and 9 pt tables, corrected the margin request to narrower margins, and requested more assertive refinement. This implementation changes composition and publication tooling. RC493 manuscript bytes, rules, artwork selections, and the 57 source-bound figure reviews are preserved.

## Effective design

`config/design_tokens.json` now controls the renderer, table allocator, measurement, and geometry checks. `config/production.json` mirrors the publication values and is checked for agreement.

| Element | Effective treatment |
|---|---|
| Page | Portrait US Letter, 612 x 792 pt |
| Margins | Inside 45 pt, outside 42 pt, top/bottom 45 pt |
| Usable frame | 525 x 702 pt; two 254.4 pt columns with a 16.2 pt gutter |
| Body | Source Serif 4, 10.5 pt; 2.9 pt additive leading, approximately 13.925 pt baseline pitch |
| Tables | Source Sans 3, 9 pt; 4 pt horizontal / 2.2 pt vertical cell padding |
| Hierarchy | 50 pt chapter, 21 pt major section, 12.5 pt subsection; 9 pt captions and navigation |
| Opening flavour | Full-width flow with an 82% reading measure; ordinary rules retain two columns |
| Substrate | Flat warm cream and paper-white companions; grayscale information hierarchy |

The overall frame grows from 518.4 x 692.64 pt. The outside margin is 2.4 pt wider than the old effective margin to protect the 9 pt outer navigation; the inside and vertical margins narrow. This is a net increase in usable area. The narrower margins and smaller type are coordinated with spacing and table allocation rather than applied as independent overrides.

Table headings retain source alignment, descriptive columns receive family-specific widths, and native repeated headers identify continuations. An immediately preceding source heading suppresses a duplicate opening identity. The identity retains constant measured continuation geometry: showing or hiding its text cannot feed back into pagination. The table's top brush was removed because it crossed the identity text; the bottom rule remains. Potion and poison tables T055-T064 and equipment quick reference T332 use measured full-width layouts, with overrides bound to their exact source cells so changed content requires another measurement review. T071 remains in its existing format because widening it alone still exceeds a usable page.

A paired actual-source trial of T059 measured its heading and table at 700.025 pt with 2.5 pt vertical cell padding, versus 687.425 pt at 2.2 pt. The latter moves together to a fresh page; the former continued across pages after partial-page material. The 2.2 pt specimen was directly inspected at readable size with all 20 rows and 9 pt type intact.

Paragraph and list spacing, table insets, and panel insets are tighter. Whole list items provide safe column split points; numbered starts and nested content remain intact. Prose tails use line-level column flow when they fit. Opening headings retain substantive following content, including text after a short instruction such as "Roll 1d10.". Complete fit-capable units take precedence over balancing. A genuinely over-height unit continues through its permitted children; an oscillating balance proposal falls back explicitly to natural columns.

The figure wrapper adds no second layer of padding. A specimen did not demonstrate a fixed saving from that change because Typst already collapses the relevant spacing; no page saving is attributed to it. Figure art, caption content, and semantic approvals are unchanged. Later scenario pages repeat the source scenario title and "(continued)" in the running head. Scope ends at the next scenario or higher-rank heading; long titles shorten at a word boundary while retaining 9 pt navigation.

The final Index tab was shortened to retain a clear gap from the folio. Hanging punctuation is disabled to keep body glyphs inside the navigation-safe frame.

## Reliable measurement and verification

Position records and unit heights are serialized as PDF attachments by the same warning-aware compiler export that produces their PDF. Separate `Compiler.query` calls previously performed another layout. The replacement binds evidence to the exact PDF, generated source, complete publication inputs, compiler version, timestamp, and variant. The physical PDF's independent destinations corroborate position records. Edited sidecars, stale inputs, nonconvergence, missing coverage, duplicate markers, and avoidable splits fail closed.

The required keep inventory is enumerated from parsed source independently of the emitter's log. Every required heading unit, nested list, table, quote/example, and placed figure must be accounted for. Cream/white comparison covers glyph geometry, raster content and transforms, vector geometry, links, and outlines, rather than equal text and page count alone. Reconciliation checks complete source blocks, table cells, and emphasis. Sparse-page and paragraph-tail diagnostics support visual review. The release gate also rejects a missing, malformed, stale, contradictory, or flagged layout report.

The old page-position feedback in `keepcol` was replaced with available layout dimensions. Prose flow reserves are derived from measured text, baseline pitch, and internal headings instead of a blanket 40 pt. Regression fixtures exercise partial-page starts, nested lists, continuation headers, wrapping identities, figures, exact coin amounts, navigation clearance, and physical-page evidence.

## Comparison and completion evidence

The comparison baseline is RC493 rendered through the precompact pipeline from the saved main checkout: **673 pages**, SHA-256 `caef0c9b53e9c9127b9d46a6acd567139fb4ba946aedf75900132cf8547488c7`. It is the same manuscript as this implementation. Historical RC492-build-37 has 672 pages and is not the same-source comparison.

The final local cream and white interiors have **603 pages**, a reduction of **70 pages (10.40%)**. The digital edition has **606 pages**, including its additional front/back matter. The cream PDF SHA-256 is `bda0a463dd2c4082cfe795fc985f953dfdc7dbc80c8699c6d5a45793e79da927`; white is `da1e1347a7d148a8468611aa4b3f744b8841721a26e153a06f22d1153f3a1768`; digital is `059e1b029ced83242519d0aa373db57ac05843789954e159b8de79acf60036a1`.

| Final local check | Result |
|---|---|
| Warning-aware compiler and balancing | Converged; final build required one 38.7-second composition pass after 65.3-second measurement |
| Source-unit coverage | 2,736 expected and audited; 2,492 fit-capable; zero avoidable splits, missing units, malformed markers, or measurement errors |
| Cream and digital reconciliation | All 8,430 blocks in order; 332 tables / 10,315 cells; 22,847 bold and 447 emphasis runs; zero missing or duplicated source blocks |
| Physical page evidence | 832 independently serialized destinations agree; 536 unique source headings corroborated through 551 bookmarks; no invalid bounds |
| Layout detectors | Zero flags across all 603 pages |
| Cream/white inkjet file checks | Both PASS |
| Cream/white content and geometry | PASS: identical glyph/font/bbox geometry, rasters/transforms, vectors, links and outlines; 1,214 internal links, no unresolved targets; 274 raster placements |
| Figure semantic currency | 57/57 PASS; no stale review or open finding |
| Repository checks | 281 tests run, 3 expected skips, no failures; dependency, contract, immutable-history, and whitespace checks PASS |

All 26 contact sheets, 28 manifest details, both covers, and calibration image were directly inspected and their hashes checked against this exact PDF manifest. The integration review also inspected twelve targeted page renders, including the accepted blank p6, the Tier 5 tables, setup key, two dense scenario diagrams, corrected Triumph opening, C.14, and last Index page. The two workers covered separate halves of the book; this is not a claim of two independent whole-book reviews or glyph-by-glyph proofreading. No confirmed major visual defect was found at this review resolution.

A discarded scenario-header prototype increased compile time to 93.5 seconds and a subsequent event placement risked changing numbered-heading treatment and re-emitting metadata in running furniture. Bounded fixtures exposed both issues. The final implementation scopes lightweight events to chapters containing numbered scenarios, keeps metadata outside reusable heading bodies, and resolves each event through its actual heading anchor. Its 38.7-second final pass retains the engraved numbers and correctly scoped continuation titles. Regression checks enforce event count, title clearance, size, and closure.

Intermediate PDFs that fail convergence, reconciliation, keeps, or layout checks are diagnostics and are not accepted reductions.

## Remaining limits

Residual cosmetic density candidates include the sparse ancestry opening on p100, short genuine table continuations on pp170/186, a left-heavy Attack Sequence treatment on p75, and scenario endings on pp395/476. They do not establish a safe alternative to the current complete-unit keeps. Fresh chapter/section starts, source order, complete entries, and attached figures still take precedence over filling every blank region. The mandatory fit audit uses the documented 690 pt conservative fitting threshold within the 702 pt usable frame.

The source title "C.13 Single-Sheet Rules Summary" is retained, but its current contents span pp593-598 at the approved sizes and constraints. A literal one-sheet aid would require a separate editorial scope; shrinking or omitting its rules was not used to reduce pagination. The equipment reference now finishes entirely on p599 rather than leaving a final paragraph on another page.

The preserved local evidence directory is `build/checks/layout-v5/`. Local diagnostics do not constitute a GitHub candidate or release and do not replace the exact-PDF publication review ledger. The last delivered release remains RC492-build-37. Physical print is **NOT TESTED**.
