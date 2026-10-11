#!/usr/bin/env python3
"""Validate the built skill package, and its agreement with a Heraldry repo checkout.

  python scripts/validate_skill.py --zip skill.zip                an unextracted zip (the normal case)
  python scripts/validate_skill.py                                an extracted, built skill folder
  python scripts/validate_skill.py --zip skill.zip --repo PATH    name the repo explicitly

The repo is found by walking up from the current directory when --repo is not given. The skill source folder inside
the repo has no manifest or reference images until tools/art_skill_build.py builds them, so validate the zip.
Only reads files. Python files are compiled to check syntax, never run."""
import argparse, hashlib, json, re, sys, tempfile, zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:                                           # pragma: no cover
    sys.exit("Pillow is required: pip install pillow")

HERE = Path(__file__).resolve().parents[1]
SIZES = {"3:2": "1536x1024", "2:3": "1024x1536", "1:1": "1024x1024"}
REQUIRED = ["SKILL.md", "README.md", "OPERATOR_CARD.md", "manifest.json", "scripts/heraldry_art.py", "scripts/validate_skill.py",
            "references/STYLE.md", "references/QA_CHECKLIST.md", "references/REPAIR.md", "references/FAMILIES.md",
            "references/AD_HOC.md", "references/images/SOURCES.json",
            "references/STYLE_CONSISTENCY.md", "references/WORK_OPERATIONS.md",
            "scripts/fidelity_gate.py", "scripts/work_preflight.py", "scripts/delivery_guard.py", "scripts/style_audit.py",
            "references/VISUAL_ACCEPTANCE.md", "VERIFICATION_REPORT.md"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def find_repo():
    here = Path.cwd().resolve()
    for d in [here, *here.parents]:
        if (d / "production/art/gpt/QUEUE.json").is_file() and (d / "config/art_style.json").is_file():
            return d
    return None


def check_package(base):
    errors = []
    for rel in REQUIRED:
        if not (base / rel).is_file():
            errors.append(f"missing {rel}")
    mf = base / "manifest.json"
    manifest = json.loads(mf.read_text()) if mf.is_file() else {"files": {}}
    if manifest.get("version") != "7.0.0":
        errors.append("expected v7.0.0 manifest")
    on_disk = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts} - {"manifest.json"}
    for rel, rec in manifest["files"].items():
        f = base / rel
        if not f.is_file():
            errors.append(f"manifest lists a missing file: {rel}")
        elif sha(f.read_bytes()) != rec["sha256"] or f.stat().st_size != rec["bytes"]:
            errors.append(f"hash mismatch: {rel}")
    for rel in sorted(on_disk - set(manifest["files"])):
        errors.append(f"file not in manifest: {rel}")
    skill = (base / "SKILL.md").read_text() if (base / "SKILL.md").is_file() else ""
    m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", skill)
    if not m or m.group(1) != "heraldry-classic-ink-art":
        errors.append("SKILL.md front matter must be name then description, name heraldry-classic-ink-art")
    elif len(m.group(2)) > 1024:
        errors.append("SKILL.md description exceeds 1024 characters")
    for ref in set(re.findall(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`", skill)):
        if not (base / ref).exists():
            errors.append(f"SKILL.md names a missing file: {ref}")
    for py in (base / "scripts").glob("*.py"):
        try:
            compile(py.read_text(), str(py), "exec")
        except SyntaxError as e:
            errors.append(f"{py.name}: {e}")
    src = base / "references/images/SOURCES.json"
    images = json.loads(src.read_text())["images"] if src.is_file() else []
    for rec in images:
        f = base / rec["file"]
        try:
            with Image.open(f) as im:
                im.verify()
            if sha(f.read_bytes()) != rec["sha256"]:
                errors.append(f"{rec['file']}: differs from SOURCES.json")
        except Exception as e:
            errors.append(f"{rec['file']}: unreadable image ({e})")
    return errors, images


def check_repo(base, repo, images):
    errors = []
    for rec in images:
        f = repo / rec["repo_path"]
        if not f.is_file():
            errors.append(f"repo file missing: {rec['repo_path']}")
        elif sha(f.read_bytes()) != rec["sha256"]:
            errors.append(f"{rec['repo_path']} differs from the copy in the skill: rebuild with tools/art_skill_build.py")
    cfg = json.loads((repo / "config/art_style.json").read_text())
    rows = {}
    for line in (base / "references/FAMILIES.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[0] in cfg["families"]:
            rows[cells[0]] = cells
    att = cfg["gpt_max_attempts"]
    for fam, spec in cfg["families"].items():
        want = [fam, cfg["gpt_reference_sets"]["register_of_family"][fam], SIZES[spec["aspect"]], f"{spec['print_w_in']} in", str(att.get(fam, att["default"]))]
        if rows.get(fam, [])[:5] != want:
            errors.append(f"FAMILIES.md row for {fam} is {rows.get(fam, [])[:5]}, repo says {want}")
    qf = repo / "production/art/gpt/QUEUE.json"
    if not qf.is_file():
        errors.append("QUEUE.json not found in the repo")
    else:
        q = json.loads(qf.read_text())
        if q.get("schema", 1) < 2:
            errors.append("QUEUE.json is schema 1")
        for it in q["items"]:
            pf = repo / it["prompt"]
            text = pf.read_text() if pf.is_file() else None
            if text is None or sha((text[:-1] if text.endswith("\n") else text).encode()) != it["prompt_sha256"]:
                errors.append(f"{it['id']}: prompt file missing or not matching the queue hash")
            for r in it["references"]:
                if not (repo / r).is_file():
                    errors.append(f"{it['id']}: reference missing {r}")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zip", type=Path)
    ap.add_argument("--repo", type=Path)
    a = ap.parse_args()
    tmp = None
    base = HERE
    errors = []
    if a.zip:
        tmp = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(a.zip) as z:
            if len(z.namelist()) != len(set(z.namelist())):
                errors.append("duplicate ZIP member names")
            if any((x.external_attr >> 16) & 0o170000 == 0o120000 for x in z.infolist()):
                errors.append("ZIP contains symlinks")
            if any(n.startswith("/") or ".." in Path(n).parts or "\\" in n for n in z.namelist()):
                errors.append("unsafe ZIP traversal path")
                print(json.dumps({"status":"FAIL","errors":errors},indent=2))
                return 1
            if errors:
                print(json.dumps({"status":"FAIL","errors":errors},indent=2))
                return 1
            if z.testzip() is not None:
                errors.append("zip CRC error")
            if "SKILL.md" not in z.namelist():
                errors.append("SKILL.md is not at the zip root")
            z.extractall(tmp.name)
        base = Path(tmp.name)
    repo = a.repo.resolve() if a.repo else find_repo()
    repo_checks = "skipped: no repo found; pass --repo <clone>"
    if not a.zip and not (base / "manifest.json").is_file():
        errors.append("this folder has no manifest.json: it is the skill source, not a built package. "
                      "Build it with tools/art_skill_build.py, then validate the zip with --zip")
        repo_checks = "skipped: not a built package"
    else:
        pk, images = check_package(base)
        errors += pk
        if repo:
            errors += check_repo(base, repo, images)
            repo_checks = "done"
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "checked": str(a.zip or base),
                      "repo": str(repo) if repo else None, "repo_checks": repo_checks, "errors": errors}, indent=1))
    if tmp:
        tmp.cleanup()
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
