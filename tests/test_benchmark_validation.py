from __future__ import annotations

import json
from copy import deepcopy

from chemworld.eval.baseline_report import SERIOUS_BASELINE_AGENTS
from chemworld.eval.benchmark_validation import (
    BENCHMARK_VALIDATION_SCHEMA_VERSION,
    PRIMARY_METRIC_FIELDS,
    load_official_validation,
    official_empirical_statuses,
    validate_serious_baseline_report,
)
from chemworld.tasks import SERIOUS_TASK_IDS, get_task


def _passing_report() -> dict:
    rows = []
    for task_index, task_id in enumerate(SERIOUS_TASK_IDS):
        task = get_task(task_id)
        for agent_index, agent_name in enumerate(SERIOUS_BASELINE_AGENTS):
            score = 0.10 + 0.025 * agent_index + 0.005 * task_index
            rows.append(
                {
                    "task_id": task_id,
                    "agent_name": agent_name,
                    "runs": len(task.seeds),
                    "seeds": list(task.seeds),
                    "mean_total_score": score,
                    "mean_invalid_action_rate": 0.0,
                    "mean_final_assay_count": 3.0,
                    "success_rate": 0.2 + 0.1 * agent_index,
                    "mean_bo_entered_acquisition": (
                        1.0 if agent_name in {"gp_bo", "safe_gp_bo"} else 0.0
                    ),
                    "mean_bo_acquisition_recipe_count": (
                        1.5 if agent_name in {"gp_bo", "safe_gp_bo"} else 0.0
                    ),
                    PRIMARY_METRIC_FIELDS[task_id]: 0.2 + 0.02 * agent_index,
                }
            )
    return {"schema_version": "chemworld-baseline-report-test", "summary_rows": rows}


def test_empirical_validator_accepts_complete_task_valid_evidence() -> None:
    validation = validate_serious_baseline_report(_passing_report())
    assert validation["validated"] is True
    assert validation["validated_task_count"] == len(SERIOUS_TASK_IDS)
    assert all(item["validated"] for item in validation["task_evidence"].values())


def test_empirical_validator_rejects_invalid_or_shallow_baseline() -> None:
    report = deepcopy(_passing_report())
    target = next(
        row
        for row in report["summary_rows"]
        if row["task_id"] == "partition-discovery" and row["agent_name"] == "gp_bo"
    )
    target["mean_invalid_action_rate"] = 0.2
    target["mean_bo_entered_acquisition"] = 0.0
    validation = validate_serious_baseline_report(report)
    assert validation["validated"] is False
    checks = {
        item["check_id"]: item
        for item in validation["task_evidence"]["partition-discovery"]["checks"]
    }
    assert checks["valid_actions"]["passed"] is False
    assert checks["active_learning_phase"]["passed"] is False


def test_official_evidence_rejects_incomplete_coverage(tmp_path) -> None:
    path = tmp_path / "validation.json"
    path.write_text(
        '{"schema_version": "' + BENCHMARK_VALIDATION_SCHEMA_VERSION + '"}',
        encoding="utf-8",
    )
    try:
        load_official_validation(path)
    except ValueError as error:
        assert "task coverage" in str(error)
    else:
        raise AssertionError("incomplete official validation was accepted")


def test_official_evidence_is_bound_to_current_task_hashes(tmp_path) -> None:
    validation = validate_serious_baseline_report(_passing_report())
    validation["task_evidence"]["partition-discovery"]["task_contract_hash"] = "stale"
    path = tmp_path / "validation.json"
    path.write_text(json.dumps(validation), encoding="utf-8")
    statuses = official_empirical_statuses(path)
    assert statuses["partition-discovery"] == "candidate"
    assert all(
        status == "validated"
        for task_id, status in statuses.items()
        if task_id != "partition-discovery"
    )
