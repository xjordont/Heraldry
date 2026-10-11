# Prompt to paste into Codex

The same prompt serves every session; the live queue says what to do. Without the authorization line, Codex only runs the readiness checks.

```text
You are the Heraldry art worker in C:\Heraldry\art-producer (xjordont/Heraldry, branch main). Read AGENTS.md and production/art/codex/BATCH_CARD.md, and follow the card exactly. Do not read other docs unless the card names one for a specific case. Use C:\Heraldry\art-venv\Scripts\python.exe with HERALDRY_SCRATCH=C:\Heraldry\art-scratch and PYTHONUTF8=1.

Production is authorized for the full batch queue: generate every item status gives you, in order, delivering each image with ship as soon as it is saved, until status says NOTHING LEFT or a stop condition on the card applies. If your session or usage limit ends, stop; I will start a new session with this same prompt and you resume from status.

Report one line per item and the commit SHA of each delivery. Nothing you make is approved: Claude Code reviews it.
```

After an art-direction change, start with a short calibration run: add the line `Stop after 5 delivered images.` to the prompt, let Claude Code review those five, then run the full queue with the unchanged prompt.

For a readiness check only, delete the "Production is authorized" paragraph: Codex then runs the card's start-of-session steps and stops.
