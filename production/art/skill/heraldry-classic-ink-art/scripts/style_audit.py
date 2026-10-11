#!/usr/bin/env python3
"""V6 advisory batch drift report. No automated aesthetic approval.

Read queued saved images, compare only within the same visual register, detect
exact duplicates and obvious cross-image/edge anomalies. Writes JSON only to a
path outside the repository. Must accompany, never replace, visual contact sheets.
"""
import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path
from PIL import Image, ImageOps

try:
    from fidelity_gate import diagnostics
except ImportError:
    from scripts.fidelity_gate import diagnostics

FORMATS = ('.png', '.jpg', '.jpeg', '.webp')

def record(repo, item):
    iid=item['id']
    files=[repo/'assets/art/incoming'/(iid+e) for e in FORMATS]
    found=[p for p in files if p.is_file()]
    if not found:
        return None
    if len(found)>1:
        raise ValueError(f'multiple native formats for {iid}')
    src=found[0]
    with Image.open(src) as im:
        im.verify()
    d=diagnostics(src, [])['candidate']
    return {'id':iid,'register':item.get('register','unspecified'),
            'size':item.get('size'),'source':src.relative_to(repo).as_posix(),
            'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'signature':d,'advisories':[]}

def build(repo, limit=10):
    repo=Path(repo).resolve()
    q=json.loads((repo/'production/art/gpt/QUEUE.json').read_text(encoding='utf-8'))
    rows=[record(repo,it) for it in q['items']]
    rows=[r for r in rows if r is not None][:limit]
    groups={}
    for r in rows:
        groups.setdefault(r['register'],[]).append(r)
        e=r['signature'].get('edge_ink_by_side',{})
        # Advisories only: scene vignette may intentionally include sparse fragments.
        if r['register']=='scene' and any(v>.09 for v in e.values()):
            r['advisories'].append('Substantial ink reaches one or more outer edges: inspect four-side vignette.')
        if r['register']!='scene' and any(v>.025 for v in e.values()):
            r['advisories'].append('Isolated illustration approaches a canvas boundary: inspect crop.')
    for group in groups.values():
        if len(group)<3: continue
        for field,maximum in [('ink_occupancy',.18),('deep_black',.11),('mid_gray',.22)]:
            baseline=statistics.median(r['signature'][field] for r in group)
            for r in group:
                if abs(r['signature'][field]-baseline)>maximum:
                    r['advisories'].append(f'Possible within-register {field} outlier: check side-by-side; material or scene can justify difference.')
    seen={}
    for r in rows:
        if r['sha256'] in seen:
            r['advisories'].append('Exact duplicate of '+seen[r['sha256']]+': investigate subject mixup.')
        seen[r['sha256']]=r['id']
    return {'schema':1,'purpose':'ADVISORY, not artistic approval',
            'total_saved_checked':len(rows),'by_register':{k:len(v) for k,v in groups.items()},
            'items':rows,'warnings':[{'id':r['id'],'advisory':a} for r in rows for a in r['advisories']]}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',default='.')
    ap.add_argument('--limit',type=int,default=10)
    ap.add_argument('--out',required=True)
    args=ap.parse_args(argv)
    repo=Path(args.repo).resolve();out=Path(args.out).resolve()
    if args.limit<1 or out==repo or repo in out.parents:
        ap.error('positive --limit and an --out path outside the repository required')
    try:
        report=build(repo,args.limit)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    except (ValueError,OSError,KeyError) as e:
        print('ERROR: '+str(e),file=sys.stderr);return 2
    print(json.dumps({'report':str(out),'images':report['total_saved_checked'],
                      'advisories':len(report['warnings'])},indent=2))
    return 0

if __name__=='__main__':sys.exit(main())
