// PA-3 Combat. Wording condensed from §5.1–5.7, §2.4.1, §4.5 and C.5–C.6.
#import "kit.typ": *
#let head = (5, "3", "Combat", "§ 5.1–5.7 · § 2.4.1 · § 4.5 · C.5–C.6")
#let dn = down(label: none, h: 16pt, x: 150pt)

#side(..head, face: "front", art: "ART-CLA-BERSERKER", art-w: 104pt)[
  #grid(columns: (322pt, 1fr), column-gutter: 18pt,
  [
    #aside-head(seed: 1)[The Attack Sequence]
    #stage(1, [Declare and verify])[Name attacker, attack, target and damage types. Confirm range, LOS, visibility, Cover and that the target is legal.]
    #dn
    #stage(2, [Declare Reactions])[Resolve redirection and verify again; an illegal attack fails. Then declare *every* Reaction and pay or commit its cost, *before any damage dice are rolled*.]
    #dn
    #stage(3, [Roll and build damage])[Roll base dice with Advantage or Disadvantage and any allowed rerolls. Find Total Miss and Critical Hit; roll exploding and other dice; add modifiers by type. *Luck* now rerolls the whole roll. Use only the final roll: a Total Miss ends the attack.]
    #dn
    #stage(4, [Defend and mitigate])[Resolve the declared Block, Dodge or Parry, then the *Mitigation Order*. No new Reactions.]
    #dn
    #stage(5, [Apply and finish])[Reduce HP by what remains. Then resolve Critical Hit riders, conditions and damage triggers.]
  ],
  [
    #aside-head(seed: 3)[The Dice]
    *Critical Hit:* any retained base die shows its maximum.
    #v(3pt)
    *Exploding:* each such die adds a bonus die of its type; a bonus die at maximum explodes again.
    #v(3pt)
    *Total Miss:* every retained base die is a natural 1. No damage; the attack ends.
    #v(3pt)
    #text(size: 9.5pt)[Only retained base dice count. Flat damage with no base dice cannot Crit or Total Miss.]
    #gap-v
    #aside-head(seed: 5)[Critical Riders]
    Primary damage type only (first listed).
    #dot[*Piercing:* ignores AV.]
    #dot[*Blunt:* halve total AV. Afterwards the target loses 1 AP; a Monster or a target with no AP becomes Prone instead.]
    #dot[*Slashing:* 1+ damage after mitigation: Bleeding.]
    #gap-v
    #aside-head(seed: 7)[Mitigation Order]
    #steps[Keep types apart. AV first (blunt, piercing, slashing only), then other flat mitigation in the defender's order; each once; minimum 0.][Immune, Resistant, Vulnerable per type.][Total and apply. Damaged only if 1+.]
  ])
]

#side(..head, face: "back")[
  #aid-table((84pt, 1fr, 1.25fr, 1.6fr), ("key", "text", "text", "text"), ("Reaction (1 AP)", "Trigger", "Effect", "Notes"), (
    ([Block], [Blunt, piercing or slashing damage would hit you; shield equipped.], [Roll the shield's AD and add its flat AV to your AV against that source.], []),
    ([Dodge], [An attack or harmful effect from another combatant would affect you.], [DEX Check (DEX counts up to +5). Success: the source has no effect on you. Natural 1: also Prone.], [Not against: sources that give you a Check avoiding all of it; recurring Aura, condition or delayed effects; hazards, terrain, weather, Falling; your own HP loss.]),
    ([Parry], [A blunt, piercing or slashing melee attack targets you; Parrying weapon.], [Roll its base dice plus normal attack modifier. Equal to or above the attack's total damage (before mitigation): take none of it.], [All natural 1s: fails and the attack ignores your AV. Success with a maximum die: the attacker takes a *Riposte* equal to the parry total (AV applies).]),
    ([Reflex Attack], [In an enemy's activation it leaves your melee distance with Move, or makes a ranged attack within it.], [One melee attack, base dice with Disadvantage.], [Not Shift, forced movement or ranged Reactions. Movement: resolve before it leaves. Ranged: declare before its damage; resolve right after it.]),
  ), title: [Reactions])
  #v(2pt)
  #grid(columns: (1fr, 1fr, 1fr), column-gutter: 16pt,
  [
    #aside-head(seed: 2, size: 16pt)[Reacting]
    #dot[Needs enough *unspent AP*.]
    #dot[Declare before the source's damage dice; pay then, even if it misses.]
    #dot[One Reaction per action or effect for each affected combatant.]
    #dot[Allowed in your own activation; it neither starts nor ends one.]
    #dot[Summons only if granted; Monsters never unless granted.]
    #gap-v
    #aside-head(seed: 6, size: 16pt)[Attacks]
    #dot[Each weapon attack costs 1 AP.]
    #dot[A Hero's or Hireling's 2nd and later weapon attack in one activation: base dice with *Disadvantage*. Reaction attacks don't count.]
    #dot[Add *STR* to melee, *DEX* to ranged and Finesse, the higher to Thrown; once per attack. Monsters add none.]
  ],
  [
    #aside-head(seed: 4, size: 16pt)[Damage and AV]
    #dot[AV stops only blunt, piercing and slashing.]
    #dot[Chest AD rolls automatically against those, plus flat AV. Shield AD and AV only with Block.]
    #dot[*Immune* 0; *Resistant* half; *Vulnerable* double; both cancel.]
    #dot[HP loss has no type and ignores AV and Resistance.]
    #dot[*Temporary HP* absorbs first; keep the higher; gone at End of Round or 0 HP.]
    #dot[*Engaged:* adjacent to an enemy that is not Knocked Out.]
  ],
  [
    #aside-head(seed: 8, size: 16pt)[Attack Modifiers]
    Base damage dice only.
    #v(4pt)
    #caps[Advantage]
    #dot[Attacker 2″+ higher]
    #dot[First qualifying attack while Hidden]
    #dot[Melee against a Prone target]
    #v(6pt)
    #caps[Disadvantage]
    #dot[Attacker Blinded or Weakened, or Frightened by the target]
    #dot[Attacker swimming in Deep Water]
    #dot[Target in Cover: ranged or thrown weapon, non-area ranged Power]
    #dot[Target Invisible and adjacent]
    #dot[Ranged against a Prone target over 2″ away]
    #dot[Reflex Attack; 2nd+ weapon attack in an activation]
  ])
]
