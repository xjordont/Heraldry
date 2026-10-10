# RC487 manuscript contradiction repairs

Owner-authorized repair of the RC486 audit: **21 findings and 6 questions resolved**. RC484–RC486 are immutable. RC487 is d77a72f9030061f76ea61e947bf520dcc81628bd653f61ba144f2a474a088254.

**All 835 printed finished item price cells are unchanged.** Developmental item-value formulas, quality-table value adjustments and trait multipliers were removed. The previous proposed price recalculations CA-10–CA-13 are withdrawn. Mechanical quality effects, base prices, treasure outcomes, sale percentages and existing Masterwork cost differences remain intact. Unpriced granted qualities retain the existing value; unpriced enhancements are not newly priced for purchase or upgrade.

The batch makes 48 exact replacements. Summary rules follow their governing rules. Special weapons inherit missing handling fields from their named mundane type; Maul means War Maul and Dual Daggers means the existing pair. Charge abilities explicitly make their already named attack. Scenario names, setup dependencies, small-party deployment, central objectives, forced breaking, damage-type timing and designated-item victories now resolve consistently. Monster protection modifies the hostile-source Check rather than inventing Monster ability scores. Ice walls and complex terrain now have bounded, usable geometry.

## Resolution ledger

| ID | Finding/question | Resolution |
|---|---|---|
| F01 | Spot summaries omit the higher SPI option | Spot summaries omit the higher SPI option; Spot summaries omit the higher SPI option |
| F02 | DEX Pen glossary says damage is unaffected | DEX Pen glossary says damage is unaffected |
| F03 | Impassable Terrain summaries omit the Cover exception | Impassable Terrain summaries omit the Cover exception; Impassable Terrain summaries omit the Cover exception |
| F04 | 9.5 allegiance summary omits same-Group allies | 9.5 allegiance summary omits same-Group allies |
| F05 | C.13 AI flow continues after a valid AI Step | C.13 AI flow continues after a valid AI Step |
| F06 | Fifteen enhanced-table values differ from the quality formula | Remove developmental value multipliers from material/craftsmanship traits; preserve their effects.; Owner-selected fixed prices govern; remove the pricing formula and example. Unpriced granted qualities retain the existing value rather than generating a new price.; Remove only the developmental Value column from the quality table; retain every quality effect.; Remove only the developmental Value column from the quality table; retain every quality effect.; Align the equipment reference with fixed item values.; Define base value as the finished listed price; retain sale percentages, rounding and minimum.; Use only stated Masterwork prices for upgrades; retain the existing cost difference, minimum and resale rule. |
| F07 | Fifty Special Weapon rows lack an explicit complete equipment profile | Inherit only missing handling/profile fields; preserve every printed cost, damage, trait and effect. Use the existing Thrown default, correcting the audit overstatement. |
| F08 | Burning Seal uses an unbounded “maximum possible” Parry value | Maximize base dice only; retain normal explosions and Riposte instead of an undefined maximum whole roll. |
| F09 | Two AI charge abilities grant a bonus to an attack they never perform | The charge performs its named attack if engaged, then ends under normal AI-Step timing.; Skeletal Beast performs the named charge attack without continuing the rest of AI. |
| F10 | Bandit’s Toll requires two deployed Heroes in a legal one-Hero game | Support one-Hero parties without changing deployment for larger parties. |
| F11 | Spider Silk Route does not designate a central Bundle; scaled second Bundle can disappear | Use one of the existing Webbed Sections at the central Boss/Bundle location; add no terrain count.; Designate a central existing objective and retain it when scaling reduces the count; preserve the printed count of three.; Preserve the two resting tarantulas when one objective remains; use an existing peripheral Webbed Section. |
| F12 | Ambushed Emissary Group 3 has incompatible placement geometry | Retain the explicit six-inch distance and wake trigger; remove the incompatible Camp-perimeter requirement. |
| F13 | Two solo objective fields use names absent from their scenario objects | Two solo objective fields use names absent from their scenario objects; Two solo objective fields use names absent from their scenario objects |
| F14 | Shifting Sands asks for extraction of undefined Chronal Chests | Count the two generated chests actually looted; do not create portable chests or new carrying rules. |
| F15 | Iron-Vein Vault forcing action does not state its successful effect | A successful forcing Check breaks the Point through its existing zero-HP transition. |
| F16 | Swirling Vials determines damage type after damage is inflicted | Choose the existing damage type once per declared attack before Reactions, damage and mitigation. |
| F17 | Icebound Court immediate ending prevents its same-round contest | Retain the same-round contest and resolve it at round end. An opponent’s item does not satisfy the designated objective or end the game early. |
| F18 | Ritual Chant gives Monsters Advantage on Checks they never roll | Move the defensive modifier to the existing hostile-source Check; Monsters still never roll Checks and gain no invented scores or immunity. |
| F19 | Teaching example omits Mara’s automatic armour reduction | Author an explicit illustrative armour roll of 2 and apply automatic AD; no observed roll is claimed.; Propagate Mara’s corrected HP through both remaining state summaries. |
| F20 | Teaching example ignores the Dire Wolf’s retained maximum and piercing Critical Hit | Retain the printed critical base roll; author a bonus 2 and apply piercing armour bypass, leaving Varek conscious at 1 HP.; Propagate the Critical Hit through the final teaching state. |
| F21 | Basic Mode combined Traps/Hidden Strongbox variants cannot allocate all tokens | Supply two extra blank tokens for the two extra markers, preserving the printed trap count.; Identify one real Strongbox before pickup traps; discard fake tokens unseen, remove other fakes on success and retain real identity after a trapped pickup. |
| U01 | Created ice wall placement/profile | Bound the wall to an adjacent origin; use the existing Line width of 1 inch and preserve length, height, expiry and continuation.; Make the terrain footprint, adjacent placement and attackable-object resolution explicit; preserve HP, AV and three-round lifespan. |
| U02 | Command Tent and other complex-terrain interiors | Assign the existing complex feature’s parts so its plans and Commander are legally accessible.; Keep the Dais body impassable while identifying the intended legal upper surface for its Boss and hazard.; Separate the inaccessible mound exterior from its enterable flooded sanctum; add no depth, movement cost or new hazard. |
| U03 | Chasm Crossing solo extraction direction | Two solo objective fields use names absent from their scenario objects |
| U04 | War Room bonus in PvE Initiative | Apply existing party Initiative bonuses in PvE, including War Room/Veteran and explicit PvE bonuses, without importing leader ability scores. |
| U05 | Move-only Monster steps and “in Reach” wording | Clarify the existing move-only fallback without adding an attack.; Clarify the existing move-only fallback without adding an attack.; Use the listed Bash’s ordinary melee distance, without granting Reach. |
| U06 | Teaching aids: two-square footprint and objective setup order | Use an existing standard footprint in the multi-square LOS example.; Order existing solo setup tasks so referenced terrain/objectives exist before dependent Monster deployment; keep eleven steps.; Match the solo setup example to the dependency order. |

## Teaching example

These two dice are newly authored illustrative results, not observations. Mara: 4 + 3 = 7 attack damage, automatic Gambeson AD 2, suffers 5; 12 → **7 HP**. Varek: Advantage retains 8, Critical Hit explodes for an illustrative 2; 8 + 2 + 1 = **11 piercing damage**, bypassing all AV including AD; 12 → **1 HP**. Their later state summaries agree. The earlier failed STR Check still leaves Varek Prone; the following successful Check does not remove it.

## Verification and scope

Exact reconstruction of all 48 archived patches and immutable snapshot hashes PASS. Independent parsing confirms all 835 finished prices are unchanged, 332 tables remain, and all 50 Special Weapon rows map to available mundane handling profiles. Historical RC486 audit evidence is reproduced independently from its pinned snapshot and is superseded by this resolution ledger, not rewritten as a current failure. Thrown already had a 6-inch default; that part of F07 was an audit overstatement.

The publication additionally withholds proposed or low-score artwork until approval. No new art generation or art approval was performed. Figure and PDF review, release verification, and package evidence are recorded separately after the rebuild.

This clearance covers the audited 27 items; it is not a formal gameplay proof. The original GitHub email’s three annotation texts remain unavailable through the plugin; this report does not invent them. Physical printing remains untested.
