#!/usr/bin/env python3
"""V6 guarded direct-main art delivery; read-only audit and explicit ship.

Requires a clean index, a non-divergent origin/main, queued incoming images, full
prompt- and native-byte-bound v6/v6 receipts, and Git LFS for PNG. Never force,
rebase, merge, change unrelated paths, or silently accept old receipts.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

ALLOWED_RECEIPTS = 'production/art/gpt/RECEIPTS.jsonl'
ALLOWED_IMAGE = re.compile(r'^assets/art/incoming/(ART-[A-Za-z0-9-]+)\.(png|jpg|jpeg|webp)$')
QA_CRITERIA = (
    'subject_and_source', 'required_details', 'prohibited_details',
    'anatomy_or_architecture', 'composition_and_scale', 'style_reference_match',
    'black_ink_and_paper', 'vignette_or_isolation', 'small_print_readability',
    'originality_no_reference_bleed'
)

class Error(Exception):
    pass


def cmd(repo, *parts, check=True):
    proc = subprocess.run(['git', *parts], cwd=repo, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, timeout=60)
    if check and proc.returncode:
        raise Error('git ' + ' '.join(parts) + ' failed: ' + proc.stderr.strip()[:350])
    return proc.stdout.strip()


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def latest_receipts(path):
    records = {}
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except (ValueError, TypeError) as e:
            raise Error(f'invalid JSONL receipt line {number}: {e}')
        if not isinstance(rec, dict) or not isinstance(rec.get('id'), str):
            raise Error(f'invalid receipt at line {number}')
        records[rec['id']] = rec
    return records


def check_receipt(item, path, rec):
    iid = item['id']
    if not rec or rec.get('refused') is True:
        raise Error(f'{iid}: image missing a non-refusal receipt')
    if rec.get('prompt_sha256') != item.get('prompt_sha256'):
        raise Error(f'{iid}: receipt does not match the queued prompt SHA256')
    if rec.get('native_sha256') != sha_file(path):
        raise Error(f'{iid}: native file changed after receipt; regenerate visual QA before delivery')
    q = rec.get('qa_review')
    if not isinstance(q, dict):
        raise Error(f'{iid}: no complete image-bound QA review in receipt')
    for key in QA_CRITERIA:
        v = q.get(key)
        if not isinstance(v, dict) or not isinstance(v.get('pass'), bool) or len(str(v.get('evidence', '')).strip()) < 15:
            raise Error(f'{iid}: missing meaningful review evidence for {key}')
    failed = {k for k in QA_CRITERIA if q[k]['pass'] is False}
    declared = rec.get('qa_failed_criteria')
    if not isinstance(declared, list) or set(declared) != failed or len(declared) != len(set(declared)):
        raise Error(f'{iid}: QA failed-criteria list does not match QA evidence')
    if failed and not rec.get('accepted_flags'):
        raise Error(f'{iid}: failed visual review without exhausted-budget exception')
    if rec.get('qa_unresolved') and not rec.get('accepted_flags'):
        raise Error(f'{iid}: unresolved QA issues cannot be shipped as a clean pass')
    expected_refs = item.get('references', [])
    shas = rec.get('reference_shas')
    if not isinstance(shas, list) or len(shas) != len(expected_refs) or not all(re.fullmatch(r'[0-9a-f]{64}', s or '') for s in shas):
        raise Error(f'{iid}: reference SHA evidence incomplete')
    # Verify queued prompt content and supplied references have not moved after review.
    for ref in expected_refs:
        source = path.parents[3] / ref # root from .../assets/art/incoming/ID.png
        if not source.is_file() or source.read_bytes()[:32].startswith(b'version https://git-lfs'):
            raise Error(f'{iid}: reference unavailable: {ref}')
    for ref, expected in zip(expected_refs, shas):
        if sha_file(path.parents[3] / ref) != expected:
            raise Error(f'{iid}: queued reference changed after QA: {ref}')
    with Image.open(path) as src:
        src.verify()
    with Image.open(path) as src:
        exact = f'{src.width}x{src.height}' == item.get('size')
        fmt = (src.format or '').lower()
    if fmt not in ('png', 'jpeg', 'webp'):
        raise Error(f'{iid}: unsupported encoded image format {fmt}')
    if path.suffix.lower() not in ('.'+fmt, '.jpg' if fmt=='jpeg' else '.invalid'):
        raise Error(f'{iid}: file extension does not match image contents')
    if not exact and not rec.get('accepted_flags'):
        raise Error(f'{iid}: native dimensions differ from queue without recorded exception')


def validate(repo, need_remote=True):
    repo = Path(repo).resolve()
    queue_file = repo/'production/art/gpt/QUEUE.json'
    if not queue_file.is_file():
        raise Error('not a Heraldry queue checkout')
    if cmd(repo, 'branch', '--show-current') != 'main':
        raise Error('not on main: current repo uses direct-main delivery')
    if not cmd(repo, 'lfs', 'version', check=False):
        raise Error('git lfs unavailable; use helper bundle fallback')
    if cmd(repo, 'diff', '--cached', '--name-only'):
        raise Error('index already contains staged files; inspect and clear it before v6 ship')
    q = json.loads(queue_file.read_text(encoding='utf-8'))
    if q.get('schema') != 2 or not isinstance(q.get('items'), list):
        raise Error('queue schema 2 required')
    known = {it['id']: it for it in q['items']}
    raw = cmd(repo, 'status', '--porcelain', '--untracked-files=all')
    changed = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        status, path = line[:2], line[3:].strip('"')
        if any(c in path for c in ('\r', '\n', '\0')) or ' -> ' in path or 'R' in status or 'C' in status or 'D' in status:
            raise Error('rename, deletion or malformed path not permitted: ' + path)
        match = ALLOWED_IMAGE.fullmatch(path)
        if path != ALLOWED_RECEIPTS and (not match or match.group(1) not in known):
            raise Error('unrelated or unqueued working-tree change: ' + path)
        if match:
            if path.endswith('.png') and not cmd(repo, 'check-attr', 'filter', '--', path).endswith(': lfs'):
                raise Error('PNG missing LFS filter: ' + path)
            img_path = repo/path
            if img_path.is_symlink() or not img_path.is_file():
                raise Error('incoming image missing or symlink: ' + path)
            with img_path.open('rb') as fh:
                if fh.read(40).startswith(b'version https://git-lfs'):
                    raise Error('incoming file is a Git LFS pointer: ' + path)
        changed.append(path)
    if not changed:
        raise Error('nothing to deliver')
    image_files = sorted({p for p in changed if ALLOWED_IMAGE.fullmatch(p)})
    if ALLOWED_RECEIPTS not in changed:
        raise Error('incoming batch has no new or changed receipts')
    receipts = repo/ALLOWED_RECEIPTS
    if not receipts.is_file() or receipts.is_symlink():
        raise Error('RECEIPTS.jsonl missing or symlink')
    entries = latest_receipts(receipts)
    seen = set()
    for rel in image_files:
        iid = ALLOWED_IMAGE.fullmatch(rel).group(1)
        if iid in seen:
            raise Error('multiple file formats present for one queued ID: ' + iid)
        seen.add(iid)
        check_receipt(known[iid], repo/rel, entries.get(iid))
        prompt = repo / known[iid]['prompt']
        if not prompt.is_file():
            raise Error(iid + ': queued prompt file missing')
        content = prompt.read_text(encoding='utf-8').removesuffix('\n')
        if hashlib.sha256(content.encode('utf-8')).hexdigest() != known[iid]['prompt_sha256']:
            raise Error(iid + ': queued prompt file has changed')
    remote = cmd(repo, 'ls-remote', '--exit-code', 'origin', 'refs/heads/main') if need_remote else ''
    if need_remote and not remote:
        raise Error('origin/main inaccessible')
    return {'changed': sorted(set(changed)), 'images': image_files,
            'remote_head': remote.split()[0] if remote else None,
            'receipts_checked': len(image_files)}


def ship(repo):
    repo = Path(repo).resolve()
    pre = validate(repo)
    cmd(repo, 'fetch', 'origin', 'main')
    head = cmd(repo, 'rev-parse', 'HEAD')
    upstream = cmd(repo, 'rev-parse', 'origin/main')
    if head != upstream or head != pre['remote_head']:
        raise Error('local HEAD diverges from origin/main; stop and ask maintainer to reconcile')
    allowed = pre['changed']
    cmd(repo, 'add', '--', *allowed)
    staged = cmd(repo, 'diff', '--cached', '--name-only').splitlines()
    if set(staged) != set(allowed):
        raise Error('staged paths do not exactly match allowlisted paths')
    for img in pre['images']:
        if img.endswith('.png'):
            if not cmd(repo, 'ls-files', '--stage', '--', img):
                raise Error('PNG not staged: ' + img)
            size = int(cmd(repo, 'cat-file', '-s', ':' + img))
            if size > 2048 or not cmd(repo, 'show', ':' + img).startswith('version https://git-lfs'):
                raise Error('PNG staged without Git LFS pointer: ' + img)
    remote = cmd(repo, 'ls-remote', '--exit-code', 'origin', 'refs/heads/main').split()[0]
    if remote != head:
        raise Error('origin/main advanced before commit; no push attempted')
    ids = [ALLOWED_IMAGE.fullmatch(x).group(1) for x in pre['images']]
    span = f'{ids[0]} .. {ids[-1]}' if ids else 'refusals'
    cmd(repo, 'commit', '-m', 'art(gpt): ' + span)
    cmd(repo, 'push', 'origin', 'main')  # fast-forward only; no force flags
    return {'status': 'PUSHED', 'commit': cmd(repo, 'rev-parse', 'HEAD'), 'images': pre['images']}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['audit', 'ship'])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--execute', action='store_true')
    a = ap.parse_args(argv)
    try:
        if a.command == 'ship' and not a.execute:
            raise Error('ship requires --execute; run audit and use bundle fallback if blocked')
        result = ship(a.repo) if a.command == 'ship' else validate(a.repo)
        print(json.dumps({'status':'PUSHED' if a.command == 'ship' else 'PASS', **result}, indent=2))
        return 0
    except (Error, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)}, indent=2), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
