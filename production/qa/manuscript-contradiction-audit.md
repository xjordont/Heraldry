# RC486 manuscript contradiction audit — 2026-10-09

**Review complete; semantic clearance: OPEN FINDINGS. RC484–RC486 remain unchanged.**

Audited repository `xjordont/Heraldry` at `0c96b1ea6f91e109cf940d66d853e60e14d63738`. Active manuscript: `source/Heraldry_RC486.md`, 1,451,198 bytes, 17,969 lines, SHA-256 `5da05cec6153ac11865874a0da416c002ce90b2dc4936fc9ce50abca9d3dbbe5`. Line references below are one-based and bound to this exact snapshot, not PDF page numbers.

The audit records **21 open findings**, **6 explicitly isolated questions**, and **13 exact proposed replacements**. Fifteen value differences form one numerical finding. The exact batch has nine copy/name repairs plus four whole-table replacements covering those 15 cells. It contains no inferred weapon statistics, new example rolls, or winner-timing choices.

The smallest source-supported corrections are F01–F05 and the name-only part of F13. Their governing text already exists. F06 supplies exact arithmetic alignment but needs confirmation that treasure and market values are intended to agree. Remaining findings require a procedure/intent decision or a newly authored example. All candidates remain `proposed`; no RC487 has been created.

## Authority and audit method

Section 1.6: specific rules override general rules; equally specific rules use the more restrictive result; examples, summaries and reference tables never override main text. Appendix C reiterates that it is a reference aid. `source/versions.json`, `editorial/history/RC485.json`, `editorial/history/RC486.json`, `CLAUDE.md`, `MASTER_PROMPT.md`, and `docs/WORKFLOW.md` supply revision/provenance requirements. Any approved text changes must create a new immutable RC487 snapshot through `tools/revise_manuscript.py`, with its registry and exact history in one commit. The present commit adds evidence/proposals and updates state only.

Coverage combines a manual mechanical review, chapter/appendix inventory, cross-reference/bestiary checks, exact snapshot/history checks, numerical table verification, and targeted counterexamples. This is a completed editorial audit of the available source, not a mathematical guarantee that no defect can remain. Pure flavour text was reviewed selectively where relevant to rule claims; literary proofreading and external canon verification were outside scope.

| Section | Reviewed scope | Method / limit |
|---|---|---|
| 1 | Introduction, modes, setting, and rules hierarchy | Hierarchy used for all conflicts; lore checked for cross-reference consistency, not rewritten to harmonize intentionally competing history. |
| 2 | Scores, Checks, footprint/range/LOS, area templates, terrain and timing | Full mechanical review; terrain parts and specific overrides used to reject false positives. |
| 3–5 | Rounds, AP/actions, movement, attack/critical sequence, Reactions, HP/Wounds and conditions | Compared with all reference/teaching summaries and unique special procedures. |
| 6 | Hero creation, ancestry/classes/Talents, leveling, party/APL | Reviewed interactions and printed exception rules; no inferred balance changes. |
| 7 | Equipment, traits, treasure, quality formulas, consumables, special items | Reviewed procedures; all 274 recognizable quality-prefixed enhanced rows checked numerically. Fifty Special Weapon rows reviewed for missing profile fields. |
| 8 | Power traditions, casting, metal restrictions and Power profiles | Reviewed range/target/cost/duration/critical defaults and explicit exceptions; no external spell canon. |
| 9 | Monster rules, all 135 bestiary mechanical entries and Random tables | All mechanical entries reviewed; 1,898 Random-table references resolve. Flavour prose sampled for relevant rule claims; not a word-by-word literary proof. |
| 10 | Preparation, 120 Secondary Objectives, weather, all 36 Core Scenarios, solo/co-op/scaling | Reviewed setup geometry, tokens, states, extraction, end/win timing and mode conversion; direct die ranges checked automatically. |
| 11 | Campaign cycle, Town, training/recruitment/retirement, Strongholds and finale | Reviewed accounting, caps, progression and PvE interaction; War Room applicability isolated. |
| A–C | Teaching example, starter profiles/Basic Mode, glossary/quick reference/examples | Compared all mechanical summaries/profiles/procedures with governing rules; identified two missing teaching resolutions and combined-variant gap. |

## Findings register

| ID | Finding | Type | Severity | Smallest next action |
|---|---|---|---|---|
| F01 | Spot summaries omit the higher SPI option | summary | minor | exact_copy_repair |
| F02 | DEX Pen glossary says damage is unaffected | summary | major | exact_copy_repair |
| F03 | Impassable Terrain summaries omit the Cover exception | summary | minor | exact_copy_repair |
| F04 | 9.5 allegiance summary omits same-Group allies | summary | major | exact_copy_repair |
| F05 | C.13 AI flow continues after a valid AI Step | summary | major | exact_copy_repair |
| F06 | Fifteen enhanced-table values differ from the quality formula | numerical | major | valuation_alignment_proposed |
| F07 | Fifty Special Weapon rows lack an explicit complete equipment profile | procedure | major | author_decision |
| F08 | Burning Seal uses an unbounded “maximum possible” Parry value | procedure | major | author_decision |
| F09 | Two AI charge abilities grant a bonus to an attack they never perform | procedure | major | author_decision |
| F10 | Bandit’s Toll requires two deployed Heroes in a legal one-Hero game | scenario | major | author_decision |
| F11 | Spider Silk Route does not designate a central Bundle; scaled second Bundle can disappear | scenario | major | author_decision |
| F12 | Ambushed Emissary Group 3 has incompatible placement geometry | scenario | major | author_decision |
| F13 | Two solo objective fields use names absent from their scenario objects | scenario_copy | major | exact_copy_repair |
| F14 | Shifting Sands asks for extraction of undefined Chronal Chests | scenario | major | author_decision |
| F15 | Iron-Vein Vault forcing action does not state its successful effect | scenario | major | author_decision |
| F16 | Swirling Vials determines damage type after damage is inflicted | procedure | major | author_decision |
| F17 | Icebound Court immediate ending prevents its same-round contest | scenario | major | author_decision |
| F18 | Ritual Chant gives Monsters Advantage on Checks they never roll | procedure | major | author_decision |
| F19 | Teaching example omits Mara’s automatic armour reduction | example | major | example_rewrite_required |
| F20 | Teaching example ignores the Dire Wolf’s retained maximum and piercing Critical Hit | example | major | example_rewrite_required |
| F21 | Basic Mode combined Traps/Hidden Strongbox variants cannot allocate all tokens | procedure | major | author_decision |

Severity describes manuscript usability, not CI failure. A major summary error can still have an unambiguous authoritative rule; a missing procedure can require a genuine decision. All open findings are manuscript issues. They are independent of the Pillow dependency failure and of implementation test results.

### F01 — Spot summaries omit the higher SPI option

**summary; minor; exact_copy_repair.**

The action table and glossary require INT alone. The full Spot action permits INT or SPI, whichever is higher; C.4 and C.13 already match it. Under 1.6 the full action governs. A SPI-focused Hero following the stale summaries would lose a legal advantage.

Source evidence: [1217](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L1217), [17717](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17717), [1254](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L1254).

Smallest repair: Copy the higher-of-INT-or-SPI instruction into those two summaries; do not change DC, AP, range, LOS, Cover, or targeting.

### F02 — DEX Pen glossary says damage is unaffected

**summary; major; exact_copy_repair.**

The glossary says DEX Pen does not reduce damage, while 7.10 applies it to damage totals and other values that add DEX. Starter profiles in Appendix B follow 7.10. The glossary can produce inflated ranged/Finesse damage.

Source evidence: [17496](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17496), [3677](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L3677).

Smallest repair: Replace the conflicting glossary sentence with the 7.10 scope, including Dodge. Keep the existing armour and shield stacking rules.

### F03 — Impassable Terrain summaries omit the Cover exception

**summary; minor; exact_copy_repair.**

The Chapter 4 terrain reference and glossary claim unconditional Cover. RC485 P-02 explicitly made Cover subject to the terrain entry; pits and chasms do not provide it. The authoritative rule already resolves play.

Source evidence: [870](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L870), [872](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L872), [1176](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L1176), [17556](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17556), [838](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L838).

Smallest repair: Add “unless its terrain entry says otherwise” to the two summaries. Preserve P-02 and the distinct terrain types/tags.

### F04 — 9.5 allegiance summary omits same-Group allies

**summary; major; exact_copy_repair.**

9.3 preserves allies inside the same Monster Group unless explicitly overridden. 9.5 A omits that exception and can send hostile-to-all Group members against one another. C.8 and the glossary already preserve same-Group allegiance.

Source evidence: [7609](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L7609), [7571](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L7571).

Smallest repair: Add the same-Group allied exception to 9.5 A, with “unless a rule explicitly says otherwise”.

### F05 — C.13 AI flow continues after a valid AI Step

**summary; major; exact_copy_repair.**

The numbered quick flow resolves a valid AI Step, then lists ordinary attacks/movement without the stop instruction. 9.5 C–D explicitly ends the activation after a valid step unless continuation is printed. Read as a procedure, C.13 would grant extra actions.

Source evidence: [17931](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17931), [7636](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L7636).

Smallest repair: Append the authoritative stop/explicit-continuation instruction to step 4. Do not modify any individual Monster ability.

### F06 — Fifteen enhanced-table values differ from the quality formula

**numerical; major; valuation_alignment_proposed.**

A complete scan of quality-prefixed enhanced rows reproduces 15 differences from mundane costs and 7.11 multipliers, flat additions, minima, and rounding. Shield differences concern Spiked Targe and Kite Shield; weapon differences concern Repeating Crossbow. Adamantine Steel Scale at 60c is correct because the armour minimum is 60c and is excluded. Importantly, 7.11 grants the finished item printed on a treasure table, so the discrepancies may be intentional treasure valuations rather than arithmetic mistakes. They should not be silently “fixed” during play.

Source evidence: [3796](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L3796), [3871](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L3871), [3946](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L3946), [4040](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4040), [3704](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L3704).

Smallest repair: If one value is intended for purchased/crafted and treasure versions, align only the 15 cells to the existing formula. Exact table replacements are proposed separately from summary/name repairs. Do not change base prices, quality effects, or balance formulas.

Uncertainty: The source supplies both a formula and finished-item values, but no justification for these particular exceptions. Author intent on separate treasure valuations is unverified.

| Table | Item | Printed c | Formula c |
|---|---|---:|---:|
| T041 | Masterwork Spiked Targe | 13 | 12 |
| T041 | Masterwork Kite Shield | 21 | 18 |
| T041 | Silvered Spiked Targe | 13 | 12 |
| T041 | Silvered Kite Shield | 21 | 18 |
| T041 | Cold Iron Spiked Targe | 13 | 12 |
| T044 | Masterwork Kite Shield | 21 | 18 |
| T044 | Silvered Kite Shield | 21 | 18 |
| T044 | Cold Iron Kite Shield | 21 | 18 |
| T044 | Palesteel Kite Shield | 28 | 24 |
| T047 | Masterwork Kite Shield | 21 | 18 |
| T047 | Sacred Kite Shield | 28 | 24 |
| T047 | Palesteel Kite Shield | 28 | 24 |
| T051 | Enchanted +4 Repeating Crossbow | 66 | 58 |
| T051 | Enchanted +5 Repeating Crossbow | 80 | 72 |
| T051 | Adamantine Repeating Crossbow | 120 | 88 |

Bases: Spiked Targe 8c, Kite Shield 12c, Repeating Crossbow 22c. ×1.5 gives 12c/18c; ×2 gives 24c; +36/+50 gives 58c/72c; ×4 gives 88c. Minimums and round-down are applied before calling a difference.

### F07 — Fifty Special Weapon rows lack an explicit complete equipment profile

**procedure; major; author_decision.**

The five 7.17 weapon tables list damage/traits/rules but omit Hands, requirements, and numeric ranged/thrown ranges. Elven Bow and other ranged weapons have Ranged without a distance; Ember Dagger and Rime Hatchet have Thrown without a range. Parenthetical/base-type names suggest inheritance, but the explicit inheritance paragraph covers Special Shields only. 7.17.3 shows that some later named weapons do print complete equipment details.

Source evidence: [4688](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4688), [4703](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4703), [4718](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4718), [4733](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4733), [4748](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4748), [4647](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4647).

Smallest repair: Decide whether these weapons inherit every unmodified mundane profile field. If so, add one explicit inheritance rule with an unambiguous base mapping for each weapon; otherwise add the missing fields. Do not infer new ranges, requirements, or hand counts from names.

Uncertainty: Intended base mapping is obvious for some entries and not explicit for all 50. Missing requirements could mean none; missing ranged distances still prevent an unambiguous complete profile.

### F08 — Burning Seal uses an unbounded “maximum possible” Parry value

**procedure; major; author_decision.**

Parry dice explode recursively under 5.5.3/5.3, so the entire Parry roll has no finite maximum. The item does not state whether only its base die is maximized, whether bonus dice are rolled, or whether Riposte follows. Maximizing a single armour die is finite, but the shared wording does not settle the Parry case.

Source evidence: [4909](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4909), [4913](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L4913), [1662](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L1662).

Smallest repair: Specify which die/result is maximized and how explosions and Riposte resolve. Possible policies are maximize retained base dice then roll normal explosions, or supply a finite non-exploding result. Choosing one changes behaviour and requires a decision.

### F09 — Two AI charge abilities grant a bonus to an attack they never perform

**procedure; major; author_decision.**

Gorebeak Bear Charging Gore and Skeletal Beast Run Down move, then modify an attack “this activation”, but neither performs an attack or explicitly continues. Under 9.5, the valid AI Step ends the activation; both bonuses are consequently unused. A different Run Down entry explicitly says “then makes their attacks”, demonstrating a working pattern without proving the intended behaviour for these two.

Source evidence: [8052](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L8052), [9473](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L9473), [7640](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L7640).

Smallest repair: Choose whether each charge makes the named attack, continues normal AI, or intentionally only moves. Add the selected instruction locally; do not change the global end-after-step rule.

### F10 — Bandit’s Toll requires two deployed Heroes in a legal one-Hero game

**scenario; major; author_decision.**

10.6 permits one-Hero parties and the scenario contains a Solo/Co-op field. Its deployment instruction nevertheless requires at least two Heroes on the Trail for each party. A one-Hero party cannot satisfy that condition.

Source evidence: [12170](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12170), [14807](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14807), [14817](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14817), [14838](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14838), [14844](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14844), [14870](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14870), [14901](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14901), [14907](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14907), [14915](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14915), [14919](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14919), [14930](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14930), [14952](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14952).

Smallest repair: Choose between “at least two, or every Hero if the party has fewer than two” and an explicit minimum party size for this scenario. The former preserves one-Hero support but is a design decision.

### F11 — Spider Silk Route does not designate a central Bundle; scaled second Bundle can disappear

**scenario; major; author_decision.**

The objective placement supplies three separated Bundles without designating one central. Boss deployment requires a central Bundle and another tarantula Group near a second Bundle. Token scaling can leave only one Bundle, removing the second placement reference. Nearest-legal-space fallback does not identify the intended marker.

Source evidence: [12211](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12211), [12232](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12232), [12201](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12201).

Smallest repair: Designate the boss-associated Bundle and specify the tarantula placement when fewer than two Bundles remain. Do not reuse P-09 as authority for an unapproved new placement.

### F12 — Ambushed Emissary Group 3 has incompatible placement geometry

**scenario; major; author_decision.**

A roughly 4×4 Camp has an edge 2 inches from its centre and corners about 2.83 inches away. A location 6 inches from the centre cannot also be on that perimeter. The full Monster Group also needs legal footprint placement. P-05 repaired a different clearing instruction and does not decide this Camp placement.

Source evidence: [12280](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12280), [12312](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12312).

Smallest repair: Choose Camp perimeter placement or an outside 6-inch ring, and state which part of the Group is measured. Keep its state, wake trigger, and rolled composition.

### F13 — Two solo objective fields use names absent from their scenario objects

**scenario_copy; major; exact_copy_repair.**

Fallen Observatory creates Star Lens and Bronze Orrery Fragments, while its solo objective names Central Lens/Lesser Fragment. Chasm Crossing creates Survey Map, while the solo objective names Cartographer’s Map. Each has a unique corresponding objective in the same scenario, supporting a name-only repair. Chasm Crossing’s extraction route is a separate uncertainty (U03).

Source evidence: [12443](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12443), [12451](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12451), [12452](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12452), [12961](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12961), [12969](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12969).

Smallest repair: Rename the Observatory objects to Star Lens and Bronze Orrery Fragment, preserving quantity; rename Cartographer’s Map to Survey Map, leaving the route wording unchanged for a separate decision.

### F14 — Shifting Sands asks for extraction of undefined Chronal Chests

**scenario; major; author_decision.**

No object called Chronal Chest is created. The scenario produces ordinary Treasure Chests and rewards treasure/looted Coins, while the solo field requires extracting two physical chests. Section 10 defaults govern objects identified as carried objectives; they do not declare these chests portable. A name-only replacement would leave the carrying and counting procedure unresolved.

Source evidence: [12585](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12585), [12612](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12612), [12618](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12618).

Smallest repair: Decide whether the solo objective counts looting two generated chests, extracting their contents, or carrying two physical chests. State the pickup and banking/counting rules for the chosen objective. Do not invent a carrying penalty or new chest type.

### F15 — Iron-Vein Vault forcing action does not state its successful effect

**scenario; major; author_decision.**

Interact [2 AP] plus a passed STR Check can “force” a Binding Point, but the only explicit transition to Broken is reaching 0 HP. The text assigns no damage or direct state change to the successful Check. The intended break-open alternative is recognizable, but instant breaking versus HP damage materially changes the opposition’s sealing game.

Source evidence: [12860](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12860), [12814](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12814).

Smallest repair: State the successful Check result explicitly: e.g. a direct Broken transition or a defined HP effect. Do not supply either without a decision; preserve existing attack and re-sealing rules.

### F16 — Swirling Vials determines damage type after damage is inflicted

**procedure; major; author_decision.**

The Alchemical Golem rolls the type only when an attack has already damaged a target. Type is needed earlier for legal mitigation, Resistance, Immunity, and damage-type critical riders. A target immune to one possible type creates a circular test: whether it was damaged depends on the type that is determined only if damaged.

Source evidence: [13455](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L13455), [1511](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L1511).

Smallest repair: Place the existing d4 type roll before damage resolution and specify whether it is once per attack or once per target. Retain the printed four outcomes and damage formula. Moving the trigger changes when rolls occur, so the exact timing must be approved.

### F17 — Icebound Court immediate ending prevents its same-round contest

**scenario; major; author_decision.**

After the Boss falls, the first extraction ends the adventure immediately. The rival cannot subsequently extract during that round, although another bullet reserves an end-of-round comparison if both designated items escape. The more-specific same-round case cannot be reached by sequential voluntary extractions once play has ended. No instruction defers the first end trigger.

Source evidence: [13761](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L13761), [13764](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L13764).

Smallest repair: Choose immediate first-extraction victory and remove the unreachable same-round branch, or defer that end trigger to the round end and retain the comparison. Also state how extracting the other party’s item affects ending and winning. Do not silently select a winner timing.

### F18 — Ritual Chant gives Monsters Advantage on Checks they never roll

**procedure; major; author_decision.**

Mire-Scale Shaman grants allied Monsters Advantage on resistance Checks. 2.3 and 9.1 prohibit Monster Checks and automatically resolve the failed-Check outcome unless immune. Ritual Chant supplies neither a Monster score nor a specific replacement procedure; a modifier alone does not explicitly authorize making a forbidden roll. As written its listed benefit has no effect.

Source evidence: [14317](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14317), [523](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L523).

Smallest repair: Choose an explicit defensive effect or an explicit exception with a complete roll procedure. Removing an intentionally inert benefit is also possible. Do not assume Monsters roll d20+0 or gain immunity.

### F19 — Teaching example omits Mara’s automatic armour reduction

**example; major; example_rewrite_required.**

Appendix A explicitly keeps printed AD in use. Mara’s Gambeson supplies d3 AD, but Senna’s adjacent shot applies all 7 damage with no armour roll, taking Mara from 12 to 5. Spending AP on Reflex Attack does not suppress automatic Chest AD. An unstated d3 result would leave Mara at 6–8 HP, not 5. Subsequent Mara state summaries repeat the error.

Source evidence: [16455](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L16455), [16138](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L16138), [16117](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L16117).

Smallest repair: Supply an explicit AD roll, resolve the shot correctly, and update all dependent Mara HP states. The manuscript contains no observed armour result; an illustrative new result must be identified as editorially chosen.

### F20 — Teaching example ignores the Dire Wolf’s retained maximum and piercing Critical Hit

**example; major; example_rewrite_required.**

The retained 8 on d8 is a Critical Hit. Bite is piercing, so the printed armour reduction is invalid and at least one exploding bonus d8 must be rolled. With Varek at 12 HP, the minimum is 8+1+1=10 damage, leaving at most 2 HP; a bonus of 3 or more knocks him out. The printed 9 HP, later successful STR Check, Prone state, and subsequent state ledger are not supported.

Source evidence: [16477](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L16477), [1539](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L1539), [1528](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L1528).

Smallest repair: Either retain the 8 and supply a complete exploding-die chain, critical rider, damage/KO resolution and dependent ledger, or deliberately change the illustrative base roll and recalculate the attack. Do not weaken Critical Hit rules or assert an unseen bonus roll.

### F21 — Basic Mode combined Traps/Hidden Strongbox variants cannot allocate all tokens

**procedure; major; author_decision.**

The variants expressly allow combining them. Three Satchels plus three Hidden Strongbox markers require six tokens when Traps says put one under each treasure marker, but it provides four. With Advanced Ogre there are seven markers and five tokens. The text also does not order the fake/real Check against revealing a trap on the same pickup Interact.

Source evidence: [17098](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17098), [17104](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17104), [17110](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17110).

Smallest repair: Specify whether fakes receive tokens and how the token count/composition changes, then order Strongbox identification versus trap reveal/pickup. Do not invent additional trap probability.

## Explicit uncertainties — not asserted as proven contradictions

### U01 — Created ice wall placement/profile

Gelid Fiend chooses a separating 6-inch wall; Frost Bailiff creates a 6×3 wall with HP/AV/duration, but neither gives a clear placement range. Width/height orientation and collision differ between them. 2.7.3 supplies default source origins for areas, and Section 10 supplies nearest-legal placement; neither clearly classifies these created walls as a Line area versus free-standing terrain. It would be overconfident to claim an unlimited range or ignore these defaults.

Next step: Confirm terrain versus area status, origin/placement, dimensions, blocking/collision and attackable-object procedure. Do not add a distance or thickness without authority.

Source evidence: [9269](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L9269), [13735](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L13735).

### U02 — Command Tent and other complex-terrain interiors

Outpost Raid puts Battle Plans and the Commander inside a Blocking Terrain tent. Taken as an entire solid footprint, entry and LOS-based Interact fail. However, 2.9 explicitly separates complex-feature parts/supporting surfaces, defaults floors to Open, and requires pre-play assignment. An enterable tent with Blocking walls may be a legal reading. Similar barrow/dais cases can use distinct floors/upper surfaces and are not automatically contradictions.

Next step: Confirm that the tent has an accessible floor and opening, and distinguish its walls from its interior in setup/diagram. Do not certify an unreachable objective without checking the parts assignment.

Source evidence: [13104](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L13104), [824](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L824).

### U03 — Chasm Crossing solo extraction direction

The map starts near a ledge, not on an edge, yet the solo instruction says “edge opposite its starting edge”. F13 safely corrects its name only. The start/delivery sides suggest the intended direction, but the object itself has no starting edge.

Next step: Name the delivery-side edge or party-deployment opposite edge explicitly after confirming intended geometry. Do not alter the competitive Stone delivery objective.

Source evidence: [12961](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12961), [12969](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L12969).

### U04 — War Room bonus in PvE Initiative

10.5.4 replaces competitive Initiative with a d20 threshold and does not add the ordinary Initiative Bonus. War Room and its Veteran improve that bonus; campaign rules allow normal Stronghold benefits in PvE. The specific replacement can simply make this bonus inapplicable, so this is not a proven contradictory roll. It may leave a purchased benefit ineffective in PvE.

Next step: Confirm intended PvE applicability. Do not automatically import leader INT/SPI, change the threshold, or add the bonus.

Source evidence: [15690](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L15690), [14708](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14708).

### U05 — Move-only Monster steps and “in Reach” wording

Stone Sentinel/Tomb Guardian fallback movement ends the activation and may deliberately be move-only. White-Court Sentinel says attack an enemy “in Reach” while its Bash lacks a Reach trait. Ordinary melee distance may be intended. These phrases do not authorize granting an extra attack or 2-inch Reach.

Next step: Confirm intent or clarify wording to ordinary melee distance; retain default distance and end-after-step behaviour pending that decision.

Source evidence: [8359](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L8359), [9607](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L9607), [9148](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L9148).

### U06 — Teaching aids: two-square footprint and objective setup order

C.12’s “two-square Monster” does not match standard 1×1, 2×2 or 3×3 footprints unless it means two squares wide. Separately, solo setup deploys Monsters before placing objectives/hazards although some deployments depend on those positions. Planning the positions in advance may satisfy the latter without a rules change.

Next step: Use an explicit standard footprint in the example if desired; clarify planning/deployment dependencies without treating the appendix as an override or inventing a new setup phase.

Source evidence: [17811](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L17811), [14670](https://github.com/xjordont/Heraldry/blob/0c96b1ea6f91e109cf940d66d853e60e14d63738/source/Heraldry_RC486.md#L14670).

## Cleared conflicts and preserved exceptions

- 1.6 resolves examples, summaries, and equally specific rules; full rules govern stale references.

- RC485/RC486 P-01–P-12 remain present; the audit does not reopen their approved cone, terrain, deployment, or scenario-placement repairs.

- Scenario-specific failed Jump consequences override the core fallback. The older chasm-jump triage is not a new defect.

- Solo conversion/extraction continues past competitive ending conditions where 10.5.5 explicitly says so.

- The global six-Group limit rejects a seventh placement event. A setup with five Random Groups plus multiple scenario Groups may omit a later Group, but is not allowed to place seven. The allocation may merit balance review; no new cap or merging rule is needed to resolve legality.

- Boss Relentless activations, their per-round cap, and lack of ordinary Monster Phase activation are explicit; start-of-Monster-Phase effects remain applicable.

- Tier-0 Hybrid cost, Sorcery resolving despite Blood Price, natural-form equipment suspension, and fixed Basic Mode profiles are explicit exceptions.

- Immunity to Poisoned does not imply immunity to poison damage; Resistance and condition immunity are separate.

- Scroll attack profiles can differ from known Powers because scrolls provide their own complete effect.

- Throwing Knives always use one base die; Martial Supremacy and other die increases do not override the explicit exception.

- Scenario CV/role deviations are deliberately allowed in 10.6.4; no automatic Monster repricing is justified.

- Historical accounts of the Fall are deliberately competing/unreliable. No external canon was used to invent lore corrections.

## Verification and delivery scope

Existing repository verification: preflight baseline **8/8 PASS**; unittest **15/15 PASS**; cross references **633 citations / 254 numbered headings / 0 unresolved / 0 duplicates**; bestiary **135 entries / 1,898 mentions / 0 missing**. Parser inventory: **8,426 text blocks, 833 headings, 332 tables, 10,341 cells, 0 ragged tables**. These checks establish structure/provenance and selected invariants; they do not prove coherent rules meaning.

The accompanying `manuscript_contradiction_checks.py` independently reproduces the enhanced-value comparisons with proper quality minima, complete face coverage for direct die-labelled range tables, exact candidate match counts, source/hash/history integrity, and evidence-line validation. It is an audit utility, not a new CI semantic gate. Run from a checkout after `python tools/parse_source.py`: `python production/qa/manuscript_contradiction_checks.py --output production/qa/manuscript-contradiction-verification.json`.

No manuscript file, registry, history archive, gameplay implementation, or existing PDF was changed. No release PDF was rebuilt/reapproved. Historical layout, artwork and figure PASS ledgers remain scoped to their recorded input/PDF hashes. Physical proof and the separate art pipeline are still separate work.

The former `Complete rules contradiction audit: NOT TESTED` status is replaced with `COMPLETE — OPEN FINDINGS`. The corrected dependency-install workflow passed after the Pillow fix, but that CI success is not manuscript semantic clearance. The original email’s three annotation texts remain unavailable; this audit does not identify them by conjecture.

## Reviewable proposed batch

`editorial/proposals/rc487-contradiction-audit.json` has source SHA, unique exact find/replace text, expected match counts, finding IDs, and per-entry decision classes. CA-01–CA-09 are nine copy/name replacements. CA-10–CA-13 align the four enhanced tables if uniform valuation is approved. F13’s Chasm map rename deliberately leaves U03 open. The batch is proposed, not approved; `revise_manuscript.py` correctly refuses it in that state.

A subsequent repair pass should first record decisions on the substantive items, author the two missing teaching resolutions with a complete HP/KO ledger, promote only approved exact patches as one new RC snapshot, rerun structure/history checks, and rebuild/reconcile affected figures and PDFs before claiming a corrected release.
