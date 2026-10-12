#!/usr/bin/env python3
"""Validate the current publication repository; report runtime gaps without installing anything."""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_HASH = '2744833106569e6b20f6913340de5d80c7869782556e23b8f738a0407e4f16f3'
AGENTS = {'book-designer': 'medium', 'publication-engineer': 'high',
          'publication-auditor': 'high', 'rules-illustrator': 'high',
          'mechanical-assistant': None}
REQUIRED = ['MASTER_PROMPT.md', 'CLAUDE.md', 'README.md',
            'docs/DESIGN_SPEC.md', 'docs/ART_DIRECTION.md', 'docs/REFERENCE_ANALYSIS.md',
            'docs/LAUNCH_CHECKLIST.md', 'source/source_inventory.json',
            'references/reference_manifest.json', 'references/README.md',
            'tools/render_reference_pages.py', 'config/production.json',
            '.claude/settings.json', 'production/STATE.md', 'config/design_tokens.json',
            'docs/INKJET_PRINT.md', 'docs/VISUAL_QA.md', 'tools/verify_inkjet_pdf.py']


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--baseline', action='store_true', help='Also verify the archived original RC484 baseline')
    parser.add_argument('--report', type=Path, help='Optional JSON output; no secrets or environment values are recorded')
    args = parser.parse_args()
    root = args.root.resolve()
    checks = []

    def check(name, fn):
        try:
            detail = fn()
            checks.append({'check': name, 'status': 'PASS', 'detail': detail})
        except Exception as exc:
            checks.append({'check': name, 'status': 'FAIL', 'detail': str(exc)})

    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def required_files():
        missing = [p for p in REQUIRED if not (root / p).is_file()]
        require(not missing, 'Missing files: ' + ', '.join(missing))
        return f'{len(REQUIRED)} required files present'

    def source_integrity():
        json.loads((root / 'config/production.json').read_text())
        from manuscript import check
        current = check(root)
        return {"sha256": current["sha256"], "bytes": current["bytes"], "version": f"RC{current['number']}"}

    def configuration():
        c = json.loads((root / 'config/production.json').read_text())
        s = json.loads((root / '.claude/settings.json').read_text())
        require(s['model'] == c['models']['orchestrator'], 'Orchestrator settings/config differ')
        require(s['effortLevel'] == c['models']['orchestrator_effort'], 'Orchestrator effort differs')
        require(c['models']['max_concurrent_subagents'] == 2, 'Concurrency differs from reviewed limit')
        require(c["workflow"]["working_branch"] == "main", "Working branch differs from owner instruction")
        f = c['format']
        require(f['trim_width_inches'] == 8.5 and f['trim_height_inches'] == 11, 'Reviewed trim changed')
        require(f['minimum_essential_text_pt'] >= 9, 'Essential type minimum is too small')
        require(f['inside_margin_inches'] > f['outside_margin_inches'], 'Binding gutter is not larger than outside margin')
        i = c['image_generation']
        require(i['route'] == 'chatgpt_builtin' and i['generation_owner'] == 'ChatGPT Work', 'Artwork route differs from owner instruction')
        require(i['external_api_generation'] is False, 'Artwork generation belongs in ChatGPT Work')
        return 'Configuration reconciles; runtime model access requires live checks'

    def design_print_contract():
        c = json.loads((root / 'config/production.json').read_text())
        t = json.loads((root / 'config/design_tokens.json').read_text())
        p = c['inkjet']
        require(c['format']['orientation'] == 'portrait', 'Primary orientation changed')
        require(p['borderless'] and not p['crop_marks'] and p['external_bleed_inches'] == 0, 'Borderless sheet contract changed')
        require((p['page_width_pt'], p['page_height_pt']) == (612, 792), 'Inkjet page is not exact Letter')
        require((t['page']['width_pt'], t['page']['height_pt']) == (612, 792), 'Design token page differs')
        require(not p['landscape_pages_allowed'], 'Landscape fallback contradicts portrait edition')
        require(p['essential_edge_safe_inches'] >= 0.375, 'Inkjet essential safe area too small')
        require(t['page']['essential_edge_safe_pt'] == p['essential_edge_safe_inches'] * 72, 'Safe zones differ')
        require(1 < p['overscan_test_scale'] <= 1.1 and p['overscan_test_scale'] == t['page']['overscan_test_scale'], 'Overscan design test differs')
        require(t['substrate']['cover_to_page_edge'] and t['substrate']['default'] in {'warm_cream', 'paper_white'}, 'Substrate contract invalid')
        for key in ('warm_cream_hex', 'paper_white_hex'):
            require(re.fullmatch(r'#[0-9A-Fa-f]{6}', t['substrate'][key]) is not None, 'Invalid substrate colour')
        require(t['type_pt']['minimum_essential'] == c['format']['minimum_essential_text_pt'], 'Type minimum differs')
        require(t['fonts']['max_families'] <= 3 and not t['ornament']['ordinary_page_perimeter_frame'] and not t['ornament']['decorative_watermark'], 'Visual restraint contract changed')
        return 'Portrait Letter borderless/cream tokens, safe area, and print checks reconcile'

    def agent_contracts():
        for name, effort in AGENTS.items():
            text = (root / '.claude/agents' / (name + '.md')).read_text()
            parts = text.split('---', 2)
            require(len(parts) == 3 and not parts[0].strip(), f'{name}: missing frontmatter')
            fields = {}
            for line in parts[1].strip().splitlines():
                match = re.fullmatch(r'([A-Za-z]+):\s*(.*)', line)
                require(match is not None, f'{name}: unsupported frontmatter syntax')
                require(match[1] not in fields, f'{name}: duplicate frontmatter field')
                fields[match[1]] = match[2]
            require(fields.get('name') == name, f'{name}: name mismatch')
            require(bool(fields.get('description')), f'{name}: missing description')
            config = json.loads((root / 'config/production.json').read_text())
            model = config['models']['mechanical_work' if name == 'mechanical-assistant' else 'bulk_work']
            require(fields.get('model') == model, f'{name}: model/config mismatch')
            require(fields.get('effort') == effort, f'{name}: effort mismatch')
            tools = {x.strip() for x in fields.get('tools', '').split(',')}
            require({'Read', 'Write', 'Bash'} <= tools and 'Agent' not in tools, f'{name}: invalid tool contract')
        return 'Five bounded model/effort/tool definitions validated; runtime resolution is separate'

    def references():
        m = json.loads((root / 'references/reference_manifest.json').read_text())
        refs = m['references']
        require(len({x['id'] for x in refs}) == len(refs), 'Duplicate reference IDs')
        require(len({x['sha256'] for x in refs}) == len(refs), 'Duplicate selected books')
        for x in refs:
            require(re.fullmatch('[0-9a-f]{64}', x['sha256']) is not None, 'Invalid reference hash')
            require(x['priority'] in {'primary', 'secondary'}, 'Invalid reference priority')
            require(len(set(x['pages'])) == len(x['pages']), 'Duplicate selected pages')
            require(all(isinstance(n, int) and 1 <= n <= x['page_count'] for n in x['pages']), 'Reference page out of range')
        return {'primary_pages': sum(len(x['pages']) for x in refs if x['priority'] == 'primary'),
                'all_selected_pages': sum(len(x['pages']) for x in refs), 'availability': 'optional'}

    def scripts():
        for p in sorted((root / 'tools').glob('*.py')):
            ast.parse(p.read_text(), filename=str(p))
        return 'Python scripts parse successfully'

    def baseline():
        require(digest(root / 'source/Heraldry_RC484.md') == SOURCE_HASH, 'Original RC484 baseline altered')
        return 'Archived RC484 baseline hash verified; historical launch-kit checksums are in docs/history/launch-kit/'

    check('required_files', required_files)
    check('source_integrity', source_integrity)
    check('configuration', configuration)
    check('agent_contracts', agent_contracts)
    check('design_print_contract', design_print_contract)
    check('reference_manifest', references)
    check('script_syntax', scripts)
    if args.baseline:
        check('shipped_baseline', baseline)
    commands = {n: bool(shutil.which(n)) for n in ['git', 'python3', 'typst', 'pandoc', 'pdfinfo', 'pdftoppm', 'qpdf', 'gs']}
    modules = {n: importlib.util.find_spec(n) is not None for n in ['typst', 'fitz', 'pypdf', 'markdown_it', 'fontTools', 'PIL']}
    result = {'scope': 'Repository contracts only; not publication or live-Claude-account certification',
              'kit_status': 'FAIL' if any(c['status'] == 'FAIL' for c in checks) else 'PASS',
              'checks': checks,
              'runtime_observed': {'python': sys.version.split()[0], 'commands': commands, 'python_modules': modules},
              'external_inputs': {'claude_model_access': 'VERIFY_IN_CLAUDE',
                                  'cloud_network_and_dependency_provisioning': 'VERIFY_IN_CLAUDE',
                                  'original_illustrations': 'CHATGPT_WORK_GENERATED_MASTERS; INTEGRATE_AND_REVIEW',
                                  'physical_inkjet_proof': 'NOT TESTED; DOES NOT BLOCK FILE COMPLETION',
                                  'commercial_cover_wrap': 'NOT APPLICABLE UNLESS SEPARATELY REQUESTED'},
              'missing_tools_policy': 'Provision during the capability milestone; availability is not kit integrity'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['kit_status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
