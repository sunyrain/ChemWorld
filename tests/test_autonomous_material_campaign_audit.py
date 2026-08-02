from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import chemworld.eval.autonomous_material_campaign_audit as audit_module
from chemworld.eval.autonomous_material_campaign_audit import (
    AutonomousMaterialCampaignAuditError,
    audit_autonomous_material_campaign,
    render_autonomous_material_campaign_markdown,
    write_autonomous_material_campaign_audit,
)
from chemworld.eval.campaign_resources import (
    CampaignResourceLedger,
    campaign_resource_event_id,
    generous_electrochemical_max_envelope_card,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _committed() -> dict[str, Any]:
    return {
        "transaction_status": "committed",
        "operation_committed": True,
    }


def _nominal_dossier() -> dict[str, Any]:
    return {
        "contract_version": "synthetic-nominal-dossier-0.1",
        "choices": {
            "solvent": [
                {
                    "action_value": index,
                    "anonymous_material_id": f"solvent-S{index}",
                    "nominal_properties": {
                        "relative_conductivity": float(index + 1),
                        "relative_cost_index": float(4 - index),
                    },
                }
                for index in range(4)
            ],
            "electrolyte_profile": [
                {
                    "action_value": index,
                    "anonymous_material_id": f"electrolyte-E{index}",
                    "nominal_properties": {
                        "bulk_conductivity_S_m": float(10 * (index + 1)),
                        "acid_concentration_mol_L": float(index) / 10.0,
                    },
                }
                for index in range(4)
            ],
        },
    }


def _build_cell(
    root: Path,
    *,
    seed: int,
    arm: str,
) -> dict[str, Any]:
    run_dir = root / f"world-{seed}-{arm}"
    run_dir.mkdir()
    mode = (
        "anonymous_nominal_properties"
        if arm == "nominal"
        else "opaque_codes"
    )
    public_material_information: dict[str, Any] = {"mode": mode}
    if arm == "nominal":
        dossier = _nominal_dossier()
        public_material_information.update(
            {
                "dossier": dossier,
                "dossier_sha256": canonical_json_sha256(dossier),
            }
        )
    pair_hash = canonical_json_sha256(
        {
            "seed": seed,
            "task": "electrochemical-conversion",
            "arm_excluded": True,
        }
    )
    config: dict[str, Any] = {
        "schema_version": "synthetic-autonomous-cell-0.1",
        "source": {"git_commit": "synthetic-code-commit"},
        "paired_config_sha256": pair_hash,
        "material_information": {"mode": mode},
        "electrochemical_material_family_id": "nominal-prior-material-family-v1",
        "electrochemical_material_family_sha256": "material-family-sha",
        "electrochemical_material_instance_sha256": f"material-instance-{seed}",
        "task": {
            "world_seed": seed,
            "electrochemical_workflow_mode": "autonomous_open_v1",
            "observation_noise_mode": "keyed",
            "observation_noise_namespace": f"paired-noise-{seed}",
            "observation_seed": 10_000 + seed,
        },
    }
    config["config_sha256"] = canonical_json_sha256(config)
    _write_json(run_dir / "run_config.json", config)

    ledger = CampaignResourceLedger(
        generous_electrochemical_max_envelope_card()
    )
    records: list[dict[str, Any]] = []
    event_index = 0
    for batch_index in range(6):
        solvent = batch_index % 3 if arm == "nominal" else 0
        electrolyte = (batch_index + 1) % 3 if arm == "nominal" else 0
        potential = 0.9 + 0.05 * batch_index if arm == "nominal" else 1.0
        actions: tuple[dict[str, Any], ...] = (
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": solvent},
            {"operation": "add_reagent", "amount_mol": 0.01},
            {
                "operation": "set_potential",
                "potential_V": potential,
                "current_mA": 80.0,
                "electrolyte_profile": electrolyte,
            },
            {"operation": "electrolyze", "duration_s": 180.0},
            {"operation": "measure", "instrument": "uvvis"},
            {
                "operation": "set_potential",
                "potential_V": potential + 0.02,
                "current_mA": 90.0,
                "electrolyte_profile": electrolyte,
            },
            {"operation": "electrolyze", "duration_s": 240.0},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        )
        for operation_index, action in enumerate(actions):
            event_index += 1
            event_id = campaign_resource_event_id(
                f"synthetic-{seed}-{arm}",
                event_index,
            )
            starts_vessel = operation_index == 0
            assert ledger.preflight(
                event_id,
                action,
                starts_vessel=starts_vessel,
            ).allowed
            outcome: dict[str, Any] = _committed()
            if action.get("instrument") == "uvvis":
                outcome["sample_consumed"] = 0.0002
            if action.get("instrument") == "final_assay":
                outcome["sample_consumed"] = 0.0003
            ledger.record_outcome(
                event_id,
                action,
                outcome,
                starts_vessel=starts_vessel,
            )
            final_score = (
                0.20
                + 0.04 * batch_index
                + (0.03 if arm == "nominal" else 0.0)
                if action.get("instrument") == "final_assay"
                else None
            )
            final_components = (
                {
                    "selective_product_yield": 0.30 + 0.02 * batch_index,
                    "electrochemical_selectivity": 0.50 + 0.01 * batch_index,
                    "electrochemical_conversion": 0.60 + 0.01 * batch_index,
                    "faradaic_efficiency": 0.70 + 0.01 * batch_index,
                    "transport_efficiency": 0.80 - 0.01 * batch_index,
                    "ohmic_efficiency": 0.75 - 0.01 * batch_index,
                    "energy_efficiency": 0.65 + 0.01 * batch_index,
                    "safety_risk": 0.10 + 0.01 * batch_index,
                    "cost": 0.20 + 0.01 * batch_index,
                }
                if action.get("instrument") == "final_assay"
                else {}
            )
            records.append(
                {
                    "schema_version": "chemworld-trajectory-0.2",
                    "step": event_index,
                    "experiment_index": batch_index,
                    "seed": seed,
                    "world_seed": seed,
                    "world_id": f"synthetic-world-{seed}",
                    "world_family_version": "synthetic-world-family-v1",
                    "mechanism_hash": f"mechanism-{seed}",
                    "electrochemical_material_family_id": (
                        "nominal-prior-material-family-v1"
                    ),
                    "electrochemical_material_family_sha256": (
                        "material-family-sha"
                    ),
                    "electrochemical_material_instance_sha256": (
                        f"material-instance-{seed}"
                    ),
                    "scoring_contract_hash": "scoring-contract-sha",
                    "action": action,
                    "operation_type": action["operation"],
                    "instrument": action.get("instrument"),
                    "transaction_status": "committed",
                    "state_delta_summary": {
                        "delta_time_s": (
                            float(action.get("duration_s", 0.0))
                            if action["operation"] == "electrolyze"
                            else 0.0
                        )
                    },
                    "evaluation_outcome": {
                        "leaderboard_score": final_score,
                        "scoring_contract_hash": "scoring-contract-sha",
                    },
                    "environment_outcome": {
                        "transaction_status": "committed",
                        "observation": final_components,
                    },
                    "leaderboard_score": final_score,
                }
            )
    trajectory_path = run_dir / "trajectory.jsonl"
    trajectory_path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    resource_snapshot = ledger.snapshot()
    resource_path = run_dir / "campaign_resource_ledger.json"
    _write_json(resource_path, resource_snapshot)
    replay_receipt = {
        "schema_version": "synthetic-exact-replay-0.1",
        "verified": True,
        "checked_steps": len(records),
        "trajectory_record_count": len(records),
        "trajectory_sha256": file_sha256(trajectory_path),
        "campaign_resource_ledger_sha256": resource_snapshot[
            "ledger_sha256"
        ],
        "mismatches": [],
    }
    _write_json(run_dir / "exact_replay.json", replay_receipt)
    summary = {
        "schema_version": "synthetic-autonomous-summary-0.1",
        "run_status": "completed",
        "config_sha256": config["config_sha256"],
        "trajectory_sha256": file_sha256(trajectory_path),
        "behavior": {
            "operation_count": len(records),
            "complete_experiment_count": 6,
        },
        "campaign_resource_ledger_path": "campaign_resource_ledger.json",
        "exact_replay_path": "exact_replay.json",
        "evaluator_provenance": {
            "electrochemical_material_family_id": (
                "nominal-prior-material-family-v1"
            ),
            "electrochemical_material_family_sha256": "material-family-sha",
            "electrochemical_material_instance_sha256": (
                f"material-instance-{seed}"
            ),
        },
        "environment_contract": {
            "public_contract": {
                "material_information": public_material_information,
            }
        },
        "method_resources": {
            "input_token_count": 1_000 + seed + (200 if arm == "nominal" else 0),
            "output_token_count": 200 + seed + (50 if arm == "nominal" else 0),
            "model_call_count": 6,
            "provider_usage_pending": False,
            "provider_usage_accounting_complete": True,
            "provider_token_accounting_complete": True,
            "provider_call_accounting_complete": True,
        },
        "provider_receipts": [
            {
                "session_id": f"session-{index}",
                "status": "completed",
                "return_code": 0,
                "terminal_reason": "experiment_complete",
                "final_payload_valid": True,
                "final_payload_status": "experiment_complete",
                "usage_complete": True,
                "lab_tool_integrity_verified_after_session": True,
                "tool_events": (
                    [
                        {
                            "classification": "lab_step",
                            "tool_name": "misleading-status-name",
                        },
                        {
                            "classification": "file_read",
                            "referenced_relative_paths": [
                                "reference/material_information.json"
                            ],
                        },
                        {
                            "classification": "material_information_read",
                            "server": "chemworld_lab",
                            "tool": "material_information",
                        },
                        {"classification": "status_read"},
                        {"classification": "history_read"},
                        {"classification": "artifact_inspect"},
                    ]
                    if index == 0
                    else []
                ),
            }
            for index in range(6)
        ],
        "provider_session_audit": {
            "passed": True,
            "target_experiment_count": 6,
            "receipt_count": 6,
            "receipt_count_matches_target": True,
            "all_receipts_passed": True,
            "all_method_resource_checks_passed": True,
        },
    }
    _write_json(run_dir / "run_summary.json", summary)
    return {
        "cell_id": f"cell-{seed}-{arm}",
        "world_seed": seed,
        "arm": mode,
        "run_dir": str(run_dir.relative_to(root)),
    }


def _build_matrix(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    cells = [
        _build_cell(tmp_path, seed=seed, arm=arm)
        for seed in range(5)
        for arm in ("opaque", "nominal")
    ]
    manifest = {
        "schema_version": "synthetic-autonomous-matrix-0.1",
        "world_seeds": list(range(5)),
        "cells": cells,
    }
    path = tmp_path / "matrix_manifest.json"
    _write_json(path, manifest)
    return path


def test_audit_validates_and_summarizes_full_paired_matrix(
    tmp_path: Path,
) -> None:
    manifest = _build_matrix(tmp_path)

    report = audit_autonomous_material_campaign(manifest)

    assert report["matrix"] == {
        "world_seeds": [0, 1, 2, 3, 4],
        "arms": ["opaque", "nominal"],
        "cell_count": 10,
        "expected_vessels_per_cell": 6,
        "all_cells_complete": True,
        "right_censored_cell_count": 0,
        "right_censored_cell_ids": [],
        "all_resource_ledgers_verified": True,
        "all_exact_replays_verified": True,
        "all_provider_sessions_verified": True,
        "all_pairs_physically_matched": True,
    }
    assert len(report["cells"]) == 10
    assert len(report["paired_worlds"]) == 5
    nominal = next(
        cell
        for cell in report["cells"]
        if cell["world_seed"] == 0 and cell["arm"] == "nominal"
    )
    assert nominal["completion"]["completion_rate"] == 1.0
    assert nominal["operations"]["count"] == 54
    assert nominal["operations"]["invalid_count"] == 0
    assert nominal["scores"]["final_score_sequence"] == pytest.approx(
        [0.23, 0.27, 0.31, 0.35, 0.39, 0.43]
    )
    assert nominal["scores"]["best_final_score"] == pytest.approx(0.43)
    assert nominal["scores"][
        "batch_final_assay_running_best_auc"
    ] == pytest.approx(0.33)
    assert nominal["scores"][
        "operation_attempt_running_best_auc"
    ] == pytest.approx(14.38 / 54.0)
    assert nominal["scores"][
        "budget_normalized_operation_attempt_running_best_auc"
    ] == pytest.approx((14.38 + 30 * 0.43) / 84.0)
    assert nominal["scores"]["operation_attempt_running_best_sequence"][
        :8
    ] == [0.0] * 8
    assert nominal["scores"]["final_assay_score_components"][
        "selective_product_yield"
    ][0] == pytest.approx(0.30)
    assert nominal["scores"]["final_assay_score_components"][
        "faradaic_efficiency"
    ][-1] == pytest.approx(0.75)
    assert nominal["scores"]["final_assay_score_components"][
        "safety_risk"
    ][-1] == pytest.approx(0.15)
    assert nominal["measurements"]["committed_count"] == 6
    assert nominal["materials"]["unique_batch_material_policy_count"] == 3
    material_endpoints = nominal["materials"]["predeclared_endpoints"]
    assert material_endpoints["first_batch_choices"] == {
        "solvent": "solvent-S0",
        "electrolyte_profile": "electrolyte-E1",
    }
    assert len(material_endpoints["first_two_batch_choices"]) == 2
    assert material_endpoints["coverage_by_field"]["solvent"][
        "material_space_coverage_fraction"
    ] == pytest.approx(0.75)
    assert material_endpoints["joint_first_choice_policy"][
        "adjacent_switch_count"
    ] == 5
    ranks = nominal["materials"]["nominal_descriptor_ranks"]
    assert ranks["available"] is True
    first_solvent_rank = ranks["fields"]["solvent"]["selections"][0][
        "descriptors"
    ]["relative_conductivity"]
    assert first_solvent_rank == {
        "value": 1.0,
        "ascending_dense_rank": 1,
        "descending_dense_rank": 4,
    }
    opaque = next(
        cell
        for cell in report["cells"]
        if cell["world_seed"] == 0 and cell["arm"] == "opaque"
    )
    assert opaque["materials"]["nominal_descriptor_ranks"][
        "available"
    ] is False
    assert "opaque arm" in opaque["materials"][
        "nominal_descriptor_ranks"
    ]["unavailable_reason"]
    adaptation = nominal["diagnostic_adaptation"]
    assert adaptation["diagnostic_event_count"] == 6
    assert adaptation["matched_event_count"] == 6
    assert adaptation["changed_control_event_count"] == 6
    first_adaptation = adaptation["events"][0]
    assert first_adaptation["next_control_operation"] == "set_potential"
    assert first_adaptation["operation_attempt_lag"] == 1
    assert first_adaptation["intervening_operation_attempt_count"] == 0
    assert set(first_adaptation["changed_fields"]) == {
        "potential_V",
        "current_mA",
    }
    assert first_adaptation["field_changes"]["potential_V"][
        "absolute_delta"
    ] == pytest.approx(0.02)
    learning = nominal["trajectory_learning"]
    discovery = learning["discovery_retention_recovery"]
    assert discovery["global_best_first_batch_number"] == 6
    assert discovery["global_best_discovery_fraction"] == pytest.approx(1.0)
    assert discovery["incumbent_update_count"] == 6
    assert discovery["online_retention_rate"] == pytest.approx(1.0)
    assert discovery["post_global_best_retention_rate"] is None
    assert discovery[
        "maximum_absolute_drawdown_from_prior_incumbent"
    ] == pytest.approx(0.0)
    assert discovery["terminal_to_global_best_ratio"] == pytest.approx(1.0)
    assert discovery["loss_episode_count"] == 0
    assert discovery["recovery_rate"] is None
    conversion = learning["diagnostic_control_to_final"]["changed_control"]
    assert conversion["eligible_batch_count"] == 5
    assert conversion["positive_next_final_delta_count"] == 5
    assert conversion["positive_next_final_delta_rate"] == pytest.approx(1.0)
    assert conversion["new_incumbent_rate"] == pytest.approx(1.0)
    assert conversion["mean_next_final_delta_vs_previous"] == pytest.approx(
        0.04
    )
    first_shift = nominal["cross_batch_policy_shifts"][0]
    assert first_shift["antecedent_final_outcome"]["score"] == pytest.approx(
        0.23
    )
    assert first_shift["antecedent_final_outcome"]["components"][
        "selective_product_yield"
    ] == pytest.approx(0.30)
    assert first_shift["material_policy_change"]["changed"] is True
    usage = nominal["method_usage"]
    assert usage["tool_event_count"] == 6
    assert usage["lab_step_count"] == 1
    assert usage["status_read_count"] == 1
    assert usage["history_read_count"] == 1
    assert usage["artifact_inspect_count"] == 1
    assert usage["material_information_file_read_count"] == 1
    assert usage["material_information_mcp_read_count"] == 1
    assert usage["material_information_reference_adherence"][
        "observed"
    ] is True
    assert usage["material_information_reference_adherence"]["read_count"] == 2
    assert nominal["provider_sessions"][
        "all_lab_tool_integrity_verified_after_session"
    ] is True
    assert report["paired_worlds"][0]["nominal_minus_opaque"][
        "best_final_score"
    ] == pytest.approx(0.03)
    assert report["paired_worlds"][0]["nominal_minus_opaque"][
        "operation_attempt_running_best_auc"
    ] == pytest.approx(46 * 0.03 / 54.0)
    assert report["paired_worlds"][0]["nominal_minus_opaque"][
        "online_incumbent_retention_rate"
    ] == pytest.approx(0.0)
    nominal_learning_aggregate = report["arm_descriptive_aggregates"][
        "nominal"
    ]["trajectory_learning"]
    assert nominal_learning_aggregate[
        "mean_global_best_discovery_fraction"
    ] == pytest.approx(1.0)
    assert nominal_learning_aggregate["loss_episode_count"] == 0
    assert nominal_learning_aggregate["diagnostic_control_to_final"][
        "changed_control"
    ]["positive_next_final_delta_rate"] == pytest.approx(1.0)
    assert report["interpretation"]["n_pairs"] == 5
    assert report["interpretation"]["confirmatory_claim_allowed"] is False
    assert "n=5" in report["interpretation"]["caveat"]

    markdown = render_autonomous_material_campaign_markdown(report)
    assert "nominal - opaque" in markdown
    assert "attempt AUC" in markdown
    assert "自主逐操作材料信息配对实验审计" in markdown
    assert "鑷" not in markdown


def test_audit_accepts_retry_aware_authoritative_attempt_directories(
    tmp_path: Path,
) -> None:
    manifest_path = _build_matrix(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for cell in manifest["cells"]:
        cell["authoritative_attempt_dir"] = cell.pop("run_dir")
    _write_json(manifest_path, manifest)

    report = audit_autonomous_material_campaign(manifest_path)

    assert report["matrix"]["cell_count"] == 10
    assert report["matrix"]["all_cells_complete"] is True


def test_direct_provider_decisions_are_qualified_per_primitive_operation() -> None:
    receipts = [
        {
            "logical_decision_index": 1,
            "status": "failed",
            "usage_complete": True,
        },
        {
            "logical_decision_index": 1,
            "status": "succeeded",
            "usage_complete": True,
        },
        {
            "logical_decision_index": 2,
            "status": "succeeded",
            "usage_complete": True,
        },
    ]
    decisions = [
        {
            "operation_index": 1,
            "attempt_count": 2,
            "attempts": receipts[:2],
            "passed": True,
        },
        {
            "operation_index": 2,
            "attempt_count": 1,
            "attempts": receipts[2:],
            "passed": True,
        },
    ]
    summary = {
        "run_status": "completed",
        "behavior": {"operation_count": 2},
        "provider_receipts": receipts,
        "method_resources": {
            "model_call_count": 3,
            "provider_usage_accounting_complete": True,
            "provider_token_accounting_complete": True,
            "provider_call_accounting_complete": True,
        },
        "provider_decision_audit": {
            "passed": True,
            "all_decisions_passed": True,
            "all_method_resource_checks_passed": True,
            "logical_indices_match_operations": True,
            "logical_decision_count": 2,
            "target_operation_count": 2,
            "receipt_count": 3,
            "decisions": decisions,
        },
    }

    qualified = audit_module._provider_session_qualification(
        summary,
        cell_id="direct-cell",
        expected_experiments=6,
    )

    assert qualified["verified"] is True
    assert qualified["qualification_kind"] == "primitive_operation_decision"
    assert qualified["logical_decision_count"] == 2


def _legacy_test_writer_emits_json_and_markdown(tmp_path: Path) -> None:
    manifest = _build_matrix(tmp_path)
    json_path = tmp_path / "audit" / "report.json"
    markdown_path = tmp_path / "audit" / "report.md"

    report = write_autonomous_material_campaign_audit(
        manifest,
        json_path=json_path,
        markdown_path=markdown_path,
    )

    assert json.loads(json_path.read_text(encoding="utf-8")) == report
    assert markdown_path.read_text(encoding="utf-8").startswith(
        "# 自主逐操作材料信息配对实验审计"
    )


def test_writer_emits_utf8_json_and_markdown(tmp_path: Path) -> None:
    manifest = _build_matrix(tmp_path)
    json_path = tmp_path / "audit" / "report.json"
    markdown_path = tmp_path / "audit" / "report.md"

    report = write_autonomous_material_campaign_audit(
        manifest,
        json_path=json_path,
        markdown_path=markdown_path,
    )

    assert json.loads(json_path.read_text(encoding="utf-8")) == report
    rendered = markdown_path.read_text(encoding="utf-8")
    assert rendered.startswith("# 自主逐操作材料信息配对实验审计")
    assert "鑷" not in rendered


def test_operation_attempt_auc_and_diagnostic_alignment_exact_definitions() -> None:
    records = [
        {
            "step": 1,
            "action": {"operation": "set_potential", "potential_V": 1.0},
            "transaction_status": "committed",
        },
        {
            "step": 2,
            "action": {"operation": "electrolyze", "duration_s": 100.0},
            "transaction_status": "committed",
        },
        {
            "step": 3,
            "action": {"operation": "measure", "instrument": "ph_meter"},
            "transaction_status": "committed",
        },
        {
            "step": 4,
            "action": {"operation": "set_potential", "potential_V": 1.2},
            "transaction_status": "invalid",
        },
        {
            "step": 5,
            "action": {"operation": "electrolyze", "duration_s": 160.0},
            "transaction_status": "committed",
        },
        {
            "step": 6,
            "action": {"operation": "measure", "instrument": "final_assay"},
            "transaction_status": "committed",
            "leaderboard_score": 0.4,
        },
        {
            "step": 7,
            "action": {"operation": "add_reagent", "amount_mol": 0.01},
            "transaction_status": "invalid",
        },
    ]

    assert audit_module._operation_attempt_running_best(records) == [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.4,
        0.4,
    ]
    adaptation = audit_module._diagnostic_adaptation_metrics(
        records,
        [0] * len(records),
    )
    event = adaptation["events"][0]
    assert event["next_control_operation"] == "electrolyze"
    assert event["operation_attempt_lag"] == 2
    assert event["intervening_operation_attempt_count"] == 1
    assert event["committed_operation_lag"] == 1
    assert event["changed_fields"] == ["duration_s"]
    assert event["field_changes"]["duration_s"] == {
        "before": 100.0,
        "after": 160.0,
        "changed": True,
        "signed_delta": 60.0,
        "absolute_delta": 60.0,
    }


def test_discovery_retention_recovery_and_conversion_exact_definitions() -> None:
    scores = [0.60, 0.30, 0.58, 0.70, 0.50, 0.64]
    final_outcomes = [
        {"batch_index": index, "score": score}
        for index, score in enumerate(scores)
    ]

    discovery = audit_module._discovery_retention_recovery_metrics(
        final_outcomes
    )

    assert discovery["retention_fraction"] == pytest.approx(0.90)
    assert discovery["global_best_score"] == pytest.approx(0.70)
    assert discovery["global_best_first_final_assay_ordinal"] == 4
    assert discovery["global_best_first_batch_number"] == 4
    assert discovery["global_best_discovery_fraction"] == pytest.approx(0.60)
    assert discovery["incumbent_update_count"] == 2
    assert discovery["online_retained_count"] == 3
    assert discovery["online_retention_rate"] == pytest.approx(3 / 5)
    assert discovery["post_global_best_retained_count"] == 1
    assert discovery["post_global_best_retention_rate"] == pytest.approx(0.5)
    assert discovery[
        "maximum_absolute_drawdown_from_prior_incumbent"
    ] == pytest.approx(0.30)
    assert discovery[
        "maximum_relative_drawdown_from_prior_incumbent"
    ] == pytest.approx(0.50)
    assert discovery["terminal_to_global_best_ratio"] == pytest.approx(
        0.64 / 0.70
    )
    assert discovery["loss_episode_count"] == 2
    assert discovery["recovered_loss_episode_count"] == 2
    assert discovery["unresolved_loss_episode_count"] == 0
    assert discovery["recovery_rate"] == pytest.approx(1.0)
    assert discovery["mean_recovery_delay_final_assays"] == pytest.approx(1.0)
    assert [
        episode["loss_start_batch_number"]
        for episode in discovery["loss_episodes"]
    ] == [2, 5]

    diagnostic_adaptation = {
        "events": [
            {
                "batch_index": batch_index,
                "matched_next_control": True,
                "comparison_available": True,
                "any_control_field_changed": True,
            }
            for batch_index in (1, 3, 4)
        ]
    }
    conversion = audit_module._diagnostic_control_to_final_metrics(
        final_outcomes,
        diagnostic_adaptation,
    )["changed_control"]
    assert conversion["eligible_batch_count"] == 3
    assert conversion["positive_next_final_delta_count"] == 1
    assert conversion["positive_next_final_delta_rate"] == pytest.approx(1 / 3)
    assert conversion["new_incumbent_count"] == 1
    assert conversion["new_incumbent_rate"] == pytest.approx(1 / 3)
    assert conversion["mean_next_final_delta_vs_previous"] == pytest.approx(
        (-0.30 + 0.12 - 0.20) / 3
    )

    unresolved = audit_module._discovery_retention_recovery_metrics(
        [
            {"batch_index": 0, "score": 0.60},
            {"batch_index": 1, "score": 0.30},
            {"batch_index": 2, "score": 0.20},
        ]
    )
    assert unresolved["loss_episode_count"] == 1
    assert unresolved["recovered_loss_episode_count"] == 0
    assert unresolved["unresolved_loss_episode_count"] == 1
    assert unresolved["recovery_rate"] == pytest.approx(0.0)
    assert unresolved["loss_episodes"][0][
        "recovery_time_right_censored"
    ] is True


def test_incomplete_batch_partition_is_explicitly_opt_in() -> None:
    records = [
        {
            "step": 1,
            "experiment_index": 0,
            "action": {"operation": "measure", "instrument": "final_assay"},
            "transaction_status": "committed",
            "leaderboard_score": 0.4,
        },
        {
            "step": 2,
            "experiment_index": 1,
            "action": {"operation": "discard_batch"},
            "transaction_status": "committed",
        },
        {
            "step": 3,
            "experiment_index": 2,
            "action": {"operation": "add_reagent", "amount_mol": 0.01},
            "transaction_status": "committed",
        },
    ]
    batch_indices = audit_module._batch_indices(records)

    with pytest.raises(
        AutonomousMaterialCampaignAuditError,
        match="closed batches",
    ):
        audit_module._final_assay_outcomes(
            records,
            batch_indices,
            expected_batches=3,
            cell_id="censored-cell",
        )

    outcomes = audit_module._final_assay_outcomes(
        records,
        batch_indices,
        expected_batches=3,
        cell_id="censored-cell",
        allow_incomplete=True,
    )
    assert [outcome["score"] for outcome in outcomes] == [0.4]


def test_hash_mismatched_optional_dossier_is_reported_unavailable(
    tmp_path: Path,
) -> None:
    manifest = _build_matrix(tmp_path)
    summary_path = tmp_path / "world-0-nominal" / "run_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["environment_contract"]["public_contract"][
        "material_information"
    ]["dossier_sha256"] = "tampered"
    _write_json(summary_path, summary)

    report = audit_autonomous_material_campaign(manifest)

    nominal = next(
        cell
        for cell in report["cells"]
        if cell["world_seed"] == 0 and cell["arm"] == "nominal"
    )
    ranks = nominal["materials"]["nominal_descriptor_ranks"]
    assert ranks["available"] is False
    assert "mismatched" in ranks["unavailable_reason"]


def test_audit_fails_closed_when_post_session_lab_tool_integrity_is_false(
    tmp_path: Path,
) -> None:
    manifest = _build_matrix(tmp_path)
    summary_path = tmp_path / "world-0-opaque" / "run_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["provider_receipts"][0][
        "lab_tool_integrity_verified_after_session"
    ] = False
    _write_json(summary_path, summary)

    with pytest.raises(
        AutonomousMaterialCampaignAuditError,
        match="lab_tool_integrity_verified_after_session",
    ):
        audit_autonomous_material_campaign(manifest)


def test_audit_fails_closed_on_physical_pairing_mismatch(
    tmp_path: Path,
) -> None:
    manifest = _build_matrix(tmp_path)
    run_dir = tmp_path / "world-2-nominal"
    config_path = run_dir / "run_config.json"
    summary_path = run_dir / "run_summary.json"
    trajectory_path = run_dir / "trajectory.jsonl"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    config["electrochemical_material_instance_sha256"] = "wrong-instance"
    config.pop("config_sha256")
    config["config_sha256"] = canonical_json_sha256(config)
    summary["config_sha256"] = config["config_sha256"]
    records = [
        json.loads(line)
        for line in trajectory_path.read_text(encoding="utf-8").splitlines()
    ]
    for record in records:
        record["electrochemical_material_instance_sha256"] = "wrong-instance"
    trajectory_path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    summary["trajectory_sha256"] = file_sha256(trajectory_path)
    replay_path = run_dir / "exact_replay.json"
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    replay["trajectory_sha256"] = summary["trajectory_sha256"]
    _write_json(replay_path, replay)
    _write_json(config_path, config)
    _write_json(summary_path, summary)

    with pytest.raises(
        AutonomousMaterialCampaignAuditError,
        match="physical pairing mismatch: material_instance_sha256",
    ):
        audit_autonomous_material_campaign(manifest)


def test_audit_reports_missing_resource_and_replay_fields_explicitly(
    tmp_path: Path,
) -> None:
    manifest = _build_matrix(tmp_path)
    summary_path = tmp_path / "world-0-opaque" / "run_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary.pop("campaign_resource_ledger_path")
    (summary_path.parent / "campaign_resource_ledger.json").unlink()
    _write_json(summary_path, summary)

    with pytest.raises(
        AutonomousMaterialCampaignAuditError,
        match="missing campaign resource ledger snapshot",
    ):
        audit_autonomous_material_campaign(manifest)

    manifest = _build_matrix(tmp_path / "second")
    summary_path = tmp_path / "second" / "world-0-opaque" / "run_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary.pop("exact_replay_path")
    (summary_path.parent / "exact_replay.json").unlink()
    _write_json(summary_path, summary)
    with pytest.raises(
        AutonomousMaterialCampaignAuditError,
        match="missing exact trajectory replay receipt",
    ):
        audit_autonomous_material_campaign(manifest)
