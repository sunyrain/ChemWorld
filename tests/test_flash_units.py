from __future__ import annotations

import pytest

from chemworld.physchem import (
    ActivityModelSpec,
    MaturityLevel,
    flash_unit_model_cards,
    tp_flash_with_energy_balance,
    validate_model_card,
)


def _enthalpy_maps() -> tuple[dict[str, float], dict[str, float], dict[str, float]]:
    feed = {"light": 0.0, "heavy": 0.0}
    liquid = {"light": 0.0, "heavy": 0.0}
    vapor = {"light": 30_000.0, "heavy": 40_000.0}
    return feed, liquid, vapor


def test_tp_flash_closes_material_and_enthalpy_balances() -> None:
    feed_h, liquid_h, vapor_h = _enthalpy_maps()
    result = tp_flash_with_energy_balance(
        {"light": 0.5, "heavy": 0.5},
        temperature_K=350.0,
        pressure_Pa=100_000.0,
        vapor_pressures_Pa={"light": 200_000.0, "heavy": 50_000.0},
        feed_molar_enthalpies_J_mol=feed_h,
        liquid_molar_enthalpies_J_mol=liquid_h,
        vapor_molar_enthalpies_J_mol=vapor_h,
    )

    assert result.converged
    assert result.phase_status == "two_phase"
    assert result.vapor_fraction == pytest.approx(0.5)
    assert result.material_balance_error_mol < 1.0e-12
    assert result.energy_balance_error_J < 1.0e-12
    assert result.heat_duty_J > 0.0
    for component_id, feed_amount in result.feed_amounts_mol.items():
        recovered = (
            result.liquid_amounts_mol[component_id]
            + result.vapor_amounts_mol[component_id]
        )
        assert recovered == pytest.approx(feed_amount)


def test_tp_flash_exposes_nonideal_gamma_phi_hooks() -> None:
    feed_h, liquid_h, vapor_h = _enthalpy_maps()
    activity = ActivityModelSpec(
        "margules_light_heavy",
        ("light", "heavy"),
        "margules",
        {"A:light|heavy": 1.2, "A:heavy|light": 0.8},
    )
    result = tp_flash_with_energy_balance(
        {"light": 0.4, "heavy": 0.6},
        temperature_K=350.0,
        pressure_Pa=100_000.0,
        vapor_pressures_Pa={"light": 150_000.0, "heavy": 40_000.0},
        feed_molar_enthalpies_J_mol=feed_h,
        liquid_molar_enthalpies_J_mol=liquid_h,
        vapor_molar_enthalpies_J_mol=vapor_h,
        activity_model=activity,
        vapor_fugacity_coefficients={"light": 0.95, "heavy": 0.98},
        liquid_reference_fugacity_coefficients={"light": 1.0, "heavy": 1.0},
        poynting_factors={"light": 1.01, "heavy": 1.02},
    )

    assert result.converged
    assert result.activity_coefficients["light"] > 1.0
    assert result.vapor_fugacity_coefficients["light"] == pytest.approx(0.95)
    assert result.k_values["light"] > result.k_values["heavy"]
    assert result.material_balance_error_mol < 1.0e-10


def test_tp_flash_model_card_is_auditable() -> None:
    cards = flash_unit_model_cards()

    assert len(cards) == 1
    assert cards[0].model_id == "tp_gamma_phi_flash_energy_balance_v1"
    assert cards[0].maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(cards[0]) == []


@pytest.mark.parametrize(
    "kwargs",
    (
        {"pressure_Pa": 0.0},
        {"temperature_K": 0.0},
        {"max_iterations": 0},
    ),
)
def test_tp_flash_rejects_invalid_controls(kwargs: dict[str, float | int]) -> None:
    feed_h, liquid_h, vapor_h = _enthalpy_maps()
    inputs = {
        "temperature_K": 350.0,
        "pressure_Pa": 100_000.0,
        "vapor_pressures_Pa": {"light": 200_000.0, "heavy": 50_000.0},
        "feed_molar_enthalpies_J_mol": feed_h,
        "liquid_molar_enthalpies_J_mol": liquid_h,
        "vapor_molar_enthalpies_J_mol": vapor_h,
        **kwargs,
    }
    with pytest.raises(ValueError):
        tp_flash_with_energy_balance({"light": 0.5, "heavy": 0.5}, **inputs)
