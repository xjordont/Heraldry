# Codex runbook: Heraldry illustration generation (local Windows PC)

**For production sessions, `BATCH_CARD.md` is the operative one-page contract.** This runbook is background and first-time setup.

Owner decision 2026-10-11: image generation continues in **Codex on the owner's Windows PC**, which has the owner's own GitHub login, Git, Git LFS and Python. GitHub `main` is the primary source and delivery route; ZIP hand-off is reserved for the v6 fallback when authenticated inputs or guarded delivery are unavailable. Codex clones `xjordont/Heraldry`, generates the queued images, and pushes them through LFS with the guarded delivery script. GitHub Actions ink-prepares them, and Claude Code reviews and approves them, then publishes the next queue.

## Roles

| Who | Owns | Never does |
|---|---|---|
| Claude Code (orchestrator) | prompts, queue, references, art direction, review and approval (`tools/art_intake.py`), manuscript, layout, builds, all shared files | generate the final art |
| Codex (art worker) | generating images, mechanical checks, its own visual QA record, saving to `assets/art/incoming/<ID>.<ext>` plus `production/art/gpt/RECEIPTS.jsonl`, guarded delivery | edit prompts, queue, manuscript, tools, config or the skill; approve art; build PDFs; push anything other than incoming images and receipts; force-push; create branches |
| Owner | starts Codex sessions, art-direction calls, final say | |

Codex is a worker with disjoint ownership in the sense of `CLAUDE.md`. Its only writable paths are `assets/art/incoming/ART-*.{png,jpg,webp}` and `production/art/gpt/RECEIPTS.jsonl`, and `delivery_guard.py` enforces this.

## One-time setup (PowerShell)

The configured PC already has this checkout and environment. If either path exists, inspect and reuse it; do not rerun creation commands over it. For a new installation, install Git, Git LFS, and Python 3.12, authenticate Git locally through the browser flow, then create the separate paths:

```powershell
New-Item -ItemType Directory -Force C:\Heraldry | Out-Null
git lfs install --skip-repo
$env:GIT_LFS_SKIP_SMUDGE = "1"
git clone -c core.autocrlf=false https://github.com/xjordont/Heraldry.git C:\Heraldry\art-producer
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
Set-Location C:\Heraldry\art-producer
git lfs install --local --skip-smudge
py -3.12 -m venv C:\Heraldry\art-venv
$artPython = "C:\Heraldry\art-venv\Scripts\python.exe"
$pillowPin = (Select-String -Path requirements.lock -Pattern '^pillow==').Line
& $artPython -m pip install $pillowPin
New-Item -ItemType Directory -Force C:\Heraldry\art-scratch | Out-Null
```

`core.autocrlf=false` keeps checked-out text byte-exact; `.gitattributes` also pins prompts and the skill to LF. Set it locally in an existing checkout only after confirming its unchanged text matches the committed bytes. Never fetch `references/private/pdfs/` (owner reference books) for this work. Fetch only the exact queue-listed reference paths when required.

## Every session

Use the separate art checkout at `C:\Heraldry\art-producer`, `C:\Heraldry\art-venv\Scripts\python.exe` (Python 3.12 with the repository-pinned Pillow), and `C:\Heraldry\art-scratch` on the configured PC. Set `HERALDRY_SCRATCH` and `PYTHONUTF8=1` in every relevant subprocess. Use the selected art interpreter for every helper command.

Inspect the branch, worktree, index, and remote first. Run the update block only on a clean `main` checkout. If incoming images or receipts are unsent, skip the pull, run `status`, and follow guarded delivery or bundle procedures. Stop on unrelated edits or divergence. Never pull or rebase over unsent work.

```powershell
Set-Location C:\Heraldry\art-producer
$artPython = "C:\Heraldry\art-venv\Scripts\python.exe"
git status --short             # must be clean before the next command
git branch --show-current      # must be main
git diff --cached --stat        # staging index must be clean
git remote -v
git pull --ff-only origin main
$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"   # outside the repo
$env:PYTHONUTF8 = "1"
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

The preflight should say `READY` with `delivery: git_lfs`. Show the complete preflight, doctor, and status outputs. Stop on `BLOCKED` or `NOT READY`; report the output verbatim and repair setup before production. `status` prints the single next action. Obey it only within the owner's current authorization. A readiness-only request stops before generation, production receipts, or artwork delivery.

### Counted smoke/pilot gate

Once production is authorized, use one queued attempt to prove actual image generation, attachment of every queue-listed reference in order and no extra references, and access to the original native file that Pillow opens. Tool exposure alone is insufficient. If any capability fails, stop and report it.

Only after all three succeed, write a scratch JSON record with `image_generated`, `all_queue_references_attached`, and `native_file_accessible` set to true, then rerun `work_preflight.py --repo . --require-installed --smoke-file <scratch record>`. This generation counts toward the item's live attempt budget. Retain its exact prompt, reference, model, and native-byte provenance, and use the normal `check`, QA, and `save` procedure. Never reset attempt counters or create a free extra attempt.

## Image generation

- Use the image generation available in Codex under the owner's ChatGPT plan. **Do not use a paid OpenAI API key** (owner: no extra spending beyond ChatGPT Plus). If Codex cannot generate images within the plan, stop and say so.
- Preferred model: **GPT Image 2.5 Sunburst** (`gpt-image-2.5-sunburst`) if offered, otherwise the default image model. Record the exact model label actually shown with `save --model`, or "not shown". Do not infer the active model from an old prompt. Report unavailable size, quality, or model controls.
- Attach **every** reference listed for the item, and nothing else: the owner's gritty ink samples in `assets/art/style/`. If the tool cannot take reference images, stop and report it: never generate unanchored.
- Size: the queue size is the minimum and fixes the aspect. Request the largest size offered at that aspect.
- Art direction (owner, 2026-10-11, later): "closer to the more old school black and white gritty style". That means bold, rough brush contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast and visible human marks, like the samples, in pure black ink. No grey wash, stipple fields, machine-even texture, clean vector-like line or rendered polish. Details are in `production/art/skill/heraldry-classic-ink-art/references/STYLE.md` and `docs/ART_DIRECTION.md`.

## Per item (from `SKILL.md`; the full contract is there)

1. `heraldry_art.py show ID`: the verbatim prompt, references, size, MUST and DO NOT DRAW lists.
2. Generate with the verbatim prompt; at most two correction sentences on retries (`references/REPAIR.md`).
3. Save the native file to `%HERALDRY_SCRATCH%`, then `heraldry_art.py check ID FILE`. Look at the image and the print-size preview beside the references.
4. `fidelity_gate.py create ID FILE --prompt-sha <hash> --reference <each ref> --out %HERALDRY_SCRATCH%\ID.qa.json`, then fill all ten criteria with real, specific evidence (`references/QA_CHECKLIST.md`).
5. `heraldry_art.py save ID FILE --qa-file ... --must "..." --avoid-clear --model "..."`.
6. Stay within each item's attempt budget; `--accept-flags` only at the last attempt.

## Primary delivery: guarded Git LFS to main

When `status` asks for delivery:

```powershell
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py sheet --refs --out "$env:HERALDRY_SCRATCH\sheet.jpg"
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/style_audit.py --repo . --out "$env:HERALDRY_SCRATCH\style.json"
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py audit --repo .
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py ship --execute --repo .
```

`ship` stages only queued images and receipts, verifies every receipt against the native bytes, prompt, references and QA, checks LFS, and pushes to `main` with no force. If `main` advanced only in paths you are not delivering (the intake bot's ink, selection and review commits after every push), `ship` fast-forwards by itself and retries a lost push race up to three times. It undoes only its own unpublished commit and never rebases, merges or forces. If `main` diverged, changed the same files, or the guard blocks on authentication, LFS, QA, or unexpected changes, stop before delivery. Do not force-push, auto-rebase, or pull over unsent artwork or receipts. Preserve the work, create the helper's review bundle, and ask the maintainer to reconcile the blocker. The push triggers the `Intake ChatGPT artwork` workflow.

Then report: IDs, model name, pixel sizes, attempts, QA failures or accepted flags, and the commit SHA. Stop at the phase gate. For anchors, deliver all five and stop until Claude Code has reviewed them and published the next queue.

## ZIP fallback

If guarded Git/LFS delivery fails, use `heraldry_art.py bundle` outside the checkout, with the contact sheet, style audit, smoke record, and saved QA evidence. Report the bundle path and SHA-256 and state that no push succeeded. Bundle creation does not approve art. The independent reviewer verifies and imports it through the existing fallback procedure.

If an authenticated checkout cannot be obtained, use the explicitly selected offline Work input package described in `production/art/gpt/WORK_PROMPT.md`. Follow `START_HERE.md`, use `--offline-package`, never run `git init`, clone, or pull inside the package, and deliver by bundle only with remote access `NOT_ATTEMPTED`.

## Rules that always apply

- `CLAUDE.md` governs the repository. Work on `main` only, never force-push, never rewrite history.
- Never print, log or commit a credential. Git uses the owner's existing Windows login.
- Build on request only: Codex never runs `make all`, builds PDFs or dispatches the delivery rebuild.
- Nothing Codex delivers is approved. Claude Code reviews every image.
