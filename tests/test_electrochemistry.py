from __future__ import annotations

import math

import pytest

from chemworld.physchem.electrochemistry import (
    FARADAY_C_PER_MOL,
    ElectrodeReactionSpec,
    butler_volmer_current,
    electrochemistry_model_cards,
    faradaic_extent_mol,
    nernst_potential,
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


def test_run_electrolysis_limits_substrate_and_reports_energy_accounting() -> None:
    spec = _spec()
    result = run_electrolysis(
        spec,
        electrode_potential_V=1.0,
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


def test_electrochemistry_model_card_is_valid() -> None:
    cards = electrochemistry_model_cards()
    assert [card.model_id for card in cards] == ["nernst_butler_volmer_faradaic_v1"]
    for card in cards:
        assert validate_model_card(card) == []
