from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.foundation import equipment_settings
from chemworld.physchem.crystallization_adapter_manifest import (
    RUNTIME_MODEL_ID,
    ValidatedCrystallizationRuntimeProvider,
    crystallization_runtime_adapter_manifest,
)
from chemworld.physchem.crystallization_units import (
    CrystallizationExecutionSpec,
    CrystallizationKineticsSpec,
    SolubilityCurveSpec,
)
from chemworld.physchem.crystallization_validation import CrystallizationGridCase
from chemworld.runtime.kernel_contracts import ModelProviderResult

REACTION_STEPS = (
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
    {"operation": "wait", "duration_s": 900.0, "stirring_speed_rpm": 720.0},
)


class RecordingProvider(ValidatedCrystallizationRuntimeProvider):
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def evaluate(self, inputs: Any) -> ModelProviderResult:
        self.calls.append(dict(inputs))
        return super().evaluate(inputs)


def test_formal_runtime_dynamically_calls_validated_population_balance_provider() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        base: Any = env.unwrapped
        for action in REACTION_STEPS:
            env.step(action)
        env.step({"operation": "seed_crystals", "seed_mass_g": 0.006})
        provider = RecordingProvider()
        base.runtime.domain_services.crystallization.runtime_provider = provider

        _obs, _reward, _terminated, _truncated, info = env.step(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 278.15,
                "duration_s": 1800.0,
            }
        )

        assert info["transaction_status"] == "committed"
        assert len(provider.calls) == 1
        assert isinstance(provider.calls[0]["case"], CrystallizationGridCase)
        assert isinstance(provider.calls[0]["execution_spec"], CrystallizationExecutionSpec)
        assert provider.calls[0]["execution_spec"].fail_on_no_transfer is False
        assert provider.calls[0]["execution_spec"].fail_on_no_population is False
        assert provider.calls[0]["execution_spec"].fail_on_solver_nonconvergence is True
        execution = base.runtime.domain_services.crystallization.last_provider_execution
        assert execution["success"] is True
        assert execution["model_id"] == RUNTIME_MODEL_ID
        assert execution["diagnostics"]["runtime_validated"] is True

        state = base._state
        settings = equipment_settings(state.equipment, "crystallizer")
        manifest = crystallization_runtime_adapter_manifest()
        assert settings["crystallization_model_id"] == RUNTIME_MODEL_ID
        assert settings["provider_path"] == manifest.provider_contract.provider_path
        assert settings["provider_manifest_hash"] == manifest.manifest_hash
        assert settings["provider_diagnostics"]["runtime_validated"] is True
        assert settings["growth_solver_converged"] is True
        assert settings["material_balance_error_mol"] <= 1.0e-10
        assert settings["particle_target_balance_error_mol"] <= 1.0e-10
        assert all(error <= 1.0e-10 for error in settings["component_balance_errors_mol"].values())
        assert settings["csd_number_moment_0"] == pytest.approx(
            settings["csd_total_particle_count"]
        )
        assert settings["csd_volume_moment_3_m3"] > 0.0
        assert len(settings["temperature_history_K"]) == provider.calls[0]["time_steps"] + 1
        assert settings["temperature_history_K"][0] > settings["temperature_history_K"][-1]
        assert len(settings["supersaturation_history"]) == provider.calls[0]["time_steps"]
        assert len(settings["nucleation_history_per_L_s"]) == provider.calls[0]["time_steps"]
        assert len(settings["growth_history_m_s"]) == provider.calls[0]["time_steps"]
        assert len(settings["execution_history"]) == 1
        assert state.phases.total_amounts_mol() == pytest.approx(state.species_amounts)
    finally:
        env.close()


def test_cooling_seed_and_time_perturbations_change_yield_purity_size_tradeoff() -> None:
    mild = _runtime_outcome(seed_mass_g=0.006, target_temperature_K=305.0, duration_s=1200.0)
    deep = _runtime_outcome(
        seed_mass_g=0.006,
        target_temperature_K=278.15,
        duration_s=1800.0,
    )
    long = _runtime_outcome(
        seed_mass_g=0.006,
        target_temperature_K=278.15,
        duration_s=3600.0,
    )
    low_seed = _runtime_outcome(
        seed_mass_g=0.002,
        target_temperature_K=278.15,
        duration_s=1800.0,
    )
    high_seed = _runtime_outcome(
        seed_mass_g=0.012,
        target_temperature_K=278.15,
        duration_s=1800.0,
    )

    assert deep["yield"] > mild["yield"] + 0.30
    assert long["time_s"] > deep["time_s"]
    assert long["yield"] > deep["yield"]
    assert long["purity"] > deep["purity"]
    assert long["d50_m"] > deep["d50_m"]
    assert long["fines_fraction"] < deep["fines_fraction"]
    assert high_seed["purity"] > low_seed["purity"] + 5.0e-4
    assert high_seed["maximum_supersaturation"] < low_seed["maximum_supersaturation"]


def test_filter_consumes_validated_solid_and_closes_retention_ledger() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        for action in REACTION_STEPS:
            env.step(action)
        env.step({"operation": "seed_crystals", "seed_mass_g": 0.006})
        env.step(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 278.15,
                "duration_s": 1800.0,
            }
        )
        before = env.unwrapped._state
        species_view = env.unwrapped.runtime.domain_services.crystallization.species_view
        target = species_view.primary_target_species
        impurity = species_view.primary_impurity_species
        solid_before = before.phases.phases["solid"].species_amounts_mol

        _obs, _reward, _terminated, _truncated, info = env.step({"operation": "filter_crystals"})

        assert info["transaction_status"] == "committed"
        state = env.unwrapped._state
        settings = equipment_settings(state.equipment, "crystal_filter")
        solid_after = state.phases.phases["solid"].species_amounts_mol
        assert solid_after[target] == pytest.approx(solid_before[target] * 0.96)
        assert solid_after[impurity] == pytest.approx(solid_before[impurity] * 0.92)
        assert settings["target_returned_to_filtrate_mol"] == pytest.approx(
            solid_before[target] * 0.04
        )
        assert settings["impurity_returned_to_filtrate_mol"] == pytest.approx(
            solid_before[impurity] * 0.08
        )
        assert settings["component_balance_error_mol"] <= 1.0e-12
        assert state.phases.total_amounts_mol() == pytest.approx(state.species_amounts)
    finally:
        env.close()


@pytest.mark.parametrize(
    "seed_mass_g,target_temperature_K,duration_s,expected_reason,provider_called",
    [
        (0.006, 278.15, 60.0, "maximum_cooling_rate", False),
        (1.0e-6, 278.15, 1800.0, "minimum_effective_seed_particles", True),
    ],
)
def test_invalid_cooling_proposals_roll_back_without_crystal_state(
    seed_mass_g: float,
    target_temperature_K: float,
    duration_s: float,
    expected_reason: str,
    provider_called: bool,
) -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        for action in REACTION_STEPS:
            env.step(action)
        env.step({"operation": "seed_crystals", "seed_mass_g": seed_mass_g})
        base: Any = env.unwrapped
        before = base._state

        _obs, _reward, _terminated, _truncated, info = env.step(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": target_temperature_K,
                "duration_s": duration_s,
            }
        )

        assert info["transaction_status"] == "validation_failed"
        assert info["measurement_cost"] == 0.0
        assert base._state.temperature_K == pytest.approx(before.temperature_K)
        assert base._state.species_amounts == pytest.approx(before.species_amounts)
        assert base._state.phases.to_dict() == before.phases.to_dict()
        execution = base.runtime.domain_services.crystallization.last_provider_execution
        if provider_called:
            assert execution["success"] is False
            assert expected_reason in execution["failure_reason"]
        else:
            assert execution == {}
            invalid_reasons = info["world_events"][0]["payload"]["invalid_reasons"]
            assert "payload_coupling:maximum_cooling_rate_K_s" in invalid_reasons
        assert (
            equipment_settings(base._state.equipment, "crystallizer").get(
                "crystallization_model_id"
            )
            is None
        )
    finally:
        env.close()


def test_exhausted_target_rolls_back_and_does_not_fabricate_crystals() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        env.step({"operation": "add_solvent", "volume_L": 0.028, "solvent": 2})
        env.step({"operation": "add_reagent", "amount_mol": 0.010})
        base: Any = env.unwrapped
        before = base._state
        _obs, _reward, _terminated, _truncated, info = env.step(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 278.15,
                "duration_s": 1800.0,
            }
        )
        assert info["transaction_status"] == "rolled_back"
        assert base._state.species_amounts == pytest.approx(before.species_amounts)
        assert base._state.phases.to_dict() == before.phases.to_dict()
        assert base.runtime.domain_services.crystallization.last_provider_execution == {}
        assert "cool_crystallize_requires_reaction_or_seed" in info[
            "world_events"
        ][0]["payload"]["failed_preconditions"]
    finally:
        env.close()


def test_isothermal_negative_crystallization_is_a_committed_observation() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        for action in REACTION_STEPS:
            env.step(action)
        base: Any = env.unwrapped
        base._state = base._state.replace(temperature_K=320.0)
        initial_temperature = base._state.temperature_K

        _obs, _reward, _terminated, _truncated, info = env.step(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": initial_temperature,
                "duration_s": 1200.0,
            }
        )

        assert info["transaction_status"] == "committed"
        execution = base.runtime.domain_services.crystallization.last_provider_execution
        assert execution["success"] is True
        assert execution["diagnostics"]["crystal_population_formed"] is False
        assert execution["diagnostics"]["meaningful_transfer"] is False
        assert base._state.process.metrics["crystal_yield"] == pytest.approx(0.0)
    finally:
        env.close()


def test_provider_fails_closed_for_no_population_no_transfer_and_nonconvergence() -> None:
    provider = ValidatedCrystallizationRuntimeProvider()
    policy = CrystallizationExecutionSpec.strict_runtime()

    no_population = provider.evaluate(
        {
            "case": _case(seed_mass_g=0.0, nucleation_coefficient=0.0),
            "time_steps": 60,
            "execution_spec": policy,
        }
    )
    no_transfer_case = _case(seed_mass_g=0.006)
    no_transfer = provider.evaluate(
        {
            "case": replace(
                no_transfer_case,
                final_temperature_K=320.0,
                solubility_curve=replace(
                    no_transfer_case.solubility_curve,
                    reference_solubility_mol_L=0.40,
                ),
            ),
            "time_steps": 60,
            "execution_spec": policy,
        }
    )
    nonconverged = provider.evaluate(
        {
            "case": _case(
                seed_mass_g=0.006,
                nucleation_coefficient=0.0,
                growth_coefficient=1.0e-4,
            ),
            "time_steps": 24,
            "execution_spec": replace(policy, max_growth_solver_iterations=1),
        }
    )

    assert no_population.success is False
    assert "no crystal population" in (no_population.failure_reason or "")
    assert no_transfer.success is False
    assert "no meaningful crystallization transfer" in (no_transfer.failure_reason or "")
    assert nonconverged.success is False
    assert "solver did not converge" in (nonconverged.failure_reason or "")
    assert not no_population.outputs and not no_transfer.outputs and not nonconverged.outputs


def test_runtime_manifest_and_machine_report_are_truthful() -> None:
    manifest = crystallization_runtime_adapter_manifest()
    assert manifest.status == "integrated"
    assert manifest.provider_contract.role.value == "runtime"
    assert manifest.provider_contract.model_id == RUNTIME_MODEL_ID
    assert manifest.provider_contract.maturity.value == "professional_candidate"

    report = json.loads(
        Path("workstreams/world_foundation/reports/crystallization-coupling.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["task_complete"] is True
    assert report["runtime_coupling"]["dynamic_provider_called"] is True
    assert report["runtime_coupling"]["hidden_public_fields"] == 0
    assert report["maturity_truth"]["effective_maturity"] == "professional_candidate"
    assert report["maturity_truth"]["limitations"]


def _runtime_outcome(
    *,
    seed_mass_g: float,
    target_temperature_K: float,
    duration_s: float,
) -> dict[str, float]:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        for action in REACTION_STEPS:
            env.step(action)
        env.step({"operation": "seed_crystals", "seed_mass_g": seed_mass_g})
        _obs, _reward, _terminated, _truncated, info = env.step(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": target_temperature_K,
                "duration_s": duration_s,
            }
        )
        assert info["transaction_status"] == "committed"
        state = env.unwrapped._state
        settings = equipment_settings(state.equipment, "crystallizer")
        return {
            "yield": state.process.metrics["crystal_yield"],
            "purity": state.process.metrics["crystal_purity"],
            "d50_m": settings["csd_d50_m"],
            "fines_fraction": settings["csd_fines_number_fraction"],
            "maximum_supersaturation": settings["maximum_supersaturation_ratio"],
            "time_s": state.ledger.time_s,
        }
    finally:
        env.close()


def _case(
    *,
    seed_mass_g: float,
    nucleation_coefficient: float = 2.0e7,
    growth_coefficient: float = 2.0e-8,
) -> CrystallizationGridCase:
    return CrystallizationGridCase(
        feed_amounts_mol={"P": 0.030, "B": 0.003},
        target_component="P",
        impurity_component="B",
        solvent_volume_L=0.10,
        initial_temperature_K=320.0,
        final_temperature_K=280.0,
        duration_s=1800.0,
        solubility_curve=SolubilityCurveSpec(
            model_id="test_solubility",
            reference_solubility_mol_L=0.20,
            reference_temperature_K=320.0,
            dissolution_enthalpy_J_mol=18_000.0,
            minimum_temperature_K=260.0,
            maximum_temperature_K=340.0,
            provenance_id="test_solubility_reference",
        ),
        kinetics=CrystallizationKineticsSpec(
            model_id="test_kinetics",
            primary_nucleation_coefficient_per_L_s=nucleation_coefficient,
            primary_nucleation_exponent=2.0,
            growth_coefficient_m_s=growth_coefficient,
            growth_exponent=1.0,
            crystal_density_kg_m3=1200.0,
            target_molecular_weight_kg_mol=0.10,
            nucleus_diameter_m=8.0e-6,
            impurity_occlusion_mol_per_mol=0.02,
            supersaturation_occlusion_factor=0.5,
            fines_threshold_m=20.0e-6,
            provenance_id="test_kinetics_reference",
        ),
        seed_mass_g=seed_mass_g,
        seed_diameter_m=100.0e-6,
    )
