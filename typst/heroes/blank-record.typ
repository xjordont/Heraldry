// Blank expanded record. Book typography and boundary ornament, with open writing fields.
// Basic Mode cards deliberately keep their previous template until the blank is settled.
#import "/typst/aids/kit.typ": *
#import "parts.typ": arch-path, wound

#let writing-ink = rgb(0, 0, 0, 34%)
#let label(t, size: 9pt) = text(font: sans, weight: 650, size: size, t)
#let writing-line(w: 100%) = line(length: w, stroke: 0.45pt + writing-ink)

// One label, one writing surface. No tinted cell, inset border, or enclosing panel.
#let write(label-text, h: 28pt) = block(width: 100%, height: h, spacing: 0pt, {
  place(label(label-text))
  place(bottom + left, writing-line())
})

#let section(title, seed: 1, right: none) = block(width: 100%, height: 23pt, spacing: 0pt, {
  place(grid(columns: (auto, 1fr, auto), column-gutter: 6pt, align: horizon,
    box(baseline: 0pt, lozenge(size: 4.5pt)),
    text(font: goth, weight: 600, size: 18pt, title),
    if right == none { [] } else { right }))
  place(bottom + left, brush(weight: 1.1pt, seed: seed))
})

// Open ledger: only column separators and row rules, with no outer or nested frame.
#let ledger(heads, widths, n, row: 20pt, two-lines: false) = table(
  columns: widths, rows: (15pt,) + (row,) * n,
  inset: (left: 4pt, right: 4pt, y: 0pt), align: left + horizon,
  stroke: none,
  ..heads.map(t => table.cell(stroke: (bottom: 0.85pt + ink), label(t))),
  ..range(n).map(r => range(heads.len()).map(c => table.cell(
    stroke: (bottom: 0.45pt + writing-ink,
      left: if c == 0 { none } else { 0.35pt + writing-ink }),
    if two-lines and c == heads.len() - 1 {
      block(width: 100%, height: row, {
        place(dy: row / 2, writing-line())
      })
    } else { [] }))).flatten())

#let ability(abbr) = box(width: 55pt, height: 52pt, {
  shield-curve(55pt, 52pt, stroke: 1pt + ink)
  place(dx: 0pt, dy: 3pt, box(width: 55pt, align(center,
    text(font: sans, weight: 700, size: 11pt, abbr))))
  place(dx: 10pt, dy: 37pt, writing-line(w: 35pt))
})

#let resource(title, fields) = block(width: 100%, height: 53pt, spacing: 0pt, {
  place(text(font: serif, weight: 700, size: 12.5pt, title))
  place(dy: 22pt, grid(columns: (1fr,) * fields.len(), column-gutter: 8pt,
    ..fields.map(f => write(f, h: 30pt))))
})

#let heading(title, face, reverse: false) = block(width: 100%, height: 32pt, spacing: 0pt, {
  place(grid(columns: (23pt, 1fr, auto), column-gutter: 8pt, align: horizon,
    signature(s: 23pt),
    text(font: goth, weight: 600, size: if reverse { 27pt } else { 30pt }, title),
    if reverse { box(width: 155pt, write("Hero", h: 25pt)) }
    else { align(right, text(font: sans, weight: 650, size: 9pt, tracking: 0.08em)[HERALDRY SKIRMISH \ #face]) }))
  place(bottom + left, brush(weight: 1.7pt, seed: 6))
})

#let record-side(face, n, body) = page(width: page-w, height: page-h,
  margin: (x: 36pt, top: 36pt, bottom: 52pt), fill: paper)[
  #set text(font: serif, size: 10.5pt, fill: ink, lang: "en", region: "CA", hyphenate: false,
    top-edge: 0.8em, bottom-edge: -0.25em)
  #set par(leading: 2pt, spacing: 0pt, justify: false)
  #block(width: 100%, height: 704pt, spacing: 0pt, body)
  #place(bottom + left, dy: 22pt, block(width: 100%, {
    line(length: 100%, stroke: 0.65pt + ink)
    v(3pt)
    grid(columns: (auto, 1fr, auto), column-gutter: 6pt, align: horizon,
      shield(w: 14pt, body: text(font: sans, weight: 700, size: 9pt, fill: paper, str(n))),
      label("HERALDRY SKIRMISH"), text(font: sans, size: 9pt, rules-rc + " | " + face))
  }))
]

#record-side("Hero Record / front", 1, {
  place(heading("Hero Record", "DETAILS AND INVENTORY"))
  place(dy: 42pt, block(width: 426pt, {
    grid(columns: (270pt, 144pt), column-gutter: 12pt, write("Name"), write("Class"))
    v(5pt)
    grid(columns: (1fr, 1fr), column-gutter: 12pt, write("Ancestry", h: 24pt), write("Background", h: 24pt))
    v(5pt)
    grid(columns: (41pt, 100pt, 70pt, 63pt, 112pt), column-gutter: 10pt,
      write("Level", h: 24pt), write("Archetype", h: 24pt), write("Casting", h: 24pt),
      write("HP/Level", h: 24pt), write("Senses", h: 24pt))
  }))
  // Deliberately empty: the owner may draw or attach a portrait or arms.
  place(dx: 440pt, dy: 42pt, arch-path(100pt, 88pt, stroke: 0.8pt + ink))
  place(dy: 140pt, grid(columns: (55pt, 55pt, 55pt, 55pt, 90pt, 83pt, 75pt),
    column-gutter: 12pt, align: top,
    ability("STR"), ability("DEX"), ability("INT"), ability("SPI"),
    write("Initiative", h: 46pt), write("Speed", h: 46pt), write("Size", h: 46pt)))
  place(dy: 202pt, grid(columns: (180pt, 140pt, 94pt, 90pt), column-gutter: 12pt,
    resource("Hit Points", ("Current", "Max", "Temp")),
    resource("Energy / NRG", ("Current", "Max")),
    resource("Luck", ("Current", "Max")),
    resource("AP", ("Current", "Max"))))
  place(dy: 266pt, block(width: 322pt, {
    text(font: goth, weight: 600, size: 17pt, "Defence")
    v(4pt)
    grid(columns: (48pt, 48pt, 56pt, 56pt, 48pt, 48pt), column-gutter: 3pt,
      write("Chest AD", h: 27pt), write("Chest AV", h: 27pt), write("DEX Pen", h: 27pt),
      write("Max SPD", h: 27pt), write("Shield AD", h: 27pt), write("Shield AV", h: 27pt))
  }))
  place(dx: 338pt, dy: 266pt, block(width: 202pt, {
    grid(columns: (auto, auto, 1fr), column-gutter: 7pt, align: horizon,
      text(font: goth, weight: 600, size: 17pt, "Wounds"),
      box(wound(s: 12pt) + h(5pt) + wound(s: 12pt) + h(5pt) + wound(s: 12pt)), [])
    v(4pt)
    write("Lingering Injuries", h: 27pt)
  }))
  place(dy: 325pt, block(width: 100%, {
    section("Weapons", seed: 2)
    ledger(("Weapon", "Hands", "Damage and Type", "Range", "Traits"),
      (130pt, 39pt, 140pt, 42pt, 1fr), 3, row: 26pt)
  }))
  place(dy: 448pt, block(width: 100%, {
    section("Inventory", seed: 3,
      right: box(width: 104pt, write("Coins", h: 18pt)))
    ledger(("Qty", "Item", "Equipped / Location", "Notes"),
      (30pt, 208pt, 115pt, 1fr), 12, row: 18pt)
  }))
})

#record-side("Hero Record / reverse", 2, {
  place(heading("Powers and Talents", "", reverse: true))
  place(dy: 44pt, block(width: 100%, {
    section("Powers", seed: 4)
    ledger(("Name / Tradition / Tier", "Cost / Range / Effect / Duration / Reference"),
      (146pt, 1fr), 7, row: 38pt, two-lines: true)
  }))
  place(dy: 358pt, block(width: 100%, {
    section("Talents and Special Abilities", seed: 5)
    ledger(("Name / Type / Level", "Cost / Effect / Duration / Reference"),
      (146pt, 1fr), 7, row: 32pt, two-lines: true)
  }))
  place(dy: 630pt, block(width: 100%, {
    section("Hero Details", seed: 7,
      right: box(width: 202pt, grid(columns: (85pt, 105pt), column-gutter: 12pt,
        write("Adventures", h: 18pt), write("Fate", h: 18pt))))
    v(22pt); writing-line()
    v(22pt); writing-line()
  }))
})
