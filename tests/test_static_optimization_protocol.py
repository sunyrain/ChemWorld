from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.static_optimization_protocol import (
    exploration_experiment_count,
    static_optimization_material_family_id,
    static_optimization_scoring_contract_id,
    static_optimization_workflow_mode,
    validate_development_seed_policy,
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
from chemworld.world.electrochemical_material_family import (
    NOMINAL_PRIOR_MATERIAL_FAMILY,
)
from chemworld.world.scoring import (
    DISTILLATION_S0_BALANCED_AUDIT_SAFETY_V2,
    ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2,
    FLOW_S0_BALANCED_PROCESS_V1,
    PARTITION_S0_EXTRACTION_EFFICIENCY_V2,
    TaskScoringContract,
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
    protocol["world_policy"]["electrochemical_material_family_id"] = "nominal-prior-latent-v2"
    protocol["reward_contract"] = {
        "scoring_contract_id": "electrochemical-s0-balanced-efficiency-v2"
    }
    validate_static_optimization_protocol(protocol)
    assert (
        static_optimization_workflow_mode(protocol) == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
    )


def test_non_electrochemical_protocol_has_no_irrelevant_workflow_requirement() -> None:
    protocol = _protocol("reaction-to-crystallization")

    validate_static_optimization_protocol(protocol)

    assert (
        static_optimization_workflow_mode(protocol) == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
    )


def test_formal_declared_diagnostics_without_reference_must_be_explicitly_unscored() -> None:
    protocol = _protocol("reaction-to-crystallization")
    protocol["formal_result"] = True
    protocol["world_understanding"] = {
        "enabled": True,
        "declared_claims_are_secondary_diagnostics": True,
        "predictive_score_enabled": False,
    }

    with pytest.raises(ValueError, match="declared_scoring_enabled=false"):
        validate_static_optimization_protocol(protocol)

    protocol["world_understanding"]["declared_scoring_enabled"] = False
    protocol["secondary_metrics"] = ["world_understanding_structural_edge_f1"]
    with pytest.raises(ValueError, match="structural F1"):
        validate_static_optimization_protocol(protocol)

    protocol["secondary_metrics"] = ["best_exploration_score"]
    validate_static_optimization_protocol(protocol)


def test_static_protocol_rejects_budget_alias_drift() -> None:
    protocol = _protocol("reaction-to-crystallization")
    protocol["horizon"] = 7

    with pytest.raises(ValueError, match="budget disagree"):
        exploration_experiment_count(protocol)


def test_historical_electrochemical_protocols_declare_their_legacy_mode() -> None:
    root = Path(__file__).resolve().parents[1]
    for path in sorted((root / "configs" / "benchmark").glob("scientific_optimization_s0_*.json")):
        protocol = json.loads(path.read_text(encoding="utf-8"))
        if "electrochemical-conversion" not in protocol.get("tasks", []):
            continue
        executor = protocol.get("executor_contract", {})
        assert executor.get("electrochemical_workflow_mode") in {
            ELECTROCHEMICAL_WORKFLOW_ADAPTIVE_TWO_STAGE,
            ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
        }, path.name


def test_nominal_material_family_is_explicit_and_electrochemical_only() -> None:
    protocol = _protocol("electrochemical-conversion")
    protocol["executor_contract"] = {
        "atomic_complete_experiment": True,
        "electrochemical_workflow_mode": ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    }
    protocol["world_policy"]["electrochemical_material_family_id"] = NOMINAL_PRIOR_MATERIAL_FAMILY
    protocol["reward_contract"] = {
        "scoring_contract_id": "electrochemical-s0-balanced-efficiency-v2"
    }
    protocol["material_information"] = {"mode": "anonymous_nominal_properties"}

    validate_static_optimization_protocol(protocol)
    assert static_optimization_material_family_id(protocol) == (NOMINAL_PRIOR_MATERIAL_FAMILY)
    assert static_optimization_scoring_contract_id(protocol) == (
        ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2
    )

    protocol["tasks"] = ["reaction-to-crystallization"]
    with pytest.raises(ValueError, match="require exactly"):
        validate_static_optimization_protocol(protocol)


def test_electrochemical_s0_v2_score_has_no_composite_double_counting() -> None:
    from chemworld.tasks import get_task

    task = get_task("electrochemical-conversion")
    contract = TaskScoringContract.from_success_metrics(
        objective=task.objective,
        success_metrics=task.success_metrics,
        contract_id=ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2,
    )

    assert "reaction_score" not in contract.component_weights
    assert "cost" not in contract.component_weights
    assert "safety_risk" not in contract.component_weights
    assert sum(contract.component_weights.values()) == pytest.approx(1.0)
    assert contract.component_weights == {
        "selective_product_yield": 0.30,
        "electrochemical_selectivity": 0.15,
        "electrochemical_conversion": 0.10,
        "faradaic_efficiency": 0.12,
        "transport_efficiency": 0.10,
        "ohmic_efficiency": 0.08,
        "energy_efficiency": 0.15,
    }


def test_distillation_s0_v2_scoring_contract_is_task_scoped() -> None:
    protocol = _protocol("reaction-to-distillation")
    protocol["reward_contract"] = {"scoring_contract_id": DISTILLATION_S0_BALANCED_AUDIT_SAFETY_V2}

    assert static_optimization_scoring_contract_id(protocol) == (
        DISTILLATION_S0_BALANCED_AUDIT_SAFETY_V2
    )

    protocol["tasks"] = ["reaction-optimization-standard"]
    with pytest.raises(ValueError, match="requires exactly"):
        static_optimization_scoring_contract_id(protocol)


@pytest.mark.parametrize(
    ("task_id", "contract_id", "other_task"),
    [
        (
            "partition-discovery",
            PARTITION_S0_EXTRACTION_EFFICIENCY_V2,
            "flow-reaction-optimization",
        ),
        (
            "flow-reaction-optimization",
            FLOW_S0_BALANCED_PROCESS_V1,
            "partition-discovery",
        ),
    ],
)
def test_extended_s0_scoring_contracts_are_task_scoped(
    task_id: str,
    contract_id: str,
    other_task: str,
) -> None:
    protocol = _protocol(task_id)
    protocol["reward_contract"] = {"scoring_contract_id": contract_id}

    assert static_optimization_scoring_contract_id(protocol) == contract_id

    protocol["tasks"] = [other_task]
    with pytest.raises(ValueError, match="requires exactly"):
        static_optimization_scoring_contract_id(protocol)


def test_single_seed_development_policy_rejects_seed_expansion() -> None:
    protocol = _protocol("partition-discovery")
    protocol["world_policy"]["world_seed"] = 0
    protocol["algorithm_seeds"] = [0]
    protocol["development_seed_policy"] = {
        "world_seeds": [0],
        "algorithm_seeds": [0],
        "multi_seed_execution_allowed": False,
    }

    validate_static_optimization_protocol(protocol)
    validate_development_seed_policy(protocol, algorithm_seed=0)

    with pytest.raises(ValueError, match="algorithm seed is outside"):
        validate_development_seed_policy(protocol, algorithm_seed=1)

    protocol["world_policy"]["world_seed"] = 1
    with pytest.raises(ValueError, match="world seed is outside"):
        validate_static_optimization_protocol(protocol)


def test_material_pilot_protocols_differ_only_by_information_condition() -> None:
    root = Path(__file__).resolve().parents[1] / "configs" / "benchmark"
    paths = [
        root / "scientific_optimization_s0_v0.6_material_pilot_opaque_8_dev.json",
        root / "scientific_optimization_s0_v0.6_material_pilot_nominal_8_dev.json",
        root / "scientific_optimization_s0_v0.6_material_pilot_shuffled_8_dev.json",
    ]
    protocols = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    for protocol in protocols:
        validate_static_optimization_protocol(protocol)

    normalized = []
    for protocol in protocols:
        comparable = dict(protocol)
        comparable.pop("protocol_id")
        comparable.pop("condition_id")
        comparable.pop("material_information")
        normalized.append(comparable)
    assert normalized[0] == normalized[1] == normalized[2]


def test_retired_semantic_profile_and_shared_prefix_fail_closed() -> None:
    protocol = _protocol("electrochemical-conversion")
    protocol["executor_contract"] = {
        "atomic_complete_experiment": True,
        "electrochemical_workflow_mode": ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    }
    protocol["world_policy"]["electrochemical_semantic_profile_id"] = "retired"
    with pytest.raises(ValueError, match="semantic profiles were retired"):
        validate_static_optimization_protocol(protocol)

    del protocol["world_policy"]["electrochemical_semantic_profile_id"]
    protocol["shared_calibration_prefix"] = {"experiments": []}
    with pytest.raises(ValueError, match="shared calibration prefixes were retired"):
        validate_static_optimization_protocol(protocol)


def test_static_observation_seed_namespaces_remain_stable_and_distinct() -> None:
    exploration = exploration_observation_seed("electrochemical-conversion", 3)
    validation = validation_observation_seed("electrochemical-conversion", 3, "paired-replicate", 0)
    predictive = predictive_observation_seed("electrochemical-conversion", 3, "potential_V-high", 0)

    assert exploration == exploration_observation_seed("electrochemical-conversion", 3)
    assert len({exploration, validation, predictive}) == 3
