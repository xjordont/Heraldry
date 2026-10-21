// PA-4 The Fallen. Wording condensed from §5.8, §5.8.1, §5.9 (Knocked Out), §11.2.4 (Chapel) and C.10.
#import "kit.typ": *
#let head = (6, "4", "The Fallen", "§ 5.8 · § 5.8.1 · § 11.2.4 · C.10")

#side(..head, face: "front", art: "ART-MON-GHOUL", art-w: 132pt)[
  #grid(columns: (330pt, 1fr), column-gutter: 18pt,
  [
    #block(spacing: 0pt, endbox(ends: false)[
      #text(font: goth, weight: 700, size: 15pt)[A Hero drops to 0 HP] #h(6pt) HP never falls below 0.])
    #link-at(62pt)
    #stage(1, [Knocked Out])[The Hero becomes *Knocked Out* and *Prone*, and loses all Temporary HP.]
    #link-at(62pt)
    #stage(2, [Mark 1 Wound])[A Hero has at most 3 Wounds. Wounds are not a condition.]
    #link-at(62pt)
    #flow(lead: 0pt, w: 124pt,
      rows: ((none, [Third Wound?], [Dies: removed from play. Place a death marker. No Injuries Roll.], "Dead"),),
      end: (none, [*Injuries Roll:* 1d20 on the Injuries Table (back). A roll, not a Check: apply modifiers, then treat below 1 as 1 and above 20 as 20.], "Roll"))
    #v(10pt)
    #note[A rule may let a Hero skip the Wound and the roll (such as Determined Resolve), but never prevents True Death, a third Wound, or death from a rule that kills outright.]
  ],
  [
    #aside-head(seed: 1)[Hit While Down]
    Each source that deals *1+ damage or HP loss* to a Knocked Out Hero, after mitigation, marks *1 Wound*; the third kills. Once per source; no Injuries Roll. A source reduced to 0 does nothing.
    #gap-v
    #aside-head(seed: 3)[Knocked Out]
    Cannot activate, act, move by choice, attack, use Powers or Special Abilities, or react. Stays Prone. Never Engaged, and makes no one Engaged. Ends when HP rises above 0; Wounds and injuries remain.
    #gap-v
    #aside-head(seed: 5)[Others at 0 HP]
    Hirelings, Monsters, and Bosses are removed from play: no Wounds, no Injuries Roll.
    #gap-v
    #aside-head(seed: 7)[Death Marker]
    Does not block movement or LOS; cannot be targeted. An adjacent allied Hero may *Interact* (1 AP) to recover the dead Hero's items; they are secured only if that Hero extracts with them.
  ])
]

#side(..head, face: "back")[
  #aid-table((26pt, 112pt, 1fr), ("roll", "key", "text"), ("d20", "Result", "Effect"), (
    ([1], [True Death], [Dies at once; removed from play. Campaign: off the Roster unless returned to life before the next adventure.]),
    ([2], [Bleeding Out], [Dies at the end of the following round unless restored to 1+ HP, or an adjacent ally uses Bandages (Interact, 1 AP) and passes an INT Check. Then stays Knocked Out unless healed above 0.]),
    ([3], [Shattered Arm], [Stays Knocked Out. After: Disadvantage on STR Checks; no 2-Hand items or shields.]),
    ([4], [Crushed Leg], [Stays Knocked Out. After: Speed −2″, no Shift, Disadvantage on DEX Checks.]),
    ([5], [Cracked Skull], [Stays Knocked Out. After: Disadvantage on INT, SPI, and Casting Checks.]),
    ([6], [Gut Wound], [Stays Knocked Out. After: maximum HP −3.]),
    ([7], [Blood in the Eyes], [Stays Knocked Out. After: LOS 6″; Disadvantage on sight-based attacks and Checks.]),
    ([8], [Broken Ribs], [1 HP, stays Prone; at most 1 AP in their next activation.]),
    ([9], [Concussion], [Stays Knocked Out and Prone, and becomes Stunned.]),
    ([10], [Torn Shoulder], [1 HP, stays Prone. First weapon attack each round: base dice with Disadvantage.]),
    ([11], [Split Brow], [1 HP, stays Prone, gains Bleeding.]),
    ([12], [Winded], [1 HP, stays Prone; no Reactions until the start of their next activation.]),
    ([13], [Crawling Survival], [Stays Knocked Out; the next damage this round is reduced by 2 (possibly to 0, before the hit-while-down rule).]),
    ([14], [Shaking Hands], [1 HP, stays Prone; no Powers, scrolls, or Special Abilities this round.]),
    ([15], [Scarred but Standing], [1 HP, Stands, gains Bleeding.]),
    ([16], [Grim Return], [1d4 HP, Stands; Disadvantage on their next Check this round.]),
    ([17], [Last Reserve], [1 HP, Stands; regains 1 NRG or 1 Luck Point (Luck if Max NRG 0).]),
    ([18], [Spiteful Return], [1 HP, stays Prone. Next weapon attack before the end of their next activation: +2 damage of its primary type, unless a Total Miss.]),
    ([19], [Death Refused], [1d6 HP, Stands, may Shift 1″ at once.]),
    ([20], [Vengeful Surge], [Half maximum HP (minimum 1), Stands, +1 AP for their next activation.]),
  ), title: [Injuries Table], size: 10pt)
  #text(size: 9.5pt)[1–5 catastrophic · 6–14 lingering · 15–20 hard survival. Results marked "after" last until healed in the Town Phase; Torn Shoulder too.]
  #v(8pt)
  #grid(columns: (1fr, 1fr, 1fr), column-gutter: 16pt,
    [*Chirurgeon's Care* #cost[1 TAP] \ Remove 1 Wound from one Hero. 6c × Level.],
    [*Cleanse Affliction* #cost[1 TAP] \ Remove one lasting injury result. 3c.],
    [*Resurrection* #cost[2 TAP] \ Return a dead Hero with a retained record, with 1 Wound. 8c × Level; once per Hero per campaign.])
]
