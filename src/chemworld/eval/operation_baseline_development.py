"""Train/Dev-only audit for frozen operation-level control baselines."""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from collections import Counter, defaultdict
from collections.abc import Iterator, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import fmean
from typing import Any

from chemworld.agents.operation_baselines import OPERATION_BASELINE_IDS
from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.formal_operation import (
    audit_operation_method_freeze,
    load_operation_method_freeze,
    make_frozen_operation_agent,
)
from chemworld.eval.formal_protocol_v0_4 import CORE_TASKS, load_formal_protocol
from chemworld.eval.formal_runner import canonical_sha256
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task
from chemworld.world.world_family import axes_for_task

ROOT = Path(__file__).resolve().parents[3]
OPERATION_DEVELOPMENT_VERSION = "chemworld-operation-baseline-development-audit-0.4.1"
OPERATION_DEVELOPMENT_PLAN_VERSION = "chemworld-operation-development-plan-0.4.1"
DEFAULT_PLAN_PATH = (
    ROOT / "configs" / "methods" / "operation_v0.4.1" / "operation_development_plan.json"
)
DEFAULT_REPORT_PATH = (
    ROOT
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "operation-baselines-dev-v0.4.1.json"
)
FORMAL_CHECKPOINTS = (4, 8, 12, 20, 40)
NUMERIC_THREAD_ENV_VARS = (
    "OPENBLAS_NUM_THREADS",
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)
NUMERIC_THREADS_PER_WORKER = 1


@contextmanager
def _numeric_worker_environment() -> Iterator[None]:
    """Prevent process workers from recursively oversubscribing numeric threads."""

    previous = {name: os.environ.get(name) for name in NUMERIC_THREAD_ENV_VARS}
    try:
        for name in NUMERIC_THREAD_ENV_VARS:
            os.environ[name] = str(NUMERIC_THREADS_PER_WORKER)
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def _default_cache_root() -> Path:
    raw = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=ROOT,
        text=True,
    ).strip()
    path = Path(raw)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    return path / "chemworld-private" / "operation-dev-v0.4.1"


DEFAULT_CACHE_ROOT = _default_cache_root()


@dataclass(frozen=True)
class OperationDevelopmentCell:
    split: str
    task_id: str
    method_id: str
    world_seed: int
    method_seed: int
    complete_experiments: int
    operation_limit: int
    risk_limit: float
    world_interventions: tuple[dict[str, Any], ...]
    formal_protocol_sha256: str
    method_freeze_sha256: str
    development_plan_sha256: str
    method_artifact_sha256: str
    source_commit: str
    determinism_check: bool = False

    @property
    def cell_id(self) -> str:
        return canonical_sha256(
            {
                "schema_version": OPERATION_DEVELOPMENT_VERSION,
                **asdict(self),
            }
        )


def load_operation_development_plan(
    path: str | Path = DEFAULT_PLAN_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("operation development plan must be a JSON object")
    if payload.get("schema_version") != OPERATION_DEVELOPMENT_PLAN_VERSION:
        raise ValueError("operation development plan schema is unsupported")
    return payload


def audit_operation_development_plan(
    plan: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = load_operation_development_plan() if plan is None else plan
    reasons: list[str] = []
    expected_tasks = list(CORE_TASKS)
    expected_methods = list(OPERATION_BASELINE_IDS)
    if resolved.get("status") != "preregistered_bench_unseen":
        reasons.append("status_invalid")
    if resolved.get("bench_access_allowed") is not False:
        reasons.append("bench_access_guard_invalid")
    if resolved.get("reference_search_access_allowed") is not False:
        reasons.append("reference_access_guard_invalid")
    if resolved.get("task_ids") != expected_tasks:
        reasons.append("task_set_or_order_mismatch")
    if resolved.get("method_ids") != expected_methods:
        reasons.append("method_set_or_order_mismatch")
    split = resolved.get("split_contract")
    if not isinstance(split, Mapping):
        reasons.append("split_contract_missing")
    else:
        expected_ranges = {
            "train_seeds": {"start": 10_000, "stop_inclusive": 10_003},
            "dev_seeds": {"start": 11_000, "stop_inclusive": 11_019},
        }
        for name, expected in expected_ranges.items():
            if split.get(name) != expected:
                reasons.append(f"{name}_mismatch")
        if split.get("paired_world_and_method_rng") is not True:
            reasons.append("paired_rng_contract_missing")
        if split.get("public_world_family_interventions") is not True:
            reasons.append("public_intervention_contract_missing")
    budget = resolved.get("budget_contract")
    if not isinstance(budget, Mapping):
        reasons.append("budget_contract_missing")
    else:
        if budget.get("complete_experiments_per_cell") != 40:
            reasons.append("complete_experiment_budget_mismatch")
        if budget.get("checkpoints") != list(FORMAL_CHECKPOINTS):
            reasons.append("checkpoint_contract_mismatch")
        if budget.get("runner_action_repair") is not False:
            reasons.append("action_repair_guard_invalid")
        if budget.get("runner_automatic_closeout") is not False:
            reasons.append("automatic_closeout_guard_invalid")
    return {
        "schema_version": "chemworld-operation-development-plan-audit-0.4.1",
        "status": "ready" if not reasons else "failed",
        "plan_ready": not reasons,
        "bench_access_allowed": False,
        "reference_search_access_allowed": False,
        "reasons": sorted(set(reasons)),
    }


def _trajectory_digest(history: Sequence[Any]) -> str:
    payload = [
        {
            "step": record.step,
            "action": record.action,
            "observation": record.observation,
            "reward": record.reward,
            "event_type": record.event_type,
            "decision_audit": record.decision_audit,
            "constraint_flags": record.info.get("constraint_flags", {}),
            "transaction_status": record.info.get("transaction_status"),
        }
        for record in history
    ]
    return canonical_sha256({"records": payload})


def _primary_values(
    terminal: Sequence[Any],
    primary_metric: str,
) -> tuple[list[float | None], list[float | None]]:
    values: list[float | None] = []
    curve: list[float | None] = []
    current: float | None = None
    for record in terminal:
        raw = record.observation.get(primary_metric)
        value = (
            float(raw)
            if isinstance(raw, int | float)
            and not isinstance(raw, bool)
            and math.isfinite(float(raw))
            else None
        )
        values.append(value)
        if value is not None:
            current = value if current is None else max(current, value)
        curve.append(current)
    return values, curve


def _run_cell_once(cell: OperationDevelopmentCell) -> tuple[dict[str, Any], str]:
    task = get_task(cell.task_id)
    agent = make_frozen_operation_agent(cell.method_id)
    history = run_agent(
        env_id=task.env_id,
        agent=agent,
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=cell.world_seed,
        agent_seed=cell.method_seed,
        task_id=task.task_id,
        budget_override=cell.operation_limit,
        episode_mode_override="campaign",
        method_resource_limits={
            "operation_limit": cell.operation_limit,
            "complete_experiment_limit": cell.complete_experiments,
            "checkpoint_complete_experiments": tuple(
                point for point in FORMAL_CHECKPOINTS if point <= cell.complete_experiments
            ),
        },
        world_interventions=cell.world_interventions,
        safety_limit_override=cell.risk_limit,
    )
    terminal = [record for record in history if record.event_type == "experiment_end"]
    protocol_task = load_formal_protocol()["task_roles"]["formal_core"][cell.task_id]
    primary_metric = str(protocol_task["primary_metric"])
    primary_values, best_curve = _primary_values(terminal, primary_metric)
    action_counts = Counter(str(record.action.get("operation", "invalid")) for record in history)
    invalid_reasons: Counter[str] = Counter()
    invalid_operation_count = 0
    runtime_domain_failure_count = 0
    for record in history:
        flags = record.info.get("constraint_flags", {})
        if isinstance(flags, Mapping) and flags.get("precondition_failed", False):
            invalid_operation_count += 1
            preconditions = record.info.get("preconditions", {})
            if isinstance(preconditions, Mapping):
                failed = [str(key) for key, passed in preconditions.items() if not passed]
                invalid_reasons.update(failed or ("unspecified_precondition",))
                runtime_domain_failure_count += int(
                    preconditions.get("runtime_domain_valid") is False
                )
    decision_audits_complete = all(
        record.decision_audit.get("status") == "provided" for record in history
    )
    measurement_adaptation_count = sum(
        record.decision_audit.get("adaptation_source") == "measurement" for record in history
    )
    measurement_count = sum(record.action.get("operation") == "measure" for record in history)
    final_assay_count = sum(
        record.action.get("operation") == "measure"
        and record.action.get("instrument") == "final_assay"
        for record in history
    )
    final_resources = history[-1].method_resources if history else {}
    agent_usage = final_resources.get("agent_usage", {})
    result = {
        "schema_version": OPERATION_DEVELOPMENT_VERSION,
        "cell_id": cell.cell_id,
        "split": cell.split,
        "task_id": cell.task_id,
        "method_id": cell.method_id,
        "world_seed": cell.world_seed,
        "method_seed_role": "paired_public_development_rng",
        "formal_protocol_sha256": cell.formal_protocol_sha256,
        "method_freeze_sha256": cell.method_freeze_sha256,
        "development_plan_sha256": cell.development_plan_sha256,
        "method_artifact_sha256": cell.method_artifact_sha256,
        "source_commit": cell.source_commit,
        "complete_experiment_count": len(terminal),
        "operation_limit": cell.operation_limit,
        "operation_count": len(history),
        "measurement_count": measurement_count,
        "final_assay_count": final_assay_count,
        "primary_metric": primary_metric,
        "primary_terminal_values": primary_values,
        "primary_values_complete": len(primary_values) == cell.complete_experiments
        and all(value is not None for value in primary_values),
        "best_curve": best_curve,
        "action_counts": dict(sorted(action_counts.items())),
        "distinct_operation_count": len(action_counts),
        "invalid_operation_count": invalid_operation_count,
        "invalid_reason_counts": dict(sorted(invalid_reasons.items())),
        "runtime_domain_failure_count": runtime_domain_failure_count,
        "decision_audit_count": len(history),
        "decision_audits_complete": decision_audits_complete,
        "measurement_adaptation_count": measurement_adaptation_count,
        "cpu_time_s": float(agent_usage.get("cpu_time_s", 0.0)),
        "gpu_time_s": float(agent_usage.get("gpu_time_s", 0.0)),
        "run_wall_time_s": float(final_resources.get("run_wall_time_s", 0.0)),
        "provider_request_count": int(agent_usage.get("model_call_count", 0)),
        "training_environment_step_count": int(
            agent_usage.get("training_environment_step_count", 0)
        ),
        "accounting_complete": final_resources.get("accounting_complete") is True,
        "world_interventions": list(cell.world_interventions),
    }
    return result, _trajectory_digest(history)


def _run_development_cell(
    cell: OperationDevelopmentCell,
    cache_root: str,
) -> dict[str, Any]:
    root = Path(cache_root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{cell.cell_id}.json"
    if path.is_file():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached.get("cell_id") == cell.cell_id:
            return cached
    result, first_digest = _run_cell_once(cell)
    result["trajectory_digest"] = first_digest
    if cell.determinism_check:
        _, second_digest = _run_cell_once(cell)
        result["determinism_checked"] = True
        result["deterministic_replay"] = first_digest == second_digest
    else:
        result["determinism_checked"] = False
        result["deterministic_replay"] = None
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
    return result


def _paired_method_seed(split: str, world_seed: int) -> int:
    digest = hashlib.sha256(f"operation-v0.4:{split}:{world_seed}".encode()).digest()
    return 300_000 + int.from_bytes(digest[:4], "big") % 700_000_000


def _public_interventions(
    protocol: Mapping[str, Any],
    *,
    task_id: str,
    split: str,
    seed: int,
) -> tuple[dict[str, Any], ...]:
    public = protocol["world_family_contract"]["public_development_severities"][split]
    modes = tuple(sorted(public))
    offset = seed - int(protocol["split_contract"][split]["base_seeds"]["start"])
    mode = modes[offset % len(modes)]
    severities = tuple(float(item) for item in public[mode])
    severity = severities[(offset // len(modes)) % len(severities)]
    axes = axes_for_task(task_id)
    axis = axes[(offset // max(1, len(modes) * len(severities))) % len(axes)]
    return ({"axis_id": axis.axis_id, "mode": mode, "severity": severity},)


def build_operation_development_cells(
    *,
    tasks: Sequence[str] = CORE_TASKS,
    methods: Sequence[str] | None = None,
    train_seeds: Sequence[int] = tuple(range(10_000, 10_004)),
    dev_seeds: Sequence[int] = tuple(range(11_000, 11_020)),
    complete_experiments: int = 40,
) -> list[OperationDevelopmentCell]:
    plan = load_operation_development_plan()
    if audit_operation_development_plan(plan)["plan_ready"] is not True:
        raise RuntimeError("operation development plan must pass before cell construction")
    protocol = load_formal_protocol()
    freeze = load_operation_method_freeze()
    if audit_operation_method_freeze(freeze)["controls_ready"] is not True:
        raise RuntimeError("operation method freeze must pass before cell construction")
    selected_methods = tuple(OPERATION_BASELINE_IDS) if methods is None else tuple(methods)
    if not tasks or not selected_methods or not train_seeds or not dev_seeds:
        raise ValueError("operation development requires non-empty tasks, methods, and splits")
    if len(set(tasks)) != len(tasks) or len(set(selected_methods)) != len(selected_methods):
        raise ValueError("operation development tasks and methods must be unique")
    if not set(tasks).issubset(protocol["task_roles"]["formal_core"]):
        raise ValueError("operation development task is outside the formal core")
    if not set(selected_methods).issubset(freeze["methods"]):
        raise ValueError("operation development method is not frozen")
    if not 2 <= complete_experiments <= 40:
        raise ValueError("operation development requires 2..40 complete experiments")
    ranges = protocol["split_contract"]
    protocol_sha256 = canonical_sha256(protocol)
    freeze_sha256 = canonical_sha256(freeze)
    plan_sha256 = canonical_sha256(plan)
    source_commit = _git_commit()
    first_train = min(train_seeds)
    cells: list[OperationDevelopmentCell] = []
    for split, seeds in (("train", train_seeds), ("dev", dev_seeds)):
        start = int(ranges[split]["base_seeds"]["start"])
        stop = int(ranges[split]["base_seeds"]["stop_inclusive"])
        if len(set(seeds)) != len(seeds):
            raise ValueError(f"{split} seeds contain duplicates")
        if any(seed < start or seed > stop for seed in seeds):
            raise ValueError(f"{split} seed is outside the public formal range")
        for seed in seeds:
            for task_id in tasks:
                task = get_task(task_id)
                operation_limit = 2 * task_recipe_event_count(task.to_dict()) * complete_experiments
                interventions = _public_interventions(
                    protocol,
                    task_id=task_id,
                    split=split,
                    seed=seed,
                )
                for method_id in selected_methods:
                    cells.append(
                        OperationDevelopmentCell(
                            split=split,
                            task_id=task_id,
                            method_id=method_id,
                            world_seed=seed,
                            method_seed=_paired_method_seed(split, seed),
                            complete_experiments=complete_experiments,
                            operation_limit=operation_limit,
                            risk_limit=float(
                                protocol["task_roles"]["formal_core"][task_id]["risk_limit"]
                            ),
                            world_interventions=interventions,
                            formal_protocol_sha256=protocol_sha256,
                            method_freeze_sha256=freeze_sha256,
                            development_plan_sha256=plan_sha256,
                            method_artifact_sha256=str(
                                freeze["methods"][method_id]["artifact_sha256"]
                            ),
                            source_commit=source_commit,
                            determinism_check=split == "train" and seed == first_train,
                        )
                    )
    return cells


def _mean(values: Sequence[float | None]) -> float | None:
    finite = [float(value) for value in values if value is not None and math.isfinite(value)]
    return fmean(finite) if finite else None


def _method_task_summary(
    method_id: str,
    task_id: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    complete_experiments: int,
) -> dict[str, Any]:
    train = [row for row in rows if row["split"] == "train"]
    dev = [row for row in rows if row["split"] == "dev"]
    checkpoints = tuple(point for point in FORMAL_CHECKPOINTS if point <= complete_experiments)
    mean_curve = {
        str(point): _mean(
            [
                row["best_curve"][point - 1] if len(row["best_curve"]) >= point else None
                for row in dev
            ]
        )
        for point in checkpoints
    }
    action_counts: Counter[str] = Counter()
    invalid_reasons: Counter[str] = Counter()
    for row in rows:
        action_counts.update(row["action_counts"])
        invalid_reasons.update(row["invalid_reason_counts"])
    deterministic = [row for row in train if row["determinism_checked"]]
    return {
        "method_id": method_id,
        "task_id": task_id,
        "train_cell_count": len(train),
        "dev_cell_count": len(dev),
        "mean_dev_best_primary": _mean(
            [row["best_curve"][-1] if row["best_curve"] else None for row in dev]
        ),
        "mean_budget_curve": mean_curve,
        "action_counts": dict(sorted(action_counts.items())),
        "distinct_operation_count": len(action_counts),
        "invalid_operation_count": sum(int(row["invalid_operation_count"]) for row in rows),
        "invalid_reason_counts": dict(sorted(invalid_reasons.items())),
        "runtime_domain_failure_count": sum(
            int(row["runtime_domain_failure_count"]) for row in rows
        ),
        "measurement_adaptation_count": sum(
            int(row["measurement_adaptation_count"]) for row in rows
        ),
        "determinism_check_count": len(deterministic),
        "deterministic_replay": bool(deterministic)
        and all(row["deterministic_replay"] is True for row in deterministic),
        "all_cells_complete": all(
            int(row["complete_experiment_count"]) == complete_experiments for row in rows
        ),
        "all_primary_values_complete": all(row["primary_values_complete"] is True for row in rows),
        "all_decision_audits_complete": all(
            row["decision_audits_complete"] is True for row in rows
        ),
        "accounting_complete": all(row["accounting_complete"] is True for row in rows),
    }


def _method_summary(
    method_id: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    complete_experiments: int,
) -> dict[str, Any]:
    by_task: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_task[str(row["task_id"])].append(row)
    task_summaries = {
        task_id: _method_task_summary(
            method_id,
            task_id,
            task_rows,
            complete_experiments=complete_experiments,
        )
        for task_id, task_rows in sorted(by_task.items())
    }
    return {
        "method_id": method_id,
        "task_summaries": task_summaries,
        "cell_count": len(rows),
        "invalid_operation_count": sum(
            int(summary["invalid_operation_count"]) for summary in task_summaries.values()
        ),
        "runtime_domain_failure_count": sum(
            int(summary["runtime_domain_failure_count"]) for summary in task_summaries.values()
        ),
        "measurement_adaptation_count": sum(
            int(summary["measurement_adaptation_count"]) for summary in task_summaries.values()
        ),
        "all_cells_complete": all(
            summary["all_cells_complete"] for summary in task_summaries.values()
        ),
        "all_primary_values_complete": all(
            summary["all_primary_values_complete"] for summary in task_summaries.values()
        ),
        "all_decision_audits_complete": all(
            summary["all_decision_audits_complete"] for summary in task_summaries.values()
        ),
        "accounting_complete": all(
            summary["accounting_complete"] for summary in task_summaries.values()
        ),
        "deterministic_replay": all(
            summary["deterministic_replay"] for summary in task_summaries.values()
        ),
    }


def run_operation_baseline_development_audit(
    *,
    tasks: Sequence[str] = CORE_TASKS,
    methods: Sequence[str] | None = None,
    train_seeds: Sequence[int] = tuple(range(10_000, 10_004)),
    dev_seeds: Sequence[int] = tuple(range(11_000, 11_020)),
    complete_experiments: int = 40,
    workers: int | None = None,
    cache_root: str | Path = DEFAULT_CACHE_ROOT,
    report_path: str | Path | None = DEFAULT_REPORT_PATH,
) -> dict[str, Any]:
    """Run public Train/Dev controls without opening Bench or reference-search."""

    plan = load_operation_development_plan()
    plan_audit = audit_operation_development_plan(plan)
    freeze = load_operation_method_freeze()
    freeze_audit = audit_operation_method_freeze(freeze)
    if plan_audit["plan_ready"] is not True or freeze_audit["controls_ready"] is not True:
        raise RuntimeError("operation development controls must pass before execution")
    source_commit = _git_commit()
    source_tree_clean_at_start = _git_tree_clean()
    cells = build_operation_development_cells(
        tasks=tasks,
        methods=methods,
        train_seeds=train_seeds,
        dev_seeds=dev_seeds,
        complete_experiments=complete_experiments,
    )
    if any(cell.source_commit != source_commit for cell in cells):
        raise RuntimeError("source commit changed while operation cells were being issued")
    if workers is not None and workers < 1:
        raise ValueError("workers must be positive")
    worker_count = workers or max(1, min(12, (os.cpu_count() or 2) - 1))
    if worker_count == 1:
        rows = [_run_development_cell(cell, str(cache_root)) for cell in cells]
    else:
        rows = []
        with (
            _numeric_worker_environment(),
            ProcessPoolExecutor(max_workers=worker_count) as executor,
        ):
            futures = {
                executor.submit(_run_development_cell, cell, str(cache_root)): cell
                for cell in cells
            }
            for future in as_completed(futures):
                rows.append(future.result())
    rows.sort(
        key=lambda row: (
            row["split"],
            row["world_seed"],
            row["task_id"],
            row["method_id"],
        )
    )
    by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_method[str(row["method_id"])].append(row)
    summaries = {
        method_id: _method_summary(
            method_id,
            method_rows,
            complete_experiments=complete_experiments,
        )
        for method_id, method_rows in sorted(by_method.items())
    }
    full_scope = (
        tuple(tasks) == CORE_TASKS
        and tuple(summaries) == tuple(sorted(OPERATION_BASELINE_IDS))
        and tuple(train_seeds) == tuple(range(10_000, 10_004))
        and tuple(dev_seeds) == tuple(range(11_000, 11_020))
        and complete_experiments == 40
        and len(rows) == 288
    )
    all_cells_complete = all(
        int(row["complete_experiment_count"]) == complete_experiments for row in rows
    )
    all_primary_values_complete = all(row["primary_values_complete"] is True for row in rows)
    all_accounting_complete = all(row["accounting_complete"] is True for row in rows)
    all_decision_audits_complete = all(row["decision_audits_complete"] is True for row in rows)
    all_checked_replays_deterministic = all(
        row["deterministic_replay"] is True for row in rows if row["determinism_checked"]
    ) and sum(row["determinism_checked"] is True for row in rows) == len(tasks) * len(summaries)
    nonrandom_invalid_controls_pass = all(
        summaries[method_id]["invalid_operation_count"] == 0
        for method_id in ("observation_blind", "rule_based")
        if method_id in summaries
    )
    diversity_controls_pass = all(
        int(task_summary["distinct_operation_count"]) >= 3
        for summary in summaries.values()
        for task_summary in summary["task_summaries"].values()
    )
    rule_adaptation_controls_pass = "rule_based" not in summaries or (
        set(summaries["rule_based"]["task_summaries"]) == set(tasks)
        and all(
            int(summary["measurement_adaptation_count"]) > 0
            for summary in summaries["rule_based"]["task_summaries"].values()
        )
    )
    random_invalid_count = int(
        summaries.get("operation_random", {}).get("invalid_operation_count", 0)
    )
    method_controls_pass = all(
        (
            all_cells_complete,
            all_primary_values_complete,
            all_accounting_complete,
            all_decision_audits_complete,
            all_checked_replays_deterministic,
            nonrandom_invalid_controls_pass,
            diversity_controls_pass,
            rule_adaptation_controls_pass,
        )
    )
    source_commit_before_report = _git_commit()
    source_commit_stable = source_commit_before_report == source_commit
    source_tree_clean_before_report = _git_tree_clean()
    formal_ready = all(
        (
            full_scope,
            source_tree_clean_at_start,
            source_commit_stable,
            source_tree_clean_before_report,
            method_controls_pass,
        )
    )
    protocol = load_formal_protocol()
    report = {
        "schema_version": OPERATION_DEVELOPMENT_VERSION,
        "status": (
            "formal_operation_baselines_ready" if formal_ready else "development_diagnostic_only"
        ),
        "formal_operation_baselines_ready": formal_ready,
        "bench_results_present": False,
        "reference_search_results_used": False,
        "split_scope": ["train", "dev"],
        "source_commit": source_commit,
        "source_commit_before_report": source_commit_before_report,
        "source_commit_stable": source_commit_stable,
        "source_tree_clean_at_start": source_tree_clean_at_start,
        "source_tree_clean_before_report": source_tree_clean_before_report,
        "formal_protocol_sha256": canonical_sha256(protocol),
        "operation_freeze_sha256": canonical_sha256(freeze),
        "operation_development_plan_sha256": canonical_sha256(plan),
        "tasks": list(tasks),
        "methods": sorted(summaries),
        "train_seeds": list(train_seeds),
        "dev_seeds": list(dev_seeds),
        "complete_experiments_per_cell": complete_experiments,
        "cell_count": len(rows),
        "worker_count": worker_count,
        "numeric_threads_per_worker": (
            NUMERIC_THREADS_PER_WORKER if worker_count > 1 else None
        ),
        "cache_root_role": "git_private_resumable_development_cache",
        "selection_policy": (
            "all three methods are mandatory interaction controls; no cross-observation-set "
            "champion is selected"
        ),
        "method_summaries": summaries,
        "acceptance": {
            "full_preregistered_development_scope": full_scope,
            "source_tree_clean_at_start": source_tree_clean_at_start,
            "source_commit_stable": source_commit_stable,
            "source_tree_clean_before_report": source_tree_clean_before_report,
            "all_method_controls_pass": method_controls_pass,
            "all_cells_complete": all_cells_complete,
            "all_primary_values_complete": all_primary_values_complete,
            "all_accounting_complete": all_accounting_complete,
            "all_decision_audits_complete": all_decision_audits_complete,
            "all_checked_replays_deterministic": all_checked_replays_deterministic,
            "nonrandom_invalid_controls_pass": nonrandom_invalid_controls_pass,
            "action_diversity_controls_pass": diversity_controls_pass,
            "rule_measurement_adaptation_controls_pass": rule_adaptation_controls_pass,
            "operation_random_invalid_operation_count": random_invalid_count,
            "operation_random_invalid_actions_retained": True,
            "bench_feedback_used": False,
            "reference_search_feedback_used": False,
        },
        "cells": rows,
    }
    if report_path is not None:
        destination = Path(report_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        temporary.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(destination)
    return report


def _git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()


def _git_tree_clean() -> bool:
    return not subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=normal"],
        cwd=ROOT,
        text=True,
    ).strip()


__all__ = [
    "DEFAULT_CACHE_ROOT",
    "DEFAULT_PLAN_PATH",
    "DEFAULT_REPORT_PATH",
    "OPERATION_DEVELOPMENT_PLAN_VERSION",
    "OPERATION_DEVELOPMENT_VERSION",
    "OperationDevelopmentCell",
    "audit_operation_development_plan",
    "build_operation_development_cells",
    "load_operation_development_plan",
    "run_operation_baseline_development_audit",
]
