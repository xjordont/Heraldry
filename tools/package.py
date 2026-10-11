#!/usr/bin/env python3
"""Package the current verified revision; external audit describes the finished ZIP."""
import hashlib
import json
import zipfile
from pathlib import Path
from manuscript import ROOT, check, version
from provenance import check as check_build

DIST = ROOT / "dist"
INCLUDE = ["Makefile", "requirements.lock", "README.md", "README_SETUP.md", "BUILD.md", "CLAUDE.md",
           "MASTER_PROMPT.md", ".gitignore", ".claude", ".github", "tests", "references",
           "source", "editorial", "typst", "tools", "figures", "fonts", "config", "docs", "assets", "production", "dist"]
# style = owner-supplied generation references (never packaged); masters = raw generated art (ink derivatives ship)
EXCLUDE_PARTS = {"__pycache__", "test", "private", ".git", "build", "overscan", "style", "masters"}
EXCLUDE_NAMES = {"content.typ", "SHA256SUMS.txt", "package-audit.json"}
LFS_POINTER = b"version https://git-lfs"


def generated_natives():
    """Native generated images in assets/art/incoming (recorded in SELECTIONS.json): raw art like masters/, so only
    their ink derivatives ship. The twelve legacy atmospheric masters are not in SELECTIONS and still ship."""
    sels = ROOT / "production/art/SELECTIONS.json"
    return set(json.loads(sels.read_text())) if sels.is_file() else set()


def files():
    natives = generated_natives()
    for top in INCLUDE:
        p = ROOT / top
        for f in ([p] if p.is_file() else sorted(p.rglob("*"))):
            rel = f.relative_to(ROOT)
            if not f.is_file() or set(rel.parts) & EXCLUDE_PARTS or f.name in EXCLUDE_NAMES:
                continue
            if f.suffix in {".pyc", ".zip", ".pem"} or f.name.startswith(".env"):
                continue
            if rel.parts[0] == "dist" and f.name.startswith("Heraldry_") and not f.name.startswith(f"Heraldry_{version()}_"):
                continue
            if rel.parts[:3] == ("assets", "art", "incoming") and f.stem in natives:
                continue
            with f.open("rb") as fh:
                if fh.read(len(LFS_POINTER)) == LFS_POINTER:
                    raise SystemExit(f"{rel} is a Git LFS pointer: fetch it before packaging")
            yield f


def main():
    check()
    provenance = check_build()
    status = json.loads((ROOT / "production/qa/STATUS.json").read_text())
    if status.get("release_gate") != "PASS" or status.get("provenance") != provenance:
        raise SystemExit("Current build has no matching passing verification; run make verify")
    archive = DIST / f"Heraldry_{version()}_release.zip"
    prefix = Path(f"Heraldry_{version()}")
    fl = list(files())
    sums = "\n".join(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(ROOT)}" for f in fl) + "\n"
    (DIST / "SHA256SUMS.txt").write_text(sums)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in fl:
            z.write(f, prefix / f.relative_to(ROOT))
        z.writestr(str(prefix / "SHA256SUMS.txt"), sums)
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or z.testzip():
            raise SystemExit("Duplicate or corrupt ZIP entry")
        for f in fl:
            if z.read(str(prefix / f.relative_to(ROOT))) != f.read_bytes():
                raise SystemExit(f"Archive content mismatch: {f}")
    rep = {"zip": str(archive.relative_to(ROOT)), "bytes": archive.stat().st_size,
           "files": len(names), "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
           "status": "PASS", "duplicate_entries": [], "checksums_verified": len(fl),
           "note": "This audit is external to the ZIP to avoid self-reference; PDFs are verified files, visual and physical proof statuses remain separately qualified."}
    (ROOT / "production/qa/package-audit.json").write_text(json.dumps(rep, indent=2) + "\n")
    print(json.dumps(rep))


if __name__ == "__main__":
    main()
