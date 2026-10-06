#!/usr/bin/env python3
"""One-time GitHub Actions assisted import of the owner's exact reference PDFs."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'references/sample_pdfs.json'


def request_json(url, data, headers):
    raw = json.dumps(data).encode()
    req = urllib.request.Request(url, raw, headers, method='POST')
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.load(response)


def batch(operation, files):
    repo = os.environ['GITHUB_REPOSITORY']
    token = os.environ['GH_TOKEN']
    auth = base64.b64encode(('x-access-token:' + token).encode()).decode()
    return request_json('https://github.com/' + repo + '.git/info/lfs/objects/batch',
                        {'operation': operation, 'transfers': ['basic'],
                         'objects': [{'oid': f['sha256'], 'size': f['bytes']} for f in files]},
                        {'Authorization': 'Basic ' + auth,
                         'Accept': 'application/vnd.git-lfs+json',
                         'Content-Type': 'application/vnd.git-lfs+json'})['objects']


def prepare(output):
    catalog = json.loads(CATALOG.read_text())
    token = os.environ['GH_TOKEN']
    req = urllib.request.Request('https://api.github.com/repos/' + os.environ['GITHUB_REPOSITORY'],
                                 headers={'Authorization': 'Bearer ' + token,
                                          'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        if not json.load(response)['private']:
            raise ValueError('This import is restricted to the existing private repository')
    objects = batch('upload', catalog['files'])
    by_oid = {o['oid']: o for o in objects}
    if len(by_oid) != len(catalog['files']):
        raise ValueError('Incomplete LFS upload batch')
    transfers = []
    for f in catalog['files']:
        obj = by_oid[f['sha256']]
        if obj.get('error'):
            raise ValueError('LFS upload rejected: ' + str(obj['error'].get('code')))
        if obj['size'] != f['bytes']:
            raise ValueError('LFS size mismatch')
        transfers.append({**f, 'actions': obj.get('actions', {})})
    # Export only delegated, object-specific actions, never the job credential.
    payload = json.dumps({'repository': os.environ['GITHUB_REPOSITORY'], 'files': transfers})
    basic = base64.b64encode(('x-access-token:' + token).encode()).decode()
    if token in payload or basic in payload:
        raise ValueError('Refusing to export a repository credential')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'upload-actions.json').write_text(payload)
    print(f'Prepared {len(transfers)} object-specific LFS transfer slots')


def finish(timeout):
    catalog = json.loads(CATALOG.read_text())
    files = catalog['files']
    deadline = time.monotonic() + timeout
    while True:
        objects = batch('download', files)
        by_oid = {o['oid']: o for o in objects}
        if all(not by_oid.get(f['sha256'], {}).get('error') and
               'download' in by_oid.get(f['sha256'], {}).get('actions', {}) for f in files):
            break
        if time.monotonic() >= deadline:
            raise TimeoutError('Reference upload did not finish; no PDF pointers committed')
        time.sleep(15)
    for f in files:
        action = by_oid[f['sha256']]['actions']['download']
        req = urllib.request.Request(action['href'], headers=action.get('header', {}))
        digest = hashlib.sha256()
        size = 0
        with urllib.request.urlopen(req, timeout=180) as response:
            while block := response.read(1024 * 1024):
                digest.update(block)
                size += len(block)
        if size != f['bytes'] or digest.hexdigest() != f['sha256']:
            raise ValueError('Stored reference differs from original: ' + f['filename'])
        print('Verified stored original: ' + f['filename'])
    # Take any unrelated main updates before writing; reject reference conflicts.
    base = os.environ['GITHUB_SHA']
    subprocess.run(['git', 'fetch', 'origin', 'main'], cwd=ROOT, check=True)
    changed = subprocess.check_output(['git', 'diff', '--name-only', base, 'origin/main', '--',
                                       'references/sample_pdfs.json', 'references/private/pdfs',
                                       'references/import_lfs.py', '.gitattributes'], cwd=ROOT).strip()
    if changed:
        raise ValueError('Reference setup changed during transfer; objects retained, no stale commit')
    subprocess.run(['git', 'pull', '--ff-only', 'origin', 'main'], cwd=ROOT, check=True)
    for f in files:
        dest = ROOT / f['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text('version https://git-lfs.github.com/spec/v1\n'
                        f"oid sha256:{f['sha256']}\nsize {f['bytes']}\n")
    catalog['status'] = 'uploaded_and_hash_verified'
    catalog['verification'] = 'All 22 original objects downloaded from GitHub LFS and verified by SHA256 and byte count before committing pointers'
    CATALOG.write_text(json.dumps(catalog, indent=2) + '\n')
    subprocess.run(['git', 'add', '-f', 'references/private/pdfs'], cwd=ROOT, check=True)
    subprocess.run(['git', 'add', 'references/sample_pdfs.json'], cwd=ROOT, check=True)
    subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], cwd=ROOT, check=True)
    subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', 'Add 22 hash-verified visual reference PDFs through Git LFS'], cwd=ROOT, check=True)
    env = dict(os.environ, GIT_LFS_SKIP_PUSH='1')  # objects were uploaded and verified already
    subprocess.run(['git', 'push', 'origin', 'HEAD:main'], cwd=ROOT, env=env, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['prepare', 'finish'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args()
    if args.mode == 'prepare':
        if args.output is None:
            parser.error('--output is required')
        prepare(args.output)
    else:
        finish(args.timeout)
