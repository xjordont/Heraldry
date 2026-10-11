#!/usr/bin/env python3
"""Create and verify image-bound visual QA records with four-edge style diagnostics.

This is NOT an automated artistic judge: the diagnostics are advisory; a human or visual agent
must inspect the native image, the print-size preview, and the item's references. The QA record
binds those attestations to the exact image bytes, queue prompt hash and explicit references.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps, ImageStat
except ImportError:
    raise SystemExit('Pillow required: pip install pillow')

CRITERIA = (
    'subject_and_source', 'required_details', 'prohibited_details',
    'anatomy_or_architecture', 'composition_and_scale', 'style_reference_match',
    'black_ink_and_paper', 'vignette_or_isolation', 'small_print_readability',
    'originality_no_reference_bleed',
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def diagnostics(path, refs):
    """Comparative diagnostics. Numeric differences are not proof of artistic quality."""
    def signature(p):
        with Image.open(p) as src:
            src.load()
            rgb = src.convert('RGB')
        g = ImageOps.grayscale(rgb)
        w, h = rgb.size
        # Main area ignores the edge vignette and avoids penalizing deliberate blank paper.
        inner = g.crop((round(.1*w), round(.1*h), round(.9*w), round(.9*h)))
        j = inner.histogram()
        m = sum(j) or 1
        avg = ImageStat.Stat(inner).mean[0]
        rgb_sample = rgb.resize((min(w,512),min(h,512)))
        # approximate saturation from HSV, not a semantic or ink-fibre test
        sat = rgb_sample.convert('HSV').getchannel('S').histogram()
        # Four-side blank-paper and boundary diagnostics are independent of scene size.
        bw = g.point(lambda v: 255 if v < 180 else 0)
        def ink_ratio(region):
            cut = bw.crop(region)
            h0 = cut.histogram()
            return round(h0[255] / max(1, cut.width*cut.height), 4)
        dx=max(1,round(.025*w));dy=max(1,round(.025*h))
        edge_bands={
            'top': ink_ratio((0,0,w,dy)),
            'bottom':ink_ratio((0,h-dy,w,h)),
            'left':ink_ratio((0,0,dx,h)),
            'right':ink_ratio((w-dx,0,w,h)),
        }
        inset=max(1,round(.08*w));insy=max(1,round(.08*h))
        inner_ink=ink_ratio((inset,insy,w-inset,h-insy))
        outer_ink=sum(edge_bands.values())/4
        return {
            'px':[w,h],
            'ink_occupancy':round(sum(j[:200])/m,4),
            'deep_black':round(sum(j[:65])/m,4),
            'mid_gray':round(sum(j[90:210])/m,4),
            'central_mean_luma':round(avg,2),
            'edge_ink_by_side':edge_bands,
            'inner_ink':inner_ink,
            'mean_outer_ink':round(outer_ink,4),
            'edge_to_inner_ratio':round(outer_ink / max(.0001,inner_ink),3),
            'saturation_gt_60':round(sum(sat[61:])/sum(sat),4),
        }
    me=signature(path)
    others=[]
    for ref in refs:
        rf=Path(ref)
        if rf.is_file():
            others.append({'path':str(rf),'sha256':digest(rf),'signature':signature(rf)})
    return {'candidate':me,'references':others,
            'caution':'Style signatures are advisory only. Scene, figure, and still-life registers differ; visual inspection controls.'}


def create(id, image, prompt_sha, refs, out):
    image=Path(image)
    if not image.is_file():
        raise ValueError(f'missing image: {image}')
    d = {
       'schema':1,'id':id,'image_sha256':digest(image),'prompt_sha256':prompt_sha,
       'prompt_unchanged':False, 'references_attached':False,
       'references_used':[{'path':r,'sha256':digest(r)} for r in refs if Path(r).is_file()],
       'checks':{k:{'pass':None,'evidence':''} for k in CRITERIA},
       'style_diagnostics':diagnostics(image, refs),
       'unresolved_issues':[], 'operator_note':'',
       'visual_review_at_print_size':False, 'register_compared':'',
    }
    out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return d


def verify_record(record, image, item, require_pass=True):
    if not isinstance(record,dict):
        raise ValueError('QA report must be a JSON object')
    errors=[]
    if record.get('schema') != 1: errors.append('unsupported QA schema')
    if record.get('id') != item['id']: errors.append('QA item ID mismatch')
    if record.get('image_sha256') != digest(image): errors.append('QA image SHA256 mismatch: file changed after visual review')
    if record.get('prompt_sha256') != item['prompt_sha256']: errors.append('QA prompt SHA256 mismatch')
    if record.get('prompt_unchanged') is not True: errors.append('verbatim prompt not attested')
    if record.get('references_attached') is not True: errors.append('required references not attested')
    if record.get('visual_review_at_print_size') is not True: errors.append('print-size preview review not attested')
    if record.get('register_compared') not in ('scene','figure','still_life','portrait','creature','interior','other'):
        errors.append('comparison register not specified')
    refs=record.get('references_used',[])
    if not isinstance(refs,list):
        errors.append('references_used must be a list');refs=[]
    if len(refs)!=len(item.get('references',[])):
        errors.append(f"reference count mismatch: expected {len(item.get('references',[]))}, recorded {len(refs)}")
    if any(not isinstance(x,dict) for x in refs):errors.append('reference entries must be objects');refs=[x for x in refs if isinstance(x,dict)]
    if len({x.get('path') for x in refs})!=len(refs):errors.append('duplicate reference path in QA record')
    for i,r in enumerate(refs):
        p=Path(r.get('path',''))
        expected=item.get('references',[])[i] if i<len(item.get('references',[])) else ''
        # queue paths are POSIX; tolerate Windows separators on either side, on any platform
        expected=expected.replace('\\','/')
        got=str(r.get('path','')).replace('\\','/')
        if not (got==expected or got.endswith('/'+expected)):
            errors.append(f'wrong reference at position {i+1}: expected {expected}, got {p}')
        if not p.is_file() or digest(p)!=r.get('sha256'):
            errors.append(f"reference missing/changed: {r.get('path')}")
    checks=record.get('checks')
    if not isinstance(checks,dict):errors.append('missing checks');checks={}
    for k in CRITERIA:
        v=checks.get(k)
        if not isinstance(v,dict) or not isinstance(v.get('pass'),bool):
            errors.append(f'{k}: explicit pass/fail required')
        elif require_pass and not v['pass']:
            errors.append(f'{k}: visual hard failure')
        if not isinstance(v,dict) or len(str(v.get('evidence','')).strip())<15:
            errors.append(f'{k}: meaningful visual evidence required (at least 15 chars)')
    if not isinstance(record.get('unresolved_issues',[]),list):errors.append('unresolved issues must be a list')
    if require_pass and record.get('unresolved_issues'):
        errors.append('unresolved issues on a claimed passing image')
    return errors


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='cmd',required=True)
    cr=sub.add_parser('create');cr.add_argument('id');cr.add_argument('image');cr.add_argument('--prompt-sha',required=True);cr.add_argument('--reference',action='append',default=[]);cr.add_argument('--out',required=True)
    vr=sub.add_parser('verify');vr.add_argument('file');vr.add_argument('image');vr.add_argument('--item-json',required=True);vr.add_argument('--allow-fails',action='store_true')
    a=ap.parse_args(argv)
    try:
        if a.cmd=='create':
            create(a.id,a.image,a.prompt_sha,a.reference,a.out)
            print(f'Created DRAFT QA report at {a.out}. Inspect image and print proof, complete every criterion, then verify.')
        else:
            r=json.loads(Path(a.file).read_text(encoding="utf-8"));it=json.loads(Path(a.item_json).read_text(encoding="utf-8"))
            errors=verify_record(r,a.image,it,not a.allow_fails)
            print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2))
            return int(bool(errors))
    except (ValueError,OSError,KeyError) as e:
        print('ERROR:',e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(main())
