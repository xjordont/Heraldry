# RC493 figure semantic delta review: setup and teaching

Reviewer: Codex delegated authority/setup reviewer. Reviewed 2026-10-15, completed 23:14 UTC. The reviewer did not author the RC493 manuscript patches or these SVGs. Scope: FIG-16, FIG-18, and FIG-19 only.

Current source: `source/Heraldry_RC493.md`, SHA-256 `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`, verified from file bytes and the active registry. Compared the exact RC492-to-RC493 text delta with each figure's dependencies, caption, every SVG text node, relevant full rules, and current ledger findings. Read the live contracts and `docs/CANON_AUTHORITY.md` before reviewing.

All three existing SVGs were rendered without regeneration, using Python `typst.compile(format="png", ppi=144, root=repo, font_paths=[repo / "fonts/static"])`. Each wrapper uses a 504 pt page width, zero margins, and the original SVG at its native 504 pt width. All three resulting PNGs were actually viewed. These are isolated source-figure renders, not book-page or PDF builds. No source, SVG, caption, manifest, dependency configuration, or shared review ledger was edited.

## Verdicts and exact bindings

The values below come from `figure_review_gate.current_hashes()` against active RC493, after the actual review. Matching unchanged SVG/caption hashes was not used as a substitute for inspection.

| Figure | Verdict | SVG SHA-256 | Caption SHA-256 | Dependent rules SHA-256 |
| --- | --- | --- | --- | --- |
| FIG-16 | **PASS_WITH_NOTES** | `ee2d73d64f4e2c1396530cc69b2c044f987907991e2927475703211d76d835c8` | `ae5fde33740332bc58851e5f222f4cb7d6a742c0b0bcd7b59081340c117c55d7` | `869e39c91a8afac6869ab4aca7751855328f4ddb7896a320f8271e32af21ad03` |
| FIG-18 | **PASS_WITH_NOTES** | `2627c83d32b5c91333b6ebb22a1166756bd5a2f28733b836890785ef3a92b686` | `0e28e0e58ebb9a1ac43821294569d5aad172d5cc1dccd85a98f16cafc7337d9d` | `894d234f58ca960a33618502f6786a4149c7f08d74b6ea8e705996527fadfd86` |
| FIG-19 | **PASS_WITH_NOTES** | `fb50d064c7ce685f410f6188688a8e37abac0de8eafba61eaefc0d83f2d9226c` | `fe49806f43a98b023b889e149ab5d124fada5cd1ddb23fceae5a6a02f9988d64` | `385bbb51aec6acc3852dac54d683b0f646971a86a1aaf77bdd19d650bd6be153` |

| Actually viewed render | PNG SHA-256 |
| --- | --- |
| `build/checks/RC493/setup-FIG-16.png` | `049ab64f43593455ec91d0addadcd7ff5de441f39a49d5d1fec51c12af4d9db1` |
| `build/checks/RC493/setup-FIG-18.png` | `c388bd1cf23d1308f1b559528f4b3800de161f3810e6ada63b230978a0144a9d` |
| `build/checks/RC493/setup-FIG-19.png` | `21f2d7393044d56ffa04bdc3eb21cf35caa7dddcc5ac261a276cc1ff6fa9d601` |

Wrappers are the matching `setup-FIG-16.typ`, `setup-FIG-18.typ`, and `setup-FIG-19.typ` in that ignored checks directory. They include the existing SVG directly, without caption alteration or synthetic diagram replacements.

## FIG-16: The Whispering Grove

Dependencies: **10.4** and **9.5**, from `config/figure_dependencies.json`. Current caption is at placement anchor `B12100` in `figures/placements.json`.

RC493 changes the lead sentence of **9.5 C. Standard Monster AI Script** at source line 7628 from combatant `their/they` to `its/it`. The evaluation order, special Target Priority, first-valid-instruction rule, and activation-ending rule are unchanged. No RC493 edit changes this scenario's setup or Warden ability.

The actual render shows the Standing Stones in a triangle, a schematic central clearing, one Hero from each party, the Warden adjacent to the first Hero's Stone, the special target line toward the rival Hero, and Group 2 inside the clearing. Panel B and the caption state the correct first-Interact placement, latest attempted/activated Stone target, 8" Entangling Roots condition, DEX Check, and activation ending. Checked against RC493 lines 12062, 12076-12078, 12088, 12092-12094, and 12100. Compared **9.5 C-G**, especially lines 7628-7648 and 7672, to confirm the scenario's printed priority takes precedence and its valid AI Step ends the activation before an ordinary attack.

The unchanged schematic note and the small visual gap between the Warden and Stone remain consistent with the ledger's accepted minor. The text expressly requires adjacency; this review does not certify the drawn gap as a measurement instruction. The dimensions and labels remain legible in the actual render. No new semantic issue found. **PASS_WITH_NOTES**, retaining that accepted schematic limitation.

## FIG-18: Appendix A setup and Round 1

Dependency: **Appendix A**, from `config/figure_dependencies.json`. Current caption is at placement anchor `B16371`.

RC493 clarifies **A.9** at lines 16323-16328: an already Engaged Dire Wolf skips movement, declares exactly one Bite, applies Pack Tactics before rolling, resolves the Attack Sequence, applies a damage-triggered STR Check, and ends its activation. It also corrects the isolated **A.8 Block Example** at line 16309 to declare Block before damage, and changes the Round 2 example's competing Reaction from Block to Dodge at line 16455. The diagram depicts setup and **Round 1**, so it does not purport to illustrate either changed example.

Actually observed and cross-checked:

- Panel A shows 24" x 24" setup, opposite 4" deployment bands, centre ruin, flanking low wall/rubble, Chest 5" east of centre, and the four Heroes. The Satchel/wolves are explicitly one legal arrangement; the separate inset identifies the A.11 relative layout without claiming a fixed ruin side. Checked **A.2/A.4** (16098-16111, 16180-16184) and **A.11 Initial Positions** (16354-16371).
- Party activations and AP markers match **A.11** lines 16377-16409: initiative 14 versus 10; Edric spends 3 AP; Varek's 9 damage minus 4 armour reduces Edric from 16 to 11 HP; Mara deals 6 damage to Wolf 3; Mara spends the retained AP on a successful Dodge; Senna retains 1 AP. The automatic armour does not become a Reaction.
- Monster rows show **one Bite for Wolf 1 and one Bite for Wolf 2**, not one attack in each branch of the clarified A.9 flow. Wolf 1's 6 minus 3 armour deals 3; its STR total of 12 prevents Prone. Only Wolf 2 receives Pack Tactics, keeps 7 from 4/7, adds 1, and deals 3 after 5 armour. Its STR total of 9 causes Prone. Wolves 3 and 4 cannot reach a legal engaging position and do not attack. Checked profile/riders at 16166-16170, clarified flow at 16323-16328, and the complete Round 1 Monster Phase at 16413-16427.
- The final state and caption's arithmetic agree: Edric 16 -> 11 -> 8 -> 5 HP, Prone, carrying the Satchel, Engaged by Varek and Wolves 1/2; Senna's unspent AP is removed at the End of Round. There is no extra Bite, duplicate STR Check, premature Pack Tactics, or delayed damage rider in the figure.

Reaction timing was checked against **5.2**, lines 1515-1519, and the explicit **A.11** Dodge declaration at 16401. The figure's compact Senna row prints the fixed damage result before the words "Mara declares Dodge". It is an outcome summary and does not explicitly grant a post-roll choice, but its reading order leaves a **minor teaching ambiguity**. Recommended later figure-copy clarification: state "Dodge declared before damage". This is not a new RC493 mechanical contradiction and does not affect its correct AP, Check, damage, or HP values. Leave that note visible to the integration owner; do not report the row as explicitly teaching declaration timing.

The old ledger's accepted note describing the Satchel label north of the ruin is not literally observable in this current render: the label is below the Satchel on the south side, and the caption below the board says the ruin side is not stated. Preserve the old observation as history, not as a current location claim. **PASS_WITH_NOTES**: no major findings; retain the explicit schematic limitation and the nonblocking Reaction-summary note above.

## FIG-19: Basic Mode default scenario

Dependency: **Appendix B**, from `config/figure_dependencies.json`. Current caption is at placement anchor `B17094`.

RC493 changes only **B.3 Components** within Appendix B, at lines 16555-16556, to require 4 Satchels and 4 Monster Entry markers when using **Advanced Ogre**. Full **B.7 Advanced Ogre**, line 17102, already adds a fourth marker, the Ogre, and its fourth Satchel. **B.6**, lines 17074-17094, remains the default three-group setup. The actual figure title, text, and caption identify that default scenario and make no claim to depict the optional Ogre variant; adding a fourth default marker would be wrong.

Observed three Entry markers, three Satchels, three resting-group glyphs, the central Strongbox, opposite 4" deployment bands, road, two central terrain pieces, and four quarter pieces. The text states random assignment of one complete group to each marker, terrain classification, 5-7" centre distance, minimum 4" marker separation, treasure values, carrying penalty, own-edge extraction, and Round 6 scoring. These agree with **B.6**, lines 17076-17094. Caption wording correctly distinguishes extracted treasure from defeated Monsters.

Re-derived the assumed example from the current full rules: Ironscar SPD 4" at 16587, minus the Strongbox's 2" penalty at 17086, gives 2" per Move; the centre-to-edge open-ground distance is 12", requiring at least 6 Moves. Pickup costs a separate Interact [1 AP], as the figure says. Strongbox 12c + Satchel 4c + two Goblins at 1c each + Bandit 3c = 21c (17022, 17048, 17082, 17092). The example does not include an Ogre or claim the three-component default is sufficient for its variant.

Previously resolved ledger items remain resolved in the actual view: the Group-R label is clear of the cart/wall hatch, the Strongbox uses a distinct glyph, and the two fixed extraction arrows are solid. The accepted **5-7" label on the outer dashed ring** remains legible with its white halo. **PASS_WITH_NOTES**, retaining that accepted label-placement minor. No new semantic issue found.

## Limits and integration

This is an actual render-and-source semantic delta review of the three assigned figures, with relevant surrounding rules inspected. It is not an exhaustive new audit of all material in Chapters 9-10 or Appendices A-B, nor an independent whole-manuscript copyedit. Existing typography and combatant-pronoun style in unchanged SVG prose was not revised. No book layout, pagination, final placed size, digital-PDF accessibility, physical print, or binding proof is certified. The integration owner must read this report before updating only the corresponding shared review entries; this report itself does not stamp the shared gate.
