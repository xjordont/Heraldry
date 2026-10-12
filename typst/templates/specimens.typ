// Template specimens: one page per page type, set with real RC492 manuscript excerpts, approved art
// and the real vector figures. Rendered to PNG by tools/render_template_specimens.py, never to a
// book PDF. Text is copied verbatim; an excerpt may stop at a boundary, and that is the only editing.
#import "system.typ": *
#set smartquote(enabled: false)
#show: base

#let art(id) = "../../assets/art/ink/" + id + ".png"
#let fig(id) = "../../figures/out/" + id + ".svg"

// ================================================================ 1. title page (recto i)
#shell(1, furniture: false, folio-on: false)[
  #v(0.15in)
  #align(center)[
    #text(font: sans, weight: 700, size: 9pt, tracking: 0.5em)[A SKIRMISH GAME OF THE DYING LANDS]
    #v(10pt)
    #text(font: goth, weight: 700, size: 72pt)[Heraldry]
    #v(-30pt)
    #text(font: goth, weight: 500, size: 30pt)[Skirmish]
    #v(-6pt)
    #flourish(len: 110pt)
    #v(10pt)
    #image(art("ART-COVER-002"), width: 100%)
    #v(12pt)
    #text(font: fell, size: 13pt, fill: ink2)[Rules for desperate expeditions, brutal clashes, and hard-won survival]
    #v(1fr)
    #text(font: sans, weight: 600, size: 8pt, tracking: 0.3em, fill: ink2)[RULEBOOK · RELEASE CANDIDATE 492]
  ]
]

// ================================================================ 2. contents (verso iv)
#shell(4, furniture: false)[
  #align(center)[#text(font: goth, weight: 600, size: 42pt)[Contents] #v(-12pt) #flourish(len: 80pt)]
  #v(14pt)
  #columns(2, gutter: gap)[
    #toc-chapter("1", "The World of Heraldry", 9, n: 1)
    #toc-line("1.1", "What is Heraldry Skirmish?", 9)
    #toc-line("1.2", "The Grim World", 11)
    #toc-line("1.3", "The Dying Lands", 13)
    #toc-line("1.4", "What You Need to Play", 17)
    #toc-line("1.5", "Goals of the Game", 18)
    #toc-line("1.6", "Rules Hierarchy and Precedence", 19)
    #toc-chapter("2", "Core Mechanics", 21, n: 2)
    #toc-line("2.1", "Core Terms", 21)
    #toc-line("2.2", "Ability Scores", 23)
    #toc-line("2.3", "Ability Checks", 24)
    #toc-line("2.4", "Advantages and Disadvantages", 25)
    #toc-line("2.5", "Action Points and Summons", 26)
    #toc-line("2.6", "Measurement, Size, Distances, and Rounding", 27)
    #toc-line("2.7", "Line of Sight and Areas of Effect", 31)
    #toc-line("2.8", "Cover, Light, Hidden, and Visibility", 35)
    #toc-line("2.9", "Terrain", 38)
    #toc-line("2.10", "Luck Points", 42)
    #toc-chapter("3", "The Game Round", 45, n: 3)
    #toc-line("3.1", "Overview of a Round", 45)
    #toc-line("3.2", "Initiative Phase", 46)
    #toc-line("3.3", "Party Phase", 48)
    #toc-line("3.4", "Monster Phase", 50)
    #toc-line("3.5", "End of Round", 51)
    #toc-line("3.6", "Timing Rules", 52)
    #colbreak()
    #toc-chapter("9", "Monsters", 287, n: 9)
    #toc-line("9.1", "Monster Stat Profile", 287)
    #toc-line("9.2", "Determining Monsters for an Adventure", 289)
    #toc-line("9.3", "Monster Placement and Initial State", 291)
    #toc-line("9.4", "Monster Waking and Activation State", 292)
    #toc-line("9.5", "Universal Monster AI Principles", 294)
    #toc-line("9.6", "Universal Special Abilities (SA) List", 299)
    #toc-line("9.7", "The Bestiary", 303)
    #toc-line("9.8", "Random Monster Generation Tables", 363)
    #toc-chapter("10", "Scenarios", 371, n: 10)
    #toc-line("10.1", "Adventure Preparation Sequence", 373)
    #toc-line("10.2", "Secondary Objectives by Climate", 379)
    #toc-line("10.3", "Weather Tables by Climate", 385)
    #toc-line("10.4", "Core Scenario Outlines", 389)
    #toc-line("10.5", "Solo and Cooperative Play", 463)
    #toc-line("10.6", "Dynamic Party and Scenario Scaling", 467)
    #toc-chapter("A", "Learn to Play", 521, n: 12)
    #toc-chapter("B", "Basic Mode", 545, n: 13)
    #toc-chapter("C", "Rules Reference", 561, n: 14)
    #v(8pt)
    #text(font: sans, size: 7.6pt, fill: ink3)[Specimen: page numbers are placeholders until the book is paginated.]
  ]
]

// ================================================================ 3. chapter opener (recto)
#shell(9, tab: 1, furniture: false, frame: true)[
  #chapter-opener("One", "The World of Heraldry", n: 1, art: art("ART-CH01-002"),
    lead: [Banners rot in the rain. Shrines sink into the mud. Oaths are broken, kings are buried, and the roads between settlements grow more dangerous with each passing season. Yet the ruins of the world still glitter with coin, relics, and forgotten power, and the desperate, the devout, the greedy, and the doomed continue to march into darkness to claim them.])
  #section("1.1", "What is Heraldry Skirmish?")
  #columns(2, gutter: gap)[
    #dropcap[*Heraldry Skirmish* is a competitive GM-less PvPvE fantasy tabletop miniatures game of desperate expeditions, brutal clashes, and hard-won survival. Most battles pit two rival adventuring parties against one another as they race through monster-haunted ruins, damned wilderness, and blood-soaked strongholds in search of treasure, glory, and escape.]

    A standard competitive game uses *4 Heroes per side* on a *36"×36"* battlefield. It is usually played by *2 players*, but supports *2–8 players* by dividing control of each side's Heroes among allied players.
  ]
]

// ================================================================ 4. ordinary rules (verso)
#shell(28, chapter: "Core Mechanics", section: "2.6 Measurement", tab: 2)[
  #section("2.6", "Measurement, Size, Distances, and Rounding")
  #columns(2, gutter: gap)[
    You may measure any distance or check *LOS* at any time.

    Heraldry Skirmish is played on a *36"×36"* battlefield unless a scenario says otherwise.

    #runin[Tabletop Mode:][Measure distances in inches between the closest points of the source and target spaces. If a rule measures from or to an origin point, target point, or other point, use that point.]

    #runin[Grid Mode:][Use a *36"×36"* battle map marked in *1"* squares. A combatant occupies the squares listed by their *Sz* footprint. A marker, token, hazard, or terrain feature occupies every square whose centre lies under it, rounded outward at ties.]

    Each orthogonal square of movement or distance counts as *1"*, and each diagonal square counts as *1.5"*, unless a rule says otherwise. For range and other non-movement distances, count the shortest grid distance without counting the source square. Obstacles do not change this distance unless a rule says otherwise; check *LOS*, *Cover*, and terrain separately.

    Track movement and distance in *0.5"* increments. Do not round a *1.5"* diagonal or a combatant's remaining movement.

    #example[In *Grid Mode*, a Hero with *Speed 5"* takes a *Move* action. They enter one orthogonal square for *1"*, then two diagonal squares for *1.5"* each, spending *4"* in total. With *1"* of movement remaining, they may enter one more orthogonal square, but they cannot enter another diagonal square, because its *1.5"* cost exceeds their remaining movement.]

    If a source or target occupies more than one square, check each source-square and target-square pair. When range, *LOS*, and *Cover* apply to the same target or effect, one pair must satisfy all requirements. If more than one pair does, use the pair that grants the target the least *Cover*. If *Cover* is tied, use the shortest range. For a distance that does not also require *LOS* or *Cover*, use the closest occupied squares.

    If a rule measures from or to a point, marker, hazard, or terrain feature, use the square containing it unless the rule says otherwise.

    #subsection("2.5.1", "Summon Limits")
    A party's limit is *2 allied Summons* in play.

    If a rule would create a third allied Summon for that party, create the Summon, then immediately choose one allied Summon in that party to be dispelled and removed from play. Resolve the new Summon's "when summoned" effects only if the new Summon remains in play.

    #note-box[If more than one player controls that party, the player exercising *Party Leader* authority chooses which allied Summon is dispelled.]

    Enemy, neutral, and Monster-created Summons do not count against a party's allied Summon limit unless a rule says otherwise.
  ]
]

// ================================================================ 5. rules with a full-width figure (recto)
#shell(33, chapter: "Core Mechanics", section: "2.7 Line of Sight and Areas of Effect", tab: 2)[
  #figure-block("FIG-07", "Line of sight, Cover and Blocking Terrain", fig("FIG-07"),
    [Blocking Terrain, a corner shared by two Blocking squares and the interior of Cover Terrain block LOS. Touching only a Cover Terrain corner, an intervening combatant and Impassable Terrain leave LOS clear and give the target Cover (Impassable Terrain unless its terrain entry says otherwise); a Shift of 1 AP clear of the line removes the combatant's Cover (see 2.7.2 and 2.8.4).])
  #columns(2, gutter: gap)[
    #example(title: "Cover from an ally")[A Ranger has clear *LOS* to a Skeleton Warrior, but the sight line crosses their own Fighter. The Skeleton Warrior has *Cover*, so the Ranger rolls their base damage dice with *Disadvantage*. The Fighter is not a target and suffers nothing. If the Ranger first spends *1 AP* to *Shift* clear of the sight line, no *Cover* applies.]
    #colbreak()
    #procedure(title: "Specimen: procedure component", (
      [Roll *1d20 + Party Leader's INT + Party Leader's SPI* for each side.],
      [The higher total wins *Initiative* and chooses to act first or second.],
      [A Power that lasts until the start of the round ends after Initiative is determined.],
    ))
    #text(font: sans, size: 7.4pt, fill: ink3)[The steps above illustrate the component only; the book sets each procedure exactly as its source section lists it.]
  ]
]

// ================================================================ 6. tables (verso)
#shell(386, chapter: "Scenarios", section: "10.3 Weather Tables by Climate", tab: 10)[
  #ref-table((0.42in, 1.35in, 1fr), ("roll", "key", "text"), ("1d6", "Weather Condition", "Effect"),
    title: "Climate 1: Greenmark Weather Table", (
    ([1], [*Blackwater Deluge*], [*LOS* is reduced to 6". Every area of *Open Terrain* and *Cover Terrain* that is not explicitly "Indoors" or "Rocky" becomes *Difficult Terrain*; *Impassable Terrain* and *Blocking Terrain* are unchanged. At the end of their activation, each combatant that is not in *Cover* must pass a *STR Check* or suffer *1 HP loss*.]),
    ([2], [*Heavy Rain and Mud*], [Every area of *Open Terrain* and *Cover Terrain* that is not explicitly "Indoors" or "Rocky" becomes *Difficult Terrain*; *Impassable Terrain* and *Blocking Terrain* are unchanged. Ranged attacks targeting beyond 10" roll their base damage dice with *Disadvantage*.]),
    ([3], [*Thick Morning Fog*], [The battlefield starts in *Light*. Fog covers the battlefield and provides *Cover* in every space.]),
    ([4], [*Strong Gusting Winds*], [All ranged weapon attacks suffer a -1 penalty to their final damage total. Powers are unaffected. Combatants using *Fly (X")* movement from any source treat all air as *Difficult Terrain*. At the end of each round, roll *1d6* for each such combatant that is not on a surface. On a *1–3*, *Slide* them *1"* using *Random Direction* in *10.1*.]),
    ([5], [*Intermittent Showers*], [At the start of each round, roll 1d6. On a 1–2, the Heavy Rain and Mud effects apply for this round. On a 3–6, no adverse weather effect applies this round.]),
    ([6], [*Dappled Sunlight*], [Shifting light and shade play across the forest floor. No adverse weather effects apply. Standard conditions apply.]),
  ))
  #ref-table((1fr, 0.62in, 0.55in, 0.6in, 0.6in, 0.95in, 1.65in), ("key", "c", "c", "c", "c", "c", "text"),
    ("Weapon", [COST #coin(s: 7pt, fill: paper)], "Hands", "STR Req", "DEX Req", "Damage", "Traits"),
    title: "7.8 Melee Weapons (excerpt)", (
    ([Unarmed Combat], [0], [2], [-], [-], [1 (B)], [*Trip*]),
    ([Club], [0], [1], [-], [-], [1d4 (B)], [-]),
    ([Mace], [2], [1], [2], [-], [1d6 (B)], [*Parrying*]),
    ([Morningstar], [6], [1], [2], [-], [1d8 (B)], [*Deadly*]),
    ([Flail], [10], [1], [3], [-], [1d8 (B)], [*Sweep*, *Trip*]),
    ([War Maul], [24], [2], [4], [-], [1d12 (B)], [*Fatal*, *Heavy*]),
    ([Greathammer], [30], [2], [5], [-], [1d12+1 (B)], [*Fatal*, *Heavy*]),
    ([Dagger], [1], [1], [-], [-], [1d4 (P)], [*Agile*, *Finesse*, *Light*]),
    ([Stiletto], [2], [1], [1], [2], [1d4 (P)], [*Deadly*, *Finesse*, *Light*]),
    ([Shortsword], [5], [1], [2], [1], [1d6 (S)], [*Light*, *Parrying*]),
    ([Rapier], [8], [1], [-], [3], [1d8 (P)], [*Agile*, *Finesse*, *Parrying*]),
    ([Estoc], [19], [1/2], [3], [2], [1d8/1d10 (P)], [*Fatal*, *Finesse*, *Versatile*]),
  ))
]

// ================================================================ 7. hero class (recto)
#shell(155, chapter: "Your Adventuring Party", section: "6.13 Hero Classes", tab: 6)[
  #character-entry("Fighter", "Hero Class", "1/5 Complexity", art: art("ART-CLA-FIGHTER"),
    [A Fighter is forged in places where hesitation gets people killed. Drill, repetition, and hard lessons carve in the instinct to hold ground when holding it is the only thing that matters. They have watched lines collapse, and they know to the heartbeat how long one can stand before it does.],
    (("Archetype", [Martial]), ("Class Modifiers", [STR +2, DEX +1, INT 0, SPI -1]), ("Starting HP Bonus", [+5]),
     ("Max HP Gained per Level", [+3]), ("Primary Casting Score", [None]), ("NRG Pool", [None])))[
    #columns(2, gutter: gap)[
      #label-rule("Starting Packages")
      - *A. Vanguard (Defensive):* Shortsword, Targe, Ring Shirt, Dagger.
      - *B. Ravager (Offensive):* Great Falchion, Ring Shirt, Javelin, Bandages.
      - *C. Duelist (Flexible):* Main-Gauche, Leather Coat, Healer's Kit, Bandages, Rope, 4c.
      #minor("Novice Fighter Talents")
      - *Combat Mastery:* Your second weapon attack during your activation does not suffer *Disadvantage* from the *Multiple Attacks* rule. Later attacks resolve normally.
      - *Shield Drill:* While you are equipped with a shield, you gain *+1 AV* against melee weapon attacks.
      - *Duelist's Riposte:* When you declare *Parry*, you may spend *1 additional AP*. If the *Parry* succeeds, make one melee weapon attack against the attacker after resolving any normal *Riposte*. This attack does not count toward the multi-attack *Disadvantage* chain.
      #colbreak()
      #minor("Adept Fighter Talents")
      - *Guard Break:* Reduce the *AV* an enemy applies against your melee weapon attack by *1*. When an enemy uses *Parry* against your melee weapon attack, reduce their parry total by *1*.
      - *Relentless:* When you succeed on *Push* or *Trip*, you may make one melee weapon attack against the same target for *0 AP*. The bonus attack counts toward the multi-attack *Disadvantage* chain.
      - *Iron Discipline [1 AP Reaction]:* *Trigger:* You fail a *STR*, *DEX*, or *SPI Check* that was not made as part of another Reaction. *Effect:* Reroll that *Check*. You must use the new result.
      - *Spiked Armour:* While equipped with Chest armour, after an adjacent enemy's attack resolves, that enemy loses *1 HP* if the attack damaged you, or if you successfully used *Parry* against it.
      #minor("Master Fighter Talents")
      - *War Master:* Your melee weapon attacks do not suffer *Disadvantage* from the *Multiple Attacks* rule.
    ]
  ]
]

// ================================================================ 8. powers (verso)
#shell(216, chapter: "Powers and Traditions", section: "8.3 Arcane Spells", tab: 8)[
  #section("8.3", "Arcane Spells")
  #columns(2, gutter: gap)[
    Arcane Core Rules:
    - Arcane Spells follow *8.2 Casting Powers*.
    - Arcane Spells may use their printed *Empower* options.
    #tier-head("Tier 0 Arcane Cantrips: Wizard")
    #power(1, "Arcane Dart", "1 AP · 0 NRG", (("Range", [12"]), ("Target", [1 combatant])),
      [*Effect:* Deal *1d4 arcane damage*.\ *Critical Cast:* You may immediately *Shift 1"*.])
    #power(2, "Mage Hand", "1 AP · 0 NRG", (("Range", [8"]), ("Target", [1 unsecured object, unlocked door, lever, latch, or similar small interactable element])),
      [*Effect:* *Interact* with the target within *8"*. This can open or close an unlocked door, pull a lever, lift or place one unsecured object, or perform a similar *Interact* effect at range. This can never deal damage, make an attack, or complete an objective unless that objective explicitly allows *Mage Hand*.])
    #power(3, "Spark Ward", "1 AP · 0 NRG", (("Range", [Self]), ("Target", [Self])),
      [*Effect:* Add *+3 AV* the next time you apply *AV* this round.])
    #colbreak()
    #tier-head("Tier 0 Arcane Cantrips: Trickster")
    #power(1, "Glamour Shard", "1 AP · 0 NRG", (("Range", [2"]), ("Target", [1 combatant])),
      [*Effect:* Deal *1d6 + INT arcane damage* and then *Shift 2"*.])
    #power(2, "False Footing", "1 AP · 0 NRG", (("Range", [2"]), ("Target", [1 enemy in *LOS*])),
      [*Effect:* The target must pass a *DEX Check* or become *Prone*.])
    #v(10pt)
    #text(font: sans, size: 7.4pt, fill: ink3)[In the manuscript the cost reads *[1 AP, 0 NRG]*; the book keeps the text exactly and only sets it in the black cost tag.]
  ]
]

// ================================================================ 9. bestiary (recto)
#shell(305, chapter: "Monsters", section: "9.7 The Bestiary · The Pale City", tab: 9)[
  #columns(2, gutter: gap)[
    #monster("Fallen Paladin", "Elite", art: art("ART-MON-FALLEN-PALADIN"),
      [Holy oath turned to grave-frost, the fallen paladin is an undead knight in defiled plate, radiating an aura that withers the courage of all who come near. Its flamberge carries a necrotic chill, and despair leaks off it the way cold leaks off ice. It guards the Pale City's blackest chapels. Whatever vow it broke in life, it keeps a darker one now.],
      ("HP", "AV", "SPD", "LVL", "CV", "Sz"), ("45", "3", "5\"", "6", [36#h(1.5pt)#coin(s: 8pt)], "M"),
      (("AI Steps", ([*Oathbreaker's Charge (AI Step 1):* Moves their full Speed toward the nearest visible enemy, then attacks; the *Aura of Despair* affects every enemy they pass within *4"* of during this move.],)),
       ("Attacks", ([*Defiled Flamberge:* 1d12 + 5 slashing damage + 1d6 necrotic damage.],)),
       ("Special Abilities", (
         [*Undead:* *Immune* to *Poisoned [dX]*, *Bleeding*, *Frightened*, and *Sleeping*.],
         [*Stalwart:* This *Monster* ignores *Critical Hit* effects from melee attackers.],
         [*Aura of Despair:* An enemy that starts their activation within *4"* must pass a *SPI Check* or become *Weakened* until the end of the round.],
         [*Resistant:* necrotic, ice. #h(4pt) *Vulnerable:* holy. #h(4pt) *Darkvision (9").*],
       ))))
    #colbreak()
    #monster("Werebear", "Brute", art: art("ART-MON-WEREBEAR"),
      [In the Pale City's frozen wilds prowls the werebear, a hulking man-beast of white fur and ruinous strength, damned kin to the werewolf but built to maul rather than skirmish. It strikes with both paws and a bone-cracking bite, and hurls grown men aside. Mundane weapons barely part its hide. A single one can break a war-band.],
      ("HP", "AV", "SPD", "LVL", "CV", "Sz"), ("40", "3", "6\"", "6", [31#h(1.5pt)#coin(s: 8pt)], "L"),
      (("Attacks", (
         [*Multi-Attack:* Makes two *Claws* attacks and one *Bite* attack during their attack step.],
         [*Claws:* 1d10 slashing damage.],
         [*Bite:* 1d12 piercing damage. When this attack damages a target, *Push* that target *2"* directly away.],)),
       ("Special Abilities", (
         [*Lycanthrope:* This *Monster* is *Resistant* to non-magical, non-silvered weapon damage. *Holy* damage ignores this *Resistance*.],
         [*Keen Senses (9").*],))))
  ]
]

// ================================================================ 10. scenario opening (recto)
#shell(431, chapter: "Scenarios", section: "10.4 Core Scenario Outlines · The Pale City", tab: 10)[
  #scenario-head("Pale City 2", "The Alchemist's Frozen Laboratory",
    [In the ice-locked Silent District, north along the road out of Hearthhold, an alchemist's laboratory remains sealed under frost. The formula inside might be worth a village, and Hearthhold burns through everything it owns just to stay warm. The cold has preserved the benches, the bottles, the last mistakes, and the guardians left to watch them. Some things in that laboratory were never meant to thaw.])
  #columns(2, gutter: gap)[
    #dossier((
      ("Primary Objective", [Be the party to secure the most Alchemical Reagents and escape with them.]),
      ("Final Random Monster Groups", [Determine using *10.6.4*.]),
      ("Awake Groups", [Random Monster Groups begin *Resting* unless a listed setup rule says otherwise. Scenario-specific Monsters use their listed state.]),
      ("Minion Swarm", [No.]),
      ("Objective Scaling", [Apply *10.6.9* to the Alchemical Reagent Chests.]),
      ("Pressure Clock", [Use *Collapse* from *10.5.7*.]),
      ("Party Deployment", [Parties deploy on opposite short battlefield edges, within *6"* of their edge.]),
    ))
    #runin[Battlefield and Terrain (36"×36"):][Represent a frozen city block with 6–7 ruined, ice-covered building footprints, one of which is the Laboratory (about 6"×8"). Scatter 4–6 Ice Barricades (*Impassable Terrain*) and Frozen Debris markers (*Cover Terrain* tagged *Difficult Terrain*) in any combination. The exposed ground is *Slippery Terrain*.]
    #colbreak()
    #figure-block("FIG-40", "Deployment map", fig("FIG-40"),
      [The Alchemist's Frozen Laboratory: parties deploy within 6" of opposite short edges; the Laboratory, about 6"×8", holds three Reagent Chests and the Alchemical Golem; key: FIG-20 (see 10.4, Pale City Scenario 2).])
    #block(above: 4pt, below: 0pt)[#text(font: goth, weight: 600, size: 15pt)[Scenario-Specific Monster: Alchemical Golem]]
    #stat-card(("HP", "AV", "SPD", "LVL", "CV", "Sz"),
      ([(5 × Party Size × (4 + (1 × APL))) / 8], [2 + (APL/3, rounded down)], [4"], [APL + 1 (min 3, max 7)], [2 × (2 + (4 × APL)) Coins], [M]))
  ]
]

// ================================================================ 10b. gazetteer (recto)
#shell(15, chapter: "The World of Heraldry", section: "1.3 The Dying Lands · The Bastions", tab: 1)[
  #gazetteer("Deepwarden", "Bastion", art: art("ART-BAS-DEEPWARDEN"))[
    *Deepwarden* is a sealed mining city carved into the foothills of the broken mountains. It survived the Fall by closing its great gate. Half the city was on the wrong side when it closed. The half that survived now lives in the upper terraces above what its people call simply *the Dark*.

    Deepwarden is governed by the *Lantern Council*: mine masters, tunnel-priests, and forge-captains who meet in chambers without doors that can be barred from the outside. Each Council member carries a lantern of consecrated flame. A Council member whose lantern goes dark is considered to have resigned.

    Deepwarden controls the best forges in the surviving world. It pays for that monopoly with hunger for grain, labour, timber, and safe routes to the other Bastions, none of which it fully trusts. Adventurers find work here readily. Most contracts include a clause explaining what to do if the contractor begins speaking in a voice that does not belong to them.
  ]
]

// ================================================================ 11. quick reference (verso)
#shell(566, chapter: "Rules Reference", section: "C.3 Conditions Summary", tab: 14)[
  #qref-head("C.3", "Conditions Summary")
  #ref-table((1in, 1fr, 2in), ("key", "text", "text"), ("Condition", "Effect", "Ends When"), size: 8.8pt, (
    ([*Bleeding*], [At the end of their activation, the combatant loses *2 HP*. This HP loss cannot be reduced by *AV*, *AD*, *Resistance*, or *Immune*.], [The combatant regains HP, receives successful *Bandages*, or a rule removes it.]),
    ([*Blinded*], [Cannot draw *LOS* beyond *2"*. Attack damage rolls and sight-based *Checks* are made with *Disadvantage*.], [End of the affected combatant's next activation, or when a rule removes it.]),
    ([*Burning*], [Suffers *1 fire damage* at the end of each round.], [During their activation, the combatant spends *1 AP* to extinguish it; they enter water; or a rule removes it.]),
    ([*Cursed*], [Cannot regain HP by any means.], [End of the adventure, or when removed by *Purify*, a *Potion of Remove Curse*, or a similar effect.]),
    ([*Frightened*], [Cannot willingly move closer to the source while they are in *LOS*. Attack damage rolls and *Checks* against the source are made with *Disadvantage*.], [End of the affected combatant's next activation, or when a rule removes it.]),
    ([*Immobilized*], [Speed becomes *0"*. Cannot *Move*, *Shift*, *Climb*, or *Jump*.], [End of the affected combatant's next activation, or when a rule removes it.]),
    ([*Poisoned [dX]*], [At the end of the combatant's next activation, suffer the listed poison damage, then remove *Poisoned*.], [After the poison damage resolves, or earlier by *Antitoxin*, or by a rule that explicitly removes *Poisoned* or poison.]),
    ([*Silenced*], [Cannot cast Powers or use a Special Ability that explicitly requires speech, chanting, or invocation.], [End of the affected combatant's next activation, or when a rule removes it.]),
    ([*Slowed*], [If Speed is greater than *0"*, it is halved, rounded down to a minimum of *1"*.], [End of the affected combatant's next activation, or when a rule removes it.]),
  ))
  #text(font: sans, size: 7.4pt, fill: ink3)[Specimen excerpt: the book sets every row of C.3 in source order.]
]

// ================================================================ 12. index (recto)
#shell(597, chapter: "Index", section: "Index", tab: 15)[
  #align(center)[#text(font: goth, weight: 600, size: 38pt)[Index] #v(-10pt) #flourish(len: 60pt)]
  #v(6pt)
  #columns(3, gutter: 0.2in)[
    #index-letter("A")
    #index-entry("Ability Checks", "24")
    #index-entry("Ability Scores", "23")
    #index-entry("Action Points (AP)", "26, 61")
    #index-entry("Summons", "26", sub: true)
    #index-entry("Actions Summary", "568")
    #index-entry("Adventure Preparation Sequence", "373")
    #index-entry("Advantages and Disadvantages", "25")
    #index-entry("Areas of Effect", "33")
    #index-entry("Armour", "203")
    #index-entry("Attack Sequence", "84")
    #index-letter("B")
    #index-entry("Backgrounds", "137")
    #index-entry("Basic Mode", "545")
    #index-entry("Bastions", "13, 495")
    #index-entry("Bestiary", "303")
    #index-entry("Bleeding", "97, 566")
    #index-entry("Blinded", "97, 566")
    #index-entry("Burning", "97, 566")
    #index-letter("C")
    #index-entry("Campaign Cycle", "491")
    #index-entry("Casting Powers", "214")
    #index-entry("Conditions", "96")
    #index-entry("Conditions Summary", "566", sub: true)
    #index-entry("Core Terms", "21")
    #index-entry("Cover", "35")
    #index-entry("Critical Hits", "88")
    #index-entry("Cursed", "97, 566")
    #index-letter("D")
    #index-entry("Damage Types", "90")
    #index-entry("Darkvision", "300")
    #index-entry("Deployment", "377")
    #index-entry("Difficult Terrain", "39")
    #index-entry("Dodge", "73")
    #v(6pt)
    #text(font: sans, size: 7.2pt, fill: ink3)[Specimen: terms and pages are placeholders; the book's index is generated from tagged terms.]
  ]
]

// ================================================================ 13. back cover
#shell(600, furniture: false, folio-on: false)[
  #v(1.3in)
  #align(center)[
    #flourish(len: 90pt)
    #v(16pt)
    #block(width: 78%)[
      #set par(leading: 5pt, justify: false)
      #text(font: fell, size: 15pt)[Banners rot in the rain. Shrines sink into the mud. Oaths are broken, kings are buried, and the roads between settlements grow more dangerous with each passing season.]
    ]
    #v(18pt)
    #image(art("ART-MON-LICH"), width: 34%)
    #v(1fr)
    #text(font: goth, weight: 600, size: 26pt)[Heraldry Skirmish]
    #v(-8pt)
    #text(font: sans, weight: 600, size: 7.6pt, tracking: 0.3em, fill: ink2)[A SKIRMISH GAME OF THE DYING LANDS]
  ]
]

// ================================================================ 15. the armoury (design sheet)
#shell(601, furniture: false, folio-on: false)[
  #align(center)[#text(font: goth, weight: 600, size: 34pt)[The Armoury] #v(-10pt) #flourish(len: 70pt)]
  #v(8pt)
  #text(font: sans, weight: 700, size: 7.4pt, tracking: 0.16em)[THE ARMS OF THE FIFTEEN PARTS · ONE HERALDIC ORDINARY EACH]
  #v(4pt)
  #grid(columns: (1fr,) * 5, row-gutter: 14pt, column-gutter: 8pt,
    ..range(1, 16).map(i => align(center)[#arms(i, w: 34pt)#v(-2pt)#text(font: goth, weight: 600, size: 12pt, tab-keys.at(i - 1))\ #text(font: sans, size: 7pt, fill: ink3, ("Per pale", "Fess", "Bend", "Chevron", "Saltire", "Cross", "Pale", "Pile", "Per saltire", "Chief", "Bordure", "Quarterly", "Per bend", "Per fess", "Lozenge").at(i - 1))]))
  #v(14pt)
  #grid(columns: (1fr, 1fr, 1fr, 1fr), column-gutter: 10pt, align: center + bottom,
    [#crown(s: 46pt)\ #text(font: sans, size: 7.4pt)[Broken crown: the book's signature]],
    [#coin(s: 30pt)\ #text(font: sans, size: 7.4pt)[Coin: replaces the source's "c"]],
    [#shield(w: 30pt, inner: true, body: text(font: sans, weight: 700, size: 10pt, fill: paper)[2.6])\ #text(font: sans, size: 7.4pt)[Engraved shield: numbers]],
    [#box(width: 44pt, height: 44pt, corner("tl", s: 44pt))\ #text(font: sans, size: 7.4pt)[Corner flourish: panels]],
  )
  #v(14pt)
  #grid(columns: (1fr, 1fr), column-gutter: 20pt, row-gutter: 8pt,
    brush(weight: 2.4pt, seed: 3), text(font: sans, size: 7.4pt)[Brush rule: hand-inked, tapered; tables, sections, stat bars],
    tag[Example], text(font: sans, size: 7.4pt)[Banner tag: examples, notes, roles, scenarios],
  )
]
