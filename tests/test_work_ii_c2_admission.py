from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval import work_ii_c2_admission
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_c2_admission import (
    build_c2_admission_report,
    validate_c2_admission_report,
)

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "configs/benchmark/work_ii_c2_admission_manifest_v0.1.json"
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"


def _cells() -> list[dict[str, object]]:
    return [{"cell_id": f"ae-{index:02d}"} for index in range(75)]


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


def test_admission_rejects_two_independently_forged_selection_rosters(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    commit = "a" * 40
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
                "locus": locus,
                "task_id": task_id,
                "selection_slot": slot,
                "selection_rule": {
                    "method": "eligible_then_ascending_frozen_rank",
                    "formal_participant_outcomes_permitted": False,
                    "selection_slot": slot,
                    "required_selected_task_count": 2,
                },
                "candidate_roster": sorted(
                    roster, key=lambda row: int(row["frozen_rank"])
                ),
                "selection_sha256": canonical_json_sha256([locus, slot]),
            }
            selection_path = tmp_path / f"{locus.lower()}-{slot}-selection.json"
            write_json_atomic(selection_path, selection)
            receipt = {
                "task_id": task_id,
                "source_binding": {"tested_commit": commit},
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
    monkeypatch.setattr(work_ii_c2_admission, "git_worktree_dirty", lambda root: False)
    monkeypatch.setattr(
        work_ii_c2_admission,
        "_ae_qualification_errors",
        lambda *args, **kwargs: (
            {
                "report_sha256": "b" * 64,
                "c2_source_binding": {"tested_commit": commit},
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
                "c2_source_binding": {"tested_commit": commit},
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
