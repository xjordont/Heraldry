// Inkjet calibration sheet — diagnostic only; never part of the reader edition.
// Its edge markers intentionally sit inside the 0.375 in safe zone.
#import "heraldry.typ": *
#let revision = json("../source/versions.json").current
#let pt-label(value) = str(value / 1pt) + " pt"
#let minimum-size = publication.format.minimum_essential_text_pt * 1pt
// A real, unchanged paragraph from the active snapshot, not generated example prose.
#let source-lines = read("../" + publication.source).split("\n").map(line => line.trim())
#let body-samples = source-lines.filter(line => line.starts-with("The battlefield is never passive."))
#assert(body-samples.len() == 1, message: "Calibration source sample must resolve exactly once in the active manuscript.")
#set page(width: page-w, height: page-h, fill: substrate, margin: 0pt)
#set text(font: sans, size: 9.5pt, fill: ink)

// inset distance markers on all four edges at 0.125/0.25/0.375/0.5 in
#for (k, (d, lbl)) in ((0.125in, "1/8"), (0.25in, "1/4"), (0.375in, "3/8 SAFE"), (0.5in, "1/2")).enumerate() {
  let st = if lbl.contains("SAFE") { 1pt + ink } else { (paint: ink, thickness: 0.5pt, dash: "dashed") }
  place(top + left, dx: d, dy: d, rect(width: page-w - 2 * d, height: page-h - 2 * d, stroke: st))
  place(top + left, dx: 1.2in + k * 1.1in, dy: d + 1.5pt, text(size: 6.5pt, lbl + " in"))
}
#place(top + left, dx: 0.75in, dy: 0.75in, block(width: page-w - 1.5in)[
  #text(font: display, weight: 700, size: 20pt)[Inkjet Calibration: #("RC" + str(revision))]
  #v(-4pt)
  #text(size: 9.5pt)[Print at Letter portrait, 100% / Actual size, borderless on. Diagnostic sheet only (edge markers intentionally violate the book's 0.375 in safe edge). Substrate of this file: #substrate-name.]
  #v(8pt)
  #grid(columns: (1fr, 1fr), gutter: 18pt,
    [
      *1-inch square and ruler* \
      #v(4pt)
      #rect(width: 1in, height: 1in, stroke: 0.75pt + ink)
      #v(4pt)
      #box(width: 3in, height: 18pt, {
        place(line(start: (0pt, 0pt), end: (3in, 0pt), stroke: 0.6pt))
        for i in range(0, 25) {
          let x = i * 0.125in
          let l = if calc.rem(i, 8) == 0 { 12pt } else if calc.rem(i, 4) == 0 { 8pt } else { 4pt }
          place(dx: x, line(start: (0pt, 0pt), end: (0pt, l), stroke: 0.5pt))
          if calc.rem(i, 8) == 0 { place(dx: x + 2pt, dy: 9pt, text(size: 7pt, str(int(i / 8)))) }
        }
      })
      #v(10pt)
      *Type sizes* \
      #text(font: serif, size: 9pt)[9 pt Source Serif 4: 1d6 + APL/2 [1 AP] 36"×36" ±×] \
      #text(font: serif, size: 9.5pt)[9.5 pt Source Serif 4: Advantage, Cover, Engaged] \
      #text(font: serif, size: body-size)[#pt-label(body-size) #serif: body text size] \
      #text(font: sans, size: minimum-size)[#pt-label(minimum-size) #sans: essential minimum 0123456789] \
      #text(font: sans, size: table-size)[#pt-label(table-size) #sans: table text 0123456789] \
      #text(font: display, size: 21pt, weight: 600)[21 pt Grenze Gotisch section heading]
      #v(10pt)
      *Current source sample (1.1)* \
      #block({
        set text(font: serif, size: body-size, lang: "en", region: "CA", hyphenate: true)
        set par(leading: body-lead, justify: true)
        text(body-samples.first())
      })
      #v(10pt)
      *Rule weights* \
      #for w in (0.3pt, 0.45pt, 0.6pt, 0.75pt, 1pt) [
        #box(width: 2.2in, line(length: 100%, stroke: w + ink)) #h(6pt) #text(size: 8.5pt)[#repr(w)] \
      ]
    ],
    [
      *Table bands* \
      #v(4pt)
      #block({
      set text(font: sans, size: table-size)
      set par(leading: table-lead)
      table(columns: (0.5in, 1fr), inset: 4pt, stroke: (x, y) => (bottom: 0.3pt + rgb(0,0,0,22%)),
        fill: (x, y) => if calc.even(y) { band } else { none },
        [*d6*], [*Result (active table band)*], [1], [Row text at #pt-label(table-size)], [2], [Banded row], [3], [Row text], [4], [Banded row])
      })
      #v(4pt)
      #block(fill: ink, inset: 4pt, head-cell([Current table header]))
      #v(10pt)
      *Substrate comparison* \
      #v(4pt)
      #grid(columns: 2, gutter: 8pt,
        rect(width: 1.3in, height: 0.8in, fill: rgb("#FCFAF5"), stroke: 0.5pt)[#text(size: 8pt)[cream \#FCFAF5]],
        rect(width: 1.3in, height: 0.8in, fill: rgb("#FFFFFF"), stroke: 0.5pt)[#text(size: 8pt)[white \#FFFFFF]])
      #v(10pt)
      *Hatch survival* (0.3–0.6 pt lines at 1.6–3 pt pitch) \
      #v(4pt)
      #for (pitch, w) in ((1.6pt, 0.3pt), (2.2pt, 0.4pt), (3pt, 0.6pt)) {
        box(width: 0.9in, height: 0.9in, clip: true, stroke: 0.5pt, {
          for i in range(0, 120) {
            place(dx: -0.9in + i * pitch, line(start: (0pt, 0.9in), end: (0.9in, 0pt), stroke: w + ink))
          }
        })
        h(6pt)
      }
      #v(10pt)
      *Grayscale steps* \
      #for g in (100%, 90%, 80%, 65%, 50%, 35%, 20%, 0%) {
        box(width: 0.3in, height: 0.3in, fill: luma(g), stroke: 0.3pt)
      }
    ],
  )
  #v(10pt)
  #line(length: 100%, stroke: 0.5pt)
  #text(size: 9pt)[Check after printing: the 1-inch square measures 1 in; the solid 3/8 in SAFE frame is fully visible on all four sides (if the driver's borderless expansion crops it, the book's folios and text may be at risk, so reduce expansion); 9 pt type and 0.3 pt rules are legible; bands are visible but light; hatch lines remain separate; the cream tone reaches all edges without white bands.]
])
