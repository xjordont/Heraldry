# Rules-text review: findings for RC527

**Status: proposed, nothing applied.** Every patch in the JSON twin `editorial/proposals/rc527-rules-text-review.json` is `status: "proposed"`. The snapshot `source/Heraldry_RC526.md` is untouched. Promotion to RC527 happens only after the owner approves, through `tools/revise_manuscript.py`.

Prepared 2026-10-31 against `source/Heraldry_RC526.md` (SHA-256 `040357729080de051fbf8d398240d131ba2e55bdcabe57ac32fefe5cfc09c235`, 18,552 lines). Scope: every line of non-lore text, read in order: the table of contents, the rules prose and tables of Sections 1 to 11, the Elite and Boss profiles, the Powers, the item tables, the scenarios, Appendices A, B (including the B.4 hero cards and B.5 Basic Mode profiles), and C (quick references, glossary, worked examples). Italic lore passages were excluded; they were reviewed in RC523 to RC526. Each finding below is an exact find/replace patch whose `find` occurs exactly once in RC526 (two patches replace a repeated string and say so), verified both against the snapshot and in sequence, so the batch reconstructs cleanly.

## Verdict

The rules text is in good shape. A full read plus mechanical sweeps found no broken cross-reference, no incomplete dice table, no Monster AI Step that fails to say whether the activation ends or continues, no unresolved Monster or scenario name, no stray typography (the only non-ASCII characters are the multiplication sign and the en dash), no American spellings, and no arithmetic error in the B.4 hero cards, the A.11 worked example, or the treasure, retirement, and stronghold tables. The five settled canon conventions hold throughout.

What remains is 95 small patches. Most are copy: a lowercase example opener, a missing table space, bold applied unevenly to the Enchanted rows, 19 cross-references written as 'Section N.N' where the book otherwise writes a bare bold number, and one hyphenation split ('nonmagical' beside 'non-magical'). A smaller group clarifies wording that points at text that does not exist ('Learn 1 new Power'), collides with a defined term ('primary target' beside the Monster AI's **Primary Target**), or uses a state that cannot occur (a swallowing Monster being **Knocked Out**). The consistency group fixes three wrong glossary pointers, a placeholder glossary entry, two worked examples that give the Guard Hireling a shortsword and a STR score, a missing damage abbreviation, and the Terror Aura reminders. Thirteen patches change what a rule says and are listed as owner decisions: the Repeating Crossbow's enhanced prices, the Charm of Epic Luck, two 'a caster' weapons, four Druidic Rituals that target an undefined 'Monster Group marker', and the Lodestone's 'base contact'.

## Counts

| Category | Patches | Standing |
|---|---|---|
| Copy | 57 | Recommended (9 of them marked optional) |
| Clarity | 14 | Recommended |
| Consistency | 11 | Recommended |
| Rules | 13 | Owner decision |
| **Total** | **95** | |

Under about 150 patches, so this is a single proposal rather than per-chapter batches.

## Owner decisions

Each of these changes a rule's wording, so none is recommended for silent approval. The patches are in the JSON twin exactly as described; approving a decision means approving its patch IDs.

1. **Repeating Crossbow prices (RULE-01 to RULE-03).** The 7.8 base cost is **20c**. Every other enhanced weapon follows base +36 for Enchanted +4 (17 rows), base +50 for Enchanted +5 (7 rows), and base ×4 for Adamantine weapons; the three Repeating Crossbow rows (58, 72, 88) are the only exceptions, and all three fit a base of **22c** exactly. Option A (patched): change the three enhanced rows to 56, 70, and 80. Option B: change the 7.8 base to 22c and leave the rows. Recommendation: A, because 7.8 is the table players shop from and it is the one that appears in every package and starting-kit price check; if the owner remembers the base being lowered from 22 deliberately, A is also the correct follow-through of that decision.
2. **Charm of Epic Luck (RULE-04).** 'Gain **+2 Luck**' is the only Luck bonus not written as 'Increase maximum **Luck** by **N**' (Halfling, Goblin, and the 6.10 background bonus all use that form). Recommendation: approve the maximum-Luck wording. If the owner intends two one-off Luck Points instead, the entry should say that explicitly.
3. **'A caster' (RULE-05, RULE-06).** The Magehunter Crossbow and the Thought-Eater Scourge drain NRG from 'a caster', which is not a defined category. Recommendation: 'a combatant that has **NRG**', because the effect only does anything to such a combatant. The alternative wording already used by the Godsbane Distillate, 'a target that knows at least one Power', would also be consistent; pick one.
4. **'Neutral Monster Group marker' (RULE-07 to RULE-10).** Monster Lure, Beast Pacification, Monster Stampede, and Beast Commander target a marker that no rule defines, and 8.2 requires range and **LOS** to each target. Recommendation: target the Monster Group and measure range and **LOS** to any Monster in it, with Monster Lure's 12" measured from any Monster in the Group. The alternative is to define a Monster Group marker in 9.3, which is a larger addition and would need its own placement rules.
5. **Lodestone 'base contact' (RULE-11 to RULE-13).** The Undermarches Secondary Objective is the only text in the book that uses 'base contact'; every other proximity rule on the square grid says 'adjacent'. Recommendation: approve 'adjacent to the Lodestone'. On a grid the two mean the same thing, but this is a scoring objective, so it is the owner's call.
6. **Buckler enhanced prices (no patch).** Masterwork, Silvered, and Cold Iron items cost base ×1.5 rounded down, minimum +2 (Hide Cuirass 3c → 4c, Mail Shirt 6c → 9c). The three Buckler rows read **5c** where that rule gives **4c**. Either the Buckler rows or the Hide Cuirass rounding is the intended one; I have not proposed a patch because the direction is a pricing choice, and the three rows can be added to this batch on request.

## Dependency impact

- **Figures.** `tools/figure_dependencies.py` hashes the full text of each section a figure explains, so any edit inside a listed section, however cosmetic, marks that figure's semantic review stale. If every patch is applied, 59 of 77 figures change hash (FIG-01 to FIG-76). 55 patches touch no figure and no player-aid sheet; 15 touch one to four figures each; and 9 patches (COPY-35, SEC-13, SEC-14, HYPH-02, CLAR-07, CLAR-08, CLAR-09, CLAR-10, CLAR-11) each invalidate the roughly 40 scenario and preparation figures that depend on **10.1**, **10.4**, or **2.9.1** (FIG-13, FIG-14, FIG-20 to FIG-57). All of these are wording changes with no effect on what the figures draw, so the re-review is a confirmation, but it still has to be recorded. If the owner would rather keep the figure gate green until the next figure pass, approving everything except those 9 patches leaves 18 figures to re-confirm instead of 59.
- **Player-aid sheets.** `tools/aids_fidelity.py` will report changed sections for pa01, pa02, pa03, pa04, pa05, pa06, pa07, pa10: pa01 (COPY-03, SEC-02, SEC-03, SEC-15); pa02 (COPY-27, COPY-28, COPY-29, COPY-30, COPY-31, COPY-32, COPY-33, COPY-36, SEC-02, SEC-03, SEC-10, SEC-11, CLAR-12, CONS-03, CONS-04, CONS-05); pa03 (COPY-04, COPY-05, SEC-06, CONS-06); pa04 (COPY-06); pa05 (COPY-36); pa06 (COPY-05, SEC-05, SEC-06); pa07 (COPY-02, HYPH-01, HYPH-02); pa10 (COPY-35, SEC-13). None of the patched wording is quoted on a sheet except the C.3 Hidden row (COPY-36) and the 5.8.1 injury row (COPY-06), so re-recording after a diff is expected to be a confirmation; the sheets themselves do not need rebuilding unless the owner asks for one.
- **Hero cards.** COPY-09 edits Mossgrave's B.4 card ('Wolf Shape' to 'Wolf'), so `typst/heroes/basic-heroes.json` must be re-extracted after promotion and `tools/hero_cards.py check` re-run.
- **Content anchors.** Every prefix in `config/content_anchors.json` still resolves after all 95 patches; none needs updating.
- **Back cover and How to use.** No string in `editorial/back_cover.json` or `editorial/how_to_use.json` is affected.
- **Build.** Nothing was built. The source table of contents is replaced by a generated one during the build, so COPY-01 has no layout effect.

## Findings

Grouped by the section of the manuscript the patch sits in, in manuscript order, with the category and standing on each. Line numbers refer to `source/Heraldry_RC526.md`.

## Table of contents

### COPY-01: Table of contents

**Copy. Recommended.** 10.1.1 is the only level-4 heading listed in the table of contents; every other #### heading is omitted. The build replaces the manual TOC with a generated one, so this only tidies the source.

*Line 110, under "Table of Contents".* Dependencies: none.

**Current text**

>   - [10.1 Adventure Preparation Sequence](#101-adventure-preparation-sequence)
>     - [10.1.1 Climate and Core Scenario Selection](#1011-climate-and-core-scenario-selection)

**Proposed text**

>   - [10.1 Adventure Preparation Sequence](#101-adventure-preparation-sequence)

## Section 2

### SEC-01: 2.5 Action Points

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 572, under "2.5 Action Points and Summons".* Dependencies: 2 figures (FIG-02, FIG-71).

**Current text**

> following the Monster AI rules in **Section 9.5**.

**Proposed text**

> following the Monster AI rules in **9.5**.

### COPY-02: 2.8.4 example

**Copy. Recommended.** Worked examples open with a capital after 'Example:' everywhere else.

*Line 810, under "2.8.4 Cover".* Dependencies: 2 figures (FIG-07, FIG-63); player-aid sheet pa07.

**Current text**

> *Example: a Ranger has clear **LOS**

**Proposed text**

> *Example: A Ranger has clear **LOS**

## Section 3

### SEC-02: 3.4 Monster Phase

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 1104, under "3.4.1 Monster Wake-Up".* Dependencies: 1 figure (FIG-01); player-aid sheets pa01, pa02.

**Current text**

> resolve Monster waking rules in **Section 9.4** and any scenario

**Proposed text**

> resolve Monster waking rules in **9.4** and any scenario

### SEC-03: 3.4.3 Monster activations

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 1122, under "3.4.3 Monster Activations".* Dependencies: 3 figures (FIG-01, FIG-11, FIG-66); player-aid sheets pa01, pa02.

**Current text**

> **Standard Monster AI Script** in **Section 9.5** from top to bottom

**Proposed text**

> **Standard Monster AI Script** in **9.5** from top to bottom

## Section 4

### SEC-04: 4.1 Actions

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 1199, under "4.1 Action Basics".* Dependencies: none.

**Current text**

> If a **Monster** is required to make an ability-style **Check**, use **Section 2.3**.

**Proposed text**

> If a **Monster** is required to make an ability-style **Check**, use **2.3**.

### COPY-03: 4.2 action table

**Copy. Recommended.** Missing space before the closing pipe; every other row of the table has one.

*Line 1214, under "4.2 Universal Actions".* Dependencies: 3 figures (FIG-02, FIG-70, FIG-71); player-aid sheet pa01.

**Current text**

> | **Shift** | 1 AP | **Shift 1"** without triggering **Reflex Attack**.|

**Proposed text**

> | **Shift** | 1 AP | **Shift 1"** without triggering **Reflex Attack**. |

### SEC-05: 4.4.7 Terrain and movement

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 1385, under "4.4.7 Terrain and Movement".* Dependencies: 2 figures (FIG-05, FIG-09); player-aid sheet pa06.

**Current text**

> Terrain types and tags are defined in **Section 2.9**.

**Proposed text**

> Terrain types and tags are defined in **2.9**.

### COPY-04: 4.5 example

**Copy. Recommended.** Worked examples open with a capital after 'Example:' everywhere else.

*Line 1447, under "4.5 Reactions".* Dependencies: 4 figures (FIG-02, FIG-03, FIG-08, FIG-68); player-aid sheet pa03.

**Current text**

> *Example: an Ogre attacks a Cleric.

**Proposed text**

> *Example: An Ogre attacks a Cleric.

## Section 5

### COPY-05: 5.1.2 Reaction table

**Copy. Recommended.** The only table in the manuscript with bold header cells; headers are plain text everywhere else.

*Line 1523, under "5.1.2 Combat Reaction Guide".* Dependencies: 1 figure (FIG-06); player-aid sheets pa03, pa06.

**Current text**

> | **Reaction** | **AP** Cost | Best Use |

**Proposed text**

> | Reaction | AP Cost | Best Use |

### CONS-06: 5.5.3 Parry example

**Consistency. Recommended.** 'Guard' is the 11.2.5 Hireling, who carries a Mace and has no STR score. This example gives the Guard a shortsword and **STR +2**, so it contradicts the profile; a Fighter fits.

*Line 1703, under "5.5.3 Parry [1 AP]".* Dependencies: player-aid sheet pa03.

**Current text**

> *Example: A Guard is targeted by a melee attack and declares **Parry** with a shortsword, spending **1 AP** before damage dice are rolled. The attack deals **5 slashing** and **2 fire** damage, **7** in total. The Guard rolls the shortsword's d6 and gets a **6**, rolls an exploding d6 for **2**, then adds **STR +2** for a parry total of **10**. The **Parry** succeeds, so the Guard suffers none of the attack's damage. Because the retained parry base die showed its maximum value, the attacker suffers **10 Riposte damage** and applies **AV** against it normally.*

**Proposed text**

> *Example: A Fighter is targeted by a melee attack and declares **Parry** with a shortsword, spending **1 AP** before damage dice are rolled. The attack deals **5 slashing** and **2 fire** damage, **7** in total. The Fighter rolls the shortsword's d6 and gets a **6**, rolls an exploding d6 for **2**, then adds **STR +2** for a parry total of **10**. The **Parry** succeeds, so the Fighter suffers none of the attack's damage. Because the retained parry base die showed its maximum value, the attacker suffers **10 Riposte damage** and applies **AV** against it normally.*

### SEC-06: 5.5.4 Reflex Attack

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 1713, under "5.5.4 Reflex Attack [1 AP]".* Dependencies: 1 figure (FIG-06); player-aid sheets pa03, pa06.

**Current text**

> **Reflex Attacks** are **Reactions** and follow **Section 4.5**.

**Proposed text**

> **Reflex Attacks** are **Reactions** and follow **4.5**.

### COPY-06: 5.8.1 Lasting Injuries row 14

**Copy. Recommended.** The action is named **Stand** (4.2); 'Standing' is not a defined term.

*Line 1838, under "5.8.1 Injuries Table".* Dependencies: player-aid sheet pa04.

**Current text**

> **Max Speed 4"**, **Standing** costs **+1 AP**, and cannot **Jump**.

**Proposed text**

> **Max Speed 4"**, **Stand** costs **+1 AP**, and cannot **Jump**.

## Section 6

### COPY-07: 6.10 Sailor special rule

**Copy. Recommended.** The Terrain Tag is **Shallow Water** (2.9.6); the sentence already bolds the sibling tag **Slippery Terrain**.

*Line 2442, under "Sailor".* Dependencies: none.

**Current text**

> caused by wind, rain, ice, shallow water, and **Slippery Terrain** caused by water

**Proposed text**

> caused by wind, rain, ice, **Shallow Water**, and **Slippery Terrain** caused by water

### COPY-08: 6.13 Druid Wild Shape Forms table

**Copy. Recommended.** The other six Wild Shape forms are named by animal alone (Boar, Great Eagle, Lynx, Bear, Stag, Lion); 'Wolf Shape' breaks the parallel.

*Line 3230, under "Wild Shape Forms".* Dependencies: none.

**Current text**

> | **Wolf Shape** | Novice |

**Proposed text**

> | **Wolf** | Novice |

## Section 7

### SEC-07: 7.1 Equipment limits

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 3389, under "7.2 Universal Item Rules".* Dependencies: none.

**Current text**

> items from **Section 7.17** and does not count

**Proposed text**

> items from **7.17** and does not count

### CLAR-14: 7.2 Buying and selling, Sale value

**Clarity. Recommended.** The second sentence restates the rounding-and-minimum rule immediately before it.

*Line 3401, under "7.2 Universal Item Rules".* Dependencies: none.

**Current text**

> Round the sale value down to the nearest **1c**, minimum **0c**. An item with a final sale value below **1c** sells for **0c**.

**Proposed text**

> Round the sale value down to the nearest **1c**, minimum **0c**.

### CONS-01: 7.8 Weapons, abbreviation key

**Consistency. Recommended.** 5.4.3 lists acid among the damage types and the item tables use **(Ac)**; the abbreviation key omits it.

*Line 3634, under "7.8 Melee Weapons".* Dependencies: none.

**Current text**

> Damage type abbreviations in weapon tables: **(B)** blunt,

**Proposed text**

> Damage type abbreviations in weapon tables: **(Ac)** acid, **(B)** blunt,

### SEC-08: 7.11 Item Qualities

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 3746, under "Weapon Qualities".* Dependencies: none.

**Current text**

> grant that exact trait from **Section 7.7**.

**Proposed text**

> grant that exact trait from **7.7**.

### COPY-10: 7.11 Weapon Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3757, under "Weapon Qualities".* Dependencies: none.

**Current text**

> | Enchanted +1 | This weapon deals

**Proposed text**

> | **Enchanted +1** | This weapon deals

### COPY-11: 7.11 Weapon Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3758, under "Weapon Qualities".* Dependencies: none.

**Current text**

> | Enchanted +2 | This weapon deals

**Proposed text**

> | **Enchanted +2** | This weapon deals

### COPY-12: 7.11 Weapon Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3759, under "Weapon Qualities".* Dependencies: none.

**Current text**

> | Enchanted +3 | This weapon deals

**Proposed text**

> | **Enchanted +3** | This weapon deals

### COPY-13: 7.11 Weapon Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3760, under "Weapon Qualities".* Dependencies: none.

**Current text**

> | Enchanted +4 | This weapon deals

**Proposed text**

> | **Enchanted +4** | This weapon deals

### COPY-14: 7.11 Weapon Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3761, under "Weapon Qualities".* Dependencies: none.

**Current text**

> | Enchanted +5 | This weapon deals

**Proposed text**

> | **Enchanted +5** | This weapon deals

### COPY-15: 7.11 Armour Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3775, under "Armour and Shield Qualities".* Dependencies: none.

**Current text**

> | Enchanted +1 | **Chest only:**

**Proposed text**

> | **Enchanted +1** | **Chest only:**

### COPY-16: 7.11 Armour Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3776, under "Armour and Shield Qualities".* Dependencies: none.

**Current text**

> | Enchanted +2 | **Chest only:**

**Proposed text**

> | **Enchanted +2** | **Chest only:**

### COPY-17: 7.11 Armour Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3777, under "Armour and Shield Qualities".* Dependencies: none.

**Current text**

> | Enchanted +3 | **Chest only:**

**Proposed text**

> | **Enchanted +3** | **Chest only:**

### COPY-18: 7.11 Armour Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3778, under "Armour and Shield Qualities".* Dependencies: none.

**Current text**

> | Enchanted +4 | **Chest only:**

**Proposed text**

> | **Enchanted +4** | **Chest only:**

### COPY-19: 7.11 Armour Qualities table

**Copy. Recommended.** Every other quality name in the 7.11 tables is bold, and **Enchanted +X** is bold wherever else it appears.

*Line 3779, under "Armour and Shield Qualities".* Dependencies: none.

**Current text**

> | Enchanted +5 | **Chest only:**

**Proposed text**

> | **Enchanted +5** | **Chest only:**

### RULE-01: 7.9 Tier 5 Enhanced Weapon Table

**Rules. Owner decision.** Repeating Crossbow costs 20c (7.8). Every other enhanced ranged weapon follows base +36 for Enchanted +4, base +50 for Enchanted +5, and base ×4 for Adamantine (Longbow 17 → 53, 67). The three Repeating Crossbow entries (58, 72, 88) all fit a base of 22c instead.

**Owner decision.** Option A (patched): correct the three enhanced prices to 56, 70, 80 to match the 20c base. Option B: raise the 7.8 base cost to 22c and leave these three rows. Recommendation: A, because the base table is the authority players shop from and 20c sits between the Heavy Crossbow (15) and the Longbow (17) scale as intended.

*Line 4084, under "Tier 5 Enhanced Weapon Table (d20)".* Dependencies: none.

**Current text**

> | 5 | Enchanted +4 Repeating Crossbow | 58 |

**Proposed text**

> | 5 | Enchanted +4 Repeating Crossbow | 56 |

### RULE-02: 7.9 Tier 5 Enhanced Weapon Table

**Rules. Owner decision.** See RULE-01.

*Line 4093, under "Tier 5 Enhanced Weapon Table (d20)".* Dependencies: none.

**Current text**

> | 14 | Enchanted +5 Repeating Crossbow | 72 |

**Proposed text**

> | 14 | Enchanted +5 Repeating Crossbow | 70 |

### RULE-03: 7.9 Tier 5 Enhanced Weapon Table

**Rules. Owner decision.** See RULE-01.

*Line 4099, under "Tier 5 Enhanced Weapon Table (d20)".* Dependencies: none.

**Current text**

> | 20 | Adamantine Repeating Crossbow | 88 |

**Proposed text**

> | 20 | Adamantine Repeating Crossbow | 80 |

### COPY-20: 7.14 Tier 5 poison 3, World Serpent Venom

**Copy. Recommended.** 'For the rest of the round' is the only use in the manuscript; the timing phrase used everywhere else is 'until the end of the round'.

*Line 4432, under "Tier 5 Poisons".* Dependencies: 1 figure (FIG-76).

**Current text**

> target cannot move, heal, or use **Reactions** for the rest of the round.

**Proposed text**

> target cannot move, heal, or use **Reactions** until the end of the round.

### RULE-05: 7.17 Legendary Weapons 8, Magehunter Crossbow

**Rules. Owner decision.** 'A caster' is not a defined combatant category. The effect only does anything to a combatant with NRG, so naming that condition removes the ambiguity (compare Godsbane Distillate, which says 'a target that knows at least one Power').

**Owner decision.** Confirm the intended scope. 'Has **NRG**' is the recommended reading because the effect drains NRG; the alternative 'knows at least one Power' would also catch Power-using combatants without an NRG pool, on whom the drain does nothing.

*Line 4754, under "Tier 2 Special Weapons (APL 3–4)".* Dependencies: none.

**Current text**

> When this attack damages a caster, the target immediately loses **1 NRG**.

**Proposed text**

> When this attack damages a combatant that has **NRG**, the target immediately loses **1 NRG**.

### RULE-06: 7.17 Legendary Weapons 10, Thought-Eater Scourge

**Rules. Owner decision.** See RULE-05.

*Line 4786, under "Tier 4 Special Weapons (APL 7–8)".* Dependencies: none.

**Current text**

> When this attack damages a caster, the target loses **1 NRG** and you regain **1 NRG**.

**Proposed text**

> When this attack damages a combatant that has **NRG**, the target loses **1 NRG** and you regain **1 NRG**.

### COPY-21: 7.17 Legendary Artifact Armour 6, Archsage Vestments

**Copy. Recommended.** Faulty parallelism: 'Gain ..., are Resistant ..., and gain ...' has no subject for 'are'. Adding 'You' repairs it without touching the effect.

*Line 4812, under "Tier 5 Legendary Artifact Armour and Shields (d20)".* Dependencies: none.

**Current text**

> This armour is non-metal. Gain **+2** to **Casting Checks**, are **Resistant** to damage from Powers, and gain **+2** on **Checks** made to resist enemy Powers.

**Proposed text**

> This armour is non-metal. You gain **+2** to **Casting Checks**, are **Resistant** to damage from Powers, and gain **+2** on **Checks** made to resist enemy Powers.

### COPY-22: 7.17 Legendary Artifacts 14, Lenses of Apex Mastery

**Copy. Recommended.** Faulty parallelism: as written, the INT Checks 'ignore visual penalties' and 'gain +2 to Casting Checks'. The wearer does. Effects unchanged.

*Line 4860, under "Tier 5 Legendary Artifacts (d20)".* Dependencies: none.

**Current text**

> **INT Checks** are made with **Advantage**, ignore visual penalties, and gain **+2** to **Casting Checks**.

**Proposed text**

> Your **INT Checks** are made with **Advantage**. You ignore visual penalties and gain **+2** to **Casting Checks**.

### RULE-04: 7.17 Legendary Artifacts 15, Charm of Epic Luck

**Rules. Owner decision.** 'Gain +2 Luck' could mean two current Luck Points or a higher maximum. Every other Luck bonus in the manuscript reads 'Increase maximum **Luck** by **N**' (Halfling, Goblin, 6.10 background bonus).

**Owner decision.** Confirm the item raises maximum Luck (recommended, matching every other Luck bonus). If it is meant to grant two one-off Luck Points instead, say so explicitly rather than keep the ambiguous wording.

*Line 4861, under "Tier 5 Legendary Artifacts (d20)".* Dependencies: none.

**Current text**

> Gain **+2 Luck**. Rerolls made by spending

**Proposed text**

> Increase maximum **Luck** by **2**. Rerolls made by spending

## Section 8

### SEC-09: 8.2 Power durations

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 5313, under "Power Durations".* Dependencies: 1 figure (FIG-08).

**Current text**

> use the condition entry in **Section 5.9** unless the Power explicitly overrides it. A **Summon** uses the duration stated by their rule, or the default Summon duration in **Section 2.5.1**, and

**Proposed text**

> use the condition entry in **5.9** unless the Power explicitly overrides it. A **Summon** uses the duration stated by their rule, or the default Summon duration in **2.5.1**, and

### CLAR-01: 8.3 Known Powers

**Clarity. Recommended.** No class table says 'Learn 1 new Power'. The class entries say 'Learn one additional **Arcane Spell** at Levels 3, 5, ...' (eight entries), so the quoted bold label points at text that does not exist.

*Line 5382, under "Known Powers".* Dependencies: 1 figure (FIG-08).

**Current text**

> - When a class table says **Learn 1 new Power**, choose one Power from a tier that Hero can currently access.

**Proposed text**

> - When a class entry says to learn one additional Power, choose one Power from a tier that Hero can currently access.

### CLAR-03: 8.4/8.6 chain lightning Powers

**Clarity. Recommended.** 'Primary target' collides with the Monster AI term **Primary Target** (9.5), which has a specific meaning. These chain Powers mean the first target chosen; 'first target' says so and matches the 'additional targets' that follow.

*Line 5737, under "Tier 2 Arcane Spells (d20)".* Dependencies: none.

**Current text**

> Deal **2d6 + INT lightning damage** to the primary target. Then deal

**Proposed text**

> Deal **2d6 + INT lightning damage** to the first target. Then deal

### CLAR-04: 8.4/8.6 chain lightning Powers

**Clarity. Recommended.** 'Primary target' collides with the Monster AI term **Primary Target** (9.5), which has a specific meaning. These chain Powers mean the first target chosen; 'first target' says so and matches the 'additional targets' that follow.

*Line 5794, under "Tier 3 Arcane Spells (d20)".* Dependencies: none.

**Current text**

> Deal **4d6 + INT lightning damage** to the primary target. Then deal

**Proposed text**

> Deal **4d6 + INT lightning damage** to the first target. Then deal

### CLAR-05: 8.4/8.6 chain lightning Powers

**Clarity. Recommended.** 'Primary target' collides with the Monster AI term **Primary Target** (9.5), which has a specific meaning. These chain Powers mean the first target chosen; 'first target' says so and matches the 'additional targets' that follow.

*Line 6495, under "Tier 2 Sorceries (d20)".* Dependencies: none.

**Current text**

> Deal **2d6 + SPI lightning damage** to the primary target. Then deal

**Proposed text**

> Deal **2d6 + SPI lightning damage** to the first target. Then deal

### CLAR-06: 8.4/8.6 chain lightning Powers

**Clarity. Recommended.** 'Primary target' collides with the Monster AI term **Primary Target** (9.5), which has a specific meaning. These chain Powers mean the first target chosen; 'first target' says so and matches the 'additional targets' that follow.

*Line 6621, under "Tier 3 Sorceries (d20)".* Dependencies: none.

**Current text**

> Deal **4d6 + SPI lightning damage** to the primary target. Then deal

**Proposed text**

> Deal **4d6 + SPI lightning damage** to the first target. Then deal

### COPY-23: 8.6 Druidic Rituals, Summon Burrow Badger

**Copy. Recommended.** The Summon profile label should carry the Summon's full name as used by the Power and its Effect line.

*Line 6888, under "Tier 1 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Summon (Badger):**

**Proposed text**

> - **Summon (Burrow Badger):**

### COPY-24: 8.6 Druidic Rituals, Summon Great Hawk

**Copy. Recommended.** The Summon profile label should carry the Summon's full name as used by the Power and its Effect line.

*Line 6996, under "Tier 2 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Summon (Hawk):**

**Proposed text**

> - **Summon (Great Hawk):**

### RULE-07: 8.6 Druidic Rituals 17, Monster Lure

**Rules. Owner decision.** No rule defines a 'Monster Group marker'; Monster Groups are sets of Monster models (9.3), and 8.2 requires range and LOS to each target. As written, the Power has nothing to measure to.

**Owner decision.** Confirm that these four Powers target a Monster Group by measuring to any Monster in it (recommended; it is the only reading the current rules can resolve). Alternative: define a Monster Group marker in 9.3 instead, which is a larger rules addition.

*Line 7010, under "Tier 2 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Target:** 1 neutral Monster Group marker
> - **Effect:** When that group activates this round, replace its **Primary Target** priority with the nearest enemy combatant within **12"** of the marker.

**Proposed text**

> - **Target:** 1 neutral Monster Group (measure range and **LOS** to any **Monster** in that Group)
> - **Effect:** When that group activates this round, replace its **Primary Target** priority with the nearest enemy combatant within **12"** of any **Monster** in that Group.

### RULE-08: 8.6 Druidic Rituals 18, Beast Pacification

**Rules. Owner decision.** See RULE-07.

*Line 7016, under "Tier 2 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Target:** 1 neutral Monster Group marker whose group contains only **Monsters** with **Beast**
> - **Effect:** That group cannot make attacks

**Proposed text**

> - **Target:** 1 neutral Monster Group that contains only **Monsters** with **Beast** (measure range and **LOS** to any **Monster** in that Group)
> - **Effect:** That group cannot make attacks

### COPY-25: 8.6 Druidic Rituals, Summon Bear Guardian

**Copy. Recommended.** The Summon profile label should carry the Summon's full name as used by the Power and its Effect line.

*Line 7092, under "Tier 3 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Summon (Bear):**

**Proposed text**

> - **Summon (Bear Guardian):**

### COPY-26: 8.6 Druidic Rituals, Summon Carrion Hounds

**Copy. Recommended.** The Summon profile label should carry the Summon's full name as used by the Power and its Effect line.

*Line 7106, under "Tier 3 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Summon (Hound, Each):**

**Proposed text**

> - **Summon (Carrion Hound, Each):**

### RULE-09: 8.6 Druidic Rituals 15, Monster Stampede

**Rules. Owner decision.** See RULE-07.

*Line 7122, under "Tier 3 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Target:** 1 neutral Monster Group marker
> - **Effect:** Resolve each **Monster** in that group separately.

**Proposed text**

> - **Target:** 1 neutral Monster Group (measure range and **LOS** to any **Monster** in that Group)
> - **Effect:** Resolve each **Monster** in that group separately.

### RULE-10: 8.6 Druidic Rituals 16, Beast Commander

**Rules. Owner decision.** See RULE-07.

*Line 7128, under "Tier 3 Druidic Rituals (d20)".* Dependencies: none.

**Current text**

> - **Target:** 1 neutral Monster Group marker whose group contains only **Monsters** with **Beast**
> - **Effect:** During that group's next activation

**Proposed text**

> - **Target:** 1 neutral Monster Group that contains only **Monsters** with **Beast** (measure range and **LOS** to any **Monster** in that Group)
> - **Effect:** During that group's next activation

## Section 9

### CLAR-12: 9.1 Monster profile, CV

**Clarity. Recommended.** 10.5.11 is titled 'Reward Timing and Banking' and contains no 'outcome grade'; the description should match the section it points to.

*Line 7564, under "9.1 Monster Stat Profile".* Dependencies: player-aid sheet pa02.

**Current text**

> until the outcome-grade rules in **10.5.11** secure it

**Proposed text**

> until the reward-banking rules in **10.5.11** secure it

### SEC-10: 9.1 Monster profile

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 7577, under "9.1 Monster Stat Profile".* Dependencies: player-aid sheet pa02.

**Current text**

> following the **Monster** AI rules in **Section 9.5**,

**Proposed text**

> following the **Monster** AI rules in **9.5**,

### SEC-11: 9.3 Monster Groups

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 7649, under "A. Core AI Rules".* Dependencies: 3 figures (FIG-11, FIG-12, FIG-16); player-aid sheet pa02.

**Current text**

> as described in **Section 3.4**. Within an activating Group

**Proposed text**

> as described in **3.4**. Within an activating Group

### CLAR-13: 9.6 Swallow Whole

**Clarity. Recommended.** Monsters are never **Knocked Out** (that state belongs to Heroes in 5.8); a Monster at 0 HP is removed. 'Killed' is also not a defined state. The new wording uses the manuscript's own phrasing for Monster defeat (see 9.1 CV).

*Line 7766, under "9.6 Universal Special Abilities (SA) List".* Dependencies: none.

**Current text**

> If the swallowing **Monster** is **Knocked Out**, removed, or killed, place all swallowed targets

**Proposed text**

> If the swallowing **Monster** is reduced to **0 HP** or otherwise removed from play, place all swallowed targets

### SEC-12: 9.6 Special Abilities

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 7788, under "Interpreting Monster Special Abilities".* Dependencies: none.

**Current text**

> targeting priorities from **Section 9.5**.

**Proposed text**

> targeting priorities from **9.5**.

### CONS-02: 9 Elite Monsters, Terror Aura reminder

**Consistency. Recommended.** 9.6 defines **Terror Aura (X")** as functioning as **Frightful Presence (X")**, which applies to 'an enemy non-Monster combatant'. Monsters never make Checks (canon convention), so the reminder text should name the same scope.

*Line 9725, under "Demon [Elite]".* Dependencies: none.

**Current text**

> - **Terror Aura (4"):** An enemy that starts their activation within **4"** of this Monster must pass a **SPI Check** or become **Frightened**.

**Proposed text**

> - **Terror Aura (4"):** An enemy non-Monster combatant that starts their activation within **4"** of this Monster must pass a **SPI Check** or become **Frightened**.

### COPY-27: 9 Bosses, The Hollow Crown of the Ashlands [Boss]

**Copy. Recommended, optional.** Boss placement rules are the only place the manuscript writes 'place 2 **Name**' in the singular; every other count of two or more uses the plural ('4 Dire Wolves', '3 Satchels', '2 Feverwort markers'). All seven Boss rules share the pattern, so apply all seven or none.

*Line 10214, under "The Hollow Crown of the Ashlands [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> if fewer than 3 allied Undead are within **8"**, place 2 **Forsaken Knight** in legal spaces within **6"**

**Proposed text**

> if fewer than 3 allied Undead are within **8"**, place 2 **Forsaken Knights** in legal spaces within **6"**

### COPY-28: 9 Bosses, Avatar of the Old Growth [Boss]

**Copy. Recommended, optional.** Boss placement rules are the only place the manuscript writes 'place 2 **Name**' in the singular; every other count of two or more uses the plural ('4 Dire Wolves', '3 Satchels', '2 Feverwort markers'). All seven Boss rules share the pattern, so apply all seven or none.

*Line 10258, under "Avatar of the Old Growth [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> **Awaken the Grove (AI Step 1, on d6 6+):** Once per adventure, place 2 **Briarling** in

**Proposed text**

> **Awaken the Grove (AI Step 1, on d6 6+):** Once per adventure, place 2 **Briarlings** in

### COPY-29: 9 Bosses, The Broodmother Prime [Boss]

**Copy. Recommended, optional.** Boss placement rules are the only place the manuscript writes 'place 2 **Name**' in the singular; every other count of two or more uses the plural ('4 Dire Wolves', '3 Satchels', '2 Feverwort markers'). All seven Boss rules share the pattern, so apply all seven or none.

*Line 10281, under "The Broodmother Prime [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> place 2 **Giant Black Widow** in legal spaces

**Proposed text**

> place 2 **Giant Black Widows** in legal spaces

### CONS-04: 9 Bosses, Broodmother

**Consistency. Recommended.** See CONS-02. The 8" line is duplicated between two Bosses, so the find includes the preceding bullet to stay unique.

*Line 10293, under "The Broodmother Prime [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> - **Web Tyrant:** Allied spiders within **8"** roll their base damage dice with **Advantage**.
> - **Terror Aura (8"):** An enemy that starts their activation within **8"** of this Monster must pass a **SPI Check** or become **Frightened**.

**Proposed text**

> - **Web Tyrant:** Allied spiders within **8"** roll their base damage dice with **Advantage**.
> - **Terror Aura (8"):** An enemy non-Monster combatant that starts their activation within **8"** of this Monster must pass a **SPI Check** or become **Frightened**.

### COPY-30: 9 Bosses, Captain Veyr of the Forsaken [Boss]

**Copy. Recommended, optional.** Boss placement rules are the only place the manuscript writes 'place 2 **Name**' in the singular; every other count of two or more uses the plural ('4 Dire Wolves', '3 Satchels', '2 Feverwort markers'). All seven Boss rules share the pattern, so apply all seven or none.

*Line 10305, under "Captain Veyr of the Forsaken [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> Once per adventure, place 2 **Forsaken Knight** in legal spaces within **6"**, then all

**Proposed text**

> Once per adventure, place 2 **Forsaken Knights** in legal spaces within **6"**, then all

### CONS-05: 9 Bosses, Captain Veyr

**Consistency. Recommended.** See CONS-02 and CONS-04.

*Line 10315, under "Captain Veyr of the Forsaken [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> - **Cursed Command:** An enemy that ends their activation within **8"** of Captain Veyr becomes **Cursed**.
> - **Terror Aura (8"):** An enemy that starts their activation within **8"** of this Monster must pass a **SPI Check** or become **Frightened**.

**Proposed text**

> - **Cursed Command:** An enemy that ends their activation within **8"** of Captain Veyr becomes **Cursed**.
> - **Terror Aura (8"):** An enemy non-Monster combatant that starts their activation within **8"** of this Monster must pass a **SPI Check** or become **Frightened**.

### COPY-31: 9 Bosses, The Frost Bailiff Magistrate [Boss]

**Copy. Recommended, optional.** Boss placement rules are the only place the manuscript writes 'place 2 **Name**' in the singular; every other count of two or more uses the plural ('4 Dire Wolves', '3 Satchels', '2 Feverwort markers'). All seven Boss rules share the pattern, so apply all seven or none.

*Line 10327, under "The Frost Bailiff Magistrate [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> place 2 **White Court Guard** in

**Proposed text**

> place 2 **White Court Guards** in

### COPY-32: 9 Bosses, The Sun-Crowned Prince [Boss]

**Copy. Recommended, optional.** Boss placement rules are the only place the manuscript writes 'place 2 **Name**' in the singular; every other count of two or more uses the plural ('4 Dire Wolves', '3 Satchels', '2 Feverwort markers'). All seven Boss rules share the pattern, so apply all seven or none.

*Line 10350, under "The Sun-Crowned Prince [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> place 2 **Skeleton Warrior** in legal spaces

**Proposed text**

> place 2 **Skeleton Warriors** in legal spaces

### CONS-03: 9 Bosses, Terror Aura reminder

**Consistency. Recommended.** See CONS-02.

*Line 10360, under "The Sun-Crowned Prince [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> - **Terror Aura (10"):** An enemy that starts their activation within **10"** of this Monster must pass a **SPI Check** or become **Frightened**.

**Proposed text**

> - **Terror Aura (10"):** An enemy non-Monster combatant that starts their activation within **10"** of this Monster must pass a **SPI Check** or become **Frightened**.

### COPY-33: 9 Bosses, The Antlered Warden of the Tithe [Boss]

**Copy. Recommended, optional.** Boss placement rules are the only place the manuscript writes 'place 2 **Name**' in the singular; every other count of two or more uses the plural ('4 Dire Wolves', '3 Satchels', '2 Feverwort markers'). All seven Boss rules share the pattern, so apply all seven or none.

*Line 10371, under "The Antlered Warden of the Tithe [Boss]".* Dependencies: player-aid sheet pa02.

**Current text**

> **Call the Wild Court (AI Step 1, on d6 6+):** Once per adventure, place 2 **Briarling** in

**Proposed text**

> **Call the Wild Court (AI Step 1, on d6 6+):** Once per adventure, place 2 **Briarlings** in

## Section 10

### COPY-35: 10.1 Setup Roll-off

**Copy. Recommended.** The paragraph defines and otherwise always writes the full bold term **Setup Roll-off**.

*Line 11078, under "Setup Roll-off".* Dependencies: 39 figures (FIG-13 to FIG-57, see the dependency section); player-aid sheet pa10.

**Current text**

> The higher result wins the roll-off.

**Proposed text**

> The higher result wins the **Setup Roll-off**.

### SEC-13: 10.1 Adventure Preparation Sequence

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 11105, under "Preparation Steps".* Dependencies: 39 figures (FIG-13 to FIG-57, see the dependency section); player-aid sheet pa10.

**Current text**

> APL as described in **Section 6.14**.

**Proposed text**

> APL as described in **6.14**.

### RULE-11: 10.2 Secondary Objective, Lodestone

**Rules. Owner decision.** 'Base contact' appears only in this Secondary Objective; the game is played on a square grid and every other proximity rule uses 'adjacent'.

**Owner decision.** Confirm 'adjacent' is the intended trigger (recommended). On a grid, base contact and adjacency are the same thing, but the change is to a scoring objective so the owner should confirm.

*Line 11531, under "Climate 3: Undermarches Secondary Objectives (1d20)".* Dependencies: none.

**Current text**

> An AP-using non-Monster combatant in base contact with the Lodestone is **Immobilized**

**Proposed text**

> An AP-using non-Monster combatant adjacent to the Lodestone is **Immobilized**

### RULE-12: 10.2 Secondary Objective, Lodestone

**Rules. Owner decision.** See RULE-11.

*Line 11531, under "Climate 3: Undermarches Secondary Objectives (1d20)".* Dependencies: none.

**Current text**

> A Monster in base contact is **Immobilized** until the end of their next activation

**Proposed text**

> A Monster adjacent to the Lodestone is **Immobilized** until the end of their next activation

### RULE-13: 10.2 Secondary Objective, Lodestone

**Rules. Owner decision.** See RULE-11.

*Line 11532, under "Climate 3: Undermarches Secondary Objectives (1d20)".* Dependencies: none.

**Current text**

> A Hero in base contact with the Lodestone pries loose

**Proposed text**

> A Hero adjacent to the Lodestone pries loose

### COPY-34: 10.3 Greenmark weather table

**Copy. Recommended.** 'Standard conditions apply' repeats 'No adverse weather effects apply'; the other climates' clear-weather rows carry one sentence.

*Line 11948, under "Climate 1: Greenmark Weather Table".* Dependencies: none.

**Current text**

> | 6 | Dappled Sunlight | Shifting light and shade play across the forest floor. No adverse weather effects apply. Standard conditions apply. |

**Proposed text**

> | 6 | Dappled Sunlight | Shifting light and shade play across the forest floor. No adverse weather effects apply. |

### CLAR-02: 10.3 Ashlands weather table

**Clarity. Recommended.** 'The ambient heat is notable' has no rules content and the parenthetical is hard to parse. The Sun-Drowned row 6 already says the same thing cleanly; this mirrors it.

*Line 11959, under "Climate 2: Ashlands Weather Table".* Dependencies: none.

**Current text**

> | 6 | Clear Skies, Hot Air | No adverse weather effects apply, but the ambient heat is notable (carrying Waterskins remains specified by the scenario). |

**Proposed text**

> | 6 | Clear Skies, Hot Air | No adverse weather effects apply beyond any scenario rule that requires water. |

### CLAR-07: 10.4 Core Scenario victory conditions

**Clarity. Recommended.** The manuscript's term is 'battlefield' (carried off the battlefield, leave the battlefield, battlefield edge); 'off-map' appears only in these five victory conditions and 'map' is not otherwise a rules term.

*Line 12080, under "Scenario 1: Hunt the Wild Beast [Intro]".* Dependencies: 41 figures (FIG-13 to FIG-56, see the dependency section).

**Current text**

> The adventure ends when the Pelt is carried off-map,

**Proposed text**

> The adventure ends when the Pelt is carried off the battlefield,

### CLAR-08: 10.4 Core Scenario victory conditions

**Clarity. Recommended.** The manuscript's term is 'battlefield' (carried off the battlefield, leave the battlefield, battlefield edge); 'off-map' appears only in these five victory conditions and 'map' is not otherwise a rules term.

*Line 12377, under "Scenario 5: The Ambushed Emissary".* Dependencies: 41 figures (FIG-13 to FIG-56, see the dependency section).

**Current text**

> The adventure ends when the Satchel is carried off-map,

**Proposed text**

> The adventure ends when the Satchel is carried off the battlefield,

### CLAR-09: 10.4 Core Scenario victory conditions

**Clarity. Recommended.** The manuscript's term is 'battlefield' (carried off the battlefield, leave the battlefield, battlefield edge); 'off-map' appears only in these five victory conditions and 'map' is not otherwise a rules term.

*Line 12463, under "Scenario 6: Ritual of the Old Growth".* Dependencies: 41 figures (FIG-13 to FIG-56, see the dependency section).

**Current text**

> when the Totem is carried off-map,

**Proposed text**

> when the Totem is carried off the battlefield,

### CLAR-10: 10.4 Core Scenario victory conditions

**Clarity. Recommended.** The manuscript's term is 'battlefield' (carried off the battlefield, leave the battlefield, battlefield edge); 'off-map' appears only in these five victory conditions and 'map' is not otherwise a rules term.

*Line 12744, under "Scenario 4: The Sealed Archive".* Dependencies: 41 figures (FIG-13 to FIG-56, see the dependency section).

**Current text**

> The adventure ends when the Archive Codex is carried off-map,

**Proposed text**

> The adventure ends when the Archive Codex is carried off the battlefield,

### CLAR-11: 10.4 Core Scenario victory conditions

**Clarity. Recommended.** The manuscript's term is 'battlefield' (carried off the battlefield, leave the battlefield, battlefield edge); 'off-map' appears only in these five victory conditions and 'map' is not otherwise a rules term.

*Line 12816, under "Scenario 5: The Reliquary of Broken Saints".* Dependencies: 41 figures (FIG-13 to FIG-56, see the dependency section).

**Current text**

> The adventure ends when Kest's Reliquary is carried off-map,

**Proposed text**

> The adventure ends when Kest's Reliquary is carried off the battlefield,

### SEC-14: 10.4 Chasm scenario rules

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 13050, under "Scenario 2: The Chasm Crossing".* Dependencies: 41 figures (FIG-13 to FIG-56, see the dependency section).

**Current text**

> **Jump** rules in **Section 4.4.9**.

**Proposed text**

> **Jump** rules in **4.4.9**.

## Appendix B

### COPY-09: B.4 Mossgrave hero card

**Copy. Recommended.** Follows COPY-08 so the hero card matches the class table. Requires hero-card re-extraction after promotion.

*Line 17220, under "Mossgrave".* Dependencies: 1 figure (FIG-19); `tools/hero_cards.py` (B.4 re-extraction).

**Current text**

>   - **Wolf Shape:** Speed **7"**

**Proposed text**

>   - **Wolf:** Speed **7"**

## Appendix C

### SEC-15: C.1 Round sequence

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 17732, under "C.1 Timing Summary".* Dependencies: player-aid sheet pa01.

**Current text**

> - Activate each **Awake** Monster Group as described in **Section 3.4**.

**Proposed text**

> - Activate each **Awake** Monster Group as described in **3.4**.

### COPY-36: C.3 Conditions quick reference, Hidden row

**Copy. Recommended.** The defined term (5.9 Hidden, 2.8, 4.3.2) is **Hide distance**, bolded as one term.

*Line 17794, under "C.3 Conditions Summary".* Dependencies: player-aid sheets pa02, pa05.

**Current text**

> use that distance as your **Hide** distance while the rule applies

**Proposed text**

> use that distance as your **Hide distance** while the rule applies

### SEC-16: C.6 and Glossary, Empower

**Copy. Recommended.** Same normalization; this sentence occurs twice (C.6 and the glossary), so the patch replaces both. This find occurs **2** times and the patch replaces every occurrence (`expected_count: 2`).

*First occurrence at line 17897, under "C.7 Power Summary".* Dependencies: none.

**Current text**

> See **Empower** in **Section 8.2**.

**Proposed text**

> See **Empower** in **8.2**.

### CONS-08: Glossary, Adamantine

**Consistency. Recommended.** 7.6 is Treasure Tables; the Adamantine quality is defined in 7.11 Item Qualities.

*Line 17963, under "C.11 Glossary of Terms and Conditions".* Dependencies: none.

**Current text**

> **Adamantine** items are metal for rules that care whether an item is metal. See **7.6**.

**Proposed text**

> **Adamantine** items are metal for rules that care whether an item is metal. See **7.11**.

### CONS-10: Glossary, Blood Surge

**Consistency. Recommended.** The glossary entry is a placeholder ('as defined by the specific rule that grants it'); Blood Surge is one specific Novice Sorcerer Talent in 6.13. The new entry summarizes that Talent and points to it.

*Line 18011, under "C.11 Glossary of Terms and Conditions".* Dependencies: none.

**Current text**

> **Blood Surge:** A Sorcery or Sorcerer rule that increases power through blood-fuelled cost or backlash, as defined by the specific rule that grants it.

**Proposed text**

> **Blood Surge:** A Novice Sorcerer Talent. Once per round, after a **Sorcery's** damage is rolled but before mitigation, the caster may lose HP up to their current Level, to a maximum of **5 HP**, and add the same amount to the damage applied to one enemy affected by that roll. See **6.13**.

### CONS-09: Glossary, Wild Shape

**Consistency. Recommended.** 6.12 is General Talents; Wild Shape is in the Druid entry of 6.13 Hero Classes.

*Line 18349, under "C.11 Glossary of Terms and Conditions".* Dependencies: none.

**Current text**

> replacing **SPD**, **Sz**, and other listed values. See **6.12**.

**Proposed text**

> replacing **SPD**, **Sz**, and other listed values. See **6.13**.

### CONS-07: C.12 Parry worked example

**Consistency. Recommended.** Same collision with the 11.2.5 Guard Hireling (shortsword, **+4 STR**). The weapon is the Handaxe (7.8), one word; lowercased to match 'shortsword' in the same example.

*Line 18367, under "Melee Combat Example".* Dependencies: none.

**Current text**

> *A Raider attacks a Guard with a hand axe. The Guard declares **Parry** before any damage dice are rolled. The Raider then rolls **1d6 = 5**, adds **+2 STR**, and would deal **7 damage**. The Guard rolls a parry total with a shortsword: **1d6 = 5**, plus **+4 STR**, for **9**. The parry succeeds, so the Guard takes **0 damage**. Because the Guard's parry base die was not a maximum result, no **Riposte** damage is dealt back.*

**Proposed text**

> *A Raider attacks a Fighter with a handaxe. The Fighter declares **Parry** before any damage dice are rolled. The Raider then rolls **1d6 = 5**, adds **+2 STR**, and would deal **7 damage**. The Fighter rolls a parry total with a shortsword: **1d6 = 5**, plus **+4 STR**, for **9**. The parry succeeds, so the Fighter takes **0 damage**. Because the Fighter's parry base die was not a maximum result, no **Riposte** damage is dealt back.*

### COPY-37: C.12 Monster Phase worked example

**Copy. Recommended.** This worked example in C.12 is the only one in the appendix set in roman type; the sibling examples in C.12 are italic, and the build styles examples by their emphasis.

*Line 18379, under "Monster AI Example".* Dependencies: none.

**Current text**

> During the **Monster Phase**, Groups 1, 2, and 4 are **Awake**. They activate in ascending group number order: Group 1 first, then Group 2, then Group 4. When Group 2 activates, no rule sets the order of its individual Monsters, so use **Random Determination** to choose which remaining Monster activates next. Each chosen Monster executes the **first valid instruction** of the **Standard Monster AI Script** and ends their activation before another Monster in the Group is chosen. No player chooses to delay or reorder the Groups or their individual Monsters.

**Proposed text**

> *During the **Monster Phase**, Groups 1, 2, and 4 are **Awake**. They activate in ascending group number order: Group 1 first, then Group 2, then Group 4. When Group 2 activates, no rule sets the order of its individual Monsters, so use **Random Determination** to choose which remaining Monster activates next. Each chosen Monster executes the **first valid instruction** of the **Standard Monster AI Script** and ends their activation before another Monster in the Group is chosen. No player chooses to delay or reorder the Groups or their individual Monsters.*

### CONS-11: C.12 Monster AI worked example

**Consistency. Recommended.** Poison Breath (Green Dragon, 9) deals **4d8 poison damage** with no Check, so 'the listed Checks' points at nothing. Also italicizes the example to match its siblings (see COPY-37).

*Line 18383, under "Hostile AI Step 1 Example".* Dependencies: none.

**Current text**

> A **Green Dragon** begins their activation with three Heroes clustered in front of them. They roll **5** for **Poison Breath (AI Step 1, on d6 5+)**, so the AI Step is valid. Place the cone using the Monster area-placement priorities, resolve the listed Checks and damage, and end the Dragon's activation.

**Proposed text**

> *A **Green Dragon** begins their activation with three Heroes clustered in front of them. They roll **5** for **Poison Breath (AI Step 1, on d6 5+)**, so the AI Step is valid. Place the cone using the Monster area-placement priorities, resolve the listed damage, and end the Dragon's activation.*

### SEC-17: C.12 Round sequence

**Copy. Recommended.** Subsection cross-references are written as a bare bold number (**9.5**, **3.4.2**) in over a hundred places; these 19 'Section N.N' forms are the outliers. Whole-chapter references ('Section 7') are left as they are.

*Line 18424, under "Round Sequence".* Dependencies: none.

**Current text**

> then activate each **Awake** Monster Group as described in **Section 3.4**.

**Proposed text**

> then activate each **Awake** Monster Group as described in **3.4**.

### COPY-38: C.13 Terrain and Cover Snapshot

**Copy. Recommended.** Every other bullet in the Terrain and Cover Snapshot begins its definition with a capital.

*Line 18524, under "Terrain and Cover Snapshot".* Dependencies: none.

**Current text**

> - **Dangerous Terrain:** resolve the listed hazard

**Proposed text**

> - **Dangerous Terrain:** Resolve the listed hazard

## Whole manuscript

### HYPH-01: Whole manuscript, 16 occurrences

**Copy. Recommended, optional.** The manuscript hyphenates every other 'non-' compound (non-metal, non-Monster, non-consumable, and non-magical ×12) but closes 'nonmagical' ×16 and 'nonadjacent' ×10. Hyphenating the two closed forms removes the split with the fewest changes; none of the occurrences is in italic lore. The alternative is to close the 12 'non-magical' instead, which would also need its own patch. This find occurs **16** times and the patch replaces every occurrence (`expected_count: 16`).

*First occurrence at line 793, under "2.8.3 Darkness".* Dependencies: 2 figures (FIG-19, FIG-63); player-aid sheet pa07.

**Current text**

> nonmagical

**Proposed text**

> non-magical

### HYPH-02: Whole manuscript, 10 occurrences

**Copy. Recommended, optional.** See HYPH-01. Note that one occurrence sits in 2.9.1, on which the scenario figures depend, so this patch alone re-marks about 40 figures. This find occurs **10** times and the patch replaces every occurrence (`expected_count: 10`).

*First occurrence at line 791, under "2.8.3 Darkness".* Dependencies: 40 figures (FIG-07 to FIG-63, see the dependency section); player-aid sheet pa07.

**Current text**

> nonadjacent

**Proposed text**

> non-adjacent

## Checked and deliberately left alone

- **Bold-list punctuation.** The pattern '**Small (S), Medium (M), Large (L),** or **Huge (H)**' (comma inside the bold run) is used 22 times and is the house style, not an error.
- **'Hero that' and 'Hero who'.** Both forms are used throughout (the 1.5 retirement list mixes them in one paragraph). Normalizing would be dozens of patches for no gain in meaning.
- **Bold numerals.** Some rules sentences bold their numbers and some do not (2.7.2 'a corner shared by 2 **Blocking Terrain** squares'). The convention is not uniform enough to normalize without several hundred patches, and the item tables are internally consistent.
- **Serial 'and' in the 2.9.1 feature lists.** Some table cells list examples with a serial comma and some without; these are descriptive lists inside cells, and the rules prose itself is consistent.
- **'Resistance' in 4.4.10.** 5.4.4 defines Resistance as the rule and **Resistant** as the state, so 'cannot be reduced by **AV**, **AD**, **Resistance**, or **Immune**' is correct as written.
- **'Already Wounded' and 'heal'.** 'Wounded' and 'Heal / Healing' are both glossary-defined, so the poison and artifact entries that use them ('if the target is already Wounded', 'heal **1d6 HP**') were left alone, and COPY-20 keeps 'heal'.
- **Scenario-specific Terror Auras** at lines 13707 and 13992 use their own trigger wording ('within the Aura', 'entering or starting'). They belong to scenario Monsters, Monsters never make Checks under the settled convention, and only the bestiary reminders that copy the 9.6 template were aligned (CONS-02 to CONS-05).
- **Whole-chapter references** ('Section 7', 'Section 8', 'Section 10') read naturally and are left as they are; only the subsection forms were normalized (SEC-01 to SEC-17).
- **The 31c entry** in the 7.6 Tier 5 treasure table was checked against its neighbours and left alone.
- **B.5 Basic Mode profiles** omit Darkvision and the blunt Vulnerability that the full bestiary profiles carry. This reads as a deliberate simplification for the teaching mode, so it is noted here and not patched.
- **B.4 Club entry format, Lantern versus Lantern (Hooded), and the italic potion names in 11.1.3** were each checked; they follow their own local pattern and no patch improves them.
- **Pricing.** Every Masterwork, Silvered, Cold Iron, Sacred, Palesteel, Elven, Enchanted, and Adamantine row was recomputed from its base cost. The only departures are the Repeating Crossbow (RULE-01 to RULE-03) and the Buckler (owner decision 6, no patch). Full Plate and Steel Lamellar follow their own stated rules.
- **Mechanical sweeps that found nothing to patch.** All 'See **N.N**' and bold cross-references resolve to an existing heading; every d6, d10, d12, and d20 table has a complete range; every AI Step says 'ends' or 'continues'; every Monster named in a scenario or Boss rule has a profile; every scenario named in 10.1 and C.9 exists; no curly quotes, em dashes, or double spaces; no American spellings ('armor', 'color', 'defense').

## Coverage

| Lines | Content | Read |
|---|---|---|
| 1–160 | Title and table of contents | yes |
| 161–215, 405–440 | Section 1 non-italic text (route table, glance box, 1.4 to 1.6) | yes; italic lore excluded |
| 441–986 | Section 2 | yes |
| 987–1161 | Section 3 | yes |
| 1162–1468 | Section 4 | yes |
| 1469–1995 | Section 5 | yes |
| 1996–3343 | Section 6 | yes |
| 3344–5203 | Section 7 | yes |
| 5204–7549 | Section 8 | yes |
| 7550–11014 | Section 9, including Elites and Bosses | yes; italic lore excluded |
| 11015–15018 | Section 10 | yes |
| 15019–16123 | Section 11 | yes |
| 16124–16561 | Appendix A | yes |
| 16562–17688 | Appendix B, including B.4 and B.5 | yes |
| 17689–18552 | Appendix C, including the glossary and worked examples | yes |

## Approval process

1. The owner approves, declines, or amends findings by ID. Rules findings need an explicit decision; the recommendation is stated on each.
2. Approved patches are set to `status: "approved"` in the JSON twin, the declined ones removed, and the file given an `authorization` line quoting the owner's instruction and date.
3. `python tools/revise_manuscript.py --patches editorial/proposals/rc527-rules-text-review.json --reason ... --authorization ...` creates `source/Heraldry_RC527.md` and `editorial/history/RC527.json`. The tool rejects the batch if any `find` no longer matches exactly once (or exactly `expected_count` times).
4. Afterwards: re-extract the hero cards if COPY-09 was approved, re-record `production/aids/fidelity.json` after diffing each changed section, re-confirm the stale figure reviews, run `python tools/dev.py check`, update `production/STATE.md`, and commit. No build unless the owner asks for one.
