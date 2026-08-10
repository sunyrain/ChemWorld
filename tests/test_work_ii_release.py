from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.work_ii_release import (
    PREREGISTRATION_FREEZE_RECEIPT_VERSION,
    build_prerun_evidence_graph,
    preregistration_freeze_receipt_sha256,
    prerun_evidence_graph_sha256,
    validate_clean_release_receipt,
    validate_preregistration_freeze_receipt,
    validate_prerun_evidence_graph,
)

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "workstreams/flagship_tasks/reports/work-ii-prerun-evidence-graph-v0.1.json"


def test_prerun_evidence_graph_is_deterministic_current_and_acyclic() -> None:
    first = build_prerun_evidence_graph(ROOT)
    second = build_prerun_evidence_graph(ROOT)
    assert first == second
    assert validate_prerun_evidence_graph(ROOT, first) == []
    assert first["status"] == "passed_final_freeze_blocked"
    assert first["summary"] == {
        "node_count": 13,
        "edge_count": 17,
        "passed_node_count": 13,
        "failed_node_count": 0,
        "preregistration_blocker_count": 5,
    }
    assert first["provider_calls_executed"] == 0
    assert first["formal_participant_outcome_count"] == 0


def test_committed_prerun_evidence_graph_matches_current_artifacts() -> None:
    committed = json.loads(GRAPH.read_text(encoding="utf-8"))
    assert committed == build_prerun_evidence_graph(ROOT)
    assert validate_prerun_evidence_graph(ROOT, committed) == []


def test_prerun_evidence_graph_rejects_cycle_even_with_refreshed_hash() -> None:
    graph = build_prerun_evidence_graph(ROOT)
    tampered = deepcopy(graph)
    tampered["edges"].append(
        {
            "from": "preregistration_draft",
            "to": "current_registry",
            "relation": "invalid_cycle",
        }
    )
    tampered["summary"]["edge_count"] += 1
    tampered["graph_sha256"] = prerun_evidence_graph_sha256(tampered)
    errors = validate_prerun_evidence_graph(ROOT, tampered)
    assert "Work II pre-run evidence graph has an unexpected edge count" in errors
    assert "evidence graph contains a cycle" in errors


def test_clean_release_receipt_validator_rejects_shallow_pass() -> None:
    assert validate_clean_release_receipt({"status": "passed"})


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
