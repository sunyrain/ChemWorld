"""Train/Dev-only execution and selection audit for frozen classic methods."""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from collections import defaultdict
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import fmean
from typing import Any

from chemworld.eval.formal_classic import (
    audit_classic_method_freeze,
    load_classic_method_freeze,
    make_frozen_classic_agent,
)
from chemworld.eval.formal_protocol_v0_4 import CORE_TASKS, load_formal_protocol
from chemworld.eval.formal_runner import canonical_sha256
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task
from chemworld.world.world_family import axes_for_task

ROOT = Path(__file__).resolve().parents[3]
CLASSIC_DEVELOPMENT_VERSION = "chemworld-classic-development-audit-0.4"
DEFAULT_REPORT_PATH = (
    ROOT / "workstreams" / "benchmark_v1" / "reports" / "classic-dev-v0.4.json"
)
FORMAL_CHECKPOINTS = (4, 8, 12, 20, 40)


def _default_cache_root() -> Path:
    raw = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=ROOT,
        text=True,
    ).strip()
    path = Path(raw)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    return path / "chemworld-private" / "classic-dev-v0.4"


DEFAULT_CACHE_ROOT = _default_cache_root()


@dataclass(frozen=True)
class DevelopmentCell:
    split: str
    task_id: str
    method_id: str
    world_seed: int
    method_seed: int
    complete_experiments: int
    risk_limit: float
    world_interventions: tuple[dict[str, Any], ...]
    formal_protocol_sha256: str
    method_artifact_sha256: str
    source_commit: str
    determinism_check: bool = False

    @property
    def cell_id(self) -> str:
        return canonical_sha256(
            {
                "schema_version": CLASSIC_DEVELOPMENT_VERSION,
                **asdict(self),
            }
        )


def _trajectory_digest(history: Sequence[Any]) -> str:
    payload = [
        {
            "step": record.step,
            "action": record.action,
            "observation": record.observation,
            "reward": record.reward,
            "event_type": record.event_type,
        }
        for record in history
    ]
    return canonical_sha256({"records": payload})


def _run_cell_once(cell: DevelopmentCell) -> tuple[dict[str, Any], str]:
    task = get_task(cell.task_id)
    agent = make_frozen_classic_agent(cell.method_id)
    event_count = _recipe_event_count(task.to_dict())
    history = run_agent(
        env_id=task.env_id,
        agent=agent,
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=cell.world_seed,
        agent_seed=cell.method_seed,
        task_id=task.task_id,
        budget_override=event_count * cell.complete_experiments,
        episode_mode_override="campaign",
        method_resource_limits={
            "operation_limit": event_count * cell.complete_experiments,
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
    values: list[float] = []
    for record in terminal:
        value = record.observation.get(primary_metric)
        if value is not None:
            values.append(float(value))
    best_curve: list[float] = []
    current = -math.inf
    for value in values:
        current = max(current, value)
        best_curve.append(current)
    traces_factory = getattr(agent, "agent_trace", None)
    traces = traces_factory() if callable(traces_factory) else []
    acquisition_traces = [item for item in traces if item.get("phase") == "acquisition"]
    safe_traces = [
        item
        for item in acquisition_traces
        if isinstance(item.get("decision_diagnostics"), Mapping)
        and "safe_candidate_count" in item["decision_diagnostics"]
    ]
    constraint_active = any(
        item.get("selected_policy") == "safe_gp_risk_fallback"
        or int(item["decision_diagnostics"]["safe_candidate_count"])
        < int(item["decision_diagnostics"]["candidate_count"])
        for item in safe_traces
    )
    compute_factory = getattr(agent, "formal_compute_events", None)
    compute_events = compute_factory() if callable(compute_factory) else []
    final_resources = history[-1].method_resources if history else {}
    invalid_count = sum(
        bool(record.info.get("constraint_flags", {}).get("precondition_failed", False))
        for record in history
    )
    result = {
        "schema_version": CLASSIC_DEVELOPMENT_VERSION,
        "cell_id": cell.cell_id,
        "split": cell.split,
        "task_id": cell.task_id,
        "method_id": cell.method_id,
        "world_seed": cell.world_seed,
        "method_seed_role": "paired_public_development_rng",
        "formal_protocol_sha256": cell.formal_protocol_sha256,
        "method_artifact_sha256": cell.method_artifact_sha256,
        "source_commit": cell.source_commit,
        "complete_experiment_count": len(terminal),
        "operation_count": len(history),
        "primary_metric": primary_metric,
        "primary_terminal_values": values,
        "best_curve": best_curve,
        "acquisition_decision_count": len(acquisition_traces),
        "fit_count": sum(item.get("event_kind") == "fit" for item in compute_events),
        "acquisition_optimization_count": sum(
            item.get("event_kind") == "acquisition_optimization" for item in compute_events
        ),
        "safe_constraint_diagnostic_count": len(safe_traces),
        "safe_constraint_activated": constraint_active,
        "invalid_operation_count": invalid_count,
        "cpu_time_s": float(
            final_resources.get("agent_usage", {}).get("cpu_time_s", 0.0)
        ),
        "run_wall_time_s": float(final_resources.get("run_wall_time_s", 0.0)),
        "accounting_complete": final_resources.get("accounting_complete") is True,
        "world_interventions": list(cell.world_interventions),
    }
    return result, _trajectory_digest(history)


def _run_development_cell(cell: DevelopmentCell, cache_root: str) -> dict[str, Any]:
    root = Path(cache_root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{cell.cell_id}.json"
    if path.is_file():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached.get("cell_id") == cell.cell_id:
            return cached
    result, first_digest = _run_cell_once(cell)
    if cell.determinism_check:
        _, second_digest = _run_cell_once(cell)
        result["determinism_checked"] = True
        result["deterministic_replay"] = first_digest == second_digest
        result["trajectory_digest"] = first_digest
    else:
        result["determinism_checked"] = False
        result["deterministic_replay"] = None
        result["trajectory_digest"] = None
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)
    return result


def _recipe_event_count(task_info: dict[str, Any]) -> int:
    from chemworld.agents.task_recipes import task_recipe_event_count

    return task_recipe_event_count(task_info)


def _paired_method_seed(split: str, world_seed: int) -> int:
    digest = hashlib.sha256(f"classic-v0.4:{split}:{world_seed}".encode()).digest()
    return 200_000 + int.from_bytes(digest[:4], "big") % 700_000_000


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


def build_development_cells(
    *,
    tasks: Sequence[str] = CORE_TASKS,
    methods: Sequence[str] | None = None,
    train_seeds: Sequence[int] = tuple(range(10_000, 10_004)),
    dev_seeds: Sequence[int] = tuple(range(11_000, 11_020)),
    complete_experiments: int = 40,
) -> list[DevelopmentCell]:
    protocol = load_formal_protocol()
    freeze = load_classic_method_freeze()
    protocol_sha256 = canonical_sha256(protocol)
    source_commit = _git_commit()
    selected_methods = tuple(sorted(freeze["methods"])) if methods is None else tuple(methods)
    allowed_tasks = set(protocol["task_roles"]["formal_core"])
    allowed_methods = set(freeze["methods"])
    if not set(tasks).issubset(allowed_tasks) or not set(selected_methods).issubset(
        allowed_methods
    ):
        raise ValueError("development cells must use frozen formal tasks and methods")
    if complete_experiments < 5 or complete_experiments > 40:
        raise ValueError("classic development requires 5..40 complete experiments")
    ranges = protocol["split_contract"]
    cells: list[DevelopmentCell] = []
    first_train = min(train_seeds) if train_seeds else None
    for split, seeds in (("train", train_seeds), ("dev", dev_seeds)):
        start = int(ranges[split]["base_seeds"]["start"])
        stop = int(ranges[split]["base_seeds"]["stop_inclusive"])
        if any(seed < start or seed > stop for seed in seeds):
            raise ValueError(f"{split} seed is outside the public formal range")
        for seed in seeds:
            for task_id in tasks:
                risk_limit = float(
                    protocol["task_roles"]["formal_core"][task_id]["risk_limit"]
                )
                interventions = _public_interventions(
                    protocol,
                    task_id=task_id,
                    split=split,
                    seed=seed,
                )
                for method_id in selected_methods:
                    cells.append(
                        DevelopmentCell(
                            split=split,
                            task_id=task_id,
                            method_id=method_id,
                            world_seed=seed,
                            method_seed=_paired_method_seed(split, seed),
                            complete_experiments=complete_experiments,
                            risk_limit=risk_limit,
                            world_interventions=interventions,
                            formal_protocol_sha256=protocol_sha256,
                            method_artifact_sha256=str(
                                freeze["methods"][method_id]["artifact_sha256"]
                            ),
                            source_commit=source_commit,
                            determinism_check=split == "train" and seed == first_train,
                        )
                    )
    return cells


def _method_summary(
    method_id: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    complete_experiments: int,
) -> dict[str, Any]:
    dev = [row for row in rows if row["split"] == "dev"]
    train = [row for row in rows if row["split"] == "train"]
    checkpoints = tuple(
        point for point in FORMAL_CHECKPOINTS if point <= complete_experiments
    )
    curve = {
        str(point): fmean(float(row["best_curve"][point - 1]) for row in dev)
        for point in checkpoints
    }
    deterministic = [row for row in train if row["determinism_checked"]]
    acquisition_required = method_id.startswith("structured_")
    acquisition_ok = all(int(row["acquisition_decision_count"]) > 0 for row in dev)
    compute_ok = all(
        int(row["fit_count"]) > 0 and int(row["acquisition_optimization_count"]) > 0
        for row in dev
    )
    safe_required = method_id == "structured_safe_gp_ei"
    safe_activation_rate = (
        fmean(bool(row["safe_constraint_activated"]) for row in dev)
        if safe_required
        else None
    )
    return {
        "method_id": method_id,
        "train_cell_count": len(train),
        "dev_cell_count": len(dev),
        "mean_dev_best_primary": fmean(float(row["best_curve"][-1]) for row in dev),
        "mean_dev_cpu_time_s": fmean(float(row["cpu_time_s"]) for row in dev),
        "mean_dev_wall_time_s": fmean(float(row["run_wall_time_s"]) for row in dev),
        "mean_budget_curve": curve,
        "budget_curve_non_degenerate": any(
            len({round(float(value), 12) for value in row["best_curve"]}) > 1
            for row in dev
        ),
        "determinism_check_count": len(deterministic),
        "deterministic_replay": bool(deterministic)
        and all(row["deterministic_replay"] is True for row in deterministic),
        "acquisition_required": acquisition_required,
        "acquisition_effective": (acquisition_ok and compute_ok)
        if acquisition_required
        else None,
        "safe_constraint_required": safe_required,
        "safe_constraint_activation_rate": safe_activation_rate,
        "safe_constraint_effective": (
            safe_activation_rate is not None and safe_activation_rate > 0.0
        )
        if safe_required
        else None,
        "invalid_operation_count": sum(int(row["invalid_operation_count"]) for row in rows),
        "accounting_complete": all(row["accounting_complete"] is True for row in rows),
        "all_cells_complete": all(
            int(row["complete_experiment_count"]) == complete_experiments for row in rows
        ),
    }


def _select_family_champions(
    summaries: Mapping[str, Mapping[str, Any]],
    freeze: Mapping[str, Any],
) -> dict[str, str]:
    families: dict[str, list[str]] = defaultdict(list)
    for method_id, card in freeze["methods"].items():
        if method_id in summaries:
            families[str(card["family"])].append(method_id)
    champions: dict[str, str] = {}
    for family, method_ids in sorted(families.items()):
        ranked = sorted(
            method_ids,
            key=lambda method_id: (
                -float(summaries[method_id]["mean_dev_best_primary"]),
                float(summaries[method_id]["mean_dev_cpu_time_s"]),
                method_id,
            ),
        )
        champions[family] = ranked[0]
    return champions


def run_classic_development_audit(
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
    """Run only public Train/Dev cells and freeze family champions without Bench access."""

    freeze = load_classic_method_freeze()
    freeze_audit = audit_classic_method_freeze(freeze)
    if freeze_audit["controls_ready"] is not True:
        raise RuntimeError("classic freeze must pass before development execution")
    cells = build_development_cells(
        tasks=tasks,
        methods=methods,
        train_seeds=train_seeds,
        dev_seeds=dev_seeds,
        complete_experiments=complete_experiments,
    )
    worker_count = workers or max(1, min(12, (os.cpu_count() or 2) - 1))
    rows: list[dict[str, Any]] = []
    if worker_count == 1:
        rows = [_run_development_cell(cell, str(cache_root)) for cell in cells]
    else:
        with ProcessPoolExecutor(max_workers=worker_count) as executor:
            futures = {
                executor.submit(_run_development_cell, cell, str(cache_root)): cell
                for cell in cells
            }
            for future in as_completed(futures):
                rows.append(future.result())
    rows.sort(key=lambda row: (row["split"], row["world_seed"], row["task_id"], row["method_id"]))
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
    champions = _select_family_champions(summaries, freeze)
    full_scope = (
        tuple(tasks) == CORE_TASKS
        and set(summaries) == set(freeze["methods"])
        and tuple(train_seeds) == tuple(range(10_000, 10_004))
        and tuple(dev_seeds) == tuple(range(11_000, 11_020))
        and complete_experiments == 40
    )
    method_controls_pass = all(
        summary["all_cells_complete"]
        and summary["accounting_complete"]
        and summary["deterministic_replay"]
        and summary["budget_curve_non_degenerate"]
        and int(summary["invalid_operation_count"]) == 0
        and (summary["acquisition_effective"] is not False)
        and (summary["safe_constraint_effective"] is not False)
        for summary in summaries.values()
    )
    protocol = load_formal_protocol()
    report = {
        "schema_version": CLASSIC_DEVELOPMENT_VERSION,
        "status": (
            "formal_classic_matrix_ready"
            if full_scope and method_controls_pass
            else "development_diagnostic_only"
        ),
        "formal_classic_matrix_ready": full_scope and method_controls_pass,
        "bench_results_present": False,
        "reference_search_results_used": False,
        "split_scope": ["train", "dev"],
        "source_commit": _git_commit(),
        "formal_protocol_sha256": canonical_sha256(protocol),
        "classic_freeze_sha256": canonical_sha256(freeze),
        "tasks": list(tasks),
        "methods": sorted(summaries),
        "train_seeds": list(train_seeds),
        "dev_seeds": list(dev_seeds),
        "complete_experiments_per_cell": complete_experiments,
        "cell_count": len(rows),
        "worker_count": worker_count,
        "cache_root_role": "git_private_resumable_development_cache",
        "method_summaries": summaries,
        "family_champions": champions,
        "selection_rule": freeze["selection_rule"],
        "acceptance": {
            "full_preregistered_development_scope": full_scope,
            "all_method_controls_pass": method_controls_pass,
            "all_cells_complete": all(
                int(row["complete_experiment_count"]) == complete_experiments for row in rows
            ),
            "all_accounting_complete": all(row["accounting_complete"] is True for row in rows),
            "all_checked_replays_deterministic": all(
                row["deterministic_replay"] is True
                for row in rows
                if row["determinism_checked"]
            ),
            "bench_feedback_used": False,
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
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


__all__ = [
    "CLASSIC_DEVELOPMENT_VERSION",
    "DEFAULT_CACHE_ROOT",
    "DEFAULT_REPORT_PATH",
    "DevelopmentCell",
    "build_development_cells",
    "run_classic_development_audit",
]
