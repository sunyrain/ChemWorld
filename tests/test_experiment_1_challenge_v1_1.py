from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval import experiment_1_challenge_v1_1 as challenge
from chemworld.eval.provenance import canonical_json_sha256, file_sha256


def test_information_choice_is_evaluated_at_first_reliable_stop() -> None:
    result = challenge._finish_trace(
        [
            {
                "unique_condition_cost": 1,
                "reliable_falsification": False,
                "information_gain_over_default": 0.0,
                "action_id": "default",
            },
            {
                "unique_condition_cost": 2,
                "reliable_falsification": True,
                "information_gain_over_default": 0.1,
                "action_id": "first-stop",
            },
            {
                "unique_condition_cost": 3,
                "reliable_falsification": True,
                "information_gain_over_default": 9.0,
                "action_id": "later",
            },
        ],
        budget=4,
        minimum_information_gain=1.0,
    )

    assert result["minimum_reliable_unique_condition_cost"] == 2
    assert result["information_choice_gain_over_default_at_stop"] == 0.1
    assert result["active_information_passed"] is False


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
                    "observation_noise_namespace": "unit-test",
                    "observation_seed": 1 if law_id == "linear_response" else 2,
                    "status": "completed",
                }
            )
    result = challenge._pa_structural_trace(
        {},
        rows,
        {
            "ordered_action_ids": ["a", "b"],
            "minimum_slope_deviation": 0.2,
            "observed_noise_replicates_per_condition": 999,
            "minimum_noise_replicates": 3,
            "participant_budget": 4,
            "minimum_information_gain": 0.2,
        },
    )

    assert result["minimum_reliable_unique_condition_cost"] is None
    assert set(result["repeated_noise_support"]["observed_replicates_by_condition"].values()) == {1}
    assert result["ordered_policy_steps"][0]["observation_sha256"]


def test_rx_structural_replicate_count_comes_from_hidden_receipt_keys() -> None:
    rows = []
    for action_index, action_id in enumerate(("a", "b")):
        for law_index, law_id in enumerate(("deactivating_baseline", "reversible_target_pathway")):
            value = 0.1 + 0.2 * action_index + 0.05 * law_index
            rows.append(
                {
                    "status": "completed",
                    "cell_id": action_id,
                    "law_id": law_id,
                    "direct_noise_key_sha256": f"noise-{action_id}-{law_id}",
                    "direct_metrics": {
                        "yield": value,
                        "conversion": value,
                        "selectivity": value,
                    },
                }
            )
    result = challenge._rx_structural_trace(
        {},
        rows,
        {
            "ordered_action_ids": ["a", "b"],
            "minimum_accumulation": 0.01,
            "observed_noise_replicates_per_condition": 999,
            "minimum_noise_replicates": 3,
            "participant_budget": 4,
            "minimum_information_gain": 0.01,
        },
    )

    assert result["minimum_reliable_unique_condition_cost"] is None
    assert result["repeated_noise_support"]["observed_replicates_by_condition"] == {
        "a": 1,
        "b": 1,
    }
    assert "offline_paired_family_separability" in result


def test_pa_parametric_is_recomputed_from_raw_receipts_not_gate_fields() -> None:
    report = {
        "aligned_prior": {"k_star_band": [1.8, 2.2]},
        "misspecified_prior": {"k_star_band": [0.6, 0.8]},
        "noise_robust_counterexample": True,
        "prediction_gap": 999.0,
    }
    rows = []
    for action_id, organic_volume in (("reference", 1.0), ("low_ratio", 2.0)):
        for replicate in range(3):
            rows.append(
                {
                    "status": "completed",
                    "point_id": action_id,
                    "observation_noise_namespace": "unit-test",
                    "observation_seed": replicate,
                    "receipt_sha256": f"{action_id}-{replicate}",
                    "extractant_volume_L": organic_volume,
                    "solvent_volume_L": 0.5,
                    "aqueous_volume_L": 0.5,
                    "measurement": {
                        "product_in_organic": 0.66 + 0.01 * replicate,
                        "product_in_aqueous": 0.34 - 0.01 * replicate,
                    },
                }
            )
    policy = {
        "ordered_action_ids": ["reference", "low_ratio"],
        "minimum_prediction_gap": 0.05,
        "minimum_signal_to_noise_ratio": 2.0,
        "minimum_noise_replicates": 3,
        "participant_budget": 3,
        "minimum_information_gain": 0.005,
    }
    first = challenge._pa_parametric_trace(report, rows, policy)
    report["noise_robust_counterexample"] = False
    report["prediction_gap"] = 0.0
    second = challenge._pa_parametric_trace(report, rows, policy)

    assert first == second
    assert first["ordered_policy_steps"][0]["observation_sha256"]


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


def test_bound_contract_permutation_rejects_missing_or_mismatched_file(tmp_path: Path) -> None:
    missing = {"path": "missing.json", "sha256": "0" * 64}
    with pytest.raises(ValueError, match="missing"):
        challenge.descriptor_permutation_from_bound_contracts(tmp_path, [missing])

    path = tmp_path / "contract.json"
    path.write_text(json.dumps({"loci": {"entity": {"descriptor_permutation": [3, 1, 2, 0]}}}))
    with pytest.raises(ValueError, match="digest mismatch"):
        challenge.descriptor_permutation_from_bound_contracts(
            tmp_path, [{"path": "contract.json", "sha256": "0" * 64}]
        )


def test_bound_registry_rejects_forged_path_and_canonical_self_hash(tmp_path: Path) -> None:
    registry = {"rows": []}
    registry["registry_sha256"] = canonical_json_sha256(registry)
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(registry), encoding="utf-8")
    contract = {
        "source_registry": {
            "path": "registry.json",
            "sha256": file_sha256(path),
            "registry_sha256": registry["registry_sha256"],
        }
    }
    assert challenge.load_bound_registry(contract, tmp_path, path) == registry
    with pytest.raises(ValueError, match="exact contract binding"):
        challenge.load_bound_registry(contract, tmp_path, tmp_path / "other.json")

    registry["registry_sha256"] = "f" * 64
    path.write_text(json.dumps(registry), encoding="utf-8")
    contract["source_registry"]["sha256"] = file_sha256(path)
    contract["source_registry"]["registry_sha256"] = "f" * 64
    with pytest.raises(ValueError, match="canonical self-hash"):
        challenge.load_bound_registry(contract, tmp_path, path)


def test_manifest_and_probe_canonical_self_hashes_fail_closed() -> None:
    manifest = {"rows": []}
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    assert challenge.verify_canonical_self_hash(manifest, "manifest_sha256")
    manifest["rows"].append({"unit_id": "forged"})
    with pytest.raises(ValueError, match="canonical self-hash"):
        challenge.verify_canonical_self_hash(manifest, "manifest_sha256")

    probe = {"loci": []}
    probe["challenge_probe_sha256"] = canonical_json_sha256(probe)
    probe["loci"].append({"block": "forged"})
    with pytest.raises(ValueError, match="canonical self-hash"):
        challenge.verify_canonical_self_hash(probe, "challenge_probe_sha256")


def test_report_must_match_manifest_and_registry_digests(tmp_path: Path) -> None:
    report = {"world_id": "W01"}
    report["report_sha256"] = canonical_json_sha256(report)
    path = tmp_path / "world-report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    digest = file_sha256(path)
    evidence = {"sha256": digest, "report_sha256": report["report_sha256"]}
    manifest = {"report_path": "runs/W01/world-report.json", "report_sha256": digest}
    assert (
        challenge.validate_report_artifact(
            path, manifest, evidence, relative_path="runs/W01/world-report.json"
        )
        == report
    )

    manifest["report_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="disagrees with registry"):
        challenge.validate_report_artifact(
            path, manifest, evidence, relative_path="runs/W01/world-report.json"
        )

    manifest["report_sha256"] = digest
    report["world_id"] = "stale-mutation"
    path.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(ValueError, match="source report file digest mismatch"):
        challenge.validate_report_artifact(
            path, manifest, evidence, relative_path="runs/W01/world-report.json"
        )
