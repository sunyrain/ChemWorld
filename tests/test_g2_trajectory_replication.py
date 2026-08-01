from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import pytest
from scripts import run_g2_autonomous_material_matrix as base
from scripts import run_g2_trajectory_replication as replication

from chemworld.eval.provenance import canonical_json_sha256


def _source() -> dict[str, Any]:
    return {
        "git_commit": "test-commit",
        "worktree_dirty": False,
        "material_source_tree_sha256": "test-tree",
        "protocol_file_sha256": "test-protocol",
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _environment_contract(cell: dict[str, Any]) -> dict[str, Any]:
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


def test_protocol_freezes_independent_world_replicate_and_arm_axes() -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)
    cells = replication._scheduled_cells(protocol)

    assert len(cells) == 20
    assert len({cell["cell_id"] for cell in cells}) == 20
    assert {
        (cell["world_seed"], cell["trajectory_replicate_id"])
        for cell in cells
    } == {
        (seed, replicate_id)
        for seed in (1, 3)
        for replicate_id in ("r01", "r02", "r03", "r04", "r05")
    }
    assert all(
        len(
            {
                cell["agent_seed"]
                for cell in cells
                if cell["world_seed"] == seed
                and cell["trajectory_replicate_id"] == replicate_id
            }
        )
        == 1
        for seed in (1, 3)
        for replicate_id in ("r01", "r02", "r03", "r04", "r05")
    )
    first_arm_counts = Counter(
        cell["condition_id"]
        for cell in cells
        if cell["within_pair_order"] == 1
    )
    assert first_arm_counts == Counter(
        {"anonymous_nominal_properties": 5, "opaque_codes": 5}
    )
    assert cells[0]["world_seed"] == 1
    assert cells[0]["trajectory_replicate_id"] == "r01"
    assert cells[0]["agent_seed"] == 120101
    assert cells[0]["condition_id"] == "anonymous_nominal_properties"
    assert cells[1]["condition_id"] == "opaque_codes"


def test_pair_hash_and_cell_config_bind_replicate_and_local_agent_seed() -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)
    cells = replication._scheduled_cells(protocol)
    card = base._campaign_card(protocol, qualification=False)
    limits = base._method_limits(protocol, qualification=False)
    cli = {"version": "test-codex"}
    configs = [
        base._cell_config(
            protocol=protocol,
            source=_source(),
            cli=cli,
            cell=cell,
            card=card,
            method_limits=limits,
            qualification=False,
        )
        for cell in cells[:4]
    ]

    assert configs[0]["pair_config_sha256"] == configs[1]["pair_config_sha256"]
    assert configs[0]["pair_config_sha256"] != configs[2]["pair_config_sha256"]
    for config, cell in zip(configs, cells, strict=False):
        assert config["world_seed"] == cell["world_seed"]
        assert config["trajectory_replicate_id"] == cell["trajectory_replicate_id"]
        assert config["agent_seed"] == cell["agent_seed"]
        unhashed = dict(config)
        declared = unhashed.pop("config_sha256")
        assert declared == canonical_json_sha256(unhashed)


def test_all_ten_dry_run_pair_identities_pass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)

    def inspect(
        *,
        protocol: Any,
        cell: dict[str, Any],
        card: Any,
        operation_limit: int,
    ) -> dict[str, Any]:
        del protocol, card, operation_limit
        return _environment_contract(cell)

    monkeypatch.setattr(base, "_inspect_cell_environment", inspect)
    report = replication._dry_run_report(protocol=protocol, source=_source())

    assert report["passed"] is True
    assert report["planned_pair_blocks"] == 10
    assert report["planned_cells"] == 20
    assert report["planned_physical_experiments"] == 120
    assert len(report["pair_audits"]) == 10
    assert all(
        audit["invariants"]["trajectory_replicate_id"]
        and audit["invariants"]["agent_seed"]
        for audit in report["pair_audits"]
    )


def _attempt(
    output_root: Path,
    cell_id: str,
    number: int,
    *,
    status: str,
    accepted: int,
) -> None:
    root = output_root / cell_id / f"attempt-{number:02d}"
    _write_json(root / "run_config.json", {})
    _write_json(
        root / "run_summary.json",
        {
            "run_status": status,
            "accepted_operation_count": accepted,
        },
    )


def test_attempt_state_machine_never_replaces_observed_trajectories(
    tmp_path: Path,
) -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)
    cells = replication._scheduled_cells(protocol)
    first = cells[0]

    state = replication._cell_state(
        output_root=tmp_path,
        cell=first,
        maximum_pre_action_attempts=3,
    )
    assert state["state"] == "pending"

    _attempt(
        tmp_path,
        first["cell_id"],
        1,
        status="provider_infrastructure_failure",
        accepted=0,
    )
    assert replication._cell_state(
        output_root=tmp_path,
        cell=first,
        maximum_pre_action_attempts=3,
    )["state"] == "pending_provider_retry"
    _attempt(
        tmp_path,
        first["cell_id"],
        2,
        status="provider_infrastructure_failure",
        accepted=0,
    )
    assert replication._cell_state(
        output_root=tmp_path,
        cell=first,
        maximum_pre_action_attempts=3,
    )["state"] == "pending_provider_retry"
    _attempt(
        tmp_path,
        first["cell_id"],
        3,
        status="provider_infrastructure_failure",
        accepted=0,
    )
    assert replication._cell_state(
        output_root=tmp_path,
        cell=first,
        maximum_pre_action_attempts=3,
    )["state"] == "provider_retry_exhausted"

    observed = cells[1]
    _attempt(
        tmp_path,
        observed["cell_id"],
        1,
        status="provider_infrastructure_failure",
        accepted=7,
    )
    observed_state = replication._cell_state(
        output_root=tmp_path,
        cell=observed,
        maximum_pre_action_attempts=3,
    )
    assert observed_state["state"] == "right_censored"
    assert observed_state["authoritative_attempt_dir"].endswith("attempt-01")

    method_limited = cells[2]
    _attempt(
        tmp_path,
        method_limited["cell_id"],
        1,
        status="method_resource_limit_exhausted",
        accepted=84,
    )
    assert replication._cell_state(
        output_root=tmp_path,
        cell=method_limited,
        maximum_pre_action_attempts=3,
    )["state"] == "right_censored"

    code_failure = cells[3]
    _attempt(
        tmp_path,
        code_failure["cell_id"],
        1,
        status="infrastructure_or_execution_failure",
        accepted=0,
    )
    assert replication._cell_state(
        output_root=tmp_path,
        cell=code_failure,
        maximum_pre_action_attempts=3,
    )["state"] == "audit_required"


def test_attempt_after_nonretryable_predecessor_is_rejected(tmp_path: Path) -> None:
    cell = replication._scheduled_cells(
        replication._load_protocol(replication.DEFAULT_CONFIG)
    )[0]
    _attempt(tmp_path, cell["cell_id"], 1, status="completed", accepted=9)
    _attempt(
        tmp_path,
        cell["cell_id"],
        2,
        status="provider_infrastructure_failure",
        accepted=0,
    )

    with pytest.raises(RuntimeError, match="non-retryable predecessor"):
        replication._cell_state(
            output_root=tmp_path,
            cell=cell,
            maximum_pre_action_attempts=3,
        )


def test_failure_attempt_identity_binds_replicate_agent_and_trajectory(
    tmp_path: Path,
) -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)
    cell = replication._scheduled_cells(protocol)[0]
    card = base._campaign_card(protocol, qualification=False)
    limits = base._method_limits(protocol, qualification=False)
    source = _source()
    cli = {"version": "test-codex"}
    config = base._cell_config(
        protocol=protocol,
        source=source,
        cli=cli,
        cell=cell,
        card=card,
        method_limits=limits,
        qualification=False,
    )
    attempt_root = tmp_path / cell["cell_id"] / "attempt-01"
    _write_json(attempt_root / "run_config.json", config)
    _write_json(
        attempt_root / "run_summary.json",
        {
            "run_status": "provider_infrastructure_failure",
            "cell": cell,
            "config_sha256": config["config_sha256"],
            "pair_config_sha256": config["pair_config_sha256"],
            "accepted_operation_count": 0,
        },
    )

    summary = replication._validate_attempt_identity(
        attempt_root=attempt_root,
        cell=cell,
        protocol=protocol,
        source=source,
        cli=cli,
        card=card,
        method_limits=limits,
    )
    assert summary["accepted_operation_count"] == 0

    tampered = dict(config)
    tampered["agent_seed"] += 1
    _write_json(attempt_root / "run_config.json", tampered)
    with pytest.raises(RuntimeError, match="attempt identity validation failed"):
        replication._validate_attempt_identity(
            attempt_root=attempt_root,
            cell=cell,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=limits,
        )


def _fake_materialized_summaries(
    *,
    output_root: Path,
    states: list[dict[str, Any]],
    **_: Any,
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for state in states:
        authoritative = state.get("authoritative_attempt_dir")
        if authoritative is None:
            continue
        summary = json.loads(
            (output_root / authoritative / "run_summary.json").read_text(
                encoding="utf-8"
            )
        )
        result[state["cell"]["cell_id"]] = summary
    return result


def test_main_retries_only_zero_action_provider_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str]] = []

    def run_cell(*, cell: dict[str, Any], cell_root: Path, **_: Any) -> dict[str, Any]:
        calls.append((cell["cell_id"], cell_root.name))
        _write_json(cell_root / "run_config.json", {})
        if len(calls) == 1:
            summary = {
                "run_status": "provider_infrastructure_failure",
                "accepted_operation_count": 0,
                "cell": cell,
            }
            _write_json(cell_root / "run_summary.json", summary)
            raise RuntimeError("synthetic pre-action provider failure")
        summary = {
            "run_status": "completed",
            "accepted_operation_count": 0,
            "cell": cell,
        }
        _write_json(cell_root / "run_summary.json", summary)
        return summary

    monkeypatch.setattr(replication, "_source_manifest", lambda path: _source())
    monkeypatch.setattr(base, "_codex_cli_manifest", lambda: {"version": "test"})
    monkeypatch.setattr(base, "_run_cell", run_cell)
    monkeypatch.setattr(
        replication,
        "_materialized_summaries",
        _fake_materialized_summaries,
    )
    monkeypatch.setattr(
        base,
        "_pair_audit",
        lambda left, right: {"passed": True},
    )

    output_root = tmp_path / "retry-matrix"
    assert replication.main(
        [
            "--allow-external-provider",
            "--output-root",
            str(output_root),
        ]
    ) == 0
    assert calls[:2] == [("cell-001", "attempt-01"), ("cell-001", "attempt-02")]
    assert len(calls) == 21
    manifest = json.loads(
        (output_root / "matrix_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["run_status"] == "completed"
    assert manifest["completed_cell_count"] == 20
    assert len(manifest["cells"][0]["attempts"]) == 2
    assert manifest["cells"][0]["attempts"][0]["classification"] == (
        "retryable_pre_action_provider_failure"
    )


def test_main_counts_observed_provider_failure_as_right_censored(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def run_cell(*, cell: dict[str, Any], cell_root: Path, **_: Any) -> dict[str, Any]:
        calls.append(cell["cell_id"])
        _write_json(cell_root / "run_config.json", {})
        if len(calls) == 1:
            summary = {
                "run_status": "provider_infrastructure_failure",
                "accepted_operation_count": 1,
                "cell": cell,
            }
            _write_json(cell_root / "run_summary.json", summary)
            raise RuntimeError("synthetic post-action provider failure")
        summary = {
            "run_status": "completed",
            "accepted_operation_count": 0,
            "cell": cell,
        }
        _write_json(cell_root / "run_summary.json", summary)
        return summary

    monkeypatch.setattr(replication, "_source_manifest", lambda path: _source())
    monkeypatch.setattr(base, "_codex_cli_manifest", lambda: {"version": "test"})
    monkeypatch.setattr(base, "_run_cell", run_cell)
    monkeypatch.setattr(
        replication,
        "_materialized_summaries",
        _fake_materialized_summaries,
    )
    monkeypatch.setattr(
        base,
        "_pair_audit",
        lambda left, right: {"passed": True},
    )

    output_root = tmp_path / "censored-matrix"
    assert replication.main(
        [
            "--allow-external-provider",
            "--output-root",
            str(output_root),
        ]
    ) == 2
    assert len(calls) == 20
    assert calls.count("cell-001") == 1
    manifest = json.loads(
        (output_root / "matrix_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["run_status"] == "completed_with_right_censoring"
    assert manifest["right_censored_cell_count"] == 1
    assert manifest["cells"][0]["state"] == "right_censored"
