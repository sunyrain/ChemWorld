from __future__ import annotations

from dataclasses import replace

import gymnasium as gym
import numpy as np
import pytest

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import (
    CONSTITUTIVE_MECHANISM_TASKS,
    REACTION_MECHANISM_TASKS,
    ConstitutiveLawFamilyChange,
    MechanismFamilyIntervention,
    RateLawFamilyChange,
    TopologyFamilyChange,
    derive_mechanism_family,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario


def _intervention(mode: str, severity: float = 0.8) -> dict:
    return {"kind": "mechanism_family", "mode": mode, "severity": severity}


def _run_midpoint(task_id: str, mode: str | None) -> tuple[float, dict]:
    kwargs = get_task(task_id).env_kwargs(seed=0)
    if mode is not None:
        kwargs["world_interventions"] = [_intervention(mode)]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=0)
        task_info = env.unwrapped.task_info()
        recipe = task_recipe_from_unit_vector(
            task_info,
            np.full(task_recipe_dimension(task_info), 0.5),
        )
        observation: dict = {}
        info: dict = {}
        for action in recipe["steps"]:
            observation, _, _, _, info = env.step(action)
        observation["_audit_mass_balance_error"] = np.asarray(
            [info["raw_signal"]["mass_balance"]["process_mass_balance_error"]]
        )
        return float(info["leaderboard_score"]), observation
    finally:
        env.close()


@pytest.mark.parametrize("task_id", REACTION_MECHANISM_TASKS)
@pytest.mark.parametrize("mode", ["rate_law_family", "topology_family"])
def test_mechanism_family_changes_hash_structure_and_task_response(
    task_id: str,
    mode: str,
) -> None:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(task_id)
    base = generator.generate(scenario, 0)
    shifted = generator.generate(scenario, 0, (_intervention(mode),))
    repeated = generator.generate(scenario, 0, (_intervention(mode),))
    assert shifted.compiled_mechanism.mechanism_hash != base.compiled_mechanism.mechanism_hash
    assert shifted.compiled_mechanism.mechanism_hash == repeated.compiled_mechanism.mechanism_hash
    assert shifted.parameters.world_id != base.parameters.world_id
    assert shifted.compiled_mechanism.mechanism_id.startswith("mechanism-family-")
    if mode == "topology_family":
        assert (
            len(shifted.compiled_mechanism.network.reactions)
            == len(base.compiled_mechanism.network.reactions) + 1
        )
    else:
        base_laws = [r.rate_law.equation_id for r in base.compiled_mechanism.network.reactions]
        shifted_laws = [
            r.rate_law.equation_id for r in shifted.compiled_mechanism.network.reactions
        ]
        assert shifted_laws != base_laws
    base_score, base_observation = _run_midpoint(task_id, None)
    shifted_score, shifted_observation = _run_midpoint(task_id, mode)
    task = get_task(task_id)
    deltas = [abs(shifted_score - base_score)]
    deltas.extend(
        abs(float(shifted_observation[key][0]) - float(base_observation[key][0]))
        for key in task.success_metrics
        if shifted_observation.get(key) is not None and base_observation.get(key) is not None
    )
    assert max(deltas) > 1.0e-8


def test_partition_constitutive_family_changes_executed_law_not_reaction_network() -> None:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("partition-discovery")
    base = generator.generate(scenario, 0)
    intervention = (_intervention("constitutive_law_family"),)
    shifted = generator.generate(scenario, 0, intervention)
    repeated = generator.generate(scenario, 0, intervention)
    assert shifted.compiled_mechanism.mechanism_hash == base.compiled_mechanism.mechanism_hash
    assert shifted.parameters.domain_parameter(
        "partition_coefficient_exponent"
    ) > base.parameters.domain_parameter("partition_coefficient_exponent")
    assert (
        shifted.initial_state.metadata["mechanism_family_intervention_hash"]
        == (repeated.initial_state.metadata["mechanism_family_intervention_hash"])
    )
    assert ":mechanism-" in shifted.parameters.world_id
    base_score, _ = _run_midpoint("partition-discovery", None)
    shifted_score, shifted_observation = _run_midpoint(
        "partition-discovery",
        "constitutive_law_family",
    )
    assert abs(shifted_score - base_score) > 1.0e-8
    assert float(shifted_observation["_audit_mass_balance_error"][0]) <= 1.0e-8


@pytest.mark.parametrize("task_id", CONSTITUTIVE_MECHANISM_TASKS)
def test_constitutive_family_changes_executed_provider_without_network_rewrite(
    task_id: str,
) -> None:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(task_id)
    base = generator.generate(scenario, 0)
    shifted = generator.generate(
        scenario,
        0,
        (_intervention("constitutive_law_family"),),
    )
    assert shifted.compiled_mechanism.mechanism_hash == base.compiled_mechanism.mechanism_hash
    assert shifted.initial_state.metadata["mechanism_family_intervention_hash"]
    base_score, _ = _run_midpoint(task_id, None)
    shifted_score, shifted_observation = _run_midpoint(
        task_id,
        "constitutive_law_family",
    )
    assert abs(shifted_score - base_score) > 1.0e-8
    assert float(shifted_observation["_audit_mass_balance_error"][0]) <= 1.0e-8


def test_electrochemical_constitutive_change_is_explicit_and_calibrated() -> None:
    intervention = MechanismFamilyIntervention(
        "constitutive_law_family",
        0.8,
        constitutive_law_change=ConstitutiveLawFamilyChange(
            transform_id="electrochemical_response_stress_v1",
            transfer_asymmetry_multiplier_at_full_severity=1.4,
            selectivity_decay_multiplier_at_full_severity=3.0,
            standard_potential_multiplier_at_full_severity=1.25,
        ),
    )
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("electrochemical-conversion")
    baseline = generator.generate(scenario, 0)
    shifted = generator.generate(scenario, 0, (intervention.to_dict(),))

    assert shifted.compiled_mechanism.mechanism_hash == (
        baseline.compiled_mechanism.mechanism_hash
    )
    assert shifted.parameters.domain_parameter(
        "electro_transfer_asymmetry_multiplier"
    ) == pytest.approx(1.32)
    assert shifted.parameters.domain_parameter(
        "electro_selectivity_decay_multiplier"
    ) == pytest.approx(2.6)
    assert shifted.parameters.domain_parameter(
        "electro_standard_potential_multiplier"
    ) == pytest.approx(1.2)
    assert (
        shifted.initial_state.metadata["derived_constitutive_transform_id"]
        == "electrochemical_response_stress_v1"
    )


def test_electrochemical_constitutive_change_contract_round_trips() -> None:
    payload = {
        "kind": "mechanism_family",
        "mode": "constitutive_law_family",
        "severity": 0.8,
        "constitutive_law_change": {
            "transform_id": "electrochemical_response_stress_v1",
            "transfer_asymmetry_multiplier_at_full_severity": 1.4,
            "selectivity_decay_multiplier_at_full_severity": 3.0,
            "standard_potential_multiplier_at_full_severity": 1.25,
        },
    }
    assert MechanismFamilyIntervention.from_dict(payload).to_dict() == payload


def test_constitutive_change_rejects_task_transform_mismatch() -> None:
    intervention = MechanismFamilyIntervention(
        "constitutive_law_family",
        0.8,
        constitutive_law_change=ConstitutiveLawFamilyChange(
            transform_id="partition_power_response_stress_v1",
            partition_coefficient_exponent_at_full_severity=1.75,
        ),
    )
    with pytest.raises(ValueError, match="requires 'electrochemical_response_stress_v1'"):
        DefaultScenarioGenerator().generate(
            get_scenario("electrochemical-conversion"),
            0,
            (intervention.to_dict(),),
        )


@pytest.mark.parametrize(
    "task_id",
    ["electrochemical-conversion", "equilibrium-characterization"],
)
def test_nonreaction_tasks_reject_reaction_network_modes(task_id: str) -> None:
    with pytest.raises(ValueError, match="not causally reachable"):
        DefaultScenarioGenerator().generate(
            get_scenario(task_id),
            0,
            (_intervention("topology_family"),),
        )


def test_zero_intervention_preserves_frozen_mechanism() -> None:
    scenario = get_scenario("reaction-to-crystallization")
    generator = DefaultScenarioGenerator()
    base = generator.generate(scenario, 0)
    empty = generator.generate(scenario, 0, ())
    assert empty.compiled_mechanism.mechanism_hash == base.compiled_mechanism.mechanism_hash
    assert empty.parameters.world_id == base.parameters.world_id
    assert empty.parameters.domain_parameter("partition_coefficient_exponent") == 1.0


@pytest.mark.parametrize(
    ("task_id", "expected_reaction_id"),
    [
        ("reaction-to-crystallization", "side_formation"),
        ("reaction-to-distillation", "ether_side_reaction"),
        ("flow-reaction-optimization", "side_high_temperature"),
    ],
)
def test_default_rate_law_family_binds_the_primary_competing_pathway(
    task_id: str,
    expected_reaction_id: str,
) -> None:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(task_id)
    base = generator.generate(scenario, 0)
    shifted = generator.generate(scenario, 0, (_intervention("rate_law_family"),))

    changed_reactions = [
        before.reaction_id
        for before, after in zip(
            base.compiled_mechanism.network.reactions,
            shifted.compiled_mechanism.network.reactions,
            strict=True,
        )
        if before.rate_law.to_dict() != after.rate_law.to_dict()
    ]
    metadata = shifted.compiled_mechanism.network.metadata
    assert changed_reactions == [expected_reaction_id]
    assert metadata["derived_family_target_reaction_id"] == expected_reaction_id
    assert (
        metadata["derived_family_target_reaction_role"]
        == "primary_competing_pathway"
    )
    assert (
        metadata["derived_family_transform_id"]
        == "arrhenius_form_and_scale_stress_v1"
    )
    assert shifted.parameters.domain_parameters == base.parameters.domain_parameters


def test_rate_law_family_can_declaratively_target_a_primary_product_pathway() -> None:
    intervention = MechanismFamilyIntervention(
        "rate_law_family",
        0.8,
        rate_law_change=RateLawFamilyChange(
            reaction_role="primary_target_pathway",
        ),
    )
    shifted = DefaultScenarioGenerator().generate(
        get_scenario("flow-reaction-optimization"),
        0,
        (intervention.to_dict(),),
    )
    assert (
        shifted.compiled_mechanism.network.metadata[
            "derived_family_target_reaction_id"
        ]
        == "target_exothermic"
    )


def test_catalytic_activity_order_pivot_stress_changes_only_target_pathway() -> None:
    intervention = MechanismFamilyIntervention(
        "rate_law_family",
        0.8,
        rate_law_change=RateLawFamilyChange(
            reaction_role="primary_target_pathway",
            transform_id="catalytic_activity_order_pivot_stress_v1",
            activity_order_at_full_severity=0.2,
            catalyst_activity_pivot=5.0,
        ),
    )
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-to-crystallization")
    baseline = generator.generate(scenario, 0)
    shifted = generator.generate(scenario, 0, (intervention.to_dict(),))

    changed = [
        (before, after)
        for before, after in zip(
            baseline.compiled_mechanism.network.reactions,
            shifted.compiled_mechanism.network.reactions,
            strict=True,
        )
        if before.rate_law.to_dict() != after.rate_law.to_dict()
    ]
    assert len(changed) == 1
    before, after = changed[0]
    assert before.reaction_id == after.reaction_id == "target_formation"
    assert before.rate_law.equation_id == after.rate_law.equation_id == "catalytic_activity"
    assert before.rate_law.parameters["activity_order"] == pytest.approx(1.0)
    assert after.rate_law.parameters["activity_order"] == pytest.approx(0.36)
    assert after.rate_law.parameters["A"] == pytest.approx(
        before.rate_law.parameters["A"] * 5.0**0.64
    )
    scale_ratio = (
        after.rate_law.parameters["A"] / before.rate_law.parameters["A"]
    )
    order_delta = (
        after.rate_law.parameters["activity_order"]
        - before.rate_law.parameters["activity_order"]
    )
    low_activity_multiplier = scale_ratio * 1.6**order_delta
    pivot_multiplier = scale_ratio * 5.0**order_delta
    high_activity_multiplier = scale_ratio * 11.0**order_delta
    assert 1.0 < low_activity_multiplier < 2.2
    assert pivot_multiplier == pytest.approx(1.0)
    assert 0.5 < high_activity_multiplier < 1.0
    metadata = shifted.compiled_mechanism.network.metadata
    assert metadata["derived_family_target_reaction_role"] == "primary_target_pathway"
    assert (
        metadata["derived_family_transform_id"]
        == "catalytic_activity_order_pivot_stress_v1"
    )
    assert metadata["derived_family_catalyst_activity_pivot"] == pytest.approx(5.0)
    assert shifted.parameters.domain_parameters == baseline.parameters.domain_parameters


def test_explicit_rate_law_change_contract_round_trips() -> None:
    payload = {
        "kind": "mechanism_family",
        "mode": "rate_law_family",
        "severity": 0.8,
        "rate_law_change": {
            "reaction_role": "primary_competing_pathway",
            "transform_id": "arrhenius_form_and_scale_stress_v1",
            "reference_temperature_K": 350.0,
            "reference_rate_multiplier_at_full_severity": 8.0,
            "temperature_exponent_at_full_severity": 0.75,
        },
    }
    assert MechanismFamilyIntervention.from_dict(payload).to_dict() == payload


def test_catalytic_activity_order_pivot_change_contract_round_trips() -> None:
    payload = {
        "kind": "mechanism_family",
        "mode": "rate_law_family",
        "severity": 0.8,
        "rate_law_change": {
            "reaction_role": "primary_target_pathway",
            "transform_id": "catalytic_activity_order_pivot_stress_v1",
            "activity_order_at_full_severity": 0.2,
            "catalyst_activity_pivot": 5.0,
        },
    }
    assert MechanismFamilyIntervention.from_dict(payload).to_dict() == payload


def test_rate_law_transform_rejects_irrelevant_calibration_fields() -> None:
    with pytest.raises(ValueError, match="unknown rate-law change fields"):
        RateLawFamilyChange.from_dict(
            {
                "reaction_role": "primary_target_pathway",
                "transform_id": "catalytic_activity_order_pivot_stress_v1",
                "activity_order_at_full_severity": 0.2,
                "catalyst_activity_pivot": 5.0,
                "reference_temperature_K": 350.0,
            }
        )


def test_reversible_target_topology_change_is_explicit_and_calibrated() -> None:
    intervention = MechanismFamilyIntervention(
        "topology_family",
        0.8,
        topology_change=TopologyFamilyChange(
            reaction_role="primary_target_pathway",
            transform_id="reversible_target_pathway_stress_v1",
            reverse_rate_constant_s_inv_at_full_severity=0.000625,
        ),
    )
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-to-crystallization")
    baseline = generator.generate(scenario, 0)
    shifted = generator.generate(scenario, 0, (intervention.to_dict(),))

    assert len(shifted.compiled_mechanism.network.reactions) == (
        len(baseline.compiled_mechanism.network.reactions) + 1
    )
    added = shifted.compiled_mechanism.network.reactions[-1]
    assert added.reaction_id == "family_reverse_channel"
    assert added.reactants == {"P": 1.0}
    assert added.products == {"A": 1.0}
    assert added.rate_law.parameters["k"] == pytest.approx(0.0005)
    metadata = shifted.compiled_mechanism.network.metadata
    assert metadata["derived_family_target_reaction_id"] == "target_formation"
    assert metadata["derived_family_target_reaction_role"] == "primary_target_pathway"
    assert (
        metadata["derived_family_transform_id"]
        == "reversible_target_pathway_stress_v1"
    )


def test_topology_change_contract_round_trips() -> None:
    payload = {
        "kind": "mechanism_family",
        "mode": "topology_family",
        "severity": 0.8,
        "topology_change": {
            "reaction_role": "primary_target_pathway",
            "transform_id": "reversible_target_pathway_stress_v1",
            "reverse_rate_constant_s_inv_at_full_severity": 0.000625,
        },
    }
    assert MechanismFamilyIntervention.from_dict(payload).to_dict() == payload


def test_rate_law_role_resolution_is_independent_of_reaction_declaration_order() -> None:
    compiled = DefaultScenarioGenerator().generate(
        get_scenario("reaction-to-crystallization"),
        0,
    ).compiled_mechanism
    reordered_network = replace(
        compiled.network,
        reactions=tuple(reversed(compiled.network.reactions)),
    )
    reordered = replace(compiled, network=reordered_network)
    shifted = derive_mechanism_family(
        reordered,
        MechanismFamilyIntervention("rate_law_family", 0.8),
    )
    assert (
        shifted.network.metadata["derived_family_target_reaction_id"]
        == "side_formation"
    )
