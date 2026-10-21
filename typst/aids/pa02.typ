// PA-2 Monster AI. Wording condensed from §9.3–9.6, §3.4, §9.7 (Bosses) and C.8.
#import "kit.typ": *
#let head = (9, "2", "Monster AI", "§ 9.3–9.5 · § 3.4 · C.8")

#side(..head, face: "front", art: "ART-MON-MINOTAUR", art-w: 100pt)[
  #flow(gap: 12pt, min-link: 28pt,
    start: [#text(font: goth, weight: 700, size: 15pt)[Each Monster activates] #h(6pt)
      Remove Prone. Pick the *Primary Target* (printed Target Priority first). Roll for spent Recharge abilities. Resolve start-of-activation Special Abilities.],
    rows: (
      (1, [Any AI Step valid?], [Resolve the *first* valid one, lowest number first. *on d6 N+:* roll 1d6, need N or higher. #h(1fr) #text(size: 9.5pt)[_Says it continues? Go to step 2._]]),
      (2, [Engaged?], [Attack the Engaged enemy with the *lowest current HP*. Use Multi-Attack if listed; otherwise melee, or ranged if it has no melee attack.]),
      (3, [Enemy visible?], [Move toward the Primary Target; attack if Engaged on arrival. *Ranged, and able to fire without becoming Engaged:* move to the nearest legal firing position, then attack. *Knocked Out target:* stop within melee distance and attack.]),
      (4, [Hidden enemy within 12″ and LOS?], [*Search:* the nearest one's controller makes a DEX Check. On a failure, that enemy is no longer Hidden.]),
    ),
    end: (5, [Move toward the Guard Point, objective, patrol route, or scenario destination.]))
  #v(6pt)
  #grid(columns: (1fr, 1fr, 1fr), column-gutter: 18pt,
  [
    #aside-head(seed: 1)[Primary Target]
    The *nearest visible enemy*: in perception range (12″, or a sense's range) and LOS. Hidden and Invisible enemies don't count unless a rule says so. Re-pick if it stops being legal.
    #v(4pt)
    #caps[Ties, in order]
    #steps[Lowest current HP][Last to damage this Monster][Random Determination]
  ],
  [
    #aside-head(seed: 3)[Movement]
    #steps[Shortest legal route][Tied routes: avoid hazards][End nearest to attack or threaten]
    #v(6pt)
    #aside-head(seed: 7)[Never]
    No AP, NRG, or Reactions. Effects that call for a Check apply unless Immune; Terrain Checks always succeed.
  ],
  [
    #aside-head(seed: 5)[Blocked Route]
    Can't reach and attack the Primary Target? Switch to the nearest visible enemy it can. None: move full Speed toward the target (or a firing position); no attack.
  ])
]

#side(..head, face: "back")[
  #grid(columns: (1fr, 1fr), column-gutter: 20pt,
  [
    #aside-head(seed: 2)[The Monster Phase]
    #stage(1, [Wake-up])[Check every Resting Group against the wake-up triggers and any scenario rule.]
    #vlink(h: 18pt)
    #stage(2, [Groups in order])[Each *Awake* Group activates in ascending Group number. Players never choose, delay, skip, or reorder Groups.]
    #vlink(h: 18pt)
    #stage(3, [Monsters in a Group])[No order set? Pick the next Monster by Random Determination. Resolve its activation completely, then repeat.]
    #v(9pt)
    *Woken mid-phase:* the Group joins the remaining order. If its place has passed, it goes next after the current Group or effect. Ties: ascending number.
    #gap-v
    #aside-head(seed: 4)[Wake-up Triggers]
    A *Resting* Group does not activate. It wakes, and stays Awake for the adventure, when:
    #dot[an enemy moves within *6″* (no LOS needed);]
    #dot[a visible enemy enters its LOS within *12″*;]
    #dot[the Group suffers damage;]
    #dot[an Explosion, collapsing terrain, or a loud effect occurs within *6″*;]
    #dot[a scenario rule wakes it.]
    #v(4pt)
    Measure from any Monster in the Group. A Hidden enemy trips the 6″ trigger only within its Hide distance, and stays Hidden. Hidden or Invisible enemies trip the 12″ trigger only if a rule makes them visible.
  ],
  [
    #aside-head(seed: 6)[Setup]
    Unless the scenario says otherwise, each Group starts *Resting*, within *3″* of its starting point, with a *Guard Point*: the nearest scenario landmark, else the nearest designated major terrain, else its start. Ties: random.
    #gap-v
    #aside-head(seed: 8)[Allegiance]
    Neutral Groups are allied to each other and hostile to every party. They never target, engage, or wake because of allied Monsters. *Hostile to all:* every other combatant is an enemy, except its own Group.
    #gap-v
    #aside-head(seed: 9)[Bosses]
    Unless the scenario says otherwise, start *Awake* and use *Relentless Assault*, not the Monster Phase: after each hostile Hero's activation, the Boss takes 1 activation. A Hero left at 0 AP by a Reaction before activating triggers it after the current activation or effect. At most one per starting hostile Hero each round. AI Steps and start-of-activation abilities only on the first activation each round; every attack step uses the full Multi-Attack. *Immune* to Stunned, Sleeping, Immobilized, Silenced, and Frightened; an enemy effect that would make it Stunned, Sleeping, or Immobilized, set its Speed to 0″, skip or end its activation, stop its attacks, control it, or remove it without 0 HP instead blocks its AI Steps and gives Disadvantage to its first attack damage roll, until the end of its next activation. Forced movement works normally.
    #gap-v
    #aside-head(seed: 10)[Areas]
    Origin in LOS. Cover the most enemies, then the fewest allies, then include the Primary Target; then random.
    #gap-v
    #aside-head(seed: 11)[Powers and AP]
    A Monster ignores AP loss, gain, or costs. Instead, next activation: no AI Steps, and its first attack damage roll has Disadvantage, unless the rule gives a specific Monster result. Casting a Power at a Monster whose LVL exceeds the caster's Level: Disadvantage on the Casting Check.
  ])
]
