# Editorial ledger — RC484 publication layer

Canonical source: `source/Heraldry_RC484.md`, SHA-256 `2744833106569e6b20f6913340de5d80c7869782556e23b8f738a0407e4f16f3` (verified on every parse).

## Applied source patches

None. `editorial/patches.json` is empty; the publication text is byte-identical to the manuscript at the inline-text level.

## Layout-only transformations (not text changes)

| ID | Transformation | Scope | Evidence |
|---|---|---|---|
| L-01 | Manual Markdown table of contents (source lines 9–159, 149 links) replaced by the generated, page-numbered, linked contents and PDF bookmarks | front matter | `production/mappings/blocks.json` rows tagged `replaced-by-generated-toc` |
| L-02 | Title block (H1, subtitle, version line) set as a designed title page; H1 "HERALDRY SKIRMISH: THE DYING LANDS" displayed on two lines without the colon; the full title is kept in PDF metadata and the colophon | title page | `front-matter-title-page` |
| L-03 | Soft line breaks (671, all preceding a bold field label, plus one before an italic run) rendered as line breaks, following the author's one-field-per-line structure | body | `production/inventory/summary.json` (`inline_soft`) |
| L-04 | No-break spaces inside dice expressions, `[n AP]`, `n AP`, `STR +n`, `APL n–m`, `Round n` | body/tables | `tools/build_book.py` `NOBREAK` |
| L-05 | Chapter-final horizontal rules (`---` immediately before the next chapter) absorbed by the chapter page break; other rules rendered as the ornament | 42 rules | `hr-absorbed-by-chapter-break` |
| L-06 | First italic paragraph of a chapter set as the chapter-opening lead | chapter openers | `chapter-lead` |
| L-07 | 18 prose-heavy many-column tables set as labelled entries (cards); 34 single-row stat tables with formula cells set as labelled key/value profiles; 138 monster stat lines set as stat strips | tables | `production/mappings/tables.json` (`rep`, `field_map`) |
| L-08 | Lone bold caption paragraphs and headings immediately preceding a full-width table travel with that table | 38 full-width tables | `full-width-caption` |

## Mechanical audits performed (no defects requiring patches)

* Section-citation audit: 633 numbered section citations resolve to existing headings; no duplicate or gapped section numbers (`production/qa/xref-audit.json`).
* All 149 manual-TOC links resolve to heading anchors (parser fails on unresolved links).
* Table structure: 332 tables, no ragged rows (`production/inventory/summary.json`).
* Constructs: no images, code blocks or unsupported HTML; 18 `<br>` elements, 1 block quote; parser raises on unsupported constructs.

## Rules ambiguities / contradictions

No full semantic contradiction audit of the 241,000-word manuscript has been performed in this build. Ambiguities found while drawing figures are listed in `figures/manifest.json` (field `ambiguity`) and summarised here when present. Final-content status therefore remains qualified: no known unresolved contradiction, full rules audit NOT TESTED.
