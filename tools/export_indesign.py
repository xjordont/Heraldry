#!/usr/bin/env python3
"""Explicit, source-based editable InDesign export; never part of a PDF build."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, unquote
import zipfile
import xml.etree.ElementTree as ET

from manuscript import ROOT, check
from indesign_assets import gather_assets, copy_assets
from indesign_story import (story_xml, heading_destinations, story_links,
                            PARAGRAPH_STYLES, CHARACTER_STYLES, NO_CHARACTER_STYLE)

NS = "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"
MIME = b"application/vnd.adobe.indesign-idml-package"
ET.register_namespace("idPkg", NS)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def xml(root, document=False):
    instruction = (b'<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="16.0(0)"?>\n'
                   if document else b"")
    return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + instruction + ET.tostring(root, encoding="utf-8") + b"\n"


def part(name):
    return ET.Element(f"{{{NS}}}{name}", {"DOMVersion": "16.0"})


def properties(element):
    p = element.find("Properties")
    if p is None:
        p = ET.Element("Properties")
        element.insert(0, p)
    return p


def label(element, key, value):
    labels = properties(element).find("Label")
    if labels is None:
        labels = ET.SubElement(properties(element), "Label")
    ET.SubElement(labels, "KeyValuePair", {"Key": key, "Value": str(value)})


def geometry(element, x, y, w, h):
    path = ET.SubElement(properties(element), "PathGeometry")
    points = ET.SubElement(ET.SubElement(path, "GeometryPathType", {"PathOpen": "false"}), "PathPointArray")
    for px, py in ((x, y), (x + w, y), (x + w, y + h), (x, y + h)):
        pair = f"{px:g} {py:g}"
        ET.SubElement(points, "PathPointType", {"Anchor": pair, "LeftDirection": pair, "RightDirection": pair})


def frame(identifier, story, bounds, layer="layer_text", previous="n", next="n", columns=1, gutter=0):
    x, y, w, h = bounds
    item = ET.Element("TextFrame", {"Self": identifier, "Name": identifier, "ParentStory": story,
        "PreviousTextFrame": previous, "NextTextFrame": next, "ContentType": "TextType", "ItemLayer": layer,
        "ItemTransform": "1 0 0 1 0 0", "FillColor": "Swatch/None", "StrokeColor": "Swatch/None", "StrokeWeight": "0"})
    geometry(item, x, y, w, h)
    pref = ET.SubElement(item, "TextFramePreference", {"TextColumnCount": str(columns), "TextColumnGutter": str(gutter),
        "TextColumnFixedWidth": str((w - (columns - 1) * gutter) / columns), "UseFixedColumnWidth": "false",
        "VerticalJustification": "TopAlign", "FirstBaselineOffset": "AscentOffset"})
    insets = ET.SubElement(properties(pref), "InsetSpacing", {"type": "list"})
    for _ in range(4):
        ET.SubElement(insets, "ListItem", {"type": "unit"}).text = "0"
    label(item, "heraldry-story", story)
    return item


def graphic(asset, width=None, height=None, x=0, y=0):
    """Native anchored frame and a live vector/raster link; never a rendered page."""
    w, h = width or asset["width_pt"], height or asset["height_pt"]
    key = "asset_" + re.sub(r"[^a-zA-Z0-9_]", "_", asset["id"])
    item = ET.Element("Rectangle", {"Self": key, "Name": asset["id"], "ContentType": "GraphicType",
        "ItemLayer": "layer_art", "ItemTransform": "1 0 0 1 0 0", "FillColor": "Swatch/None",
        "StrokeColor": "Swatch/None", "StrokeWeight": "0"})
    geometry(item, x, y, w, h)
    label(item, "heraldry-asset", asset["id"])
    label(item, "heraldry-package-path", asset["package_path"])
    vector = asset["package_path"].lower().endswith(".svg")
    image = ET.SubElement(item, "SVG" if vector else "Image", {"Self": key + "_graphic", "ItemTransform": f"1 0 0 1 {x:g} {y:g}"})
    if not vector:
        image.set("ImageTypeName", "$ID/PNG")
    ET.SubElement(properties(image), "GraphicBounds", {"Left": "0", "Top": "0", "Right": str(w), "Bottom": str(h)})
    ET.SubElement(image, "Link", {"Self": key + "_link", "LinkResourceURI": "file:" + quote(asset["package_path"], safe="/"),
        "LinkResourceFormat": "$ID/SVG" if vector else "$ID/PNG", "StoredState": "Normal",
        "LinkResourceModified": "false", "LinkObjectModified": "false", "ShowInUI": "true",
        "CanEmbed": "true", "CanUnembed": "true", "CanPackage": "true"})
    return item


def styles_xml(profile):
    root = part("Styles")
    t = profile["type"]
    chars = ET.SubElement(root, "RootCharacterStyleGroup", {"Self": "rcsg"})
    ET.SubElement(chars, "CharacterStyle", {"Self": NO_CHARACTER_STYLE, "Name": "$ID/[No character style]"})
    for name, identifier in CHARACTER_STYLES.items():
        style = ET.SubElement(chars, "CharacterStyle", {"Self": identifier, "Name": "Heraldry " + name})
        if name in {"Bold", "Italic", "Bold Italic"}:
            style.set("FontStyle", name)
        if name == "Code":
            ET.SubElement(properties(style), "AppliedFont", {"type": "string"}).text = t["label_family"]
    paras = ET.SubElement(root, "RootParagraphStyleGroup", {"Self": "rpsg"})
    names = dict(PARAGRAPH_STYLES, **{"Furniture": "ParagraphStyle/Heraldry Furniture"})
    for name, identifier in names.items():
        size, leading, family = t["body_size"], t["body_leading"], t["body_family"]
        attrs = {"Self": identifier, "Name": "Heraldry " + name, "FontStyle": "Regular", "FillColor": "Color/Black",
                 "Justification": "LeftAlign", "Hyphenation": "false", "SpaceAfter": "6.5", "KeepFirstLines": "2", "KeepLastLines": "2"}
        if name.startswith("Heading "):
            level = int(name[-1])
            size = t["heading_sizes"][level - 1]
            leading, family = size * 1.2, t["display_family"] if level <= 3 else t["body_family"]
            attrs.update(KeepWithNext="2", KeepAllLinesTogether="true", SpaceBefore="12", SpaceAfter="6")
            if level <= 3:
                attrs["SpanColumnType"] = "SpanColumns"
        if name in {"Table Body", "Table Header", "Caption", "Furniture"}:
            family = t["label_family"]
            size = t["table_size"] if name.startswith("Table") else t["caption_size"] if name == "Caption" else 9
            leading = t["table_leading"] if name.startswith("Table") else size * 1.25
        if name == "Table Header":
            attrs["FontStyle"] = "Semibold"
        if name == "Figure":
            attrs.update(Justification="CenterAlign", KeepWithNext="1")
        if name == "Quote":
            attrs["FontStyle"] = "Italic"
        attrs["PointSize"] = str(size)
        style = ET.SubElement(paras, "ParagraphStyle", attrs)
        ET.SubElement(properties(style), "AppliedFont", {"type": "string"}).text = family
        ET.SubElement(properties(style), "Leading", {"type": "unit"}).text = str(leading)
    tables = ET.SubElement(root, "RootTableStyleGroup", {"Self": "rtsg"})
    ET.SubElement(tables, "TableStyle", {"Self": "TableStyle/Heraldry Table", "Name": "Heraldry Table"})
    cells = ET.SubElement(root, "RootCellStyleGroup", {"Self": "rcellsg"})
    ET.SubElement(cells, "CellStyle", {"Self": "CellStyle/Heraldry Cell", "Name": "Heraldry Cell",
        "TopInset": "3", "BottomInset": "3", "LeftInset": "4", "RightInset": "4",
        "TopEdgeStrokeWeight": "0.35", "BottomEdgeStrokeWeight": "0.35", "LeftEdgeStrokeWeight": "0", "RightEdgeStrokeWeight": "0"})
    return xml(root)


def fonts_xml(fonts):
    root, families = part("Fonts"), {}
    for index, font in enumerate(fonts):
        family = font["family"]
        if family not in families:
            families[family] = ET.SubElement(root, "FontFamily", {"Self": f"ff_{len(families)}", "Name": family})
        ET.SubElement(families[family], "Font", {"Self": f"font_{index}", "Name": font["fullname"], "FontFamily": family,
            "PostScriptName": font["postscript"], "FontStyleName": font["style"], "FullName": font["fullname"],
            "FullNameNative": font["fullname"], "FontStyleNameNative": font["style"], "FontType": "OpenTypeTT",
            "Status": "Installed", "WritingScript": "0"})
    return xml(root)


def groups(blocks):
    chapters, current = [], []
    for block in blocks:
        if block["type"] == "heading" and block["level"] == 2 and current:
            chapters.append(current)
            current = []
        current.append(block)
    if current:
        chapters.append(current)
    return chapters


def source_text(blocks):
    """Independent text walk for the round-trip gate; list markers are formatting."""
    from parse_source import plain
    result = []
    for b in blocks:
        if b["type"] in {"para", "heading"}:
            result.append(plain(b["c"]))
        elif b["type"] == "table":
            result.extend(plain(cell) for row in [b["header"]] + b["rows"] for cell in row)
        elif b["type"] == "list":
            result.extend(source_text(it["blocks"]) for it in b["items"])
        elif b["type"] == "quote":
            result.append(source_text(b["blocks"]))
    return "".join(result)


def text_digest(value):
    return sha(re.sub(r"\s+", " ", value).encode("utf-8"))


def source_tables(blocks):
    from parse_source import plain
    result = []
    for b in blocks:
        if b["type"] == "table":
            rows = [b["header"]] + b["rows"]
            result.append({"rows": len(rows), "columns": len(b["header"]),
                           "cells": [text_digest(plain(cell)) for row in rows for cell in row]})
        elif b["type"] == "list":
            for item in b["items"]:
                result.extend(source_tables(item["blocks"]))
        elif b["type"] == "quote":
            result.extend(source_tables(b["blocks"]))
    return result


def native_tables(story):
    result = []
    for table in story.iter("Table"):
        cells = sorted(table.findall("Cell"), key=lambda c: tuple(reversed(tuple(map(int, c.get("Name").split(":"))))))
        rows = int(table.get("HeaderRowCount", 0)) + int(table.get("BodyRowCount", 0)) + int(table.get("FooterRowCount", 0))
        columns = int(table.get("ColumnCount", len(table.findall("Column"))))
        if len(cells) != rows * columns or {c.get("Name") for c in cells} != {f"{c}:{r}" for r in range(rows) for c in range(columns)}:
            raise ValueError("Native table cell positions are missing or duplicated")
        result.append({"rows": rows, "columns": columns, "cells": [text_digest(story_text(c)) for c in cells]})
    return result


def story_text(story):
    def walk(element):
        if element.tag == "ParagraphStyleRange" and element.get("AppliedParagraphStyle") == PARAGRAPH_STYLES["Caption"]:
            return ""
        if element.tag == "Content":
            return element.text or ""
        return "".join(walk(child) for child in element)
    return walk(story)


def resource_parts(profile, assets):
    p = profile["page"]
    prefs = part("Preferences")
    ET.SubElement(prefs, "DocumentPreference", {"PageWidth": str(p["width"]), "PageHeight": str(p["height"]),
        "FacingPages": "true", "PagesPerDocument": "1", "AllowPageShuffle": "false", "DocumentBleedTopOffset": "0",
        "DocumentBleedBottomOffset": "0", "DocumentBleedInsideOrLeftOffset": "0", "DocumentBleedOutsideOrRightOffset": "0"})
    ET.SubElement(prefs, "ViewPreference", {"HorizontalMeasurementUnits": "Points", "VerticalMeasurementUnits": "Points", "RulerOrigin": "PageOrigin"})
    graphic_root = part("Graphic")
    ET.SubElement(graphic_root, "Swatch", {"Self": "Swatch/None", "Name": "None"})
    for name, space, values in (("Black", "CMYK", "0 0 0 100"), ("Heraldry Paper", "RGB", " ".join(map(str, profile["paper_rgb"])))):
        ET.SubElement(graphic_root, "Color", {"Self": "Color/" + name, "Name": name, "Model": "Process", "Space": space, "ColorValue": values})
    return {"Resources/Styles.xml": styles_xml(profile), "Resources/Fonts.xml": fonts_xml(assets["fonts"]),
            "Resources/Preferences.xml": xml(prefs), "Resources/Graphic.xml": xml(graphic_root)}


def add_page(spread, identifier, number, profile, master="master_A", dx=0):
    p = profile["page"]
    page = ET.SubElement(spread, "Page", {"Self": identifier, "Name": str(number), "AppliedMaster": master,
        "GeometricBounds": f"0 0 {p['height']} {p['width']}", "ItemTransform": f"1 0 0 1 {dx} 0",
        "MasterPageTransform": "1 0 0 1 0 0"})
    left, right = (p["inside"], p["outside"]) if int(number) % 2 else (p["outside"], p["inside"])
    ET.SubElement(page, "MarginPreference", {"ColumnCount": str(p["columns"]), "ColumnGutter": str(p["gutter"]),
        "Left": str(left), "Right": str(right), "Top": str(p["top"]), "Bottom": str(p["bottom"])})
    return page


def furniture(profile):
    p, parts = profile["page"], {}
    root = part("MasterSpread")
    master = ET.SubElement(root, "MasterSpread", {"Self": "master_A", "Name": "A-Heraldry", "NamePrefix": "A",
        "BaseName": "Heraldry", "PageCount": "2", "ItemTransform": "1 0 0 1 0 0"})
    for side, number, dx in (("left", 2, -p["width"]), ("right", 1, 0)):
        add_page(master, "master_page_" + side, number, profile, master="n", dx=dx)
        bg = ET.SubElement(master, "Rectangle", {"Self": "paper_" + side, "ItemLayer": "layer_background", "FillColor": "Color/Heraldry Paper",
            "StrokeColor": "Swatch/None", "StrokeWeight": "0", "ItemTransform": "1 0 0 1 0 0"})
        geometry(bg, dx, 0, p["width"], p["height"])
        for role, y, content in (("head", 28, "HERALDRY SKIRMISH"), ("folio", p["height"] - 35, "")):
            story_id = f"furniture_{side}_{role}"
            item = frame("frame_" + story_id, story_id, (dx + p["outside"], y, p["width"] - 2 * p["outside"], 15), "layer_furniture")
            label(item, "heraldry-furniture", role)
            master.append(item)
            story = part("Story")
            s = ET.SubElement(story, "Story", {"Self": story_id})
            para = ET.SubElement(s, "ParagraphStyleRange", {"AppliedParagraphStyle": "ParagraphStyle/Heraldry Furniture",
                "Justification": "LeftAlign" if side == "left" else "RightAlign"})
            run = ET.SubElement(para, "CharacterStyleRange", {"AppliedCharacterStyle": NO_CHARACTER_STYLE})
            c = ET.SubElement(run, "Content")
            if role == "folio":
                c.append(ET.ProcessingInstruction("ACE", "18"))
            else:
                c.text = content
            parts[f"Stories/Story_{story_id}.xml"] = xml(story)
    parts["MasterSpreads/MasterSpread_A.xml"] = xml(root)
    return parts


def make_idml(blocks, assets, profile):
    """Return deterministic IDML parts and expected independent story text hashes."""
    parts = resource_parts(profile, assets)
    parts.update(furniture(profile))
    designmap = ET.Element("Document", {"DOMVersion": "16.0", "Self": "document", "Name": "Heraldry.indd",
        "ActiveLayer": "layer_text", "ZeroPoint": "0 0"})
    for key, name, locked in reversed((("background", "01 Paper", True), ("art", "02 Artwork and vector figures", False),
                              ("text", "03 Editable manuscript", False), ("furniture", "04 Navigation and ornament", False))):
        ET.SubElement(designmap, "Layer", {"Self": "layer_" + key, "Name": name, "Locked": str(locked).lower(), "Visible": "true", "Printable": "true"})
    expected, stories, hyperlinks = {}, [], []
    page_number = 1
    p = profile["page"]
    width, height = p["width"] - p["inside"] - p["outside"], p["height"] - p["top"] - p["bottom"]
    column_width = (width - (p["columns"] - 1) * p["gutter"]) / p["columns"]
    cover = next((a for a in assets["items"] if a["kind"] == "cover"), None)
    if cover:
        cover_part = part("Spread")
        spread = ET.SubElement(cover_part, "Spread", {"Self": "spread_cover", "PageCount": "1", "ItemTransform": "1 0 0 1 0 0"})
        add_page(spread, "page_cover", page_number, profile, master="n")
        spread.append(graphic(cover, p["width"], p["height"]))
        parts["Spreads/Spread_cover.xml"] = xml(cover_part)
        page_number += 1
    for index, chapter in enumerate(groups(deepcopy(blocks))):
        story_id = f"manuscript_{index:02d}"
        expected[story_id] = text_digest(source_text(chapter))
        anchors = {b["id"] for b in chapter}
        chapter_assets = {}
        for asset in assets["items"]:
            if asset["kind"] == "cover" or asset["anchor"] not in anchors:
                continue
            target_width = width if asset["scope"] == "full" else column_width
            scale = min(1, target_width / asset["width_pt"], (height - 90) / asset["height_pt"])
            w, h = asset["width_pt"] * scale, asset["height_pt"] * scale
            descriptor = dict(asset, width_pt=w, element=graphic(asset, w, h),
                              span_columns=asset["scope"] == "full", position="before" if asset["kind"] == "art" and asset.get("family") == "chapter" else "after")
            chapter_assets.setdefault(asset["anchor"], []).append(descriptor)
        def measure_tables(sequence):
            from tables import measure_table, allocate
            for block in sequence:
                if block["type"] == "table":
                    minimum, maximum, _ = measure_table(block)
                    scale = profile["type"]["table_size"] / 9.5
                    widths, _ = allocate([m * scale for m in minimum], [m * scale for m in maximum], width)
                    if widths is None:
                        raise ValueError(f"Table {block['id']} cannot fit at the configured readable size; adjust its native layout explicitly")
                    # Allocate returns natural width for a short table; scale its
                    # columns uniformly to the selected native table width.
                    block["idml_width_pt"] = width
                    block["idml_column_widths"] = [w * width / sum(widths) for w in widths]
                if block["type"] == "list":
                    for item in block["items"]:
                        measure_tables(item["blocks"])
                elif block["type"] == "quote":
                    measure_tables(block["blocks"])
        measure_tables(chapter)
        content = ET.fromstring(story_xml(story_id, chapter, chapter_assets))
        label(content.find("Story"), "heraldry-story", story_id)
        parts[f"Stories/Story_{story_id}.xml"] = xml(content)
        stories.append(story_id)
        hyperlinks.extend(story_links(chapter, story_id))
        for destination in heading_destinations(chapter):
            ET.SubElement(designmap, "Bookmark", {"Self": "bookmark_" + sha(destination["id"].encode())[:20],
                "Name": destination["name"], "Destination": destination["id"]})
        # Seed two threaded pages. InDesign's explicit finishing step composes the
        # entire story, adds pages as needed, and removes trailing empty seed pages.
        for seed in range(2):
            spread_part = part("Spread")
            spread_id, frame_id = f"spread_{index:02d}_{seed}", f"frame_{story_id}_{seed}"
            spread = ET.SubElement(spread_part, "Spread", {"Self": spread_id, "PageCount": "1", "ItemTransform": "1 0 0 1 0 0", "AllowPageShuffle": "false"})
            add_page(spread, "page_" + spread_id, page_number, profile)
            left = p["inside"] if page_number % 2 else p["outside"]
            spread.append(frame(frame_id, story_id, (left, p["top"], width, height),
                previous=f"frame_{story_id}_0" if seed else "n", next=f"frame_{story_id}_1" if not seed else "n",
                columns=p["columns"], gutter=p["gutter"]))
            parts[f"Spreads/Spread_{index:02d}_{seed}.xml"] = xml(spread_part)
            page_number += 1
    destinations = {d["id"] for chapter in groups(blocks) for d in heading_destinations(chapter)}
    for i, link in enumerate(hyperlinks):
        target = link.get("destination")
        if target and target not in destinations:
            raise ValueError(f"Unresolved manuscript link: {link['href']}")
        if not target:
            target = f"url_{i}"
            ET.SubElement(designmap, "HyperlinkURLDestination", {"Self": target, "Name": link["href"], "DestinationURL": link["href"]})
        hyperlink = ET.SubElement(designmap, "Hyperlink", {"Self": f"hyperlink_{i}", "Name": f"Heraldry link {i}", "Source": link["source"], "Visible": "false"})
        ET.SubElement(properties(hyperlink), "Destination", {"type": "object"}).text = target
    for path in parts:
        kind = path.split("/")[0]
        type_name = path.rsplit("/", 1)[1].split("_", 1)[0].split(".", 1)[0] if kind in {"Stories", "Spreads"} else "MasterSpread" if kind == "MasterSpreads" else Path(path).stem
        ET.SubElement(designmap, f"{{{NS}}}{type_name}", {"src": path})
    designmap.set("StoryList", " ".join(stories + [f"furniture_{side}_{role}" for side in ("left", "right") for role in ("head", "folio")]))
    parts["designmap.xml"] = xml(designmap, document=True)
    parts["META-INF/container.xml"] = b'<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="designmap.xml" media-type="text/xml"/></rootfiles></container>'
    return parts, expected


def validate_profile(profile):
    if profile.get("schema") != 1 or profile.get("dom_version") != "16.0":
        raise ValueError("Unsupported InDesign export profile")
    p, t = profile["page"], profile["type"]
    for name in ("width", "height", "inside", "outside", "top", "bottom", "gutter"):
        value = p[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError("Invalid InDesign page measurement: " + name)
    if type(p["columns"]) is not int or p["columns"] not in (1, 2, 3):
        raise ValueError("InDesign export supports 1 to 3 text columns")
    if min(p["inside"], p["outside"], p["top"], p["bottom"]) < 27:
        raise ValueError("InDesign essential margins must remain at least 27 pt")
    if p["width"] - p["inside"] - p["outside"] - (p["columns"] - 1) * p["gutter"] <= 0 or p["height"] - p["top"] - p["bottom"] < 180:
        raise ValueError("InDesign profile has no usable text frame")
    for name in ("body_size", "body_leading", "table_size", "table_leading", "caption_size"):
        value = t[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 9:
            raise ValueError("Invalid/unreadable InDesign type size: " + name)
    if len(t["heading_sizes"]) != 6 or any(type(v) not in (int, float) or not math.isfinite(v) or v < 9 for v in t["heading_sizes"]):
        raise ValueError("Six readable InDesign heading sizes are required")
    if type(profile["maximum_pages"]) is not int or not 1 <= profile["maximum_pages"] <= 10000:
        raise ValueError("Invalid native composition page limit")
    rgb = profile["paper_rgb"]
    if len(rgb) != 3 or any(type(v) is not int or not 0 <= v <= 255 for v in rgb):
        raise ValueError("Invalid InDesign paper colour")


def zip_parts(path, parts):
    with zipfile.ZipFile(path, "x") as archive:
        for name, data in [("mimetype", MIME), *sorted(parts.items())]:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            archive.writestr(info, data)


def audit_idml(path, expected, expected_tables=None):
    """Check content and references independently of the writer, without InDesign."""
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if (not names or names[0] != "mimetype" or archive.infolist()[0].compress_type != zipfile.ZIP_STORED
                or len(names) != len(set(names)) or archive.testzip() or archive.read("mimetype") != MIME):
            raise ValueError("Corrupt or duplicate IDML package")
        roots = {name: ET.fromstring(archive.read(name)) for name in names if name.endswith(".xml")}
    designmap = roots["designmap.xml"]
    for reference in designmap.findall(f"{{{NS}}}*"):
        if reference.get("src") not in roots:
            raise ValueError("Missing IDML part: " + str(reference.get("src")))
    ids, references, stories, counts = set(), [], {}, Counter()
    frames, linked_files = {}, []
    for root in roots.values():
        for element in root.iter():
            identifier = element.get("Self")
            if identifier:
                if identifier in ids:
                    raise ValueError("Duplicate IDML object ID: " + identifier)
                ids.add(identifier)
            for key in ("ParentStory", "PreviousTextFrame", "NextTextFrame", "AppliedMaster", "ItemLayer", "AppliedParagraphStyle", "AppliedCharacterStyle", "AppliedCellStyle", "AppliedTableStyle", "Source"):
                if element.get(key) not in {None, "n"}:
                    references.append(element.get(key))
            if element.tag == "Destination" and element.get("type") == "object":
                references.append(element.text)
            if element.tag == "Bookmark":
                references.append(element.get("Destination"))
            counts[element.tag] += 1
            if element.tag == "TextFrame":
                frames[identifier] = element
            if element.tag == "Link":
                uri = element.get("LinkResourceURI", "")
                if not uri.startswith("file:"):
                    raise ValueError("Only packaged local graphic links are supported")
                relative = Path(unquote(uri[5:]))
                if relative.is_absolute() or ".." in relative.parts or relative.parts[:1] != ("Links",):
                    raise ValueError("Graphic link escapes the package")
                linked_files.append(relative.as_posix())
        for story in root.findall("Story"):
            key = next((x.get("Value") for x in story.findall("Properties/Label/KeyValuePair") if x.get("Key") == "heraldry-story"), None)
            if key in expected:
                if key in stories:
                    raise ValueError("Repeated manuscript story binding: " + key)
                stories[key] = text_digest(story_text(story))
                if expected_tables is not None and native_tables(story) != expected_tables[key]:
                    raise ValueError("Native table cells differ from their source positions")
    missing = set(references) - ids
    if missing:
        raise ValueError("Unresolved IDML object references: " + ", ".join(sorted(missing)))
    if stories != expected:
        raise ValueError("IDML native story text differs from manuscript or a manuscript story is missing")
    for relative in linked_files:
        if not (Path(path).parent / relative).is_file():
            raise ValueError("Missing packaged graphic: " + relative)
    for identifier, item in frames.items():
        next_id, previous = item.get("NextTextFrame", "n"), item.get("PreviousTextFrame", "n")
        for neighbour, reverse in ((next_id, "PreviousTextFrame"), (previous, "NextTextFrame")):
            if neighbour != "n" and (neighbour not in frames or frames[neighbour].get(reverse) != identifier
                    or frames[neighbour].get("ParentStory") != item.get("ParentStory")):
                raise ValueError("Broken native text-frame thread")
        visited, cursor = set(), identifier
        while cursor != "n":
            if cursor in visited:
                raise ValueError("Cyclic native text-frame thread")
            visited.add(cursor)
            cursor = frames[cursor].get("NextTextFrame", "n")
    return {"structural_status": "PASS", "manuscript_stories": len(stories), "native_tables": counts["Table"],
            "native_cells": counts["Cell"], "text_frames": counts["TextFrame"], "links": counts["Link"], "bookmarks": counts["Bookmark"],
            "native_composition": "NOT TESTED", "visual_review": "NOT TESTED", "physical_print": "NOT TESTED"}


def output_location(root, destination):
    root, destination = Path(root).resolve(), Path(destination).resolve()
    if destination == root or (destination.is_relative_to(root) and not destination.is_relative_to(root / "build/indesign")):
        raise ValueError("Export to build/indesign/ or an external directory; never overwrite project source/evidence")
    if destination.exists():
        raise ValueError("Output already exists; choose a new directory to preserve manual edits")
    return destination


def export_project(root, destination):
    from parse_source import parse
    from update_manuscript import anchor_model
    root = Path(root).resolve()
    destination = output_location(root, destination)
    authority = check(root)
    source_bytes = (root / authority["path"]).read_bytes()
    if sha(source_bytes) != authority["sha256"]:
        raise ValueError("Manuscript changed during export; preserve the immutable source and inspect")
    inputs = {name: sha((root / name).read_bytes()) for name in ("config/indesign.json", "config/content_anchors.json", "config/figure_dependencies.json", "source/versions.json")}
    blocks = parse(source_bytes.decode("utf-8"))
    anchor_model(blocks)
    profile = json.loads((root / "config/indesign.json").read_text(encoding="utf-8"))
    validate_profile(profile)
    assets = gather_assets(root, blocks)
    packaged = copy_assets(root, destination, assets)
    parts, expected = make_idml(blocks, packaged, profile)
    filename = f"Heraldry_RC{authority['number']}.idml"
    zip_parts(destination / filename, parts)
    expected_tables = {f"manuscript_{i:02d}": source_tables(chapter) for i, chapter in enumerate(groups(blocks))}
    audit = audit_idml(destination / filename, expected, expected_tables)
    source = destination / "Source" / Path(authority["path"]).name
    source.parent.mkdir()
    source.write_bytes(source_bytes)
    manifest = {"schema": 1, "manuscript": authority, "idml": filename, "idml_sha256": sha((destination / filename).read_bytes()),
        "profile": profile, "assets": packaged, "expected_story_text": expected, "expected_story_tables": expected_tables,
        "audit": audit, "limitations": [profile["figure_editing"], profile["layout"],
        "Run Finish in InDesign.jsx to compose all stories, resolve links, check overset and missing fonts, and save native INDD. Structural checks alone do not certify InDesign compatibility or page design."],
        "input_hashes": inputs}
    if check(root) != authority or any(sha((root / name).read_bytes()) != digest for name, digest in inputs.items()):
        raise ValueError("Inputs changed during export; preserve the partial project and create a fresh export")
    manifest["export_id"] = sha(json_bytes({"idml": manifest["idml_sha256"], "assets": packaged,
        "profile": profile, "inputs": manifest["input_hashes"], "finisher": sha((root / "tools/indesign/finish.jsx").read_bytes())}))
    template = (root / "tools/indesign/finish.jsx").read_text(encoding="utf-8")
    settings = {"idml": filename, "native": filename[:-5] + ".indd", "roundtrip": filename[:-5] + ".composed.idml",
                "source_sha256": authority["sha256"], "export_id": manifest["export_id"], "profile": profile,
                "expected_story_count": len(expected), "expected_links": audit["links"],
                "links": {Path(a["package_path"]).name: a["package_path"] for a in packaged["items"]}}
    (destination / "Finish in InDesign.jsx").write_bytes(template.replace("/*HERALDRY_SETTINGS*/", json.dumps(settings, ensure_ascii=True)).encode("utf-8"))
    (destination / "README.md").write_bytes((f"# Heraldry RC{authority['number']} - editable InDesign project\n\n"
        "Open the Scripts panel in InDesign 16.0 or later and run `Finish in InDesign.jsx` from this folder. Keep Links and Document fonts alongside the document. The script opens only this package, relinks assets, composes/adds pages, checks fonts/links/overset, and saves INDD plus a round-trip IDML. It refuses an existing native output.\n\n"
        "All manuscript text and tables are native editable content. Chapter stories thread across pages. Named paragraph/character/table/cell styles, layers, masters, heading bookmarks and TOC hyperlinks are supplied. Figures remain linked editable SVG originals: edit their paths/text in a vector editor and update the link in InDesign. They are not flattened page images or converted into native InDesign paths. Illustrations retain their original raster pixels.\n\n"
        "This is an independent editable layout. InDesign recomposes pagination; it does not reproduce the approved Typst PDF page for page. Initial IDML contains seed pages and full story content; the finishing step completes text flow and flags unsplittable overset.\n\n"
        "Structural audit: PASS. Native InDesign composition and visual review: NOT TESTED until the finishing step and actual inspection. Physical print: NOT TESTED. Current PDF release/review ledgers are unchanged. Fonts and their OFL licences are bundled; install them if your InDesign installation does not activate Document fonts automatically.\n").encode("utf-8"))
    manifest["files"] = {p.relative_to(destination).as_posix(): sha(p.read_bytes()) for p in sorted(destination.rglob("*")) if p.is_file()}
    (destination / "project.json").write_bytes(json_bytes(manifest))
    return manifest


def verify_project(project, native=False):
    project = Path(project).resolve()
    manifest = json.loads((project / "project.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files"].items():
        path = (project / name).resolve()
        if not path.is_relative_to(project) or sha(path.read_bytes()) != expected:
            raise ValueError("Packaged source/asset changed: " + name)
    result = audit_idml(project / manifest["idml"], manifest["expected_story_text"], manifest["expected_story_tables"])
    if native:
        report = json.loads((project / "native-report.json").read_text(encoding="utf-8"))
        if report.get("status") != "PASS" or report.get("source_sha256") != manifest["manuscript"]["sha256"] or report.get("export_id") != manifest.get("export_id"):
            raise ValueError("No passing native InDesign composition report for this manuscript")
        if any(report.get(key) != [] for key in ("missing_fonts", "missing_links", "overset_stories", "overset_cells")) or type(report.get("pages")) is not int or not 0 < report["pages"] <= manifest["profile"]["maximum_pages"]:
            raise ValueError("Native InDesign report is incomplete or contains unresolved findings")
        roundtrip = project / manifest["idml"].replace(".idml", ".composed.idml")
        # InDesign rewrites IDs, default resources and absolute link URIs. Its
        # round-trip gate compares the actual story content and tagged bindings.
        with zipfile.ZipFile(roundtrip) as archive:
            actual = {}
            for name in archive.namelist():
                if name.startswith("Stories/") and name.endswith(".xml"):
                    root = ET.fromstring(archive.read(name))
                    story = root.find("Story")
                    key = next((x.get("Value") for x in story.findall("Properties/Label/KeyValuePair") if x.get("Key") == "heraldry-story"), None)
                    if key in manifest["expected_story_text"]:
                        if key in actual:
                            raise ValueError("Duplicate round-trip manuscript story")
                        actual[key] = text_digest(story_text(story))
                        if native_tables(story) != manifest["expected_story_tables"][key]:
                            raise ValueError("Native round-trip table cells differ from their source positions")
            if actual != manifest["expected_story_text"]:
                raise ValueError("Native InDesign round-trip text differs from the manuscript")
        native_file = project / manifest["idml"].replace(".idml", ".indd")
        if not native_file.is_file() or not native_file.stat().st_size:
            raise ValueError("Native InDesign output is missing or empty")
        if native_file.stat().st_size != report.get("native_bytes") or roundtrip.stat().st_size != report.get("roundtrip_bytes"):
            raise ValueError("Native outputs changed since the InDesign composition report")
        proof = {"export_id": manifest["export_id"], "native_sha256": sha(native_file.read_bytes()),
                 "roundtrip_sha256": sha(roundtrip.read_bytes())}
        proof_path = project / "native-verification.json"
        if proof_path.exists() and json.loads(proof_path.read_text(encoding="utf-8")) != proof:
            raise ValueError("Native files changed after verified composition; review the manual edits separately")
        proof_path.write_bytes(json_bytes(proof))
        result["native_composition"] = "PASS (InDesign script plus IDML text round trip); visual review still required"
    return result


def compose(project, prog_id="InDesign.Application"):
    project = Path(project).resolve()
    verify_project(project)
    manifest = json.loads((project / "project.json").read_text(encoding="utf-8"))
    if any((project / manifest["idml"].replace(".idml", suffix)).exists() for suffix in (".indd", ".composed.idml")):
        raise ValueError("Native output already exists; choose a fresh export folder to preserve manual edits")
    if sys.platform != "win32":
        raise ValueError("Automatic composition uses Windows InDesign COM; run Finish in InDesign.jsx manually on macOS")
    script = project / "Finish in InDesign.jsx"
    # Literal PowerShell strings; paths are never evaluated as command text.
    literal = lambda value: "'" + str(value).replace("'", "''") + "'"
    command = "$ErrorActionPreference='Stop'; $indesign=New-Object -ComObject " + literal(prog_id) + "; $indesign.DoScript(" + literal(script) + ",1246973031)"
    try:
        result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
    except subprocess.TimeoutExpired as exc:
        raise ValueError("InDesign composition timed out; inspect the application and preserved output before retrying") from exc
    if result.returncode:
        raise ValueError("InDesign composition failed; inspect native-report.json and the preserved project. " + result.stderr.strip()[:800])
    return verify_project(project, native=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export", help="explicitly create a fresh editable IDML project and asset folder")
    export.add_argument("--output", required=True, type=Path)
    export.add_argument("--compose", action="store_true", help="also launch installed Windows InDesign and save native INDD")
    for name in ("verify", "compose"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--project", required=True, type=Path)
        if name == "verify":
            cmd.add_argument("--native", action="store_true")
        else:
            cmd.add_argument("--prog-id", default="InDesign.Application")
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            manifest = export_project(ROOT, args.output)
            print(f"Created {args.output / manifest['idml']}")
            print(json.dumps(compose(args.output) if args.compose else manifest["audit"], indent=2))
            print("Run Finish in InDesign.jsx to complete native composition. Existing PDF/release evidence is unchanged.")
        else:
            print(json.dumps(compose(args.project, args.prog_id) if args.command == "compose" else verify_project(args.project, args.native), indent=2))
        return 0
    except (ValueError, OSError, KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        print("FAILED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
