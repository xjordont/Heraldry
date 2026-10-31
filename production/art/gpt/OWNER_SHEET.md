# Owner tailpiece sheet: 47 section-end images, made by hand in ChatGPT

Owner decision 2026-10-31: Codex's and ChatGPT Work's image tools no longer accept reference files for a new image, so the owner generates each tailpiece in ordinary ChatGPT with the references attached by hand. Derived from `production/art/gpt/QUEUE.json` (batch phase); the prompts are the queued files, unchanged.

## For each item

1. Start a **new** ChatGPT chat (no earlier image in it).
2. Attach that item's reference images, in the order listed. They are in `C:\Heraldry\art-producer\assets\art\style\`.
3. Paste the prompt exactly as given, then add on its own line: `Wide 3:2 landscape, the largest size and highest quality you offer.`
4. Generate **once**. Do not ask for changes; a weak image is fixed later as a redo.
5. Download the image unchanged and name it after the item ID, for example `ART-END-ACTION-BASICS.png` (keep whatever extension ChatGPT gives).

## Sending them back

Upload the images, as they are, to `production/art/owner_upload/` on GitHub (Add file, Upload files), in as many batches as you like. Tell Claude Code when a batch is up: it checks each image against its references and prompt, fills the QA record and receipt, and packages them so the `Import Work review bundle` workflow commits them through Git LFS. Nothing is approved until it has been reviewed.

## Reference sets

| Set | Used for | Files, in order |
|---|---|---|
| A | scenes (32 items) | `STYLE-REF-30-forest-path-stipple.jpg`<br>`STYLE-REF-58-waterfall-ruins-flight.jpg`<br>`STYLE-REF-55-siege-wall-climb.jpg`<br>`STYLE-REF-44-haden-vignette-farm.jpg` |
| B | spells (4 items) | `STYLE-REF-29-cleric-holy-fire.jpg`<br>`STYLE-REF-26-wizard-summoning-beast.jpg`<br>`STYLE-REF-28-wizard-vs-serpent-fiend.jpg`<br>`STYLE-REF-63-wizard-flame-hand.jpg` |
| C | equipment (11 items) | `STYLE-REF-15-sword-mace-items.jpg`<br>`STYLE-REF-40-rag-wrapped-scythe.jpg`<br>`STYLE-REF-27-carved-scroll-case.jpg`<br>`STYLE-REF-33-bound-bone-cross.jpg`<br>`STYLE-REF-56-weapons-sheet.jpg` |

## 1. The dropped torch (`ART-END-ACTION-BASICS`)

Save as `ART-END-ACTION-BASICS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE DROPPED TORCH - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Hero at the foot of a cellar stair letting a lit torch fall to free a hand, drawing a blade as shapes stir in the dark ahead, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Low view at the bottom of a short stone stair: the Hero stands at the centre with the torch tumbling from one hand toward the floor and the other hand pulling a sword from its scabbard; the passage beyond is a block of solid black with two vague shapes.

SUBJECT DETAILS
* Human Hero in a hooded mantle and leather coat, weight on the back foot
* Torch mid-fall, its flame drawn as a few clean ink tongues
* Shortsword halfway out of a worn scabbard
* Worn cellar stair behind, three or four steps
* Two indistinct hunched shapes in the black passage, no features
* Torchlight as a ring of open paper on the floor
Must be shown exactly:
* One Hero only; the shapes stay vague

HUMAN ACTIVITY
* The Hero drops the torch and draws in one movement

ARTISTIC STYLE AND ATMOSPHERE
A heartbeat of decision in the dark.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No detailed Monster.
* Not the Undercroft or the Shadowed Under Passage.
* No glow effect around the torch.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 2. The imp dispelled (`ART-END-ACTION-POINTS-AND-SUMMONS`)

Save as `ART-END-ACTION-POINTS-AND-SUMMONS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE IMP DISPELLED - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of an Infernal Imp, a Sorcerer's temporary Summon, unravelling into smoke and cinders as it is dispelled from the world, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Eye-level view of a single fallen column drum; the imp crouches on top of it at the centre, its lower body and one wing already coming apart into curling smoke that drifts off to the right and thins to nothing.

SUBJECT DETAILS
* Knee-high, bat-winged imp with a barbed tail, small clawed hands and a snarling face
* One wing intact and spread, the other shredding into smoke strands and flicked cinder flecks
* Tail and legs dissolving from the tips inward
* Fallen column drum with a cracked fluting, the imp's claws gripping its edge
* A faint scorch ring on the stone where it was called
* Smoke drawn in a few bold broken curves, not as grey haze
Must be shown exactly:
* Only the imp and the column drum; no caster in frame

HUMAN ACTIVITY
* The imp twists to look at its own vanishing wing

ARTISTIC STYLE AND ATMOSPHERE
Brief, spiteful and borrowed; nothing summoned stays.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Sun-Drowned Imp bestiary portrait: no tomb setting, no flying pose.
* No glow, grey wash or airbrushed smoke.
* No summoning circle with symbols.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 3. The higher ground (`ART-END-ADVANTAGES-AND-DISADVANTAGES`)

Save as `ART-END-ADVANTAGES-AND-DISADVANTAGES.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE HIGHER GROUND - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the advantage of higher elevation: an archer kneeling on the broken top of a ruined wall, shooting down at a Beastman scrambling up the rubble below, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Low angle from the foot of the rubble slope: the wall stub rises at right with the archer kneeling on its broken top, the Beastman climbing the scree at lower left, a clear diagonal from archer to target.

SUBJECT DETAILS
* Elf archer in a leather coat kneeling on the wall top, shortbow at full draw aimed steeply downward
* Ruined wall stub with broken coursing and a jagged top edge, about twice a person's height
* Beastman: hunched man-shape with a goat's head and black-clawed hands, clawing up loose rubble
* Loose stones sliding from under the Beastman's feet
* A spent arrow standing in the rubble near the Beastman
* Weeds in the wall joints
Must be shown exactly:
* The archer is clearly well above the Beastman

HUMAN ACTIVITY
* The archer looses downward
* The Beastman claws upward, slipping

ARTISTIC STYLE AND ATMOSPHERE
Hard, cold advantage taken without mercy.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No longbow, staff or plate armour on the archer.
* Not the aqueduct of the chapter 4 opener.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 4. The scout on the ridge (`ART-END-ADVENTURE-PREPARATION-SEQUENCE`)

Save as `ART-END-ADVENTURE-PREPARATION-SEQUENCE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE SCOUT ON THE RIDGE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Scout Hireling lying on a ridge with a spyglass, surveying the ruin below before the party deploys, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter rear view: the Scout lies flat along the ridge crest in the foreground at left, spyglass to one eye; below and beyond at right, a small ruined chapel and broken walls drawn light and simple.

SUBJECT DETAILS
* Scout in a hooded leather coat, shortsword at the hip, lying flat
* Extended brass spyglass
* Ridge grass and a boulder for cover
* Distant ruined chapel with a fallen roof and a broken wall circuit
* A thin thread of smoke rising from the ruin
Must be shown exactly:
* The ruin stays small and lightly drawn; the Scout is the focal point

HUMAN ACTIVITY
* The Scout watches, motionless

ARTISTIC STYLE AND ATMOSPHERE
Calm before commitment.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the chapter 10 crossroads or the chapter 1 pass.
* No banners.
* No Monsters drawn in detail.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 5. The life left behind (`ART-END-BACKGROUNDS`)

Save as `ART-END-BACKGROUNDS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE LIFE LEFT BEHIND - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the life a Hero walked away from: an abandoned smallholding gate left swinging open, footprints leading out to the road, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view of a field gate at the centre, hanging open on one hinge; the farm track runs from it toward the viewer and away into white paper, a single line of footprints in the mud.

SUBJECT DETAILS
* Wooden field gate on one hinge, a broken bar
* Leaning gatepost with a rusted hook
* Footprints in the muddy track, heading out
* Sickle hung on the gatepost
* A low drystone wall and a dead tree
* A roofless cottage small in the distance
Must be shown exactly:
* No figures

ARTISTIC STYLE AND ATMOSPHERE
Departure without farewell.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Farmer or Vagabond still lifes.
* Not the Grim World burnt farmstead.
* No banners or smoke.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 6. Arm's reach (`ART-END-COMBAT-BASICS`)

Save as `ART-END-COMBAT-BASICS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
ARM'S REACH - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Bugbear rising out of dead bracken to strike from arm's reach with its spiked morningstar, before its quarry can close, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view: the Bugbear looms at left, long arm fully extended, the morningstar swinging out over the bracken toward a Hero at right who is still a full stride away with shield raised late.

SUBJECT DETAILS
* Bugbear: seven feet of shaggy, long-armed menace, flat face, fur like dead bracken
* Spiked morningstar at the end of the overlong arm
* Dead bracken and undergrowth parting around the Bugbear's legs
* Hero in a gambeson with a small round targe and a shortsword, one foot sliding back
* Clear gap of ground between the Hero's blade and the Bugbear
Must be shown exactly:
* The Bugbear's reach visibly exceeds the Hero's

HUMAN ACTIVITY
* The Bugbear swings from beyond the Hero's reach
* The Hero flinches back behind the targe

ARTISTIC STYLE AND ATMOSPHERE
Ambush and the cruelty of a longer arm.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Bugbear bestiary portrait: this is a two-figure clash.
* No goblins.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 7. Eyes in the dark (`ART-END-COMMON-TRAIT-RULES`)

Save as `ART-END-COMMON-TRAIT-RULES.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
EYES IN THE DARK - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Darkvision: a Dwarf and a Gnome advancing through a lightless mine gallery without any lamp, seeing what others could not, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Head-on view into a mine gallery: the gallery is solid black, and the two figures are drawn in white line and sparse highlight within it, the Dwarf leading and the Gnome a step behind; the black shape thins into paper at its ragged edges.

SUBJECT DETAILS
* Broad Dwarf with a pick on the shoulder and a hand on the timber prop
* Small Gnome with a tinker's satchel, head tilted, peering ahead
* Timber props and a sagging crossbeam
* No lantern, torch or flame anywhere
* Pale glint in both pairs of eyes
* Ore cart rail fading into the dark
Must be shown exactly:
* No light source in the picture

HUMAN ACTIVITY
* Both walk steadily forward through total darkness

ARTISTIC STYLE AND ATMOSPHERE
The dark as home ground.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No glowing eyes beams or glow effects.
* Not the Undermarches climate cutaway or the Quake scenario.
* No monsters.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 8. Frightened (`ART-END-CONDITIONS`)

Save as `ART-END-CONDITIONS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
FRIGHTENED - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Hero made Frightened: backing away with a shaking torch from the shadow of a Spectre sliding across a ruined wall, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view along a stretch of ruined wall: the Hero at left steps backward with torch held out at arm's length; across the wall at right spreads a huge tattered shadow of a drifting figure, with no Spectre body drawn.

SUBJECT DETAILS
* Human Hero in a padded coat, shoulders hunched, face turned half away
* Torch flame bent and guttering, the arm visibly trembling
* Spectre shadow: a tall ragged figure with trailing hems and reaching hands, in solid black on the wall
* Plastered ruined wall with cracks and a blind window
* Dropped shield lying face down at the Hero's feet
Must be shown exactly:
* The Spectre appears only as a shadow

HUMAN ACTIVITY
* The Hero backs away, stumbling

ARTISTIC STYLE AND ATMOSPHERE
Cold, unreasoning fear.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No visible ghost body, face or glow.
* Not the chapter 8 library or the Shadowed Under Passage.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 9. The bow too big (`ART-END-CORE-HERO-CREATION-RULES`)

Save as `ART-END-CORE-HERO-CREATION-RULES.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE BOW TOO BIG - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Halfling Hero standing beside a Greatbow propped upright, the Heavy bow far taller than they are: equipment a Small Hero cannot wield, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Straight-on view at a weapon rack's foot: the Greatbow stands upright at the centre, the Halfling beside it with a hand on the stave, gazing up at its tip.

SUBJECT DETAILS
* Small Halfling with adult proportions, hood pushed back, sling tucked in the belt
* Greatbow, unstrung, more than twice the Halfling's height
* Bare weathered wooden rack end with pegs
* Quiver of long arrows leaning on the rack
* Packed-earth floor fading out
Must be shown exactly:
* The Halfling is child-sized with adult proportions; the bow towers over them

HUMAN ACTIVITY
* The Halfling looks up at the bow with wry resignation

ARTISTIC STYLE AND ATMOSPHERE
Dry humour in a hard world.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Do not make the Halfling a cute child or cartoon.
* Not the Halfling ancestry figure: no crouch, no sling throw.
* No armour.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 10. Hero, Hireling, and Monster (`ART-END-CORE-TERMS`)

Save as `ART-END-CORE-TERMS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
HERO, HIRELING, AND MONSTER - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the three kinds of combatant the rules name, met in one crypt passage: a Dwarf Hero, the Guard Hireling at their side, and a Ghoul, the Monster that has come for them, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Side view down a short vaulted crypt passage: the Dwarf Hero and the Guard stand shoulder to shoulder at left, the Ghoul crouched low at right in the passage mouth, the gap of bare floor between them the centre of the picture.

SUBJECT DETAILS
* Dwarf Hero: very broad, short-limbed, braided beard, mail, lantern raised in one hand and handaxe in the other
* Guard Hireling: human retainer in a padded coat with a heater shield and a mace, a step behind the Dwarf's shoulder
* Ghoul: grey, gaunt and hook-clawed, loping low on all fours with its head thrust forward
* Low barrel vault of rough stone, two niches with old bones
* Lantern light shown by open white paper around the pair, the Ghoul's end of the passage in solid black
* Dust and a dropped bone on the floor between them
Must be shown exactly:
* Three combatants only: one Dwarf Hero, one shield-bearing Guard, one Ghoul

HUMAN ACTIVITY
* The Dwarf and the Guard brace side by side
* The Ghoul creeps forward, claws on the flagstones

ARTISTIC STYLE AND ATMOSPHERE
Close, cold and about to break.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Undercroft room (no hidden door, no cloaked figure) and not the Shadowed Under Passage scenario.
* Do not draw the Ghoul as a zombie or a skeleton.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 11. Goblin-sign on the road (`ART-END-DETERMINING-MONSTERS-FOR-AN-ADVENTURE`)

Save as `ART-END-DETERMINING-MONSTERS-FOR-AN-ADVENTURE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
GOBLIN-SIGN ON THE ROAD - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Greythorn gate-warden crouched on the forest road, reading goblin-sign in a scatter of chewed bones to learn what waits ahead, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view at ground level: the warden crouches at centre-left over the sign, one gloved hand turning a bone; the scatter of bones, river stones and a notched blade lies on the road stones at centre-right.

SUBJECT DETAILS
* Gate-warden in a long patched coat and a dented kettle helm, spear laid across the knees
* Chewed bones with gnaw marks, a split rib and a knuckle
* Small, crude notched goblin blade
* Three smooth river stones left in a little pile
* Old forest road paving with a root lifting one slab
* Fern edge and a tree root at one side
Must be shown exactly:
* No goblins in the picture

HUMAN ACTIVITY
* The warden studies the sign, head cocked as if listening

ARTISTIC STYLE AND ATMOSPHERE
Grim, practised knowledge of what hunts the road.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No goblins or other Monsters.
* Not the Broken Courier road or the Bandit's Toll barricade.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 12. The ratkin swarm (`ART-END-DYNAMIC-PARTY-AND-SCENARIO-SCALING`)

Save as `ART-END-DYNAMIC-PARTY-AND-SCENARIO-SCALING.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE RATKIN SWARM - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Minion swarm: Ratkin Scavengers of the Pale City boiling up out of a broken drain grate in a frozen street, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view: the wrenched grate at the centre, a stream of ratkin pouring out of it and fanning across the frozen cobbles toward the lower edge.

SUBJECT DETAILS
* Iron drain grate wrenched aside, its bars bent
* Scrawny, twitching ratkin in matted grey fur, a few clutching sacks or crude blades
* Frozen cobbles with frost and an icicle hanging from the kerb
* One ratkin dragging a stolen boot
* Snow scuffed by many small feet
Must be shown exactly:
* The ratkin read as one swarm, not separate portraits

HUMAN ACTIVITY
* The swarm pours out of the drain

ARTISTIC STYLE AND ATMOSPHERE
Endless, verminous pressure.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Ratkin ancestry or bestiary portraits.
* No gore.
* No Heroes in frame.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 13. Camouflage (`ART-END-GENERAL-TALENTS`)

Save as `ART-END-GENERAL-TALENTS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
CAMOUFLAGE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the Camouflage talent: a Hero lying hidden in ferns and roots, only the eyes and an arrowhead showing, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Low view at ground level: a tangle of ferns and roots fills the centre, and inside it the Hero's face and bow hand are barely visible among the leaves.

SUBJECT DETAILS
* Fern fronds and roots drawn in bold shapes
* A pair of watchful eyes and a strip of brow in the leaves
* Shortbow arrowhead and fingers at the string
* Leaf litter and a mossy log
* A beetle on the log for scale
Must be shown exactly:
* The Hero is mostly hidden; the cover dominates

HUMAN ACTIVITY
* The Hero waits motionless

ARTISTIC STYLE AND ATMOSPHERE
Patient, unseen menace.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No full figure.
* Not the Scout background or the Ranger class figure.
* No enemies.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 14. Paying for training (`ART-END-HERO-ADVANCEMENT`)

Save as `ART-END-HERO-ADVANCEMENT.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
PAYING FOR TRAINING - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Advancement bought with coin: a Hero's scarred hand dropping a purse into a trainer's open palm over a practice sword, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Close crop at waist height: two hands meet at the centre, the purse falling from one into the other; a wooden practice sword lies across the trainer's forearm.

SUBJECT DETAILS
* Hero's hand, scarred knuckles, a worn bracer
* Trainer's broad calloused palm, older, missing a fingertip
* Small leather purse, coins showing at its mouth without stamps
* Wooden practice sword with a dented edge
* Sleeve cuffs: mail on the Hero, a padded sleeve on the trainer
Must be shown exactly:
* Hands only; no faces

HUMAN ACTIVITY
* The purse changes hands

ARTISTIC STYLE AND ATMOSPHERE
Skill earned in blood and paid for in silver.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Expedition Hall training yard.
* No ledgers or writing.
* No full figures.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 15. Wild Shape: the stag (`ART-END-HERO-CLASSES`)

Save as `ART-END-HERO-CLASSES.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
WILD SHAPE: THE STAG - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Druid in the Apex Wild Shape of the Stag, charging through a birch stand with a druid's charm cord still tangled in its antlers, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view: the stag bursts from left to right at the centre, head lowered with antlers forward, birch trunks thinning into white paper at both edges.

SUBJECT DETAILS
* Great red-deer stag with a broad antler crown
* Charm cord of knotted bone and holly beads caught in one antler
* Muscled shoulders mid-bound, forelegs tucked
* A few slim birch trunks with peeling bark
* Torn leaves and soil flung as ink flecks
Must be shown exactly:
* An ordinary stag in build, not monstrous

HUMAN ACTIVITY
* The stag charges at full speed

ARTISTIC STYLE AND ATMOSPHERE
Wild force with a human will behind it.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No half-human transformation.
* Not the Antlered Warden of the Tithe or any Monster.
* No glow.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 16. The porter's drag (`ART-END-HIRELINGS`)

Save as `ART-END-HIRELINGS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE PORTER'S DRAG - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Porter Hireling dragging a Knocked Out Hero by the collar out of a fight's edge, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Side view on rough ground: the Porter leans hard backward at left, both hands in the Hero's collar; the unconscious Hero slides behind at right, heels furrowing the dirt.

SUBJECT DETAILS
* Porter: a lean, unarmed retainer with a big empty pack frame on the back
* Hero in a ring shirt, limp, head lolling, sword left behind
* Two furrows dug by the Hero's heels
* Dropped shortsword and a dented targe left behind
* Scrub and a broken fence post
Must be shown exactly:
* The Porter carries no weapon

HUMAN ACTIVITY
* The Porter hauls with gritted teeth

ARTISTIC STYLE AND ATMOSPHERE
Unheroic loyalty, bought and paid for.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No gore.
* Not the Barracks room or the chapter 6 hall.
* No enemies in frame.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 17. Warden of the Threshold (`ART-END-LEGENDARY-VETERANS`)

Save as `ART-END-LEGENDARY-VETERANS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
WARDEN OF THE THRESHOLD - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Legendary Veteran, retired at the height of their craft, keeping watch at the Stronghold's gate as the Warden of the Threshold, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view: the old veteran sits on a bench beside the gate post at the centre, sword across the knees, looking down the empty road that leads away to the right.

SUBJECT DETAILS
* Grey-bearded, scarred veteran in an old mail shirt under a heavy cloak
* Notched longsword lying across the knees, a hand resting on the pommel
* Thick gate post of the palisade with a lantern hung on a hook
* Bench of a split log
* Muddy road running off past a ditch and stakes
Must be shown exactly:
* One figure, plainly old

HUMAN ACTIVITY
* The veteran watches the road, unhurried

ARTISTIC STYLE AND ATMOSPHERE
Hard-won rest that never quite lets its guard down.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Expedition Hall yard or the Outer Walls night view.
* No banners.
* No Monsters.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 18. The goblin tide (`ART-END-MONSTER-PHASE`)

Save as `ART-END-MONSTER-PHASE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE GOBLIN TIDE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Goblin mob of the Greenmark waking and pouring over the top of a ruined steading wall at night, the moment a Monster Group activates, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Front view of a low wall top running across the picture: a dense knot of goblins spills over it at the centre, more heads and blades behind, the knot thinning to a few stragglers at each end.

SUBJECT DETAILS
* Knee-high, green-grey, all elbows and malice: six to eight goblins in a tight mass
* Notched blades raised, two swinging slings of river stones
* Wide eyes and bared teeth catching small white highlights
* Rough stone wall top with a broken thatch edge from the steading behind
* Night shown by solid black behind the mob, white paper below the wall
* One goblin tumbling head first over the wall
Must be shown exactly:
* The mob reads as one mass, not as separate portraits

HUMAN ACTIVITY
* The goblins surge over the wall all at once

ARTISTIC STYLE AND ATMOSPHERE
Sudden, chittering and overwhelming; singly cowards, in numbers a tide.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Goblin bestiary portrait: no single isolated goblin.
* No goblin shaman, no bugbear.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 19. Wolves resting at the wagon (`ART-END-MONSTER-PLACEMENT-AND-INITIAL-STATE`)

Save as `ART-END-MONSTER-PLACEMENT-AND-INITIAL-STATE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
WOLVES RESTING AT THE WAGON - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Resting Monster Group at its Guard Point: a pack of Greenmark dire wolves asleep around an overturned wagon they have claimed, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Low three-quarter view: the overturned wagon lies at the centre with one wheel in the air; three dire wolves lie curled against it and in its shadow, one with its head up and ears half-pricked.

SUBJECT DETAILS
* Overturned wagon with a cracked bed and a wheel missing spokes
* Three dire wolves, bigger than a pony at the shoulder, scarred, curled nose to tail
* One wolf's yellow eye half-open, drawn as a small white slit
* Spilled crates and a torn sack
* Trampled grass and a broken yoke pole
Must be shown exactly:
* The wolves are resting, not attacking

HUMAN ACTIVITY
* The pack sleeps; one wolf stirs

ARTISTIC STYLE AND ATMOSPHERE
Stillness that will not last.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Dire Wolf bestiary portrait and not the Broken Courier race.
* No human figures or corpses.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 20. The leap between roofs (`ART-END-MOVEMENT-RULES`)

Save as `ART-END-MOVEMENT-RULES.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE LEAP BETWEEN ROOFS - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Human Rogue jumping a gap between two broken rooftops in a ruined town, the street far below, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Side view across the gap: the take-off roof edge at left, the landing ledge at right, the Rogue in mid-air at the centre with legs tucked, the narrow street a dark slot beneath.

SUBJECT DETAILS
* Rogue in a leather coat with a rapier at the hip, arms flung forward
* Left roof: broken slates and an exposed rafter
* Right roof: a lower, narrow stone ledge with a cracked gutter
* Dark drop between drawn in solid black and hatching
* Loose slate falling from the take-off edge
* Cloak streaming behind
Must be shown exactly:
* The landing point is level with or below the take-off point

HUMAN ACTIVITY
* The Rogue is airborne mid-jump

ARTISTIC STYLE AND ATMOSPHERE
Nerve and momentum over a long fall.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the chapter 4 aqueduct or a chasm in a cave.
* No rope or grappling hook.
* No flying or magic.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 21. One moves, one waits (`ART-END-PARTY-PHASE`)

Save as `ART-END-PARTY-PHASE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
ONE MOVES, ONE WAITS - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Two Heroes of one party taking turns at a ruined corner: one dashes across an open gap while the other waits behind cover with a loaded crossbow, holding back for whatever answers, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view of a broken corner of wall: the waiting Hero kneels behind it in the foreground with the crossbow levelled past the edge, the running Hero is mid-stride in the open gap beyond, smaller.

SUBJECT DETAILS
* Kneeling Hero in a gambeson with a light crossbow braced on the wall edge, finger off the trigger
* Running Hero in a leather coat, low and fast, shortsword in hand, cloak flying
* Corner of a ruined wall with a fallen lintel
* Open gap of cracked paving between the two
* A spent bolt and a dropped glove by the kneeling Hero's knee
Must be shown exactly:
* Two Heroes only, clearly on the same side

HUMAN ACTIVITY
* One Hero crosses the gap
* The other holds still, watching for the reply

ARTISTIC STYLE AND ATMOSPHERE
Measured, patient, every breath spent with care.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No enemies in frame.
* Not the chapter 3 dawn gathering.
* No banners.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 22. The Party Leader's halt (`ART-END-PARTY-STRUCTURE`)

Save as `ART-END-PARTY-STRUCTURE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE PARTY LEADER'S HALT - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Party Leader at the head of a four-Hero file, fist raised to halt the others at the mouth of a ruined colonnade, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter rear view: the Party Leader at centre-left stands one pace ahead with a closed fist raised; the other three Heroes are stopped in a short staggered file behind, smaller; two broken columns frame the way ahead.

SUBJECT DETAILS
* Party Leader: a Human in a ring shirt with a shortsword at the hip, fist raised at shoulder height
* Behind: a tall lean Elf with a shortbow, a broad Dwarf with a mace and targe, a small Halfling with a pack
* Two broken columns with fallen capitals
* Path of cracked paving leading on into white paper
* Packs, bedrolls and a lantern on the Dwarf's belt
Must be shown exactly:
* Four Heroes, one clearly leading

HUMAN ACTIVITY
* The leader signals halt
* The others stop and look past the leader

ARTISTIC STYLE AND ATMOSPHERE
Trust, discipline and the weight of one person's call.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the cover party in rain, the postern gate departure or the chapter 1 pass.
* No banners.
* No monsters.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 23. Travellers of five peoples (`ART-END-RANDOM-ANCESTRY-TABLES`)

Save as `ART-END-RANDOM-ANCESTRY-TABLES.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
TRAVELLERS OF FIVE PEOPLES - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Five travellers of different ancestries, Human, Halfling, Dwarf, Elf and Gnome, sharing one small roadside fire at night, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Low view across a small fire at the centre: the five sit or stand around it in a loose ring, their differing heights and builds reading as silhouettes against the light.

SUBJECT DETAILS
* Tall, lean Elf standing with a long cloak
* Very broad, short-limbed Dwarf seated on a stone, braided beard
* Small hooded Halfling with a cooking pot
* Small Gnome with a tinker's satchel and a lens on a cord
* Plain Human in a road coat feeding the fire
* Small fire of sticks with flames as clean ink tongues and sparks as ink flecks
Must be shown exactly:
* Five figures, clearly different in height and build

HUMAN ACTIVITY
* They share the fire in tired silence

ARTISTIC STYLE AND ATMOSPHERE
Unlikely company against the cold.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No rare ancestries (no horns, tusks, scales or rat features).
* Not the four-Hero cover party.
* No glow halo around the fire.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 24. Tracks at the water's edge (`ART-END-RANDOM-MONSTER-GENERATION-TABLES`)

Save as `ART-END-RANDOM-MONSTER-GENERATION-TABLES.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
TRACKS AT THE WATER'S EDGE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Mire mud bank crossed by the tracks of many different Monsters, a record of whatever might come out of the swamp next, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. High-angle view down onto a mud bank at the water's edge: a crossing of different tracks fills the centre, reeds along the top edge and a wedge of black water at one corner.

SUBJECT DETAILS
* A line of clawed lizardfolk prints
* A broad snake drag-mark curving through the mud
* A crocodile's tail furrow flanked by splayed claw prints
* One huge webbed print, wider than a shield
* Bent and broken reeds and a dropped fish skeleton
Must be shown exactly:
* No creatures shown, only their tracks

ARTISTIC STYLE AND ATMOSPHERE
Uncertain, layered menace.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No figures.
* Not the Mire climate walkway or the Mire Titan's Fen.
* No readable symbols in the tracks.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 25. The costly escape (`ART-END-SOLO-AND-COOPERATIVE-PLAY`)

Save as `ART-END-SOLO-AND-COOPERATIVE-PLAY.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE COSTLY ESCAPE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Costly Victory in the Ashlands: one Hero escapes the ruin with the relic while a companion lies Knocked Out beside a collapsed archway behind, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view: the escaping Hero strides toward the viewer at left, relic clutched to the chest, looking back over the shoulder; at right in the middle distance the collapsed archway with the fallen companion beside it.

SUBJECT DETAILS
* Hero in a soot-stained coat carrying a small cracked reliquary box
* Collapsed archway, its voussoirs fallen in a heap
* Fallen companion lying still beside the rubble
* Ash drifts and soot-blackened stones
* Dust still settling from the collapse as dry-brush drag
Must be shown exactly:
* Both the escaping Hero and the fallen companion read clearly

HUMAN ACTIVITY
* The Hero leaves, glancing back

ARTISTIC STYLE AND ATMOSPHERE
Victory paid for with someone left behind.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No gore.
* No enemies.
* Not the Reliquary of Broken Saints nave.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 26. The ford and the fallen column (`ART-END-TERRAIN`)

Save as `ART-END-TERRAIN.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE FORD AND THE FALLEN COLUMN - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a small stretch of Dying Lands ground that holds every kind of terrain a party must read: a shallow ford, a deep channel, a fallen column, a thorn hedge and a rubble field, with no one in it, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Slightly raised three-quarter view: a stream crosses the picture, a broken imperial column lies across it as a footbridge at the centre, stepping stones in the shallows to one side and a dark deep pool to the other; a thorn hedge and rubble frame the near bank.

SUBJECT DETAILS
* Fallen fluted column lying across the stream, moss on its top, one end resting on a statue base
* Shallow ford with stepping stones and ripples drawn in short broken strokes
* Deep channel below the column drawn as a solid black pool
* Reeds and a thorn hedge on the near bank
* Scatter of rubble blocks and a broken capital
* Mud bank with a single boot print
Must be shown exactly:
* No figures and no creatures

ARTISTIC STYLE AND ATMOSPHERE
Quiet ground that will cost time, footing or blood to cross.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the chapter 1 pass, the Greenmark climate road or the Mire walkway.
* No bridge of planks, no buildings.
* No square grid or measured lines.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 27. The bind (`ART-END-THE-ATTACK-SEQUENCE`)

Save as `ART-END-THE-ATTACK-SEQUENCE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE BIND - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the instant of defence in an attack: two blades locked at the crossguard in a Parry, close enough to see the notches, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Close crop at chest height: two gloved hands and two crossed blades fill the centre, locked near the hilts; the fighters' arms and shoulders fade into white paper at each side.

SUBJECT DETAILS
* Left blade: a plain longsword with a straight crossguard, held in a mailed glove
* Right blade: a heavy single-edged falchion in a bare scarred fist
* Blades crossed in an X near the guards, a notch biting into one edge
* Sleeves: a mail cuff on one arm, a padded sleeve on the other
* A few flicked sparks as ink flecks at the contact point
Must be shown exactly:
* Hands and blades only; no faces

HUMAN ACTIVITY
* Both fighters strain against the locked blades

ARTISTIC STYLE AND ATMOSPHERE
Strain, grit and a second that decides everything.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No full figures.
* No glow or motion blur.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 28. The drowned bell tower (`ART-END-THE-BESTIARY`)

Save as `ART-END-THE-BESTIARY.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE DROWNED BELL TOWER - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the lair of Vossegar of the Flooded Cathedral: the bell tower of a drowned cathedral standing out of black Mire water, one black coil breaking the surface beside it, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Water-level view: the broken bell tower rises at centre-right from flat black water; a single glossy coil of the wyrm arcs out of the water at left, the ripples between them the only movement.

SUBJECT DETAILS
* Gothic bell tower with an empty belfry arch and a cracked pinnacle, its lower windows drowned
* Black still water drawn in solid black with a few white ripple lines
* One sleek black coil with pitted scales arcing out of the water
* Dead reeds and the tip of a drowned stone cross
* Water weed hanging from the belfry sill
Must be shown exactly:
* Only one coil of the wyrm is visible; no head, wings or full body

ARTISTIC STYLE AND ATMOSPHERE
Hushed, heavy dread where the frogs no longer sing.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No full dragon and no breath.
* Not the Black Dragon or Vossegar portraits, and not the Serpent's Sunken Hoard sinkhole.
* No figures.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 29. The Antlered Path cairn (`ART-END-THE-CAMPAIGN-CYCLE`)

Save as `ART-END-THE-CAMPAIGN-CYCLE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE ANTLERED PATH CAIRN - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the Antlered Path Shrine: a cairn of three struck stones beside the old Greenmark trail, Old Wode's mark found on the journey home, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Low view from the trail: the cairn stands at the centre on the trail edge, ferns and roots crowding in on both sides, the trail itself fading into paper.

SUBJECT DETAILS
* Three rough stones stacked one on another, each bearing a single dented strike mark
* Moss on the lowest stone
* Old earthen trail with roots crossing it
* Fern fronds and a fallen branch
* A shed antler tine laid at the cairn's foot
Must be shown exactly:
* Exactly three stones; no figures

ARTISTIC STYLE AND ATMOSPHERE
Old, quiet blessing on the long walk home.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Whispering Grove standing stones.
* No carved symbols or runes.
* No glow.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 30. The shield shove (`ART-END-UNIVERSAL-ACTIONS`)

Save as `ART-END-UNIVERSAL-ACTIONS.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
THE SHIELD SHOVE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the Push: a Dwarf Hero driving a shield into an Orc raider and shoving them back toward a broken balustrade, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Side view on a short stretch of ruined terrace: the Dwarf at left with shoulder behind a round shield, the Orc at right rocked backward off balance, their heels at the broken edge, open air beyond.

SUBJECT DETAILS
* Dwarf: very broad and heavy, braided beard, mail, round shield braced with the shoulder, handaxe held back
* Orc: broad as a doorway, grey-skinned, heavy-jawed, lower tusks jutting, battleaxe and shield flung wide
* Broken stone balustrade with missing balusters behind the Orc
* Terrace paving cracked, one slab tilting
* Dust kicked up at the Dwarf's planted boots
Must be shown exactly:
* The Dwarf is pushing, not striking; the Orc is falling back

HUMAN ACTIVITY
* The Dwarf drives forward
* The Orc staggers back toward the edge

ARTISTIC STYLE AND ATMOSPHERE
Brute weight against brute weight.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the chapter 5 bridge clash and no undead.
* Do not give the Dwarf a greataxe or a horned helm.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 31. Whiteout (`ART-END-WEATHER-TABLES-BY-CLIMATE`)

Save as `ART-END-WEATHER-TABLES-BY-CLIMATE.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
WHITEOUT - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Whiteout Blizzard in the Pale City: two travellers roped together, bent into a storm that has erased the world around them, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Three-quarter view: the two travellers at the centre with the rope between them, leaning into driving snow from the right; around them almost nothing but white paper and slanting strokes.

SUBJECT DETAILS
* Lead traveller in a fur coat and arctic gear, hood drawn tight, rope in the fist
* Second traveller a few paces behind, one arm raised against the wind
* Rope sagging between them
* Driving snow as long slanting broken strokes
* A half-buried statue head emerging from a drift
Must be shown exactly:
* The storm is drawn in line only; the white is the paper

HUMAN ACTIVITY
* The two push forward into the wind

ARTISTIC STYLE AND ATMOSPHERE
Erased, isolated, enduring.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No grey wash or tonal fog.
* Not the Pale City climate gate.
* No Monsters.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 32. Rivals at the chest (`ART-END-WHAT-IS-HERALDRY-SKIRMISH`)

Save as `ART-END-WHAT-IS-HERALDRY-SKIRMISH.png`. Attach set A: `STYLE-REF-30-forest-path-stipple.jpg`, `STYLE-REF-58-waterfall-ruins-flight.jpg`, `STYLE-REF-55-siege-wall-climb.jpg`, `STYLE-REF-44-haden-vignette-farm.jpg`.

```text
RIVALS AT THE CHEST - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Two rival adventurers of the Dying Lands who have reached the same iron-bound treasure chest in a monster-haunted ruin at the same moment, while a Monster closes in behind them: the competitive PvPvE race for treasure in miniature, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Low three-quarter view: the chest sits at the centre on cracked flagstones, one rival crouched at each end with a hand on its ring handle; a broken wall stub rises behind the chest, and over its top reaches a single long clawed Monster arm, shape only.

SUBJECT DETAILS
* Iron-bound wooden treasure chest, lid still shut, corner straps rusted, one ring handle at each end
* Left rival: a Human in a battered ring shirt, shortsword half-drawn, one gauntleted hand on the handle
* Right rival: a lean Elf in a leather coat, dagger reversed in the free hand, the other hand on the opposite handle
* Neither looks at the other's face: both stare at the clawed arm coming over the wall
* Knee-high broken wall stub with moss and a fallen capstone, the clawed arm drawn in solid black
* A few coins spilled from a split seam, hatched dull with no stamps
* Cracked flagstones fading out in a few strokes on all sides
Must be shown exactly:
* Exactly two rival figures and one chest; the Monster shows only as one clawed arm and shoulder

HUMAN ACTIVITY
* Both rivals freeze mid-grab, each still gripping their end of the chest
* The clawed arm reaches over the wall top toward them

ARTISTIC STYLE AND ATMOSPHERE
Greed and dread in the same breath; the richest party is the one that bleeds.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Do not repeat the chapter 2 sighting across a fog valley or the cover's shrine arch.
* No full Monster figure, face or portrait.
* No banners or heraldic devices.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 33. Steadfast Word (`ART-END-DIVINE-PRAYERS`)

Save as `ART-END-DIVINE-PRAYERS.png`. Attach set B: `STYLE-REF-29-cleric-holy-fire.jpg`, `STYLE-REF-26-wizard-summoning-beast.jpg`, `STYLE-REF-28-wizard-vs-serpent-fiend.jpg`, `STYLE-REF-63-wizard-flame-hand.jpg`.

```text
STEADFAST WORD - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Steadfast Word, a Paladin's Tier 0 Orison: a mail-clad Paladin speaks one word over a fallen, Frightened companion and hauls them back to their feet, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Small scene vignette of the tradition's magic at work, densest at the caster and thinning into white paper toward irregular edges. Three-quarter view at knee height: the Paladin stands at the centre, leaning down, one hand locked around the companion's forearm; the companion rises from one knee at right, still half turned toward something off the edge of the picture.

SUBJECT DETAILS
* Paladin in a ring shirt with a targe on the free arm and a mace at the belt, mouth open on a single word
* Companion in a leather coat, pale and wide-eyed, rising from one knee with a dropped shortsword beside them
* A thin ring of short upright ink strokes rising from the ground around both figures
* Cracked flagstones and a few loose stones
* Forearm-to-forearm grip drawn large and clear as the focal point
Must be shown exactly:
* Exactly two figures; the Paladin is lifting, not striking

HUMAN ACTIVITY
* The Paladin speaks and pulls the companion upright
* The companion's fear breaks as they stand

ARTISTIC STYLE AND ATMOSPHERE
Plain courage passed from one hand to another.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No halo, sunburst or radiant glow.
* Not the Tier 1 lantern-healing priest or the Tier 2 roadside shrine.
* No longsword drawn and no enemy in frame.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 34. Vine Lash (`ART-END-DRUIDIC-RITUALS`)

Save as `ART-END-DRUIDIC-RITUALS.png`. Attach set B: `STYLE-REF-29-cleric-holy-fire.jpg`, `STYLE-REF-26-wizard-summoning-beast.jpg`, `STYLE-REF-28-wizard-vs-serpent-fiend.jpg`, `STYLE-REF-63-wizard-flame-hand.jpg`.

```text
VINE LASH - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Vine Lash, a Druid's Tier 0 Minor Ritual: a thorned vine bursts from the soil, snares a Bandit by the ankle and drags them toward the Druid, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Small scene vignette of the tradition's magic at work, densest at the caster and thinning into white paper toward irregular edges. Low side view: the Druid stands at left with one fist pulled back; a single thorned vine snakes across the ground from the Druid's feet to the Bandit at right, who pitches forward with the vine wrapped around one ankle.

SUBJECT DETAILS
* Druid in a lichen-stained coat, hood back, quarterstaff in the other hand, no metal
* One thick thorned vine with a few leaves, taut like a rope
* Bandit: a hard-faced deserter in a stolen pauldron, dagger flung wide, falling forward
* Torn soil and flung clods as flicked ink flecks along the vine's path
* Tufts of grass and a stone
Must be shown exactly:
* The vine visibly links Druid and Bandit

HUMAN ACTIVITY
* The Druid pulls; the vine drags the Bandit off balance toward them

ARTISTIC STYLE AND ATMOSPHERE
The ground itself takes a side.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No metal weapon, armour or shield on the Druid.
* Not the Tier 1 kneeling root ritual or the Tier 2 bending trees.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 35. Telekinetic Hand (`ART-END-PSYCHIC-ABILITIES`)

Save as `ART-END-PSYCHIC-ABILITIES.png`. Attach set B: `STYLE-REF-29-cleric-holy-fire.jpg`, `STYLE-REF-26-wizard-summoning-beast.jpg`, `STYLE-REF-28-wizard-vs-serpent-fiend.jpg`, `STYLE-REF-63-wizard-flame-hand.jpg`.

```text
TELEKINETIC HAND - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Telekinetic Hand, a Psion's Tier 0 Technique: the Psion lifts an iron door latch from across a cellar with no more than a look, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Small scene vignette of the tradition's magic at work, densest at the caster and thinning into white paper toward irregular edges. Three-quarter view: the Psion stands at left, two fingers raised toward the door; at right a heavy plank door with an iron thumb-latch, the latch bar lifted clear of its keeper with nothing touching it.

SUBJECT DETAILS
* Psion in a plain hide cuirass with a dagger at the belt, eyes fixed and unblinking
* Heavy plank door with iron strap hinges and a thumb-latch rising on its own
* A few faint concentric ripples drawn around the latch
* Stone cellar floor and a worn step
* A dust trickle falling from the door frame
Must be shown exactly:
* The latch moves with no hand touching it

HUMAN ACTIVITY
* The Psion lifts the latch by thought alone

ARTISTIC STYLE AND ATMOSPHERE
Quiet, eerie precision.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No glow beams or lightning.
* Not the Tier 1 hovering-pebble meditation.
* No treasure chest or trap.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 36. Blood Flicker (`ART-END-SORCERIES`)

Save as `ART-END-SORCERIES.png`. Attach set B: `STYLE-REF-29-cleric-holy-fire.jpg`, `STYLE-REF-26-wizard-summoning-beast.jpg`, `STYLE-REF-28-wizard-vs-serpent-fiend.jpg`, `STYLE-REF-63-wizard-flame-hand.jpg`.

```text
BLOOD FLICKER - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Blood Flicker, a Sorcerer's Tier 0 Sorcery: the Sorcerer blinks two strides through the air, leaving a spray of their own blood hanging where they stood, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND WHITE VIGNETTE
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
The illustration must have a natural, irregular, hand-drawn white vignette around all four edges. The artwork gradually dissolves into blank ivory-white paper through increasingly sparse pen strokes, broken outlines and diminishing hatching.
Leave approximately 5-8% clean white margin around the perimeter, with an additional organic transition zone. Avoid digital blur, artificial feathering, or hard rectangular cropping. Keep crisp line and strong contrast at the focal point.

COMPOSITION
Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes. Small scene vignette of the tradition's magic at work, densest at the caster and thinning into white paper toward irregular edges. Side view: at left a small cloud of blood droplets hangs in the air above two empty footprints; at right the Sorcerer has just landed mid-step, cloak still settling, one hand pressed to a cut wrist.

SUBJECT DETAILS
* Gaunt Sorcerer in torn dark cloth layers, quarterstaff in one hand, no metal armour
* Fresh cut on the wrist with a bead of blood
* Hanging droplets drawn as small black teardrops, a few stretched sideways toward the Sorcerer
* Two empty footprints in the dust at the vacated spot
* Cracked flagstones with a single weed
Must be shown exactly:
* One Sorcerer only, drawn once (not as a double image)

HUMAN ACTIVITY
* The Sorcerer lands from the blink and glances back at the blood

ARTISTIC STYLE AND ATMOSPHERE
Speed bought in blood, cheaply and too often.
Ink it gritty and bold, like old-school rulebook art: strong brush contours of uneven weight, large shapes of solid black for shadow, night and depth, and rough, scratchy hatching and dry-brush drag where light turns into shadow, with the bite of a woodcut. High contrast: let solid black and open white paper carry the picture, with few in-between textures. Visible human marks are welcome: broken lines, dry-brush streaks, a few flicked ink spatters. Put the deepest blacks and sharpest contrast at the focal point and let distance thin to simpler, lighter line. No stipple fields, no uniform micro-texture, no tonal haze, no smooth digital rendering. Accurate perspective, believable construction and coherent geography; the world shows withered beauty: once-grand things rusted, cracked, overgrown or hollowed by age. It must look drawn by hand with brush and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No metal Chest armour on the Sorcerer.
* No glow, motion blur or ghost image.
* Not the Tier 1 cut-palm close-up or the Tier 2 storm between the hands.
* No gore.
Avoid photorealism, digital-render polish, clean vector-like line, uniform machine texture, stipple fields, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, artificial symmetry and competing focal points. The finished artwork should be gritty and high-contrast and print crisply in pure black ink, with an organically fading white vignette, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 37. Hook, rope, and spikes (`ART-END-ADVENTURING-EQUIPMENT`)

Save as `ART-END-ADVENTURING-EQUIPMENT.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
HOOK, ROPE, AND SPIKES - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the adventurer's breaking-in tools: a grappling hook with coiled rope, iron spikes, a crowbar and a bag of caltrops, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a flagstone: the hook at the centre with rope coiled around it, crowbar laid across the front, spikes and caltrop bag beside. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Three-pronged grappling hook
* Thick coil of rope knotted to the hook
* Crowbar with a split end
* Handful of iron spikes
* Small sack of caltrops, a few spilled
Must be shown exactly:
* Only these items

ARTISTIC STYLE AND ATMOSPHERE
Practical tools for doors that were not meant to open.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No lantern.
* Not the background still lifes.
* No labels.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 38. Brigandine on the stand (`ART-END-ARMOUR`)

Save as `ART-END-ARMOUR.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
BRIGANDINE ON THE STAND - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a Brigandine, a coat of plates, hung on a wooden armour stand over a Gambeson, scarred and ready, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life of a single cross-shaped wooden stand at the centre wearing the armour, a mail coif draped on its top. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Brigandine with rows of rivet heads over hidden plates, cloth cover torn in places
* Quilted gambeson under it with the sleeves hanging
* Mail coif draped over the stand's head
* Buckles at the side, one strap cut
* Base of the stand on a scrap of floor
Must be shown exactly:
* One stand, no wearer

ARTISTIC STYLE AND ATMOSPHERE
Protection that has already been tested.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Armoury room.
* No full plate or knight's helm.
* No heraldic devices.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 39. Three starting bundles (`ART-END-CHOSEN-AND-RANDOM-CREATION`)

Save as `ART-END-CHOSEN-AND-RANDOM-CREATION.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
THREE STARTING BUNDLES - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Three bound starting-kit bundles laid side by side on a hiring-hall bench, a small coin pouch beside them: the choice, or the chance, of a new Hero's first gear, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a worn bench end viewed at slight elevation: three bundles in a row, each tied with cord and each a different shape, the pouch at the near corner. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* First bundle: a shortsword in a scabbard rolled with a gambeson
* Second bundle: a shortbow lashed to a quiver and a leather coat
* Third bundle: a quarterstaff tied across a satchel
* Small drawstring coin pouch, a few coins showing, no stamps
* Cord knots and frayed ends
* Worn bench boards with nail heads
Must be shown exactly:
* Exactly three bundles

ARTISTIC STYLE AND ATMOSPHERE
A whole life packed small.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the chapter 6 hiring hall interior.
* No labels or tags.
* No figures.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 40. The pierced breastplate (`ART-END-CRITICAL-HITS-AND-EXPLODING-DAMAGE-DICE`)

Save as `ART-END-CRITICAL-HITS-AND-EXPLODING-DAMAGE-DICE.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
THE PIERCED BREASTPLATE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the aftermath of a Critical Hit: a steel breastplate punched clean through by a crossbow bolt, beside a helm crushed flat by a blunt blow, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a scrap of trampled ground at slight elevation: the breastplate lies on its back at the centre with the bolt standing out of it, the dented helm on its side beside it. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Steel cuirass with a crossbow bolt driven through the centre, the hole clean and puckered
* Fletching of the bolt torn and bent
* Open-faced helm caved in on one side, a rivet sprung
* Torn leather strap and a broken buckle
* A split shield rim at the edge of the arrangement
* Trampled grass and mud under the pieces
Must be shown exactly:
* No wearer and no body

ARTISTIC STYLE AND ATMOSPHERE
Armour that did not matter in the end.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No blood or gore.
* Not the Armoury room racks or the armour still life.
* No maker's marks.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 41. The full pack (`ART-END-EQUIPMENT-OVERVIEW`)

Save as `ART-END-EQUIPMENT-OVERVIEW.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
THE FULL PACK - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of an adventurer's fully loaded pack set down at the end of a day's march, the reasonable load every Hero carries, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a small patch of ground: the pack slumped on its side at the centre with gear lashed all over it. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Heavy canvas and leather pack with worn straps
* Bedroll lashed on top
* Hooded lantern hanging from a side ring
* Waterskin and a tin cup
* Coil of rope and a torch thrust under a strap
* Bandage roll poking from a side pouch
Must be shown exactly:
* One pack only

ARTISTIC STYLE AND ATMOSPHERE
Weight, wear and readiness.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No weapons in the arrangement.
* Not the background still lifes.
* No labels.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 42. The broker's scale (`ART-END-ITEM-AVAILABILITY`)

Save as `ART-END-ITEM-AVAILABILITY.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
THE BROKER'S SCALE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the price of rarity: a Grand Hall broker's balance with a heap of coins on one pan outweighed by a single old ring on the other, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a counter end: the balance scale stands at the centre, the ring pan dipped low and the coin pan high. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Brass balance on an iron post, beam tilted
* Low pan: one heavy old ring set with a dull stone
* High pan: a heap of tarnished coins, no stamps
* Spare weights in a row, one missing
* Counter edge worn smooth, a candle stub
Must be shown exactly:
* The single ring outweighs the coins

ARTISTIC STYLE AND ATMOSPHERE
Some things cannot simply be bought.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Treasure Tables still life.
* No sparkle effects.
* No readable marks.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 43. The Bell's Tongue (`ART-END-PERMANENT-SPECIAL-ITEMS`)

Save as `ART-END-PERMANENT-SPECIAL-ITEMS.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
THE BELL'S TONGUE - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the Bell's Tongue, a clapper torn from a very old bell, lying beside the Bell-Shard Charm, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on stone: the heavy clapper lies across the centre, the shard charm on its cord curled beside it. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Long iron bell clapper with a ball end, pitted and frosted with rime
* Bell-shard: a curved fragment of bell bronze on a leather cord
* Stone surface with damp patches
* A few rime crystals
Must be shown exactly:
* Only the clapper and the charm

ARTISTIC STYLE AND ATMOSPHERE
Cold, old and listening.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No ringing lines or sound effects.
* Not the Voice Beneath the Bells boss.
* No runes.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 44. Staff, sword, and symbol (`ART-END-RANDOM-CLASS-TABLE`)

Save as `ART-END-RANDOM-CLASS-TABLE.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
STAFF, SWORD, AND SYMBOL - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of Three callings in three objects: a caster's quarterstaff crossed over a soldier's shortsword, a cleric's holy symbol hanging from the staff, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a flat stone at slight elevation: staff and sword crossed in a low X at the centre, the holy symbol dangling on its chain from the staff's head. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Plain ash quarterstaff, scuffed and iron-free
* Shortsword in a worn scabbard with a wrapped grip
* Holy symbol as a simple disc on a chain, chipped, no readable mark
* Flat stone with a crack and a lichen patch
* A few dry leaves
Must be shown exactly:
* Only these three objects

ARTISTIC STYLE AND ATMOSPHERE
Different roads into the same dark.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Magic in the Dying Lands altar still life.
* No runes or glyphs.
* No glow.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 45. Lesser missiles (`ART-END-RANGED-WEAPONS`)

Save as `ART-END-RANGED-WEAPONS.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
LESSER MISSILES - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of the humbler ranged weapons of the Dying Lands laid together: a hand crossbow, a blowgun with darts, a coiled lasso and two javelins, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life viewed at slight elevation on a scrap of sacking: javelins laid diagonally behind, hand crossbow at the centre, blowgun and lasso in front. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Hand crossbow, small one-handed, with a bolt laid beside it
* Blowgun of hollow reed with three darts
* Coiled rope lasso with a running noose
* Two javelins with leaf-shaped iron heads
* Sacking cloth with a frayed edge
Must be shown exactly:
* Only the four named weapons; no bows

ARTISTIC STYLE AND ATMOSPHERE
Small tools for close murder.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* Not the Melee Weapons still life.
* No shortbow, longbow or greatbow.
* No maker's marks.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 46. The contract and the map (`ART-END-READING-A-SCENARIO-BEFORE-SETUP`)

Save as `ART-END-READING-A-SCENARIO-BEFORE-SETUP.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
THE CONTRACT AND THE MAP - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a party's preparation before an expedition: a sealed Guild of Keys contract and a hand-drawn map of the approaches, weighted down with a dagger and a candle stub, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a table corner at slight elevation: the map lies unrolled at the centre, its corners held by a dagger and a candle stub, the folded contract with its wax seal laid across one edge. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Map drawn only with abstract lines: a river, a cluster of ruin squares and a road, no lettering
* Folded contract with a plain wax seal and no device
* Dagger pinning one corner
* Candle stub in a dish with wax runs
* Stick of chalk and a chalk scuff on the table edge
Must be shown exactly:
* No legible writing, numbers or symbols on map or contract

ARTISTIC STYLE AND ATMOSPHERE
Studied caution before the danger.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No compass rose or grid on the map.
* Not the War Room interior.
* No figures.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```

## 47. The spent scroll (`ART-END-SCROLLS`)

Save as `ART-END-SCROLLS.png`. Attach set C: `STYLE-REF-15-sword-mace-items.jpg`, `STYLE-REF-40-rag-wrapped-scythe.jpg`, `STYLE-REF-27-carved-scroll-case.jpg`, `STYLE-REF-33-bound-bone-cross.jpg`, `STYLE-REF-56-weapons-sheet.jpg`.

```text
THE SPENT SCROLL - GRITTY OLD-SCHOOL INK ILLUSTRATION

Create a gritty, old-school black-and-white ink illustration of a scroll destroyed in the reading: one scroll crumbling to ash beside an open leather case of sealed, unused scrolls, in the dark fantasy world of Heraldry Skirmish, drawn the way a human illustrator inked the interior art of a late-1970s or 1980s fantasy rulebook or adventure module: brush, dip pen and India ink on paper, with the bite of a woodcut.

FORMAT AND ISOLATION
Wide 3:2 landscape composition. Pure black ink on warm ivory-white paper, with no colour, lettering, borders, or decorative framing.
A still-life arrangement isolated on blank ivory-white paper, resting on a small surface that fades out in a few sparse strokes. No figure and no background scenery.
Leave at least 8% clean white margin on every side; nothing touches or is cropped by the image edge.

COMPOSITION
Still life on a flat stone: the case lies open at left with three rolled scrolls inside, the spent scroll at right curling and flaking into ash. Closing tailpiece at the foot of a page, printed about 2.6 to 3.3 in wide and as short as 1.6 in: one clear focal subject with a strong silhouette in the middle of the frame, generous open white paper around it, and every edge dissolving into the paper in sparse broken strokes.
Still-life arrangement of the described objects, worn and used. Isolated on white paper with only a small patch of ground and its cast shadow; no background scenery.

SUBJECT DETAILS
* Leather scroll case with a strap and a brass cap
* Three rolled scrolls tied with cord, plain wax seals with no device
* Spent scroll curling, its edges blackened, ash flakes drifting
* Unreadable faint lines on the spent sheet only as abstract marks
* Stone surface with a crack
Must be shown exactly:
* No legible writing anywhere

ARTISTIC STYLE AND ATMOSPHERE
Power used once and gone.
Ink it like old-school rulebook equipment art: a bold, rough contour of uneven weight around each object, heavy solid-black shadow shapes, and scratchy hatching or dry-brush drag that follows each material: grain on wood, dents and pits on metal, folds and wear on leather and cloth. High contrast, with few in-between textures. Each object reads as a clear silhouette first and detail second: no stipple fields, no uniform micro-texture, no over-rendered surfaces. Light falls from the upper left. Believable construction, worn and used. It must look drawn by hand with brush, pen and ink, not generated or rendered.

FINAL VISUAL REQUIREMENTS
Do not draw:
* No lettering, numbers, dice, game tokens, or rulebook pages.
* No runes or glyphs.
* No glow.
* Not the Tier 2 Arcane copying scene.
Avoid photorealism, digital-render polish, clean vector-like line, stippled or noisy texture, painterly shading, smooth gradients, grey wash or grey ink tones, airbrush, colour, typography, readable runes, watermarks, signatures, modern objects, cartoon or anime proportions and cropped limbs. The finished artwork should be gritty, bold and readable at small size and print crisply in pure black ink, like original ink art in an old-school fantasy rulebook.

STYLE REFERENCES
The attached reference images show the target ink style. Match their bold, rough contours, heavy solid blacks, scratchy hatching, dry-brush texture, contrast and finish. Some are centuries-old etchings or woodcuts: take only their line, blacks and finish, never their period costume. Do not copy their subjects or compositions, and draw in pure black ink only.
```
