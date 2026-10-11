#!/usr/bin/env python3
"""Read-only capability and repository-contract preflight for the ChatGPT Work runner.

The image model's reference-upload ability cannot be tested by Python; this script reports it
UNVERIFIED unless a real image/reference smoke test was explicitly confirmed externally.
"""
import argparse, json, os, shutil, subprocess, sys, hashlib
from pathlib import Path
try:
    import PIL
except ImportError:
    PIL=None


def invoke(repo,*args,timeout=15):
    try:
        p=subprocess.run(args,cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
        return p.returncode,p.stdout.strip(),p.stderr.strip()
    except (OSError,subprocess.TimeoutExpired) as e:
        return 127,'',str(e)


def run(repo,mode='auto',smoke_file=None,require_installed=False):
    repo=Path(repo).resolve()
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
    if git:
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
    else:warnings.append('git unavailable')
    delivery='git_lfs' if git and lfs and remote_ok else 'bundle'
    if mode=='git_lfs' and delivery!='git_lfs':errors.append('Git LFS delivery requested but unavailable')
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
    return {'status':'READY' if not errors else 'BLOCKED','installed_skill':skill_version,
            'image_smoke_required':smoke!='OPERATOR_RECORDED_PASS',
            'delivery':delivery,'git':bool(git),'git_lfs':lfs,'origin_main_access':remote_ok,'image_and_reference_tool':smoke,'warnings':warnings,'errors':errors}


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',default='.')
    ap.add_argument('--mode',choices=['auto','git_lfs','bundle'],default='auto')
    ap.add_argument('--smoke-file')
    ap.add_argument('--require-installed',action='store_true',help='block production until v6 is deployed into the repository')
    a=ap.parse_args(argv);d=run(a.repo,a.mode,a.smoke_file,a.require_installed)
    print(json.dumps(d,indent=2))
    return int(d['status']!='READY')

if __name__=='__main__':sys.exit(main())
