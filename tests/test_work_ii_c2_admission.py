from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval import work_ii_c2_admission
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_c2_admission import (
    C2_OUTCOME_BLIND_SELECTION_VERSION,
    _execution_cohort_key,
    _release_execution_context_errors,
    build_c2_admission_report,
    validate_c2_admission_report,
)

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "configs/benchmark/work_ii_c2_admission_manifest_v0.1.json"
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"


def _cells() -> list[dict[str, object]]:
    return [{"cell_id": f"ae-{index:02d}"} for index in range(75)]


def _release_context(
    *, freeze_id: str = "b" * 64, tested_commit: str = "a" * 40
) -> dict[str, object]:
    return {
        "execution_mode": "release",
        "evidence_status": "release_candidate",
        "release_eligible": True,
        "c2_admission_authorized": True,
        "tested_commit": tested_commit,
        "freeze_id": freeze_id,
        "release_manifest_sha256": "c" * 64,
        "execution_surface_sha256": "d" * 64,
    }


def _v02_resource_cards() -> list[dict[str, object]]:
    keys = (
        ("A_E", "electrochemical-conversion", 8),
        ("A_E", "reaction-to-crystallization", 8),
        ("A_E", "reaction-to-distillation", 8),
        ("A_E", "partition-discovery", 8),
        ("A_E", "reaction-safety-constrained", 8),
        ("A_P", "reaction-safety-constrained", 10),
        ("A_P", "electrochemical-conversion", 10),
        ("A_S", "partition-discovery", 12),
        ("A_S", "reaction-to-crystallization", 12),
    )
    fractions = {"A_E": 0.15, "A_P": 0.15, "A_S": 0.20}
    return [
        {
            "card_identity": {
                "locus": locus,
                "task_id": task_id,
                "rounds": rounds,
                "resource_formula_binding": {
                    "formula": {
                        "process_time_formula": {
                            "protected_reserve_fraction": fractions[locus]
                        }
                    }
                },
            },
            "protected_closeout_reserve_enforced": True,
        }
        for locus, task_id, rounds in keys
    ]


def _write_v02_resource_calibration(
    tmp_path: Path,
    cards: list[dict[str, object]],
) -> tuple[Path, Path]:
    manifest_path = tmp_path / "manifest.json"
    summary_path = tmp_path / "summary.json"
    write_json_atomic(manifest_path, {"schema_version": "v0.2"})
    write_json_atomic(
        summary_path,
        {
            "schema_version": "v0.2",
            "status": "passed",
            "calibration_passed": True,
            "method_qualification_may_be_authorized": True,
            "resource_card_proposals": cards,
        },
    )
    return manifest_path, summary_path


def _bypass_v02_producer_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    from chemworld.eval import work_ii_resource_calibration_v02

    monkeypatch.setattr(work_ii_resource_calibration_v02, "validate_manifest", lambda *a: [])
    monkeypatch.setattr(work_ii_resource_calibration_v02, "validate_summary", lambda *a, **k: [])


def test_c2_consumes_exact_v02_task_cards_with_locus_closeout_fractions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _bypass_v02_producer_validation(monkeypatch)
    manifest_path, summary_path = _write_v02_resource_calibration(
        tmp_path, _v02_resource_cards()
    )

    _, errors = work_ii_c2_admission._resource_calibration_errors(
        tmp_path, manifest_path, summary_path
    )

    assert errors == []


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "substituted"])
def test_c2_rejects_missing_duplicate_or_substituted_v02_task_card(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
) -> None:
    _bypass_v02_producer_validation(monkeypatch)
    cards = _v02_resource_cards()
    if mutation == "missing":
        cards.pop()
    elif mutation == "duplicate":
        cards[-1] = deepcopy(cards[0])
    else:
        cards[-1]["card_identity"]["task_id"] = "substituted-task"
    manifest_path, summary_path = _write_v02_resource_calibration(tmp_path, cards)

    _, errors = work_ii_c2_admission._resource_calibration_errors(
        tmp_path, manifest_path, summary_path
    )

    assert "W2-26 requires the exact nine task resource cards" in errors


@pytest.mark.parametrize("locus", ["A_E", "A_P", "A_S"])
def test_c2_rejects_unenforced_or_wrong_fraction_v02_task_card(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    locus: str,
) -> None:
    _bypass_v02_producer_validation(monkeypatch)
    cards = _v02_resource_cards()
    target = next(card for card in cards if card["card_identity"]["locus"] == locus)
    target["protected_closeout_reserve_enforced"] = False
    target["card_identity"]["resource_formula_binding"]["formula"][
        "process_time_formula"
    ]["protected_reserve_fraction"] = 0.99
    manifest_path, summary_path = _write_v02_resource_calibration(tmp_path, cards)

    _, errors = work_ii_c2_admission._resource_calibration_errors(
        tmp_path, manifest_path, summary_path
    )

    assert any("does not enforce closeout" in error for error in errors)
    assert any("closeout fraction differs" in error for error in errors)


def test_current_c2_admission_is_truthfully_incomplete() -> None:
    report = build_c2_admission_report(ROOT, PLAN, DESIGN, _cells())

    assert report["status"] == "not_ready_fail_closed"
    assert report["formal_execution_allowed"] is False
    assert report["blocks"]["A_E"]["public_schedule"][
        "public_schedule_cell_count"
    ] == 75
    assert any("A_P requires exactly 2" in row for row in report["blocking_requirements"])
    assert any("A_S requires exactly 2" in row for row in report["blocking_requirements"])
    assert any("A_E prior" in row for row in report["blocking_requirements"])
    assert any("W2-26" in row for row in report["blocking_requirements"])
    assert validate_c2_admission_report(ROOT, report, PLAN, DESIGN, _cells()) == []


def test_rehashing_an_incomplete_admission_as_ready_is_rejected() -> None:
    report = build_c2_admission_report(ROOT, PLAN, DESIGN, _cells())
    forged = deepcopy(report)
    forged["status"] = "ready_for_formal_authorization"
    forged["formal_execution_allowed"] = True
    forged["blocking_requirements"] = []
    forged["evidence_validation_errors"] = []
    forged["admission_sha256"] = canonical_json_sha256(
        {key: value for key, value in forged.items() if key != "admission_sha256"}
    )

    assert "C2 admission report differs from deterministic evidence rebuild" in (
        validate_c2_admission_report(ROOT, forged, PLAN, DESIGN, _cells())
    )


def test_development_execution_context_is_explicitly_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    development = {
        "execution_mode": "development",
        "evidence_status": "development_only",
        "release_eligible": False,
        "c2_admission_authorized": False,
        "tested_commit": None,
        "freeze_id": None,
        "release_manifest_sha256": None,
        "execution_surface_sha256": None,
    }
    monkeypatch.setattr(
        work_ii_c2_admission,
        "validate_execution_envelope",
        lambda *args, **kwargs: [],
    )

    errors = _release_execution_context_errors(
        tmp_path, development, label="Q1 report"
    )

    assert errors == ["Q1 report is not release-authorized for C2 admission"]


def test_release_cohort_key_binds_both_freeze_and_tested_commit() -> None:
    first = _release_context()
    changed_freeze = _release_context(freeze_id="e" * 64)
    changed_commit = _release_context(tested_commit="f" * 40)

    assert _execution_cohort_key(first) == ("b" * 64, "a" * 40)
    assert _execution_cohort_key(first) != _execution_cohort_key(changed_freeze)
    assert _execution_cohort_key(first) != _execution_cohort_key(changed_commit)


def test_admission_rejects_two_independently_forged_selection_rosters(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan_path = tmp_path / "plan.json"
    design_path = tmp_path / "design.json"
    ae_path = tmp_path / "ae.json"
    calibration_manifest = tmp_path / "calibration-manifest.json"
    calibration_summary = tmp_path / "calibration-summary.json"
    for path in (design_path, ae_path, calibration_manifest, calibration_summary):
        write_json_atomic(path, {})

    receipt_paths: dict[str, list[str]] = {"A_P": [], "A_S": []}
    for locus in ("A_P", "A_S"):
        for slot in (1, 2):
            task_id = f"{locus.lower()}-task-{slot}"
            if locus == "A_S":
                task_id = (
                    "rejected-crystallization" if slot == 1 else "rejected-flow"
                )
                roster = [
                    {
                        "task_id": task_id,
                        "frozen_rank": slot,
                        "eligible_before_formal_outcomes": True,
                        "eligibility_basis": "independent forged selection",
                    },
                    {
                        "task_id": f"private-placeholder-{slot}",
                        "frozen_rank": 3 - slot,
                        "eligible_before_formal_outcomes": True,
                        "eligibility_basis": "independent forged selection",
                    },
                ]
            else:
                roster = [
                    {
                        "task_id": f"{locus.lower()}-task-{index}",
                        "frozen_rank": index,
                        "eligible_before_formal_outcomes": True,
                        "eligibility_basis": "shared frozen candidate roster",
                    }
                    for index in (1, 2)
                ]
            selection = {
                "schema_version": C2_OUTCOME_BLIND_SELECTION_VERSION,
                "locus": locus,
                "task_id": task_id,
                "selection_slot": slot,
                "selection_rule": {
                    "method": "terminally_eligible_then_ascending_frozen_rank",
                    "formal_participant_outcomes_permitted": False,
                    "required_selected_task_count": 2,
                    "all_candidates_require_terminal_eligibility_disposition": True,
                },
                "candidate_roster": sorted(
                    [
                        {
                            "task_id": row["task_id"],
                            "frozen_rank": row["frozen_rank"],
                            "terminal_qualification_passed": True,
                            "disposition": "eligible",
                        }
                        for row in roster
                    ],
                    key=lambda row: int(row["frozen_rank"]),
                ),
                "selection_protocol_binding": {
                    "path": (
                        f"configs/benchmark/{locus.lower()}-shared-protocol.json"
                        if locus == "A_P"
                        else f"configs/benchmark/{locus.lower()}-{slot}-forged-protocol.json"
                    ),
                    "sha256": ("d" if locus == "A_P" else str(slot)) * 64,
                    "protocol_sha256": ("e" if locus == "A_P" else str(slot + 2)) * 64,
                },
                "selection_sha256": canonical_json_sha256([locus, slot]),
            }
            selection_path = tmp_path / f"{locus.lower()}-{slot}-selection.json"
            write_json_atomic(selection_path, selection)
            receipt = {
                "task_id": task_id,
                "outcome_blind_selection_binding": {
                    "path": selection_path.relative_to(tmp_path).as_posix()
                },
                "receipt_sha256": canonical_json_sha256([task_id, "receipt"]),
            }
            receipt_path = tmp_path / f"{locus.lower()}-{slot}-receipt.json"
            write_json_atomic(receipt_path, receipt)
            receipt_paths[locus].append(receipt_path.relative_to(tmp_path).as_posix())

    plan = {
        "required_blocks": {
            "A_E": {
                "public_schedule_cell_count": 75,
                "prior_qualification_report_path": ae_path.relative_to(
                    tmp_path
                ).as_posix(),
            },
            "A_P": {"task_admission_receipt_paths": receipt_paths["A_P"]},
            "A_S": {"task_admission_receipt_paths": receipt_paths["A_S"]},
        },
        "resource_calibration": {
            "manifest_path": calibration_manifest.relative_to(tmp_path).as_posix(),
            "summary_path": calibration_summary.relative_to(tmp_path).as_posix(),
        },
    }
    write_json_atomic(plan_path, plan)

    monkeypatch.setattr(work_ii_c2_admission, "_plan_errors", lambda plan: [])
    monkeypatch.setattr(
        work_ii_c2_admission, "_task_receipt_errors", lambda *args, **kwargs: []
    )
    monkeypatch.setattr(
        work_ii_c2_admission,
        "_ae_qualification_errors",
        lambda *args, **kwargs: (
            {
                "report_sha256": "b" * 64,
            },
            [],
        ),
    )
    monkeypatch.setattr(
        work_ii_c2_admission,
        "_resource_calibration_errors",
        lambda *args, **kwargs: (
            {
                "summary_sha256": "c" * 64,
            },
            [],
        ),
    )

    report = build_c2_admission_report(
        tmp_path, plan_path, design_path, _cells()
    )

    assert report["formal_execution_allowed"] is False
    assert report["blocks"]["A_P"]["outcome_blind_selection_pair"]["passed"] is True
    assert report["blocks"]["A_S"]["outcome_blind_selection_pair"]["passed"] is False
    assert any(
        "A_S selection records do not share the exact candidate roster" in error
        for error in report["evidence_validation_errors"]
    )
    assert validate_c2_admission_report(
        tmp_path, report, plan_path, design_path, _cells()
    ) == []
