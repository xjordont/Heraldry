"""Collect only publication assets for the explicitly requested InDesign workflow.

This module performs no parsing, art generation, font conversion, PDF build, or
approval. Sources remain linked/editable; hashes bind copying to the inspected
bytes. An absent/LFS/stale selection is an error rather than an omitted image.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET


LFS_HEADER = b"version https://git-lfs.github.com/spec/v1"
APPROVED = {"approved", "anchor-approved"}


def _path(root, relative, prefix=None):
    root = Path(root).resolve()
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Asset must be a contained relative path: {relative}")
    path = (root / relative).resolve()
    try:
        actual = path.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError(f"Asset escapes the repository: {relative}") from error
    if prefix and (not relative.as_posix().startswith(prefix) or not actual.startswith(prefix)):
        raise ValueError(f"Asset is outside its publication directory: {relative}")
    if not path.is_file():
        raise ValueError(f"Missing publication asset: {relative}")
    return path


def _bytes(root, relative, prefix=None, expected=None):
    data = _path(root, relative, prefix).read_bytes()
    if not data or data.lstrip().startswith(LFS_HEADER):
        raise ValueError(f"Empty or unfetched Git LFS publication asset: {relative}; fetch its LFS bytes")
    digest = sha256(data).hexdigest()
    if expected is not None and digest != expected:
        raise ValueError(f"Publication asset hash mismatch: {relative}")
    return data, digest


def _json(root, relative):
    data, _ = _bytes(root, relative)
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate metadata key {key!r}: {relative}")
            result[key] = value
        return result
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique)


def _positive(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"Invalid {label}: {value!r}")
    return float(value)


def _raster(data, relative):
    from PIL import Image
    try:
        with Image.open(BytesIO(data)) as image:
            image.verify()
        with Image.open(BytesIO(data)) as image:
            return image.size
    except Exception as error:
        raise ValueError(f"Invalid raster publication asset: {relative}") from error


def _svg(data, relative):
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError(f"SVG declarations are unsupported: {relative}")
    try:
        svg = ET.fromstring(data)
    except ET.ParseError as error:
        raise ValueError(f"Invalid SVG publication asset: {relative}") from error
    if svg.tag.rsplit("}", 1)[-1] != "svg":
        raise ValueError(f"Publication vector is not SVG: {relative}")
    for element in svg.iter():
        if element.tag.rsplit("}", 1)[-1] in {"script", "foreignObject", "image"}:
            raise ValueError(f"SVG contains a nonvector/active resource: {relative}")
        for key, value in element.attrib.items():
            if key.rsplit("}", 1)[-1] == "href" and not value.startswith("#"):
                raise ValueError(f"SVG has an external/embedded resource: {relative}")
        for value in list(element.attrib.values()) + [element.text or ""]:
            for resource in re.findall(r"url\(\s*[\"']?([^\s\)\"']+)", value, flags=re.I):
                if not resource.startswith("#"):
                    raise ValueError(f"SVG has an external style resource: {relative}")
    viewbox = svg.get("viewBox", "").replace(",", " ").split()
    if len(viewbox) == 4:
        return _positive(float(viewbox[2]), "SVG width"), _positive(float(viewbox[3]), "SVG height")
    def length(name):
        value = svg.get(name, "")
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(?:pt|px)?", value)
        if not match:
            raise ValueError(f"SVG needs a viewBox or numeric dimensions: {relative}")
        return _positive(float(match.group(1)), f"SVG {name}")
    return length("width"), length("height")


def _model(parsed_blocks):
    if isinstance(parsed_blocks, dict) and "chapters" in parsed_blocks:
        return parsed_blocks
    if not isinstance(parsed_blocks, list):
        raise ValueError("Expected a parsed block list or chapter model")
    return {"chapters": [{"blocks": parsed_blocks}]}


def gather_assets(root, parsed_blocks):
    """Return hash-bound placements, installed-source fonts and their licences.

    Art follows current stable heading IDs and their flavour paragraphs rather
    than the catalog's obsolete source-line IDs. Figures resolve their persistent
    content anchors. Marks are the approved cream-substrate SVG derivatives.
    The owner front cover deliberately supersedes the older generated cover art.
    """
    from content_anchors import resolve_model
    from parse_source import plain
    from fontTools.ttLib import TTFont

    root = Path(root).resolve()
    model = _model(parsed_blocks)
    # Parser IDs inside a list intentionally share their source line with the
    # containing list. Publication anchors and artwork target top-level blocks.
    blocks = [block for chapter in model["chapters"] for block in chapter["blocks"]]
    ids = [block.get("id") for block in blocks]
    if not all(isinstance(value, str) and value for value in ids) or len(set(ids)) != len(ids):
        raise ValueError("Parsed manuscript needs unique block IDs")
    headings = {block["id"]: i for i, block in enumerate(blocks) if block["type"] == "heading"}
    chapters = {}
    for heading, i in headings.items():
        match = re.match(r"^(\d+)\.\s+", plain(blocks[i]["c"]))
        if match:
            number = int(match.group(1))
            if number in chapters:
                raise ValueError(f"Duplicate numbered chapter heading: {number}")
            chapters[number] = heading
    catalog = _json(root, "production/art/SPOT_CATALOG.json")["entries"]
    catalog_by_id = {entry["id"]: entry for entry in catalog}
    if len(catalog_by_id) != len(catalog):
        raise ValueError("Duplicate artwork catalog IDs")
    selections = _json(root, "production/art/SELECTIONS.json")
    if set(selections) != set(catalog_by_id):
        raise ValueError("Every catalog item needs one approved selection; reconcile catalog and selections")
    style = _json(root, "config/art_style.json")
    overrides = style.get("art_width_overrides", {})
    items, excluded = [], []
    placement_ids = set()
    def add(item):
        if item["id"] in placement_ids:
            raise ValueError(f"Duplicate asset placement ID: {item['id']}")
        placement_ids.add(item["id"])
        _positive(item["width_pt"], "placement width")
        _positive(item["height_pt"], "placement height")
        items.append(item)
    for aid in sorted(selections):
        selection, entry = selections[aid], catalog_by_id[aid]
        if selection.get("status") not in APPROVED:
            raise ValueError(f"Artwork has no explicit approval: {aid}")
        if not selection.get("spec_sha256") or selection["spec_sha256"] != entry.get("spec_sha256"):
            raise ValueError(f"Artwork specification is stale: {aid}")
        family = entry["family"]
        if selection.get("family") != family:
            raise ValueError(f"Artwork family disagrees with approved catalog: {aid}")
        if family == "cover":
            excluded.append({"id": aid, "reason": "Superseded by owner-supplied full front cover"})
            continue
        if family == "chapter":
            match = re.fullmatch(r"ART-CH(\d+)-002", aid)
            anchor = chapters.get(int(match.group(1))) if match else None
            if anchor is None:
                raise ValueError(f"Chapter artwork has no current chapter: {aid}")
            scope = "full"
        else:
            heading = entry.get("heading_id")
            i = headings.get(heading)
            if i is None or i + 1 >= len(blocks) or blocks[i + 1]["type"] != "para":
                raise ValueError(f"Artwork heading/flavour paragraph no longer resolves: {aid}")
            paragraph = blocks[i + 1]
            nodes = [node for node in paragraph.get("c", []) if node.get("t") != "text" or node.get("v", "").strip()]
            if not nodes or any(node.get("t") != "em" for node in nodes):
                raise ValueError(f"Artwork no longer precedes a flavour paragraph: {aid}")
            anchor, scope = paragraph["id"], "column"
        ink = selection.get("ink", {})
        relative = ink.get("path", "")
        if not ink.get("sha256"):
            raise ValueError(f"Artwork has no approved derivative hash: {aid}")
        data, digest = _bytes(root, relative, "assets/art/ink/", ink["sha256"])
        wpx, hpx = _raster(data, relative)
        if ink.get("px") != [wpx, hpx]:
            raise ValueError(f"Approved artwork dimensions disagree: {aid}")
        width = min(_positive(style["families"][family]["print_w_in"], "family print width"), wpx / 300)
        if aid in overrides:
            width = min(width, _positive(overrides[aid], "art width override"))
        add({"id": aid, "kind": "art", "source": relative, "sha256": digest,
             "width_pt": width * 72, "height_pt": width * 72 * hpx / wpx,
             "anchor": anchor, "caption": "", "scope": scope, "family": family})

    figures = _json(root, "figures/manifest.json")
    definitions = _json(root, "config/content_anchors.json")
    figure_ids = {figure["id"] for figure in figures}
    if len(figure_ids) != len(figures):
        raise ValueError("Duplicate figure manifest IDs")
    if any(fid not in definitions for fid in figure_ids):
        raise ValueError("Every figure requires a persistent content anchor")
    anchors = resolve_model({fid: definitions[fid] for fid in sorted(figure_ids)}, model)
    for figure in sorted(figures, key=lambda figure: figure["id"]):
        relative = figure["file"]
        if Path(relative).suffix.lower() != ".svg":
            raise ValueError(f"Editable figure source must be SVG: {relative}")
        data, digest = _bytes(root, relative, "figures/out/")
        _svg(data, relative)
        size = figure["size_pt"]
        add({"id": figure["id"], "kind": "figure", "source": relative, "sha256": digest,
             "width_pt": _positive(size["width"], "figure width"),
             "height_pt": _positive(size["height"], "figure height"), "anchor": anchors[figure["id"]],
             "caption": figure["caption"], "scope": figure["scope"]})

    relative = "assets/art/cover/front.png"
    data, digest = _bytes(root, relative, "assets/art/cover/")
    wpx, hpx = _raster(data, relative)
    width = min(558.0, 738.0 * wpx / hpx)
    add({"id": "COVER-FRONT", "kind": "cover", "source": relative, "sha256": digest,
         "width_pt": width, "height_pt": width * hpx / wpx, "anchor": None, "caption": "", "scope": "cover"})

    approved = _json(root, "production/art/marks/APPROVED.json")
    if not approved.get("logo") or not approved.get("coin") or not approved.get("arms"):
        raise ValueError("Missing owner-approved mark choices")
    names = [(f"arms-{int(number):02d}", 16.0, chapters.get(int(number))) for number in approved["arms"]]
    names += [("coin", 7.0, None), ("coin-reversed", 7.0, None), ("logo", 14.0, None)]
    for name, width, anchor in sorted(names):
        relative = f"typst/templates/marks/cream/{name}.svg"
        data, digest = _bytes(root, relative, "typst/templates/marks/cream/")
        w, h = _svg(data, relative)
        add({"id": f"MARK-{name.upper()}", "kind": "mark", "source": relative, "sha256": digest,
             "width_pt": width, "height_pt": width * h / w, "anchor": anchor, "caption": "", "scope": "furniture"})

    fonts = []
    for path in sorted((root / "fonts/static").glob("*")):
        if path.suffix.lower() not in {".ttf", ".otf"}:
            continue
        relative = path.relative_to(root).as_posix()
        data, digest = _bytes(root, relative, "fonts/static/")
        try:
            with TTFont(BytesIO(data), lazy=False) as font:
                names = font["name"]
                record = {"path": relative, "sha256": digest,
                          "family": names.getBestFamilyName(), "style": names.getBestSubFamilyName(),
                          "fullname": names.getDebugName(4), "postscript": names.getDebugName(6),
                          "variable": "fvar" in font,
                          "axes": [{"tag": axis.axisTag, "min": axis.minValue, "default": axis.defaultValue,
                                    "max": axis.maxValue} for axis in font["fvar"].axes] if "fvar" in font else []}
                if not all(record[key] for key in ("family", "style", "fullname", "postscript")):
                    raise ValueError("Required OpenType names are missing")
        except Exception as error:
            raise ValueError(f"Unreadable publication font: {relative}") from error
        fonts.append(record)
    licences = []
    for path in sorted((root / "fonts/licences").glob("*")):
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            _, digest = _bytes(root, relative, "fonts/licences/")
            licences.append({"path": relative, "sha256": digest})
    if not fonts or not licences:
        raise ValueError("Publication fonts and their licences must both be present")
    return {"items": items, "fonts": fonts, "licences": licences, "excluded": excluded}


def copy_assets(root, destination, assets):
    """Create an absent package directory and copy precisely the collected bytes.

    Returned records add ``package_path`` using forward-slash relative paths.
    Every source is rehashed before any output is created. Failure leaves its
    diagnostic partial directory intact and never overwrites an earlier export.
    """
    root, destination = Path(root).resolve(), Path(destination).resolve()
    if destination.exists():
        raise ValueError(f"InDesign output already exists: {destination}")
    result, pending, targets = deepcopy(assets), [], set()
    for key in ("items", "fonts", "licences"):
        for record in result[key]:
            relative = record["source"] if key == "items" else record["path"]
            if key == "items":
                prefixes = {"art": "assets/art/ink/", "figure": "figures/out/", "cover": "assets/art/cover/",
                            "mark": "typst/templates/marks/cream/"}
                prefix = prefixes[record["kind"]]
                package_path = "Links/" + Path(relative).name
            else:
                prefix = "fonts/static/" if key == "fonts" else "fonts/licences/"
                package_path = ("Document fonts/" if key == "fonts" else "Document fonts/Licences/") + Path(relative).name
            target_key = package_path.casefold()
            if target_key in targets:
                raise ValueError(f"Package filename collision: {package_path}")
            targets.add(target_key)
            data, _ = _bytes(root, relative, prefix, record["sha256"])
            pending.append((package_path, data))
            record["package_path"] = package_path
    destination.mkdir(parents=True, exist_ok=False)
    for relative, data in pending:
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data)
    return result
