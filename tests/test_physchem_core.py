from __future__ import annotations

import pytest

from chemworld.foundation import convert_value
from chemworld.physchem import (
    ComponentSpec,
    MixtureSpec,
    PropertyCorrelation,
    element_matrix,
    hill_formula,
    mass_fractions_from_mole_fractions,
    mole_fractions_from_mass_fractions,
    molecular_weight,
    parse_formula,
)


def test_formula_parser_and_element_matrix() -> None:
    water = parse_formula("H2O")
    ethanol = parse_formula("C2H6O")
    carbon_dioxide = parse_formula("CO2")
    calcium_hydroxide = parse_formula("Ca(OH)2")

    assert water == {"H": 2.0, "O": 1.0}
    assert ethanol == {"C": 2.0, "H": 6.0, "O": 1.0}
    assert carbon_dioxide == {"C": 1.0, "O": 2.0}
    assert calcium_hydroxide == {"Ca": 1.0, "O": 2.0, "H": 2.0}
    assert hill_formula(ethanol) == "C2H6O"

    matrix, elements = element_matrix([water, ethanol, carbon_dioxide])
    assert elements == ("H", "C", "O")
    assert matrix == ((2.0, 0.0, 1.0), (6.0, 2.0, 1.0), (0.0, 1.0, 2.0))


def test_component_spec_is_json_friendly_and_validated() -> None:
    component = ComponentSpec(
        identifier="ethanol",
        formula="C2H6O",
        default_phase="liquid",
        safety_tags=("flammable", "volatile"),
        allowed_property_correlations=("antoine", "liquid_density"),
    )

    payload = component.to_dict()
    assert payload["identifier"] == "ethanol"
    assert payload["composition"] == {"C": 2.0, "H": 6.0, "O": 1.0}
    assert payload["hill_formula"] == "C2H6O"
    assert payload["units"] == {"molecular_weight_g_mol": "g/mol"}
    assert component.molecular_weight_g_mol == pytest.approx(46.069)

    with pytest.raises(ValueError, match="Unknown element"):
        ComponentSpec(identifier="bad", formula="Xx2")
    with pytest.raises(ValueError, match="Unsupported default phase"):
        ComponentSpec(identifier="bad_phase", formula="H2O", default_phase="plasma")


def test_mole_and_mass_fraction_conversions_are_reversible() -> None:
    water = ComponentSpec(identifier="water", formula="H2O", default_phase="liquid")
    ethanol = ComponentSpec(identifier="ethanol", formula="C2H6O", default_phase="liquid")
    components = (water, ethanol)

    zs = (0.25, 0.75)
    ws = mass_fractions_from_mole_fractions(components, zs)
    recovered_zs = mole_fractions_from_mass_fractions(components, ws)

    assert sum(ws) == pytest.approx(1.0)
    assert recovered_zs == pytest.approx(zs)

    mixture = MixtureSpec.from_mole_fractions(
        components,
        zs,
        phase_label="liquid",
        temperature_K=298.15,
        pressure_Pa=101325.0,
    )
    assert mixture.mass_fractions == pytest.approx(ws)
    assert mixture.average_molecular_weight_g_mol == pytest.approx(
        0.25 * molecular_weight(water.composition)
        + 0.75 * molecular_weight(ethanol.composition)
    )
    assert mixture.to_dict()["units"]["pressure_Pa"] == "Pa"


def test_property_correlation_units_fail_before_kernel_use() -> None:
    correlation = PropertyCorrelation(
        correlation_id="water_cp_poly",
        equation_id="cp_polynomial",
        coefficients={"a": 75.3, "b": 0.0},
        input_units={"temperature": "K"},
        output_unit="J/mol",
        validity_ranges={"temperature": (273.15, 373.15)},
        source_note="benchmark placeholder correlation",
    )
    assert correlation.to_dict()["output_unit"] == "J/mol"

    with pytest.raises(ValueError, match="Unsupported unit"):
        PropertyCorrelation(
            correlation_id="bad",
            equation_id="bad",
            coefficients={"a": 1.0},
            input_units={"temperature": "rankine"},
            output_unit="J/mol",
        )
    with pytest.raises(ValueError, match="Invalid validity range"):
        PropertyCorrelation(
            correlation_id="bad_range",
            equation_id="bad",
            coefficients={"a": 1.0},
            input_units={"temperature": "K"},
            output_unit="J/mol",
            validity_ranges={"temperature": (400.0, 300.0)},
        )


def test_extended_units_cover_physchem_dimensions() -> None:
    assert convert_value(1.0, "kW", "W") == 1000.0
    assert convert_value(1.0, "kJ/mol", "J/mol") == 1000.0
    assert convert_value(1.0, "g/mL", "kg/m^3") == 1000.0
    assert convert_value(1.0, "mPa*s", "Pa*s") == 0.001
