// The party ledger: the campaign's persistent records (§ 11.1.2 Roster, § 11.1.3 persistent elements,
// § 11.1.4 Treasury and Storage, § 11.2.5–11.2.6 Hirelings, § 11.3 Stronghold, § 11.4 Legendary Veterans).
#import "parts.typ": *

#let ruled-table(header, widths, n, cells: none) = table(columns: widths, inset: (x: 5pt, y: 0pt),
  rows: (15pt,) + (PITCH + 1pt,) * n, align: horizon,
  stroke: (x, y) => (bottom: if y == 0 { none } else { 0.55pt + pen }, left: if x > 0 and y > 0 { 0.4pt + pen } else { none }),
  fill: (x, y) => if y == 0 { ink } else { none },
  ..header.map(t => lbl(t, fill: paper)),
  ..if cells == none { range(n * header.len()).map(_ => []) } else { range(n).map(cells).flatten() })

#let COMPONENTS = ("The Vault", "The Barracks", "The Armoury", "The Apothecary", "The Outer Walls",
  "The Arcanum", "The Stronghold Chapel", "The War Room", "The Expedition Hall", "The Undercroft")

#leaf("Party Ledger", "Campaign Record", "§ 11.1 · § 11.2.5 · § 11.3 · § 11.4 · Side 1 of 2", face: "front", arm: 11)[
  #grid(columns: (1fr, 1fr, 150pt), column-gutter: 12pt, align: bottom,
    field("Party", h: 32pt), field("Party Leader", h: 32pt, note: "not changed voluntarily"),
    box(inset: (bottom: 3pt), {
      set text(size: 10pt, weight: 600)
      stack(spacing: 5pt, [#check() #h(3pt) Competitive campaign], [#check() #h(3pt) Solo or cooperative])
    }))
  #v(8pt)
  #sheet-head("Roster", seed: 2, right: "Up to 8 Heroes · Active Party normally 4 · the rest are the Bench")
  #ruled-table(("Hero", "Class", "Level", "Wounds", "Active", "Lingering Injuries and Notes"),
    (1.2fr, 0.9fr, 40pt, 62pt, 44pt, 1.7fr), 8,
    cells: i => ([], [], [], align(center, ticks(3, s: 10pt)), align(center, check()), []))
  #v(8pt)
  #sheet-head("Hirelings and Animal Companions", seed: 4, right: "Up to 8 together · assign each active Hireling to a Hero with printed SPI ≥ Min SPI")
  #ruled-table(("Hireling", "Type", "Min SPI", "HP", "AV", "Assigned Hero", "Notes"),
    (1.1fr, 0.9fr, 50pt, 34pt, 32pt, 1fr, 1fr), 5)
  #v(8pt)
  #sheet-head("Stronghold", seed: 6, right: "1 Component per Town Phase [1 TAP] · next costs 130c, 170c, 210c, 250c, then 290c")
  #grid(columns: (1fr, 1fr), column-gutter: 18pt, row-gutter: 0pt,
    ..COMPONENTS.map(c => block(width: 100%, height: PITCH + 2pt, spacing: 0pt, {
      place(bottom + left, line(length: 100%, stroke: 0.55pt + pen))
      place(bottom + left, dy: -4pt, grid(columns: (148pt, auto), column-gutter: 6pt,
        [#check() #h(3pt) #text(weight: 700, c)], hint("Legendary Veteran")))
    })))
  #v(8pt)
  #grid(columns: (1.3fr, 1fr, 1fr), column-gutter: 14pt,
    {
      lbl("Unassigned Veterans")
      v(1pt)
      hint("Assign each to a completed Component from the next Town Phase.")
      ruled(h: PITCH)
    },
    {
      grid(columns: (auto, 1fr), column-gutter: 8pt, align: horizon, lbl("Hero Deaths"), ticks(4, s: 14pt))
      v(3pt)
      hint("Solo or cooperative: the fourth permanent death ends the campaign in defeat.")
    },
    {
      grid(columns: (auto, 1fr), column-gutter: 8pt, align: horizon, lbl("Triumph"), check(s: 14pt))
      v(3pt)
      hint("Five different Components, or the Triumph Finale (solo or cooperative)")
    })
]

#leaf("Treasury and Storage", "Campaign Record", "§ 11.1.4 · § 11.2.3 · § 11.2.4 · Side 2 of 2", face: "back", arm: 11, title-size: 24pt)[
  #sheet-head("Campaign Log and Treasury", seed: 3, right: "Record each secured reward once, in the Aftermath · round percentage-reduced costs up")
  #ruled-table(("No.", "Scenario, Climate, and Result", "Coins In", "Coins Out", "Treasury"),
    (30pt, 1fr, 66pt, 72pt, 76pt), 16)
  #v(8pt)
  #sheet-head("Storage", seed: 5, right: "All unequipped items, scrolls, potions, and poisons between adventures")
  #grid(columns: (1fr, 1fr), column-gutter: 18pt, ruled(h: 1fr), ruled(h: 1fr))
]
