// Standalone cover sheets: page 1 front, page 2 back.
#import "cover.typ": *
#let cd = json("../build/cover.json")
#set document(title: publication.verified_publication_metadata.title + ", Covers, " + publication.verified_publication_metadata.version, author: publication.verified_publication_metadata.author_credit)
#set text(font: serif, size: 10.5pt, fill: ink)
#set smartquote(enabled: false)
#front-cover(cd.title, emph(cd.subtitle), cd.version)
#back-cover((lead: emph(cd.lead), facts: cd.facts), cd.version)
