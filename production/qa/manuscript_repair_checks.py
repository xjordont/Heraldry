#!/usr/bin/env python3
"""Verify immutable RC487 repairs, intentional prices, and complete base mappings."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from manuscript import check
from parse_source import parse,plain

def tables(text):
    result=[]
    def walk(bs):
        for b in bs:
            if b['type']=='table':result.append(([plain(c) for c in b['header']],[[plain(c) for c in r] for r in b['rows']]))
            walk(b.get('blocks',[]))
            for item in b.get('items',[]):walk(item['blocks'])
    walk(parse(text))
    return result

def run():
    authority=check(ROOT)
    registry=json.loads((ROOT/'source/versions.json').read_text())
    a=(ROOT/'source/Heraldry_RC486.md').read_text();b=(ROOT/'source/Heraldry_RC487.md').read_text()
    batch=json.loads((ROOT/'editorial/history/RC487.json').read_text())
    rebuilt=a
    for p in batch['patches']:
        assert p['status']=='approved' and rebuilt.count(p['find'])==p['expected_count'],p['id']
        rebuilt=rebuilt.replace(p['find'],p['replace'])
    rebuilt=rebuilt.replace('**Release Candidate 486 (RC486)**','**Release Candidate 487 (RC487)**')
    assert rebuilt==b
    old,new=tables(a),tables(b)
    def prices(ts):
        return [(ti,ri,col,r[ci]) for ti,(h,rs) in enumerate(ts) for ci,col in enumerate(h)
                if col in ('Cost (c)','Value (c)') for ri,r in enumerate(rs)]
    pa,pb=prices(old),prices(new);assert pa==pb
    base={}; specials=[]
    for h,rs in new:
        if h[0]=='Weapon' and 'Hands' in h:
            for r in rs:base[r[0]]=dict(zip(h,r))
        if h==['d10','Name','Cost (c)','Damage','Traits','Rule']:specials+=rs
    mappings=[]
    for r in specials:
        name=r[1];par=re.search(r'\(([^)]*)\)$',name)
        if par:
            mundane=par[1];mundane='Dagger' if mundane=='Dual Daggers' else mundane
        else:
            hits=[n for n in base if name.lower().endswith(n.lower())]
            mundane=max(hits,key=len) if hits else 'War Maul' if name.endswith('Maul') else None
        assert mundane in base,(name,mundane)
        inherited={k:v for k,v in base[mundane].items() if k in ('Hands','Range','STR Req','DEX Req')}
        if 'Thrown' in r[4] and 'Range' not in inherited:inherited['Range']='6" (existing Thrown default)'
        assert 'Ranged' not in r[4] or 'Range' in inherited,name
        mappings.append({'name':name,'mundane':mundane,'inherited':inherited,'pair':'Dual Daggers' in name})
    assert len(mappings)==50
    history=[]
    for rev in registry['revisions']:
        data=(ROOT/rev['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==rev['sha256']
        history.append({'revision':rev['number'],'sha256':rev['sha256'],'status':'PASS'})
    return {'schema':1,'status':'PASS','source_sha256':hashlib.sha256(b.encode()).hexdigest(),
      'active_revision':authority['number'],'exact_archived_patch_reconstruction':'PASS',
      'printed_finished_price_cells_preserved':len(pa),'tables_before':len(old),'tables_after':len(new),
      'special_weapon_base_mappings':mappings,'immutable_snapshots':history,
      'limits':'These checks verify preservation, exact authorized edits, and available base profiles; human review resolves rules meaning. They do not simulate gameplay or certify future revisions.'}

if __name__=='__main__':
    result=run();(ROOT/'production/qa/manuscript-repair-verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('special_weapon_base_mappings','immutable_snapshots')}))
