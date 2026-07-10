from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from chemworld.runtime.maturity_audit import (
    MATURITY_AUDIT_SCHEMA_VERSION,
    build_maturity_audit,
    validate_maturity_audit_report,
    write_maturity_audit_report,
)
from chemworld.tasks import list_tasks


def test_full_report_covers_all_fifteen_tasks_and_actual_dependencies() -> None:
    root = Path(__file__).parents[1]
    report = build_maturity_audit(repository_root=root)

    assert report["schema_version"] == MATURITY_AUDIT_SCHEMA_VERSION
    assert report["task_count"] == 15
    assert {item["task_id"] for item in report["tasks"]} == {task.task_id for task in list_tasks()}
    assert report["contract_integrity_passed"]
    assert report["declaration_alignment_status"] == "gaps_detected"
    assert report["declaration_gap_count"] == 9
    assert validate_maturity_audit_report(report, repository_root=root) == []


def test_each_task_report_contains_hashes_routes_maturity_and_evidence() -> None:
    root = Path(__file__).parents[1]
    report = build_maturity_audit(repository_root=root)

    for item in report["tasks"]:
        assert len(item["task_contract_hash"]) == 64
        assert len(item["runtime_profile_hash"]) == 64
        assert item["actual_dependencies"]["operations"]
        assert item["actual_dependencies"]["domain_services"]
        assert item["actual_dependencies"]["kernels"]
        assert item["actual_model_ids"] == sorted(item["actual_model_ids"])
        assert item["minimum_actual_maturity"]
        assert item["evidence_paths"]
        assert all((root / path).is_file() for path in item["evidence_paths"])


def test_role_audit_separates_runtime_diagnostic_and_reference_models() -> None:
    root = Path(__file__).parents[1]
    report = build_maturity_audit(repository_root=root)

    assert report["role_boundary_passed"]
    assert set(report["provider_role_catalog"].values()) >= {
        "runtime",
        "runtime_fallback",
        "diagnostic",
        "reference",
    }
    for item in report["tasks"]:
        actual_roles = item["actual_provider_roles"]
        assert item["actual_role_partition"]["reference"] == []
        assert set(actual_roles) == set(item["actual_model_ids"])
        assert all(
            item["declared_provider_roles"][model_id] for model_id in item["declared_model_ids"]
        )
    equilibrium = next(
        item for item in report["tasks"] if item["task_id"] == "equilibrium-characterization"
    )
    assert equilibrium["declared_provider_roles"]["fixed_tp_ideal_gibbs_minimization"] == (
        "reference"
    )
    assert "fixed_tp_ideal_gibbs_minimization" not in equilibrium["actual_model_ids"]


def test_report_is_deterministic_and_fixed_json_round_trips(tmp_path: Path) -> None:
    root = Path(__file__).parents[1]
    first = build_maturity_audit(repository_root=root)
    second = build_maturity_audit(repository_root=root)
    assert first == second

    output = tmp_path / "maturity-audit.json"
    written = write_maturity_audit_report(output, repository_root=root)
    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded == written
    assert validate_maturity_audit_report(loaded, repository_root=root) == []


@pytest.mark.parametrize(
    "mutation, expected",
    [
        (lambda report: report["tasks"].pop(), "task coverage mismatch"),
        (
            lambda report: report["tasks"][0].__setitem__("task_contract_hash", "bad"),
            "task contract hash mismatch",
        ),
        (
            lambda report: report["tasks"][0]["evidence_paths"].append("missing.py"),
            "missing evidence path",
        ),
        (
            lambda report: report.__setitem__("report_hash", "bad"),
            "report_hash mismatch",
        ),
    ],
)
def test_report_validator_rejects_tampering(mutation, expected: str) -> None:
    root = Path(__file__).parents[1]
    report = copy.deepcopy(build_maturity_audit(repository_root=root))
    mutation(report)

    errors = validate_maturity_audit_report(report, repository_root=root)
    assert any(expected in error for error in errors)


def test_missing_task_is_not_accepted_as_a_complete_report() -> None:
    root = Path(__file__).parents[1]
    report = build_maturity_audit(repository_root=root, task_ids=("reaction-to-assay",))

    errors = validate_maturity_audit_report(report, repository_root=root)
    assert any("task coverage mismatch" in error for error in errors)
