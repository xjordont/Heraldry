"""Lossless semantic Markdown blocks as native, editable IDML story content.

This module writes no files and never composes pages. Adobe's IDML specification
(Stories, Tables, and Hyperlink Text Sources) defines the emitted object model.
Paragraph endings are Br elements; forced line breaks are LF inside Content.
The caller owns document resources, hyperlink definitions, and graphic geometry.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from xml.etree import ElementTree as ET


PACKAGING_NS = "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"
DOM_VERSION = "16.0"
NO_CHARACTER_STYLE = "CharacterStyle/$ID/[No character style]"
PARAGRAPH_STYLES = {
    name: f"ParagraphStyle/Heraldry {name}"
    for name in ("Body", "Table Body", "Table Header", "List", "Quote", "Caption", "Figure", "Rule",
                 *(f"Heading {i}" for i in range(1, 7)))
}
CHARACTER_STYLES = {
    name: f"CharacterStyle/Heraldry {name}"
    for name in ("Bold", "Italic", "Bold Italic", "Code", "Link")
}


def _digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def destination_id(anchor):
    """The document-global destination ID for a Markdown heading anchor."""
    return "HyperlinkTextDestination/Heraldry-" + _digest(str(anchor).removeprefix("#"))


def _xml_text(text):
    if not isinstance(text, str):
        raise ValueError("IDML text must be a string")
    if any(not (c in "\t\n\r" or 0x20 <= ord(c) <= 0xD7FF
                or 0xE000 <= ord(c) <= 0xFFFD or 0x10000 <= ord(c) <= 0x10FFFF) for c in text):
        raise ValueError("Manuscript contains a character forbidden by XML 1.0")
    return text


def _properties(element):
    properties = element.find("Properties")
    if properties is None:
        properties = ET.Element("Properties")
        element.insert(0, properties)
    return properties


def _label(element, values):
    label = _properties(element).find("Label")
    if label is None:
        label = ET.SubElement(_properties(element), "Label")
    for key, value in values.items():
        ET.SubElement(label, "KeyValuePair", {"Key": key, "Value": _xml_text(str(value))})


def _walk(blocks, path=()):
    for index, block in enumerate(blocks):
        here = (*path, index)
        yield block, here
        if block["type"] == "list":
            for number, item in enumerate(block["items"]):
                yield from _walk(item["blocks"], (*here, "item", number))
        elif block["type"] == "quote":
            yield from _walk(block["blocks"], (*here, "quote"))


def _key(block, path, story_id):
    return str(block.get("id") or story_id + "/block/" + "/".join(map(str, path)))


def _heading_anchor(block):
    if block.get("anchor") or block.get("id"):
        return str(block.get("anchor") or str(block["id"]).removeprefix("h-"))
    raise ValueError("Headings require the parser's assigned id or anchor")


def heading_destinations(blocks):
    """Definitions already embedded in stories; use these IDs in designmap links."""
    destinations = []
    seen = set()
    for block, _ in _walk(blocks):
        if block["type"] == "heading":
            anchor = _heading_anchor(block)
            if anchor in seen:
                raise ValueError(f"Duplicate heading anchor: {anchor}")
            seen.add(anchor)
            destinations.append({"id": destination_id(anchor), "name": anchor,
                                 "block_id": block.get("id")})
    return destinations


def _link_id(seed, path):
    return "HyperlinkTextSource/Heraldry-" + _digest(seed + "/" + "/".join(map(str, path)))


def _links(nodes, seed, block_id, path=()):
    for index, node in enumerate(nodes):
        here = (*path, index)
        if node["t"] == "link":
            href = node.get("href")
            if not isinstance(href, str) or not href:
                raise ValueError("A manuscript link has no destination")
            source = _link_id(seed, here)
            yield {"id": source, "source": source, "href": href,
                   "destination": destination_id(href[1:]) if href.startswith("#") else None,
                   "block_id": block_id}
        if "c" in node:
            yield from _links(node["c"], seed, block_id, here)


def story_links(blocks, story_id="story"):
    """Hyperlink sources and targets for the caller's document-level definitions."""
    links = []
    for block, path in _walk(blocks):
        key = _key(block, path, story_id)
        if "c" in block:
            links.extend(_links(block["c"], key, block.get("id")))
        elif block["type"] == "table":
            for row_index, row in enumerate([block["header"], *block["rows"]]):
                for column_index, nodes in enumerate(row):
                    links.extend(_links(nodes, f"{key}/cell/{row_index}/{column_index}", block.get("id")))
    return links


def _style(flags):
    if "code" in flags:
        name = "Code"
    elif "link" in flags:
        name = "Link"
    elif "strong" in flags and "em" in flags:
        name = "Bold Italic"
    elif "strong" in flags:
        name = "Bold"
    elif "em" in flags:
        name = "Italic"
    else:
        return {"AppliedCharacterStyle": NO_CHARACTER_STYLE}
    attributes = {"AppliedCharacterStyle": CHARACTER_STYLES[name]}
    # Link and code styles must retain surrounding emphasis too.
    if name in {"Link", "Code"}:
        font_style = "Bold Italic" if {"strong", "em"} <= flags else (
            "Bold" if "strong" in flags else "Italic" if "em" in flags else None)
        if font_style:
            attributes["FontStyle"] = font_style
    return attributes


class _Writer:
    def __init__(self, story_id, blocks, assets):
        if not isinstance(story_id, str) or not story_id:
            raise ValueError("An IDML story requires a nonempty ID")
        heading_destinations(blocks)  # Refuse duplicate/missing anchors before generation.
        self.story_id = story_id
        self.serial = 0
        self.assets = assets or {}
        self.claimed_assets = set()
        self.story = ET.Element("Story", {"Self": _xml_text(story_id), "TrackChanges": "false"})
        source_map = [{"id": _key(b, path, story_id), "type": b["type"], "src": b.get("src", b.get("lines"))}
                      for b, path in _walk(blocks)]
        _label(self.story, {"heraldry:source-map": json.dumps(source_map, ensure_ascii=False, separators=(",", ":"))})

    def uid(self, kind):
        self.serial += 1
        return "uHeraldry_" + _digest(self.story_id) + "_" + kind + str(self.serial)

    def text(self, parent, value, flags=frozenset()):
        run = ET.SubElement(parent, "CharacterStyleRange", _style(flags))
        ET.SubElement(run, "Content").text = _xml_text(value)
        return run

    def inline(self, parent, nodes, seed, flags=frozenset(), path=()):
        for index, node in enumerate(nodes):
            here = (*path, index)
            kind = node["t"]
            if kind in {"text", "code"}:
                self.text(parent, node["v"], flags | ({"code"} if kind == "code" else set()))
            elif kind == "soft":
                self.text(parent, " ", flags)
            elif kind == "br":
                self.text(parent, "\n", flags)
            elif kind in {"strong", "em"}:
                self.inline(parent, node["c"], seed, flags | {kind}, here)
            elif kind == "link":
                href = node.get("href")
                if not isinstance(href, str) or not href:
                    raise ValueError("A manuscript link has no destination")
                run = ET.SubElement(parent, "CharacterStyleRange", _style(flags | {"link"}))
                source = ET.SubElement(run, "HyperlinkTextSource", {
                    "Self": _link_id(seed, here), "Name": _link_id(seed, here), "Hidden": "false"})
                _label(source, {"heraldry:href": href})
                self.inline(source, node["c"], seed, flags | {"link"}, here)
            else:
                raise ValueError(f"Unsupported manuscript inline node: {kind}")

    def paragraph(self, style, attributes=None, parent=None):
        return ET.SubElement(parent if parent is not None else self.story, "ParagraphStyleRange", {
            "AppliedParagraphStyle": PARAGRAPH_STYLES[style], **(attributes or {})})

    def end(self, paragraph):
        run = ET.SubElement(paragraph, "CharacterStyleRange", {"AppliedCharacterStyle": NO_CHARACTER_STYLE})
        ET.SubElement(run, "Br")

    def destination(self, paragraph, block):
        run = ET.SubElement(paragraph, "CharacterStyleRange", {"AppliedCharacterStyle": NO_CHARACTER_STYLE})
        target = ET.SubElement(run, "HyperlinkTextDestination", {
            "Self": destination_id(_heading_anchor(block)), "Name": _heading_anchor(block), "Hidden": "false"})
        _label(target, {"heraldry:block-id": block.get("id", ""),
                        "heraldry:source-span": json.dumps(block.get("src", block.get("lines")))})

    def list_attributes(self, paragraph, context):
        if context is None:
            return
        depth = context["depth"]
        paragraph.set("LeftIndent", str(14 * depth))
        if not context["pending"]:
            paragraph.set("FirstLineIndent", "0")
            paragraph.set("BulletsAndNumberingListType", "NoList")
            return
        context["pending"] = False
        paragraph.set("FirstLineIndent", "-10")
        if context["ordered"]:
            if depth > 9:
                raise ValueError("InDesign supports at most 9 native numbering levels")
            paragraph.set("BulletsAndNumberingListType", "NumberedList")
            paragraph.set("NumberingLevel", str(depth))
            paragraph.set("NumberingExpression", "^#.^t")
            paragraph.set("NumberingContinue", "true" if context["index"] else "false")
            paragraph.set("NumberingStartAt", str(context["start"]))
            ET.SubElement(_properties(paragraph), "NumberingFormat", {"type": "enumeration"}).text = "Arabic"
        else:
            paragraph.set("BulletsAndNumberingListType", "BulletList")
            paragraph.set("BulletsTextAfter", "^t")
            ET.SubElement(_properties(paragraph), "BulletChar", {
                "BulletCharacterType": "UnicodeOnly", "BulletCharacterValue": "8226"})

    def table(self, block, key, list_context=None):
        rows = [block["header"], *block["rows"]]
        columns = len(block["header"])
        if not columns or any(len(row) != columns for row in rows):
            raise ValueError(f"Table {key} has missing or inconsistent cells")
        if columns > 200 or len(block["rows"]) > 10000:
            raise ValueError(f"Table {key} exceeds InDesign's table limits")
        width = float(block.get("idml_width_pt", 540))
        if not math.isfinite(width) or width <= 0:
            raise ValueError("IDML table width must be positive and finite")
        column_widths = block.get("idml_column_widths")
        if column_widths is None:
            column_widths = [width / columns] * columns
        else:
            if not isinstance(column_widths, list) or len(column_widths) != columns:
                raise ValueError("IDML column widths must be a list with one width per table column")
            if any(isinstance(value, bool) or not isinstance(value, (int, float))
                   or not math.isfinite(value) or value <= 0 for value in column_widths):
                raise ValueError("IDML column widths must be positive and finite numbers")
            if abs(math.fsum(column_widths) - width) > 1e-5:
                raise ValueError("IDML column widths must sum to the table width within 0.00001 pt")
        paragraph = self.paragraph("Table Body", {"SpanColumnType": "SpanColumns"})
        self.list_attributes(paragraph, list_context)
        run = ET.SubElement(paragraph, "CharacterStyleRange", {"AppliedCharacterStyle": NO_CHARACTER_STYLE})
        table_id = self.uid("table")
        # A header-only Markdown table remains one native row, styled as its
        # header. IDML requires at least one body row; no empty cell is invented.
        table = ET.SubElement(run, "Table", {"Self": table_id,
            "HeaderRowCount": "1" if block["rows"] else "0", "FooterRowCount": "0",
            "BodyRowCount": str(max(1, len(block["rows"]))), "ColumnCount": str(columns),
            "AppliedTableStyle": "TableStyle/Heraldry Table", "TableDirection": "LeftToRightDirection",
            "BreakHeaders": "InAllTextColumns", "SpaceBefore": "6", "SpaceAfter": "6"})
        _label(table, {"heraldry:block-id": key, "heraldry:source-span": json.dumps(block.get("src", block.get("lines")))})
        for r in range(len(rows)):
            ET.SubElement(table, "Row", {"Self": f"{table_id}_row{r}", "Name": str(r),
                                        "AutoGrow": "true", "MinimumHeight": "18",
                                        "KeepWithNextRow": "true" if r == 0 and block["rows"] else "false"})
        for c in range(columns):
            ET.SubElement(table, "Column", {"Self": f"{table_id}_column{c}", "Name": str(c),
                                           "SingleColumnWidth": format(column_widths[c], ".12g")})
        for r, row in enumerate(rows):
            for c, nodes in enumerate(row):
                cell = ET.SubElement(table, "Cell", {"Self": f"{table_id}_cell{c}_{r}", "Name": f"{c}:{r}",
                    "RowSpan": "1", "ColumnSpan": "1", "AppliedCellStyle": "CellStyle/Heraldry Cell",
                    "TopInset": "3", "BottomInset": "3", "LeftInset": "4", "RightInset": "4"})
                alignment = (block.get("align") or [])[c:c + 1]
                justification = {"left": "LeftAlign", "center": "CenterAlign", "right": "RightAlign"}.get(
                    alignment[0] if alignment else None, "LeftAlign")
                cell_paragraph = self.paragraph("Table Header" if r == 0 else "Table Body",
                                                 {"Justification": justification}, parent=cell)
                self.inline(cell_paragraph, nodes, f"{key}/cell/{r}/{c}")
                if not len(cell_paragraph):
                    self.text(cell_paragraph, "")
        self.end(paragraph)

    def asset(self, descriptor):
        element = descriptor.get("element")
        if not isinstance(element, ET.Element) or element.tag not in {
                "Rectangle", "Group", "TextFrame", "Polygon", "Oval", "GraphicLine"}:
            raise ValueError("Every anchored asset needs a prebuilt native IDML page-item element")
        item = deepcopy(element)
        if not item.get("Self"):
            item.set("Self", self.uid("asset"))
        _label(item, {"heraldry:asset-id": descriptor.get("id", item.get("Self"))})
        anchoring = item.find("AnchoredObjectSetting")
        if anchoring is None:
            anchoring = ET.SubElement(item, "AnchoredObjectSetting")
        anchoring.attrib.update({"AnchoredPosition": "AboveLine", "HorizontalAlignment": "CenterAlign",
                                "AnchorSpaceAbove": "6", "AnchorYoffset": "6", "LockPosition": "false"})
        attributes = {}
        if descriptor.get("span_columns") or float(descriptor.get("width_pt", 0)) > 261:
            attributes["SpanColumnType"] = "SpanColumns"
        paragraph = self.paragraph("Figure", attributes)
        run = ET.SubElement(paragraph, "CharacterStyleRange", {"AppliedCharacterStyle": NO_CHARACTER_STYLE})
        run.append(item)
        self.end(paragraph)
        caption = descriptor.get("caption")
        if caption:
            paragraph = self.paragraph("Caption", attributes)
            nodes = [{"t": "text", "v": caption}] if isinstance(caption, str) else caption
            self.inline(paragraph, nodes, self.story_id + "/caption/" + str(descriptor.get("id", item.get("Self"))))
            self.end(paragraph)

    def blocks(self, blocks, path=(), list_context=None, quote_depth=0):
        for index, block in enumerate(blocks):
            here = (*path, index)
            key = _key(block, here, self.story_id)
            assets = []
            if key not in self.claimed_assets and key in self.assets:
                self.claimed_assets.add(key)
                value = self.assets[key]
                assets = [value] if isinstance(value, dict) else list(value)
            for asset in assets:
                if asset.get("position", "after") == "before":
                    self.asset(asset)
                elif asset.get("position", "after") != "after":
                    raise ValueError("Asset position must be before or after")
            kind = block["type"]
            if kind in {"heading", "para"}:
                level = block.get("level")
                if kind == "heading" and level not in range(1, 7):
                    raise ValueError("IDML headings support levels 1 through 6")
                style = f"Heading {level}" if kind == "heading" else (
                    "Quote" if quote_depth else "List" if list_context else "Body")
                paragraph = self.paragraph(style)
                if quote_depth:
                    paragraph.set("LeftIndent", str(12 * quote_depth))
                    paragraph.set("RightIndent", "12")
                self.list_attributes(paragraph, list_context)
                if kind == "heading":
                    self.destination(paragraph, block)
                self.inline(paragraph, block["c"], key)
                self.end(paragraph)
            elif kind == "table":
                self.table(block, key, list_context)
            elif kind == "list":
                for item_index, item in enumerate(block["items"]):
                    context = {"depth": (list_context["depth"] if list_context else 0) + 1,
                               "ordered": bool(block["ordered"]), "index": item_index,
                               "start": block.get("start", 1), "pending": True}
                    self.blocks(item["blocks"], (*here, "item", item_index), context, quote_depth)
            elif kind == "quote":
                self.blocks(block["blocks"], (*here, "quote"), list_context, quote_depth + 1)
            elif kind == "hr":
                paragraph = self.paragraph("Rule", {"RuleBelow": "true", "RuleBelowLineWeight": "0.6",
                    "RuleBelowWidth": "ColumnWidth"})
                ET.SubElement(_properties(paragraph), "RuleBelowColor", {"type": "object"}).text = "Color/Black"
                self.list_attributes(paragraph, list_context)
                self.text(paragraph, "")
                self.end(paragraph)
            else:
                raise ValueError(f"Unsupported manuscript block: {kind}")
            for asset in assets:
                if asset.get("position", "after") == "after":
                    self.asset(asset)


def story_xml(story_id, blocks, assets_by_anchor=None):
    """Return one IDML Story XML part, using native text, tables, and anchors.

    ``blocks`` is the assigned parse_source model. Tables may specify
    ``idml_width_pt`` and ``idml_column_widths``; measured column widths must be
    positive and sum to the total within 0.00001 pt. ``assets_by_anchor`` maps a
    block ID to a descriptor or list of descriptors. Every descriptor must carry
    ``element``: a native page-item Element built by the package layer. This
    explicit hook prevents dropped artwork or rasterisation of editable figures.
    Optional fields are id, caption, position (before/after), width_pt and
    span_columns. The input model and page-item Elements are never modified.
    """
    writer = _Writer(story_id, blocks, assets_by_anchor)
    writer.blocks(blocks)
    unused = set(writer.assets) - writer.claimed_assets
    if unused:
        raise ValueError("Unresolved IDML asset anchors: " + ", ".join(sorted(map(str, unused))))
    paragraphs = writer.story.findall("ParagraphStyleRange")
    if not paragraphs:
        writer.text(writer.paragraph("Body"), "")
    else:
        # The final paragraph is implicit at story end; adding Br would create an
        # additional empty paragraph rather than representing manuscript text.
        last = paragraphs[-1]
        if len(last) and last[-1].tag == "CharacterStyleRange" and len(last[-1]) == 1 and last[-1][0].tag == "Br":
            last.remove(last[-1])
    ET.register_namespace("idPkg", PACKAGING_NS)
    root = ET.Element(f"{{{PACKAGING_NS}}}Story", {"DOMVersion": DOM_VERSION})
    root.append(writer.story)
    return (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            + ET.tostring(root, encoding="utf-8") + b"\n")
