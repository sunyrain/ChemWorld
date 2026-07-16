"""Run the preregistered current-contract SAC step-0/trained Dev gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from collections.abc import Mapping, Sequence
from functools import partial
from pathlib import Path
from time import perf_counter, process_time
from typing import Any, cast

from chemworld.rl.checkpoint_contract import RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION
from chemworld.rl.environment import build_rl_environment
from chemworld.rl.evaluation import evaluate_sb3_checkpoint
from chemworld.rl.formal_training import build_formal_allocation
from chemworld.rl.observation_contract import rl_observation_contract
from chemworld.rl.training import train_sb3_baseline

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN_PATH = Path("configs/methods/rl_v0.4/sac_v048_preflight_plan.json")
PLAN_VERSION = "chemworld-sac-v048-preflight-plan-0.1"
JOB_VERSION = "chemworld-sac-v048-preflight-job-0.1"
REPORT_VERSION = "chemworld-sac-v048-preflight-report-0.1"
POST_AFFORDANCE_PLAN_VERSION = "chemworld-sac-v049-preflight-plan-0.1"
PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION = "chemworld-sac-v0410-preflight-plan-0.1"
PUBLIC_PRECONDITION_PLAN_VERSION = "chemworld-sac-v0411-preflight-plan-0.1"
CRYSTALLIZATION_DOMAIN_PLAN_VERSION = "chemworld-sac-v0412-preflight-plan-0.1"
PREFLIGHT_PROFILES = {
    PLAN_VERSION: {
        "task_id": "benchmark-v05-rl-adapters--slice-sac-train-dev",
        "job_version": JOB_VERSION,
        "report_version": REPORT_VERSION,
        "attempt_version": "chemworld-sac-v048-preflight-attempt-0.1",
        "failure_version": "chemworld-sac-v048-preflight-attempt-failure-0.1",
        "execution_status_version": "chemworld-sac-v048-preflight-execution-status-0.1",
        "status_prefix": "sac_v048",
        "result_role": "current_contract_train_dev_preflight",
    },
    POST_AFFORDANCE_PLAN_VERSION: {
        "task_id": "benchmark-v05-rl-adapters--slice-sac-v049-post-affordance-dev",
        "job_version": "chemworld-sac-v049-preflight-job-0.1",
        "report_version": "chemworld-sac-v049-preflight-report-0.1",
        "attempt_version": "chemworld-sac-v049-preflight-attempt-0.1",
        "failure_version": "chemworld-sac-v049-preflight-attempt-failure-0.1",
        "execution_status_version": "chemworld-sac-v049-preflight-execution-status-0.1",
        "status_prefix": "sac_v049",
        "result_role": "post_affordance_runtime_domain_train_dev_preflight",
    },
    PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION: {
        "task_id": "benchmark-v05-rl-adapters--slice-sac-v0410-public-schema-adapter-dev",
        "job_version": "chemworld-sac-v0410-preflight-job-0.1",
        "report_version": "chemworld-sac-v0410-preflight-report-0.1",
        "attempt_version": "chemworld-sac-v0410-preflight-attempt-0.1",
        "failure_version": "chemworld-sac-v0410-preflight-attempt-failure-0.1",
        "execution_status_version": "chemworld-sac-v0410-preflight-execution-status-0.1",
        "status_prefix": "sac_v0410",
        "result_role": "public_schema_projected_train_dev_preflight",
    },
    PUBLIC_PRECONDITION_PLAN_VERSION: {
        "task_id": "benchmark-v05-rl-adapters--slice-sac-v0411-public-preconditions-dev",
        "job_version": "chemworld-sac-v0411-preflight-job-0.1",
        "report_version": "chemworld-sac-v0411-preflight-report-0.1",
        "attempt_version": "chemworld-sac-v0411-preflight-attempt-0.1",
        "failure_version": "chemworld-sac-v0411-preflight-attempt-failure-0.1",
        "execution_status_version": "chemworld-sac-v0411-preflight-execution-status-0.1",
        "status_prefix": "sac_v0411",
        "result_role": "public_precondition_repair_train_dev_preflight",
    },
    CRYSTALLIZATION_DOMAIN_PLAN_VERSION: {
        "task_id": "benchmark-v05-rl-adapters--slice-sac-v0412-crystallization-domain-dev",
        "job_version": "chemworld-sac-v0412-preflight-job-0.1",
        "report_version": "chemworld-sac-v0412-preflight-report-0.1",
        "attempt_version": "chemworld-sac-v0412-preflight-attempt-0.1",
        "failure_version": "chemworld-sac-v0412-preflight-attempt-failure-0.1",
        "execution_status_version": "chemworld-sac-v0412-preflight-execution-status-0.1",
        "status_prefix": "sac_v0412",
        "result_role": "crystallization_domain_repair_train_dev_preflight",
    },
}
RATE_FIELDS = (
    "episode_completion_rate",
    "behavior_complete_experiment_rate",
    "quick_close_rate",
    "invalid_action_rate",
    "unsafe_step_rate",
    "high_cost_step_rate",
)


class SACPreflightError(RuntimeError):
    """Raised when execution cannot preserve the preregistered SAC gate."""


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def scientific_contract_sha256(plan: Mapping[str, Any]) -> str:
    """Hash outcome-relevant settings while excluding versioned execution paths."""

    return _canonical_sha256(
        {
            "algorithm": plan.get("algorithm"),
            "formal_protocol_path": plan.get("formal_protocol_path"),
            "formal_core_tasks": plan.get("formal_core_tasks"),
            "comparison": plan.get("comparison"),
            "development_evaluation": plan.get("development_evaluation"),
            "gate": plan.get("gate"),
        }
    )


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SACPreflightError(f"cannot read {label}: {path}") from exc
    if not isinstance(payload, dict):
        raise SACPreflightError(f"{label} must be a JSON object")
    return payload


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _profile(plan: Mapping[str, Any]) -> Mapping[str, str]:
    profile = PREFLIGHT_PROFILES.get(str(plan.get("schema_version")))
    if profile is None:
        raise SACPreflightError("unsupported SAC preflight plan schema")
    return profile


def _inside(root: Path, relative: str, label: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise SACPreflightError(f"{label} escapes the repository") from exc
    return candidate


def _git_output(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=root, text=True, encoding="utf-8"
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise SACPreflightError(f"git {' '.join(args)} failed") from exc


def source_state(root: Path, *, require_clean: bool = True) -> dict[str, Any]:
    head = _git_output(root, "rev-parse", "HEAD")
    origin_main = _git_output(root, "rev-parse", "origin/main")
    status = _git_output(root, "status", "--porcelain=v1", "--untracked-files=all")
    state = {
        "source_commit": head,
        "origin_main_commit": origin_main,
        "source_tree_clean": not status,
        "source_commit_on_origin_main": head == origin_main,
    }
    if head != origin_main:
        raise SACPreflightError("preflight source commit is not the current origin/main tip")
    if require_clean and status:
        raise SACPreflightError("preflight requires a clean source tree")
    return state


def source_state_before_report(root: Path, start: Mapping[str, Any]) -> dict[str, Any]:
    """Require a clean, unchanged worktree while allowing origin/main to advance elsewhere."""

    head = _git_output(root, "rev-parse", "HEAD")
    status = _git_output(root, "status", "--porcelain=v1", "--untracked-files=all")
    stable = head == start.get("source_commit")
    clean = not status
    if not stable:
        raise SACPreflightError("preflight source commit changed before report")
    if not clean:
        raise SACPreflightError("preflight source tree changed before report")
    return {
        "source_commit_before_report": head,
        "source_commit_stable": stable,
        "source_tree_clean_before_report": clean,
    }


def validate_plan(plan: Mapping[str, Any], protocol: Mapping[str, Any]) -> dict[str, bool]:
    profile = _profile(plan)
    tasks = plan.get("formal_core_tasks")
    comparison = plan.get("comparison")
    development = plan.get("development_evaluation")
    gate = plan.get("gate")
    execution = plan.get("execution")
    comparability = plan.get("comparability_boundary")
    boundary = plan.get("evidence_boundary")
    reattestation = plan.get("adapter_reattestation")
    expected_adapter = (
        "chemworld-sb3-box-latent-adapter-0.2"
        if plan.get("schema_version")
        in {
            PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION,
            PUBLIC_PRECONDITION_PLAN_VERSION,
            CRYSTALLIZATION_DOMAIN_PLAN_VERSION,
        }
        else "chemworld-sb3-box-latent-adapter-0.1"
    )
    protocol_tasks = protocol.get("task_roles", {}).get("formal_core", {})
    checks = {
        "schema": plan.get("schema_version") in PREFLIGHT_PROFILES,
        "task_id": plan.get("task_id") == profile["task_id"],
        "algorithm": plan.get("algorithm") == "sac",
        "preregistered": plan.get("status") == "preregistered_before_execution",
        "four_tasks": isinstance(tasks, Mapping)
        and list(tasks)
        == [
            "partition-discovery",
            "reaction-to-crystallization",
            "reaction-to-distillation",
            "flow-reaction-optimization",
        ],
        "task_metrics_and_sesoi": isinstance(tasks, Mapping)
        and isinstance(protocol_tasks, Mapping)
        and all(
            isinstance(spec, Mapping)
            and isinstance(protocol_tasks.get(task_id), Mapping)
            and spec.get("primary_metric") == protocol_tasks[task_id].get("primary_metric")
            and float(spec.get("sesoi", -1.0)) == float(protocol_tasks[task_id].get("sesoi", -2.0))
            for task_id, spec in tasks.items()
        ),
        "step0_vs_25600": isinstance(comparison, Mapping)
        and comparison.get("model_seed") == 0
        and comparison.get("untrained_environment_steps") == 0
        and comparison.get("trained_environment_steps") == 25_600,
        "frozen_training": isinstance(comparison, Mapping)
        and comparison.get("parallel_environments") == 1
        and comparison.get("vectorization_backend") == "dummy"
        and comparison.get("device") == "cpu"
        and comparison.get("torch_num_threads") == 4
        and comparison.get("training_hyperparameters")
        == {
            "learning_rate": 0.0003,
            "buffer_size": 100000,
            "learning_starts": 1000,
            "batch_size": 256,
            "gamma": 0.99,
            "tau": 0.005,
        },
        "same_dev_evaluator": isinstance(development, Mapping)
        and development.get("allocation") == "dev"
        and development.get("episodes_per_condition") == 20
        and development.get("operation_budget_per_episode") == 60
        and development.get("policy_mode") == "stochastic_frozen_seed"
        and development.get("deterministic_policy") is False
        and development.get("evaluation_repetitions") == 2
        and development.get("same_task_split_seed_cohort_budget_contract_and_evaluator") is True
        and development.get("exact_replay_required") is True,
        "gate_frozen": isinstance(gate, Mapping)
        and gate.get("minimum_tasks_with_learning_signal") == 2
        and gate.get("threshold_changes_after_execution_allowed") is False
        and gate.get("failure_action")
        == "write fail-closed report and do not start the full SAC matrix",
        "paths_present": isinstance(execution, Mapping)
        and all(
            isinstance(execution.get(key), str) and bool(execution[key])
            for key in ("artifact_root", "report", "full_training_plan")
        ),
        "comparability_disclosed": isinstance(comparability, Mapping)
        and comparability.get("native_hybrid_distribution") is False
        and comparability.get("same_public_affordance_decoder_as_ppo") is True
        and comparability.get("action_adapter_schema_version") == expected_adapter
        and comparability.get("system_level_comparison_only") is True,
        "evidence_boundary": isinstance(boundary, Mapping)
        and boundary.get("formal_results_present") is False
        and boundary.get("benchmark_claim_allowed") is False
        and boundary.get("bench_accessed") is False
        and boundary.get("reference_search_used") is False
        and boundary.get("full_matrix_allowed_only_if_gate_passes") is True,
        "source_snapshot_contract": plan.get("schema_version") == PLAN_VERSION
        or plan.get("source_binding")
        == {
            "require_origin_main_at_start": True,
            "require_clean_tree_at_start": True,
            "require_stable_head_until_report": True,
            "require_clean_tree_before_report": True,
        },
        "adapter_reattestation_contract": plan.get("schema_version")
        not in {
            PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION,
            PUBLIC_PRECONDITION_PLAN_VERSION,
            CRYSTALLIZATION_DOMAIN_PLAN_VERSION,
        }
        or (
            plan.get("schema_version") == PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION
            and isinstance(reattestation, Mapping)
            and reattestation.get("parent_source_commit")
            == "9e2339c437a09f6bde05c95aeadca1f980df6725"
            and reattestation.get("parent_plan_path")
            == "configs/methods/rl_v0.4/sac_v049_preflight_plan.json"
            and reattestation.get("sac_adapter_diagnostic_report")
            == "workstreams/benchmark_v1/reports/rl-sac-v049-preflight-v0.4.json"
            and reattestation.get("ppo_infrastructure_failure_report")
            == "workstreams/benchmark_v1/reports/rl-ppo-v049-infrastructure-failure-v0.4.json"
            and reattestation.get("action_adapter_schema_version") == expected_adapter
            and reattestation.get("threshold_split_seed_and_hyperparameter_changes") is False
            and reattestation.get("v049_scientific_contract_sha256")
            == scientific_contract_sha256(plan)
            and isinstance(boundary, Mapping)
            and boundary.get("v049_ppo_infrastructure_failure_remains_immutable") is True
            and boundary.get("v049_sac_adapter_diagnostic_remains_immutable") is True
        )
        or (
            plan.get("schema_version") == PUBLIC_PRECONDITION_PLAN_VERSION
            and isinstance(reattestation, Mapping)
            and reattestation.get("parent_source_commit")
            == "4c34e8c99aa46ed08baecae508f3aaec6b295786"
            and reattestation.get("parent_plan_path")
            == "configs/methods/rl_v0.4/sac_v0410_preflight_plan.json"
            and reattestation.get("ppo_v0410_negative_report")
            == "workstreams/benchmark_v1/reports/rl-ppo-v0410-preflight-v0.4.json"
            and reattestation.get("action_adapter_schema_version") == expected_adapter
            and reattestation.get("conditional_hybrid_action_schema_version")
            == "chemworld-conditional-hybrid-action-0.3"
            and reattestation.get("sac_v0410_execution_skipped") is True
            and reattestation.get("threshold_split_seed_and_hyperparameter_changes") is False
            and reattestation.get("v0410_scientific_contract_sha256")
            == scientific_contract_sha256(plan)
            and isinstance(boundary, Mapping)
            and boundary.get("v0410_ppo_negative_report_remains_immutable") is True
            and boundary.get("v0410_sac_execution_skipped_on_shared_gap") is True
        )
        or (
            plan.get("schema_version") == CRYSTALLIZATION_DOMAIN_PLAN_VERSION
            and isinstance(reattestation, Mapping)
            and reattestation.get("parent_source_commit")
            == "ab62d3fb5e0a8337cba2026d8204d00a6aedfd94"
            and reattestation.get("parent_plan_path")
            == "configs/methods/rl_v0.4/sac_v0411_preflight_plan.json"
            and reattestation.get("ppo_v0411_negative_report")
            == "workstreams/benchmark_v1/reports/rl-ppo-v0411-preflight-v0.4.json"
            and reattestation.get("action_adapter_schema_version") == expected_adapter
            and reattestation.get("conditional_hybrid_action_schema_version")
            == "chemworld-conditional-hybrid-action-0.4"
            and reattestation.get("sac_v0411_execution_skipped") is True
            and reattestation.get("threshold_split_seed_and_hyperparameter_changes") is False
            and reattestation.get("v0411_scientific_contract_sha256")
            == scientific_contract_sha256(plan)
            and isinstance(boundary, Mapping)
            and boundary.get("v0411_ppo_negative_report_remains_immutable") is True
            and boundary.get("v0411_sac_execution_skipped_on_shared_gap") is True
        ),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise SACPreflightError("preflight plan validation failed: " + ", ".join(failed))
    return checks


def validate_adapter_reattestation(root: Path, plan: Mapping[str, Any]) -> dict[str, Any]:
    """Bind repair-only retries to their immutable parent diagnostics."""

    schema_version = plan.get("schema_version")
    if schema_version not in {
        PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION,
        PUBLIC_PRECONDITION_PLAN_VERSION,
        CRYSTALLIZATION_DOMAIN_PLAN_VERSION,
    }:
        return {}
    reattestation = cast(Mapping[str, Any], plan["adapter_reattestation"])
    if schema_version == CRYSTALLIZATION_DOMAIN_PLAN_VERSION:
        parent_path = _inside(root, str(reattestation["parent_plan_path"]), "parent plan")
        report_path = _inside(
            root,
            str(reattestation["ppo_v0411_negative_report"]),
            "PPO v0.4.11 negative report",
        )
        parent = _load_object(parent_path, "parent SAC preflight plan")
        report = _load_object(report_path, "PPO v0.4.11 negative report")
        gate = report.get("gate_assessment")
        resources = report.get("resource_accounting")
        checks = {
            "negative_report_schema": report.get("schema_version")
            == "chemworld-ppo-v0411-preflight-report-0.1",
            "negative_report_status": report.get("status")
            == "ppo_v0411_preflight_failed_full_matrix_forbidden",
            "negative_report_forbids_full_matrix": report.get("full_matrix_allowed") is False,
            "negative_report_source": report.get("source", {}).get("source_commit")
            == reattestation.get("parent_source_commit"),
            "complete_negative_execution": isinstance(resources, Mapping)
            and resources.get("training_environment_step_count") == 102_400
            and len(report.get("jobs", [])) == 4,
            "shared_operational_gap": isinstance(gate, Mapping)
            and gate.get("failed_checks") == ["all_tasks_operational"]
            and gate.get("learning_signal_task_count") == 4,
            "sac_v0411_skipped": reattestation.get("sac_v0411_execution_skipped") is True,
            "scientific_contract": reattestation.get("v0411_scientific_contract_sha256")
            == scientific_contract_sha256(parent)
            == scientific_contract_sha256(plan),
        }
        failed = sorted(name for name, passed in checks.items() if not passed)
        if failed:
            raise SACPreflightError(
                "SAC crystallization-domain reattestation is invalid: "
                + ", ".join(failed)
            )
        return {"ppo_v0411_negative_report": report}
    if schema_version == PUBLIC_PRECONDITION_PLAN_VERSION:
        parent_path = _inside(root, str(reattestation["parent_plan_path"]), "parent plan")
        report_path = _inside(
            root,
            str(reattestation["ppo_v0410_negative_report"]),
            "PPO v0.4.10 negative report",
        )
        parent = _load_object(parent_path, "parent SAC preflight plan")
        report = _load_object(report_path, "PPO v0.4.10 negative report")
        gate = report.get("gate_assessment")
        resources = report.get("resource_accounting")
        checks = {
            "negative_report_schema": report.get("schema_version")
            == "chemworld-ppo-v0410-preflight-report-0.1",
            "negative_report_status": report.get("status")
            == "ppo_v0410_preflight_failed_full_matrix_forbidden",
            "negative_report_forbids_full_matrix": report.get("full_matrix_allowed") is False,
            "negative_report_source": report.get("source", {}).get("source_commit")
            == reattestation.get("parent_source_commit"),
            "complete_negative_execution": isinstance(resources, Mapping)
            and resources.get("training_environment_step_count") == 102_400
            and len(report.get("jobs", [])) == 4,
            "shared_operational_gap": isinstance(gate, Mapping)
            and gate.get("failed_checks") == ["all_tasks_operational"],
            "sac_v0410_skipped": reattestation.get("sac_v0410_execution_skipped") is True,
            "scientific_contract": reattestation.get("v0410_scientific_contract_sha256")
            == scientific_contract_sha256(parent)
            == scientific_contract_sha256(plan),
        }
        failed = sorted(name for name, passed in checks.items() if not passed)
        if failed:
            raise SACPreflightError(
                "SAC public-precondition reattestation is invalid: " + ", ".join(failed)
            )
        return {"ppo_v0410_negative_report": report}

    parent_path = _inside(root, str(reattestation["parent_plan_path"]), "parent plan")
    diagnostic_path = _inside(
        root,
        str(reattestation["sac_adapter_diagnostic_report"]),
        "SAC adapter diagnostic report",
    )
    failure_path = _inside(
        root,
        str(reattestation["ppo_infrastructure_failure_report"]),
        "PPO infrastructure failure report",
    )
    parent = _load_object(parent_path, "parent SAC preflight plan")
    diagnostic = _load_object(diagnostic_path, "SAC adapter diagnostic report")
    failure = _load_object(failure_path, "PPO infrastructure failure report")
    observed = failure.get("observed_work")
    checks = {
        "sac_diagnostic_schema": diagnostic.get("schema_version")
        == "chemworld-sac-v049-preflight-report-0.1",
        "sac_diagnostic_status": diagnostic.get("status")
        == "sac_v049_preflight_failed_full_matrix_forbidden",
        "sac_source": diagnostic.get("source", {}).get("source_commit")
        == reattestation.get("parent_source_commit"),
        "sac_complete_negative": diagnostic.get("full_matrix_allowed") is False
        and len(diagnostic.get("jobs", [])) == 4
        and diagnostic.get("gate_assessment", {}).get("learning_signal_task_count") == 0,
        "ppo_failure_schema": failure.get("schema_version")
        == "chemworld-ppo-v049-infrastructure-failure-report-0.1",
        "ppo_zero_outcome": isinstance(observed, Mapping)
        and observed.get("training_environment_step_count") == 0
        and observed.get("dev_evaluation_count") == 0
        and observed.get("outcome_metric_observed") is False,
        "scientific_contract": reattestation.get("v049_scientific_contract_sha256")
        == scientific_contract_sha256(parent)
        == scientific_contract_sha256(plan),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise SACPreflightError("SAC adapter reattestation is invalid: " + ", ".join(failed))
    return {"sac_adapter_diagnostic": diagnostic, "ppo_infrastructure_failure": failure}


def _environment_contract(env: Any, name: str) -> dict[str, Any]:
    current = env
    while current is not None:
        factory = getattr(current, name, None)
        if callable(factory):
            return dict(factory())
        current = getattr(current, "env", None)
    raise SACPreflightError(f"SAC environment is missing its {name}")


def create_step0_checkpoint(
    *,
    task_id: str,
    allocation: Any,
    model_seed: int,
    operation_budget: int,
    algorithm_kwargs: Mapping[str, Any],
    torch_num_threads: int,
    output_dir: Path,
) -> dict[str, Any]:
    """Create a true initialized SAC checkpoint without calling ``learn``."""

    try:
        import stable_baselines3 as sb3
        import torch
        from stable_baselines3.common.vec_env import DummyVecEnv
    except ImportError as exc:
        raise SACPreflightError("install ChemWorld with the rl extra") from exc

    output_dir.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(torch_num_threads)
    probe = build_rl_environment(
        task_id=task_id,
        allocation=allocation,
        sampler_seed=model_seed,
        operation_budget=operation_budget,
        training_reward=True,
    )
    try:
        action = _environment_contract(probe, "action_contract")
        reward = _environment_contract(probe, "reward_contract")
        observation_shape = list(probe.observation_space.shape or ())
    finally:
        probe.close()
    observation = rl_observation_contract(task_id)
    if observation_shape != observation["shape"]:
        raise SACPreflightError("step-0 observation shape drifted from the public contract")
    env = DummyVecEnv(
        [
            partial(
                build_rl_environment,
                task_id=task_id,
                allocation=allocation,
                sampler_seed=model_seed,
                operation_budget=operation_budget,
                training_reward=True,
            )
        ]
    )
    wall_started = perf_counter()
    cpu_started = process_time()
    try:
        model = sb3.SAC(
            "MlpPolicy",
            env,
            seed=model_seed,
            verbose=0,
            device="cpu",
            **dict(algorithm_kwargs),
        )
        checkpoint_stem = output_dir / f"sac-{task_id}-seed{model_seed}-step0"
        model.save(checkpoint_stem)
        if int(model.num_timesteps) != 0:
            raise SACPreflightError("untrained SAC checkpoint has a nonzero step ledger")
    finally:
        env.close()
    checkpoint = checkpoint_stem.with_suffix(".zip")
    sidecar = {
        "schema_version": RL_CHECKPOINT_SIDECAR_SCHEMA_VERSION,
        "algorithm": "sac",
        "task_id": task_id,
        "training_environment_step_count": 0,
        "checkpoint": checkpoint.name,
        "checkpoint_sha256": _file_sha256(checkpoint),
        "observation_contract_hash": observation["contract_hash"],
        "action_contract_hash": action["contract_hash"],
        "training_reward_contract_hash": reward["contract_hash"],
        "policy_distribution_contract_hash": None,
        "shape_only_compatible": False,
        "legacy_checkpoint_compatible": False,
    }
    sidecar_path = checkpoint.with_suffix(".manifest.json")
    _write_json(sidecar_path, sidecar)
    return {
        "checkpoint": checkpoint.name,
        "checkpoint_sha256": _file_sha256(checkpoint),
        "checkpoint_contract": sidecar_path.name,
        "checkpoint_contract_sha256": _file_sha256(sidecar_path),
        "training_environment_step_count": 0,
        "model_seed": model_seed,
        "allocation": allocation.public_manifest(),
        "observation_contract_hash": observation["contract_hash"],
        "action_contract_hash": action["contract_hash"],
        "training_reward_contract_hash": reward["contract_hash"],
        "policy_distribution_contract_hash": None,
        "wall_time_s": perf_counter() - wall_started,
        "cpu_time_s": process_time() - cpu_started,
        "gpu_time_s": 0.0,
    }


def _writer_gate(root: Path, plan: Mapping[str, Any], source_commit: str) -> dict[str, Any]:
    relative = plan.get("writer_gate_path")
    if not isinstance(relative, str):
        raise SACPreflightError("preflight plan is missing writer_gate_path")
    path = _inside(root, relative, "writer gate")
    gate = _load_object(path, "writer gate")
    ready = (
        gate.get("writer_contract_ready") is True
        and gate.get("formal_training_allowed") is True
        and gate.get("source_tree_clean") is True
        and gate.get("source_commit") == source_commit
        and all(
            gate.get("algorithms", {}).get(algorithm, {}).get("writer_ready") is True
            for algorithm in ("ppo", "sac")
        )
    )
    if not ready:
        raise SACPreflightError("current-source PPO/SAC writer gate is not ready")
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": _file_sha256(path),
        "source_commit": source_commit,
        "writer_contract_ready": True,
        "formal_training_allowed": True,
    }


def _evaluate_repetitions(
    *,
    root: Path,
    output_dir: Path,
    checkpoint: Path,
    task_id: str,
    allocation: Any,
    primary_metric: str,
    episodes: int,
    operation_budget: int,
    sampler_seed: int,
    policy_seed: int,
    repetitions: int,
) -> dict[str, Any]:
    payloads: list[dict[str, Any]] = []
    paths: list[str] = []
    file_hashes: list[str] = []
    for repetition in range(1, repetitions + 1):
        payload = evaluate_sb3_checkpoint(
            algorithm="sac",
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=allocation,
            episodes=episodes,
            operation_budget=operation_budget,
            sampler_seed=sampler_seed,
            policy_seed=policy_seed,
            deterministic=False,
            primary_metric=primary_metric,
        )
        path = output_dir / f"replay-{repetition}.json"
        _write_json(path, payload)
        payloads.append(payload)
        paths.append(path.relative_to(root).as_posix())
        file_hashes.append(_file_sha256(path))
    canonical_hashes = [_canonical_sha256(payload) for payload in payloads]
    return {
        "evaluation_paths": paths,
        "evaluation_file_sha256s": file_hashes,
        "canonical_evaluation_sha256": canonical_hashes[0],
        "canonical_replay_sha256s": canonical_hashes,
        "repetition_count": len(payloads),
        "exact_replay": len(set(canonical_hashes)) == 1,
        "policy_mode": payloads[0]["policy_mode"],
        "checkpoint_contract_compatibility": payloads[0]["checkpoint_contract_compatibility"],
        "summary": payloads[0]["summary"],
    }


def _task_root(root: Path, plan: Mapping[str, Any], task_id: str) -> Path:
    execution = cast(Mapping[str, Any], plan["execution"])
    return _inside(root, str(execution["artifact_root"]), "artifact root") / task_id


def run_task(
    *,
    root: Path,
    plan: Mapping[str, Any],
    protocol: Mapping[str, Any],
    task_id: str,
    source_commit: str,
) -> dict[str, Any]:
    profile = _profile(plan)
    task_root = _task_root(root, plan, task_id)
    summary_path = task_root / "job-summary.json"
    plan_sha = _canonical_sha256(plan)
    if summary_path.is_file():
        summary = _load_object(summary_path, "SAC preflight job summary")
        if (
            summary.get("schema_version") != profile["job_version"]
            or summary.get("plan_sha256") != plan_sha
            or summary.get("source_commit") != source_commit
            or summary.get("status") != "complete"
        ):
            raise SACPreflightError(f"retained preflight job binding drifted for {task_id}")
        return summary
    if task_root.exists() and any(task_root.iterdir()):
        raise SACPreflightError(
            f"retained incomplete preflight attempt requires audit before rerun: {task_id}"
        )
    task_root.mkdir(parents=True, exist_ok=True)
    _write_json(
        task_root / "attempt-start.json",
        {
            "schema_version": profile["attempt_version"],
            "status": "started",
            "task_id": task_id,
            "source_commit": source_commit,
            "plan_sha256": plan_sha,
        },
    )
    tasks = cast(Mapping[str, Mapping[str, Any]], plan["formal_core_tasks"])
    comparison = cast(Mapping[str, Any], plan["comparison"])
    development = cast(Mapping[str, Any], plan["development_evaluation"])
    task_index = list(tasks).index(task_id)
    model_seed = int(comparison["model_seed"])
    train_allocation = build_formal_allocation(protocol, task_id=task_id, name="train")
    dev_allocation = build_formal_allocation(protocol, task_id=task_id, name="dev")
    try:
        step0_dir = task_root / "step0"
        step0_manifest = create_step0_checkpoint(
            task_id=task_id,
            allocation=train_allocation,
            model_seed=model_seed,
            operation_budget=int(comparison["training_operation_budget"]),
            algorithm_kwargs=cast(Mapping[str, Any], comparison["training_hyperparameters"]),
            torch_num_threads=int(comparison["torch_num_threads"]),
            output_dir=step0_dir,
        )
        step0_checkpoint = step0_dir / str(step0_manifest["checkpoint"])
        trained_dir = task_root / "trained"
        trained_manifest = train_sb3_baseline(
            algorithm="sac",
            task_id=task_id,
            allocation=train_allocation,
            total_timesteps=int(comparison["trained_environment_steps"]),
            model_seed=model_seed,
            output_dir=trained_dir,
            algorithm_kwargs=dict(cast(Mapping[str, Any], comparison["training_hyperparameters"])),
            operation_budget=int(comparison["training_operation_budget"]),
            checkpoint_steps=(int(comparison["trained_environment_steps"]),),
            parallel_environments=int(comparison["parallel_environments"]),
            vectorization_backend=cast(Any, comparison["vectorization_backend"]),
            device=cast(Any, comparison["device"]),
            torch_num_threads=int(comparison["torch_num_threads"]),
            progress_interval_steps=int(comparison["progress_interval_steps"]),
        )
        trained_checkpoint = trained_dir / str(trained_manifest["checkpoint"])
        sampler_seed = int(development["sampler_seed_base"]) + task_index
        policy_seed = int(development["policy_seed_base"]) + task_index
        step0 = _evaluate_repetitions(
            root=root,
            output_dir=task_root / "dev" / "step0",
            checkpoint=step0_checkpoint,
            task_id=task_id,
            allocation=dev_allocation,
            primary_metric=str(tasks[task_id]["primary_metric"]),
            episodes=int(development["episodes_per_condition"]),
            operation_budget=int(development["operation_budget_per_episode"]),
            sampler_seed=sampler_seed,
            policy_seed=policy_seed,
            repetitions=int(development["evaluation_repetitions"]),
        )
        trained = _evaluate_repetitions(
            root=root,
            output_dir=task_root / "dev" / "trained",
            checkpoint=trained_checkpoint,
            task_id=task_id,
            allocation=dev_allocation,
            primary_metric=str(tasks[task_id]["primary_metric"]),
            episodes=int(development["episodes_per_condition"]),
            operation_budget=int(development["operation_budget_per_episode"]),
            sampler_seed=sampler_seed,
            policy_seed=policy_seed,
            repetitions=int(development["evaluation_repetitions"]),
        )
        summary = {
            "schema_version": profile["job_version"],
            "status": "complete",
            "task_id": task_id,
            "primary_metric": tasks[task_id]["primary_metric"],
            "sesoi": tasks[task_id]["sesoi"],
            "model_seed": model_seed,
            "source_commit": source_commit,
            "plan_sha256": plan_sha,
            "train_allocation": train_allocation.public_manifest(),
            "dev_allocation": dev_allocation.public_manifest(),
            "sampler_seed": sampler_seed,
            "policy_seed": policy_seed,
            "step0_checkpoint": {
                **step0_manifest,
                "path": step0_checkpoint.relative_to(root).as_posix(),
            },
            "trained_checkpoint": {
                "path": trained_checkpoint.relative_to(root).as_posix(),
                "checkpoint_sha256": _file_sha256(trained_checkpoint),
                "manifest_path": trained_checkpoint.with_suffix(".manifest.json")
                .relative_to(root)
                .as_posix(),
                "manifest_sha256": _file_sha256(trained_checkpoint.with_suffix(".manifest.json")),
                "requested_training_environment_step_count": trained_manifest[
                    "requested_training_environment_step_count"
                ],
                "training_environment_step_count": trained_manifest[
                    "training_environment_step_count"
                ],
                "step_budget_exact": trained_manifest["step_budget_exact"],
                "training_diagnostics": trained_manifest["training_diagnostics"],
                "wall_time_s": trained_manifest["wall_time_s"],
                "cpu_time_s": trained_manifest["cpu_time_s"],
                "gpu_time_s": trained_manifest["gpu_time_s"],
                "training_infrastructure": trained_manifest["training_infrastructure"],
            },
            "step0_evaluation": step0,
            "trained_evaluation": trained,
            "comparability_boundary": plan["comparability_boundary"],
            "bench_accessed": False,
            "reference_search_used": False,
            "formal_results_present": False,
        }
        _write_json(summary_path, summary)
        return summary
    except Exception as exc:
        _write_json(
            task_root / "attempt-failure.json",
            {
                "schema_version": profile["failure_version"],
                "status": "failed_retained",
                "task_id": task_id,
                "source_commit": source_commit,
                "plan_sha256": plan_sha,
                "exception_type": type(exc).__name__,
                "message": str(exc),
            },
        )
        raise


def _condition_operational(condition: Mapping[str, Any]) -> dict[str, bool]:
    summary = cast(Mapping[str, Any], condition.get("summary", {}))
    compatibility = condition.get("checkpoint_contract_compatibility")
    rates_finite = all(
        isinstance(summary.get(field), (int, float))
        and not isinstance(summary.get(field), bool)
        and math.isfinite(float(summary[field]))
        and 0.0 <= float(summary[field]) <= 1.0
        for field in RATE_FIELDS
    )
    return {
        "contract_exact": isinstance(compatibility, Mapping)
        and bool(compatibility)
        and all(value is True for value in compatibility.values()),
        "replay_exact": condition.get("exact_replay") is True,
        "policy_mode_stochastic_frozen_seed": condition.get("policy_mode")
        == "stochastic_frozen_seed",
        "nonempty_execution": int(summary.get("operation_count", 0)) > 0
        and bool(summary.get("operation_counts")),
        "runtime_domain_stable": summary.get("runtime_domain_failure_count") == 0,
        "observation_domain_stable": summary.get("observation_domain_failure_count") == 0,
        "rates_finite_and_bounded": rates_finite,
    }


def assess_gate(plan: Mapping[str, Any], jobs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    profile = _profile(plan)
    tasks = cast(Mapping[str, Mapping[str, Any]], plan["formal_core_tasks"])
    gate = cast(Mapping[str, Any], plan["gate"])
    by_task = {str(job.get("task_id")): job for job in jobs}
    if set(by_task) != set(tasks):
        raise SACPreflightError("gate assessment requires all four preregistered tasks")
    task_results: list[dict[str, Any]] = []
    total_before_behavior = 0
    total_after_behavior = 0
    total_after_observations = 0
    for task_id, task_spec in tasks.items():
        job = by_task[task_id]
        before = cast(Mapping[str, Any], job["step0_evaluation"])
        after = cast(Mapping[str, Any], job["trained_evaluation"])
        before_summary = cast(Mapping[str, Any], before["summary"])
        after_summary = cast(Mapping[str, Any], after["summary"])
        before_behavior = int(before_summary["behavior_complete_experiment_count"])
        after_behavior = int(after_summary["behavior_complete_experiment_count"])
        total_before_behavior += before_behavior
        total_after_behavior += after_behavior
        total_after_observations += int(after_summary["primary_metric_observation_count"])
        raw_before = before_summary.get("mean_episode_best_primary_metric")
        raw_after = after_summary.get("mean_episode_best_primary_metric")
        before_endpoint = (
            float(raw_before)
            if isinstance(raw_before, (int, float)) and not isinstance(raw_before, bool)
            else 0.0
        )
        after_endpoint = (
            float(raw_after)
            if isinstance(raw_after, (int, float)) and not isinstance(raw_after, bool)
            else None
        )
        delta = after_endpoint - before_endpoint if after_endpoint is not None else None
        behavior_signal = after_behavior > before_behavior
        metric_signal = delta is not None and delta >= float(task_spec["sesoi"])
        before_checks = _condition_operational(before)
        after_checks = _condition_operational(after)
        task_results.append(
            {
                "task_id": task_id,
                "primary_metric": task_spec["primary_metric"],
                "sesoi": task_spec["sesoi"],
                "step0_mean_episode_best_primary_metric": raw_before,
                "trained_mean_episode_best_primary_metric": raw_after,
                "primary_metric_delta_with_missing_step0_as_zero": delta,
                "step0_behavior_complete_experiment_count": before_behavior,
                "trained_behavior_complete_experiment_count": after_behavior,
                "step0_runtime_domain_failure_count": before_summary[
                    "runtime_domain_failure_count"
                ],
                "trained_runtime_domain_failure_count": after_summary[
                    "runtime_domain_failure_count"
                ],
                "step0_observation_domain_failure_count": before_summary[
                    "observation_domain_failure_count"
                ],
                "trained_observation_domain_failure_count": after_summary[
                    "observation_domain_failure_count"
                ],
                "behavior_learning_signal": behavior_signal,
                "primary_metric_learning_signal": metric_signal,
                "learning_signal": behavior_signal or metric_signal,
                "step0_operational_checks": before_checks,
                "trained_operational_checks": after_checks,
                "operational": all(before_checks.values()) and all(after_checks.values()),
            }
        )
    signal_count = sum(int(item["learning_signal"]) for item in task_results)
    checks = {
        "all_tasks_operational": all(item["operational"] for item in task_results),
        "minimum_learning_signal_tasks": signal_count
        >= int(gate["minimum_tasks_with_learning_signal"]),
        "trained_primary_metric_observations_present": total_after_observations
        >= int(gate["trained_primary_metric_observation_count_minimum"]),
        "trained_total_behavior_complete_not_decreased": total_after_behavior
        >= total_before_behavior,
    }
    passed = all(checks.values())
    return {
        "passed": passed,
        "status": f"{profile['status_prefix']}_preflight_"
        + ("passed_full_matrix_allowed" if passed else "failed_full_matrix_forbidden"),
        "checks": checks,
        "failed_checks": sorted(name for name, value in checks.items() if not value),
        "learning_signal_task_count": signal_count,
        "required_learning_signal_task_count": int(gate["minimum_tasks_with_learning_signal"]),
        "step0_total_behavior_complete_experiment_count": total_before_behavior,
        "trained_total_behavior_complete_experiment_count": total_after_behavior,
        "trained_primary_metric_observation_count": total_after_observations,
        "task_results": task_results,
    }


def _scan_jobs(*, root: Path, plan: Mapping[str, Any], source_commit: str) -> list[dict[str, Any]]:
    profile = _profile(plan)
    jobs: list[dict[str, Any]] = []
    plan_sha = _canonical_sha256(plan)
    tasks = cast(Mapping[str, Any], plan["formal_core_tasks"])
    for task_id in tasks:
        path = _task_root(root, plan, task_id) / "job-summary.json"
        if not path.is_file():
            continue
        job = _load_object(path, "SAC preflight job summary")
        if (
            job.get("schema_version") != profile["job_version"]
            or job.get("status") != "complete"
            or job.get("source_commit") != source_commit
            or job.get("plan_sha256") != plan_sha
        ):
            raise SACPreflightError(f"preflight job binding drifted: {task_id}")
        jobs.append(job)
    return jobs


def finalize(
    *,
    root: Path,
    plan_path: Path,
    plan: Mapping[str, Any],
    protocol_path: Path,
    source: Mapping[str, Any],
    writer_gate: Mapping[str, Any],
) -> dict[str, Any]:
    profile = _profile(plan)
    jobs = _scan_jobs(root=root, plan=plan, source_commit=str(source["source_commit"]))
    expected = len(cast(Mapping[str, Any], plan["formal_core_tasks"]))
    if len(jobs) != expected:
        return {
            "schema_version": profile["execution_status_version"],
            "status": "incomplete",
            "completed_task_count": len(jobs),
            "expected_task_count": expected,
            "remaining_task_ids": [
                task_id
                for task_id in cast(Mapping[str, Any], plan["formal_core_tasks"])
                if task_id not in {job["task_id"] for job in jobs}
            ],
        }
    assessment = assess_gate(plan, jobs)
    source_for_report = dict(source)
    source_for_report.update(source_state_before_report(root, source))
    execution = cast(Mapping[str, Any], plan["execution"])
    report_path = _inside(root, str(execution["report"]), "preflight report")
    resources = {
        "training_environment_step_count": sum(
            int(job["trained_checkpoint"]["training_environment_step_count"]) for job in jobs
        ),
        "cpu_time_s": sum(float(job["trained_checkpoint"]["cpu_time_s"]) for job in jobs),
        "gpu_time_s": sum(float(job["trained_checkpoint"]["gpu_time_s"]) for job in jobs),
        "summed_job_wall_time_s_diagnostic_only": sum(
            float(job["trained_checkpoint"]["wall_time_s"]) for job in jobs
        ),
        "parallel_wall_time_sum_used_as_elapsed": False,
    }
    report = {
        "schema_version": profile["report_version"],
        "status": assessment["status"],
        "task_id": plan["task_id"],
        "algorithm": "sac",
        "result_role": profile["result_role"],
        "source": source_for_report,
        "preflight_plan_path": plan_path.relative_to(root).as_posix(),
        "preflight_plan_file_sha256": _file_sha256(plan_path),
        "preflight_plan_canonical_sha256": _canonical_sha256(plan),
        "formal_protocol_path": protocol_path.relative_to(root).as_posix(),
        "formal_protocol_sha256": _file_sha256(protocol_path),
        "writer_gate": dict(writer_gate),
        "adapter_reattestation": plan.get("adapter_reattestation"),
        "comparison": plan["comparison"],
        "development_evaluation": plan["development_evaluation"],
        "preregistered_gate": plan["gate"],
        "comparability_boundary": plan["comparability_boundary"],
        "gate_assessment": assessment,
        "jobs": jobs,
        "resource_accounting": resources,
        "full_matrix_allowed": assessment["passed"],
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "bench_accessed": False,
        "reference_search_used": False,
        "historical_diagnostic_used_as_current_result": False,
        "claim_boundary": (
            "Source-bound public Train/Dev SAC learning preflight only; this is neither "
            "full-matrix method readiness nor formal Bench evidence."
        ),
    }
    _write_json(report_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN_PATH)
    parser.add_argument("--task")
    parser.add_argument("--finalize-only", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--skip-finalize", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    plan_path = args.plan if args.plan.is_absolute() else root / args.plan
    plan_path = plan_path.resolve()
    plan = _load_object(plan_path, "SAC preflight plan")
    protocol_path = _inside(root, str(plan["formal_protocol_path"]), "formal protocol")
    protocol = _load_object(protocol_path, "formal protocol")
    validate_plan(plan, protocol)
    validate_adapter_reattestation(root, plan)
    source = source_state(root, require_clean=not args.audit_only)
    writer_gate = _writer_gate(root, plan, str(source["source_commit"]))
    tasks = cast(Mapping[str, Any], plan["formal_core_tasks"])
    if args.task is not None and args.task not in tasks:
        parser.error(f"unknown preflight task: {args.task}")
    if not args.audit_only and not args.finalize_only:
        selected = [args.task] if args.task else list(tasks)
        for task_id in selected:
            run_task(
                root=root,
                plan=plan,
                protocol=protocol,
                task_id=cast(str, task_id),
                source_commit=str(source["source_commit"]),
            )
    if args.skip_finalize:
        result: dict[str, Any] = {
            "schema_version": _profile(plan)["execution_status_version"],
            "status": "task_execution_complete_finalize_skipped",
        }
    else:
        result = finalize(
            root=root,
            plan_path=plan_path,
            plan=plan,
            protocol_path=protocol_path,
            source=source,
            writer_gate=writer_gate,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
