from __future__ import annotations

import json
from pathlib import Path

import chemworld.eval.work_ii_development_readiness as readiness
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_development_readiness import (
    WORK_II_DEVELOPMENT_READINESS_VERSION,
    validate_development_readiness_receipt,
)


def _write_receipt(
    root: Path,
    config: Path,
    trajectory: Path,
    receipt_path: Path,
) -> None:
    receipt = {
        "schema_version": WORK_II_DEVELOPMENT_READINESS_VERSION,
        "generated_at": "2026-08-10T00:00:00+00:00",
        "source_commit": "test-commit",
        "config": {
            "path": config.relative_to(root).as_posix(),
            "sha256": file_sha256(config),
            "task_id": "reaction-to-crystallization",
        },
        "schedule": {
            "world_seeds": [0],
            "prior_arms": ["opaque", "aligned_nominal", "misindexed_nominal"],
            "expected_cell_count": 3,
            "max_concurrency": 3,
        },
        "provider": {
            "provider_id": "deepseek",
            "model": "deepseek-v4-flash",
            "wire_api": "responses",
            "reasoning_effort": "high",
        },
        "checks": {"historical_current_code_audits_passed": True},
        "historical_audit": {
            "trajectory_count": 1,
            "passed_trajectory_count": 1,
            "all_trajectories_passed": True,
            "provider_call_count": 0,
            "trajectories": [
                {
                    "path": trajectory.as_posix(),
                    "sha256": file_sha256(trajectory),
                    "execution_audit_passed": True,
                }
            ],
        },
        "provider_call_count": 0,
        "ready": True,
    }
    receipt["readiness_sha256"] = canonical_json_sha256(receipt)
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")


def test_readiness_receipt_binds_commit_config_schedule_and_history(
    monkeypatch,
    tmp_path: Path,
) -> None:
    config = tmp_path / "config.json"
    config.write_text("{}", encoding="utf-8")
    trajectory = tmp_path / "trajectory.jsonl"
    trajectory.write_text('{"step":1}\n', encoding="utf-8")
    receipt = tmp_path / "readiness.json"
    _write_receipt(tmp_path, config, trajectory, receipt)
    monkeypatch.setattr(
        "chemworld.eval.work_ii_development_readiness.git_source_commit",
        lambda _root: "test-commit",
    )

    assert validate_development_readiness_receipt(tmp_path, receipt, config, [0]) == []

    trajectory.write_text('{"step":2}\n', encoding="utf-8")
    errors = validate_development_readiness_receipt(tmp_path, receipt, config, [0])
    assert any("trajectory binding changed" in error for error in errors)

    trajectory.write_text('{"step":1}\n', encoding="utf-8")
    errors = validate_development_readiness_receipt(tmp_path, receipt, config, [1])
    assert "readiness receipt seed schedule mismatch" in errors


def test_readiness_receipt_rejects_tampering_and_stale_commit(
    monkeypatch,
    tmp_path: Path,
) -> None:
    config = tmp_path / "config.json"
    config.write_text("{}", encoding="utf-8")
    trajectory = tmp_path / "trajectory.jsonl"
    trajectory.write_text('{"step":1}\n', encoding="utf-8")
    receipt = tmp_path / "readiness.json"
    _write_receipt(tmp_path, config, trajectory, receipt)
    monkeypatch.setattr(
        "chemworld.eval.work_ii_development_readiness.git_source_commit",
        lambda _root: "different-commit",
    )

    errors = validate_development_readiness_receipt(tmp_path, receipt, config, [0])
    assert "readiness receipt source commit is stale" in errors

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["ready"] = False
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    errors = validate_development_readiness_receipt(tmp_path, receipt, config, [0])
    assert "readiness receipt self-hash mismatch" in errors
    assert "readiness receipt is not passing" in errors


def test_five_seed_readiness_requires_bound_seed0_pilot(
    monkeypatch,
    tmp_path: Path,
) -> None:
    config = tmp_path / "config.json"
    config.write_text("{}", encoding="utf-8")
    trajectory = tmp_path / "trajectory.jsonl"
    trajectory.write_text('{"step":1}\n', encoding="utf-8")
    receipt = tmp_path / "readiness.json"
    _write_receipt(tmp_path, config, trajectory, receipt)
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["schedule"]["world_seeds"] = [0, 1, 2, 3, 4]
    payload["schedule"]["expected_cell_count"] = 15
    payload["readiness_sha256"] = canonical_json_sha256(
        {key: value for key, value in payload.items() if key != "readiness_sha256"}
    )
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(
        "chemworld.eval.work_ii_development_readiness.git_source_commit",
        lambda _root: "test-commit",
    )

    errors = validate_development_readiness_receipt(
        tmp_path,
        receipt,
        config,
        [0, 1, 2, 3, 4],
    )
    assert "five-seed readiness lacks a passing seed-0 expansion pilot" in errors


def test_continuation_readiness_binds_terminal_seed0_without_requalifying_it(
    monkeypatch,
    tmp_path: Path,
) -> None:
    config = tmp_path / "config.json"
    config.write_text("{}", encoding="utf-8")
    trajectory = tmp_path / "trajectory.jsonl"
    trajectory.write_text('{"step":1}\n', encoding="utf-8")
    seed0_matrix = tmp_path / "matrix_report.json"
    seed0_matrix.write_text('{"terminal_cell_count":3}\n', encoding="utf-8")
    receipt = tmp_path / "readiness.json"
    _write_receipt(tmp_path, config, trajectory, receipt)
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["schedule"].update(
        {
            "world_seeds": [1, 2, 3, 4],
            "expected_cell_count": 12,
            "execution_scope": "terminal_seed0_preserving_continuation",
        }
    )
    payload["seed0_terminal_continuation"] = {
        "passed": True,
        "semantics": "retain_seed0_outcomes_without_requalification_or_replacement",
        "bindings": [{"path": seed0_matrix.as_posix(), "sha256": file_sha256(seed0_matrix)}],
    }
    payload["readiness_sha256"] = canonical_json_sha256(
        {key: value for key, value in payload.items() if key != "readiness_sha256"}
    )
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(
        "chemworld.eval.work_ii_development_readiness.git_source_commit",
        lambda _root: "test-commit",
    )

    assert validate_development_readiness_receipt(tmp_path, receipt, config, [1, 2, 3, 4]) == []

    seed0_matrix.write_text('{"terminal_cell_count":2}\n', encoding="utf-8")
    errors = validate_development_readiness_receipt(tmp_path, receipt, config, [1, 2, 3, 4])
    assert any("seed-0 continuation binding changed" in error for error in errors)


def test_wellau_sol_medium_is_an_authorized_responses_harness(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("WELLAU_API_KEY", "test-only")
    monkeypatch.setattr(readiness, "git_worktree_dirty", lambda _root: False)
    config = tmp_path / "wellau.json"
    config.write_text(
        json.dumps(
            {
                "prior_arms": {
                    "opaque": {},
                    "aligned_nominal": {},
                    "misindexed_nominal": {},
                },
                "snapshot_stages": [
                    "pre_evidence",
                    "after_experiment_1",
                    "after_experiment_2",
                    "final",
                ],
                "campaign": {
                    "complete_experiments": 4,
                    "operation_attempt_limit": 28,
                    "vessel_start_limit": 4,
                    "final_assay_limit": 4,
                    "checkpoint_complete_experiments": [0, 1, 2, 4],
                },
                "method_resources": {
                    "complete_experiment_limit": 4,
                    "operation_limit": 28,
                    "wall_time_limit_s": 5400,
                    "input_token_limit": 2_400_000,
                    "uncached_input_token_limit": 320_000,
                    "output_token_limit": 24_000,
                    "model_call_limit": 1,
                    "checkpoint_complete_experiments": [1, 2, 4],
                },
                "execution": {
                    "max_concurrency": 3,
                    "within_cell_concurrency": 1,
                    "parallelization_unit": "same_seed_prior_arm_triplet",
                    "failure_semantics": (
                        "retain cell failures and continue every scheduled seed triplet"
                    ),
                    "systemic_failure_semantics": (
                        "stop only when all three arms fail before the first committed operation"
                    ),
                    "pilot_expansion_headroom_fraction": 0.2,
                },
                "provider": {
                    "id": "wellau",
                    "model": "gpt-5.6-sol",
                    "reasoning_effort": "medium",
                    "wire_api": "responses",
                    "env_key": "WELLAU_API_KEY",
                    "session_wall_time_limit_s": 1800,
                    "max_recovered_mcp_tool_failures": 3,
                    "max_consecutive_mcp_tool_failures": 1,
                    "max_provider_error_events": 1,
                    "progress_interval_s": 30,
                },
                "qualification": {"max_resource_rejections": 1},
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    checks = readiness._config_checks(tmp_path, config, [1])

    assert checks["responses_codex_harness_contract"] is True
    assert checks["domain_mcp_routing_catalog_frozen"] is True
    assert checks["credential_file_exists_and_is_git_ignored"] is True
    assert all(checks.values())
