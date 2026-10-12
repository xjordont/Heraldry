# Artwork workflow — GPT image pen-and-ink route

Images are generated with GPT image generation within the owner's ChatGPT plan, with no paid image API (owner decisions 2026-10-10 and 2026-10-11).
- **Current route:** Codex on the owner's Windows PC, following `production/art/codex/BATCH_CARD.md`.
- **Fallback:** ChatGPT Work with the offline input package.
- **Retired:** the 2026-10-08 Gemini API pipeline (`tools/art_generate.py` generation and the manual-only `Generate pen-and-ink artwork` workflow). It stays in the repository as a fallback and is never run without an owner instruction.

This document is the current state; the dated history is in `production/STATE.md`.

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
   - Each queue item carries its register, its own references (at most six, from `gpt_reference_sets` in `config/art_style.json`), its printed width, its attempt budget (`gpt_max_attempts`: 1, one generation per item, owner 2026-10-12) and the brief's must and avoid lists.
   - References come from `gpt_reference_sets` (mapping v8, 17 sets of up to five, the image tool's limit; see `docs/ART_DIRECTION.md`). Precedence:
     1. `kind_sets`: five monster kinds, by ID; the pack fails if a monster has no kind or two.
     2. `family_sets`.
     3. The register `sets`.

     Each item records its `ref_set`. References are the owner's gritty ink samples and four public-domain prints; generated images are never references, and no isolated figure receives a scenic reference.
   - Order: redos first, then `gpt_lead_ids` (seventeen items, one per set, so the drift reviews at images 10 and 20 test every set), then the rest. The batch phase follows the approved anchors (Greythorn plus four hand-inked images).
2. **The art worker** (Codex on the owner's PC; ChatGPT Work as the fallback) follows `production/art/codex/BATCH_CARD.md` (or `production/art/gpt/INSTRUCTIONS.md`) and the `heraldry-classic-ink-art` skill (below).
   - It pastes each prompt verbatim, attaches that item's references only, generates once in a fresh context (never a retry: a defect is saved flagged, and the reviewer decides on a redo), and saves the native image unmodified as `assets/art/incoming/<ID>.<png|jpg|webp>` (all Git LFS).
   - `heraldry_art.py save` does the check, copy and receipt (`production/art/gpt/RECEIPTS.jsonl`, recording the saved attempt and how many were generated) in one step, and `delivery_guard.py ship` pushes each image as soon as it is saved.
   - `next` and `status` first fast-forward a clean clone, so a rejection sent back mid-session appears as a redo at once.
3. **The `Intake ChatGPT artwork` workflow** (on push to `assets/art/incoming/**`) runs `tools/art_intake.py scan`.
   - It writes a transparent pure-black ink derivative to `assets/art/ink/<ID>.png` (Git LFS).
   - It records the image as `received` in `production/art/SELECTIONS.json`, with hashes, pixels, flags and the receipt.
   - It commits no contact sheet (at one image per push that would add about 30 MB of history).
4. **The orchestrator** runs `tools/art_intake.py pending --sheet` (flagged images first; it fetches just those ink files and writes local sheets to `build/art/review/`), reviews the sheets, plus the full-size image where needed, and then runs one of the following:
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
- Generated images are recorded as AI-generated, naming the surface the receipt records (Codex or ChatGPT Work), never as hand-drawn.
- Rules and deployment diagrams remain source-faithful vector figures and are not generated.

## The skill (v8)

`production/art/skill/heraldry-classic-ink-art/` is the skill source, and Codex runs it straight from the clone. The installable ZIP (`Heraldry_Classic_Ink_Art_Skill_v8_0.zip`) is built only when ChatGPT Work needs it: `make art-packages`, or the `Build art packages` workflow (`docs/LARGE_FILES.md`).

- **`SKILL.md`** is the procedure: session start, the per-item loop, ten hard fails, delivery and drift reviews, stop conditions. `BATCH_CARD.md` is the same contract on one page for Codex.
- **`scripts/heraldry_art.py`**: `doctor`, `status`, `next`, `show`, `check`, `qa`, `save`, `refuse`, `sheet` and `bundle`.
  - `check` counts attempts and reports mechanical tripwires, using the same colour, mid-tone and border formulas as `tools/art_ink.py` (a test keeps them in step).
  - `qa` pre-fills the byte-bound ten-criterion QA draft, and `save` uses it.
  - `next` and `status` fast-forward a clean clone first.
- **The other scripts:**
  - `delivery_guard.py ship --execute` delivers each image (it validates, fast-forwards over the intake bot, retries a lost race and never forces);
  - `style_audit.py` gives advisory drift statistics;
  - `fidelity_gate.py` checks the QA records;
  - `work_preflight.py` checks readiness;
  - `validate_skill.py` checks a built ZIP.
- **`tools/art_skill_build.py`** writes the skill's `references/FAMILIES.md` from the config and builds the ZIP deterministically. The tests build it fresh and validate it.

Claude Code owns the prompts, queue, references, review and approval. The skill only runs the queue and checks what it delivers.

## Codex cadence

- **Per image:** `push_every: 1`, so each saved image is delivered at once, and a 5-hour or weekly usage limit never strands work.
- **Every tenth image:** a drift review (`sheet --recent 10 --refs`, `style_audit.py --recent 10`). Codex reports drift and keeps going (owner 2026-10-12: run the whole list); Claude Code reviews and sends redos.
- **Usage:** ChatGPT Plus resets every 5 hours. Codex stops at the limit with everything delivered, and the same prompt resumes. Codex's image tool accepts at most five reference images (it refused six on 2026-10-12).
- **Resumable:** the next session's identical prompt (`CODEX_PROMPT.md`) resumes from `next`.
- **Lean token use:**
  - The batch card replaces the long docs.
  - References are viewed once per session.
  - Reports are one line per item.
  - The reviewer works from `art_intake.py pending --sheet`, opening full size only flagged images and spot checks.
- **LFS bandwidth:** the intake fetches only new images; the build fetches only the art it places, cached (`docs/LARGE_FILES.md`).

## Offline fallback: ChatGPT Work

Work cannot authenticate git, and a credential must never be pasted into a chat (a token route was tried on 2026-10-11 and withdrawn). `tools/art_work_package.py` covers this route:

- **`build`** writes `build/art/Heraldry_Work_Input_<phase>.zip` from committed inputs (its manifest names the source commit). It holds the queue, its prompts, every queue-listed reference, the skill (source and ZIP), receipts, selections, the config and `START_HERE.md`, each with SHA-256. It holds no other art and no private PDFs.
- **`verify ZIP`** runs the packaged preflight, `doctor`, `status` and the guard (which must refuse) with Git credentials stripped.
- **Delivery** is `heraldry_art.py bundle`. Its ZIP records `pushed_to_github: false` and "not approved". The owner commits it to `production/art/work/inbox/`.
- **The `Import Work review bundle` workflow:**
  - re-runs `verify-bundle` (manifest, receipts against native bytes, prompt and reference hashes, bound QA reports);
  - commits the images through LFS and appends the receipts;
  - runs the intake;
  - records the bundle in `IMPORTED.json` and removes the ZIP.
- **Limits:** ChatGPT's GitHub plugin passes file contents only as inline text (about 1 MB at most), so it cannot carry images or bundles. Whether the image tool accepts the listed references can only be shown by the first real item.

## Heraldic marks (owner 2026-10-12)

The logo and the fifteen chapter arms are generated with the Gemini image API on an explicit owner instruction. Prompts are in `production/art/marks/PROMPTS.json`; generation runs through `tools/mark_generate.py` in the manual "Generate heraldic marks" workflow. It shares the budget cap and the ledger. Candidates land in `assets/art/marks/candidates/` for review. The book illustrations still go through Codex.
