#!/usr/bin/env python3
"""Refresh only the generated README status block; never build the book."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
COMMIT_MESSAGE = "docs: refresh generated README"
PUBLICATION_PATHS = {"production/build-request.json", "production/qa/visual-review.json"}
PUBLICATION_WORKFLOWS = ("build-candidate.yml", "rebuild-delivery.yml")


def git(root, *args, data=None, env=None):
    result = subprocess.run(["git", *args], cwd=root, input=data, capture_output=True, env=env)
    if result.returncode:
        raise RuntimeError(f"git {args[0]} failed; working files and history are preserved")
    return result.stdout


class Snapshot:
    def __init__(self, root, ref=None):
        self.root, self.ref = Path(root), ref

    def read(self, path):
        if self.ref:
            return git(self.root, "show", f"{self.ref}:{path}")
        return (self.root / path).read_bytes()

    def json(self, path):
        return json.loads(self.read(path))


def replace_block(text, name, content):
    start, end = f"<!-- BEGIN AUTO:{name} -->", f"<!-- END AUTO:{name} -->"
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError(f"README requires one ordered AUTO:{name} marker pair; no file was changed")
    a, b = text.index(start) + len(start), text.index(end)
    newline = '\r\n' if '\r\n' in text else '\n'
    content = newline.join(content.rstrip().splitlines())
    return text[:a] + newline * 2 + content + newline * 2 + text[b:]


def escape_markdown(text):
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    for char in "\\`*_{}[]<>|":
        text = text.replace(char, "\\" + char)
    return text


def figure_status(snapshot, source):
    from figure_dependencies import hashes_for_text
    manifest = snapshot.json("figures/manifest.json")
    figures = manifest if isinstance(manifest, list) else manifest["figures"]
    placements = snapshot.json("figures/placements.json")
    captions = {item['id']: item['caption'] for rows in placements.values() for item in rows}
    ledger = {item['id']: item for item in snapshot.json("production/qa/figure-semantic-review.json")["figures"]}
    rules = hashes_for_text(source, snapshot.json("config/figure_dependencies.json"))
    current, open_findings = 0, 0
    for item in figures:
        fid = item['id']
        record = ledger.get(fid, {})
        expected = {"svg_sha256": hashlib.sha256(snapshot.read(f"figures/out/{fid}.svg")).hexdigest(),
                    "caption_sha256": hashlib.sha256(captions[fid].encode()).hexdigest(), "rules_sha256": rules[fid]}
        unresolved = [f for f in record.get("findings", []) if f.get("status") == "open" or
                      (f.get("severity") in {"major", "critical"} and f.get("status") != "resolved")]
        open_findings += len(unresolved)
        if all(record.get(k) == v for k, v in expected.items()) and record.get("verdict") in {"PASS", "PASS_WITH_NOTES"}:
            current += 1
    return len(figures), current, open_findings


def status_block(snapshot):
    versions = snapshot.json("source/versions.json")
    number = versions['current']
    revision = next(r for r in versions['revisions'] if r['number'] == number)
    source = snapshot.read(revision['path']).decode('utf-8')
    if hashlib.sha256(source.encode()).hexdigest() != revision['sha256']:
        raise ValueError("Active manuscript bytes do not match the registry; README not updated")
    release = snapshot.json("dist/RELEASE.json")
    result = snapshot.json("production/RELEASE_RESULT.json")
    review = snapshot.json("production/qa/visual-review.json")
    tag = release['tag']
    if not re.fullmatch(r"RC\d+-build-\d+(?:-attempt-\d+)?", tag):
        raise ValueError("Unrecognised delivery tag")
    # Use the repository's recorded release pointer, not an arbitrary metadata URL.
    delivery = f"https://github.com/xjordont/Heraldry/releases/tag/{tag}"
    assets = release.get('assets', [])
    edition = next((a for a in assets if a['name'].endswith('_digital.pdf')), {})
    pages = f", {review['pages']} pages" if edition.get('sha256') == review.get('sha256') and isinstance(review.get('pages'), int) else ""
    records = snapshot.json("production/art/SELECTIONS.json")
    approved = sum(r.get('status') == 'approved' for r in records.values())
    queue = len(snapshot.json("production/art/gpt/QUEUE.json")['items'])
    total, current, findings = figure_status(snapshot, source)
    pending = f" RC{number} source changes await a separately requested PDF build." if not tag.startswith(f"RC{number}-") else " Newer source/tooling changes may await a separately requested build."
    return "\n".join([
        f"- **Manuscript:** [RC{number}]({revision['path']}) (`source/versions.json`). Earlier snapshots are immutable.",
        f"- **Last recorded delivery:** [{tag}]({delivery}){pages}.{pending} [Evidence and limits](production/STATE.md).",
        f"- **Last release workflow result:** {escape_markdown(str(result.get('result', 'UNAVAILABLE')))}. This records that run, not verification of newer inputs.",
        f"- **Illustration records:** {approved} approved of {len(records)}; {queue} generation-queue items.",
        f"- **Rules figures:** {total}; {current}/{total} current source/SVG/caption review bindings; {findings} open findings. [Review ledger](production/qa/figure-semantic-review.json).",
    ])


def render(root=ROOT, ref=None):
    snapshot = Snapshot(root, ref)
    if ref:
        mode = git(root, 'ls-tree', ref, '--', 'README.md').decode().split()[0]
        if mode not in {'100644', '100755'}:
            raise ValueError('README must be an ordinary tracked file')
    elif (Path(root) / 'README.md').is_symlink():
        raise ValueError('README must be an ordinary file, not a symlink')
    text = snapshot.read('README.md').decode('utf-8')
    return replace_block(text, 'status', status_block(snapshot)).encode('utf-8')


def api_json(repository, endpoint, token):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) or not token:
        raise ValueError('A repository and existing Actions token are required')
    request = urllib.request.Request(f'https://api.github.com/repos/{repository}/{endpoint}', headers={
        'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'Heraldry-README-updater'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except (urllib.error.URLError, ValueError) as exc:
        # Do not expose a token, request object or response body in logs.
        raise RuntimeError('Could not confirm publication status through GitHub; README publication deferred') from None


def publication_busy(repository, token, api=api_json):
    for workflow in PUBLICATION_WORKFLOWS:
        # Enumerate active states separately so older waiting runs are not hidden by completed runs.
        for status in ('queued', 'in_progress', 'pending', 'waiting', 'requested'):
            data = api(repository, f'actions/workflows/{workflow}/runs?branch=main&status={status}&per_page=1', token)
            if data['total_count']:
                return True
    return False


def publication_trigger(root, event):
    before, after = event.get('before'), event.get('after')
    if not before or not after or before == '0' * 40:
        return False
    if not all(re.fullmatch(r'[0-9a-f]{40}', sha) for sha in (before, after)):
        raise ValueError('Unrecognised push commit range')
    changed = git(root, 'diff', '--name-only', before, after).decode().splitlines()
    return bool(PUBLICATION_PATHS.intersection(changed))


def publish(root=ROOT, repository=None, token=None, event=None, busy=None, attempts=4):
    """Add README only atop current remote main; a race retries without checkout/reset/rebase."""
    root = Path(root)
    event = event or {}
    busy = busy or (lambda: publication_busy(repository, token))
    if attempts < 1:
        raise ValueError('At least one publication attempt is required')
    if publication_trigger(root, event) or busy():
        return 'DEFERRED: publication workflow will refresh README after completion'
    previous = None
    for attempt in range(attempts):
        git(root, 'fetch', 'origin', 'refs/heads/main:refs/remotes/origin/main')
        parent = git(root, 'rev-parse', 'refs/remotes/origin/main').decode().strip()
        if previous and publication_trigger(root, {'before': previous, 'after': parent}):
            return 'DEFERRED: publication inputs changed during README retry'
        previous = parent
        payload = render(root, parent)
        if payload == Snapshot(root, parent).read('README.md'):
            return 'UNCHANGED: README is current'
        if busy():
            return 'DEFERRED: publication workflow is queued or running'
        with tempfile.TemporaryDirectory(prefix='heraldry-readme-') as directory:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(directory)/'index'))
            git(root, 'read-tree', parent, env=env)
            blob = git(root, 'hash-object', '-w', '--stdin', data=payload).decode().strip()
            git(root, 'update-index', '--add', '--cacheinfo', f'100644,{blob},README.md', env=env)
            tree = git(root, 'write-tree', env=env).decode().strip()
        commit = git(root, 'commit-tree', tree, '-p', parent, data=(COMMIT_MESSAGE+'\n').encode()).decode().strip()
        if git(root, 'diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines() != ['README.md']:
            raise RuntimeError('README commit scope is not exactly README.md; nothing pushed')
        if busy():
            return 'DEFERRED: publication workflow started; no README push'
        result = subprocess.run(['git','push','origin',f'{commit}:refs/heads/main'],cwd=root,capture_output=True)
        if result.returncode == 0:
            return 'UPDATED: '+commit
        error = result.stderr.decode('utf-8',errors='replace').lower()
        if not any(word in error for word in ('non-fast-forward','fetch first','failed to update ref')):
            raise RuntimeError('README push refused; no history or working files changed')
        git(root, 'fetch', 'origin', 'refs/heads/main:refs/remotes/origin/main')
        if git(root, 'rev-parse', 'refs/remotes/origin/main').decode().strip() == parent:
            raise RuntimeError('README push refused without a competing main update; no retry')
    raise RuntimeError('README deferred after repeated main-update races; no history was rewritten')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','publish'):
        modes.add_argument('--'+mode,action='store_true')
    args = parser.parse_args()
    try:
        if args.publish:
            event_path = os.environ.get('GITHUB_EVENT_PATH')
            event = json.loads(Path(event_path).read_text()) if event_path else {}
            print(publish(repository=os.environ.get('GITHUB_REPOSITORY'), token=os.environ.get('GH_TOKEN'), event=event))
            return 0
        payload = render()
        current = (ROOT/'README.md').read_bytes()
        if args.check:
            if payload != current:
                print('README is stale: run python tools/update_readme.py --write',file=sys.stderr)
                return 1
            print('PASS: generated README sections are current')
        elif payload != current:
            (ROOT/'README.md').write_bytes(payload)
            print('Updated generated README sections')
        else:
            print('README already current')
        return 0
    except (OSError,ValueError,KeyError,RuntimeError) as exc:
        print('FAILED: '+str(exc),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
