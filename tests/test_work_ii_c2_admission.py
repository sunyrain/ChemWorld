from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256
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
