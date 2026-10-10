"""Owner-fixed prices are preserved independently of removed pricing formulas."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from parse_source import parse, plain


def prices(path):
    found = []
    def walk(blocks):
        for b in blocks:
            if b['type'] == 'table':
                header = [plain(c) for c in b['header']]
                for col, name in enumerate(header):
                    if name in {'Cost (c)', 'Value (c)'}:
                        found.extend((tuple(header), i, plain(row[col])) for i, row in enumerate(b['rows']))
            walk(b.get('blocks', []))
            for item in b.get('items', []):
                walk(item['blocks'])
    walk(parse(path.read_text()))
    return found


class FixedValues(unittest.TestCase):
    def test_rc487_preserves_every_printed_finished_item_price(self):
        before = prices(ROOT / 'source/Heraldry_RC486.md')
        after = prices(ROOT / 'source/Heraldry_RC487.md')
        self.assertGreater(len(before), 274)
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
