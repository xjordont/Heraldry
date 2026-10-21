"""Enumerate required keeps from parsed source, independently of emitted layout logs."""
import re
from parse_source import plain


def source_unit_manifest(model, placements):
    result = []
    def walk(blocks):
        for block in blocks:
            kind = block['type']
            example = False
            if kind == 'para':
                nodes = [n for n in block['c'] if not (n['t'] == 'text' and not n['v'].strip())]
                text = plain(block['c']).strip()
                example = bool(nodes and ((nodes[0]['t'] == 'em' and text.startswith('Example')) or
                    (nodes[0]['t'] == 'strong' and re.match(r"^[\w ,'-]*Example:", text))))
            if (kind == 'heading' and block['level'] >= 3) or kind in {'table', 'list', 'quote'} or example:
                result.append({'id': block['id'], 'kind': 'section' if kind == 'heading' else 'example' if example else kind,
                               'src': block['src']})
            for item in block.get('items', []):
                walk(item['blocks'])
            walk(block.get('blocks', []))
    for chapter in model['chapters']:
        if chapter['id'] not in {'front', 'h-table-of-contents'}:
            walk(chapter['blocks'])
    for figures in placements.values():
        result.extend({'id': figure['id'], 'kind': 'figure'} for figure in figures)
    ids = [row['id'] for row in result]
    if len(ids) != len(set(ids)):
        raise ValueError('Source keep inventory contains duplicate identifiers')
    return result
