"""Figure metadata for figures/manifest.json and figures/placements.json.

Single source of truth for IDs, captions, insertion targets and semantic checks.
Historical line spans refer to RC484/RC485; placements resolve via config/content_anchors.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.abspath(os.path.join(HERE, ".."))

DEP_MAP = {
    "A Opposite long edges (fixed)": [
        "Greenmark 1 Hunt the Wild Beast (12025)", "Ashlands 1 The Fallen Observatory (12481)",
        "Ashlands 5 The Reliquary of Broken Saints (12759)", "Ashlands 6 The Iron-Vein Vault (12846)",
        "Sun-Drowned 1 The Oasis Raiders (13819)", "The Mire 5 Salttide's Reckoning, along the outer banks (14554; 6\" per 10.1 step 11 default)"],
    "B Opposite short edges (fixed)": [
        "Ashlands 2 The Guardian's Test (12546)", "Ashlands 4 The Sealed Archive (12680)",
        "Undermarches 5 The Shadowed Under Passage, Party A at the end farther from the Heart (13239)",
        "Undermarches 6 The Ritual of Shadow Binding, Party A at one short edge (13318)",
        "Pale City 2 The Alchemist's Frozen Laboratory (13470)", "Pale City 3 The Haunted Mausoleum, outside the mausoleum (13541)",
        "Pale City 6 The Icebound Court (13745)", "Sun-Drowned 2 The Cinder Lord's Lost Brazier, converging on the plaza (13884; 6\" per 10.1 step 11 default)",
        "Sun-Drowned 6 The Cinder Lord's Obsidian Prison (14168)", "The Mire 1 The Reliquary of Edrava Salttide, driest banks (14254)",
        "The Mire 4 The Blighted Heartwood (14477)", "The Mire 6 The Serpent's Sunken Hoard, outside the Sinkhole area (14633; 6\" per 10.1 step 11 default)"],
    "A or B (edges stated only as 'opposite battlefield edges'; the Setup Roll-off winner chooses the edge and the other party takes the opposite one, 10.1 step 11 default, zone 6\" deep)": [
        "Pale City 5 The Ice Wyrm's Hoard, where tunnel approaches enter (13671)", "Sun-Drowned 4 The Sandwyrm's Lair (14018)",
        "Sun-Drowned 5 The Cursed Colossus of the Waste (14089)", "The Mire 2 The Lizardfolk's Stolen Offerings (14325)"],
    "C Roll-off winner chooses the edge": [
        "Greenmark 6 Ritual of the Old Growth, a long edge (12398)", "Pale City 4 The Clockwork Menagerie, any battlefield edge (13603)"],
    "D Roll-off winner chooses a corner": ["Greenmark 2 The Whispering Grove (12096)"],
    "E Opposite corner zones": [
        "Greenmark 5 The Ambushed Emissary, alternate placing (12314)", "Ashlands 3 The Shifting Sands of Time, alternate placing (12604)",
        "Undermarches 1 The Crystal Harvest, alternate placing (12929)", "Undermarches 4 The Undermarches Outpost Raid, alternate placing (13166)",
        "Pale City 1 Plunder of the Frozen Ruins, 8x8 zones, alternate placing per 10.1 step 11 default (13404)",
        "Sun-Drowned 3 Tomb of the Sunken Kings, 8x8 zones and alternate placing per 10.1 step 11 default (13955)", "The Mire 3 The Mire Titan's Fen, outer banks, 8x8 zones and alternate placing per 10.1 step 11 default (14402)"],
    "FIG-14 A Trail": ["Greenmark 3 The Bandit's Toll (12170)"],
    "FIG-14 B One shared short edge": ["Undermarches 2 The Chasm Crossing (12997)"],
    "FIG-14 C Central Safe Zone": ["Undermarches 3 The Quake (13062)"],
    "FIG-14 D Across a Ravine": ["Greenmark 4 The Spider's Silk Route (12238)"],
}

META = {
    "FIG-01": dict(
        title="Round and phase sequence",
        purpose="Show the four phases of a round in order, what each resolves, the loop to the next round, and the stated order exception.",
        source_refs=["3.1 Overview of a Round (source lines 985-1016)", "3.2 Initiative Phase (1017-1036)", "3.3 Party Phase (1037-1090)",
                     "3.4 Monster Phase (1091-1120)", "3.5 End of Round (1121-1131)"],
        geometry_spec="Four phase boxes in order (Initiative, Party, Monster, End of Round) with arrows; bullet text restates 3.1-3.5; return arrow to the next round; exception strip shows Initiative > Monster > Party > End of Round.",
        caption="The four phases of a round in order. If a specific rule places the Monster Phase before the Party Phase, both phases still resolve once before End of Round (see 3.1).",
        insert_after="B01015", scope="full", schematic=False,
        semantic_check="Phase names, bullet content and order compared with lines 985-1015; initiative formula, first-activation choice, Pass rule and group-number activation compared with 3.2-3.4; End of Round list compared with 3.5 (1121-1131); exception compared with 3.1 last paragraph (1015) and 3.4.3 (1117)."),
    "FIG-02": dict(
        title="Activation, AP and Reaction timing",
        purpose="Show the activation procedure and where AP and Reactions fall in a round, using a Hero's 3 AP.",
        source_refs=["2.5 Action Points and Summons (564-571)", "3.3.1 Activating a Combatant (1055-1072)", "3.3.2 Unspent AP and Reactions (1073-1080)",
                     "4.2 Universal Actions (1200-1220)", "4.5 Reactions (1418-1435)", "5.5.1 Block (1623-1632)"],
        geometry_spec="Panel A: eligibility list, 5 numbered activation steps, Reaction note. Panel B (added worked example, assumptions stated: Hero with a shield): 3 AP at Initiative; Move 1 AP + Attack 1 AP leaves 1 AP; Block Reaction 1 AP in the Monster Phase leaves 0; unspent AP removed at End of Round.",
        caption="Left: the activation procedure. Right: a Hero's 3 AP across one round, assuming a shield: Move (1 AP) and Attack (1 AP) leave 1 AP, which a Block Reaction (1 AP) uses in the Monster Phase; otherwise it is removed at End of Round (see 3.3).",
        insert_after="B01071", scope="full", schematic=False,
        semantic_check="Eligibility bullets and 5 steps compared with 3.3 and 3.3.1; 3 - 1 - 1 - 1 = 0 AP; Move and Attack 1 AP (4.2 table); Block 1 AP and shield requirement (5.5.1); Reactions do not begin or end an activation (4.5); unspent AP removed at End of Round (3.5, 3.3.2)."),
    "FIG-03": dict(
        title="Attack sequence, Mitigation Order and damage/defence examples",
        purpose="Show the five attack steps (with Total Miss branch) and apply the Mitigation Order to the source's own damage examples.",
        source_refs=["5.1.1 Mitigation Order and example (1486-1501)", "5.2 The Attack Sequence (1511-1522)", "5.3 Critical Hits and Total Miss (1523-1546)", "5.4.3 Damage Types, AV example (1573-1610)"],
        geometry_spec="Panel A: 5 numbered step boxes with flow arrows + Total Miss note. Panel B: Mitigation Order list; table 6 slashing + 4 fire, 5 AV -> 1 + 4 = 5 (source 5.1.1 example, numbers unchanged); table 9 slashing, d6 = 3 -> 6, with Block +2 AV -> 5 AV -> 4 (source 5.4.3 example).",
        caption="The five-step attack sequence and the Mitigation Order. Source example: 6 slashing and 4 fire damage against 5 AV is (6 − 5) + 4 = 5 damage; with d6 AD rolling 3, 9 slashing is 9 − 3 = 6, or 9 − (3 + 2) = 4 with a +2 AV Block (see 5.2).",
        insert_after="B01515", scope="full", schematic=False,
        semantic_check="Steps compared with 5.2 list (1515-1520); Total Miss with 5.3; mitigation order with 5.1.1; arithmetic: 6-5=1, 1+4=5; 9-3=6, 3+2=5, 9-5=4 matches 5.4.3 statement 'their total would have been 5 AV'."),
    "FIG-04": dict(
        title="Measurement, footprints and declared movement",
        purpose="Contrast Tabletop closest-point measurement with Grid orthogonal/diagonal counting, show footprints by Sz, and show the declared-movement and Declared State procedure.",
        source_refs=["2.6 Measurement, Size, Distances, and Rounding (588-609)", "Size and Footprints table (610-628)", "2.6.1 Declared Movement and Positional State (629-647)"],
        geometry_spec="Panel A schematic closest-point distance between a 1x1 and 2x2 footprint (no numeric distance). Panel B 7x4 grid, 22 pt squares: source (1,3) to target (4,1), path 2 diagonals + 1 orthogonal = 1.5 + 1.5 + 1 = 4 inches, source square not counted. Panel C footprints S 1x1, M 1x1, L 2x2, H 3x3 at 16 pt per inch. Panel D four-step flow Declare, Verify, Move, Declared State.",
        caption="Tabletop Mode measures between closest points; Grid Mode counts orthogonal squares as 1\" and diagonal squares as 1.5\", so this range is 1.5 + 1.5 + 1 = 4\" without the source square. Footprints follow Sz, and movement is declared and verified before it is resolved (see 2.6).",
        insert_after="B00598", scope="full", schematic=True,
        semantic_check="Closest points (594), orthogonal 1\" / diagonal 1.5\" and 'without counting the source square' (598), footprints table, Declared State sequence compared with lines 634-650. dx=3, dy=2: k diagonals cost 5 - 0.5k, minimum 4 at k=2. Panel A and C marked schematic; no unstated inch values drawn.",
        ambiguity="None in the drawn content. Source does not give a Tabletop distance example, so none is shown."),
    "FIG-05": dict(
        title="Grid movement costs, difficult terrain and multi-square footprints",
        purpose="Show the source's Speed 5\" Grid movement example, step costs on open and Difficult Terrain, the highest-cost rule for multi-square footprints and the diagonal-corner restriction.",
        source_refs=["2.6 Grid Mode (598-600)", "2.9.3 Difficult Terrain (893-896)", "4.4.3 Grid Mode Movement and example (1320-1331)", "4.4.7 Terrain and Movement (1376-1383)"],
        geometry_spec="Panel A 7x5 grid, 20 pt squares: orthogonal (1) then 2 diagonals (1.5 each) = 4, one more orthogonal = 5, forbidden diagonal from the 4\" cell would be 4 + 1.5 = 5.5. Panel B two 3x3 grids: open 1 / 1.5, Difficult 2 / 3. Panel C Large 2x2 footprint stepping east onto a Difficult square: cost 2. Panel D two 2x2 grids: both orthogonals Blocking = not allowed; one Blocking = allowed.",
        caption="Source example: a Speed 5\" Move of 1 + 1.5 + 1.5 = 4\" leaves 1\", enough for one orthogonal square but not for another 1.5\" diagonal. Difficult Terrain costs 2\" orthogonal and 3\" diagonal, a multi-square footprint pays the highest cost among its squares, and a diagonal step needs an open orthogonal route (see 4.4.3).",
        insert_after="B01330", scope="full", schematic=False,
        semantic_check="1 + 1.5 + 1.5 = 4; 5 - 4 = 1; 4 + 1.5 = 5.5 > 5 (a diagonal from the 4\" cell is illegal; the figure labels that cell 5.5, matching the arrow that leaves the 4\" cell). Difficult 2/3 from 2.9.3; highest cost per step from 4.4.3 para 4; corner rule from 4.4.3 para 3. Panel C: the first step east occupies a Difficult square, cost 2\".",
        ambiguity="Panel C shows only the first orthogonal step of a Large footprint onto a single Difficult square (cost 2\"), the uncontested reading; how later steps count squares already occupied is not drawn."),
    "FIG-06": dict(
        title="Engagement, Reach and Reflex Attack",
        purpose="Show Grid melee and Reach square bands, what Engages, and the difference between Move and Shift when leaving an enemy's melee distance.",
        source_refs=["5.1 Combat Basics (1454-1485)", "4.4.4 Shift (1332-1343)", "5.5.4 Reflex Attack (1677-1688)", "2.6.1 trigger point (629-647)"],
        geometry_spec="Panel A 5x5 grid, 22 pt squares: 8 adjacent squares, 16 second-ring Reach squares; Party B in an adjacent square (Engaged), Monster in the Reach band (not Engaged). Panel B two 5x3 grids: Party B's adjacent squares shaded; Move 2 squares east leaves the band (Reflex Attack at the trigger point), Shift 1 square east leaves it (no Reflex Attack).",
        caption="In Grid Mode a melee attack targets the 8 surrounding squares and Reach extends to 2 squares; only adjacency Engages. Leaving an enemy's melee distance with Move allows a Reflex Attack at the trigger point, while Shift does not (see 5.1).",
        insert_after="B01466", scope="full", schematic=False,
        semantic_check="Adjacent = immediately surrounding squares incl. diagonals, Reach = within 2 squares (1460-1462); 'Reach does not change Engagement' (1466); Move triggers, Shift/forced movement do not, Reflex Attack costs 1 AP, Disadvantage, resolves at trigger point (5.5.4, 2.6.1).",
        ambiguity="The exact position of the Grid 'trigger point' between squares is not defined; the figure marks the last square inside the melee band."),
    "FIG-07": dict(
        title="Line of sight, Cover and Blocking Terrain",
        purpose="Show six Grid Mode sight-line cases separating what blocks LOS from what only grants Cover.",
        source_refs=["2.7.1 The Sight Line (664-681)", "2.7.2 Blocked Line of Sight (682-697)", "2.8.4 Cover incl. Ranger/Fighter example (789-813)", "2.9.1 Terrain Types (832-879)"],
        geometry_spec="Six 8x4 grids, 20 pt squares, centre-to-centre sight lines: (A) Blocking column on the line; (B) Blocking squares (3,1),(4,2) sharing corner (4,2) on the line from (2,3) to (5,0); (C) Cover Terrain column crossed; (D) Cover squares (3,2),(3,3), line from (2,1) to (5,2) touches only corner (4,2); (E) ally in line (Fighter) then Shift to (1,1): line (1,1)-(7,2) clears the Fighter square; (F) generic Impassable column crossed; its label states Cover unless the terrain entry says otherwise (chasms and pits provide none), per editorial patch P-02.",
        caption="Blocking Terrain, a corner shared by two Blocking squares and the interior of Cover Terrain block LOS. Touching only a Cover Terrain corner, an intervening combatant and Impassable Terrain leave LOS clear and give the target Cover (Impassable Terrain unless its terrain entry says otherwise); a Shift of 1 AP clear of the line removes the combatant's Cover (see 2.7.2 and 2.8.4).",
        insert_after="B00810", scope="full", schematic=False,
        semantic_check="Panel texts compared with 2.7.2 (Grid: corner of 2 Blocking squares; interior of Cover square neither occupies; edge or corner touch does not pass through but grants Cover), 2.8.4 (non-Open feature edge/corner; intervening combatant not Prone/Knocked Out, same or larger Sz; Cover binary), 2.9.1 as patched by P-02 (Impassable provides Cover unless its terrain entry says otherwise, does not block LOS; defaults row: chasms and pits provide no Cover). Panel F is a generic Impassable feature and its label carries the P-02 qualifier; no chasm or pit is drawn with Cover. Geometry checked numerically: line (2.5,3.5)-(5.5,0.5) passes the shared corner (4,2); line (2.5,1.5)-(5.5,2.5) reaches y=2 only at x=4 (corner); line (1.5,1.5)-(7.5,2.5) stays above y=2 over the Fighter square.",
        ambiguity="Panel E's intervening combatant is assumed to be the same Sz as the target (the Ranger example in 2.8.4 does not state Sz)."),
    "FIG-08": dict(
        title="Areas of Effect",
        purpose="Show Cone, Line and Aura templates, the Grid Mode affected-square rules, Blocking Terrain stopping an area, and the shared-damage order.",
        source_refs=["2.7.3 Areas of Effect (698-747)"],
        geometry_spec="Panel A schematic templates with variable X; text states that a Cone or Line does not affect the combatant it originates from (P-01). Panel B Aura 2\" on a 7x7 grid: squares with centre within 2 of the source centre, ties included = 13 squares including the source square (an Aura includes its source square). Panel C Cone 3\" on a 6x5 grid: apex at the origin square centre, far edge 3 along the centreline and 3 wide; squares with centre inside, ties outward = 7 squares beyond the origin; the origin square is left unshaded (it is not counted) and the panel text says the combatant the cone originates from is not affected. Panel D same cone with one Blocking square at (2,3): square (3,3) is covered by the cone but its sight line from the origin crosses the Blocking square. Panel E four-step shared-damage flow.",
        caption="A Grid Mode Aura 2\" affects 13 squares (including the source square); a 3\" Cone affects 7 squares beyond its origin square, and never affects the combatant it originates from. A square whose sight line from the origin is blocked by Blocking Terrain is unaffected even if the template covers it, and shared area damage is rolled once (see 2.7.3).",
        insert_after="B00741", scope="full", schematic=True,
        semantic_check="Aura rule 'every square whose centre lies within the listed straight-line distance ... rounded outward at ties' and 'Include every source square' -> offsets with dx^2+dy^2<=4: 1+4+4+4=13. Cone rule 'every square whose centre lies within the cone' -> |dy|<=dx/2: x=1:1, x=2:3, x=3:3 = 7 squares beyond the origin; origin square not counted in the 7; per 2.7.3 as patched by P-01 the combatant a cone or line originates from is not affected (the patch concerns the combatant, not the square); make_figures.selfcheck asserts the origin square is not among the counted cone squares. Blocking: sight line origin-to-square-centre tested with a corner/interior check in code. Four-step order compared with the list at 741-745.",
        ambiguity="Resolved by P-01: the Cone panel, its text and the caption agree that the combatant the cone originates from is not affected; the origin square is simply not among the 7 counted squares. Not drawn: a Grid Line (the source text includes the origin square of a Line only 'if its centre lies within the line unless the rule says otherwise'; the figure draws no Grid Line and states only the P-01 sentence for templates in panel A)."),
    "FIG-09": dict(
        title="Forced movement, Collision and the ledge example",
        purpose="Show Push, Pull and Slide, a Collision with terrain or a combatant, and the source's ledge example.",
        source_refs=["4.4.6 Forced Movement and ledge example (1350-1375)", "4.4.7 (1376-1383)", "5.6.1 Push (1701-1708)"],
        geometry_spec="Panel A three 7x1 strips with dotted arrows away from, toward, and along a named direction. Panel B Impassable square and another combatant stopping the arrow early. Panel C 7x3 grid, 22 pt squares: Skeleton starts 2\" before an edge (dimension 2\"), Push 3\" shown by a dimension, forced movement ends at the edge point beyond which the surface is missing (Impassable pattern).",
        caption="Forced movement follows a line and stops at the last legal position; a Collision deals no damage by itself. Source example: a 3\" Push toward a ledge 2\" away moves the Skeleton 2\" to the edge point, then Falling is resolved from that point (see 4.4.6).",
        insert_after="B01374", scope="full", schematic=False,
        semantic_check="Ledge numbers 3\" / 2\" taken from the example (line 1374); 'not a Collision' and Falling after movement ends compared with 4.4.6; Collision definition and 'no damage by itself' compared with 4.4.6; forced movement never triggers Reflex Attack.",
        ambiguity="The source says the target moves 'to the edge point'; the drawn marker centre sits on the edge line without claiming how the footprint straddles it. Fall height is not stated, so no HP loss is shown."),
    "FIG-10": dict(
        title="Monster Group states and wake-up triggers",
        purpose="Show Resting/Awake transitions with the five wake-up triggers and how 6\" movement, 12\" LOS and blocked LOS differ.",
        source_refs=["9.3 Monster Placement and Initial State (7551-7572)", "9.4 Monster Waking and Activation State (7573-7590)", "Hide distance 2\" (1868)"],
        geometry_spec="Panel A: Resting -> Awake one-way arrow, five numbered triggers, Hide note. Panel B concentric rings at 6\" (solid) and 12\" (dashed), ratio 1:2, schematic: (1) enemy moves inside 6\" with a Blocking wall between: wakes; (2) enemy inside 12\" with open LOS: wakes; third enemy outside 6\" with blocked LOS: no trigger.",
        caption="A Monster Group begins Resting and becomes Awake for the rest of the adventure when a trigger occurs: an enemy moving within 6\" (no LOS needed), a visible enemy entering LOS within 12\", damage, a loud event within 6\", or a scenario rule (see 9.4).",
        insert_after="B07590", scope="full", schematic=True,
        semantic_check="Trigger list compared with 9.4 bullets; '6\" movement trigger does not require LOS' and 'Hidden trips only within Hide distance' (7588); Awake permanence (7590); setup defaults 3\" / Guard Point (9.3). Rings drawn at 6:12 ratio only; panel labelled schematic.",
        ambiguity="None; stat-block or scenario overrides are noted in the figure heading."),
    "FIG-11": dict(
        title="Standard Monster AI Script",
        purpose="Show the five-instruction decision procedure: first valid instruction executes and the activation ends.",
        source_refs=["9.5 C Standard Monster AI Script (7626-7637)", "9.5 D AI Step Abilities (7638-7641)", "3.4.3 Monster Activations (1113-1120)"],
        geometry_spec="Five condition boxes with yes arrows to outcome boxes and no arrows downward: AI Step, Engaged, Visible Target, Search, No Visible Target; preface states Primary Target and 'first valid instruction'.",
        caption="The Standard Monster AI Script: a Monster executes the first valid instruction and its activation then ends. Each instruction is tried only if the one above it does not apply (see 9.5 C).",
        insert_after="B07636", scope="full", schematic=False,
        semantic_check="Wording of each instruction compared with lines 7630-7635 and 7636 (activation ends unless a rule says otherwise); d6 N+ rule from 9.5 D; lowest current HP and tie order from step 2; Search DEX Check by the enemy's controller; Movement Priorities referenced for step 5.",
        ambiguity="None."),
    "FIG-12": dict(
        title="Primary Target, tie-breakers and Blocked Route",
        purpose="Show target selection by nearest visible enemy, the three tie-breakers, and the Blocked Route retargeting rule.",
        source_refs=["9.5 A Core AI Rules (7605-7614)", "9.5 E Target Priorities and Tie-Breakers (7642-7651)", "9.5 F Movement Priorities and Blocked Route (7652-7669)"],
        geometry_spec="Panel A: Hidden enemy nearest but not visible; Primary Target is the nearest visible enemy. Panel B: two enemies at equal distance, example HP 4 and 7, ladder Lowest Current HP, Most Recent Attacker, Random Determination. Panel C 8x5 grid: nearest visible enemy ringed by Impassable Terrain (LOS not blocked, no route), other visible enemy reachable, becomes the new Primary Target.",
        caption="Primary Target is the nearest visible enemy; equal candidates are separated by lowest current HP, then Most Recent Attacker, then Random Determination. If the Primary Target cannot be reached, the nearest reachable visible enemy becomes the new Primary Target (see 9.5 E and 9.5 F).",
        insert_after="B07662", scope="full", schematic=True,
        semantic_check="Primary Target and Hidden/Invisible exclusion (7644, 7624); tie hierarchy 1-3 (7646-7649); Blocked Route text (7662); Impassable Terrain does not block LOS (2.9.1). HP values 4 and 7 are labelled examples.",
        ambiguity="Panel C assumes a melee Monster whose Speed lets it reach the second enemy this activation (the rule's condition); a Monster with a ranged attack could attack the ringed enemy from a legal firing position and Blocked Route would not apply."),
    "FIG-13": dict(
        title="Party deployment configurations I",
        purpose="One validated diagram for each general deployment pattern used by the Core Scenarios: fixed long/short edges, roll-off choice of edge or corner, and corner zones.",
        source_refs=["10.1 Adventure Preparation Sequence, Setup Roll-off, Battlefield Edges (11029-11075)", "10.4 Party Deployment lines (36 scenarios; see 'coverage')"],
        geometry_spec="Five 36\"x36\" boards at 4 pt per inch (to scale): A bands 6\" wide on both long edges; B bands 6\" on both short edges; C winner's edge (callout 1) and opposite edge (callout 2), 6\"; D 8\"x8\" corner (callout 1) and diagonally opposite 8\"x8\" corner (callout 2); E opposite 8\"x8\" corner zones. Hero markers enlarged. Panel captions and the key cite the 10.1 step 11 default (P-03) for depth 6\" and corner zones 8\"x8\" only where the scenario is silent (panel D notes that Greenmark 2 states its own 8\"x8\"), the edge/corner choice by the Setup Roll-off winner with the opposite zone for the other party, and alternate placing starting with the Roll-off loser; the former 'distance not stated' marks are removed. Unified iconography 2026-10-07: every symbol is drawn by the shared glyph functions of scenkit.py (zones with edge bands, Hero discs, markers, terrain patterns, dimension lines with end ticks, rings, step circles), explained by the key FIG-20; a compact key strip on the figure lists the glyphs it uses.",
        caption="Deployment patterns used by the Core Scenarios, drawn on a 36\"×36\" battlefield: opposite long or short edges within 6\", a Setup Roll-off winner's choice of edge or 8\"×8\" corner, and opposite corner zones with alternating placement. Where a scenario is silent, the 10.1 step 11 default supplies the 6\" depth, the 8\"×8\" corner size and the placing order; key: FIG-20 (see 10.1 and each scenario's Party Deployment).",
        insert_after="B11062", scope="full", schematic=False,
        coverage=DEP_MAP,
        semantic_check="All 36 Party Deployment lines (grep 'Party Deployment:') classified; distances 6\" and 8\" and 'long = East/West, short = North/South' (10.1) compared with the source; geometry drawn from stated values and from the 10.1 step 11 default as patched by P-03 (Roll-off winner chooses the edge or corner zone and the other party takes the opposite one; zones 6\" from the edge; corner zone 8\"x8\"; alternate placing starting with the Roll-off loser). Sun-Drowned 2, The Mire 5 and The Mire 6 (depth), Sun-Drowned 3 and The Mire 3 (corner size and order) and Pale City 1 (alternation) now rest on that default and are labelled so in the coverage list. Redrawn with the shared zone glyph (edge bands show the edge a zone is measured from: Party A solid band, Party B open band); distances 6\" and 8\" unchanged.",
        ambiguity="Resolved by P-03: depth (Sun-Drowned 2, The Mire 5, The Mire 6), corner-zone size and placing order (Sun-Drowned 3, The Mire 3, Pale City 1) and the edge pair for scenarios that name only 'opposite battlefield edges' (Pale City 5, Sun-Drowned 4 and 5, The Mire 2) come from the 10.1 step 11 default; the figure draws the generic patterns and does not pick long or short edges for the last group (panels A, B and C each apply)."),
    "FIG-14": dict(
        title="Party deployment configurations II",
        purpose="Deployment patterns with extra spatial conditions: Trail, shared short edge, central Safe Zone, and short edges across a Ravine.",
        source_refs=["10.4 The Bandit's Toll (12132-12170)", "10.4 The Chasm Crossing (12965-12997)", "10.4 The Quake (13035-13062)", "10.4 The Spider's Silk Route (12209-12238)"],
        geometry_spec="Four 36\"x36\" boards at 3.3 pt per inch (panel C is a 6.6 pt per inch detail of the centre): A 6\" bands, Trail 3.5\" wide (source 3-4\") full length, 2 Heroes per side on the Trail; B one 8\"-deep band on a short edge, Chasm 8\" wide; separation drawn as a dashed arc 6\" from the Party A Hero's marker edge plus a dimension line (arrowheads and end ticks) from that marker edge to the nearest Party B marker edge, 7\" (above the 6\" limit), with a 6\" radial dimension to the arc; C 8\"x8\" Safe Zone at 6.6 pt per inch with Hero markers at true 1\" size (r = 0.5\"): dashed ring 3\" from the Party A footprint edge, a 3\" radial dimension, and a dimension line from the Party A footprint edge to the nearest Party B footprint edge, 4\" (above the 3\" limit); all markers inside the zone; D 6\" bands and a 7\" Ravine (source 6-8\") between them. Unified iconography 2026-10-07: every symbol is drawn by the shared glyph functions of scenkit.py (zones with edge bands, Hero discs, markers, terrain patterns, dimension lines with end ticks, rings, step circles), explained by the key FIG-20; a compact key strip on the figure lists the glyphs it uses.",
        caption="Special deployments: a Trail with at least two Heroes on it, one shared short edge within 8\" (no Hero within 6\" of an opposing Hero), a central 8\"×8\" Safe Zone (no Hero within 3\" of an opposing Hero), and short edges either side of a Ravine; key: FIG-20 (see 10.4).",
        insert_after="B11062", scope="full", schematic=False,
        coverage={k: v for k, v in DEP_MAP.items() if k.startswith("FIG-14")},
        semantic_check="Trail, 8\", 6\", 3\" and Safe Zone texts compared with the four Party Deployment paragraphs (12170, 12997, 13062, 12238) and terrain paragraphs (12132, 12965, 13035, 12209). Correction pass: 13062 ('cannot be placed within 3\" of an opposing Hero', central 8\"x8\" Safe Zone) and 12997 ('within 6\"'; within 8\" of the edge) checked against the redrawn panels C and B; distances measured between the closest points of footprints per 2.6 (594). make_figures.selfcheck asserts that each separation dimension spans exactly the closest edges of the nearest opposing Heroes, that the gaps (B 7\", C 4\") exceed the limits (6\", 3\"), that every A-B pair in panel C is more than 3\" apart edge to edge, and that panel C markers lie inside the 8\"x8\" zone. Zone-depth dimensions (6\", 8\") span zone edge to zone edge. Redrawn with the shared dimension glyph (line with end ticks): the separation dimensions still span exactly the closest edges (2.6) and the selfcheck assertions on GEOM14 are unchanged; the Chasm now uses the shared Chasm pattern (a drop, not Impassable Terrain) and the Ravine the Difficult pattern used on FIG-24.",
        ambiguity="Source ranges (Trail 3-4\", Ravine 6-8\") are drawn at 3.5\" and 7\"; lateral Trail position and Ravine/Chasm position along the board are not fixed by the source and are drawn centred. The Chasm Crossing 'start' short edge is not specified (top drawn). The source states the limits as 'within 6\"' and 'within 3\"'; the redrawn Heroes are placed clearly outside the limits (7\" and 4\" between closest edges) so that no reading of the exact-limit case (exactly 6\" or 3\") is drawn. Panel B markers are enlarged and the dimension is measured between drawn marker edges at 3.3 pt per inch; the true 1\" footprints would be farther apart."),
    "FIG-15": dict(
        title="The Chasm Crossing: ledges and objective placement",
        purpose="Show where the Survey Map, ledges, Chasm and Cartographer's Stone sit relative to the shared deployment edge, and how Jump applies to ledge gaps.",
        source_refs=["10.4 Undermarches Scenario 2: The Chasm Crossing (12945-13014), including Jumping the Gaps (13003) and Chasm Fall with the Fly/Climb provisions (13005-13007)", "4.4.9 Jump (1394-1405)"],
        geometry_spec="36\"x36\" at 5.4 pt per inch: 8\" deployment band on the start edge; Chasm 8\" wide, its near edge 14\" from the start edge; Survey Map 3\" before the first ledge, Cartographer's Stone 3\" after the last ledge; four ledges (schematic proportions), one drawn Crumbling. Correction pass: board redrawn at 4.3 pt per inch; panel C (full width, steps 6-8) reproduces the Chasm Fall paragraph and the two Fly/Climb provisions (Hero or Hireling; Monster) of 13005-13007 in the source's wording. Unified iconography 2026-10-07: every symbol is drawn by the shared glyph functions of scenkit.py (zones with edge bands, Hero discs, markers, terrain patterns, dimension lines with end ticks, rings, step circles), explained by the key FIG-20; a compact key strip on the figure lists the glyphs it uses.",
        caption="In The Chasm Crossing the Survey Map starts 3\" from the first ledge and must be placed adjacent to the Cartographer's Stone 3\" beyond the last ledge. Gaps of 1–2\" between ledges are crossed by Jump, and a failed Jump into the Chasm causes a Chasm Fall, with stated exceptions for Fly or Climb Speeds; key: FIG-20 (see 10.4).",
        insert_after="B12997", scope="full", schematic=True,
        semantic_check="3\" map and stone distances, 8\" Chasm, 1\" wide ledges, 1-2\" gaps requiring Jump, 1-2 Crumbling ledges and Speed -1\" from 12965-12969; Jump cost 2\" per 1\" and DEX Check from 4.4.9; failed Jump into the Chasm = Chasm Fall, removed from play, Hero Defeated with a normal Injuries Roll, carried items including the Survey Map lost, replacing normal Falling (13003-13005); victory = Hero places the Survey Map adjacent to the Stone (13011). Correction pass, 13005-13007 compared sentence by sentence with panel C steps 6-8: Pushed off a Ledge or failed Crumbling Ledge Check -> immediately removed from play; Hero Defeated and normal Injuries Roll; non-Hero resolved as though reduced to 0 HP; replaces normal Falling; carried items including the Survey Map lost. Hero or Hireling with Fly or Climb Speed: may immediately spend 1 unspent AP, including AP reserved for Reactions; placed Prone in the nearest legal space on a Ledge; current movement ends; if the AP cannot be spent, Chasm Fall resolves normally. Monster with Fly or Climb Speed: placed Prone in the nearest legal space on a Ledge, activation ends (no AP cost stated). Redrawn with the shared glyphs: Chasm pattern, Ledge and Crumbling Ledge (crack line) glyphs, step circles, 3\" dimension lines with end ticks; all numbers and rules text unchanged.",
        ambiguity="The source gives 3-4 ledges, 1-2\" gaps, and does not give ledge length or the board position of the Chasm or ledge path; these are schematic. Treasure Chest positions (alcoves on both sides) and wall markers are not drawn. Generic 4.4.9 failure (last legal point before the gap, Prone, movement ends) versus the scenario's Chasm Fall: the scenario text says to use the normal Jump rules but a failed Jump into the Chasm causes a Chasm Fall, which replaces normal Falling; the figure states the scenario rule only and does not draw the generic failure result. Crumbling Ledge DEX Check failure also causes a Chasm Fall (13005)."),
    "FIG-16": dict(
        title="Whispering Grove: PvPvE interaction",
        purpose="Show how one neutral Monster responds to two competing parties through its printed Target Priority.",
        source_refs=["10.4 Greenmark Scenario 2: The Whispering Grove (12042-12111)", "9.5 E (7642-7651)"],
        geometry_spec="Detail of the Central Clearing at 10 pt per inch: clearing drawn 13.5\" across (source about 12-15\"), three Standing Stones in a rough triangle 7\" apart (source 6-8\"), Party A Hero at the first Stone Interacted with, Party B Hero at another; Antlered Warden (Large, 2\" square) placed adjacent to the Party A Hero's Stone (P-04); Random Monster Group 2 marker inside the clearing 2.75\" from its centre, i.e. 4\" from the clearing edge, with a 4\" radial dimension (P-05; selfcheck-style assertion in the drawing code); dashed targeting line from Warden to the Party B Hero. Positions schematic. Unified iconography 2026-10-07: every symbol is drawn by the shared glyph functions of scenkit.py (zones with edge bands, Hero discs, markers, terrain patterns, dimension lines with end ticks, rings, step circles), explained by the key FIG-20; a compact key strip on the figure lists the glyphs it uses.",
        caption="In the Whispering Grove the Antlered Warden is placed adjacent to the first Standing Stone a Hero Interacts with, and its Target Priority is the valid Hero who most recently activated or attempted to activate a Stone, whichever party that Hero belongs to. Entangling Roots then applies if the target is within 8\"; key: FIG-20 (see 10.4).",
        insert_after="B12100", scope="full", schematic=True,
        semantic_check="Interact [2 AP] + SPI Check, one claimant per stone (12100); Warden placement as patched by P-04 (when a Hero first Interacts with a Standing Stone, adjacent to that Stone; Awake when placed), Target Priority wording and Entangling Roots (8\", DEX Check, Immobilized, end activation) from 12042-12094; Group 2 as patched by P-05 (inside the Central Clearing, 4\" from its edge, Resting); normal priorities as fallback (9.5 E). Redrawn with the shared glyphs: Standing Stones as objective diamonds, Antlered Warden as a Large Monster square at footprint scale (10 pt per inch, 2\" = 20 pt), Group 2 as a Monster hexagon, Central Clearing as an open feature, targeting line glyph; all numbers unchanged (6-8\", 12-15\", 4\", 8\" in step 5).",
        ambiguity="Resolved by P-04 and P-05: the Warden stands adjacent to the first Stone a Hero Interacts with (the drawn Party A Hero's Stone, an illustrative choice of which Stone is first) and Group 2 stands inside the Central Clearing 4\" from its edge. Remaining schematic choices: the 4\" is drawn from the marker centre to the clearing edge, and Group 2's direction around the clearing is not fixed by the source. Groups 1 and 3 are not drawn."),
    "FIG-17": dict(
        title="Campaign cycle and Town Phase",
        purpose="Give a concise campaign/downtime sequence: four phases, Aftermath steps, Town checklist and locations.",
        source_refs=["11.2 The Campaign Cycle (15189-15199)", "11.2.1 Expedition (15200-15216)", "11.2.3 Aftermath Steps 1-3 (15221-15252)", "11.2.4 Town Phase checklist and locations (15405-15480)"],
        geometry_spec="Four phase boxes with loop arrow; checklist of the 6 Town Phase steps; six Town locations with their one-line purposes.",
        caption="Each adventure runs Expedition, Skirmish, Aftermath, then Town; Aftermath and Town follow every adventure, win or lose, unless a rule says otherwise. The Town Phase grants 4 TAP, or the Journey-modified amount, to spend at six locations (see 11.2).",
        insert_after="B15198", scope="full", schematic=False,
        semantic_check="Phase order and 'after every adventure, whether the party wins or loses' (15189-15198); 1d10 Expedition Event, Aftermath Steps 1-3 and 1d20 Journey Table, 4 TAP and checklist (15405-15420); location summaries compared with the opening sentence of each location subsection.",
        ambiguity="None."),
    "FIG-18": dict(
        title="Learn to Play: setup and first-round opening",
        purpose="Show the Appendix A starting positions and the sample Round 1 using only Appendix A rules and the A.11 fixed rolls.",
        source_refs=["A.1-A.4 setup, Quickstart Scenario (16082-16208)", "A.7-A.9 activations, Reactions, Dire Wolf AI (16254-16339)", "A.11 Sample Opening, Round 1 (16348-16490)"],
        geometry_spec='Left: the 24"x24" battlefield drawn by the shared map renderer (scenario_specs.json, section appendix, 7.5 pt per inch) with the shared glyphs: 4" deployment zones on the two short edges (Party A south, Party B north, A.11); 3"x3" centre ruin, Blocking, centred (A.2); low wall about 2"x3" (Impassable) and rubble about 3"x3" (Cover tagged Difficult), each 4-6" from the centre on opposite flanks, and two Cover scatter pieces, all grey dashed because their positions are open; Dispatch Satchel adjacent to the ruin and 4 Dire Wolves within 2" of it, grey dashed because the side of the ruin is not stated (one legal arrangement); Treasure Chest 5" east of the centre with a 5" dimension; Edric (12",20"), Mara (18",20"), Varek (12",4"), Senna (18",4") from the A.11 table with 6" dimensions; exit arrows on all four edges. An inset at 10 pt per inch shows the A.11 relative layout (Wolves 1-4 2" south, east, west and north of the Satchel). Right: Round 1 table with AP squares. A compact key strip at the bottom lists exactly the glyphs used; the full key is FIG-20.',
        caption="Appendix A starting positions, with the Dispatch Satchel adjacent to the centre ruin, and Round 1 of the sample game. Edric ends the round with 16 − 5 = 11, 11 − 3 = 8 and 8 − 3 = 5 HP after Varek's attack and two Dire Wolf bites; key: FIG-20 (see A.11).",
        insert_after="B16371", scope="full", schematic=True,
        semantic_check='Hero and Chest positions from the A.11 table (16358-16367); terrain from A.2 (16108-16111) as stated in the figure and asserted in scenario_specs.json (Satchel within 1" of the ruin per the 2.1 adjacency definition at line 465, wolves within 2" of the Satchel, low wall and rubble 4-6" from the centre); Satchel adjacent to the centre ruin as patched by P-07; Wolves 2" N/S/E/W of the Satchel (A.11); every printed inch value is found in its cited lines (check_scenmaps); initiative 13+0+1=14 vs 10+0+0=10; Varek 6+3=9, AD 4, 9-4=5; Mara 4+3=7, AV 1, 6; Dodge 11+3=14 >= 12; Wolf 1 5+1=6, AD 3 -> 3, STR 9+3=12 success; Wolf 2 max(4,7)+1=8, AD 5 -> 3, STR 6+3=9 fail. Only actions and Reactions named in A.7-A.8 are used (Move, Attack, Interact, Dodge, Pack Tactics); no advanced rules appear in the figure or its key strip.',
        ambiguity='Resolved by P-07: the Satchel is adjacent to the centre ruin. Remaining: the side of the ruin where the Satchel stands, and therefore where the Wolves stand, is not stated, so the board shows one legal arrangement in grey dashes (the Wolves within 2" of it as A.4 says) and the inset shows the A.11 relative layout; the flank of the low wall and of the rubble is likewise open; the third scatter piece permitted by A.2 is not drawn.'),
    "FIG-19": dict(
        title="Basic Mode: The Courier's Strongbox setup and an example score",
        purpose="Show the Appendix B setup constraints (zones, Monster Entry band, terrain types) and one source-supported carrying and scoring example.",
        source_refs=["B.1 Basic Mode At a Glance (16519-16532)", "B.5 Monster profiles (17016-17070)", "B.6 Basic Scenario: The Courier's Strongbox (17072-17095)", "B.4 Ironscar SPD 4\" (16584-16590)"],
        geometry_spec='Left: the 24"x24" battlefield drawn by the shared map renderer (scenario_specs.json, section appendix, 7.5 pt per inch): 4" zones on opposite edges (north and south drawn grey dashed, because the source does not say which edges), road band across the centre (width not stated, grey dashed), Strongbox at the centre, three Monster Entry markers 6" from the centre (inside the 5-7" ring pair, more than 4" apart, outside both zones) each with one Monster group and one Satchel drawn beside it, two 3"x3" pieces within 4" of the centre (Blocking ruin, Impassable cart or low wall) and four 3"x3" Cover pieces one per quarter, all grey dashed; exit arrows through the own deployment edges. Right: placement rules and the example 4" - 2" = 2"; 12" / 2" = 6 Moves; 12 + 4 + 2 + 3 = 21c. A compact key strip at the bottom lists exactly the glyphs used; the full key is FIG-20.',
        caption="Basic Mode setup for The Courier's Strongbox on a 24\"×24\" battlefield, with one complete Monster group per Entry marker, assigned at random. Assumed example: carrying the Strongbox cuts Ironscar's SPD 4\" by 2\" to 2\" per Move; extracting it with 1 Satchel, having defeated 2 Goblins and 1 Bandit, scores 12 + 4 + 2 + 3 = 21c; key: FIG-20 (see B.6).",
        insert_after="B17082", scope="full", schematic=True,
        semantic_check="Terrain counts, 3\"x3\" size, 4\" deployment, Entry markers (5-7\", >= 4\" apart, outside zones, one complete group each assigned at random per P-06, Resting), Strongbox 12c, Satchels 4c, -2\" Speed to a minimum of 1\", extraction through own edge (17074-17094); step 3 text reads \"assigned to the markers at random, one complete group per marker\"; Goblin 1c, Skeleton Warrior 1c, Bandit 3c (B.5); Ironscar SPD 4\" (B.4). Only B-appendix terms used; no Hide, Powers or advanced rules.",
        ambiguity="Resolved by P-06: groups are assigned to Monster Entry markers at random, one complete group per marker (all markers carry identical group glyphs, so no assignment is drawn). The Monster group and Satchel are drawn beside, not on, each Entry marker for legibility. Terrain positions, the road's width, who places the markers and which opposite edges are the deployment edges are not specified (north and south drawn, grey dashed)."),
}

AUDIT = {
    "FIG-02": ("Minor 1 fixed: Monster Phase row now reads 'A Monster's slashing attack would damage the Hero' so Block's blunt/piercing/slashing trigger is visible.", "revised after audit: minor fixed"),
    "FIG-05": ("MAJOR fixed: the forbidden-diagonal cell label changed from 6.5 to 5.5 (4 + 1.5) to match the arrow leaving the 4\" cell; geometry_spec and semantic_check updated; selfcheck asserts 4 + 1.5 = 5.5.", "revised after audit: major fixed"),
    "FIG-06": ("Minor fixed: adjacent and Reach bands now also carry digit labels 1 and 2 (distance in squares), so the two grays are no longer tone-only.", "revised after audit: minor fixed"),
    "FIG-07": ("Minor fixed: panel E Fighter moved to the third square so the post-Shift sight line clears the Fighter's square by at least a quarter square (1.75 vs 2.0 at the square's edge); selfcheck asserts clearance.", "revised after audit: minor fixed"),
    "FIG-08": ("Minor fixed: panel B now says 'including the source square: 13 squares'.", "revised after audit: minor fixed"),
    "FIG-12": ("Minor fixed: step badges 1 and 2 now sit beside the ringed enemy and the reachable enemy; panel C text says 'melee Monster' and the manifest ambiguity records the ranged-Monster case.", "revised after audit: minor fixed"),
    "FIG-13": ("Minor fixed: key text and manifest coverage/ambiguity mark Sun-Drowned 2, The Mire 5 and The Mire 6 as 'distance not stated' (6\" band shown only as the general pattern).", "revised after audit: minor fixed"),
    "FIG-14": ("Minor fixed: panel C frame is dashed with an on-drawing 'centre detail' tag, and the dimension is labelled 'min 3\"'.", "revised after audit: minor fixed"),
    "FIG-15": ("MAJOR fixed: step 5 now states the scenario's own rule (failed Jump into the Chasm causes a Chasm Fall: removed from play, Hero Defeated with a normal Injuries Roll, carried items including the Survey Map lost, replacing normal Falling); caption mentions Chasm Fall; the generic-versus-scenario conflict is recorded in ambiguity. Minor fixed: step 4 now says the Map is placed adjacent to the Stone.", "revised after audit: major and minor fixed"),
    "FIG-17": ("Minor fixed: 'unless a rule says otherwise' added to the Town box and loop strip; caption no longer claims the whole cycle repeats unconditionally.", "revised after audit: minor fixed"),
    "FIG-19": ("Minor fixed: Strongbox now has its own glyph (chest) distinct from the Satchel diamond; the road band is white with a dotted centre line and 'road' labels; the example now reads 'at least 6 Moves' and notes the Interact [1 AP] to pick up.", "revised after audit: minor fixed"),
}

CORRECTED = {
    "FIG-14": "Release correction pass 2026-10-06: the floating 'min 3\"' label in panel C is replaced by a dimension line with arrowheads and end ticks that runs exactly between the closest edges (2.6) of one Party A Hero and the nearest Party B Hero (4\"), plus a dashed ring marking the 3\" limit; panel C markers are now true 1\" size at the stated 6.6 pt per inch. Panel B's 6\" label, which floated between markers, is replaced the same way (6\" arc and radial dimension, 7\" edge-to-edge dimension to the nearest Party B Hero). The remaining dimensions (6\", 8\") span zone edges and were checked. Selfcheck asserts the dimension endpoints.",
    "FIG-15": "Release correction pass 2026-10-06: step 5 stated the Chasm Fall consequence but omitted the Fly/Climb provisions of 13007. New panel C (steps 6-8) states the Chasm Fall (Hero Defeated with a normal Injuries Roll; non-Hero as though reduced to 0 HP; carried items lost) and separately the Hero or Hireling Fly/Climb option (spend 1 unspent AP, including AP reserved for Reactions; Prone on the nearest legal Ledge space; movement ends; Chasm Fall if the AP cannot be spent) and the Monster Fly/Climb provision (Prone on the nearest legal Ledge space; activation ends) in the source's wording. Caption notes the exceptions. Height 328 pt.",
}

# editorial patches (editorial/patches.json) applied 2026-10-06; figures re-aligned to the patched text
PATCHED = {
    "FIG-07": "P-02: panel F label and caption state that Impassable Terrain provides Cover unless its terrain entry says otherwise (chasms and pits provide none).",
    "FIG-08": "P-01: Cone panel, panel A text and caption agree that a cone or line does not affect the combatant it originates from (stated for the combatant, not the origin square).",
    "FIG-13": "P-03: the 'distance not stated' marks are replaced by the 10.1 step 11 default (6\" zones, 8\"x8\" corners, Roll-off winner chooses, alternate placing from the Roll-off loser); key, captions and coverage updated.",
    "FIG-16": "P-04 and P-05: Warden drawn adjacent to the first Stone a Hero Interacts with; Random Monster Group 2 drawn inside the Central Clearing 4\" from its edge; 'central Stone' and 'perimeter' ambiguity text removed.",
    "FIG-18": "P-07: Satchel is adjacent to the centre ruin (no longer 'at the battlefield centre'); centre ruin drawn; Satchel and Wolves shown as a relative layout because the side is not stated.",
    "FIG-19": "P-06: step 3 now reads 'assigned to the markers at random, one complete group per marker'.",
}
PATCH_STATUS = "aligned to editorial patches 2026-10-06"

UNIFIED = {"FIG-%02d" % n for n in (13, 14, 15, 16, 18, 19)} | {"FIG-%d" % n for n in range(20, 58)}
UNIFIED_STATUS = "unified iconography 2026-10-07, pending independent review"

# RC486 (P-08 to P-12): the four formerly unplaced elements are drawn; open minor review findings fixed (labels, leaders, foot notes, layout).
RC486_REDRAWN = {"FIG-%d" % n for n in (19, 20, 22, 23, 24, 25, 26, 27, 28, 30, 31, 33, 36, 37, 38, 39, 41, 42, 43, 44, 45, 47, 48, 51, 52, 53, 55, 56)}
RC486_STATUS = "redrawn 2026-10-07 for RC486 and minor review findings, pending independent re-review"

# Scenario deployment maps (FIG-20 onward) are generated from figures/src/scenario_specs.json.
import fig_scenmaps
META.update(fig_scenmaps.meta_entries())

# Resolve placement against the current manuscript, never against inherited line numbers.
import sys
sys.path.insert(0, os.path.join(FIG_DIR, "..", "tools"))
from content_anchors import resolve
for fid, anchor in resolve().items():
    if fid in META:
        META[fid]["insert_after"] = anchor

# (id, ...) order for manifest
ORDER = sorted(META)


def write_all(dims=None):
    manifest = []
    placements = {}
    for fid in ORDER:
        m = dict(META[fid])
        entry = {"id": fid}
        entry["title"] = m.pop("title")
        entry["purpose"] = m.pop("purpose")
        entry["source_refs"] = m.pop("source_refs")
        entry["geometry_spec"] = m.pop("geometry_spec")
        entry["caption"] = m.pop("caption")
        entry["insert_after"] = m.pop("insert_after")
        entry["scope"] = m.pop("scope")
        entry["schematic"] = m.pop("schematic")
        entry["file"] = "figures/out/%s.svg" % fid
        if dims and fid in dims:
            entry["size_pt"] = {"width": dims[fid][0], "height": dims[fid][1]}
        entry["generator"] = "figures/src/make_figures.py"
        entry["semantic_check"] = m.pop("semantic_check")
        entry["status"] = "semantic review complete (author); visual inspection of rendered PNG done"
        if fid in AUDIT:
            entry["status"] = AUDIT[fid][1] + "; independent audit findings addressed; geometry/arithmetic selfcheck and render re-run"
            entry["audit_response"] = AUDIT[fid][0]
        else:
            entry["audit_response"] = "Independent audit: no findings (PASS)."
        if fid in CORRECTED:
            entry["status"] = "corrected 2026-10-06 (release correction pass)"
            entry["audit_response"] = CORRECTED[fid] + " Earlier audit response: " + entry["audit_response"]
            import hashlib
            with open(os.path.join(FIG_DIR, "out", fid + ".svg"), "rb") as sf:
                entry["svg_sha256"] = hashlib.sha256(sf.read()).hexdigest()
        if fid in PATCHED:
            entry["status"] = PATCH_STATUS
            entry["audit_response"] = "Editorial patch alignment: " + PATCHED[fid] + " Earlier: " + entry["audit_response"]
            entry["editorial_patches"] = sorted(set(__import__("re").findall(r"P-0\d", PATCHED[fid])))
            import hashlib
            with open(os.path.join(FIG_DIR, "out", fid + ".svg"), "rb") as sf:
                entry["svg_sha256"] = hashlib.sha256(sf.read()).hexdigest()
        if m.pop("new_figure", False):
            import hashlib
            entry["status"] = "drawn 2026-10-06 pending independent review"
            entry["audit_response"] = "Not yet independently reviewed (drawn 2026-10-06; generator selfcheck and render inspection done)."
            with open(os.path.join(FIG_DIR, "out", fid + ".svg"), "rb") as sf:
                entry["svg_sha256"] = hashlib.sha256(sf.read()).hexdigest()
        if fid in UNIFIED:
            import hashlib
            prev = entry["audit_response"]
            entry["status"] = UNIFIED_STATUS
            entry["audit_response"] = ("Iconography unified 2026-10-07 (shared glyph registry scenkit.REG, key FIG-20, mechanical registry check in make_figures); "
                                       "not yet independently re-reviewed. Earlier record: " + prev)
            entry["iconography"] = "shared-v2"
            if fid in RC486_REDRAWN:
                entry["status"] = RC486_STATUS
                entry["audit_response"] = ("Redrawn 2026-10-07 against RC486 (P-08 to P-12 resolved elements, open minor findings fixed); not yet independently re-reviewed. Earlier record: " + entry["audit_response"].split("Earlier record: ")[-1])
            with open(os.path.join(FIG_DIR, "out", fid + ".svg"), "rb") as sf:
                entry["svg_sha256"] = hashlib.sha256(sf.read()).hexdigest()
        if "ambiguity" in m:
            entry["ambiguity"] = m.pop("ambiguity")
        if "coverage" in m:
            entry["coverage"] = m.pop("coverage")
        manifest.append(entry)
        placements.setdefault(entry["insert_after"], []).append(
            {"id": fid, "caption": entry["caption"], "width": "100%", "scope": entry["scope"]})
    with open(os.path.join(FIG_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(FIG_DIR, "placements.json"), "w", encoding="utf-8") as f:
        json.dump(placements, f, indent=2, ensure_ascii=False)
        f.write("\n")
