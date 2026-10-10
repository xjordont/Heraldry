# Retries: narrow corrections and the attempt budget

## Budget

At most the item's `max_attempts` generations (the queue says; usually 3, cover and chapters 5). Never exceed it. The helper counts every distinct image you run through `check`, shows "attempt N of M", and fails an attempt beyond the budget. Stop at the first attempt with no hard fail. After the last allowed attempt save the best one with `--accept-flags` and say in `--notes` what is still wrong. The reviewer can send the item back; you do not need to keep trying.

An edit through the image tool's own edit or regenerate control counts as an attempt. Never open an image in any other editor.

## How to retry

A retry prompt is the verbatim prompt plus at most two correction sentences at the very end. Each names what to change and what to keep. Put the failure that breaks the earliest-numbered hard fail first. If a failure persists, repeat or sharpen its sentence; never stack more than two. Record the sentences in `--notes`. The receipt's `prompt_sha256` stays the queue's value: the corrections are a recorded addition, not a different prompt.

If a retry makes the image worse, go back to the better earlier one and use that.

## Correction sentences

| Failure | Add this sentence |
|---|---|
| Wrong count of limbs, eyes or heads | `Correction: exactly <N> <parts>, <layout>. Keep the pose and composition.` |
| A must-show item missing or wrong | `Correction: <the item, as the prompt states it> must be clearly visible. Keep everything else.` |
| A do-not-draw item present | `Correction: remove <the item>. Keep everything else.` |
| Scenery behind a figure or still life | `Correction: no background. Only a small ground patch and cast shadow, pure white paper everywhere else.` |
| Figure cropped or too close to the edge | `Correction: the whole subject fits inside the frame with at least 8% white margin on every side.` |
| Frame, border or box | `Correction: no border, frame or box of any kind.` |
| Hard crop or no vignette on a scene | `Correction: the drawing dissolves into blank white paper at all four edges and corners.` |
| Lettering or runes | `Correction: no letters, runes, signs or writing anywhere.` |
| Grey wash or soft shading | `Correction: no grey tone anywhere. Shade only with black ink hatching and stippling.` |
| Colour | `Correction: black ink only, no colour at all.` |
| Paper texture, stains or darkened corners | `Correction: perfectly flat, clean white paper with no texture or shading.` |
| Reference bleed | `Correction: do not include <trees, standing stones, a palisade or a bridge>. The subject is only <the subject>.` |
| A scale figure that was not asked for | `Correction: no human figure. Draw the creature at the stated size.` |
| Missing scale figure that was asked for | `Correction: include one small human figure for scale, as described.` |
| Hands, grips or weapons wrong | `Correction: the <weapon> is held correctly in <both/one> hand<s>. Keep everything else.` |
| Soft, blurry or hazy | `Correction: crisp, fine pen lines with sharp contrast and no haze.` |
| Subject too small or too fine to read when printed small | `Correction: draw the subject larger, filling about 70% of the frame, with fewer and bolder forms.` |
| Same pose or composition as a sibling | `Correction: <the pose or camera the prompt describes>, a different composition from the references.` |

## When a requirement seems to clash

A must-show item that looks opposed to a do-not-draw line is almost always about scale or focus, not a contradiction. Satisfy both the narrowest way: draw the required item as small and incidental as the prompt's composition places it, and do not make it the subject. Do not stop, and do not use `--accept-flags`.

If the prompt truly cannot be satisfied, or contradicts the rulebook text it quotes, do not fix it. Generate once as written, save with a note, and put the contradiction in your report. Claude Code owns the prompts.
