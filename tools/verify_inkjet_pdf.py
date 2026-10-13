#!/usr/bin/env python3
"""Check the primary book PDF's borderless Letter file contract; not physical-print certification."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys


def inspect(pdf: Path, config: dict) -> dict:
    import fitz
    profile = config['inkjet']
    width, height = profile['page_width_pt'], profile['page_height_pt']
    safe = profile['essential_edge_safe_inches'] * 72
    scale = profile['overscan_test_scale']
    minimum = config['format']['minimum_essential_text_pt']
    counts = {}
    examples = []

    def fail(code, page, detail):
        counts[code] = counts.get(code, 0) + 1
        if len(examples) < 50:
            examples.append({'code': code, 'page': page, 'detail': detail})

    def equal_box(rect):
        return all(abs(a - b) <= 0.1 for a, b in zip(rect, (0, 0, width, height)))

    seen_fonts = set()
    text_spans = 0
    with fitz.open(pdf) as doc:
        if doc.is_encrypted:
            raise ValueError('Encrypted PDF is not inspectable')
        if not len(doc):
            raise ValueError('PDF has no pages')
        for n, page in enumerate(doc, 1):
            if page.rotation != 0:
                fail('page_rotation', n, page.rotation)
            for name in ('mediabox', 'cropbox', 'trimbox', 'bleedbox'):
                rect = getattr(page, name)
                if not equal_box(rect):
                    fail('page_box', n, {'box': name, 'actual': list(rect)})
            flags = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES
            for block in page.get_text('dict', flags=flags)['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        if not span['text'].strip():
                            continue
                        text_spans += 1
                        x0, y0, x1, y1 = span['bbox']
                        if span['size'] < minimum - 0.1:
                            fail('small_type', n, {'size_pt': span['size'], 'text': span['text'][:80]})
                        # Thumb tab (design v4): the rotated chapter keyword in the outer 0.42 in strip is
                        # redundant navigation (the running head names the chapter), so it is exempt from the
                        # essential-content edge rule; it must still survive the overscan test below.
                        tab = x1 < 0.42 * 72 or x0 > width - 0.42 * 72
                        if not tab and min(x0, y0, width - x1, height - y1) < safe - 0.1:
                            fail('unsafe_text', n, {'bbox': span['bbox'], 'text': span['text'][:80]})
                        grown = [(x0 - width/2)*scale + width/2,
                                 (y0 - height/2)*scale + height/2,
                                 (x1 - width/2)*scale + width/2,
                                 (y1 - height/2)*scale + height/2]
                        if min(grown[0], grown[1], width-grown[2], height-grown[3]) < -0.1:
                            fail('overscan_text_clip', n, {'scale': scale, 'text': span['text'][:80]})
            for font in page.get_fonts(full=True):
                xref = font[0]
                if xref in seen_fonts:
                    continue
                seen_fonts.add(xref)
                try:
                    embedded = bool(xref and doc.extract_font(xref)[3])
                except Exception:
                    embedded = False
                if not embedded:
                    fail('font_not_verified_embedded', n, {'xref': xref, 'font': font[3]})
        if not text_spans:
            fail('no_searchable_text', None, 'The primary book must retain searchable text')
        pages = len(doc)
    return {'status': 'FAIL' if counts else 'PASS', 'pdf': str(pdf), 'pages': pages,
            'text_spans_checked': text_spans, 'font_resources_checked': len(seen_fonts),
            'checks': ['Letter portrait boxes/rotation', 'minimum text size', 'text edge safety',
                       'simulated centred overscan text clipping', 'referenced font embedding', 'searchable text present'],
            'failure_counts': counts, 'failure_examples_first_50': examples,
            'physical_inkjet_proof': 'NOT TESTED',
            'limits': 'Not source reconciliation, art/background/raster/mark inspection, all-page visual QA, or physical printer certification',
            'tool': {'PyMuPDF': fitz.VersionBind, 'python': sys.version.split()[0]}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--config', type=Path, default=Path(__file__).resolve().parents[1] / 'config/production.json')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args.pdf, json.loads(args.config.read_text()))
    except Exception as exc:
        result = {'status': 'FAIL', 'error': str(exc), 'physical_inkjet_proof': 'NOT TESTED'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
