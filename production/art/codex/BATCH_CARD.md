# Codex batch card (the whole art-worker contract on one page)

Read this and `AGENTS.md` only. Open `SKILL.md` or `references/*.md` only when one of them is named below for a specific case. Work in PowerShell from `C:\Heraldry\art-producer`, with `$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"`, `$env:HERALDRY_ARCHIVE = "C:\Heraldry\art-archive"` (save keeps the PC's copy of each delivered image there) and `$env:PYTHONUTF8 = "1"`. `H <name>.py` stands for `& C:\Heraldry\art-venv\Scripts\python.exe production/art/skill/heraldry-classic-ink-art/scripts/<name>.py`. Keep every file you make in `$env:HERALDRY_SCRATCH`, never in the clone: a stray file there blocks delivery.

## Start of session
1. `git status --short` must be empty, or show only your unsent `assets/art/incoming/*` and `RECEIPTS.jsonl`. If it is clean, `git pull --ff-only origin main`. If work is unsent, or that pull fails, run `H delivery_guard.py ship --execute --repo .` first (it recovers unsent and half-sent deliveries itself). Never resolve git by hand.
2. `H work_preflight.py --repo . --require-installed`. If it is BLOCKED only by lines `LFS pointer, fetch before generation: PATH`, run `git lfs pull --include="assets/art/style/*"` (never the PDFs) and run it again. Any other BLOCKED: stop and quote it. No smoke-test file is needed.
3. The target is gritty old-school ink: bold rough contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast, pure black ink (no grey wash). Each item names its reference set (`ref_set`); look at each reference file once per session, the first time it is attached. A few references are old etchings (take their line and blacks, never their period costume), and a few are cleaner line work (02, 15, 20, 36: take their construction; the grit target still applies). The lead items (after any redo) cover one of each set.

## Per item (repeat until NOTHING LEFT)
1. `H heraldry_art.py next --n 1` names the next item (redos first, with the reviewer's reason; it first brings a clean clone up to date, so a redo sent back mid-session shows at once), then `H heraldry_art.py show ID`.
2. **One generation per item** (owner 2026-10-12: first generations are far better than retries). Generate once, in a fresh image request with no earlier image or item in its context, with the prompt exactly as printed (for a redo, plus at most two correction sentences from the reviewer's reason, `references/REPAIR.md`; if the reason contradicts the prompt, the prompt wins: say so). Attach exactly the listed references, in order. Request the largest size and best quality offered at the listed aspect; GPT Image 2.5 Sunburst if offered, otherwise the default; no paid API. Save the native file unchanged as `$env:HERALDRY_SCRATCH\ID.<the tool's extension>`. If the image call shows no image, do not call it again: the tool usually saved it anyway, so take the newest file in the tool's generated-images folder made after the call. Only if no such file exists may you make one more call, and say so in `--notes`.
3. `H heraldry_art.py check ID FILE`. Look at the image and its print-size preview: every MUST line (count things), every DO NOT DRAW line, no lettering, black ink only, edges (a fault only if the subject is cropped or touches an edge; a narrow margin is fine), anatomy, and grit (too clean or finely engraved is a style fail). A line "Not the X (traits)" means your image must not show those traits; do not open X.
4. Never generate a second image for the item. A hard fail is still saved, with `--accept-flags --notes "<what is wrong>"`; Claude Code decides on a redo.
5. `H heraldry_art.py qa ID FILE` on the exact file you will save. In the JSON it names, set `references_attached`, `prompt_unchanged` (still true with correction sentences) and `visual_review_at_print_size` to `true`; `register_compared` as printed; each of the ten `checks` to `{"pass": true|false, "evidence": "<15+ characters of what you saw>"}`. A clean save leaves `unresolved_issues` as `[]`; with `--accept-flags`, failed checks are `false` and the defects are listed there.
6. `H heraldry_art.py save ID FILE --must "<positive statement, 10+ characters>" --avoid-clear --model "<label shown, or not shown>" --notes "<correction sentences used, if any>"`. Give exactly one `--must` per MUST line, in order, and none when `show` lists no MUST line. A statement that admits a miss ("missing", "not shown", "0 x") is refused.

## Delivery (after every saved image; then `H heraldry_art.py status`)
- **status says DELIVER:** `H delivery_guard.py ship --execute --repo .` (it runs every delivery check, fast-forwards over the intake bot's commits and retries a lost race). Give the command at least 10 minutes: the Git LFS upload can be slow. If it prints nothing (your tool timed out), run `H heraldry_art.py status`; `0 saved-not-pushed` means the delivery landed. A ship that reports `UP-TO-DATE` is not a fault: continue with `next`.
- **status says DRIFT REVIEW** (every 10 images): `H heraldry_art.py sheet --recent 10 --refs` and `H style_audit.py --repo . --recent 10` (both write to the scratch folder; the audit prints any advisories); look at the sheet once. Then ship in every case. One image drifted: name it in your report. Two or more same-register images share a style drift (line weight, grey tone, too clean, scenery behind figures; not margins): name it in your report and keep going (Claude Code reviews and sends redos). Nothing drifted: say so.
- **ship says BLOCKED:** `H heraldry_art.py bundle`, report the reason and stop. Never pull, rebase, force or commit by hand.

## Stop and report when
- `next` says nothing pending and status says NOTHING LEFT;
- the image tool cannot attach the listed references (if it refuses one item, `H heraldry_art.py refuse ID --reason "<what it said>"`, deliver, and continue);
- the plan's usage limit is reached (ChatGPT Plus: it resets every 5 hours; everything saved is already delivered, and the owner restarts the same prompt, which resumes from `next`);
- ship is BLOCKED.

Do not stop for drift, flagged images or a long queue: the owner wants the whole list run (2026-10-12).

## Keep it lean
- Don't re-read docs between items, don't print JSON you don't need, don't cat receipts.
- Report one line per item (ID, attempts, flags) plus the commit SHA of each delivery.

## Never
- Edit prompts, the queue, the manuscript, tools, config or the skill.
- Approve art, build PDFs, create branches, force-push, or print credentials.
- Write anything in the clone except `assets/art/incoming/<ID>.<ext>` and `production/art/gpt/RECEIPTS.jsonl`, and those only via `save` and `ship`.
