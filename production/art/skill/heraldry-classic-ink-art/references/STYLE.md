# House style and how to read the references

The prompt already carries the style text. This page explains what the references are for and what the image has to survive afterwards.

## Gritty old-school direction (owner, 2026-10-11)

The target is gritty, old-school black-and-white ink, like late-1970s and 1980s rulebook and module art. The references are the owner's samples STYLE-REF-03 to STYLE-REF-10.
- Look for: bold, rough brush contours of uneven weight; heavy solid-black shadow shapes; scratchy hatching and dry-brush drag where form turns; the bite of a woodcut; high contrast with few in-between textures. Visible human marks (broken lines, dry-brush streaks, an occasional ink fleck) are welcome.
- It still must look hand-made, not generated. A result covered in uniform micro-detail, stipple fields, machine-even texture, clean vector-like line, glossy rendering or soft tonal haze fails `style_reference_match`, however impressive it looks. Grey wash or grey ink tone fails, because the book prints pure black ink.
- Only the owner's samples are attached as references, never an earlier generated image.

## Three registers

| Register | Families | Look |
|---|---|---|
| scene | cover, chapter, world, climate, bastion, scenario, campaign, boss, tradition | Gritty brush and pen work: rough contours of varied weight, big solid-black masses for shadow and depth, scratchy hatching and dry-brush where light turns; distance thins to simpler, lighter line, never haze. The deepest blacks and sharpest contrast gather at the focus, and the drawing dissolves into blank paper through broken strokes on all four sides. |
| creature, person | monster; class, ancestry | One subject drawn whole, like old-school rulebook monster art: a bold rough contour, heavy solid-black shadow shapes, scratchy hatching or dry-brush where form turns, a strong silhouette first. Isolated on white with only a small patch of ground and a cast shadow. Light from the upper left. |
| still | background, item | The figure look applied to a group of objects on a small surface. No figure, no scenery. |

Figures print 1.6 to 1.9 inches wide, so the silhouette and the big black shapes must read at that size; fine texture is lost. Do not let a figure pick up scene backgrounds, and do not let a scene lose its fading vignette.

## What the references give you, and what they must not

Take from a reference: line weight, hatching density, contrast, finish. Take nothing else.

References carry subjects that tend to leak into unrelated images. Reject any result that has one without the prompt asking for it:
- **Figures:** a skeleton king on a throne with a gargoyle-faced armrest, cobwebs, a skeleton warrior with a shield, a winged armoured dragon-man with a great axe, a roaring bear's exact pose, a gnoll with a skull on its belt, a crab-clawed insectoid, a hooded archer with a quiver, period fencers or beggars in ruffs, breeches and rags.
- **Scenes:** a full moon behind skeletons, a crowd of undead faces, a zombie facing a cloaked swordsman, a warrior-priest calling down fire on lizard silhouettes, a wizard in a pointed hat, an adventuring party on a forest path, a donkey under trees, prison chains, wheels and drawbridges, armour on mannequin stands, dungeon pits.
- **Towns** (the city references used for bastion and world scenes): framing oaks, standing stones with spirals, a timber palisade with twin gate towers, tree banners, a stone-pier bridge, a walled city seen from above.

Each item has at most three references, chosen per family (and per monster kind) so that scenery never reaches figure items; do not add more. A few references are centuries-old etchings or woodcuts: take their line, blacks and finish, never their period costume.

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


## Style matching

Read `references/STYLE_CONSISTENCY.md` and complete its ten-criterion, byte-bound visual QA for every generated candidate. Scene, figure and still-life references must not be mixed for density comparisons. If two or more images in a batch drift toward the same fault, stop rather than normalizing that fault.
