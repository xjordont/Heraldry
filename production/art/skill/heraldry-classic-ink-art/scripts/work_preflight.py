#!/usr/bin/env python3
"""Read-only capability and repository-contract preflight for the ChatGPT Work runner.

The image model's reference-upload ability cannot be tested by Python; this script reports it
UNVERIFIED unless a real image/reference smoke test was explicitly confirmed externally.

Two sources are supported. A Git checkout is checked as before (git, Git LFS, origin/main access).
An offline Work input package (a folder unzipped from tools/art_work_package.py, carrying
WORK_PACKAGE.json and no .git) is checked against its own manifest instead: every file hash, the
queue and prompt hashes, and that every queue reference is a decodable image. Git is never run in
package mode, remote access is reported as not attempted, and delivery is always the bundle.
"""
import argparse, json, os, shutil, subprocess, sys, hashlib
from pathlib import Path
try:
    import PIL
    from PIL import Image
except ImportError:
    PIL=None

PACKAGE_MANIFEST='WORK_PACKAGE.json'
PACKAGE_KIND='heraldry-work-input-package'
LFS_MAGIC=b'version https://git-lfs'


def invoke(repo,*args,timeout=15):
    try:
        p=subprocess.run(args,cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
        return p.returncode,p.stdout.strip(),p.stderr.strip()
    except (OSError,subprocess.TimeoutExpired) as e:
        return 127,'',str(e)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def is_package(repo):
    """An unzipped offline Work input package: its manifest at the root and no Git checkout."""
    return (repo/PACKAGE_MANIFEST).is_file() and not (repo/'.git').exists()


def decode_image(path):
    """(format, [w, h]) of a fully decodable image, or raise. LFS pointers and truncated files fail."""
    data=path.read_bytes()
    if data[:len(LFS_MAGIC)]==LFS_MAGIC:
        raise ValueError('Git LFS pointer, not image bytes')
    with Image.open(path) as im:
        im.verify()
    with Image.open(path) as im:
        im.load()
        return im.format, [im.width, im.height]


def check_package(repo):
    """Verify an offline package against WORK_PACKAGE.json. Returns (source, errors, warnings)."""
    errors=[];warnings=[]
    try:
        man=json.loads((repo/PACKAGE_MANIFEST).read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:
        return {}, ['unreadable '+PACKAGE_MANIFEST+': '+str(e)], warnings
    if not isinstance(man,dict) or man.get('schema')!=1 or man.get('kind')!=PACKAGE_KIND:
        return {}, [PACKAGE_MANIFEST+' is not a schema-1 Heraldry Work input package manifest'], warnings
    src=man.get('source') or {}
    source={'kind':'offline_package','repository':src.get('repository'),'commit':src.get('commit'),
            'phase':(man.get('queue') or {}).get('phase'),'manifest_sha256':sha_bytes((repo/PACKAGE_MANIFEST).read_bytes())}
    if not isinstance(src.get('commit'),str) or len(src.get('commit',''))!=40:
        errors.append('package manifest lacks the 40-character source commit SHA')
    listed={}
    for rec in man.get('files') or []:
        rel=rec.get('path','')
        if not rel or rel.startswith('/') or '..' in Path(rel).parts:
            errors.append('unsafe path in package manifest: '+repr(rel));continue
        listed[rel]=rec
        f=repo/rel
        if f.is_symlink() or not f.is_file():
            errors.append('package file missing: '+rel);continue
        data=f.read_bytes()
        if rec.get('mutable')=='append_only':
            # Receipts grow as Work saves images; the packaged lines must stay unchanged at the front.
            if len(data)<rec.get('bytes',0) or sha_bytes(data[:rec.get('bytes',0)])!=rec.get('sha256'):
                errors.append('package file changed (append-only file was rewritten): '+rel)
        elif len(data)!=rec.get('bytes') or sha_bytes(data)!=rec.get('sha256'):
            errors.append('package file changed or corrupt (SHA-256 mismatch): '+rel)
    qrec=man.get('queue') or {}
    if qrec.get('path')!='production/art/gpt/QUEUE.json' or qrec.get('path') not in listed:
        errors.append('package manifest does not list production/art/gpt/QUEUE.json')
    refs={r.get('path'):r for r in man.get('references') or []}
    try:
        data=json.loads((repo/'production/art/gpt/QUEUE.json').read_text(encoding='utf-8'))
        ids=[it['id'] for it in data['items']]
        if qrec.get('ids')!=ids:errors.append('package manifest item IDs differ from QUEUE.json')
        for it in data['items']:
            if it['prompt'] not in listed:errors.append('prompt not listed in package manifest: '+it['prompt'])
            for ref in it['references']:
                if ref not in listed:errors.append('queue reference not packaged: '+ref);continue
                f=repo/ref
                if not f.is_file():continue
                try:
                    fmt,px=decode_image(f)
                except Exception as e:
                    errors.append(f'queue reference does not decode as an image: {ref} ({e})');continue
                want=refs.get(ref) or {}
                if want.get('format')!=fmt or want.get('px')!=px:
                    errors.append(f'reference format/size differs from the package manifest: {ref}')
    except (OSError,ValueError,KeyError,TypeError) as e:
        errors.append('Bad queue: '+str(e))
    # The package must never carry private reference PDFs or other books.
    for f in repo.rglob('*'):
        rel=f.relative_to(repo).as_posix()
        if f.is_file() and (f.suffix.lower()=='.pdf' or rel.startswith('references/private/')):
            errors.append('private reference material must not be in a Work package: '+rel)
    return source, errors, warnings


def run(repo,mode='auto',smoke_file=None,require_installed=False,offline_package=False):
    repo=Path(repo).resolve()
    package=offline_package or is_package(repo)
    if offline_package and not (repo/PACKAGE_MANIFEST).is_file():
        return {'status':'BLOCKED','source':{'kind':'offline_package'},'errors':['--offline-package given but '+PACKAGE_MANIFEST+' is not in '+str(repo)],'warnings':[]}
    q=repo/'production/art/gpt/QUEUE.json'
    installed=repo/'production/art/skill/heraldry-classic-ink-art/SKILL.md'
    skill_version='NOT_INSTALLED'
    if installed.is_file():
        skill_version='v6' if '(v6)' in installed.read_text(encoding='utf-8') else 'NOT_V6'
    if require_installed and skill_version!='v6':
        errors_preinstall=['Repository v6 skill not installed; upgrade before autonomous production']
    else:
        errors_preinstall=[]
    errors=list(errors_preinstall);warnings=[]
    python_ok=sys.version_info>=(3,9)
    if not python_ok:errors.append('Python 3.9+ required')
    if PIL is None:errors.append('Pillow missing')
    if not q.is_file():errors.append('Missing queue: must run in a Heraldry repository checkout')
    try:
        data=json.loads(q.read_text())
        if data['schema']<2:errors.append('Queue schema must be 2+')
        for it in data['items']:
            p=repo/it['prompt']
            if not p.is_file():errors.append('missing prompt: '+it['prompt']);continue
            b=p.read_text().removesuffix('\n').encode()
            if hashlib.sha256(b).hexdigest()!=it['prompt_sha256']:errors.append('prompt hash mismatch: '+it['id'])
            for ref in it['references']:
                f=repo/ref
                if not f.is_file():errors.append('missing reference: '+ref)
                elif f.read_bytes()[:32].startswith(b'version https://git-lfs'):errors.append('LFS pointer, fetch before generation: '+ref)
    except (OSError,ValueError,KeyError,TypeError) as e:errors.append('Bad queue: '+str(e))
    git=shutil.which('git');lfs=False;remote_ok=False
    source={'kind':'git_checkout'}
    if package:
        # Offline package: never run git, never contact a remote, never imply a push is possible.
        source,perr,pwarn=check_package(repo)
        errors+=perr;warnings+=pwarn
        if (repo/'.git').exists():warnings.append('a .git entry exists beside WORK_PACKAGE.json; package mode still delivers by bundle only')
        delivery='bundle'
        if mode=='git_lfs':errors.append('Git LFS delivery requested, but an offline Work package has no Git checkout or remote credentials')
        git_used=False
    if not package and git:
        rc,_,_=invoke(repo,git,'lfs','version');lfs=(rc==0)
        r,branch,_=invoke(repo,git,'branch','--show-current')
        if r or branch!='main':warnings.append('Not on main; existing repository direct-push contract requires main')
        r,remote,err=invoke(repo,git,'remote','get-url','origin')
        if r: warnings.append('No origin remote configured')
        else:
            r,_,err=invoke(repo,git,'ls-remote','--exit-code','origin','refs/heads/main',timeout=20)
            remote_ok=(r==0)
            if not remote_ok:warnings.append('origin/main could not be read using current credentials: '+err[:200])
        if not lfs:warnings.append('git-lfs unavailable')
        rc,out,_=invoke(repo,git,'check-attr','filter','--','assets/art/incoming/ART-TEST.png')
        if rc or not out.endswith(': lfs'):warnings.append('Incoming PNGs are not configured for LFS')
    elif not package:warnings.append('git unavailable')
    if not package:
        delivery='git_lfs' if git and lfs and remote_ok else 'bundle'
        if mode=='git_lfs' and delivery!='git_lfs':errors.append('Git LFS delivery requested but unavailable')
        git_used=bool(git)
    smoke='UNVERIFIED'
    if smoke_file:
        p=Path(smoke_file)
        if p.is_file():
            try:
                data=json.loads(p.read_text())
                if data.get('image_generated') is True and data.get('all_queue_references_attached') is True and data.get('native_file_accessible') is True:
                    smoke='OPERATOR_RECORDED_PASS'
                else:errors.append('smoke test record does not attest all 3 capabilities')
            except Exception as e:errors.append('invalid smoke test record: '+str(e))
        else:errors.append('smoke test record not found')
    out={'status':'READY' if not errors else 'BLOCKED','source':source,'installed_skill':skill_version,
            'image_smoke_required':smoke!='OPERATOR_RECORDED_PASS',
            'delivery':delivery,'git':git_used,'git_lfs':lfs,'origin_main_access':remote_ok,'image_and_reference_tool':smoke,'warnings':warnings,'errors':errors}
    if package:
        out['remote_access']='NOT_ATTEMPTED (offline package: no Git credentials are used or needed; nothing can be pushed from here)'
        out['git_lfs']=False
    return out


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',default='.')
    ap.add_argument('--mode',choices=['auto','git_lfs','bundle'],default='auto')
    ap.add_argument('--smoke-file')
    ap.add_argument('--require-installed',action='store_true',help='block production until v6 is deployed into the repository')
    ap.add_argument('--offline-package',action='store_true',help='validate an unzipped Work input package (WORK_PACKAGE.json) without Git; '
                    'chosen automatically when the manifest is present and there is no .git')
    a=ap.parse_args(argv);d=run(a.repo,a.mode,a.smoke_file,a.require_installed,a.offline_package)
    print(json.dumps(d,indent=2))
    return int(d['status']!='READY')

if __name__=='__main__':sys.exit(main())
