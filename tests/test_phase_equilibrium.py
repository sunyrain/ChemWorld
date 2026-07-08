from __future__ import annotations

import pytest

from chemworld.physchem import (
    ActivityModelSpec,
    activity_coefficients,
    bubble_pressure_pa,
    dew_pressure_pa,
    flash_isothermal,
    liquid_liquid_split,
    rachford_rice_vapor_fraction,
    raoult_k_values,
)


def test_ideal_and_margules_activity_coefficients() -> None:
    ideal = ActivityModelSpec("ideal_ab", ("A", "B"), "ideal")
    assert activity_coefficients(ideal, {"A": 0.2, "B": 0.8}, temperature_K=298.15) == {
        "A": 1.0,
        "B": 1.0,
    }

    margules = ActivityModelSpec(
        "margules_ab",
        ("A", "B"),
        "margules",
        {"A:A|B": 1.2, "A:B|A": 0.8},
    )
    gamma = activity_coefficients(margules, {"A": 0.2, "B": 0.8}, temperature_K=298.15)
    assert gamma["A"] > 1.0
    assert gamma["B"] > 1.0
    assert gamma["A"] > gamma["B"]


def test_nrtl_lite_activity_coefficients_are_positive() -> None:
    model = ActivityModelSpec(
        "nrtl_ab",
        ("A", "B"),
        "nrtl_lite",
        {
            "tau:A|B": 1.0,
            "tau:B|A": -0.2,
            "alpha:A|B": 0.3,
            "alpha:B|A": 0.3,
        },
    )
    gamma = activity_coefficients(model, {"A": 0.4, "B": 0.6}, temperature_K=310.0)
    assert all(value > 0.0 for value in gamma.values())
    assert gamma["A"] != pytest.approx(1.0)


def test_rachford_rice_flash_balances_two_phase_split() -> None:
    z = {"light": 0.5, "heavy": 0.5}
    k_values = {"light": 2.0, "heavy": 0.5}
    beta = rachford_rice_vapor_fraction(z, k_values)
    flash = flash_isothermal(z, k_values)

    assert beta == pytest.approx(0.5)
    assert flash.vapor_fraction == pytest.approx(0.5)
    assert flash.vapor_composition["light"] > flash.liquid_composition["light"]
    assert sum(flash.liquid_composition.values()) == pytest.approx(1.0)
    assert sum(flash.vapor_composition.values()) == pytest.approx(1.0)


def test_raoult_k_values_bubble_and_dew_pressure() -> None:
    model = ActivityModelSpec("ideal_ab", ("A", "B"), "ideal")
    psat = {"A": 100_000.0, "B": 20_000.0}
    liquid = {"A": 0.25, "B": 0.75}
    vapor = {"A": 0.6, "B": 0.4}

    bubble = bubble_pressure_pa(
        liquid,
        vapor_pressures_Pa=psat,
        activity_model=model,
        temperature_K=330.0,
    )
    dew = dew_pressure_pa(
        vapor,
        vapor_pressures_Pa=psat,
        activity_model=model,
        temperature_K=330.0,
    )
    k_values = raoult_k_values(
        model,
        liquid,
        vapor_pressures_Pa=psat,
        pressure_Pa=bubble,
        temperature_K=330.0,
    )

    assert 20_000.0 < bubble < 100_000.0
    assert 20_000.0 < dew < 100_000.0
    assert sum(liquid[key] * k_values[key] for key in liquid) == pytest.approx(1.0)


def test_lle_split_preserves_material_and_extractant_volume_improves_recovery() -> None:
    feed = {"product": 1.0, "impurity": 0.2}
    small = liquid_liquid_split(
        feed,
        partition_coefficients={"product": 4.0, "impurity": 0.5},
        aqueous_volume_L=1.0,
        organic_volume_L=0.25,
        stage_efficiency=0.9,
    )
    large = liquid_liquid_split(
        feed,
        partition_coefficients={"product": 4.0, "impurity": 0.5},
        aqueous_volume_L=1.0,
        organic_volume_L=1.0,
        stage_efficiency=0.9,
    )

    assert large.recovery_to_organic["product"] > small.recovery_to_organic["product"]
    assert large.recovery_to_organic["product"] > large.recovery_to_organic["impurity"]
    assert large.material_balance_error_mol < 1e-12


def test_phase_equilibrium_validation_fails_fast() -> None:
    model = ActivityModelSpec("ideal_ab", ("A", "B"), "ideal")
    with pytest.raises(ValueError, match="missing"):
        activity_coefficients(model, {"A": 1.0}, temperature_K=298.15)
    with pytest.raises(ValueError, match="K-value"):
        flash_isothermal({"A": 0.5, "B": 0.5}, {"A": 1.0})
    with pytest.raises(ValueError, match="phase volumes"):
        liquid_liquid_split(
            {"A": 1.0},
            partition_coefficients={"A": 1.0},
            aqueous_volume_L=0.0,
            organic_volume_L=1.0,
        )
