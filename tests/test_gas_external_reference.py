from __future__ import annotations

import json

import pytest
from scipy.integrate import quad
from scripts.validate_gas_external_reference import (
    INITIAL_TEMPERATURE_K,
    REFERENCE_PATH,
    compare,
    initial_moles,
    metrics,
    reference_heat_j,
    sealed_heating,
    shomate,
)

from chemworld.foundation.gas import GAS_R


@pytest.fixture
def reference():
    return json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize("gas", ["nitrogen", "oxygen", "argon"])
def test_enthalpy_unit_conversion_matches_independent_cp_quadrature(reference, gas):
    # Independent numerical integration catches kJ/J and Cp/Cv conversion errors.
    integrated, _ = quad(
        lambda temperature: shomate(reference, gas, temperature)[0] - GAS_R,
        INITIAL_TEMPERATURE_K,
        470.0,
        epsabs=1e-9,
    )
    assert reference_heat_j(reference, gas, 470.0) == pytest.approx(
        initial_moles() * integrated, rel=1e-12
    )
    assert reference_heat_j(reference, gas, INITIAL_TEMPERATURE_K) == 0.0
    assert initial_moles() == pytest.approx(0.000806791, rel=1e-6)


@pytest.mark.parametrize(
    ("gas", "expected_cp"), [("nitrogen", 29.124), ("oxygen", 29.383), ("argon", 20.786)]
)
def test_room_temperature_reference_scale(reference, gas, expected_cp):
    assert shomate(reference, gas, 298.15)[0] == pytest.approx(expected_cp, abs=0.001)


@pytest.mark.parametrize("gas", ["nitrogen", "oxygen", "argon"])
def test_runtime_rejects_1000k_even_with_closed_valves(reference, gas):
    assert shomate(reference, gas, 1000.0)[0] > 0
    with pytest.raises(ValueError, match="Gas advancement outside time/temperature domain"):
        sealed_heating(gas, 1000.0)


def test_reference_rejects_extrapolation(reference):
    with pytest.raises(ValueError, match="reference domain"):
        shomate(reference, "argon", 250.0)
    with pytest.raises(ValueError, match="reference domain"):
        shomate(reference, "oxygen", 2100.0)


def test_summary_keeps_prediction_and_execution_failures_distinct():
    rows = [
        compare(10.0, 10.0, "J") | {"execution_status": "complete"},
        compare(8.0, 10.0, "J") | {"execution_status": "complete"},
        {"execution_status": "error", "error": "unavailable"},
    ]
    result = metrics(rows, expected=4)
    assert (result["expected"], result["evaluated"], result["passed"]) == (4, 2, 1)
    assert (result["prediction_failed"], result["execution_failed"], result["missing"]) == (1, 1, 1)
    assert result["metric_denominator"] == 2
    assert result["mae"] == 1.0
    assert result["max_relative_error"] == 0.2
    assert metrics([], expected=2)["mae"] is None
