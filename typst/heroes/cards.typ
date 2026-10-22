// Every B.4 word, approved individual portrait, and shared Basic Mode reminder.
// Individual PDFs use one or two sides. The combined print pack pads short Heroes.
#import "compact.typ": *
#let pick = sys.inputs.at("hero", default: "all")
#for hr in DATA.heroes.filter(x => pick == "all" or x.name == pick) {
  compact-card(hr)
  if pick == "all" {
    context {
      if not query(<hero-needs-back>).any(it => it.value.name == hr.name) {
        page(width: 612pt, height: 792pt, margin: 32pt, fill: paper)[#box(height: 1pt)]
      }
    }
  }
}
