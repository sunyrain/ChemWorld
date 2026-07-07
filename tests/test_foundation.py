from __future__ import annotations

from chemworld.core.batch_reactor import (
    batch_reactor_instruments,
    initial_batch_reactor_state,
    make_batch_reactor_constitution,
)
from chemworld.foundation import Quantity, convert_value


def test_unit_conversion_table() -> None:
    assert convert_value(1.0, "h", "s") == 3600.0
    assert convert_value(25.0, "degC", "K") == 298.15
    assert Quantity(1000.0, "mL").to("L").value == 1.0


def test_constitution_initial_state_passes() -> None:
    constitution = make_batch_reactor_constitution()
    report = constitution.check_state(initial_batch_reactor_state())
    assert report.passed


def test_constitution_rejects_negative_amount() -> None:
    constitution = make_batch_reactor_constitution()
    state = initial_batch_reactor_state().replace(species_amounts={"A": -1.0})
    report = constitution.check_state(state)
    assert not report.passed
    assert any(check.name.startswith("nonnegative") for check in report.failures())


def test_final_assay_requires_termination() -> None:
    constitution = make_batch_reactor_constitution()
    state = initial_batch_reactor_state().replace(volume_L=0.02)
    preconditions = constitution.check_preconditions(
        "measure",
        state,
        {"instrument": "final_assay"},
    )
    assert not preconditions["measure_final_requires_terminated"]
    assert batch_reactor_instruments()["final_assay"].requires_terminated

