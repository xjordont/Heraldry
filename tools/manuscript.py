"""Single manuscript authority shared by revision, build and QA commands."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_SHA = "2744833106569e6b20f6913340de5d80c7869782556e23b8f738a0407e4f16f3"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(root=ROOT):
    return json.loads((Path(root) / "source/versions.json").read_text(encoding="utf-8"))


def active(root=ROOT):
    m = load(root)
    return m["revisions"][-1]


def version(root=ROOT):
    return f"RC{active(root)['number']}"


def pdf_epoch(root=ROOT):
    from datetime import datetime
    return int(datetime.fromisoformat(active(root).get("created_at", "2026-10-01T00:00:00+00:00")).timestamp())


def source_path(root=ROOT):
    return Path(root) / active(root)["path"]


def check(root=ROOT):
    root = Path(root)
    m = load(root)
    revisions = m["revisions"]
    if not revisions or revisions[0]["number"] != 484 or revisions[0]["sha256"] != ORIGINAL_SHA:
        raise ValueError("Original RC484 authority changed")
    previous = None
    for r in revisions:
        expected = f"source/Heraldry_RC{r['number']}.md"
        if r["path"] != expected or sha256(root / expected) != r["sha256"] or (root / expected).stat().st_size != r["bytes"]:
            raise ValueError(f"Snapshot altered: {expected}; create a new revision instead")
        if previous and (r["number"] != previous["number"] + 1 or r.get("parent_sha256") != previous["sha256"]):
            raise ValueError("Revision sequence or parent hash broken")
        if previous and not (r.get("reason") and r.get("authorization")):
            raise ValueError("Revision needs reason and authorization")
        if r.get("patch_file") and sha256(root / r["patch_file"]) != r["patch_sha256"]:
            raise ValueError("Archived patch evidence altered")
        if previous:
            parent_text = (root / previous["path"]).read_text(encoding="utf-8")
            rebuilt = parent_text
            evidence = json.loads((root / r["patch_file"]).read_text(encoding="utf-8"))
            patches = evidence["patches"]
            if [p["id"] for p in patches] != r["patch_ids"] or not patches:
                raise ValueError("Revision patch IDs differ from its evidence")
            for p in patches:
                if p.get("status") not in {"approved", "applied"} or not p.get("find") or rebuilt.count(p["find"]) != p.get("expected_count", 1):
                    raise ValueError("Revision cannot be reconstructed from approved exact patches")
                rebuilt = rebuilt.replace(p["find"], p["replace"])
            if rebuilt == parent_text:
                raise ValueError("Revision has no manuscript text change")
            rebuilt = rebuilt.replace(f"**Release Candidate {previous['number']} (RC{previous['number']})**", f"**Release Candidate {r['number']} (RC{r['number']})**", 1)
            if rebuilt != (root / expected).read_text(encoding="utf-8"):
                raise ValueError("Snapshot differs from its recorded patches")
        marker = f"**Release Candidate {r['number']} (RC{r['number']})**"
        if marker not in (root / expected).read_text(encoding="utf-8"):
            raise ValueError("Snapshot version marker differs")
        previous = r
    current = revisions[-1]
    if m["current"] != current["number"]:
        raise ValueError("Current revision is not the newest snapshot")
    c = json.loads((root / "config/production.json").read_text(encoding="utf-8"))
    if c["source"] != current["path"] or c["verified_publication_metadata"]["version"] != f"Release Candidate {current['number']} (RC{current['number']})":
        raise ValueError("Production configuration differs from revision registry")
    patches = json.loads((root / "editorial/patches.json").read_text(encoding="utf-8"))
    if patches.get("patches"):
        raise ValueError("Publication-only text patches are disabled; promote them to a new manuscript revision")
    return current


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--version", action="store_true")
    a = p.parse_args()
    print(version() if a.version else json.dumps(check(), indent=2))
