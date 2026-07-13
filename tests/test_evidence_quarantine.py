from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from chemworld.eval.evidence_quarantine import (
    EvidenceQuarantineError,
    assert_formal_run_allowed,
    audit_evidence_quarantine,
    build_exposure_inventory,
    load_evidence_quarantine_policy,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "evidence-quarantine-v0.5.json"
SHA = "a" * 64


def test_public_exposure_inventory_covers_consumed_and_development_seeds() -> None:
    inventory = build_exposure_inventory(load_evidence_quarantine_policy())
    exposed = set(inventory["exposed_seeds"])
    assert set(range(20, 40)).issubset(exposed)
    assert set(range(300, 320)).issubset(exposed)
    assert set(range(500, 520)).issubset(exposed)
    assert {106, 110, 1100, 1119, 1200, 1209, 1300, 1304}.issubset(exposed)
    assert inventory["retained_result_count"] == 160
    assert inventory["git_history_config_blob_count"] >= 79
    assert inventory["exposed_world_cell_count"] > 0
    assert any(
        source.startswith("git:") for source in inventory["sources"]["300"]
    )


@pytest.mark.parametrize("seed", [20, 39, 300, 319, 500, 519, 1100])
def test_formal_guard_rejects_every_publicly_exposed_seed(seed: int) -> None:
    with pytest.raises(EvidenceQuarantineError, match="already publicly exposed"):
        assert_formal_run_allowed(
            seed=seed,
            protocol_id="chemworld-formal-0.4",
            protocol_benchmark_claim_allowed=True,
            backend_id="chemworld-backend-v0.5",
            backend_semantic_hash=SHA,
            private_seed_commitment=SHA,
        )


def test_formal_guard_rejects_quarantined_or_incompletely_bound_identity() -> None:
    policy = load_evidence_quarantine_policy()
    unseen_seed = 987_654_321
    with pytest.raises(EvidenceQuarantineError, match="protocol is quarantined"):
        assert_formal_run_allowed(
            seed=unseen_seed,
            protocol_id="chemworld-vnext-confirmatory-freeze-0.3",
            protocol_benchmark_claim_allowed=True,
            backend_id="chemworld-backend-v0.5",
            backend_semantic_hash=SHA,
            private_seed_commitment=SHA,
            policy=policy,
        )
    with pytest.raises(EvidenceQuarantineError, match="has not enabled"):
        assert_formal_run_allowed(
            seed=unseen_seed,
            protocol_id="chemworld-formal-0.4",
            protocol_benchmark_claim_allowed=False,
            backend_id="chemworld-backend-v0.5",
            backend_semantic_hash=SHA,
            private_seed_commitment=SHA,
            policy=policy,
        )
    with pytest.raises(EvidenceQuarantineError, match="semantic sha256"):
        assert_formal_run_allowed(
            seed=unseen_seed,
            protocol_id="chemworld-formal-0.4",
            protocol_benchmark_claim_allowed=True,
            backend_id="chemworld-backend-v0.5",
            backend_semantic_hash="missing",
            private_seed_commitment=SHA,
            policy=policy,
        )


def test_formal_guard_accepts_a_fully_bound_unseen_identity() -> None:
    assert_formal_run_allowed(
        seed=987_654_321,
        protocol_id="chemworld-formal-0.4",
        protocol_benchmark_claim_allowed=True,
        backend_id="chemworld-backend-v0.5",
        backend_semantic_hash=SHA,
        private_seed_commitment=SHA,
    )


def test_audit_fails_when_a_consumed_cohort_is_not_declared_exposed() -> None:
    policy = copy.deepcopy(load_evidence_quarantine_policy())
    policy["known_consumed_cohorts"].append(
        {"cohort_id": "tampered", "start": 999_999_990, "stop_inclusive": 999_999_999}
    )
    report = audit_evidence_quarantine(policy)
    assert report["controls_ready"] is False
    assert report["controls"]["known_consumed_cohorts_are_exposed"] is False


def test_retained_primary_0_3_is_explicitly_quarantined() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["formal_guard_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["formal_results_present"] is False
    assert report["legacy_primary_0_3"]["result_count"] == 160
    assert report["legacy_primary_0_3"]["trajectory_count"] == 160
    assert report["legacy_primary_0_3"]["classification"] == "pre-v0.5_diagnostic_only"
    assert report["controls"]["legacy_results_replay_verified"] is True
    assert report["controls"]["legacy_results_bind_lite_maturity"] is True
    assert report["stale_documentation_matches"] == []
