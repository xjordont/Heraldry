// PA-1 The Round. Wording condensed from §3.1–3.6, §2.3–2.4, §2.10, §4.2, C.1, C.4 and 10.5.4.
#import "kit.typ": *
#let head = (3, "1", "The Round", "§ 3 · § 2.3–2.4 · § 2.10 · C.1 · C.4")
#let small(t) = text(size: 9.5pt, t)

#side(..head, face: "front")[
  #cycle(
    (1, [Initiative Phase], [
      #steps[Refresh AP to maximum.][Each side rolls *1d20 + Party Leader's INT + SPI*; higher wins. No Leader on the battlefield: another allied Hero; no Hero: no modifier.][The winner chooses which side activates first.][Resolve start-of-round effects.]
      #v(4pt)
      #small[*Ties:* highest DEX among the Heroes rolled (if both sides used one); then, from Round 2, last round's winner; then roll again.]]),
    (2, [Party Phase], [
      #dot[Sides alternate activating *one* eligible combatant at a time.]
      #dot[Each combatant activates *once* per round and must spend at least 1 AP, unless it can take no action.]
      #dot[A side *Passes* only when it has no eligible combatant; then it activates no one else this round, not even a new Summon. Its unspent AP still pays for Reactions.]
      #dot[Ends when every side has Passed.]]),
    (3, [Monster Phase], [
      #steps[Resolve wake-up rules.][Each Awake Group activates in ascending Group number (Player Aid 2).]
      #v(4pt)
      #small[A Boss acts by *Relentless Assault* during the Party Phase instead.]]),
    (4, [End of Round], [
      #steps[Resolve end-of-round effects (timing order, back).][End "until the end of the round" effects; remove Temporary HP.][Remove unspent AP.][Resolve scoring, extraction, round limits, and victory.]]),
    arms(3, w: 46pt))
  #v(12pt)
  #grid(columns: (1.3fr, 1fr, 0.95fr), column-gutter: 16pt,
  [
    #aside-head(seed: 1)[Activating]
    #steps[Choose an eligible allied combatant.][Resolve start-of-activation effects.][Spend AP on actions in any order.][Resolve end-of-activation effects.][Mark it as activated.]
    #v(4pt)
    #small[A Hero reduced to 0 HP in their own activation ends it at once (Player Aid 4).]
  ],
  [
    #aside-head(seed: 3)[Eligible If]
    On the battlefield, on your side, at least *1 AP*, not yet activated, not prevented by a rule.
    #v(4pt)
    *Stunned or Sleeping:* may activate with 0 AP only to end the condition.
    #v(4pt)
    *Summon from a Power:* activates right after the current activation, if its side has not Passed.
  ],
  [
    #aside-head(seed: 5)[Solo & Co-op]
    *PvE Initiative:* one player rolls 1d20 plus party Initiative bonuses (no INT or SPI). *12+:* Party Phase first. *11 or less:* Monster Phase first. Each phase resolves once, then End of Round.
  ])
]

#side(..head, face: "back", art: "ART-CLA-FIGHTER", art-w: 118pt)[
  #grid(columns: (1.18fr, 1fr), column-gutter: 18pt,
  [
    #aid-table((auto, auto, 1fr), ("key", "c", "text"), ("Action", "AP", "Effect"), (
      ([Move], [1], [Move up to your Speed.]),
      ([Shift], [1], [Move 1" without triggering Reflex Attack.]),
      ([Attack], [1], [One melee or ranged attack. A Hero's 2nd+ weapon attack in an activation: Disadvantage.]),
      ([Push], [1], [Adjacent target; STR Check with Disadvantage. Success: Push it 2".]),
      ([Trip], [1], [Needs a Trip weapon; target your Sz or smaller. STR or DEX Check with Disadvantage. Success: Prone.]),
      ([Power], [var.], [Use one Power you know.]),
      ([Read Scroll], [1], [Use one equipped scroll.]),
      ([Special Ability], [var.], [Use one activated ability; it lists its AP.]),
      ([Stand], [1], [Remove Prone. Not movement.]),
      ([Interact], [1], [Use an adjacent, visible battlefield element.]),
      ([Hide], [1], [Become Hidden: outside every enemy's LOS, or in Cover from each enemy with LOS and none within your Hide distance. Not while Engaged or carrying a Light Source.]),
      ([Spot], [1], [Pick an eligible Hidden enemy; INT or SPI Check (higher) against 12. Success: it loses Hidden.]),
      ([Wait], [1], [Do nothing.]),
      ([Reload], [1], [Ready an equipped Reload weapon.]),
    ), title: [Actions])
    #text(size: 9.5pt)[The same non-Reaction 0 AP action only once per activation. Monsters use Monster AI instead.]
    #gap-v
    #aside-head(seed: 6)[Luck]
    A Hero may spend *1 Luck Point* after seeing a d20 Check made by or against them, or a damage roll they caused or that directly affects them, before its consequences apply. Reroll the whole roll, keeping Advantage or Disadvantage, and use the new result. Once per roll; one Hero only (Initiative winner's side decides first). Refreshes each adventure.
  ],
  [
    #aside-head(seed: 2)[Checks]
    Roll *1d20 + ability*. *12 or more* succeeds; 11 or less fails. *Natural 20* always succeeds; *natural 1* always fails (Critical Failure). Monsters never make Checks (Player Aid 2).
    #v(5pt)
    *Advantage:* add one die, drop the lowest. *Disadvantage:* add one die, drop the highest. On damage rolls only base dice count. Both cancel; neither stacks.
    #gap-v
    #aside-head(seed: 4)[Timing]
    #dot[*Start of round:* after AP refresh and Initiative, before the first activation.]
    #dot[*Start of activation:* as soon as the combatant is chosen.]
    #dot[*End of activation:* as soon as it finishes acting.]
    #dot[*End of round:* the End of Round phase, after both phases.]
    #v(6pt)
    #caps[Simultaneous effects]
    #v(1pt)
    The more specific rule first. Otherwise:
    #steps[Initiative winner's side][Other side][Monster Groups, ascending number][Terrain, weather, hazards, scenario]
    #v(4pt)
    #text(size: 9.5pt)[Solo or co-op: the phase that resolved first goes first. Same side: the Party Leader's controller orders them. Still tied: Random Determination.]
  ])
]
