"""Preview manuscript sidecar impact without publishing or parsing to disk."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from content_anchors import resolve, resolve_model
from figure_dependencies import hashes, hashes_for_text


def paragraph(identifier, text):
    return {"type": "para", "id": identifier, "c": [{"t": "text", "v": text}]}


class ManuscriptAnchors(unittest.TestCase):
    def setUp(self):
        self.definitions = {"example": {"section": "h-rules", "type": "para", "prefix": 'A 36"×36" field'}}
        self.model = {"chapters": [{"blocks": [
            {"type": "heading", "id": "h-rules"},
            paragraph("p-10", 'A 36"×36" field is measured in inches.'),
            {"type": "heading", "id": "h-other"},
            paragraph("p-20", 'A 36"×36" field uses the same text elsewhere.'),
        ]}]}

    def test_anchor_uses_exact_section_type_and_text_prefix(self):
        self.assertEqual(resolve_model(self.definitions, self.model), {"example": "p-10"})
        self.model["chapters"][0]["blocks"].insert(1, {"type": "list", "id": "list-9", "items": []})
        self.assertEqual(resolve_model(self.definitions, self.model), {"example": "p-10"})

    def test_missing_anchor_requires_explicit_repair(self):
        self.model["chapters"][0]["blocks"][1] = paragraph("p-10", "Changed wording.")
        with self.assertRaisesRegex(ValueError, "Anchor example: 0 matches"):
            resolve_model(self.definitions, self.model)

    def test_ambiguous_anchor_requires_explicit_repair(self):
        self.model["chapters"][0]["blocks"].insert(2, paragraph("p-11", 'A 36"×36" field appears twice.'))
        with self.assertRaisesRegex(ValueError, "Anchor example: 2 matches"):
            resolve_model(self.definitions, self.model)

    def test_nested_list_and_table_anchor_text_is_preserved(self):
        nodes = lambda text: [{"t": "text", "v": text}]
        blocks = self.model["chapters"][0]["blocks"]
        blocks.insert(2, {"type": "list", "id": "list-12", "items": [
            {"blocks": [paragraph("p-13", "First item."), {"type": "list", "items": [
                {"blocks": [paragraph("p-14", "Nested item.")]},
            ]}]},
        ]})
        blocks.insert(3, {"type": "table", "id": "tbl-15", "header": [nodes("Cost")], "rows": [[nodes("25c")]]})
        self.definitions.update({
            "list": {"section": "h-rules", "type": "list", "prefix": "First item. Nested item."},
            "table": {"section": "h-rules", "type": "table", "prefix": "Cost | 25c"},
        })
        self.assertEqual(resolve_model(self.definitions, self.model), {"example": "p-10", "list": "list-12", "table": "tbl-15"})

    def test_existing_file_wrapper_matches_in_memory_preview_with_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, data in (("config/content_anchors.json", self.definitions), ("build/blocks.json", self.model)):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            self.assertEqual(resolve(root), {"example": "p-10"})


class FigureDependencies(unittest.TestCase):
    def setUp(self):
        self.text = ("**Release Candidate 10 (RC10)**\n\n"
                     "## 1 Rules\n\nIntro.\n\n"
                     "### 1.1 Movement\n\nMove 6\".\n\n"
                     "#### 1.1.1 Terrain\n\nClimb 3\".\n\n"
                     "### 1.2 Combat\n\nAttack.\n\n"
                     "## Appendix A Reference\n\nA summary.\n")
        self.dependencies = {"FIG-MOVE": ["1.1"], "FIG-FIGHT": ["1.2"], "FIG-APPENDIX": ["A"]}

    def test_hash_retains_existing_exact_section_content_and_nested_rules(self):
        movement = '### 1.1 Movement\n\nMove 6".\n\n#### 1.1.1 Terrain\n\nClimb 3".\n\n'
        expected = hashlib.sha256(json.dumps({"1.1": movement}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        self.assertEqual(hashes_for_text(self.text, self.dependencies)["FIG-MOVE"], expected)

    def test_changed_section_invalidates_only_dependent_figures(self):
        before = hashes_for_text(self.text, self.dependencies)
        after = hashes_for_text(self.text.replace('Climb 3".', 'Climb 4".'), self.dependencies)
        self.assertNotEqual(before["FIG-MOVE"], after["FIG-MOVE"])
        self.assertEqual(before["FIG-FIGHT"], after["FIG-FIGHT"])
        self.assertEqual(before["FIG-APPENDIX"], after["FIG-APPENDIX"])

    def test_release_marker_and_unrelated_front_matter_do_not_invalidate_figures(self):
        changed = self.text.replace("10", "11").replace("## 1 Rules", "Unrelated front matter.\n\n## 1 Rules")
        self.assertEqual(hashes_for_text(self.text, self.dependencies), hashes_for_text(changed, self.dependencies))

    def test_missing_and_empty_dependencies_fail(self):
        for dependencies in ({"FIG-MOVE": ["9.9"]}, {"FIG-MOVE": []}):
            with self.subTest(dependencies=dependencies), self.assertRaisesRegex(ValueError, "FIG-MOVE: missing figure source dependency"):
                hashes_for_text(self.text, dependencies)

    def test_file_wrapper_matches_preview_with_utf8_and_crlf_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, data in (("source/versions.json", {"revisions": [{"path": "source/test.md"}]}),
                                   ("config/figure_dependencies.json", self.dependencies)):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(json.dumps(data).encode("utf-8"))
            (root / "source/test.md").write_bytes(self.text.replace("Move", "Déplace").replace("\n", "\r\n").encode("utf-8"))
            self.assertEqual(hashes(root), hashes_for_text(self.text.replace("Move", "Déplace"), self.dependencies))


if __name__ == "__main__":
    unittest.main()
