// PA-9 The Town. Wording condensed from §11.2.4–11.2.6, §11.3 and C.10.
#import "kit.typ": *
#let head = (11, "9", "The Town", "§ 11.2.4–11.2.6 · § 11.3 · C.10")
#let place-head(t, sub, seed: 1) = { aside-head(seed: seed, size: 18pt, t); v(-3pt); text(size: 9.5pt, fill: ink3, sub) }

#side(..head, face: "front")[
  #grid(columns: (1fr, 1.15fr), column-gutter: 20pt,
  [
    #aside-head(seed: 9)[Town Phase]
    #steps[Confirm Storage, Treasury, Roster, and lingering injuries.][Resolve start-of-Town effects, then gain *4 TAP* (or a Journey's amount).][Spend TAP on legal actions, in any order.][Pay each action's Coin cost as it resolves.][Update sheets, Powers, gear, commissions, Storage, and Stronghold.][Confirm a legal Roster and Active Party.]
    #v(6pt)
    #text(size: 9.5pt)[Locations may be visited repeatedly. Unspent TAP are lost.]
    #gap-v
    #place-head([The Chapel], [Healing, afflictions, miracles], seed: 3)
    #act([Chirurgeon's Care], [1 TAP])[Remove 1 Wound from one Hero. 6c × Level.]
    #act([Cleanse Affliction], [1 TAP])[Remove one lingering injury or other permanent effect of the Injuries Table or a similar injury rule. 3c.]
    #act([Quiet the Bells], [1 TAP])[Remove Heard the Song from one Hero. 0c.]
    #act([Resurrection], [2 TAP])[A Hero with a retained death record returns with 1 Wound. 8c × Level. Not past the roster maximum; once per Hero per campaign.]
  ],
  [
    #place-head([The Grand Hall], [Trade, brokerage, commissions, fencing], seed: 1)
    #act([Buy and Sell Goods], [0 TAP])[Buy Tier 1–2 items at list price (mundane gear, Tier 1–2 consumables, non-special enhanced items below Rare). Sell at 50%. With a *Merchant* on the Roster, once: one sale at 75% or one purchase at 90% (rounded up). Not with other modifiers.]
    #act([Commission Rare Item], [1 TAP])[Reserve a Tier 1–3 permanent special item, a Tier 3 consumable, or an Enchanted +3 item to buy next Town Phase at normal price. APL 7+: Tier 4 or Enchanted +4 instead, at +25%. One pending commission; one commissioned purchase per Town Phase. Never Tier 5, Legendary Artifacts, or +5. Expires if not bought.]
    #act([Appraise and Fence], [1 TAP])[Sell up to 2 items at 70%.]
    #act([Recruit Hero], [1 TAP])[Fewer than 8 Heroes and no recruit yet this Town Phase: pay 10c, add one recruit. Its starting items stay with it until it completes an adventure in the Active Party.]
    #gap-v
    #place-head([The Arcane Spire], [Powers and scrolls], seed: 5)
    #act([Scribe Scroll], [1 TAP])[A Hero scribes a known Tier 1–2 Arcane Spell or Divine Prayer. 60% of its scroll price. Cannot be sold.]
    #act([Research Power], [1 TAP])[Learn a Tier 1–3 Power of a tradition already used. 6c × Tier × Tier.]
    #act([Transcribe Lore], [1 TAP])[Swap a known Tier 1–3 Power for another of the same tradition and Tier or lower. 3c × Tier × Tier.]
    #v(3pt)
    #text(size: 9.5pt)[Never above the Hero's highest Tier; each Hero researches or transcribes once per Town Phase.]
  ])
]

#side(..head, face: "back", art: "ART-BAS-HEARTHHOLD", art-w: 200pt)[
  #grid(columns: (1fr, 1fr), column-gutter: 20pt,
  [
    #place-head([The Training Grounds], [Veterans and technique], seed: 2)
    #act([Train], [1 TAP])[Train one Hero under Hero Advancement (§6.16).]
    #act([Retrain], [1 TAP])[Swap one Class or General Talent for another of the same tier or list. Not Archetype Abilities. 4c × Level.]
    #gap-v
    #place-head([The Ironworks], [Gear], seed: 4)
    #act([Masterwork Upgrade], [1 TAP])[Up to 2 mundane weapons, Chest armour, or shields with no Item Quality and a listed Masterwork value gain Masterwork. Pay the difference (minimum 1c) each. Sells at its old value.]
    #gap-v
    #aside-head(seed: 6, size: 18pt)[Hirelings]
    Recruit: *1 TAP* plus the listed Coins; no upkeep. Up to 8 on the Stronghold roster, Animal Companions included. Dismiss for 0 TAP, no refund.
  ],
  [
    #place-head([The Guild of Keys], [Contracts, maps, logistics], seed: 8)
    #act([Accept Contract], [1 TAP])[One active side contract. After the next adventure is generated, before deployment, roll 1d6: *1–2 Monster Writ:* defeat 1+ Monster Group and 1+ Hero extracts. *3–4 Salvage Writ:* extract 1+ treasure, relic, clue, captive, or object beyond the primary objective. *5–6 Survey Writ:* a Hero not Engaged uses Interact (1 AP) adjacent to a feature or marker within 6" of the centre. No extraction route: a living Hero on any edge at the end meets the extraction part. Reroll an impossible term; none possible: cancel and refund 1 TAP next Town Phase. Done, with a Hero extracted: *5c × APL* (start-of-adventure APL) in Aftermath. Never changes victory conditions; not for the Triumph Finale.]
    #act([Map Room], [1 TAP])[Competitive: win the next Setup Roll-off. Solo or co-op: roll a second Core Scenario from the Climate and choose. Fixed adventure: Advantage on the party's first Setup Roll-off, search, or scenario Interact Check.]
    #gap-v
    #aid-table((1fr, 1fr), ("c", "c"), ("Built", "Next Component"), (
      ([0], [130c]), ([1], [170c]), ([2], [210c]), ([3], [250c]), ([4+], [290c]),
    ), title: [Stronghold], size: 10pt)
    #text(size: 9.5pt)[*1 TAP*, at most one Component per Town Phase. A Vault Reserve is spent only in the Town Phase it is gained.]
  ])
]
