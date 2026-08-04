"""Deterministic first-paper composition qualification runner."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any, cast

import gymnasium as gym

import chemworld
from chemworld.agent_interface import agent_view_bundle
from chemworld.data.logging import TrajectoryLogger, load_jsonl, observation_to_json
from chemworld.eval.composition_qualification_design import (
    EXPECTED_GENERATED_CASE_COUNT,
    EXPECTED_PATTERN_CASE_COUNTS,
    QUALIFICATION_DESIGN_VERSION,
    UNSEEN_PATTERN_ID,
    build_generated_suites,
)
from chemworld.eval.cross_world_infrastructure_qualification import (
    recipe_cases,
    run_task_world_unit,
)
from chemworld.eval.verify import verify_records
from chemworld.foundation.public_leakage import audit_public_payload
from chemworld.tasks import list_tasks
from chemworld.world.composition import WorldCompositionError

REPORT_SCHEMA_VERSION = "chemworld-first-paper-composition-qualification-report-0.1"
QUALIFICATION_ID = "first-paper-composition-qualification-v1"
EXPECTED_REFERENCE_UNIT_COUNT = 64
EXPECTED_REFERENCE_RECIPE_COUNT = 1786
EXPECTED_NEGATIVE_PROBE_COUNT = 192
EXPECTED_COMPILE_MUTANT_COUNT = 7
EXPECTED_MODULE_PROBE_COUNT = 32
EXPECTED_INTERFACE_PATH_COUNT = 7

EXPERIMENT_NOTE = Path(
    "workstreams/arxiv_v1/experiments/first-paper-composition-qualification.md"
)

_REFERENCE_RESOURCE_CARD = {
    "operation_attempt_limit": 8,
    "vessel_start_limit": 2,
    "final_assay_limit": 2,
    "nonfinal_instrument_use_limit": 2,
    "stock_limits": {"reagent_mol": 0.08, "solvent_L": 0.026},
    "per_instrument_limits": {},
}

_OPERATION_COMPONENTS = {
    "add_solvent": "reaction",
    "add_reagent": "reaction",
    "add_catalyst": "reaction",
    "quench": "reaction",
    "heat": "thermal",
    "wait": "thermal",
    "add_phase": "phase",
    "add_extractant": "separation",
    "mix": "separation",
    "settle": "separation",
    "separate_phase": "separation",
    "wash": "separation",
    "dry": "separation",
    "concentrate": "separation",
    "transfer": "separation",
    "seed_crystals": "crystallization",
    "cool_crystallize": "crystallization",
    "filter_crystals": "crystallization",
    "evaporate": "distillation",
    "distill": "distillation",
    "collect_fraction": "distillation",
    "set_flow_rate": "continuous_flow",
    "run_flow": "continuous_flow",
    "set_potential": "electrochemistry",
    "electrolyze": "electrochemistry",
    "measure": "observation",
}

_MODULE_CONFIGS = {
    "reaction": {
        "pattern": "reaction-thermal-observation",
        "operation": "add_reagent",
        "field": "amount_mol",
        "low": 0.003,
        "high": 0.030,
        "metric": "total_species_mol",
    },
    "thermal": {
        "pattern": "reaction-thermal-observation",
        "operation": "heat",
        "field": "target_temperature_K",
        "low": 350.0,
        "high": 390.0,
        "metric": "temperature_K",
    },
    "phase": {
        "pattern": "phase-separation-observation",
        "operation": "add_phase",
        "field": "volume_L",
        "low": 0.010,
        "high": 0.020,
        "metric": "volume_L",
    },
    "separation": {
        "pattern": "phase-separation-observation",
        "operation": "mix",
        "field": "duration_s",
        "low": 60.0,
        "high": 300.0,
        "metric": "time_s",
    },
    "crystallization": {
        "pattern": "reaction-crystallization-observation",
        "operation": "seed_crystals",
        "field": "seed_mass_g",
        "low": 0.002,
        "high": 0.010,
        "metric": "cost",
    },
    "distillation": {
        "pattern": "reaction-distillation-observation",
        "operation": "distill",
        "field": "duration_s",
        "low": 900.0,
        "high": 2400.0,
        "metric": "time_s",
    },
    "continuous_flow": {
        "pattern": "reaction-continuous-flow-observation",
        "operation": "run_flow",
        "field": "duration_s",
        "low": 1200.0,
        "high": 3600.0,
        "metric": "time_s",
    },
    "electrochemistry": {
        "pattern": "reaction-electrochemistry-observation",
        "operation": "electrolyze",
        "field": "duration_s",
        "low": 300.0,
        "high": 1800.0,
        "metric": "time_s",
    },
}

_INTERFACE_PATHS = {
    "reaction--thermal": "reaction-thermal-observation",
    "reaction--phase--separation": "reaction-phase-separation-observation",
    "phase--separation": "phase-separation-observation",
    "reaction--crystallization": "reaction-crystallization-observation",
    "reaction--distillation": "reaction-distillation-observation",
    "reaction--continuous-flow": "reaction-continuous-flow-observation",
    "reaction--electrochemistry": "reaction-electrochemistry-observation",
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256_value(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _reference_protocol() -> dict[str, Any]:
    return {
        "protocol_id": QUALIFICATION_ID,
        "intervention": {
            "negative_probes_per_unit": {
                "resource_exhaustion": {"resource_card": _REFERENCE_RESOURCE_CARD}
            }
        },
    }


def _leakage_findings(env: Any, payload: Any, surface: str) -> list[dict[str, Any]]:
    hidden_species = set(env.unwrapped._state.species_amounts)
    return [
        {"surface": surface, **finding.to_dict()}
        for finding in audit_public_payload(payload, hidden_species_ids=hidden_species)
    ]


def _physical_snapshot(env: Any) -> dict[str, Any]:
    state = env.unwrapped._state.to_dict(include_hidden=True)
    state.pop("ledger", None)
    state.pop("process", None)
    return state


def validate_launch_preconditions(
    repository_root: str | Path,
    *,
    require_clean: bool,
) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    errors: list[str] = []
    current_path = root / "configs/current.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    task_design = current.get("task_design", {})
    matrix_path = root / str(task_design.get("matrix", ""))
    if task_design.get("status") != "all_registered_task_designs_executable_and_metric_bound":
        errors.append("current task_design status is not executable and metric-bound")
    if not matrix_path.is_file():
        errors.append("current task_design matrix is missing")
        matrix: dict[str, Any] = {}
    else:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    tasks = list_tasks()
    reference_units = sum(len(task.seeds) for task in tasks)
    reference_recipes = sum(len(task.seeds) * len(recipe_cases(task)) for task in tasks)
    if len(tasks) != 15 or matrix.get("task_count") != 15:
        errors.append("registered task denominator drifted")
    if reference_units != EXPECTED_REFERENCE_UNIT_COUNT:
        errors.append(f"reference unit denominator drifted: {reference_units}")
    if reference_recipes != EXPECTED_REFERENCE_RECIPE_COUNT:
        errors.append(f"reference recipe denominator drifted: {reference_recipes}")
    suites = build_generated_suites()
    generated_count = sum(len(suite.cases) for suite in suites)
    if generated_count != EXPECTED_GENERATED_CASE_COUNT:
        errors.append(f"generated composition denominator drifted: {generated_count}")
    note_path = root / EXPERIMENT_NOTE
    if not note_path.is_file():
        errors.append("qualification experiment note is missing")
    if require_clean and _git(root, "status", "--porcelain", "--untracked-files=all"):
        errors.append("formal execution requires a clean worktree")
    if errors:
        raise RuntimeError("; ".join(errors))
    return {
        "status": "passed",
        "execution_commit": _git(root, "rev-parse", "HEAD"),
        "experiment_note": EXPERIMENT_NOTE.as_posix(),
        "experiment_note_sha256": _sha256_path(note_path),
        "current_registry": "configs/current.json",
        "current_registry_sha256": _sha256_path(current_path),
        "task_design_matrix": str(matrix_path.relative_to(root)).replace("\\", "/"),
        "task_design_matrix_sha256": _sha256_path(matrix_path),
        "qualification_design_version": QUALIFICATION_DESIGN_VERSION,
    }


def build_task_structure_baseline(repository_root: str | Path) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    current = json.loads((root / "configs/current.json").read_text(encoding="utf-8"))
    rows = []
    all_components: set[str] = set()
    all_operations: set[str] = set()
    all_instruments: set[str] = set()
    all_metrics: set[str] = set()
    for task in list_tasks():
        components = sorted(
            {
                _OPERATION_COMPONENTS[operation]
                for operation in task.allowed_operations
                if operation in _OPERATION_COMPONENTS
            }
        )
        all_components.update(components)
        all_operations.update(task.allowed_operations)
        all_instruments.update(task.allowed_instruments)
        all_metrics.update(task.success_metrics)
        rows.append(
            {
                "task_id": task.task_id,
                "world_seed_count": len(task.seeds),
                "components": components,
                "operations": list(task.allowed_operations),
                "instruments": list(task.allowed_instruments),
                "resources": {
                    "operation_budget": task.budget,
                    "sample_accounting": "per-instrument",
                    "time_accounting": "per-operation-and-instrument",
                },
                "termination": task.termination_policy,
                "evaluation_metrics": list(task.success_metrics),
            }
        )
    return {
        "status": "passed",
        "task_design_binding": copy.deepcopy(current["task_design"]),
        "registered_task_count": len(rows),
        "world_unit_count": sum(row["world_seed_count"] for row in rows),
        "coverage": {
            "components": sorted(all_components),
            "operations": sorted(all_operations),
            "instruments": sorted(all_instruments),
            "evaluation_metrics": sorted(all_metrics),
        },
        "tasks": rows,
    }


def _run_generated_case(case: Any, *, world_seed: int, scratch_dir: Path) -> dict[str, Any]:
    env = gym.make("ChemWorld", composition=case.request, seed=world_seed)
    trajectory_path = scratch_dir / f"{case.case_id}.jsonl"
    failures: list[dict[str, Any]] = []
    leakage: list[dict[str, Any]] = []
    committed_count = 0
    final_assay_count = 0
    constitution_failure_count = 0
    event_count = 0
    started = time.perf_counter()
    try:
        observation, reset_info = env.reset(seed=world_seed)
        base: Any = env.unwrapped
        logging_task_info = {**base.task_info(), **base.evaluator_provenance()}
        leakage.extend(_leakage_findings(env, reset_info, "reset_info"))
        leakage.extend(
            _leakage_findings(env, agent_view_bundle(env, observation, {}), "initial_agent_view")
        )
        with TrajectoryLogger(trajectory_path) as logger:
            for step, action in enumerate(case.actions, start=1):
                validation = base.validate_action(action)
                if not bool(validation.get("valid")):
                    failures.append(
                        {
                            "step": step,
                            "class": "generated_action_prevalidation_failed",
                            "invalid_reasons": validation.get("invalid_reasons", []),
                        }
                    )
                observation, reward, terminated, truncated, info = env.step(action)
                committed = info.get("transaction_status") == "committed"
                committed_count += int(committed)
                if not committed:
                    failures.append(
                        {
                            "step": step,
                            "class": "generated_transaction_not_committed",
                            "operation": action.get("operation"),
                            "transaction_status": info.get("transaction_status"),
                            "preconditions": info.get("preconditions", {}),
                        }
                    )
                failed_checks = [
                    check
                    for check in info.get("constitution_checks", [])
                    if isinstance(check, dict) and check.get("passed") is False
                ]
                constitution_failure_count += len(failed_checks)
                if failed_checks:
                    failures.append(
                        {
                            "step": step,
                            "class": "constitution_check_failed",
                            "checks": failed_checks,
                        }
                    )
                event_count += len(info.get("world_events", []))
                if (
                    action.get("operation") == "measure"
                    and action.get("instrument") == "final_assay"
                ):
                    final_assay_count += int(committed)
                public_view = agent_view_bundle(env, observation, info)
                leakage.extend(_leakage_findings(env, public_view, f"agent_view.step-{step}"))
                logger.log(
                    task_info=logging_task_info,
                    step=step,
                    action=action,
                    observation=observation_to_json(observation),
                    reward=float(reward),
                    terminated=bool(terminated),
                    truncated=bool(truncated),
                    info=info,
                    agent_metadata={"agent_id": "composition-qualification-reference"},
                    agent_view=public_view,
                )
        records = load_jsonl(trajectory_path)
        replay = verify_records(records, tolerance=0.0).to_dict()
        if not replay["verified"]:
            failures.append({"class": "exact_replay_failed", "mismatches": replay["mismatches"]})
    except Exception as exc:
        replay = {"verified": False, "checked_steps": 0, "max_abs_error": None, "mismatches": []}
        failures.append(
            {
                "class": "execution_exception",
                "exception_type": type(exc).__name__,
                "message": str(exc),
            }
        )
    finally:
        env.close()
    if leakage:
        failures.append({"class": "public_private_leakage", "finding_count": len(leakage)})
    if final_assay_count != 1:
        failures.append(
            {"class": "lifecycle_not_closed", "committed_final_assay_count": final_assay_count}
        )
    elapsed = time.perf_counter() - started
    return {
        "case_id": case.case_id,
        "composition_id": case.request["composition_id"],
        "pattern": str(case.compiled.compatibility.pattern),
        "workflow_id": case.workflow_id,
        "component_count": len(case.request["components"]),
        "workflow_stage_count": len(case.actions),
        "action_count": len(case.actions),
        "committed_action_count": committed_count,
        "constitution_failure_count": constitution_failure_count,
        "world_event_count": event_count,
        "committed_final_assay_count": final_assay_count,
        "public_private_leakage_count": len(leakage),
        "exact_replay": replay,
        "elapsed_s": elapsed,
        "trajectory_bytes": trajectory_path.stat().st_size if trajectory_path.exists() else 0,
        "passed": not failures,
        "failures": failures,
    }


def run_generated_qualification(*, scratch_dir: Path) -> dict[str, Any]:
    suites = build_generated_suites()
    receipts = [
        _run_generated_case(case, world_seed=0, scratch_dir=scratch_dir)
        for suite in suites
        for case in suite.cases
    ]
    pattern_rows = []
    for pattern, denominator in EXPECTED_PATTERN_CASE_COUNTS.items():
        rows = [row for row in receipts if row["pattern"] == pattern]
        pattern_rows.append(
            {
                "pattern": pattern,
                "passed": sum(bool(row["passed"]) for row in rows),
                "denominator": denominator,
                "coverage_report": next(
                    suite.report
                    for suite in suites
                    if str(suite.cases[0].compiled.compatibility.pattern) == pattern
                ),
            }
        )
    return {
        "passed": sum(bool(row["passed"]) for row in receipts),
        "denominator": len(receipts),
        "unseen_pattern": UNSEEN_PATTERN_ID,
        "unseen_passed": sum(
            bool(row["passed"]) for row in receipts if row["pattern"] == UNSEEN_PATTERN_ID
        ),
        "unseen_denominator": EXPECTED_PATTERN_CASE_COUNTS[UNSEEN_PATTERN_ID],
        "pattern_matrix": pattern_rows,
        "cases": receipts,
    }


def _mutant_requests() -> list[dict[str, Any]]:
    by_pattern = {
        str(suite.cases[0].compiled.compatibility.pattern): copy.deepcopy(suite.cases[0].request)
        for suite in build_generated_suites()
    }
    missing_observation = copy.deepcopy(by_pattern["reaction-thermal-observation"])
    missing_observation["composition_id"] = "qualification-mutant-missing-observation"
    missing_observation["components"] = [
        item for item in missing_observation["components"] if item["kind"] != "observation"
    ]
    missing_thermal = copy.deepcopy(by_pattern["reaction-crystallization-observation"])
    missing_thermal["composition_id"] = "qualification-mutant-crystallization-without-thermal"
    missing_thermal["components"] = [
        item for item in missing_thermal["components"] if item["kind"] != "thermal"
    ]
    conflicting = copy.deepcopy(by_pattern["reaction-crystallization-observation"])
    conflicting["composition_id"] = "qualification-mutant-conflicting-phase-owner"
    conflicting["components"].insert(2, {"kind": "phase", "role": "phase", "parameters": {}})
    wrong_unit = copy.deepcopy(by_pattern["reaction-thermal-observation"])
    wrong_unit["composition_id"] = "qualification-mutant-thermal-unit"
    next(item for item in wrong_unit["components"] if item["kind"] == "thermal")["parameters"] = {
        "temperature_range_K": {"value": [350.0, 390.0], "unit": "L"}
    }
    invalid_fraction = copy.deepcopy(by_pattern["reaction-distillation-observation"])
    invalid_fraction["composition_id"] = "qualification-mutant-fraction-count"
    next(item for item in invalid_fraction["components"] if item["kind"] == "distillation")[
        "parameters"
    ]["fraction_count"] = 0
    lifecycle = copy.deepcopy(by_pattern["reaction-thermal-observation"])
    lifecycle["composition_id"] = "qualification-mutant-lifecycle-hole"
    lifecycle["task"]["operations"] = [
        item
        for item in lifecycle["task"].get(
            "operations",
            [
                "add_solvent",
                "add_reagent",
                "add_catalyst",
                "heat",
                "wait",
                "measure",
                "terminate",
            ],
        )
        if item != "terminate"
    ]
    impossible = copy.deepcopy(by_pattern["reaction-thermal-observation"])
    impossible["composition_id"] = "qualification-mutant-resource-impossibility"
    impossible["task"]["budget"] = 3
    impossible["task"]["resources"]["operation_budget"] = 3
    return [
        {
            "mutant_id": "missing-observation",
            "expected": "missing_dependency",
            "request": missing_observation,
        },
        {
            "mutant_id": "crystallization-missing-thermal",
            "expected": "missing_dependency",
            "request": missing_thermal,
        },
        {
            "mutant_id": "conflicting-phase-owner",
            "expected": "conflicting_state_owner",
            "request": conflicting,
        },
        {"mutant_id": "thermal-unit-mismatch", "expected": "unit_mismatch", "request": wrong_unit},
        {
            "mutant_id": "invalid-fraction-count",
            "expected": "invalid_parameter",
            "request": invalid_fraction,
        },
        {"mutant_id": "missing-terminate", "expected": "lifecycle_hole", "request": lifecycle},
        {
            "mutant_id": "insufficient-budget",
            "expected": "resource_impossibility",
            "request": impossible,
        },
    ]


def run_compile_mutants() -> dict[str, Any]:
    receipts = []
    for mutant in _mutant_requests():
        codes: list[str] = []
        constructed = False
        try:
            chemworld.compile_world_composition(mutant["request"])
            constructed = True
        except WorldCompositionError as exc:
            codes = sorted({item.code for item in exc.diagnostics})
        passed = not constructed and mutant["expected"] in codes
        receipts.append(
            {
                "mutant_id": mutant["mutant_id"],
                "expected_diagnostic": mutant["expected"],
                "observed_diagnostics": codes,
                "environment_constructed": constructed,
                "passed": passed,
                "failures": [] if passed else ["compile mutant did not fail closed as specified"],
            }
        )
    return {
        "passed": sum(bool(row["passed"]) for row in receipts),
        "denominator": len(receipts),
        "mutants": receipts,
    }


def _state_metric(env: Any, metric: str) -> float:
    state = env.unwrapped._state
    if metric == "total_species_mol":
        return float(sum(state.species_amounts.values()))
    if metric == "temperature_K":
        return float(state.temperature_K)
    if metric == "volume_L":
        return float(state.volume_L)
    if metric == "time_s":
        return float(state.ledger.time_s)
    if metric == "cost":
        return float(state.ledger.cost)
    raise ValueError(f"unknown module probe metric: {metric}")


def _module_action_receipt(case: Any, config: dict[str, Any], value: float) -> dict[str, Any]:
    env = gym.make("ChemWorld", composition=case.request, seed=0)
    operation = str(config["operation"])
    try:
        env.reset(seed=0)
        focus_index = next(
            index for index, action in enumerate(case.actions) if action["operation"] == operation
        )
        for setup_action in case.actions[:focus_index]:
            _observation, _reward, _terminated, _truncated, info = env.step(setup_action)
            if info.get("transaction_status") != "committed":
                return {"passed": False, "failure": "module setup action did not commit"}
        action = copy.deepcopy(case.actions[focus_index])
        action[str(config["field"])] = value
        before_physical = _physical_snapshot(env)
        before_metric = _state_metric(env, str(config["metric"]))
        base: Any = env.unwrapped
        validation = base.validate_action(action)
        _observation, _reward, _terminated, _truncated, info = env.step(action)
        after_metric = _state_metric(env, str(config["metric"]))
        committed = info.get("transaction_status") == "committed"
        failed_checks = [
            check
            for check in info.get("constitution_checks", [])
            if isinstance(check, dict) and check.get("passed") is False
        ]
        return {
            "passed": committed and bool(validation.get("valid")) and not failed_checks,
            "validation_passed": bool(validation.get("valid")),
            "transaction_status": info.get("transaction_status"),
            "metric_before": before_metric,
            "metric_after": after_metric,
            "metric_delta": after_metric - before_metric,
            "constitution_failure_count": len(failed_checks),
            "physical_state_preserved": _physical_snapshot(env) == before_physical,
        }
    finally:
        env.close()


def run_module_probes() -> dict[str, Any]:
    suites = {
        str(suite.cases[0].compiled.compatibility.pattern): suite
        for suite in build_generated_suites()
    }
    receipts = []
    maturity_rows = []
    for module_id, config in _MODULE_CONFIGS.items():
        case = suites[str(config["pattern"])].cases[0]
        zero = _module_action_receipt(case, config, 0.0)
        zero_delta = zero.get("metric_delta")
        zero_passed = (
            zero.get("transaction_status") != "committed"
            or (
                isinstance(zero_delta, int | float)
                and abs(float(zero_delta)) <= 1.0e-12
            )
        )
        low = _module_action_receipt(case, config, cast(float, config["low"]))
        high = _module_action_receipt(case, config, cast(float, config["high"]))
        low_delta = low.get("metric_delta")
        high_delta = high.get("metric_delta")
        direction_passed = (
            bool(low.get("passed"))
            and bool(high.get("passed"))
            and isinstance(low_delta, int | float)
            and isinstance(high_delta, int | float)
            and float(high_delta) > float(low_delta)
        )
        invariant_passed = (
            int(low.get("constitution_failure_count", 1)) == 0
            and int(high.get("constitution_failure_count", 1)) == 0
        )
        receipts.extend(
            [
                {
                    "module_id": module_id,
                    "probe_id": "zero_input",
                    "classification": "bounded_runtime_probe",
                    "passed": zero_passed,
                    "receipt": zero,
                    "failures": [] if zero_passed else ["zero-input behavior drifted"],
                },
                {
                    "module_id": module_id,
                    "probe_id": "legal_low_high",
                    "classification": "bounded_runtime_probe",
                    "passed": bool(low.get("passed")) and bool(high.get("passed")),
                    "receipt": {"low": low, "high": high},
                    "failures": (
                        []
                        if bool(low.get("passed")) and bool(high.get("passed"))
                        else ["legal low/high boundary did not commit"]
                    ),
                },
                {
                    "module_id": module_id,
                    "probe_id": "directionality_pair",
                    "classification": "conceptual_or_synthetic",
                    "passed": direction_passed,
                    "receipt": {
                        "metric": config["metric"],
                        "low_delta": low.get("metric_delta"),
                        "high_delta": high.get("metric_delta"),
                    },
                    "failures": (
                        [] if direction_passed else ["declared directional pair failed"]
                    ),
                },
                {
                    "module_id": module_id,
                    "probe_id": "conservation_invariant",
                    "classification": "runtime_constitution",
                    "passed": invariant_passed,
                    "receipt": {
                        "low_constitution_failure_count": low.get(
                            "constitution_failure_count"
                        ),
                        "high_constitution_failure_count": high.get(
                            "constitution_failure_count"
                        ),
                    },
                    "failures": (
                        []
                        if invariant_passed
                        else ["module conservation or invariant check failed"]
                    ),
                },
            ]
        )
        env = gym.make("ChemWorld", composition=case.request, seed=0)
        try:
            env.reset(seed=0)
            base: Any = env.unwrapped
            kernel_maturity = base.task_info()["kernel_maturity"]
        finally:
            env.close()
        maturity_rows.append(
            {
                "module_id": module_id,
                "domain": str(config["pattern"]),
                "maturity": kernel_maturity,
                "claim_boundary": "virtual_instrument_qualification_only",
            }
        )
    return {
        "passed": sum(bool(row["passed"]) for row in receipts),
        "denominator": len(receipts),
        "probes": receipts,
        "model_boundaries": maturity_rows,
    }


def build_interface_receipts(generated: dict[str, Any]) -> dict[str, Any]:
    receipts = []
    for path_id, pattern in _INTERFACE_PATHS.items():
        cases = [row for row in generated["cases"] if row["pattern"] == pattern]
        checks = {
            "material_identity_and_units": all(
                int(row["constitution_failure_count"]) == 0 for row in cases
            ),
            "nonnegative_and_applicable_balances": all(
                int(row["constitution_failure_count"]) == 0 for row in cases
            ),
            "state_and_event_propagation": all(
                int(row["world_event_count"]) >= int(row["committed_action_count"])
                for row in cases
            ),
            "transaction_and_replay_closure": all(
                bool(row["passed"]) and bool(row["exact_replay"]["verified"])
                for row in cases
            ),
        }
        receipts.append(
            {
                "path_id": path_id,
                "pattern": pattern,
                "case_count": len(cases),
                "checks": checks,
                "passed": bool(cases) and all(checks.values()),
                "failures": (
                    []
                    if bool(cases) and all(checks.values())
                    else ["cross-component interface path failed"]
                ),
            }
        )
    return {
        "passed": sum(bool(row["passed"]) for row in receipts),
        "denominator": len(receipts),
        "paths": receipts,
    }


def _failure_counts(report_parts: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("passed") is False:
                failures = value.get("failures")
                if isinstance(failures, list) and failures:
                    for failure in failures:
                        if isinstance(failure, dict):
                            counts[str(failure.get("class", "unclassified"))] += 1
                        else:
                            counts[str(failure)] += 1
                elif "failure" in value:
                    counts[str(value["failure"])] += 1
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    for part in report_parts:
        visit(part)
    return dict(sorted(counts.items()))


def build_report(
    *,
    repository_root: str | Path,
    require_clean: bool = True,
) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    binding = validate_launch_preconditions(root, require_clean=require_clean)
    task_structure = build_task_structure_baseline(root)
    reference_units = []
    with tempfile.TemporaryDirectory(prefix="chemworld-composition-qualification-") as tmp:
        scratch = Path(tmp)
        protocol = _reference_protocol()
        for task in list_tasks():
            for world_seed in task.seeds:
                reference_units.append(
                    run_task_world_unit(
                        task,
                        int(world_seed),
                        protocol,
                        scratch_dir=scratch,
                    )
                )
        generated = run_generated_qualification(scratch_dir=scratch)
    valid_cases = [case for unit in reference_units for case in unit["valid_recipe_cases"]]
    negative_probes = [probe for unit in reference_units for probe in unit["negative_probes"]]
    reference = {
        "unit_passed": sum(bool(unit["passed"]) for unit in reference_units),
        "unit_denominator": len(reference_units),
        "recipe_passed": sum(bool(case["passed"]) for case in valid_cases),
        "recipe_denominator": len(valid_cases),
        "negative_probe_passed": sum(bool(probe["passed"]) for probe in negative_probes),
        "negative_probe_denominator": len(negative_probes),
        "units": reference_units,
    }
    mutants = run_compile_mutants()
    modules = run_module_probes()
    interfaces = build_interface_receipts(generated)
    failure_counts = _failure_counts([reference, generated, mutants, modules, interfaces])
    missing_receipt_count = sum(
        (
            EXPECTED_REFERENCE_UNIT_COUNT
            - cast(int, reference["unit_denominator"]),
            EXPECTED_REFERENCE_RECIPE_COUNT
            - cast(int, reference["recipe_denominator"]),
            EXPECTED_NEGATIVE_PROBE_COUNT
            - cast(int, reference["negative_probe_denominator"]),
            EXPECTED_GENERATED_CASE_COUNT - generated["denominator"],
            EXPECTED_COMPILE_MUTANT_COUNT - mutants["denominator"],
            EXPECTED_MODULE_PROBE_COUNT - modules["denominator"],
            EXPECTED_INTERFACE_PATH_COUNT - interfaces["denominator"],
        )
    )
    leakage_count = sum(
        int(case["public_private_leakage_count"]) for case in generated["cases"]
    ) + sum(
        int(case["public_private_leakage_count"])
        for unit in reference_units
        for case in unit["valid_recipe_cases"]
    ) + sum(
        int(probe["public_private_leakage_count"])
        for unit in reference_units
        for probe in unit["negative_probes"]
    )
    overall_pass = (
        reference["unit_passed"] == EXPECTED_REFERENCE_UNIT_COUNT
        and reference["recipe_passed"] == EXPECTED_REFERENCE_RECIPE_COUNT
        and reference["negative_probe_passed"] == EXPECTED_NEGATIVE_PROBE_COUNT
        and generated["passed"] == EXPECTED_GENERATED_CASE_COUNT
        and generated["unseen_passed"] == generated["unseen_denominator"] == 8
        and mutants["passed"] == EXPECTED_COMPILE_MUTANT_COUNT
        and modules["passed"] == EXPECTED_MODULE_PROBE_COUNT
        and interfaces["passed"] == EXPECTED_INTERFACE_PATH_COUNT
        and leakage_count == 0
        and missing_receipt_count == 0
        and not failure_counts
    )
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "qualification_id": QUALIFICATION_ID,
        "status": "passed" if overall_pass else "failed",
        "source_binding": binding,
        "claim_boundary": [
            "Deterministic virtual-instrument qualification only.",
            "Finite v1 component and interface coverage; not exhaustive task-space validation.",
            "No physical-laboratory external-validity or agent-intelligence claim.",
        ],
        "counting_rule": {
            "reference_independent_unit": "registered task by registered world seed",
            "generated_independent_unit": "frozen generated composition case",
            "statistics": "deterministic exact counts only",
        },
        "summary": {
            "reference_units": {
                "passed": reference["unit_passed"],
                "denominator": reference["unit_denominator"],
            },
            "reference_recipes": {
                "passed": reference["recipe_passed"],
                "denominator": reference["recipe_denominator"],
            },
            "negative_probes": {
                "passed": reference["negative_probe_passed"],
                "denominator": reference["negative_probe_denominator"],
            },
            "generated_compositions": {
                "passed": generated["passed"],
                "denominator": generated["denominator"],
            },
            "unseen_distillation_compositions": {
                "passed": generated["unseen_passed"],
                "denominator": generated["unseen_denominator"],
            },
            "compile_mutants": {"passed": mutants["passed"], "denominator": mutants["denominator"]},
            "module_probes": {"passed": modules["passed"], "denominator": modules["denominator"]},
            "interface_paths": {
                "passed": interfaces["passed"],
                "denominator": interfaces["denominator"],
            },
            "public_private_leakage_count": leakage_count,
            "missing_receipt_count": missing_receipt_count,
            "failure_class_counts": failure_counts,
        },
        "task_structure": task_structure,
        "reference_qualification": reference,
        "generated_qualification": generated,
        "compile_mutants": mutants,
        "module_qualification": modules,
        "interface_qualification": interfaces,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    rows = [
        ("Registered task/world units", summary["reference_units"]),
        ("Valid midpoint/boundary/category recipes", summary["reference_recipes"]),
        ("Negative runtime probes", summary["negative_probes"]),
        ("Generated compositions", summary["generated_compositions"]),
        ("Frozen unseen reaction--distillation cases", summary["unseen_distillation_compositions"]),
        ("Compile-time mutants", summary["compile_mutants"]),
        ("Module probes", summary["module_probes"]),
        ("Cross-component interface paths", summary["interface_paths"]),
    ]
    lines = [
        "# First-paper composition qualification",
        "",
        f"Status: **{str(report['status']).upper()}**",
        "",
        "## Exact deterministic counts",
        "",
        "| Quantity | Passed | Denominator |",
        "| --- | ---: | ---: |",
        *[
            f"| {label} | {value['passed']} | {value['denominator']} |"
            for label, value in rows
        ],
        "",
        f"Public/private leakage findings: `{summary['public_private_leakage_count']}`.",
        f"Missing receipts: `{summary['missing_receipt_count']}`.",
        "",
        "## Generated pattern matrix",
        "",
        "| Pattern | Passed | Denominator |",
        "| --- | ---: | ---: |",
    ]
    lines.extend(
        f"| {row['pattern']} | {row['passed']} | {row['denominator']} |"
        for row in report["generated_qualification"]["pattern_matrix"]
    )
    lines.extend(["", "## Failure classes", ""])
    failures = summary["failure_class_counts"]
    if failures:
        lines.extend(f"- `{name}`: {count}" for name, count in failures.items())
    else:
        lines.append("None.")
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            *[f"- {item}" for item in report["claim_boundary"]],
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(report: dict[str, Any], *, output_path: str | Path) -> tuple[Path, Path]:
    report_path = Path(output_path)
    markdown_path = report_path.with_suffix(".md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_path.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    return report_path, markdown_path


__all__ = [
    "EXPECTED_COMPILE_MUTANT_COUNT",
    "EXPECTED_INTERFACE_PATH_COUNT",
    "EXPECTED_MODULE_PROBE_COUNT",
    "EXPECTED_NEGATIVE_PROBE_COUNT",
    "EXPECTED_REFERENCE_RECIPE_COUNT",
    "EXPECTED_REFERENCE_UNIT_COUNT",
    "QUALIFICATION_ID",
    "REPORT_SCHEMA_VERSION",
    "build_interface_receipts",
    "build_report",
    "build_task_structure_baseline",
    "render_markdown",
    "run_compile_mutants",
    "run_generated_qualification",
    "run_module_probes",
    "validate_launch_preconditions",
    "write_outputs",
]
