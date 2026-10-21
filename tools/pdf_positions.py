"""Read position evidence serialized by the PDF's own Typst layout.

Never attach a new `typst query` result to an existing PDF: a query compiles a
document again. The JSON attachment is created inside the PDF export instead.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pypdf

from manuscript import ROOT, pdf_epoch
from provenance import inputs

ATTACHMENT = "heraldry-positions.json"
SELECTORS = ("<pm>", "<tblpos>", "<ixpos>", "<hpos>", "<um-pos>")
GENERATED_INPUTS = ("build/blocks.json", "build/index.json", "build/cover.json")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compilation_identity(root=ROOT, variant="cream", edition="print", content=None):
    """Fingerprint complete publication inputs plus generated compiler inputs."""
    import typst
    root = Path(root)
    content = Path(content) if content is not None else root / "typst/content.typ"
    inventory = inputs(root)
    for name in GENERATED_INPUTS:
        p = root / name
        if p.exists():
            inventory[name] = digest(p)
    return {
        "schema": 1,
        "content_sha256": digest(content),
        "input_sha256": hashlib.sha256(json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "variant": variant, "edition": edition,
        "compiler": typst.__version__, "timestamp": pdf_epoch(root),
    }


def read_positions(pdf, *, root=ROOT, current=True, variant="cream", edition="print", content=None):
    """Extract and validate the exact-PDF attachment, including named anchors."""
    pdf = Path(pdf)
    reader = pypdf.PdfReader(pdf)
    blobs = list(reader.attachments.get(ATTACHMENT, []))
    if len(blobs) != 1:
        raise ValueError("PDF must contain exactly one serialized position attachment; rebuild it")
    payload = json.loads(blobs[0])
    if payload.get("schema") != 1 or not isinstance(payload.get("identity"), dict):
        raise ValueError("Invalid serialized position identity")
    identity = payload["identity"]
    for key in ("content_sha256", "input_sha256"):
        if not isinstance(identity.get(key), str) or len(identity[key]) != 64:
            raise ValueError("Missing complete serialized position identity: " + key)
    if identity.get("variant") != variant or identity.get("edition") != edition:
        raise ValueError("Position attachment variant/edition does not match requested PDF")
    if current and identity != compilation_identity(root, variant, edition, content):
        raise ValueError("PDF positions do not describe current source/style/font/asset inputs; rebuild")
    positions = payload.get("positions", {})
    if any(not isinstance(positions.get(s), list) for s in SELECTORS):
        raise ValueError("Incomplete serialized position selectors")
    pages = len(reader.pages)
    for selector in SELECTORS:
        records = positions[selector]
        if selector == "<hpos>":
            if len(records) != 1 or not isinstance(records[0], list):
                raise ValueError("Expected one complete heading-position summary")
            records = records[0]
        for m in records:
            if not isinstance(m, dict) or type(m.get("page")) is not int or not 1 <= m["page"] <= pages:
                raise ValueError("Invalid physical page in serialized " + selector)
    anchors = serialized_anchor_audit(reader, positions)
    if anchors["mismatches"] or anchors["missing"]:
        raise ValueError("Serialized PDF anchors disagree with position attachment: " + json.dumps(anchors))
    return positions | {"binding": {
        "schema": 1, "origin": "pdf-attachment", "pdf_sha256": digest(pdf),
        "pdf_pages": pages, "identity": identity, "serialized_anchors": anchors,
    }}


def serialized_anchor_audit(reader, positions):
    """Independently compare attachment pages with the PDF destination objects."""
    actual = {name: reader.get_destination_page_number(dest) + 1
              for name, dest in reader.named_destinations.items()}
    expected = [(str(h["id"]), h["page"]) for h in positions["<hpos>"][0]]
    expected += [(("fig-" if str(m["id"]).startswith("FIG") else "tbl-") + str(m["id"]), m["page"])
                 for m in positions["<tblpos>"] if m.get("edge") == "s"]
    missing, mismatch, unexported = [], [], []
    checked = 0
    for name, page in expected:
        if name not in actual:
            # Typst emits named destinations for bookmarked/referenced labels.
            # An unreferenced metadata label need not be exported at all.
            unexported.append(name)
        elif actual[name] != page:
            checked += 1
            mismatch.append({"id": name, "position_page": page, "pdf_destination_page": actual[name]})
        else:
            checked += 1
    required = min(10, max(1, len(positions["<hpos>"][0]) // 10)) if expected else 0
    if checked < required:
        missing.append("insufficient independently serialized destinations")
    return {"checked": checked, "minimum_required": required, "unexported_labels": unexported,
            "missing": missing, "mismatches": mismatch}


def validate_sidecar(data, pdf, *, root=ROOT, current=True):
    """Reject edited, stale or independently queried sidecars, even with a PDF hash."""
    identity = data.get("binding", {}).get("identity", {})
    exact = read_positions(pdf, root=root, current=current,
                           variant=identity.get("variant", "cream"), edition=identity.get("edition", "print"))
    if data != exact:
        raise ValueError("Position sidecar differs from the exact PDF's serialized position evidence")
    return exact
