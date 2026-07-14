from __future__ import annotations

import copy
from typing import Any

import pytest

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.operation_baselines import make_operation_baseline_agent
from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task


def _field(field: str, *, low: float = 0.0, high: float = 1.0) -> dict[str, Any]:
    return {
        "field": field,
        "bounds": {"low": low, "high": high},
        "recommended_range": {"low": low, "high": high},
    }


def _affordance(operation: str) -> dict[str, Any]:
    fields: list[dict[str, Any]] = []
    if operation == "add_solvent":
        fields = [
            _field("volume_L", high=0.08),
            {"field": "solvent", "choices": [0, 1, 2, 3]},
        ]
    elif operation == "wait":
        fields = [
            _field("duration_s", high=14400.0),
            _field("stirring_speed_rpm", low=100.0, high=1200.0),
        ]
    elif operation == "run_flow":
        fields = [
            _field("target_temperature_K", low=250.0, high=520.0),
            _field("duration_s", high=14400.0),
        ]
    elif operation == "measure":
        fields = [{"field": "instrument", "choices": ["uvvis", "final_assay"]}]
    return {
        "operation": operation,
        "valid": True,
        "schema": {"operation": operation, "fields": fields},
    }


def _view(*operations: str) -> dict[str, Any]:
    return {
        "tool_json": {
            "available_actions": [_affordance(operation) for operation in operations],
            "lab_report": {"visible_metrics": {}},
        }
    }


def _context(
    *operations: str,
    stage: str = "experiment_control",
    metrics: dict[str, Any] | None = None,
    task_id: str = "flow-reaction-optimization",
) -> AgentDecisionContext:
    return AgentDecisionContext(
        step=1,
        task_id=task_id,
        decision_stage=stage,
        campaign_state={"remaining_budget": 20},
        visible_metrics=dict(metrics or {}),
        latest_spectra={},
        uncertainty={},
        constraint_flags={},
        available_operations=tuple(operations),
        previous_event_type=None,
    )


def test_random_is_seeded_and_blind_control_ignores_metric_and_spectrum_payloads() -> None:
    task_info = get_task("flow-reaction-optimization").to_dict()
    left = make_operation_baseline_agent("operation_random")
    right = make_operation_baseline_agent("operation_random")
    left.reset(task_info, 17)
    right.reset(task_info, 17)
    context = _context("add_solvent", "wait", "measure")
    assert left.act_with_public_view(context, _view(*context.available_operations)) == (
        right.act_with_public_view(context, _view(*context.available_operations))
    )

    blind_a = make_operation_baseline_agent("observation_blind")
    blind_b = make_operation_baseline_agent("observation_blind")
    blind_a.reset(task_info, 1)
    blind_b.reset(task_info, 999)
    clean = _view("add_solvent", "wait", "measure")
    mutated = copy.deepcopy(clean)
    mutated["tool_json"]["raw_signal"] = {"hidden_like_decoy": [1, 2, 3]}
    mutated["tool_json"]["lab_report"]["visible_metrics"] = {"score": 0.99}
    action_a = blind_a.act_with_public_view(context, clean)
    action_b = blind_b.act_with_public_view(context, mutated)
    assert action_a == action_b
    assert blind_a.interaction_capabilities().consumes_intermediate_observations is False
    assert blind_a.interaction_capabilities().consumes_spectra is False


def test_rule_based_uses_only_public_measurement_for_one_retry() -> None:
    task_info = get_task("flow-reaction-optimization").to_dict()
    agent = make_operation_baseline_agent("rule_based")
    agent.reset(task_info, 7)
    context = _context(
        "run_flow",
        "terminate",
        stage="evidence_update",
        metrics={"flow_conversion": 0.2},
    )
    action = agent.act_with_public_view(context, _view(*context.available_operations))
    assert action["operation"] == "run_flow"
    audit = agent.decision_audit()
    assert audit is not None
    assert audit["adaptation_source"] == "measurement"
    assert "visible_metric:flow_conversion" in audit["evidence"]
    assert agent.interaction_capabilities().adapts_within_experiment is True
    assert agent.interaction_capabilities().adapts_across_experiments is False


def test_all_baselines_explicitly_request_final_assay_in_closeout() -> None:
    task_info = get_task("flow-reaction-optimization").to_dict()
    for method_id in ("operation_random", "observation_blind", "rule_based"):
        agent = make_operation_baseline_agent(method_id)
        agent.reset(task_info, 3)
        context = _context("measure", stage="experiment_closeout")
        assert agent.act_with_public_view(context, _view("measure")) == {
            "operation": "measure",
            "instrument": "final_assay",
        }


@pytest.mark.parametrize(
    "task_id",
    [
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    ],
)
@pytest.mark.parametrize("method_id", ["operation_random", "observation_blind", "rule_based"])
def test_real_runner_smoke_completes_with_audited_resources(
    task_id: str,
    method_id: str,
) -> None:
    task = get_task(task_id)
    experiments = 2
    operation_limit = 2 * task_recipe_event_count(task.to_dict()) * experiments
    history = run_agent(
        env_id=task.env_id,
        agent=make_operation_baseline_agent(method_id),
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=10_000,
        agent_seed=12345,
        task_id=task.task_id,
        budget_override=operation_limit,
        episode_mode_override="campaign",
        method_resource_limits={
            "operation_limit": operation_limit,
            "complete_experiment_limit": experiments,
            "checkpoint_complete_experiments": (1, 2),
        },
    )
    assert sum(record.event_type == "experiment_end" for record in history) == experiments
    invalid_actions = sum(
        bool(record.info.get("constraint_flags", {}).get("precondition_failed", False))
        for record in history
    )
    if method_id != "operation_random":
        assert invalid_actions == 0
    assert history[-1].method_resources["accounting_complete"] is True
    assert all(record.decision_audit["status"] == "provided" for record in history)
