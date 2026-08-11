#!/usr/bin/env python3
"""Run the provider-free Work II mechanism-oracle relative qualification."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

import gymnasium as gym
import numpy as np
from scipy.optimize import differential_evolution

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    write_json_atomic,
)
from chemworld.eval.work_ii_mechanism_oracle_qualification import (
    EXPECTED_OPTIMIZER_REQUESTS,
    FULL_PERTURBATION_COUNT,
    INITIAL_POPULATION_SIZE,
    MECHANISM_ORACLE_VERSION,
    OPTIMIZER_GENERATIONS,
    TARGET_GRID_SIDE,
    VALIDATION_EXECUTION_COUNT,
    VALIDATION_REPLICATES,
    analyze_mechanism_oracle_world,
    balanced_initial_population,
    deterministic_oracle_seed,
    full_dimensional_perturbations,
    local_target_grid,
    select_validation_candidates,
)
from chemworld.tasks import get_task
from chemworld.world.scoring import task_score_observation

try:
    from scripts.run_work_ii_q1_response_surface import (
        TASK_SPECS,
        _compile_actions,
        _emit,
        _execute_recipe,
        _load,
        _q0_audit,
        _q1_coordinate_schema,
        _scoped_dirty_paths,
    )
except ModuleNotFoundError:
    from run_work_ii_q1_response_surface import (  # type: ignore[no-redef]
        TASK_SPECS,
        _compile_actions,
        _emit,
        _execute_recipe,
        _load,
        _q0_audit,
        _q1_coordinate_schema,
        _scoped_dirty_paths,
    )

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-mechanism-oracle-five-world-summary-0.1"
WORLD_REPORT_VERSION = "chemworld-work-ii-mechanism-oracle-world-report-0.1"
TOTAL_WORLD_REQUESTS = (
    EXPECTED_OPTIMIZER_REQUESTS
    + TARGET_GRID_SIDE**2
    + FULL_PERTURBATION_COUNT
    + VALIDATION_EXECUTION_COUNT
)


def _canonical_vector(
    vector: Sequence[float],
    schema: Sequence[Mapping[str, Any]],
) -> tuple[float, ...]:
    if len(vector) != len(schema):
        raise ValueError("mechanism-oracle vector has the wrong dimension")
    output = [float(np.clip(value, 0.0, 1.0)) for value in vector]
    for item in schema:
        if item.get("kind") != "categorical":
            continue
        coordinate = int(item["coordinate"])
        count = int(item["category_count"])
        category = min(int(output[coordinate] * count), count - 1)
        output[coordinate] = (category + 0.5) / count
    return tuple(round(value, 12) for value in output)


def _environment_kwargs(
    task_id: str,
    config: Mapping[str, Any],
    *,
    world_seed: int,
    budget: int,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "world_split": str(config["world_split"]),
        "budget": budget,
        "objective": str(config["objective"]),
        "seed": world_seed,
        "task_id": task_id,
        "budget_override": budget,
        "episode_mode_override": "single_experiment",
        "observation_seed_override": deterministic_oracle_seed(task_id, world_seed),
        "observation_noise_mode": "keyed",
        "observation_noise_namespace": (f"work-ii-mechanism-oracle-{task_id}-w{world_seed}"),
    }
    optional = (
        "electrochemical_material_family_id",
        "crystallization_material_family_id",
        "electrochemical_workflow_mode",
        "scoring_contract_id",
    )
    for key in optional:
        if config.get(key) is not None:
            kwargs[key] = config[key]
    return kwargs


def _rollback_failed_checks(info: Mapping[str, Any]) -> list[str]:
    checks: set[str] = set()
    for event in info.get("world_events", []):
        if not isinstance(event, Mapping) or event.get("event_type") != "transaction_rollback":
            continue
        payload = event.get("payload", {})
        if not isinstance(payload, Mapping):
            continue
        raw = payload.get("failed_checks", [])
        if isinstance(raw, str):
            values = raw.split(",")
        elif isinstance(raw, Sequence):
            values = raw
        else:
            values = []
        checks.update(str(value) for value in values if str(value))
    return sorted(checks)


class InMemoryMechanismEvaluator:
    """Execute public recipes while retaining only non-leaking evaluator summaries."""

    def __init__(
        self,
        *,
        task_id: str,
        config: Mapping[str, Any],
        spec: Mapping[str, Any],
        world_seed: int,
        progress_callback: Callable[[str, int, int], None] | None = None,
    ) -> None:
        self.task_id = task_id
        self.config = dict(config)
        self.spec = dict(spec)
        self.world_seed = int(world_seed)
        self.schema = _q1_coordinate_schema(task_id)
        midpoint_actions, _ = _compile_actions(
            task_id,
            self.config,
            [0.5] * len(self.schema),
        )
        self.env = gym.make(
            get_task(task_id).env_id,
            **_environment_kwargs(
                task_id,
                self.config,
                world_seed=self.world_seed,
                budget=len(midpoint_actions),
            ),
        )
        self.base_env: Any = self.env.unwrapped
        self.progress_callback = progress_callback
        self.rows: list[dict[str, Any]] = []
        self._cache: dict[tuple[float, ...], dict[str, Any]] = {}
        self.request_count = 0
        self.failure_count = 0
        self.physical_failure_count = 0

    def close(self) -> None:
        self.env.close()

    def evaluate(
        self,
        vector: Sequence[float],
        *,
        phase: str,
        extra: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.request_count += 1
        canonical = _canonical_vector(vector, self.schema)
        cached = self._cache.get(canonical)
        if cached is not None:
            row = copy.deepcopy(cached)
            row["cache_hit"] = True
            if extra:
                row.update(dict(extra))
            if self.progress_callback is not None:
                self.progress_callback(
                    phase,
                    self.request_count,
                    self.failure_count + self.physical_failure_count,
                )
            return row

        started = perf_counter()
        evaluation_id = f"m{len(self.rows) + 1:06d}"
        failure: dict[str, str] | None = None
        metrics: dict[str, float] | None = None
        score: float | None = None
        risk: float | None = None
        ledger_cost: float | None = None
        scoring_cost: float | None = None
        action_count: int | None = None
        metadata_sha256: str | None = None
        physical_failure: dict[str, Any] | None = None
        try:
            actions, metadata = _compile_actions(self.task_id, self.config, canonical)
            action_count = len(actions)
            metadata_sha256 = canonical_json_sha256(metadata)
            self.env.reset(seed=self.world_seed)
            last_info: Mapping[str, Any] | None = None
            for action_index, action in enumerate(actions, start=1):
                _, _, terminated, truncated, info = self.env.step(action)
                last_info = info
                if (
                    info.get("transaction_status") == "rolled_back"
                    and info.get("rollback_reason") == "constitution_failed"
                ):
                    physical_failure = {
                        "operation_index": action_index,
                        "operation": str(action.get("operation")),
                        "transaction_status": "rolled_back",
                        "rollback_reason": "constitution_failed",
                        "failed_checks": _rollback_failed_checks(info),
                    }
                    self.physical_failure_count += 1
                    break
                if info.get("transaction_status") != "committed":
                    raise ValueError(
                        "mechanism recipe operation was not committed: "
                        f"index={action_index}, operation={action.get('operation')}, "
                        f"status={info.get('transaction_status')}"
                    )
                if truncated and not terminated:
                    raise ValueError("mechanism recipe truncated before completion")
                if terminated and action_index != len(actions):
                    raise ValueError("mechanism recipe terminated before its final action")
            if physical_failure is not None:
                last_info = None
            elif last_info is None or last_info.get("leaderboard_score") is None:
                raise ValueError("mechanism recipe lacks a committed final assay")
            if physical_failure is None:
                state = self.base_env._state
                truth = self.base_env.observation_kernel._truth_values(state)
                ledger_cost = float(state.ledger.cost)
                scoring_cost = min(1.0, ledger_cost)
                risk = float(state.ledger.risk)
                scoring_values: dict[str, float | None] = {
                    **truth,
                    "cost": scoring_cost,
                    "safety_risk": risk,
                }
                score = float(
                    task_score_observation(
                        contract=self.base_env.scoring_contract,
                        values=scoring_values,
                    )
                )
                metrics = {}
                for metric in self.spec["metrics"]:
                    metric_id = str(metric)
                    if metric_id == "score":
                        metrics[metric_id] = score
                    elif metric_id == "safety_risk":
                        metrics[metric_id] = risk
                    elif metric_id == "cost":
                        metrics[metric_id] = ledger_cost
                    elif metric_id in truth:
                        metrics[metric_id] = float(truth[metric_id])
                    else:
                        raise ValueError(f"mechanism truth lacks metric {metric_id}")
        except Exception as error:
            failure = {"type": type(error).__name__, "message": str(error)[:1000]}
            self.failure_count += 1

        row: dict[str, Any] = {
            "evaluation_id": evaluation_id,
            "phase": phase,
            "world_seed": self.world_seed,
            "vector": list(canonical),
            "status": (
                "failed"
                if failure is not None
                else "physical_failure"
                if physical_failure is not None
                else "completed"
            ),
            "safe": bool(
                failure is None
                and risk is not None
                and risk < float(get_task(self.task_id).safety_limit)
            ),
            "score": score,
            "safety_risk": risk,
            "ledger_cost": ledger_cost,
            "scoring_cost": scoring_cost,
            "metrics": metrics,
            "action_count": action_count,
            "recipe_metadata_sha256": metadata_sha256,
            "failure": failure,
            "physical_failure": physical_failure,
            "elapsed_s": round(perf_counter() - started, 6),
            "cache_hit": False,
        }
        self.rows.append(row)
        self._cache[canonical] = row
        output = copy.deepcopy(row)
        if extra:
            output.update(dict(extra))
        if self.progress_callback is not None:
            self.progress_callback(
                phase,
                self.request_count,
                self.failure_count + self.physical_failure_count,
            )
        return output


def _lexicographic_objective(row: Mapping[str, Any], safety_limit: float) -> float:
    if row.get("status") != "completed":
        return 2.0
    risk = float(row["safety_risk"])
    score = float(row["score"])
    if risk >= safety_limit:
        return 1.0 + (risk - safety_limit) - 1.0e-6 * score
    return -score


def _run_optimizer(
    evaluator: InMemoryMechanismEvaluator,
    *,
    task_id: str,
    world_seed: int,
    schema: Sequence[Mapping[str, Any]],
    initial_population: Sequence[Sequence[float]] | None = None,
) -> dict[str, Any]:
    population = np.asarray(
        initial_population
        if initial_population is not None
        else balanced_initial_population(task_id, world_seed, schema),
        dtype=float,
    )
    safety_limit = float(get_task(task_id).safety_limit)

    def objective(vector: np.ndarray) -> float:
        return _lexicographic_objective(
            evaluator.evaluate(vector, phase="optimizer"),
            safety_limit,
        )

    result = differential_evolution(
        objective,
        bounds=[(0.0, 1.0)] * len(schema),
        init=population,
        maxiter=OPTIMIZER_GENERATIONS,
        mutation=(0.5, 1.0),
        recombination=0.7,
        seed=deterministic_oracle_seed(task_id, world_seed),
        polish=False,
        workers=1,
        updating="immediate",
        tol=0.0,
        atol=-1.0,
    )
    return {
        "request_count": int(result.nfev),
        "generation_count": int(result.nit),
        "best_vector": list(_canonical_vector(result.x, schema)),
        "objective_value": float(result.fun),
        "success": bool(result.success),
        "message": str(result.message),
    }


class _Progress:
    def __init__(
        self,
        *,
        task_id: str,
        world_seed: int,
        progress_path: Path,
    ) -> None:
        self.task_id = task_id
        self.world_seed = world_seed
        self.progress_path = progress_path
        self.started = perf_counter()
        self.last_emit = self.started
        self.base_completed = 0

    def set_base(self, completed: int) -> None:
        self.base_completed = completed

    def update(
        self,
        stage: str,
        stage_completed: int,
        failures: int,
        *,
        force: bool = False,
    ) -> None:
        now = perf_counter()
        completed = self.base_completed + stage_completed
        if not force and stage_completed % 32 != 0 and now - self.last_emit < 30.0:
            return
        elapsed = now - self.started
        rate = completed / elapsed if elapsed > 0.0 else 0.0
        _emit(
            self.progress_path,
            {
                "event": "mechanism_oracle_progress",
                "task_id": self.task_id,
                "world_seed": self.world_seed,
                "stage": stage,
                "completed": completed,
                "total": TOTAL_WORLD_REQUESTS,
                "throughput_requests_per_minute": round(rate * 60.0, 2),
                "eta_s": (
                    round((TOTAL_WORLD_REQUESTS - completed) / rate, 1) if rate > 0.0 else None
                ),
                "failure_count": failures,
                "elapsed_s": round(elapsed, 1),
            },
        )
        self.last_emit = now


def _run_observed_validation(
    *,
    task_id: str,
    config: Mapping[str, Any],
    spec: Mapping[str, Any],
    world_seed: int,
    candidates: Sequence[Mapping[str, Any]],
    world_root: Path,
    progress: _Progress,
    prior_failure_count: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    output_root = world_root / "observed-validation"
    output_root.mkdir(parents=True, exist_ok=False)
    for candidate in candidates:
        rank = int(candidate["candidate_rank"])
        for replicate in range(1, VALIDATION_REPLICATES + 1):
            row = _execute_recipe(
                task_id=task_id,
                config=config,
                spec=spec,
                world_seed=world_seed,
                recipe_id=f"c{rank:02d}-r{replicate}",
                vector=candidate["vector"],
                phase="observed_validation",
                output_root=output_root,
                extra={
                    "candidate_rank": rank,
                    "replicate": replicate,
                    "oracle_score": float(candidate["oracle_score"]),
                    "oracle_risk": float(candidate["oracle_risk"]),
                },
            )
            rows.append(row)
            failures = prior_failure_count + sum(item.get("failure") is not None for item in rows)
            progress.update(
                "observed_validation",
                len(rows),
                failures,
                force=len(rows) == len(candidates) * VALIDATION_REPLICATES,
            )
    return rows


def _run_world(
    *,
    task_id: str,
    config: Mapping[str, Any],
    spec: Mapping[str, Any],
    world_seed: int,
    world_root: Path,
    progress_path: Path,
) -> dict[str, Any]:
    world_root.mkdir(parents=True, exist_ok=False)
    schema = _q1_coordinate_schema(task_id)
    progress = _Progress(
        task_id=task_id,
        world_seed=world_seed,
        progress_path=progress_path,
    )
    evaluator = InMemoryMechanismEvaluator(
        task_id=task_id,
        config=config,
        spec=spec,
        world_seed=world_seed,
        progress_callback=lambda stage, completed, failures: progress.update(
            stage,
            completed,
            failures,
        ),
    )
    started = perf_counter()
    try:
        optimizer = _run_optimizer(
            evaluator,
            task_id=task_id,
            world_seed=world_seed,
            schema=schema,
        )
        progress.update(
            "optimizer",
            int(optimizer["request_count"]),
            evaluator.failure_count + evaluator.physical_failure_count,
            force=True,
        )
        evaluator.progress_callback = None
        safe_optimizer_rows = [
            row
            for row in evaluator.rows
            if row.get("status") == "completed" and bool(row.get("safe"))
        ]
        optimum = (
            max(safe_optimizer_rows, key=lambda row: float(row["score"]))
            if safe_optimizer_rows
            else None
        )

        target_rows: list[dict[str, Any]] = []
        perturbation_rows: list[dict[str, Any]] = []
        progress.set_base(int(optimizer["request_count"]))
        if optimum is not None:
            target_design = local_target_grid(
                optimum["vector"],
                tuple(spec["target_indices"]),
            )
            for index, design in enumerate(target_design, start=1):
                target_rows.append(
                    evaluator.evaluate(
                        design["vector"],
                        phase="target_grid",
                        extra={
                            "grid_i": int(design["grid_i"]),
                            "grid_j": int(design["grid_j"]),
                            "offset": list(design["offset"]),
                        },
                    )
                )
                progress.update(
                    "target_grid",
                    index,
                    evaluator.failure_count + evaluator.physical_failure_count,
                    force=index == len(target_design),
                )

            progress.set_base(int(optimizer["request_count"]) + len(target_design))
            perturbations = full_dimensional_perturbations(
                task_id,
                world_seed,
                optimum["vector"],
                schema,
            )
            for index, vector in enumerate(perturbations, start=1):
                perturbation_rows.append(
                    evaluator.evaluate(
                        vector,
                        phase="full_dimensional_perturbation",
                        extra={"perturbation_index": index},
                    )
                )
                progress.update(
                    "full_dimensional_perturbation",
                    index,
                    evaluator.failure_count + evaluator.physical_failure_count,
                    force=index == len(perturbations),
                )

        candidates = select_validation_candidates(evaluator.rows)
        progress.set_base(
            int(optimizer["request_count"]) + len(target_rows) + len(perturbation_rows)
        )
        validation_rows = _run_observed_validation(
            task_id=task_id,
            config=config,
            spec=spec,
            world_seed=world_seed,
            candidates=candidates,
            world_root=world_root,
            progress=progress,
            prior_failure_count=evaluator.failure_count + evaluator.physical_failure_count,
        )
    finally:
        evaluator.close()

    analysis = analyze_mechanism_oracle_world(
        evaluator.rows,
        target_rows,
        validation_rows,
        optimizer_request_count=int(optimizer["request_count"]),
        optimizer_generation_count=int(optimizer["generation_count"]),
        task_threshold=float(get_task(task_id).threshold),
        safety_limit=float(get_task(task_id).safety_limit),
        primary_metric=str(spec["primary_metric"]),
        target_indices=tuple(spec["target_indices"]),
        require_safety_frontier=bool(spec["require_safety_frontier"]),
    )
    validation_failures = [
        {
            "recipe_id": row["recipe_id"],
            "phase": "observed_validation",
            **dict(row["failure"]),
        }
        for row in validation_rows
        if row.get("failure") is not None
    ]
    mechanism_failures = [
        {
            "evaluation_id": row["evaluation_id"],
            "phase": row["phase"],
            **dict(row["failure"]),
        }
        for row in evaluator.rows
        if row.get("failure") is not None
    ]
    physical_failures = [
        {
            "evaluation_id": row["evaluation_id"],
            "phase": row["phase"],
            **dict(row["physical_failure"]),
        }
        for row in evaluator.rows
        if row.get("physical_failure") is not None
    ]
    operational_failure = bool(mechanism_failures or validation_failures)
    report: dict[str, Any] = {
        "schema_version": WORLD_REPORT_VERSION,
        "qualification_schema_version": MECHANISM_ORACLE_VERSION,
        "formal_result": False,
        "task_id": task_id,
        "world_seed": world_seed,
        "coverage": {
            "initial_population_size": INITIAL_POPULATION_SIZE,
            "optimizer_generations": OPTIMIZER_GENERATIONS,
            "optimizer_expected_requests": EXPECTED_OPTIMIZER_REQUESTS,
            "target_grid_side": TARGET_GRID_SIDE,
            "target_grid_requests": len(target_rows),
            "full_perturbation_requests": len(perturbation_rows),
            "validation_candidate_count": len(candidates),
            "validation_execution_count": len(validation_rows),
        },
        "optimizer": optimizer,
        "validation_candidates": candidates,
        "analysis": analysis,
        "operational_failure": operational_failure,
        "failure_count": len(mechanism_failures) + len(validation_failures),
        "failures": [*mechanism_failures, *validation_failures],
        "physical_failure_count": len(physical_failures),
        "physical_failures": physical_failures,
        "mechanism_rows": evaluator.rows,
        "target_grid_rows": target_rows,
        "full_perturbation_rows": perturbation_rows,
        "validation_rows": validation_rows,
        "elapsed_s": round(perf_counter() - started, 3),
    }
    report["report_sha256"] = canonical_json_sha256(report)
    write_json_atomic(world_root / "world-report.json", report)
    return report


def _decision(world_reports: Sequence[Mapping[str, Any]]) -> str:
    if any(bool(report["operational_failure"]) for report in world_reports):
        return "inconclusive_platform_failure_restart_task_from_world0"
    if all(bool(report["analysis"]["passed"]) for report in world_reports):
        return "proceed_to_q2_matched_prior_construction"
    return "reject_candidate_cohort_before_q2"


def run(args: argparse.Namespace) -> dict[str, Any]:
    task_id = str(args.task_id)
    spec = TASK_SPECS[task_id]
    scoped_dirty = _scoped_dirty_paths()
    if scoped_dirty:
        raise RuntimeError(
            "mechanism-oracle qualification requires clean Work II/runtime sources: "
            + ", ".join(scoped_dirty)
        )
    output_root = args.output_root.resolve()
    summary_path = args.summary.resolve()
    progress_path = args.progress_file.resolve()
    if output_root.exists() or summary_path.exists():
        raise FileExistsError("refusing to overwrite existing mechanism-oracle output")
    config_path = (ROOT / str(spec["config"])).resolve()
    config = _load(config_path)
    if config.get("task_id") != task_id:
        raise ValueError("mechanism-oracle config task differs from selected task")
    q0 = _q0_audit(task_id, config, spec)
    _emit(
        progress_path,
        {
            "event": "mechanism_oracle_q0_completed",
            "task_id": task_id,
            "passed": q0["passed"],
            "checks": q0["checks"],
        },
    )
    if not q0["passed"]:
        raise RuntimeError("mechanism-oracle Q0 audit failed")

    output_root.mkdir(parents=True)
    started = perf_counter()
    world_reports: list[dict[str, Any]] = []
    for world_index, world_seed in enumerate(get_task(task_id).seeds, start=1):
        _emit(
            progress_path,
            {
                "event": "mechanism_oracle_world_started",
                "task_id": task_id,
                "world_seed": world_seed,
                "world_index": world_index,
                "world_total": 5,
            },
        )
        report = _run_world(
            task_id=task_id,
            config=config,
            spec=spec,
            world_seed=int(world_seed),
            world_root=output_root / f"world-{world_seed}",
            progress_path=progress_path,
        )
        world_reports.append(report)
        _emit(
            progress_path,
            {
                "event": "mechanism_oracle_world_completed",
                "task_id": task_id,
                "world_seed": world_seed,
                "world_index": world_index,
                "world_total": 5,
                "passed": report["analysis"]["passed"],
                "operational_failure": report["operational_failure"],
                "oracle_score": (
                    None
                    if report["analysis"]["oracle_optimum"] is None
                    else report["analysis"]["oracle_optimum"]["score"]
                ),
                "failures": report["failure_count"],
                "elapsed_s": report["elapsed_s"],
            },
        )

    decision = _decision(world_reports)
    raw_bindings = []
    for report in world_reports:
        path = output_root / f"world-{report['world_seed']}" / "world-report.json"
        raw_bindings.append(
            {
                "world_seed": report["world_seed"],
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(path),
                "passed": report["analysis"]["passed"],
                "operational_failure": report["operational_failure"],
            }
        )
    failures = [
        {"world_seed": report["world_seed"], **failure}
        for report in world_reports
        for failure in report["failures"]
    ]
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": MECHANISM_ORACLE_VERSION,
        "formal_result": False,
        "source_commit": git_source_commit(ROOT),
        "scoped_runtime_clean": True,
        "unrelated_dirty_paths_excluded": [
            line[3:].strip().replace("\\", "/")
            for line in subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            ).stdout.splitlines()
            if not line[3:]
            .strip()
            .replace("\\", "/")
            .startswith(("src/", "scripts/", "configs/benchmark/", "workstreams/flagship_tasks/"))
        ],
        "task_id": task_id,
        "world_seeds": list(get_task(task_id).seeds),
        "q0": q0,
        "coverage": {
            "world_count": 5,
            "optimizer_requests_per_world": EXPECTED_OPTIMIZER_REQUESTS,
            "target_grid_requests_per_world": TARGET_GRID_SIDE**2,
            "full_perturbations_per_world": FULL_PERTURBATION_COUNT,
            "observed_validations_per_world": VALIDATION_EXECUTION_COUNT,
            "planned_request_count": 5 * TOTAL_WORLD_REQUESTS,
        },
        "denominators": {
            "world_count": 5,
            "passed_world_count": sum(
                bool(report["analysis"]["passed"]) for report in world_reports
            ),
            "operational_failure_world_count": sum(
                bool(report["operational_failure"]) for report in world_reports
            ),
            "unique_mechanism_evaluation_count": sum(
                int(report["analysis"]["mechanism_evaluation_count"]) for report in world_reports
            ),
            "completed_mechanism_evaluation_count": sum(
                int(report["analysis"]["mechanism_completed_count"]) for report in world_reports
            ),
            "observed_validation_count": sum(
                int(report["analysis"]["observed_validation_completed_count"])
                for report in world_reports
            ),
            "observed_validation_exact_replay_count": sum(
                int(report["analysis"]["observed_validation_exact_replay_count"])
                for report in world_reports
            ),
            "provider_call_count": 0,
            "physical_failure_count": sum(
                int(report["physical_failure_count"]) for report in world_reports
            ),
        },
        "worlds": [
            {
                "world_seed": report["world_seed"],
                "passed": report["analysis"]["passed"],
                "operational_failure": report["operational_failure"],
                "elapsed_s": report["elapsed_s"],
                "analysis": report["analysis"],
            }
            for report in world_reports
        ],
        "raw_bindings": raw_bindings,
        "failure_count": len(failures),
        "failures": failures,
        "qualification_passed": decision == "proceed_to_q2_matched_prior_construction",
        "q2_authorized": decision == "proceed_to_q2_matched_prior_construction",
        "restart_required": decision.startswith("inconclusive_platform_failure"),
        "decision": decision,
        "elapsed_s": round(perf_counter() - started, 3),
        "interpretation": (
            "Provider-free evaluator qualification. Historical threshold reachability is "
            "diagnostic; the pass decision uses safe oracle-relative quality, local-law "
            "identifiability and independent observed replay."
        ),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(summary_path, summary)
    _emit(
        progress_path,
        {
            "event": "mechanism_oracle_task_completed",
            "task_id": task_id,
            "passed_worlds": summary["denominators"]["passed_world_count"],
            "worlds": 5,
            "operational_failure_worlds": summary["denominators"][
                "operational_failure_world_count"
            ],
            "observed_validation_exact_replay": summary["denominators"][
                "observed_validation_exact_replay_count"
            ],
            "decision": decision,
            "elapsed_s": summary["elapsed_s"],
            "summary": str(summary_path),
        },
    )
    return summary


def benchmark(args: argparse.Namespace) -> dict[str, Any]:
    task_id = str(args.task_id)
    spec = TASK_SPECS[task_id]
    config = _load((ROOT / str(spec["config"])).resolve())
    schema = _q1_coordinate_schema(task_id)
    population = balanced_initial_population(task_id, int(args.world_seed), schema)
    count = min(int(args.benchmark_count), len(population))
    evaluator = InMemoryMechanismEvaluator(
        task_id=task_id,
        config=config,
        spec=spec,
        world_seed=int(args.world_seed),
    )
    started = perf_counter()
    rows: list[dict[str, Any]] = []
    try:
        for vector in population[:count]:
            rows.append(evaluator.evaluate(vector, phase="benchmark"))
    finally:
        evaluator.close()
    elapsed = perf_counter() - started
    report = {
        "task_id": task_id,
        "world_seed": int(args.world_seed),
        "requested": count,
        "completed": sum(row["status"] == "completed" for row in rows),
        "failures": sum(row["status"] != "completed" for row in rows),
        "elapsed_s": round(elapsed, 6),
        "requests_per_minute": round(count / elapsed * 60.0, 2) if elapsed > 0.0 else None,
        "estimated_five_world_hours": round(
            (5 * TOTAL_WORLD_REQUESTS) / (count / elapsed) / 3600.0,
            3,
        )
        if elapsed > 0.0 and count > 0
        else None,
        "score_min": min(
            (float(row["score"]) for row in rows if row["score"] is not None),
            default=None,
        ),
        "score_max": max(
            (float(row["score"]) for row in rows if row["score"] is not None),
            default=None,
        ),
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True), flush=True)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", choices=sorted(TASK_SPECS), required=True)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--benchmark-count", type=int, default=0)
    parser.add_argument("--world-seed", type=int, default=0)
    args = parser.parse_args()
    if args.benchmark_count:
        if args.benchmark_count < 1:
            parser.error("--benchmark-count must be positive")
        benchmark(args)
        return 0
    if args.output_root is None or args.summary is None or args.progress_file is None:
        parser.error("qualification requires --output-root, --summary and --progress-file")
    summary = run(args)
    if summary["restart_required"]:
        return 3
    return 0 if summary["qualification_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
