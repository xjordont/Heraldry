# Codex batch card (the whole art-worker contract on one page)

Read this and `AGENTS.md` only. Open `SKILL.md` or `references/*.md` only when one of them is named below for a specific case. Work in PowerShell from `C:\Heraldry\art-producer`, with `$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"` and `$env:PYTHONUTF8 = "1"`. `H <name>.py` stands for `& C:\Heraldry\art-venv\Scripts\python.exe production/art/skill/heraldry-classic-ink-art/scripts/<name>.py`. Keep every file you make in `$env:HERALDRY_SCRATCH`, never in the clone: a stray file there blocks delivery.

## Start of session
1. `git status --short` must be empty, or show only your unsent `assets/art/incoming/*` and `RECEIPTS.jsonl`. If it is clean, `git pull --ff-only origin main`. If work is unsent, or that pull fails, run `H delivery_guard.py ship --execute --repo .` first (it recovers unsent and half-sent deliveries itself). Never resolve git by hand.
2. `H work_preflight.py --repo . --require-installed`. If it is BLOCKED only by lines `LFS pointer, fetch before generation: PATH`, run `git lfs pull --include="assets/art/style/*"` (never the PDFs) and run it again. Any other BLOCKED: stop and quote it. No smoke-test file is needed.
3. The target is gritty old-school ink: bold rough contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast, pure black ink (no grey wash). Each item names its reference set (`ref_set`); look at each reference file once per session, the first time it is attached. A few references are old etchings (take their line and blacks, never their period costume), and a few are cleaner line work (02, 15, 20, 36: take their construction; the grit target still applies). The first seventeen items cover one of each set.

## Per item (repeat until NOTHING LEFT)
1. `H heraldry_art.py next --n 1` names the next item (redos first, with the reviewer's reason), then `H heraldry_art.py show ID`.
2. Generate with the prompt exactly as printed. Attach exactly the listed references, in order. Request the largest size and best quality offered at the listed aspect; GPT Image 2.5 Sunburst if offered, otherwise the default; no paid API. Save the native file unchanged as `$env:HERALDRY_SCRATCH\ID_aN.<the tool's extension>`.
3. `H heraldry_art.py check ID FILE`. Look at the image and its print-size preview: every MUST line (count things), every DO NOT DRAW line, no lettering, black ink only, edges, anatomy, and grit (too clean or finely engraved is a style fail). A line "Not the X (traits)" means your image must not show those traits; do not open X.
4. On any hard fail, retry with at most two correction sentences (`references/REPAIR.md`); for a redo, base them on the reviewer's reason (if it contradicts the prompt, the prompt wins: say so). Stop at the first clean attempt. After the item's last attempt, save the best attempt with `--accept-flags --notes "<what is still wrong>"`.
5. `H heraldry_art.py qa ID FILE` on the exact file you will save. In the JSON it names, set `references_attached`, `prompt_unchanged` (still true with correction sentences) and `visual_review_at_print_size` to `true`; `register_compared` as printed; each of the ten `checks` to `{"pass": true|false, "evidence": "<15+ characters of what you saw>"}`. A clean save leaves `unresolved_issues` as `[]`; with `--accept-flags`, failed checks are `false` and the defects are listed there.
6. `H heraldry_art.py save ID FILE --must "<positive statement, 10+ characters>" --avoid-clear --model "<label shown, or not shown>" --notes "<correction sentences used, if any>"`. Give exactly one `--must` per MUST line, in order, and none when `show` lists no MUST line. A statement that admits a miss ("missing", "not shown", "0 x") is refused.

## Delivery (after every saved image; then `H heraldry_art.py status`)
- **status says DELIVER:** `H delivery_guard.py ship --execute --repo .` (it runs every delivery check, fast-forwards over the intake bot's commits and retries a lost race).
- **status says DRIFT REVIEW** (every 10 images): `H heraldry_art.py sheet --recent 10 --refs` and `H style_audit.py --repo . --recent 10` (both write to the scratch folder; the audit prints any advisories); look at the sheet once. Then ship in every case. One image drifted: name it in your report. Two or more same-register images share a fault: ship, then stop and report. Nothing drifted: say so and continue.
- **ship says BLOCKED:** `H heraldry_art.py bundle`, report the reason and stop. Never pull, rebase, force or commit by hand.

## Stop and report when
- `next` says nothing pending and status says NOTHING LEFT;
- the image tool cannot attach the listed references (if it refuses one item, `H heraldry_art.py refuse ID --reason "<what it said>"`, deliver, and continue);
- the plan's usage limit is reached (everything saved is already delivered; the next session resumes from `next`);
- a drift review finds a shared fault, or ship is BLOCKED.

## Keep it lean
- Don't re-read docs between items, don't print JSON you don't need, don't cat receipts.
- Report one line per item (ID, attempts, flags) plus the commit SHA of each delivery.

## Never
- Edit prompts, the queue, the manuscript, tools, config or the skill.
- Approve art, build PDFs, create branches, force-push, or print credentials.
- Write anything in the clone except `assets/art/incoming/<ID>.<ext>` and `production/art/gpt/RECEIPTS.jsonl`, and those only via `save` and `ship`.
