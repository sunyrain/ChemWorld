from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval import experiment_1_challenge_v1_1 as challenge
from chemworld.eval.provenance import file_sha256


def test_entity_cost_is_measured_from_replicated_public_observations() -> None:
    report = {"descriptor_permutation": [3, 1, 2, 0]}
    rows = []
    for target, values in ((0, (0.20, 0.21, 0.19)), (3, (0.70, 0.72, 0.68))):
        for replicate, value in enumerate(values):
            rows.append(
                {
                    "status": "completed",
                    "nuisance_anchor": 0,
                    "target_category": target,
                    "allowed_metrics": {"transport_efficiency": value},
                    "receipt_sha256": f"{target}-{replicate}",
                }
            )
    result = challenge._entity_trace(
        report,
        rows,
        {
            "target_field": "target_category",
            "anchor_field": "nuisance_anchor",
            "anchor_value": 0,
            "metric_container": "allowed_metrics",
            "metric": "transport_efficiency",
            "reliable_snr": 2.0,
            "minimum_effect": 0.05,
            "participant_budget": 4,
            "minimum_information_gain": 2.0,
        },
    )

    assert result["default_one_shot_reliably_discriminates"] is False
    assert result["minimum_reliable_unique_condition_cost"] == 2
    assert result["budget_window_passed"] is True
    assert result["ordered_policy_steps"][1]["observation_sha256"]


def test_entity_missing_replicates_fails_closed() -> None:
    report = {"descriptor_permutation": [3, 1, 2, 0]}
    rows = [
        {
            "status": "completed",
            "solvent": 0,
            "extractant": target,
            "measurement": {"product_in_organic": value},
            "receipt_sha256": str(target),
        }
        for target, value in ((0, 0.2), (3, 0.8))
    ]
    result = challenge._entity_trace(
        report,
        rows,
        {
            "target_field": "extractant",
            "anchor_field": "solvent",
            "anchor_value": 0,
            "metric_container": "measurement",
            "metric": "product_in_organic",
            "reliable_snr": 2.0,
            "minimum_effect": 0.05,
            "participant_budget": 4,
            "minimum_information_gain": 2.0,
        },
    )

    assert result["minimum_reliable_unique_condition_cost"] is None
    assert result["budget_window_passed"] is False


def test_pa_structural_without_repeated_noise_support_fails_closed() -> None:
    rows = []
    for pair_id, linear, power in (
        ("a", (0.6, 0.4), (0.8, 0.2)),
        ("b", (0.4, 0.6), (0.2, 0.8)),
    ):
        for law_id, values in (("linear_response", linear), ("power_response", power)):
            rows.append(
                {
                    "pair_id": pair_id,
                    "law_id": law_id,
                    "measurement": {
                        "product_in_organic": values[0],
                        "product_in_aqueous": values[1],
                    },
                    "receipt_sha256": f"{pair_id}-{law_id}",
                }
            )
    result = challenge._pa_structural_trace(
        {},
        rows,
        {
            "ordered_action_ids": ["a", "b"],
            "minimum_slope_deviation": 0.2,
            "observed_noise_replicates_per_condition": 1,
            "minimum_noise_replicates": 3,
            "participant_budget": 4,
            "minimum_information_gain": 0.2,
        },
    )

    assert result["minimum_reliable_unique_condition_cost"] is None
    assert result["repeated_noise_support"]["observed_replicates_per_condition"] == 1


def test_raw_artifact_digest_mismatch_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "receipts.json"
    path.write_text(json.dumps([{"receipt_sha256": "a", "status": "completed"}]))
    manifest = {
        "report_path": "runs/example/world-report.json",
        "raw_filename": "receipts.json",
        "raw_sha256": "0" * 64,
        "raw_rows": 1,
    }
    with pytest.raises(ValueError, match="digest mismatch"):
        challenge.validate_raw_artifact(
            path, manifest, report_path="runs/example/world-report.json"
        )


def test_raw_artifact_duplicate_and_malformed_rows_fail_closed(tmp_path: Path) -> None:
    path = tmp_path / "receipts.json"
    path.write_text(
        json.dumps(
            [
                {"receipt_sha256": "a", "status": "completed"},
                {"receipt_sha256": "a", "status": "completed"},
            ]
        )
    )
    manifest = {
        "report_path": "runs/example/world-report.json",
        "raw_filename": "receipts.json",
        "raw_sha256": file_sha256(path),
        "raw_rows": 2,
    }
    with pytest.raises(ValueError, match="duplicate identities"):
        challenge.validate_raw_artifact(
            path, manifest, report_path="runs/example/world-report.json"
        )
