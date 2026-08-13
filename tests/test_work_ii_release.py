from __future__ import annotations

import json
import shutil
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_release as release
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_release import (
    PREREGISTRATION_FREEZE_RECEIPT_VERSION,
    WORK_II_RELEASE_TEST_FILES,
    clean_release_receipt_sha256,
    preregistration_freeze_receipt_sha256,
    validate_clean_release_receipt,
    validate_preregistration_freeze_receipt,
)

ROOT = Path(__file__).resolve().parents[1]


def _formal_manifest() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-formal-matrix-runner-preflight-v0.1.json"
        ).read_text(encoding="utf-8")
    )


def _qualification_bridge_manifest(
    formal: dict[str, object],
) -> dict[str, object]:
    local = {
        field: deepcopy(formal[field])
        for field in (
            "provider_contract",
            "provider_attempt_contract",
            "participant_execution_contract",
            "method_qualification_contract",
        )
    }
    local["manifest_sha256"] = canonical_json_sha256(local)
    return local


def _clean_release_receipt() -> dict[str, object]:
    receipt: dict[str, object] = {
        "schema_version": "chemworld-work-ii-clean-release-receipt-0.1",
        "status": "passed",
        "formal_result": False,
        "formal_execution_allowed": False,
        "provider_calls_executed": 0,
        "formal_participant_outcome_count": 0,
        "tested_commit": "a" * 40,
        "independent_checkout": {
            "mode": "git_clone_no_local",
            "path_recorded": False,
            "clean_before": True,
            "clean_after": True,
        },
        "work_ii_tests": {
            "status": "passed",
            "test_files": list(WORK_II_RELEASE_TEST_FILES),
            "passed": 1,
            "skipped": 0,
            "failed": 0,
            "stdout_sha256": "b" * 64,
            "stderr_sha256": "c" * 64,
        },
        "wheel": {
            "status": "passed",
            "sha256": "d" * 64,
            "bytes": 1,
            "installed_import_smoke": True,
        },
        "failures": [],
    }
    receipt["receipt_sha256"] = clean_release_receipt_sha256(receipt)
    return receipt


def test_clean_release_receipt_validator_rejects_shallow_pass() -> None:
    assert validate_clean_release_receipt({"status": "passed"})


def test_clean_release_roster_freezes_new_execution_and_q0_tests() -> None:
    assert {
        "tests/test_work_ii_ae_formal_cohort.py",
        "tests/test_work_ii_ae_prior_qualification_v02.py",
        "tests/test_work_ii_formal_evaluators.py",
        "tests/test_work_ii_private_execution.py",
        "tests/test_work_ii_public_c2.py",
        "tests/test_work_ii_catalyst_deactivation_q0.py",
        "tests/test_work_ii_c2_admission.py",
        "tests/test_work_ii_c2_task_admission.py",
        "tests/test_work_ii_constitutive_structural_qualification.py",
        "tests/test_work_ii_crystallization_reversible_q0.py",
        "tests/test_work_ii_distillation_additional_rollback_q0.py",
        "tests/test_work_ii_partition_constitutive_q0.py",
        "tests/test_work_ii_static_topology_q0.py",
    }.issubset(WORK_II_RELEASE_TEST_FILES)


def test_clean_release_validator_rejects_test_roster_drift() -> None:
    receipt = _clean_release_receipt()
    receipt["work_ii_tests"]["test_files"] = list(WORK_II_RELEASE_TEST_FILES[:-1])
    receipt["work_ii_tests"]["passed"] = 1
    receipt["receipt_sha256"] = release.clean_release_receipt_sha256(receipt)
    assert "Work II clean-release receipt lacks the exact release test result" in (
        validate_clean_release_receipt(receipt)
    )


def test_clean_release_receipt_is_not_current_for_a_dirty_repository(
    monkeypatch,
) -> None:
    receipt = _clean_release_receipt()
    monkeypatch.setattr(release, "git_worktree_dirty", lambda _root: True)
    monkeypatch.setattr(release, "git_source_commit", lambda _root: "b" * 40)
    monkeypatch.setattr(
        release,
        "_material_tree_changed_since",
        lambda _root, _commit: (True, None),
    )
    monkeypatch.setattr(
        release.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0, "stderr": b""},
        )(),
    )
    errors = validate_clean_release_receipt(receipt, root=ROOT)
    assert "current Work II release worktree is dirty" in errors
    assert (
        "current Work II implementation differs from the clean-release tested commit"
        in errors
    )


@pytest.mark.parametrize(
    ("contract_field", "nested_path", "changed_value", "expected_error"),
    [
        (
            "provider_contract",
            ("model",),
            "different-model",
            "method qualification provider contract differs from formal manifest",
        ),
        (
            "provider_attempt_contract",
            ("maximum_total_provider_attempts_per_cell",),
            3,
            "method qualification provider-attempt contract differs from formal manifest",
        ),
        (
            "participant_execution_contract",
            ("sampling_contract", "reasoning_effort"),
            "high",
            "method qualification participant method contract differs from formal manifest",
        ),
        (
            "method_qualification_contract",
            ("complete_experiments_per_cell",),
            7,
            "method qualification qualification gate contract differs from formal manifest",
        ),
    ],
)
def test_method_qualification_bridge_rejects_rehashed_contract_drift(
    contract_field: str,
    nested_path: tuple[str, ...],
    changed_value: object,
    expected_error: str,
) -> None:
    formal = _formal_manifest()
    local = _qualification_bridge_manifest(formal)
    assert release._validate_method_qualification_formal_bridge(formal, local) == []

    target = local[contract_field]
    for key in nested_path[:-1]:
        target = target[key]
    target[nested_path[-1]] = changed_value
    local["manifest_sha256"] = canonical_json_sha256(
        {key: value for key, value in local.items() if key != "manifest_sha256"}
    )

    errors = release._validate_method_qualification_formal_bridge(formal, local)
    assert expected_error in errors


def test_method_qualification_bridge_ignores_formal_matrix_attempt_totals() -> None:
    formal = _formal_manifest()
    local = _qualification_bridge_manifest(formal)
    attempt = local["provider_attempt_contract"]
    attempt["public_matrix_initial_attempt_count"] = 3
    attempt["public_matrix_provider_attempt_hard_cap"] = 6
    assert release._validate_method_qualification_formal_bridge(formal, local) == []


def test_preregistration_freeze_receipt_validator_rejects_shallow_pass(
    tmp_path: Path,
) -> None:
    manifest = json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-formal-matrix-runner-preflight-v0.1.json"
        ).read_text(encoding="utf-8")
    )
    errors = validate_preregistration_freeze_receipt(
        ROOT,
        {"status": "passed_final_freeze"},
        manifest,
        {},
        tmp_path / "missing-qualification-manifest.json",
        {},
        tmp_path / "missing-qualification.json",
        currency_ceiling_usd=1.0,
    )
    assert errors


def test_preregistration_freeze_forbids_prior_formal_outcomes_even_if_rehashed(
    tmp_path: Path,
) -> None:
    manifest = json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-formal-matrix-runner-preflight-v0.1.json"
        ).read_text(encoding="utf-8")
    )
    receipt: dict[str, object] = {
        "schema_version": PREREGISTRATION_FREEZE_RECEIPT_VERSION,
        "status": "passed_final_freeze",
        "formal_result": False,
        "formal_participant_outcome_count": 1,
        "formal_execution_authorized": True,
    }
    receipt["receipt_sha256"] = preregistration_freeze_receipt_sha256(receipt)
    errors = validate_preregistration_freeze_receipt(
        ROOT,
        receipt,
        manifest,
        {},
        tmp_path / "missing-qualification-manifest.json",
        {},
        tmp_path / "missing-qualification.json",
        currency_ceiling_usd=1.0,
    )
    assert (
        "Work II preregistration-freeze receipt crossed its outcome boundary" in errors
    )


def test_preregistration_freeze_rejects_in_memory_qualification_substitution(
) -> None:
    manifest = json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-formal-matrix-runner-preflight-v0.1.json"
        ).read_text(encoding="utf-8")
    )
    package = Path(tempfile.mkdtemp(prefix=".pytest-release-package-", dir=ROOT))
    try:
        local_manifest_path = package / "qualification-manifest.json"
        local_manifest_path.write_text("{}", encoding="utf-8")
        qualification_path = package / "qualification.json"
        qualification_path.write_text("{}", encoding="utf-8")

        errors = validate_preregistration_freeze_receipt(
            ROOT,
            {"status": "passed_final_freeze"},
            manifest,
            {"manifest_sha256": "a" * 64},
            local_manifest_path,
            {"receipt_sha256": "b" * 64},
            qualification_path,
            currency_ceiling_usd=1.0,
        )
    finally:
        shutil.rmtree(package)

    assert (
        "method-qualification local manifest argument differs from its file" in errors
    )
    assert "method-qualification receipt argument differs from its file" in errors


def test_preregistration_freeze_consumer_rejects_cross_provider_qualification(
) -> None:
    formal = _formal_manifest()
    local = _qualification_bridge_manifest(formal)
    local["provider_contract"]["model"] = "different-model"
    local["manifest_sha256"] = canonical_json_sha256(
        {key: value for key, value in local.items() if key != "manifest_sha256"}
    )
    qualification = {"receipt_sha256": "b" * 64}
    package = Path(tempfile.mkdtemp(prefix=".pytest-release-package-", dir=ROOT))
    try:
        local_path = package / "qualification-manifest.json"
        local_path.write_text(json.dumps(local), encoding="utf-8")
        receipt_path = package / "qualification.json"
        receipt_path.write_text(json.dumps(qualification), encoding="utf-8")
        errors = validate_preregistration_freeze_receipt(
            ROOT,
            {"status": "passed_final_freeze"},
            formal,
            local,
            local_path,
            qualification,
            receipt_path,
            currency_ceiling_usd=1.0,
        )
    finally:
        shutil.rmtree(package)

    assert (
        "method qualification provider contract differs from formal manifest"
        in errors
    )
