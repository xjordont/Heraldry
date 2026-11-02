# Automatic GitHub README maintenance

You don't need to do anything to keep the README current: GitHub refreshes it.

`tools/update_readme.py` owns only the `AUTO:status` and `AUTO:recent` blocks in the root `README.md`. Edit the hand-written guidance outside them freely, but never edit the generated blocks.

- **Status block:** built from the active manuscript registry, the recorded release, the PDF review, the illustration records and queue, and the figure review hashes. It separates the current source from the last PDF delivery.
- **Recent block:** links the six latest commits that touch anything other than `README.md`.

## GitHub

The `Update GitHub README` workflow runs after every push to `main` and after each workflow that commits to `main` (those commits use the workflow token, which starts no push run). It installs nothing and runs no tests: the refresher is standard library only, and Repository checks already tests each push. When you add a workflow that commits to `main`, add its exact name to the completion list; a repository test enforces the list both ways.

The workflow shares the `publication-main` concurrency group (`queue: max`) with the candidate and release jobs, and defers while a build is queued or running. It commits only `README.md`, with a normal fast-forward push, and makes no commit when nothing changed.

## Locally (optional)

`python tools/dev.py check` refreshes the blocks as a side effect. For a focused refresh or a currency check:

```sh
python tools/update_readme.py --write
python tools/update_readme.py --check
```
