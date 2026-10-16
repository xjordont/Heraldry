# RC493 semantic delta review: FIG-06, FIG-11, FIG-12

Reviewer: Codex RC493 figure delta reviewer, the same model-family worker that drafted the bounded source-proof proposals. Date: 2026-10-15. This is an actual source, SVG, caption, and standalone-render review; it is not an independent human review or a review of final PDF placement.

Active source: `source/Heraldry_RC493.md`, SHA-256 `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`.

Result: **PASS_WITH_NOTES for all 3 figures; 0 open major/critical findings; 3 new open minor findings.** Existing resolved and accepted findings are preserved below. No geometry change is required by the RC493 delta. The copy/typography notes are follow-up proposals, outside the ten approved manuscript replacements.

## Method and limits

Read the current `AGENTS.md`, `CLAUDE.md`, and `docs/CANON_AUTHORITY.md`. Compared RC492 against RC493, inspected the configured source dependencies and complete governing passages, read each actual SVG's text and configured caption/anchor, and read the prior semantic-review entries. Used `tools/figure_review_gate.current_hashes()` for the current SVG, UTF-8 caption, and dependency-section hashes below.

Each unchanged current SVG was rendered separately through the installed `typst.compile(format="png", ppi=144)` with repository fonts. Each specimen places the SVG at its 504 pt width and includes the actual configured caption underneath. **All three resulting PNGs were directly viewed.** The specimen caption uses Libre Baskerville at 9 pt; it is an inspection wrapper, not a reconstruction or approval of the book's caption styling or placement. No PDF, full-book build, figure regeneration, shared ledger edit, source edit, or artwork edit was performed.

The RC493 changes within these dependencies are limited to:

- **5.1, line 1456:** `if they are adjacent` becomes `if it is adjacent` in the Engaged definition.
- **9.5 C, line 7628:** `their Primary Target` becomes `its Primary Target`, and `says they continue` becomes `says it continues` in the script's introductory paragraph.

Other approved RC493 changes are outside these figures' dependency sections. The review conclusions below come from the actual diagrams and rules, not solely from unchanged SVG/caption bytes.

## FIG-06: Engagement, Reach and Reflex Attack

**Verdict: PASS_WITH_NOTES. New open findings: 0. Open major/critical findings: 0.**

Dependencies: **2.6.1**, **4.4.4**, **5.1**, **5.5.4**. Complete governing passages read: RC493 lines 629-647, 1332-1343, 1454-1485, and 1677-1688. Configured caption anchor: `B01466`, beside the Reach/Engagement discussion.

Observed in `ai-FIG-06.png`: Panel A has the 5-by-5 melee-band grid with 8 adjacent squares and the outer Reach band. Numerals 1 and 2 distinguish the unoccupied band squares as well as grey tone. The Party B token is diagonally adjacent to Party A; the Monster token is in the outer band and does not Engage. The text explicitly distinguishes Tabletop melee 1 inch/Reach 2 inches, says Reach does not change Engagement, and keeps the Grid square-band exception separate from diagonal movement cost. These remain faithful to 5.1 after the pronoun correction.

Panel B contrasts a Move leaving the enemy melee band with a 1-inch Shift leaving it. The Move's trigger marker is on the last illustrated square within the melee band, with text saying the Reflex Attack resolves before leaving, costs 1 AP, and rolls base damage dice with Disadvantage. Shift and forced movement are explicitly excluded. The caption agrees with those displayed cases. All observed labels, arrows, numerals, legend items, and caption are readable without clipping in the standalone render.

Prior findings rechecked:

- **Resolved minor retained:** band numerals are present; the distinction does not rely on grey tone alone.
- **Accepted minor retained:** the exact boundary trigger point is represented by the last square inside the melee band. The explicit before-leaving text agrees with 2.6.1 and 5.5.4; the diagram does not change the Declared State procedure.

RC493 impact: the antecedent in the Engaged definition changed grammatically, while adjacency, Reach, and trigger mechanics did not. The displayed relationship remains correct. No diagram or caption change is needed for this delta.

## FIG-11: Standard Monster AI Script

**Verdict: PASS_WITH_NOTES. New open minor findings: 2. Open major/critical findings: 0.**

Dependencies: **3.4.3**, **9.5**. Complete governing passages read: RC493 lines 1113-1120 and 7592-7673. Configured caption anchor: `B07636`, at the end of the Standard Monster AI Script.

Observed in `ai-FIG-11.png`: Five condition boxes run from AI Step Abilities through Engaged, Visible Target, Search, and No Visible Target. Yes arrows lead to the appropriate outcome; no arrows lead down to the next condition. The preface states first valid instruction, re-evaluation of an illegal Primary Target, scenario Target Priority first, and no Monster AP. The first outcome also states the explicit continuation exception. The Engaged outcome gives lowest HP, then Most Recent Attacker, then random; it permits the listed Multi-Attack or otherwise the legal attack type. The Visible Target outcome includes the legal firing-position branch. Search correctly gives the DEX Check to the enemy's controller and ends the activation. It does not assign a Check to the Monster. The final outcome refers to Movement Priorities. These are faithful summaries of current 9.5; omitted attack-selection details and tied Search targets remain governed by the cited full rule.

The rendered labels, text boxes, connectors, and actual configured caption are legible without overlap or clipping. The source pronoun change does not alter first-valid-instruction semantics, but the actual SVG still contains the older pronoun wording noted below.

New minor findings, both **open**:

1. **RC493-F11-M01 - Singular Monster pronoun remains in SVG preface.** Actual SVG text at `x=5, y=33.98` reads `instruction and ignores the rest unless a rule says they continue. Monsters do not use AP.` Current 9.5 C at line 7628 uses `it continues`. Proposed narrow follow-up: replace `unless a rule says they continue` with `unless a rule says it continues` in the figure generator and regenerated SVG. This is copy alignment; no AI behaviour changes.
2. **RC493-F11-M02 - Caption states unconditional activation end.** The actual configured caption begins `The Standard Monster AI Script: a Monster executes the first valid instruction and its activation then ends.` Current 3.4.3, 9.5 C, and 9.5 D preserve explicit continuation exceptions. The prominent SVG preface and AI Step outcome already print the exception, so the combined specimen supplies the correct rule; the caption alone is overbroad. Proposed narrow follow-up: replace that first sentence with `The Standard Monster AI Script: a Monster executes the first valid instruction and its activation then ends unless a rule explicitly says it continues.` Preserve the caption's second sentence. Review any changed wrapping at the next requested build.

The prior figure entry had no findings. Neither new issue blocks the diagram's semantic delta review, but both must remain visible as unresolved minor copy issues. No correction was enacted in this review.

## FIG-12: Primary Target, tie-breakers and Blocked Route

**Verdict: PASS_WITH_NOTES. New open minor findings: 1. Open major/critical findings: 0.**

Dependency: **9.5**. Complete governing passage read: RC493 lines 7592-7673, especially A, C, E, and F. The complete terrain-type passage at 832-879 was also read for the depicted Impassable Terrain. Configured caption anchor: `B07662`, at the Blocked Route paragraph.

Observed in `ai-FIG-12.png`: Panel A depicts the nearer Hidden enemy being excluded and the nearest visible enemy receiving the Primary Target marker. Panel B identifies HP 4 and HP 7 as example values at equal distance and presents lowest HP, Most Recent Attacker, and Random Determination in the proper order. The Most Recent Attacker description includes both HP damage and HP loss. Panel C surrounds the initial enemy with Impassable Terrain, leaves its sight line visible, and directs the melee Monster toward another reachable visible enemy. Its body text explicitly qualifies the case as a melee Monster and an attack possible this activation. The displayed labels, badges, grid, arrows, key, and actual caption are readable without clipping.

This agrees with 9.5 E/F provided the stated melee Monster can reach and attack the second enemy this activation. Current 2.9.1 at line 838 confirms Impassable Terrain does not itself block LOS. The caption is a short summary; the body preserves the activation/attack qualification. The pronoun-only edit to 9.5 C does not change the target or route examples.

Prior findings rechecked:

- **Resolved minor retained:** badges 1 and 2 sit beside the ringed enemy and reachable enemy; `melee Monster` is printed in Panel C.
- **Accepted minor retained:** Panel C assumes the melee/reachability case. A ranged Monster with a legal firing position uses the more specific firing-position rule; the diagram does not claim to depict that case.

New minor finding, **open**:

1. **RC493-F12-M01 - Four em dashes violate the rulebook typography lock.** The actual SVG contains U+2014 at Panel A `x=0, y=205` and Panel B `x=194, y=153`, `191.2`, and `250.6`. They are visible in the inspected render. Proposed narrow follow-up replacements are `Schematic — not to scale` to `Schematic - not to scale`, `Lowest current HP — HP 4 is` to `Lowest current HP - HP 4 is`, `Most Recent Attacker — the tied` to `Most Recent Attacker - the tied`, and `Random Determination — among` to `Random Determination - among`. Apply through the generator, then inspect changed SVG text and wrapping. This is one repeated typography issue at four locations, not four semantic defects.

No targeting, tie-break, or geometry change is needed for the RC493 delta. No correction was enacted in this review.

## Exact reviewed hashes

These values came from `figure_review_gate.current_hashes()` while RC493 was active:

```json
{
  "FIG-06": {
    "svg_sha256": "95b6280c207fe96d78d386a2f3662ce4a93a59f93fdc40051f9d04a7d177b8e8",
    "caption_sha256": "2b64538ff90d7b6bf81b00fc10ab6af2508ff75c98b78c44ddb2309b98f3604c",
    "rules_sha256": "54b70505eeac96080a0001de5bef77e11dd62232e2cdd6931e01324832267132"
  },
  "FIG-11": {
    "svg_sha256": "1e5f3f6044822265041b4b981aa80478f44121742703d6a8d498837e929fe930",
    "caption_sha256": "8da7d89daaa60fbf9f01e91971cfa7dafd10c016db63e670bc9fd22b6ce3ae01",
    "rules_sha256": "f9d695a6b8ceb164269fee683d9b62b9426d4d322693aa0511d7f5b752e879fe"
  },
  "FIG-12": {
    "svg_sha256": "4e71c511ba9a4939192f2e7f50ffe9cbea30b36f65edf35351ac6aea66925395",
    "caption_sha256": "945896acf9d3b54252f47c392792c1f06dae616e04a3d44d2f388600297b457d",
    "rules_sha256": "2eee4832b5377f529b7c048e4ee932be50481c22deb1a42bec3d18fa316aef91"
  }
}
```

| Figure | Directly viewed render | PNG SHA-256 |
| --- | --- | --- |
| FIG-06 | `build/checks/RC493/ai-FIG-06.png` | `e4d5fe527656d1c7431d249a763555805d9851e82cd3a06011f447e6b798c401` |
| FIG-11 | `build/checks/RC493/ai-FIG-11.png` | `f272161d74acb8cdfa896d8a1bba4e63211fab025c2ce1ea57705b0d4b36c8c5` |
| FIG-12 | `build/checks/RC493/ai-FIG-12.png` | `3eb528d807908d3b37c77d4c80df2966ed85bf35c8e538f3a37fdec2bac65a82` |

The corresponding specimen files are `ai-FIG-06.typ`, `ai-FIG-11.typ`, and `ai-FIG-12.typ` in the same ignored folder. Their SHA-256 values are respectively `b7a8da1570c7022269449daada8fcbe289375dc82e75079b70e9c4c58ec5a6bb`, `930d397ea2abe99e1811a7ce45dc5c9f6ff80e9f1add2c4df53ab35d4d90782d`, and `375350978e604dc3eb100125792e442bd842235bebaf815e516329bc9c79a0b1`.

Root may bind only these reviewed SVG/caption/rules combinations and retain the 3 open minor findings. This record does not sign off final pagination, book-level figure/caption placement, PDF accessibility, glyph-level full-book copyediting, or physical print/binding. Physical proof remains **NOT TESTED**.
