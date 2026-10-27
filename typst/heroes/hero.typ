// The hero sheet (§ 6.4 Hero Attributes, § 7.2 equip limits, § 6.13 progression, § 6.16 training,
// § 11.1.5 fates) and the Basic Mode hero cards (Appendix B.4), which fill the same front.
#import "parts.typ": *

#let DATA = json("/typst/heroes/basic-heroes.json")
#let get(hr, k) = if hr == none { none } else { hr.at(k) }
#let signed(n) = if n >= 0 { "+" + str(n) } else { "−" + str(-n) }
#let BAND = 13pt                         // gap between plates (room for the next ribbon)

// Table inside a plate: small-caps heads over a rule, then ruled pencil rows.
#let pencil-table(heads, widths, n, row: PITCH, aligns: none, first: ()) = table(columns: widths, inset: (x: 4pt, y: 0pt),
  rows: (15pt,) + (row,) * n, align: (x, y) => if aligns == none { left + horizon } else { aligns.at(x) + horizon },
  stroke: (x, y) => (bottom: if y == 0 { 0.8pt + ink } else { 0.5pt + pen },
    left: if x > 0 { 0.4pt + pen } else { none }),
  ..heads.map(t => lbl(t, size: 9pt, weight: 700)),
  ..range(n).map(r => (lbl(first.at(r, default: ""), weight: 600, fill: ink2),) + range(heads.len() - 1).map(_ => [])).flatten())
// The same table with as many rows as its container's height allows.
#let fill-table(heads, widths, aligns: none) = block(height: 1fr, width: 100%, layout(size => {
  pencil-table(heads, widths, calc.max(1, calc.floor((size.height - 15pt) / PITCH)), aligns: aligns)
}))

// ---------------------------------------------------------------- side 1: the Hero
#let identity(hr) = {
  let arch = get(hr, "archetype")
  let H = 140pt
  grid(columns: (1fr, 124pt), column-gutter: 14pt,
    plate(title: "The Hero", h: H, inset: (x: 11pt, top: 13pt, bottom: 9pt))[
      #grid(columns: (1fr, 122pt), column-gutter: 12pt,
        field("Name", value: get(hr, "name"), size: 18pt),
        field("Senses", value: if hr != none { hr.stats.at("Senses", default: "—") } else { none }, size: 12pt))
      #v(2pt)
      #grid(columns: (1fr, 1fr, 1fr), column-gutter: 12pt,
        field("Ancestry", value: get(hr, "ancestry")),
        field("Background", value: get(hr, "background")),
        field("Class", value: get(hr, "class")))
      #v(4pt)
      #grid(columns: (50pt, auto, 1fr, 1fr), column-gutter: 12pt, align: bottom,
        roundel("Level", value: get(hr, "level"), d: 36pt, size: 18pt),
        box(inset: (bottom: 1pt), {
          set text(size: 9.5pt, weight: 600)
          stack(spacing: 2.5pt, ..("Martial", "Hybrid", "Caster").map(a => [#check(on: arch == a, s: 9.5pt) #h(2pt) #a]))
          v(3pt)
          lbl("Archetype", weight: 600, fill: ink2)
        }),
        {
          field("Casting Score", value: get(hr, "casting"), size: 13pt)
          v(3pt)
          box[#check(s: 11pt) #h(3pt) #lbl("Party Leader", weight: 600, fill: ink2)]
        },
        {
          field("HP per Level", value: get(hr, "hp_per_level"), size: 13pt)
          v(3pt)
          text(size: 9pt, fill: ink3)[Leader: INT + SPI on Initiative]
        })
    ],
    arch-frame(124pt, H, body: if hr != none { image("/assets/art/ink/" + hr.art + ".png", height: 104pt) }
      else { box(height: 60pt, align(center + horizon, rubric[portrait or arms])) }))
}

#let scores-row(hr) = {
  let s(k) = if hr == none { none } else { hr.scores.at(k) }
  let init = if hr == none { none } else {
    signed(int(hr.scores.INT.replace("+", "")) + int(hr.scores.SPI.replace("+", "")))
  }
  grid(columns: (1fr,) * 4 + (92pt,), column-gutter: 8pt, align: bottom,
    score("STR", "Strength", value: s("STR")), score("DEX", "Dexterity", value: s("DEX")),
    score("INT", "Intelligence", value: s("INT")), score("SPI", "Spirit", value: s("SPI")),
    roundel("Initiative", value: init, d: 48pt, size: 22pt, sub: "INT + SPI"))
}

// A resource that changes in play: pencil room for the current value, the maximum in a roundel.
#let pool(title, max: none, temp: false) = plate(title: title, inset: (x: 8pt, top: 12pt, bottom: 7pt))[
  #grid(columns: if temp { (1fr, 38pt, 40pt) } else { (1fr, 40pt) }, column-gutter: 6pt, align: bottom,
    block(height: 40pt, place(bottom + left, lbl("Current", weight: 600, fill: ink2))),
    ..if temp { (align(center, { box(width: 34pt, height: 24pt, stroke: 0.6pt + ink); v(2pt, weak: false); lbl("Temp", weight: 600, fill: ink2) }),) },
    roundel("Max", value: max, d: 34pt, size: 16pt))
]

#let vitals(hr) = {
  let st(k) = if hr == none { none } else { hr.stats.at(k) }
  grid(columns: (1.45fr, 1fr, 1fr, 46pt, 46pt, 46pt), column-gutter: 9pt, align: bottom,
    pool("Hit Points", max: st("HP"), temp: true), pool("Energy", max: st("NRG")), pool("Luck", max: st("Luck")),
    roundel("SPD", value: st("SPD"), d: 42pt, size: 16pt), roundel("Sz", value: st("Sz"), d: 42pt, size: 16pt),
    roundel("AP", value: st("AP"), d: 42pt, size: 16pt))
}

#let armour-wounds = grid(columns: (1fr, 168pt), column-gutter: 14pt,
  plate(title: "Armour", h: 92pt)[
    #pencil-table(("", "Item", "AD", "AV", "DEX Pen", "Max SPD"), (44pt, 1fr, 36pt, 36pt, 50pt, 52pt), 2, row: 20pt,
      aligns: (left, left, center, center, center, center), first: ("Chest", "Shield"))
    #v(4pt)
    #text(size: 9pt, fill: ink3)[Shield AD and AV only through Block · Chest and shield DEX Pen add together]
  ],
  plate(title: "Wounds", h: 92pt, inset: (x: 10pt, top: 15pt, bottom: 7pt))[
    #align(center)[#wound(s: 17pt) #h(6pt) #wound(s: 17pt) #h(6pt) #wound(s: 17pt)]
    #v(2pt)
    #align(center, rubric[A Hero who marks a third Wound dies.])
    #v(1pt)
    #lbl("Lingering Injuries", weight: 600, fill: ink2)
    #ruled(h: 1fr)
  ])

#let weapons-plate = plate(title: "Weapons")[
  #pencil-table(("P/O", "Weapon", "Hands", "Damage and Type", "Range", "Traits"),
    (30pt, 1.3fr, 40pt, 1.2fr, 42pt, 1.6fr), 3)
  #v(4pt)
  #text(size: 9pt, fill: ink3)[P Primary Weapon · O Off-Hand Weapon: always exactly 1 base damage die]
]

#let carried-plate = block(height: 1fr, plate(title: "Carried", h: "fill")[
  #grid(columns: (1fr, 64pt), column-gutter: 14pt,
    block(height: 1fr, ruled(h: 1fr)),
    block(height: 1fr, align(center + horizon, roundel("Coins", d: 34pt, sub: "carried"))))
])

// Basic Mode replaces armour, Wounds, and weapons with the profile's equipment and the appendix's rules.
#let card-gear(hr) = {
  let eq = hr.sections.find(s => s.title == "Equipment and Items")
  let ad = hr.stats.AD
  twin(("Equipment and Items", { for it in eq.items { rule-item(it, size: 9.5pt) }; v(2pt); ruled(h: 1fr) }),
    ("Armour", {
      align(center, fit-inked(ad, size: 13pt, room: 0pt))
      align(center, lbl("Armour Dice", weight: 600, fill: ink2))
      v(1pt)
      align(center, text(size: 9pt, fill: ink3, if ad.contains("Shield") [Shield AD only when you Block]
        else if ad != "None" [Chest AD rolls against blunt, piercing, and slashing damage]))
      v(1fr)
      field("Hand")
      field("Hand")
      field("Carried Coins")
    }), cols: (1fr, 156pt))
  v(BAND)
  block(height: 1fr, plate(title: "Basic Mode", h: "fill")[
    #set text(size: 9.5pt)
    #rich(DATA.notes.hands)
    #v(3pt)
    #rich(DATA.notes.knocked_out)
    #v(2pt)
    #ruled(h: 1fr)
  ])
}

#let front(hr) = leaf(if hr == none { "Hero Sheet" } else { hr.name },
  if hr == none { "Heraldry Skirmish · § 6.4 · Side 1" } else { hr.class + " · " + hr.ancestry + " " + hr.background + " · Basic Mode" },
  face: "front", arm: if hr == none { 6 } else { 13 })[
  #identity(hr)
  #v(13pt)
  #scores-row(hr)
  #v(BAND)
  #vitals(hr)
  #v(BAND)
  #if hr == none {
    armour-wounds
    v(BAND)
    weapons-plate
    v(BAND)
    carried-plate
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
  align(center, lbl(title, weight: 700))
  v(-3pt)
  line(length: 100%, stroke: 0.8pt + ink)
  v(-5pt)
  for l in labels {
    block(width: 100%, height: PITCH, spacing: 0pt, {
      place(bottom + left, line(length: 100%, stroke: 0.5pt + pen))
      place(bottom + left, dy: -3pt, text(size: 9pt, fill: ink3, l))
    })
  }
}

#let level-shield(n) = box(width: 24pt, height: 28pt, {
  shield-curve(24pt, 28pt, stroke: 1.4pt + ink)
  let k = 2.2pt
  shield-curve(24pt - 2 * k, 28pt - 2.3 * k, dx: k, dy: k, stroke: 0.4pt + ink)
  place(top + center, dy: 5pt, text(font: goth, weight: 700, size: 13pt, str(n)))
})

#let back-blank = leaf("Powers and Progress", "Hero Sheet · Side 2",
  face: "back", arm: 6, title-size: 26pt)[
  #plate(title: "Known Powers")[
    #pencil-table(("Power", "Tier", "AP", "NRG", "Range", "Target and Effect"), (1.3fr, 30pt, 28pt, 32pt, 40pt, 3fr), 6)
    #v(4pt)
    #text(size: 9pt, fill: ink3)[Cast under § 8.2, including its metal equipment restrictions]
  ]
  #v(BAND)
  #plate(title: "Talents and Special Abilities")[
    #grid(columns: (1fr, 1fr, 1fr), column-gutter: 14pt,
      labelled-lines("General Talents", ("L1", "L4", "L6", "L8", "")),
      labelled-lines("Class Talents", ("L1 Novice", "L3 Novice", "L5 Adept", "L7 Adept", "L9 Master")),
      labelled-lines("Special Abilities", ("Ancestry", "Ancestry", "Background", "L4 Archetype", "L7 Archetype")))
  ]
  #v(BAND)
  #plate(title: "Advancement")[
    #grid(columns: (1fr,) * 10, column-gutter: 5pt, row-gutter: 3pt,
      ..range(10).map(i => align(center, level-shield(i + 1))),
      ..GAINS.map(g => block(width: 100%, height: 47pt, align(center, text(size: 9pt, g)))),
      ..range(10).map(i => align(center, text(size: 9pt)[#text(fill: ink3)[Train] *#TRAIN.at(i)* \ #text(fill: ink3)[Retire] *#PAYOUT.at(i)*])))
    #v(3pt)
    #line(length: 100%, stroke: 0.5pt + pen)
    #v(-2pt)
    #text(size: 9pt)[*Each level:* add Max HP per Level, gain its benefits, learn any class Power, and recalculate Initiative Bonus and Max NRG. *Archetype Abilities 1 and 2:* Martial, Martial Supremacy and Sunder · Hybrid, Martial Supremacy and +1 Primary Casting Score · Caster, Caster Supremacy and +4 Max NRG. Train [1 TAP] in the Town Phase.]
  ]
  #v(BAND)
  #block(height: 1fr, grid(columns: (1fr, 122pt), column-gutter: 14pt,
    plate(title: "Equipped", h: "fill")[
      #let sl = ("Chest", "Head", "Back", "Neck", "Waist", "Arms", "Feet", "Ring", "Ring", "Hand", "Hand")
      #grid(columns: (1fr,) * 3, column-gutter: 12pt, ..sl.map(s => field(s, h: 24pt)),
        block(height: 24pt, align(bottom, [#lbl("Special", weight: 600, fill: ink2) #h(2pt) #ticks(5, s: 9.5pt, gap: 2pt)])))
      #v(1fr)
      #text(size: 9pt, fill: ink3)[One item per slot, up to 2 Rings and 2 hands · Special: tick each Permanent Special Item, at most 5]
    ],
    plate(title: "Fate", h: "fill")[
      #align(center, roundel("Adventures", d: 32pt, sub: "tally"))
      #v(1fr)
      #set text(size: 9.5pt, weight: 600)
      #stack(spacing: 4pt, [#check(s: 9.5pt) #h(2pt) Died], [#check(s: 9.5pt) #h(2pt) Retired],
        [#check(s: 9.5pt) #h(2pt) Legendary Veteran], [#check(s: 9.5pt) #h(2pt) Triumph])
    ]))
]
