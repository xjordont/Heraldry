import sys, os, typst
ROOT='/home/user/Heraldry'
ids=sys.argv[1:]
ppi=int(os.environ.get('PPI','170'))
for fid in ids:
    t=f'#set page(width: auto, height: auto, margin: 8pt, fill: rgb("#FCFAF5"))\n#image("/figures/out/{fid}.svg")\n'
    p=f'{ROOT}/figures/src/test/{fid}.typ'
    open(p,'w').write(t)
    typst.compile(p, output=f'{ROOT}/figures/src/test/{fid}.png', root=ROOT, font_paths=[f'{ROOT}/fonts/static'], ppi=ppi)
    print('rendered',fid)
