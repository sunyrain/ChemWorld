"""Behavioral compatibility audit for formal RL checkpoint writers."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Literal

from chemworld.eval.formal_protocol_v0_4 import load_formal_protocol
from chemworld.rl.checkpoint_contract import (
    RL_CHECKPOINT_MANIFEST_SCHEMA_VERSION,
    RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION,
)
from chemworld.rl.formal_training import build_formal_allocation
from chemworld.rl.observation_contract import rl_observation_contract
from chemworld.rl.training import train_sb3_baseline

ROOT = Path(__file__).resolve().parents[3]
RL_TRAINING_WRITER_AUDIT_VERSION = "chemworld-rl-training-writer-audit-0.4"
PROBE_TASK_ID = "flow-reaction-optimization"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _inside(root: Path, relative: Any) -> Path | None:
    if not isinstance(relative, str) or not relative:
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def audit_rl_training_writer_artifacts(
    manifest: Mapping[str, Any],
    *,
    output_root: str | Path,
    task_id: str,
    algorithm: Literal["ppo", "sac"],
) -> dict[str, Any]:
    """Verify that one emitted checkpoint family is accepted by current readers."""

    root = Path(output_root).resolve()
    observation = rl_observation_contract(task_id)
    compatibility = manifest.get("checkpoint_compatibility")
    compatibility = compatibility if isinstance(compatibility, Mapping) else {}
    checkpoint = _inside(root, manifest.get("checkpoint"))
    checkpoint_sha = manifest.get("checkpoint_sha256")
    checks: dict[str, bool] = {
        "manifest_schema_current": manifest.get("schema_version")
        == RL_CHECKPOINT_MANIFEST_SCHEMA_VERSION,
        "algorithm_exact": manifest.get("algorithm") == algorithm,
        "task_exact": manifest.get("task_id") == task_id,
        "observation_contract_exact": manifest.get("observation_contract") == observation,
        "observation_contract_hash_exact": manifest.get("observation_contract_hash")
        == observation["contract_hash"],
        "observation_shape_exact": manifest.get("observation_shape") == observation["shape"],
        "shape_only_compatibility_forbidden": compatibility.get("shape_only_compatible") is False,
        "legacy_compatibility_forbidden": compatibility.get("legacy_checkpoint_compatible")
        is False,
        "checkpoint_digest_bound": checkpoint is not None
        and checkpoint.is_file()
        and _is_sha256(checkpoint_sha)
        and _sha256(checkpoint) == checkpoint_sha,
        "action_contract_hash_present": _is_sha256(manifest.get("action_contract_hash")),
        "reward_contract_hash_present": _is_sha256(manifest.get("training_reward_contract_hash")),
        "policy_distribution_hash_well_formed": manifest.get("policy_distribution_contract_hash")
        is None
        or _is_sha256(manifest.get("policy_distribution_contract_hash")),
    }

    raw_artifacts = manifest.get("periodic_checkpoint_artifacts")
    artifacts = (
        [
            item
            for item in raw_artifacts
            if isinstance(item, Mapping) and item.get("artifact_type") == "checkpoint"
        ]
        if isinstance(raw_artifacts, list)
        else []
    )
    raw_sidecars = manifest.get("periodic_checkpoint_contract_manifests")
    sidecar_refs = (
        [item for item in raw_sidecars if isinstance(item, Mapping)]
        if isinstance(raw_sidecars, list)
        else []
    )
    checks["periodic_sidecar_count_exact"] = bool(artifacts) and len(sidecar_refs) == len(artifacts)

    artifact_by_name = {Path(str(item.get("path"))).name: item for item in artifacts}
    sidecar_results: list[dict[str, Any]] = []
    for reference in sidecar_refs:
        path = _inside(root, reference.get("path"))
        sidecar_checks: dict[str, bool] = {
            "path_safe_and_present": path is not None and path.is_file(),
            "sidecar_digest_bound": False,
            "schema_current": False,
            "algorithm_exact": False,
            "task_exact": False,
            "observation_contract_hash_exact": False,
            "action_contract_hash_exact": False,
            "reward_contract_hash_exact": False,
            "policy_distribution_hash_exact": False,
            "shape_only_compatibility_forbidden": False,
            "legacy_compatibility_forbidden": False,
            "checkpoint_digest_bound": False,
        }
        payload: Mapping[str, Any] = {}
        if path is not None and path.is_file():
            sidecar_checks["sidecar_digest_bound"] = _is_sha256(
                reference.get("sha256")
            ) and _sha256(path) == reference.get("sha256")
            try:
                loaded = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                loaded = None
            if isinstance(loaded, Mapping):
                payload = loaded
        sidecar_checks.update(
            {
                "schema_current": payload.get("schema_version")
                == RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION,
                "algorithm_exact": payload.get("algorithm") == algorithm,
                "task_exact": payload.get("task_id") == task_id,
                "observation_contract_hash_exact": payload.get("observation_contract_hash")
                == observation["contract_hash"],
                "action_contract_hash_exact": payload.get("action_contract_hash")
                == manifest.get("action_contract_hash"),
                "reward_contract_hash_exact": payload.get("training_reward_contract_hash")
                == manifest.get("training_reward_contract_hash"),
                "policy_distribution_hash_exact": payload.get("policy_distribution_contract_hash")
                == manifest.get("policy_distribution_contract_hash"),
                "shape_only_compatibility_forbidden": payload.get("shape_only_compatible") is False,
                "legacy_compatibility_forbidden": payload.get("legacy_checkpoint_compatible")
                is False,
            }
        )
        artifact = artifact_by_name.get(str(payload.get("checkpoint")))
        sidecar_checks["checkpoint_digest_bound"] = bool(
            artifact
            and payload.get("checkpoint_sha256") == artifact.get("sha256")
            and _is_sha256(artifact.get("sha256"))
        )
        sidecar_results.append(
            {
                "path": reference.get("path"),
                "checks": sidecar_checks,
                "passed": all(sidecar_checks.values()),
            }
        )
    checks["all_periodic_sidecars_runtime_compatible"] = bool(sidecar_results) and all(
        item["passed"] is True for item in sidecar_results
    )
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "writer_ready": not failed,
        "checks": checks,
        "failed_checks": failed,
        "observation_contract_hash": observation["contract_hash"],
        "periodic_checkpoint_count": len(artifacts),
        "periodic_sidecar_count": len(sidecar_refs),
        "periodic_sidecars": sidecar_results,
    }


def _source_probe(root: Path) -> dict[str, Any]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=root,
        text=True,
    ).strip()
    return {"commit": commit, "clean": not status}


def run_rl_training_writer_probe(*, root: str | Path = ROOT) -> dict[str, Any]:
    """Train two tiny public probes and audit the artifacts they actually emit."""

    repository = Path(root).resolve()
    source = _source_probe(repository)
    protocol = load_formal_protocol(repository / "configs/benchmark/formal_protocol_v0.4.json")
    allocation = build_formal_allocation(
        protocol,
        task_id=PROBE_TASK_ID,
        name="train",
    )
    algorithms: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="chemworld-rl-writer-") as temporary:
        temporary_root = Path(temporary)
        for algorithm in ("ppo", "sac"):
            output = temporary_root / algorithm
            kwargs: dict[str, Any]
            if algorithm == "ppo":
                kwargs = {"n_steps": 2, "batch_size": 2, "n_epochs": 1}
            else:
                kwargs = {
                    "buffer_size": 10,
                    "learning_starts": 1,
                    "batch_size": 1,
                    "train_freq": 1,
                    "gradient_steps": 1,
                }
            try:
                manifest = train_sb3_baseline(
                    algorithm=algorithm,
                    task_id=PROBE_TASK_ID,
                    allocation=allocation,
                    total_timesteps=2,
                    model_seed=0,
                    output_dir=output,
                    algorithm_kwargs=kwargs,
                    operation_budget=2,
                    checkpoint_steps=(2,),
                    save_replay_buffer=algorithm == "sac",
                    progress_interval_steps=2,
                    torch_num_threads=1,
                )
            except Exception as exc:  # pragma: no cover - exercised by real runtimes
                algorithms[algorithm] = {
                    "writer_ready": False,
                    "probe_exception_type": type(exc).__name__,
                    "failed_checks": ["probe_execution"],
                }
            else:
                algorithms[algorithm] = audit_rl_training_writer_artifacts(
                    manifest,
                    output_root=output,
                    task_id=PROBE_TASK_ID,
                    algorithm=algorithm,
                )
    writer_ready = bool(algorithms) and all(
        item.get("writer_ready") is True for item in algorithms.values()
    )
    return {
        "schema_version": RL_TRAINING_WRITER_AUDIT_VERSION,
        "status": "writer_contract_ready" if writer_ready else "writer_contract_blocked",
        "writer_contract_ready": writer_ready,
        "formal_training_allowed": writer_ready,
        "benchmark_claim_allowed": False,
        "formal_results_present": False,
        "bench_accessed": False,
        "reference_search_used": False,
        "probe_task_id": PROBE_TASK_ID,
        "probe_environment_step_count": 4,
        "required_checkpoint_manifest_schema": RL_CHECKPOINT_MANIFEST_SCHEMA_VERSION,
        "required_periodic_sidecar_schema": RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION,
        "source_commit": source["commit"],
        "source_tree_clean": source["clean"],
        "source_files": {
            "src/chemworld/rl/training.py": _sha256(repository / "src/chemworld/rl/training.py"),
            "src/chemworld/rl/checkpoint_contract.py": _sha256(
                repository / "src/chemworld/rl/checkpoint_contract.py"
            ),
            "src/chemworld/rl/observation_contract.py": _sha256(
                repository / "src/chemworld/rl/observation_contract.py"
            ),
        },
        "algorithms": algorithms,
    }


__all__ = [
    "PROBE_TASK_ID",
    "RL_TRAINING_WRITER_AUDIT_VERSION",
    "audit_rl_training_writer_artifacts",
    "run_rl_training_writer_probe",
]
