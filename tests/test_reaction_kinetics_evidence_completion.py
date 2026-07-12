from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import chemworld.physchem.reaction_network as reaction_network_module
from chemworld.physchem.reaction_reference_cases import (
    ThresholdMeasurementStrategy,
    product_inhibition_implicit_time_s,
    product_inhibition_reference_network,
    select_threshold_measurement_strategy,
)

REPORT_PATH = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "world_foundation"
    / "reports"
    / "reaction-kinetics-evidence-completion.json"
)
INITIAL_AMOUNTS = {"A": 1.0}
CANDIDATE_TIMES_S = (5.0, 10.0, 20.0, 40.0, 80.0)


def _strategies() -> tuple[ThresholdMeasurementStrategy, ThresholdMeasurementStrategy]:
    uninhibited = product_inhibition_reference_network(product_inhibition_L_per_mol=0.0)
    inhibited = product_inhibition_reference_network(product_inhibition_L_per_mol=12.0)
    kwargs = {
        "volume_L": 1.0,
        "temperature_K": 350.0,
        "observable_species_id": "P",
        "threshold_mol": 0.6,
        "candidate_times_s": CANDIDATE_TIMES_S,
    }
    return (
        select_threshold_measurement_strategy(uninhibited, INITIAL_AMOUNTS, **kwargs),
        select_threshold_measurement_strategy(inhibited, INITIAL_AMOUNTS, **kwargs),
    )


def test_bounded_product_inhibition_matches_rate_identity_and_implicit_reference() -> None:
    coefficient = 12.0
    network = product_inhibition_reference_network(
        rate_constant_s=0.08,
        product_inhibition_L_per_mol=coefficient,
    )
    derivatives = network.amount_derivatives(
        {"A": 0.8, "P": 0.2},
        volume_L=1.0,
        temperature_K=350.0,
    )
    expected_rate_mol_s = 0.08 * 0.8 / (1.0 + coefficient * 0.2)
    assert derivatives["P"] == pytest.approx(expected_rate_mol_s, rel=1.0e-12)
    assert derivatives["A"] == pytest.approx(-expected_rate_mol_s, rel=1.0e-12)
    uninhibited = product_inhibition_reference_network(
        rate_constant_s=0.08,
        product_inhibition_L_per_mol=0.0,
    )
    assert uninhibited.amount_derivatives(
        {"A": 0.8, "P": 0.2},
        volume_L=1.0,
        temperature_K=350.0,
    )["P"] == pytest.approx(0.08 * 0.8, rel=1.0e-12)

    result = network.integrate_batch(
        INITIAL_AMOUNTS,
        volume_L=1.0,
        temperature_K=350.0,
        duration_s=80.0,
        evaluation_times_s=(0.0, *CANDIDATE_TIMES_S),
    )
    final_product_mol = result.final_amounts_mol["P"]
    reference_time_s = product_inhibition_implicit_time_s(
        product_amount_mol=final_product_mol,
        initial_reactant_mol=1.0,
        volume_L=1.0,
        rate_constant_s=0.08,
        product_inhibition_L_per_mol=coefficient,
    )
    assert reference_time_s == pytest.approx(80.0, abs=5.0e-5)
    assert sum(result.final_amounts_mol.values()) == pytest.approx(1.0, abs=1.0e-10)
    assert result.solver_diagnostic["maximum_conservation_drift_mol"] < 1.0e-10


def test_product_inhibition_reference_rejects_out_of_domain_inputs() -> None:
    with pytest.raises(ValueError, match="finite and nonnegative"):
        product_inhibition_reference_network(product_inhibition_L_per_mol=-1.0)
    with pytest.raises(ValueError, match="must lie"):
        product_inhibition_implicit_time_s(
            product_amount_mol=1.0,
            initial_reactant_mol=1.0,
            volume_L=1.0,
            rate_constant_s=0.08,
            product_inhibition_L_per_mol=12.0,
        )
    network = product_inhibition_reference_network()
    with pytest.raises(ValueError, match="strictly increasing"):
        select_threshold_measurement_strategy(
            network,
            INITIAL_AMOUNTS,
            volume_L=1.0,
            temperature_K=350.0,
            observable_species_id="P",
            threshold_mol=0.6,
            candidate_times_s=(20.0, 10.0),
        )


def test_mechanism_difference_changes_executable_measurement_strategy() -> None:
    initial_snapshot = dict(INITIAL_AMOUNTS)
    uninhibited, inhibited = _strategies()

    assert uninhibited.selected_time_s == 20.0
    assert inhibited.selected_time_s == 80.0
    assert inhibited.predicted_amounts_mol[-1] < uninhibited.predicted_amounts_mol[-1]
    assert uninhibited.candidate_times_s == inhibited.candidate_times_s
    assert initial_snapshot == INITIAL_AMOUNTS


def test_forced_solver_nonconvergence_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    network = product_inhibition_reference_network()
    initial = {"A": 1.0}
    initial_snapshot = dict(initial)

    def forced_failure(*_args: object, **_kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(
            success=False,
            message="forced nonconvergence for fail-closed regression",
        )

    monkeypatch.setattr(reaction_network_module, "solve_ivp", forced_failure)
    with pytest.raises(
        RuntimeError,
        match="Reaction-network integration failed: forced nonconvergence",
    ):
        network.integrate_batch(
            initial,
            volume_L=1.0,
            temperature_K=350.0,
            duration_s=80.0,
        )
    assert initial == initial_snapshot


def test_committed_report_matches_executable_causal_evidence() -> None:
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    uninhibited, inhibited = _strategies()

    assert report["status"] == "evidence_complete"
    assert report["validation"]["targeted_status"] == "passed"
    assert report["validation"]["ruff_status"] == "passed"
    assert report["runtime_compatibility"]["formal_runtime_contract_changed"] is False
    assert all(report["checks"].values())
    recorded = report["measurement_strategy_evidence"]
    assert recorded["candidate_times_s"] == list(CANDIDATE_TIMES_S)
    assert recorded["uninhibited"]["selected_time_s"] == uninhibited.selected_time_s
    assert recorded["inhibited"]["selected_time_s"] == inhibited.selected_time_s
    assert recorded["uninhibited"]["predicted_product_mol"] == pytest.approx(
        uninhibited.predicted_amounts_mol,
        abs=1.0e-10,
    )
    assert recorded["inhibited"]["predicted_product_mol"] == pytest.approx(
        inhibited.predicted_amounts_mol,
        abs=1.0e-10,
    )
    reference = report["product_inhibition_reference"]
    assert reference["final_product_mol"] == pytest.approx(
        inhibited.predicted_amounts_mol[-1],
        abs=1.0e-10,
    )
    assert product_inhibition_implicit_time_s(
        product_amount_mol=reference["final_product_mol"],
        initial_reactant_mol=reference["initial_reactant_mol"],
        volume_L=reference["volume_L"],
        rate_constant_s=reference["rate_constant_s^-1"],
        product_inhibition_L_per_mol=reference["product_inhibition_L_per_mol"],
    ) == pytest.approx(reference["analytical_implicit_time_s"], abs=1.0e-10)
