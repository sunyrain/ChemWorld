from copy import deepcopy
from types import SimpleNamespace

import gymnasium as gym
import pytest
from scripts.analyze_work_ii_full_process_diagnostic import assay_truth_metrics

import chemworld  # noqa: F401
from chemworld.agent_interface import full_process_operational_state, tool_json_view
from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.interactive_codex_experiment import _bounded_current_packet
from chemworld.foundation import WorldState
from chemworld.foundation.state import PhaseLedger, PhaseRecord, ProcessLedger, SpeciesLedger


def test_purification_assay_includes_impurities_outside_local_partition_family():
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    try:
        env.reset(seed=0)
        amounts = {
            "A": 0.0,
            "P_org": 0.015,
            "P_aq": 0.0,
            "B_org": 0.005,
            "B_aq": 0.0,
            "E": 0.08,
            "D": 0.0,
        }
        env.unwrapped._state = env.unwrapped._state.replace(
            species_amounts=amounts,
            species=SpeciesLedger(initial_amounts_mol={"A": 0.10}),
            process=ProcessLedger(
                metrics={"purity": 0.75, "recovery": 0.50, "pre_separation_product_mol": 0.03}
            ),
            phases=PhaseLedger(
                {
                    "organic": PhaseRecord(
                        phase_id="organic",
                        vessel_id="test",
                        phase_type="organic",
                        volume_L=0.02,
                        species_amounts_mol=amounts,
                        selected=True,
                    )
                }
            ),
        )
        truth = assay_truth_metrics(env.unwrapped, "reaction-to-purification")
        assert truth["purity"] == pytest.approx(0.15)
        assert truth["recovery"] == pytest.approx(0.15)
        assert env.unwrapped._state.process.metrics["purity"] == 0.75
    finally:
        env.close()


def test_paid_reading_is_fresh_then_explicitly_carried_after_quench():
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    try:
        env.reset(seed=0)
        for action in (
            {"operation": "add_solvent", "solvent": 2, "volume_L": 0.028},
            {"operation": "add_reagent", "amount_mol": 0.01},
            {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.00025},
            {
                "operation": "heat",
                "target_temperature_K": 385.0,
                "duration_s": 300.0,
                "stirring_speed_rpm": 720.0,
            },
        ):
            _, _, _, _, info = env.step(action)
            assert info["transaction_status"] == "committed"
        obs, _, _, _, info = env.step({"operation": "measure", "instrument": "hplc"})
        measured = tool_json_view(env, obs, info)["operational_state"]
        assert measured["measurement_context"]["fresh_measurement_this_step"] is True
        assert measured["measurement_context"]["instrument_this_step"] == "hplc"
        assert measured["temperature_K"] == env.unwrapped._state.temperature_K
        assert measured["temperature_K"] != 385.0
        obs, _, _, _, info = env.step({"operation": "quench"})
        carried = tool_json_view(env, obs, info)["operational_state"]
        assert carried["measurement_context"]["status"] == "carried_not_remeasured"
        assert carried["measurement_context"]["instrument_this_step"] is None
        assert carried["quenched"] is True
        assert carried["temperature_K"] < measured["temperature_K"]
        _, reset_info = env.reset(seed=0)
        assert full_process_operational_state(env, reset_info)["measurement_context"]["status"] == (
            "not_measured"
        )
    finally:
        env.close()


@pytest.mark.parametrize(
    "task", ("reaction-to-purification", "reaction-to-crystallization", "reaction-to-distillation")
)
def test_operational_packet_retains_phase_identity_without_latent_composition(task):
    state = WorldState(
        species_amounts={"secret_product": 0.02},
        volume_L=0.02,
        temperature_K=310.0,
        pressure_Pa=101325.0,
        phase="liquid",
        vessel_id="test-vessel",
        phases=PhaseLedger(
            {
                "distillate": PhaseRecord(
                    phase_id="distillate",
                    vessel_id="test-vessel",
                    phase_type="liquid",
                    volume_L=0.02,
                    species_amounts_mol={"secret_product": 0.01},
                    selected=True,
                ),
                "collected_fraction": PhaseRecord(
                    phase_id="collected_fraction",
                    vessel_id="test-vessel",
                    phase_type="liquid",
                    volume_L=0.01,
                    species_amounts_mol={"secret_product": 0.01},
                    selected=False,
                ),
            }
        ),
        process=ProcessLedger(metrics={"secret_rate": 987.0}),
        metadata={"secret_partition": 321.0},
    )
    base = SimpleNamespace(task_id=task, _state=state)
    operational = full_process_operational_state(base, {})
    alternate = deepcopy(base)
    alternate._state = state.replace(
        species_amounts={"another_secret": 300.0},
        process=ProcessLedger(metrics={"secret_rate": -654.0}),
        metadata={"secret_partition": 0.01},
    )
    assert full_process_operational_state(alternate, {}) == operational
    assert "secret" not in str(operational)
    context = AgentDecisionContext(
        step=1,
        task_id=task,
        decision_stage="experiment_control",
        campaign_state={},
        visible_metrics={},
        latest_spectra={},
        uncertainty={},
        constraint_flags={},
        available_operations=("measure",),
        previous_event_type=None,
    )
    packet = _bounded_current_packet(
        context, {"tool_json": {"operational_state": operational}}, artifact=None
    )
    delivered = packet["operational_state"]
    assert delivered["selected_phase"] == "distillate"
    assert delivered["phases"]["collected_fraction"]["selected"] is False
    assert delivered["phases"]["distillate"]["volume_L"] == 0.02
    if task == "reaction-to-crystallization":
        assert "only by final_assay" in delivered["particle_measurement_contract"]
