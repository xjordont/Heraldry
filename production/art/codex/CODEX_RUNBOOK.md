# Codex runbook: Heraldry illustration generation (local Windows PC)

Owner decision 2026-10-11: image generation continues in **Codex on the owner's Windows PC**, which has the owner's own GitHub login, Git, Git LFS and Python. That removes every ZIP hand-off. Codex clones `xjordont/Heraldry`, generates the queued images, and pushes them through LFS with the guarded delivery script. GitHub Actions ink-prepares them, and Claude Code reviews and approves them, then publishes the next queue.

## Roles

| Who | Owns | Never does |
|---|---|---|
| Claude Code (orchestrator) | prompts, queue, references, art direction, review and approval (`tools/art_intake.py`), manuscript, layout, builds, all shared files | generate the final art |
| Codex (art worker) | generating images, mechanical checks, its own visual QA record, saving to `assets/art/incoming/<ID>.<ext>` plus `production/art/gpt/RECEIPTS.jsonl`, guarded delivery | edit prompts, queue, manuscript, tools, config or the skill; approve art; build PDFs; push anything other than incoming images and receipts; force-push; create branches |
| Owner | starts Codex sessions, art-direction calls, final say | |

Codex is a worker with disjoint ownership in the sense of `CLAUDE.md`. Its only writable paths are `assets/art/incoming/ART-*.{png,jpg,webp}` and `production/art/gpt/RECEIPTS.jsonl`, and `delivery_guard.py` enforces this.

## One-time setup (PowerShell)

```powershell
git lfs install
$env:GIT_LFS_SKIP_SMUDGE = "1"          # don't download LFS art or the private PDFs you don't need
git clone -c core.autocrlf=false https://github.com/xjordont/Heraldry.git
cd Heraldry
git lfs install --local --skip-smudge
py -3 -m pip install pillow
```

`core.autocrlf=false` keeps prompt files byte-exact; `.gitattributes` also pins them to LF. Never fetch `references/private/pdfs/` (owner reference books) for this work.

## Every session

```powershell
cd Heraldry
git status                     # must be clean, or only your own unsent images and receipts
git pull --ff-only origin main
$env:HERALDRY_SCRATCH = "$HOME\heraldry_scratch"   # previews, attempt counts, QA files: outside the repo
py -3 production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
py -3 production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
py -3 production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

The preflight should say `READY` with `delivery: git_lfs`. `status` prints the single next action. Obey it.

## Image generation

- Use the image generation available in Codex under the owner's ChatGPT plan. **Do not use a paid OpenAI API key** (owner: no extra spending beyond ChatGPT Plus). If Codex cannot generate images within the plan, stop and say so.
- Preferred model: **GPT Image 2.5 Sunburst** (`gpt-image-2.5-sunburst`) if offered, otherwise the best available. Record the exact model name with `save --model`.
- Attach **every** reference listed for the item, and nothing else: the owner's hand-inked samples in `assets/art/style/`. If the tool cannot take reference images, stop and report it: never generate unanchored.
- Size: the queue size is the minimum and fixes the aspect. Request the largest size offered at that aspect.
- Art direction (owner, 2026-10-11): "a notch more hand drawn and authentic human art-like". That means confident hand-inked contours, economy of line, hatching only for form and shadow, and open white paper, like the samples. No hyper-detail, stipple fields, noisy texture or rendered polish. Details are in `production/art/skill/heraldry-classic-ink-art/references/STYLE.md` and `docs/ART_DIRECTION.md`.

## Per item (from `SKILL.md`; the full contract is there)

1. `heraldry_art.py show ID`: the verbatim prompt, references, size, MUST and DO NOT DRAW lists.
2. Generate with the verbatim prompt; at most two correction sentences on retries (`references/REPAIR.md`).
3. Save the native file to `%HERALDRY_SCRATCH%`, then `heraldry_art.py check ID FILE`. Look at the image and the print-size preview beside the references.
4. `fidelity_gate.py create ID FILE --prompt-sha <hash> --reference <each ref> --out %HERALDRY_SCRATCH%\ID.qa.json`, then fill all ten criteria with real, specific evidence (`references/QA_CHECKLIST.md`).
5. `heraldry_art.py save ID FILE --qa-file ... --must "..." --avoid-clear --model "..."`.
6. Stay within each item's attempt budget; `--accept-flags` only at the last attempt.

## Delivery (no ZIPs)

When `status` asks for delivery:

```powershell
py -3 production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py sheet --refs --out "$env:HERALDRY_SCRATCH\sheet.jpg"
py -3 production/art/skill/heraldry-classic-ink-art/scripts/style_audit.py --repo . --out "$env:HERALDRY_SCRATCH\style.json"
py -3 production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py audit --repo .
py -3 production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py ship --execute --repo .
```

`ship` stages only queued images and receipts, verifies every receipt against the native bytes, prompt, references and QA, checks LFS, and pushes to `main` with no force. If it says `main` advanced: `git pull --ff-only origin main`, then audit and ship again. If the pull refuses, stop and report. The push triggers the `Intake ChatGPT artwork` workflow.

Then report: IDs, model name, pixel sizes, attempts, QA failures or accepted flags, and the commit SHA. Stop at the phase gate. For anchors, deliver all five and stop until Claude Code has reviewed them and published the next queue.

## Rules that always apply

- `CLAUDE.md` governs the repository. Work on `main` only, never force-push, never rewrite history.
- Never print, log or commit a credential. Git uses the owner's existing Windows login.
- Build on request only: Codex never runs `make all`, builds PDFs or dispatches the delivery rebuild.
- Nothing Codex delivers is approved. Claude Code reviews every image.
