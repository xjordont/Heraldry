# Standing Heraldry artwork prompts

## Codex on the owner's PC (current route)

Use Codex on the owner's Windows PC with the authenticated `xjordont/Heraldry` checkout on `main`. GitHub holds the authoritative prompts, queue, references, artwork, receipts, and approvals. The separate art checkout provides local file bytes and Git LFS transport.

Start with [CODEX_PROMPT.md](../codex/CODEX_PROMPT.md), which follows [BATCH_CARD.md](../codex/BATCH_CARD.md), [CODEX_RUNBOOK.md](../codex/CODEX_RUNBOOK.md), `INSTRUCTIONS.md`, and the v8 skill. Deliver every image through `delivery_guard.py ship --execute` to GitHub `main`; that push is the only delivery. Keep native attempts, QA reports, previews, and contact sheets outside the checkout.

If guarded delivery fails, stop: keep the saved images and receipts in the clone, and report that delivery is pending. Don't force-push, auto-rebase, or pull over unsent artwork or receipts. A readiness-only session runs the setup checks and reports capabilities without generating images.

## ChatGPT Work and other clients

Another client can run the queue only with an authenticated Git checkout of `main`, Git LFS, Python, and an image tool that accepts each item's listed references, because Git push is the only delivery. Use the session prompt in the skill's [OPERATOR_CARD.md](../skill/heraldry-classic-ink-art/OPERATOR_CARD.md).

**No credentials ever go into a Work conversation.** An earlier draft (2026-10-11) had Work clone and push with a GitHub token. ChatGPT refused it and flagged the pasted token as a leaked secret, and it was right to: a credential pasted into a third-party chat is exposed. That route is withdrawn; if a token was ever pasted, revoke it. Without authenticated Git, a Work session cannot deliver: it says so and stops.
