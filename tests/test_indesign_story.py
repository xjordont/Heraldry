"""Editable IDML stories preserve semantic content without publication builds."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from indesign_story import (CHARACTER_STYLES, DOM_VERSION, PACKAGING_NS,
                            PARAGRAPH_STYLES, destination_id, heading_destinations,
                            story_links, story_xml)
from parse_source import parse, plain
from update_manuscript import anchor_model


def model(markdown):
    blocks = parse(markdown)
    anchor_model(blocks)
    return blocks


def document(blocks, assets=None):
    return ET.fromstring(story_xml("uFixtureStory", blocks, assets))


def contents(element):
    return "".join(child.text or "" for child in element.iter("Content"))


class InDesignStories(unittest.TestCase):
    def test_namespace_document_version_and_deterministic_output(self):
        blocks = model("# Name\n\nAn editable paragraph.\n")
        before = deepcopy(blocks)
        first = story_xml("uFixtureStory", blocks)
        self.assertEqual(first, story_xml("uFixtureStory", blocks))
        self.assertEqual(before, blocks)
        root = ET.fromstring(first)
        self.assertEqual(root.tag, "{" + PACKAGING_NS + "}Story")
        self.assertEqual(root.get("DOMVersion"), DOM_VERSION)
        self.assertEqual(root.find("Story").get("Self"), "uFixtureStory")

    def test_rich_text_unicode_and_xml_metacharacters_are_editable(self):
        blocks = model('A **bold** and *italic* and ***both*** `x < 6 & y` café × 2.\n')
        root = document(blocks)
        self.assertEqual(contents(root), plain(blocks[0]["c"]))
        styles = {node.get("AppliedCharacterStyle") for node in root.iter("CharacterStyleRange")}
        self.assertTrue({CHARACTER_STYLES[name] for name in ("Bold", "Italic", "Bold Italic", "Code")} <= styles)
        self.assertFalse(list(root.iter("Image")))

    def test_soft_and_forced_breaks_do_not_create_paragraphs(self):
        blocks = model("First line\nsoft wrapped  \nforced line<br>HTML break.\n\nNext paragraph.\n")
        root = document(blocks)
        paragraphs = root.find("Story").findall("ParagraphStyleRange")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(contents(paragraphs[0]), "First line soft wrapped\nforced line\nHTML break.")
        self.assertEqual(len(list(root.iter("Br"))), 1)
        self.assertFalse(list(root.iter("Content/Br")))

    def test_headings_have_unique_named_destinations_and_source_labels(self):
        blocks = model("# Heading\n\n## Repeated\n\n## Repeated\n")
        root = document(blocks)
        expected = heading_destinations(blocks)
        self.assertEqual([record["name"] for record in expected], ["heading", "repeated", "repeated-1"])
        actual = list(root.iter("HyperlinkTextDestination"))
        self.assertEqual([node.get("Self") for node in actual], [record["id"] for record in expected])
        labels = {node.get("Key"): node.get("Value") for node in actual[0].iter("KeyValuePair")}
        self.assertEqual(labels["heraldry:block-id"], blocks[0]["id"])
        source_label = next(node for node in root.iter("KeyValuePair") if node.get("Key") == "heraldry:source-map")
        self.assertEqual(json.loads(source_label.get("Value"))[0]["src"], [0, 1])
        self.assertEqual(destination_id("#heading"), destination_id("heading"))

    def test_explicit_anchor_and_duplicate_anchor_refusal(self):
        blocks = model("# A\n\n# B\n")
        blocks[0]["anchor"] = "owner-anchor"
        self.assertEqual(heading_destinations(blocks)[0]["name"], "owner-anchor")
        blocks[1]["anchor"] = "owner-anchor"
        with self.assertRaisesRegex(ValueError, "Duplicate heading"):
            story_xml("story", blocks)

    def test_links_keep_destinations_nested_styles_and_stable_source_ids(self):
        blocks = model("## Rules\n\nSee [the **rules**](#rules) and [Adobe](https://www.adobe.com/a?x=1&y=2).\n")
        records = story_links(blocks, "uFixtureStory")
        root = document(blocks)
        sources = list(root.iter("HyperlinkTextSource"))
        self.assertEqual(len(sources), 2)
        self.assertEqual([node.get("Self") for node in sources], [record["source"] for record in records])
        self.assertEqual(records[0]["destination"], destination_id("rules"))
        self.assertIsNone(records[1]["destination"])
        self.assertEqual(contents(sources[0]), "the rules")
        bold = next(node for node in sources[0].iter("CharacterStyleRange") if node.get("FontStyle") == "Bold")
        self.assertEqual(contents(bold), "rules")
        hrefs = [node.get("Value") for node in root.iter("KeyValuePair") if node.get("Key") == "heraldry:href"]
        self.assertEqual(hrefs, [record["href"] for record in records])

    def test_native_lists_retain_start_continuation_and_nested_indentation(self):
        blocks = model("3. First **item**\n   - Nested item\n   - Other item\n4. Second item\n\n- Bullet\n")
        root = document(blocks)
        paragraphs = root.find("Story").findall("ParagraphStyleRange")
        self.assertEqual([contents(node) for node in paragraphs],
                         ["First item", "Nested item", "Other item", "Second item", "Bullet"])
        numbered = [node for node in paragraphs if node.get("BulletsAndNumberingListType") == "NumberedList"]
        self.assertEqual([node.get("NumberingContinue") for node in numbered], ["false", "true"])
        self.assertEqual(numbered[0].get("NumberingStartAt"), "3")
        self.assertEqual(paragraphs[1].get("LeftIndent"), "28")
        self.assertEqual(paragraphs[4].get("LeftIndent"), "14")
        self.assertEqual(len(list(root.iter("BulletChar"))), 3)

    def test_multiblock_list_item_gets_one_native_number(self):
        blocks = model("1. First paragraph.\n\n   Continuation paragraph.\n\n2. Next item.\n")
        root = document(blocks)
        paragraphs = root.find("Story").findall("ParagraphStyleRange")
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[1].get("BulletsAndNumberingListType"), "NoList")
        self.assertEqual(paragraphs[1].get("FirstLineIndent"), "0")

    def test_quote_and_horizontal_rule_remain_editable_objects(self):
        blocks = model("> First **quoted** paragraph.\n>\n> > Nested quotation.\n\n---\n\nBody.\n")
        root = document(blocks)
        paragraphs = root.find("Story").findall("ParagraphStyleRange")
        self.assertEqual(paragraphs[0].get("AppliedParagraphStyle"), PARAGRAPH_STYLES["Quote"])
        self.assertEqual(paragraphs[1].get("LeftIndent"), "24")
        rule = paragraphs[2]
        self.assertEqual(rule.get("AppliedParagraphStyle"), PARAGRAPH_STYLES["Rule"])
        self.assertEqual(rule.get("RuleBelow"), "true")
        self.assertEqual(rule.find("Properties/RuleBelowColor").text, "Color/Black")
        self.assertEqual(contents(paragraphs[-1]), "Body.")

    def test_tables_are_native_row_major_cells_with_rich_text_and_alignment(self):
        blocks = model("| Left | Middle | Right |\n| :--- | :---: | ---: |\n| **A** | *B* | `C` |\n| D<br>E | [F](#end) | |\n\n# End\n")
        blocks[0]["idml_width_pt"] = 510
        root = document(blocks)
        table = next(root.iter("Table"))
        self.assertEqual(table.get("ColumnCount"), "3")
        self.assertEqual(table.get("HeaderRowCount"), "1")
        self.assertEqual(table.get("BodyRowCount"), "2")
        self.assertEqual([cell.get("Name") for cell in table.findall("Cell")],
                         ["0:0", "1:0", "2:0", "0:1", "1:1", "2:1", "0:2", "1:2", "2:2"])
        self.assertEqual([contents(cell) for cell in table.findall("Cell")],
                         ["Left", "Middle", "Right", "A", "B", "C", "D\nE", "F", ""])
        self.assertEqual([column.get("SingleColumnWidth") for column in table.findall("Column")], ["170"] * 3)
        self.assertEqual([cell.find("ParagraphStyleRange").get("Justification") for cell in table.findall("Cell")[:3]],
                         ["LeftAlign", "CenterAlign", "RightAlign"])
        source_ids = [node.get("Self") for node in root.iter("HyperlinkTextSource")]
        self.assertEqual(source_ids, [record["source"] for record in story_links(blocks, "uFixtureStory")])
        self.assertEqual(root.find("Story/ParagraphStyleRange").get("SpanColumnType"), "SpanColumns")
        self.assertEqual(table.find("Cell").get("AppliedCellStyle"), "CellStyle/Heraldry Cell")
        self.assertEqual([row.get("KeepWithNextRow") for row in table.findall("Row")], ["true", "false", "false"])
        self.assertTrue(all(cell.find("ParagraphStyleRange").get("SpanColumnType") is None
                            for cell in table.findall("Cell")))

    def test_measured_column_widths_preserve_inputs_and_source_content(self):
        blocks = model("| Short | Long column |\n| --- | --- |\n| A | All of the original text. |\n")
        blocks[0]["idml_width_pt"] = 518.4
        blocks[0]["idml_column_widths"] = [119.1234567891, 399.2765432109]
        before = deepcopy(blocks)
        root = document(blocks)
        table = next(root.iter("Table"))
        widths = [float(column.get("SingleColumnWidth")) for column in table.findall("Column")]
        self.assertAlmostEqual(sum(widths), 518.4, places=8)
        for actual, expected in zip(widths, blocks[0]["idml_column_widths"]):
            self.assertAlmostEqual(actual, expected, places=8)
        self.assertEqual([contents(cell) for cell in table.findall("Cell")],
                         ["Short", "Long column", "A", "All of the original text."])
        self.assertEqual(blocks, before)

    def test_column_widths_require_positive_finite_matching_list(self):
        blocks = model("| A | B |\n| --- | --- |\n| C | D |\n")
        blocks[0]["idml_width_pt"] = 500
        invalid_values = ([], [500], [100, 100, 300], (250, 250), "250,250",
                          [0, 500], [-10, 510], [True, 499], ["250", 250],
                          [float("nan"), 250], [float("inf"), 250], [249, 250])
        for values in invalid_values:
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, "IDML column widths"):
                blocks[0]["idml_column_widths"] = values
                document(blocks)

    def test_column_width_sum_tolerance_is_absolute_in_points(self):
        blocks = model("| A | B |\n| --- | --- |\n| C | D |\n")
        blocks[0]["idml_width_pt"] = 500
        blocks[0]["idml_column_widths"] = [200, 300.000009]
        document(blocks)
        blocks[0]["idml_column_widths"] = [200, 300.000011]
        with self.assertRaisesRegex(ValueError, "sum to the table width"):
            document(blocks)

    def test_header_only_table_adds_no_synthetic_row_or_cell(self):
        blocks = model("| Header | Other |\n| --- | --- |\n")
        root = document(blocks)
        table = next(root.iter("Table"))
        self.assertEqual(table.get("BodyRowCount"), "1")
        self.assertEqual(table.get("HeaderRowCount"), "0")
        self.assertEqual(len(table.findall("Row")), 1)
        self.assertEqual(len(table.findall("Cell")), 2)

    def test_inconsistent_table_or_nonfinite_width_refuses(self):
        blocks = model("| A | B |\n| --- | --- |\n| C | D |\n")
        malformed = deepcopy(blocks)
        malformed[0]["rows"][0].pop()
        with self.assertRaisesRegex(ValueError, "inconsistent cells"):
            story_xml("uFixtureStory", malformed)
        for width in (0, -1, float("nan"), float("inf")):
            with self.subTest(width=width), self.assertRaisesRegex(ValueError, "positive and finite"):
                blocks[0]["idml_width_pt"] = width
                story_xml("uFixtureStory", blocks)

    def test_native_assets_are_cloned_anchored_and_caption_is_editable(self):
        blocks = model("# Chapter\n\nOriginal paragraph.\n")
        element = ET.Element("Group", {"Self": "uEditableFigure"})
        ET.SubElement(element, "Polygon", {"Self": "uEditableShape"})
        before = ET.tostring(element)
        asset = {"id": "FIG-01", "element": element, "width_pt": 400, "caption": "An editable caption."}
        root = document(blocks, {blocks[0]["id"]: [asset]})
        self.assertEqual(ET.tostring(element), before)
        group = next(root.iter("Group"))
        self.assertEqual(group.find("AnchoredObjectSetting").get("AnchoredPosition"), "AboveLine")
        paragraphs = root.find("Story").findall("ParagraphStyleRange")
        self.assertEqual([node.get("AppliedParagraphStyle") for node in paragraphs], [
            PARAGRAPH_STYLES["Heading 1"], PARAGRAPH_STYLES["Figure"],
            PARAGRAPH_STYLES["Caption"], PARAGRAPH_STYLES["Body"]])
        self.assertEqual(paragraphs[1].get("SpanColumnType"), "SpanColumns")
        self.assertEqual(contents(paragraphs[2]), "An editable caption.")

    def test_assets_cannot_be_silently_dropped_or_rasterised(self):
        blocks = model("Body.\n")
        with self.assertRaisesRegex(ValueError, "Unresolved IDML asset anchors"):
            document(blocks, {"not-present": []})
        with self.assertRaisesRegex(ValueError, "native IDML page-item"):
            document(blocks, {blocks[0]["id"]: {"package_path": "Links/image.png"}})
        with self.assertRaisesRegex(ValueError, "before or after"):
            document(blocks, {blocks[0]["id"]: {"position": "elsewhere"}})

    def test_unknown_nodes_and_xml_controls_refuse_instead_of_losing_text(self):
        with self.assertRaisesRegex(ValueError, "Unsupported manuscript inline"):
            document([{"type": "para", "c": [{"t": "mystery", "v": "Never drop"}]}])
        with self.assertRaisesRegex(ValueError, "Unsupported manuscript block"):
            document([{"type": "mystery"}])
        for invalid in ("bad\x00text", "bad\ud800text"):
            with self.subTest(invalid=repr(invalid)), self.assertRaisesRegex(ValueError, "XML 1.0"):
                document([{"type": "para", "c": [{"t": "text", "v": invalid}]}])

    def test_empty_story_has_an_editable_empty_paragraph(self):
        root = document([])
        self.assertEqual(len(root.find("Story").findall("ParagraphStyleRange")), 1)
        self.assertEqual(contents(root), "")


if __name__ == "__main__":
    unittest.main()
