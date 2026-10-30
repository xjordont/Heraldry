// PA-10 Setup. Wording condensed from §10.1, §10.1.1 and §10.5.
#import "kit.typ": *
#let head = (10, "10", "Setup", "§ 10.1 · § 10.1.1 · § 10.5")

#let compass = box(width: 150pt, height: 150pt, {
  let c = 75pt
  let r = 46pt
  place(dx: c - r, dy: c - r, circle(radius: r, stroke: 1.2pt + ink, fill: tint))
  place(dx: c - r + 5pt, dy: c - r + 5pt, circle(radius: r - 5pt, stroke: 0.45pt + ink))
  let names = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
  for i in range(8) {
    let a = i * 45deg
    let long = if calc.even(i) { r + 6pt } else { r - 10pt }
    let tip = (c + long * calc.sin(a), c - long * calc.cos(a))
    let w = if calc.even(i) { 6pt } else { 4pt }
    let lft = (c + w * calc.sin(a - 90deg), c - w * calc.cos(a - 90deg))
    let rgt = (c + w * calc.sin(a + 90deg), c - w * calc.cos(a + 90deg))
    place(polygon(fill: if calc.even(i) { ink } else { ink3 }, tip, lft, (c, c), rgt))
    let lr = r + 20pt
    let lp = (c + lr * calc.sin(a), c - lr * calc.cos(a))
    place(dx: lp.at(0) - 14pt, dy: lp.at(1) - 9pt, box(width: 28pt, align(center,
      text(size: 9pt, weight: 800)[#str(i + 1) #text(weight: 600, fill: ink3, names.at(i))])))
  }
  place(dx: c - 7pt, dy: c - 8pt, shield(w: 14pt, inner: true))
})

#side(..head, face: "front", art: "ART-CLI-THE-GREENMARK", art-w: 190pt)[
  #grid(columns: (1.25fr, 1fr), column-gutter: 20pt,
  [
    #aside-head(seed: 1)[Preparation]
    #steps(
      [*APL:* find each party's Average Party Level.],
      [*Climate:* choose or roll 1d6 (back).],
      [*Core Scenario:* choose or roll 1d6 for that Climate.],
      [*Secondary Objectives:* roll or choose; record, don't place.],
      [*Weather:* roll or choose; record, don't place.],
      [*Setup Roll-off,* unless the scenario replaces it.],
      [*Terrain:* fix deployment zones (scenario silent: winner picks an edge, 6" deep, or an 8" × 8" corner; the other party takes the opposite). Place required terrain, then alternate the rest, Roll-off loser first. Alternately placed Impassable and Blocking Terrain stays out of deployment zones; Blocking pieces more than 2" apart.],
      [*Objectives and markers:* scenario, Secondary Objective, and Weather markers, outside deployment zones; alternate Weather markers, loser first.],
      [*Monsters:* generate and place the Groups.],
      [*Guard Points:* as the scenario directs, else the default.],
      [*Deploy:* alternate placing Heroes, Roll-off loser first, unless the scenario orders it.],
      [*Begin Round 1* with the Initiative Phase.],
    )
  ],
  [
    #aside-head(seed: 3)[Setup Roll-off]
    Each Party Leader's controller rolls *1d20*; higher wins, ties reroll. The winner makes the listed choice. Two automatic wins cancel. Never a free choice between unequal scenario roles.
    #v(4pt)
    *Solo or co-op:* the allied party wins automatically.
    #gap-v
    #aside-head(seed: 5)[Random Direction]
    Roll *1d8*; move that way, stopping at the last legal point.
    #align(center, compass)
    The Roll-off winner names an edge *North*. North and South are the *short* edges; East and West the *long* ones.
  ])
]

#let row(cl, n, sc, ob) = (if cl != none { [#cl] } else { [] }, [#n], [#sc], text(size: 9.5pt, ob))
#side(..head, face: "back")[
  #aid-table((88pt, 22pt, 0.95fr, 1.3fr), ("key", "roll", "text", "text"), ("Climate", "d6", "Core Scenario", "Objective at a glance"), (
    row([1 Greenmark], 1, [Hunt the Wild Beast (Intro)], [Escape with the Pristine Boar Pelt.]),
    row(none, 2, [The Whispering Grove], [Activate the most Standing Stones.]),
    row(none, 3, [The Bandit's Toll], [Defeat the Toll Captain; bank the most Coin Value.]),
    row(none, 4, [The Spider's Silk Route], [Extract the highest Coin Value in Spider Silk.]),
    row(none, 5, [The Ambushed Emissary], [Retrieve and escape with the Diplomatic Satchel.]),
    row(none, 6, [Ritual of the Old Growth], [Steal the Heartwood Totem or protect the ritual.]),
    row([2 Ashlands], 1, [The Fallen Observatory (Intro)], [Finish with the highest total Coin Value.]),
    row(none, 2, [The Guardian's Test], [Complete the Trials; claim the Vault Keystone.]),
    row(none, 3, [The Shifting Sands of Time], [Finish with the highest total Coin Value.]),
    row(none, 4, [The Sealed Archive], [Extract the Archive Codex.]),
    row(none, 5, [The Reliquary of Broken Saints], [Steal the Reliquary or complete the Ritual of Quiet.]),
    row(none, 6, [The Iron-Vein Vault], [Seal the Vault, or break it open and extract the Vault Record.]),
    row([3 Undermarches], 1, [The Crystal Harvest (Intro)], [Extract the highest Coin Value in Crystal Clusters.]),
    row(none, 2, [The Chasm Crossing], [Carry the Survey Map to the Cartographer's Stone.]),
    row(none, 3, [The Quake], [Mine and extract the most Gemstone value.]),
    row(none, 4, [The Undermarches Outpost Raid], [Steal the Battle Plans; defeat the Outpost Commander.]),
    row(none, 5, [The Shadowed Under Passage], [Steal the Heart of Shadow or consecrate every Font.]),
    row(none, 6, [The Ritual of Shadow Binding], [Disrupt the ritual or bind the Shadow Spirit.]),
    row([4 Pale City], 1, [Plunder of the Frozen Ruins (Intro)], [Finish with the highest total Coin Value.]),
    row(none, 2, [The Alchemist's Frozen Laboratory], [Finish with the highest total Coin Value.]),
    row(none, 3, [The Haunted Mausoleum], [Finish with the highest total Coin Value.]),
    row(none, 4, [The Clockwork Menagerie], [Finish with the highest total Coin Value.]),
    row(none, 5, [The Ice Wyrm's Hoard], [Defeat the Ice Wyrm; loot the Central Hoard.]),
    row(none, 6, [The Icebound Court], [Defeat the Magistrate; escape with your assigned relic.]),
    row([5 Sun-Drowned], 1, [The Oasis Raiders (Intro)], [Defeat the Raider Chieftain; control the Wellspring.]),
    row(none, 2, [The Cinder Lord's Lost Brazier], [Find and attune the Lost Brazier.]),
    row(none, 3, [Tomb of the Sunken Kings], [Finish with the highest total Coin Value.]),
    row(none, 4, [The Sandwyrm's Lair], [Defeat the Great Sandwyrm; loot the Hoard.]),
    row(none, 5, [The Cursed Colossus of the Waste], [Retrieve and extract the Heartstone.]),
    row(none, 6, [The Cinder Lord's Obsidian Prison], [Reinforce the prison or free the Cinder Lord.]),
    row([6 The Mire], 1, [The Reliquary of Edrava Salttide (Intro)], [Retrieve and extract Salttide's Reliquary.]),
    row(none, 2, [The Lizardfolk's Stolen Offerings], [Recover the Sunstone Amulet or steal Offering wealth.]),
    row(none, 3, [The Mire Titan's Fen], [Defeat the Mire Titan or extract enough Geodes.]),
    row(none, 4, [The Blighted Heartwood], [Destroy the Heartwood or complete the Syphon.]),
    row(none, 5, [Salttide's Reckoning], [Break the curse or complete the Curse Ritual.]),
    row(none, 6, [The Serpent's Sunken Hoard], [Defeat the Great Swamp Serpent; recover the Sunken Hoard.]),
  ), title: [Climate and Core Scenario #h(1fr) #text(font: sans, weight: 400, size: 9.5pt)[Roll 1d6 for the Climate, then 1d6. The full entry in §10.4 governs.]], size: 9.5pt)
]
