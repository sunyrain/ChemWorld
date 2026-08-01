from __future__ import annotations

import json

import pytest
from scripts import run_g2_autonomous_material_triarm as triarm


def test_triarm_protocol_freezes_three_conditions_and_counterbalanced_schedule() -> None:
    protocol = triarm._load_protocol(triarm.DEFAULT_CONFIG)
    cells = triarm._scheduled_cells(protocol)

    assert len(cells) == 15
    assert [cell["world_seed"] for cell in cells[:6]] == [0, 0, 0, 1, 1, 1]
    assert [cell["arm"] for cell in cells[:3]] == [
        "unknown",
        "known",
        "mismatched",
    ]
    assert [cell["condition_id"] for cell in cells[:3]] == [
        "opaque_codes",
        "anonymous_nominal_properties",
        "anonymous_misindexed_properties",
    ]
    assert cells[3]["arm"] == "known"
    assert cells[4]["arm"] == "mismatched"
    assert cells[5]["arm"] == "unknown"
    assert [cell["world_seed"] for cell in triarm._scheduled_cells(protocol, [0])] == [
        0,
        0,
        0,
    ]


def test_triarm_dry_run_artifact_passes_all_world_invariants() -> None:
    protocol = triarm._load_protocol(triarm.DEFAULT_CONFIG)
    cells = triarm._scheduled_cells(protocol)
    inspected = []
    for cell in cells:
        inspected.append(
            {
                "cell": cell,
                "environment_contract": {
                    "public_contract": {
                        "task_contract_hash": "task",
                        "runtime_profile_hash": "runtime",
                        "scoring_contract_hash": "score",
                        "observation_contract_hash": "observation",
                        "workflow_mode": "autonomous_open_v1",
                    },
                    "evaluator_identity": {
                        "world_id": f"world-{cell['world_seed']}",
                        "mechanism_hash": f"mechanism-{cell['world_seed']}",
                        "electrochemical_material_family_id": "family",
                        "electrochemical_material_family_sha256": "family-sha",
                        "electrochemical_material_instance_sha256": (
                            f"instance-{cell['world_seed']}"
                        ),
                        "observation_noise_mode": "keyed",
                        "observation_noise_namespace": "triarm",
                    },
                },
            }
        )

    audits = triarm._triarm_audits(inspected)
    assert len(audits) == 5
    assert all(item["passed"] for item in audits)


def test_triarm_analysis_computes_paired_contrasts_and_wrong_prior_metrics() -> None:
    def result(
        *,
        arm: str,
        condition_id: str,
        first: int,
        last: int,
        scores: list[float],
    ) -> dict[str, object]:
        return {
            "run_status": "completed",
            "world_seed": 0,
            "arm": arm,
            "condition_id": condition_id,
            "exact_replay_verified": True,
            "behavior": {
                "operation_count": 24,
                "closed_batch_count": 4,
                "invalid_operation_count": 0,
                "resource_rejection_count": 0,
                "terminal_scores": scores,
                "best_final_score": max(scores),
                "mean_final_score": sum(scores) / len(scores),
                "incumbent_auc_per_operation": 0.5,
                "experiments": [
                    {"solvent_choices": [first]},
                    {"solvent_choices": [last]},
                    {"solvent_choices": [last]},
                    {"solvent_choices": [last]},
                ],
            },
        }

    results = [
        result(
            arm="unknown",
            condition_id="opaque_codes",
            first=0,
            last=3,
            scores=[0.2, 0.3, 0.4, 0.5],
        ),
        result(
            arm="known",
            condition_id="anonymous_nominal_properties",
            first=1,
            last=3,
            scores=[0.4, 0.5, 0.6, 0.7],
        ),
        result(
            arm="mismatched",
            condition_id="anonymous_misindexed_properties",
            first=3,
            last=1,
            scores=[0.3, 0.35, 0.55, 0.65],
        ),
    ]
    analysis = triarm._triarm_analysis(
        results,
        operation_limit=24,
        target_batches=4,
    )
    assert analysis is not None
    assert analysis["all_lifecycles_completed"] is True
    assert analysis["all_exact_replays_verified"] is True
    assert analysis["wrong_prior"]["manipulation_visible"] is True
    assert analysis["wrong_prior"]["recovery_visible"] is True
    assert analysis["paired_best_final_score"]["known_minus_unknown"]["mean"] == pytest.approx(0.2)


def test_triarm_manifest_embeds_analysis_for_completed_cells() -> None:
    protocol = triarm._load_protocol(triarm.DEFAULT_CONFIG)
    cells = triarm._scheduled_cells(protocol, [0])
    identities = {
        "world_id": "world-0",
        "mechanism_hash": "mechanism-0",
        "electrochemical_material_family_id": "family",
        "electrochemical_material_family_sha256": "family-sha",
        "electrochemical_material_instance_sha256": "instance-0",
        "observation_noise_mode": "keyed",
        "observation_noise_namespace": "triarm",
    }
    public = {
        "task_contract_hash": "task",
        "runtime_profile_hash": "runtime",
        "scoring_contract_hash": "score",
        "observation_contract_hash": "observation",
        "workflow_mode": "autonomous_open_v1",
    }
    results = []
    scores = {
        "opaque_codes": [0.2, 0.3, 0.4, 0.5],
        "anonymous_nominal_properties": [0.4, 0.5, 0.6, 0.7],
        "anonymous_misindexed_properties": [0.3, 0.35, 0.55, 0.65],
    }
    for cell in cells:
        values = scores[cell["condition_id"]]
        results.append(
            {
                "run_status": "completed",
                "cell": cell,
                "world_seed": 0,
                "condition_id": cell["condition_id"],
                "arm": cell["condition_id"],
                "config_sha256": "config",
                "trajectory_sha256": "trajectory",
                "campaign_resource_ledger_sha256": "ledger",
                "exact_replay_verified": True,
                "environment_contract": {
                    "evaluator_identity": identities,
                    "public_contract": public,
                },
                "behavior": {
                    "operation_count": 24,
                    "closed_batch_count": 4,
                    "invalid_operation_count": 0,
                    "resource_rejection_count": 0,
                    "terminal_scores": values,
                    "best_final_score": max(values),
                    "mean_final_score": sum(values) / len(values),
                    "incumbent_auc_per_operation": 0.5,
                    "experiments": [
                        {"solvent_choices": [1 if cell["arm"] == "known" else 3]},
                        {"solvent_choices": [1 if cell["arm"] == "mismatched" else 3]},
                        {"solvent_choices": [1]},
                        {"solvent_choices": [1]},
                    ],
                },
            }
        )
    manifest = triarm._manifest(
        protocol=protocol,
        source={
            "material_source_tree_sha256": "tree",
            "protocol_file_sha256": "protocol",
        },
        cli={"version": "test"},
        cells=results,
        audits=triarm._triarm_audits(results),
        status="completed",
        dry_run=False,
    )
    assert manifest["analysis"]["cell_count"] == 3
    assert manifest["completed_cell_count"] == 3
    assert manifest["all_triarm_audits_passed"] is True


def test_triarm_resume_accepts_only_a_validated_prefix(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    protocol = triarm._load_protocol(triarm.DEFAULT_CONFIG)
    cells = triarm._scheduled_cells(protocol, [0])
    root = tmp_path / "resume"
    root.mkdir()
    (root / "cell-01").mkdir()
    manifest = {
        "runner_version": triarm.RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "world_seeds": [0],
        "source": {
            "material_source_tree_sha256": "tree",
            "protocol_file_sha256": "protocol",
        },
        "codex_cli": {"version": "test"},
        "cells": [
            {
                "cell_id": "cell-01",
                "world_seed": 0,
                "condition_id": cells[0]["condition_id"],
                "run_dir": "cell-01",
            }
        ],
    }
    (root / "triarm_manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    monkeypatch.setattr(
        triarm.matrix,
        "_validated_resume_result",
        lambda **kwargs: {
            "run_status": "completed",
            "cell": kwargs["cell"],
            "world_seed": 0,
            "condition_id": kwargs["cell"]["condition_id"],
            "arm": kwargs["cell"]["arm"],
        },
    )
    results = triarm._load_resume_results(
        root,
        protocol=protocol,
        source={
            "material_source_tree_sha256": "tree",
            "protocol_file_sha256": "protocol",
        },
        cli={"version": "test"},
        card=triarm.matrix._campaign_card(protocol, qualification=False),
        method_limits=triarm.matrix._method_limits(protocol, qualification=False),
        scheduled_cells=cells,
    )
    assert len(results) == 1
    assert results[0]["cell"]["cell_id"] == "cell-01"
