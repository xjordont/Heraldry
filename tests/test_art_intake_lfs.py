"""The intake fetches only new images: an LFS pointer's oid is the image SHA-256, so images already recorded
in SELECTIONS with the same bytes need no download (flat LFS bandwidth with one image per push)."""
import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import art_intake as ai  # noqa: E402


def pointer(sha, size=123):
    return f"version https://git-lfs.github.com/spec/v1\noid sha256:{sha}\nsize {size}\n".encode()


class NeedsPull(unittest.TestCase):
    def test_only_new_or_changed_pointers_are_listed_and_scan_skips_recorded_ones(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            inc = root / "assets/art/incoming"
            inc.mkdir(parents=True)
            old, new, changed = ("a" * 64, "b" * 64, "c" * 64)
            (inc / "ART-OLD.png").write_bytes(pointer(old))
            (inc / "ART-NEW.png").write_bytes(pointer(new))
            (inc / "ART-CHG.png").write_bytes(pointer(changed))
            sels = {"ART-OLD": {"master": {"sha256": old}}, "ART-CHG": {"master": {"sha256": "d" * 64}}}
            with mock.patch.object(ai, "ROOT", root), mock.patch.object(ai, "INCOMING", inc), \
                 mock.patch.object(ai.g, "load", side_effect=lambda p, d=None: sels if "SELECTIONS" in str(p) else (d if d is not None else {})):
                self.assertEqual(ai.needs_pull(), ["assets/art/incoming/ART-CHG.png", "assets/art/incoming/ART-NEW.png"])
                self.assertEqual(ai.pointer_oid(pointer(old)), old)


if __name__ == "__main__":
    unittest.main()
