from __future__ import annotations

from typing import Any, cast

import gymnasium as gym
import pytest

import chemworld.runtime.distillation_services as distillation_services
from chemworld.foundation import equipment_settings
from chemworld.runtime.species import MechanismSpeciesView


def _runtime(env: gym.Env) -> Any:
    return cast(Any, env.unwrapped)


def _prepare_feed() -> gym.Env:
    env = gym.make("ChemWorld", task_id="reaction-to-distillation", seed=0)
    env.reset(seed=0)
    actions = (
        {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
        {"operation": "add_reagent", "amount_mol": 0.010},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": 0.00025,
            "catalyst": 1,
        },
        {
            "operation": "heat",
            "target_temperature_K": 385.0,
            "duration_s": 1500.0,
            "stirring_speed_rpm": 720.0,
        },
        {"operation": "wait", "duration_s": 900.0},
        {"operation": "evaporate", "target_temperature_K": 335.0, "duration_s": 600.0},
    )
    for action in actions:
        _, _, _, _, info = env.step(action)
        assert info["transaction_status"] == "committed", (action, info)
    return env


def _distill(
    *,
    duration_s: float = 1500.0,
    reflux_ratio: float = 2.0,
    target_temperature_K: float = 360.0,
) -> gym.Env:
    env = _prepare_feed()
    _, _, _, _, info = env.step(
        {
            "operation": "distill",
            "target_temperature_K": target_temperature_K,
            "duration_s": duration_s,
            "reflux_ratio": reflux_ratio,
        }
    )
    assert info["transaction_status"] == "committed", info
    return env


def _target_amount(env: gym.Env, phase_id: str) -> float:
    runtime = _runtime(env)
    state = runtime._state
    view = MechanismSpeciesView(runtime.scenario_instance.compiled_mechanism)
    target_species = view.target_species_for_state(state)
    return sum(
        float(state.phases.phases[phase_id].species_amounts_mol.get(species_id, 0.0))
        for species_id in target_species
    )


def test_formal_distill_operation_executes_integrated_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0
    original = distillation_services.run_duty_limited_distillation

    def tracked(*args: Any, **kwargs: Any) -> Any:
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(
        distillation_services,
        "run_duty_limited_distillation",
        tracked,
    )
    env = _prepare_feed()
    try:
        feed_volume = _runtime(env)._state.volume_L
        _, _, _, _, info = env.step(
            {
                "operation": "distill",
                "target_temperature_K": 360.0,
                "duration_s": 1500.0,
                "reflux_ratio": 2.0,
            }
        )
        state = _runtime(env)._state
        settings = equipment_settings(state.equipment, "distillation_column")
        kernel = settings["distillation_kernel"]

        assert info["transaction_status"] == "committed"
        assert calls == 1
        assert settings["distillation_model"] == (
            "chemworld_duty_limited_distillation_vnext"
        )
        assert settings["distillation_adapter_id"] == (
            "wf-60-duty-limited-distillation"
        )
        assert settings["distillation_provider_path"].endswith(
            "DutyLimitedDistillationProvider"
        )
        assert settings["distillation_provenance"]
        assert kernel["material_balance_error_mol"] < 1.0e-10
        assert kernel["energy_balance_error_J"] < 1.0e-10
        assert kernel["bubble_pressure_margin_Pa"] > 0.0
        assert kernel["total_reboiler_duty_J"] > 0.0
        assert kernel["condenser_duty_J"] > 0.0
        assert state.phases.total_amounts_mol() == pytest.approx(state.species_amounts)
        assert sum(phase.volume_L for phase in state.phases.phases.values()) == (
            pytest.approx(feed_volume)
        )
        assert state.volume_L == pytest.approx(
            state.phases.phases["distillate"].volume_L
        )
        assert _runtime(env).constitution.check_state(state).passed
    finally:
        env.close()


def test_reflux_and_duration_create_recovery_purity_energy_tradeoffs() -> None:
    cases = (
        {"duration_s": 1500.0, "reflux_ratio": 0.0, "target_temperature_K": 360.0},
        {"duration_s": 1500.0, "reflux_ratio": 5.0, "target_temperature_K": 360.0},
        {"duration_s": 3600.0, "reflux_ratio": 2.0, "target_temperature_K": 390.0},
    )
    results: list[dict[str, Any]] = []
    for case in cases:
        env = _distill(**case)
        try:
            settings = equipment_settings(
                _runtime(env)._state.equipment,
                "distillation_column",
            )
            results.append(settings["distillation_kernel"])
        finally:
            env.close()

    no_reflux, high_reflux, long_run = results
    assert high_reflux["light_key_distillate_purity"] > (
        no_reflux["light_key_distillate_purity"]
    )
    assert high_reflux["light_key_recovery"] > no_reflux["light_key_recovery"]
    assert high_reflux["total_reboiler_duty_J"] > no_reflux["total_reboiler_duty_J"]
    assert long_run["actual_distillate_cut_fraction"] > (
        high_reflux["actual_distillate_cut_fraction"]
    )
    assert long_run["total_reboiler_duty_J"] > no_reflux["total_reboiler_duty_J"]


def test_fraction_collection_preserves_bottoms_remainder_and_prior_cuts() -> None:
    env = _distill()
    try:
        state = _runtime(env)._state
        feed_total = state.phases.total_amounts_mol()
        phase_volume = sum(phase.volume_L for phase in state.phases.phases.values())
        initial_target = _target_amount(env, "distillate")

        _, _, _, _, first_info = env.step(
            {"operation": "collect_fraction", "transfer_fraction": 0.60}
        )
        assert first_info["transaction_status"] == "committed"
        assert _target_amount(env, "collected_fraction") == pytest.approx(
            initial_target * 0.60
        )
        assert _target_amount(env, "distillate") == pytest.approx(initial_target * 0.40)

        _, _, _, _, second_info = env.step(
            {"operation": "collect_fraction", "transfer_fraction": 0.50}
        )
        state = _runtime(env)._state
        assert second_info["transaction_status"] == "committed"
        assert _target_amount(env, "collected_fraction") == pytest.approx(
            initial_target * 0.80
        )
        assert _target_amount(env, "distillate") == pytest.approx(initial_target * 0.20)
        assert {"bottoms", "distillate", "collected_fraction"} <= set(
            state.phases.phases
        )
        assert state.phases.phases["collected_fraction"].selected is True
        assert state.phases.total_amounts_mol() == pytest.approx(feed_total)
        assert sum(phase.volume_L for phase in state.phases.phases.values()) == (
            pytest.approx(phase_volume)
        )
    finally:
        env.close()


def test_fraction_collection_before_distillation_fails_without_material_mutation() -> None:
    env = _prepare_feed()
    try:
        before = _runtime(env)._state
        _, _, _, _, info = env.step(
            {"operation": "collect_fraction", "transfer_fraction": 0.80}
        )
        after = _runtime(env)._state
        assert info["constraint_flags"]["precondition_failed"] is True
        assert info["transaction_status"] in {"validation_failed", "rolled_back"}
        assert after.species_amounts == before.species_amounts
        assert after.phases == before.phases
        assert after.equipment == before.equipment
        assert after.volume_L == before.volume_L
    finally:
        env.close()

