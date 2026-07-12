from __future__ import annotations

import pytest

from chemworld.physchem import (
    MaturityLevel,
    RunawayStateInput,
    SafetyEnvelopeSpec,
    arrhenius_heat_generation_slope,
    assess_safety_envelope,
    safety_envelope_model_cards,
    validate_model_card,
)


def _envelope() -> SafetyEnvelopeSpec:
    return SafetyEnvelopeSpec(
        envelope_id="test_reactor_envelope",
        temperature_warning_K=380.0,
        maximum_allowable_temperature_K=420.0,
        pressure_warning_Pa=400_000.0,
        relief_set_pressure_Pa=500_000.0,
        maximum_allowable_pressure_Pa=600_000.0,
        relief_capacity_kg_s=0.10,
        risk_cost_weight=2.0,
        relief_activation_cost=3.0,
        emergency_shutdown_cost=10.0,
        provenance_id="synthetic-reactor-safety-card",
    )


def _runaway(**overrides: float) -> RunawayStateInput:
    values = {
        "heat_generation_W": 500.0,
        "heat_removal_W": 700.0,
        "heat_removal_slope_W_K": 50.0,
        "activation_energy_J_mol": 40_000.0,
        "process_heat_capacity_J_K": 20_000.0,
        "remaining_exotherm_J": 100_000.0,
        "pressure_rate_Pa_s": 0.0,
        "vapor_generation_kg_s": 0.01,
        **overrides,
    }
    return RunawayStateInput(**values)


def test_arrhenius_heat_generation_slope_matches_analytical_derivative() -> None:
    slope = arrhenius_heat_generation_slope(
        heat_generation_W=1000.0,
        activation_energy_J_mol=50_000.0,
        temperature_K=350.0,
    )

    assert slope == pytest.approx(1000.0 * 50_000.0 / (8.31446261815324 * 350.0**2))


def test_normal_state_has_margins_no_projected_limit_and_low_cost() -> None:
    result = assess_safety_envelope(
        _envelope(),
        temperature_K=330.0,
        pressure_Pa=200_000.0,
        runaway=_runaway(),
    )

    assert result.status == "normal"
    assert result.flags == ()
    assert result.predicted_temperature_rate_K_s < 0.0
    assert result.time_to_temperature_limit_s is None
    assert result.time_to_relief_set_s is None
    assert result.runaway_stability_margin_W_K > 0.0
    assert result.risk_score == pytest.approx(0.0)
    assert result.incremental_safety_cost == pytest.approx(0.0)


def test_runaway_indicators_project_limit_and_raise_safety_cost() -> None:
    result = assess_safety_envelope(
        _envelope(),
        temperature_K=390.0,
        pressure_Pa=450_000.0,
        runaway=_runaway(
            heat_generation_W=5000.0,
            heat_removal_W=1000.0,
            heat_removal_slope_W_K=5.0,
            remaining_exotherm_J=800_000.0,
            pressure_rate_Pa_s=1000.0,
            vapor_generation_kg_s=0.08,
        ),
    )

    assert result.status == "warning"
    assert result.predicted_temperature_rate_K_s == pytest.approx(0.2)
    assert result.time_to_temperature_limit_s == pytest.approx(150.0)
    assert result.time_to_relief_set_s == pytest.approx(50.0)
    assert result.maximum_temperature_of_synthesis_reaction_K == pytest.approx(430.0)
    assert "mtsr_exceeds_maximum_temperature" in result.flags
    assert "thermal_runaway_slope_unstable" in result.flags
    assert "net_heat_accumulation" in result.flags
    assert result.risk_score > 0.5
    assert result.incremental_safety_cost > 1.0


def test_relief_and_mawp_breach_trigger_emergency_and_capacity_costs() -> None:
    result = assess_safety_envelope(
        _envelope(),
        temperature_K=410.0,
        pressure_Pa=620_000.0,
        runaway=_runaway(
            heat_generation_W=6000.0,
            heat_removal_W=500.0,
            heat_removal_slope_W_K=4.0,
            remaining_exotherm_J=1_000_000.0,
            pressure_rate_Pa_s=2000.0,
            vapor_generation_kg_s=0.15,
        ),
    )

    assert result.status == "emergency_shutdown"
    assert result.time_to_relief_set_s == pytest.approx(0.0)
    assert result.relief_load_ratio == pytest.approx(1.5)
    assert "relief_set_pressure_reached" in result.flags
    assert "maximum_allowable_pressure_exceeded" in result.flags
    assert "relief_capacity_insufficient" in result.flags
    assert result.incremental_safety_cost == pytest.approx(
        2.0 * result.risk_score + 3.0 + 10.0
    )
    assert result.constraint_flags() == {
        "unsafe": True,
        "relief_required": False,
        "emergency_shutdown": True,
        "safety_risk": result.risk_score,
        "incremental_safety_cost": result.incremental_safety_cost,
    }


def test_envelope_validation_rejects_misordered_limits() -> None:
    with pytest.raises(ValueError, match="pressure limits"):
        SafetyEnvelopeSpec(
            envelope_id="bad",
            temperature_warning_K=380.0,
            maximum_allowable_temperature_K=420.0,
            pressure_warning_Pa=500_000.0,
            relief_set_pressure_Pa=400_000.0,
            maximum_allowable_pressure_Pa=600_000.0,
            relief_capacity_kg_s=0.1,
            risk_cost_weight=1.0,
            relief_activation_cost=1.0,
            emergency_shutdown_cost=1.0,
            provenance_id="bad-limits",
        )


def test_safety_envelope_model_card_is_reference_validated() -> None:
    card = safety_envelope_model_cards()[0]

    assert card.model_id == "pressure_temperature_runaway_safety_envelope_v1"
    assert card.maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(card) == []
