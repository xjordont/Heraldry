# Prompt to paste into Codex

## Shared client authority

Owner instruction, 2026-10-22: Claude Code, Codex, and ChatGPT Work have equal developer, orchestrator, repair, and reviewer authority under `docs/AGENT_OPERATIONS.md`. Client names in the procedure identify the original route, not exclusive permissions. A generation-only worker remains scoped to its assigned image/receipt delivery and does not approve its own work. An assigned reviewer on any client may inspect, approve, reject, and send redos using the existing evidence gates. Use the actual client and reviewer name in provenance. Native model/tool, authentication, file, and transport availability must be checked in the current session.


The same prompt serves every session; the live queue says what to do. It runs the whole list (owner 2026-10-12). Codex stops only at NOTHING LEFT, a usage limit, a reference-attachment failure or a blocked ship; a refused item is recorded and skipped. ChatGPT Plus usage resets every 5 hours: when Codex stops at the limit, everything saved is already delivered, so paste the same prompt again after the reset and it resumes from `next`, redos first.

```text
You are the Heraldry art worker in C:\Heraldry\art-producer (xjordont/Heraldry, branch main). Read AGENTS.md and production/art/codex/BATCH_CARD.md, and follow the card exactly. Do not read other docs unless the card names one for a specific case. Use C:\Heraldry\art-venv\Scripts\python.exe with HERALDRY_SCRATCH=C:\Heraldry\art-scratch, HERALDRY_ARCHIVE=C:\Heraldry\art-archive and PYTHONUTF8=1.

Production is authorized for the entire batch queue. Generate every item that next gives you, in order, one generation per item at the maximum output resolution and highest quality your image tool offers at the item's aspect, attaching all of its listed references (up to five) by passing their absolute paths, in order, as referenced_image_paths. An item that lists no references (reference set none) is generated from its prompt alone; that is not a stop. Leave num_last_images_to_include out. For an item that does list references, if your image tool's own instructions forbid reference paths for a new image, stop and report it: never generate such an item without its references. Report the size and quality options the tool offers once, at the start. Deliver each image with ship as soon as it is saved. Do not stop for drift reviews, flagged images, a colour warning, a conflict between a redo reason and the prompt (the prompt wins: note it and continue) or the length of the queue, and do not end your turn after a delivery or wait for review: the assigned reviewer reviews the batch after you finish. Report and keep going until status says NOTHING LEFT. If the image tool refuses one item, record it with refuse, deliver and continue. Stop only for a stop condition on the card: a usage limit, the image tool unable to attach the references an item lists, or ship BLOCKED. If you stop at a usage limit, say so; I will paste this same prompt after the reset and you resume from next.

Report one line per item (ID, flags) and the commit SHA of each delivery, plus a line for each drift review. Nothing you make is approved: The assigned reviewer inspects it and sends redos.
```

For a readiness check only, delete the "Production is authorized" paragraph: Codex then runs the card's start-of-session steps and stops.
