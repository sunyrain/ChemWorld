from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.static_optimization_multiseed import (
    aggregate_static_optimization_runs,
)


def _write_run(root: Path, *, seed: int, scores: list[float]) -> None:
    root.mkdir(parents=True)
    report = {
        "method_config_sha256": "method-hash",
        "method_ids": ["method"],
        "provider_mode": "mock",
        "protocol_id": "s0-protocol",
        "protocol_sha256": f"protocol-{seed}",
        "completed_cell_count": 1,
        "cell_count": 1,
        "completed_experiment_count": len(scores),
        "planned_experiment_count": len(scores),
        "provider_call_count": len(scores),
        "provider_attempt_count": len(scores),
        "provider_reported_total_tokens": 100 * len(scores),
        "accounting_complete": False,
        "cells": [
            {
                "cell": {"world_seed": seed, "task_id": "task"},
                "cell_status": "completed",
                "completed_experiment_count": len(scores),
                "scores": scores,
                "experiments": [
                    {"decision_audit": {"prompt_estimated_tokens": 100 + index}}
                    for index in range(len(scores))
                ],
            }
        ],
    }
    audit = {
        "static_world_verified": True,
        "no_mechanism_fields_in_plans": True,
        "report_receipt_hashes_match": True,
        "replay": {"all_verified": True},
    }
    (root / "report.json").write_text(json.dumps(report), encoding="utf-8")
    (root / "postrun_audit.json").write_text(json.dumps(audit), encoding="utf-8")


def test_multiseed_aggregation_reports_task_curves(tmp_path: Path) -> None:
    first = tmp_path / "seed0"
    second = tmp_path / "seed1"
    _write_run(first, seed=0, scores=[0.1, 0.3, 0.2])
    _write_run(second, seed=1, scores=[0.2, 0.1, 0.4])

    report = aggregate_static_optimization_runs([first, second])

    assert report["seeds"] == [0, 1]
    assert report["completed_experiment_count"] == 6
    assert report["all_audits_passed"] is True
    task = report["tasks"][0]
    assert task["first_score"]["mean"] == pytest.approx(0.15)
    assert task["last_score"]["mean"] == pytest.approx(0.3)
    assert task["best_so_far_curve"][-1]["mean"] == pytest.approx(0.35)
    assert task["seed_rows"][0]["best_experiment_index"] == 1


def test_multiseed_aggregation_rejects_duplicate_seed(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    _write_run(first, seed=0, scores=[0.1])
    _write_run(second, seed=0, scores=[0.2])

    with pytest.raises(ValueError, match="duplicate S0 world seed"):
        aggregate_static_optimization_runs([first, second])
