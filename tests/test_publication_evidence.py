from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.publication_evidence import PUBLICATION_EVIDENCE_SCHEMA_VERSION
from chemworld.eval.publication_protocol import (
    canonical_protocol_sha256,
    load_publication_protocol,
)
from chemworld.tasks import SERIOUS_TASK_IDS

SUMMARY_PATH = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "publication-classic20-full-summary.json"
)
HISTORICAL_PROTOCOL_SHA256 = (
    "1a0789f5ffae2222e0235e9b36ca6bbae5888aace4b3bf405b78492e69a1742a"
)


def test_historical_publication_evidence_remains_bound_and_fail_closed() -> None:
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    protocol = load_publication_protocol()

    assert summary["schema_version"] == PUBLICATION_EVIDENCE_SCHEMA_VERSION
    assert summary["protocol_sha256"] == HISTORICAL_PROTOCOL_SHA256
    assert summary["protocol_sha256"] != canonical_protocol_sha256(protocol)
    assert summary["status"] == "blocked"
    assert summary["publication_ready"] is False
    assert summary["matrix"]["result_count"] == 600
    assert summary["matrix"]["seeds"] == list(range(20))
    assert summary["matrix"]["complete_experiments_per_task_seed"] == 40
    assert set(summary["tasks"]) == set(SERIOUS_TASK_IDS)
    assert summary["integrity"]["verified_result_count"] == 600


def test_publication_evidence_records_positive_signal_and_blockers() -> None:
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    gates = summary["gates"]

    assert gates["total_score_positive_all_tasks"] is True
    assert gates["total_score_holm_significant_all_tasks"] is True
    assert gates["total_score_sesoi_task_count"] == 4
    assert gates["primary_direction_supported_task_count"] == 4
    assert gates["primary_sesoi_task_count"] == 2
    assert gates["primary_claims_validated_all_tasks"] is False
    assert gates["safety_risk_signal_observed"] is True
    assert gates["safety_constraint_active"] is False
    assert gates["safety_risk_signal_informative"] is False

    method_risks = [
        method["mean_safety_risk"]
        for task in summary["tasks"].values()
        for method in task["methods"].values()
    ]
    assert min(method_risks) > 0.0
    assert gates["generalization_evidence_complete"] is False
    assert gates["exploit_audit_complete"] is False
