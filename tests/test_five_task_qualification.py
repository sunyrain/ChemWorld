from __future__ import annotations

from pathlib import Path

import pytest
from scripts.qualify_static_s0_five_tasks import (
    _load_object,
    _recipe_design_checks,
    _task_protocol,
)

from chemworld.eval.static_optimization_protocol import (
    validate_development_seed_policy,
    validate_static_optimization_protocol,
)
from chemworld.tasks import get_task
from chemworld.world.scoring import TaskScoringContract

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs/benchmark/static_s0_five_task_single_seed_qualification_v0.1_dev.json"
EXPECTED_TASK_IDS = [
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "flow-reaction-optimization",
]


def test_five_task_qualification_plan_is_seed0_only() -> None:
    plan = _load_object(PLAN_PATH)

    assert plan["task_ids"] == EXPECTED_TASK_IDS
    assert list(plan["tasks"]) == EXPECTED_TASK_IDS
    assert plan["seed_policy"] == {
        "world_seeds": [0],
        "algorithm_seeds": [0],
        "multi_seed_execution_allowed": False,
        "release_condition": (
            "every task must pass every single-seed qualification gate before "
            "any multi-seed execution"
        ),
    }
    for task_id in EXPECTED_TASK_IDS:
        protocol = _task_protocol(plan, task_id)
        validate_static_optimization_protocol(protocol)
        validate_development_seed_policy(protocol, algorithm_seed=0)
        with pytest.raises(ValueError, match="algorithm seed is outside"):
            validate_development_seed_policy(protocol, algorithm_seed=1)


@pytest.mark.parametrize("task_id", EXPECTED_TASK_IDS)
def test_five_task_qualification_design_and_score_contracts_are_live(
    task_id: str,
) -> None:
    plan = _load_object(PLAN_PATH)
    task = get_task(task_id)
    task_plan = plan["tasks"][task_id]

    design = _recipe_design_checks(
        task_id,
        task.to_dict(),
        int(task_plan["dimension"]),
    )
    scoring = TaskScoringContract.from_success_metrics(
        objective=task.objective,
        success_metrics=task.success_metrics,
        contract_id=task_plan["scoring_contract_id"],
    )

    assert design["passed"] is True
    assert design["dead_recipe_coordinates"] == []
    assert scoring.contract_id == task_plan["scoring_contract_id"]
    if task_id in {"partition-discovery", "flow-reaction-optimization"}:
        assert "reaction_score" not in scoring.component_weights
