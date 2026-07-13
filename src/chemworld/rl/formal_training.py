"""Resumable, preregistered PPO Train/Dev execution for formal RL v0.4."""

from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

from chemworld.eval.formal_rl import RLCheckpointBinding, file_sha256
from chemworld.eval.resource_accounting_v0_4 import (
    RL_TRAINING_RESOURCE_VERSION,
    audit_rl_training_resource,
)
from chemworld.rl.environment import RLWorldAllocation
from chemworld.rl.evaluation import evaluate_sb3_checkpoint
from chemworld.rl.training import train_sb3_baseline

PPO_PLAN_VERSION = "chemworld-formal-ppo-training-plan-0.4"
PPO_JOB_SUMMARY_VERSION = "chemworld-formal-ppo-job-summary-0.4"
PPO_CHECKPOINT_INDEX_VERSION = "chemworld-formal-rl-checkpoint-index-0.4"
PPO_REPORT_VERSION = "chemworld-formal-ppo-development-report-0.4"
DEFAULT_PLAN_PATH = Path("configs/methods/rl_v0.4/ppo_training_plan.json")
DEFAULT_METHODS_PATH = Path("configs/methods/rl_v0.4/rl_methods.json")
DEFAULT_FORMAL_PROTOCOL_PATH = Path("configs/benchmark/formal_protocol_v0.4.json")


class FormalPPOTrainingError(RuntimeError):
    """Raised when preregistration, retained evidence, or selection fails closed."""


@dataclass(frozen=True, order=True)
class FormalPPOJob:
    task_id: str
    model_seed: int

    @property
    def job_id(self) -> str:
        return f"ppo-{self.task_id}-seed{self.model_seed}"


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FormalPPOTrainingError(f"cannot load {label}: {path}") from exc
    if not isinstance(payload, dict):
        raise FormalPPOTrainingError(f"{label} must be a JSON object")
    return payload


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(dict(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _inside(root: Path, relative: str | Path, label: str) -> Path:
    repository = root.resolve()
    candidate = (repository / relative).resolve()
    try:
        candidate.relative_to(repository)
    except ValueError as exc:
        raise FormalPPOTrainingError(f"{label} escapes the repository root") from exc
    return candidate


def load_training_plan(path: str | Path = DEFAULT_PLAN_PATH) -> dict[str, Any]:
    return _load_object(Path(path), "formal PPO training plan")


def validate_training_plan(
    plan: Mapping[str, Any],
    *,
    formal_protocol: Mapping[str, Any],
    methods_config: Mapping[str, Any],
) -> dict[str, bool]:
    """Validate every frozen task, split, budget, and no-access condition."""

    formal_tasks_raw = formal_protocol.get("task_roles", {}).get("formal_core", {})
    task_metrics = (
        {
            str(task_id): str(payload.get("primary_metric"))
            for task_id, payload in formal_tasks_raw.items()
            if isinstance(payload, Mapping)
        }
        if isinstance(formal_tasks_raw, Mapping)
        else {}
    )
    configured_tasks = plan.get("formal_core_tasks")
    training = plan.get("training", {})
    infrastructure = plan.get("infrastructure", {})
    development = plan.get("development_selection", {})
    execution = plan.get("execution", {})
    boundary = plan.get("evidence_boundary", {})
    method_training = methods_config.get("training", {})
    ppo_method = method_training.get("ppo", {}) if isinstance(method_training, Mapping) else {}
    formal_splits = formal_protocol.get("split_contract", {})
    split_bindings = plan.get("split_bindings", {})
    rollout_quantum = int(training.get("hyperparameters", {}).get("n_steps", 0)) * int(
        infrastructure.get("parallel_environments", 0)
    )
    checkpoint_steps = training.get("checkpoint_steps")
    checks = {
        "schema_version": plan.get("schema_version") == PPO_PLAN_VERSION,
        "algorithm": plan.get("algorithm") == "ppo",
        "exact_task_primary_metrics": configured_tasks == task_metrics,
        "exact_model_seeds": plan.get("model_seeds") == method_training.get("model_seeds"),
        "exact_training_budget": training.get("requested_environment_steps_per_run")
        == ppo_method.get("requested_environment_steps"),
        "exact_checkpoint_steps": checkpoint_steps == ppo_method.get("checkpoint_steps"),
        "exact_hyperparameters": training.get("hyperparameters")
        == ppo_method.get("hyperparameters"),
        "rollout_quantum_exact": bool(
            rollout_quantum > 0
            and isinstance(checkpoint_steps, list)
            and all(
                isinstance(step, int) and step % rollout_quantum == 0 for step in checkpoint_steps
            )
        ),
        "train_split_exact": isinstance(split_bindings, Mapping)
        and split_bindings.get("train") == formal_splits.get("train"),
        "dev_split_exact": isinstance(split_bindings, Mapping)
        and split_bindings.get("dev") == formal_splits.get("dev"),
        "reference_and_bench_forbidden": isinstance(split_bindings, Mapping)
        and split_bindings.get("reference_search_access") == "forbidden"
        and split_bindings.get("bench_access") == "forbidden",
        "dev_only_deterministic_selection": isinstance(development, Mapping)
        and development.get("deterministic_policy") is True
        and development.get("episodes_per_candidate") == 20,
        "exact_matrix_counts": isinstance(execution, Mapping)
        and execution.get("expected_training_run_count") == len(task_metrics) * 5
        and execution.get("expected_candidate_checkpoint_count") == len(task_metrics) * 15
        and execution.get("expected_selected_checkpoint_count") == len(task_metrics),
        "cpu_execution_declared": isinstance(infrastructure, Mapping)
        and infrastructure.get("device") == "cpu",
        "no_bench_or_reference_feedback": isinstance(boundary, Mapping)
        and boundary.get("bench_finetuning_used") is False
        and boundary.get("reference_search_used") is False
        and boundary.get("reference_repositories_used") == []
        and boundary.get("formal_results_present") is False
        and boundary.get("benchmark_claim_allowed") is False,
        "parent_and_sac_remain_pending": isinstance(boundary, Mapping)
        and boundary.get("parent_task_complete") is False
        and boundary.get("sac_training_in_scope") is False,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise FormalPPOTrainingError("formal PPO plan validation failed: " + ", ".join(failed))
    return checks


def build_formal_allocation(
    formal_protocol: Mapping[str, Any],
    *,
    task_id: str,
    name: Literal["train", "dev"],
) -> RLWorldAllocation:
    """Build a public Train or Dev allocation directly from formal protocol v0.4."""

    split = formal_protocol.get("split_contract", {}).get(name, {})
    world = formal_protocol.get("world_family_contract", {})
    axes = world.get("axes", {}).get(task_id)
    severities = world.get("public_development_severities", {}).get(name)
    if (
        not isinstance(split, Mapping)
        or not isinstance(axes, list)
        or not isinstance(severities, Mapping)
    ):
        raise FormalPPOTrainingError(f"formal {name} allocation is incomplete for {task_id}")
    seed_range = split.get("base_seeds")
    if not isinstance(seed_range, Mapping):
        raise FormalPPOTrainingError(f"formal {name} seed range is invalid")
    cells = tuple(
        (str(axis_id), str(mode), float(severity))
        for axis_id in axes
        for mode, values in severities.items()
        if isinstance(values, list)
        for severity in values
    )
    return RLWorldAllocation(
        name=name,
        task_id=task_id,
        base_seeds=tuple(range(int(seed_range["start"]), int(seed_range["stop_inclusive"]) + 1)),
        cells=cells,
        namespace_id=str(split.get("namespace_id")),
    )


def build_jobs(plan: Mapping[str, Any]) -> tuple[FormalPPOJob, ...]:
    tasks = plan.get("formal_core_tasks")
    seeds = plan.get("model_seeds")
    if not isinstance(tasks, Mapping) or not isinstance(seeds, list):
        raise FormalPPOTrainingError("formal PPO task/seed matrix is invalid")
    return tuple(FormalPPOJob(str(task_id), int(seed)) for task_id in tasks for seed in seeds)


def _artifact_root(root: Path, plan: Mapping[str, Any]) -> Path:
    execution = plan.get("execution")
    if not isinstance(execution, Mapping):
        raise FormalPPOTrainingError("formal PPO execution plan is missing")
    return _inside(root, str(execution.get("artifact_root")), "PPO artifact root")


def _job_root(root: Path, plan: Mapping[str, Any], job: FormalPPOJob) -> Path:
    return _artifact_root(root, plan) / "jobs" / job.task_id / f"seed-{job.model_seed}"


def _next_attempt(job_root: Path) -> Path:
    indices = []
    for path in job_root.glob("attempt-*"):
        match = re.fullmatch(r"attempt-(\d{4})", path.name)
        if match:
            indices.append(int(match.group(1)))
    return job_root / f"attempt-{max(indices, default=0) + 1:04d}"


def _candidate_is_eligible(evaluation: Mapping[str, Any]) -> bool:
    summary = evaluation.get("summary")
    compatibility = evaluation.get("checkpoint_contract_compatibility")
    if not isinstance(summary, Mapping) or not isinstance(compatibility, Mapping):
        return False
    endpoint = summary.get("mean_episode_best_primary_metric")
    return bool(
        isinstance(endpoint, (int, float))
        and not isinstance(endpoint, bool)
        and math.isfinite(float(endpoint))
        and summary.get("episode_completion_rate") == 1.0
        and summary.get("behavior_complete_experiment_rate") == 1.0
        and summary.get("primary_metric_missing_count") == 0
        and summary.get("runtime_domain_failure_count") == 0
        and summary.get("observation_domain_failure_count") == 0
        and all(value is True for value in compatibility.values())
    )


def _valid_completed_summary(
    path: Path,
    *,
    root: Path,
    plan_sha256: str,
    job: FormalPPOJob,
    expected_steps: tuple[int, ...],
) -> dict[str, Any] | None:
    try:
        payload = _load_object(path, "PPO job summary")
        if (
            payload.get("schema_version") != PPO_JOB_SUMMARY_VERSION
            or payload.get("status") != "complete"
            or payload.get("plan_sha256") != plan_sha256
            or payload.get("job_id") != job.job_id
            or payload.get("task_id") != job.task_id
            or payload.get("model_seed") != job.model_seed
        ):
            return None
        manifest_path = _inside(root, str(payload["training_manifest_path"]), "training manifest")
        if file_sha256(manifest_path) != payload.get("training_manifest_sha256"):
            return None
        manifest = _load_object(manifest_path, "training manifest")
        if manifest.get("step_budget_exact") is not True or manifest.get(
            "training_environment_step_count"
        ) != manifest.get("requested_training_environment_step_count"):
            return None
        candidates = payload.get("candidates")
        if (
            not isinstance(candidates, list)
            or tuple(int(item.get("training_environment_step_count", -1)) for item in candidates)
            != expected_steps
        ):
            return None
        for candidate in candidates:
            checkpoint = _inside(root, str(candidate["checkpoint_path"]), "candidate checkpoint")
            evaluation = _inside(root, str(candidate["dev_evaluation_path"]), "Dev evaluation")
            if file_sha256(checkpoint) != candidate.get("checkpoint_sha256") or file_sha256(
                evaluation
            ) != candidate.get("dev_evaluation_sha256"):
                return None
        return payload
    except (FormalPPOTrainingError, KeyError, TypeError, ValueError, OSError):
        return None


def scan_completed_jobs(
    *, root: Path, plan: Mapping[str, Any]
) -> dict[FormalPPOJob, dict[str, Any]]:
    plan_sha256 = _canonical_sha256(plan)
    expected_steps = tuple(int(step) for step in plan["training"]["checkpoint_steps"])
    completed: dict[FormalPPOJob, dict[str, Any]] = {}
    for job in build_jobs(plan):
        attempts = sorted(_job_root(root, plan, job).glob("attempt-*/job-summary.json"))
        for summary_path in reversed(attempts):
            summary = _valid_completed_summary(
                summary_path,
                root=root,
                plan_sha256=plan_sha256,
                job=job,
                expected_steps=expected_steps,
            )
            if summary is not None:
                completed[job] = summary
                break
    return completed


def _task_index(plan: Mapping[str, Any], task_id: str) -> int:
    tasks = list(plan["formal_core_tasks"])
    return tasks.index(task_id)


def run_one_job(
    *,
    root: Path,
    plan: Mapping[str, Any],
    formal_protocol: Mapping[str, Any],
    job: FormalPPOJob,
) -> dict[str, Any]:
    """Run one retained training attempt and all preregistered Dev candidates."""

    plan_sha256 = _canonical_sha256(plan)
    completed = scan_completed_jobs(root=root, plan=plan)
    if job in completed:
        return completed[job]
    attempt = _next_attempt(_job_root(root, plan, job))
    attempt.mkdir(parents=True, exist_ok=False)
    _write_json(
        attempt / "attempt-start.json",
        {
            "schema_version": "chemworld-formal-ppo-attempt-0.4",
            "status": "started",
            "job_id": job.job_id,
            "task_id": job.task_id,
            "model_seed": job.model_seed,
            "plan_sha256": plan_sha256,
        },
    )
    training = cast(Mapping[str, Any], plan["training"])
    infrastructure = cast(Mapping[str, Any], plan["infrastructure"])
    development = cast(Mapping[str, Any], plan["development_selection"])
    task_index = _task_index(plan, job.task_id)
    try:
        train_allocation = build_formal_allocation(
            formal_protocol, task_id=job.task_id, name="train"
        )
        dev_allocation = build_formal_allocation(formal_protocol, task_id=job.task_id, name="dev")
        manifest = train_sb3_baseline(
            algorithm="ppo",
            task_id=job.task_id,
            allocation=train_allocation,
            total_timesteps=int(training["requested_environment_steps_per_run"]),
            model_seed=job.model_seed,
            output_dir=attempt,
            algorithm_kwargs=dict(cast(Mapping[str, Any], training["hyperparameters"])),
            operation_budget=int(training["operation_budget"]),
            checkpoint_steps=[int(step) for step in training["checkpoint_steps"]],
            parallel_environments=int(infrastructure["parallel_environments"]),
            vectorization_backend=cast(Any, infrastructure["vectorization_backend"]),
            device=cast(Any, infrastructure["device"]),
        )
        manifest_path = attempt / f"{job.job_id}.manifest.json"
        expected_steps = tuple(int(step) for step in training["checkpoint_steps"])
        candidates: list[dict[str, Any]] = []
        checkpoint_artifacts = [
            item
            for item in manifest["periodic_checkpoint_artifacts"]
            if item.get("artifact_type") == "checkpoint"
        ]
        by_step: dict[int, Mapping[str, Any]] = {}
        for artifact in checkpoint_artifacts:
            match = re.search(r"_(\d+)_steps\.zip$", str(artifact.get("path")))
            if match:
                by_step[int(match.group(1))] = artifact
        if tuple(sorted(by_step)) != expected_steps:
            raise FormalPPOTrainingError("training did not produce the exact checkpoint schedule")
        for step in expected_steps:
            checkpoint = attempt / str(by_step[step]["path"])
            evaluation = evaluate_sb3_checkpoint(
                algorithm="ppo",
                checkpoint=checkpoint,
                task_id=job.task_id,
                allocation=dev_allocation,
                episodes=int(development["episodes_per_candidate"]),
                operation_budget=int(development["operation_budget_per_episode"]),
                sampler_seed=int(development["sampler_seed_base"]) + task_index,
                policy_seed=int(development["policy_seed_base"]) + task_index,
                deterministic=bool(development["deterministic_policy"]),
                primary_metric=str(plan["formal_core_tasks"][job.task_id]),
            )
            evaluation_path = attempt / "dev" / f"checkpoint-{step}.json"
            _write_json(evaluation_path, evaluation)
            candidates.append(
                {
                    "training_environment_step_count": step,
                    "checkpoint_path": checkpoint.relative_to(root).as_posix(),
                    "checkpoint_sha256": file_sha256(checkpoint),
                    "checkpoint_contract_path": checkpoint.with_suffix(".manifest.json")
                    .relative_to(root)
                    .as_posix(),
                    "dev_evaluation_path": evaluation_path.relative_to(root).as_posix(),
                    "dev_evaluation_sha256": file_sha256(evaluation_path),
                    "eligible": _candidate_is_eligible(evaluation),
                    "summary": evaluation["summary"],
                }
            )
        summary = {
            "schema_version": PPO_JOB_SUMMARY_VERSION,
            "status": "complete",
            "job_id": job.job_id,
            "task_id": job.task_id,
            "model_seed": job.model_seed,
            "plan_sha256": plan_sha256,
            "training_manifest_path": manifest_path.relative_to(root).as_posix(),
            "training_manifest_sha256": file_sha256(manifest_path),
            "requested_training_environment_step_count": manifest[
                "requested_training_environment_step_count"
            ],
            "training_environment_step_count": manifest["training_environment_step_count"],
            "step_budget_exact": manifest["step_budget_exact"],
            "cpu_time_s": manifest["cpu_time_s"],
            "gpu_time_s": manifest["gpu_time_s"],
            "wall_time_s": manifest["wall_time_s"],
            "training_diagnostics": manifest["training_diagnostics"],
            "candidates": candidates,
            "reference_search_used": False,
            "bench_accessed": False,
            "bench_finetuning_used": False,
        }
        _write_json(attempt / "job-summary.json", summary)
        return summary
    except Exception as exc:
        _write_json(
            attempt / "attempt-failure.json",
            {
                "schema_version": "chemworld-formal-ppo-attempt-failure-0.4",
                "status": "failed_retained",
                "job_id": job.job_id,
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "plan_sha256": plan_sha256,
            },
        )
        raise


def run_pending_jobs(
    *,
    root: Path,
    plan: Mapping[str, Any],
    formal_protocol: Mapping[str, Any],
    task_id: str | None = None,
    model_seed: int | None = None,
    max_jobs: int | None = None,
) -> dict[str, Any]:
    jobs = [
        job
        for job in build_jobs(plan)
        if (task_id is None or job.task_id == task_id)
        and (model_seed is None or job.model_seed == model_seed)
    ]
    if not jobs:
        raise FormalPPOTrainingError("no PPO job matches the requested filters")
    completed_before = scan_completed_jobs(root=root, plan=plan)
    pending = [job for job in jobs if job not in completed_before]
    if max_jobs is not None:
        if max_jobs <= 0:
            raise FormalPPOTrainingError("max_jobs must be positive")
        pending = pending[:max_jobs]
    executed = [
        run_one_job(root=root, plan=plan, formal_protocol=formal_protocol, job=job)
        for job in pending
    ]
    completed_after = scan_completed_jobs(root=root, plan=plan)
    return {
        "schema_version": "chemworld-formal-ppo-execution-status-0.4",
        "planned_job_count": len(build_jobs(plan)),
        "matching_job_count": len(jobs),
        "executed_job_count": len(executed),
        "completed_job_count": len(completed_after),
        "remaining_job_count": len(build_jobs(plan)) - len(completed_after),
        "executed_job_ids": [item["job_id"] for item in executed],
    }


def select_task_candidate(task_id: str, summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    eligible: list[dict[str, Any]] = []
    for summary in summaries:
        if summary.get("task_id") != task_id:
            continue
        for candidate_raw in cast(list[dict[str, Any]], summary.get("candidates", [])):
            candidate = dict(candidate_raw)
            if candidate.get("eligible") is not True:
                continue
            endpoint = candidate.get("summary", {}).get("mean_episode_best_primary_metric")
            if not isinstance(endpoint, (int, float)) or isinstance(endpoint, bool):
                continue
            candidate["model_seed"] = int(summary["model_seed"])
            candidate["job_id"] = str(summary["job_id"])
            candidate["training_manifest_path"] = str(summary["training_manifest_path"])
            eligible.append(candidate)
    if not eligible:
        raise FormalPPOTrainingError(
            f"{task_id} has no behavior-complete, domain-stable PPO candidate"
        )
    return min(
        eligible,
        key=lambda item: (
            -float(item["summary"]["mean_episode_best_primary_metric"]),
            int(item["training_environment_step_count"]),
            int(item["model_seed"]),
        ),
    )


def _selected_paths(root: Path, plan: Mapping[str, Any], task_id: str) -> tuple[Path, Path, Path]:
    directory = _artifact_root(root, plan) / "selected" / task_id
    checkpoint = directory / f"ppo-{task_id}.zip"
    return (
        checkpoint,
        checkpoint.with_suffix(".manifest.json"),
        checkpoint.with_suffix(".resources.json"),
    )


def _materialize_selection(
    *,
    root: Path,
    plan: Mapping[str, Any],
    formal_protocol: Mapping[str, Any],
    task_id: str,
    selected: Mapping[str, Any],
    task_summaries: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_checkpoint = _inside(
        root, str(selected["checkpoint_path"]), "selected source checkpoint"
    )
    source_manifest = _inside(
        root, str(selected["training_manifest_path"]), "selected source manifest"
    )
    checkpoint, manifest_path, resource_path = _selected_paths(root, plan, task_id)
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_checkpoint, checkpoint)
    checkpoint_sha = file_sha256(checkpoint)
    manifest = _load_object(source_manifest, "selected source training manifest")
    manifest.update(
        {
            "formal_evidence": False,
            "checkpoint": checkpoint.name,
            "checkpoint_sha256": checkpoint_sha,
            "bench_finetuning_used": False,
            "selected_on_allocation": "dev",
            "selected_checkpoint_training_environment_step_count": selected[
                "training_environment_step_count"
            ],
            "selected_model_seed": selected["model_seed"],
            "selection_primary_metric": plan["formal_core_tasks"][task_id],
            "selection_mean_episode_best_primary_metric": selected["summary"][
                "mean_episode_best_primary_metric"
            ],
            "source_training_manifest_sha256": file_sha256(source_manifest),
            "source_candidate_contract_sha256": file_sha256(
                _inside(root, str(selected["checkpoint_contract_path"]), "candidate contract")
            ),
            "training_selection_cohort": {
                "model_seeds": list(plan["model_seeds"]),
                "run_count": len(task_summaries),
                "candidate_checkpoint_count": sum(
                    len(cast(list[Any], item["candidates"])) for item in task_summaries
                ),
                "ranking": plan["development_selection"]["ranking"],
            },
            "limitations": [
                "This checkpoint was selected on public Dev evidence and has not accessed Bench.",
                (
                    "The binary remains in the ignored controlled run tree; clean-environment "
                    "distribution is a later parent-task gate."
                ),
                (
                    "Formal Bench eligibility additionally requires SAC completion, method "
                    "freeze, and the sealed evaluation workflow."
                ),
            ],
        }
    )
    manifest.pop("periodic_checkpoint_artifacts", None)
    manifest.pop("periodic_checkpoint_contract_manifests", None)
    _write_json(manifest_path, manifest)
    requested = sum(
        int(item["requested_training_environment_step_count"]) for item in task_summaries
    )
    actual = sum(int(item["training_environment_step_count"]) for item in task_summaries)
    resources = {
        "schema_version": RL_TRAINING_RESOURCE_VERSION,
        "accounting_complete": True,
        "training_run_id": f"ppo-{task_id}-five-seed-selection-cohort",
        "checkpoint_sha256": checkpoint_sha,
        "source_manifest_sha256": file_sha256(manifest_path),
        "requested_training_environment_step_count": requested,
        "training_environment_step_count": actual,
        "cpu_time_s": sum(float(item["cpu_time_s"]) for item in task_summaries),
        "gpu_time_s": sum(float(item["gpu_time_s"]) for item in task_summaries),
        "wall_time_s": sum(float(item["wall_time_s"]) for item in task_summaries),
        "training_run_count": len(task_summaries),
        "rejected_training_runs_retained": len(task_summaries) - 1,
    }
    audited = audit_rl_training_resource(resources)
    if audited["accounting_complete"] is not True:
        raise FormalPPOTrainingError(
            "selected PPO training resource ledger failed: " + ", ".join(audited["failure_reasons"])
        )
    _write_json(resource_path, resources)
    entry = {
        "method_id": "ppo",
        "task_id": task_id,
        "checkpoint_path": checkpoint.relative_to(root).as_posix(),
        "checkpoint_manifest_path": manifest_path.relative_to(root).as_posix(),
        "training_resource_path": resource_path.relative_to(root).as_posix(),
        "checkpoint_sha256": checkpoint_sha,
    }
    binding = RLCheckpointBinding.from_payload(entry, root=root, formal_protocol=formal_protocol)
    return {**entry, "binding": binding.public_summary()}


def _replay_selected(
    *,
    root: Path,
    plan: Mapping[str, Any],
    formal_protocol: Mapping[str, Any],
    entry: Mapping[str, Any],
) -> dict[str, Any]:
    task_id = str(entry["task_id"])
    development = cast(Mapping[str, Any], plan["development_selection"])
    task_index = _task_index(plan, task_id)
    checkpoint = _inside(root, str(entry["checkpoint_path"]), "selected checkpoint")
    allocation = build_formal_allocation(formal_protocol, task_id=task_id, name="dev")
    payloads = [
        evaluate_sb3_checkpoint(
            algorithm="ppo",
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=allocation,
            episodes=int(development["episodes_per_candidate"]),
            operation_budget=int(development["operation_budget_per_episode"]),
            sampler_seed=int(development["sampler_seed_base"]) + task_index,
            policy_seed=int(development["policy_seed_base"]) + task_index,
            deterministic=True,
            primary_metric=str(plan["formal_core_tasks"][task_id]),
        )
        for _ in range(int(development["deterministic_replay_repetitions_for_selected_checkpoint"]))
    ]
    hashes = [_canonical_sha256(payload) for payload in payloads]
    if len(set(hashes)) != 1:
        raise FormalPPOTrainingError(f"selected PPO replay drifted for {task_id}")
    replay_dir = checkpoint.parent / "replay"
    for index, payload in enumerate(payloads, start=1):
        _write_json(replay_dir / f"dev-replay-{index}.json", payload)
    return {
        "repetition_count": len(payloads),
        "deterministic": True,
        "canonical_evaluation_sha256": hashes[0],
        "summary": payloads[0]["summary"],
    }


def finalize_training(
    *,
    root: Path,
    plan: Mapping[str, Any],
    formal_protocol: Mapping[str, Any],
    methods_config: Mapping[str, Any],
) -> dict[str, Any]:
    """Select four checkpoints, bind cohort resources, replay, and write tracked evidence."""

    validation = validate_training_plan(
        plan, formal_protocol=formal_protocol, methods_config=methods_config
    )
    completed = scan_completed_jobs(root=root, plan=plan)
    jobs = build_jobs(plan)
    if len(completed) != len(jobs):
        raise FormalPPOTrainingError(
            f"cannot finalize PPO: {len(completed)}/{len(jobs)} jobs are complete"
        )
    summaries = [completed[job] for job in jobs]
    selections: list[dict[str, Any]] = []
    selection_reports: list[dict[str, Any]] = []
    for task_id in plan["formal_core_tasks"]:
        task_summaries = [item for item in summaries if item["task_id"] == task_id]
        selected = select_task_candidate(str(task_id), task_summaries)
        entry = _materialize_selection(
            root=root,
            plan=plan,
            formal_protocol=formal_protocol,
            task_id=str(task_id),
            selected=selected,
            task_summaries=task_summaries,
        )
        replay = _replay_selected(
            root=root,
            plan=plan,
            formal_protocol=formal_protocol,
            entry=entry,
        )
        selections.append({key: value for key, value in entry.items() if key != "binding"})
        selection_reports.append(
            {
                "task_id": task_id,
                "primary_metric": plan["formal_core_tasks"][task_id],
                "selected_model_seed": selected["model_seed"],
                "selected_training_environment_step_count": selected[
                    "training_environment_step_count"
                ],
                "selected_dev_evaluation_sha256": selected["dev_evaluation_sha256"],
                "selected_dev_summary": selected["summary"],
                "checkpoint_binding": entry["binding"],
                "deterministic_replay": replay,
            }
        )
    execution = cast(Mapping[str, Any], plan["execution"])
    index_path = _inside(root, str(execution["checkpoint_index"]), "PPO checkpoint index")
    checkpoint_index = {
        "schema_version": PPO_CHECKPOINT_INDEX_VERSION,
        "status": "ppo_ready_sac_pending",
        "method_ids": ["ppo"],
        "formal_core_tasks": list(plan["formal_core_tasks"]),
        "checkpoints": selections,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "parent_task_complete": False,
        "checkpoint_binaries_committed": False,
    }
    _write_json(index_path, checkpoint_index)
    checks = {
        **validation,
        "twenty_training_runs_complete": len(summaries) == 20,
        "sixty_candidate_checkpoints_complete": sum(
            len(cast(list[Any], item["candidates"])) for item in summaries
        )
        == 60,
        "four_dev_selected_checkpoints": len(selections) == 4,
        "all_training_step_budgets_exact": all(
            item["step_budget_exact"] is True
            and item["training_environment_step_count"]
            == item["requested_training_environment_step_count"]
            for item in summaries
        ),
        "all_selected_replay_deterministic": all(
            item["deterministic_replay"]["deterministic"] is True for item in selection_reports
        ),
        "no_bench_or_reference_access": all(
            item["bench_accessed"] is False and item["reference_search_used"] is False
            for item in summaries
        ),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise FormalPPOTrainingError("PPO evidence checks failed: " + ", ".join(failed))
    report = {
        "schema_version": PPO_REPORT_VERSION,
        "status": "ppo_train_dev_complete_sac_pending",
        "controls_ready": True,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "parent_task_complete": False,
        "plan_sha256": _canonical_sha256(plan),
        "formal_protocol_sha256": _canonical_sha256(formal_protocol),
        "methods_config_sha256": _canonical_sha256(methods_config),
        "checkpoint_index_path": index_path.relative_to(root).as_posix(),
        "checkpoint_index_sha256": file_sha256(index_path),
        "checks": checks,
        "failed_checks": failed,
        "training_run_count": len(summaries),
        "candidate_checkpoint_count": 60,
        "selected_checkpoint_count": len(selections),
        "total_training_environment_step_count": sum(
            int(item["training_environment_step_count"]) for item in summaries
        ),
        "training_resources": {
            "cpu_time_s": sum(float(item["cpu_time_s"]) for item in summaries),
            "gpu_time_s": sum(float(item["gpu_time_s"]) for item in summaries),
            "wall_time_s": sum(float(item["wall_time_s"]) for item in summaries),
        },
        "jobs": [
            {
                "job_id": item["job_id"],
                "task_id": item["task_id"],
                "model_seed": item["model_seed"],
                "training_manifest_path": item["training_manifest_path"],
                "training_manifest_sha256": item["training_manifest_sha256"],
                "training_environment_step_count": item["training_environment_step_count"],
                "candidate_evaluations": [
                    {
                        "training_environment_step_count": candidate[
                            "training_environment_step_count"
                        ],
                        "dev_evaluation_sha256": candidate["dev_evaluation_sha256"],
                        "eligible": candidate["eligible"],
                        "summary": candidate["summary"],
                    }
                    for candidate in item["candidates"]
                ],
            }
            for item in summaries
        ],
        "task_selections": selection_reports,
        "reference_repositories_used": [],
        "remaining_parent_work": [
            "four-task five-seed SAC Train/Dev execution",
            "clean-environment checkpoint distribution and load proof",
            "observation-blind comparison at the parent method gate",
            "method freeze before any sealed Bench access",
        ],
        "limitations": [
            (
                "This report is public Train/Dev method-development evidence, not formal Bench "
                "evidence."
            ),
            "PPO completion alone does not complete benchmark-v05-rl-adapters.",
            (
                "Selected checkpoint binaries are digest-bound local artifacts under the ignored "
                "controlled run tree."
            ),
        ],
    }
    report_path = _inside(root, str(execution["report"]), "PPO Dev report")
    _write_json(report_path, report)
    return report


def load_execution_inputs(
    *, root: Path, plan_path: str | Path = DEFAULT_PLAN_PATH
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = _load_object(_inside(root, plan_path, "PPO plan"), "formal PPO training plan")
    formal = _load_object(
        _inside(root, DEFAULT_FORMAL_PROTOCOL_PATH, "formal protocol"), "formal protocol"
    )
    methods = _load_object(
        _inside(root, DEFAULT_METHODS_PATH, "RL methods config"), "RL methods config"
    )
    validate_training_plan(plan, formal_protocol=formal, methods_config=methods)
    return plan, formal, methods


__all__ = [
    "DEFAULT_PLAN_PATH",
    "PPO_CHECKPOINT_INDEX_VERSION",
    "PPO_JOB_SUMMARY_VERSION",
    "PPO_PLAN_VERSION",
    "PPO_REPORT_VERSION",
    "FormalPPOJob",
    "FormalPPOTrainingError",
    "build_formal_allocation",
    "build_jobs",
    "finalize_training",
    "load_execution_inputs",
    "load_training_plan",
    "run_one_job",
    "run_pending_jobs",
    "scan_completed_jobs",
    "select_task_candidate",
    "validate_training_plan",
]
