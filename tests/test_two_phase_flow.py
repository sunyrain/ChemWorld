from __future__ import annotations

import pytest

from chemworld.physchem import (
    MaturityLevel,
    lockhart_martinelli_pressure_drop,
    transport_model_cards,
    validate_model_card,
)


def test_lockhart_martinelli_matches_published_fluids_example() -> None:
    result = lockhart_martinelli_pressure_drop(
        mass_flow_kg_s=0.6,
        vapor_quality=0.1,
        liquid_density_kg_m3=915.0,
        vapor_density_kg_m3=2.67,
        liquid_viscosity_Pa_s=180.0e-6,
        vapor_viscosity_Pa_s=14.0e-6,
        diameter_m=0.05,
        length_m=1.0,
    )

    assert result.pressure_drop_Pa == pytest.approx(716.4695654888483, rel=1.0e-12)
    assert result.chisholm_parameter == pytest.approx(20.0)
    assert result.liquid_regime == "turbulent"
    assert result.vapor_regime == "turbulent"
    assert result.pressure_drop_Pa == pytest.approx(
        result.liquid_only_pressure_drop_Pa * result.liquid_multiplier_squared
    )


def test_lockhart_martinelli_selects_regime_specific_chisholm_parameter() -> None:
    result = lockhart_martinelli_pressure_drop(
        mass_flow_kg_s=0.001,
        vapor_quality=0.5,
        liquid_density_kg_m3=900.0,
        vapor_density_kg_m3=3.0,
        liquid_viscosity_Pa_s=0.02,
        vapor_viscosity_Pa_s=1.0e-5,
        diameter_m=0.02,
    )

    assert result.liquid_regime == "laminar"
    assert result.vapor_regime == "turbulent"
    assert result.chisholm_parameter == pytest.approx(12.0)
    assert result.martinelli_parameter > 0.0


def test_lockhart_martinelli_is_linear_in_pipe_length() -> None:
    inputs = {
        "mass_flow_kg_s": 0.2,
        "vapor_quality": 0.25,
        "liquid_density_kg_m3": 950.0,
        "vapor_density_kg_m3": 5.0,
        "liquid_viscosity_Pa_s": 0.001,
        "vapor_viscosity_Pa_s": 1.5e-5,
        "diameter_m": 0.04,
    }
    one = lockhart_martinelli_pressure_drop(length_m=1.0, **inputs)
    four = lockhart_martinelli_pressure_drop(length_m=4.0, **inputs)

    assert four.pressure_drop_Pa == pytest.approx(4.0 * one.pressure_drop_Pa)
    assert four.liquid_multiplier_squared == pytest.approx(
        one.liquid_multiplier_squared
    )


def test_lockhart_martinelli_reports_endpoint_and_microchannel_warnings() -> None:
    result = lockhart_martinelli_pressure_drop(
        mass_flow_kg_s=0.01,
        vapor_quality=0.99,
        liquid_density_kg_m3=900.0,
        vapor_density_kg_m3=4.0,
        liquid_viscosity_Pa_s=0.001,
        vapor_viscosity_Pa_s=1.0e-5,
        diameter_m=0.002,
    )

    assert "quality_near_single_phase_endpoint" in result.warnings
    assert "microchannel_surface_tension_effects_not_modeled" in result.warnings


def test_lockhart_martinelli_rejects_endpoints_and_inclined_flow() -> None:
    base = {
        "mass_flow_kg_s": 0.1,
        "liquid_density_kg_m3": 900.0,
        "vapor_density_kg_m3": 4.0,
        "liquid_viscosity_Pa_s": 0.001,
        "vapor_viscosity_Pa_s": 1.0e-5,
        "diameter_m": 0.02,
    }
    with pytest.raises(ValueError, match="inside"):
        lockhart_martinelli_pressure_drop(vapor_quality=0.0, **base)
    with pytest.raises(ValueError, match="horizontal"):
        lockhart_martinelli_pressure_drop(
            vapor_quality=0.2,
            inclination_degrees=5.0,
            **base,
        )


def test_two_phase_pressure_drop_model_card_is_reference_validated() -> None:
    card = {
        item.model_id: item for item in transport_model_cards()
    }["lockhart_martinelli_chisholm_horizontal_v1"]

    assert card.maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(card) == []
