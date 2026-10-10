# Artwork workflow — ChatGPT Work pen-and-ink route

Owner decision, 2026-10-10 (Claude Code session): "Yes make the chat gpt work the official image generation pathway." The owner reported that GPT Images gave better results and wanted generation covered by the ChatGPT subscription rather than pay-as-you-go API fees. This supersedes the 2026-10-08 Gemini API route. That pipeline (`tools/art_generate.py` and the manual-only `Generate pen-and-ink artwork` workflow) stays in the repository as a retired fallback and is not run without an owner instruction. Its six test drawings are superseded.

## Scope

`tools/art_catalog.py` derives the catalog deterministically from the current manuscript. It covers every heading whose first block is flavour text, plus the cover and the 11 chapter openers. It writes `production/art/SPOT_CATALOG.json`.

There are 275 entries:

| Family | Count |
|---|---|
| Monsters | 120 |
| Scenarios | 37 |
| Backgrounds | 20 |
| Bosses | 15 |
| Tradition tiers | 15 |
| Classes | 12 |
| Ancestries | 11 |
| Campaign rooms | 11 |
| Chapter openers | 11 |
| World sections | 8 |
| Climates | 6 |
| Bastions | 6 |
| Equipment sections | 2 |
| Cover | 1 |

Flavour text is quoted verbatim in every prompt.

## Art direction and prompts

These sources feed every prompt:

- **`config/art_style.json`**
  - `prompt_v2` is the prompt template. Its structure follows the owner's Greythorn prompt: title, introduction, format and white vignette (scenes) or isolation (figures and still lifes), composition, subject details, activity, source text, style and atmosphere, final requirements, style references.
  - `families` sets the aspect ratio and printed width for each family.
- **`production/art/SUBJECT_PLAN.json`**
  - Fresh chapter subjects.
  - A distinct direction for any entry whose flavour text is abstract or whose name collides with another entry.
- **`production/art/briefs/`** holds one brief per entry, written from the manuscript: identity, composition, details, activity, atmosphere, pitfalls and sources.
- **`production/art/OWNER_PROMPTS.json`** holds owner-authored prompts, used verbatim. The first is Greythorn.

`tools/art_catalog.py` builds each entry's `spec_sha256` from its flavour text, plan, brief and owner prompt. Changing any of these makes the entry pending again. The script also fails on a duplicate subject or an unseparated name collision.

`tools/art_list.py` writes `production/art/ILLUSTRATION_LIST.md`, which lists every entry with its prompt.

Manuscript issues found while briefing are recorded in `production/art/SOURCE_NOTES.md`. When the owner fixes them, the change becomes a new RC with `tools/revise_manuscript.py`, and the briefs follow.

## Production loop

1. **`python3 tools/art_gpt_pack.py`**
   - Writes `production/art/gpt/QUEUE.json`, `QUEUE.md` and one prompt file per pending entry in `production/art/gpt/prompts/`.
   - The anchors phase comes first and uses the owner's style samples as references. The batch phase uses the approved GPT anchors as references.
2. **ChatGPT Work** follows `production/art/gpt/INSTRUCTIONS.md`.
   - It pastes each prompt, attaches the references, keeps the best of up to three variants, and saves the image unmodified as `assets/art/incoming/<ID>.png`.
   - It appends a receipt to `production/art/gpt/RECEIPTS.jsonl` and commits in batches.
3. **The `Intake ChatGPT artwork` workflow** (on push to `assets/art/incoming/**`) runs `tools/art_intake.py scan`.
   - It writes a transparent pure-black ink derivative to `assets/art/ink/<ID>.png` (Git LFS).
   - It records the image as `received` in `production/art/SELECTIONS.json`, with hashes, pixels, flags and the receipt.
   - It commits a review contact sheet to `production/art/review/`.
4. **The orchestrator** reviews each sheet, plus enlarged crops where needed, and then runs one of:
   - `tools/art_intake.py approve --ids ...`
   - `reject --ids ...`, which returns the entry to the queue;
   - `approve-anchors`, which makes the received anchors the references for the batch queue.

Only `approved` and `anchor-approved` art is placed in the book.

## Layout

- `tools/build_book.py` places approved ink art above each entry's flavour text, inside that entry's keep unit. The one-page-keep audit therefore includes the image.
- Each image prints at its family width, never above native 300 ppi. GPT images are at most 1536 px on the long side, so chapter openers print about 5.1 in wide.
- Chapter openers and the cover use `ART-CHnn-002` and `ART-COVER-002` once approved, and fall back to the original masters until then.
- Artwork changes never change the manuscript RC number.

## Review and honesty

- The orchestrator reviews placed pages and updates the hash-bound visual ledger before release.
- Generated images are recorded as AI-generated (ChatGPT Work), never as hand-drawn.
- Rules and deployment diagrams remain source-faithful vector figures and are not generated.
