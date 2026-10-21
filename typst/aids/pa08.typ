// PA-8 The Campaign. Wording condensed from §11.1.5, §11.2.1–11.2.3, §11.3 and C.10.
#import "kit.typ": *
#let head = (11, "8", "The Campaign", "§ 11.1–11.3 · C.10")
#let small(t) = text(size: 9.5pt, t)

#side(..head, face: "front")[
  #cycle(
    (1, [Expedition], [
      After choosing the Active Party, before the battlefield, each party rolls *1d10* on the Expedition Event Table (back). Apply it now unless it names a later setup timing.
      #v(3pt)
      #small[Same timing: the Setup Roll-off winner orders them. Roll-off effects apply before that roll.]]),
    (2, [Skirmish], [
      Generate the battlefield, deploy, and play the adventure (Player Aid 10).
      #v(3pt)
      #small[An allied Hero adjacent to a death marker may *Interact* (1 AP) to recover a dead Hero's items; secured only if they extract.]]),
    (3, [Aftermath], [
      Every adventure, won or lost:
      #steps[*Secure:* secured Coins to the Treasury, unequipped items to Storage, once each.][*The fallen:* apply rolled results. A dead Hero leaves the Roster; keep the record until the next adventure, for resurrection.][*Journey home:* roll *1d20* on the Climate's Journey Table.]]),
    (4, [Town], [
      Spend *4 TAP* on Town actions (Player Aid 9). Some Journey results change the TAP or give a discount for this Town Phase only.]),
    arms(11, w: 46pt))
  #v(12pt)
  #block(width: 100%, stroke: (top: 0.5pt + ink, bottom: 0.5pt + ink), inset: (y: 6pt))[
    *Start of the next adventure:* refresh each Hero's normal resources, *then* apply Journey results, *then* Expedition Events.]
  #v(8pt)
  #grid(columns: (1fr, 1fr, 1fr), column-gutter: 18pt,
  [
    #aside-head(seed: 1, size: 16pt)[Monster CV]
    A party-controlled source that defeats a Monster collects its CV. *Competitive:* secured when the adventure ends. *Solo or co-op:* Major and Costly Victory secure it; Withdrawal and Catastrophe lose it.
  ],
  [
    #aside-head(seed: 3, size: 16pt)[The Three Fates]
    *Die:* removed unless returned to life before the next adventure; carried items are lost unless recovered. *Retire:* in the Town Phase, for the Retirement Payout; at Level 10, a Legendary Veteran. *Triumph:* share the final victory.
  ],
  [
    #aside-head(seed: 5, size: 16pt)[Triumph]
    *Competitive:* complete any *5* different Stronghold Components; Triumph after that Town Phase (both, if together). *Solo or co-op:* attempt the Triumph Finale with 5 Components and an Active Party of APL 9–10.
  ])
  #v(8pt)
  #text(size: 9.5pt)[*Limits:* Roster 8 Heroes; 1 new Hero per Town Phase. Stronghold roster 8 Hirelings, Animal Companions included. Journey results use only living Heroes of the Active Party that played; ignore any part with no eligible target.]
]

#side(..head, face: "back", art: "ART-WOR-1-3-6-ADVENTURERS-AND-THE-ROAD", art-w: 260pt)[
  #aid-table((30pt, 120pt, 1fr), ("roll", "key", "text"), ("d10", "Event", "Effect"), (
    ([1], [Ambush on the Road], [Your side has −1 on its Initiative roll in Round 1.]),
    ([2], [Foul Weather], [Treat this adventure's Weather roll as 1. No effect if the weather is set without a roll.]),
    ([3], [Treacherous Path], [One chosen Hero in your Active Party starts having lost 1d4 HP (not below 1 HP).]),
    ([4], [Lost and Delayed], [The opposing party automatically wins the Setup Roll-off.]),
    ([5], [Uneventful Journey], [No effect.]),
    ([6], [Wandering Peddler], [Buy one Tier 1 or 2 consumable at 50% now for an eligible Hero in the Active Party. It cannot be sold.]),
    ([7], [A Moment of Rest], [One chosen Hero starts with +1 Luck Point, up to 1 above their maximum this adventure.]),
    ([8], [Scout's Vantage], [Reposition one random Monster Group up to 4″ before Hero deployment.]),
    ([9], [Omen of Blood], [The first time your party reduces an enemy Hero or an Elite Monster to 0 HP, add 1c to unbanked rewards.]),
    ([10], [Shortcut], [Your Heroes may deploy up to 2″ outside their deployment zone.]),
  ), title: [Expedition Events], size: 10.5pt)
  #text(size: 9.5pt)[Solo or co-op: a result that names an opposing party uses the solo conversion in §10.5.5.]
  #v(10pt)
  #grid(columns: (1fr, 1fr), column-gutter: 18pt,
  [
    #aside-head(seed: 2, size: 16pt)[Journey Home]
    Roll *1d20* on the Journey Table of the Climate just completed (§11.2.3). A discount, free service, or similar benefit applies to the very next Town Phase only. A more specific scenario or campaign rule wins any conflict.
  ],
  [
    #aside-head(seed: 4, size: 16pt)[Keep a Record]
    Between adventures, record enough to resume:
    #dot[the Roster and Active Party;]
    #dot[each Hero's Level, Wounds, advancement, and lasting rewards;]
    #dot[Treasury and Storage; Hirelings and Animal Companions;]
    #dot[Stronghold Components; any death, retirement, Journey result, or injury that still matters.]
  ])
]
