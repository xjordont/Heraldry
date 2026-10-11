"""Adversarial tests for v6 artifact integrity, QA, and delivery guards."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from PIL import Image,ImageDraw
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import delivery_guard as dg
import fidelity_gate as fg
import style_audit as sa
import work_preflight as wp

class V6SecurityTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.repo=Path(self.tmp.name)/'repo';self.repo.mkdir()
        self.ref=self.repo/'assets/art/style/sample.png';self.ref.parent.mkdir(parents=True)
        Image.new('RGB',(80,80),'white').save(self.ref)
        self.incoming=self.repo/'assets/art/incoming/ART-TEST.png';self.incoming.parent.mkdir(parents=True)
        im=Image.new('RGB',(1024,1024),'white'); d=ImageDraw.Draw(im);d.rectangle((290,300,710,750),outline='black',width=5)
        im.save(self.incoming)
        self.prompt=self.repo/'production/art/gpt/prompts/ART-TEST.txt';self.prompt.parent.mkdir(parents=True)
        self.prompt.write_text('Example prompt\n',encoding='utf-8')
        self.item={'id':'ART-TEST','prompt':str(self.prompt.relative_to(self.repo)),
                   'prompt_sha256':hashlib.sha256(b'Example prompt').hexdigest(),
                   'references':[str(self.ref.relative_to(self.repo))],
                   'register':'scene','size':'1024x1024'}
        self.queue=self.repo/'production/art/gpt/QUEUE.json'
        self.queue.write_text(json.dumps({'schema':2,'items':[self.item]}))
        self.receipt={'id':'ART-TEST','prompt_sha256':self.item['prompt_sha256'],
                    'native_sha256':dg.sha_file(self.incoming),
                    'reference_shas':[dg.sha_file(self.ref)],
                    'qa_review':{k:{'pass':True,'evidence':'Inspected native art and final print preview'} for k in fg.CRITERIA},
                    'qa_failed_criteria':[],'qa_unresolved':[]}
        self.receipt_file=self.repo/'production/art/gpt/RECEIPTS.jsonl'
        self.dump()
    def tearDown(self):self.tmp.cleanup()
    def dump(self):self.receipt_file.write_text(json.dumps(self.receipt)+'\n')

    def test_receipt_valid(self):
        dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_image_modified_after_review_blocks_delivery(self):
        Image.new('RGB',(1024,1024),'black').save(self.incoming)
        with self.assertRaisesRegex(dg.Error,'changed after receipt'):
            dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_style_reference_modified_after_review_blocks(self):
        Image.new('RGB',(80,80),'black').save(self.ref)
        with self.assertRaisesRegex(dg.Error,'queued reference changed'):
            dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_prompt_sha_mismatch_blocks(self):
        self.receipt['prompt_sha256']='f'*64
        with self.assertRaisesRegex(dg.Error,'prompt SHA256'):
            dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_incomplete_review_blocks(self):
        self.receipt['qa_review']['style_reference_match']['evidence']='great'
        with self.assertRaisesRegex(dg.Error,'meaningful review evidence'):
            dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_flags_disagree_blocks(self):
        self.receipt['qa_review']['subject_and_source']['pass']=False
        with self.assertRaisesRegex(dg.Error,'failed-criteria list'):
            dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_unresolved_unflagged_blocks(self):
        self.receipt['qa_unresolved']=['unresolved detail']
        with self.assertRaisesRegex(dg.Error,'unresolved QA'):
            dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_native_dimensions_exception_required(self):
        im=Image.new('RGB',(1020,1024),'white'); im.save(self.incoming)
        self.receipt['native_sha256']=dg.sha_file(self.incoming)
        with self.assertRaisesRegex(dg.Error,'native dimensions'):
            dg.check_receipt(self.item,self.incoming,self.receipt)
        self.receipt['accepted_flags']=True
        dg.check_receipt(self.item,self.incoming,self.receipt)
    def test_qa_requires_print_size_attestation(self):
        file=Path(self.tmp.name)/'qa.json'
        fg.create(self.item['id'],self.incoming,self.item['prompt_sha256'],[str(self.ref)],file)
        rec=json.loads(file.read_text());rec['prompt_unchanged']=True;rec['references_attached']=True
        rec['register_compared']='scene'
        for k in fg.CRITERIA:rec['checks'][k]={'pass':True,'evidence':'Actual features inspected at print size'}
        self.assertTrue(any('print-size' in e for e in fg.verify_record(rec,self.incoming,self.item)))
        rec['visual_review_at_print_size']=True
        self.assertEqual(fg.verify_record(rec,self.incoming,self.item),[])
    def test_advisory_style_diagnostics_four_edges(self):
        sig=fg.diagnostics(self.incoming,[])['candidate']
        self.assertEqual(set(sig['edge_ink_by_side']),{'top','bottom','left','right'})
        self.assertEqual(sig['edge_to_inner_ratio'],0)
        report=sa.build(self.repo)
        self.assertEqual(report['total_saved_checked'],1)
        self.assertEqual(report['by_register']['scene'],1)
    def test_work_preflight_requires_deployed_v6(self):
        out=wp.run(self.repo,require_installed=True)
        self.assertEqual(out['status'],'BLOCKED')
        self.assertIn('not installed',out['errors'][0])
    def test_receipt_duplicate_last_wins(self):
        invalid=dict(self.receipt,native_sha256='0'*64)
        self.receipt_file.write_text(json.dumps(invalid)+'\n'+json.dumps(self.receipt)+'\n')
        self.assertEqual(dg.latest_receipts(self.receipt_file)['ART-TEST']['native_sha256'],self.receipt['native_sha256'])
    def test_refused_receipt_blocks_image(self):
        self.receipt['refused']=True
        with self.assertRaisesRegex(dg.Error,'non-refusal'):
            dg.check_receipt(self.item,self.incoming,self.receipt)

if __name__=='__main__':unittest.main()
