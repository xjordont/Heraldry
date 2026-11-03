#!/usr/bin/env python3
"""Prepare and explicitly approve a supplied Markdown manuscript without building PDFs."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys

from manuscript import ROOT, check
from revise_manuscript import revise, RevisionRecoveryError
from git_publish import PublishError, require_current_main

SCHEMA = 1
MARKER = re.compile(r"^\*\*Release Candidate (\d+) \(RC(\d+)\)\*\*$", re.MULTILINE)
CONFIGS = ("config/content_anchors.json", "config/figure_dependencies.json")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def normalise(raw, current, target_rc=None):
    """Only remove a UTF-8 BOM, normalise line endings, and manage the RC marker."""
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    if "\x00" in text:
        raise ValueError("Input contains NUL bytes; supply a UTF-8 Markdown file")
    markers = list(MARKER.finditer(text))
    if len(markers) != 1 or markers[0][1] != markers[0][2]:
        raise ValueError("Input needs exactly one **Release Candidate N (RCN)** line with matching numbers")
    incoming = int(markers[0][1])
    if target_rc is not None and (type(target_rc) is not int or target_rc <= current):
        raise ValueError("Target RC must be an integer greater than the current RC")
    if incoming < current:
        raise ValueError(f"Input identifies older RC{incoming}; current manuscript is RC{current}")
    if target_rc is not None and target_rc != incoming:
        raise ValueError("Target RC must match the supplied manuscript RC; uploads are never renumbered")
    marker = f"**Release Candidate {current} (RC{current})**"
    text = text[:markers[0].start()] + marker + text[markers[0].end():]
    return text, {"incoming_rc": incoming, "utf8_bom_removed": raw.startswith(b"\xef\xbb\xbf"),
                  "line_endings_normalised": b"\r" in raw}


def line_matcher(old, new):
    """Trim identical ends first so small edits in a large book stay inexpensive."""
    first = 0
    while first < min(len(old), len(new)) and old[first] == new[first]:
        first += 1
    old_end, new_end = len(old), len(new)
    while old_end > first and new_end > first and old[old_end - 1] == new[new_end - 1]:
        old_end -= 1
        new_end -= 1
    start = max(0, first - 3)
    return difflib.SequenceMatcher(None, old[start:min(len(old), old_end + 3)],
                                  new[start:min(len(new), new_end + 3)], autojunk=False), start


def exact_patches(original, proposed, marker):
    """Generate reversible exact patches; repeated passages fall back to a larger span."""
    old_segments, new_segments = original.split(marker), proposed.split(marker)
    if len(old_segments) != 2 or len(new_segments) != 2:
        raise ValueError("Expected exactly one managed version marker")
    working, patches = original, []
    # Work backwards so later edits cannot move earlier source offsets.
    for side in (1, 0):
        old, new = old_segments[side], new_segments[side]
        if old == new:
            continue
        offset = len(old_segments[0]) + len(marker) if side else 0
        old_lines, new_lines = old.splitlines(keepends=True), new.splitlines(keepends=True)
        matcher, start = line_matcher(old_lines, new_lines)
        groups = list(matcher.get_grouped_opcodes(3))
        candidate, edits = working, []
        for group in reversed(groups):
            a, z, b, y = group[0][1], group[-1][2], group[0][3], group[-1][4]
            a, z, b, y = a + start, z + start, b + start, y + start
            find, replace = "".join(old_lines[a:z]), "".join(new_lines[b:y])
            at = offset + sum(map(len, old_lines[:a]))
            if (not find or candidate.count(find) != 1 or candidate.find(find) != at
                    or "Release Candidate" in find or "Release Candidate" in replace):
                break
            edits.append((find, replace))
            candidate = candidate.replace(find, replace, 1)
        else:
            working = candidate
            patches.extend(edits)
            continue
        # Exact common prefix/suffix keeps the fallback small while adding enough
        # unchanged context to distinguish repeated text and pure insertions.
        start = 0
        while start < min(len(old), len(new)) and old[start] == new[start]:
            start += 1
        end = 0
        while end < min(len(old), len(new)) - start and old[-end - 1] == new[-end - 1]:
            end += 1
        left, right = start, len(old) - end
        while True:
            find = old[left:right]
            replace = old[left:start] + new[start:len(new) - end if end else None] + old[len(old) - end:right]
            if find and working.count(find) == 1 and working.find(find) == offset + left:
                break
            if left == 0 and right == len(old):
                raise ValueError("Cannot form an unambiguous exact patch around the version marker")
            left, right = max(0, left - 64), min(len(old), right + 64)
        if "Release Candidate" in find or "Release Candidate" in replace:
            raise ValueError("An edit overlaps reserved Release Candidate text")
        patches.append((find, replace))
        working = working.replace(find, replace, 1)
    if working != proposed:
        raise ValueError("Generated patches did not reproduce the supplied manuscript exactly")
    return [{"id": f"IMPORT-{i:03d}", "status": "proposed", "find": a, "replace": b, "expected_count": 1}
            for i, (a, b) in enumerate(patches, 1)]


def anchor_model(blocks):
    """Assign the parser's IDs in memory, without writing build or inventory files."""
    from parse_source import plain, slugify
    slugs, table_number = {}, 0

    def walk(sequence):
        nonlocal table_number
        for block in sequence:
            if block["type"] == "heading":
                slug = slugify(plain(block["c"]))
                n = slugs.get(slug, 0)
                slugs[slug] = n + 1
                block["id"] = "h-" + slug + (f"-{n}" if n else "")
            elif block["type"] == "table":
                table_number += 1
                block["id"] = f"T{table_number:03d}"
            else:
                block["id"] = f"B{block['lines'][0] + 1:05d}"
            if block["type"] == "list":
                for item in block["items"]:
                    walk(item["blocks"])
            elif block["type"] == "quote":
                walk(block["blocks"])
    walk(blocks)
    return {"chapters": [{"blocks": blocks}]}


def impact(root, original, proposed):
    from content_anchors import resolve_model
    from figure_dependencies import hashes_for_text
    from parse_source import parse, Unsupported
    blockers, anchors, affected = [], {}, []
    try:
        blocks = parse(proposed)
        definitions = json.loads((root / CONFIGS[0]).read_text(encoding="utf-8"))
        # Collect every broken anchor so one preparation gives a complete repair list.
        model = anchor_model(blocks)
        for key, definition in definitions.items():
            try:
                anchors.update(resolve_model({key: definition}, model))
            except ValueError as exc:
                blockers.append(str(exc))
    except Unsupported as exc:
        blockers.append("Unsupported Markdown: " + str(exc))
    dependencies = json.loads((root / CONFIGS[1]).read_text(encoding="utf-8"))
    try:
        before = hashes_for_text(original, dependencies)
    except ValueError:
        # A companion dependency edit may reference a section introduced by this update.
        before = {}
        for fid, sections in dependencies.items():
            try:
                before.update(hashes_for_text(original, {fid: sections}))
            except ValueError:
                before[fid] = None
    try:
        after = hashes_for_text(proposed, dependencies)
        affected = [fid for fid in dependencies if before[fid] != after[fid]]
    except ValueError:
        # Missing sections are unusual; report each broken dependency in that case.
        for fid, sections in dependencies.items():
            try:
                after_hash = hashes_for_text(proposed, {fid: sections})[fid]
                if before[fid] != after_hash:
                    affected.append(fid)
            except ValueError as exc:
                blockers.append(str(exc))
    matcher, _ = line_matcher(original.splitlines(), proposed.splitlines())
    opcodes = matcher.get_opcodes()
    changed = [op for op in opcodes if op[0] != "equal"]
    return {"blockers": blockers, "anchors_resolved": len(anchors), "affected_figures": affected,
            "lines_added": sum(j2 - j1 for _, i1, i2, j1, j2 in changed),
            "lines_removed": sum(i2 - i1 for _, i1, i2, j1, j2 in changed),
            "line_numbers_shift": any(i2 - i1 != j2 - j1 for _, i1, i2, j1, j2 in changed)}


def analyse(root, raw, target_rc=None):
    root = Path(root)
    old = check(root)
    original = (root / old["path"]).read_text(encoding="utf-8")
    proposed, normalisations = normalise(raw, old["number"], target_rc)
    number = normalisations["incoming_rc"]
    if proposed == original:
        raise ValueError("No manuscript text changes after normalisation; no revision is needed")
    if number <= old["number"]:
        raise ValueError("Uploaded manuscript RC must be higher than the current RC; never overwrite or renumber an upload")
    marker = f"**Release Candidate {old['number']} (RC{old['number']})**"
    patches = exact_patches(original, proposed, marker)
    candidate = proposed.replace(marker, f"**Release Candidate {number} (RC{number})**", 1)
    candidate_bytes = candidate.encode("utf-8")
    report = {"schema": SCHEMA, "base_rc": old["number"], "base_sha256": old["sha256"],
              "next_rc": number, "input_sha256": digest(raw),
              "candidate_sha256": digest(candidate_bytes), "normalisations": normalisations,
              "configuration_sha256": {name: digest((root / name).read_bytes()) for name in CONFIGS},
              "impact": impact(root, original, proposed)}
    batch = {"base_sha256": old["sha256"], "import": {"input_sha256": digest(raw),
             "candidate_sha256": digest(candidate_bytes), "normalisations": normalisations}, "patches": patches}
    if target_rc is not None or number > old["number"] + 1:
        report["target_rc"] = number
        batch["target_rc"] = number
    diff_lines = difflib.unified_diff(original.splitlines(keepends=True), candidate.splitlines(keepends=True),
                                    fromfile=old["path"], tofile=f"source/Heraldry_RC{number}.md")
    diff = "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n" for line in diff_lines)
    return report, batch, candidate_bytes, diff.encode("utf-8")


def review_location(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    if path == root or (path.is_relative_to(root) and not path.is_relative_to(root / "build/manuscript-updates")):
        raise ValueError("Review bundles belong in build/manuscript-updates/ or outside the repository")
    return path


def prepare(root, input_path, review_dir=None, target_rc=None):
    root, input_path = Path(root), Path(input_path)
    if input_path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("Supply a UTF-8 Markdown (.md or .markdown) manuscript")
    raw = input_path.read_bytes()
    report, batch, candidate, diff = analyse(root, raw, target_rc)
    suffix = digest(json_bytes(report["configuration_sha256"]))[:8]
    path = review_location(root, review_dir or root / f"build/manuscript-updates/RC{report['next_rc']}-{digest(raw)[:12]}-{suffix}")
    path.mkdir(parents=True, exist_ok=False)
    payloads = {"incoming.md": raw, "candidate.md": candidate, "proposed-patches.json": json_bytes(batch), "changes.diff": diff}
    for name, data in payloads.items():
        (path / name).write_bytes(data)
    report["files"] = {name: digest(data) for name, data in payloads.items()}
    (path / "summary.json").write_bytes(json_bytes(report))
    state = "BLOCKED: repair the listed bindings/format and prepare again." if report["impact"]["blockers"] else "READY FOR OWNER REVIEW. No revision has been applied."
    effects = report["impact"]
    details = (f"- Text lines: +{effects['lines_added']} / -{effects['lines_removed']} (excluding the RC marker).\n"
               f"- Content anchors resolved: {effects['anchors_resolved']}.\n"
               f"- Figures needing semantic review: {', '.join(effects['affected_figures']) or 'none'}.\n"
               f"- Normalisations: {json.dumps(report['normalisations'])}.\n"
               f"- Candidate SHA-256: `{report['candidate_sha256']}`.\n")
    if effects["blockers"]:
        details += "\n" + "\n".join("- BLOCKED: " + item for item in effects["blockers"]) + "\n"
    citations = ("Source line numbers shift: inspect figure source citations before regenerating figures; no citations are automatically remapped.\n"
                 if effects["line_numbers_shift"] else "")
    (path / "REVIEW.md").write_bytes((f"# Manuscript update RC{report['base_rc']} to RC{report['next_rc']}\n\n{state}\n\n"
        + details + "\n"
        "Read changes.diff, candidate.md, and summary.json. Confirm every edit is intended.\n"
        "Affected figures require an actual semantic review before the next release.\n" + citations + "\n"
        "To apply the reviewed content, run from the repository:\n\n```sh\n"
        f'python tools/dev.py manuscript apply --review-dir "{path.as_posix()}" --approve '
        '--reason "Describe this update" --authorization "Actual owner instruction/date"\n```\n\n'
        "This creates one new immutable RC through revise_manuscript.py. It does not commit, push, build a PDF, or renew a review ledger.\n").encode("utf-8"))
    return path, report


def apply_review(root, review_dir, reason, authorization, approve=False):
    if not approve:
        raise ValueError("Review the diff and candidate, then pass --approve to authorise exactly this batch")
    if not reason.strip() or not authorization.strip():
        raise ValueError("A concrete reason and actual owner authorization are required")
    root, path = Path(root), review_location(root, review_dir)
    recorded = json.loads((path / "summary.json").read_text(encoding="utf-8"))
    if not isinstance(recorded, dict) or recorded.get("schema") != SCHEMA:
        raise ValueError("Unsupported review bundle schema; prepare again")
    for name in ("incoming.md", "candidate.md", "proposed-patches.json", "changes.diff"):
        if digest((path / name).read_bytes()) != recorded.get("files", {}).get(name):
            raise ValueError(f"Review bundle changed: {name}; prepare and review again")
    current = check(root)
    if current["sha256"] != recorded.get("base_sha256"):
        raise ValueError("Review base is stale; prepare against the current manuscript and review again")
    report, batch, candidate, diff = analyse(root, (path / "incoming.md").read_bytes(), recorded.get("target_rc"))
    if report != {key: value for key, value in recorded.items() if key != "files"}:
        raise ValueError("Review analysis/configuration changed; prepare and review again")
    if (candidate != (path / "candidate.md").read_bytes() or diff != (path / "changes.diff").read_bytes()
            or json_bytes(batch) != (path / "proposed-patches.json").read_bytes()):
        raise ValueError("Review bundle no longer reproduces exactly; prepare again")
    if report["impact"]["blockers"]:
        raise ValueError("Review is blocked: " + "; ".join(report["impact"]["blockers"]))
    for patch in batch["patches"]:
        patch["status"] = "approved"
    approved = path / "approved-patches.json"
    approved.write_bytes(json_bytes(batch))
    return revise(root, approved, reason, authorization)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare", help="prepare a review bundle without changing the active manuscript")
    prep.add_argument("--input", required=True, type=Path)
    prep.add_argument("--review-dir", type=Path)
    prep.add_argument("--target-rc", type=int, help="optional assertion of the uploaded RC number; cannot renumber it")
    apply = sub.add_parser("apply", help="promote an explicitly approved review to its reviewed RC")
    apply.add_argument("--review-dir", required=True, type=Path)
    apply.add_argument("--approve", action="store_true")
    apply.add_argument("--reason", required=True)
    apply.add_argument("--authorization", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            path, report = prepare(ROOT, args.input, args.review_dir, args.target_rc)
            print(f"Review bundle: {path}")
            print(f"RC{report['base_rc']} -> RC{report['next_rc']}: +{report['impact']['lines_added']} / -{report['impact']['lines_removed']} text lines")
            print("Affected figures: " + (", ".join(report["impact"]["affected_figures"]) or "none"))
            for blocker in report["impact"]["blockers"]:
                print("BLOCKED: " + blocker)
            print("Read REVIEW.md and changes.diff. Active manuscript and released PDFs are unchanged.")
            return 1 if report["impact"]["blockers"] else 0
        if not args.approve:
            raise ValueError("Review the diff and candidate, then pass --approve to authorise exactly this batch")
        require_current_main(ROOT, allowed_changes=CONFIGS)
        record = apply_review(ROOT, args.review_dir, args.reason, args.authorization, args.approve)
        print(f"Applied RC{record['number']}: {record['path']} ({record['sha256']})")
        print("Update STATE.md, then commit all four revision files together. No PDF build was requested.")
        return 0
    except (ValueError, OSError, KeyError, RevisionRecoveryError, PublishError) as exc:
        print("FAILED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
