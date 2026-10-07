# Artwork workflow — ChatGPT Work

The owner has chosen ChatGPT Work's built-in image-generation tool for all atmospheric artwork. The required suite is the cover plus eleven chapter images in `production/art/ART_MANIFEST.json`. Claude integrates and reviews these supplied original masters; it does not invoke an external image API. InDesign output is on hold.

Generate the Greythorn chapter image first as an original style anchor. Follow ART_DIRECTION.md: expressive black ink, controlled crosshatching, grounded construction/anatomy, readable silhouettes and clean negative space. Use the anchor only for medium and finish when generating each new subject; avoid repeating its trees/gate/composition across unrelated chapters. Keep rules/deployment figures as source-faithful editable vectors.

Preserve each native PNG unchanged under the stable asset ID in `assets/art/incoming/`. Record exact generation prompt, tool provenance, native pixel size, alpha state, hash, intended physical placement and effective PPI. Save versioned candidates separately if revised. Generate no lettering; titles remain typeset in the book. Review each image at readable size for subject fidelity, construction and artifacts, then inspect placed-size crops on both cream and white pages. Never describe generated images as hand-drawn.

A prompt requesting a resolution does not establish the delivered resolution. Measure actual pixels; if a native image is below the starting target at its intended size, place it smaller or regenerate. Resampling or changing a DPI tag does not create native detail. Preserve the alpha channel and reject rectangular white matte, dirty parchment, halos or accidental grid overlays.

Integration: use the exact manifest filename, apply chapter images at chapter openers and the cover image in the front-cover component, rebuild all PDFs, regenerate navigation, inspect downstream pagination and update current hash-bound visual evidence. Keep source RC unchanged for artwork/layout changes. Store prompts/provenance with the images and provide a ZIP of the complete suite.

Current suite: all twelve masters are generated and reviewed. Read production/art/HANDOFF.md before integrating. Fetch PNGs with Git LFS and run tools/check_art.py. Exact executed prompts are in production/art/PROMPTS.json.
