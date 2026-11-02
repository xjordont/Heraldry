# Codex runbook: Heraldry illustration generation (local Windows PC)

**For production sessions, `BATCH_CARD.md` is the operative one-page contract.** This runbook is background and first-time setup.

Owner decision 2026-10-11: image generation continues in **Codex on the owner's Windows PC**, which has the owner's own GitHub login, Git, Git LFS and Python. GitHub `main` is the primary source and delivery route; ZIP hand-off is reserved for the offline fallback when authenticated inputs or guarded delivery are unavailable. Codex clones `xjordont/Heraldry`, generates the queued images, and pushes them through LFS with the guarded delivery script. GitHub Actions ink-prepares them; they are then approved or sent back with `tools/art_intake.py` (by Codex itself, after looking at them, or by the owner or another session), and the next queue is published.

## Scope of a generation run

While generating, the run writes only `assets/art/incoming/ART-*.{png,jpg,webp}` and `production/art/gpt/RECEIPTS.jsonl`; `delivery_guard.py` enforces this. Approval afterwards is an ordinary commit of `production/art/SELECTIONS.json` (`BATCH_CARD.md`, "After the run"). The owner starts Codex sessions and has the final say on art direction.

## One-time setup (PowerShell)

The configured PC already has this checkout and environment. If either path exists, inspect and reuse it; do not rerun creation commands over it. For a new installation, install Git, Git LFS, and Python 3.12, authenticate Git locally through the browser flow, then create the separate paths:

```powershell
New-Item -ItemType Directory -Force C:\Heraldry | Out-Null
git lfs install --skip-repo
$env:GIT_LFS_SKIP_SMUDGE = "1"
git clone --filter=blob:none -c core.autocrlf=false https://github.com/xjordont/Heraldry.git C:\Heraldry\art-producer
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
Set-Location C:\Heraldry\art-producer
git lfs install --local --skip-smudge
py -3.12 -m venv C:\Heraldry\art-venv
$artPython = "C:\Heraldry\art-venv\Scripts\python.exe"
$pillowPin = (Select-String -Path requirements.lock -Pattern '^pillow==').Line
& $artPython -m pip install $pillowPin
New-Item -ItemType Directory -Force C:\Heraldry\art-scratch, C:\Heraldry\art-archive | Out-Null
```

`--filter=blob:none` downloads commits and trees but not the old PDFs and ZIPs in history; files are fetched when first needed (`docs/LARGE_FILES.md`). An existing full clone keeps working as it is. `core.autocrlf=false` keeps checked-out text byte-exact; `.gitattributes` also pins prompts and the skill to LF. Set it locally in an existing checkout only after confirming its unchanged text matches the committed bytes. Never fetch `references/private/pdfs/` (owner reference books) for this work. Fetch only the exact queue-listed reference paths when required.

## Every session

Use the separate art checkout at `C:\Heraldry\art-producer`, `C:\Heraldry\art-venv\Scripts\python.exe` (Python 3.12 with the repository-pinned Pillow), `C:\Heraldry\art-scratch` and `C:\Heraldry\art-archive` on the configured PC. Set `HERALDRY_SCRATCH`, `HERALDRY_ARCHIVE` and `PYTHONUTF8=1` in every relevant subprocess. The archive is the PC's own copy of every delivered image, written by `save` with no download; GitHub (Git LFS) stays the master. Delete the scratch folder once the run is finished and reviewed. Use the selected art interpreter for every helper command.

Inspect the branch, worktree, index, and remote first. Run the update block only on a clean `main` checkout. If incoming images or receipts are unsent, skip the pull, run `status`, and follow guarded delivery or bundle procedures. Stop on unrelated edits or divergence. Never pull or rebase over unsent work.

```powershell
Set-Location C:\Heraldry\art-producer
$artPython = "C:\Heraldry\art-venv\Scripts\python.exe"
git status --short             # must be clean before the next command
git branch --show-current      # must be main
git diff --cached --stat        # staging index must be clean
git remote -v
git pull --ff-only origin main
$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"   # outside the repo: attempts, previews, attempt counts
$env:HERALDRY_ARCHIVE = "C:\Heraldry\art-archive"   # outside the repo: save keeps one copy of each delivered image here
$env:PYTHONUTF8 = "1"
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

The preflight should say `READY` with `delivery: git_lfs`. Stop on `BLOCKED` or `NOT READY` and report the output verbatim. `status` prints the single next action. A readiness-only request stops before generation.

### Capability check

The first real item proves the capabilities: the image tool must accept every listed reference, in order, and give you the native file. If it cannot, stop and report it. No separate smoke file is needed.

## Image generation

- Use the image generation available in Codex under the owner's ChatGPT plan. **Do not use a paid OpenAI API key** (owner: no extra spending beyond ChatGPT Plus). If Codex cannot generate images within the plan, stop and say so.
- Preferred model: **GPT Image 2.5 Sunburst** (`gpt-image-2.5-sunburst`) if offered, otherwise the default image model. Record the exact model label actually shown with `save --model`, or "not shown". Do not infer the active model from an old prompt. Report unavailable size, quality, or model controls.
- Attach **every** reference listed for the item, and nothing else: the owner's gritty ink samples in `assets/art/style/`. If the tool cannot take reference images, stop and report it: never generate unanchored.
- Size: the queue size is the minimum and fixes the aspect. Target the maximum output resolution (owner 2026-10-12): the largest size and highest quality offered at that aspect, never the default; `check` warns below the queue's `target_pixels`.
- Art direction (owner, 2026-10-11, later): "closer to the more old school black and white gritty style". That means bold, rough brush contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast and visible human marks, like the samples, in pure black ink. No grey wash, stipple fields, machine-even texture, clean vector-like line or rendered polish. Details are in `production/art/skill/heraldry-classic-ink-art/references/STYLE.md` and `docs/ART_DIRECTION.md`.

## Per item

Follow `BATCH_CARD.md` ("Per item"); `SKILL.md` has the full procedure.

## Primary delivery: guarded Git LFS to main

When `status` asks for delivery:

```powershell
# every tenth image (status says DRIFT REVIEW), first:
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py sheet --recent 10 --refs
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/style_audit.py --repo . --recent 10
# after every image:
& $artPython production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py ship --execute --repo .
```

`ship` stages only queued images and receipts, verifies every receipt against the native bytes, prompt, references and QA, checks LFS, and pushes to `main` with no force. If `main` advanced only in paths you are not delivering (the intake bot's ink, selection and review commits after every push), `ship` fast-forwards by itself and retries a lost push race up to three times. It undoes only its own unpublished commit and never rebases, merges or forces. If `main` diverged, changed the same files, or the guard blocks on authentication, LFS, QA, or unexpected changes, stop before delivery. Do not force-push, auto-rebase, or pull over unsent artwork or receipts. Preserve the work, create the helper's review bundle, and report the blocker. The push triggers the `Intake ChatGPT artwork` workflow.

Report one line per item (ID, attempts, flags) and the commit SHA of each delivery, and continue until NOTHING LEFT or a stop condition on `BATCH_CARD.md`.

## ZIP fallback

If guarded Git/LFS delivery fails, use `heraldry_art.py bundle` outside the checkout, with the contact sheet, style audit and saved QA evidence. Report the bundle path and SHA-256 and state that no push succeeded. The `Import Work review bundle` workflow verifies and imports it.

If an authenticated checkout cannot be obtained, use the explicitly selected offline Work input package described in `production/art/gpt/WORK_PROMPT.md`. Follow `START_HERE.md`, use `--offline-package`, never run `git init`, clone, or pull inside the package, and deliver by bundle only with remote access `NOT_ATTEMPTED`.

## Rules that always apply

- `CLAUDE.md` governs the repository. Work on `main` only, never force-push, never rewrite history.
- Never print, log or commit a credential. Git uses the owner's existing Windows login.
- Build on request only: Codex never runs `make all`, builds PDFs or dispatches the delivery rebuild.
- Only approved art is placed in the book; approve an image only after looking at it.
