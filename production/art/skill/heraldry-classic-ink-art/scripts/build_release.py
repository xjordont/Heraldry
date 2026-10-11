#!/usr/bin/env python3
"""Build deterministic root-of-ZIP skill package with SHA256 inventory. Run outside GitHub production loop."""
import hashlib,json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/(ROOT.name+'.zip')
FILES=sorted((p for p in ROOT.rglob('*') if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts and p.suffix != '.pyc'),key=lambda p:p.relative_to(ROOT).as_posix())
manifest={
  'skill':'heraldry-classic-ink-art','version':'7.0.0',
  'repo_contract':{'queue_schema':2,'queue':'production/art/gpt/QUEUE.json','receipts':'production/art/gpt/RECEIPTS.jsonl', 'images':'assets/art/incoming/<ID>.png|jpg|webp','min_python':'3.9'},
  'release_notes':'V7: gritty old-school art direction, per-family and per-monster-kind reference sets, a mixed first ten, per-image delivery with drift review every ten, version-free reference docs.',
  'files': {p.relative_to(ROOT).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in FILES},
}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
  for p in [*FILES,ROOT/'manifest.json']:
    rel=p.relative_to(ROOT).as_posix()
    zi=zipfile.ZipInfo(rel,date_time=(2026,10,10,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED
    zi.external_attr=0o644<<16
    z.writestr(zi,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=7)
print(OUT,len(FILES)+1,OUT.stat().st_size)
