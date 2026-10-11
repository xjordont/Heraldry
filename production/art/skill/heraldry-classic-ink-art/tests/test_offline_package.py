"""Offline Work input package: preflight without Git, helper and guard behaviour in a package folder."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import delivery_guard as dg
import heraldry_art as ha
import work_preflight as wp


def manifest_for(repo, ids, refs):
    files=[]
    for f in sorted(repo.rglob('*')):
        rel=f.relative_to(repo).as_posix()
        if f.is_file() and rel!='WORK_PACKAGE.json':
            b=f.read_bytes()
            files.append({'path':rel,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),
                          **({'mutable':'append_only'} if rel.endswith('RECEIPTS.jsonl') else {})})
    out=[]
    for r in refs:
        with Image.open(repo/r) as im:
            out.append({'path':r,'format':im.format,'px':[im.width,im.height]})
    return {'schema':1,'kind':'heraldry-work-input-package','source':{'repository':'xjordont/Heraldry','branch':'main','commit':'a'*40},
            'queue':{'path':'production/art/gpt/QUEUE.json','phase':'anchors','ids':ids},'references':out,'files':files}


class OfflinePackage(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.repo=Path(self.tmp.name)/'pkg'
        self.ref='assets/art/style/STYLE-REF-03-figure-spotblack.jpg'
        (self.repo/self.ref).parent.mkdir(parents=True)
        Image.new('RGB',(64,64),'white').save(self.repo/self.ref)
        prompt=self.repo/'production/art/gpt/prompts/ART-T.txt';prompt.parent.mkdir(parents=True)
        prompt.write_text('an ink drawing\n')
        (self.repo/'production/art/gpt/RECEIPTS.jsonl').write_text('{"id": "ART-OLD"}\n')
        item={'id':'ART-T','prompt':'production/art/gpt/prompts/ART-T.txt','prompt_sha256':hashlib.sha256(b'an ink drawing').hexdigest(),
              'references':[self.ref]}
        (self.repo/'production/art/gpt/QUEUE.json').write_text(json.dumps({'schema':2,'phase':'anchors','items':[item]}))
        self.write_manifest()

    def tearDown(self):self.tmp.cleanup()

    def write_manifest(self):
        (self.repo/'WORK_PACKAGE.json').write_text(json.dumps(manifest_for(self.repo,['ART-T'],[self.ref])))

    def test_package_is_detected_and_verified_without_git(self):
        d=wp.run(self.repo)
        self.assertEqual(d['status'],'READY',d)
        self.assertEqual((d['source']['kind'],d['delivery'],d['git'],d['origin_main_access'],d['git_lfs']),('offline_package','bundle',False,False,False))
        self.assertIn('NOT_ATTEMPTED',d['remote_access'])
        self.assertEqual(wp.run(self.repo,'git_lfs')['status'],'BLOCKED')

    def test_receipts_may_grow_but_not_be_rewritten(self):
        f=self.repo/'production/art/gpt/RECEIPTS.jsonl'
        f.write_text(f.read_text()+'{"id": "ART-T"}\n')
        self.assertEqual(wp.run(self.repo)['status'],'READY')
        f.write_text('{"id": "ART-NEW"}\n')
        self.assertIn('append-only',' '.join(wp.run(self.repo)['errors']))

    def test_changed_pointer_or_undecodable_reference_blocks(self):
        (self.repo/self.ref).write_bytes(b'version https://git-lfs.github.com/spec/v1\n')
        errors=' '.join(wp.run(self.repo)['errors'])
        self.assertIn('SHA-256 mismatch',errors)
        self.assertIn('LFS pointer',errors)

    def test_private_pdf_blocks(self):
        (self.repo/'references/private/pdfs').mkdir(parents=True)
        (self.repo/'references/private/pdfs/book.pdf').write_bytes(b'%PDF-1.4')
        self.assertIn('private reference material',' '.join(wp.run(self.repo)['errors']))

    def test_explicit_flag_without_manifest_blocks(self):
        (self.repo/'WORK_PACKAGE.json').unlink()
        self.assertEqual(wp.run(self.repo,offline_package=True)['status'],'BLOCKED')

    def test_guard_refuses_and_helper_ignores_an_enclosing_checkout(self):
        with self.assertRaisesRegex(dg.Error,'offline Work input package'):
            dg.validate(self.repo,need_remote=False)
        # Unzipped inside some other Git checkout: still not a checkout of its own.
        if subprocess.run(['git','init','-q',self.tmp.name],capture_output=True).returncode==0:
            self.assertFalse(ha.git_ok(self.repo))
            self.assertIsNotNone(ha.package_info(self.repo))

    def test_scratch_defaults_beside_the_package(self):
        import os
        from unittest import mock
        with mock.patch.dict(os.environ,{},clear=False):
            os.environ.pop('HERALDRY_SCRATCH',None)
            self.assertEqual(ha.scratch_dir(self.repo),self.repo.resolve().parent/'pkg_scratch')
            os.environ['HERALDRY_SCRATCH']=str(Path(self.tmp.name)/'elsewhere')
            self.assertEqual(ha.scratch_dir(self.repo).parent,Path(self.tmp.name)/'elsewhere'/'heraldry_art')

if __name__=='__main__':unittest.main()
