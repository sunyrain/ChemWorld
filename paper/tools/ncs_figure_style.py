"""Shared semantic colours from the current NCS figure style specification."""

import json
from pathlib import Path

STYLE = Path(__file__).resolve().parents[1] / "figures/final-ppt/style-and-export.json"
ARMS = ("Opaque", "Aligned", "MisIndexed")
_palette = json.loads(STYLE.read_text(encoding="utf-8"))["palette"]
ARM_COLORS = {arm: _palette[arm] for arm in ARMS}
