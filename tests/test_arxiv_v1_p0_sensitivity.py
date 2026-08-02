from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark" / "releases" / "chemworld-serious-v1" / "arxiv-v1-p0-sensitivity.json"


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def test_p0_sensitivity_report_is_self_hashed_and_complete() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    declared = report.pop("sensitivity_sha256")
    assert report["schema_version"] == "chemworld-arxiv-v1-p0-sensitivity-0.1"
    assert report["status"] == "frozen_complete"
    assert report["primary_analysis_unchanged"] is True
    assert declared == _canonical_sha256(report)


def test_p0_censoring_and_threshold_results_are_explicit() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    g2 = report["g2_v0_5"]
    censoring = g2["right_censoring_missing_sign_sensitivity"]
    assert censoring["minimum_possible_mixed_core_classifications"] == 6
    assert censoring["core_classification_count"] == 8
    by_setting = {
        (row["threshold"], row["zero_mode"]): row["mixed_core_classification_count"]
        for row in g2["classification_sensitivity"]
    }
    assert by_setting[(0.75, "include_zeros")] == 6
    assert by_setting[(0.8, "include_zeros")] == 8
    by_retention = {
        row["retention_fraction"]: row["classification"]["mixed_core_classification_count"]
        for row in g2["retention_fraction_sensitivity"]
    }
    assert by_retention == {0.8: 5, 0.9: 6, 0.95: 6}


def test_p0_first_launch_is_disclosed_without_pooling() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    launch = report["g2_v0_5"]["first_launch_sensitivity"]
    assert launch["status"] == "excluded_launch_reported_as_protocol_deviation"
    assert launch["cross_launch_pairing_primary_analysis_allowed"] is False
    assert launch["completed_cell"]["completed_vessels"] == 6
    assert launch["partial_next_cell_accepted_operation_count"] == 4
