from __future__ import annotations

import numpy as np
import pytest

from chemworld.agents.task_recipes import (
    electrochemical_recipe_parameters_from_unit_vector,
    electrochemical_recipe_unit_vector_from_parameters,
    task_recipe_from_unit_vector,
)
from chemworld.foundation import equipment_settings
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_TASK_CONTRACT,
)
from chemworld.physchem.mechanism_library import get_mechanism_card
from chemworld.physchem.reaction_network import RateLawSpec, ReactionSpec, evaluate_rate_law
from chemworld.runtime.mechanisms import compile_mechanism_for_scenario
from chemworld.tasks import get_task


def test_electrochemical_contract_aligns_card_mechanism_and_runtime_roles() -> None:
    contract = ELECTROCHEMICAL_TASK_CONTRACT
    compiled = compile_mechanism_for_scenario(contract.task_id)
    card = get_mechanism_card(contract.mechanism_id)

    contract.validate_compiled_mechanism(compiled)
    assert set(compiled.species_index) == {"Ox", "Red", "SideRed"}
    assert tuple(reaction.reaction_id for reaction in compiled.network.reactions) == (
        contract.desired_pathway_id,
        contract.side_pathway_id,
    )
    assert compiled.manifest.rate_law_equation_ids == ("runtime_owned",)
    assert card.scenario_id == contract.task_id
    assert card.recommended_tasks == (contract.task_id,)
    assert card.operating_window["potential_V"] == {
        "min": contract.s0_potential_bounds_V[0],
        "max": contract.s0_potential_bounds_V[1],
    }
    assert card.operating_window["current_mA"] == {
        "min": contract.s0_current_magnitude_bounds_mA[0],
        "max": contract.s0_current_magnitude_bounds_mA[1],
    }
    assert not compiled.observable_mapping["degradation"]


def test_runtime_owned_rate_law_fails_closed_in_generic_network() -> None:
    with pytest.raises(ValueError, match="require runtime_model_id"):
        RateLawSpec("missing-runtime", "runtime_owned", {})
    reaction = ReactionSpec.from_equation(
        reaction_id="runtime-pathway",
        equation="A => B",
        rate_law=RateLawSpec(
            "runtime-rate",
            "runtime_owned",
            {"runtime_model_id": "specialized-runtime"},
        ),
    )
    with pytest.raises(ValueError, match="cannot be evaluated by the generic reaction network"):
        evaluate_rate_law(
            reaction,
            concentrations_mol_L={"A": 1.0, "B": 0.0},
            temperature_K=298.15,
        )


def test_named_electrochemical_parameters_round_trip_through_internal_vector() -> None:
    parameters = {
        "electrolyte_profile": 2,
        "solvent": 1,
        "reagent_amount_mol": 0.012,
        "probe_potential_V": 0.85,
        "probe_current_mA": 50.0,
        "probe_duration_s": 480.0,
        "controlled_potential_V": 1.15,
        "controlled_current_mA": 72.0,
        "controlled_duration_s": 1800.0,
    }
    vector = electrochemical_recipe_unit_vector_from_parameters(parameters)
    decoded = electrochemical_recipe_parameters_from_unit_vector(vector)
    recipe = task_recipe_from_unit_vector(
        get_task("electrochemical-conversion").to_dict(), vector
    )

    assert np.all((vector >= 0.0) & (vector <= 1.0))
    assert decoded == pytest.approx(parameters)
    assert recipe["steps"][2]["potential_V"] == pytest.approx(0.85)
    assert recipe["steps"][6]["potential_V"] == pytest.approx(1.15)


def test_electrochemical_runtime_records_contract_and_keeps_reverse_side_pool_closed() -> None:
    import gymnasium as gym

    env = gym.make("ChemWorld", task_id="electrochemical-conversion", seed=0)
    try:
        env.reset(seed=0)
        env.step({"operation": "add_solvent", "volume_L": 0.025, "solvent": 0})
        env.step({"operation": "add_reagent", "amount_mol": 0.010})
        env.step(
            {
                "operation": "set_potential",
                "potential_V": 0.80,
                "current_mA": 80.0,
                "electrolyte_profile": 1,
            }
        )
        env.step({"operation": "electrolyze", "duration_s": 900.0})
        forward_state = env.unwrapped._state
        side_after_forward = forward_state.species_amounts["SideRed"]
        assert forward_state.species_amounts["Red"] > 0.0

        env.step(
            {
                "operation": "set_potential",
                "potential_V": 2.0,
                "current_mA": 40.0,
                "electrolyte_profile": 1,
            }
        )
        env.step({"operation": "electrolyze", "duration_s": 120.0})
        reverse_state = env.unwrapped._state
        settings = equipment_settings(reverse_state.equipment, "electrochemical_cell")

        assert reverse_state.process is not None
        assert reverse_state.process.metrics["reaction_direction"] == -1.0
        assert reverse_state.species_amounts["SideRed"] == pytest.approx(side_after_forward)
        assert settings["task_contract"]["task_contract_version"] == (
            ELECTROCHEMICAL_TASK_CONTRACT.contract_version
        )
        assert settings["current_setpoint_semantics"] == (
            "nonnegative_magnitude_cap_signed_current_from_butler_volmer"
        )
    finally:
        env.close()
