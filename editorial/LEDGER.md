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

## Additional layout notes
* L-03 addendum: a `<br>` followed by a source newline renders as one line break.
* L-09: paragraphs consisting only of one bold label (e.g. "Initiative Phase", "APL 1–2 (d10)") are kept with the following block (run-in label); text unchanged.

## Ambiguity triage (independent review, `production/qa/ambiguity-triage.json`)

Canonical text is unchanged in every case. Section 1.6 lines: 431, 433, 435

### Resolved by Section 1.6 (3) — not open issues

* **A-01 Appendix A: centre ruin 'at the centre' vs Dispatch Satchel 'at the battlefield centre, adjacent to the centre ruin'** (FIG-18; lines 16108, 16180, 16182, 16358): Satchel is adjacent to the centre ruin (not on the exact centre point); A.11 coordinates are illustrative only. FIG-18 draws the A.11 positions and says the A.2 terrain is not drawn.
* **A-10 The Chasm Crossing: generic failed Jump (4.4.9: place at last legal point before the gap, Prone, movement ends) vs scenario 'A failed Jump into the Chasm causes a Chasm Fall'** (FIG-15; lines 1394, 1399, 13003, 13005, 13007): A failed Jump across a Ledge gap over the Chasm is a Chasm Fall (removed from play; Hero Defeated with a normal Injuries Roll; non-Hero as 0 HP; carried items lost), subject to the Hero/Hireling Fly/Climb AP option and the Monster Fly/Climb placement in 13007.
* **A-19 Audit addition (not in ledger): Impassable Terrain 'provides Cover' vs terrain table row 'Chasms and pits - Impassable Terrain - They provide no Cover'** (FIG-07, FIG-09, FIG-14, FIG-15; lines 838, 872): Chasms and pits provide no Cover; other Impassable Terrain does (FIG-07 panel F unaffected).

### Genuinely unresolved (7) — reported to the author; figures draw only the uncontested part

* **A-02 Whispering Grove: Warden placed 'adjacent to the central Standing Stone' but 3 Stones form a rough triangle** (FIG-16; lines 12088, 12062, 12100): (1) The Stone nearest the centre of the Central Clearing / battlefield. (2) The Stone that was just Interacted with (the placement trigger). (3) Random Determination among the three Stones (by analogy with 7612). (4) Any point adjacent to the centre of the triangle (reading 'central' loosely).. Impact: Low to moderate: changes the Warden's starting position relative to the Stones and Heroes (8" Entangling Roots range, who is nearest), so can sway which party the Warden pressures first. No rule contradiction; players need a house default.
* **A-03 Whispering Grove Group 2: 'perimeter of the Central Clearing, 4" from its edge'** (FIG-16; lines 12093): (1) On the perimeter circle. (2) 4" inside the edge. (3) 4" outside the clearing. (4) Anywhere in the ring from edge to 4" inside.. Impact: Low: places one Resting group; affects wake-up distances (6" movement trigger) but no figure shows it.
* **A-04 Grid Mode Cone: is the origin square 'within the cone'?** (FIG-08; lines 708, 727, 728, 741): (1) Included: the apex centre is a tie and rounds outward, so the source's own square is in the area. (2) Excluded: the cone extends away from the source, matching how Line and Aura state inclusion explicitly where intended.. Impact: Low to moderate: decides whether a Cone hits the combatant, marker or hazard in its own origin square (normally the source itself), i.e. self-damage by area effects.
* **A-07 Scenarios say only 'opposite battlefield edges' (long vs short not stated)** (FIG-13; lines 13671, 14018, 14089, 14325, 11058): (1) Long edges (East/West). (2) Short edges (North/South). (3) The Setup Roll-off winner or the players choose which opposite pair.. Impact: Low to moderate: changes approach geometry and range to objectives; both parties are treated symmetrically either way.
* **A-08 Deployment distance not stated: Sun-Drowned 2 ('converging on the plaza'), The Mire 5 ('along the outer banks'), The Mire 6 ('outside the immediate Sinkhole area')** (FIG-13; lines 13884, 14554, 14633): (1) Reuse the 6" band used by the other edge scenarios. (2) Players agree the depth. (3) Any space on the named edge/area satisfying the phrase.. Impact: Moderate for these three scenarios only: deployment depth affects early-round reach and the 6" terrain-placement buffer from a deployment zone (11068).
* **A-09 Corner zones with no stated size (Sun-Drowned 3, The Mire 3) and corner scenarios without an alternate-placement statement (Pale City 1, Sun-Drowned 3, The Mire 3)** (FIG-13; lines 13404, 13955, 14402, 12314): (1) Use the 8"x8" size of the other corner scenarios. (2) Players agree a size. For placement order: (1) alternate starting with the Roll-off loser as in other scenarios; (2) each party places its whole party in turn.. Impact: Low to moderate for those two or three scenarios: zone size and placement order affect the opening position.
* **A-18 Basic Mode: which Monster group goes at which Monster Entry marker (and who places the markers)** (FIG-19; lines 17080, 16540, 16541): (1) Players agree/alternate. (2) Random Determination (2.6.3). (3) Setup Roll-off winner chooses.. Impact: Low: markers are constrained to a 5-7" ring and are symmetric by rule, but Goblins vs Bandits near a given deployment edge changes difficulty slightly.

### Not ambiguities (9) — schematic or unspecified drawing details without rules consequence

* A-05 Grid Mode Line: tie squares at both ends and origin square
* A-06 Source ranges drawn at one value (Trail 3-4", Ravine 6-8", ledge count/length/gaps, Clearing 12-15", stone spacing 6-8")
* A-11 FIG-05 panel C: how later steps count squares already occupied by a multi-square footprint
* A-12 FIG-06: exact Grid position of the 'trigger point' for Reflex Attack
* A-13 FIG-07 panel E: Sz of the intervening combatant
* A-14 FIG-09: footprint straddling the edge point and unstated fall height
* A-15 FIG-12 panel C: ranged Monster and Blocked Route
* A-16 FIG-14: placements drawn clear of the 'within 6"' / 'within 3"' limits; Chasm Crossing 'start' edge and lateral positions not specified
* A-17 FIG-19: terrain positions, road width and which edges are deployment edges not specified

Final-content status: no unresolved direct contradiction was found; the unresolved items are source gaps (unstated values or undefined references). A full semantic audit of the whole manuscript remains NOT TESTED.
