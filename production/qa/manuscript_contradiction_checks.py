#!/usr/bin/env python3
"""Reproduce bounded RC486 editorial checks; never mutate source or claim semantic PASS.

Run python tools/parse_source.py first. Findings are expected on RC486; exit 0
means evidence reproduced, not that the manuscript is free of contradictions.
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from manuscript import check
from parse_source import plain

def run(root=ROOT):
    audit=json.loads((root/'production/qa/manuscript-contradiction-audit.json').read_text())
    proposal=json.loads((root/'editorial/proposals/rc487-contradiction-audit.json').read_text())
    raw=(root/audit['source']['path']).read_bytes()
    txt=raw.decode('utf-8'); lines=txt.splitlines()
    assert hashlib.sha256(raw).hexdigest()==audit['source']['sha256']==proposal['source_sha256']
    assert len(raw)==audit['source']['bytes'] and len(lines)==audit['source']['lines']
    current=check(root)
    assert current['number']==486 and current['sha256']==audit['source']['sha256']
    registry=json.loads((root/'source/versions.json').read_text())
    history=[]
    prior=None
    for rev in registry['revisions']:
        data=(root/rev['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==rev['sha256'] and len(data)==rev['bytes']
        if prior:
            hist_raw=(root/rev['patch_file']).read_bytes()
            assert hashlib.sha256(hist_raw).hexdigest()==rev['patch_sha256']
            batch=json.loads(hist_raw)
            rebuilt=prior[1].decode('utf-8')
            for p in batch['patches']:
                assert rebuilt.count(p['find'])==p.get('expected_count',1)
                rebuilt=rebuilt.replace(p['find'],p['replace'])
            rebuilt=rebuilt.replace(f"**Release Candidate {prior[0]['number']} (RC{prior[0]['number']})**",f"**Release Candidate {rev['number']} (RC{rev['number']})**")
            assert rebuilt.encode('utf-8')==data
            history.append({'revision':rev['number'],'patch_ids':[p['id'] for p in batch['patches']],'exact_reconstruction':'PASS'})
        prior=(rev,data)
    table_blocks=[]
    def walk(bs):
        for b in bs:
            if b['type']=='table': table_blocks.append(b)
            walk(b.get('blocks',[]))
            for i in b.get('items',[]):walk(i['blocks'])
    model=json.loads((root/'build/blocks.json').read_text())
    for c in model['chapters']:walk(c['blocks'])
    tables=[dict(id=b['id'],header=[plain(c) for c in b['header']],rows=[[plain(c) for c in r] for r in b['rows']]) for b in table_blocks]
    base={}
    for t in tables:
        if t['header'][0] in ('Weapon','Armour','Shield') and 'Cost (c)' in t['header']:
            kind='weapon' if t['header'][0]=='Weapon' else 'armour'
            costidx=t['header'].index('Cost (c)')
            for row in t['rows']:
                if not row[costidx].isdigit():continue
                name=re.sub(r'\s*\([^)]*\)','',row[0]).strip()
                base[name]=(int(row[costidx]),kind)
    mult={'Masterwork':(1.5,3),'Silvered':(1.5,3),'Cold Iron':(1.5,3),
          'Elven':(2,5),'Sacred':(2,5),'Palesteel':(2,5),'Adamantine':(4,10)}
    addw={1:8,2:16,3:24,4:36,5:50}; adda={1:7,2:15,3:24,4:36,5:48}
    differences=[]; checked=0; unmapped=[]
    for t in tables:
        if t['header']!=['d20','Item','Value (c)']:continue
        for row in t['rows']:
            item=row[1]; cost=row[2]
            m=re.match(r'^(Masterwork|Silvered|Cold Iron|Elven|Sacred|Palesteel|Adamantine|Enchanted \+[1-5]) (.+)$',item)
            if not m:continue
            q,name=m.groups()
            if name not in base:
                unmapped.append({'table':t['id'],'item':item});continue
            assert cost.isdigit(),item
            b,kind=base[name]
            if q.startswith('Enchanted'):
                n=int(q[-1]); expected=b+(addw if kind=='weapon' else adda)[n]
            else:
                factor,minimum=mult[q]
                if q=='Adamantine' and kind=='armour':minimum=60
                expected=max(int(b*factor),minimum)
            checked+=1
            if int(cost)!=expected:
                differences.append({'table':t['id'],'item':item,'printed':int(cost),'computed':expected,'base':b,'kind':kind})
    assert not unmapped,unmapped
    die_tables=[];range_issues=[]
    for t in tables:
        m=re.fullmatch(r'd(\d+)',t['header'][0],re.I)
        if not m:continue
        size=int(m[1]); faces=[];valid=True
        for row in t['rows']:
            r=re.fullmatch(r'(\d+)(?:\s*[–—-]\s*(\d+))?',row[0])
            if not r:valid=False;break
            a=int(r[1]);b=int(r[2] or r[1])
            faces.extend(range(a,b+1))
        if not valid:continue
        count=Counter(faces);missing=[i for i in range(1,size+1) if not count[i]]
        repeated={i:n for i,n in count.items() if n>1};outside=[i for i in count if i<1 or i>size]
        die_tables.append(t['id'])
        if missing or repeated or outside:range_issues.append(dict(table=t['id'],missing=missing,repeated=repeated,outside=outside))
    evidence_count=0
    for record in audit['findings']+audit['uncertainties']:
        for ev in record['evidence']:
            for hit in ev['matches']:
                assert lines[hit['line']-1]==hit['text'],(record['id'],hit['line'])
                evidence_count+=1
    exact=[];candidate=txt
    for p in proposal['patches']:
        assert p['status']=='proposed'
        count=candidate.count(p['find'])
        assert count==p['expected_count'],(p['id'],count)
        candidate=candidate.replace(p['find'],p['replace'])
        exact.append({'id':p['id'],'matches':count,'status':'PASS'})
    # Check reported numerical evidence, not implementation-mirroring assertions
    # of an invented value list. The actual list is computed from manuscript costs.
    assert len(differences)==audit['counts']['enhanced_value_cells']
    assert len(audit['findings'])==audit['counts']['open_findings']
    assert len(exact)==audit['counts']['exact_proposed_patches']
    ragged=[t['id'] for t in tables if any(len(r)!=len(t['header']) for r in t['rows'])]
    return {'schema':1,'source_sha256':audit['source']['sha256'],
      'verification_status':'PASS','semantic_clearance':'OPEN_FINDINGS',
      'meaning':'PASS verifies bounded calculations, evidence anchors, proposed matches and immutable history; it does not clear the manuscript.',
      'history':history,'tables':{'count':len(tables),'cells':sum(len(t['header'])+sum(len(r) for r in t['rows']) for t in tables),'ragged':ragged},
      'enhanced_values':{'checked':checked,'unmapped':unmapped,'differences':differences},
      'direct_die_range_tables':{'checked':len(die_tables),'issues':range_issues,'scope':'Only direct dN-labelled tables whose first column is wholly numeric ranges; excludes narrative and multi-table outcome semantics.'},
      'evidence_anchors_checked':evidence_count,'proposed_patch_matches':exact,
      'original_source_unchanged': hashlib.sha256((root/audit['source']['path']).read_bytes()).hexdigest()==audit['source']['sha256']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=run()
    if args.output:args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('proposed_patch_matches','history','enhanced_values')},ensure_ascii=False))
    print(json.dumps({'enhanced_rows_checked':result['enhanced_values']['checked'],'enhanced_value_differences':len(result['enhanced_values']['differences'])}))
