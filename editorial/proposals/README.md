# Manuscript proposals

Keep new, unapplied proposal batches here. Promote an owner-approved batch once with `tools/revise_manuscript.py`; the canonical applied evidence is its immutable `editorial/history/RC###.json`, referenced and hashed by `source/versions.json`.

Seven already-applied proposal copies were removed on 2026-10-15 after byte-for-byte comparison with their archived records. `production/cleanup/2026-10-15.json` maps each former path to its retained canonical copy and records its SHA-256. Historical mentions of those proposal paths describe the original transaction.

`rc487-contradiction-audit.json` remains because it is unique evidence referenced by the contradiction audit and its checks. It is a proposed historical batch, not an authorization to apply it.

The approved `publication-first-pass.json` was promoted once to RC493 and its applied duplicate removed after byte-for-byte comparison with `editorial/history/RC493.json`. The retained archive and SHA-256 are recorded in `production/qa/rc493-editorial-verification.json`; the proposal remains recoverable in Git history.
