from __future__ import annotations

import hashlib
import json
from pathlib import Path

from chemworld.eval.rl_training_writer_audit import (
    audit_rl_training_writer_artifacts,
)
from chemworld.rl.checkpoint_contract import (
    RL_CHECKPOINT_MANIFEST_SCHEMA_VERSION,
    RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION,
)
from chemworld.rl.observation_contract import rl_observation_contract

TASK_ID = "flow-reaction-optimization"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifacts(tmp_path: Path) -> dict[str, object]:
    observation = rl_observation_contract(TASK_ID)
    checkpoint = tmp_path / "checkpoints" / "ppo-probe_2_steps.zip"
    checkpoint.parent.mkdir(parents=True)
    checkpoint.write_bytes(b"checkpoint")
    checkpoint_sha = _sha256(checkpoint)
    sidecar = {
        "schema_version": RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION,
        "algorithm": "ppo",
        "task_id": TASK_ID,
        "training_environment_step_count": 2,
        "checkpoint": checkpoint.name,
        "checkpoint_sha256": checkpoint_sha,
        "observation_contract_hash": observation["contract_hash"],
        "action_contract_hash": "a" * 64,
        "training_reward_contract_hash": "b" * 64,
        "policy_distribution_contract_hash": "c" * 64,
        "shape_only_compatible": False,
        "legacy_checkpoint_compatible": False,
    }
    sidecar_path = checkpoint.with_suffix(".manifest.json")
    sidecar_path.write_text(
        json.dumps(sidecar, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    final_checkpoint = tmp_path / "ppo-probe.zip"
    final_checkpoint.write_bytes(b"final-checkpoint")
    return {
        "schema_version": RL_CHECKPOINT_MANIFEST_SCHEMA_VERSION,
        "algorithm": "ppo",
        "task_id": TASK_ID,
        "observation_contract": observation,
        "observation_contract_hash": observation["contract_hash"],
        "observation_shape": observation["shape"],
        "action_contract_hash": "a" * 64,
        "training_reward_contract_hash": "b" * 64,
        "policy_distribution_contract_hash": "c" * 64,
        "checkpoint_compatibility": {
            "policy": "exact_contract_hash_match",
            "shape_only_compatible": False,
            "legacy_checkpoint_compatible": False,
        },
        "checkpoint": final_checkpoint.name,
        "checkpoint_sha256": _sha256(final_checkpoint),
        "periodic_checkpoint_artifacts": [
            {
                "path": checkpoint.relative_to(tmp_path).as_posix(),
                "sha256": checkpoint_sha,
                "artifact_type": "checkpoint",
            }
        ],
        "periodic_checkpoint_contract_manifests": [
            {
                "path": sidecar_path.relative_to(tmp_path).as_posix(),
                "sha256": _sha256(sidecar_path),
            }
        ],
    }


def test_current_writer_contract_accepts_exact_manifest_and_sidecars(
    tmp_path: Path,
) -> None:
    report = audit_rl_training_writer_artifacts(
        _artifacts(tmp_path),
        output_root=tmp_path,
        task_id=TASK_ID,
        algorithm="ppo",
    )

    assert report["writer_ready"] is True
    assert report["failed_checks"] == []
    assert report["periodic_checkpoint_count"] == 1
    assert report["periodic_sidecar_count"] == 1


def test_writer_contract_rejects_legacy_schema_and_observation_drift(
    tmp_path: Path,
) -> None:
    manifest = _artifacts(tmp_path)
    manifest["schema_version"] = "chemworld-rl-checkpoint-0.2"
    manifest["observation_contract_hash"] = "0" * 64

    report = audit_rl_training_writer_artifacts(
        manifest,
        output_root=tmp_path,
        task_id=TASK_ID,
        algorithm="ppo",
    )

    assert report["writer_ready"] is False
    assert "manifest_schema_current" in report["failed_checks"]
    assert "observation_contract_hash_exact" in report["failed_checks"]


def test_writer_contract_rejects_unsafe_sidecar_path(tmp_path: Path) -> None:
    manifest = _artifacts(tmp_path)
    manifest["periodic_checkpoint_contract_manifests"] = [
        {"path": "../outside.json", "sha256": "a" * 64}
    ]

    report = audit_rl_training_writer_artifacts(
        manifest,
        output_root=tmp_path,
        task_id=TASK_ID,
        algorithm="ppo",
    )

    assert report["writer_ready"] is False
    assert report["checks"]["all_periodic_sidecars_runtime_compatible"] is False
