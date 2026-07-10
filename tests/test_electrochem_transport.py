from __future__ import annotations

from math import exp

import pytest

from chemworld.physchem import (
    DiffusionLayerSpec,
    MaturityLevel,
    diffusion_layer_current_response,
    electrochemistry_model_cards,
    validate_model_card,
)


def _spec() -> DiffusionLayerSpec:
    return DiffusionLayerSpec(
        model_id="planar_diffusion_layer",
        electrons_transferred=1.0,
        electrode_area_m2=0.01,
        diffusivity_m2_s=1.0e-9,
        diffusion_layer_thickness_m=100.0e-6,
        electrolyte_volume_m3=1.0e-4,
        provenance_id="synthetic-planar-electrode-case",
    )


def test_limiting_current_matches_planar_diffusion_layer_formula() -> None:
    spec = _spec()
    limiting = spec.limiting_current_a(100.0)

    assert limiting == pytest.approx(
        96485.33212 * 0.01 * 1.0e-9 * 100.0 / (100.0e-6)
    )


def test_high_applied_current_has_analytical_plateau_and_exponential_depletion() -> None:
    spec = _spec()
    concentration = 100.0
    duration = 200.0
    result = diffusion_layer_current_response(
        spec,
        bulk_concentration_mol_m3=concentration,
        applied_current_A=10.0,
        duration_s=duration,
    )
    expected_final = concentration * exp(
        -spec.mass_transfer_rate_m3_s * duration / spec.electrolyte_volume_m3
    )

    assert result.mass_transfer_limited_initially
    assert result.transition_to_limiting_time_s == pytest.approx(0.0)
    assert result.initial_useful_current_A == pytest.approx(
        result.initial_limiting_current_A
    )
    assert result.final_bulk_concentration_mol_m3 == pytest.approx(expected_final)
    assert result.final_surface_concentration_mol_m3 == pytest.approx(0.0)
    assert result.current_efficiency < 1.0
    assert result.side_reaction_charge_C > 0.0


def test_sub_limiting_current_gives_linear_depletion_before_transition() -> None:
    spec = _spec()
    limiting = spec.limiting_current_a(100.0)
    applied = 0.25 * limiting
    duration = 10.0
    result = diffusion_layer_current_response(
        spec,
        bulk_concentration_mol_m3=100.0,
        applied_current_A=applied,
        duration_s=duration,
    )
    concentration_rate = applied / (
        96485.33212 * spec.electrolyte_volume_m3
    )

    assert not result.mass_transfer_limited_initially
    assert result.transition_to_limiting_time_s is None
    assert result.final_bulk_concentration_mol_m3 == pytest.approx(
        100.0 - concentration_rate * duration
    )
    assert result.current_efficiency == pytest.approx(1.0)
    assert result.side_reaction_charge_C == pytest.approx(0.0)
    assert result.final_surface_concentration_mol_m3 > 0.0


def test_response_transitions_from_constant_current_to_limiting_current() -> None:
    spec = _spec()
    initial_limiting = spec.limiting_current_a(100.0)
    result = diffusion_layer_current_response(
        spec,
        bulk_concentration_mol_m3=100.0,
        applied_current_A=0.8 * initial_limiting,
        duration_s=1000.0,
    )

    assert not result.mass_transfer_limited_initially
    assert result.transition_to_limiting_time_s is not None
    assert 0.0 < result.transition_to_limiting_time_s < result.duration_s
    assert "transitioned_to_mass_transfer_limit" in result.warnings
    assert result.final_limiting_current_A < abs(result.applied_current_A)


def test_kinetic_cap_also_reduces_current_efficiency_against_applied_charge() -> None:
    result = diffusion_layer_current_response(
        _spec(),
        bulk_concentration_mol_m3=1000.0,
        applied_current_A=-0.5,
        kinetic_current_A=-0.1,
        duration_s=20.0,
    )

    assert result.initial_useful_current_A < 0.0
    assert result.average_useful_current_A < 0.0
    assert result.current_efficiency == pytest.approx(0.2)
    assert result.side_reaction_charge_C == pytest.approx(8.0)


def test_diffusion_layer_contract_rejects_nonphysical_geometry() -> None:
    with pytest.raises(ValueError, match="diffusivity"):
        DiffusionLayerSpec(
            model_id="bad",
            electrons_transferred=1.0,
            electrode_area_m2=0.01,
            diffusivity_m2_s=0.0,
            diffusion_layer_thickness_m=1.0e-4,
            electrolyte_volume_m3=1.0e-4,
            provenance_id="bad",
        )


def test_diffusion_layer_model_card_is_professional_candidate() -> None:
    card = {
        item.model_id: item for item in electrochemistry_model_cards()
    }["diffusion_layer_limiting_current_v1"]

    assert card.maturity is MaturityLevel.PROFESSIONAL_CANDIDATE
    assert validate_model_card(card) == []
