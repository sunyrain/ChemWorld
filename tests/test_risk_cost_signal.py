from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.risk_cost_signal_audit import (
    RiskCostTaskPolicy,
    load_risk_cost_protocol,
)
from chemworld.tasks import SERIOUS_TASK_IDS

ROOT = Path(__file__).resolve().parents[1]
FROZEN_REPORT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "risk-cost-signal-controls.json"


def test_risk_cost_protocol_has_task_specific_limits() -> None:
    protocol = load_risk_cost_protocol()
    assert tuple(protocol["tasks"]) == SERIOUS_TASK_IDS
    policies = [RiskCostTaskPolicy.from_protocol(task_id, protocol) for task_id in SERIOUS_TASK_IDS]
    assert len({policy.risk_limit for policy in policies}) == len(SERIOUS_TASK_IDS)
    assert len({policy.process_cost_limit for policy in policies}) == len(SERIOUS_TASK_IDS)


def test_vnext_task_info_overlay_is_explicit_and_non_physical() -> None:
    protocol = load_risk_cost_protocol()
    policy = RiskCostTaskPolicy.from_protocol("flow-reaction-optimization", protocol)
    overlay = policy.task_info_overlay()
    assert overlay["safety_limit"] == pytest.approx(policy.risk_limit)
    assert overlay["risk_aggregation"] == "max_operation_risk_per_experiment"
    assert "not_real_world_safety" in overlay["risk_limit_semantics"]


def test_frozen_risk_cost_report_keeps_method_and_measurement_gates_closed() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["risk_process_signal_identifiable"] is True
    assert report["measurement_policy_identifiable"] is False
    assert report["formal_method_comparison_ready"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["checks"]["formal_scope"] is True
    assert report["checks"]["experiment_matrix_complete"] is True
    tradeoff_tasks = {
        task_id
        for task_id, task_report in report["tasks"].items()
        if task_report["risk_tradeoff_task"]
    }
    assert tradeoff_tasks == {
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    }
