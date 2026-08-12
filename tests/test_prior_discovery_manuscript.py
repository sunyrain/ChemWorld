from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper/prior_discovery_manuscript.md"
EVIDENCE_MAP = ROOT / "paper/prior_discovery_evidence_map.md"
DISPLAY_ITEMS = ROOT / "paper/prior_discovery_display_items.md"
FIGURE_MANIFEST = ROOT / "paper/figures/prior-discovery/figure_manifest.json"
BUILD_MANIFEST = ROOT / "paper/exports/prior-discovery-draft/build-manifest.json"
CLOSEOUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-five-task-development-complete-20260810.json"
)


def test_deepseek_five_task_closeout_denominators_are_bound_without_overclaim() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    evidence_map = EVIDENCE_MAP.read_text(encoding="utf-8")
    closeout = json.loads(CLOSEOUT.read_text(encoding="utf-8"))

    denominators = closeout["denominators"]
    assert denominators["terminal_record_count"] == 75
    assert denominators["qualified_cell_count"] == 69
    assert denominators["complete_experiment_count"] == 290
    assert denominators["provider_error_event_count"] == 0
    assert denominators["exact_replay_verified_count"] == 75
    usage = denominators["provider_usage_totals"]
    assert usage["input_token_count"] == 267_929_149
    assert usage["cached_input_token_count"] == 260_033_536
    assert usage["uncached_input_token_count"] == 7_895_613
    assert usage["output_token_count"] == 2_932_468
    combined = manuscript + evidence_map
    assert "75/75" in combined
    assert "69/75" in combined
    assert "290/300" in combined
    assert "formal hypothesis test" in manuscript
    assert "provider groups are never pooled into a capability ranking" in manuscript
    assert "267,929,149 input tokens" in manuscript
    assert "97.05%" in manuscript
    assert "repeated model output" in manuscript
    assert "Web search is disabled" in manuscript
    assert "not the model weights in isolation" in manuscript


def test_seed_zero_gate_pilots_do_not_enter_paired_scientific_contrasts() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    display_items = DISPLAY_ITEMS.read_text(encoding="utf-8")
    figure_manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))
    evidence_map = EVIDENCE_MAP.read_text(encoding="utf-8")

    assert "their seeds 1--4 in a separate continuation block" in manuscript
    assert "partition discovery and" in evidence_map
    assert "immutable seed-0 failures" in evidence_map
    assert "common three-task" in display_items
    assert "paired endpoint/warning panels" in display_items
    limits = " ".join(figure_manifest["interpretation_limits"])
    assert "operational descriptive evidence" in limits
    assert "not pooled into the three-task paired endpoint panels" in limits


def test_draft_manifest_preserves_development_formal_private_boundaries() -> None:
    manifest = json.loads(BUILD_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["formal_result"] is False
    assert manifest["status"] == "compiled_development_draft"
    limits = " ".join(manifest["interpretation_limits"])
    assert "common three-task provider-separated source" in limits
    assert "Public formal and private confirmation results remain uncollected." in limits
    sources = {row["path"] for row in manifest["sources"]}
    assert (
        "workstreams/flagship_tasks/reports/"
        "work-ii-deepseek-five-task-development-complete-20260810.json"
    ) in sources
    assert (
        "configs/benchmark/"
        "work_ii_deepseek_five_task_development_complete_analysis_sources_20260810.json"
    ) in sources
