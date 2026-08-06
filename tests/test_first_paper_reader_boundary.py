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
    assert re.search(r"\bv1\b", lowered) is None
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


def test_reader_visible_story_is_advantage_led_and_excludes_development_history() -> None:
    lowered = _reader_visible_manuscript().lower()
    forbidden = (
        "what is not established",
        "chemworld is narrower",
        "does not claim novelty",
        "development diagnostics",
        "superseded engineering runs",
        "does not establish arbitrary physics",
        "preregistered",
    )
    assert all(phrase not in lowered for phrase in forbidden)
    required = (
        "controlled experimental freedom",
        "programmable experimental freedom",
        "evaluator-complete observability",
        "controlled counterfactual process analysis",
    )
    assert all(phrase in lowered for phrase in required)


def test_main_figures_prioritize_scientific_capability_over_provider_accounting() -> None:
    figure_one = (FIGURE_DIR / "figure-1-system-overview.svg").read_text(encoding="utf-8").lower()
    figure_two = (
        FIGURE_DIR / "figure-2-composition-and-qualification.svg"
    ).read_text(encoding="utf-8").lower()
    figure_three = (FIGURE_DIR / "figure-3-runtime-semantics.svg").read_text(
        encoding="utf-8"
    ).lower()
    figure_four = (FIGURE_DIR / "figure-4-forks-and-agent.svg").read_text(encoding="utf-8").lower()
    assert "not a claim of laboratory equivalence" not in figure_one
    assert "no physical reagents or wet-lab hazard" not in figure_one
    assert "60/60 levels" in figure_two
    assert "180/180 pairs" in figure_two
    assert "3 new topologies" in figure_two
    assert "8 identity-new distillation cases" in figure_two
    assert "the planned failure is retained" in figure_three
    assert "one lifecycle, one replayable record" in figure_four
    assert "relative difference magnitude" in figure_four
    assert "signed relative difference" not in figure_four
    assert "cached input" not in figure_four
    assert "provider input" not in figure_four
    assert "repeated output" not in figure_four


def test_public_author_and_correspondence_metadata_are_complete() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    arxiv_tex = (ROOT / "paper/arxiv/main.tex").read_text(encoding="utf-8")

    assert 'pdf_author: "Jiangjie Qiu; Yijun Li; Xiaonan Wang"' in manuscript
    assert 'name: "Xiaonan Wang"' in manuscript
    assert 'affiliation_markers: "1,*"' in manuscript
    assert 'correspondence: "wangxiaonan@tsinghua.edu.cn"' in manuscript
    assert "Xiaonan Wang" in arxiv_tex
    assert "wangxiaonan@tsinghua.edu.cn" in arxiv_tex


def test_qualification_scope_and_provider_details_have_clear_placement() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    main_text, _, methods = manuscript.partition("# 9. Methods")

    assert "## 8.4 Qualification scope" in main_text
    assert "software experimental substrate" in main_text
    assert "GPT-5.6-sol" not in main_text
    assert "Codex subscription provider" not in main_text
    assert "GPT-5.6-sol" in methods
    assert "Codex subscription provider" in methods
    assert "direction is checked separately by the frozen divergence oracle" in main_text
    assert "protocol-defined" not in _reader_visible_manuscript().lower()
