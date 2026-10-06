"""Resolve persistent publication anchors by section and exact text prefix.

Line-based parser IDs may change between revisions; sidecar anchors must not silently
attach to an unrelated block that happens to inherit the old line number.
"""
import json
from manuscript import ROOT


def text_of(block):
    from parse_source import plain
    if block["type"] in {"para", "heading"}:
        return plain(block["c"])
    if block["type"] == "table":
        return " | ".join(plain(c) for row in [block["header"]] + block["rows"] for c in row)
    return " ".join(text_of(b) for it in block.get("items", []) for b in it["blocks"])


def resolve(root=ROOT):
    definitions = json.loads((root / "config/content_anchors.json").read_text())
    model = json.loads((root / "build/blocks.json").read_text())
    candidates = []
    section = None
    for ch in model["chapters"]:
        for b in ch["blocks"]:
            if b["type"] == "heading":
                section = b["id"]
            candidates.append((section, b))
    result = {}
    for key, a in definitions.items():
        hits = [b["id"] for section, b in candidates if section == a["section"]
                and b["type"] == a["type"] and text_of(b).startswith(a["prefix"])]
        if len(hits) != 1:
            raise ValueError(f"Anchor {key}: {len(hits)} matches; explicitly update its section/prefix")
        result[key] = hits[0]
    return result
