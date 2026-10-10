# Artwork workflow — automated Gemini pen-and-ink pipeline

Owner decision, 2026-10-08 (Claude Code session): "I want to automate the entire process with as little effort as possible. While the existing art assets can serve as a generate inspiration I think it would be best to replace them as well to ensure consistency." This replaces the earlier ChatGPT Work route and the earlier rule against an external image API.

## Scope

`tools/art_catalog.py` derives the catalog deterministically from the current manuscript: every heading whose first block is flavour text, plus the cover and 11 chapter openers. It writes `production/art/SPOT_CATALOG.json` with 275 entries: 135 monsters, 37 scenarios, 20 backgrounds, 15 tradition tiers, 12 classes, 11 ancestries, 11 campaign rooms, 8 world sections, 6 climates, 6 bastions, 2 equipment sections, 11 chapters and the cover. Flavour text is copied verbatim into prompts and never paraphrased.

## Style

`config/art_style.json` is the single style bible: one illustrator's dip-pen line, hatching and crosshatching, pure black ink on white, light from the upper left, and no text, frame, colour or grey wash. It also sets per-family aspect ratio, resolution and printed width, the model preference lists, the budget cap and the candidate counts.

## Pipeline (`tools/art_generate.py`)

1. **anchors.** Generates four candidates each for six anchor subjects (a climate, a bastion, two monsters, a class and an ancestry). The original masters are attached only as inspiration. The judge picks one per subject, and `production/art/ANCHORS.json` becomes `proposed`.
2. **approve-anchors.** The orchestrator inspects the anchor contact sheet and approves it, or rejects it and reruns. Approval is recorded with a timestamp.
3. **batch.** For every pending entry, generates three candidates with the approved anchors attached as style references.
   - An automated judge model scores each candidate for style match, subject fidelity and craft.
   - Ink preparation rejects candidates with colour, a frame or box, or grey wash.
   - Below the pass score, a second round runs. If that also fails, the best candidate is kept as `low-score-needs-review`.
4. **ink.** Selection writes:
   - the raw master to `assets/art/masters/<id>.png` (Git LFS; bound by SHA256);
   - a pure-black-on-transparent derivative to `assets/art/ink/<id>.png` (Git LFS), which prints on both the cream and white editions;
   - a record in `production/art/SELECTIONS.json`, with the prompt, model, judge scores, hashes, pixels and maximum print width at 300 ppi.
5. **Ledger and budget.** Every API call is appended to `production/art/GENERATION_LEDGER.jsonl` with its token usage and an estimated cost. The run stops at `budget_usd`; Google's billing console is the authoritative cost.
6. **Resuming.** The workflow commits progress every 10 entries and stops cleanly before the job time limit. Rerunning it continues from the pending entries.

Changing an entry's flavour text, its subject plan or its family changes its `spec_sha256`, which makes that entry pending again. Style-bible changes do not invalidate selected art automatically; regenerate the affected entries with `--ids`.

**Uniqueness.** `production/art/SUBJECT_PLAN.json` holds the orchestrator's art direction: fresh chapter subjects and a concrete, distinct image for every entry whose flavour text is abstract or whose name collides with another entry. Named bosses form their own `boss` family (shown in their lair); scenarios show place and situation, with creatures small; backgrounds are still lifes of their trade. `tools/art_catalog.py` fails on a duplicate subject or an unseparated name collision. `tools/art_list.py` writes `production/art/ILLUSTRATION_LIST.md` with every entry's exact prompt.

## Running it

GitHub → Actions → **Generate pen-and-ink artwork** → Run workflow, with `phase` set to `plan`, `anchors` or `batch` (optional `family` and `limit`). It needs the repository secret `GEMINI_API_KEY`. Candidates and contact sheets are uploaded as a workflow artifact; rejected candidates are not committed.

## Layout

- `tools/build_book.py` places the selected ink art above each entry's flavour text, inside that entry's keep unit, so the one-page-keep audit includes the image.
- Each image is printed at its family width, never above native 300 ppi.
- Chapter openers and the cover use `ART-CHnn-002` and `ART-COVER-002` when selected, and fall back to the original masters otherwise.
- Artwork changes never change the manuscript RC number.

## Review and honesty

- The orchestrator still reviews contact sheets and placed pages, and updates the hash-bound visual ledger before release.
- Generated images are recorded as AI-generated, never described as hand-drawn.
- Rules and deployment diagrams remain source-faithful vector figures and are not generated.
