from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_confirmatory import (
    WorkIIConfirmatoryAnalysisError,
    build_confirmatory_analysis,
    validate_confirmatory_analysis,
)

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
TASKS = (
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "reaction-safety-constrained",
)
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")


def _plan() -> dict[str, object]:
    return json.loads(ANALYSIS_PLAN.read_text(encoding="utf-8"))


def _dataset(*, primary_effect: float = 0.20) -> dict[str, object]:
    cluster_rows: list[dict[str, object]] = []
    cell_rows: list[dict[str, object]] = []
    for task_index, task_id in enumerate(TASKS):
        for world_index in range(5):
            cluster_id = f"{task_id}-world-{world_index}"
            jitter = (world_index - 2) * 0.01
            aligned_improvement = 0.04 + jitter
            misindexed_improvement = aligned_improvement + primary_effect
            cluster_rows.append(
                {
                    "world_cluster_id": cluster_id,
                    "task_id": task_id,
                    "complete_case": True,
                    "H1_prior_utility": 0.12 + 0.005 * task_index + jitter,
                    "H2_prior_vulnerability": 0.10 + 0.004 * task_index + jitter,
                    "H3_misindexed_improvement": misindexed_improvement,
                    "H3_aligned_improvement": aligned_improvement,
                    "H3_primary_contrast": misindexed_improvement - aligned_improvement,
                    "H3_misindexed_improvement_lower_bound": misindexed_improvement,
                    "H3_aligned_improvement_lower_bound": aligned_improvement,
                    "H3_primary_contrast_lower_bound": (
                        misindexed_improvement - aligned_improvement
                    ),
                }
            )
            arm_improvements = {
                "opaque": 0.03 + jitter,
                "aligned_nominal": aligned_improvement,
                "misindexed_nominal": misindexed_improvement,
            }
            h1 = 0.12 + 0.005 * task_index + jitter
            h2 = 0.10 + 0.004 * task_index + jitter
            pre_errors = {
                "opaque": 0.50,
                "aligned_nominal": 0.50 - h1,
                "misindexed_nominal": 0.50 + h2,
            }
            for arm_index, arm in enumerate(ARMS):
                improvement = arm_improvements[arm]
                gain = (
                    0.6 * improvement + 0.01 * task_index + 0.005 * arm_index + 0.002 * world_index
                )
                cell_rows.append(
                    {
                        "cell_id": f"{cluster_id}-{arm}",
                        "world_cluster_id": cluster_id,
                        "task_id": task_id,
                        "prior_arm": arm,
                        "terminal_state": "completed",
                        "checkpoint_error": {
                            "primary_improvement": improvement,
                            "effective_pre_error": pre_errors[arm],
                            "confirmatory_improvement_bounds": [
                                improvement,
                                improvement,
                            ],
                            "missing_failure_rule": "observed_final",
                        },
                        "blind_outcome": {
                            "status": "completed",
                            "completed_execution_count": 6,
                            "recommendation_gain_over_incumbent": gain,
                        },
                        "final_law_summary": {
                            "present": True,
                            "schema_version_matches": True,
                            "evaluator_executability_status": (
                                "passed_registered_query_execution"
                            ),
                            "continuous_prediction_validity_status": (
                                "evaluated_descriptive_no_public_binary_threshold"
                            ),
                            "normalized_mae": 0.10 + 0.002 * arm_index,
                        },
                    }
                )
    dataset: dict[str, object] = {
        "schema_version": "chemworld-work-ii-formal-analysis-dataset-0.1",
        "formal_result": True,
        "status": "passed",
        "formal_preflight_sha256": "a" * 64,
        "retained_cell_count": 75,
        "cluster_contrast_count": 25,
        "state_counts": {"completed": 75, "right_censored": 0, "failed": 0},
        "cell_rows": cell_rows,
        "cluster_rows": cluster_rows,
        "errors": [],
    }
    dataset["dataset_sha256"] = canonical_json_sha256(dataset)
    return dataset


def _rehash(dataset: dict[str, object]) -> None:
    dataset.pop("dataset_sha256", None)
    dataset["dataset_sha256"] = canonical_json_sha256(dataset)


def test_confirmatory_positive_fixture_passes_h3_and_is_deterministic() -> None:
    dataset = _dataset(primary_effect=0.20)
    first = build_confirmatory_analysis(dataset, _plan())
    second = build_confirmatory_analysis(dataset, _plan())

    assert first == second
    assert validate_confirmatory_analysis(first) == []
    assert first["primary_H3"]["passed"] is True
    assert first["primary_H3"]["components"]["H3_primary_contrast"]["passed"] is True
    assert first["sensitivity_analyses"]["HC3"]["passed"] is True
    assert first["sensitivity_analyses"]["task_stratified_cluster_bootstrap"]["passed"] is True
    assert (
        first["confirmatory_secondary"]["Holm"]["results"]["H1_prior_utility"]["rejected"] is True
    )
    assert (
        first["confirmatory_secondary"]["Holm"]["results"]["H2_prior_vulnerability"]["rejected"]
        is True
    )
    assert (
        first["exploratory_H4_knowledge_to_action_translation"]["status"]
        == "estimated"
    )
    assert first["exploratory_H4_knowledge_to_action_translation"]["confirmatory"] is False
    assert first["confirmatory_secondary"]["Holm"]["family_size"] == 2
    assert first["law_summary_and_transfer_boundary"]["typed_final_summary_present_count"] == 75
    assert (
        first["law_summary_and_transfer_boundary"][
            "evaluator_executability_passed_count"
        ]
        == 75
    )
    assert (
        first["law_summary_and_transfer_boundary"][
            "continuous_prediction_validity_evaluated_count"
        ]
        == 75
    )
    assert (
        first["law_summary_and_transfer_boundary"]["descriptive_normalized_mae"][
            "formal_test_performed"
        ]
        is False
    )
    assert first["claim_decisions"]["reusable_law_discovery"] is False
    assert first["claim_decisions"]["private_transfer"] == "not_collected_by_public_analysis"


def test_zero_primary_effect_does_not_pass_intersection_union() -> None:
    report = build_confirmatory_analysis(_dataset(primary_effect=0.0), _plan())

    assert report["primary_H3"]["passed"] is False
    assert report["claim_decisions"]["selective_evidence_driven_wrong_prior_correction"] is False


def test_failed_arm_uses_finite_symmetric_adverse_bound_and_blocks_h3() -> None:
    dataset = _dataset(primary_effect=0.20)
    cluster_rows = dataset["cluster_rows"]
    cell_rows = dataset["cell_rows"]
    for cluster_index, cell_index in ((0, 2), (1, 5)):
        cluster_rows[cluster_index]["complete_case"] = False
        cluster_rows[cluster_index]["H3_misindexed_improvement_lower_bound"] = -1.0
        cluster_rows[cluster_index]["H3_primary_contrast_lower_bound"] = (
            -1.0 - cluster_rows[cluster_index]["H3_aligned_improvement"]
        )
        cell_rows[cell_index]["terminal_state"] = "failed"
        cell_rows[cell_index]["checkpoint_error"][
            "confirmatory_improvement_bounds"
        ] = [-1.0, 1.0]
        cell_rows[cell_index]["checkpoint_error"]["missing_failure_rule"] = (
            "missing_final_with_valid_pre_sets_zero_improvement"
        )
    dataset["state_counts"] = {"completed": 73, "right_censored": 0, "failed": 2}
    _rehash(dataset)

    report = build_confirmatory_analysis(dataset, _plan())
    assert report["primary_H3"]["estimand"] == "symmetric_failure_aware_adverse_bounds"
    assert report["primary_H3"]["passed"] is False
    assert report["sensitivity_analyses"]["observed_point_summary"]["passed"] is True
    assert report["denominators"]["complete_case_cluster_count"] == 23


def test_missing_blind_outcomes_keep_h4_exploratory_and_outside_holm() -> None:
    dataset = _dataset(primary_effect=0.20)
    for row in dataset["cell_rows"]:
        row["blind_outcome"] = {
            "status": "missing_required_blind_pack",
            "completed_execution_count": 0,
            "recommendation_gain_over_incumbent": None,
        }
    _rehash(dataset)

    report = build_confirmatory_analysis(dataset, _plan())
    h4 = report["exploratory_H4_knowledge_to_action_translation"]
    assert h4["status"] == "not_estimable_insufficient_complete_blind_cells"
    assert h4["one_sided_p_value"] == 1.0
    assert h4["confirmatory"] is False
    assert "H4_knowledge_to_action_translation" not in report[
        "confirmatory_secondary"
    ]["Holm"]["results"]


def test_confirmatory_analysis_rejects_development_or_tampered_input() -> None:
    development = _dataset()
    development["formal_result"] = False
    _rehash(development)
    with pytest.raises(WorkIIConfirmatoryAnalysisError, match="passed formal dataset"):
        build_confirmatory_analysis(development, _plan())

    tampered = deepcopy(_dataset())
    tampered["cluster_rows"][0]["H3_primary_contrast"] = 99.0
    with pytest.raises(WorkIIConfirmatoryAnalysisError, match="self-hash mismatch"):
        build_confirmatory_analysis(tampered, _plan())


def test_confirmatory_analysis_rejects_rehashed_cluster_bound_tampering() -> None:
    tampered = deepcopy(_dataset())
    tampered["cluster_rows"][0]["H3_primary_contrast_lower_bound"] = -2.0
    _rehash(tampered)

    with pytest.raises(
        WorkIIConfirmatoryAnalysisError,
        match="H3_primary_contrast_lower_bound differs from its three cell rows",
    ):
        build_confirmatory_analysis(tampered, _plan())
