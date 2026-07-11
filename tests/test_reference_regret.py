from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from chemworld.eval.reference_regret import (
    METHOD_SCORE_OBSERVATION_VERSION,
    REFERENCE_ESTIMATE_VERSION,
    ReferenceRegretError,
    audit_reference_regret_protocol,
    evaluate_reference_regret,
    load_reference_regret_protocol,
    reference_regret_protocol_sha256,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "reference-regret-controls.json"
)


def _digest(*parts: object) -> str:
    return hashlib.sha256("\0".join(str(part) for part in parts).encode()).hexdigest()


def _small_evidence() -> tuple[dict, list[dict], list[dict]]:
    protocol = copy.deepcopy(load_reference_regret_protocol())
    protocol["formal_task_ids"] = ["partition-discovery"]
    protocol["seed_ids"] = [20, 21]
    protocol["metrics"] = {"objective": protocol["metrics"]["objective"]}
    protocol["uncertainty_policy"]["bootstrap_samples"] = 200
    protocol_digest = reference_regret_protocol_sha256(protocol)
    references = []
    methods = []
    for seed, estimate in ((20, 0.60), (21, 0.70)):
        references.append(
            {
                "schema_version": REFERENCE_ESTIMATE_VERSION,
                "protocol_sha256": protocol_digest,
                "task_id": "partition-discovery",
                "seed": seed,
                "metric_id": "objective",
                "estimate": estimate,
                "interval_lower": estimate - 0.02,
                "interval_upper": estimate + 0.03,
                "confidence_level": 0.95,
                "is_oracle": False,
                "builder_id": "reference_portfolio",
                "source_split": "reference-search",
                "frozen_before_method_scoring": True,
                "source_count": 1,
                "trajectory_digests": [_digest("reference", seed)],
                "result_schema_version": "chemworld-evaluation-result-0.3",
                "score_replay_binding_version": "chemworld-score-replay-binding-0.1",
                "replay_verified": True,
            }
        )
        methods.append(
            {
                "schema_version": METHOD_SCORE_OBSERVATION_VERSION,
                "protocol_sha256": protocol_digest,
                "task_id": "partition-discovery",
                "seed": seed,
                "metric_id": "objective",
                "method_id": "strong_method",
                "value": estimate + 0.05,
                "trajectory_sha256": _digest("method", seed),
                "result_schema_version": "chemworld-evaluation-result-0.3",
                "score_replay_binding_version": "chemworld-score-replay-binding-0.1",
                "replay_verified": True,
            }
        )
    return protocol, references, methods


def test_protocol_controls_are_ready_without_claiming_formal_results() -> None:
    report = audit_reference_regret_protocol(load_reference_regret_protocol())

    assert report["controls_ready"] is True
    assert report["parent_task_complete"] is False
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
    assert report["probe_count"] == 11
    assert all(report["adversarial_probes"].values())
    assert report["control_grid"] == {
        "expected_reference_cells": 160,
        "observed_reference_cells": 160,
        "method_ids": ["control_above", "control_below"],
        "observed_method_cells": 320,
        "complete": True,
    }


def test_signed_regret_preserves_methods_exceeding_best_known_reference() -> None:
    protocol, references, methods = _small_evidence()
    result = evaluate_reference_regret(protocol, references, methods)

    regrets = [item["signed_regret"] for item in result["paired_regret"]]
    assert regrets == pytest.approx([-0.05, -0.05])
    summary = result["summaries"]["strong_method"]["partition-discovery"]["objective"]
    assert summary["mean_signed_regret"] == pytest.approx(-0.05)
    assert summary["method_exceeds_reference_count"] == 2
    assert summary["negative_regret_preserved"] is True
    assert summary["reference_uncertainty_mean_endpoint_interval"] == pytest.approx(
        [-0.07, -0.02]
    )


def test_reference_regret_fails_closed_on_missing_or_contaminated_evidence() -> None:
    protocol, references, methods = _small_evidence()
    with pytest.raises(ReferenceRegretError, match="reference coverage incomplete"):
        evaluate_reference_regret(protocol, references[:-1], methods)

    contaminated = copy.deepcopy(methods)
    contaminated[0]["trajectory_sha256"] = references[0]["trajectory_digests"][0]
    with pytest.raises(ReferenceRegretError, match="trajectories overlap"):
        evaluate_reference_regret(protocol, references, contaminated)

    unverified = copy.deepcopy(methods)
    unverified[0]["replay_verified"] = False
    with pytest.raises(ReferenceRegretError, match="not replay verified"):
        evaluate_reference_regret(protocol, references, unverified)


def test_protocol_audit_fails_closed_if_oracle_semantics_are_tampered() -> None:
    protocol = load_reference_regret_protocol()
    protocol["reference_semantics"]["is_oracle"] = True

    report = audit_reference_regret_protocol(protocol)

    assert report["controls_ready"] is False
    assert report["checks"]["reference_is_not_oracle"] is False
    assert not any(report["adversarial_probes"].values())


def test_frozen_control_report_keeps_formal_gate_closed() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))

    assert report["controls_ready"] is True
    assert report["status"] == "controls_ready_formal_reference_search_pending"
    assert report["parent_task_complete"] is False
    assert report["formal_results_present"] is False
    assert report["reference_semantics"]["is_oracle"] is False
    assert report["reference_semantics"]["negative_regret_policy"] == "preserve_and_report"
