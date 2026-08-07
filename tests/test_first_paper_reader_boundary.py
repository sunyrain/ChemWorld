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
        if path.name == "figure-1-system-overview.svg":
            assert text.count("<image") == 1
        else:
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
        "world construction as a locus of experimental control",
        "world construction as an experimental variable",
        "evaluator-complete observability",
        "controlled studies of experimental agency",
        "process-complete evidence for replay and intervention attribution",
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
    assert figure_one.count("<image") == 1
    assert "<text" not in figure_one
    assert "60/60 levels" in figure_two
    assert "180/180 pairs" in figure_two
    assert "3 new topologies" in figure_two
    assert "8 identity-new distillation cases" in figure_two
    assert "every execution census completed" not in figure_two
    assert "module, interface and fail-closed probes" not in figure_two
    assert "eight frozen use cases" in figure_three
    assert "1 rollback" in figure_three
    assert "18 subsequent commits" in figure_three
    assert "rollback discards candidate state" not in figure_three
    assert "all lifecycles close and replay" not in figure_three
    assert "one private mechanism changes under one public contract" in figure_four
    assert "relative difference magnitude" in figure_four
    assert "one world, two independent execution units" not in figure_four
    assert "one lifecycle, one replayable record" not in figure_four
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
    main_text, _, methods = manuscript.partition("# 8. Methods")

    assert "## 7.4 Qualification scope" in main_text
    assert "software-scale experimental regime" in main_text
    assert "GPT-5.6-sol" not in main_text
    assert "Codex subscription provider" not in main_text
    assert "GPT-5.6-sol" in methods
    assert "Codex subscription provider" in methods
    assert "direction is checked separately by the frozen divergence oracle" in main_text
    assert "protocol-defined" not in _reader_visible_manuscript().lower()


def test_world_transaction_and_private_boundary_formalization_are_closed() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    lowered = manuscript.lower()

    assert r"\mathcal{W}=(W_{\mathrm{pub}},\theta)" in manuscript
    assert (
        r"T=(W_{\mathrm{pub}},S_{0,\mathrm{pub}},A,I,O,R,\tau,E)"
        in manuscript
    )
    assert r"T=(W,S_0,A,I,O,R,\tau,E)" not in manuscript
    assert r"\theta_p&\neq\theta_c,& T_p&=T_c=T" in manuscript

    assert "runtime commit-gate predicate" in lowered
    assert "preflight-rejection event" in lowered
    assert "runtime-rollback event" in lowered
    assert "post-execution predicate" not in lowered
    assert "post-execution rollback event" not in lowered
    assert (
        "candidate physical, observation and uncommitted resource effects are discarded"
        in lowered
    )

    assert "public/private leakage" not in lowered
    assert "undeclared private-field exposure" in lowered
    assert "inferential information about hidden" in lowered
    assert "state conveyed through task-declared measurements" in lowered
    assert "full submitted action/transaction" in lowered
    assert "every submitted typed action in recorded order" in lowered
    assert "64 invalid-schema/unknown-operation probes" in lowered
    assert "64 campaign-resource-exhaustion probes" in lowered
    assert "64 runtime-precondition probes" in lowered
    assert "solver-diagnostic and candidate-observation fault" in lowered
    assert "did not assign them separate qualification denominators" in lowered
    assert r"\mathrm{world\text{-}spec\ ID}" in manuscript
    assert r"\mathrm{scenario\ ID}" in manuscript
    assert r"\mathrm{task\text{--}world\ unit}" in manuscript
    assert r"\rho_t" in manuscript


def test_fork_and_process_coordinate_details_are_reader_visible() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    lowered = manuscript.lower()

    for phrase in (
        r"K^{1.00}\rightarrow K^{1.75}",
        r"(0,1,2,3)\rightarrow(2,1,0,3)",
        r"\Delta\geq10^{-4}",
        r"\Delta\geq10^{-6}",
        r"\texttt{product\_in\_organic}",
        r"\texttt{ohmic\_efficiency}",
    ):
        assert phrase in manuscript

    coordinate_labels = (
        "closed lifecycle fraction",
        "assay commitment fraction",
        "discard fraction",
        "measured lifecycle fraction",
        "instrument uses per closed lifecycle",
        "first-measurement timing",
        "post-measure continuation prevalence",
        "post-measure operations per closed lifecycle",
        "threshold-eligible fraction",
        "evidence-to-terminal concordance",
        "attempted operations per closed lifecycle",
        "committed operations per closed lifecycle",
        "cost per closed lifecycle",
        "risk debit per closed lifecycle",
        "global-best discovery fraction",
        "online incumbent retention",
        "maximum incumbent drawdown",
        "loss-episode recovery rate",
        "terminal-to-best retention",
    )
    assert all(label in lowered for label in coordinate_labels)
    assert r"N_c=N_a+N_d" in manuscript
    assert r"(j^\star-1)/(N_a-1)" in manuscript
    assert "each task's frozen score" in lowered
    assert "orientation and scale binding" in lowered
