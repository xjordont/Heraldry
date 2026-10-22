#import "expanded.typ": *
#import "hero.typ": GAINS, TRAIN, PAYOUT

#record-page("Hero Record / front", {
  identity(none); v(8pt); statistics(none); v(8pt); resources(none); v(8pt)
  grid(columns: (382pt, 150pt), column-gutter: 8pt,
    panel("Armour", {
      record-table(("Slot", "Item", "AD", "AV", "DEX Pen", "Max SPD"),
        (33pt, 1fr, 27pt, 27pt, 42pt, 44pt), 2, row: 22pt, first: ("Chest", "Shield"))
      v(4pt)
      text(size: 9pt, "Shield AD and AV apply only through Block. Use only the worse DEX Pen.")
    }, h: 110pt),
    panel("Wounds", {
      align(center, ticks(3, s: 15pt, gap: 8pt))
      v(7pt)
      cell("Lingering Injuries", h: 45pt)
    }, h: 110pt))
  v(8pt)
  panel("Weapons", {
    record-table(("P/O", "Weapon", "Hands", "Damage and Type", "Range", "Traits"),
      (25pt, 1.2fr, 37pt, 1.2fr, 38pt, 1.4fr), 3, row: 22pt)
    v(4pt)
    text(size: 9pt, "P = Primary. O = Off-Hand: exactly 1 base damage die. See 6.13.")
  })
  v(8pt)
  block(height: 1fr, grid(columns: (1fr, 1fr), column-gutter: 8pt,
    panel("Ancestry and Background", h: "fill", {
      cell("Ancestry Traits", h: 42pt)
      cell("Background Rule", h: 42pt)
      cell("Other Special Abilities", h: 42pt)
    }),
    panel("Carried Items", h: "fill", {
      ruled-area(h: 78pt, pitch: 26pt)
      v(8pt)
      grid(columns: (1fr, 1fr), column-gutter: 0pt,
        cell("Carried Coins", h: 40pt), block(width: 100%, height: 40pt, {
          place(cell("Party Leader", h: 40pt))
          place(dx: 7pt, dy: 19pt, check(s: 13pt))
        }))
    })))
})

#record-page("Hero Record / reverse", {
  reverse-heading("Powers and Progress")
  v(8pt)
  layout(sz => {
    let powers = panel("Known Powers", {
      record-table(("Power / Tradition", "Tier", "AP", "NRG", "Range", "Effect / Reference"),
        (83pt, 22pt, 22pt, 26pt, 33pt, 1fr), 6, row: 19pt)
    })
    let right-side = {
      panel("Equipped Items", {
        record-table(("Slot", "Item"), (43pt, 1fr), 11, row: 21pt,
          first: ("Chest", "Head", "Back", "Neck", "Waist", "Arms", "Feet", "Ring", "Ring", "Hand", "Hand"))
        v(5pt)
        small("Permanent Special Items")
        v(3pt)
        ticks(5, s: 11pt, gap: 6pt)
      })
      v(8pt)
      panel("Fate", {
        cell("Adventures", h: 24pt)
        v(6pt)
        grid(columns: (1fr, 1fr), row-gutter: 5pt,
          [#check(s: 9pt) #text(size: 9pt, "Died")], [#check(s: 9pt) #text(size: 9pt, "Retired")],
          [#check(s: 9pt) #text(size: 9pt, "Triumph")], [#check(s: 9pt) #text(size: 9pt, "Legendary Veteran")])
      })
    }
    let right-h = measure(block(width: 206pt, right-side)).height
    let powers-h = measure(block(width: 326pt, powers)).height
    let talents-h = right-h - powers-h - 8pt
    let row-h = (talents-h - 49pt) / 11
    grid(columns: (326pt, 206pt), column-gutter: 8pt,
      {
        powers
        v(8pt)
        panel("Talents and Special Abilities", h: talents-h, {
          record-table(("Type", "Name", "Effect / Level / Reference"),
            (57pt, 84pt, 1fr), 11, row: row-h)
        })
      }, right-side)
  })
  v(8pt)
  panel("Advancement Reference / 6.13 and 6.16", pad: 5pt, {
    table(columns: (30pt, 1fr, 44pt, 44pt), rows: (16pt,) + (12pt,) * 10,
      inset: (x: 4pt, y: 0pt), align: left + horizon, stroke: 0.4pt + rule-ink,
      fill: (_, y) => if y == 0 { label-fill } else { none },
      ..("Level", "Gain", "Train", "Retire").map(t => small(t)),
      ..range(10).map(i => (text(size: 9pt, str(i + 1)), text(size: 9pt, GAINS.at(i)),
        text(size: 9pt, TRAIN.at(i)), text(size: 9pt, PAYOUT.at(i)))).flatten())
    v(3pt)
    text(size: 9pt)[*Each level:* add Max HP per Level, gain its benefits, learn any class Power, and recalculate Initiative Bonus and Max NRG. Train [1 TAP] in the Town Phase.]
    v(2pt)
    text(size: 9pt)[*Archetype Abilities 1 and 2:* Martial: Martial Supremacy and Sunder. Hybrid: Martial Supremacy and +1 Primary Casting Score. Caster: Caster Supremacy and +4 Max NRG.]
  })
})
