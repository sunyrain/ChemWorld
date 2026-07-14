from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.agents.random import RandomRecipeAgent
from chemworld.data.logging import load_jsonl
from chemworld.eval.risk_cost_signal_audit import (
    RiskCostTaskPolicy,
    _experiment_rows,
    load_risk_cost_protocol,
)
from chemworld.eval.runner import run_agent
from chemworld.tasks import SERIOUS_TASK_IDS, get_task

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
    assert len(policy.policy_hash) == 64


def test_official_runner_binds_vnext_policy_to_agent_environment_and_trajectory(
    tmp_path: Path,
) -> None:
    task_id = "partition-discovery"
    policy = RiskCostTaskPolicy.from_protocol(task_id, load_risk_cost_protocol())
    agent = RandomRecipeAgent()
    trajectory = tmp_path / "risk-bound.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=agent,
        world_split="public-dev",
        budget=get_task(task_id).budget,
        objective="balanced",
        seed=3,
        task_id=task_id,
        output_path=trajectory,
        evaluation_policy="vnext_risk_cost",
    )
    records = load_jsonl(trajectory)
    assert history
    assert records
    assert agent.task_info["safety_limit"] == pytest.approx(policy.risk_limit)
    assert agent.task_info["risk_limit_semantics"] == policy.risk_semantics
    assert records[0]["safety_limit"] == pytest.approx(policy.risk_limit)
    assert records[0]["agent_metadata"]["evaluation_policy"] == "vnext_risk_cost"
    assert records[0]["agent_metadata"]["risk_policy_hash"] == policy.policy_hash
    for record in records:
        risk = record["observation"]["safety_risk"]
        if risk is not None:
            assert record["constraint_flags"]["unsafe"] is (risk >= policy.risk_limit)


def test_vnext_policy_requires_a_registered_serious_task() -> None:
    with pytest.raises(ValueError, match="registered serious task_id"):
        run_agent(
            env_id="ChemWorld",
            agent=RandomRecipeAgent(),
            world_split="public-dev",
            budget=1,
            objective="balanced",
            seed=0,
            evaluation_policy="vnext_risk_cost",
        )


def test_risk_cost_rows_use_unsaturated_ledger_deltas(tmp_path: Path) -> None:
    trajectory = tmp_path / "saturated-cost.jsonl"
    records = [
        {
            "observation": {"cost": 0.9, "safety_risk": 0.1},
            "measurement_cost": 0.0,
            "state_delta_summary": {"delta_cost": 0.9},
            "leaderboard_score": None,
        },
        {
            "observation": {"cost": 1.0, "safety_risk": 0.1},
            "measurement_cost": 0.8,
            "state_delta_summary": {"delta_cost": 0.8},
            "leaderboard_score": 0.5,
        },
    ]
    trajectory.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )

    rows = _experiment_rows(
        {
            "task_id": "partition-discovery",
            "baseline_agent": "test-agent",
            "seed": 1,
        },
        trajectory,
    )

    assert rows[0]["total_cost"] == pytest.approx(1.7)
    assert rows[0]["measurement_cost"] == pytest.approx(0.8)
    assert rows[0]["process_cost"] == pytest.approx(0.9)


def test_frozen_risk_cost_report_keeps_method_and_measurement_gates_closed() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["risk_process_signal_identifiable"] is True
    assert report["measurement_policy_identifiable"] is False
    assert report["formal_method_comparison_ready"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["checks"]["formal_scope"] is True
    assert report["checks"]["experiment_matrix_complete"] is True
    assert report["checks"]["runner_binding_declared"] is True
    assert not any("expose the frozen" in gate for gate in report["remaining_release_gates"])
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
