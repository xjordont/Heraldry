#!/usr/bin/env python3
"""Assemble dist/Heraldry_RC484_release.zip with SHA-256 checksums.
Includes deliverable PDFs, editable sources, fonts + licences, figures, ledgers and QA evidence.
Excludes build intermediates, caches, page renders, credentials and reference material."""
import hashlib, json, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ZIP = DIST / "Heraldry_RC484_release.zip"

INCLUDE = ["Makefile", "requirements.lock", "README.md", "BUILD.md", "CLAUDE.md", "MASTER_PROMPT.md",
           "source", "editorial", "typst", "tools", "figures", "fonts", "config", "docs", "assets",
           "production", "dist"]
EXCLUDE_PARTS = {"__pycache__", "test", "private", ".git", "build"}
EXCLUDE_NAMES = {"content.typ", ZIP.name, ".env"}


def files():
    for top in INCLUDE:
        p = ROOT / top
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                rel = f.relative_to(ROOT)
                if f.is_file() and not (set(rel.parts) & EXCLUDE_PARTS) and f.name not in EXCLUDE_NAMES \
                        and not f.suffix in (".pyc",) and "overscan" not in rel.parts:
                    yield f


def main():
    sums = []
    fl = list(files())
    for f in fl:
        sums.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(ROOT)}")
    (DIST / "SHA256SUMS.txt").write_text("\n".join(s for s in sums if not s.endswith("dist/SHA256SUMS.txt")) + "\n")
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in fl:
            z.write(f, Path("Heraldry_RC484") / f.relative_to(ROOT))
        z.write(DIST / "SHA256SUMS.txt", Path("Heraldry_RC484") / "SHA256SUMS.txt")
    # audit archive contents
    with zipfile.ZipFile(ZIP) as z:
        names = z.namelist()
    bad = [n for n in names if any(k in n.lower() for k in (".env", ".pem", "references/private", "page-renders", "__pycache__"))]
    pdfs = [n for n in names if n.endswith(".pdf")]
    rep = {"zip": str(ZIP.relative_to(ROOT)), "bytes": ZIP.stat().st_size, "files": len(names), "pdfs": pdfs,
           "forbidden_entries": bad, "sha256": hashlib.sha256(ZIP.read_bytes()).hexdigest()}
    (ROOT / "production/qa/package-audit.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({k: rep[k] for k in ("zip", "bytes", "files", "forbidden_entries")}))
    if bad:
        raise SystemExit("forbidden entries in archive")


if __name__ == "__main__":
    main()
