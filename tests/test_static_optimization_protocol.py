from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.static_optimization_protocol import (
    exploration_experiment_count,
    static_optimization_workflow_mode,
    validate_static_optimization_protocol,
)
from chemworld.eval.static_optimization_seeds import (
    exploration_observation_seed,
    predictive_observation_seed,
    validation_observation_seed,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_ADAPTIVE_TWO_STAGE,
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
)


def _protocol(task_id: str) -> dict[str, object]:
    return {
        "tasks": [task_id],
        "horizon": 8,
        "scientific_campaign_budget": {
            "exploration_experiments": 8,
            "final_synthesis_after_exploration": True,
        },
        "world_policy": {
            "mode": "static_for_entire_campaign",
            "interventions": [],
            "phase_changes": [],
            "hidden_world_fields_in_public_context": False,
        },
        "executor_contract": {"atomic_complete_experiment": True},
        "final_synthesis": {"enabled": True},
    }


def test_electrochemical_static_protocol_requires_explicit_workflow() -> None:
    protocol = _protocol("electrochemical-conversion")

    with pytest.raises(ValueError, match="explicitly declare"):
        validate_static_optimization_protocol(protocol)

    protocol["executor_contract"] = {
        "atomic_complete_experiment": True,
        "electrochemical_workflow_mode": ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    }
    validate_static_optimization_protocol(protocol)
    assert (
        static_optimization_workflow_mode(protocol)
        == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
    )


def test_non_electrochemical_protocol_has_no_irrelevant_workflow_requirement() -> None:
    protocol = _protocol("reaction-to-crystallization")

    validate_static_optimization_protocol(protocol)

    assert (
        static_optimization_workflow_mode(protocol)
        == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
    )


def test_static_protocol_rejects_budget_alias_drift() -> None:
    protocol = _protocol("reaction-to-crystallization")
    protocol["horizon"] = 7

    with pytest.raises(ValueError, match="budget disagree"):
        exploration_experiment_count(protocol)


def test_historical_electrochemical_protocols_declare_their_legacy_mode() -> None:
    root = Path(__file__).resolve().parents[1]
    for path in sorted(
        (root / "configs" / "benchmark").glob("scientific_optimization_s0_*.json")
    ):
        protocol = json.loads(path.read_text(encoding="utf-8"))
        if "electrochemical-conversion" not in protocol.get("tasks", []):
            continue
        executor = protocol.get("executor_contract", {})
        assert executor.get("electrochemical_workflow_mode") in {
            ELECTROCHEMICAL_WORKFLOW_ADAPTIVE_TWO_STAGE,
            ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
        }, path.name


def test_static_observation_seed_namespaces_remain_stable_and_distinct() -> None:
    exploration = exploration_observation_seed("electrochemical-conversion", 3)
    validation = validation_observation_seed(
        "electrochemical-conversion", 3, "paired-replicate", 0
    )
    predictive = predictive_observation_seed(
        "electrochemical-conversion", 3, "potential_V-high", 0
    )

    assert exploration == exploration_observation_seed(
        "electrochemical-conversion", 3
    )
    assert len({exploration, validation, predictive}) == 3
