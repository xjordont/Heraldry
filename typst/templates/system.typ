// HERALDRY SKIRMISH — book design system v4 ("Grim Heraldry", refined).
// Page templates and components for every page type in the book; the plan and rationale are in
// docs/BOOK_DESIGN_PLAN.md, the reference evidence in docs/design/REFERENCE_STUDY.md.
// Self-contained: specimens use it today, and the book build adopts it component by component.
//
// Direction (owner 2026-10-12): ornate, grim, medieval heraldry; tasteful; never distracting from
// text or art; clarity, ease of use and no page bloat first. Ornament lives at boundaries only.

// Owner 2026-10-16: compact v5 profile supersedes the earlier 11 pt lock.
// ================================================================ tokens
#let substrate-name = sys.inputs.at("substrate", default: "cream")
#let paper = if substrate-name == "white" { rgb("#FFFFFF") } else { rgb("#FCFAF5") }
#let ink = rgb(0, 0, 0)
#let ink2 = luma(16%)                 // flavour text: near-black so it reads as easily as rules
#let ink3 = luma(42%)                 // furniture labels and quiet numbers
#let hair = rgb(0, 0, 0, 24%)         // row hairlines
#let tint = rgb(0, 0, 0, 5%)          // banding, examples, panels (transparent: cream and white)
#let tint2 = rgb(0, 0, 0, 9%)         // die column of roll tables

#let profile = json("../../config/design_tokens.json")
#let type-token = profile.type_pt
#let space-token = profile.spacing_pt
#let serif = profile.fonts.body
#let sans = profile.fonts.table_label
#let goth = profile.fonts.display
#let fell = profile.fonts.flavour

#let page-w = profile.page.width_pt * 1pt
#let page-h = profile.page.height_pt * 1pt
#let m-in = profile.page.inside_margin_pt * 1pt
#let m-out = profile.page.outside_margin_pt * 1pt
#let m-top = profile.page.top_margin_pt * 1pt
#let m-bot = profile.page.bottom_margin_pt * 1pt
#let gap = profile.page.column_gap_pt * 1pt
#let frame-w = page-w - m-in - m-out
#let col-w = (frame-w - gap) / 2

#let body-size = type-token.body * 1pt
#let body-lead = type-token.body_leading_additive * 1pt
#let table-size = type-token.table * 1pt
#let table-lead = type-token.table_leading_additive * 1pt
#let table-x = space-token.table_horizontal_padding * 1pt
#let table-y = space-token.table_vertical_padding * 1pt
#let par-space = space-token.paragraph_after * 1pt
#let list-space = space-token.list_item * 1pt
#let aside-size = body-size
#let aside-lead = body-lead
#let dossier-size = body-size

// ================================================================ the armoury (original vector marks)
#let mark(name) = "marks/" + substrate-name + "/" + name + ".svg"
#let lozenge(size: 6pt, fill: ink) = box(width: size, height: size, baseline: 0.05em,
  polygon(fill: fill, (size / 2, 0pt), (size, size / 2), (size / 2, size), (0pt, size / 2)))

// Brush rule: a hand-inked stroke with tapered ends and a slightly uneven edge (deterministic, so
// every printing is identical). Replaces plain rules at structural boundaries.
#let brush(weight: 2pt, seed: 0) = layout(size => {
  let w = size.width
  let n = calc.max(12, int(w / 6pt))
  let mid = weight
  let taper(x) = calc.pow(calc.max(0.0, calc.min(1.0, calc.min(x / (0.06 * w), (w - x) / (0.06 * w)))), 0.55)
  let top = ()
  let bot = ()
  for i in range(n + 1) {
    let x = w * i / n
    let t = taper(x)
    let a = 1 + 0.16 * calc.sin(i * 1.71 + seed) + 0.08 * calc.sin(i * 0.53 + seed * 2)
    let b = 1 + 0.14 * calc.sin(i * 1.29 + seed + 1.3) + 0.08 * calc.sin(i * 0.41 + seed)
    top.push((x, mid - weight / 2 * t * a))
    bot.push((x, mid + weight / 2 * t * b))
  }
  box(width: w, height: 2 * weight, polygon(fill: ink, ..top, ..bot.rev()))
})

// Coin: a medieval long-cross penny (beaded rim, voided long cross, a pellet in each angle); stands
// for the source's "c". It sits on the baseline so it aligns with the figures beside it.
#let coin(s: 7pt, fill: ink) = box(baseline: 0pt, image(mark(if fill == ink { "coin" } else { "coin-reversed" }), width: s))

// Heater shield outline as a curve (w x h at dx, dy).
#let shield-curve(w, h, dx: 0pt, dy: 0pt, fill: none, stroke: none) = place(dx: dx, dy: dy, curve(fill: fill, stroke: stroke,
  curve.move((0pt, 0pt)), curve.line((w, 0pt)), curve.line((w, h * 0.42)),
  curve.cubic((w, h * 0.78), (w * 0.62, h * 0.9), (w * 0.5, h)),
  curve.cubic((w * 0.38, h * 0.9), (0pt, h * 0.78), (0pt, h * 0.42)), curve.close()))

// Shield with an optional body (a number) and an engraved inner line.
#let shield(w: 14pt, fill: ink, stroke: none, inner: false, body: none) = box(width: w, height: w * 1.18, baseline: 20%, {
  let h = w * 1.18
  shield-curve(w, h, fill: fill, stroke: stroke)
  if inner { let k = w * 0.1; shield-curve(w - 2 * k, h - 2.3 * k, dx: k, dy: k, stroke: 0.45pt + paper) }
  if body != none { place(center + top, dy: h * 0.15, box(width: w, align(center, body))) }
})

// Chapter arms and the logo: the owner-approved marks (production/art/marks/APPROVED.json), traced by
// tools/prepare_marks.py onto one shared shield. Owner 2026-10-13: "Make sure they are big enough to see."
#let arms(n, w: 16pt) = box(baseline: 22%, image(mark("arms-" + (if n < 10 { "0" } else { "" }) + str(n)), width: w))

// Signature mark: the book's logo, the broken shield bearing a castle (owner-approved 2026-10-13).
#let signature(s: 14pt) = box(baseline: 15%, image(mark("logo"), width: s))
#let crown(s: 12pt, fill: ink) = signature(s: s)

// Corner flourish: a fine L with an inner hairline and a lozenge finial at each arm and the angle.
#let corner(which, s: 15pt) = box(width: s, height: s, {
  let fx = if which.ends-with("r") { (x) => s - x } else { (x) => x }
  let fy = if which.starts-with("b") { (y) => s - y } else { (y) => y }
  let p(x, y) = (fx(x), fy(y))
  place(line(start: p(0pt, 0pt), end: p(s - 3pt, 0pt), stroke: 1.2pt + ink))
  place(line(start: p(0pt, 0pt), end: p(0pt, s - 3pt), stroke: 1.2pt + ink))
  place(line(start: p(3pt, 3pt), end: p(s * 0.62, 3pt), stroke: 0.4pt + ink))
  place(line(start: p(3pt, 3pt), end: p(3pt, s * 0.62), stroke: 0.4pt + ink))
  let lz(c, d) = place(dx: c.at(0) - d / 2, dy: c.at(1) - d / 2, polygon(fill: ink, (d / 2, 0pt), (d, d / 2), (d / 2, d), (0pt, d / 2)))
  lz(p(0pt, 0pt), 5pt)
  lz(p(s - 2pt, 0pt), 3.4pt)
  lz(p(0pt, s - 2pt), 3.4pt)
})

#let cornered(body, fill: none, inset: (x: 11pt, y: 10pt), s: 14pt) = block(width: 100%, breakable: false, fill: fill, {
  block(width: 100%, inset: inset, spacing: 0pt, body)
  place(top + left, corner("tl", s: s))
  place(top + right, corner("tr", s: s))
  place(bottom + left, corner("bl", s: s))
  place(bottom + right, corner("br", s: s))
})

// Ornamental break: brush — crown — brush. Ends a chapter's last section, opens title pages.
#let flourish(len: 70pt) = box(baseline: 30%,
  grid(columns: (len, auto, len), column-gutter: 6pt, align: horizon,
    brush(weight: 1.6pt, seed: 1), crown(s: 22pt), brush(weight: 1.6pt, seed: 2)))

// Label with a fine rule running to the margin: the entry-anatomy separator.
#let label-rule(body, size: 7.4pt) = block(above: 8pt, below: 3.5pt, sticky: true, width: 100%,
  grid(columns: (auto, 1fr), column-gutter: 6pt, align: horizon,
    text(font: sans, weight: 700, size: size, tracking: 0.14em, upper(body)),
    line(length: 100%, stroke: 0.5pt + ink)))

// Banner tag: a short black strap with a pointed right end.
#let tag(body, size: 7pt) = box({
  let t = text(font: sans, weight: 700, size: size, tracking: 0.16em, fill: paper, upper(body))
  context {
    let m = measure(t)
    let h = m.height + 6pt
    let w = m.width + 14pt
    box(width: w, height: h, {
      place(polygon(fill: ink, (0pt, 0pt), (w - 5pt, 0pt), (w, h / 2), (w - 5pt, h), (0pt, h)))
      place(left + horizon, dx: 5pt, t)
    })
  }
})

// Drop capital: blackletter initial reversed in an engraved black block, three lines deep
// (vendored droplet 0.3.1, MIT, typst/vendor/).
#import "../vendor/droplet-0.3.1/src/lib.typ": dropcap as _dropcap
#let dropcap(body, lines: 3) = _dropcap(height: lines, gap: 6pt, hanging-indent: 0pt,
  transform: letter => box(fill: ink, inset: 1.6pt, box(stroke: 0.45pt + paper, inset: (x: 4.5pt, top: 3pt, bottom: 4pt),
    text(font: goth, weight: 600, fill: paper, letter))), body)

// ================================================================ running furniture
// Chapter tabs: tall pennants on the outer edge, one fixed slot per part, each carrying its
// keyword in blackletter, bold and centred, rotated to run along the edge (owner 2026-10-12).
#let tab-keys = ("World", "Mechanics", "Round", "Actions", "Combat", "Party", "Equipment", "Powers",
  "Monsters", "Scenarios", "Campaign", "Learn", "Basic", "Reference", "Index")
#let thumb-tab(n, recto) = {
  let top0 = 0.4in
  // End the navigation ladder above the lower folio, not near the trim.
  let tab-bottom = page-h - m-bot - 12pt
  let slot-h = (tab-bottom - top0) / tab-keys.len()
  let y = top0 + slot-h * (n - 1)
  // Decoration remains wholly outside the body frame, with clearance so that full-measure
  // lines and table rules never touch the tab (design review 2026-10-29).
  let w = m-out - profile.page.thumb_tab_clearance_pt * 1pt
  let h = slot-h - 3pt
  let k = 4.5pt                                 // bevelled inner corners
  let pts = if recto { ((w, 0pt), (k, 0pt), (0pt, k), (0pt, h - k), (k, h), (w, h)) }
            else { ((0pt, 0pt), (w - k, 0pt), (w, k), (w, h - k), (w - k, h), (0pt, h)) }
  let inner = if recto { ((w, 1.8pt), (k + 0.6pt, 1.8pt), (1.8pt, k + 0.6pt), (1.8pt, h - k - 0.6pt), (k + 0.6pt, h - 1.8pt), (w, h - 1.8pt)) }
              else { ((0pt, 1.8pt), (w - k - 0.6pt, 1.8pt), (w - 1.8pt, k + 0.6pt), (w - 1.8pt, h - k - 0.6pt), (w - k - 0.6pt, h - 1.8pt), (0pt, h - 1.8pt)) }
  let avail = h - 4pt
  let word = context {
    let s = type-token.navigation * 1pt
    let t = text(font: goth, weight: 700, size: s, fill: paper, tab-keys.at(n - 1))
    assert(s >= type-token.minimum_essential * 1pt, message: "Navigation type is below the essential floor")
    assert(measure(t).width <= avail, message: "Navigation keyword exceeds its slot at the approved size")
    t
  }
  // The lettering sits against the essential safe line, 27 pt in from the trim, and reaches toward
  // the text frame; the tab itself stops short of the frame by the clearance token.
  let safe = profile.page.essential_edge_safe_pt * 1pt
  let face = 12.9pt                              // the keyword's line box at 9 pt Grenze Gotisch
  place(top + left, dx: if recto { page-w - w } else { 0pt }, dy: y, box(width: w, height: h, {
    place(polygon(fill: ink, ..pts))
    place(polygon(fill: none, stroke: 0.45pt + paper, ..inner))
    // 1.5 pt outward centres the ink (not the font's tall metric box) between the safe line and
    // the engraved inner line; the verifiers check rotated keywords by their glyph outlines.
    let shift = 1.5pt
    place(top + left, dx: if recto { w - safe - face + shift } else { safe - shift }, box(width: face, height: h,
      align(center + horizon, rotate(if recto { 90deg } else { -90deg }, reflow: true,
        box(width: h, align(center, word))))))
  }))
}

// Running head: label at the outer end with the chapter's arms; a thick-and-thin rule.
#let running-head(left-text, right-text, recto, tab: none) = {
  set text(font: sans, size: type-token.navigation * 1pt, weight: 600, tracking: 0.12em, fill: ink2)
  let a = if tab != none { box(baseline: 30%, arms(tab, w: 15pt)) } else { lozenge(size: 4.4pt) }
  block(width: 100%, below: 0pt, {
    if recto [#h(1fr)#upper(right-text)#h(6pt)#a] else [#a#h(6pt)#upper(left-text)#h(1fr)]
    v(2.5pt)
    line(length: 100%, stroke: 1.1pt + ink)
    v(-4.6pt)
    line(length: 100%, stroke: 0.35pt + ink)
  })
}

// Folio: page number in an engraved black shield at the outer corner, a short brush toward the gutter.
#let folio(n, recto) = {
  let sh = shield(w: 23pt, inner: true, body: text(font: sans, size: type-token.navigation * 1pt, weight: 700, fill: paper, number-type: "lining", str(n)))
  let b = box(width: 40pt, baseline: -6pt, brush(weight: 1.2pt, seed: n))
  if recto { align(right)[#b#h(5pt)#sh] } else { align(left)[#sh#h(5pt)#b] }
}

// Opener frame: double border with corner flourishes, the broken crown at the head and the
// folio shield at the foot. Chapter openers only.
#let opener-frame(recto, n: none) = {
  let x0 = 0.42in
  let y0 = 0.42in
  let w = page-w - 2 * x0
  let h = page-h - 2 * y0
  place(top + left, dx: x0, dy: y0, box(width: w, height: h, {
    place(rect(width: w, height: h, stroke: 1.4pt + ink))
    place(dx: 3.5pt, dy: 3.5pt, rect(width: w - 7pt, height: h - 7pt, stroke: 0.4pt + ink))
    place(top + left, dx: 7pt, dy: 7pt, corner("tl", s: 26pt))
    place(top + right, dx: -7pt, dy: 7pt, corner("tr", s: 26pt))
    place(bottom + left, dx: 7pt, dy: -7pt, corner("bl", s: 26pt))
    place(bottom + right, dx: -7pt, dy: -7pt, corner("br", s: 26pt))
    place(top + center, dy: -15pt, box(fill: paper, inset: (x: 6pt), crown(s: 30pt)))
    if n != none {
      place(bottom + center, dy: 12pt, box(fill: paper, inset: (x: 5pt),
        shield(w: 23pt, inner: true, body: text(font: sans, size: 9pt, weight: 700, fill: paper, str(n)))))
    }
  }))
}

// A page shell for specimens: furniture comes from explicit arguments (the book derives it).
#let shell(n, chapter: "", section: "", tab: none, furniture: true, folio-on: true, frame: false, body) = {
  let recto = calc.odd(n)
  set page(width: page-w, height: page-h, fill: paper,
    margin: if recto { (left: m-in, right: m-out, top: m-top, bottom: m-bot) }
            else { (left: m-out, right: m-in, top: m-top, bottom: m-bot) },
    header: if furniture { running-head(chapter, section, recto, tab: tab) },
    header-ascent: 14pt,
    footer: if folio-on and not frame { folio(n, recto) },
    footer-descent: 2pt,
    background: {
      if frame { opener-frame(recto, n: if folio-on { n }) }
      if tab != none { thumb-tab(tab, recto) }
    },
  )
  body
}

// ================================================================ base text and typesetting policy
// Paragraph policy (docs/BOOK_DESIGN_PLAN.md section 13): no widows or orphans, no one-word last
// lines ("runts"), hyphenation discouraged but allowed in narrow columns. Body text is justified
// within limits (owner 2026-10-12); --body rag in the specimen renderer shows the ragged alternative.
#let base(body) = {
  set text(font: serif, size: body-size, lang: "en", region: "CA", fill: ink, hyphenate: true, overhang: false,
    top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining",
    costs: (hyphenation: 100%, runt: 160%, widow: 1000%, orphan: 1000%))
  set par(leading: body-lead, spacing: par-space, justify: sys.inputs.at("body", default: "justify") == "justify", first-line-indent: 0pt,
    justification-limits: (spacing: (min: 90%, max: 140%), tracking: (min: -0.005em, max: 0.02em)))
  set strong(delta: 200)
  set list(marker: (box(baseline: -1.2pt, lozenge(size: 4.4pt)), [–]), indent: 1pt, body-indent: 6pt, spacing: list-space)
  set enum(indent: 1pt, body-indent: 6pt, spacing: list-space, numbering: n => text(font: sans, weight: 700, size: 9pt)[#n.])
  // A list item (a talent, a package, a step) is a reference entry: it never splits across a column or page.
  show list.item: it => block(breakable: false, it)
  show enum.item: it => block(breakable: false, it)
  body
}

// Balanced columns: two columns of equal depth. Used wherever a run ends on the page (a section's
// close, an excerpt, lore), so no column stands half empty beside a full one.
// The depth is half the single-column depth plus one line of allowance. When the page has less room
// than that but still more than half the depth plus a quarter line, the block takes exactly the room
// left, so a near-full page never pushes an empty frame onto the next page.
#let balanced(body, gutter: gap, slack: 2pt) = layout(size => {
  let w = (size.width - gutter) / 2
  let h = measure(block(width: w, body)).height
  let pitch = body-size * 1.05 + body-lead
  let target = h / 2 + pitch + slack
  let room = page.height - m-bot - here().position().y
  let depth = if target > room and room >= h / 2 + pitch / 4 { room } else { target }
  block(width: 100%, height: depth, columns(2, gutter: gutter, body))
})

// ================================================================ headings
// Numbered section (x.y): number in an engraved shield, blackletter title, brush rule beneath.
#let section(num, title) = block(above: 6pt, below: 12pt, sticky: true, width: 100%, breakable: false)[
  #set par(justify: false)
  #grid(columns: (auto, 1fr), column-gutter: 10pt, align: horizon,
    shield(w: 24pt, inner: true, body: text(font: sans, weight: 700, size: if num.len() > 3 { 7.4pt } else { 8.8pt }, fill: paper, num)),
    text(font: goth, weight: 600, size: 24pt, hyphenate: false, title))
  #v(3pt)
  #brush(weight: 2.2pt, seed: num.len())
]

// Subsection (x.y.z): serif bold with a quiet sans number after a small lozenge.
#let subsection(num, title) = block(above: 14pt, below: 5pt, sticky: true)[
  #set par(justify: false)
  #lozenge(size: 5.5pt)#h(5pt)#if num != none [#text(font: sans, weight: 700, size: 9.5pt, fill: ink3, num)#h(5pt)]#text(font: serif, weight: 700, size: 12.5pt, title)
]

// Minor named heading inside a subsection.
#let minor(title) = block(above: 11pt, below: 3pt, sticky: true, text(font: goth, weight: 600, size: 14pt, title))

// Run-in label for definition-style paragraphs ("Primary Objective:" etc.).
#let runin(label, body) = par[#text(weight: 700, label)#h(0.3em)#body]

// ================================================================ text components
// Flavour: one size and one set of rules everywhere (owner 2026-10-12): IM FELL roman 12 pt,
// near-black, paragraphs separated by a clear space. Section-level flavour (`lead-block`) sits in
// a single column of 80% measure; entry flavour (`flavour`) fills its column. Both are justified
// (a soft, book-like block) unless the specimens are rendered with --input lead=center.
#let flav-size = body-size
#let lead-mode = sys.inputs.at("lead", default: "justify")
#let flavour-set(body) = {
  set par(justify: lead-mode == "justify", leading: space-token.flavour_leading_additive * 1pt, spacing: space-token.flavour_paragraph_after * 1pt,
    justification-limits: (spacing: (min: 90%, max: 140%), tracking: (min: -0.005em, max: 0.02em)))
  set text(font: fell, size: flav-size, fill: ink2, hyphenate: lead-mode == "justify")
  body
}
#let flavour(body, size: none) = block(above: 5pt, below: 9pt, flavour-set(body))
#let lead-block(body, size: none, width: 80%) = block(width: 100%, above: space-token.lead_above * 1pt, below: space-token.lead_below * 1pt,
  align(center, block(width: width, align(if lead-mode == "justify" { left } else { center }, flavour-set(body)))))

// Entry title: the banner tag always stands directly above the top-left corner of its title,
// 5 pt clear of the title's cap height, whether the title is set left or centred (owner 2026-10-12).
// The title box is cut to cap height and baseline so the spacing is exact for every face and size.
#let entry-title(name, tag-text, size: 21pt, al: left, tag-size: 6.8pt) = block(width: 100%, above: 0pt, below: 4pt, sticky: true,
  align(al, box(stack(dir: ttb, spacing: 5pt,
    align(left, tag(tag-text, size: tag-size)),
    text(font: goth, weight: 600, size: size, hyphenate: false, top-edge: "cap-height", bottom-edge: "baseline", name)))))

// Set-apart panel shared by worked examples and rules notes (owner 2026-10-12): tinted field on a
// black spine, the banner tag at the top left, body text at the running size.
#let panel(label, body) = block(width: 100%, above: space-token.panel_above * 1pt, below: space-token.panel_below * 1pt, breakable: false,
  fill: tint, stroke: (left: 2.6pt + ink), inset: (x: space-token.panel_horizontal_padding * 1pt, y: space-token.panel_vertical_padding * 1pt))[
  #tag(label)
  #v(3pt)
  #set text(size: aside-size)
  #set par(leading: aside-lead)
  #body
]
#let example(title: none, body) = panel([Example#if title != none [ #h(2pt)·#h(2pt) #title]], body)
// Rules note: the example panel with its own tag ("RULES NOTE", "CLARIFICATION", "DESIGN NOTE").
#let note-box(tag-text: "Rules Note", body) = panel(tag-text, body)

// Procedure: numbered steps on small black shields.
#let procedure(title: none, steps) = block(width: 100%, above: 9pt, below: 10pt, breakable: true)[
  #if title != none { label-rule(title) }
  #for (i, s) in steps.enumerate() {
    block(above: 5pt, below: 5pt, breakable: false,
      grid(columns: (17pt, 1fr), column-gutter: 6pt,
        shield(w: 15pt, body: text(font: sans, weight: 700, size: 8pt, fill: paper, str(i + 1))),
        s))
  }
]

// ================================================================ tables: the ledger
// Reading first (Deth Wizards p22 and BlackDeathCity p66 lessons): values centred under centred
// headings, long text left-aligned, the key column bold and left; a black header band; light
// banding and hairlines; no vertical rules; a brush stroke above and below. Every visual choice
// serves finding a row and reading across it.
#let table-title(body) = block(below: 4pt, sticky: true, width: 100%,
  text(font: goth, weight: 600, size: 15.5pt, body))

// aligns: one of "key" (bold, left), "text" (left), "c" (centre) per column. Header labels follow.
#let ref-table(widths, aligns, header, rows, title: none, roll: false, band: true, notes: none, size: table-size) = {
  set text(font: sans, size: size, number-type: "lining", number-width: "tabular", hyphenate: false)
  set par(leading: table-lead, spacing: par-space, justify: false)
  let n = header.len()
  let al(x) = { let a = aligns.at(x, default: "text"); if a == "c" or a == "roll" { center } else { left } }
  let cells = ()
  for (i, row) in rows.enumerate() {
    cells += row.enumerate().map(((x, c)) => {
      let a = aligns.at(x, default: "text")
      table.cell(if a == "key" { text(weight: 700, c) } else if a == "roll" { text(weight: 700, size: size + 1pt, c) } else { c })
    })
    if notes != none and notes.at(i, default: none) != none {
      cells.push(table.cell(colspan: n, inset: (left: 16pt, right: 6pt, top: 0pt, bottom: 4.5pt),
        text(size: calc.max(type-token.minimum_essential * 1pt, size - 0.6pt), fill: ink2, notes.at(i))))
    }
  }
  let head = header.enumerate().map(((i, h)) => table.cell(align: al(i) + horizon,
    text(weight: 700, size: table-size, tracking: 0.04em, fill: paper, if type(h) == str { upper(h) } else { h })))
  block(width: 100%, above: space-token.table_above * 1pt, below: space-token.table_below * 1pt, breakable: true)[
    #if title != none { table-title(title) }
    #brush(weight: 2.4pt, seed: 3)
    #v(-2.2pt)
    #table(
      columns: widths,
      align: (x, y) => al(x) + horizon,
      inset: (x: table-x, y: table-y),
      fill: (x, y) => if y == 0 { ink } else if aligns.at(x, default: "") == "roll" { tint2 } else if band and calc.even(y) { tint } else { none },
      stroke: (x, y) => (bottom: if y == 0 { none } else { 0.35pt + hair }),
      table.header(repeat: true, ..head),
      ..cells,
    )
    #v(-1pt)
    #brush(weight: 2.4pt, seed: 5)
  ]
}

// ================================================================ figures and art
// Caption welded to the figure: a black band with the number and title, the caption beneath.
#let figure-block(id, title, file, caption, width: 100%) = block(width: 100%, above: 10pt, below: 12pt, breakable: false)[
  #align(center, image(file, width: width))
  #v(4pt)
  #block(width: 100%, fill: ink, inset: (x: 7pt, y: 3.6pt), spacing: 0pt,
    text(font: sans, size: 9pt, weight: 700, tracking: 0.1em, fill: paper)[#id #h(4pt)#lozenge(size: 4pt, fill: paper)#h(4pt) #upper(title)])
  #block(width: 100%, inset: (x: 6pt, top: 4.5pt, bottom: 5pt), spacing: 0pt, {
    set text(font: sans, size: 9pt)
    set par(leading: 2.5pt, justify: false)
    caption
  })
  #line(length: 100%, stroke: 0.6pt + ink)
]

#let spot(file, width: 100%) = block(width: 100%, above: 6pt, below: 8pt, breakable: false,
  align(center, image(file, width: width)))

// ================================================================ profiles and entries
#let cost-tag(body) = box(fill: ink, inset: (x: 4pt, top: 2.4pt, bottom: 1.8pt), baseline: 0.15em,
  text(font: sans, weight: 700, size: 7.2pt, tracking: 0.08em, fill: paper, body))

// Stat bar: black label row, values centred beneath in large sans, brush close.
#let stat-strip(header, values, size: 12pt) = block(width: 100%, above: 7pt, below: 6pt, breakable: false, {
  set text(font: sans, number-type: "lining", number-width: "tabular")
  set par(justify: false)
  grid(columns: (1fr,) * header.len(), column-gutter: 0pt, row-gutter: 0pt,
    ..header.map(h => block(width: 100%, fill: ink, inset: (y: 3pt), align(center,
      text(size: 6.8pt, weight: 700, tracking: 0.14em, fill: paper, h)))),
    ..values.enumerate().map(((i, v)) => block(width: 100%, inset: (x: 2pt, top: 4pt, bottom: 3.6pt),
      stroke: if i > 0 { (left: 0.4pt + hair) } else { none },
      align(center, text(size: size, weight: 600, v)))))
  v(-1pt)
  brush(weight: 2pt, seed: 7)
})

// Formula profile (scenario-scaled monsters): black label column, values in prose.
#let stat-card(header, values) = block(width: 100%, above: 7pt, below: 7pt, breakable: false, {
  set text(font: sans, size: 9pt, number-type: "lining")
  set par(justify: false, leading: 2.5pt)
  table(columns: (auto, 1fr), inset: (x: 6pt, y: 3.6pt), stroke: (x, y) => (bottom: 0.35pt + hair),
    fill: (x, y) => if x == 0 { ink } else if calc.odd(y) { tint } else { none },
    ..header.zip(values).map(((h, v)) => (text(weight: 700, size: 7.4pt, tracking: 0.1em, fill: paper, h), v)).flatten())
  v(-2pt)
  brush(weight: 2pt, seed: 9)
})

#let anatomy(sections, size: aside-size) = for (label, items) in sections {
  label-rule(label)
  set text(size: size)
  set par(leading: 3pt, justify: false)
  for it in items { block(above: 3pt, below: 3pt, par(hanging-indent: 8pt, it)) }
}

// Monster entry = portrait, name + role, flavour, stat bar, labelled anatomy. One keep unit.
#let monster(name, role, art: none, art-width: 80%, flavour-text, header, values, sections) = block(width: 100%, breakable: false, above: 0pt, below: 14pt)[
  #if art != none { block(width: 100%, height: 2.5in, spacing: 0pt, align(center + bottom, image(art, height: 100%, width: art-width, fit: "contain"))); v(3pt) }
  #entry-title(name, role, size: 21pt)
  #v(2pt)
  #flavour(flavour-text)
  #stat-strip(header, values)
  #anatomy(sections)
]

// Class / ancestry / background entry: a tall portrait in the outer column beside the entry head.
#let character-entry(name, kicker, tag-text, art: none, flavour-text, facts, body) = block(width: 100%, breakable: true, above: 0pt)[
  #grid(columns: (1fr, 2.15in), column-gutter: gap, align: top,
    [
      #entry-title(name, [#kicker #h(2pt)·#h(2pt) #tag-text], size: 36pt)
      #v(3pt)
      #brush(weight: 2.2pt, seed: 4)
      #v(4pt)
      #flavour(flavour-text)
      #block(above: 6pt, width: 100%, {
        set text(font: sans, size: 9pt)
        set par(justify: false, leading: 2.5pt)
        table(columns: (auto, 1fr), inset: (x: 6pt, y: 3.6pt), stroke: (x, y) => (bottom: 0.35pt + hair),
          fill: (x, y) => if x == 0 { ink } else if calc.odd(y) { tint } else { none },
          ..facts.map(((k, v)) => (text(weight: 700, size: 7.4pt, tracking: 0.1em, fill: paper, upper(k)), v)).flatten())
        v(-2pt)
        brush(weight: 2pt, seed: 6)
      })
    ],
    if art != none { image(art, width: 100%) })
  #body
]

// Power entry: shield numeral, blackletter name, cost tag, italic field strip, then effect.
#let power(n, name, cost, fields, effect) = block(width: 100%, breakable: false, above: 9pt, below: 8pt)[
  #set par(justify: false)
  #grid(columns: (15pt, 1fr), column-gutter: 6pt, align: horizon,
    shield(w: 14pt, body: text(font: sans, weight: 700, size: 7.6pt, fill: paper, str(n))),
    [#text(font: goth, weight: 600, size: 15.5pt, name)#h(6pt)#cost-tag(cost)])
  #v(1pt)
  #block(inset: (left: 21pt), {
    text(font: sans, size: 8.4pt, fill: ink2, fields.map(((k, v)) => [#text(weight: 700)[#k] #emph(v)]).join(h(4pt) + sym.dot.c + h(4pt)))
    v(2pt)
    set text(size: aside-size)
    effect
  })
]

// Tradition tier head: blackletter on a black band with lozenge terminals.
#let tier-head(title) = block(above: 13pt, below: 6pt, sticky: true, width: 100%,
  block(width: 100%, fill: ink, inset: (x: 8pt, y: 4pt), spacing: 0pt,
    grid(columns: (auto, 1fr, auto), column-gutter: 6pt, align: horizon,
      lozenge(size: 5pt, fill: paper), text(font: goth, weight: 600, size: 13.5pt, fill: paper, title), lozenge(size: 5pt, fill: paper))))

// ================================================================ chapter opener
// Framed page: art at the head, the chapter's arms, "Chapter One", the blackletter title, the
// crown flourish and the lead in IM FELL; rules resume on the same page with a drop capital.
#let chapter-opener(word, title, n: 1, art: none, lead: none) = block(width: 100%, breakable: false, above: 0pt, below: 12pt)[
  #if art != none {
    v(-0.05in)
    align(center, image(art, width: 86%))
    v(-10pt)
  } else { v(1.2in) }
  #align(center)[
    #arms(n, w: 52pt)
    #v(-2pt)
    #text(font: sans, weight: 700, size: 8.2pt, tracking: 0.42em, upper[Chapter #word])
    #v(-6pt)
    #text(font: goth, weight: 600, size: 50pt, hyphenate: false, title)
    #v(-8pt)
    #flourish(len: 90pt)
  ]
  #if lead != none { lead-block(lead, width: 82%) }
]

// ================================================================ scenario
#let scenario-head(num, title, flavour-text, art: none) = block(width: 100%, below: 8pt, breakable: false)[
  #if art != none { align(center, image(art, width: 60%)); v(-2pt) }
  #entry-title(title, [Scenario #h(2pt) #num], size: 32pt, al: center)
  #v(4pt)
  #lead-block(flavour-text)
  #brush(weight: 2.2pt, seed: 8)
]

// Setup dossier: the source's labelled setup fields in a tinted, corner-flourished panel.
#let dossier(fields) = block(width: 100%, above: 10pt, breakable: false, cornered(fill: tint, inset: (x: 13pt, y: 12pt))[
  #set text(size: dossier-size)
  #set par(leading: 2.9pt, justify: false, spacing: 5pt)
  #for (k, v) in fields { block(below: 5.5pt, [#text(font: sans, weight: 700, size: 7.2pt, tracking: 0.12em, upper(k))\ #v]) }
])

#let outcome(fields) = block(width: 100%, above: 10pt, breakable: false, cornered(inset: (x: 13pt, y: 11pt))[
  #set text(size: 9.6pt)
  #set par(justify: false, leading: 2.9pt)
  #for (k, v) in fields { block(below: 4pt, [#text(weight: 700, k) #v]) }
])

// ================================================================ quick reference (Appendix C)
#let qref-head(code, title) = block(width: 100%, above: 0pt, below: 8pt, {
  block(width: 100%, fill: ink, inset: (x: 10pt, y: 6pt), spacing: 0pt, text(fill: paper)[
    #box(baseline: 30%, shield(w: 16pt, fill: paper, body: text(font: sans, weight: 700, size: 6.8pt, fill: ink, code)))#h(9pt)#text(font: goth, weight: 600, size: 19pt, title)#h(1fr)#text(font: sans, weight: 700, size: 7pt, tracking: 0.2em)[RULES REFERENCE]])
  v(1.5pt)
  line(length: 100%, stroke: 0.5pt + ink)
})

// ================================================================ contents and index
#let toc-chapter(num, title, page, n: none) = block(above: 10pt, below: 3pt, breakable: false, width: 100%)[
  #grid(columns: (20pt, 1fr, auto), column-gutter: 7pt, align: horizon,
    if n != none { arms(n, w: 22pt) } else { shield(w: 15pt, body: text(font: sans, weight: 700, size: 7.4pt, fill: paper, num)) },
    [#text(font: sans, weight: 700, size: 8pt, fill: ink3, num)#h(5pt)#text(font: goth, weight: 600, size: 16pt, title)],
    text(font: sans, weight: 700, size: 10pt, str(page)))
  #v(-4pt)
  #line(length: 100%, stroke: 0.7pt + ink)
]
#let toc-line(num, title, page) = block(above: 2.6pt, below: 2.6pt, {
  set text(font: serif, size: 9.4pt)
  grid(columns: (20pt, 1fr, auto), column-gutter: 7pt,
    text(font: sans, size: 8.4pt, weight: 600, fill: ink3, num),
    box(width: 100%)[#title #box(width: 1fr, repeat(gap: 2.4pt)[#text(fill: ink3)[.]])],
    text(font: sans, size: 8.8pt, str(page)))
})

#let index-letter(l) = block(above: 10pt, below: 3pt, sticky: true,
  grid(columns: (auto, 1fr), column-gutter: 6pt, align: horizon,
    box(fill: ink, inset: 1.4pt, box(stroke: 0.45pt + paper, inset: (x: 4.5pt, top: 1pt, bottom: 3pt), text(font: goth, weight: 600, size: 17pt, fill: paper, l))),
    line(length: 100%, stroke: 0.6pt + ink)))
#let index-entry(term, pages, sub: false) = block(above: 1.4pt, below: 1.4pt, {
  set text(font: sans, size: 9pt)
  set par(hanging-indent: 10pt, justify: false, leading: 2.3pt)
  if sub { h(8pt) }
  [#term#h(4pt)#text(fill: ink3, pages)]
})

// ================================================================ gazetteer (places of the world)
#let gazetteer(name, kicker, art: none, body) = block(width: 100%, breakable: false, above: 0pt, below: 16pt)[
  #if art != none { align(center, image(art, width: 100%)); v(-2pt) }
  #entry-title(name, kicker, size: 30pt, al: center)
  #v(4pt)
  #align(center, block(width: 46%, brush(weight: 2pt, seed: 10)))
  #lead-block(body)
]
