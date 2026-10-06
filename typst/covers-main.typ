// Standalone cover sheets: page 1 front, page 2 back.
#import "cover.typ": *
#let cd = json("../build/cover.json")
#set text(font: serif, size: 10.5pt, fill: ink)
#front-cover(cd.title, emph(cd.subtitle), cd.version)
#back-cover((lead: emph(cd.lead), facts: cd.facts), cd.version)
