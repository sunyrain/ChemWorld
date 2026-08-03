from copy import deepcopy
from pathlib import Path

from scripts.run_work_i_latent_terminal_shadow_assays import (
    EXPECTED_PROTOCOL_SHA256,
    PROTOCOL_PATH,
    _formal_receipt,
    _read_json,
    protocol_sha256,
    report_sha256,
    validate_formal_report,
    validate_preflight,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_protocol_is_self_hashed_and_source_bound() -> None:
    protocol = _read_json(ROOT / PROTOCOL_PATH)
    assert protocol_sha256(protocol) == EXPECTED_PROTOCOL_SHA256
    assert validate_protocol(protocol, root=ROOT) == []


def test_preflight_validator_rejects_outcome_access() -> None:
    report = {
        "status": "PASS",
        "census": {
            "registered_discard_units": 36,
            "formal_shadow_evaluations_executed": 0,
            "formal_shadow_scores_accessed": 1,
            "agent_provider_calls": 0,
        },
        "gates": {"outcome_blind": True},
    }
    report["report_sha256"] = report_sha256(report)
    assert "preflight crossed the outcome boundary" in validate_preflight(report)


def test_formal_receipt_fails_closed_on_repeat_mismatch() -> None:
    unit = {
        "discard_id": "cell-01:lifecycle-01:terminal-step-001",
        "lifecycle_index": 1,
        "terminal_step": 1,
        "public_prefix_sha256": "a" * 64,
        "terminal_action_sha256": "b" * 64,
    }
    cell = {"cell_id": "cell-01", "world_seed": 0, "information_arm": "opaque_codes"}
    evaluation = {
        "leaderboard_score": 0.5,
        "terminal_evaluation_identity_sha256": "c" * 64,
        "shadow_observation_sha256": "d" * 64,
        "noise_key_sha256": "e" * 64,
    }
    first = {"status": "resolved", "evaluation": evaluation}
    repeat = deepcopy(first)
    repeat["evaluation"]["leaderboard_score"] = 0.6
    receipt = _formal_receipt(
        unit,
        cell,
        first,
        repeat,
        contract_sha256="f" * 64,
        population_manifest_sha256="0" * 64,
    )
    assert receipt["outcome_status"] == "unresolved"
    assert receipt["failure_category"] == "same_identity_replay_mismatch"


def test_formal_validator_accepts_bounded_unresolved_population() -> None:
    receipts = [
        {"discard_id": f"discard-{index:02d}", "outcome_status": "unresolved"}
        for index in range(36)
    ]
    report = {"status": "FAIL", "gates": {"all_resolved": False}, "receipts": receipts}
    report["report_sha256"] = report_sha256(report)
    assert validate_formal_report(report) == []
