# Automatic GitHub README maintenance

`tools/update_readme.py` owns only the `AUTO:status` and `AUTO:recent` blocks in the root `README.md`. Hand-written guidance outside them remains editable. Do not edit generated blocks directly.

The status comes from the active manuscript registry (with its hash checked), recorded release pointer/result, matching PDF-review page count, illustration selection records and generation queue, and current figure/SVG/caption/manuscript review hashes. It distinguishes current source from the last recorded PDF delivery. It never approves artwork or figures, binds reviews, changes the manuscript, or builds/releases PDFs. Physical printing remains NOT TESTED unless the release result explicitly records TESTED.

The recent-change list links the six latest commits affecting files other than README.md. README-only commits are excluded so the updater does not continually report itself. Commit subjects are escaped as Markdown.

## Local use

`python tools/dev.py check` refreshes the generated blocks before its ordinary checks. For a focused refresh or read-only currency check:

```sh
python tools/update_readme.py --write
python tools/update_readme.py --check
```

Commit the refreshed README with your checked changes. Its recent-commit list catches up to the new commit after GitHub receives the push.

## GitHub use

The `Update GitHub README` workflow runs after every push to main, with no path exclusions. It also runs after completion (success, failure, or cancellation) of every other repository workflow. This covers commits made with GitHub's workflow token, which do not trigger another push workflow. A manual dispatch is available for recovery. When adding a workflow, add its exact name to the completion list; a repository test enforces coverage.

Only trusted main is checked out. Pull-request workflow completions and other repositories are excluded. The updater consumes no upstream artifacts or caches. It runs baseline preflight and the required tests before publishing.

README, candidate, and release jobs share the `publication-main` concurrency group with `queue: max`, so a README update cannot push during a running publication job or replace its pending run. The updater also defers when a candidate/release is queued, pending, waiting, requested, or running, and when its triggering push changes the build request or visual-review ledger. Completion of that publication workflow supplies the follow-up refresh. API failures fail closed and are visible as a failed README workflow. The existing release guard still rejects stale event commits, including an exceptionally timed new dispatch; no stale build is made releasable by this updater.

Publication fetches current main and renders metadata, README, and history from that same commit. A temporary Git index creates a commit whose only changed path must be README.md. A normal fast-forward push is required. A competing main update retries from the new parent; new publication inputs defer it. No checkout reset, rebase, or force-push is used. Unchanged content produces no commit. Hosted refreshes take effect after their checks finish; GitHub outages or workflow failures require a successful rerun.

The workflow has contents-write and actions-read permissions. No personal token or additional paid service is needed. [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) and [concurrency queues](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) document these platform behaviours.
