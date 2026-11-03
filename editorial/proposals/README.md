# Manuscript proposals

Proposal batches live here: a Markdown write-up for the owner and, while the batch awaits approval, its machine-readable JSON twin (`status: "proposed"`; drafts cannot be promoted). Promote an owner-approved batch once with `tools/revise_manuscript.py`. The canonical applied evidence is its immutable `editorial/history/RC###.json`, referenced and hashed by `source/versions.json`.

Applied write-ups stay here as records. Each file's header states whether it was applied, as which RC, and which items were left out. After promotion the JSON twin is normally removed once it matches the archive (`rc528-humanizer-review.json` was kept). Wording proposals can be checked with the read-only `blind-editorial-reviewer` role (`docs/agents/blind-editorial-reviewer.md`), which rates each proposed line against the current one without seeing the rationale.

`rc487-contradiction-audit.json` remains because it is unique evidence referenced by the contradiction audit and its checks. It is a proposed historical batch, not an authorization to apply it.

Earlier applied copies were removed after byte-for-byte comparison with their archives: seven on 2026-10-15 (`production/cleanup/2026-10-15.json` maps each former path to its retained copy), and `publication-first-pass.json` after it became RC493 (`production/qa/rc493-editorial-verification.json`).
