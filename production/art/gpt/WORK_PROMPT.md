# Standing ChatGPT Work prompt (Git route, no ZIP files)

The owner pastes the text below into ChatGPT Work to start every art session. It never changes between batches: Work pulls the current queue, prompts and references from GitHub, and pushes the images back. Claude Code publishes each new queue to `main`.

One-time setup (owner): create a fine-grained GitHub token. In GitHub, go to Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token and choose:

- **Repository access:** Only select repositories → `xjordont/Heraldry`
- **Permissions:** Contents: Read and write (Metadata: Read is added automatically). Nothing else.
- **Expiration:** 30 days. Revoke it whenever art work pauses.

Give the token to Work once per session, as the prompt asks. It ends up in that Work conversation's history, which is why it is limited to this one repository's contents and expires.

---

```text
Run the Heraldry art queue from GitHub (xjordont/Heraldry, branch main) using the heraldry-classic-ink-art v6 skill in the repository. No ZIP files: you clone, generate and push.

SETUP (never print, echo or log the token)
1. I will give you a GitHub token. Save it with Python to /mnt/data/.heraldry_token (file mode 600) and never display it.
2. Run in the shell:
   git config --global credential.helper '!f(){ echo username=x-access-token; echo "password=$(cat /mnt/data/.heraldry_token)"; }; f'
   git config --global user.name "ChatGPT Work"; git config --global user.email "chatgpt-work@users.noreply.github.com"
   cd /mnt/data && rm -rf heraldry
   GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --sparse https://github.com/xjordont/Heraldry.git heraldry
   cd heraldry && git sparse-checkout set production/art/gpt production/art/skill assets/art/style assets/art/incoming config && git lfs install --local --skip-smudge
3. Read production/art/gpt/INSTRUCTIONS.md and production/art/skill/heraldry-classic-ink-art/SKILL.md, then follow them exactly, from /mnt/data/heraldry. Keep scratch files in /mnt/data/heraldry_scratch (set HERALDRY_SCRATCH=/mnt/data/heraldry_scratch on every helper command).
4. Run work_preflight.py --repo . --require-installed, then heraldry_art.py doctor and status. Show me the output. If anything says BLOCKED, stop and report it word for word.

SMOKE TEST
5. Confirm that your image tool accepts every reference image an item lists and that the generated file is on disk where Python can read it. Only if all three are true, write /mnt/data/heraldry_scratch/smoke.json and rerun the preflight with --smoke-file. If not, stop and report it.

GENERATE
6. Use the GPT Image 2.5 Sunburst model if your image tool offers it, otherwise the default. Request the largest size offered at each item's aspect. Generate only what `status` says, in queue order, following the per-item loop in SKILL.md: show ID, the exact prompt, only the listed references, check, inspect beside the references at print size, the ten-point QA file, then save with --qa-file. Art direction: hand-inked, economy of line, open white paper, like the owner's samples; no hyper-detail or stippling.

DELIVER
7. When status asks for delivery (every 5 images, at the end of the queue, or at session end): run sheet --refs and the style audit, then delivery_guard.py audit --repo . and, only if it passes, delivery_guard.py ship --execute --repo . Report the commit SHA it prints.
8. If the push is refused for any reason, run heraldry_art.py bundle with the sheet, style audit and smoke record as --evidence, give me the review ZIP as a downloadable file, and say plainly that nothing was pushed.

STOP
9. Stop when status says STOP (for the anchors phase, after delivering all five). Report each ID, the image model name, the pixel size produced, attempts used, QA failures or accepted flags, and the commit SHA or bundle. Nothing you deliver is approved: Claude Code reviews it.
```
