// Front and back cover sheets (portrait US Letter, borderless background).
// Original vector heraldic device built from the book's broken-ring/tapered-rule motif.
#import "heraldry.typ": *

// Heater shield path, origin top-left, width w.
#let shield-path(w) = {
  let h = w * 1.18
  curve(
    curve.move((0pt, 0pt)),
    curve.line((w, 0pt)),
    curve.line((w, h * 0.42)),
    curve.cubic((w, h * 0.78), (w * 0.62, h * 0.93), (w * 0.5, h)),
    curve.cubic((w * 0.38, h * 0.93), (0pt, h * 0.78), (0pt, h * 0.42)),
    curve.close(),
  )
}

#let device(w: 220pt) = {
  let h = w * 1.18
  box(width: w, height: h)[
    // field: fine horizontal hatching below the fess, plain above
    #place(top + left, {
      // hatch, clipped to shield by drawing within a masked block
      let lines = range(0, 60).map(i => {
        let y = h * 0.5 + i * 2.6pt
        if y < h { place(top + left, dy: y, line(start: (0pt, 0pt), end: (w, 0pt), stroke: 0.45pt + ink)) }
      })
      box(width: w, height: h, clip: true, {
        for l in lines { l }
      })
    })
    // mask outside shield bottom curve with substrate-coloured shapes
    #place(top + left, curve(fill: substrate, stroke: 1.5pt + substrate,
      curve.move((-3pt, h * 0.42)), curve.line((0pt, h * 0.42)),
      curve.cubic((0pt, h * 0.78), (w * 0.38, h * 0.93), (w * 0.5, h)),
      curve.line((w * 0.5, h + 3pt)), curve.line((-3pt, h + 3pt)), curve.close()))
    #place(top + left, curve(fill: substrate, stroke: 1.5pt + substrate,
      curve.move((w + 3pt, h * 0.42)), curve.line((w, h * 0.42)),
      curve.cubic((w, h * 0.78), (w * 0.62, h * 0.93), (w * 0.5, h)),
      curve.line((w * 0.5, h + 3pt)), curve.line((w + 3pt, h + 3pt)), curve.close()))
    // fess line
    #place(top + left, dy: h * 0.5, line(start: (0pt, 0pt), end: (w, 0pt), stroke: 1.2pt + ink))
    // outlines
    #place(top + left, curve(stroke: 2.4pt + ink,
      curve.move((0pt, 0pt)), curve.line((w, 0pt)), curve.line((w, h * 0.42)),
      curve.cubic((w, h * 0.78), (w * 0.62, h * 0.93), (w * 0.5, h)),
      curve.cubic((w * 0.38, h * 0.93), (0pt, h * 0.78), (0pt, h * 0.42)), curve.close()))
    #place(top + left, dx: 7pt, dy: 7pt, curve(stroke: 0.6pt + ink,
      curve.move((0pt, 0pt)), curve.line((w - 14pt, 0pt)), curve.line((w - 14pt, h * 0.40)),
      curve.cubic((w - 14pt, h * 0.74), (w * 0.62 - 7pt, h * 0.88), (w * 0.5 - 7pt, h * 0.94)),
      curve.cubic((w * 0.38 - 7pt, h * 0.88), (0pt, h * 0.74), (0pt, h * 0.40)), curve.close()))
    // broken ring charge on a plain disc so the hatch does not run through it
    #let r = w * 0.27
    #place(top + left, dx: w / 2 - r - 6pt, dy: h * 0.44 - r - 6pt, circle(radius: r + 6pt, fill: substrate, stroke: none))
    #place(top + left, dx: w / 2 - r, dy: h * 0.44 - r,
      box(width: 2 * r, height: 2 * r, ring(size: 2 * r, stroke: 5pt)))
    // tapered blade through the ring
    #place(top + left, dx: w / 2 - 5pt, dy: h * 0.08,
      polygon(fill: ink, (0pt, 0pt), (10pt, 0pt), (5pt, h * 0.78)))
    #place(top + left, dx: w / 2 - 22pt, dy: h * 0.08 + 18pt, rect(width: 44pt, height: 4.5pt, fill: ink))
  ]
}

#let cover-page(body) = page(width: page-w, height: page-h, fill: substrate, margin: 0pt, header: none, footer: none, numbering: none, body)

#let front-cover(title, subtitle, version) = cover-page[
  // thin inset frame at a safe distance (decorative, inside the 0.375 in safe edge)
  #place(top + left, dx: 0.5in, dy: 0.5in, rect(width: page-w - 1in, height: page-h - 1in, stroke: 0.8pt + ink))
  #place(top + left, dx: 0.56in, dy: 0.56in, rect(width: page-w - 1.12in, height: page-h - 1.12in, stroke: 0.4pt + ink))
  #place(top + center, dy: 1.15in)[
    #set align(center)
    #set par(leading: 8pt)
    #text(font: display, weight: 700, size: 40pt, tracking: 0.03em, hyphenate: false, title.at(0))
    #v(2pt)
    #text(font: display, weight: 600, size: 21pt, tracking: 0.16em, title.at(1))
    #v(8pt)
    #motif(len: 120pt)
  ]
  // cover art from build/cover.json: generated ink art when selected, else ART-COVER-001 at native 300 ppi; title stays live type
  #let cart = json("../build/cover.json").art
  #place(center + horizon, dy: 0.45in, image(cart.path, width: cart.w_in * 1in, height: cart.h_in * 1in))
  #place(bottom + center, dy: -1.0in)[
    #set align(center)
    #block(width: 5.2in)[#set text(size: 13pt); #subtitle]
    #v(14pt)
    #text(font: sans, size: 11pt, weight: 600, tracking: 0.12em, version)
  ]
]

#let back-cover(copy, version) = cover-page[
  #place(top + left, dx: 0.5in, dy: 0.5in, rect(width: page-w - 1in, height: page-h - 1in, stroke: 0.8pt + ink))
  #place(top + left, dx: 0.56in, dy: 0.56in, rect(width: page-w - 1.12in, height: page-h - 1.12in, stroke: 0.4pt + ink))
  #place(top + center, dy: 1.25in, block(width: 5.4in)[
    #set align(center)
    #motif(len: 70pt)
    #v(16pt)
    #set par(leading: 5pt, justify: false)
    #set text(size: 12.5pt)
    #copy.lead
    #v(18pt)
    #line(length: 30%, stroke: 0.6pt + ink)
    #v(14pt)
    #set text(size: 11pt)
    #set par(leading: 4pt, spacing: 9pt)
    #for p in copy.facts [#p #parbreak()]
  ])
  #place(bottom + center, dy: -1.05in)[
    #set align(center)
    #device(w: 60pt)
    #v(10pt)
    #text(font: sans, size: 10pt, weight: 600, tracking: 0.12em, version)
  ]
]
