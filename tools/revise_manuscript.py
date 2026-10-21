#!/usr/bin/env python3
"""Create the next immutable RC snapshot from an authorized exact text-patch batch."""
import argparse
import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from manuscript import ROOT, check, load


class RevisionRecoveryError(RuntimeError):
    """An operating-system error prevented complete transaction rollback."""


def _json_bytes(data):
    # Write bytes so Windows newline translation cannot alter the serialized evidence.
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


@contextmanager
def _revision_lock(root):
    path = root / "source/.revision.lock"
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(f"Another revision or an interrupted transaction owns {path}; inspect it before retrying") from exc
    recovery_required = False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(f"Manuscript revision transaction, PID {os.getpid()}\n".encode("ascii"))
        yield
    except RevisionRecoveryError:
        recovery_required = True
        raise
    finally:
        if not recovery_required:
            path.unlink()


def _stage_bytes(path, data):
    """Fully write a temporary file beside its destination before publishing it."""
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    staged = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def _publish_revision(root, payloads, originals):
    """Publish a four-file revision, restoring exact original bytes on failure.

    No-clobber hard links publish new immutable files; replacements publish mutable
    metadata. This protects existing revision numbers even if another writer ignores
    the lock. Ordinary write/check failures roll back. A killed process or failing
    storage still needs inspection of the retained lock/temporary recovery files.
    """
    staged, backups, published = {}, {}, []
    recovery_required = False
    try:
        for path, data in payloads.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            staged[path] = _stage_bytes(path, data)
        for path, data in originals.items():
            backups[path] = _stage_bytes(path, data)
        for path, data in originals.items():
            if path.read_bytes() != data:
                raise ValueError(f"Revision state changed while preparing the transaction: {path}")
        for path in payloads:
            if path in originals:
                os.replace(staged[path], path)
            else:
                # Unlike replace(), link() refuses an existing file, including a symlink.
                os.link(staged[path], path)
            published.append(path)
        check(root)
    except BaseException as failure:
        rollback_errors = []
        for path in reversed(published):
            try:
                if path in originals:
                    os.replace(backups[path], path)
                else:
                    path.unlink()
            except OSError as exc:
                rollback_errors.append(f"{path}: {exc}")
        if rollback_errors:
            recovery_required = True
            raise RevisionRecoveryError(
                "Revision rollback needs inspection; lock and recovery files retained. "
                + "; ".join(rollback_errors)
            ) from failure
        raise
    finally:
        if not recovery_required:
            for path in (*staged.values(), *backups.values()):
                path.unlink(missing_ok=True)


def revise(root, patch_path, reason, authorization):
    root, patch_path = Path(root), Path(patch_path)
    with _revision_lock(root):
        return _revise(root, patch_path, reason, authorization)


def _revise(root, patch_path, reason, authorization):
    old = check(root)
    registry = load(root)
    raw = patch_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() in {r.get("patch_sha256") for r in registry["revisions"]}:
        raise ValueError("This exact patch batch is already archived; do not apply it twice")
    batch = json.loads(raw)
    if not isinstance(batch, dict):
        raise ValueError("A patch batch must be a JSON object")
    if "base_sha256" in batch and batch["base_sha256"] != old["sha256"]:
        raise ValueError("Patch batch base_sha256 differs from the current manuscript; prepare it again")
    patches = batch.get("patches", [])
    if not isinstance(reason, str) or not isinstance(authorization, str) or not reason.strip() or not authorization.strip() or not isinstance(patches, list) or not patches:
        raise ValueError("A nonempty authorized patch batch and reason are required")
    text = (root / old["path"]).read_text(encoding="utf-8")
    seen = set()
    for p in patches:
        if not isinstance(p, dict) or not isinstance(p.get("id"), str) or not p["id"].strip() or p["id"] in seen:
            raise ValueError("Missing or duplicate patch ID")
        seen.add(p["id"])
        if p.get("status") not in {"approved", "applied"}:
            raise ValueError(f"{p['id']}: patch is not approved")
        if not isinstance(p.get("find"), str) or not isinstance(p.get("replace"), str) or not p["find"] or p["find"] == p["replace"]:
            raise ValueError(f"{p['id']}: empty/no-op patch")
        n = text.count(p["find"])
        expected = p.get("expected_count", 1)
        if isinstance(expected, bool) or not isinstance(expected, int) or expected < 1 or n != expected:
            raise ValueError(f"{p['id']}: matched {n}, expected {expected}")
        if "Release Candidate" in p["find"] or "Release Candidate" in p["replace"]:
            raise ValueError("The tool owns the version marker")
        text = text.replace(p["find"], p["replace"])
    original = (root / old["path"]).read_text(encoding="utf-8")
    if text == original:
        raise ValueError("Batch has no net text change")
    number = batch.get("target_rc", old["number"] + 1)
    if type(number) is not int or number <= old["number"]:
        raise ValueError("Target RC must be an integer greater than the current RC")
    if number != old["number"] + 1 and not isinstance(batch.get("import"), dict):
        raise ValueError("Version jumps require a reviewed manuscript import")
    old_marker = f"**Release Candidate {old['number']} (RC{old['number']})**"
    new_marker = f"**Release Candidate {number} (RC{number})**"
    if text.count(old_marker) != 1:
        raise ValueError("Expected exactly one version marker")
    text = text.replace(old_marker, new_marker, 1)
    output = root / f"source/Heraldry_RC{number}.md"
    evidence = root / f"editorial/history/RC{number}.json"
    if os.path.lexists(output) or os.path.lexists(evidence):
        raise ValueError("Revision already exists; never overwrite or reuse a number")
    data = text.encode("utf-8")
    imported = batch.get("import")
    if isinstance(imported, dict) and imported.get("candidate_sha256") != hashlib.sha256(data).hexdigest():
        raise ValueError("Imported candidate differs from the reviewed manuscript hash")
    record = {"number": number, "path": output.relative_to(root).as_posix(),
              "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
              "parent_sha256": old["sha256"], "created_at": datetime.now(timezone.utc).isoformat(),
              "reason": reason, "authorization": authorization,
              "patch_ids": list(p["id"] for p in patches),
              "patch_file": evidence.relative_to(root).as_posix(),
              "patch_sha256": hashlib.sha256(raw).hexdigest()}
    config_path, registry_path = root / "config/production.json", root / "source/versions.json"
    originals = {path: path.read_bytes() for path in (config_path, registry_path)}
    config = json.loads(originals[config_path])
    config["source"] = record["path"]
    config["source_authority"] = "Active immutable snapshot in source/versions.json; prior snapshots retained"
    config["verified_publication_metadata"]["version"] = f"Release Candidate {number} (RC{number})"
    registry["current"] = number
    registry["revisions"].append(record)
    # Publish these four files together in one Git commit after the transaction succeeds.
    _publish_revision(root, {output: data, evidence: raw,
                             config_path: _json_bytes(config), registry_path: _json_bytes(registry)}, originals)
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
