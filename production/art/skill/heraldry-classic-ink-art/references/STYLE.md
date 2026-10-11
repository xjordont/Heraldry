# House style and how to read the references

The prompt already carries the style text. This page explains what the references are for and what the image has to survive afterwards.

## Three registers

| Register | Families | Look |
|---|---|---|
| scene | cover, chapter, world, climate, bastion, scenario, campaign, boss, tradition | Dense dip-pen work: varied line weight, hatching, crosshatching and stippling; distance by finer, sparser marks, never haze. The drawing is densest at its focus and dissolves into blank paper through broken strokes on all four sides. |
| creature, person | monster; class, ancestry | One subject drawn whole. A slightly heavier outer contour, crisp interior lines, form-following hatching, sparse stipple, a few solid-black shapes for the deepest shadows. Isolated on white with only a small patch of ground and a cast shadow. Light from the upper left. |
| still | background, item | The figure look applied to a group of objects on a small surface. No figure, no scenery. |

The two registers are different on purpose. Figures print 1.6–1.9 inches wide, so bold contour and simple tone survive; the dense scene texture does not. Do not let a figure drift toward scene texture, and do not let a scene drift toward clean figure line.

## What the references give you, and what they must not

Take from a reference: line weight, hatching density, contrast, finish. Take nothing else.

References carry subjects that tend to leak into unrelated images. Reject any result that has them without the prompt asking: ancient oaks, standing stones tied with rope or carved with spirals, a timber palisade gate, a timber bridge over a stream, a watchtower with a banner, a skeleton warrior with a shield, a walled city seen from above. Each item has at most three references, chosen so that scenery never reaches figure items; do not add more.

## Ink and paper

- Pure black ink. Dark brown-black ink is acceptable; coloured accents are not.
- The paper is flat and near white. Warm ivory is fine. The repo's intake keys the paper out to transparent and keeps only the ink, so what matters is that the paper is uniform: no grain, stains, tint gradient, darkened vignette or border. Texture on the paper is lost or flagged; grey wash is lost.
- No grey wash, gradients, soft shadows or blur. Tone comes from marks.
- No lettering of any kind, including runes, bark signs, labels and signatures.

## Scale

The prompt is canonical: a creature's `Size:` line, or what a scene says about its people.

| Class | Meaning |
|---|---|
| Small | smaller than a human |
| Medium | about human-sized |
| Large | roughly twice a human's height or bulk |
| Huge | towering many times a human's size |

Draw a small human figure for scale only when the prompt asks for one. A prompt that says "No humans" means none.

## Print size

Images print between 1.6 and 4.8 inches wide. `check` writes a preview at 150 pixels per printed inch. The subject must be unmistakable there. If it is not, the usual causes are a subject that is too small in the frame, hatching so fine it greys out, and too many small competing forms. The fix is larger, bolder, fewer forms (`references/REPAIR.md`), never added detail.


## V6 style matching

Read `references/STYLE_CONSISTENCY_V6.md` and complete its ten-criterion, byte-bound visual QA for every generated candidate. Scene, figure and still-life references must not be mixed for density comparisons. If two or more images in a batch drift toward the same fault, stop rather than normalizing that fault.
