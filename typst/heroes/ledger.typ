// The party ledger: the campaign's persistent records (§ 11.1.2 Roster, § 11.1.3 persistent elements,
// § 11.1.4 Treasury and Storage, § 11.2.5–11.2.6 Hirelings, § 11.3 Stronghold, § 11.4 Legendary Veterans).
#import "hero.typ": *

#let note(t) = text(size: 9pt, fill: ink3, t)
#let COMPONENTS = ("The Vault", "The Barracks", "The Armoury", "The Apothecary", "The Outer Walls",
  "The Arcanum", "The Stronghold Chapel", "The War Room", "The Expedition Hall", "The Undercroft")

// Pencil table whose rows may carry printed marks (ticks, wound lozenges) in given columns.
#let marked-table(heads, widths, n, marks: (:), aligns: none) = table(columns: widths, inset: (x: 4pt, y: 0pt),
  rows: (15pt,) + (PITCH,) * n, align: (x, y) => if aligns == none { left + horizon } else { aligns.at(x) + horizon },
  stroke: (x, y) => (bottom: if y == 0 { 0.8pt + ink } else { 0.5pt + pen }, left: if x > 0 { 0.4pt + pen } else { none }),
  ..heads.map(t => lbl(t, size: 9pt, weight: 700)),
  ..range(n).map(_ => range(heads.len()).map(x => marks.at(str(x), default: []))).flatten())

#leaf("Party Ledger", "Campaign Record · Side 1", face: "front", arm: 11)[
  #plate(title: "The Party")[
    #grid(columns: (1fr, 1fr, 150pt), column-gutter: 14pt, align: bottom,
      field("Party Name"), field("Party Leader"),
      box(inset: (bottom: 2pt), {
        set text(size: 9.5pt, weight: 600)
        stack(spacing: 4pt, [#check(s: 9.5pt) #h(2pt) Competitive campaign], [#check(s: 9.5pt) #h(2pt) Solo or cooperative])
      }))
    #v(5pt)
    #grid(columns: (1fr, 1fr), column-gutter: 14pt,
      {
        box[#lbl("Hero Deaths", weight: 600, fill: ink2) #h(4pt) #wound(s: 14pt) #wound(s: 14pt) #wound(s: 14pt) #wound(s: 14pt)]
        v(2pt)
        note[Solo or cooperative: the fourth permanent death ends the campaign in defeat.]
      },
      {
        box[#lbl("Triumph", weight: 600, fill: ink2) #h(4pt) #check(s: 13pt)]
        v(2pt)
        note[Five different Components, or the Triumph Finale (solo or cooperative)]
      })
    #v(2pt)
    #note[The Party Leader cannot be changed voluntarily.]
  ]
  #v(BAND)
  #plate(title: "Roster")[
    #marked-table(("Hero", "Class", "Level", "Wounds", "Active", "Injuries and Notes"),
      (1.2fr, 0.9fr, 40pt, 66pt, 44pt, 1.7fr), 8,
      marks: ("3": [#wound(s: 11pt) #wound(s: 11pt) #wound(s: 11pt)], "4": check()),
      aligns: (left, left, center, center, center, left))
    #v(3pt)
    #note[Up to 8 Heroes · the Active Party is normally 4 · the rest are the Bench]
  ]
  #v(BAND)
  #plate(title: "Stronghold")[
    #grid(columns: (1fr, 1fr), column-gutter: 20pt,
      ..COMPONENTS.map(c => block(width: 100%, height: PITCH + 1pt, spacing: 0pt, {
        place(bottom + left, line(length: 100%, stroke: 0.5pt + pen))
        place(bottom + left, dy: -4pt, grid(columns: (140pt, auto), column-gutter: 4pt,
          [#check(s: 9.5pt) #h(3pt) #text(weight: 700, size: 9.5pt, c)], note[Veteran:]))
      })))
    #block(width: 100%, height: PITCH + 2pt, spacing: 0pt, {
      place(bottom + left, line(length: 100%, stroke: 0.5pt + pen))
      place(bottom + left, dy: -4pt, [#text(weight: 700, size: 9.5pt)[Unassigned Legendary Veterans:] #h(4pt) #note[assign each to a completed Component from the next Town Phase]])
    })
    #v(4pt)
    #note[One Component per Town Phase [1 TAP] · the next costs 130c, 170c, 210c, 250c, then 290c]
  ]
  #v(BAND)
  #block(height: 1fr, plate(title: "Notes", h: "fill")[#ruled(h: 1fr)])
]

#leaf("Treasury and Storage", "Campaign Record · Side 2", face: "back", arm: 11)[
  #plate(title: "Campaign Log and Treasury")[
    #marked-table(("No.", "Scenario, Climate, and Result", "Coins In", "Coins Out", "Treasury"),
      (30pt, 1fr, 66pt, 72pt, 76pt), 12, aligns: (center, left, center, center, center))
    #v(3pt)
    #note[Record each secured reward once, in the Aftermath · round percentage-reduced costs up]
  ]
  #v(BAND)
  #plate(title: "Hirelings and Animal Companions")[
    #marked-table(("Hireling", "Type", "Min SPI", "HP", "AV", "Assigned Hero", "Notes"),
      (1.1fr, 0.9fr, 50pt, 34pt, 32pt, 1fr, 1fr), 8, aligns: (left, left, center, center, center, left, left))
    #v(3pt)
    #note[Up to 8 together · assign each active Hireling to a Hero whose printed SPI is at least its Min SPI]
  ]
  #v(BAND)
  #block(height: 1fr, plate(title: "Storage", h: "fill")[
    #block(height: 1fr, grid(columns: (1fr, 1fr), column-gutter: 20pt, ruled(h: 100%), ruled(h: 100%)))
    #v(3pt)
    #note[Between adventures: all unequipped items, scrolls, potions, and poisons]
  ])
]
