from __future__ import annotations

import pytest

from chemworld.physchem import (
    ComponentPropertyPackage,
    ComponentSpec,
    MaturityLevel,
    MixtureEnthalpyLedger,
    MixtureSpec,
    MixtureVolumeLedger,
    MolarVolumeReport,
    PhaseEnthalpyReport,
    PhaseTransitionSpec,
    PropertyCorrelation,
    curated_property_case_map,
    curated_property_model_cards,
    curated_property_package,
    density_to_molar_volume_m3_mol,
    evaluate_correlation,
    heat_capacity_report,
    ideal_gas_molar_volume_report,
    list_curated_property_packages,
    mixture_density,
    mixture_enthalpy_ledger,
    mixture_molar_volume_ledger,
    mixture_viscosity_log_rule,
    molar_volume_report,
    molar_volume_to_density_kg_m3,
    phase_path_enthalpy_report,
    phase_sensible_enthalpy_report,
    phase_transition_enthalpy,
    property_correlation_model_cards,
    resolve_component_identifier,
    second_virial_coefficient_report,
    sensible_enthalpy_change,
    thermal_hazard_proxy,
    validate_model_card,
    vapor_pressure_report,
    vapor_pressure_temperature_derivative,
    virial_gas_molar_volume_report,
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

    derivative = vapor_pressure_temperature_derivative(
        water_psat,
        temperature_K=353.15,
    )
    finite_difference = (
        evaluate_correlation(water_psat, temperature_K=353.151).value
        - evaluate_correlation(water_psat, temperature_K=353.149).value
    ) / 0.002
    assert derivative.value == pytest.approx(finite_difference, rel=1e-5)

    report = vapor_pressure_report(water_psat, temperature_K=353.15)
    assert report.method_family == "Antoine"
    assert report.validity_status == "valid"
    assert report.dp_dt_pa_per_k > 0.0
    assert report.dln_pressure_dT_1_K == pytest.approx(
        derivative.value / report.pressure.value
    )
    assert report.to_dict()["method_family"] == "Antoine"


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

    report = vapor_pressure_report(water_wagner, temperature_K=350.0)
    assert report.method_family == "Wagner"
    assert report.temperature_derivative_value > 0.0


def test_vapor_pressure_report_supports_sublimation_pressure() -> None:
    ice_sublimation = PropertyCorrelation(
        correlation_id="ice_sublimation_antoine_demo",
        property_id="sublimation_pressure",
        equation_id="antoine",
        coefficients={"A": 11.344, "B": 3885.7, "C": -42.98, "base": 10.0},
        input_units={"temperature": "K"},
        output_unit="Pa",
        validity_ranges={"temperature": (180.0, 273.15)},
        source_note=(
            "Compact sublimation-pressure correlation fixture for API "
            "validation, not a broad data table."
        ),
    )

    report = vapor_pressure_report(
        ice_sublimation,
        temperature_K=250.0,
        validity_policy="raise",
    )
    assert report.pressure.property_id == "sublimation_pressure"
    assert report.pressure.value > 0.0
    assert report.temperature_derivative_value > 0.0

    with pytest.raises(ValueError, match="outside validity range"):
        vapor_pressure_report(
            ice_sublimation,
            temperature_K=290.0,
            validity_policy="raise",
        )


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


def test_phase_heat_capacity_reports_reference_state_and_phase() -> None:
    liquid_cp = PropertyCorrelation(
        correlation_id="water_liquid_cp_phase",
        property_id="liquid_heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 75.0, "b": 0.02},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (273.15, 373.15)},
        metadata={"phase": "liquid"},
    )
    solid_cp = PropertyCorrelation(
        correlation_id="ice_solid_cp_phase",
        property_id="solid_heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 37.0, "b": 0.01},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (200.0, 273.15)},
        metadata={"phase": "solid"},
    )

    cp_eval = heat_capacity_report(liquid_cp, temperature_K=298.15)
    zero = phase_sensible_enthalpy_report(
        component_id="water",
        phase="liquid",
        heat_capacity_correlation=liquid_cp,
        initial_temperature_K=298.15,
        final_temperature_K=298.15,
        reference_temperature_K=298.15,
        validity_policy="raise",
    )
    warming = phase_sensible_enthalpy_report(
        component_id="water",
        phase="solid",
        heat_capacity_correlation=solid_cp,
        initial_temperature_K=250.0,
        final_temperature_K=260.0,
        reference_temperature_K=250.0,
        validity_policy="raise",
    )

    assert cp_eval.value > 0.0
    assert isinstance(zero, PhaseEnthalpyReport)
    assert zero.total_enthalpy_J_mol == pytest.approx(0.0)
    expected_solid = (37.0 * 260.0 + 0.5 * 0.01 * 260.0**2) - (
        37.0 * 250.0 + 0.5 * 0.01 * 250.0**2
    )
    assert warming.total_enthalpy_J_mol == pytest.approx(expected_solid)


def test_phase_path_enthalpy_and_mixture_ledger() -> None:
    solid_cp = PropertyCorrelation(
        correlation_id="ice_cp_path",
        property_id="solid_heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 38.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (200.0, 273.15)},
        metadata={"phase": "solid"},
    )
    liquid_cp = PropertyCorrelation(
        correlation_id="water_cp_path",
        property_id="liquid_heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 75.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (273.15, 373.15)},
        metadata={"phase": "liquid"},
    )
    gas_cp = PropertyCorrelation(
        correlation_id="steam_cp_path",
        property_id="ideal_gas_heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 34.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (373.15, 700.0)},
        metadata={"phase": "gas"},
    )
    hfus = PropertyCorrelation(
        correlation_id="water_hfus_path",
        property_id="heat_of_fusion",
        equation_id="constant_phase_change_enthalpy",
        coefficients={"delta_h": 6010.0},
        input_units={"temperature": "K"},
        output_unit="J/mol",
        validity_ranges={"temperature": (250.0, 280.0)},
    )
    hvap = PropertyCorrelation(
        correlation_id="water_hvap_watson_path",
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
        validity_ranges={"temperature": (273.15, 647.0)},
    )
    fusion = PhaseTransitionSpec(
        transition_id="water_fusion",
        from_phase="solid",
        to_phase="liquid",
        transition_temperature_K=273.15,
        enthalpy_correlation=hfus,
    )
    vaporization = PhaseTransitionSpec(
        transition_id="water_vaporization",
        from_phase="liquid",
        to_phase="gas",
        transition_temperature_K=373.15,
        enthalpy_correlation=hvap,
    )

    report = phase_path_enthalpy_report(
        component_id="water",
        heat_capacity_correlations={
            "solid": solid_cp,
            "liquid": liquid_cp,
            "gas": gas_cp,
        },
        transitions=(fusion, vaporization),
        initial_phase="solid",
        final_phase="gas",
        initial_temperature_K=250.0,
        final_temperature_K=400.0,
        validity_policy="raise",
    )
    condensation = phase_transition_enthalpy(
        vaporization,
        from_phase="gas",
        to_phase="liquid",
        validity_policy="raise",
    )
    ledger = mixture_enthalpy_ledger(
        component_amounts_mol={"water": 2.0},
        component_reports={"water": report},
        ledger_id="reactor_heat_duty",
    )

    expected = (
        38.0 * (273.15 - 250.0)
        + 6010.0
        + 75.0 * (373.15 - 273.15)
        + 40650.0
        + 34.0 * (400.0 - 373.15)
    )
    assert report.transition_ids == ("water_fusion", "water_vaporization")
    assert report.total_enthalpy_J_mol == pytest.approx(expected)
    assert condensation.value == pytest.approx(-40650.0)
    assert isinstance(ledger, MixtureEnthalpyLedger)
    assert ledger.total_enthalpy_change_J == pytest.approx(2.0 * expected)
    assert ledger.to_dict()["ledger_id"] == "reactor_heat_duty"


def test_phase_enthalpy_failures_are_explicit() -> None:
    liquid_cp = PropertyCorrelation(
        correlation_id="bad_liquid_cp",
        property_id="liquid_heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": -10.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (250.0, 350.0)},
        metadata={"phase": "liquid"},
    )
    gas_cp = PropertyCorrelation(
        correlation_id="gas_cp_for_wrong_phase",
        property_id="ideal_gas_heat_capacity",
        equation_id="cp_polynomial",
        coefficients={"a": 30.0},
        input_units={"temperature": "K"},
        output_unit="J/(mol*K)",
        validity_ranges={"temperature": (250.0, 500.0)},
        metadata={"phase": "gas"},
    )

    with pytest.raises(ValueError, match="positive"):
        sensible_enthalpy_change(
            liquid_cp,
            initial_temperature_K=280.0,
            final_temperature_K=300.0,
        )
    with pytest.raises(ValueError, match="not 'liquid'"):
        phase_sensible_enthalpy_report(
            component_id="water",
            phase="liquid",
            heat_capacity_correlation=gas_cp,
            initial_temperature_K=280.0,
            final_temperature_K=300.0,
        )
    with pytest.raises(ValueError, match="Missing heat-capacity correlation"):
        phase_path_enthalpy_report(
            component_id="water",
            heat_capacity_correlations={"liquid": gas_cp},
            transitions=(),
            initial_phase="gas",
            final_phase="gas",
            initial_temperature_K=300.0,
            final_temperature_K=320.0,
        )


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


def test_rackett_molar_volume_report_and_density_conversion() -> None:
    propane_rackett = PropertyCorrelation(
        correlation_id="propane_rackett",
        property_id="liquid_molar_volume",
        equation_id="rackett_liquid_molar_volume",
        coefficients={"Tc": 369.83, "Pc": 4248000.0, "Zc": 0.2763},
        input_units={"temperature": "K"},
        output_unit="m^3/mol",
        validity_ranges={"temperature": (90.0, 369.0)},
        metadata={"phase": "liquid"},
    )
    report = molar_volume_report(
        propane_rackett,
        temperature_K=272.03889,
        phase="liquid",
        molecular_weight_g_mol=44.09562,
        validity_policy="raise",
    )

    expected_vm = (
        8.31446261815324
        * 369.83
        / 4248000.0
        * 0.2763 ** (1.0 + (1.0 - 272.03889 / 369.83) ** (2.0 / 7.0))
    )
    assert isinstance(report, MolarVolumeReport)
    assert report.method_family == "Rackett"
    assert report.molar_volume_m3_mol == pytest.approx(expected_vm)
    assert report.density_kg_m3 == pytest.approx(531.322141, rel=1e-6)
    assert molar_volume_to_density_kg_m3(expected_vm, 44.09562) == pytest.approx(
        report.density_kg_m3
    )
    assert density_to_molar_volume_m3_mol(report.density_kg_m3, 44.09562) == pytest.approx(
        expected_vm
    )


def test_ideal_and_virial_gas_molar_volume_reports() -> None:
    ideal = ideal_gas_molar_volume_report(
        temperature_K=300.0,
        pressure_Pa=101325.0,
        molecular_weight_g_mol=44.01,
    )
    virial_correlation = PropertyCorrelation(
        correlation_id="co2_crc_second_virial_demo",
        property_id="second_virial_coefficient",
        equation_id="crc_second_virial",
        coefficients={"a1": -100.0, "a2": 20.0},
        input_units={"temperature": "K"},
        output_unit="m^3/mol",
        validity_ranges={"temperature": (250.0, 600.0)},
    )
    second_virial = second_virial_coefficient_report(
        virial_correlation,
        temperature_K=298.15,
        validity_policy="raise",
    )
    virial = virial_gas_molar_volume_report(
        temperature_K=298.15,
        pressure_Pa=101325.0,
        second_virial_m3_mol=second_virial.value,
        molecular_weight_g_mol=44.01,
    )

    rt = 8.31446261815324 * 298.15
    expected_root = (rt + (rt * rt + 4.0 * 101325.0 * rt * second_virial.value) ** 0.5) / (
        2.0 * 101325.0
    )
    assert ideal.compressibility_status == "ideal"
    assert ideal.compressibility_factor == pytest.approx(1.0)
    assert second_virial.value == pytest.approx(-100e-6)
    assert virial.molar_volume_m3_mol == pytest.approx(expected_root)
    assert virial.compressibility_factor == pytest.approx(101325.0 * expected_root / rt)
    assert virial.compressibility_status == "low_correction"
    assert virial.density_kg_m3 > ideal.density_kg_m3


def test_mixture_molar_volume_ledger_closes_amgat_rule() -> None:
    ledger = mixture_molar_volume_ledger(
        component_mole_fractions={"water": 0.4, "ethanol": 0.6},
        component_molar_volumes_m3_mol={"water": 18.1e-6, "ethanol": 58.7e-6},
        component_molecular_weights_g_mol={"water": 18.01528, "ethanol": 46.06844},
        phase="liquid",
        ledger_id="aqueous_organic_volume_check",
    )

    expected_vm = 0.4 * 18.1e-6 + 0.6 * 58.7e-6
    expected_mw = 0.4 * 18.01528 + 0.6 * 46.06844
    assert isinstance(ledger, MixtureVolumeLedger)
    assert ledger.mixture_molar_volume_m3_mol == pytest.approx(expected_vm)
    assert ledger.mixture_density_kg_m3 == pytest.approx(
        molar_volume_to_density_kg_m3(expected_vm, expected_mw)
    )
    assert ledger.contributions["ethanol"]["volume_contribution_m3_mol"] == pytest.approx(
        0.6 * 58.7e-6
    )
    assert ledger.warnings


def test_density_molar_volume_failures_are_explicit() -> None:
    bad_rackett = PropertyCorrelation(
        correlation_id="bad_rackett",
        property_id="liquid_molar_volume",
        equation_id="rackett_liquid_molar_volume",
        coefficients={"Tc": 400.0, "Pc": 4.0e6, "Zc": 0.27},
        input_units={"temperature": "K"},
        output_unit="m^3/mol",
    )

    with pytest.raises(ValueError, match="T < Tc"):
        molar_volume_report(
            bad_rackett,
            temperature_K=410.0,
            phase="liquid",
            validity_policy="raise",
        )
    with pytest.raises(ValueError, match="no positive gas-volume root"):
        virial_gas_molar_volume_report(
            temperature_K=300.0,
            pressure_Pa=5.0e6,
            second_virial_m3_mol=-0.1,
        )
    with pytest.raises(ValueError, match="sum to 1"):
        mixture_molar_volume_ledger(
            component_mole_fractions={"a": 0.4, "b": 0.4},
            component_molar_volumes_m3_mol={"a": 1e-5, "b": 2e-5},
        )


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


def test_curated_property_packages_are_reference_ready() -> None:
    packages = list_curated_property_packages()
    cases = curated_property_case_map()
    assert {package.component.identifier for package in packages} == {
        "water",
        "ethanol",
        "acetone",
        "toluene",
        "methane",
        "carbon_dioxide",
    }

    for package in packages:
        component_id = package.component.identifier
        case = cases[component_id]
        assert ComponentSpec.from_dict(package.component.to_dict()).identifier == component_id
        assert package.component.metadata["casrn"] == case.casrn
        assert package.component.cas_number == case.casrn
        assert package.component.provenance
        assert package.component.uncertainty
        assert package.component.metadata["provenance_source_ids"]
        assert {
            uncertainty.field_id for uncertainty in package.component.uncertainty
        } >= {"molecular_weight_g_mol", "curated_property_coefficients"}

        vapor_pressure = package.evaluate(
            "vapor_pressure",
            temperature_K=case.reference_temperature_K,
            validity_policy="raise",
        )
        vapor_pressure_with_derivative = package.vapor_pressure_report(
            temperature_K=case.reference_temperature_K,
            validity_policy="raise",
        )
        ideal_gas_cp = package.evaluate(
            "ideal_gas_heat_capacity",
            temperature_K=case.reference_temperature_K,
            validity_policy="raise",
        )
        cp_correlation = package.by_property("ideal_gas_heat_capacity")[0]
        enthalpy = sensible_enthalpy_change(
            cp_correlation,
            initial_temperature_K=case.enthalpy_initial_temperature_K,
            final_temperature_K=case.enthalpy_final_temperature_K,
            validity_policy="raise",
        )

        assert vapor_pressure.value > 0.0
        assert vapor_pressure.unit == "Pa"
        assert vapor_pressure_with_derivative.method_family == "DIPPR101"
        assert vapor_pressure_with_derivative.temperature_derivative_value > 0.0
        step = 1e-3
        finite_difference = (
            package.evaluate(
                "vapor_pressure",
                temperature_K=case.reference_temperature_K + step,
                validity_policy="raise",
            ).value
            - package.evaluate(
                "vapor_pressure",
                temperature_K=case.reference_temperature_K - step,
                validity_policy="raise",
            ).value
        ) / (2.0 * step)
        assert vapor_pressure_with_derivative.temperature_derivative_value == pytest.approx(
            finite_difference,
            rel=1e-5,
        )
        assert ideal_gas_cp.value > 0.0
        assert ideal_gas_cp.unit == "J/(mol*K)"
        assert enthalpy.value > 0.0
        for correlation in package.correlations:
            payload = PropertyCorrelation.from_dict(correlation.to_dict()).to_dict()
            assert payload == correlation.to_dict()
            assert correlation.metadata["casrn"] == case.casrn


def test_curated_property_package_accepts_aliases() -> None:
    assert curated_property_package("co2").component.identifier == "carbon_dioxide"
    assert curated_property_package("carbon dioxide").component.identifier == "carbon_dioxide"
    components = tuple(package.component for package in list_curated_property_packages())
    assert resolve_component_identifier(components, "carbon dioxide") == "carbon_dioxide"
    assert resolve_component_identifier(components, "ethyl alcohol") == "ethanol"
    with pytest.raises(KeyError, match="unknown curated component"):
        curated_property_package("unobtainium")


def test_curated_property_model_card_is_auditable() -> None:
    cards = curated_property_model_cards()
    assert len(cards) == 1
    card = cards[0]
    assert card.model_id == "curated_dippr101_poling_property_subset"
    assert card.module_id == "properties"
    assert card.maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(card) == []
    assert {
        evidence.reference_backend for evidence in card.validation_evidence
    } == {"chemicals"}
    assert any("DIPPR101" in equation for equation in card.equations)


def test_property_correlation_model_card_is_auditable() -> None:
    cards = property_correlation_model_cards()
    assert len(cards) == 3
    card_map = {card.model_id: card for card in cards}
    card = card_map["vapor_pressure_correlation_families"]
    assert card.model_id == "vapor_pressure_correlation_families"
    assert card.module_id == "properties"
    assert card.maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(card) == []
    assert any("dP/dT" in equation for equation in card.equations)
    assert {
        evidence.evidence_id for evidence in card.validation_evidence
    } >= {
        "antoine-vapor-pressure-derivative-test",
        "dippr101-vapor-pressure-derivative-test",
    }
    enthalpy_card = card_map["phase_heat_capacity_enthalpy_package"]
    assert enthalpy_card.maturity is MaturityLevel.PROFESSIONAL_CANDIDATE
    assert validate_model_card(enthalpy_card) == []
    assert any("Delta H" in equation for equation in enthalpy_card.equations)
    assert {
        evidence.evidence_id for evidence in enthalpy_card.validation_evidence
    } >= {
        "phase-cp-integral-regression-test",
        "phase-transition-ledger-test",
    }
    volume_card = card_map["density_molar_volume_package"]
    assert volume_card.maturity is MaturityLevel.PROFESSIONAL_CANDIDATE
    assert validate_model_card(volume_card) == []
    assert any("Rackett" in equation for equation in volume_card.equations)
    assert {
        evidence.evidence_id for evidence in volume_card.validation_evidence
    } >= {
        "rackett-liquid-volume-test",
        "virial-gas-volume-root-test",
    }
