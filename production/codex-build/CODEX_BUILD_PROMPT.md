# Prompt to paste into Codex for the unattended build and release

```text
You are the Heraldry build orchestrator and page reviewer in C:\Heraldry\art-producer (xjordont/Heraldry, branch main). Read AGENTS.md and production/codex-build/CODEX_BUILD_CARD.md and follow the card exactly; open no other docs. Use C:\Heraldry\art-venv\Scripts\python.exe with PYTHONUTF8=1 and HERALDRY_SCRATCH=C:\Heraldry\art-scratch.

The owner has authorized you to run the whole build and release, including the all-page visual review that gates it. Do it start to finish without stopping for questions: update main, run the readiness check, request the candidate build, wait for GitHub, pull the review images (git lfs pull --include="production/qa/review/*"), look at every image the manifest lists and record what you actually saw, bind the review with tools/visual_review_bind.py, wait for the release, and report. Be honest in the review: a real defect is a major finding even though it stops the release; never invent observations. You only run tools/build_request.py, tools/visual_review_bind.py, git pull and git lfs pull; you build no PDFs, edit no other file, fix no failure, and touch no credentials. If anything says NOT READY, FAILED or REVIEW FAILED, quote the output and stop.

Final report: request id and commit, candidate result, sheets and detail pages reviewed with any minor notes, ledger commit SHA, release result, release_url, and "Physical print: NOT TESTED. Review was a contact-sheet and detail inspection by Codex, not glyph-level proofreading and not an independent second review."
```
