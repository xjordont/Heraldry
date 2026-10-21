"""Exercise source keep coverage and semantic layout, independently of PDF page numbers."""
from pathlib import Path
import json
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build_book import (Book, FRAME_FIT, FRAME_H, stabilize_balance, compute_balance, BODY_BOTTOM,
                        apply_table_scope_override, table_content_sha256, resolve_table_scope_policies,
                        TableScopePolicyError, save_converged_balance, segment_signature,
                        filtered_balance_plan)
from source_units import source_unit_manifest
from layout_profile import BODY_HEIGHT_PT


class LayoutEmitter(unittest.TestCase):
    def test_semantic_width_policy_remeasures_changed_source_cells(self):
        from copy import deepcopy
        from unittest.mock import patch
        text=lambda value:[{'t':'text','v':value}]
        table={'id':'TEST','header':[text('Roll'),text('Effect')],
               'rows':[[text('1'),text('A complete effect.')]]}
        policy={'scope':'full','reviewed_content_sha256':table_content_sha256(table),'reason':'Reviewed specimen',
                'selector':{'heading_path':['Equipment','Potions','Tier 1'], 'headers':['Roll','Effect']}}
        resolved, audit=resolve_table_scope_policies([(table,['7. Equipment','7.13 Potions','Tier 1'])],{'potions':policy})
        result=apply_table_scope_override(table,{'rep':'table','scope':'column'},resolved['TEST'])
        self.assertEqual(result['scope'],'full')
        self.assertEqual(audit[0]['status'],'matched')
        changed=deepcopy(table)
        changed['rows'][0][1]=text('A changed effect.')
        resolved, audit=resolve_table_scope_policies([(changed,['Equipment','Potions','Tier 1'])],{'potions':policy})
        self.assertEqual(audit[0]['status'],'content_changed')
        self.assertEqual(audit[0]['reviewed_content_sha256'],table_content_sha256(table))
        self.assertEqual(audit[0]['content_sha256'],table_content_sha256(changed))
        with patch('tables.measure_table',return_value=([10,20],[25,70],[])) as measured:
            result=apply_table_scope_override(changed,{'rep':'table'},resolved['TEST'])
        measured.assert_called_once_with(changed)
        self.assertEqual(result['widths'],[33.5,78.5])
        self.assertNotIn('h1',result)
        self.assertNotIn('h2',result)

    def test_semantic_width_policy_survives_table_ids_and_section_numbers_shifting(self):
        text=lambda value:[{'t':'text','v':value}]
        target={'id':'T055','header':[text('Roll'),text('Effect')],'rows':[]}
        policy={'selector':{'heading_path':['Equipment','Potions','Tier 1'], 'headers':['Roll','Effect']},
                'scope':'full','reviewed_content_sha256':table_content_sha256(target)}
        shifted=target|{'id':'T098'}
        unrelated=target|{'id':'T055'}
        resolved,audit=resolve_table_scope_policies([
            (unrelated,['Equipment','Poisons','Tier 1']),
            (shifted,['8. Equipment','8.14 Potions','Tier 1'])],{'potions':policy})
        self.assertEqual(set(resolved),{'T098'})
        self.assertEqual(audit[0]['table_id'],'T098')

    def test_removed_semantic_width_target_is_explicitly_unused(self):
        policy={'selector':{'heading_path':['Rules Reference','Equipment'], 'headers':['Procedure','Rule']},
                'scope':'full','reviewed_content_sha256':'reviewed'}
        resolved,audit=resolve_table_scope_policies([],{'equipment':policy})
        self.assertEqual(resolved,{})
        self.assertEqual(audit[0]['status'],'missing')
        self.assertIn('unused',audit[0]['message'])

    def test_ambiguous_semantic_width_target_fails_instead_of_guessing(self):
        header=[[{'t':'text','v':'Effect'}]]
        policy={'selector':{'heading_path':['Potions'], 'headers':['Effect']},
                'scope':'full','reviewed_content_sha256':'reviewed'}
        with self.assertRaises(TableScopePolicyError) as caught:
            resolve_table_scope_policies([({'id':uid,'header':header,'rows':[]},['Potions'])
                                         for uid in ['T001','T099']],{'potions':policy})
        self.assertIn('T001, T099',str(caught.exception))
        self.assertEqual(caught.exception.diagnostics[0]['status'],'ambiguous')

    def test_same_heading_path_with_different_headers_does_not_match(self):
        policy={'selector':{'heading_path':['Potions'], 'headers':['Effect']},
                'scope':'full','reviewed_content_sha256':'reviewed'}
        table={'id':'T055','header':[[{'t':'text','v':'Other'}]],'rows':[]}
        resolved,audit=resolve_table_scope_policies([(table,['Potions'])],{'potions':policy})
        self.assertEqual(resolved,{})
        self.assertEqual(audit[0]['status'],'missing')

    def test_converged_balance_cache_records_empty_final_and_signature_qualified_plans(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as td:
            path=Path(td)/'balance.json'
            self.assertTrue(save_converged_balance(path,{}, {},True))
            self.assertEqual(json.loads(path.read_text()),{})
            signature='v2:'+'a'*64
            plan={'1':[signature,3],'2':['v2:'+'b'*64,8]}
            self.assertTrue(save_converged_balance(path,plan,{'1':signature,'2':'updated'},True))
            self.assertEqual(json.loads(path.read_text()),{'1':[signature,3]})
            self.assertFalse(save_converged_balance(path,{}, {},False))
            self.assertEqual(json.loads(path.read_text()),{'1':[signature,3]})

    def test_main_saves_actual_converged_plan_on_first_and_last_allowed_pass(self):
        from contextlib import ExitStack, redirect_stdout
        from io import StringIO
        from tempfile import TemporaryDirectory
        from types import SimpleNamespace
        from unittest.mock import MagicMock, patch
        import build_book
        signature='v2:'+'a'*64
        plan={'0':[signature,1]}
        for proposals in ([{}],[plan,plan]):
            with self.subTest(passes=len(proposals)), TemporaryDirectory() as td, ExitStack() as stack:
                root=Path(td); build=root/'build'; mapping=root/'mappings'
                build.mkdir(); (root/'typst').mkdir()
                (build/'blocks.json').write_text(json.dumps({'sha256':'source','chapters':[]}))
                book=MagicMock()
                book.emit.return_value='#content'
                book.measure_requests=[];book.table_scope_diagnostics=[]
                book.table_map=[];book.block_map=[];book.unit_log=[];book.fig_slots={}
                book.seg_count=1;book.seg_sigs={'0':signature};book.piece_heads={};book.em.links=[]
                for name,value in [('ROOT',root),('BUILD',build),('MAP',mapping)]:
                    stack.enter_context(patch.object(build_book,name,value))
                stack.enter_context(patch.object(build_book,'Book',return_value=book))
                stack.enter_context(patch.object(build_book,'compile_book',return_value=('pdf',0.1,([],[]))))
                stack.enter_context(patch.object(build_book,'compute_balance',side_effect=proposals))
                stack.enter_context(patch('subprocess.run',return_value=SimpleNamespace(returncode=0,stdout='',stderr='')))
                stack.enter_context(patch.object(sys,'argv',['build_book','--passes',str(len(proposals))]))
                saved=stack.enter_context(patch.object(build_book,'save_converged_balance',wraps=save_converged_balance))
                with redirect_stdout(StringIO()):
                    build_book.main()
                expected=proposals[-1]
                saved.assert_called_once_with(build/'balance.json',expected,{'0':signature},True)
                self.assertEqual(json.loads((build/'balance.json').read_text()),expected)
                self.assertTrue(json.loads((build/'layout-build.json').read_text())['converged'])

    def test_segment_signature_invalidates_same_id_count_after_text_or_profile_change(self):
        from unittest.mock import patch
        pieces=[({'id':'unchanged'},'#text[Original content]')]
        first=segment_signature(pieces)
        self.assertRegex(first,r'^v2:[0-9a-f]{64}$')
        self.assertEqual(first,segment_signature(pieces))
        self.assertNotEqual(first,segment_signature([({'id':'unchanged'},'#text[Edited content]')]))
        with patch('build_book.profile_dict',return_value={'body_size_pt':11}):
            self.assertNotEqual(first,segment_signature(pieces))

    def test_balance_plan_rejects_malformed_negative_boolean_and_legacy_tails(self):
        signature='v2:'+'a'*64
        entries={'0':[signature,0], '1':[signature,-1], '2':[signature,True],
                 '3':[signature,'2'], '4':['legacy:5',1], '5':None,
                 '6':[signature], 'bad':[signature,0]}
        self.assertEqual(filtered_balance_plan(entries),{'0':[signature,0]})
        self.assertEqual(filtered_balance_plan([]),{})
        self.assertEqual(filtered_balance_plan({'0':[signature,1]},{'0':'v2:'+'b'*64}),{})

    def test_flush_ignores_bad_tails_and_same_id_count_edited_rendering(self):
        original=[({'id':'same','type':'para','src':[1,1]},'Original paragraph.')]
        signature=segment_signature(original)
        def emit(pieces,entry):
            book=Book.__new__(Book)
            book.seg_count=0;book.seg_sigs={};book.balance={'0':entry}
            book.block_map=[];book.piece_heads={};book.out=[]
            book.flush(pieces)
            return ''.join(book.out)
        self.assertIn('#flowtail(',emit(original,[signature,0]))
        changed=[(original[0][0],'Edited paragraph with unchanged source ID and piece count.')]
        self.assertNotIn('#flowtail(',emit(changed,[signature,0]))
        for bad in (None,[],[signature],[signature,-1],[signature,True],
                    [signature,'0'],[signature,999],['legacy:1',0]):
            with self.subTest(entry=bad):
                self.assertNotIn('#flowtail(',emit(original,bad))

    def test_measurement_and_hint_integration_hit_miss_bypass_local_and_warnings(self):
        from contextlib import ExitStack, redirect_stdout
        from io import StringIO
        from tempfile import TemporaryDirectory
        from types import SimpleNamespace
        from unittest.mock import MagicMock, patch
        import build_book
        signature='v2:'+'a'*64
        plan={'0':[signature,1]}
        cases=[('hit',[],False,plan,[],True),('miss',[],False,{},[],True),
               ('bypass',['--no-measurement-cache'],False,{},[],False),
               ('local',[],True,plan,[],False),('warnings',[],False,{},['warning: advisory'],True)]
        for name,extra,local,hint,warnings,expect_load in cases:
            with self.subTest(case=name), TemporaryDirectory() as td, ExitStack() as stack:
                root=Path(td);build=root/'build';build.mkdir();(root/'typst').mkdir()
                (build/'blocks.json').write_text(json.dumps({'sha256':'source','chapters':[]}))
                (build/'unit_measure.binding.json').write_text(json.dumps({'fresh':'binding'}))
                if local:
                    (build/'balance.json').write_text(json.dumps(plan))
                events=[]
                book=MagicMock();book.emit.return_value='#content'
                book.measure_requests=[];book.table_scope_diagnostics=[]
                book.table_map=[];book.block_map=[];book.unit_log=[];book.fig_slots={}
                book.seg_count=1;book.seg_sigs={'0':signature};book.piece_heads={};book.em.links=[]
                for key,value in [('ROOT',root),('BUILD',build),('MAP',root/'mappings')]:
                    stack.enter_context(patch.object(build_book,key,value))
                stack.enter_context(patch.object(build_book,'Book',return_value=book))
                def measure(*args,**kwargs):
                    events.append('measurement')
                    return SimpleNamespace(returncode=0,stdout='',stderr='')
                measured=stack.enter_context(patch('subprocess.run',side_effect=measure))
                def load(*args,**kwargs):
                    events.append('load_hint')
                    kwargs['diagnostics'].append({'status':name})
                    return hint
                loaded=stack.enter_context(patch.object(build_book,'load_hint',side_effect=load))
                stored=stack.enter_context(patch.object(build_book,'save_hint',return_value={'status':'stored' if not warnings else 'skipped'}))
                compiled=stack.enter_context(patch.object(build_book,'compile_book',return_value=('pdf',0.1,([],[]))))
                compiled.last_warnings=warnings
                expected=plan if name in ('hit','local') else {}
                stack.enter_context(patch.object(build_book,'compute_balance',return_value=expected))
                stack.enter_context(patch.object(sys,'argv',['build_book','--passes','1']+extra))
                with redirect_stdout(StringIO()):
                    build_book.main()
                self.assertEqual(loaded.called,expect_load)
                if expect_load:
                    self.assertEqual(events,['measurement','load_hint'])
                    self.assertEqual(loaded.call_args.args[1],{'fresh':'binding'})
                command=measured.call_args.args[0]
                self.assertEqual('--no-cache' in command,name=='bypass')
                if name=='bypass':
                    stored.assert_not_called()
                else:
                    stored.assert_called_once_with(root,{'fresh':'binding'},expected,converged=True,warnings=warnings)
                report=json.loads((build/'layout-build.json').read_text())
                self.assertEqual(report['warnings'],warnings)
                self.assertEqual(report['passes'][0]['warnings'],warnings)
                self.assertTrue(report['balance_cache'])

    def test_successful_compiler_stderr_is_visible_and_recorded_without_api_change(self):
        from contextlib import redirect_stderr
        from io import StringIO
        from types import SimpleNamespace
        from unittest.mock import patch
        import build_book
        output=StringIO()
        with patch('subprocess.run',return_value=SimpleNamespace(returncode=0,stdout='1.25\n',stderr='warning: advisory\n')), redirect_stderr(output):
            result=build_book.compile_book(query=False)
        self.assertEqual(result[1:],(1.25,None))
        self.assertEqual(build_book.compile_book.last_warnings,['warning: advisory'])
        self.assertIn('warning: advisory',output.getvalue())

    def test_short_tail_can_pull_back_a_complete_preceding_piece(self):
        pm=[{'seg':1,'piece':0,'edge':'s','page':1,'x':315,'y':BODY_BOTTOM-100},
            {'seg':1,'piece':1,'edge':'s','page':2,'x':42,'y':45},
            {'seg':1,'piece':2,'edge':'e','page':2,'x':42,'y':84}]
        self.assertEqual(compute_balance(pm,{'1':['same',1]},{'1':'same'}),{'1':['same',0]})
        pm[-1]['y']=500
        self.assertEqual(compute_balance(pm,{'1':['same',1]},{'1':'same'}),{'1':['same',1]})

    def test_short_roll_directive_keeps_the_substantive_explanation(self):
        book=Book.__new__(Book)
        book.measures={}
        book.block_map=[]
        book.log_unit=book.record=lambda *_:None
        head={'id':'head','b':{'type':'heading','level':5,'title':'Objective table','src':[1,1]},'s':'#heading[Objective table]'}
        def para(uid,text):
            return {'id':uid,'typ':'para','kind':'c','s':text,'b':{'type':'para','id':uid,'c':[{'t':'text','v':text}],'src':[2,2]}}
        node={'id':'head','level':5,'title':'Objective table','head':head,
              'children':[para('roll','Roll 1d10.'),para('meaning','These objectives are scenario objects and use the following complete procedure.')]}
        pieces,_=book.emit_x(node,[],False)
        self.assertIn('These objectives',pieces[0][1])
        self.assertIn('Roll 1d10.',pieces[0][1])

    def test_climate_and_scenario_starts_are_semantic_fresh_boundaries(self):
        book=Book.__new__(Book)
        self.assertTrue(book.is_fresh({'level':4,'title':'Climate 1: Greenmark Scenarios'}))
        self.assertTrue(book.is_fresh({'level':5,'title':'Scenario 1: Hunt the Wild Beast [Intro]'}))
        self.assertFalse(book.is_fresh({'level':4,'title':'A reference entry'}))

    def test_numbered_list_split_points_preserve_item_order_and_start(self):
        book = Book.__new__(Book)
        book.block_inline = lambda b: b['text']
        source = {'ordered': True, 'start': 4, 'items': [
            {'blocks': [{'text': 'Fourth'}, {'text': 'Its required exception.'}]},
            {'blocks': [{'text': 'Fifth'}]},
        ]}
        pieces = list(book.list_fragments(source))
        self.assertEqual(pieces, [
            '#list-fragment(number: 4)[Fourth#parbreak()Its required exception.]',
            '#list-fragment(number: 5)[Fifth]',
        ])

    def test_full_width_prose_does_not_emit_an_unaudited_keep(self):
        book = Book.__new__(Book)
        book.out, book.measures = [], {}
        book.flush = lambda _: None
        book.record = lambda *_: None
        item = {'id': 'flavour', 'kind': 'f', 'typ': 'para', 's': '#section-lead[Opening]'}
        self.assertEqual(book.emit_leaf(item, []), [])
        self.assertNotIn('#umark', ''.join(book.out))

    def test_oscillating_tail_uses_natural_flow_until_policy_is_stable(self):
        flips, excluded = {}, set()
        first = {'55': ['signature', 3]}
        self.assertEqual(stabilize_balance(first, {}, flips, excluded), first)
        self.assertEqual(stabilize_balance({}, first, flips, excluded), {})
        self.assertEqual(stabilize_balance(first, {}, flips, excluded), {})
        self.assertEqual(excluded, {'55'})
        self.assertEqual(stabilize_balance(first, {}, flips, excluded), {})

    def test_full_width_flavour_is_reserved_for_section_and_scenario_openings(self):
        book = Book.__new__(Book)
        book.block_map = []
        book.para = lambda b, role=None: f"#{role or 'flavour'}[Opening]"
        book.render = lambda b: '#heading[Entry]' if b['type'] == 'heading' else '#flavour[Opening]'
        book.figs_for = lambda b: []
        for level, title, expected in ((3, '6.1 Ancestries', 'f'), (4, 'Dire Wolf', 'c'),
                                       (5, 'Scenario 1: A Dangerous Road', 'f')):
            with self.subTest(title=title):
                items = book.chapter_items([
                    {'id': 'head', 'type': 'heading', 'title': title, 'level': level},
                    {'id': 'flavour', 'type': 'para', 'c': [{'t': 'em', 'c': [{'t': 'text', 'v': 'Opening'}]}]},
                    {'id': 'flavour-two', 'type': 'para', 'c': [{'t': 'em', 'c': [{'t': 'text', 'v': 'Continued opening'}]}]},
                ])
                for item in items[1:]:
                    self.assertEqual(item['kind'], expected)
                    self.assertEqual('section-lead' in item['s'], expected == 'f')
        continuation = book.chapter_items([
            {'id': 'continued', 'type': 'para', 'c': [{'t': 'em', 'c': [{'t': 'text', 'v': 'Chapter introduction continues.'}]}]},
        ])
        self.assertEqual(continuation[0]['kind'], 'f')

    def test_frame_uses_approved_profile(self):
        self.assertEqual(FRAME_H, BODY_HEIGHT_PT)
        self.assertEqual(FRAME_FIT, BODY_HEIGHT_PT - 12)

    def test_source_inventory_includes_nested_lists_and_figures(self):
        model = {'chapters': [{'id': 'front', 'blocks': []}, {'id': 'chapter', 'blocks': [
            {'id': 'h-one', 'type': 'heading', 'level': 3, 'src': [1, 2]},
            {'id': 'list-one', 'type': 'list', 'src': [3, 7], 'items': [{'blocks': [
                {'id': 'list-two', 'type': 'list', 'src': [4, 7], 'items': []}]}]}]}]}
        expected = source_unit_manifest(model, {'list-one': [{'id': 'FIG-01'}]})
        self.assertEqual([u['id'] for u in expected], ['h-one', 'list-one', 'list-two', 'FIG-01'])

    def test_contained_child_has_own_markers_and_record(self):
        book = Book.__new__(Book)
        book.measures = {'h-child': {'h1': 30, 'h2': 25}, 'table': {'h1': 20, 'h2': 20}}
        book.unit_log, book.logged_units = [], set()
        leaf = {'id': 'table', 'typ': 'table', 'kind': 'c', 's': '#htable("table")'}
        child = {'id': 'h-child', 'head': {'s': '#heading[Child]'}, 'children': [leaf]}
        parent = {'id': 'h-parent', 'head': {'s': '#heading[Parent]'}, 'children': [child]}
        parts = book.flat_parts(parent, marked=True)
        text = ''.join(s for _, strings in parts for s in strings)
        for uid in ('h-child', 'table'):
            self.assertEqual(text.count(f'#umark("{uid}", "s")'), 1)
            self.assertEqual(text.count(f'#umark("{uid}", "e")'), 1)
        self.assertEqual({u['id'] for u in book.unit_log}, {'h-child', 'table'})
        self.assertNotIn('h-parent', book.logged_units)

    def test_joined_title_inventory_does_not_disappear(self):
        book = Book.__new__(Book)
        book.measures = {'title': {'h1': 20, 'h2': 20}}
        book.extra_units, book.logged_units, book.unit_log = {}, set(), []
        source = {'id': 'title', 'type': 'list'}
        text = book.contained(source, '#enum([Power title])')
        self.assertIn('#umark("title", "s")', text)
        self.assertIn('#umark("title", "e")', text)
        self.assertEqual(book.unit_log[0]['id'], 'title')
        self.assertEqual(book.extra_units['title']['b'], source)


if __name__ == '__main__':
    unittest.main()
