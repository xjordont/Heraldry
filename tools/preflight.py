#!/usr/bin/env python3
"""Validate the publication launch kit; report runtime gaps without installing anything."""
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
REQUIRED = ['MASTER_PROMPT.md', 'CLAUDE.md', 'README.md', 'README_SETUP.md',
            'docs/DESIGN_SPEC.md', 'docs/ART_DIRECTION.md', 'docs/REFERENCE_ANALYSIS.md',
            'docs/LAUNCH_CHECKLIST.md', 'source/source_inventory.json',
            'references/reference_manifest.json', 'references/README.md',
            'tools/render_reference_pages.py', 'config/production.json',
            '.claude/settings.json', 'production/STATE.md']


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--baseline', action='store_true', help='Verify every shipped checksum before first execution')
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
        config = json.loads((root / 'config/production.json').read_text())
        inventory = json.loads((root / 'source/source_inventory.json').read_text())
        require(config['source'] == 'source/Heraldry_RC484.md', 'Canonical source path changed')
        source = root / config['source']
        require(digest(source) == SOURCE_HASH == inventory['sha256'], 'Canonical source hash mismatch')
        require(source.stat().st_size == inventory['bytes'], 'Canonical source size mismatch')
        return {'sha256': SOURCE_HASH, 'bytes': source.stat().st_size}

    def configuration():
        c = json.loads((root / 'config/production.json').read_text())
        s = json.loads((root / '.claude/settings.json').read_text())
        require(s['model'] == c['models']['orchestrator'], 'Orchestrator settings/config differ')
        require(s['effortLevel'] == c['models']['orchestrator_effort'], 'Orchestrator effort differs')
        require(c['models']['max_concurrent_subagents'] == 2, 'Concurrency differs from reviewed limit')
        b = c['budget']
        require(b['target_spend_usd'] + b['repair_reserve_usd'] == b['claude_cloud_credit_limit_usd'], 'Budget allocations do not reconcile')
        require(b['claude_cloud_credit_limit_usd'] == 100 and not b['allow_paid_overage'], 'Reviewed credit boundary changed')
        f = c['format']
        require(f['trim_width_inches'] == 8.5 and f['trim_height_inches'] == 11, 'Reviewed trim changed')
        require(f['minimum_essential_text_pt'] >= 9, 'Essential type minimum is too small')
        require(f['inside_margin_inches'] > f['outside_margin_inches'], 'Binding gutter is not larger than outside margin')
        i = c['image_generation']
        require(i['external_spend_limit_usd'] >= 0, 'Negative image budget')
        require(not i['paid_calls_authorized'] or i['external_spend_limit_usd'] > 0, 'Paid image calls lack a positive budget')
        return 'Configuration reconciles; account billing and model access require live checks'

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
        lines = (root / 'SHA256SUMS.txt').read_text().splitlines()
        seen = set()
        for line in lines:
            expected, name = line.split('  ', 1)
            path = (root / name).resolve()
            require(path.is_relative_to(root), 'Checksum path leaves repository')
            require(name not in seen, 'Duplicate checksum entry')
            require(path.is_file() and digest(path) == expected, 'Checksum mismatch: ' + name)
            seen.add(name)
        tracked = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
                   and '.git' not in p.parts and '__pycache__' not in p.parts
                   and p.name != 'SHA256SUMS.txt' and 'private' not in p.parts
                   and p.relative_to(root).parts[0] not in {'build', 'dist', 'tmp'}
                   and not (p.relative_to(root).parts[0] == 'production' and p.name != 'STATE.md')}
        require(tracked <= seen, 'Files missing from checksum inventory: ' + ', '.join(sorted(tracked - seen)))
        return f'{len(seen)} shipped files match checksums'

    check('required_files', required_files)
    check('source_integrity', source_integrity)
    check('configuration', configuration)
    check('agent_contracts', agent_contracts)
    check('reference_manifest', references)
    check('script_syntax', scripts)
    if args.baseline:
        check('shipped_baseline', baseline)
    commands = {n: bool(shutil.which(n)) for n in ['git', 'python3', 'typst', 'pandoc', 'pdfinfo', 'pdftoppm', 'qpdf', 'gs']}
    modules = {n: importlib.util.find_spec(n) is not None for n in ['typst', 'fitz', 'pypdf', 'pdfplumber', 'PIL']}
    result = {'scope': 'Launch-kit integrity only; not publication or live-Claude-account certification',
              'kit_status': 'FAIL' if any(c['status'] == 'FAIL' for c in checks) else 'PASS',
              'checks': checks,
              'runtime_observed': {'python': sys.version.split()[0], 'commands': commands, 'python_modules': modules},
              'external_inputs': {'claude_model_access_and_credit': 'VERIFY_IN_CLAUDE',
                                  'cloud_network_and_dependency_provisioning': 'VERIFY_IN_CLAUDE',
                                  'original_illustrations': 'SUPPLY_OR_USE_CONFIGURED_SERVICE; ART_LIGHT_FALLBACK',
                                  'printer_specification_and_cover_template': 'OPTIONAL_AT_LAUNCH; REQUIRED_FOR_SUBMISSION_READY'},
              'missing_tools_policy': 'Provision during the capability milestone; availability is not kit integrity'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['kit_status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
