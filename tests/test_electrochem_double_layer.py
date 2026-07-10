from __future__ import annotations

from math import exp

import pytest

from chemworld.physchem import (
    DoubleLayerRCSpec,
    MaturityLevel,
    electrochemistry_model_cards,
    simulate_double_layer_current_step,
    simulate_double_layer_potential_step,
    validate_model_card,
)


def _spec() -> DoubleLayerRCSpec:
    return DoubleLayerRCSpec(
        model_id="randles_test",
        double_layer_capacitance_F_m2=0.2,
        electrode_area_m2=0.01,
        series_resistance_ohm=10.0,
        charge_transfer_resistance_ohm=90.0,
        provenance_id="synthetic-eis-fit",
    )


def test_rc_spec_time_constants_match_randles_resistances() -> None:
    spec = _spec()
    capacitance = 0.2 * 0.01

    assert spec.total_capacitance_f == pytest.approx(capacitance)
    assert spec.potential_step_time_constant_s == pytest.approx(
        (10.0 * 90.0 / 100.0) * capacitance
    )
    assert spec.current_step_time_constant_s == pytest.approx(90.0 * capacitance)


def test_potential_step_current_decays_from_series_to_steady_randles_current() -> None:
    spec = _spec()
    duration = 10.0 * spec.potential_step_time_constant_s
    result = simulate_double_layer_potential_step(
        spec,
        potential_step_V=1.0,
        duration_s=duration,
        sample_interval_s=duration / 20.0,
    )

    assert result.trace[0].total_current_A == pytest.approx(1.0 / 10.0)
    assert result.trace[0].faradaic_current_A == pytest.approx(0.0)
    assert result.trace[0].capacitive_current_A == pytest.approx(1.0 / 10.0)
    assert result.trace[-1].total_current_A == pytest.approx(1.0 / 100.0, rel=5e-4)
    assert result.final_capacitive_fraction < 0.001
    assert result.startup_capacitive_fraction == pytest.approx(1.0)


def test_potential_step_charge_integrals_close_analytically() -> None:
    spec = _spec()
    tau = spec.potential_step_time_constant_s
    duration = 3.0 * tau
    result = simulate_double_layer_potential_step(
        spec,
        potential_step_V=0.5,
        duration_s=duration,
        sample_interval_s=tau / 5.0,
    )
    decay = exp(-duration / tau)
    expected_capacitive = 0.5 / 10.0 * tau * (1.0 - decay)
    expected_faradaic = 0.5 / 100.0 * (duration - tau * (1.0 - decay))

    assert result.capacitive_charge_C == pytest.approx(expected_capacitive)
    assert result.faradaic_charge_C == pytest.approx(expected_faradaic)
    assert result.total_charge_C == pytest.approx(expected_capacitive + expected_faradaic)
    assert result.charge_balance_residual_C == pytest.approx(0.0, abs=1.0e-15)


def test_current_step_splits_constant_total_into_capacitive_and_faradaic_parts() -> None:
    spec = _spec()
    tau = spec.current_step_time_constant_s
    result = simulate_double_layer_current_step(
        spec,
        current_step_A=0.02,
        duration_s=5.0 * tau,
        sample_interval_s=tau / 5.0,
    )

    assert all(point.total_current_A == pytest.approx(0.02) for point in result.trace)
    assert result.trace[0].capacitive_current_A == pytest.approx(0.02)
    assert result.trace[0].faradaic_current_A == pytest.approx(0.0)
    assert result.trace[-1].faradaic_current_A == pytest.approx(
        0.02 * (1.0 - exp(-5.0))
    )
    assert result.total_charge_C == pytest.approx(0.02 * 5.0 * tau)
    assert result.charge_balance_residual_C == pytest.approx(0.0, abs=1.0e-15)


def test_short_trace_warns_about_startup_artifact_and_observation_has_components() -> None:
    spec = _spec()
    result = simulate_double_layer_current_step(
        spec,
        current_step_A=-0.01,
        duration_s=spec.current_step_time_constant_s,
        sample_interval_s=spec.current_step_time_constant_s / 4.0,
    )
    observation = result.observation()

    assert "trace_ends_before_five_time_constants" in result.warnings
    assert "startup_current_dominated_by_non_faradaic_charging" in result.warnings
    assert len(observation["time_s"]) == len(result.trace)
    assert observation["total_current_A"][0] == pytest.approx(-0.01)
    assert observation["capacitive_current_A"][0] == pytest.approx(-0.01)
    assert observation["faradaic_current_A"][0] == pytest.approx(0.0)


def test_double_layer_contract_rejects_zero_resistance() -> None:
    with pytest.raises(ValueError, match="series_resistance"):
        DoubleLayerRCSpec(
            model_id="bad",
            double_layer_capacitance_F_m2=0.2,
            electrode_area_m2=0.01,
            series_resistance_ohm=0.0,
            charge_transfer_resistance_ohm=10.0,
            provenance_id="bad",
        )


def test_double_layer_model_card_is_professional_candidate() -> None:
    card = {
        item.model_id: item for item in electrochemistry_model_cards()
    }["randles_double_layer_transient_v1"]

    assert card.maturity is MaturityLevel.PROFESSIONAL_CANDIDATE
    assert validate_model_card(card) == []
