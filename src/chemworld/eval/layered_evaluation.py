"""Layered vNext evaluation without changing frozen v0.1 result semantics."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Literal

from chemworld.task_design import SERIOUS_TASK_DESIGNS
from chemworld.tasks import get_task

LAYERED_EVALUATION_VERSION = "chemworld-layered-evaluation-0.1"


@dataclass(frozen=True)
class TaskEvaluationContract:
    task_id: str
    objective_metric: str
    primary_task_metric: str
    direction: Literal["maximize", "minimize"]
    terminal_selector: Literal["successful_final_assay"]
    online_reward_role: Literal["diagnostic_shaping_only"]
    safety_limit: float
    cost_aggregation: Literal["sum_terminal_experiment_costs"]
    missing_primary_policy: Literal["fail"] = "fail"

    def __post_init__(self) -> None:
        if not 0.0 < self.safety_limit <= 1.0:
            raise ValueError("safety_limit must be in (0, 1]")
        if not self.primary_task_metric:
            raise ValueError("primary_task_metric cannot be empty")

    @classmethod
    def for_task(cls, task_id: str) -> TaskEvaluationContract:
        task = get_task(task_id)
        design = SERIOUS_TASK_DESIGNS[task_id]
        return cls(
            task_id=task_id,
            objective_metric="leaderboard_score",
            primary_task_metric=design.primary_metric,
            direction="maximize",
            terminal_selector="successful_final_assay",
            online_reward_role="diagnostic_shaping_only",
            safety_limit=task.safety_limit,
            cost_aggregation="sum_terminal_experiment_costs",
        )

    @property
    def contract_hash(self) -> str:
        payload = asdict(self)
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": LAYERED_EVALUATION_VERSION,
            **asdict(self),
            "contract_hash": self.contract_hash,
            "layers": {
                "objective": self.objective_metric,
                "task_primary": self.primary_task_metric,
                "online_shaping": self.online_reward_role,
                "constraint": "safety_risk and unsafe flag",
                "resource": self.cost_aggregation,
                "validity": "precondition and constitution flags",
            },
        }


def evaluate_layered_records(
    records: list[dict[str, Any]],
    *,
    contract: TaskEvaluationContract,
) -> dict[str, Any]:
    """Recompute five disjoint evaluation layers from a public trajectory."""

    if not records:
        raise ValueError("cannot evaluate an empty trajectory")
    terminal_records = [
        record for record in records if record.get("leaderboard_score") is not None
    ]
    if not terminal_records:
        raise ValueError("trajectory has no successful final assay")
    primary_values = [
        _required_observation(record, contract.primary_task_metric)
        for record in terminal_records
    ]
    objective_values = [
        _finite_float(record["leaderboard_score"], "leaderboard_score")
        for record in terminal_records
    ]
    terminal_costs = [
        _required_observation(record, "cost") for record in terminal_records
    ]
    observed_risks = [
        _finite_float(record["observation"]["safety_risk"], "safety_risk")
        for record in records
        if isinstance(record.get("observation"), dict)
        and record["observation"].get("safety_risk") is not None
    ]
    flags = [
        record.get("constraint_flags", {})
        if isinstance(record.get("constraint_flags"), dict)
        else {}
        for record in records
    ]
    unsafe_count = sum(bool(item.get("unsafe")) for item in flags)
    high_cost_count = sum(bool(item.get("high_cost")) for item in flags)
    invalid_count = sum(
        bool(item.get("precondition_failed")) or bool(item.get("constitution_failed"))
        for item in flags
    )
    rewards = [_finite_float(record.get("reward", 0.0), "reward") for record in records]
    measurement_cost = sum(
        _finite_float(record.get("measurement_cost", 0.0), "measurement_cost")
        for record in records
    )
    maximize = contract.direction == "maximize"
    select = max if maximize else min
    return {
        "schema_version": LAYERED_EVALUATION_VERSION,
        "task_id": contract.task_id,
        "evaluation_contract_hash": contract.contract_hash,
        "status": "evaluated",
        "objective": {
            "metric": contract.objective_metric,
            "best": select(objective_values),
            "last": objective_values[-1],
            "terminal_values": objective_values,
        },
        "task_primary": {
            "metric": contract.primary_task_metric,
            "best": select(primary_values),
            "last": primary_values[-1],
            "terminal_values": primary_values,
        },
        "online_shaping": {
            "role": contract.online_reward_role,
            "mean_reward": sum(rewards) / len(rewards),
            "reward_sum": sum(rewards),
            "eligible_as_primary_endpoint": False,
        },
        "constraints": {
            "safety_limit": contract.safety_limit,
            "max_observed_safety_risk": max(observed_risks) if observed_risks else None,
            "unsafe_operation_count": unsafe_count,
            "high_cost_operation_count": high_cost_count,
            "constraint_activated": unsafe_count > 0,
        },
        "resources": {
            "campaign_process_cost": sum(terminal_costs),
            "terminal_experiment_costs": terminal_costs,
            "measurement_cost": measurement_cost,
            "operation_count": len(records),
            "complete_experiment_count": len(terminal_records),
        },
        "validity": {
            "invalid_operation_count": invalid_count,
            "invalid_operation_rate": invalid_count / len(records),
        },
    }


def _required_observation(record: dict[str, Any], key: str) -> float:
    observation = record.get("observation")
    if not isinstance(observation, dict) or observation.get(key) is None:
        raise ValueError(f"successful final assay is missing required {key!r}")
    return _finite_float(observation[key], key)


def _finite_float(value: Any, field: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number


__all__ = [
    "LAYERED_EVALUATION_VERSION",
    "TaskEvaluationContract",
    "evaluate_layered_records",
]
