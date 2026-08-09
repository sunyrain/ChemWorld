from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.work_ii_release import (
    build_prerun_evidence_graph,
    prerun_evidence_graph_sha256,
    validate_clean_release_receipt,
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
        "preregistration_blocker_count": 6,
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
