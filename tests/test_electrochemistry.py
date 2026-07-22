from __future__ import annotations

import math

import pytest

from chemworld.physchem.electrochemistry import (
    FARADAY_C_PER_MOL,
    ElectrodeReactionSpec,
    ElectrolyteResistanceSpec,
    butler_volmer_current,
    electrochemistry_model_cards,
    electrolyte_resistance_ohm,
    faradaic_extent_mol,
    nernst_potential,
    ohmic_drop,
    run_electrolysis,
)
from chemworld.physchem.maturity import validate_model_card


def _spec() -> ElectrodeReactionSpec:
    return ElectrodeReactionSpec(
        reaction_id="A_to_P",
        electrons_transferred=2.0,
        standard_potential_V=1.10,
        reaction_quotient_exponents={"P": 1.0, "A": -1.0},
        exchange_current_density_A_m2=20.0,
        electrode_area_m2=0.01,
    )


def test_nernst_potential_moves_with_reaction_quotient() -> None:
    spec = _spec()
    reactant_rich = nernst_potential(spec, {"A": 1.0, "P": 0.1})
    product_rich = nernst_potential(spec, {"A": 0.1, "P": 1.0})
    assert reactant_rich > spec.standard_potential_V
    assert product_rich < spec.standard_potential_V
    assert reactant_rich > product_rich


def test_butler_volmer_current_is_zero_at_equilibrium_and_changes_sign() -> None:
    spec = _spec()
    activities = {"A": 1.0, "P": 1.0}
    equilibrium = nernst_potential(spec, activities)
    assert butler_volmer_current(
        spec,
        electrode_potential_V=equilibrium,
        activities=activities,
    ) == pytest.approx(0.0, abs=1.0e-12)
    assert (
        butler_volmer_current(
            spec,
            electrode_potential_V=equilibrium + 0.05,
            activities=activities,
        )
        > 0.0
    )
    assert (
        butler_volmer_current(
            spec,
            electrode_potential_V=equilibrium - 0.05,
            activities=activities,
        )
        < 0.0
    )


def test_faradaic_extent_uses_charge_electron_number_and_efficiency() -> None:
    extent = faradaic_extent_mol(
        current_A=0.2,
        duration_s=100.0,
        electrons_transferred=2.0,
        faradaic_efficiency=0.8,
    )
    assert extent == pytest.approx(0.2 * 100.0 * 0.8 / (2.0 * FARADAY_C_PER_MOL))


def test_electrolyte_resistance_uses_geometry_and_contact_resistance() -> None:
    spec = ElectrolyteResistanceSpec(
        electrolyte_conductivity_S_m=5.0,
        electrode_gap_m=0.002,
        electrode_area_m2=0.010,
        contact_resistance_ohm=0.20,
    )

    assert spec.electrolyte_resistance_ohm == pytest.approx(0.002 / (5.0 * 0.010))
    assert electrolyte_resistance_ohm(spec) == pytest.approx(0.24)


def test_electrolyte_resistance_rejects_invalid_geometry() -> None:
    with pytest.raises(ValueError, match="electrolyte_conductivity_S_m"):
        ElectrolyteResistanceSpec(
            electrolyte_conductivity_S_m=0.0,
            electrode_gap_m=0.002,
            electrode_area_m2=0.010,
        )
    with pytest.raises(ValueError, match="electrode_gap_m"):
        ElectrolyteResistanceSpec(
            electrolyte_conductivity_S_m=5.0,
            electrode_gap_m=-0.002,
            electrode_area_m2=0.010,
        )
    with pytest.raises(ValueError, match="electrode_area_m2"):
        ElectrolyteResistanceSpec(
            electrolyte_conductivity_S_m=5.0,
            electrode_gap_m=0.002,
            electrode_area_m2=0.0,
        )


def test_ohmic_drop_splits_measured_and_interfacial_potential() -> None:
    resistance = ElectrolyteResistanceSpec(
        electrolyte_conductivity_S_m=4.0,
        electrode_gap_m=0.004,
        electrode_area_m2=0.010,
        contact_resistance_ohm=0.10,
        voltage_window_V=1.5,
    )

    result = ohmic_drop(
        measured_potential_V=1.20,
        current_A=0.25,
        duration_s=100.0,
        resistance=resistance,
    )

    assert result.total_resistance_ohm == pytest.approx(0.20)
    assert result.uncompensated_voltage_drop_V == pytest.approx(0.05)
    assert result.interfacial_potential_V == pytest.approx(1.15)
    assert result.ohmic_loss_J == pytest.approx(0.25 * 0.25 * 0.20 * 100.0)
    assert not result.voltage_window_exceeded


def test_run_electrolysis_limits_substrate_and_reports_energy_accounting() -> None:
    spec = _spec()
    result = run_electrolysis(
        spec,
        electrode_potential_V=1.3,
        duration_s=1200.0,
        activities={"A": 1.0, "P": 0.2},
        available_substrate_mol=1.0e-4,
        applied_current_A=0.2,
    )
    assert result.converted_mol <= 1.0e-4
    assert result.product_mol + result.byproduct_mol == pytest.approx(result.converted_mol)
    assert result.charge_C == pytest.approx(abs(result.actual_current_A) * 1200.0)
    assert 0.0 <= result.faradaic_efficiency <= 1.0
    assert 0.0 <= result.product_selectivity <= 1.0
    assert 0.0 <= result.energy_efficiency <= 1.0
    assert math.isfinite(result.overpotential_V)
    assert result.reaction_direction == 1
    assert result.converted_mol > 0.0
    assert result.measured_potential_V == pytest.approx(1.3)
    assert result.interfacial_potential_V == pytest.approx(1.3)
    assert result.ohmic_loss_J == pytest.approx(0.0)


def test_run_electrolysis_uses_current_sign_and_directional_inventory() -> None:
    spec = _spec()
    activities = {"A": 1.0, "P": 1.0}
    forward = run_electrolysis(
        spec,
        electrode_potential_V=1.2,
        duration_s=100.0,
        activities=activities,
        available_substrate_mol=1.0e-3,
        available_reverse_substrate_mol=0.0,
        applied_current_A=0.05,
    )
    reverse = run_electrolysis(
        spec,
        electrode_potential_V=1.0,
        duration_s=100.0,
        activities=activities,
        available_substrate_mol=1.0e-3,
        available_reverse_substrate_mol=2.0e-4,
        applied_current_A=0.05,
    )
    reverse_without_product = run_electrolysis(
        spec,
        electrode_potential_V=1.0,
        duration_s=100.0,
        activities=activities,
        available_substrate_mol=1.0e-3,
        available_reverse_substrate_mol=0.0,
        applied_current_A=0.05,
    )

    assert forward.reaction_direction == 1
    assert forward.converted_mol > 0.0
    assert reverse.reaction_direction == -1
    assert 0.0 < reverse.converted_mol <= 2.0e-4
    assert reverse_without_product.reaction_direction == -1
    assert reverse_without_product.converted_mol == 0.0


def test_run_electrolysis_reports_ohmic_energy_loss() -> None:
    spec = _spec()
    resistance = ElectrolyteResistanceSpec(
        electrolyte_conductivity_S_m=4.0,
        electrode_gap_m=0.002,
        electrode_area_m2=0.010,
        contact_resistance_ohm=0.05,
    )
    result = run_electrolysis(
        spec,
        electrode_potential_V=1.30,
        duration_s=600.0,
        activities={"A": 1.0, "P": 0.1},
        available_substrate_mol=1.0,
        applied_current_A=0.10,
        electrolyte_resistance=resistance,
    )

    assert result.total_resistance_ohm == pytest.approx(0.10)
    assert result.uncompensated_voltage_drop_V == pytest.approx(
        result.actual_current_A * result.total_resistance_ohm
    )
    assert result.interfacial_potential_V == pytest.approx(
        result.measured_potential_V - result.uncompensated_voltage_drop_V
    )
    assert result.ohmic_loss_J == pytest.approx(
        result.actual_current_A
        * result.actual_current_A
        * result.total_resistance_ohm
        * 600.0
    )
    assert result.electrical_work_J >= result.ohmic_loss_J


def test_ohmic_drop_reports_voltage_window_exceeded() -> None:
    result = ohmic_drop(
        measured_potential_V=2.20,
        current_A=0.01,
        duration_s=10.0,
        resistance=ElectrolyteResistanceSpec(
            electrolyte_conductivity_S_m=10.0,
            electrode_gap_m=0.001,
            electrode_area_m2=0.010,
            voltage_window_V=2.0,
        ),
    )

    assert result.voltage_window_exceeded


def test_electrochemistry_model_card_is_valid() -> None:
    cards = electrochemistry_model_cards()
    assert {card.model_id for card in cards} == {
        "diffusion_layer_limiting_current_v1",
        "electrochemical_setpoint_recipe_controller_v1",
        "electrochemical_scenario_card_generation_v1",
        "nernst_butler_volmer_faradaic_v1",
        "randles_double_layer_transient_v1",
    }
    for card in cards:
        assert validate_model_card(card) == []
