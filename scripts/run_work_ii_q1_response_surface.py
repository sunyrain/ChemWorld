#!/usr/bin/env python3
"""Run the provider-free five-world Work II Q1 response-surface qualification."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np

from chemworld.agents.static_optimization import (
    StaticOptimizationValidator,
    compile_static_optimization_plan,
)
from chemworld.agents.task_recipes import (
    electrochemical_recipe_parameters_from_unit_vector,
    task_recipe_coordinate_schema,
)
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_c2_admission import (
    build_c2_source_binding,
    c2_material_dirty_paths,
)
from chemworld.eval.work_ii_response_surface_qualification import (
    ADAPTIVE_RECIPE_COUNT,
    BROAD_RECIPE_COUNT,
    TOTAL_RECIPE_COUNT,
    WORK_II_Q1_RESPONSE_SURFACE_VERSION,
    analyze_q1_world,
    broad_sobol_design,
    build_adaptive_design,
    select_adaptive_anchors,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-q1-five-world-summary-0.3"
WORLD_REPORT_VERSION = "chemworld-work-ii-q1-world-report-0.3"
SCOPED_RUNTIME_PREFIXES = (
    "src/",
    "scripts/",
    "configs/benchmark/",
    "workstreams/flagship_tasks/",
)
TASK_SPECS: dict[str, dict[str, Any]] = {
    "reaction-safety-constrained": {
        "config": "configs/benchmark/work_ii_reaction_safety_parametric_initial_model_pilot.json",
        "target_indices": (0, 1),
        "target_control_ids": ("reaction_temperature_K", "reaction_duration_s"),
        "primary_metric": "yield",
        "metrics": ("yield", "selectivity", "safety_risk", "score"),
        "require_safety_frontier": True,
        "target_operation_check": "heat",
        "expected_target_bounds": ((250.0, 470.0), (1.0, 14_400.0)),
        "required_coverage_control_ids": (
            "reaction_temperature_K",
            "reaction_duration_s",
            "reagent_amount_mol",
            "stirring_speed_rpm",
            "catalyst",
            "catalyst_amount_mol",
            "solvent",
            "solvent_volume_L",
        ),
    },
    "electrochemical-conversion": {
        "config": "configs/benchmark/work_ii_electrochemical_parametric_initial_model_pilot.json",
        "target_indices": (6, 7),
        "target_control_ids": (
            "controlled_potential_delta_V",
            "controlled_current_delta_mA",
        ),
        "primary_metric": "selective_product_yield",
        "metrics": (
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score",
        ),
        "require_safety_frontier": False,
        "target_operation_check": "set_potential",
    },
}

REACTION_SAFETY_Q1_SCHEMA: tuple[dict[str, Any], ...] = (
    {
        "coordinate": 0,
        "control_id": "reaction_temperature_K",
        "kind": "linear",
        "physical_bounds": [250.0, 470.0],
        "unit": "K",
    },
    {
        "coordinate": 1,
        "control_id": "reaction_duration_s",
        "kind": "linear",
        "physical_bounds": [1.0, 14_400.0],
        "unit": "s",
    },
    {
        "coordinate": 2,
        "control_id": "reagent_amount_mol",
        "kind": "linear",
        "physical_bounds": [0.003, 0.030],
        "unit": "mol",
    },
    {
        "coordinate": 3,
        "control_id": "stirring_speed_rpm",
        "kind": "linear",
        "physical_bounds": [100.0, 1200.0],
        "unit": "rpm",
    },
    {
        "coordinate": 4,
        "control_id": "catalyst",
        "kind": "categorical",
        "category_count": 4,
        "numeric_distance_has_scientific_meaning": False,
        "numeric_order_has_scientific_meaning": False,
        "selection_semantics": "independent_unordered_nominal_choice",
    },
    {
        "coordinate": 5,
        "control_id": "catalyst_amount_mol",
        "kind": "linear",
        "physical_bounds": [0.00008, 0.00055],
        "unit": "mol",
    },
    {
        "coordinate": 6,
        "control_id": "solvent",
        "kind": "categorical",
        "category_count": 4,
        "numeric_distance_has_scientific_meaning": False,
        "numeric_order_has_scientific_meaning": False,
        "selection_semantics": "independent_unordered_nominal_choice",
    },
    {
        "coordinate": 7,
        "control_id": "solvent_volume_L",
        "kind": "linear",
        "physical_bounds": [0.005, 0.050],
        "unit": "L",
    },
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _scoped_dirty_paths() -> list[str]:
    return c2_material_dirty_paths(ROOT)


def _emit(path: Path, payload: Mapping[str, Any]) -> None:
    rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(rendered + "\n")
    print(rendered, flush=True)


def _observation_binding(task_id: str, world_seed: int, recipe_id: str) -> dict[str, Any]:
    digest = hashlib.sha256(
        f"work-ii-q1:{task_id}:{world_seed}:{recipe_id}".encode()
    ).hexdigest()
    return {
        "observation_seed": int(digest[:8], 16) % 2_147_483_647,
        "observation_noise_namespace": (
            f"work-ii-q1-{task_id}-w{world_seed}-{recipe_id}-{digest[:10]}"
        ),
        "observation_coordinate_sha256": digest,
    }


def _q1_coordinate_schema(task_id: str) -> list[dict[str, Any]]:
    if task_id == "reaction-safety-constrained":
        return [dict(item) for item in REACTION_SAFETY_Q1_SCHEMA]
    return [dict(item) for item in task_recipe_coordinate_schema(get_task(task_id).to_dict())]


def _scale_unit(value: float, low: float, high: float) -> float:
    return low + float(value) * (high - low)


def _nominal_choice(value: float, count: int) -> int:
    return min(int(float(value) * count), count - 1)


def _compile_reaction_safety_q1_actions(
    vector: Sequence[float],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if len(vector) != len(REACTION_SAFETY_Q1_SCHEMA):
        raise ValueError("reaction-safety Q1 vector has the wrong dimension")
    values = [float(value) for value in vector]
    if any(not 0.0 <= value <= 1.0 for value in values):
        raise ValueError("reaction-safety Q1 vector must stay in [0,1]")
    physical = {
        "reaction_temperature_K": _scale_unit(values[0], 250.0, 470.0),
        "reaction_duration_s": _scale_unit(values[1], 1.0, 14_400.0),
        "reagent_amount_mol": _scale_unit(values[2], 0.003, 0.030),
        "stirring_speed_rpm": _scale_unit(values[3], 100.0, 1200.0),
        "catalyst": _nominal_choice(values[4], 4),
        "catalyst_amount_mol": _scale_unit(values[5], 0.00008, 0.00055),
        "solvent": _nominal_choice(values[6], 4),
        "solvent_volume_L": _scale_unit(values[7], 0.005, 0.050),
    }
    actions = [
        {
            "operation": "add_solvent",
            "volume_L": physical["solvent_volume_L"],
            "solvent": physical["solvent"],
        },
        {"operation": "add_reagent", "amount_mol": physical["reagent_amount_mol"]},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": physical["catalyst_amount_mol"],
            "catalyst": physical["catalyst"],
        },
        {
            "operation": "heat",
            "target_temperature_K": physical["reaction_temperature_K"],
            "duration_s": physical["reaction_duration_s"],
            "stirring_speed_rpm": physical["stirring_speed_rpm"],
        },
        {"operation": "quench"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]
    metadata = {
        "recipe_contract": "work-ii-reaction-safety-q1-executable-control-envelope-0.2",
        "search_vector": values,
        "physical_controls": physical,
        "coordinate_schema": _q1_coordinate_schema("reaction-safety-constrained"),
    }
    return actions, metadata


def _compile_actions(
    task_id: str,
    config: Mapping[str, Any],
    vector: Sequence[float],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if task_id == "reaction-safety-constrained":
        return _compile_reaction_safety_q1_actions(vector)
    task_info = get_task(task_id).to_dict()
    workflow_mode = str(config.get("electrochemical_workflow_mode", "static_single_stage"))
    validator = StaticOptimizationValidator(
        task_info,
        electrochemical_workflow_mode=workflow_mode,
    )
    payload: dict[str, Any] = {
        "experiment_intent": "provider-free Work II Q1 response-surface qualification",
        "requested_measurement_slots": list(validator.required_measurement_slot_ids),
        "measurement_objective": "measure the frozen Q1 response-surface metrics",
        "expected_effect": "resolve reachability, curvature, interaction and safety structure",
        "uncertainty": 0.0,
    }
    if task_id == "electrochemical-conversion":
        payload["recipe_parameters"] = electrochemical_recipe_parameters_from_unit_vector(
            np.asarray(vector, dtype=float)
        )
    else:
        payload["search_vector"] = [float(value) for value in vector]
    plan = validator.validate(payload)
    recipe = compile_static_optimization_plan(
        task_info,
        plan,
        electrochemical_workflow_mode=workflow_mode,
    )
    return [dict(action) for action in recipe["steps"]], dict(recipe["metadata"])


def _q0_audit(task_id: str, config: Mapping[str, Any], spec: Mapping[str, Any]) -> dict[str, Any]:
    task = get_task(task_id)
    schema = _q1_coordinate_schema(task_id)
    controls = {str(item["control_id"]): int(item["coordinate"]) for item in schema}
    target_control_ids = tuple(str(item) for item in spec["target_control_ids"])
    midpoint = [0.5] * len(schema)
    actions, metadata = _compile_actions(task_id, config, midpoint)
    operations = [str(action.get("operation")) for action in actions]
    expected_operation = str(spec["target_operation_check"])
    required_coverage_control_ids = tuple(
        str(item) for item in spec.get("required_coverage_control_ids", target_control_ids)
    )
    expected_target_bounds = tuple(spec.get("expected_target_bounds", ()))
    observed_target_bounds = tuple(
        tuple(float(value) for value in schema[controls[control]]["physical_bounds"])
        for control in target_control_ids
        if control in controls and "physical_bounds" in schema[controls[control]]
    )
    checks = {
        "target_controls_present": all(control in controls for control in target_control_ids),
        "coverage_controls_present": all(
            control in controls for control in required_coverage_control_ids
        ),
        "target_indices_match_schema": tuple(
            controls.get(control) for control in target_control_ids
        )
        == tuple(spec["target_indices"]),
        "target_physical_bounds_match": not expected_target_bounds
        or observed_target_bounds == expected_target_bounds,
        "midpoint_compiles": bool(actions),
        "target_operation_reachable": expected_operation in operations,
        "terminal_final_assay_present": bool(actions)
        and actions[-1].get("operation") == "measure"
        and actions[-1].get("instrument") == "final_assay",
        "finite_task_threshold": bool(np.isfinite(float(task.threshold))),
        "finite_safety_limit": bool(np.isfinite(float(task.safety_limit))),
    }
    return {
        "task_id": task_id,
        "world_seeds": list(task.seeds),
        "task_contract_hash": task.contract_hash,
        "task_threshold": float(task.threshold),
        "safety_limit": float(task.safety_limit),
        "schema": schema,
        "target_control_ids": list(target_control_ids),
        "target_indices": list(spec["target_indices"]),
        "required_coverage_control_ids": list(required_coverage_control_ids),
        "observed_target_bounds": [list(bounds) for bounds in observed_target_bounds],
        "expected_target_bounds": [list(bounds) for bounds in expected_target_bounds],
        "midpoint_action_count": len(actions),
        "midpoint_operations": operations,
        "midpoint_recipe_metadata_sha256": canonical_json_sha256(metadata),
        "checks": checks,
        "passed": all(checks.values()),
    }


def _scalar(value: object, field: str) -> float:
    if value is None:
        raise ValueError(f"final assay lacks {field}")
    array = np.asarray(value)
    if array.size != 1:
        raise ValueError(f"final assay {field} is not scalar")
    number = float(array.reshape(-1)[0])
    if not np.isfinite(number):
        raise ValueError(f"final assay {field} is not finite")
    return number


def _final_metrics(
    records: Sequence[Mapping[str, Any]], metrics: Sequence[str]
) -> dict[str, float]:
    final_rows = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(final_rows) != 1:
        raise ValueError("Q1 recipe must contain exactly one committed final assay")
    row = final_rows[0]
    observation = row.get("observation")
    if not isinstance(observation, Mapping):
        raise ValueError("Q1 final assay lacks an observation object")
    output: dict[str, float] = {}
    for metric in metrics:
        value = row.get("leaderboard_score") if metric == "score" else observation.get(metric)
        output[metric] = _scalar(value, metric)
    return output


def _execute_recipe(
    *,
    task_id: str,
    config: Mapping[str, Any],
    spec: Mapping[str, Any],
    world_seed: int,
    recipe_id: str,
    vector: Sequence[float],
    phase: str,
    output_root: Path,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    recipe_root = output_root / recipe_id
    recipe_root.mkdir(parents=True, exist_ok=False)
    trajectory_path = recipe_root / "trajectory.jsonl"
    binding = _observation_binding(task_id, world_seed, recipe_id)
    started = perf_counter()
    failure: dict[str, str] | None = None
    metrics: dict[str, float] | None = None
    replay: dict[str, Any] | None = None
    action_count: int | None = None
    metadata_sha256: str | None = None
    try:
        actions, metadata = _compile_actions(task_id, config, vector)
        action_count = len(actions)
        metadata_sha256 = canonical_json_sha256(metadata)
        run_agent(
            env_id=get_task(task_id).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(config["world_split"]),
            budget=len(actions),
            objective=str(config["objective"]),
            seed=world_seed,
            agent_seed=0,
            observation_seed=int(binding["observation_seed"]),
            task_id=task_id,
            output_path=trajectory_path,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            electrochemical_material_family_id=config.get(
                "electrochemical_material_family_id"
            ),
            crystallization_material_family_id=config.get(
                "crystallization_material_family_id"
            ),
            electrochemical_workflow_mode=config.get("electrochemical_workflow_mode"),
            scoring_contract_id=config.get("scoring_contract_id"),
            observation_noise_mode=str(config["observation_noise_mode"]),
            observation_noise_namespace=str(binding["observation_noise_namespace"]),
        )
        records = load_jsonl(trajectory_path)
        if [record.get("action") for record in records] != actions:
            raise ValueError("Q1 trajectory differs from its frozen action plan")
        noncommitted = [
            record
            for record in records
            if record.get("transaction_status") != "committed"
        ]
        if noncommitted:
            first = noncommitted[0]
            raise ValueError(
                "Q1 recipe contains a noncommitted operation: "
                f"operation={first.get('operation_type')}, "
                f"status={first.get('transaction_status')}, "
                f"error={first.get('error_message')}"
            )
        metrics = _final_metrics(records, spec["metrics"])
        replay = verify_records(records, tolerance=0.0).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("Q1 trajectory failed exact replay")
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)[:1000]}
    row: dict[str, Any] = {
        "recipe_id": recipe_id,
        "phase": phase,
        "world_seed": world_seed,
        "vector": [float(value) for value in vector],
        "status": "completed" if failure is None else "failed",
        "score": metrics.get("score") if metrics is not None else None,
        "safety_risk": metrics.get("safety_risk") if metrics is not None else None,
        "metrics": metrics,
        "action_count": action_count,
        "recipe_metadata_sha256": metadata_sha256,
        "observation_coordinate_sha256": binding["observation_coordinate_sha256"],
        "trajectory": (
            {
                "path": trajectory_path.relative_to(output_root).as_posix(),
                "sha256": file_sha256(trajectory_path),
            }
            if trajectory_path.is_file()
            else None
        ),
        "exact_replay": replay,
        "failure": failure,
        "elapsed_s": round(perf_counter() - started, 6),
    }
    if extra:
        row.update(dict(extra))
    write_json_atomic(recipe_root / "receipt.json", row)
    return row


def _progress_event(
    *,
    task_id: str,
    world_seed: int,
    stage: str,
    completed: int,
    total: int,
    started: float,
    failures: int,
) -> dict[str, Any]:
    elapsed = perf_counter() - started
    rate = completed / elapsed if elapsed > 0.0 else 0.0
    return {
        "event": "q1_progress",
        "task_id": task_id,
        "world_seed": world_seed,
        "stage": stage,
        "completed": completed,
        "total": total,
        "throughput_recipes_per_minute": round(rate * 60.0, 2),
        "eta_s": round((total - completed) / rate, 1) if rate > 0.0 else None,
        "failure_count": failures,
        "elapsed_s": round(elapsed, 1),
    }


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
    broad_vectors = broad_sobol_design(task_id, world_seed, len(schema))
    broad_rows: list[dict[str, Any]] = []
    adaptive_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    started = perf_counter()
    last_progress = started
    for index, vector in enumerate(broad_vectors, start=1):
        row = _execute_recipe(
            task_id=task_id,
            config=config,
            spec=spec,
            world_seed=world_seed,
            recipe_id=f"b{index:04d}",
            vector=vector,
            phase="broad",
            output_root=world_root,
        )
        broad_rows.append(row)
        if row["failure"] is not None:
            failures.append(
                {"recipe_id": row["recipe_id"], "phase": "broad", **row["failure"]}
            )
        now = perf_counter()
        if index % 16 == 0 or now - last_progress >= 30.0 or index == BROAD_RECIPE_COUNT:
            _emit(
                progress_path,
                _progress_event(
                    task_id=task_id,
                    world_seed=world_seed,
                    stage="broad",
                    completed=index,
                    total=TOTAL_RECIPE_COUNT,
                    started=started,
                    failures=len(failures),
                ),
            )
            last_progress = now

    anchors: list[dict[str, Any]] = []
    adaptive_design: list[dict[str, Any]] = []
    try:
        anchors = select_adaptive_anchors(
            broad_rows,
            schema=schema,
            target_indices=tuple(spec["target_indices"]),
            task_threshold=float(get_task(task_id).threshold),
            safety_limit=float(get_task(task_id).safety_limit),
        )
        adaptive_design = build_adaptive_design(
            anchors,
            target_indices=tuple(spec["target_indices"]),
        )
    except Exception as error:
        failures.append(
            {
                "recipe_id": None,
                "phase": "adaptive_design",
                "type": type(error).__name__,
                "message": str(error)[:1000],
            }
        )
        adaptive_design = [
            {
                "phase": "adaptive_unavailable",
                "vector": [0.5] * len(schema),
                "failure": {
                    "type": type(error).__name__,
                    "message": str(error)[:1000],
                },
            }
            for _ in range(ADAPTIVE_RECIPE_COUNT)
        ]

    for index, design in enumerate(adaptive_design, start=1):
        recipe_id = f"a{index:04d}"
        if design["phase"] == "adaptive_unavailable":
            row = {
                "recipe_id": recipe_id,
                "phase": "adaptive_unavailable",
                "world_seed": world_seed,
                "vector": list(design["vector"]),
                "status": "failed",
                "score": None,
                "safety_risk": None,
                "metrics": None,
                "action_count": None,
                "recipe_metadata_sha256": None,
                "observation_coordinate_sha256": None,
                "trajectory": None,
                "exact_replay": None,
                "failure": dict(design["failure"]),
                "elapsed_s": 0.0,
            }
        else:
            extra = {
                key: value
                for key, value in design.items()
                if key not in {"phase", "vector"}
            }
            row = _execute_recipe(
                task_id=task_id,
                config=config,
                spec=spec,
                world_seed=world_seed,
                recipe_id=recipe_id,
                vector=design["vector"],
                phase=str(design["phase"]),
                output_root=world_root,
                extra=extra,
            )
        adaptive_rows.append(row)
        if row["failure"] is not None:
            failures.append(
                {
                    "recipe_id": recipe_id,
                    "phase": row["phase"],
                    **row["failure"],
                }
            )
        completed = BROAD_RECIPE_COUNT + index
        now = perf_counter()
        if index % 16 == 0 or now - last_progress >= 30.0 or index == ADAPTIVE_RECIPE_COUNT:
            _emit(
                progress_path,
                _progress_event(
                    task_id=task_id,
                    world_seed=world_seed,
                    stage="adaptive",
                    completed=completed,
                    total=TOTAL_RECIPE_COUNT,
                    started=started,
                    failures=len(failures),
                ),
            )
            last_progress = now

    q1 = analyze_q1_world(
        broad_rows,
        adaptive_rows,
        target_indices=tuple(spec["target_indices"]),
        task_threshold=float(get_task(task_id).threshold),
        safety_limit=float(get_task(task_id).safety_limit),
        primary_metric=str(spec["primary_metric"]),
        require_safety_frontier=bool(spec["require_safety_frontier"]),
    )
    report: dict[str, Any] = {
        "schema_version": WORLD_REPORT_VERSION,
        "qualification_schema_version": WORK_II_Q1_RESPONSE_SURFACE_VERSION,
        "formal_result": False,
        "task_id": task_id,
        "world_seed": world_seed,
        "coverage": {
            "broad_recipe_count": BROAD_RECIPE_COUNT,
            "adaptive_recipe_count": ADAPTIVE_RECIPE_COUNT,
            "total_recipe_count": TOTAL_RECIPE_COUNT,
            "target_indices": list(spec["target_indices"]),
            "target_control_ids": list(spec["target_control_ids"]),
        },
        "adaptive_anchors": anchors,
        "q1": q1,
        "failure_count": len(failures),
        "failures": failures,
        "rows": [*broad_rows, *adaptive_rows],
        "elapsed_s": round(perf_counter() - started, 3),
    }
    report["report_sha256"] = canonical_json_sha256(report)
    write_json_atomic(world_root / "world-report.json", report)
    return report


def run(args: argparse.Namespace) -> dict[str, Any]:
    task_id = str(args.task_id)
    spec = TASK_SPECS[task_id]
    scoped_dirty = _scoped_dirty_paths()
    if scoped_dirty:
        raise RuntimeError(
            "Q1 qualification requires clean Work II/runtime sources: "
            + ", ".join(scoped_dirty)
        )
    output_root = args.output_root.resolve()
    summary_path = args.summary.resolve()
    progress_path = args.progress_file.resolve()
    if output_root.exists() or summary_path.exists():
        raise FileExistsError("refusing to overwrite an existing Q1 output")
    config_path = (ROOT / str(spec["config"])).resolve()
    config = _load(config_path)
    if config.get("task_id") != task_id:
        raise ValueError("Q1 config task differs from the selected task")
    q0 = _q0_audit(task_id, config, spec)
    _emit(
        progress_path,
        {
            "event": "q0_completed",
            "task_id": task_id,
            "passed": q0["passed"],
            "checks": q0["checks"],
        },
    )
    if not q0["passed"]:
        raise RuntimeError("Q0 mechanism/reachability audit failed")
    output_root.mkdir(parents=True)
    started = perf_counter()
    world_reports: list[dict[str, Any]] = []
    for index, world_seed in enumerate(get_task(task_id).seeds, start=1):
        _emit(
            progress_path,
            {
                "event": "world_started",
                "task_id": task_id,
                "world_seed": world_seed,
                "world_index": index,
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
                "event": "world_completed",
                "task_id": task_id,
                "world_seed": world_seed,
                "world_index": index,
                "world_total": 5,
                "passed": report["q1"]["passed"],
                "completed": report["q1"]["completed_recipe_count"],
                "exact_replay": report["q1"]["exact_replay_count"],
                "failures": report["failure_count"],
                "elapsed_s": report["elapsed_s"],
            },
        )
    raw_bindings = []
    for report in world_reports:
        path = output_root / f"world-{report['world_seed']}" / "world-report.json"
        raw_bindings.append(
            {
                "world_seed": report["world_seed"],
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(path),
                "passed": report["q1"]["passed"],
            }
        )
    failures = [
        {"world_seed": report["world_seed"], **failure}
        for report in world_reports
        for failure in report["failures"]
    ]
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": WORK_II_Q1_RESPONSE_SURFACE_VERSION,
        "formal_result": False,
        "source_commit": git_source_commit(ROOT),
        "c2_source_binding": build_c2_source_binding(ROOT),
        "scoped_runtime_clean": True,
        "dynamic_evidence_excluded_from_material_cleanliness": True,
        "task_id": task_id,
        "world_seeds": list(get_task(task_id).seeds),
        "q0": q0,
        "coverage": {
            "world_count": 5,
            "broad_recipes_per_world": BROAD_RECIPE_COUNT,
            "adaptive_recipes_per_world": ADAPTIVE_RECIPE_COUNT,
            "recipes_per_world": TOTAL_RECIPE_COUNT,
            "planned_recipe_count": 5 * TOTAL_RECIPE_COUNT,
        },
        "denominators": {
            "planned_recipe_count": 5 * TOTAL_RECIPE_COUNT,
            "completed_recipe_count": sum(
                int(report["q1"]["completed_recipe_count"]) for report in world_reports
            ),
            "exact_replay_count": sum(
                int(report["q1"]["exact_replay_count"]) for report in world_reports
            ),
            "failed_recipe_count": sum(
                int(report["q1"]["failed_recipe_count"]) for report in world_reports
            ),
            "passed_world_count": sum(report["q1"]["passed"] for report in world_reports),
            "world_count": 5,
            "provider_call_count": 0,
        },
        "worlds": [
            {
                "world_seed": report["world_seed"],
                "passed": report["q1"]["passed"],
                "q1": report["q1"],
                "failure_count": report["failure_count"],
                "elapsed_s": report["elapsed_s"],
            }
            for report in world_reports
        ],
        "raw_bindings": raw_bindings,
        "failure_count": len(failures),
        "failures": failures,
        "q1_passed": all(report["q1"]["passed"] for report in world_reports),
        "q2_authorized": all(report["q1"]["passed"] for report in world_reports),
        "decision": (
            "proceed_to_q2_matched_prior_construction"
            if all(report["q1"]["passed"] for report in world_reports)
            else "reject_candidate_cohort_before_q2"
        ),
        "elapsed_s": round(perf_counter() - started, 3),
        "interpretation": (
            "Provider-free environment qualification only. A failed Q1 world is an "
            "intervention-design result, not an agent-capability result."
        ),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(summary_path, summary)
    _emit(
        progress_path,
        {
            "event": "q1_task_completed",
            "task_id": task_id,
            "passed_worlds": summary["denominators"]["passed_world_count"],
            "worlds": 5,
            "completed": summary["denominators"]["completed_recipe_count"],
            "total": summary["denominators"]["planned_recipe_count"],
            "exact_replay": summary["denominators"]["exact_replay_count"],
            "failures": summary["failure_count"],
            "decision": summary["decision"],
            "elapsed_s": summary["elapsed_s"],
            "summary": str(summary_path),
        },
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", choices=sorted(TASK_SPECS), required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args)
    return 0 if summary["q1_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
