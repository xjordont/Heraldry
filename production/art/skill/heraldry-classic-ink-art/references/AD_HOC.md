# An illustration that is not in the queue

Do not generate it for the book. A book illustration needs a catalogue entry (a unique subject, a brief, a prompt, a queue slot and a layout slot), and only Claude Code can add one. Ask the owner to have Claude Code do it.

For an explicit one-off the owner asks for outside the book, use this short method, taken from the earlier v3 skill's scene-planning protocol:

1. **Source.** Separate what the text states visually, what it implies, what is only mood, and what it does not say. Never invent named landmarks, numbers of people, heraldry or lettering.
2. **Thesis.** One sentence: what must be clear at final size?
3. **Camera and layers.** One camera. Foreground, midground, background, with one eye path. Roads reach gates, bridges span gaps, buildings stand on something.
4. **Scale and density.** Express size with structure density and small scale cues, not adjectives. A large town needs visible urban mass; a creature needs a stated size class.
5. **Detail budget from print width.** At 3 inches wide: one focal silhouette and two to four supporting details. At 2 inches: anatomy, silhouette and gear only. At 1.6 inches: one unmistakable arrangement.
6. **Assemble** in the repo's prompt order: title, introduction, format (vignette for scenes, isolation for figures and still lifes), composition, subject details, "Must be shown exactly" and "Do not draw" lists, source text, style and atmosphere, final requirements, references. Copy the wording of a real file from `production/art/gpt/prompts/` for the shared sections.
7. Generate with the matching register's references (`references/STYLE.md`), run the same checklist, and tell the owner it is not in the catalogue and has no receipt or review.
