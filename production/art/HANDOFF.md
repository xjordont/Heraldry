# Heraldry atmospheric artwork handoff

The twelve required native PNG masters were generated and visually reviewed in ChatGPT Work on 2026-10-07 UTC. ART-CH01-001 (Greythorn) is the shared linework anchor. ART-CH04-001 is the correction of the exact owner-selected skeleton image: the third arm was removed.

The master files are in `assets/art/incoming/`. Exact prompts are in `PROMPTS.json`; source lore, hashes, dimensions, alpha information and placement limits are in `ART_MANIFEST.json`. Keep native masters unchanged and make any necessary production derivatives separately.

## Next Claude iteration

Work on main using RC485. Do not increment the manuscript version for this art/layout iteration. Fetch the original PNGs with `git lfs pull --include="assets/art/incoming/*.png" --exclude=""`. Run `python tools/check_art.py` before typesetting.

1. Apply `docs/DESIGN_REFINEMENT.md` to the stress specimen, then the full book.
2. The existing chapter renderer detects ART-CH01 through ART-CH11, but its full-width 3.6-inch image box must be reduced to each manifest placement limit. Center the native image, preserve its aspect ratio and its alpha. Do not stretch it, invent pixels or claim a higher effective resolution.
3. Replace the front cover's vector-only central device with ART-COVER-001 using its manifest size limit. Keep the title and other lettering as live typeset text, with a coherent cover composition and clear separation from the image.
4. Preserve the existing 57 editable vector figures, including scenario deployment maps. Atmospheric scenes do not establish distances, eligibility or exact deployment geometry.
5. When the owner requests a build (build on request only, owner decision 2026-10-11), rebuild the cream, white and digital PDFs. Review all new chapter openings, the cover, cream/white blending, art detail at placed size, overscan and all repaginated pages. Refresh the visual ledger and run the full verification/package gate. Existing PDFs remain the earlier art-light draft until this happens.

The chapter masters are about 1746–1748 pixels wide; at 300ppi they fit about 5.82 by 3 inches. The cover master is 1430 by 1100 pixels and fits about 4.76 by 3.66 inches at 300ppi. These are near-monochrome warm ink RGBA illustrations, not 600ppi one-bit line-art files. The manifest intentionally reduces the original art-slot sizes to respect the native data.

InDesign export is on hold. Continue the PDF edition. Printing on the owner's inkjet printer and paper remains untested.
