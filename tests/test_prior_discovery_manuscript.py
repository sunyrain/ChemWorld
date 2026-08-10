from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper/prior_discovery_manuscript.md"
EVIDENCE_MAP = ROOT / "paper/prior_discovery_evidence_map.md"
DISPLAY_ITEMS = ROOT / "paper/prior_discovery_display_items.md"
FIGURE_MANIFEST = ROOT / "paper/figures/prior-discovery/figure_manifest.json"
BUILD_MANIFEST = ROOT / "paper/exports/prior-discovery-draft/build-manifest.json"
CLOSEOUT = ROOT / "workstreams/flagship_tasks/reports/work-ii-deepseek-five-task-development-closeout-v0.1.json"


def test_deepseek_five_task_closeout_denominators_are_bound_without_overclaim() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    evidence_map = EVIDENCE_MAP.read_text(encoding="utf-8")
    closeout = json.loads(CLOSEOUT.read_text(encoding="utf-8"))

    denominators = closeout["denominators"]
    assert denominators["terminal_record_count"] == 51
    assert denominators["qualified_cell_count"] == 47
    assert denominators["complete_experiment_count"] == 196
    assert denominators["provider_error_event_count"] == 0
    assert denominators["exact_replay_verified_count"] == 51
    combined = manuscript + evidence_map
    assert "51/51 terminal cells" in combined
    assert "47/51 runner-qualified cells" in combined
    assert "46/51 protocol-qualified" in combined
    assert "not five-task scientific contrasts" in manuscript
    assert "These are operational development observations, not five-task scientific contrasts." in manuscript


def test_seed_zero_gate_pilots_do_not_enter_paired_scientific_contrasts() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    display_items = DISPLAY_ITEMS.read_text(encoding="utf-8")
    figure_manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))
    evidence_map = EVIDENCE_MAP.read_text(encoding="utf-8")

    assert "seeds 1--4 were not launched" in manuscript
    assert "partition discovery and" in evidence_map
    assert "safety-constrained reaction remain seed-0 pilots" in evidence_map
    assert "paired panels remain restricted to the three DeepSeek tasks" in display_items
    limits = " ".join(figure_manifest["interpretation_limits"])
    assert "seed-0 gate pilots only" in limits
    assert "not paired scientific contrasts" in limits


def test_draft_manifest_preserves_development_formal_private_boundaries() -> None:
    manifest = json.loads(BUILD_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["formal_result"] is False
    assert manifest["status"] == "compiled_development_draft"
    limits = " ".join(manifest["interpretation_limits"])
    assert "three-task five-seed subset" in limits
    assert "Public formal and private confirmation results remain uncollected." in limits
    sources = {row["path"] for row in manifest["sources"]}
    assert (
        "workstreams/flagship_tasks/reports/"
        "work-ii-deepseek-five-task-development-closeout-v0.1.json"
    ) in sources
    assert (
        "configs/benchmark/"
        "work_ii_deepseek_five_task_development_analysis_sources_v0.1.json"
    ) in sources
