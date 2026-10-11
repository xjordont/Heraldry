# Codex batch card (the whole art-worker contract on one page)

Read this and `AGENTS.md` only. Open `SKILL.md` or `references/*.md` only when one of them is named below for a specific case. Paths are relative to `C:\Heraldry\art-producer`. `H` means `C:\Heraldry\art-venv\Scripts\python.exe production/art/skill/heraldry-classic-ink-art/scripts/`. Set `HERALDRY_SCRATCH=C:\Heraldry\art-scratch` and `PYTHONUTF8=1`.

## Start of session
1. `git status --short` must be empty, or show only your unsent `assets/art/incoming/*` and `RECEIPTS.jsonl`. If it is clean: `git pull --ff-only origin main`. If work is unsent, deliver it first (see Delivery).
2. `H work_preflight.py --repo . --require-installed`, then `H heraldry_art.py status`. Stop on BLOCKED or NOT READY and quote the output.
3. Look once at each reference this session: `assets/art/style/STYLE-REF-07*`, `-09*` and `-10*` for scenes; `-03*`, `-04*`, `-05*` and `-06*` for figures and still lifes. The target is gritty old-school ink: bold rough brush contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast, pure black ink (no grey wash).

## Per item (repeat until status says NOTHING LEFT)
1. `H heraldry_art.py status`, then `H heraldry_art.py show ID`. Redo items come first; `show` prints the reviewer's reason.
2. Generate with the prompt exactly as printed. Attach exactly the listed references, in order. Request the largest size and best quality offered at the listed aspect. Use GPT Image 2.5 Sunburst if the tool offers it; otherwise the default. No paid API. Save the native file unchanged to `%HERALDRY_SCRATCH%\ID_aN.png`.
3. `H heraldry_art.py check ID FILE`. Look at the image and its print-size preview. Check every MUST line (count things), every DO NOT DRAW line, no lettering, black ink only, edges, anatomy, and that it is as gritty and bold as the references (too clean or finely engraved is a style fail).
4. On any hard fail: retry, adding at most two correction sentences (table in `references/REPAIR.md`). The budget is the item's attempts; stop at the first clean attempt. After the last attempt, save the best with `--accept-flags --notes "what is still wrong"`.
5. `H heraldry_art.py qa ID FILE`. Fill the draft it names: three true/false attestations, `register_compared`, and ten `{pass, evidence}` entries. Evidence is one concrete sentence of 15 or more characters about what you saw. Never pass something you did not check.
6. `H heraldry_art.py save ID FILE --must "<what you counted>" ... --avoid-clear --model "<label shown, or not shown>"`. The draft is found automatically.

## Delivery (after every saved image)
Every image is delivered as soon as it is saved, so a usage limit never strands work.
- **status says DELIVER:** `H delivery_guard.py audit --repo .`, then `H delivery_guard.py ship --execute --repo .`.
- **status says DRIFT REVIEW (every 10 images):** first `H heraldry_art.py sheet --recent 10 --refs --out %HERALDRY_SCRATCH%\sheet.jpg` and `H style_audit.py --repo . --recent 10 --out %HERALDRY_SCRATCH%\style.json`, and look at the sheet once. Then audit and ship. `ship` fast-forwards over the intake bot's commits by itself and retries a lost race. If it says BLOCKED: `H heraldry_art.py bundle --evidence ...`, report the reason and stop. Never pull, rebase, force or commit by hand.

## Stop and report when
- status says NOTHING LEFT;
- the image tool cannot attach the listed references, or refuses (record `H heraldry_art.py refuse ID --reason "..."` and continue with the next item);
- the plan's usage limit is reached (anything saved is already delivered or is delivered by `status` first next time; the next session resumes from `status`);
- two or more same-register images show the same drift on the contact sheet;
- ship is BLOCKED.

## Keep it lean
- Don't re-read docs between items. Don't print JSON you don't need: skip `--json`, and don't cat receipts.
- Keep native and preview viewing to what step 3 needs. References: once per session.
- Report one line per item (ID, attempts, flags), plus the commit SHA per delivery.

## Never
- Edit prompts, the queue, the manuscript, tools, config or the skill.
- Approve art, build PDFs, create branches, force-push, or print credentials.
- Write anything except `assets/art/incoming/<ID>.<ext>` and `production/art/gpt/RECEIPTS.jsonl`, and those only via `save` and `ship`.
