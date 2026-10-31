// PA-4 The Fallen. Wording condensed from §5.8 (RC522: Reduced to 0 HP, Wounds, Lingering Injuries, Death),
// §5.8.1 Injuries Table, §5.9 (Knocked Out), §11.2.4 (The Chapel) and C.10.
#import "kit.typ": *
#let head = (6, "4", "The Fallen", "§ 5.8 · § 5.8.1 · § 11.2.4 · C.10")

#side(..head, face: "front", art: "ART-MON-GHOUL", art-w: 124pt)[
  #grid(columns: (330pt, 1fr), column-gutter: 18pt,
  [
    #block(spacing: 0pt, endbox(ends: false)[
      #text(font: goth, weight: 700, size: 15pt)[A Hero drops to 0 HP] #h(6pt) HP never falls below 0.])
    #link-at(62pt)
    #stage(1, [Knocked Out])[
      The Hero becomes *Knocked Out* and *Prone*, and loses all Temporary HP.
      #v(4pt)
      *In their own activation,* it ends now: skip their remaining actions and end-of-activation effects (no Bleeding loss or Poisoned damage; Poisoned remains), then mark them as activated. Effects that last until the end of the activation still end. Unspent AP stays for Reactions.]
    #link-at(62pt)
    #stage(2, [Mark 1 Wound])[A Hero has at most 3 Wounds. Wounds are not a condition.]
    #link-at(62pt)
    #flow(lead: 0pt, w: 124pt,
      rows: ((none, [Third Wound?], [Dies: removed from play. Place a death marker. No Injuries Roll.], "Dead"),),
      end: (none, [*Injuries Roll:* 1d20 on the Injuries Table (back). A roll, not a Check: apply modifiers, then treat below 1 as 1 and above 20 as 20.], "Roll"))
    #v(10pt)
    #note[A rule may let a Hero skip the Wound and the roll (such as Determined Resolve), but never prevents a third Wound or death from a rule that kills outright.]
  ],
  [
    #aside-head(seed: 1)[Hit While Down]
    Each source that deals *1+ damage or HP loss* to a Knocked Out Hero, after mitigation, marks *1 Wound*; the third kills. Once per source; no Injuries Roll. A source reduced to 0 does nothing.
    #gap-v
    #aside-head(seed: 3)[Knocked Out]
    Cannot activate, act, move by choice, attack, use Powers or Special Abilities, or react. Stays Prone. Never Engaged, and makes no one Engaged. Ends when HP rises above 0; Wounds and Injuries Table results remain.
    #gap-v
    #aside-head(seed: 5)[Others at 0 HP]
    Hirelings, Monsters, and Bosses are removed from play: no Wounds, no Injuries Roll.
    #gap-v
    #aside-head(seed: 7)[Death Marker]
    Does not block movement or LOS; cannot be targeted. An adjacent allied Hero may *Interact* (1 AP) to recover the dead Hero's items; they are secured only if that Hero extracts with them.
  ])
]

#side(..head, face: "back")[
  #aid-table((26pt, 118pt, 1fr), ("roll", "key", "text"), ("d20", "Result", "Effect"), (
    ([1], [Decapitated], [Dies at once; removed from play. Campaign: follow 11.1.5 Die.]),
    ([2], [Severed Artery], [Stays Knocked Out. Dies at the end of the following round unless restored to 1+ HP, or an adjacent ally uses Bandages (Interact, 1 AP) and passes an INT Check. Treated: stays Knocked Out until healed above 0 HP.]),
    ([3], [Perforated Bowel], [Stays Knocked Out. -4 Max HP. Dies when the adventure ends unless, after this result, a Power, scroll, or Tier 3+ potion restores HP to them.]),
    ([4], [Punctured Lung], [Stays Knocked Out. Begins each round with 2 AP instead of 3.]),
    ([5], [Mangled Arm], [Stays Knocked Out. Holds at most 1 Hand of items; no shields; Disadvantage on STR Checks.]),
    ([6], [Fractured Leg], [Stays Knocked Out. -2" Speed (minimum 1"); no Shift or Jump; Disadvantage on DEX Checks.]),
    ([7], [Cracked Skull], [Stays Knocked Out. Disadvantage on INT, SPI, and Casting Checks.]),
    ([8], [Gouged Eye], [Stays Knocked Out. LOS 6"; Disadvantage on ranged attack damage rolls and Spot Checks.]),
    ([9], [Ruptured Eardrum], [1 HP, stays Prone, becomes Stunned. Disadvantage on Spot Checks and Dodge.]),
    ([10], [Concussion], [1 HP, stays Prone. Cannot take Reactions.]),
    ([11], [Shattered Collarbone], [1 HP, stays Prone. Weapon attack damage rolls with Disadvantage.]),
    ([12], [Crushed Hand], [1 HP, stays Prone. Weapon attacks cannot score Critical Hits or trigger exploding bonus dice.]),
    ([13], [Crushed Windpipe], [1 HP, stays Prone. -3 Max NRG (minimum 0); at most 1 weapon attack in each of their activations.]),
    ([14], [Ruptured Hamstring], [1 HP, stays Prone. Max Speed 4"; Stand costs +1 AP; cannot Jump.]),
    ([15], [Lacerated], [1 HP, Stands at once, gains Bleeding. -2 Max HP.]),
    ([16], [Split Brow], [1 HP, Stands at once. LOS 12".]),
    ([17], [Broken Ribs], [1 HP, Stands at once. -1 AV (minimum 0); cannot take the Push action.]),
    ([18], [Slashed Wrist], [1 HP, Stands at once. Melee and Thrown weapon attacks deal -1 damage.]),
    ([19], [Pierced Thigh], [1 HP, Stands at once. -1" Speed (minimum 1").]),
    ([20], [Adrenaline Surge], [Half Max HP (rounded down, minimum 1 HP), Stands at once, +1 AP at the start of their next activation.]),
  ), title: [Injuries Table], size: 9.5pt)
  #text(size: 9.5pt)[*1–3* mortal trauma · *4–8* Knocked Out, critical injury · *9–14* Prone at 1 HP, major injury · *15–19* standing at 1 HP, minor injury · *20* a surge of strength. Ongoing effects on *3–19* are lingering injuries.]
  #v(10pt)
  #grid(columns: (1fr, 1fr), column-gutter: 18pt,
  [
    #aside-head(seed: 2)[Lingering Injuries]
    #dot[*Campaign:* permanent until *Cleanse Affliction* in the Town Phase. *One-off:* until the adventure ends.]
    #dot[Applies while the Hero is not Knocked Out. Stow an item it makes illegal to hold or use (0 AP).]
    #dot[Several rules set Max Speed or LOS: use the lowest.]
    #dot[Bleeding, Prone, and Stunned from the table resolve and end normally.]
    #dot[Rolled one you already have? Reroll, ignoring 1, 2, 20, and any you have. With all 17, add none.]
  ],
  [
    #aside-head(seed: 6)[The Chapel]
    #dot[*Chirurgeon's Care* #cost[1 TAP] Remove 1 Wound from one Hero. 6c × Level.]
    #dot[*Cleanse Affliction* #cost[1 TAP] Remove one lingering injury or other permanent effect of the Injuries Table or a similar injury rule. 3c.]
    #dot[*Resurrection* #cost[2 TAP] Return a dead Hero with a retained record, with 1 Wound. 8c × Level; once per Hero per campaign.]
  ])
]
