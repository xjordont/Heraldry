// The 24 Basic Mode hero cards (Appendix B.4): the hero sheet's front, filled in, and a back that prints
// every remaining profile rule verbatim from typst/heroes/basic-heroes.json (tools/hero_cards.py).
// sys.inputs.hero: one Hero's name, or "all" for the full set in roster order.
#import "hero.typ": *

#let rules-head(t) = block(above: 9pt, below: 2pt, sticky: true, {
  text(font: goth, weight: 700, size: 13.5pt, t)
  v(-5pt)
  brush(weight: 1.6pt, seed: t.len())
})

#let back-rules(hr) = leaf(hr.name, "Basic Mode Hero", "Rules · Appendix B.4 · Side 2 of 2",
  face: "back", arm: 13, title-size: 24pt)[
  #set text(size: 10pt)
  #let body = {
    for s in hr.sections.filter(s => s.title != "Equipment and Items") {
      rules-head(s.title)
      for it in s.items { rule-item(it) }
    }
    let senses = hr.stats.at("Senses", default: none)
    if senses != none {
      let key = if senses.starts-with("Superior") { "Superior Darkvision" } else { "Darkvision" }
      let r = DATA.reminders.at(key)
      rules-head(r.head)
      block(above: 4pt, rich(r.runs))
    }
  }
  #block(above: -7pt, balanced-pair(body))
  #v(6pt)
  #sheet-head("Notes", seed: 11, right: "Conditions, ongoing effects, and reminders in pencil")
  #ruled(h: 1fr)
]

#let pick = sys.inputs.at("hero", default: "all")
#for hr in DATA.heroes.filter(x => pick == "all" or x.name == pick) {
  front(hr)
  back-rules(hr)
}
