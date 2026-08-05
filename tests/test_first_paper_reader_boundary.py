from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper/experimental_intelligence_v1_manuscript.md"
DISPLAY = ROOT / "paper/experimental_intelligence_v1_display_items.md"
FIGURE_DIR = ROOT / "paper/figures/first-paper-world-instrument-v1/publication"


def _reader_visible_manuscript() -> str:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        _, _, text = text.partition("\n---\n")
    text = re.sub(r"\\includegraphics\[[^\]]*\]\{[^}]+\}", "", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]+\}", "", text)
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    return text


def test_reader_visible_text_excludes_internal_engineering_metadata() -> None:
    visible = _reader_visible_manuscript() + "\n" + DISPLAY.read_text(encoding="utf-8")
    lowered = visible.lower()
    forbidden_literals = (
        "configs/current",
        "workstreams/",
        "scripts/",
        "paper/figures/",
        "source_commit",
        "run_id",
        "run id",
        "manifest_sha",
        "sha-256",
        "sha256",
        "w1-p",
        "u05",
        "c03",
        "e02",
    )
    assert all(token not in lowered for token in forbidden_literals)
    assert re.search(r"\b[0-9a-f]{40,64}\b", lowered) is None
    assert re.search(r"\b[^\s`]+\.(?:json|md|py)\b", visible) is None


def test_publication_svg_text_excludes_internal_engineering_metadata() -> None:
    svgs = sorted(FIGURE_DIR.glob("figure-*.svg"))
    assert len(svgs) == 4
    for path in svgs:
        text = path.read_text(encoding="utf-8").lower()
        assert "<text" in text
        assert "workstreams/" not in text
        assert "configs/current" not in text
        assert "sha256" not in text
        assert "source_commit" not in text
        assert "run_id" not in text
        assert re.search(r"\b[0-9a-f]{40,64}\b", text) is None
