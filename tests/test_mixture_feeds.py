from __future__ import annotations

from itertools import combinations

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.action_codec import ActionCodec
from chemworld.agent_interface import action_schema
from chemworld.campaign_resources import CampaignResourceCard, CampaignResourceLedger
from chemworld.data.logging import TrajectoryLogger, load_jsonl
from chemworld.eval.verify import verify_records
from chemworld.foundation import equipment_settings
from chemworld.foundation.solvents import HEAT_CAPACITY_RATIOS, SolventInventory
from chemworld.runtime.solvent_transport import total_solvents
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.mixtures import working_solvents


def make_env(task="reaction-to-assay", seed=0, **kwargs):
    env = gym.make(
        "ChemWorld",
        task_id=task,
        seed=seed,
        budget_override=80,
        episode_mode_override="single_experiment",
        **kwargs,
    )
    env.reset(seed=seed)
    return env


def step(env, action):
    result = env.step(action)
    info = result[-1]
    assert info["transaction_status"] == "committed", (
        action,
        info.get("invalid_reasons"),
        info.get("rollback_reason"),
        [key for key, passed in info.get("preconditions", {}).items() if not passed],
    )
    state = env.unwrapped._state
    account = state.solvent_accounting
    assert tuple(
        a + b - c
        for a, b, c in zip(
            account.initial.volumes_L,
            account.added.volumes_L,
            account.removed.volumes_L,
            strict=True,
        )
    ) == pytest.approx(total_solvents(state).volumes_L, abs=1e-10)
    return result


COMPOSITIONS = [c for n in range(1, 5) for c in combinations(range(4), n)]


@pytest.mark.parametrize("components", COMPOSITIONS)
def test_compositions_and_equivalent_order(components):
    states = []
    for order in (components, tuple(reversed(components))):
        with make_env() as env:
            for i in order:
                step(
                    env, {"operation": "add_solvent", "solvent": i, "volume_L": 0.025 / len(order)}
                )
            step(env, {"operation": "add_reagent", "amount_mol": 0.012})
            step(env, {"operation": "add_catalyst", "catalyst": 0, "catalyst_amount_mol": 0.0002})
            step(
                env,
                {
                    "operation": "heat",
                    "target_temperature_K": 350.0,
                    "duration_s": 600.0,
                    "stirring_speed_rpm": 600.0,
                },
            )
            states.append(env.unwrapped._state)
    left, right = states
    assert working_solvents(left).volumes_L == pytest.approx(
        working_solvents(right).volumes_L, abs=1e-12
    )
    assert left.species_amounts == pytest.approx(right.species_amounts, abs=1e-12)
    assert left.temperature_K == pytest.approx(right.temperature_K, abs=1e-8)


def test_mixture_properties_are_compositional():
    blend = SolventInventory((0.01, 0.01, 0, 0))
    assert blend.log_property((1, 4, 9, 16)) == pytest.approx(2)
    assert blend.linear_property(HEAT_CAPACITY_RATIOS) == pytest.approx(0.73)
    distillate, bottoms = blend.split(0.01, (1, 2, 1.8, 0.7))
    assert distillate.volumes_L[1] > distillate.volumes_L[0]
    assert (distillate + bottoms).volumes_L == pytest.approx(blend.volumes_L, abs=1e-14)
    assert distillate.volume_L == pytest.approx(0.01, abs=1e-14)


@pytest.mark.parametrize("amounts", [(0.012, 0), (0, 0.012), (0.012, 0.012), (0.012, 0.024)])
def test_independent_cofeed_stoichiometry(amounts, tmp_path):
    with make_env("reaction-to-distillation") as env:
        task = {**env.unwrapped.task_info(), **env.unwrapped.evaluator_provenance()}
        path = tmp_path / "cofeeds.jsonl"
        actions = [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}]
        actions += [
            {"operation": "add_component", "component": f"feed-{i}", "amount_mol": amount}
            for i, amount in enumerate(amounts)
            if amount
        ]
        with TrajectoryLogger(path) as logger:
            for index, action in enumerate(actions, 1):
                obs, reward, term, trunc, info = step(env, action)
                logger.log(
                    task_info=task,
                    step=index,
                    action=action,
                    observation=obs,
                    reward=reward,
                    terminated=term,
                    truncated=trunc,
                    info=info,
                    agent_metadata={},
                )
        assert verify_records(load_jsonl(path), tolerance=0).verified
        view = MechanismSpeciesView(env.unwrapped.scenario_instance.compiled_mechanism)
        before = env.unwrapped._state
        assert view.initial_reactant_amount(before) == pytest.approx(min(amounts))
        assert view.reactant_amount(before) == pytest.approx(min(amounts))
        step(
            env,
            {
                "operation": "heat",
                "target_temperature_K": 350.0,
                "duration_s": 600.0,
                "stirring_speed_rpm": 600.0,
            },
        )
        after = env.unwrapped._state
        if min(amounts) == 0:
            assert view.target_amount(after) == pytest.approx(0, abs=1e-12)
        else:
            assert view.target_amount(after) > 0
        assert view.initial_reactant_amount(after) == pytest.approx(min(amounts))


def test_component_codec_schema_invalid_is_atomic():
    codec = ActionCodec()
    action = {"operation": "add_component", "component": "feed-1", "amount_mol": 0.01}
    decoded = codec.decode_vector(codec.encode_vector(action))
    assert decoded["component"] == 1
    with make_env("reaction-to-distillation") as env:
        schema = action_schema(env, "add_component")
        assert next(f for f in schema["fields"] if f["field"] == "component")["choices"] == [0, 1]
        before = env.unwrapped._state
        _, _, _, _, info = env.step({**action, "component": 2})
        assert info["transaction_status"] != "committed"
        assert env.unwrapped._state.species_amounts == before.species_amounts
        assert env.unwrapped.task_info()["mixture_model"]["catalog_size"] == 4


def test_recipe_records_all_actual_feed_charges():
    with make_env("reaction-to-distillation") as env:
        step(env, {"operation": "add_reagent", "amount_mol": 0.01})
        view = MechanismSpeciesView(env.unwrapped.scenario_instance.compiled_mechanism)
        state = env.unwrapped._state
        for species in view.feed_species:
            assert state.species.initial_amounts_mol[species] == state.species_amounts[species]


def test_split_merge_mixed_carriers():
    with make_env() as env:
        for i in (0, 1):
            step(env, {"operation": "add_solvent", "solvent": i, "volume_L": 0.0125})
        step(env, {"operation": "add_reagent", "amount_mol": 0.01})
        step(env, {"operation": "quench"})
        before = total_solvents(env.unwrapped._state)
        step(env, {"operation": "create_container", "container": 1, "capacity_L": 0.05})
        for source, target, fraction, mixing in ((0, 1, 0.4, 0), (1, 0, 1.0, 1)):
            step(
                env,
                {
                    "operation": "transfer_material",
                    "source_container": source,
                    "destination_container": target,
                    "transfer_fraction": fraction,
                    "mixing": mixing,
                },
            )
        assert total_solvents(env.unwrapped._state).volumes_L == pytest.approx(before.volumes_L)


def test_electrochemical_properties_refresh_after_medium_change():
    with make_env(
        "electrochemical-conversion", electrochemical_workflow_mode="autonomous_open_v1"
    ) as env:
        step(env, {"operation": "add_solvent", "solvent": 0, "volume_L": 0.015})
        step(env, {"operation": "add_reagent", "amount_mol": 0.01})
        step(
            env,
            {
                "operation": "set_potential",
                "potential_V": 1.2,
                "current_mA": 30.0,
                "electrolyte_profile": 1,
            },
        )
        old = equipment_settings(env.unwrapped._state.equipment, "electrochemical_cell")
        step(env, {"operation": "add_solvent", "solvent": 1, "volume_L": 0.015})
        step(env, {"operation": "electrolyze", "duration_s": 60.0})
        new = equipment_settings(env.unwrapped._state.equipment, "electrochemical_cell")
        assert new["electrolyte_conductivity_S_m"] != old["electrolyte_conductivity_S_m"]
        assert new["electrolyte_acid_total_mol"] == old["electrolyte_acid_total_mol"]
        assert len(new["setpoint_history"]) == len(old["setpoint_history"])


def test_campaign_actual_multifeed_stock_and_snapshot():
    card = CampaignResourceCard(
        card_id="mixed-feed",
        operation_attempt_limit=10,
        vessel_start_limit=2,
        final_assay_limit=2,
        nonfinal_instrument_use_limit=2,
        stock_limits={"reagent_mol": 0.03},
    )
    with make_env("reaction-to-distillation", campaign_resource_card=card) as env:
        step(env, {"operation": "add_reagent", "amount_mol": 0.01})
        ledger = env.unwrapped._campaign_resource_ledger
        assert ledger.stocks_used["reagent_mol"] == pytest.approx(0.0225)
        recovered = CampaignResourceLedger.from_snapshot(ledger.snapshot())
        assert recovered.snapshot() == ledger.snapshot()
        step(env, {"operation": "add_component", "component": 0, "amount_mol": 0.005})
        assert ledger.stocks_used["reagent_mol"] == pytest.approx(0.0275)
        _, _, _, _, info = env.step({"operation": "add_reagent", "amount_mol": 0.002})
        assert info["transaction_status"] != "committed"


@pytest.mark.parametrize(
    "task,downstream",
    [
        (
            "reaction-to-distillation",
            [
                {
                    "operation": "distill",
                    "target_temperature_K": 350.0,
                    "duration_s": 1200.0,
                    "reflux_ratio": 1.5,
                },
                {"operation": "collect_fraction", "transfer_fraction": 0.7},
            ],
        ),
        (
            "reaction-to-purification",
            [
                {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.005},
                {"operation": "add_extractant", "extractant": 3, "volume_L": 0.015},
                {"operation": "add_extractant", "extractant": 2, "volume_L": 0.005},
                {"operation": "mix", "duration_s": 180.0, "stirring_speed_rpm": 600.0},
                {"operation": "settle", "duration_s": 300.0},
                {"operation": "separate_phase", "target_phase": "organic"},
                {"operation": "wash", "wash_volume_L": 0.005},
                {"operation": "dry"},
                {"operation": "concentrate", "duration_s": 300.0},
            ],
        ),
    ],
)
def test_downstream_mixed_carrier_conservation(task, downstream):
    with make_env(task) as env:
        for i in (0, 1):
            step(env, {"operation": "add_solvent", "solvent": i, "volume_L": 0.0125})
        step(env, {"operation": "add_reagent", "amount_mol": 0.012})
        step(
            env,
            {
                "operation": "heat",
                "target_temperature_K": 350.0,
                "duration_s": 600.0,
                "stirring_speed_rpm": 600.0,
            },
        )
        step(env, {"operation": "quench"})
        for action in downstream:
            step(env, action)
        state = env.unwrapped._state
        if task == "reaction-to-distillation":
            carrier = state.phases.phases["distillate"].solvents
            assert carrier.volumes_L[1] > carrier.volumes_L[0]
            kernel = equipment_settings(state.equipment, "distillation_column")[
                "distillation_kernel"
            ]
            assert kernel["energy_balance_error_J"] <= 1e-8
            assert set(kernel["feed_amounts_mol"]) >= {"carrier-0", "carrier-1"}


def test_equivalent_split_dosing_and_evaporation():
    states = []
    for repetitions in (1, 2):
        with make_env("reaction-to-distillation") as env:
            for _ in range(repetitions):
                for i in (0, 1):
                    step(
                        env,
                        {
                            "operation": "add_solvent",
                            "solvent": i,
                            "volume_L": 0.0125 / repetitions,
                        },
                    )
                step(env, {"operation": "add_reagent", "amount_mol": 0.012 / repetitions})
            states.append(env.unwrapped._state)
            before = env.unwrapped._state
            step(
                env, {"operation": "evaporate", "target_temperature_K": 330.0, "duration_s": 600.0}
            )
            after = env.unwrapped._state
            assert after.species_amounts == before.species_amounts
            assert working_solvents(after).fractions[1] < 0.5
            energy = after.metadata["last_evaporation_energy"]
            assert energy["jacket_J"] == pytest.approx(energy["sensible_J"] + energy["latent_J"])
            assert energy["jacket_J"] <= 45 * 600
    assert states[0].species_amounts == pytest.approx(states[1].species_amounts, abs=1e-12)
    assert states[0].temperature_K == pytest.approx(states[1].temperature_K, abs=1e-8)
    assert working_solvents(states[0]).volumes_L == pytest.approx(
        working_solvents(states[1]).volumes_L, abs=1e-12
    )


def test_resuspension_archives_old_liquor_composition():
    from test_recrystallization_cycles import cycle_actions

    with make_env(
        "reaction-to-crystallization", full_process_contract_id="phase-resolved-process-v5"
    ) as env:
        for i in (0, 1):
            step(env, {"operation": "add_solvent", "solvent": i, "volume_L": 0.0125})
        for action in cycle_actions()[2:9]:
            step(env, action)
        before = total_solvents(env.unwrapped._state)
        step(env, {"operation": "resuspend_crystals", "solvent": 3, "volume_L": 0.001})
        state = env.unwrapped._state
        filtrate = state.samples.samples["filtrate-0001"]
        liquor = next(iter(filtrate.contents.phases.phases.values()))
        assert liquor.solvents.fractions == pytest.approx((0.5, 0.5, 0, 0))
        expected = before + SolventInventory.pure(3, 0.001)
        assert total_solvents(state).volumes_L == pytest.approx(expected.volumes_L, abs=1e-12)


def test_flow_medium_changes_hydraulics_and_preserves_carriers():
    results = []
    for components in ((0,), (0, 1)):
        with make_env("flow-reaction-optimization") as env:
            for i in components:
                step(
                    env,
                    {"operation": "add_solvent", "solvent": i, "volume_L": 0.025 / len(components)},
                )
            step(env, {"operation": "add_reagent", "amount_mol": 0.012})
            step(
                env,
                {"operation": "set_flow_rate", "flow_rate_mL_min": 1.0, "residence_time_s": 600.0},
            )
            before = total_solvents(env.unwrapped._state)
            schema = action_schema(env, "run_flow")
            duration = next(f for f in schema["fields"] if f["field"] == "duration_s")["bounds"][
                "low"
            ]
            step(
                env,
                {
                    "operation": "run_flow",
                    "target_temperature_K": 350.0,
                    "duration_s": duration + 1.0,
                },
            )
            state = env.unwrapped._state
            assert total_solvents(state).volumes_L == pytest.approx(before.volumes_L, abs=1e-12)
            results.append(equipment_settings(state.equipment, "flow_reactor"))
    assert results[0]["pressure_drop_Pa"] != results[1]["pressure_drop_Pa"]
    assert results[0]["outlet_temperature_K"] != results[1]["outlet_temperature_K"]
