from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper/prior_discovery_manuscript.md"
EVIDENCE_MAP = ROOT / "paper/prior_discovery_evidence_map.md"
DISPLAY_ITEMS = ROOT / "paper/prior_discovery_display_items.md"
PAPER_STORY_ANALYSIS = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-paper-story-analysis-v0.1.json"
)
CURRENT_COMPOSITE_EVALUATION = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
)
B2_ANALYSIS = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b2-phase-process-results-v0.1.json"
)
LOW_B2_ANALYSIS = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b2-deepseek-v4-flash-low-results-v0.1.json"
)
B3_GPT_CLOSEOUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b3-gpt56-sol-medium-formal-closeout-v0.1.json"
)
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
    assert "protocol-development" in manuscript
    assert "not part of the prospective denominator" in manuscript
    assert "267,929,149 input tokens" not in manuscript
    assert "97.05%" not in manuscript
    assert "repeated model output" not in manuscript
    assert "Web search is disabled" not in manuscript
    assert "fixed DeepSeek-V4-Flash experimental-agent configuration" in manuscript
    assert "complete agent--tool configuration" in manuscript


def test_seed_zero_gate_pilots_do_not_enter_paired_scientific_contrasts() -> None:
    display_items = DISPLAY_ITEMS.read_text(encoding="utf-8")
    figure_manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))
    evidence_map = EVIDENCE_MAP.read_text(encoding="utf-8")

    assert "partition discovery and" in evidence_map
    assert "immutable seed-0 failures" in evidence_map
    assert "Prior uptake without established selective correction" in display_items
    assert (
        "Matched evidence replicates numerical convergence without structural recovery"
        in display_items
    )
    assert "cross-system ranking" in display_items
    limits = " ".join(figure_manifest["interpretation_limits"])
    assert "no same-arm replicate baseline" in limits
    assert "complete DeepSeek-low A-S B2 ablation" in limits


def test_draft_manifest_preserves_development_formal_private_boundaries() -> None:
    manifest = json.loads(BUILD_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["formal_result"] is False
    assert manifest["status"] == "compiled_development_draft"
    limits = " ".join(manifest["interpretation_limits"])
    assert "first-recipe" in limits
    assert "non-confirmatory" in limits
    assert "private confirmation remains uncollected" in limits
    sources = {row["path"] for row in manifest["sources"]}
    assert (
        "workstreams/flagship_tasks/reports/"
        "work-ii-deepseek-five-task-development-complete-20260810.json"
    ) in sources
    assert (
        "configs/benchmark/"
        "work_ii_deepseek_five_task_development_complete_analysis_sources_20260810.json"
    ) in sources


def test_current_c2_story_binds_completed_prediction_law_action_evaluator() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    display_items = DISPLAY_ITEMS.read_text(encoding="utf-8")
    analysis = json.loads(PAPER_STORY_ANALYSIS.read_text(encoding="utf-8"))
    evaluation = json.loads(CURRENT_COMPOSITE_EVALUATION.read_text(encoding="utf-8"))
    b2 = json.loads(B2_ANALYSIS.read_text(encoding="utf-8"))

    overall = analysis["overall"]
    assert overall["cell_count"] == 135
    assert overall["complete_experiment_count"] == 1_243
    assert overall["scheduled_experiment_count"] == 1_260
    assert overall["snapshot_count"] == 675
    assert overall["prediction_query_count"] == 6_300
    assert overall["prediction_metric_count"] == 24_300
    assert analysis["prediction_task_status"]["participant_checkpoint_collection"] == "complete"
    assert analysis["prediction_task_status"]["registered_truth_evaluator"] == "complete"
    assert analysis["prediction_task_status"]["law_summary_evaluator"] == "complete"
    assert analysis["prediction_task_status"]["blind_recommendation_replay"] == "complete"
    assert analysis["prediction_task_status"]["confirmatory_prediction_claim_allowed"] is False
    denominators = evaluation["denominators"]
    assert denominators["truth_completed_execution_count"] == 420
    assert denominators["checkpoint_scored_count"] == 675
    assert denominators["law_summary_evaluated_count"] == 135
    assert denominators["blind_completed_execution_count"] == 726
    assert evaluation["provider_call_count"] == 0
    law = evaluation["executable_law"]["overall"]["all"]
    assert round(law["mean_normalized_mae"], 4) == 0.2371
    assert law["law_better_than_final_prediction_count"] == 50
    assert law["law_worse_than_final_prediction_count"] == 84
    assert round(b2["primary_contrast"]["mean"], 4) == 0.0645
    assert b2["primary_contrast"]["positive_world_count"] == 3
    assert b2["public_summary_audit"]["by_arm"]["misindexed_nominal"][
        "exact_1_75_power_law_recovery_count"
    ] == 0
    assert (
        "Predictive learning does not establish selective repair of a wrong starting model"
        in manuscript
    )
    assert "1/119/1" in manuscript
    assert (
        "Matched counterevidence drives numerical convergence but not structural-law recovery"
        in manuscript
    )
    assert "+0.0645/+0.0915/-0.0405" in display_items
    assert "completed evaluator contains" in display_items


def test_deepseek_low_b2_ablation_is_bound_without_thinking_off_overclaim() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    evidence_map = EVIDENCE_MAP.read_text(encoding="utf-8")
    analysis = json.loads(LOW_B2_ANALYSIS.read_text(encoding="utf-8"))

    assert analysis["integrity"]["completed_sessions"] == 15
    assert analysis["integrity"]["failed_sessions"] == 0
    assert round(analysis["primary_contrast"]["mean"], 4) == -0.0405
    assert analysis["primary_contrast"]["positive_world_count"] == 2
    audit = analysis["public_summary_audit"]["by_arm"]["misindexed_nominal"]
    assert audit["exact_1_75_power_law_recovery_count"] == 0
    combined = manuscript + evidence_map
    assert "20.9%" in combined
    assert "thinking-off experiment" in manuscript
    assert "reasoning-superiority" in manuscript


def test_gpt_b3_formal_result_is_bound_with_provider_specific_limits() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    evidence_map = EVIDENCE_MAP.read_text(encoding="utf-8")
    closeout = json.loads(B3_GPT_CLOSEOUT.read_text(encoding="utf-8"))

    assert closeout["status"] == "formal_completed"
    assert closeout["integrity"]["completed_formal_cell_count"] == 30
    assert closeout["integrity"]["failed_formal_cell_count"] == 0
    by_arm = closeout["science"]["by_arm"]
    assert by_arm["opaque"]["joint_family_and_exponent_recovery_count"] == 0
    assert by_arm["aligned_nominal"]["joint_family_and_exponent_recovery_count"] == 5
    assert by_arm["misindexed_nominal"]["joint_family_and_exponent_recovery_count"] == 0
    action = closeout["science"]["action_bridge"]
    assert action["action_opportunity_eligible_cell_denominator"] == 18
    assert action["gain_at_least_0_02_count"] == 0
    combined = manuscript + evidence_map
    assert "0/18" in combined
    assert "provider-specific" in combined
    assert "cross-provider leaderboard" in evidence_map
