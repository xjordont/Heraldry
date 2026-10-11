"""Offline v6 regression suite: validates QA fidelity, failure gates, and capability fallbacks.
Not a test of actual image-model art quality, Git LFS transport, or remote intake.
"""
import hashlib, importlib.util, json, sys, tempfile, unittest
from unittest import mock
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import fidelity_gate as fg
import work_preflight as wp
import heraldry_art as ha
import delivery_guard as dg

class V6Test(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.p=Path(self.tmp.name)
        self.repo=self.p/'repo';self.repo.mkdir()
        self.ref=self.repo/'assets/art/style/STYLE-REF-03-figure-spotblack.jpg';self.ref.parent.mkdir(parents=True)
        Image.new('RGB',(1024,1024),'white').save(self.ref)
        self.native=self.p/'candidate.png'
        im=Image.new('RGB',(1024,1024),'white');im.save(self.native)
        self.it={'id':'ART-MON-TEST','prompt_sha256':'a'*64,'references':['assets/art/style/STYLE-REF-03-figure-spotblack.jpg'],'size':'1024x1024','register':'creature'}

    def tearDown(self):self.tmp.cleanup()

    def report(self):
        q=self.p/'review.json'
        fg.create(self.it['id'],str(self.native),self.it['prompt_sha256'],[str(self.ref)],q)
        report=json.loads(q.read_text())
        report['prompt_unchanged']=True
        report['references_attached']=True
        report['visual_review_at_print_size']=True
        report['register_compared']='creature'
        for k in fg.CRITERIA:
            report['checks'][k]={'pass':True,'evidence':'Inspected actual candidate and print proof: '+k}
        q.write_text(json.dumps(report))
        return q,report

    def test_qa_accept_and_hashes(self):
        q,r=self.report()
        self.assertEqual(fg.verify_record(json.loads(q.read_text()),self.native,self.it),[])
        self.assertEqual(len(r['checks']),10)
        self.assertEqual(r['image_sha256'],fg.digest(self.native))

    def test_qa_reject_modified_candidate(self):
        q,r=self.report()
        Image.new('RGB',(1024,1024),'black').save(self.native)
        self.assertTrue(any('image SHA256 mismatch' in x for x in fg.verify_record(r,self.native,self.it)))

    def test_qa_reject_missing_style_visual_evidence(self):
        q,r=self.report()
        r['checks']['style_reference_match']['evidence']='nice'
        self.assertTrue(any('style_reference_match' in x for x in fg.verify_record(r,self.native,self.it)))
        r['checks']['style_reference_match']['evidence']='Compared hatch direction against the single reference.'
        r['checks']['style_reference_match']['pass']=False
        self.assertTrue(any('visual hard failure' in x for x in fg.verify_record(r,self.native,self.it)))
        self.assertEqual(fg.verify_record(r,self.native,self.it,require_pass=False),[])

    def test_qa_reject_wrong_reference_even_matching_count(self):
        q,r=self.report()
        r['references_used'][0]['path']=str(self.native)
        r['references_used'][0]['sha256']=fg.digest(self.native)
        self.assertTrue(any('wrong reference' in x for x in fg.verify_record(r,self.native,self.it)))

    def test_qa_reject_partial_reference_attachments(self):
        q,r=self.report()
        r['references_attached']=False
        self.assertTrue(any('references not attested' in x for x in fg.verify_record(r,self.native,self.it)))
        r['references_attached']=True;r['references_used']=[]
        self.assertTrue(any('reference count mismatch' in x for x in fg.verify_record(r,self.native,self.it)))

    def test_exact_dimension_gate(self):
        m={'px':[1019,1024],'format':'PNG','colour':0,'nonpaper':.3,'sharpness':1000,'paper_tone':255,'paper_grain':0,'midtone':0,'edge2':0,'edge6':0,'intake_border_ink':0}
        failures,_,_=ha.evaluate(m,self.it)
        self.assertTrue(any('do not exactly match queue' in x for x in failures))
        m['px']=[1024,1024];failures,_,_=ha.evaluate(m,self.it)
        self.assertFalse(any('do not exactly match queue' in x for x in failures))

    def test_work_preflight_without_git_lfs_is_fallback(self):
        q=self.repo/'production/art/gpt/QUEUE.json';q.parent.mkdir(parents=True)
        prompt=self.repo/'production/art/gpt/prompts/test.txt';prompt.parent.mkdir(parents=True)
        prompt.write_text('an ink drawing\n')
        digest=hashlib.sha256(b'an ink drawing').hexdigest()
        q.write_text(json.dumps({'schema':2,'items':[{'id':self.it['id'],'prompt':str(prompt.relative_to(self.repo)),'prompt_sha256':digest,'references':self.it['references']}]}))
        d=wp.run(self.repo)
        self.assertEqual(d['status'],'READY')
        self.assertEqual(d['delivery'],'bundle')
        self.assertEqual(d['image_and_reference_tool'],'UNVERIFIED')
        self.assertEqual(wp.run(self.repo,'git_lfs')['status'],'BLOCKED')

    def test_delivery_guard_blocks_invalid_checkout(self):
        with self.assertRaises(dg.Error):dg.validate(self.repo,need_remote=False)

    def test_complete_qa_to_native_save_to_receipt(self):
        # Exercise the real v6 runner against a synthetic queue checkout; no network or image model.
        from PIL import ImageDraw
        prompt='Traditional monochrome ink adventurer portrait'
        pf=self.repo/'production/art/gpt/prompts/ART-MON-TEST.txt'
        pf.parent.mkdir(parents=True)
        pf.write_text(prompt+'\n')
        self.it['prompt_sha256']=hashlib.sha256(prompt.encode()).hexdigest()
        self.it.update({'prompt':str(pf.relative_to(self.repo)),'family':'monster','title':'Test',
                        'print_w_in':1.9,'max_attempts':3,'size_class':'Medium','must':[], 'avoid':[]})
        q=self.repo/'production/art/gpt/QUEUE.json';q.write_text(json.dumps({'schema':2,'phase':'anchors','count':1,
                          'generated_at':'2026-10-10T00:00:00+00:00','items':[self.it]}))
        im=Image.new('RGB',(1024,1024),'white');draw=ImageDraw.Draw(im)
        draw.ellipse((180,150,840,890),outline='black',width=18)
        for n in range(200,810,16): draw.line((n,350,n+35,690),fill='black',width=2)
        im.save(self.native)
        qfile,r=self.report()
        old=__import__('os').environ.get('HERALDRY_SCRATCH')
        __import__('os').environ['HERALDRY_SCRATCH']=str(self.p/'scratch')
        try:
            self.assertEqual(ha.main(['--repo',str(self.repo),'check',self.it['id'],str(self.native),'--json']),0)
            self.assertEqual(ha.main(['--repo',str(self.repo),'save',self.it['id'],str(self.native),'--qa-file',str(qfile)]),0)
        finally:
            if old is None:__import__('os').environ.pop('HERALDRY_SCRATCH',None)
            else:__import__('os').environ['HERALDRY_SCRATCH']=old
        saved=self.repo/'assets/art/incoming/ART-MON-TEST.png'
        self.assertEqual(saved.read_bytes(),self.native.read_bytes())
        rec=json.loads((self.repo/'production/art/gpt/RECEIPTS.jsonl').read_text().splitlines()[-1])
        self.assertEqual(rec['native_sha256'],fg.digest(self.native))
        self.assertEqual(len(rec['qa_review']),10)
        self.assertEqual(rec['qa_failed_criteria'],[])

    def _delivery_fixture(self):
        q=self.repo/'production/art/gpt/QUEUE.json';q.parent.mkdir(parents=True)
        pf=self.repo/'production/art/gpt/prompts/test.txt';pf.parent.mkdir(parents=True,exist_ok=True)
        pf.write_text('candidate test prompt\n')
        self.it['prompt']=str(pf.relative_to(self.repo))
        self.it['prompt_sha256']=hashlib.sha256(b'candidate test prompt').hexdigest()
        q.write_text(json.dumps({'schema':2,'items':[self.it]}))
        target=self.repo/'assets/art/incoming/ART-MON-TEST.png';target.parent.mkdir(parents=True)
        target.write_bytes(self.native.read_bytes())
        receipts=self.repo/'production/art/gpt/RECEIPTS.jsonl'
        receipt={'id':self.it['id'],'prompt_sha256':self.it['prompt_sha256'],'native_sha256':fg.digest(target),
                 'qa_review':{k:{'pass':True,'evidence':'Actual image inspected and detail verified'} for k in fg.CRITERIA},
                 'qa_failed_criteria':[], 'reference_shas':[fg.digest(self.ref)]}
        receipts.write_text(json.dumps(receipt)+'\n')
        return target,receipts

    def test_delivery_guard_allowlist_and_lfs_policy(self):
        target,receipts=self._delivery_fixture()
        def fake(repo,*args,check=True):
            if args[:3]==('diff','--cached','--name-only'):return ''
            if args[:2]==('branch','--show-current'):return 'main'
            if args[:2]==('lfs','version'):return 'git-lfs/3.0'
            if args[:3]==('status','--porcelain','--untracked-files=all'):
                return '?? assets/art/incoming/ART-MON-TEST.png\n M production/art/gpt/RECEIPTS.jsonl'
            if args[:2]==('check-attr','filter'):return 'assets/art/incoming/ART-MON-TEST.png: filter: lfs'
            if args[:2]==('ls-remote','--exit-code'):return 'a'*40+'\trefs/heads/main'
            raise AssertionError(args)
        with mock.patch.object(dg,'cmd',side_effect=fake):
            out=dg.validate(self.repo)
        self.assertEqual(out['images'],['assets/art/incoming/ART-MON-TEST.png'])
        self.assertEqual(out['remote_head'],'a'*40)

    def test_delivery_guard_blocks_remote_conflict_before_stage(self):
        self._delivery_fixture()
        check={'changed':['production/art/gpt/RECEIPTS.jsonl'],'images':[],'remote_head':'a'*40}
        commands=[]
        def fake(repo,*parts,check=True):
            commands.append(parts)
            if parts==('fetch','origin','main'):return ''
            if parts==('rev-parse','HEAD'):return 'a'*40
            if parts==('rev-parse','origin/main'):return 'b'*40
            raise AssertionError(parts)
        with mock.patch.object(dg,'validate',return_value=check),mock.patch.object(dg,'cmd',side_effect=fake):
            with self.assertRaisesRegex(dg.Error,'diverges'):dg.ship(self.repo)
        self.assertFalse(any(args[0] in ('add','commit','push') for args in commands))

    def test_original_reference_hashes_preserved(self):
        src=json.loads((ROOT/'references/images/SOURCES.json').read_text())
        for rec in src['images']:
            self.assertEqual(fg.digest(ROOT/rec['file']),rec['sha256'])

if __name__=='__main__':unittest.main()
