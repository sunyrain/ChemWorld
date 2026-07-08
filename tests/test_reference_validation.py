from __future__ import annotations

import pytest

from chemworld.physchem import (
    ReferenceBackendStatus,
    compare_scalar,
    reference_backend_specs,
    reference_backend_status,
    reference_tolerance_profiles,
    reference_validation_report,
    skipped_reference_backends,
    summarize_reference_comparisons,
    write_reference_validation_report,
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
    assert all("installed_version" in status.to_dict() for status in statuses)


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


def test_reference_validation_report_records_skipped_backends(tmp_path) -> None:
    unavailable = ReferenceBackendStatus(
        backend_id="coolprop",
        package_name="CoolProp",
        installed_available=False,
        local_repo_available=False,
        import_probe_attempted=False,
        import_available=None,
    )
    import_failed = ReferenceBackendStatus(
        backend_id="cantera",
        package_name="cantera",
        installed_available=True,
        local_repo_available=False,
        import_probe_attempted=True,
        import_available=False,
        import_error="ImportError: missing compiled extension",
    )
    import_ok = ReferenceBackendStatus(
        backend_id="chemicals",
        package_name="chemicals",
        installed_available=True,
        local_repo_available=False,
        import_probe_attempted=True,
        import_available=True,
        source="site-packages/chemicals/__init__.py",
    )

    skipped = skipped_reference_backends((unavailable, import_failed, import_ok))
    assert {item["backend_id"] for item in skipped} == {"coolprop", "cantera"}
    assert all(item["reason"] for item in skipped)

    comparison = compare_scalar(
        check_id="unit-check",
        backend_id="chemicals",
        quantity="pressure",
        chemworld_value=101325.0,
        reference_value=101325.0,
        unit="Pa",
        rtol=1e-12,
    )
    report = reference_validation_report((comparison,), reference_root=tmp_path)
    payload = report.to_dict()
    assert payload["schema_version"] == "chemworld-reference-validation-report-0.1"
    assert payload["comparison_summary"]["all_passed"] is True
    assert "backend_statuses" in payload
    assert payload["tolerance_profiles"]
    assert {profile["backend_id"] for profile in payload["tolerance_profiles"]} >= {
        "chemicals",
        "fluids",
        "thermo",
    }

    output = tmp_path / "reference_validation_report.json"
    written = write_reference_validation_report(output, (comparison,), reference_root=tmp_path)
    assert output.exists()
    assert written.to_dict()["comparison_summary"]["total"] == 1


def test_reference_tolerance_profiles_are_json_friendly() -> None:
    profiles = reference_tolerance_profiles()
    assert profiles
    assert all(profile.rtol >= 0.0 and profile.atol >= 0.0 for profile in profiles)
    assert all(profile.to_dict()["profile_id"] for profile in profiles)
