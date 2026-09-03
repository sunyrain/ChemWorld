from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_DATA = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-w2-64-publication-reanalysis-v0.1.json"
)
FIGURE_RENDERER = ROOT / "paper/figures/prior-discovery/render_prior_discovery_figures.py"
FIGURE_MANIFEST = ROOT / "paper/figures/prior-discovery/figure_manifest.json"
CURRENT_CONFIG = ROOT / "configs/current.json"


def _publication_data() -> dict[str, Any]:
    return json.loads(PUBLICATION_DATA.read_text(encoding="utf-8"))


def _contrast(block: dict[str, Any], name: str) -> dict[str, Any]:
    return next(row for row in block["contrasts"] if row["contrast"] == name)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_four_condition_primary_is_all_scheduled_and_failure_aware() -> None:
    action = _publication_data()["action_extension"]

    assert action["scheduled_condition_slots_total"] == 360
    assert action["scheduled_condition_slots_per_model"] == 180
    assert action["primary_population"] == "all 45 scheduled strata within model"

    expected = {
        "deepseek": {
            "autonomous_exploration_minus_no_evidence": -0.0912505750378417,
        },
        "codex": {
            "autonomous_exploration_minus_no_evidence": 0.11015983955245666,
            "yoked_evidence_minus_no_evidence": 0.21646484039930985,
            "learned_law_only_minus_no_evidence": 0.24591845568363727,
        },
    }
    for model_name, contrasts in expected.items():
        model = action["models"][model_name]
        primary = model["primary_all_scheduled"]
        assert primary["estimand"] == "all-scheduled failure-aware strategy estimand"
        assert primary["scheduled_stratum_count"] == 45
        for contrast_name, estimate in contrasts.items():
            row = _contrast(primary, contrast_name)
            assert row["mean_failure_aware_normalized_regret_difference"] == pytest.approx(
                estimate, abs=1e-12
            )


def test_donor_eligible_results_are_labelled_as_sensitivity_not_primary() -> None:
    action = _publication_data()["action_extension"]

    for model in action["models"].values():
        sensitivity = model["donor_eligible_sensitivity"]
        assert "primary_all_scheduled" not in sensitivity
        interpretation = sensitivity["autonomy_minus_no_evidence"]["interpretation"]
        assert "post-treatment variable" in interpretation
        assert "not the primary strategy estimand" in interpretation


def test_four_condition_task_heterogeneity_is_preserved() -> None:
    models = _publication_data()["action_extension"]["models"]
    expected = {
        "deepseek": {
            "electrochemical-conversion": -0.2397747665305388,
            "reaction-safety-constrained": -0.40596659459866197,
            "reaction-to-crystallization": 0.3719896360156757,
        },
        "codex": {
            "electrochemical-conversion": 0.08914439051387338,
            "reaction-safety-constrained": -0.21914755125605395,
            "reaction-to-crystallization": 0.46048267939955057,
        },
    }
    for model_name, task_means in expected.items():
        primary = models[model_name]["primary_all_scheduled"]
        observed = _contrast(primary, "autonomous_exploration_minus_no_evidence")["by_task"]
        for task_id, value in task_means.items():
            assert observed[task_id]["mean_regret_difference"] == pytest.approx(
                value, abs=1e-12
            )


def test_w2_50_law_and_action_denominators_are_complete_and_distinct() -> None:
    w2_50 = _publication_data()["w2_50"]
    overall = w2_50["decision_aligned_law_action"]["overall"]
    assert w2_50["decision_aligned_law_action"]["participant_model"] == "deepseek_v4_flash"
    assert {
        row["participant_model"] for row in w2_50["decision_aligned_law_action"]["cell_rows"]
    } == {"deepseek_v4_flash"}
    assert {row["law_source"] for row in w2_50["decision_aligned_law_action"]["cell_rows"]} == {
        "last_available_executable_law"
    }

    assert w2_50["scheduled_cell_count"] == 45
    assert overall["scheduled_cell_count"] == 45
    assert overall["law_evaluated_count"] == 45
    assert overall["law_unavailable_or_invalid_count"] == 0
    assert overall["law_implied_top1_count"] == 0
    assert overall["participant_top1_count"] == 11
    assert overall["law_action_agreement_evaluable_count"] == 42
    assert overall["law_implied_top1_followed_count"] == 12


def test_c2_exact_model_specific_denominators_are_preserved() -> None:
    c2 = _publication_data()["c2_denominators"]

    expected = {
        "deepseek": {
            "completed_cell_count": 121,
            "checkpoint_scored_count": 675,
            "checkpoint_scheduled_count": 675,
            "law_evaluated_count": 135,
            "law_scheduled_count": 135,
            "blind_gain_evaluable_count": 121,
            "blind_scheduled_cell_count": 135,
        },
        "codex": {
            "completed_cell_count": 126,
            "checkpoint_scored_count": 669,
            "checkpoint_scheduled_count": 675,
            "law_evaluated_count": 129,
            "law_scheduled_count": 135,
            "blind_gain_evaluable_count": 126,
            "blind_scheduled_cell_count": 135,
        },
    }
    assert c2["inference_unit"] == "45 independent task-world clusters per model"
    assert c2["session_structure"] == ("135 separate sessions nested within 45 task-world clusters")
    for model_name, denominators in expected.items():
        model = c2["models"][model_name]
        assert model["scheduled_session_count"] == 135
        for key, value in denominators.items():
            assert model[key] == value


def test_b3_reports_complete_case_and_scheduled_opportunity_denominators() -> None:
    b3 = _publication_data()["b3_denominators"]

    expected_complete_case = {"deepseek": (0, 13), "codex": (0, 18)}
    for model_name, (count, denominator) in expected_complete_case.items():
        model = b3["models"][model_name]
        complete_case = model["useful_gain_completed_opportunity"]
        scheduled = model["useful_gain_scheduled_opportunity"]
        assert (complete_case["count"], complete_case["denominator"]) == (
            count,
            denominator,
        )
        assert (scheduled["count"], scheduled["denominator"]) == (0, 18)
        assert scheduled["failure_or_unavailable_counted_as_zero"] is True

    deepseek = b3["models"]["deepseek"]
    gpt = b3["models"]["codex"]
    assert (
        deepseek["completed_cell_count"],
        deepseek["failed_cell_count"],
        deepseek["joint_law_recovery_count"],
        deepseek["top1_count"],
    ) == (17, 13, 0, 0)
    assert (
        gpt["completed_cell_count"],
        gpt["failed_cell_count"],
        gpt["joint_law_recovery_count"],
        gpt["top1_count"],
    ) == (30, 0, 5, 2)


def test_b2_expression_counts_and_identifiability_boundary_are_preserved() -> None:
    report = _publication_data()
    assert report["formal_result"] is False
    assert report["new_formal_execution"] is False
    assert "No new formal execution" in report["formal_result_scope"]
    assert report["claim_boundaries"]["initial_model_assignment_manipulated"] is True
    assert report["claim_boundaries"]["stochastic_participant_effect_identified"] is False
    assert "initial_model_intervention_causal" not in report["claim_boundaries"]
    b2 = report["b2_expression_and_identifiability"]
    assert b2["world_count"] == 5
    assert b2["session_count_per_configuration"] == 15
    assert len(b2["public_summary_rows"]) == 45

    expected = {
        "deepseek_v4_flash_high": {
            "opaque": (0, 3),
            "aligned_nominal": (1, 3),
            "misindexed_nominal": (0, 5),
        },
        "gpt_5_6_sol_medium": {
            "opaque": (0, 1),
            "aligned_nominal": (0, 3),
            "misindexed_nominal": (0, 3),
        },
        "deepseek_v4_flash_low": {
            "opaque": (0, 3),
            "aligned_nominal": (2, 4),
            "misindexed_nominal": (0, 4),
        },
    }
    for configuration, arms in expected.items():
        observed = b2["configuration_summaries"][configuration]["public_expression_audit_by_arm"]
        for arm, (exact_count, endpoint_count) in arms.items():
            assert observed[arm]["world_count"] == 5
            assert observed[arm]["exact_1_75_power_law_recovery_count"] == exact_count
            assert observed[arm]["empirical_saturation_or_endpoint_model_count"] == endpoint_count

    identifiability = b2["participant_visible_identifiability"]
    assert identifiability["decision"]["structural_family_identification_supported"] is False
    assert identifiability["exact_alias"]["present"] is True
    assert identifiability["positive_control"]["readout_positive_control_passed"] is False
    assert identifiability["constant_endpoint_baseline"]["mean_scoring_error"] == pytest.approx(
        0.0064939781, abs=1e-10
    )
    assert report["claim_boundaries"]["matched_evidence_pure_packet_effect_supported"] is False
    assert report["claim_boundaries"]["b2_structural_family_identification_supported"] is False


def test_publication_source_bindings_and_current_registry_are_fresh() -> None:
    report = _publication_data()
    assert len(report["source_bindings"]) == 15
    for binding in report["source_bindings"]:
        source = ROOT / binding["path"]
        assert source.is_file()
        assert _sha256(source) == binding["sha256"]

    current = json.loads(CURRENT_CONFIG.read_text(encoding="utf-8"))
    artifact = current["work_ii"]["w2_64_publication_reanalysis"]
    assert artifact["report"] == PUBLICATION_DATA.relative_to(ROOT).as_posix()
    assert artifact["report_sha256"] == _sha256(PUBLICATION_DATA)


def test_figure_renderer_uses_tracked_publication_data_not_formal_run_summary() -> None:
    renderer = FIGURE_RENDERER.read_text(encoding="utf-8")
    manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))

    assert "runs/formal/" not in renderer
    assert "work-ii-w2-64-publication-reanalysis-v0.1.json" in renderer
    assert 'publication_reanalysis["w2_50"]' in renderer

    source_paths = {row["path"] for row in manifest["source_bindings"]}
    assert (
        "workstreams/flagship_tasks/reports/work-ii-w2-64-publication-reanalysis-v0.1.json"
    ) in source_paths
    assert not any(path.startswith("runs/formal/") for path in source_paths)
