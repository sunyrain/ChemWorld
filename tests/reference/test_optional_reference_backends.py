from __future__ import annotations

import os

import pytest

from chemworld.physchem import (
    compare_scalar,
    flash_isothermal,
    ideal_gas_molar_volume,
    import_reference_module,
    prandtl_number,
    reynolds_number,
    summarize_reference_comparisons,
)

pytestmark = pytest.mark.skipif(
    os.environ.get("CHEMWORLD_RUN_REFERENCE_TESTS") != "1",
    reason="Set CHEMWORLD_RUN_REFERENCE_TESTS=1 to run optional reference-backend checks.",
)


def _reference_module(module_name: str):
    try:
        return import_reference_module(module_name)
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
