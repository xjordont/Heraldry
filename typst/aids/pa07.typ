// PA-7 Sight and Ground. Wording condensed from §2.6–2.9, §4.3.2–4.3.3, §5.9 (Hidden) and the Battlefield Reference Table.
#import "kit.typ": *
#let head = (2, "7", "Sight and Ground", "§ 2.7–2.9 · § 4.3 · § 5.9")

#side(..head, face: "front", art: "ART-CLA-ASSASSIN", art-w: 76pt)[
  #grid(columns: (1fr, 1fr), column-gutter: 20pt,
  [
    #aside-head(seed: 1)[Line of Sight]
    One straight sight line, centre to centre (Grid: square centre to square centre), decides both LOS and Cover. Check it at any time. It is mutual. Ignore your own space and decorative parts of models.
    #v(5pt)
    #caps[Blocked by]
    #dot[Blocking Terrain;]
    #dot[a solid floor, roof, or platform between;]
    #dot[1" or more of continuous Cover Terrain between the spaces (Grid: crossing the interior of a Cover square neither occupies);]
    #dot[Grid: touching a corner shared by 2 Blocking squares.]
    #v(4pt)
    Hidden and Invisible never block LOS.
    #gap-v
    #aid-table((34pt, 64pt, 1fr), ("roll", "key", "text"), ("Step", "State", "Effect"), (
      ([1], [Exposed], [No Cover; targeted normally.]),
      ([2], [Cover], [Targeted, but ranged attacks and effects have Disadvantage.]),
      ([3], [Hidden], [Cannot be targeted by anything that needs LOS.]),
    ), title: [Concealment], size: 10pt)
    #gap-v
    #aside-head(seed: 3)[Light and Darkness]
    #dot[The battlefield is in *Light* unless a rule sets Darkness.]
    #dot[*Light Source:* Aura 3" of Light. Its carrier cannot be Hidden.]
    #dot[*Darkness:* Cover against nonadjacent enemies; does not block LOS. Ordinary Darkvision does not ignore the Cover of *Magical* Darkness.]
  ],
  [
    #aside-head(seed: 2)[Cover]
    You have Cover from an enemy when:
    #dot[it is not adjacent and you are in Cover Terrain or an area that gives Cover;]
    #dot[the sight line crosses or touches a terrain feature that is not Open Terrain, outside both spaces;]
    #dot[the sight line crosses a combatant of your Sz or larger that is not Prone or Knocked Out;]
    #dot[a rule says so.]
    #v(4pt)
    *Effect:* ranged and thrown weapon attacks and non-area damaging ranged Powers roll base dice with *Disadvantage*; the caster's harmful LOS-based Power Checks have Disadvantage. Never melee, Areas, or hazards. Binary: never stacks.
    #gap-v
    #aside-head(seed: 4)[Hidden]
    *Hide (1 AP):* be outside every enemy's LOS, or in Cover (not from a combatant) from each enemy with LOS and none within your *Hide distance* (2"). Not while Engaged or carrying a Light Source.
    #v(4pt)
    *Lose Hidden* when you take damage, become Engaged, an enemy within Hide distance has LOS, an enemy with LOS has you out of Cover, you are Spotted, you Push or Trip, an enemy moves through your space, or after your first attack, harmful Power, or harmful Special Ability.
    #v(4pt)
    *Check* after each Move or Shift, each action, Power, or Reaction, and at the end of each activation.
    #v(4pt)
    *Spot (1 AP):* INT or SPI Check (higher) against 12.
  ])
]

#side(..head, face: "back")[
  #aid-table((92pt, 1fr, 1fr, 1fr), ("key", "c", "c", "c"), ("Terrain type", "Enter?", "Cover?", "LOS?"), (
    ([Open], [Yes], [No], [Clear]),
    ([Cover], [Yes], [To occupants, against nonadjacent enemies], [See in and out near the edge; blocked across 1"+ of depth]),
    ([Impassable], [No; may Jump over], [Yes, unless its entry says not (chasms, pits: none)], [Clear]),
    ([Blocking], [No], [-], [Blocked]),
  ), title: [Terrain Types], size: 10pt)
  #text(size: 9.5pt)[Overlapping features use the most obstructive type: Blocking, Impassable, Cover, Open. Impassable Terrain still allows adjacency and Engagement.]
  #v(8pt)
  #grid(columns: (1fr, 1fr), column-gutter: 20pt,
  [
    #aside-head(seed: 5, size: 16pt)[Terrain Tags]
    #dot[*Difficult:* 2" per 1" (Grid: 2" orthogonal, 3" diagonal).]
    #dot[*Dangerous:* entering, crossing, or ending movement in it applies its hazard, at most once per movement.]
    #dot[*Slippery:* first voluntary move through it each activation: DEX Check; fail: Prone, movement ends. Anyone made Prone or falling on it Slides 2" in their direction of travel.]
    #dot[*Shallow Water:* Difficult; no Cover by itself.]
    #dot[*Deep Water:* swim at the surface; Difficult; cannot be Prone; Disadvantage on attack damage, STR Checks, and DEX Checks. *Swim* ignores all of this.]
    #gap-v
    #aside-head(seed: 7, size: 16pt)[Elevation]
    #dot[*Higher:* 2" or more above. Attacks on the lower enemy: base dice with *Advantage*.]
    #dot[Raised ground with no stated height is 2".]
    #dot[Elevation changes only adjacency and melee distance, not range, LOS, Cover, or Areas.]
  ],
  [
    #aid-table((60pt, 1fr), ("key", "text"), ("Area", "Shape"), (
      ([Cone X"], [Triangle X" long from its origin; far edge X" wide.]),
      ([Line X"], [Rectangle X" long, 1" wide unless stated.]),
      ([Aura X"], [X" all round its source (from the footprint). Moves with its source.]),
    ), title: [Areas of Effect], size: 10pt)
    #dot[A cone or line starts at its source and never affects its source.]
    #dot[Hits anything it touches; Grid: squares whose centre is inside, ties outward.]
    #dot[Cannot pass Blocking Terrain or a solid floor, roof, or platform. Cover never protects; Hidden and Invisible are still hit.]
    #dot[Roll damage once; apply it to each target separately.]
    #dot[Measured flat: elevation adds no distance.]
  ])
]
