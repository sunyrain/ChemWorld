from __future__ import annotations

import json
from pathlib import Path

import chemworld.eval.work_ii_release as release
from chemworld.eval.work_ii_release import (
    PREREGISTRATION_FREEZE_RECEIPT_VERSION,
    WORK_II_RELEASE_TEST_FILES,
    clean_release_receipt_sha256,
    preregistration_freeze_receipt_sha256,
    validate_clean_release_receipt,
    validate_preregistration_freeze_receipt,
)

ROOT = Path(__file__).resolve().parents[1]


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
        tmp_path / "missing-qualification.json",
        currency_ceiling_usd=1.0,
    )
    assert (
        "Work II preregistration-freeze receipt crossed its outcome boundary" in errors
    )
