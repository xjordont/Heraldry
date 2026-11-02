# Prompt to paste into Codex for the unattended build and release

```text
You are building and releasing Heraldry in C:\Heraldry\art-producer (xjordont/Heraldry, branch main). Read AGENTS.md, the newest entries of production/STATE.md, and production/codex-build/CODEX_BUILD_CARD.md, then follow the card. Use C:\Heraldry\art-venv\Scripts\python.exe with PYTHONUTF8=1 and HERALDRY_SCRATCH=C:\Heraldry\art-scratch.

This prompt is an explicit request for the whole GitHub build and release, including the all-page visual review that gates it. A real defect is a major finding. Fix code or layout failures and retry; a changed PDF needs a fresh candidate and review. Never create a branch, force-push, rewrite history, edit source/ snapshots, or touch credentials. Rules or design decisions belong to the owner.

Final report: request id and commit, candidate result, sheets and detail pages reviewed with any minor notes, ledger commit SHA, release result, release_url, and "Physical print: NOT TESTED."
```
