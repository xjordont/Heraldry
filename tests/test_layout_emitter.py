"""Exercise source keep coverage and semantic layout, independently of PDF page numbers."""
from pathlib import Path
import json
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build_book import (Book, FRAME_FIT, FRAME_H, stabilize_balance, compute_balance, BODY_BOTTOM,
                        apply_table_scope_override, table_content_sha256)
from source_units import source_unit_manifest
from layout_profile import BODY_HEIGHT_PT


class LayoutEmitter(unittest.TestCase):
    def test_measured_width_decision_refuses_changed_source_cells(self):
        from copy import deepcopy
        text=lambda value:[{'t':'text','v':value}]
        table={'id':'TEST','header':[text('Roll'),text('Effect')],
               'rows':[[text('1'),text('A complete effect.')]]}
        policy={'scope':'full','content_sha256':table_content_sha256(table),'reason':'Reviewed specimen'}
        result=apply_table_scope_override(table,{'rep':'table','scope':'column'},policy)
        self.assertEqual(result['scope'],'full')
        changed=deepcopy(table)
        changed['rows'][0][1]=text('A changed effect.')
        with self.assertRaisesRegex(ValueError,'content changed'):
            apply_table_scope_override(changed,{'rep':'table'},policy)

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
