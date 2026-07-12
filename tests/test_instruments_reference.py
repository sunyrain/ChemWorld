from __future__ import annotations

import copy
import json
from math import sqrt
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np
import pytest
from apps.task_lab.spectral_payload import spectral_payload
from apps.task_lab.student_session import StudentSessionManager

import chemworld  # noqa: F401
from chemworld.physchem.chromatography_methods import (
    EmpiricalChromatographyAnalyteSpec,
    evaluate_chromatography_method,
)
from chemworld.physchem.spectroscopy import (
    charge_balance_residual,
    potentiometric_ph,
)
from chemworld.world.instruments import instrument_contracts
from chemworld.world.observation_kernel import ObservationModuleSpec, raw_signal

PUBLIC_INSTRUMENTS = {"uvvis", "ph_meter", "gc", "hplc", "final_assay"}
FORBIDDEN_PUBLIC_KEYS = {
    "debug",
    "hidden_parameters",
    "model_id",
    "model_ids",
    "private_seed",
    "provider",
    "provider_parameters",
    "provider_path",
    "world_provider",
}


def test_every_public_instrument_declares_complete_synthetic_contract() -> None:
    contracts = instrument_contracts()

    assert set(contracts) == PUBLIC_INSTRUMENTS
    for contract in contracts.values():
        payload = contract.to_dict()
        assert payload["input_state_schema"]["physical_state"] == "virtual_liquid_sample"
        assert payload["axis_contract"]["unit"]
        assert payload["calibration_contract"]["status"] == "synthetic_reference_calibration"
        assert set(payload["detection_contract"]) == {
            "lod_mol_L",
            "loq_mol_L",
            "below_lod",
        }
        assert payload["noise_model"]
        assert payload["baseline_drift_contract"]["baseline"]
        assert payload["missingness_contract"]["failed_measurement"]
        assert payload["cost"] > 0.0
        assert payload["sample_consumption_L"] > 0.0
        assert "does not predict real samples" in payload["synthetic_boundary"]


@pytest.mark.parametrize("instrument_id", ["hplc", "gc", "uvvis"])
def test_public_signal_is_layered_seeded_and_identity_safe(instrument_id: str) -> None:
    values = {
        "yield": 0.62,
        "conversion": 0.75,
        "byproduct_signal": 0.11,
        "degradation_warning": 0.03,
        "purity": 0.80,
        "distillate_purity": 0.78,
    }
    first = raw_signal(instrument_id, values, seed=41, replicate_count=3)
    replay = raw_signal(instrument_id, values, seed=41, replicate_count=3)

    assert first == replay
    assert {
        "sample_state",
        "axis",
        "raw_signal",
        "peaks",
        "assignments",
        "processed_estimates",
        "uncertainty",
        "calibration",
        "missingness",
        "metadata",
    } <= set(first)
    assert first["metadata"]["synthetic"] is True
    assert first["metadata"]["real_sample_prediction"] is False
    assert all(key.startswith("analyte_") for key in first["calibration"])
    assert not (_nested_keys(first) & FORBIDDEN_PUBLIC_KEYS)


def test_public_signals_distinguish_concentration_and_composition_without_truth() -> None:
    low = raw_signal(
        "uvvis",
        {},
        species_amounts_mol={
            "reactant_public": 0.70,
            "target_public": 0.10,
            "impurity_public": 0.02,
        },
        volume_L=1.0,
        seed=17,
        replicate_count=4,
    )
    high = raw_signal(
        "uvvis",
        {},
        species_amounts_mol={
            "reactant_public": 0.25,
            "target_public": 0.50,
            "impurity_public": 0.12,
        },
        volume_L=1.0,
        seed=17,
        replicate_count=4,
    )
    low_signal = np.asarray(low["absorbance"], dtype=float)
    high_signal = np.asarray(high["absorbance"], dtype=float)
    between_rmse = sqrt(float(np.mean((high_signal - low_signal) ** 2)))

    assert between_rmse > 0.01
    assert low["assignments"] != high["assignments"] or low["peaks"] != high["peaks"]
    assert "hidden_species" not in json.dumps(low, sort_keys=True)
    assert "hidden_species" not in json.dumps(high, sort_keys=True)

    for instrument_id in ("hplc", "gc"):
        dilute = raw_signal(
            instrument_id,
            {},
            species_amounts_mol={"target_public": 0.04, "impurity_public": 0.02},
            volume_L=1.0,
            seed=19,
            replicate_count=3,
        )
        concentrated = raw_signal(
            instrument_id,
            {},
            species_amounts_mol={"target_public": 0.40, "impurity_public": 0.02},
            volume_L=1.0,
            seed=19,
            replicate_count=3,
        )
        assert concentrated["peaks"][0]["area"] > dilute["peaks"][0]["area"]


def test_final_assay_channels_remain_public_and_synthetic() -> None:
    packet = raw_signal(
        "final_assay",
        {"yield": 0.6, "conversion": 0.8, "pH_normalized": 0.5},
        species_amounts_mol={"reactant_public": 0.2, "target_public": 0.6},
        volume_L=1.0,
        seed=12,
        replicate_count=3,
    )
    public_species = {
        "reactant_public",
        "target_public",
        "impurity_public",
        "degradation_public",
    }

    assert packet["metadata"]["synthetic"] is True
    assert not (_nested_keys(packet) & FORBIDDEN_PUBLIC_KEYS)
    assert _nested_values(packet, "species_id") <= public_species


def test_below_lod_becomes_explicit_missing_value_without_removing_raw_trace() -> None:
    packet = raw_signal(
        "hplc",
        {},
        species_amounts_mol={"target_public": 1.0e-7},
        volume_L=1.0,
        seed=9,
        replicate_count=2,
    )

    assert packet["time_min"] and packet["intensity"]
    assert packet["missingness"]["entries"]
    assert all(value is None for value in packet["processed_estimates"].values())
    assert packet["peaks"][0]["detected"] is False

    saturated = raw_signal(
        "hplc",
        {},
        species_amounts_mol={"target_public": 9.0},
        volume_L=1.0,
        seed=9,
        replicate_count=2,
    )
    assert saturated["peaks"][0]["saturated"] is True
    assert saturated["missingness"]["entries"][0]["reason"] == "above_linear_range"


def test_reference_closures_cover_uvvis_chromatography_and_ph() -> None:
    assert potentiometric_ph(hydrogen_activity_mol_L=1.0e-5) == pytest.approx(5.0)
    assert charge_balance_residual(
        {"cation_public": 0.10, "anion_public": 0.10},
        {"cation_public": 1, "anion_public": -1},
    ) == pytest.approx(0.0, abs=1.0e-12)

    analyte = EmpiricalChromatographyAnalyteSpec(
        analyte_id="public_analyte",
        instrument_id="hplc",
        reference_retention_factor=3.0,
        reference_temperature_K=298.15,
        reference_mobile_phase_fraction=0.50,
        hplc_log10_k_mobile_phase_slope=2.0,
        theoretical_plates=6400.0,
        provenance_id="bounded_synthetic_reference",
    )
    report = evaluate_chromatography_method(
        analyte,
        dead_time_min=0.50,
        temperature_K=298.15,
        detector_concentration=0.20,
        mobile_phase_fraction=0.50,
    )
    assert report.retention_time_min == pytest.approx(2.0)
    assert report.baseline_peak_width_min == pytest.approx(0.10)
    assert report.theoretical_plates == pytest.approx(6400.0)
    stronger_mobile_phase = evaluate_chromatography_method(
        analyte,
        dead_time_min=0.50,
        temperature_K=298.15,
        detector_concentration=0.20,
        mobile_phase_fraction=0.70,
    )
    assert stronger_mobile_phase.retention_time_min != pytest.approx(
        report.retention_time_min
    )

    ph_packet = raw_signal(
        "ph_meter",
        {"pH_normalized": 5.0 / 14.0, "equilibrium_residual": 0.0},
        seed=3,
        replicate_count=3,
    )
    assert ph_packet["pH"] == pytest.approx(5.0)
    assert ph_packet["calibration"]["slope_mV_per_pH"] == pytest.approx(-59.16)
    assert ph_packet["metadata"]["real_sample_prediction"] is False


def test_measurement_failure_cost_sample_and_history_are_auditable() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        base: Any = env.unwrapped
        cost_before = float(base._state.ledger.cost)
        volume_before = float(base._state.volume_L)
        _observation, _reward, _terminated, _truncated, failed = env.step(
            {"operation": "measure", "instrument": "final_assay"}
        )
        assert failed["transaction_status"] == "rolled_back"
        assert failed["measurement_cost"] == 0.0
        assert failed["sample_consumed"] == 0.0
        assert failed["raw_signal"] == {}
        failure_cost = float(failed["state_delta_summary"]["delta_cost"])
        assert failure_cost > 0.0
        assert base._state.ledger.cost - cost_before == pytest.approx(failure_cost)
        assert base._state.volume_L == pytest.approx(volume_before)

        env.step({"operation": "add_solvent", "volume_L": 0.028, "solvent": 2})
        cost_before_measurement = float(base._state.ledger.cost)
        volume_before_measurement = float(base._state.volume_L)
        _observation, _reward, _terminated, _truncated, measured = env.step(
            {"operation": "measure", "instrument": "hplc"}
        )
        contract = instrument_contracts()["hplc"]
        assert measured["transaction_status"] == "committed"
        assert measured["measurement_cost"] == pytest.approx(contract.cost)
        assert measured["sample_consumed"] == pytest.approx(contract.sample_consumption_L)
        assert base._state.ledger.cost - cost_before_measurement == pytest.approx(contract.cost)
        assert volume_before_measurement - base._state.volume_L == pytest.approx(
            contract.sample_consumption_L
        )
    finally:
        env.close()


def test_history_is_retained_on_demand_and_masking_does_not_mutate_packet() -> None:
    manager = StudentSessionManager()
    try:
        session = manager.create("reaction-to-assay", seed=0)
        for action in (
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {
                "operation": "add_catalyst",
                "catalyst_amount_mol": 0.00025,
                "catalyst": 1,
            },
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "measure", "instrument": "uvvis"},
        ):
            response = session.step(action)
            assert response["accepted"] is True
        history = session.state()["history"]
        spectra = [record["spectrum"] for record in history if record["spectrum"]["available"]]
        assert len(spectra) == 2
        assert len({packet["spectrum_id"] for packet in spectra}) == 2

        raw_packet = raw_signal("hplc", {"yield": 0.4}, seed=5, replicate_count=2)
        original = copy.deepcopy(raw_packet)
        masked = spectral_payload(raw_packet, instrument="hplc", disclosure="raw")
        assert masked["available"] is True
        assert masked["series"][0]["peaks"] == []
        assert raw_packet == original
    finally:
        manager.close_all()

    module = ObservationModuleSpec().to_dict()
    assert module["history_access"] == "on_demand_by_public_spectrum_id"
    assert module["masking_policy"].startswith("mask_spectral_evidence_only")


def test_instruments_reference_report_is_truthful_and_machine_readable() -> None:
    report = json.loads(
        Path("workstreams/world_foundation/reports/instruments-reference.json").read_text(
            encoding="utf-8"
        )
    )

    assert report["task_complete"] is True
    assert report["maturity_truth"]["bounded_contract_verified"] is True
    assert report["verification"]["public_boundary_gate"]["identity_finding_count"] == 0
    assert report["maturity_truth"]["unresolved_adjacent_claim"] == {
        "model_id": "empirical_chromatography_method_sensitivity_v1",
        "declared_maturity": "professional_candidate",
        "effective_evidence_maturity": "reference_validated",
        "reason": (
            "The strict gate requires a bound provider with runtime diagnostics and "
            "provenance. The legacy test suite currently requires the professional-"
            "candidate label, so this task does not falsify the gate result or silently "
            "change that external contract."
        ),
    }


def _nested_keys(payload: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(payload, dict):
        for key, value in payload.items():
            keys.add(str(key).lower())
            keys.update(_nested_keys(value))
    elif isinstance(payload, list | tuple):
        for value in payload:
            keys.update(_nested_keys(value))
    return keys


def _nested_values(payload: Any, target_key: str) -> set[str]:
    values: set[str] = set()
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key == target_key:
                values.add(str(value))
            values.update(_nested_values(value, target_key))
    elif isinstance(payload, list | tuple):
        for value in payload:
            values.update(_nested_values(value, target_key))
    return values
