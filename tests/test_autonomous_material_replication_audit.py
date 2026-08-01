from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from scripts import run_g2_trajectory_replication as runner

import chemworld.eval.autonomous_material_replication_audit as audit_module
from chemworld.eval.autonomous_material_replication_audit import (
    AutonomousMaterialReplicationAuditError,
    audit_autonomous_material_trajectory_replication,
    render_autonomous_material_trajectory_replication_markdown,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _environment(cell: dict[str, Any]) -> dict[str, Any]:
    seed = int(cell["world_seed"])
    return {
        "public_contract": {
            "task_contract_hash": f"task-{seed}",
            "runtime_profile_hash": f"runtime-{seed}",
            "scoring_contract_hash": f"score-{seed}",
            "observation_contract_hash": f"observation-{seed}",
            "workflow_mode": "autonomous_open_v1",
            "material_information": cell["material_information"],
        },
        "evaluator_identity": {
            "world_id": f"world-{seed}",
            "mechanism_hash": f"mechanism-{seed}",
            "electrochemical_material_family_id": "family-v2",
            "electrochemical_material_family_sha256": "family-sha",
            "electrochemical_material_instance_sha256": f"instance-{seed}",
            "observation_noise_mode": "keyed",
            "observation_noise_namespace": "paired-noise",
        },
        "initial_campaign_resources": {},
    }


def _attempt(
    root: Path,
    cell: dict[str, Any],
    number: int,
    *,
    run_status: str,
    accepted: int,
) -> dict[str, Any]:
    attempt_root = root / cell["cell_id"] / f"attempt-{number:02d}"
    pair_hash = f"pair-{cell['world_seed']}-{cell['trajectory_replicate_id']}"
    config: dict[str, Any] = {
        "protocol_id": "synthetic-replication",
        "cell": cell,
        "world_seed": cell["world_seed"],
        "trajectory_replicate_id": cell["trajectory_replicate_id"],
        "agent_seed": cell["agent_seed"],
        "condition_id": cell["condition_id"],
        "pair_config_sha256": pair_hash,
    }
    config["config_sha256"] = canonical_json_sha256(config)
    config_path = attempt_root / "run_config.json"
    summary_path = attempt_root / "run_summary.json"
    environment_path = attempt_root / "environment_contract.json"
    trajectory_path = attempt_root / "trajectory.jsonl"
    _write_json(config_path, config)
    _write_json(environment_path, _environment(cell))
    trajectory_hash: str | None = None
    if accepted:
        trajectory_path.write_text(
            "".join(json.dumps({"step": index}) + "\n" for index in range(accepted)),
            encoding="utf-8",
        )
        trajectory_hash = file_sha256(trajectory_path)
    elif trajectory_path.exists():
        trajectory_path.unlink()
    summary = {
        "run_status": run_status,
        "cell": cell,
        "config_sha256": config["config_sha256"],
        "pair_config_sha256": pair_hash,
        "trajectory_sha256": trajectory_hash,
    }
    if run_status == "completed":
        summary["behavior"] = {"operation_count": accepted}
    else:
        summary["accepted_operation_count"] = accepted
    _write_json(summary_path, summary)
    return {
        "attempt_id": attempt_root.name,
        "attempt_dir": attempt_root.relative_to(root).as_posix(),
        "run_status": run_status,
        "accepted_operation_count": accepted,
        "classification": audit_module._attempt_classification(summary),
        "config_sha256": file_sha256(config_path),
        "summary_sha256": file_sha256(summary_path),
        "trajectory_sha256": trajectory_hash,
        "environment_contract_sha256": file_sha256(environment_path),
    }


def _state(
    root: Path,
    cell: dict[str, Any],
    specifications: list[tuple[str, int]],
) -> dict[str, Any]:
    attempts = [
        _attempt(
            root,
            cell,
            index,
            run_status=status,
            accepted=accepted,
        )
        for index, (status, accepted) in enumerate(specifications, start=1)
    ]
    final_class = attempts[-1]["classification"]
    state_name = (
        "completed"
        if final_class == "completed"
        else "right_censored"
        if final_class.startswith("terminal_right_censored")
        else "audit_required"
    )
    return {
        "cell": cell,
        "state": state_name,
        "attempts": attempts,
        "authoritative_attempt_dir": attempts[-1]["attempt_dir"],
    }


def _rehash_manifest(path: Path, manifest: dict[str, Any]) -> None:
    payload = dict(manifest)
    payload.pop("manifest_sha256", None)
    manifest["manifest_sha256"] = canonical_json_sha256(payload)
    _write_json(path, manifest)


def _build_manifest(tmp_path: Path) -> Path:
    protocol = runner._load_protocol(runner.DEFAULT_CONFIG)
    cells = runner._scheduled_cells(protocol)
    states = [
        _state(tmp_path, cell, [("completed", 1)])
        for cell in cells
    ]
    manifest = {
        "schema_version": audit_module.EXPECTED_MANIFEST_VERSION,
        "protocol_id": protocol["protocol_id"],
        "world_seeds": [1, 3],
        "trajectory_replicate_ids": ["r01", "r02", "r03", "r04", "r05"],
        "source": {"material_source_tree_sha256": "synthetic-tree"},
        "cells": states,
    }
    path = tmp_path / "matrix_manifest.json"
    _rehash_manifest(path, manifest)
    return path


def _fake_completed_cell_audit(
    *,
    state_audit: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    cell = state_audit["cell"]
    seed = int(cell["world_seed"])
    replicate_id = str(cell["trajectory_replicate_id"])
    pair_hash = f"pair-{seed}-{replicate_id}"
    return {
        "cell_id": cell["cell_id"],
        "world_seed": seed,
        "trajectory_replicate_id": replicate_id,
        "agent_seed": int(cell["agent_seed"]),
        "resource_ledger": {"verified": True},
        "exact_replay": {"verified": True},
        "identity": {
            "world_seed": seed,
            "world_id": f"world-{seed}",
            "world_family_version": "world-family-v1",
            "mechanism_hash": f"mechanism-{seed}",
            "material_family_id": "family-v2",
            "material_family_sha256": "family-sha",
            "material_instance_sha256": f"instance-{seed}",
            "scoring_contract_hash": f"score-{seed}",
            "workflow_mode": "autonomous_open_v1",
            "observation_noise_mode": "keyed",
            "observation_noise_namespace": "paired-noise",
            "observation_seed": 10_000 + seed,
            "resource_card_sha256": "card-sha",
            "code_hash": "code-sha",
            "pair_config_sha256": pair_hash,
        },
    }


def _fake_right_censored_cell_audit(
    *,
    state_audit: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    cell = state_audit["cell"]
    return {
        "cell_id": cell["cell_id"],
        "world_seed": int(cell["world_seed"]),
        "trajectory_replicate_id": str(cell["trajectory_replicate_id"]),
        "condition_id": str(cell["condition_id"]),
        "resource_ledger": {"verified": True},
        "exact_replay": {"verified": True},
        "provider_sessions": {"verified": True},
    }


def _fake_paired_delta(
    nominal: dict[str, Any],
    opaque: dict[str, Any],
) -> dict[str, Any]:
    del opaque
    replicate_id = str(nominal["trajectory_replicate_id"])
    magnitude = int(replicate_id[1:]) / 10.0
    value = magnitude if int(nominal["world_seed"]) == 1 else -magnitude
    return {
        "world_seed": nominal["world_seed"],
        "nominal_cell_id": nominal["cell_id"],
        "opaque_cell_id": "synthetic-opaque",
        "nominal_minus_opaque": dict.fromkeys(
            audit_module._PAIRED_METRICS,
            value,
        ),
    }


@pytest.fixture
def synthetic_audit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        audit_module,
        "_completed_cell_audit",
        _fake_completed_cell_audit,
    )
    monkeypatch.setattr(
        audit_module,
        "_right_censored_cell_audit",
        _fake_right_censored_cell_audit,
    )
    monkeypatch.setattr(audit_module, "_paired_delta", _fake_paired_delta)


def test_replication_audit_reports_five_fresh_pairs_within_each_world(
    tmp_path: Path,
    synthetic_audit: None,
) -> None:
    del synthetic_audit
    manifest = _build_manifest(tmp_path)

    report = audit_autonomous_material_trajectory_replication(manifest)

    assert report["status"] == "completed_audited_fresh_trajectory_replication"
    assert report["matrix"]["completed_cell_count"] == 20
    assert report["matrix"]["completed_pair_count"] == 10
    assert report["matrix"]["right_censored_cell_count"] == 0
    assert report["matrix"]["all_attempt_selection_policies_verified"] is True
    assert report["matrix"]["all_physical_pairs_verified"] is True
    assert report["matrix"]["all_terminal_cells_resource_replay_verified"] is True
    seed_1 = report["within_world_descriptive_aggregates"]["1"]
    seed_3 = report["within_world_descriptive_aggregates"]["3"]
    assert seed_1["completed_pair_count"] == 5
    assert seed_1["paired_metrics"]["best_final_score"]["values"] == pytest.approx(
        [0.1, 0.2, 0.3, 0.4, 0.5]
    )
    assert seed_1["paired_metrics"]["best_final_score"][
        "sign_consistency"
    ] == pytest.approx(1.0)
    assert seed_3["paired_metrics"]["best_final_score"]["values"] == pytest.approx(
        [-0.1, -0.2, -0.3, -0.4, -0.5]
    )
    assert report["interpretation"]["selected_branch"]["branch_id"] == (
        "opposing_world_conditioned_repeatability"
    )
    assert report["interpretation"]["mapping_policy"]["sha256"]
    rendered = render_autonomous_material_trajectory_replication_markdown(report)
    assert "fresh trajectory replication" in rendered
    assert "seed 1" in rendered
    assert "seed 3" in rendered
    assert "opposing_world_conditioned_repeatability" in rendered
    assert "总体" not in rendered


@pytest.mark.parametrize(
    ("seed_1_values", "seed_3_values", "seed_1_n", "expected_branch"),
    [
        (
            [1.0, 1.0, 1.0, 1.0],
            [-1.0, -1.0, -1.0, -1.0],
            4,
            "opposing_world_conditioned_repeatability",
        ),
        (
            [1.0, -1.0, 1.0, -1.0],
            [-1.0, 1.0, -1.0, 1.0],
            4,
            "frequent_within_world_reversal",
        ),
        (
            [1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0],
            4,
            "metric_specific_or_nonopposing_repeatability",
        ),
        (
            [1.0, 1.0],
            [-1.0, -1.0, -1.0, -1.0],
            2,
            "insufficient_paired_coverage",
        ),
    ],
)
def test_outcome_blind_interpretation_policy_has_exhaustive_precedence(
    seed_1_values: list[float],
    seed_3_values: list[float],
    seed_1_n: int,
    expected_branch: str,
) -> None:
    policy = audit_module._load_interpretation_policy(
        audit_module.DEFAULT_INTERPRETATION_POLICY_PATH
    )
    metrics = [
        *policy["classification"]["core_trajectory_metrics"],
        *policy["classification"]["endpoint_diagnostics"],
    ]
    summaries = {
        "1": {
            "completed_pair_count": seed_1_n,
            "paired_metrics": {
                metric: audit_module._summary(seed_1_values) for metric in metrics
            },
        },
        "3": {
            "completed_pair_count": len(seed_3_values),
            "paired_metrics": {
                metric: audit_module._summary(seed_3_values) for metric in metrics
            },
        },
    }

    selected = audit_module._select_interpretation_branch(summaries, policy)

    assert selected["branch_id"] == expected_branch


def test_zero_action_provider_attempt_can_precede_completed_attempt(
    tmp_path: Path,
    synthetic_audit: None,
) -> None:
    del synthetic_audit
    manifest_path = _build_manifest(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cell = manifest["cells"][0]["cell"]
    manifest["cells"][0] = _state(
        tmp_path,
        cell,
        [
            ("provider_infrastructure_failure", 0),
            ("completed", 1),
        ],
    )
    _rehash_manifest(manifest_path, manifest)

    report = audit_autonomous_material_trajectory_replication(manifest_path)

    first = report["attempt_audits"][0]
    assert first["state"] == "completed"
    assert first["attempt_count"] == 2
    assert first["pre_action_provider_retry_count"] == 1
    assert first["selection_policy_verified"] is True


def test_post_action_provider_failure_is_preserved_as_right_censor(
    tmp_path: Path,
    synthetic_audit: None,
) -> None:
    del synthetic_audit
    manifest_path = _build_manifest(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cell = manifest["cells"][0]["cell"]
    manifest["cells"][0] = _state(
        tmp_path,
        cell,
        [("provider_infrastructure_failure", 1)],
    )
    _rehash_manifest(manifest_path, manifest)

    report = audit_autonomous_material_trajectory_replication(manifest_path)

    assert report["status"].endswith("with_right_censoring")
    assert report["matrix"]["completed_cell_count"] == 19
    assert report["matrix"]["right_censored_cell_count"] == 1
    assert report["matrix"]["completed_pair_count"] == 9
    assert report["matrix"]["all_terminal_cells_resource_replay_verified"] is True
    assert report["right_censored_cells"][0]["exact_replay"]["verified"] is True
    assert report["within_world_descriptive_aggregates"]["1"][
        "right_censored_pair_count"
    ] == 1
    first_pair = report["paired_trajectories"][0]
    assert first_pair["pair_complete"] is False
    assert first_pair["nominal_minus_opaque"] is None


def test_selective_replacement_after_completed_attempt_is_rejected(
    tmp_path: Path,
    synthetic_audit: None,
) -> None:
    del synthetic_audit
    manifest_path = _build_manifest(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cell = manifest["cells"][0]["cell"]
    manifest["cells"][0] = _state(
        tmp_path,
        cell,
        [("completed", 1), ("completed", 1)],
    )
    _rehash_manifest(manifest_path, manifest)

    with pytest.raises(
        AutonomousMaterialReplicationAuditError,
        match="selectively replaced",
    ):
        audit_autonomous_material_trajectory_replication(manifest_path)


def test_manifest_content_and_physical_pair_tampering_fail_closed(
    tmp_path: Path,
    synthetic_audit: None,
) -> None:
    del synthetic_audit
    manifest_path = _build_manifest(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["world_seeds"] = [3, 1]
    _write_json(manifest_path, manifest)
    with pytest.raises(
        AutonomousMaterialReplicationAuditError,
        match="content hash",
    ):
        audit_autonomous_material_trajectory_replication(manifest_path)

    manifest_path = _build_manifest(tmp_path / "physical")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    attempt = manifest["cells"][0]["attempts"][0]
    environment_path = (
        manifest_path.parent
        / attempt["attempt_dir"]
        / "environment_contract.json"
    )
    environment = json.loads(environment_path.read_text(encoding="utf-8"))
    environment["evaluator_identity"]["world_id"] = "tampered-world"
    _write_json(environment_path, environment)
    attempt["environment_contract_sha256"] = file_sha256(environment_path)
    _rehash_manifest(manifest_path, manifest)
    with pytest.raises(
        AutonomousMaterialReplicationAuditError,
        match="physical pairing failed",
    ):
        audit_autonomous_material_trajectory_replication(manifest_path)
