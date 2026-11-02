# Corrections for redos

## One generation per item

Every item gets exactly one generation per round (`max_attempts` 1; owner 2026-10-12: first generations were far better than any retry). There are no retries. A defective image is saved with `--accept-flags --notes`, and a rejection sends it back as a redo. An edit through the image tool's own edit or regenerate control counts as a generation. Never open an image in any other editor.

## Redos

A redo is a fresh round: one new generation in a fresh context (no earlier image of the item in view). Its prompt is the verbatim prompt plus at most two correction sentences at the very end, based on the rejection reason. If the reason contradicts the prompt, the prompt wins: say so. Each sentence names what to change and what to keep. Record the sentences in `--notes`. The receipt's `prompt_sha256` stays the queue's value: the corrections are a recorded addition, not a different prompt.

## Correction sentences

| Failure | Add this sentence |
|---|---|
| Wrong count of limbs, eyes or heads | `Correction: exactly <N> <parts>, <layout>. Keep the pose and composition.` |
| Wrong subject (hard fail 1) | `Correction: this is <the subject exactly as the prompt's first line states it>, not <what the attempt shows>. Keep the format and the style.` |
| A must-show item missing or wrong | `Correction: show <the item exactly as the prompt lists it>, clearly and unmistakably. Keep everything else.` |
| A do-not-draw item present | `Correction: remove <the item>. Keep everything else.` |
| Scenery behind a figure or still life | `Correction: no background. Only a small ground patch and cast shadow, pure white paper everywhere else.` |
| Figure cropped or touching the edge | `Correction: the whole subject fits inside the frame with clear white space on every side.` |
| Frame, border or box | `Correction: no border, frame or box of any kind.` |
| Hard crop or no vignette on a scene | `Correction: the drawing dissolves into blank white paper at all four edges and corners.` |
| Lettering or runes | `Correction: no letters, runes, signs or writing anywhere.` |
| Too clean, timid or finely engraved (unlike the gritty references) | `Correction: bolder, rougher brush contours, heavy solid-black shadows and scratchy hatching; less fine detail.` |
| Grey wash or soft shading | `Correction: no grey tone anywhere. Shade only with solid black, black ink hatching and dry-brush.` |
| Colour | `Correction: black ink only, no colour at all.` |
| Paper texture, stains or darkened corners | `Correction: perfectly flat, even paper with no texture, stains or shading.` |
| Reference bleed | `Correction: do not include <the leaked reference subject, e.g. a throne, a moon or a crowd of skulls>. The subject is only <the subject>.` |
| A scale figure that was not asked for | `Correction: no human figure. Draw the creature at the stated size.` |
| Missing scale figure that was asked for | `Correction: include one small human figure for scale, as described.` |
| Hands, grips or weapons wrong | `Correction: the <weapon> is held correctly in <both/one> hand<s>. Keep everything else.` |
| Soft, blurry or hazy | `Correction: crisp, bold ink lines with sharp contrast and no haze.` |
| Subject too small or too fine to read when printed small | `Correction: draw the subject larger, filling about 70% of the frame, with fewer and bolder forms.` |
| The tool returned a reference or another item's image (`check` says byte-identical or looks almost identical) | `Correction: draw a new picture of <the subject>; it must not resemble any attached reference image or any other illustration.` |
| Same pose or composition as a sibling | `Correction: <the pose or camera the prompt describes>, a different composition from the references.` |

## When a requirement seems to clash

A must-show item that looks opposed to a do-not-draw line is almost always about scale or focus, not a contradiction. Satisfy both the narrowest way: draw the required item as small and incidental as the prompt's composition places it, and do not make it the subject. Do not stop, and do not use `--accept-flags`.

If the prompt truly cannot be satisfied, or contradicts the rulebook text it quotes, do not fix it and do not generate it. Record `refuse ID --reason "prompt cannot be satisfied: <what clashes>"`, list it in your report and move on. The prompt is then fixed in the catalogue and republished.
