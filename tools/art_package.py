#!/usr/bin/env python3
"""Package the reviewed atmospheric suite, independently of the PDF release."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from check_art import ROOT, main as check_art


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    check_art()
    manifest = json.loads((ROOT / "production/art/ART_MANIFEST.json").read_text())
    names = [a["native_master"]["path"] for a in manifest["assets"]]
    names += ["production/art/ART_MANIFEST.json", "production/art/PROMPTS.json",
              "production/art/HANDOFF.md", "docs/ART_AUTOMATION.md",
              "docs/ART_DIRECTION.md", "tools/check_art.py", "tools/art_package.py"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    prefix = "Heraldry_artwork/"
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        sums = []
        for name in names:
            data = (ROOT / name).read_bytes()
            archive.writestr(prefix + name, data)
            sums.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
        archive.writestr(prefix + "SHA256SUMS.txt", "\n".join(sums) + "\n")
    with zipfile.ZipFile(args.output) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())) or archive.testzip():
            raise ValueError("Invalid artwork archive")
        for name in names:
            if archive.read(prefix + name) != (ROOT / name).read_bytes():
                raise ValueError("Artwork ZIP differs from native source")
    print(json.dumps({"zip": str(args.output), "bytes": args.output.stat().st_size,
                      "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      "status": "PASS", "scope": "Artwork suite; PDF integration still pending"}))


if __name__ == "__main__":
    main()

