from __future__ import annotations

import os

import pytest

from chemworld.physchem import (
    ActivityModelSpec,
    FluidState,
    PipeSpec,
    bubble_pressure_pa,
    compare_scalar,
    curated_property_cases,
    curated_property_package,
    darcy_friction_factor,
    dew_pressure_pa,
    flash_isothermal,
    ideal_gas_molar_volume,
    import_reference_module,
    pipe_pressure_drop,
    prandtl_number,
    raoult_k_values,
    reynolds_number,
    sensible_enthalpy_change,
    summarize_reference_comparisons,
)

pytestmark = pytest.mark.skipif(
    os.environ.get("CHEMWORLD_RUN_REFERENCE_TESTS") != "1",
    reason="Set CHEMWORLD_RUN_REFERENCE_TESTS=1 to run optional reference-backend checks.",
)


def _reference_module(module_name: str, repo_names: tuple[str, ...] | None = None):
    try:
        return import_reference_module(module_name, repo_names=repo_names)
    except Exception as exc:
        pytest.skip(f"optional reference module {module_name!r} is unavailable: {exc}")


def test_chemicals_ideal_gas_molar_volume_reference() -> None:
    chemicals_volume = _reference_module("chemicals.volume")

    temperature_K = 298.15
    pressure_Pa = 101325.0
    chemworld_value = ideal_gas_molar_volume(temperature_K, pressure_Pa)
    reference_value = chemicals_volume.ideal_gas(temperature_K, pressure_Pa)

    comparison = compare_scalar(
        check_id="chemicals-ideal-gas-molar-volume",
        backend_id="chemicals",
        quantity="ideal_gas_molar_volume",
        chemworld_value=chemworld_value,
        reference_value=reference_value,
        unit="m^3/mol",
        rtol=1e-12,
        note="Formula-level ideal-gas check against chemicals.volume.ideal_gas.",
    )
    assert comparison.passed, comparison.to_dict()


def test_fluids_dimensionless_number_reference() -> None:
    fluids_core = _reference_module("fluids.core")

    density_kg_m3 = 998.0
    velocity_m_s = 2.0
    diameter_m = 0.05
    viscosity_Pa_s = 0.001
    cp_J_kg_K = 4182.0
    thermal_conductivity_W_m_K = 0.6

    comparisons = (
        compare_scalar(
            check_id="fluids-reynolds",
            backend_id="fluids",
            quantity="Re",
            chemworld_value=reynolds_number(
                density_kg_m3=density_kg_m3,
                velocity_m_s=velocity_m_s,
                diameter_m=diameter_m,
                viscosity_Pa_s=viscosity_Pa_s,
            ),
            reference_value=fluids_core.Reynolds(
                V=velocity_m_s,
                D=diameter_m,
                rho=density_kg_m3,
                mu=viscosity_Pa_s,
            ),
            unit="dimensionless",
            rtol=1e-12,
        ),
        compare_scalar(
            check_id="fluids-prandtl",
            backend_id="fluids",
            quantity="Pr",
            chemworld_value=prandtl_number(
                heat_capacity_J_kg_K=cp_J_kg_K,
                viscosity_Pa_s=viscosity_Pa_s,
                thermal_conductivity_W_m_K=thermal_conductivity_W_m_K,
            ),
            reference_value=fluids_core.Prandtl(
                Cp=cp_J_kg_K,
                k=thermal_conductivity_W_m_K,
                mu=viscosity_Pa_s,
            ),
            unit="dimensionless",
            rtol=1e-12,
        ),
    )
    summary = summarize_reference_comparisons(comparisons)
    assert summary["all_passed"], summary


def test_fluids_friction_factor_and_pressure_drop_reference() -> None:
    fluids_friction = _reference_module("fluids.friction")

    reynolds = 100_000.0
    relative_roughness = 1e-4
    density_kg_m3 = 998.0
    viscosity_Pa_s = 0.001
    diameter_m = 0.05
    roughness_m = relative_roughness * diameter_m
    length_m = 3.0
    volumetric_flow_m3_s = 3.5e-3
    mass_flow_kg_s = density_kg_m3 * volumetric_flow_m3_s

    chemworld_flow = pipe_pressure_drop(
        PipeSpec(length_m=length_m, diameter_m=diameter_m, roughness_m=roughness_m),
        FluidState(density_kg_m3=density_kg_m3, viscosity_Pa_s=viscosity_Pa_s),
        volumetric_flow_m3_s=volumetric_flow_m3_s,
        friction_method="haaland",
        strict_friction_validity=True,
    )

    comparisons = (
        compare_scalar(
            check_id="fluids-haaland-friction-factor",
            backend_id="fluids",
            quantity="darcy_friction_factor",
            chemworld_value=darcy_friction_factor(
                reynolds=reynolds,
                relative_roughness=relative_roughness,
                method="haaland",
                strict_validity=True,
            ),
            reference_value=fluids_friction.Haaland(reynolds, relative_roughness),
            unit="dimensionless",
            rtol=1e-12,
            note="Explicit Haaland branch against fluids.friction.Haaland.",
        ),
        compare_scalar(
            check_id="fluids-one-phase-pressure-drop",
            backend_id="fluids",
            quantity="single_phase_pressure_drop",
            chemworld_value=chemworld_flow.pressure_drop_friction_Pa,
            reference_value=fluids_friction.one_phase_dP(
                m=mass_flow_kg_s,
                rho=density_kg_m3,
                mu=viscosity_Pa_s,
                D=diameter_m,
                roughness=roughness_m,
                L=length_m,
                Method="Haaland",
            ),
            unit="Pa",
            rtol=1e-12,
            note=(
                "Darcy-Weisbach frictional pressure drop against "
                "fluids.friction.one_phase_dP with Method='Haaland'."
            ),
        ),
    )
    summary = summarize_reference_comparisons(comparisons)
    assert summary["all_passed"], summary


def test_chemicals_rachford_rice_flash_reference() -> None:
    chemicals_rr = _reference_module("chemicals.rachford_rice")

    component_ids = ("light", "heavy")
    z_values = (0.5, 0.5)
    k_values = (2.0, 0.5)
    chemworld = flash_isothermal(
        dict(zip(component_ids, z_values, strict=True)),
        dict(zip(component_ids, k_values, strict=True)),
    )
    beta, x_values, y_values = chemicals_rr.Rachford_Rice_solution(
        zs=list(z_values),
        Ks=list(k_values),
    )

    comparisons = [
        compare_scalar(
            check_id="chemicals-rr-beta",
            backend_id="chemicals",
            quantity="vapor_fraction",
            chemworld_value=chemworld.vapor_fraction,
            reference_value=beta,
            unit="dimensionless",
            rtol=1e-12,
        )
    ]
    for component_id, reference_x, reference_y in zip(
        component_ids,
        x_values,
        y_values,
        strict=True,
    ):
        comparisons.append(
            compare_scalar(
                check_id=f"chemicals-rr-x-{component_id}",
                backend_id="chemicals",
                quantity=f"x_{component_id}",
                chemworld_value=chemworld.liquid_composition[component_id],
                reference_value=reference_x,
                unit="mole_fraction",
                rtol=1e-12,
            )
        )
        comparisons.append(
            compare_scalar(
                check_id=f"chemicals-rr-y-{component_id}",
                backend_id="chemicals",
                quantity=f"y_{component_id}",
                chemworld_value=chemworld.vapor_composition[component_id],
                reference_value=reference_y,
                unit="mole_fraction",
                rtol=1e-12,
            )
        )

    summary = summarize_reference_comparisons(comparisons)
    assert summary["all_passed"], summary


def test_chemicals_curated_vapor_pressure_and_enthalpy_references() -> None:
    chemicals_dippr = _reference_module("chemicals.dippr")
    chemicals_heat_capacity = _reference_module("chemicals.heat_capacity")
    chemicals_vapor_pressure = _reference_module("chemicals.vapor_pressure")
    fluids_constants = _reference_module("fluids.constants", repo_names=("fluids",))

    comparisons = []
    for case in curated_property_cases():
        package = curated_property_package(case.component_id)
        vapor_pressure = package.evaluate(
            "vapor_pressure",
            temperature_K=case.reference_temperature_K,
            validity_policy="raise",
        )
        cp_correlation = package.by_property("ideal_gas_heat_capacity")[0]
        heat_capacity = package.evaluate(
            "ideal_gas_heat_capacity",
            temperature_K=case.reference_temperature_K,
            validity_policy="raise",
        )
        enthalpy = sensible_enthalpy_change(
            cp_correlation,
            initial_temperature_K=case.enthalpy_initial_temperature_K,
            final_temperature_K=case.enthalpy_final_temperature_K,
            validity_policy="raise",
        )

        psat_row = chemicals_vapor_pressure.Psat_data_Perrys2_8.loc[case.casrn]
        cp_row = chemicals_heat_capacity.Cp_data_Poling.loc[case.casrn]
        r = fluids_constants.R
        reference_cp_coefficients = {
            "A": r * float(cp_row["a0"]),
            "B": r * float(cp_row["a1"]),
            "C": r * float(cp_row["a2"]),
            "D": r * float(cp_row["a3"]),
            "E": r * float(cp_row["a4"]),
        }

        comparisons.append(
            compare_scalar(
                check_id=f"chemicals-curated-psat-{case.component_id}",
                backend_id="chemicals",
                quantity="vapor_pressure",
                chemworld_value=vapor_pressure.value,
                reference_value=chemicals_dippr.EQ101(
                    case.reference_temperature_K,
                    float(psat_row["C1"]),
                    float(psat_row["C2"]),
                    float(psat_row["C3"]),
                    float(psat_row["C4"]),
                    float(psat_row["C5"]),
                ),
                unit="Pa",
                rtol=1e-12,
                note="Curated DIPPR101/Perry vapor-pressure record.",
            )
        )
        comparisons.append(
            compare_scalar(
                check_id=f"chemicals-curated-cpig-{case.component_id}",
                backend_id="chemicals",
                quantity="ideal_gas_heat_capacity",
                chemworld_value=heat_capacity.value,
                reference_value=chemicals_dippr.EQ100(
                    case.reference_temperature_K,
                    **reference_cp_coefficients,
                ),
                unit="J/(mol*K)",
                rtol=1e-12,
                note="Curated R-scaled Poling ideal-gas Cp record.",
            )
        )
        comparisons.append(
            compare_scalar(
                check_id=f"chemicals-curated-enthalpy-{case.component_id}",
                backend_id="chemicals",
                quantity="ideal_gas_sensible_enthalpy",
                chemworld_value=enthalpy.value,
                reference_value=(
                    chemicals_dippr.EQ100(
                        case.enthalpy_final_temperature_K,
                        order=-1,
                        **reference_cp_coefficients,
                    )
                    - chemicals_dippr.EQ100(
                        case.enthalpy_initial_temperature_K,
                        order=-1,
                        **reference_cp_coefficients,
                    )
                ),
                unit="J/mol",
                rtol=1e-12,
                note="Analytic sensible-enthalpy integral for curated Poling Cp.",
            )
        )

    summary = summarize_reference_comparisons(tuple(comparisons))
    assert summary["all_passed"], summary


def test_thermo_ideal_vle_reference() -> None:
    thermo_property_package = _reference_module(
        "thermo.property_package",
        repo_names=("fluids", "chemicals", "thermo"),
    )

    class ConstantVaporPressure:
        def __init__(self, value: float) -> None:
            self.value = value

        def __call__(self, temperature: float) -> float:
            if temperature <= 0:
                raise ValueError("temperature must be positive")
            return self.value

    component_ids = ("ethanol", "water")
    temperature_K = 298.15
    pressure_Pa = 5000.0
    composition = {"ethanol": 0.5, "water": 0.5}
    vapor_pressures_Pa = {"ethanol": 7860.0, "water": 3168.0}
    activity_model = ActivityModelSpec(
        "ideal_ethanol_water",
        component_ids,
        "ideal",
    )
    ideal_package = thermo_property_package.Ideal(
        [
            ConstantVaporPressure(vapor_pressures_Pa["ethanol"]),
            ConstantVaporPressure(vapor_pressures_Pa["water"]),
        ],
        [159.0, 273.15],
        [514.0, 647.0],
        [6.1e6, 22.1e6],
    )
    phase, reference_xs, reference_ys, reference_vapor_fraction = (
        ideal_package.flash_TP_zs(
            temperature_K,
            pressure_Pa,
            [composition[component_id] for component_id in component_ids],
        )
    )
    chemworld_k_values = raoult_k_values(
        activity_model,
        composition,
        vapor_pressures_Pa=vapor_pressures_Pa,
        pressure_Pa=pressure_Pa,
        temperature_K=temperature_K,
    )
    chemworld_flash = flash_isothermal(composition, chemworld_k_values)

    comparisons = [
        compare_scalar(
            check_id="thermo-ideal-bubble-pressure",
            backend_id="thermo",
            quantity="bubble_pressure",
            chemworld_value=bubble_pressure_pa(
                composition,
                vapor_pressures_Pa=vapor_pressures_Pa,
                activity_model=activity_model,
                temperature_K=temperature_K,
            ),
            reference_value=ideal_package.Pbubble(
                temperature_K,
                [composition[component_id] for component_id in component_ids],
            ),
            unit="Pa",
            rtol=1e-12,
            note="Ideal Raoult-law bubble pressure against thermo.property_package.Ideal.",
        ),
        compare_scalar(
            check_id="thermo-ideal-dew-pressure",
            backend_id="thermo",
            quantity="dew_pressure",
            chemworld_value=dew_pressure_pa(
                composition,
                vapor_pressures_Pa=vapor_pressures_Pa,
                activity_model=activity_model,
                temperature_K=temperature_K,
            ),
            reference_value=ideal_package.Pdew(
                temperature_K,
                [composition[component_id] for component_id in component_ids],
            ),
            unit="Pa",
            rtol=1e-12,
            note="Ideal Raoult-law dew pressure against thermo.property_package.Ideal.",
        ),
        compare_scalar(
            check_id="thermo-ideal-flash-vapor-fraction",
            backend_id="thermo",
            quantity="vapor_fraction",
            chemworld_value=chemworld_flash.vapor_fraction,
            reference_value=reference_vapor_fraction,
            unit="dimensionless",
            rtol=1e-11,
            note=(
                "Thermo phase label: "
                f"{phase}; tolerance allows bisection vs thermo flash-solver roundoff."
            ),
        ),
    ]
    for component_id, reference_x, reference_y in zip(
        component_ids,
        reference_xs,
        reference_ys,
        strict=True,
    ):
        comparisons.append(
            compare_scalar(
                check_id=f"thermo-ideal-flash-x-{component_id}",
                backend_id="thermo",
                quantity=f"x_{component_id}",
                chemworld_value=chemworld_flash.liquid_composition[component_id],
                reference_value=reference_x,
                unit="mole_fraction",
                rtol=1e-11,
            )
        )
        comparisons.append(
            compare_scalar(
                check_id=f"thermo-ideal-flash-y-{component_id}",
                backend_id="thermo",
                quantity=f"y_{component_id}",
                chemworld_value=chemworld_flash.vapor_composition[component_id],
                reference_value=reference_y,
                unit="mole_fraction",
                rtol=1e-11,
            )
        )

    summary = summarize_reference_comparisons(comparisons)
    assert summary["all_passed"], summary
