# Standing Heraldry artwork prompts

## Primary route: local Codex and GitHub main

Use Codex on the owner's Windows PC with the authenticated `xjordont/Heraldry` checkout on `main`. GitHub holds the authoritative prompts, queue, references, artwork, receipts, and review decisions. The separate art checkout provides local file bytes and Git LFS transport.

Start with [CODEX_PROMPT.md](../codex/CODEX_PROMPT.md), which follows [CODEX_RUNBOOK.md](../codex/CODEX_RUNBOOK.md), `INSTRUCTIONS.md`, and the deployed v8 skill. Deliver production artwork through `delivery_guard.py ship --execute` to GitHub `main`. Keep native attempts, QA reports, previews, and contact sheets outside the checkout.

If guarded delivery fails, preserve the work and create the review bundle. Report that delivery remains pending; do not force-push, auto-rebase, or pull over unsent artwork or receipts. ZIP transfer is a fallback, rather than the primary workflow. Independent review and the stop after the five anchors still apply.

Installing these instructions does not authorize image production. A readiness-only session runs setup checks and reports capabilities without generating images, saving production receipts, pushing artwork, or approving anything.

## Offline Work fallback

The owner pastes this into ChatGPT Work to start an art session, with a freshly built input package attached (`Heraldry_Work_Input_<phase>.zip`: download it from a run of the `Build art packages` workflow, or ask Claude Code to build it; packages are not committed).

**No credentials ever go into a Work conversation.** An earlier draft (2026-10-11) had Work clone and push with a GitHub token. ChatGPT refused it and flagged the pasted token as a leaked secret, and it was right to: a credential pasted into a third-party chat is exposed. That route is withdrawn. Use only what is below. If a token was ever pasted, revoke it.

```text
Use the attached Heraldry Work input package. Our GitHub repo is the source of truth, but you don't need Git or any credentials: everything is inside this ZIP.

1. Unzip it into a new empty folder, /mnt/data/heraldry_work. Open START_HERE.md and follow it exactly, running every command from that folder. Never run git init, clone or pull.
2. Run the offline preflight, then the helper's doctor and status. Show me the output. If anything is BLOCKED, stop and report it word for word.
3. Capability check: you must be able to attach every reference image an item lists, and the generated image must be saved as a real file Python can open. If you cannot attach every reference, stop and tell me.
4. Image model: use GPT Image 2.5 Sunburst if your image tool offers it, otherwise the default. Tell me the exact image model name you used.
5. Take items from `next` (redos first). For each item: use the exact prompt from show ID; attach only its listed references; request the maximum resolution (largest size, highest quality) you offer at the listed aspect; keep the native file unchanged; run check; inspect the image and print-size preview beside the references; run qa and complete the ten-point draft with real evidence; then save (it finds the draft). Art direction: gritty old-school black ink, bold rough brush contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast, like the owner samples. No grey wash, stippling or machine-even texture. Retry only within each item's attempt limit.
6. Whenever status says DRIFT REVIEW, THEN BUNDLE (every ten images), make the contact sheet and style audit, then bundle with those as evidence.
7. Give me the review ZIP (/mnt/data/Heraldry_Work_Review_<phase>.zip) as a downloadable file, with a short report: each ID, the image model name, the pixel size produced, attempts used, any QA failures or accepted flags, and the bundle SHA-256. State plainly that nothing was pushed and nothing is approved. Hand over one ZIP per bundle and continue until status says NOTHING LEFT or your usage ends.
```

Returning the review ZIP: upload it unchanged to `production/art/work/inbox/` on GitHub (Add file, Upload files), or attach it to Claude Code. The `Import Work review bundle` workflow verifies it, commits the images through LFS and runs the intake.
