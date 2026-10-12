# Visual continuity: art direction and objective release gates

The approved visual references govern style, not subject. Compare every candidate side by side with its queue-provided references. The three production registers need different treatments. Do NOT compare a spot-ink character's density directly to Greythorn's panoramic town scene.

## Fixed house signature

1. **Medium:** gritty old-school black ink (brush and dip pen) on near-white, even paper. Tonal depth comes from heavy solid-black shapes, rough contours, scratchy hatching, crosshatching and dry-brush drag; never a grey wash, stipple fields or machine-even texture.
2. **Line hierarchy:** main forms have confident slightly heavier contours; interior structures have thinner marks; receding objects get narrower, more interrupted strokes.
3. **Light:** one coherent upper-left light direction, with right/lower shadows unless the individual prompt explicitly overrides lighting.
4. **Surface logic:** hatches wrap bark, timber, armour, stone, ice, cloth, or hide differently; marks describe material and construction, rather than applied generic noise.
5. **Tonal hierarchy:** focal silhouettes read at actual print width. Heavy solid blacks carry the composition against open paper, with few in-between textures; keep enough reserve paper that the main forms read.
6. **Scenic vignette:** scenes dissolve organically through increasingly sparse incomplete lines into flat blank paper at all 4 edges and corners. The transition should be visibly drawn, not feathered digitally. Isolated characters and objects instead need generous clear margins and only modest cast-ground shadows.
7. **Architectural and environmental identity:** no Greythorn oaks, stone circles, bridge, palisade, banner, or gatehouse, and no reference subjects (throne, cobwebs, cave grub, skull staff, crowd of undead faces, full moon) unless the queued subject asks for them. Desert, cave, swamp, ice, ruin, and forest scenes require different construction and weathering, even under the same house style.
8. **No text:** no generated typography, pseudo-runes, visible words, signatures, watermarks, logos, borders, or accidental square grids.

## Side-by-side comparison protocol

Inspect the original at normal size and the 150 px/in print proof beside queue-selected references (at most 3). Complete `fidelity_gate.py create` JSON evidence for all 10 criteria, using the actual visible features. Describe exact failures rather than saying "looks good". The report must include:

- subject and canonical visual facts represented, not invented;
- legible first-read silhouette appropriate to printed width;
- reference relative line weight, white reserve, and deep black placement;
- observed hatch/stipple grammar and material-specific textures;
- near-white paper, no smooth grey wash;
- vignette on all four sides or clean isolated margins;
- construction/anatomy and named/must-show feature counts;
- no prohibited content and no reference subject bleed;
- no repeated clones of roof modules, hands, textures, or poses.

All comparison statistics are **advisory**; image contents and page density legitimately vary. Do not invent an 8.8/10 score and call it measured. A failing visual criterion requires another variant within budget, or a flagged handoff at exhaustion. Claude Code independently makes the publish/reject decision.

## Anti-drift batch review

Every tenth saved image (`status` says DRIFT REVIEW), run `sheet --recent 10 --refs` and `style_audit.py --repo . --recent 10`. Compare by register (scene with scene, creature/person with the figure reference, still life with still-life references). Look for creeping grey, heavier/fainter contours, cloned posing, lower contrast, inconsistent paper, or crowding. Deliver in every case and continue. When at least two siblings show the same drift, report the trend to Claude Code; it reviews the reference selection or prompt upstream and sends redos.

## Approval

**Neither self-attested checks nor code metrics are editorial approval.** Claude Code reviews every delivered image; only an `anchors` phase, if one is ever published, stops for that review.
