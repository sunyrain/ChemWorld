from __future__ import annotations

from math import log

import pytest

from chemworld.physchem import (
    CubicEOSSpec,
    EOSComponentSpec,
    cubic_compressibility_roots,
    eos_model_cards,
    evaluate_cubic_eos,
    ideal_gas_molar_volume,
    ideal_gas_pressure,
    ideal_gas_state,
)
from chemworld.physchem.eos import R_J_PER_MOL_K


def _methane() -> EOSComponentSpec:
    return EOSComponentSpec(
        "methane",
        critical_temperature_K=190.56,
        critical_pressure_Pa=4.5992e6,
        acentric_factor=0.011,
    )


def _ethane() -> EOSComponentSpec:
    return EOSComponentSpec(
        "ethane",
        critical_temperature_K=305.32,
        critical_pressure_Pa=4.872e6,
        acentric_factor=0.099,
    )


def test_ideal_gas_state_matches_pv_nrt() -> None:
    volume = ideal_gas_molar_volume(temperature_K=350.0, pressure_Pa=2.0e5)
    assert volume == pytest.approx(R_J_PER_MOL_K * 350.0 / 2.0e5)

    pressure = ideal_gas_pressure(amount_mol=2.0, volume_m3=0.1, temperature_K=350.0)
    assert pressure == pytest.approx(2.0 * R_J_PER_MOL_K * 350.0 / 0.1)

    state = ideal_gas_state({"methane": 2.0, "ethane": 1.0}, temperature_K=350.0, pressure_Pa=1e5)
    assert state.compressibility_factor == pytest.approx(1.0)
    assert state.fugacity_coefficients == {"methane": 1.0, "ethane": 1.0}
    assert state.composition["methane"] == pytest.approx(2.0 / 3.0)
    assert state.root_selection_policy == "ideal_single_root"
    assert state.molar_residual_enthalpy_J_mol == pytest.approx(0.0)
    assert state.molar_residual_entropy_J_mol_K == pytest.approx(0.0)
    assert state.molar_residual_gibbs_J_mol == pytest.approx(0.0)


def test_peng_robinson_low_pressure_approaches_ideal_gas() -> None:
    spec = CubicEOSSpec("pr_methane", "peng_robinson", (_methane(),))
    state = evaluate_cubic_eos(
        spec,
        {"methane": 1.0},
        temperature_K=350.0,
        pressure_Pa=1.0e4,
    )

    assert state.compressibility_factor == pytest.approx(1.0, rel=2e-3)
    assert state.fugacity_coefficients["methane"] == pytest.approx(1.0, rel=5e-3)
    assert state.molar_residual_enthalpy_J_mol == pytest.approx(0.0, abs=40.0)
    assert state.molar_residual_entropy_J_mol_K == pytest.approx(0.0, abs=0.2)
    assert state.molar_volume_m3_mol == pytest.approx(
        ideal_gas_molar_volume(350.0, 1.0e4),
        rel=2e-3,
    )


def test_peng_robinson_detects_liquid_and_vapor_roots() -> None:
    spec = CubicEOSSpec("pr_methane", "peng_robinson", (_methane(),))
    roots = cubic_compressibility_roots(
        spec,
        {"methane": 1.0},
        temperature_K=150.0,
        pressure_Pa=1.0e6,
    )
    liquid = evaluate_cubic_eos(
        spec,
        {"methane": 1.0},
        temperature_K=150.0,
        pressure_Pa=1.0e6,
        phase="liquid",
    )
    vapor = evaluate_cubic_eos(
        spec,
        {"methane": 1.0},
        temperature_K=150.0,
        pressure_Pa=1.0e6,
        phase="vapor",
    )

    assert len(roots) >= 2
    assert liquid.compressibility_factor == min(roots)
    assert vapor.compressibility_factor == max(roots)
    assert liquid.root_selection_policy == "smallest_z_liquid"
    assert vapor.root_selection_policy == "largest_z_vapor"
    assert liquid.molar_volume_m3_mol < vapor.molar_volume_m3_mol
    assert liquid.molar_residual_enthalpy_J_mol < vapor.molar_residual_enthalpy_J_mol


def test_srk_and_peng_robinson_mixture_fugacity_coefficients_are_positive() -> None:
    composition = {"methane": 0.7, "ethane": 0.3}
    for model in ("peng_robinson", "srk"):
        spec = CubicEOSSpec(
            f"{model}_mixture",
            model,
            (_methane(), _ethane()),
            binary_interaction={"methane|ethane": 0.01},
        )
        state = evaluate_cubic_eos(
            spec,
            composition,
            temperature_K=280.0,
            pressure_Pa=3.0e6,
            phase="stable",
        )

        assert state.compressibility_factor > 0.0
        assert all(value > 0.0 for value in state.fugacity_coefficients.values())
        assert state.root_selection_policy in {
            "single_admissible_root",
            "minimum_molar_residual_gibbs",
        }
        assert set(state.fugacity_coefficients) == {"methane", "ethane"}
        assert state.mixture_parameters["a_mix"] > 0.0
        assert state.mixture_parameters["da_mix_dT"] < 0.0
        assert state.mixture_parameters["b_mix"] > 0.0
        gibbs_from_hs = (
            state.molar_residual_enthalpy_J_mol
            - state.temperature_K * state.molar_residual_entropy_J_mol_K
        )
        assert state.molar_residual_gibbs_J_mol == pytest.approx(gibbs_from_hs, rel=2e-10)


def test_cubic_residual_gibbs_matches_fugacity_for_pure_roots() -> None:
    spec = CubicEOSSpec("pr_methane", "peng_robinson", (_methane(),))
    for phase in ("liquid", "vapor"):
        state = evaluate_cubic_eos(
            spec,
            {"methane": 1.0},
            temperature_K=150.0,
            pressure_Pa=1.0e6,
            phase=phase,
        )
        expected_gibbs = (
            R_J_PER_MOL_K
            * state.temperature_K
            * log(state.fugacity_coefficients["methane"])
        )
        assert state.molar_residual_gibbs_J_mol == pytest.approx(expected_gibbs)
        assert state.residual_properties["departure_log_argument"] > 1.0


def test_cubic_stable_root_uses_lowest_residual_gibbs() -> None:
    spec = CubicEOSSpec("pr_methane", "peng_robinson", (_methane(),))
    liquid = evaluate_cubic_eos(
        spec,
        {"methane": 1.0},
        temperature_K=150.0,
        pressure_Pa=1.0e6,
        phase="liquid",
    )
    vapor = evaluate_cubic_eos(
        spec,
        {"methane": 1.0},
        temperature_K=150.0,
        pressure_Pa=1.0e6,
        phase="vapor",
    )
    stable = evaluate_cubic_eos(
        spec,
        {"methane": 1.0},
        temperature_K=150.0,
        pressure_Pa=1.0e6,
        phase="stable",
    )

    assert stable.root_selection_policy == "minimum_molar_residual_gibbs"
    assert stable.molar_residual_gibbs_J_mol == pytest.approx(
        min(liquid.molar_residual_gibbs_J_mol, vapor.molar_residual_gibbs_J_mol)
    )


def test_eos_model_card_documents_residual_slice() -> None:
    card = next(
        card for card in eos_model_cards() if card.model_id == "cubic_eos_pr_srk_residuals"
    )

    assert card.maturity.value == "reference_validated"
    assert any("H^R" in equation for equation in card.equations)
    assert any(evidence.status in {"passing", "optional"} for evidence in card.validation_evidence)


def test_eos_validation_fails_fast() -> None:
    spec = CubicEOSSpec("pr_methane", "peng_robinson", (_methane(),))
    with pytest.raises(ValueError, match="composition values"):
        evaluate_cubic_eos(spec, {"methane": -1.0}, temperature_K=300.0, pressure_Pa=1e5)
    with pytest.raises(ValueError, match="missing"):
        evaluate_cubic_eos(
            spec,
            {"ethane": 1.0},
            temperature_K=300.0,
            pressure_Pa=1e5,
        )
    with pytest.raises(ValueError, match="temperature_K"):
        evaluate_cubic_eos(spec, {"methane": 1.0}, temperature_K=0.0, pressure_Pa=1e5)
