from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from scripts.freeze_work_i_policy_profile import build_artifact, build_markdown

from chemworld.eval.policy_validity_contract import (
    AXES,
    ENDPOINT_CONTEXT,
    METRICS,
    PROFILE_SCHEMA_ID,
    PROFILE_SCHEMA_VERSION,
    build_profile_contract,
    profile_contract_sha256,
    validate_profile_record,
)

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "configs/benchmark/work_i_policy_profile_contract_v0.1.json"
HUMAN = (
    ROOT / "workstreams/arxiv_v1/reports/work-i-policy-profile-contract-v0.1.md"
)


def _valid_record() -> dict[str, Any]:
    axes: dict[str, dict[str, float | None]] = {
        axis["axis_id"]: {} for axis in AXES
    }
    for metric in METRICS:
        axes[metric.axis_id][metric.metric_id] = (
            None if metric.nullable else 1.0
        )
    axes["terminal_commitment"].update(
        {
            "closed_lifecycle_fraction": 1.0,
            "assay_fraction": 1.0,
            "discard_fraction": 0.0,
        }
    )
    axes["evidence_acquisition"]["measured_lifecycle_fraction"] = 0.0
    axes["evidence_conditioned_action"]["threshold_eligible_fraction"] = 0.0
    return {
        "schema_id": PROFILE_SCHEMA_ID,
        "schema_version": PROFILE_SCHEMA_VERSION,
        "contract_sha256": profile_contract_sha256(),
        "identity": {
            "campaign_id": "campaign-1",
            "world_id": "world-1",
            "information_arm": "opaque",
            "policy_id": "assay_all",
            "resource_card_sha256": "resource-hash",
            "trajectory_manifest_sha256": "trajectory-hash",
        },
        "counts": {
            "planned_lifecycle_count": 6,
            "closed_lifecycle_count": 6,
            "final_assay_count": 6,
            "discard_count": 0,
            "measured_lifecycle_count": 0,
            "threshold_eligible_lifecycle_count": 0,
        },
        "construct_axes": axes,
        "endpoint_context": {
            metric.metric_id: 0.5 for metric in ENDPOINT_CONTEXT
        },
        "reliability": {
            "trajectory_exact_replay_match": True,
            "profile_exact_rebuild_match": True,
            "provider_call_count": 0,
        },
    }


def test_frozen_artifacts_rebuild_exactly() -> None:
    artifact = build_artifact()
    assert json.loads(MACHINE.read_text(encoding="utf-8")) == artifact
    assert HUMAN.read_text(encoding="utf-8") == build_markdown(artifact)
    assert artifact["contract_sha256"] == profile_contract_sha256(
        build_profile_contract()
    )


def test_construct_is_multidimensional_and_keeps_endpoint_context_separate() -> None:
    artifact = build_artifact()
    assert len(artifact["axes"]) == 5
    assert len(artifact["metrics"]) == 19
    assert len(artifact["endpoint_context"]) == 2
    assert artifact["construct"]["representation"] == (
        "multidimensional profile; no composite score"
    )
    construct_ids = {metric["metric_id"] for metric in artifact["metrics"]}
    endpoint_ids = {
        metric["metric_id"] for metric in artifact["endpoint_context"]
    }
    assert construct_ids.isdisjoint(endpoint_ids)


def test_valid_profile_record_satisfies_schema_and_invariants() -> None:
    assert validate_profile_record(_valid_record()) == []


def test_validator_rejects_count_fraction_and_null_semantic_violations() -> None:
    record = _valid_record()
    counts = cast(dict[str, Any], record["counts"])
    axes = cast(dict[str, dict[str, Any]], record["construct_axes"])
    counts["discard_count"] = 1
    axes["terminal_commitment"]["assay_fraction"] = 1.2
    axes["evidence_conditioned_action"][
        "threshold_decision_concordance"
    ] = 0.0
    errors = validate_profile_record(record)
    assert "closed lifecycle count must equal assays plus discards" in errors
    assert "assay_fraction is above 1.0" in errors
    assert (
        "threshold_decision_concordance must be null with no eligible lifecycle"
        in errors
    )


def test_validator_reports_malformed_values_without_raising() -> None:
    record = _valid_record()
    axes = cast(dict[str, dict[str, Any]], record["construct_axes"])
    axes["terminal_commitment"]["closed_lifecycle_fraction"] = "all"
    errors = validate_profile_record(record)
    assert "closed_lifecycle_fraction must be numeric or null" in errors
    assert "closed_lifecycle_fraction disagrees with counts" in errors
