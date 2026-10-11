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
   - Writes `production/art/gpt/QUEUE.json` (schema 2), `QUEUE.md` and one prompt file per pending entry in `production/art/gpt/prompts/`.
   - Each queue item carries its register, its own references (at most three, from `gpt_reference_sets` in `config/art_style.json`), its printed width, its attempt budget (`gpt_max_attempts`: 3, and 5 for the cover and chapters) and the brief's must and avoid lists.
   - Registers keep scenery out of figures: `scene` (cover, chapter, world, climate, bastion, scenario, campaign, boss, tradition) gets Greythorn, the approved Greenmark anchor and an owner scene sample; `creature` (monster) and `person` (class, ancestry) get the owner's figure sample and their approved anchors; `still` (background, item) gets the figure sample.
   - The anchors phase comes first and uses the owner's samples. Once anchors are approved, the batch phase adds them by register.
2. **ChatGPT Work** follows `production/art/gpt/INSTRUCTIONS.md` and the `heraldry-classic-ink-art` skill (below).
   - It pastes each prompt verbatim, attaches that item's references only, stops at the first attempt that passes the checks (never beyond the item's budget), and saves the image unmodified as `assets/art/incoming/<ID>.png`.
   - It appends a receipt to `production/art/gpt/RECEIPTS.jsonl` and commits in batches. `heraldry_art.py save` does the check, copy and receipt in one step.
3. **The `Intake ChatGPT artwork` workflow** (on push to `assets/art/incoming/**`) runs `tools/art_intake.py scan`.
   - It writes a transparent pure-black ink derivative to `assets/art/ink/<ID>.png` (Git LFS).
   - It records the image as `received` in `production/art/SELECTIONS.json`, with hashes, pixels, flags and the receipt.
   - It commits a review contact sheet to `production/art/review/`.
4. **The orchestrator** reviews each sheet, plus enlarged crops where needed, and then runs one of:
   - `tools/art_intake.py approve --ids ...`
   - `reject --ids ... --reason "..."`, which returns the entry to the queue; the reason is shown to the operator as a redo, so make it a sentence they can turn into a correction;
   - `approve-anchors`, which makes the received anchors the references for the batch queue.

Only `approved` and `anchor-approved` art is placed in the book.

## Layout

- `tools/build_book.py` places approved ink art above each entry's flavour text, inside that entry's keep unit. The one-page-keep audit therefore includes the image.
- Each image prints at its family width, never above native 300 ppi. GPT images are at most 1536 px on the long side. Chapter openers are 3:2 at 4.5 in wide, 3.0 in tall, matching the chapter-opener art slot.
- Chapter openers and the cover use `ART-CHnn-002` and `ART-COVER-002` once approved, and fall back to the original masters until then.
- Artwork changes never change the manuscript RC number.

## Review and honesty

- The orchestrator reviews placed pages and updates the hash-bound visual ledger before release.
- Generated images are recorded as AI-generated (ChatGPT Work), never as hand-drawn.
- Rules and deployment diagrams remain source-faithful vector figures and are not generated.

## The ChatGPT Work skill (v4; superseded by v6 below)

`production/art/skill/heraldry-classic-ink-art/` is the source of the skill ChatGPT Work runs, and `production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip` is the installable build. It replaces the owner's v3.1 draft, which planned one scene per conversation, used one style reference for every family, sized images from a preset table that disagreed with the layout slots, and had no queue, receipts or gates. The skill's README lists each change and why.

- `SKILL.md` is the procedure: session start, phases, the per-item loop, ten hard fails, batches and commits, stop conditions.
- `scripts/heraldry_art.py` has `doctor`, `status`, `next`, `show`, `check`, `save`, `refuse`, `sheet` and `bundle`. `check` reports mechanical tripwires calibrated on the approved Greythorn render, the three owner samples and synthetic defects. Its colour, mid-tone and border measures use the same formulas as `tools/art_ink.py`, and a test keeps them in step.
- `tools/art_skill_build.py` writes `references/FAMILIES.md` from `config/art_style.json` and builds the zip deterministically, with byte-identical copies of the repo's reference images and a hash manifest. `python production/art/skill/heraldry-classic-ink-art/scripts/validate_skill.py --zip production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip` (from the repo root) checks the zip and its agreement with the repo.
- `tests/test_art_skill.py` fails if the zip is older than its sources or the reference images, if `FAMILIES.md` disagrees with the config, or if the queue schema changes under the helper. After any change to the skill sources, the reference sets or the reference images, run `python3 tools/art_skill_build.py` and commit the zip.

Claude Code still owns the prompts, queue, references, review and approval. The skill only runs the queue and checks what it delivers.

## Skill v6 and the offline Work input package

The owner installed skill v6 on 2026-10-11 (`Heraldry_Classic_Ink_Art_Skill_v6_0.zip`, built by `tools/art_skill_build.py`). It is the working version. v6 adds byte-bound visual QA reports (`fidelity_gate.py`, `save --qa-file`), the guarded direct-main delivery (`delivery_guard.py`), a same-register drift report (`style_audit.py`) and `work_preflight.py`.

ChatGPT Work's first v6 test run was blocked. Shell git could not authenticate, and the GitHub connector could not fetch the binary references STYLE-REF-01 and STYLE-REF-02. The input route that fixes this is `tools/art_work_package.py`:

- `build` writes `production/art/work/Heraldry_Work_Input_<phase>.zip` and a copy of its `WORK_PACKAGE.json`. Inputs must be committed first, because the manifest names the source commit. The ZIP holds the exact queue, its prompt files, every queue-listed reference as real image bytes, the complete v6 skill (source and installable ZIP), receipts, selections, `config/art_style.json` and a generated `START_HERE.md`, each with SHA-256. Nothing else goes in: no other art and no private reference PDFs.
- `verify ZIP` extracts the package into an empty folder and checks the manifest, prompt hashes and reference decoding. It then runs the packaged `work_preflight.py --offline-package`, `doctor`, `status` and `delivery_guard.py audit` with Git credentials stripped from the environment. The guard must refuse.
- `check` is run by `tests/test_art_work_package.py`. It fails when the committed package no longer matches the queue, prompts, references or skill. Receipts may only have grown since the build, and of the selection state only rejections (redo reasons) of queued IDs are compared. After republishing a queue or rebuilding the skill, commit, run `build`, and commit the package.
- The owner's `Export Work calibration inputs` workflow (`.github/workflows/work-calibration-inputs.yml`; manual, or on queue, skill or builder changes) runs the same `build` and `verify` on GitHub Actions. It uploads the ZIP, `WORK_PACKAGE.json` and the verify report as a 14-day artifact. It is the same package format, so the offline preflight accepts it.
- `verify-bundle BUNDLE.zip` is the first reviewer step on what Work returns. It checks the manifest hashes, receipts against the native bytes, prompt and reference hashes, and each QA report bound in its receipt (via `fidelity_gate.verify_record`). It approves nothing; visual review and `tools/art_intake.py` follow.

In the package, `heraldry_art.py` never runs git. A folder counts as a checkout only when `.git` is at its root. Delivery is `bundle --evidence ...`, which first applies the guard's receipt gate. Its ZIP carries the native images, `receipts_append.jsonl`, `review_evidence/qa/<ID>.qa.json`, extra evidence and `BUNDLE_MANIFEST.json`, which records `pushed_to_github: false` and "not approved". Authenticated Git/LFS delivery is a separate capability and is never implied by the package.

The package proves the inputs only. Two capabilities can be shown only by a real smoke test inside Work: that the image tool accepts every listed reference, and that the native output file is accessible.

### Delivering a Work review bundle without Git LFS

Neither ChatGPT Work nor this cloud container can upload Git LFS objects: the container's network policy denies `lfs.github.com`. Instead, commit the review ZIP unchanged to `production/art/work/inbox/`. It is an ordinary Git file, and the owner can upload it through the GitHub web page. The `Import Work review bundle` workflow then runs `tools/art_work_package.py import-bundle`, which re-runs verify-bundle, copies the native images into `assets/art/incoming/` (committed through LFS by the Actions runner) and appends the receipts. The workflow then runs `art_intake.py scan` and records the bundle in `production/art/work/IMPORTED.json`. A bundle that fails verification imports nothing. Approval stays a separate orchestrator step.
