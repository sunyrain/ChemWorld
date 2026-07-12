from __future__ import annotations

import copy
import json

from scripts.audit_backend_v05 import (
    DEFAULT_OUTPUT,
    build_report,
    load_protocol,
    validate_report,
)


def test_backend_freeze_protocol_covers_all_current_contracts() -> None:
    protocol = load_protocol()
    report = build_report(protocol, enforce_clean_tree=False)

    assert len(report["task_contract_hashes"]) == 15
    assert report["task_contract_hashes"] == protocol["expected_task_contract_hashes"]
    assert report["checks"]["runtime_integration"] is True
    assert report["checks"]["runtime_reachability"] is True
    assert report["checks"]["maturity_truth"] is True
    assert report["checks"]["state_transition_invariants"] is True
    assert report["checks"]["public_boundary"] is True
    assert report["benchmark_claim_allowed"] is False
    assert validate_report(report) == []


def test_task_contract_drift_blocks_the_candidate_freeze() -> None:
    protocol = load_protocol()
    protocol["expected_task_contract_hashes"] = dict(
        protocol["expected_task_contract_hashes"]
    )
    protocol["expected_task_contract_hashes"]["reaction-to-assay"] = "0" * 64

    report = build_report(protocol, enforce_clean_tree=False)

    assert report["checks"]["task_contracts_exact"] is False
    assert report["backend_freeze_allowed"] is False
    assert report["status"] == "blocked"


def test_report_hash_detects_tampering() -> None:
    report = build_report(load_protocol(), enforce_clean_tree=False)
    tampered = copy.deepcopy(report)
    tampered["artifact_sha256"][next(iter(tampered["artifact_sha256"]))] = "bad"

    assert "report hash mismatch" in validate_report(tampered)


def test_committed_backend_report_is_clean_and_candidate_only() -> None:
    report = json.loads(DEFAULT_OUTPUT.read_text(encoding="utf-8"))

    assert report["backend_freeze_allowed"] is True
    assert report["source_tree_dirty"] is False
    assert report["status"] == "candidate_backend_frozen"
    assert report["benchmark_claim_allowed"] is False
    assert validate_report(report) == []
