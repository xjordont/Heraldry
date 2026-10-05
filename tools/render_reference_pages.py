#!/usr/bin/env python3
"""Render the optional, hash-verified visual references; never ingest game rules."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    kit = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path)
    parser.add_argument('--output', type=Path, default=kit / 'references/private')
    parser.add_argument('--manifest', type=Path, default=kit / 'references/reference_manifest.json')
    parser.add_argument('--ids', nargs='+')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--dpi', type=int, default=120)
    args = parser.parse_args()
    if not 72 <= args.dpi <= 300:
        parser.error('--dpi must be 72–300')
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    refs = manifest['references']
    if args.ids:
        unknown = set(args.ids) - {r['id'] for r in refs}
        if unknown:
            parser.error(f'Unknown reference IDs: {sorted(unknown)}')
        refs = [r for r in refs if r['id'] in args.ids]
    elif not args.all:
        refs = [r for r in refs if r['priority'] == 'primary']
    if args.plan:
        print(json.dumps({'books': len(refs), 'pages': sum(len(r['pages']) for r in refs),
                          'selection': [{'id': r['id'], 'title': r['title'], 'pages': r['pages']} for r in refs]}, indent=2))
        return 0
    if not args.source_root or not args.source_root.is_dir():
        parser.error('Provide --source-root pointing to an existing reference directory')
    try:
        import fitz
    except ImportError:
        parser.error('Install PyMuPDF before rendering: python3 -m pip install PyMuPDF')
    fitz.TOOLS.mupdf_display_errors(False)
    fitz.TOOLS.mupdf_display_warnings(False)
    desired = {r['sha256'] for r in refs}
    by_hash = {}
    scan_errors = []
    for path in sorted(args.source_root.rglob('*')):
        if path.is_file() and path.suffix.lower() == '.pdf':
            try:
                with path.open('rb') as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                if digest in desired:
                    by_hash.setdefault(digest, path)
            except OSError as exc:
                scan_errors.append({'file': str(path), 'error': str(exc)})
    args.output.mkdir(parents=True, exist_ok=True)
    result = {'page_numbering': '1-based PDF viewer pages', 'scan_errors': scan_errors, 'references': []}
    missing = False
    for ref in refs:
        entry = {'id': ref['id'], 'title': ref['title'], 'requested_pages': ref['pages'], 'rendered': []}
        source = by_hash.get(ref['sha256'])
        if source is None:
            entry['status'] = 'missing_exact_source'
            missing = True
        else:
            try:
                fitz.TOOLS.mupdf_warnings(reset=True)
                with fitz.open(source) as doc:
                    if len(doc) != ref['page_count']:
                        raise ValueError('PDF page count differs from verified manifest')
                    for number in ref['pages']:
                        if not 1 <= number <= len(doc):
                            raise ValueError(f'Invalid PDF page {number}')
                        output = args.output / f"{ref['id']}-pdf-p{number:03d}.png"
                        doc[number - 1].get_pixmap(dpi=args.dpi, alpha=False).save(output)
                        entry['rendered'].append({'pdf_page': number, 'image': output.name})
                entry['status'] = 'rendered'
                warning = fitz.TOOLS.mupdf_warnings(reset=True)
                if warning:
                    entry['pdf_warnings'] = warning[:2000]
            except Exception as exc:
                entry['status'] = 'failed'
                entry['error'] = str(exc)
                missing = True
        result['references'].append(entry)
    (args.output / 'render-status.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'books': len(refs), 'pages_rendered': sum(len(r['rendered']) for r in result['references']),
                      'incomplete': missing, 'output': str(args.output)}, indent=2))
    return 1 if missing else 0


if __name__ == '__main__':
    raise SystemExit(main())
