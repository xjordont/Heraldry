"""The intake fetches only new images: an LFS pointer's oid is the image SHA-256, so images already recorded
in SELECTIONS with the same bytes need no download (flat LFS bandwidth with one image per push)."""
import sys, tempfile, unittest
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
            (inc / "ART-WEB.webp").write_bytes(pointer("f" * 64))          # a non-PNG delivery is fetched too
            (inc / "README.md").write_text("not an image")
            (inc / "ART-CH01-001.png").write_bytes(pointer("e" * 64))     # a legacy master: not a catalog entry, never fetched
            sels = {"ART-OLD": {"master": {"sha256": old}}, "ART-CHG": {"master": {"sha256": "d" * 64}}}
            ents = [{"id": i} for i in ("ART-OLD", "ART-NEW", "ART-CHG", "ART-WEB")]
            with mock.patch.object(ai, "ROOT", root), mock.patch.object(ai, "INCOMING", inc), \
                 mock.patch.object(ai.g, "entries", return_value=ents), \
                 mock.patch.object(ai.g, "load", side_effect=lambda p, d=None: sels if "SELECTIONS" in str(p) else (d if d is not None else {})):
                self.assertEqual(ai.needs_pull(), ["assets/art/incoming/ART-CHG.png", "assets/art/incoming/ART-NEW.png",
                                                  "assets/art/incoming/ART-WEB.webp"])
                self.assertEqual(ai.pointer_oid(pointer(old)), old)


class ReviewSheets(unittest.TestCase):
    def test_sheets_are_written_locally_and_replace_the_previous_ones(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "assets/art/ink").mkdir(parents=True)
            sels = {}
            for i in ("ART-A", "ART-B"):
                im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
                ImageDraw.Draw(im).ellipse((20, 20, 180, 180), outline=(0, 0, 0, 255), width=8)
                im.save(root / f"assets/art/ink/{i}.png")
                sels[i] = {"ink": {"path": f"assets/art/ink/{i}.png"}}
            review = root / "build/art/review"
            review.mkdir(parents=True)
            (review / "pending-9.jpg").write_bytes(b"stale")
            with mock.patch.object(ai, "ROOT", root), mock.patch.object(ai, "REVIEW", review), \
                 mock.patch.object(ai.g, "ROOT", root), mock.patch.object(ai.g, "load", return_value=sels), \
                 mock.patch.object(ai.subprocess, "run") as run:
                self.assertEqual(ai.review_sheets(["ART-A", "ART-B"]), ["build/art/review/pending-1.jpg"])
                run.assert_not_called()                      # nothing held as an LFS pointer: no fetch
            self.assertEqual(sorted(p.name for p in review.iterdir()), ["pending-1.jpg"])


if __name__ == "__main__":
    unittest.main()
