#!/usr/bin/env python3
"""Create the next immutable RC snapshot from an authorized exact text-patch batch."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from manuscript import ROOT, check, load


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def revise(root, patch_path, reason, authorization):
    root, patch_path = Path(root), Path(patch_path)
    old = check(root)
    registry = load(root)
    raw = patch_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() in {r.get("patch_sha256") for r in registry["revisions"]}:
        raise ValueError("This exact patch batch is already archived; do not apply it twice")
    batch = json.loads(raw)
    patches = batch.get("patches", [])
    if not reason.strip() or not authorization.strip() or not patches:
        raise ValueError("A nonempty authorized patch batch and reason are required")
    text = (root / old["path"]).read_text(encoding="utf-8")
    seen = set()
    for p in patches:
        if not p.get("id") or p["id"] in seen:
            raise ValueError("Missing or duplicate patch ID")
        seen.add(p["id"])
        if p.get("status") not in {"approved", "applied"}:
            raise ValueError(f"{p['id']}: patch is not approved")
        if not p.get("find") or p["find"] == p["replace"]:
            raise ValueError(f"{p['id']}: empty/no-op patch")
        n = text.count(p["find"])
        expected = p.get("expected_count", 1)
        if not isinstance(expected, int) or expected < 1 or n != expected:
            raise ValueError(f"{p['id']}: matched {n}, expected {expected}")
        if "Release Candidate" in p["find"] or "Release Candidate" in p["replace"]:
            raise ValueError("The tool owns the version marker")
        text = text.replace(p["find"], p["replace"])
    original = (root / old["path"]).read_text(encoding="utf-8")
    if text == original:
        raise ValueError("Batch has no net text change")
    number = old["number"] + 1
    old_marker = f"**Release Candidate {old['number']} (RC{old['number']})**"
    new_marker = f"**Release Candidate {number} (RC{number})**"
    if text.count(old_marker) != 1:
        raise ValueError("Expected exactly one version marker")
    text = text.replace(old_marker, new_marker, 1)
    output = root / f"source/Heraldry_RC{number}.md"
    evidence = root / f"editorial/history/RC{number}.json"
    if output.exists() or evidence.exists():
        raise ValueError("Revision already exists; never overwrite or reuse a number")
    data = text.encode("utf-8")
    record = {"number": number, "path": output.relative_to(root).as_posix(),
              "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
              "parent_sha256": old["sha256"], "created_at": datetime.now(timezone.utc).isoformat(),
              "reason": reason, "authorization": authorization,
              "patch_ids": list(p["id"] for p in patches),
              "patch_file": evidence.relative_to(root).as_posix(),
              "patch_sha256": hashlib.sha256(raw).hexdigest()}
    config = json.loads((root / "config/production.json").read_text())
    config["source"] = record["path"]
    config["source_authority"] = "Active immutable snapshot in source/versions.json; prior snapshots retained"
    config["verified_publication_metadata"]["version"] = f"Release Candidate {number} (RC{number})"
    registry["current"] = number
    registry["revisions"].append(record)
    # Validate everything before writing. Publish these files together in one Git commit.
    output.write_bytes(data)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_bytes(raw)
    dump(root / "config/production.json", config)
    dump(root / "source/versions.json", registry)
    check(root)
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--patches", required=True, type=Path)
    p.add_argument("--reason", required=True)
    p.add_argument("--authorization", required=True, help="Actual owner instruction/date or decision reference")
    a = p.parse_args()
    print(json.dumps(revise(ROOT, a.patches, a.reason, a.authorization), indent=2))


if __name__ == "__main__":
    main()
