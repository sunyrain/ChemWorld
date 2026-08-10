from __future__ import annotations

import pytest

from chemworld.eval.work_ii_development_analysis import (
    build_single_provider_development_analysis,
)


def _result(arm: str, score: float) -> dict[str, object]:
    return {
        "arm": arm,
        "completed": True,
        "qualification": {"passed": True, "failed_checks": []},
        "exact_replay": {"verified": True},
        "failure": None,
        "analysis": {
            "complete_experiment_count": 4,
            "experiments": [{"leaderboard_score": score}],
            "operation_attempt_count": 1,
            "resource_rejection_count": 0,
            "process_profile": {"counts": {"committed_operation_count": 1}},
            "final_recommendation": {"selected_experiment_index": 1},
        },
        "method_resources": {
            "input_token_count": 10,
            "cached_input_token_count": 8,
            "uncached_input_token_count": 2,
            "output_token_count": 1,
            "provider_usage_accounting_complete": True,
            "recovered_mcp_tool_failure_count": 0,
        },
        "provider_receipts": [],
        "elapsed_s": 1.0,
    }


def _source(group: str = "deepseek_recovery_amended") -> dict[str, object]:
    return {
        "source_id": "source-a",
        "provider_group": group,
        "provider_id": "deepseek",
        "task_id": "electrochemical-conversion",
        "path": "ignored/matrix_report.json",
        "sha256": "abc",
    }


def _matrix() -> dict[str, object]:
    return {
        "expected_cell_count": 3,
        "elapsed_s": 2.0,
        "seed_reports": [
            {
                "world_seed": 0,
                "results": [
                    _result("opaque", 0.1),
                    _result("aligned_nominal", 0.2),
                    _result("misindexed_nominal", 0.3),
                ],
            }
        ],
    }


def test_single_provider_analysis_preserves_paired_denominators() -> None:
    manifest = {
        "analysis_id": "analysis-a",
        "analysis_date": "2026-08-10",
        "provider_group": "deepseek_recovery_amended",
        "interpretation_contract": {"limitations": ["development data only"]},
    }
    report = build_single_provider_development_analysis(
        manifest,
        [(_source(), _matrix())],
    )

    assert report["denominators"]["terminal_record_count"] == 3
    assert report["denominators"]["complete_experiment_count"] == 12
    assert report["complete_three_arm_cluster_count"] == 1
    contrast = report["task_reports"]["electrochemical-conversion"][
        "paired_endpoint_contrasts"
    ]["aligned_minus_opaque_best_score"]
    assert contrast["paired_seed_count"] == 1
    assert contrast["difference_summary"]["mean"] == pytest.approx(0.1)
    assert len(report["cell_records"]) == 3


def test_single_provider_analysis_rejects_mixed_provider_groups() -> None:
    manifest = {
        "analysis_id": "analysis-a",
        "analysis_date": "2026-08-10",
        "provider_group": "deepseek_recovery_amended",
        "interpretation_contract": {"limitations": []},
    }
    with pytest.raises(ValueError, match="cannot mix provider groups"):
        build_single_provider_development_analysis(
            manifest,
            [(_source("other_group"), _matrix())],
        )
