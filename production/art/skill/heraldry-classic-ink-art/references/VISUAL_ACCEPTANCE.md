# Visual acceptance and artistic consistency protocol

This is a visual inspection rubric, not a numerical model of artistic merit. Do not claim the automatic diagnostics prove style match or aesthetic quality. The image generation operator submits an evidence-backed native-image review; the independent reviewer approves final artwork.

## Evaluate in three views

1. **At final print width**: Can the subject be identified instantly? Are the important silhouette, landmark, expression, or action still readable? Details that collapse at 1.6–1.9" print width cannot carry required story information.
2. **Native image at full resolution**: Are contours variable in width? Does the crosshatching describe the object's shape, instead of forming generic grey noise? Are physical structures and anatomy believable? Inspect the face/limbs/weapon grip or gates/rooflines/pathways as relevant.
3. **Alongside its queue-provided style references**: Compare drawing grammar, deep-black placement, paper brightness, hatch density, focal weighting, and degree of finished detail. For large scenes compare against scenic examples; for spot creatures compare against the figure example. The item chooses reference assets; never attach additional samples at generation time.

## Mandatory visual qualities

- **Material-specific lines:** Bark uses branching fissures and wrapped grain; timber follows beams and joins; stone respects courses and cracks; metal reflects through white reserve and sharply placed black shadows; cloth follows folds; skin, fur and scales have anatomical patterning.
- **Hierarchical stroke weight:** Heavy outer and occlusion lines; delicate construction and texture marks; finer distant strokes. Avoid equal line weight across the image.
- **Clear value organisation:** Bold solid-black masses and an obvious white-paper reserve, high contrast. Scratchy hatching and dry-brush produce the few mid-values; stipple fields and airbrush-like greys do not.
- **Light consistency:** One coherent upper-left light source unless the item explicitly specifies otherwise. Deep blacks should correspond to real recesses, occlusion, and cast shadow.
- **Architectural coherence:** Fortifications have an intelligible defended perimeter; roads lead to gates; streets connect districts; bridges have realistic supports and destinations; buildings show believable roof structures. Cities require sufficient apparent density for their stated scale.
- **Subject distinction:** Do not transplant distinctive Greythorn elements into other locales. Preserve biome identity (forest, urban ruin, caverns, ice, desert, mire) through material and construction, not atmospheric gradients.
- **Four-sided vignette or isolation:** Scenic compositions dissolve through shorter, interrupted contours into blank paper on *all four* edges. Objects and full-length portraits instead sit on white with clear outer margins. No feathered photo border.
- **Human agency:** Populate relevant large locations with correctly scaled activity, but no unwanted human scale figure in isolated objects or creatures.
- **Repetition control:** Check duplicated rooftops, cloned crowds, matching poses, identical flowers, implausible repeating masonry and architecture.
- **Typography exclusion:** Pseudo-writing, symbols that resemble letters, watermarks, grids, decorative picture frames and signatures are unacceptable unless a specific queued item explicitly demands symbols.

## Comparison log in QA report

Before a passing `save`, complete the QA draft that `qa ID FILE` writes for the exact file you will save:

- Set `prompt_unchanged: true` only when the actual generation input was the queued prompt, apart from the allowed documented correction sentences.
- Set `references_attached: true` only when all queue-listed assets were actually attached, in the listed order.
- Set `visual_review_at_print_size: true` only after inspecting the physical print-width preview.
- Set `register_compared` to `scene`, `figure`, `still_life`, `portrait`, `creature`, `interior`, or `other` according to the artwork.
- Complete all ten `checks` with a true/false decision and specific visible evidence. Avoid boilerplate, vague praise, or generic identical explanations.
- Record genuine failures in `unresolved_issues`; a failed visual criterion is shipped as a flagged, *unapproved* image (`--accept-flags`), never retried; the reviewer decides on a redo.

## Batch drift assessment

Every tenth saved image (`status` says DRIFT REVIEW):

1. Run `heraldry_art.py sheet --recent 10 --refs`.
2. Run `style_audit.py --repo . --recent 10` (report in the scratch folder) for advisory tone and four-edge statistics by register.
3. Compare same-register siblings and references together. A single scene's greater ink coverage may be legitimate; the statistics never overrule artistic inspection.
4. Deliver in every case and continue. If **two or more** siblings show the same serious line, tone or vignette drift, flag it in your report for Claude Code, which reviews the references or prompts upstream and sends redos.
5. Never add contact sheets, debug JSON, style reports or print proofs to the repository. Keep them outside the clone or package as explicit scratch handoffs.

## Final approval boundary

The generator confirms *eligibility for review*, not quality acceptance. Claude Code/owner determines whether artwork fits the book, whether it is distinctive, and whether it should be published. There is no 'perfect score' that bypasses independent approval. Exact recreation of an already approved image means replaying the registered bytes, not stochastic regeneration.
