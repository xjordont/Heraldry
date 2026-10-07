#!/usr/bin/env python3
"""Verify the exact atmospheric masters and their native placement limits."""
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "production/art/ART_MANIFEST.json").read_text())
    expected = {"ART-COVER-001"} | {f"ART-CH{i:02d}-001" for i in range(1, 12)}
    assets = manifest["assets"]
    if len(assets) != 12 or {a["asset_id"] for a in assets} != expected:
        raise ValueError("Expected the twelve distinct required artwork assets")
    for asset in assets:
        native = asset["native_master"]
        rel = Path(native["path"])
        if rel.parts != ("assets", "art", "incoming", asset["asset_id"] + ".png"):
            raise ValueError("Unexpected artwork path")
        data = (ROOT / rel).read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            raise ValueError(f"{rel}: native PNG missing; fetch Git LFS objects")
        width, height, depth, colour = struct.unpack(">IIBB", data[16:26])
        if (width, height, depth, colour) != (native["width_px"], native["height_px"], 8, 6):
            raise ValueError(f"{rel}: expected native 8-bit RGBA dimensions")
        if len(data) != native["bytes"] or hashlib.sha256(data).hexdigest() != native["sha256"]:
            raise ValueError(f"{rel}: master differs from the reviewed asset")
        pw, ph = asset["intended_printed_size_in"]
        if not (0 < pw <= width / 300 and 0 < ph <= height / 300):
            raise ValueError(f"{rel}: placement exceeds native 300ppi limit")
    print("PASS: 12 native artwork masters, SHA256, dimensions and 300ppi placement limits")


if __name__ == "__main__":
    main()
