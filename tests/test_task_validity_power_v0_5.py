from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.eval.task_validity_power_v0_5 import (
    load_task_validity_power_protocol,
    run_task_validity_power,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = (
    ROOT / "workstreams" / "world_foundation" / "reports" / "task-validity-power-v0.5.json"
)


def test_core4_surfaces_controls_and_sesoi_are_valid() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert set(report["core_tasks"]) == {
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    }
    for task in report["core_tasks"].values():
        assert task["sample_count"] == 60
        assert task["surface"]["spread"] >= 0.05
        assert task["surface"]["sesoi"] >= 0.02
        assert task["validity_ready"] is True
        assert all(task["checks"].values())


def test_risk_cost_limits_are_active_and_legacy_failures_are_exposed() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    legacy_failures = 0
    for task in report["core_tasks"].values():
        risk_cost = task["risk_cost"]
        assert 0.1 <= risk_cost["risk_activation_rate"] <= 0.3
        assert 0.05 <= risk_cost["process_cost_activation_rate"] <= 0.2
        legacy_failures += int(
            risk_cost["legacy_risk_activation_rate"] == 0.0
            or risk_cost["legacy_process_cost_activation_rate"] in {0.0, 1.0}
        )
    assert legacy_failures >= 1


def test_behavior_probes_are_diagnostics_not_method_results() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    for task in report["core_tasks"].values():
        probes = task["behavior_probes"]
        assert set(probes) == {
            "random_recipe",
            "local_primary_climb",
            "information_space_filling",
            "risk_blind_primary_oracle_probe",
        }
        assert all(item["formal_method_evidence"] is False for item in probes.values())
        assert max(item["mean_primary"] for item in probes.values()) - min(
            item["mean_primary"] for item in probes.values()
        ) >= task["surface"]["sesoi"]


def test_twenty_seed_joint_design_is_rejected_before_bench() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    recommendation = report["formal_design_recommendation"]
    assert recommendation["candidate_paired_seed_count"] == 20
    assert recommendation["recommended_paired_seed_count"] >= 100
    assert recommendation["twenty_paired_seeds_adequate"] is False
    assert all(
        task["power"]["safety_zero_adverse_required_seed_count"] == 99
        for task in report["core_tasks"].values()
    )


def test_tampered_surface_requirement_fails_closed() -> None:
    protocol = copy.deepcopy(load_task_validity_power_protocol())
    protocol["surface"]["minimum_primary_spread"] = 1.1
    report = run_task_validity_power(protocol)
    assert report["controls_ready"] is False
    assert all(
        task["checks"]["primary_dynamic_range"] is False
        for task in report["core_tasks"].values()
    )
