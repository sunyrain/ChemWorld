from __future__ import annotations

import pytest

from chemworld.physchem import (
    ComponentPropertyPackage,
    ComponentSpec,
    MixtureSpec,
    PropertyCorrelation,
    evaluate_correlation,
    mixture_density,
    mixture_viscosity_log_rule,
    sensible_enthalpy_change,
    thermal_hazard_proxy,
    volatility_risk_from_psat,
)


def _water() -> ComponentSpec:
    return ComponentSpec(identifier="water", formula="H2O", default_phase="liquid")


def _ethanol() -> ComponentSpec:
    return ComponentSpec(
        identifier="ethanol",
        formula="C2H6O",
        default_phase="liquid",
        safety_tags=("flammable", "volatile"),
    )


def test_antoine_water_vapor_pressure_increases_monotonically() -> None:
    water_psat = PropertyCorrelation(
        correlation_id="water_antoine_mmhg",
        property_id="vapor_pressure",
        equation_id="antoine",
        coefficients={"A": 8.07131, "B": 1730.63, "C": 233.426, "base": 10.0},
        input_units={"temperature": "degC"},
        output_unit="mmHg",
        validity_ranges={"temperature": (1.0, 100.0)},
        source_note="Antoine-form benchmark coefficients for water; pressure in mmHg.",
    )

    low = evaluate_correlation(water_psat, temperature_K=293.15)
    high = evaluate_correlation(water_psat, temperature_K=353.15)
    boiling = evaluate_correlation(water_psat, temperature_K=373.15)

    assert low.to("Pa").value < high.to("Pa").value < boiling.to("Pa").value
    assert boiling.value == pytest.approx(760.0, rel=0.02)


def test_wagner_vapor_pressure_and_validity_policy() -> None:
    water_wagner = PropertyCorrelation(
        correlation_id="water_wagner",
        property_id="vapor_pressure",
        equation_id="wagner",
        coefficients={
            "Tc": 647.096,
            "Pc": 22.064e6,
            "a": -7.85951783,
            "b": 1.84408259,
            "c": -11.7866497,
            "d": 22.6807411,
        },
        input_units={"temperature": "K"},
        output_unit="Pa",
        validity_ranges={"temperature": (273.16, 647.0)},
    )

    warm = evaluate_correlation(water_wagner, temperature_K=350.0)
    hot = evaluate_correlation(water_wagner, temperature_K=450.0)
    assert warm.value < hot.value

    with pytest.raises(ValueError, match="outside validity range"):
        evaluate_correlation(water_wagner, temperature_K=260.0, validity_policy="raise")
    warned = evaluate_correlation(water_wagner, temperature_K=260.0, validity_policy="warn")
    assert warned.warnings


def test_heat_capacity_polynomial_and_enthalpy_integral() -> None:
    water_cp = PropertyCorrelation(
        correlation_id="water_liquid_cp",
        property_id="heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 75.3, "b": 0.01, "c": 0.0, "d": 0.0, "e": 0.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (273.15, 373.15)},
    )

    cp_298 = evaluate_correlation(water_cp, temperature_K=298.15)
    dh = sensible_enthalpy_change(
        water_cp,
        initial_temperature_K=298.15,
        final_temperature_K=348.15,
    )

    assert cp_298.value > 0.0
    assert dh.value > 0.0
    assert dh.unit == "J/mol"


def test_phase_change_density_viscosity_surface_tension_are_positive() -> None:
    hvap = PropertyCorrelation(
        correlation_id="water_watson_hvap",
        property_id="heat_of_vaporization",
        equation_id="watson_hvap",
        coefficients={
            "Tc": 647.096,
            "T_ref": 373.15,
            "Hvap_ref": 40650.0,
            "exponent": 0.38,
        },
        input_units={"temperature": "K"},
        output_unit="J/mol",
    )
    density = PropertyCorrelation(
        correlation_id="water_linear_density",
        property_id="liquid_density",
        equation_id="linear_liquid_density",
        coefficients={"rho_ref": 997.0, "T_ref": 298.15, "alpha": 3.0e-4},
        input_units={"temperature": "K"},
        output_unit="kg/m^3",
    )
    viscosity = PropertyCorrelation(
        correlation_id="water_andrade_viscosity",
        property_id="liquid_viscosity",
        equation_id="andrade_viscosity",
        coefficients={"A": 2.414e-5, "B": 247.8},
        input_units={"temperature": "K"},
        output_unit="Pa*s",
    )
    surface_tension = PropertyCorrelation(
        correlation_id="water_surface_tension",
        property_id="surface_tension",
        equation_id="surface_tension_power",
        coefficients={
            "Tc": 647.096,
            "T_ref": 298.15,
            "sigma_ref": 0.07197,
            "exponent": 1.26,
        },
        input_units={"temperature": "K"},
        output_unit="N/m",
    )
    fusion = PropertyCorrelation(
        correlation_id="water_constant_hfus",
        property_id="heat_of_fusion",
        equation_id="constant_phase_change_enthalpy",
        coefficients={"delta_h": 6010.0},
        input_units={"temperature": "K"},
        output_unit="J/mol",
        validity_ranges={"temperature": (250.0, 273.16)},
        source_note="constant latent-heat proxy for benchmark freezing tasks",
    )
    gas_viscosity = PropertyCorrelation(
        correlation_id="water_vapor_sutherland_viscosity",
        property_id="gas_viscosity",
        equation_id="sutherland_gas_viscosity",
        coefficients={"mu_ref": 9.0e-6, "T_ref": 300.0, "S": 110.0},
        input_units={"temperature": "K"},
        output_unit="Pa*s",
        validity_ranges={"temperature": (250.0, 900.0)},
    )

    assert evaluate_correlation(hvap, temperature_K=350.0).value > 0.0
    assert evaluate_correlation(density, temperature_K=320.0).value > 0.0
    assert evaluate_correlation(viscosity, temperature_K=298.15).value > 0.0
    assert evaluate_correlation(surface_tension, temperature_K=298.15).value > 0.0
    assert evaluate_correlation(fusion, temperature_K=260.0).value == pytest.approx(6010.0)
    assert evaluate_correlation(gas_viscosity, temperature_K=500.0).value > evaluate_correlation(
        gas_viscosity,
        temperature_K=300.0,
    ).value


def test_ideal_gas_density_uses_component_molecular_weight() -> None:
    co2 = ComponentSpec(identifier="co2", formula="CO2", default_phase="gas")
    gas_density = PropertyCorrelation(
        correlation_id="co2_ideal_gas_density",
        property_id="gas_density",
        equation_id="ideal_gas_density",
        coefficients={"unused": 0.0},
        input_units={"temperature": "K", "pressure": "Pa"},
        output_unit="kg/m^3",
    )
    value = evaluate_correlation(
        gas_density,
        temperature_K=300.0,
        pressure_Pa=101325.0,
        molecular_weight_g_mol=co2.molecular_weight_g_mol,
    )
    assert value.value == pytest.approx(1.786, rel=0.02)


def test_component_property_package_selects_valid_correlation() -> None:
    water = _water()
    low_range = PropertyCorrelation(
        correlation_id="low_range",
        property_id="heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 70.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (250.0, 280.0)},
    )
    room_range = PropertyCorrelation(
        correlation_id="room_range",
        property_id="heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 75.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (280.0, 330.0)},
    )
    package = ComponentPropertyPackage(water, (low_range, room_range))
    evaluated = package.evaluate("heat_capacity", temperature_K=298.15)

    assert evaluated.correlation_id == "room_range"
    assert evaluated.value == pytest.approx(75.0)


def test_component_property_package_respects_allowed_correlation_policy() -> None:
    water = ComponentSpec(
        identifier="water",
        formula="H2O",
        default_phase="liquid",
        allowed_property_correlations=("heat_capacity",),
    )
    allowed = PropertyCorrelation(
        correlation_id="room_range",
        property_id="heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 75.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
    )
    disallowed = PropertyCorrelation(
        correlation_id="water_antoine_mmhg",
        property_id="vapor_pressure",
        equation_id="antoine",
        coefficients={"A": 8.07131, "B": 1730.63, "C": 233.426},
        input_units={"temperature": "degC"},
        output_unit="mmHg",
    )

    assert ComponentPropertyPackage(water, (allowed,)).evaluate(
        "heat_capacity",
        temperature_K=298.15,
    ).value == pytest.approx(75.0)
    with pytest.raises(ValueError, match="not allowed"):
        ComponentPropertyPackage(water, (disallowed,))


def test_mixture_density_and_viscosity_rules_are_positive() -> None:
    water = _water()
    ethanol = _ethanol()
    mixture = MixtureSpec.from_mole_fractions(
        (water, ethanol),
        (0.4, 0.6),
        phase_label="liquid",
        temperature_K=298.15,
        pressure_Pa=101325.0,
    )

    rho = mixture_density(mixture, (997.0, 789.0))
    mu = mixture_viscosity_log_rule(mixture, (0.00089, 0.0011))

    assert 789.0 < rho.value < 997.0
    assert 0.00089 < mu.value < 0.0011


def test_safety_proxy_properties_are_bounded() -> None:
    ethanol_psat = PropertyCorrelation(
        correlation_id="ethanol_antoine_mmhg",
        property_id="vapor_pressure",
        equation_id="antoine",
        coefficients={"A": 8.20417, "B": 1642.89, "C": 230.3, "base": 10.0},
        input_units={"temperature": "degC"},
        output_unit="mmHg",
    )
    psat = evaluate_correlation(ethanol_psat, temperature_K=298.15)
    volatility = volatility_risk_from_psat(psat)
    thermal = thermal_hazard_proxy(
        temperature_K=420.0,
        onset_temperature_K=380.0,
        severe_temperature_K=500.0,
    )

    assert 0.0 <= volatility.value <= 1.0
    assert 0.0 <= thermal.value <= 1.0
    assert thermal.value == pytest.approx((420.0 - 380.0) / (500.0 - 380.0))
