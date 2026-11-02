#!/usr/bin/env python3
"""Plan, check, or run an owner-requested local layout proof without publishing."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

from manuscript import check as check_source
from provenance import inputs
from pdf_positions import GENERATED_INPUTS
from verify import layout_report_clean

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Stage:
    name: str
    args: tuple[str, ...]
    report: Path | None = None
    kind: str = "status"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(root):
    # content.typ and measure.typ are generated during composition. Everything
    # else in the full publication inventory must stay frozen after preparation.
    inventory = inputs(root)
    inventory.pop('typst/measure.typ', None)
    for name in GENERATED_INPUTS:
        path = root / name
        if path.exists():
            inventory[name] = digest(path)
    return hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest()


def stage_groups(out, *, checks_only=False):
    def task(name, *args, report=None, kind="status"):
        path = out / (report or name + '.json') if report is not False else None
        return Stage(name, tuple(args) + (("--report", str(path)) if path else ()), path, kind)
    checks = [
        [task('dependencies', 'tools/check_dependencies.py')],
        [task('preflight', 'tools/preflight.py', '--baseline', kind='preflight')],
    ]
    if checks_only:
        # Fast iteration checks; these do not replace the full pre-push suite.
        for pattern in ('test_layout*.py', 'test_*measurement*.py', 'test_pdf_position_evidence.py',
                        'test_publication_qa_contract.py'):
            checks.append([task('tests-' + pattern.replace('*', 'all'), '-m', 'unittest',
                                'discover', '-s', 'tests', '-p', pattern, report=False)])
        return checks
    checks += [
        [task('parse', 'tools/parse_source.py', report=False)],
        [task('index', 'tools/make_index.py', report=False)],
        [task('figures', 'figures/src/make_figures.py', report=False)],
        [task('figure-currency', 'tools/figure_review_gate.py')],
        [task('extras', 'tools/build_extras.py', report=False)],
        [task('cream', 'tools/build_book.py', '--passes', '8', report=False)],
        [task('keeps', 'tools/keep_audit.py', '--positions', 'build/book-cream.positions.json', '--pdf', 'build/book-cream.pdf'),
         task('page-map', 'tools/page_map_accuracy.py', '--positions', 'build/book-cream.positions.json', '--pdf', 'build/book-cream.pdf'),
         task('reconciliation', 'tools/reconcile.py', 'build/book-cream.pdf'),
         task('layout', 'tools/layout_qa.py', 'build/book-cream.pdf', kind='layout')],
        [task('variants', 'tools/build_book.py', '--variants-only', report=False)],
        [task('digital-reconciliation', 'tools/reconcile.py', 'build/book-digital.pdf', '--skip-covers')],
    ]
    return checks


def report_passes(stage):
    if stage.report is None:
        return True
    try:
        payload = json.loads(stage.report.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return False
    if stage.kind == 'layout':
        return layout_report_clean(payload)
    if stage.kind == 'preflight':
        return isinstance(payload, dict) and payload.get('kit_status') == 'PASS'
    return isinstance(payload, dict) and payload.get('status') == 'PASS'


def run_stage(stage, root, out, executor=subprocess.run):
    if stage.report:
        stage.report.unlink(missing_ok=True)
    command = [sys.executable, *stage.args]
    log = out / (stage.name + '.log')
    started = time.monotonic()
    with log.open('w', encoding='utf-8') as stream:
        result = executor(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT)
    passed = result.returncode == 0 and report_passes(stage)
    return {'name': stage.name, 'command': command, 'status': 'PASS' if passed else 'FAIL',
            'exit_code': result.returncode, 'seconds': round(time.monotonic() - started, 3),
            'log': str(log), 'report': str(stage.report) if stage.report else None,
            'report_sha256': digest(stage.report) if stage.report and stage.report.exists() else None}


def execute_groups(groups, root, out, receipt, *, executor=subprocess.run, frozen=None):
    """Finish independent checks in a batch; never start dependent work after failure."""
    for batch in groups:
        if frozen is not None and fingerprint(root) != frozen:
            raise ValueError('Publication inputs changed after preparation; start a fresh layout run')
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda s: run_stage(s, root, out, executor), batch))
        receipt['stages'].extend(results)
        write_receipt(out, receipt)
        if any(r['status'] != 'PASS' for r in results):
            names = ', '.join(r['name'] for r in results if r['status'] != 'PASS')
            raise ValueError('Layout stage failed: ' + names + '; see ' + str(out))
        if frozen is not None and fingerprint(root) != frozen:
            raise ValueError('Publication inputs changed during layout stage; start a fresh run')


def write_receipt(out, receipt):
    (out / 'run.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')


def assert_model_current(root, source):
    model = json.loads((root / 'build/blocks.json').read_text(encoding='utf-8'))
    if model.get('sha256') != source['sha256'] or model.get('source') != source['path']:
        raise ValueError('Parsed manuscript is stale; rerun preparation for the active RC')


def run_local(mode, root=ROOT):
    root = Path(root).resolve()
    source = check_source(root)
    suffix = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6]
    out = root / 'build/checks/layout-runs' / suffix
    out.mkdir(parents=True)
    receipt = {'schema': 1, 'mode': mode, 'status': 'RUNNING', 'source': source,
               'stages': [], 'limits': ['Local proof only; no publication or visual approval']}
    lock = root / 'build/layout-workflow.lock'
    acquired = False
    started = time.monotonic()
    try:
        with lock.open('x', encoding='utf-8') as stream:
            stream.write(str(out))
        acquired = True
        groups = stage_groups(out, checks_only=mode == 'check')
        if mode == 'check':
            execute_groups(groups, root, out, receipt)
            receipt['status'] = 'SCOPED_CHECKS_PASS'
        else:
            first_compile = next(i for i, batch in enumerate(groups) if batch[0].name == 'cream')
            execute_groups(groups[:first_compile], root, out, receipt)
            source = check_source(root)
            assert_model_current(root, source)
            frozen = fingerprint(root)
            receipt.update(source=source, frozen_inputs_sha256=frozen)
            execute_groups(groups[first_compile:first_compile + 1], root, out, receipt, frozen=frozen)
            interior_hash = digest(root / 'build/book-cream.pdf')
            execute_groups(groups[first_compile + 1:], root, out, receipt, frozen=frozen)
            if digest(root / 'build/book-cream.pdf') != interior_hash:
                raise ValueError('Proof PDF changed during validation: book-cream.pdf')
            # Preserve the exact interior and the digital edition the review images are made from.
            receipt['artifacts'] = {}
            for name in ('book-cream.pdf', 'book-digital.pdf'):
                shutil.copyfile(root / 'build' / name, out / name)
                receipt['artifacts'][name] = digest(out / name)
            review = Stage('review-images', ('tools/review_aids.py', 'build', '--pdf', str(out / 'book-digital.pdf'),
                '--out', str(out / 'review')))
            execute_groups([[review]], root, out, receipt, frozen=frozen)
            manifest = json.loads((out / 'review/manifest.json').read_text(encoding='utf-8'))
            if manifest.get('pdf_sha256') != receipt['artifacts']['book-digital.pdf']:
                raise ValueError('Review manifest does not match the archived proof')
            receipt['measurement'] = json.loads((root / 'build/unit_measure.binding.json').read_text(encoding='utf-8'))
            receipt['composition'] = json.loads((root / 'build/layout-build.json').read_text(encoding='utf-8'))
            receipt['status'] = 'LOCAL_QA_PASS_REVIEW_REQUIRED'
    except Exception as error:
        receipt.update(status='FAIL', error=str(error))
    finally:
        receipt['seconds'] = round(time.monotonic() - started, 3)
        write_receipt(out, receipt)
        if acquired:
            lock.unlink(missing_ok=True)
    print(json.dumps({'status': receipt['status'], 'receipt': str(out / 'run.json'),
                      'seconds': receipt['seconds'], 'error': receipt.get('error')}))
    return 1 if receipt['status'] == 'FAIL' else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('plan', 'check', 'run'))
    args = parser.parse_args()
    if args.command == 'plan':
        source = check_source()
        out = ROOT / 'build/checks/layout-runs/NEW_RUN'
        print(json.dumps({'source': source['path'], 'source_sha256': source['sha256'],
                          'batches': [[{'name': s.name, 'args': list(s.args)} for s in group]
                                      for group in stage_groups(out)],
                          'note': 'Read-only plan; run requires an owner-requested layout pass. No release or review approval.'}, indent=2))
        return 0
    return run_local(args.command)


if __name__ == '__main__':
    raise SystemExit(main())
