# Design decision log — HERALDRY SKIRMISH RC484

Frozen system (after specimen review). Reference PDFs were not available in this cloud checkout (`references/private/` absent); decisions use the written `docs/DESIGN_SPEC.md`, `docs/REFERENCE_ANALYSIS.md` principles and `config/design_tokens.json`. No reference page was viewed, so no reference-page evidence is claimed.

## Process note
The full book was generated before the formal specimen because the pipeline renders the whole manuscript in ~6 s; the specimen (`dist/specimen/`) is extracted from that actual build and the system was refined against it (fixes listed below), then frozen.

## Frozen tokens
| Token | Value | Change from config |
|---|---|---|
| Substrate | cream #FCFAF5 / white #FFFFFF, page fill to every edge | none |
| Page / margins | 612×792 pt; inside 0.875 in, outside 0.625 in, top 0.65 in, bottom 0.7 in | none |
| Columns | 2 × 3.375 in, 0.25 in gap; full-width components in flow | none |
| Body | Source Serif 4 (opsz 11 static instance) 10.5 pt, 13.5 pt baseline-to-baseline, ragged right, en-CA hyphenation | none |
| Strong | semibold (600) rather than bold, to avoid uniformly heavy pages (22,796 bold runs) | optical |
| Headings | chapter Cinzel 600 28 pt; section (H3) Cinzel 600 14.5 pt with 0.6 pt rule above; H4 Serif 600 12.5 pt; H5 Serif 700 11 pt | section 14.5 pt (spec 16–18) because many long titles wrap in a 3.375 in column |
| Tables | Source Sans 3 9.5 pt / 12 pt, semibold header, 0.75 pt header rules, 0.3 pt row rules, 6% transparent-black bands on even rows, tabular lining numerals, no hyphenation, rows unbreakable | none |
| Furniture | Source Sans 3 9 pt running heads (verso chapter, recto section) with 0.4 pt rule; folios lower outer corner | none |
| Ornament | one original broken-ring + tapered-rule motif (chapter openers, running heads, hr) | none |

## Decisions and specimen findings → repairs
1. Typst does not balance columns. Implemented in-flow two-column segments with full-width components between them, and a converging two-pass balancer (`bal`) whose height is the minimum guaranteed-fit split of prefix/suffix stacks, plus one line of slack. Overflow detector found 825 overlaps in the first attempt; 0 after repair.
2. Running heads 21 pt from the top edge failed the 0.375 in safe edge → header ascent reduced; 0 unsafe-edge flags after repair.
3. Body silently fell back to Typst's embedded Libertinus because instanced Source Serif 4 statics carried the family "Source Serif 4 11pt"; fonts re-instanced with uniform family names (`tools/make_fonts.py`); reconciliation now fails on any unexpected font.
4. Italic flavour text was double-toggled to upright (style italic wrapper + source emphasis) → wrapper removed; emphasis comes only from the source.
5. Table families (identical header signature in one section, e.g. 28 random-monster tables) now share one representation and one set of column widths; lone bold captions travel with full-width tables.
6. Hyphenation disabled inside tables (names such as "Briarling" were split).
7. Main matter starts on a recto (blank verso after contents); folio parity matches physical parity; PDF page labels i–v, 1–n.
8. Prose-heavy many-column tables (18) are labelled entries; single-row formula stat tables (34) are key/value profiles; monster stat lines (138) are compact six-field strips.
9. Chapters start on a new page, not forced recto, to avoid extra blank pages in a home-printed stack.

## Reference re-review and owner refinement — 2026-10-07

The earlier frozen-system note above describes the original cloud run, when PDFs were unavailable; it is retained as history. The ten correct original references are now on main with Git LFS and 23 selected PDF pages were visually inspected for this review. Current assignments and exact viewer-page evidence are in docs/REFERENCE_ANALYSIS.md. Earlier references outside the owner's ten-book list are no longer active design authorities.

The owner finds the latest draft too plain and requests improved sectional/table flow. docs/DESIGN_REFINEMENT.md records observed cases in the verified RC485 digital PDF (453 pages) and the next concrete component/pagination requirements. The old visual freeze is reopened for this iteration. No renderer, tokens, manuscript, artwork or PDFs were changed in this documentation checkpoint; implementation and the next visual gate remain PENDING. Preserve original review ledgers and write new hash-bound evidence after actual repairs.
