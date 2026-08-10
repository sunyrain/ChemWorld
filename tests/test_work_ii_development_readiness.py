from __future__ import annotations

import json
from pathlib import Path

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
