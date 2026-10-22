// The hero sheet (§ 6.4 Hero Attributes, § 7.2 equip limits, § 6.13 progression, § 6.16 training,
// § 11.1.5 fates) and the Basic Mode hero cards (Appendix B.4), which fill the same front.
#import "parts.typ": *

#let DATA = json("/typst/heroes/basic-heroes.json")
#let get(hr, k) = if hr == none { none } else { hr.at(k) }
#let signed(n) = if n >= 0 { "+" + str(n) } else { "−" + str(-n) }
#let ROW = 7pt                           // gap between the front's bands

// ---------------------------------------------------------------- side 1: the Hero
#let identity(hr) = {
  let arch = get(hr, "archetype")
  let left = {
    grid(columns: (1fr, 128pt), column-gutter: 12pt,
      field("Name", value: get(hr, "name"), h: 31pt, size: 20pt),
      field("Senses", value: if hr != none { hr.stats.at("Senses", default: "—") } else { none }, h: 31pt, size: 12.5pt))
    v(5pt)
    grid(columns: (1fr, 1fr, 1fr), column-gutter: 10pt,
      field("Ancestry", value: get(hr, "ancestry")),
      field("Background", value: get(hr, "background")),
      field("Class", value: get(hr, "class")))
    v(7pt)
    grid(columns: (52pt, 94pt, 1fr), column-gutter: 10pt,
      cell("Level", value: get(hr, "level"), h: 56pt, size: 26pt),
      cell("Archetype", h: 56pt, body: move(dy: 3pt, {
        set text(size: 9.5pt, weight: 600)
        stack(spacing: 2.5pt, ..("Martial", "Hybrid", "Caster").map(a => [#check(on: arch == a) #h(3pt) #a]))
      })),
      {
        grid(columns: (1fr, 1fr), column-gutter: 10pt,
          field("Casting Score", value: get(hr, "casting"), h: 30pt, size: 13pt),
          field("HP per Level", value: get(hr, "hp_per_level"), h: 30pt, size: 13pt))
        v(6pt)
        box(height: 20pt, align(bottom)[#check(s: 13pt) #h(4pt) #lbl("Party Leader") #h(4pt) #hint("INT + SPI on competitive Initiative")])
      })
  }
  grid(columns: (1fr, 138pt), column-gutter: 14pt, left,
    cornered(inset: (x: 5pt, y: 5pt), s: 12pt, block(width: 100%, height: 118pt, {
      if hr != none { place(center + horizon, image("/assets/art/ink/" + hr.art + ".png", height: 112pt)) }
      else { place(center + horizon, hint("Portrait or arms")) }
    })))
}

#let scores-row(hr) = {
  let s(k) = if hr == none { none } else { hr.scores.at(k) }
  let init = if hr == none { none } else {
    signed(int(hr.scores.INT.replace("+", "")) + int(hr.scores.SPI.replace("+", "")))
  }
  grid(columns: (1fr,) * 4 + (96pt,), column-gutter: 8pt, align: bottom,
    score("STR", "Strength", value: s("STR")), score("DEX", "Dexterity", value: s("DEX")),
    score("INT", "Intelligence", value: s("INT")), score("SPI", "Spirit", value: s("SPI")),
    box(width: 100%, inset: (bottom: 0pt), cell("Initiative", value: init, h: 50pt, size: 22pt, sub: "INT + SPI")))
}

#let vitals(hr) = {
  let st(k) = if hr == none { none } else { hr.stats.at(k) }
  grid(columns: (1.3fr, 1fr, 1fr, 48pt, 44pt, 44pt), column-gutter: 8pt,
    pool("HP", h: 52pt, max: st("HP"), extra: box(width: 46pt, height: 44pt, inset: (top: 4pt), align(center, hint("Temp HP")))),
    pool("NRG", h: 52pt, max: st("NRG")),
    pool("Luck", h: 52pt, max: st("Luck")),
    cell("SPD", value: st("SPD"), h: 52pt), cell("Sz", value: st("Sz"), h: 52pt), cell("AP", value: st("AP"), h: 52pt))
}

#let armour-blank = {
  sheet-head("Armour and Wounds", seed: 6, right: "Shield AD and AV apply only through Block · apply only the worse DEX Pen")
  let row(name) = grid(columns: (1fr, 40pt, 40pt, 54pt, 56pt), column-gutter: 7pt, align: bottom,
    field(name, h: 30pt), cell("AD", h: 34pt), cell("AV", h: 34pt), cell("DEX Pen", h: 34pt), cell("Max SPD", h: 34pt))
  grid(columns: (1fr, 146pt), column-gutter: 16pt,
    { row("Chest Armour"); v(4pt); row("Shield") },
    {
      grid(columns: (auto, 1fr), column-gutter: 8pt, align: horizon, lbl("Wounds"), ticks(3, s: 17pt))
      v(3pt)
      hint("A Hero who marks a third Wound dies.")
      v(5pt)
      lbl("Lingering Injuries")
      ruled(h: 2 * PITCH - 6pt)
    })
}

#let weapons-blank = {
  sheet-head("Weapons", seed: 8, right: "P Primary Weapon · O Off-Hand Weapon, which always rolls exactly 1 base damage die")
  table(columns: (32pt, 1.4fr, 40pt, 1.3fr, 46pt, 1.5fr), inset: (x: 5pt, y: 0pt), rows: (15pt,) + (PITCH,) * 3,
    stroke: (x, y) => (bottom: if y == 0 { none } else { 0.55pt + pen }, left: if x > 0 and y > 0 { 0.4pt + pen } else { none }),
    fill: (x, y) => if y == 0 { ink } else { none }, align: horizon,
    ..("P/O", "Weapon", "Hands", "Damage and Type", "Range", "Traits").map(t => lbl(t, fill: paper)),
    ..range(18).map(_ => []))
}

#let slots-blank = {
  sheet-head("Equipped", seed: 10, right: "One per slot · 2 Rings · 2 Hands · at most 5 Permanent Special Items")
  let sl = ("Chest", "Head", "Back", "Neck", "Waist", "Arms", "Feet", "Ring", "Ring", "Hand", "Hand")
  grid(columns: (1fr,) * 4, column-gutter: 10pt, row-gutter: 3pt,
    ..sl.map(s => field(s, h: 24pt)),
    block(height: 24pt, align(bottom + right, [#lbl("Special") #h(3pt) #ticks(5, s: 10pt)])))
}

// Basic Mode replaces armour, weapons, and slots with the profile's equipment and its 0 HP rule.
#let card-gear(hr) = {
  let ad = hr.stats.AD
  sheet-head("Equipment and Items", seed: 6, right: if ad.contains("Shield") { "Shield AD applies only when you Block" }
    else if ad != "None" { "Chest AD rolls against blunt, piercing, and slashing damage" })
  let eq = hr.sections.find(s => s.title == "Equipment and Items")
  balanced-pair(for it in eq.items { rule-item(it, size: 9.5pt) })
  v(10pt)
  grid(columns: (2.1fr, 1fr, 1fr, 92pt), column-gutter: 10pt, align: bottom,
    cell("AD", h: 40pt, body: box(width: 100%, inset: (x: 6pt), align(center, fit-inked(hr.stats.AD, size: 13pt, room: 0pt)))), field("Hand", h: 30pt), field("Hand", h: 30pt), cell("Carried Coins", h: 40pt))
  v(5pt)
  text(size: 9pt, rich(DATA.notes.hands))
  v(10pt)
  sheet-head("At 0 HP", seed: 12, right: "Basic Mode")
  text(size: 9pt, rich(DATA.notes.knocked_out))
  v(8pt)
  lbl("Notes")
  ruled(h: 1fr)
}

#let front(hr) = leaf(if hr == none { "Hero Sheet" } else { hr.name },
  if hr == none { "Hero Sheet" } else { "Basic Mode Hero" },
  if hr == none { "§ 6.4 · § 7.2 · Side 1 of 2" } else { hr.class + " · " + hr.ancestry + " " + hr.background },
  face: "front", arm: if hr == none { 6 } else { 13 })[
  #identity(hr)
  #v(ROW)
  #scores-row(hr)
  #v(ROW - 2pt)
  #vitals(hr)
  #v(ROW + 2pt)
  #if hr == none {
    armour-blank
    v(ROW)
    weapons-blank
    v(ROW)
    slots-blank
  } else { card-gear(hr) }
]

// ---------------------------------------------------------------- side 2 of the blank sheet
#let GAINS = (
  [General Talent; Novice Class Talent],
  [+1 to two different scores],
  [Novice Class Talent],
  [Archetype Ability 1; General Talent or +1],
  [Adept Class Talent],
  [General Talent or +1],
  [Archetype Ability 2; Adept Class Talent],
  [General Talent or +1],
  [Master Class Talent],
  [+1 to two different scores],
)
#let TRAIN = ("—", "16c", "24c", "32c", "40c", "48c", "56c", "64c", "72c", "80c")
#let PAYOUT = ("0c", "8c", "20c", "36c", "56c", "80c", "108c", "140c", "176c", "216c")

#let labelled-lines(title, labels) = {
  strap(title)
  v(2pt)
  for l in labels {
    block(width: 100%, height: PITCH, spacing: 0pt, {
      place(bottom + left, line(length: 100%, stroke: 0.55pt + pen))
      place(bottom + left, dy: -3pt, hint(l))
    })
  }
}

#let back-blank = leaf("Powers and Progress", "Hero Sheet", "§ 6.12 · § 6.13 · § 6.16 · § 11.1.5 · Side 2 of 2",
  face: "back", arm: 6, title-size: 24pt)[
  #sheet-head("Known Powers", seed: 3, right: "Casting: § 8.2 · metal equipment restrictions apply")
  #table(columns: (1.3fr, 32pt, 30pt, 34pt, 42pt, 3fr), inset: (x: 5pt, y: 0pt), rows: (15pt,) + (PITCH,) * 6,
    stroke: (x, y) => (bottom: if y == 0 { none } else { 0.55pt + pen }, left: if x > 0 and y > 0 { 0.4pt + pen } else { none }),
    fill: (x, y) => if y == 0 { ink } else { none }, align: horizon,
    ..("Power", "Tier", "AP", "NRG", "Range", "Target and Effect").map(t => lbl(t, fill: paper)),
    ..range(36).map(_ => []))
  #v(10pt)
  #sheet-head("Talents and Special Abilities", seed: 5, right: "General Talents follow § 6.12 and your Archetype")
  #grid(columns: (1fr, 1fr, 1fr), column-gutter: 14pt,
    labelled-lines("General Talents", ("L1", "L4", "L6", "L8", "")),
    labelled-lines("Class Talents", ("L1 Novice", "L3 Novice", "L5 Adept", "L7 Adept", "L9 Master")),
    labelled-lines("Special Abilities", ("Ancestry", "Ancestry", "Background", "L4 Archetype", "L7 Archetype")))
  #v(10pt)
  #sheet-head("Advancement", seed: 7, right: "Train [1 TAP] in the Town Phase · Level 10 is the maximum")
  #grid(columns: (1fr,) * 10, column-gutter: 5pt, row-gutter: 4pt,
    ..range(10).map(i => align(center, {
      box(width: 23pt, height: 27pt, {
        shield-curve(23pt, 27pt, stroke: 1.4pt + ink)
        place(top + center, dy: 5pt, text(font: goth, weight: 700, size: 13pt, str(i + 1)))
      })
    })),
    ..GAINS.map(g => block(width: 100%, height: 50pt, align(center, text(size: 9pt, g)))),
    ..range(10).map(i => align(center, text(size: 9pt)[#text(fill: ink3)[Train] *#TRAIN.at(i)* \ #text(fill: ink3)[Retire] *#PAYOUT.at(i)*])))
  #v(4pt)
  #block(text(size: 9pt)[*Each level:* add Max HP per Level, gain its benefits, learn any class Power, and recalculate Initiative Bonus and Max NRG. \ *Archetype Abilities 1 and 2:* Martial, Martial Supremacy and Sunder · Hybrid, Martial Supremacy and +1 Primary Casting Score · Caster, Caster Supremacy and +4 Max NRG])
  #v(10pt)
  #sheet-head("Carried and Fate", seed: 9, right: "Secured coins go to the Treasury; unequipped gear rests in Storage")
  #grid(columns: (1fr, 188pt), column-gutter: 16pt,
    block(height: 1fr, { lbl("Carried Items"); ruled(h: 1fr) }),
    block(height: 1fr, {
      grid(columns: (1fr, 1fr), column-gutter: 8pt,
        cell("Carried Coins", h: 40pt, sub: "battlefield only"), cell("Adventures", h: 40pt, sub: "tally"))
      v(8pt)
      lbl("Fate")
      v(3pt)
      set text(size: 10pt, weight: 600)
      grid(columns: (66pt, 1fr), row-gutter: 6pt,
        [#check() #h(2pt) Died], [#check() #h(2pt) Retired],
        [#check() #h(2pt) Triumph], [#check() #h(2pt) Legendary Veteran])
    }))
]
