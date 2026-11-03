"""Effective book profile shared by the planner and Typst's JSON import.

Leading constants are additive Typst paragraph gaps, not baseline distances.
No content-dependent font shrinking is permitted by this profile.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "config/design_tokens.json").read_text(encoding="utf-8"))
PAGE_WIDTH_PT = float(TOKENS["page"]["width_pt"])
PAGE_HEIGHT_PT = float(TOKENS["page"]["height_pt"])
MARGIN_INSIDE_PT = float(TOKENS["page"]["inside_margin_pt"])
MARGIN_OUTSIDE_PT = float(TOKENS["page"]["outside_margin_pt"])
MARGIN_TOP_PT = float(TOKENS["page"]["top_margin_pt"])
MARGIN_BOTTOM_PT = float(TOKENS["page"]["bottom_margin_pt"])
COLUMN_GAP_PT = float(TOKENS["page"]["column_gap_pt"])
FRAME_WIDTH_PT = PAGE_WIDTH_PT - MARGIN_INSIDE_PT - MARGIN_OUTSIDE_PT
COLUMN_WIDTH_PT = (FRAME_WIDTH_PT - COLUMN_GAP_PT) / 2
BODY_HEIGHT_PT = PAGE_HEIGHT_PT - MARGIN_TOP_PT - MARGIN_BOTTOM_PT
BODY_SIZE_PT = float(TOKENS["type_pt"]["body"])
BODY_LEADING_PT = float(TOKENS["type_pt"]["body_leading_additive"])
TABLE_SIZE_PT = float(TOKENS["type_pt"]["table"])
TABLE_LEADING_PT = float(TOKENS["type_pt"]["table_leading_additive"])
TABLE_HORIZONTAL_PADDING_PT = float(TOKENS["spacing_pt"]["table_horizontal_padding"])
TABLE_VERTICAL_PADDING_PT = float(TOKENS["spacing_pt"]["table_vertical_padding"])


def profile_dict():
    """Return the effective numerical profile for evidence and specimen reports."""
    return {name: value for name, value in globals().items()
            if name.endswith("_PT") and isinstance(value, (int, float))}


def validate():
    """Reject unsafe geometry: margins inside the essential safe frame, a positive text frame, and the type floor."""
    safe = TOKENS["page"]["essential_edge_safe_pt"]
    margins = (MARGIN_INSIDE_PT, MARGIN_OUTSIDE_PT, MARGIN_TOP_PT, MARGIN_BOTTOM_PT)
    if min(margins) < safe or COLUMN_WIDTH_PT <= 0 or BODY_HEIGHT_PT <= 0:
        raise ValueError("Layout profile violates the essential-content safe frame")
    if min(BODY_SIZE_PT, TABLE_SIZE_PT) < TOKENS["type_pt"]["minimum_essential"]:
        raise ValueError("Layout profile violates the essential type floor")
    return True


validate()
