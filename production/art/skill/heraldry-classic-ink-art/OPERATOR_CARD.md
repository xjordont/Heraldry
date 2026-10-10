# Operator card

## The loop

1. **ChatGPT Work** runs the `anchors` queue (5 images) and pushes. It stops.
2. **You** tell Claude Code: "Review the anchors." Claude Code runs the intake, looks at them, approves or rejects them, and publishes the batch queue.
3. **ChatGPT Work** runs the batch in order, pushing every 5 images (never more than 10 unsent) and at session end.
4. **Claude Code** reviews each push. A rejected image goes back into the queue and shows as `redo`.
5. Repeat 3 and 4 until `status` reports nothing left.

Claude Code owns the prompts, queue, references, review and approval. ChatGPT Work only generates and delivers.

## Start prompts

**First run (anchors)**

> Use the heraldry-classic-ink-art skill. Repo: xjordont/heraldry, branch main. Do the session start steps, then run the anchors queue exactly as the skill says. Push, then stop and tell me.

**Batch run**

> Use the heraldry-classic-ink-art skill on xjordont/heraldry, main. Pull, run doctor and status, then work through the queue in order without asking me between items. Push every 5 images and at session end. Stop at a stop condition and give me the report.

**Resume (new conversation)**

> Resume the Heraldry illustration queue with the heraldry-classic-ink-art skill. Pull main, run doctor and status, and continue from the next action it prints. The same rules apply.

**Redo rejected images**

> Use the heraldry-classic-ink-art skill. Claude Code rejected some images; they show as redo in status. Regenerate only those, within their attempt budget, and push.

## If something looks wrong

- `doctor` says NOT READY: read what it lists. Usually git-lfs is missing or the clone is stale.
- A prompt does not match its hash: someone republished the queue. Pull again.
- The whole batch looks drifted or alike, not just one or two images (the runner redoes those itself): stop the run, start a fresh conversation, and use the resume prompt.
- The tool refuses an item: the refusal is recorded in `RECEIPTS.jsonl`. Tell Claude Code; it owns the prompt.
