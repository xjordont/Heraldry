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
# The roles come from config/agent_workflows.json. Which config/production.json model each Claude adapter must name
# (default bulk_work), and the adapters that must stay read-only:
AGENT_MODELS = {'mechanical-assistant': 'mechanical_work', 'blind-editorial-reviewer': 'orchestrator'}
READ_ONLY_AGENTS = {'blind-editorial-reviewer'}
REQUIRED = ['CLAUDE.md', 'AGENTS.md', 'README.md', 'docs/PROJECT_CONTRACT.md', 'docs/AGENT_OPERATIONS.md',
            'docs/DESIGN.md', 'docs/VISUAL_QA.md', 'docs/ART_DIRECTION.md', 'config/agent_workflows.json',
            'config/production.json', 'config/design_tokens.json', '.claude/settings.json', 'production/STATE.md']


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
        json.loads((root / 'config/production.json').read_text(encoding='utf-8'))
        from manuscript import check
        current = check(root)
        return {"sha256": current["sha256"], "bytes": current["bytes"], "version": f"RC{current['number']}"}

    def configuration():
        c = json.loads((root / 'config/production.json').read_text(encoding='utf-8'))
        s = json.loads((root / '.claude/settings.json').read_text(encoding='utf-8'))
        require(s['model'] == c['models']['orchestrator'], 'Orchestrator settings/config differ')
        require(s['effortLevel'] == c['models']['orchestrator_effort'], 'Orchestrator effort differs')
        require(c['models']['max_concurrent_subagents'] == 2, 'Concurrency differs from reviewed limit')
        require(c["workflow"]["working_branch"] == "main", "Working branch differs from owner instruction")
        f = c['format']
        require(f['trim_width_inches'] == 8.5 and f['trim_height_inches'] == 11, 'Reviewed trim changed')
        require(f['minimum_essential_text_pt'] >= 9, 'Essential type minimum is too small')
        i = c['image_generation']
        require(i['route'] == 'chatgpt_builtin', 'Artwork route differs from owner instruction')
        require(i['external_api_generation'] is False, "Artwork uses the owner's ChatGPT plan, not a paid image API")
        return 'Configuration reconciles; runtime model access requires live checks'

    def design_page_contract():
        c = json.loads((root / 'config/production.json').read_text(encoding='utf-8'))
        t = json.loads((root / 'config/design_tokens.json').read_text(encoding='utf-8'))
        p = c['page']
        require(c['format']['orientation'] == 'portrait', 'Primary orientation changed')
        require((p['width_pt'], p['height_pt']) == (612, 792), 'Page is not exact Letter')
        require((t['page']['width_pt'], t['page']['height_pt']) == (612, 792), 'Design token page differs')
        require(not p['landscape_pages_allowed'], 'Landscape fallback contradicts portrait edition')
        require(p['essential_edge_safe_inches'] >= 0.375, 'Essential safe area too small')
        require(t['page']['essential_edge_safe_pt'] == p['essential_edge_safe_inches'] * 72, 'Safe zones differ')
        require(t['substrate']['cover_to_page_edge'] and t['substrate']['default'] == 'warm_cream', 'Page colour contract invalid')
        require(re.fullmatch(r'#[0-9A-Fa-f]{6}', t['substrate']['warm_cream_hex']) is not None, 'Invalid page colour')
        require(t['type_pt']['minimum_essential'] == c['format']['minimum_essential_text_pt'], 'Type minimum differs')
        require(t['fonts']['max_families'] == 4 and not t['ornament']['ordinary_page_perimeter_frame'] and not t['ornament']['decorative_watermark'], 'Visual restraint contract changed')
        return 'Portrait Letter page, cream tokens, and safe area reconcile'

    def agent_contracts():
        from agent_workflow import catalog
        shared = catalog(root)
        config = json.loads((root / 'config/production.json').read_text(encoding='utf-8'))
        for role in shared['roles']:
            name = role['name']
            text = (root / role['claude_adapter']).read_text(encoding='utf-8')
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
            model = config['models'][AGENT_MODELS.get(name, 'bulk_work')]
            require(fields.get('model') == model, f'{name}: model/config mismatch')
            require(fields.get('effort') in {None, 'low', 'medium', 'high', 'xhigh', 'max'}, f'{name}: invalid effort')
            tools = {x.strip() for x in fields.get('tools', '').split(',')}
            if name in READ_ONLY_AGENTS:
                require('Read' in tools and not tools & {'Write', 'Edit', 'Bash', 'NotebookEdit', 'Agent'}, f'{name}: invalid read-only tool contract')
            else:
                require({'Read', 'Write', 'Bash'} <= tools and 'Agent' not in tools, f'{name}: invalid tool contract')
        return f"{len(shared['roles'])} Claude-native adapters and {len(shared['workflows'])} shared workflows validated for all three clients; runtime resolution is separate"

    def scripts():
        for p in sorted((root / 'tools').glob('*.py')):
            ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
        return 'Python scripts parse successfully'

    def baseline():
        require(digest(root / 'source/Heraldry_RC484.md') == SOURCE_HASH, 'Original RC484 baseline altered')
        return 'Archived RC484 baseline hash verified; historical launch-kit checksums are in docs/history/launch-kit/'

    check('required_files', required_files)
    check('source_integrity', source_integrity)
    check('configuration', configuration)
    check('agent_contracts', agent_contracts)
    check('design_page_contract', design_page_contract)
    check('script_syntax', scripts)
    if args.baseline:
        check('shipped_baseline', baseline)
    commands = {n: bool(shutil.which(n)) for n in ['git', 'python3', 'typst', 'pandoc', 'pdfinfo', 'pdftoppm', 'qpdf', 'gs']}
    modules = {n: importlib.util.find_spec(n) is not None for n in ['typst', 'fitz', 'pypdf', 'markdown_it', 'fontTools', 'PIL']}
    result = {'scope': 'Repository contracts only; not publication or live-agent-account certification',
              'kit_status': 'FAIL' if any(c['status'] == 'FAIL' for c in checks) else 'PASS',
              'checks': checks,
              'runtime_observed': {'python': sys.version.split()[0], 'commands': commands, 'python_modules': modules},
              'external_inputs': {'agent_model_and_tool_access': 'VERIFY_IN_CURRENT_CLIENT',
                                  'cloud_network_and_dependency_provisioning': 'VERIFY_IN_CURRENT_CLIENT',
                                  'original_illustrations': 'CHATGPT_WORK_GENERATED_MASTERS; INTEGRATE_AND_REVIEW'},
              'missing_tools_policy': 'Provision during the capability milestone; availability is not kit integrity'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if result['kit_status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
