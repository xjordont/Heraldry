// Every Hero always uses the same expanded front/back format; no blank versos.
#import "expanded.typ": *
#let pick = sys.inputs.at("hero", default: "all")
#for hr in DATA.heroes.filter(x => pick == "all" or x.name == pick) {
  basic-card(hr)
}
