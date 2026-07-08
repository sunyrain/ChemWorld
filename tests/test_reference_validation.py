from __future__ import annotations

import pytest

from chemworld.physchem import (
    compare_scalar,
    reference_backend_specs,
    reference_backend_status,
    summarize_reference_comparisons,
)


def test_reference_backend_specs_are_json_friendly() -> None:
    specs = reference_backend_specs()
    payloads = [spec.to_dict() for spec in specs]

    assert {spec.backend_id for spec in specs} >= {
        "chemicals",
        "fluids",
        "thermo",
        "coolprop",
        "cantera",
        "phasepy",
        "reaktoro",
        "pycalphad",
    }
    assert payloads[0]["local_repo_names"]
    assert all(payload["comparison_scope"] for payload in payloads)


def test_reference_backend_status_does_not_require_optional_imports() -> None:
    statuses = reference_backend_status(probe_import=False)

    assert statuses
    assert all(not status.import_probe_attempted for status in statuses)
    assert all(status.import_available is None for status in statuses)
    assert all(isinstance(status.to_dict()["local_repo_available"], bool) for status in statuses)


def test_compare_scalar_and_summary_record_failures_explicitly() -> None:
    passing = compare_scalar(
        check_id="ideal-gas-volume",
        backend_id="chemicals",
        quantity="molar_volume",
        chemworld_value=1.001,
        reference_value=1.0,
        unit="m^3/mol",
        rtol=0.01,
    )
    failing = compare_scalar(
        check_id="bad-volume",
        backend_id="chemicals",
        quantity="molar_volume",
        chemworld_value=1.2,
        reference_value=1.0,
        unit="m^3/mol",
        rtol=0.01,
        note="intentional failure to prove reporting behavior",
    )
    summary = summarize_reference_comparisons((passing, failing))

    assert passing.passed
    assert passing.abs_error == passing.to_dict()["abs_error"]
    assert not failing.passed
    assert failing.rel_error == pytest.approx(0.2)
    assert summary["total"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["all_passed"] is False
