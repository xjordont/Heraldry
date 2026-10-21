// PA-6 Movement. Wording condensed from §2.6, §4.4, §5.1, §5.5.4, §5.6 and §2.9.9.
#import "kit.typ": *
#let head = (4, "6", "Movement", "§ 2.6 · § 4.4 · § 5.1 · § 5.6")

#side(..head, face: "front", art: "ART-CLA-RANGER", art-w: 100pt)[
  #aid-table((84pt, 1fr, 1.05fr), ("key", "text", "text"), ("Type", "Meaning", "Reflex Attack?"), (
    ([Move], [Voluntary, up to Speed. 1 AP.], [Yes, leaving an enemy's melee distance.]),
    ([Shift], [Voluntary, 1″ (or a granted distance). 1 AP.], [No, unless the rule says so.]),
    ([Climb], [Vertical, during a Move. 2″ per 1″; STR Check.], [Yes, leaving an enemy's melee distance.]),
    ([Jump], [Horizontal, during a Move. 2″ per 1″; DEX Check.], [Yes, leaving an enemy's melee distance.]),
    ([Fly (X″)], [Voluntary, using the Fly Speed.], [Yes, leaving an enemy's melee distance.]),
    ([Push / Pull], [Forced, directly away from / toward a source or point.], [No.]),
    ([Slide], [Forced, in the named direction.], [No.]),
    ([Teleport], [Placed at a legal destination; ignores the way between.], [No.]),
  ), title: [Movement Types], size: 10pt)
  #v(4pt)
  #grid(columns: (1fr, 1fr, 1fr), column-gutter: 16pt,
  [
    #aside-head(seed: 1, size: 16pt)[Moving]
    #dot[Through allies, never enemies (except a Hidden enemy, or a Small mover past Large or Huge).]
    #dot[Never end overlapping a combatant, Impassable Terrain, or Blocking Terrain.]
    #dot[Prone may move, but not Climb or Jump.]
    #dot[Finish one Move before another action.]
    #dot[*Fly:* ignores ground terrain and Impassable Terrain, passes over combatants; not through Blocking Terrain; must end legal or Fall.]
  ],
  [
    #aside-head(seed: 3, size: 16pt)[Costs]
    #dot[*Difficult Terrain, Climb, Jump:* 2″ per 1″. Several on the same 1″: only the highest.]
    #dot[*Grid*, orthogonal / diagonal square: 1″ / 1.5″; Difficult 2″ / 3″; jumped 2″ / 3″.]
    #dot[*Corners:* a diagonal step needs one legal orthogonal route around it.]
    #dot[*Shift:* a diagonal square costs 1″; it must pay terrain costs and cannot Climb or Jump.]
    #dot[Track in 0.5″; never round movement.]
  ],
  [
    #aside-head(seed: 5, size: 16pt)[Climb · Jump · Fall]
    #dot[*Climb:* declare an affordable destination, STR Check. Fail: stay, Prone, movement ends.]
    #dot[*Jump:* declare a landing point, DEX Check. Fail: last legal point before the gap, Prone, movement ends. Rise at most 1″.]
    #dot[*Falling:* lose 1 HP per full 1″ beyond the first (untyped, no AV), then Prone. Not movement.]
    #dot[Monsters always pass Terrain Checks.]
  ])
]

#side(..head, face: "back")[
  #grid(columns: (1fr, 1fr), column-gutter: 20pt,
  [
    #aside-head(seed: 2)[Engagement and Reach]
    #dot[*Engaged:* adjacent to an enemy that is not Knocked Out. Knocked Out combatants are never Engaged.]
    #dot[*Melee:* an adjacent enemy: within 1″, or the 8 surrounding squares.]
    #dot[*Reach:* may target within 2″ (2 squares, diagonals included). Reach does not change Engagement.]
    #dot[*Elevation:* adjacent only if horizontal distance and vertical separation are each 1″ or less.]
    #dot[Blocked LOS between two combatants: not adjacent, not Engaged.]
    #gap-v
    #aside-head(seed: 4)[Reflex Attack]
    1 AP Reaction: an enemy, in its activation, leaves your melee distance with *Move*, or makes a ranged attack within it. One melee attack, base dice with Disadvantage. Never from Shift, forced movement, Falling, or ranged Reactions.
    #gap-v
    #aid-table((26pt, 1fr, 1fr), ("key", "c", "c"), ("Sz", "Footprint", "Grid"), (
      ([S], [1″ × 1″], [1 square]),
      ([M], [1″ × 1″], [1 square]),
      ([L], [2″ × 2″], [2 × 2]),
      ([H], [3″ × 3″], [3 × 3]),
    ), title: [Size], size: 10pt)
    #text(size: 9.5pt)[Measure everything from the footprint. No listed Size: Medium.]
  ],
  [
    #aside-head(seed: 6)[Forced Movement]
    #dot[*Push X″:* up to X″ directly away. *Pull X″:* directly toward. *Slide X″:* the named direction. In Grid Mode each Push square must increase the distance, each Pull square decrease it.]
    #dot[Stops at the last legal point. Stopped by Impassable or Blocking Terrain or a combatant: *Collision* (no damage unless a rule says so).]
    #dot[A battlefield edge stops it. A drop does not: move to the edge, then *Fall*.]
    #dot[Terrain costs count against the distance; hazards resolve after it ends.]
    #gap-v
    #aside-head(seed: 8)[Push and Trip]
    Your own activation only; not attacks, so no Block, Dodge, or Parry, and no multi-attack chain. Hostile: a Hidden actor loses Hidden.
    #v(4pt)
    #grid(columns: (auto, 1fr), column-gutter: 6pt, row-gutter: 6pt,
      cost[Push 1 AP], [Adjacent target. STR Check with Disadvantage. Success: Push 2″ away.],
      cost[Trip 1 AP], [Trip weapon; target your Sz or smaller in its range or reach. STR or DEX Check with Disadvantage. Success: Prone.])
  ])
]
