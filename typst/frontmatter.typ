// Front and back matter: title page, how-to-use, generated contents, index.
#import "heraldry.typ": *
#import "cover.typ": front-cover, back-cover
#let edition = sys.inputs.at("edition", default: "print")

#let how-to-use = json("../editorial/how_to_use.json")
#let index-data = if sys.inputs.at("index", default: "on") == "on" { json("../build/index.json") } else { (entries: ()) }

#let title-page(title, subtitle, version) = page(header: none, footer: none, margin: (x: 0.9in, y: 0.9in))[
  #metadata("title") <frontmatter-start>
  #v(0.55in)
  #align(center)[
    #signature(s: 1.7in)
    #v(22pt)
    #set par(leading: 10pt, justify: false)
    #text(font: serif, weight: 700, size: 34pt, tracking: 0.12em, hyphenate: false, title.at(0))
    #v(6pt)
    #text(font: serif, weight: 600, size: 15pt, tracking: 0.32em, title.at(1))
    #v(14pt)
    #flourish(len: 96pt)
    #v(16pt)
    #block(width: 80%)[#set par(leading: 5pt, justify: false); #set text(font: fell, size: 13pt); #show emph: it => it.body; #subtitle]
    #v(1fr)
  ]
  #place(bottom + center, dy: -0.4in)[
    #set text(font: sans, size: 9pt, weight: 600)
    #version
  ]
]

// Contents: each chapter row carries its arms; sections beneath with dotted leaders.
#let toc-tab(loc) = {
  let os = query(<chapter-opener>).filter(m => m.location().page() == loc.page())
  if os.len() == 0 { none } else { opener-tab(os.first().value) }
}
#let toc-page() = {
  pagebreak(weak: true)
  block(width: 100%, below: 10pt)[
    #align(center)[
      #v(0.1in)
      #text(font: goth, weight: 600, size: 34pt)[Contents]
      #v(-6pt)
      #flourish(len: 70pt)
    ]
  ]
  set text(size: 10pt)
  set par(justify: false)
  show outline.entry.where(level: 1): it => {
    v(11pt, weak: true)
    block(sticky: true, below: 4pt)[
      #let n = toc-tab(it.element.location())
      #link(it.element.location())[#grid(columns: (22pt, 1fr, auto), column-gutter: 7pt, align: horizon,
        if n != none { arms(n, w: 20pt) } else { [] },
        text(font: goth, weight: 600, size: 14pt, it.element.body),
        text(font: sans, weight: 700, size: 10pt, it.page()))]
      #v(-3pt)
      #line(length: 100%, stroke: 0.6pt + ink)
    ]
  }
  show outline.entry.where(level: 2): it => {
    block(above: 3pt, below: 0pt, inset: (left: 29pt))[
      #set text(size: 9.5pt)
      #link(it.element.location())[#it.element.body #box(width: 1fr, repeat(text(fill: ink3)[.#h(3pt)])) #text(font: sans, size: 9.5pt, it.page())]
    ]
  }
  columns(2, gutter: gap, outline(title: none, depth: 2, indent: 0pt))
}

#let version-text = json("../build/cover.json").version
#let frontmatter(title: ("HERALDRY SKIRMISH", "THE DYING LANDS"), subtitle: [], version: []) = {
  if edition == "digital" {
    front-cover(title, emph(subtitle), version)
    page(header: none, footer: none, numbering: none)[]   // inside front cover (keeps recto/verso parity)
  }
  set page(numbering: "i")
  counter(page).update(1)
  title-page(title, subtitle, version)
  // verso of title: production/edition notice (verified information only)
  page(header: none)[
    #v(1fr)
    #set text(font: sans, size: 9pt, fill: ink)
    #set par(leading: 3pt, spacing: 6pt)
    #block(width: 70%)[
      #for p in how-to-use.colophon [#p #parbreak()]
    ]
  ]
  // How to use this book
  pagebreak(weak: true)
  align(center)[#v(0.1in) #text(font: goth, weight: 600, size: 34pt, how-to-use.title) #v(-6pt) #flourish(len: 70pt) #v(10pt)]
  columns(2, gutter: gap)[
    #for s in how-to-use.sections [
      #heading(level: 4, outlined: false, bookmarked: false, s.heading)
      #for p in s.paras [#p #parbreak()]
    ]
  ]
  toc-page()
}

#let mainmatter() = {
  pagebreak(to: "odd", weak: true)
  [#metadata("main") <mainmatter>]
}

#let index-page() = {
  if index-data.entries.len() == 0 { return }
  pagebreak(weak: true)
  block(width: 100%, below: 14pt)[
    #metadata("index") <chapter-opener>
    #v(0.1in)
    #align(center)[
      #arms(15, w: 40pt)
      #v(-2pt)
      #heading(level: 1, outlined: true, bookmarked: true, "Index") <index>
      #v(-6pt)
      #flourish(len: 70pt)
      #v(8pt)
      #block(width: 80%)[#set text(font: fell, size: 11pt); #set par(justify: false); #index-data.note]
    ]
  ]
  set text(font: sans, size: 9.5pt)
  set par(leading: 2.4pt, spacing: 2pt, hanging-indent: 10pt, justify: false)
  let pages-for(key) = {
    let hits = query(label("ix-" + key)).map(h => h.location())
    for hid in index-data.at("heads", default: (:)).at(key, default: ()) {
      let q = query(label(hid))
      if q.len() > 0 { hits.push(q.first().location()) }
    }
    let ps = hits.map(l => (n: counter(page).at(l).first(), loc: l))
    let seen = ()
    let out = ()
    for p in ps.sorted(key: p => p.n) {
      if p.n not in seen { seen.push(p.n); out.push(link(p.loc, str(p.n))) }
    }
    out.join(", ")
  }
  columns(3, gutter: 14pt)[
    #let letter = ""
    #for e in index-data.entries {
      let l = upper(e.term.first())
      if l != letter {
        letter = l
        block(above: 10pt, below: 4pt, sticky: true, grid(columns: (auto, 1fr), column-gutter: 5pt, align: horizon,
          box(fill: ink, inset: (x: 4pt, y: 2.5pt), text(font: goth, weight: 600, size: 13pt, fill: paper, l)), line(length: 100%, stroke: 0.4pt + ink3)))
      }
      block(above: 2.5pt, below: 0pt, breakable: false)[
        #text(weight: 600, e.term)#if e.keys.len() > 0 [, #context e.keys.map(k => pages-for(k)).join(", ")]#if e.at("see", default: none) != none [. #emph[See] #e.see]#if e.at("also", default: none) != none [. #emph[See also] #e.also]
      ]
      for s in e.at("sub", default: ()) {
        block(above: 1.5pt, below: 0pt, inset: (left: 9pt), breakable: false)[
          #s.term, #context s.keys.map(k => pages-for(k)).join(", ")
        ]
      }
    }
  ]
}

#let backmatter() = {
  index-page()
  if edition == "digital" {
    let cd = json("../build/cover.json")
    back-cover((lead: emph(cd.lead), facts: cd.facts), version-text)
  }
}
