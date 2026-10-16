# RC493 core figure review and repairs: FIG-01 to FIG-19

Reviewer: Codex core-figure worker, 2026-10-15. The reviewer also authored the repairs described here; this is not an independent human review.

Source: `source/Heraldry_RC493.md`, SHA-256 `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`. The current contracts and `docs/CANON_AUTHORITY.md` governed the review. No manuscript text or mechanic was changed.

**Result: 19 figures directly reviewed; 0 open major/critical findings and 0 new open minor findings after repairs.** Accepted schematic limitations remain qualified below. Every current SVG text element in this set is at least 9 pt at its intended 504 pt width. This result does not approve the final book layout, physical reproduction, or full-book accessibility.

## Actual inspection and evidence

Rendered every baseline SVG with a caption and directly viewed every final figure after regeneration at **504 pt width, 200 ppi**. The final inspection wrappers use the repository fonts, a near-white background, and the actual current `figures/src/figdata.py` caption at 9 pt in a caption band. All figures were viewed individually. FIG-08, FIG-11, FIG-12, FIG-18, and FIG-19 were inspected again after their last repairs; no unseen render is described as reviewed.

Final inspection artifacts are `build/checks/RC493/core-final-FIG-01.png` through `core-final-FIG-19.png`, with their `.typ` wrappers. Exact source, SVG, caption, rules-dependency, and PNG hashes are in the accompanying `figure-review-core-rc493.json`; the PNG hashes are also listed below. The caption hashes describe the captions actually rendered from `figdata.py`. Root integrates their matching placement entries and verifies the regenerated SVG/caption/rules hashes before updating the shared ledger.

The worker edited only its allocated generator modules and generated SVG subset. Root owns shared captions, metadata, shared rendering helpers, the semantic ledger, tests, and integration. SVG generation was restricted to FIG-01 through FIG-19; no book or PDF was built.

## Per-figure findings and outcome

| Figure | Governing source | Actual final observations and action | Verdict |
| --- | --- | --- | --- |
| **FIG-01** | 3.1-3.5 | Four phase cards, intervening arrows, next-round loop, and reversed Party/Monster exception are readable. Regeneration removed duplicated badge overdraw in the checked-in SVG, restoring one white circle and black numeral per phase with better contrast. Phase timing is unchanged. | PASS |
| **FIG-02** | 2.5; 3.3-3.3.2; 4.2; 4.5; 5.5.1 | Added the existing Stunned/Sleeping 0 AP activation exception and the cannot-perform-an-action branch. Qualified the below-1-AP reminder so it does not contradict that exception. Preserved the 3 AP example, shield assumption, slashing Block trigger, and spent/unspent squares. Cost chips now use bracket notation. Both columns remain readable without overlap. | PASS |
| **FIG-03** | 5.1.1; 5.2; 5.3; 5.4.3 | Mitigation now includes flat mitigation and reduction in the source's listed type order. The worked 6 slashing/4 fire and 9 slashing cases retain all source numbers and results. Replaced the non-applicable fire AV dash with None and normalised minus signs. The five attack stages, Total Miss note, tables, and captions are readable. | PASS |
| **FIG-04** | 2.6; 2.6.1 | Closest-point Tabletop measurement, Grid 1.5 + 1.5 + 1 = 4 inches, S/M/L/H footprints, and the Declare/Verify/Move/Declared State sequence agree with the source. Corrected singular combatant pronouns and schematic punctuation. No geometry change was required. | PASS |
| **FIG-05** | 2.6; 2.9.3; 4.4.3; 4.4.7 | Running totals 1, 2.5, 4, 5, and forbidden 5.5 are legible. The forbidden corner example has both orthogonal intermediate cells blocked; the permitted case leaves one open. Difficult Terrain costs and the Large-footprint destination cost remain correct. | PASS_WITH_NOTES |
| **FIG-06** | 2.6.1; 4.4.4; 5.1; 5.5.4 | Adjacent and Reach rings retain numeric labels, correct enemy relationships, and the Move/Shift contrast. The text states 1 AP, Disadvantage, and before-leaving timing. No semantic or geometry repair was required. | PASS_WITH_NOTES |
| **FIG-07** | 2.7.1; 2.7.2; 2.8.4; 2.9.1 | All six LOS/Cover panels remain readable: blocking interior, shared Blocking corner, Cover interior, touched corner, intervening combatant, and Impassable feature. Restored the explicit Areas of Effect/hazard Cover exception in the footer. The post-Shift line clears the intervening combatant. | PASS_WITH_NOTES |
| **FIG-08** | 2.7.3; 5.1.1; 5.4.3 | Retained the 13-square single-source Aura and 7-square cone counts and the blocked-square example. Added the originating-combatant exception qualifier and a full-width Aura-source note distinguishing point sources from combatant footprints/every occupied source square. The shared-roll flow now explicitly orders Reaction, AV determination including applicable AD, AV/flat mitigation, then Immune/Resistant/Vulnerable. The longer final box remains readable at 9 pt. Shared caption now qualifies the single source square. | PASS |
| **FIG-09** | 4.4.6; 4.4.7; 5.6.1 | Push/Pull/Slide direction examples, stopping before solid obstructions, no automatic Collision damage, and the 3-inch push/2-inch ledge example agree with the source. Fall damage is not invented. No repair was required. | PASS_WITH_NOTES |
| **FIG-10** | 9.3; 9.4; Hide distance in 5.9 | Added the omitted Hidden-retention rule and the explicit rule-based visibility exception for Hidden/Invisible enemies. Resting/Awake state transition, the five wake triggers, and blocked-LOS/distance examples remain readable and correct. | PASS |
| **FIG-11** | 3.4.3; 9.5 C-F | Corrected the singular Monster continuation pronoun. Search now explicitly says that enemy loses Hidden, and refers to 9.5 E for equal-distance ties. Root corrected the caption's continuation exception. All five yes/no branches, controller DEX Check, and no-AP instruction remain legible. | PASS |
| **FIG-12** | 9.5 A, C, E, F | Removed four em dashes. Nearest-visible selection excludes the nearer Hidden enemy; HP 4/HP 7 are labelled examples; Most Recent Attacker includes HP loss. The blocked route is explicitly a melee case. Root aligned the caption to the this-activation attack-position condition. | PASS_WITH_NOTES |
| **FIG-13** | 10.1; all 36 Party Deployment paragraphs in 10.4 | Re-read all 36 deployment paragraphs and the default procedure. The five illustrated edge/corner patterns, 6-inch depths, 8-by-8-inch corners, and placing-order explanation agree with current source. Boards and labels remain readable. No geometry change was required. | PASS |
| **FIG-14** | Bandit's Toll 12132-12170; Chasm Crossing 12965-12997; Quake 13035-13062; Spider's Silk Route 12209-12238 | Added the source's only-Hero exception to the Trail panel; root added it to the caption. Retained 8-inch shared-edge deployment, 6-inch opposing-Hero separation, 8-by-8-inch Safe Zone with 3-inch separation, and Ravine deployment. Normalised the apostrophe. Dimensions and centre-detail labelling remain readable. | PASS_WITH_NOTES |
| **FIG-15** | Chasm Crossing 12945-13014; Jump 4.4.9 | Survey Map/Stone placement, Speed penalty, ledge/gap ranges, failed Jump reference, Chasm Fall, and Fly/Climb exceptions agree with the scenario. Corrected singular pronouns and schematic punctuation. The scenario-specific removal/recovery procedure remains distinct from generic Falling. | PASS_WITH_NOTES |
| **FIG-16** | Whispering Grove 12042-12111; 9.5 E | Warden appears beside the first interacted Stone and targets the latest valid interacting Hero. Roots still checks the 8-inch range and not-Immobilized condition. Group 2 is inside the Clearing, 4 inches from its edge. Corrected the printed apostrophe; no encounter or position rule was changed. | PASS_WITH_NOTES |
| **FIG-17** | 11.2; 11.2.1; 11.2.3; 11.2.4 | Campaign phases, return Journey timing, Town checklist, six locations, default 4 TAP, Journey modification, and unless-stated-otherwise qualification agree with current authority. All phase cards and location rows are legible. No repair was required. | PASS |
| **FIG-18** | A.1-A.4; A.7-A.9; A.11 | Reordered Senna's row so Mara declares Dodge before damage generation. Preserved every fixed die, modifier, AP square, and HP result. Corrected Edric/Mara pronouns and minus signs. Expanded the compact key to A = Awake, without shrinking type. The board/inset distinction and unspecified-position notice remain explicit. | PASS_WITH_NOTES |
| **FIG-19** | B.1; B.4 Ironscar; B.5; B.6 | Default 3-group random assignment, 5-7-inch entry band, 4-inch deployment, Strongbox/Satchel values, Speed reduction, pickup AP, and 21c assumed example agree with source. Expanded the key to R = Resting. The Group label is on open space with a leader, not on the cart hatch. | PASS_WITH_NOTES |

## Historical findings re-evaluated

These are current observations, not an automatic carry-forward of old review prose.

- **FIG-02 old Block trigger omission:** remains resolved; the source's slashing trigger and shield assumption are printed. The activation exception issue found in this pass is also resolved.
- **FIG-03 accepted mitigation-summary omission:** resolved by the explicit AV/flat-mitigation and listed-type-order text.
- **FIG-05 previous 6.5 arithmetic defect:** remains resolved at 5.5. Its accepted generic Large-combatant example using Monster hatching remains valid: the destination-cost rule applies to every combatant, and the text does not grant a Monster AP or an ability score.
- **FIG-06 grey-only bands:** remain resolved by numerals. The accepted trigger marker on the last illustrated square inside the melee band remains a schematic representation of before-leaving timing, not a new Grid coordinate ruling.
- **FIG-07 old post-Shift line/generic Impassable issue:** remain resolved. Its accepted same-or-larger-Sz qualification is printed in the panel, so the example remains valid.
- **FIG-08 prior originating-combatant/origin-square inference:** remains resolved; the text refers to the combatant, not immunity for an entire origin square. New explicit source-footprint and exception qualifiers remove additional ambiguity. The shared damage mitigation order was repaired and re-inspected.
- **FIG-09 accepted edge-point marker and omitted fall height:** retained; the figure does not invent a fall height or damage result.
- **FIG-10 accepted omitted Hidden/visibility clauses:** resolved; both retention and explicit visibility exceptions are now printed.
- **FIG-11 prior open pronoun and unconditional-caption issues:** resolved. Search's controller/enemy antecedent and tie handling were clarified and re-inspected.
- **FIG-12 prior badge/Monster-type issue:** remains resolved. Its accepted melee-Monster scope remains valid and visible. The four open em-dash occurrences are resolved, and the caption now retains the legal this-activation attack-position condition.
- **FIG-13 old depth/size/order attribution findings:** remain resolved by the current 10.1 default explanation, checked against all 36 deployment paragraphs.
- **FIG-14 accepted range values and schematic lateral positions:** retained and disclosed. The printed examples avoid claiming an exact-boundary interpretation of within 3 or 6 inches. The omitted only-Hero exception is now resolved.
- **FIG-15 accepted schematic ledge/Chasm proportions and omitted Chests:** retained; the drawing is explicitly schematic and illustrates the crossing, not complete scenario setup.
- **FIG-16 accepted small visual Warden/Stone gap:** retained as a schematic depiction consistent with Tabletop adjacency within 1 inch; it does not impose contact or a new 8-inch measurement. Other Groups are expressly not drawn.
- **FIG-18 prior accepted fixed-roll arithmetic:** rechecked and unchanged. Its vague historical note about a Satchel label north of the ruin is not a current observation: the current label is below the Satchel. The stated unfixed side/terrain arrangement remains a valid disclosed limitation. The open late-Dodge narration is resolved.
- **FIG-19 old Group-label-over-hatch complaint:** resolved/superseded; the current label is over open space. The 5-7-inch band annotation remains readable with its backing. Entry-group/Satchel marker displacement is expressly for legibility. Default group assignment, extraction arrows, and the defeated-Monster score wording remain resolved.

## Verification and remaining limits

- Parsed and syntax-checked the six allocated Python modules; LF line endings preserved.
- Checked all 19 SVGs and their rendered captions with the root's visible-typography validator; no violations found. Checked every SVG text element for the 9 pt minimum.
- Rechecked the existing Grid distance, 13/7 template counts, mitigation, initiative, AP/HP, and 21c arithmetic without inventing or rolling new results.
- Directly observed final text, arrows, hatching, keys, and caption wrapping; no clipping or semantic blocker found at the reviewed width.
- Root owns full regeneration/reproducibility, complete tests, dependency/anchor reconciliation, and shared ledger integration. The report's 19 source/figure pairs do not certify unrelated figures.

No full-book typesetting or PDF was rendered. Downstream pagination, binding/gutter access, actual inkjet reproduction, accessibility reading order, and physical print remain outside this inspection. Physical proof: **NOT TESTED**. A later requested book build requires its own actual final-page review.

## Final inspected PNG hashes

The following table is generated from the inspected evidence record. Each path is in `build/checks/RC493/`.

| Figure | Inspected PNG | SHA-256 |
| --- | --- | --- |
| FIG-01 | `core-final-FIG-01.png` | `3aa5d7ea53913263b54b0dd4bc5446895e9c05ad24cd57450bf7e257c1509ffa` |
| FIG-02 | `core-final-FIG-02.png` | `b071692a3506b636eea866fa3d6ce67dc1b826d24c8a7509c62c69fb123fb742` |
| FIG-03 | `core-final-FIG-03.png` | `9db377f26f6317527f3012830c41053401aa23591648587d3ca83968882ef8f4` |
| FIG-04 | `core-final-FIG-04.png` | `37604b37492d214e240c61e9e83e5a1937a281beff638ae2e087680c8a89e960` |
| FIG-05 | `core-final-FIG-05.png` | `1ef5d919e046562f255c1d759b18eb4d6515824fb495c1733db8d09103f0825b` |
| FIG-06 | `core-final-FIG-06.png` | `529e9a150b5f2ae98762382d5827fb2b0e451c0631a027dcf2b474fc9ad5f523` |
| FIG-07 | `core-final-FIG-07.png` | `9b8585d92047de9963836c217a4e3dba4c527136e638ec168703753059e92e60` |
| FIG-08 | `core-final-FIG-08.png` | `fede2b14df8c3ad2a757239d2b89fbeb69702fd83c5e1daa70dd5de0f8284717` |
| FIG-09 | `core-final-FIG-09.png` | `bbe112659d11f1bd6a8ddeba55c136b72a84d525573c8fd01a160a43aebc290d` |
| FIG-10 | `core-final-FIG-10.png` | `ab4d10405e6fba39f300a8c95d5931ccf58491b1ee6805c7a51b8e30f2f8ae13` |
| FIG-11 | `core-final-FIG-11.png` | `c534cebd497bfd4a53c39b428bdcbbf58594a980f408bee6c1792768a2f685b7` |
| FIG-12 | `core-final-FIG-12.png` | `89c10cc6de20d1c2049b271b4c3c209e8be365d375d234b2561239f120cf9918` |
| FIG-13 | `core-final-FIG-13.png` | `52578cc6300e583acfd45d27a976ffe1511983f46e174cc14c114fe129ed0427` |
| FIG-14 | `core-final-FIG-14.png` | `a11dda4623d30e95216eb662273b21aa1c94148372b8a97d8be2f189bdd73bb6` |
| FIG-15 | `core-final-FIG-15.png` | `4154b3c737979555ba91f78a22f8ee75b6f1691a7529f42e8815558c36aafb0d` |
| FIG-16 | `core-final-FIG-16.png` | `c6d31c2b38bf77bf966823dc90c0b2ae361bacc59212ddf867a5f71859b10ed2` |
| FIG-17 | `core-final-FIG-17.png` | `db76de9950a2252acdb5403fb585f4f2cdf913481fc521396bf59e83b757c68e` |
| FIG-18 | `core-final-FIG-18.png` | `befc0afb40d8f275f59143f3269746de43b27b65a7ae88642d8dc90f15c77b7e` |
| FIG-19 | `core-final-FIG-19.png` | `b3cfbe69ae4cd316e16caabfa870aef9dbc412da2b5178f2968167d6f8027e32` |

Integration, 2026-10-16: expanded dependency bindings include the already reviewed parent 3.3 for FIG-02, 4.5/5.1.1/5.4.3 for FIG-08, and 2.6/2.9.1 for FIG-12. The JSON sidecar retains prior dependency hashes and records the current bindings; source/SVG/caption/PNG bytes are unchanged by this metadata correction.

Integration width clarification, 2026-10-16: 504 pt and 243 pt are the native SVG preview widths. The current v4 template provides 518.4 pt full width and 250.56 pt columns; normal 100% placement enlarges the diagrams slightly. Thus native-width review is conservative for label size. Caption previews use the production 9 pt size. Final PDF placement remains untested.
