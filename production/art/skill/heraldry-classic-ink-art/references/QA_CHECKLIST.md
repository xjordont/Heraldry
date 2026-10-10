# QA checklist

Two layers. The script catches mechanical problems. You catch everything else by looking.

## 1. Mechanical tripwires (the helper's `check ID FILE`; its full command is in SKILL.md)

Calibrated on the approved Greythorn render, the three owner style samples and synthetic defects (grey wash, frame, crop, tint, grain, blur). They are tripwires, not a quality score: a PASS does not mean the art is good.

| Tripwire | FAIL means | WARN means |
|---|---|---|
| aspect, size, format | The image is not the queue's size ratio (5% tolerance), is under 1000 px on the long side, or is not PNG, JPEG or WEBP. Regenerate. | |
| colour | More than 25% saturated pixels: a coloured image. | More than 10%: tinted ink or coloured accents. Look closely. Dark brown-black ink is fine. |
| blank, sparse | Almost no ink. | Very little ink: the subject may be tiny or faint at print size. |
| soft | | Blurry linework. Pen lines should be crisp. |
| paper | Dark or tinted background. | Paper not clean white: stains, darkened vignette, or a grey wash. |
| grain (figures, still lifes) | | Noise in the margin. The background must be flat. |
| wash (figures, still lifes) | Heavy grey wash. | Possible grey wash or soft shading. |
| edge (figures, still lifes) | Ink touches the image edge: a cropped limb, weapon, shadow or frame. | Stray marks at the edge, or the drawing enters the outer 6% margin. |
| edge (scenes) | Ink runs to the edge: no vignette, or a frame or box. | Marks reach the outer 2%: check all four edges fade out. |
| copy | Byte-identical to another delivered image or to one of the item's references. | Looks almost identical to one (a re-encoded or resized copy, within 16 of 256 difference bits): look before saving. |
| budget | More images checked than the item's attempt budget. | |

The intake's own flags (`colour`, `gray_wash`, `frame_or_box`) are printed as `info`. They go to the reviewer and do not reject anything. Dense, good scenes can approach them: the approved Greythorn render sits at 0.59 on a 0.60 grey-wash flag.

On a WARN, look at the thing it names. A WARN you looked at and judged fine needs no action.

## 2. Visual checklist

Run it on the image and on the print-size preview. `check` repeats the item's MUST and DO NOT DRAW lines for you; `save` asks you to state what you counted for each MUST line and to confirm the DO NOT DRAW items are absent, so do the counting first. These are the ten hard fails in SKILL.md. How to check each:

1. **Subject and source.** Re-read the prompt's SOURCE TEXT. Is this the creature, place or object it describes? Does anything contradict it?
2. **Must list.** Take each "Must be shown exactly" line and verify it by counting (legs, eyes, heads, arms, weapons, shields) or by finding the object.
3. **Do-not-draw list.** Take each line and confirm it is absent. Check scenario and boss images especially: named creatures, rival entries and "no people" lines are easy to break.
4. **Lettering.** Scan signs, banners, shields, books, bark, stonework, hilts, belts and the margins for letter-like marks.
5. **Pure ink.** No colour, grey wash, gradients, paper texture or soft shadows.
6. **Edges.** Scene: the drawing thins out to blank paper on all four sides, including the corners. Figure or still life: whole subject, about 8% white margin on every side, only a small ground patch and cast shadow, no box or frame.
7. **Reference bleed.** The bleed list in `references/STYLE.md`.
8. **Anatomy and construction.** Hands and grips. Every weapon is held or sheathed. Limbs attach. Armour has joints. Roofs, bridges and stairs connect to something. No repeated clones.
9. **Scale.** Matches the `Size:` line. No scale figure unless asked.
10. **Print-size legibility.** In the preview the subject is one unmistakable silhouette.

Any failure of 1–10 is a retry (`references/REPAIR.md`).

## 3. Soft style check

Put the image beside its references. Is the line weight, hatch density, contrast and finish the same hand? Note "heavier", "lighter", "greyer" or "cleaner than the references" in the receipt notes. Do not retry for taste alone: the reviewer decides.

## 4. Batch drift review

After each batch, view `sheet --refs`. Look for:

- the line gradually thinning, thickening or going grey;
- the same pose, camera or composition repeating within a family;
- scenery creeping in behind figures;
- paper tone or finish changing between items.

Redo the one or two worst if attempts remain. If the whole batch drifted, stop and tell the owner; starting a fresh conversation usually resets it.

## Receipt format

`save` writes it. By hand, append one JSON line per image to `production/art/gpt/RECEIPTS.jsonl`:

```json
{"id": "ART-MON-GOBLIN", "prompt_sha256": "<the item's prompt_sha256 from QUEUE.json>", "surface": "ChatGPT Work", "model": "<image model if shown, else not shown>", "date_utc": "2026-10-10", "variants_tried": 2, "notes": "<anything unusual, including any correction sentence added>", "must_checked": ["<what you counted for each MUST line>"], "avoid_clear": true}
```

`variants_tried` is the total number of generations made for the item, the saved one included. `save` fills it from the images you checked. `must_checked`, `avoid_clear`, `tripwires`, `accepted_flags` and `accepted_at_attempt` are optional extras the reviewer reads; a later receipt for the same ID replaces an earlier one.

A refusal: `{"id": "...", "refused": true, "reason": "<the tool's message>", "surface": "ChatGPT Work", "date_utc": "..."}`.
