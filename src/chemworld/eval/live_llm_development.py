"""Resumable Train/Dev-only matrices for the frozen live-LLM roles."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from chemworld.agent_interface import PUBLIC_ACTION_SCHEMA_VERSION
from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.formal_llm import (
    DEFAULT_LLM_FREEZE_PATH,
    audit_live_llm_method_freeze,
    formal_live_llm_method_bindings,
    load_live_llm_method_freeze,
)
from chemworld.eval.formal_matrix import (
    SubprocessCellExecutor,
    build_formal_matrix_plan,
    run_formal_matrix,
)
from chemworld.eval.formal_protocol_v0_4 import CORE_TASKS, load_formal_protocol
from chemworld.eval.formal_runner import (
    FormalCellSpec,
    canonical_sha256,
    file_sha256,
    issue_run_manifest,
    private_seed_commitment,
    private_world_commitment,
)
from chemworld.eval.provenance import git_worktree_dirty
from chemworld.eval.runtime_domain_affordance_audit import guarded_source_sha256
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task
from chemworld.world.world_family import axes_for_task

ROOT = Path(__file__).resolve().parents[3]
DEVELOPMENT_PLAN_PATH = configuration_root() / "methods/llm_v0.4/llm_development_plan.json"
DEFAULT_REPORT_PATH = ROOT / "workstreams/benchmark_v1/reports/live-llm-dev-v0.4.11.json"
FORMAL_PROTOCOL_REPORT_PATH = ROOT / "workstreams/benchmark_v1/reports/formal-protocol-v0.4.json"
RUNTIME_DOMAIN_AFFORDANCE_REPORT_PATH = (
    ROOT / "workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json"
)
RUNTIME_DOMAIN_AFFORDANCE_AUDIT_VERSION = (
    "chemworld-runtime-domain-affordance-audit-0.4"
)
LIVE_LLM_DEVELOPMENT_VERSION = "chemworld-live-llm-development-audit-0.4.11"
LIVE_LLM_DEVELOPMENT_PLAN_VERSION = "chemworld-live-llm-development-plan-0.4.7"
LIVE_STAGES = ("candidate_screen", "live_pilot", "development_matrix")
_PRIOR_PAID_STAGE = {
    "live_pilot": "candidate_screen",
    "development_matrix": "live_pilot",
}


def _git_common_dir() -> Path:
    raw = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"], cwd=ROOT, text=True
    ).strip()
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def _git_commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


DEFAULT_CACHE_ROOT = _git_common_dir() / "chemworld-private/live-llm-dev-v0.4.11" / _git_commit()


@dataclass(frozen=True)
class LiveLLMDevelopmentBundle:
    stage: str
    manifest: dict[str, Any]
    private_runtimes: dict[str, dict[str, Any]]
    pair_count: int
    cell_count: int
    maximum_provider_call_count: int


def load_live_llm_development_plan(
    path: str | Path = DEVELOPMENT_PLAN_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("live-LLM development plan must be a JSON object")
    if payload.get("schema_version") != LIVE_LLM_DEVELOPMENT_PLAN_VERSION:
        raise ValueError("live-LLM development plan has an unsupported schema version")
    return payload


def _promotion_gate_card(plan: Mapping[str, Any], stage: str) -> Mapping[str, Any]:
    gates = plan.get("promotion_gates")
    gate = gates.get(stage) if isinstance(gates, Mapping) else None
    if not isinstance(gate, Mapping):
        raise ValueError(f"live-LLM stage {stage!r} has no promotion gate")
    for key in (
        "minimum_overall_completion_rate",
        "minimum_per_method_completion_rate",
    ):
        value = gate.get(key)
        if (
            isinstance(value, bool)
            or not isinstance(value, int | float)
            or not 0.0 <= float(value) <= 1.0
        ):
            raise ValueError(f"live-LLM promotion gate {key!r} must be in [0, 1]")
    for key in (
        "maximum_projected_four_experiment_p90_input_tokens",
        "maximum_projected_four_experiment_p90_wall_time_s",
    ):
        value = gate.get(key)
        if isinstance(value, bool) or not isinstance(value, int | float) or float(value) <= 0.0:
            raise ValueError(f"live-LLM promotion gate {key!r} must be positive")
    return gate


def _backend_semantic_sha256() -> str:
    report = json.loads(FORMAL_PROTOCOL_REPORT_PATH.read_text(encoding="utf-8"))
    value = report.get("backend_semantic_sha256")
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError("formal protocol report is missing its backend semantic hash")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError("formal protocol backend semantic hash is not hexadecimal") from exc
    return value


def load_runtime_domain_affordance_binding(
    path: str | Path = RUNTIME_DOMAIN_AFFORDANCE_REPORT_PATH,
    *,
    verify_source: bool = True,
) -> dict[str, Any]:
    """Load the passing public-affordance audit and reject semantic drift.

    The historical formal-protocol backend hash predates the action-domain fixes.
    A live cell therefore binds this newer audit separately.  Documentation, claim,
    agent presentation and orchestration modules may change without invalidating the
    physical audit; any guarded action/validator/runtime/observation source change
    requires the audit to be regenerated before provider use.
    """

    report_path = Path(path)
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("runtime-domain affordance audit must be a JSON object")
    if payload.get("schema_version") != RUNTIME_DOMAIN_AFFORDANCE_AUDIT_VERSION:
        raise ValueError("runtime-domain affordance audit has an unsupported schema version")
    checks = payload.get("checks")
    summary = payload.get("summary")
    if (
        payload.get("passed") is not True
        or payload.get("status") != "passed"
        or not isinstance(checks, Mapping)
        or not checks
        or not all(value is True for value in checks.values())
        or payload.get("findings") != []
        or not isinstance(summary, Mapping)
        or summary.get("finding_count") != 0
        or summary.get("runtime_committed_count") != summary.get("validator_valid_count")
    ):
        raise RuntimeError("runtime-domain affordance audit is not a clean passing audit")
    source_commit = payload.get("source_commit")
    if (
        not isinstance(source_commit, str)
        or len(source_commit) != 40
        or any(character not in "0123456789abcdef" for character in source_commit)
    ):
        raise ValueError("runtime-domain affordance audit source commit is invalid")
    if verify_source:
        expected_source_digest = payload.get("guarded_source_sha256")
        if (
            not isinstance(expected_source_digest, str)
            or len(expected_source_digest) != 64
            or guarded_source_sha256(ROOT) != expected_source_digest
        ):
            raise RuntimeError(
                "runtime-affordance source changed after the passing audit; regenerate it"
            )
    return {
        "schema_version": RUNTIME_DOMAIN_AFFORDANCE_AUDIT_VERSION,
        "public_action_schema_version": PUBLIC_ACTION_SCHEMA_VERSION,
        "audit_source_commit": source_commit,
        "audit_source_tree_dirty": payload.get("guarded_sources_match_source_commit")
        is not True,
        "guarded_source_sha256": str(payload.get("guarded_source_sha256", "")),
        "audit_report_sha256": file_sha256(report_path),
        "candidate_count": int(summary["candidate_count"]),
        "validator_valid_count": int(summary["validator_valid_count"]),
        "runtime_committed_count": int(summary["runtime_committed_count"]),
        "finding_count": 0,
    }


def _require_planned_runtime_domain_binding(
    plan: Mapping[str, Any], binding: Mapping[str, Any]
) -> None:
    expected = plan.get("runtime_domain_gate")
    if not isinstance(expected, Mapping):
        raise ValueError("live-LLM development plan is missing its runtime-domain gate")
    required = {
        "required_public_action_schema_version": binding["public_action_schema_version"],
        "required_audit_schema_version": binding["schema_version"],
        "required_guarded_source_sha256": binding["guarded_source_sha256"],
        "require_zero_findings": True,
    }
    if dict(expected) != required:
        raise RuntimeError("live-LLM development plan does not match the passing runtime audit")


def _paired_method_seed(stage: str, world_seed: int) -> int:
    digest = hashlib.sha256(f"live-llm-v0.4.11:{stage}:{world_seed}".encode()).digest()
    return 300_000 + int.from_bytes(digest[:4], "big") % 700_000_000


def _pair_id(stage: str, world_seed: int) -> str:
    return canonical_sha256(
        {
            "schema_version": LIVE_LLM_DEVELOPMENT_VERSION,
            "stage": stage,
            "world_seed": world_seed,
            "role": "opaque_public_development_pair",
        }
    )


def _public_interventions(
    protocol: Mapping[str, Any],
    *,
    task_id: str,
    split: str,
    seed: int,
) -> tuple[dict[str, Any], ...]:
    public = protocol["world_family_contract"]["public_development_severities"][split]
    modes = tuple(sorted(public))
    start = int(protocol["split_contract"][split]["base_seeds"]["start"])
    offset = seed - start
    mode = modes[offset % len(modes)]
    severities = tuple(float(item) for item in public[mode])
    severity = severities[(offset // len(modes)) % len(severities)]
    axes = axes_for_task(task_id)
    axis = axes[(offset // max(1, len(modes) * len(severities))) % len(axes)]
    return ({"axis_id": axis.axis_id, "mode": mode, "severity": severity},)


def _stage_seeds(
    protocol: Mapping[str, Any],
    stage_card: Mapping[str, Any],
    supplied: Sequence[int] | None,
) -> tuple[int, ...]:
    split = str(stage_card["world_split"])
    if split not in {"train", "dev"}:
        raise ValueError("live provider development may use only Train or Dev")
    bounds = protocol["split_contract"][split]["base_seeds"]
    start = int(bounds["start"])
    stop = int(bounds["stop_inclusive"])
    count = int(stage_card["world_seeds_per_cell"])
    if stage_card.get("world_seed_selection") != "first_n_from_split":
        raise ValueError("live-LLM stage must freeze first_n_from_split seed selection")
    frozen_seeds = tuple(range(start, start + count))
    seeds = frozen_seeds if supplied is None else tuple(supplied)
    if not seeds or len(seeds) != len(set(seeds)):
        raise ValueError("live-LLM development seeds must be unique and non-empty")
    if any(isinstance(seed, bool) or seed < start or seed > stop for seed in seeds):
        raise ValueError(f"{split} seed is outside the public formal range")
    if seeds != frozen_seeds:
        raise ValueError("live-LLM stage seed set is frozen by the development plan")
    return seeds


def _operation_limits_by_task(
    stage_card: Mapping[str, Any],
    *,
    tasks: Sequence[str],
    complete_experiments: int,
) -> dict[str, int]:
    budget = stage_card.get("operation_budget")
    if not isinstance(budget, Mapping):
        raise ValueError("live-LLM stage is missing its operation-budget contract")
    if budget.get("source") != "task_recipe_event_count_times_complete_experiments":
        raise ValueError("unsupported live-LLM operation-budget source")
    multiplier = budget.get("exploration_multiplier")
    if isinstance(multiplier, bool) or not isinstance(multiplier, int) or multiplier < 1:
        raise ValueError("live-LLM exploration multiplier must be a positive integer")
    return {
        task_id: (
            task_recipe_event_count(get_task(task_id).to_dict()) * complete_experiments * multiplier
        )
        for task_id in tasks
    }


def build_live_llm_development_bundle(
    *,
    stage: str,
    seeds: Sequence[int] | None = None,
    tasks: Sequence[str] | None = None,
    methods: Sequence[str] | None = None,
    spectrum_conditions: Sequence[str] | None = None,
) -> LiveLLMDevelopmentBundle:
    """Build an issued development matrix without reading Bench/reference-search state."""

    if stage not in LIVE_STAGES:
        raise ValueError(f"stage must be one of {LIVE_STAGES}")
    plan = load_live_llm_development_plan()
    runtime_domain_binding = load_runtime_domain_affordance_binding()
    _require_planned_runtime_domain_binding(plan, runtime_domain_binding)
    protocol = load_formal_protocol()
    freeze = load_live_llm_method_freeze()
    if audit_live_llm_method_freeze(freeze)["controls_ready"] is not True:
        raise RuntimeError("live-LLM method freeze must pass before development")
    stage_card = plan["stages"][stage]
    _promotion_gate_card(plan, stage)
    stage_tasks = tuple(stage_card.get("tasks", CORE_TASKS))
    selected_tasks = stage_tasks if tasks is None else tuple(tasks)
    if selected_tasks != stage_tasks:
        raise ValueError("live-LLM stage task scope is frozen by the development plan")
    if stage_card.get("live_provider_calls") is not True:
        raise ValueError("selected stage is not a live-provider development stage")
    split = str(stage_card["world_split"])
    selected_seeds = _stage_seeds(protocol, stage_card, seeds)
    if not set(selected_tasks).issubset(set(CORE_TASKS)) or not selected_tasks:
        raise ValueError("live-LLM development tasks must be frozen formal core tasks")
    bindings = formal_live_llm_method_bindings(freeze)
    frozen_methods = tuple(plan["methods"])
    selected_methods = frozen_methods if methods is None else tuple(methods)
    if selected_methods != frozen_methods or set(selected_methods) != set(bindings):
        raise ValueError("live-LLM stage method scope is frozen by the development plan")
    frozen_conditions = tuple(plan["spectrum_conditions"])
    conditions = frozen_conditions if spectrum_conditions is None else tuple(spectrum_conditions)
    if conditions != frozen_conditions or set(conditions) != {
        "assigned",
        "unassigned",
        "masked",
    }:
        raise ValueError("live-LLM stage spectrum scope is frozen to all three conditions")
    complete_experiments = int(stage_card["complete_experiments"])
    operation_limits = _operation_limits_by_task(
        stage_card,
        tasks=selected_tasks,
        complete_experiments=complete_experiments,
    )
    resource_contract = freeze.get("resource_contract")
    if not isinstance(resource_contract, Mapping):
        raise ValueError("live-LLM freeze is missing its resource contract")
    provider_attempt_limit = int(resource_contract["provider_attempt_limit_per_operation"])
    source_commit = _git_commit()
    global_identity = {
        "schema_version": LIVE_LLM_DEVELOPMENT_VERSION,
        "stage": stage,
        "split": split,
        "tasks": list(selected_tasks),
        "methods": list(selected_methods),
        "spectrum_conditions": list(conditions),
        "pair_ids": [_pair_id(stage, seed) for seed in selected_seeds],
        "complete_experiments": complete_experiments,
        "operation_limits_by_task": operation_limits,
        "source_commit": source_commit,
        "formal_protocol_sha256": canonical_sha256(protocol),
        "llm_freeze_sha256": file_sha256(DEFAULT_LLM_FREEZE_PATH),
        "development_plan_sha256": file_sha256(DEVELOPMENT_PLAN_PATH),
        "runtime_domain_affordance": runtime_domain_binding,
    }
    run_id = canonical_sha256(global_identity)
    protocol_sha256 = canonical_sha256(protocol)
    backend_semantic_sha256 = _backend_semantic_sha256()
    evaluator_sha256 = file_sha256(ROOT / "src/chemworld/eval/verify.py")
    interaction_sha256 = file_sha256(ROOT / "configs/benchmark/interaction_strata_v0.4.json")
    statistics_sha256 = file_sha256(ROOT / "configs/benchmark/statistical_analysis_plan_v0.4.json")
    reference_sha256 = file_sha256(ROOT / "configs/benchmark/reference_portfolio_v0.4.json")
    cells: list[FormalCellSpec] = []
    runtimes: dict[str, dict[str, Any]] = {}
    for world_seed in selected_seeds:
        pair_id = _pair_id(stage, world_seed)
        method_seed = _paired_method_seed(stage, world_seed)
        seed_nonce = canonical_sha256(
            {"kind": "method_nonce", "stage": stage, "world_seed": world_seed}
        )
        world_nonce = canonical_sha256(
            {"kind": "world_nonce", "stage": stage, "world_seed": world_seed}
        )
        seed_commitment = private_seed_commitment(
            run_id=run_id,
            pair_id=pair_id,
            method_seed=method_seed,
            nonce=seed_nonce,
        )
        for task_id in selected_tasks:
            interventions = _public_interventions(
                protocol,
                task_id=task_id,
                split=split,
                seed=world_seed,
            )
            world_commitment = private_world_commitment(
                run_id=run_id,
                task_id=task_id,
                pair_id=pair_id,
                world_seed=world_seed,
                nonce=world_nonce,
                interventions=interventions,
            )
            runtime_payload = {
                "method_seed": method_seed,
                "world_seed": world_seed,
                "seed_nonce": seed_nonce,
                "world_nonce": world_nonce,
                "world_interventions": list(interventions),
            }
            for method_id in selected_methods:
                for condition in conditions:
                    operation_limit = operation_limits[task_id]
                    spec = FormalCellSpec(
                        run_id=run_id,
                        task_id=task_id,
                        pair_id=pair_id,
                        spectrum_condition=condition,
                        private_seed_commitment=seed_commitment,
                        world_commitment=world_commitment,
                        protocol_sha256=protocol_sha256,
                        backend_semantic_sha256=backend_semantic_sha256,
                        evaluator_sha256=evaluator_sha256,
                        interaction_protocol_sha256=interaction_sha256,
                        statistics_protocol_sha256=statistics_sha256,
                        reference_manifest_sha256=reference_sha256,
                        source_commit=source_commit,
                        complete_experiments=complete_experiments,
                        operation_limit=operation_limit,
                        method=bindings[method_id],
                    )
                    cells.append(spec)
                    runtimes[spec.cell_identity_sha256] = dict(runtime_payload)
    pair_ids = [_pair_id(stage, seed) for seed in selected_seeds]
    cell_count = len(cells)
    per_cell_cost_limit = float(resource_contract["monetary_cost_usd_limit_per_cell"])
    stage_cost_limit = stage_card.get("matrix_monetary_cost_usd_limit")
    if (
        isinstance(stage_cost_limit, bool)
        or not isinstance(stage_cost_limit, int | float)
        or not Decimal("0")
        < Decimal(str(stage_cost_limit))
        <= Decimal(str(per_cell_cost_limit)) * cell_count
    ):
        raise ValueError(
            "live-LLM stage matrix cost limit must be positive and no greater "
            "than the sum of its per-cell limits"
        )
    manifest = issue_run_manifest(
        cells,
        metadata={
            "matrix_contract": {
                "tasks": list(selected_tasks),
                "methods": list(selected_methods),
                "pair_ids": pair_ids,
                "spectrum_conditions_by_method": {
                    method_id: list(conditions) for method_id in selected_methods
                },
                "checkpoints": [
                    point for point in (1, 2, 4, 8, 12, 20, 40) if point <= complete_experiments
                ],
                "complete_experiments_per_cell": complete_experiments,
                "operation_limits_by_task": operation_limits,
            },
            "orchestration": {
                "cpu_workers": 1,
                "gpu_devices": [],
                "api_max_concurrency": 4,
                "api_cell_starts_per_minute": 120,
                "api_cost_usd_per_cell_limit": per_cell_cost_limit,
                "matrix_monetary_cost_usd_limit": float(stage_cost_limit),
            },
            "rl_training_resources": [],
            "development_contract": {
                "schema_version": LIVE_LLM_DEVELOPMENT_VERSION,
                "stage": stage,
                "split": split,
                "formal_protocol_split": split,
                "backend_world_split_by_task": {
                    task_id: get_task(task_id).world_split
                    for task_id in selected_tasks
                },
                "seed_count": len(selected_seeds),
                "bench_accessed": False,
                "reference_search_accessed": False,
                "private_reasoning_retained": False,
                "maximum_provider_call_count": sum(
                    cell.operation_limit * provider_attempt_limit for cell in cells
                ),
                "development_plan_sha256": file_sha256(DEVELOPMENT_PLAN_PATH),
                "runtime_domain_affordance": runtime_domain_binding,
            },
        },
    )
    return LiveLLMDevelopmentBundle(
        stage=stage,
        manifest=manifest,
        private_runtimes=runtimes,
        pair_count=len(selected_seeds),
        cell_count=cell_count,
        maximum_provider_call_count=sum(
            cell.operation_limit * provider_attempt_limit for cell in cells
        ),
    )


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def evaluate_live_llm_promotion(
    matrix_report: Mapping[str, Any],
    *,
    stage: str,
    development_plan: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Decide whether a live configuration deserves a larger paid matrix.

    Formal-matrix aggregation intentionally retains valid method failures.  That is
    necessary for unbiased benchmark accounting, but it is not a sufficient development
    gate: a configuration that repeatedly exhausts time or tokens must not automatically
    advance merely because every failure was recorded correctly.
    """

    plan = (
        dict(development_plan) if development_plan is not None else load_live_llm_development_plan()
    )
    if stage not in LIVE_STAGES:
        raise ValueError(f"stage must be one of {LIVE_STAGES}")
    gate = _promotion_gate_card(plan, stage)
    stage_card = plan["stages"][stage]
    expected_experiments = int(stage_card["complete_experiments"])
    audit = matrix_report.get("audit")
    audit = audit if isinstance(audit, Mapping) else {}
    raw_cells = audit.get("cells")
    cells = (
        [item for item in raw_cells if isinstance(item, Mapping)]
        if isinstance(raw_cells, list)
        else []
    )

    def completed(cell: Mapping[str, Any]) -> bool:
        axes = cell.get("resource_axes")
        return (
            cell.get("status") == "succeeded"
            and isinstance(axes, Mapping)
            and int(axes.get("complete_experiment_count", 0)) >= expected_experiments
            and cell.get("replay_verified") is True
        )

    successful = [cell for cell in cells if completed(cell)]
    completion_rate = len(successful) / len(cells) if cells else 0.0
    methods = sorted({str(cell.get("method_id")) for cell in cells})
    tasks = sorted({str(cell.get("task_id")) for cell in cells})
    expected_tasks = set(stage_card.get("tasks", plan["tasks"]))
    expected_methods = set(plan["methods"])
    per_method_completion_rate = {
        method: (
            sum(completed(cell) for cell in cells if cell.get("method_id") == method)
            / sum(cell.get("method_id") == method for cell in cells)
        )
        for method in methods
    }
    successful_tasks = {str(cell.get("task_id")) for cell in successful}
    successful_methods = {str(cell.get("method_id")) for cell in successful}

    projected_input: list[float] = []
    projected_wall: list[float] = []
    for cell in cells:
        axes = cell.get("resource_axes")
        if not isinstance(axes, Mapping):
            continue
        complete_count = int(axes.get("complete_experiment_count", 0))
        if complete_count <= 0:
            continue
        factor = 4.0 / complete_count
        projected_input.append(float(axes.get("input_token_count", 0)) * factor)
        projected_wall.append(float(axes.get("wall_time_s", 0.0)) * factor)

    projected_input_p90 = _percentile(projected_input, 0.9)
    projected_wall_p90 = _percentile(projected_wall, 0.9)
    minimum_overall = float(gate["minimum_overall_completion_rate"])
    minimum_per_method = float(gate["minimum_per_method_completion_rate"])
    maximum_input = float(gate["maximum_projected_four_experiment_p90_input_tokens"])
    maximum_wall = float(gate["maximum_projected_four_experiment_p90_wall_time_s"])
    checks = {
        "matrix_terminal_and_exact": bool(cells)
        and audit.get("exact_cartesian_matrix_complete") is True,
        "expected_task_and_method_scope_complete": set(tasks) == expected_tasks
        and set(methods) == expected_methods,
        "paired_spectrum_conditions_complete": audit.get("paired_conditions_complete") is True,
        "resource_accounting_complete": audit.get("all_required_resource_accounting_complete")
        is True,
        "all_successes_replay_verified": audit.get("all_successes_replay_verified") is True,
        "no_infrastructure_errors": not matrix_report.get("infrastructure_errors"),
        "minimum_overall_completion_rate": completion_rate >= minimum_overall,
        "minimum_per_method_completion_rate": bool(per_method_completion_rate)
        and all(rate >= minimum_per_method for rate in per_method_completion_rate.values()),
        "every_task_has_success": (
            not bool(gate.get("every_task_has_success")) or set(tasks).issubset(successful_tasks)
        ),
        "every_method_has_success": (
            not bool(gate.get("every_method_has_success"))
            or set(methods).issubset(successful_methods)
        ),
        "projected_input_has_headroom": projected_input_p90 is not None
        and projected_input_p90 <= maximum_input,
        "projected_wall_time_has_headroom": projected_wall_p90 is not None
        and projected_wall_p90 <= maximum_wall,
    }
    passed = all(checks.values())
    return {
        "schema_version": "chemworld-live-llm-promotion-gate-0.1",
        "stage": stage,
        "decision": "promote" if passed else "reject_or_redesign",
        "promotes_to": gate.get("promotes_to"),
        "passed": passed,
        "checks": checks,
        "terminal_cell_count": len(cells),
        "successful_cell_count": len(successful),
        "completion_rate": completion_rate,
        "per_method_completion_rate": per_method_completion_rate,
        "projected_four_experiment_p90_input_tokens": projected_input_p90,
        "projected_four_experiment_p90_wall_time_s": projected_wall_p90,
        "thresholds": dict(gate),
    }


def _percentile(values: Sequence[float], quantile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(float(value) for value in values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def _require_prior_paid_stage(stage: str, cache_root: str | Path) -> None:
    prior = _PRIOR_PAID_STAGE.get(stage)
    if prior is None:
        return
    path = Path(cache_root) / prior / "promotion-gate.json"
    if not path.is_file():
        raise RuntimeError(
            f"{stage} is blocked until {prior} has a persisted passing promotion gate"
        )
    gate = json.loads(path.read_text(encoding="utf-8"))
    if gate.get("passed") is not True:
        raise RuntimeError(f"{stage} is blocked because {prior} did not pass promotion")
    if gate.get("llm_freeze_sha256") != file_sha256(DEFAULT_LLM_FREEZE_PATH):
        raise RuntimeError(f"{stage} is blocked because the promoted LLM freeze changed")
    if gate.get("development_plan_sha256") != file_sha256(DEVELOPMENT_PLAN_PATH):
        raise RuntimeError(f"{stage} is blocked because the development plan changed")
    if gate.get("source_commit") != _git_commit():
        raise RuntimeError(f"{stage} is blocked because the promoted source commit changed")
    if gate.get("runtime_domain_affordance") != load_runtime_domain_affordance_binding():
        raise RuntimeError(f"{stage} is blocked because the runtime-domain binding changed")


def _require_clean_source_tree() -> None:
    if git_worktree_dirty(ROOT):
        raise RuntimeError(
            "live-provider development requires a clean source worktree bound to the source commit"
        )


def prepare_live_llm_development(
    *,
    stage: str,
    seeds: Sequence[int] | None = None,
    cache_root: str | Path = DEFAULT_CACHE_ROOT,
) -> tuple[LiveLLMDevelopmentBundle, Path, Path, Path]:
    bundle = build_live_llm_development_bundle(stage=stage, seeds=seeds)
    root = Path(cache_root) / stage
    manifest_path = root / "manifest.json"
    runtime_root = root / "private-runtimes"
    output_root = root / "matrix"
    if manifest_path.is_file():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        if existing.get("run_manifest_sha256") != bundle.manifest["run_manifest_sha256"]:
            raise RuntimeError("existing live-LLM development manifest has another identity")
    else:
        _atomic_json(manifest_path, bundle.manifest)
    runtime_root.mkdir(parents=True, exist_ok=True)
    for cell_id, runtime in bundle.private_runtimes.items():
        path = runtime_root / f"{cell_id}.json"
        if not path.is_file():
            _atomic_json(path, runtime)
    return bundle, manifest_path, runtime_root, output_root


def run_live_llm_development(
    *,
    stage: str,
    seeds: Sequence[int] | None = None,
    cache_root: str | Path = DEFAULT_CACHE_ROOT,
    report_path: str | Path | None = None,
    stop_after_new_terminals: int | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run or resume a live Train/Dev matrix; never reads Bench/reference-search."""

    _require_prior_paid_stage(stage, cache_root)
    _require_clean_source_tree()
    bundle, manifest_path, runtime_root, output_root = prepare_live_llm_development(
        stage=stage,
        seeds=seeds,
        cache_root=cache_root,
    )
    plan = build_formal_matrix_plan(bundle.manifest)
    executor = SubprocessCellExecutor(
        manifest_path=str(manifest_path.resolve()),
        output_root=str(output_root.resolve()),
        private_runtime_root=str(runtime_root.resolve()),
        adapter_factory=("chemworld.eval.formal_llm:create_formal_live_llm_adapter"),
        python_executable=sys.executable,
        cell_script=str((ROOT / "scripts/run_formal_cell.py").resolve()),
        private_diagnostic_root=str((runtime_root.parent / "private-diagnostics").resolve()),
    )
    outcome = run_formal_matrix(
        plan=plan,
        executor=executor,
        output_root=output_root,
        progress_callback=progress_callback,
        stop_after_new_terminals=stop_after_new_terminals,
    )
    full_scope = stage == "development_matrix" and seeds is None
    promotion_gate = evaluate_live_llm_promotion(outcome.report, stage=stage)
    persisted_promotion_gate = {
        **promotion_gate,
        "manifest_sha256": bundle.manifest["run_manifest_sha256"],
        "llm_freeze_sha256": file_sha256(DEFAULT_LLM_FREEZE_PATH),
        "development_plan_sha256": file_sha256(DEVELOPMENT_PLAN_PATH),
        "source_commit": _git_commit(),
        "runtime_domain_affordance": bundle.manifest["metadata"]["development_contract"][
            "runtime_domain_affordance"
        ],
    }
    _atomic_json(
        Path(cache_root) / stage / "promotion-gate.json",
        persisted_promotion_gate,
    )
    development_ready = (
        full_scope
        and outcome.report["audit"]["aggregation_ready"] is True
        and promotion_gate["passed"] is True
    )
    report = {
        "schema_version": LIVE_LLM_DEVELOPMENT_VERSION,
        "status": (
            "formal_live_llm_development_ready"
            if development_ready
            else (
                "live_llm_configuration_rejected"
                if outcome.report["audit"].get("exact_cartesian_matrix_complete") is True
                and promotion_gate["passed"] is False
                else outcome.report["status"]
            )
        ),
        "formal_live_llm_development_ready": development_ready,
        "benchmark_claim_allowed": False,
        "bench_results_present": False,
        "reference_search_results_used": False,
        "private_reasoning_retained": False,
        "stage": stage,
        "formal_protocol_split": bundle.manifest["metadata"][
            "development_contract"
        ]["formal_protocol_split"],
        "backend_world_split_by_task": bundle.manifest["metadata"][
            "development_contract"
        ]["backend_world_split_by_task"],
        "source_commit": _git_commit(),
        "runtime_domain_affordance": bundle.manifest["metadata"]["development_contract"][
            "runtime_domain_affordance"
        ],
        "method_freeze_audit": audit_live_llm_method_freeze(),
        "manifest_sha256": bundle.manifest["run_manifest_sha256"],
        "development_plan_sha256": file_sha256(DEVELOPMENT_PLAN_PATH),
        "cell_count": bundle.cell_count,
        "pair_count": bundle.pair_count,
        "maximum_provider_call_count": bundle.maximum_provider_call_count,
        "promotion_gate": persisted_promotion_gate,
        "matrix_run": outcome.report,
    }
    if report_path is not None:
        _atomic_json(Path(report_path), report)
    return report


__all__ = [
    "DEFAULT_CACHE_ROOT",
    "DEFAULT_REPORT_PATH",
    "DEVELOPMENT_PLAN_PATH",
    "LIVE_LLM_DEVELOPMENT_VERSION",
    "LIVE_STAGES",
    "RUNTIME_DOMAIN_AFFORDANCE_REPORT_PATH",
    "LiveLLMDevelopmentBundle",
    "build_live_llm_development_bundle",
    "evaluate_live_llm_promotion",
    "load_live_llm_development_plan",
    "load_runtime_domain_affordance_binding",
    "prepare_live_llm_development",
    "run_live_llm_development",
]
