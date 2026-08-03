from __future__ import annotations

import json
from pathlib import Path

from scripts.qualify_work_i_experiment_semantics import build_markdown, build_report

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json"
HUMAN = ROOT / "workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.md"


def test_semantics_reports_rebuild_from_executable_probes() -> None:
    rebuilt = build_report()
    committed = json.loads(MACHINE.read_text(encoding="utf-8"))
    assert committed == rebuilt
    assert HUMAN.read_text(encoding="utf-8") == build_markdown(rebuilt)


def test_all_declared_semantic_surfaces_are_qualified() -> None:
    report = json.loads(MACHINE.read_text(encoding="utf-8"))
    assert report["summary_counts"] == {
        "instrument_contract_count": 5,
        "instrument_probe_pass_count": 5,
        "operation_contract_count": 28,
        "operation_invalid_state_preservation_pass_count": 28,
        "operation_valid_commit_pass_count": 28,
        "transaction_status_count": 4,
    }
    assert report["failure_semantics"]["observed_statuses"] == [
        "campaign_resource_rejected",
        "committed",
        "rolled_back",
        "validation_failed",
    ]
    assert all(row["passed"] for row in report["operation_rows"])
    assert all(row["passed"] for row in report["instrument_rows"])
    assert all(report["gates"].values())
    assert report["passed"] is True
    assert report["claim_boundary"]["real_instrument_calibration_claim"] is False
