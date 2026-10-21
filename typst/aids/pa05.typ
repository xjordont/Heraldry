// PA-5 Conditions. Wording condensed from §5.9, §2.8.5 and C.3.
#import "kit.typ": *
#let head = (14, "5", "Conditions", "§ 5.9 · § 2.8.5 · C.3")
#let W = (84pt, 1.55fr, 1fr)
#let A = ("key", "text", "text")
#let H = ("Condition", "Effect", "Ends")
#let next = [End of their next activation, or a rule removes it.]

#side(..head, face: "front")[
  #grid(columns: (1fr, 1fr), column-gutter: 18pt,
  [
    #aside-head(seed: 1)[Stacking]
    Same-named conditions don't stack. A second copy keeps the longer duration, or the higher number; otherwise the existing one stays unless the new rule replaces it.
  ],
  [
    #aside-head(seed: 3)[Recovery Immunity]
    When a condition from an enemy effect ends, the combatant is *Immune* to it from enemies until the end of their next activation. Never for Hidden, Invisible, Prone or Knocked Out, nor self-applied conditions.
  ])
  #v(10pt)
  #aid-table(W, A, H, (
    ([Bleeding], [At the end of their activation, lose 2 HP. AV, AD, Resistance and Immune cannot reduce it.], [They regain HP, receive successful Bandages, or a rule removes it.]),
    ([Blinded], [No LOS beyond 2″. Attack damage rolls and sight-based Checks with Disadvantage.], next),
    ([Burning], [1 fire damage at the end of each round.], [Spend 1 AP in their activation to put it out, enter water, or a rule removes it.]),
    ([Cursed], [Cannot regain HP, except an Injuries Table result that sets HP (which does not end Bleeding).], [End of the adventure, or Purify, a Potion of Remove Curse or similar.]),
    ([Frightened], [Cannot willingly move closer to the source while it is in LOS. Attack damage rolls and Checks against the source with Disadvantage.], next),
    ([Hidden], [Cannot be targeted by anything that needs LOS; does not block LOS. Areas still affect them. First attack, harmful Power or Special Ability: base dice with Advantage, else their Check with Advantage, else the target's Check with Disadvantage. Enemies may move through, not stop on, their space; doing so ends Hidden.], [After that first harmful act; or they take damage, become Engaged, an enemy within Hide distance (2″) has LOS, an enemy with LOS has them out of Cover, an enemy Spots them, they Push or Trip, or a rule removes it.]),
    ([Immobilized], [Speed 0″. Cannot Move, Shift, Climb or Jump.], next),
    ([Invisible], [LOS-based effects cannot target them unless adjacent or able to ignore Invisible (Reach alone is not enough). Areas still affect them. Adjacent attacks: base dice with Disadvantage. Governs targeting over Hidden.], [After the first attack, harmful Power or Special Ability, Push or Trip resolves, unless the effect says otherwise.]),
  ), title: [Conditions A–I], size: 10.5pt)
]

#side(..head, face: "back", art: "ART-MON-NIGHT-HAG", art-w: 96pt)[
  #aid-table(W, A, H, (
    ([Knocked Out], [At 0 HP. Cannot activate, act, move by choice, attack, use Powers or Special Abilities, or react. Stays Prone. Never Engaged; makes no one Engaged (Player Aid 4).], [HP restored above 0.]),
    ([Poisoned \[dX\]], [At the end of their next activation, suffer the listed poison damage.], [After that damage, or Antitoxin, or a rule removing Poisoned or poison.]),
    ([Prone], [Melee attacks against them: base dice with Advantage. Ranged weapon attacks from over 2″: Disadvantage. Cannot Block or Parry.], [Stand (1 AP); a Monster starts its activation; or a rule removes it.]),
    ([Silenced], [Cannot cast Powers or use a Special Ability that needs speech, chanting or invocation.], next),
    ([Sleeping], [Falls Prone. Cannot act, move by choice, attack, use Powers or Special Abilities, or react. Melee attacks against them roll 1 extra base die. May activate at 0 AP only to end it.], [On taking damage or losing HP; an adjacent ally's Interact (1 AP), never an enemy's; or the end of their next activation.]),
    ([Slowed], [Speed above 0″ is halved, minimum 1″.], next),
    ([Stunned], [Cannot act, move by choice, attack, use Powers or Special Abilities, or react. May activate at 0 AP only to end it.], next),
    ([Weakened], [Attack damage rolls with Disadvantage.], next),
    ([Heard the Song], [−1 SPI (The Voice Beneath the Bells).], [Quiet the Bells (1 TAP) at the Chapel in the Town Phase.]),
  ), title: [Conditions K–Z], size: 10.5pt)
  #v(6pt)
  #grid(columns: (1fr, 112pt), column-gutter: 14pt,
  [
    #aside-head(seed: 5, size: 16pt)[Negative Conditions]
    Rules that remove or prevent a *negative condition* mean only: Bleeding, Blinded, Burning, Cursed, Frightened, Immobilized, Poisoned \[dX\], Prone, Silenced, Sleeping, Slowed, Stunned, Weakened. Hidden, Invisible, Knocked Out and Wounds are not negative conditions.
  ], [])
]
