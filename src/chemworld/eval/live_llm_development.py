"""Resumable Train/Dev-only matrices for the frozen live-LLM roles."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
from chemworld.tasks import get_task
from chemworld.world.world_family import axes_for_task

ROOT = Path(__file__).resolve().parents[3]
DEVELOPMENT_PLAN_PATH = ROOT / "configs/methods/llm_v0.4/llm_development_plan.json"
DEFAULT_REPORT_PATH = ROOT / "workstreams/benchmark_v1/reports/live-llm-dev-v0.4.6.json"
FORMAL_PROTOCOL_REPORT_PATH = (
    ROOT / "workstreams/benchmark_v1/reports/formal-protocol-v0.4.json"
)
LIVE_LLM_DEVELOPMENT_VERSION = "chemworld-live-llm-development-audit-0.4.6"
LIVE_STAGES = ("live_pilot", "development_matrix")


def _git_common_dir() -> Path:
    raw = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"], cwd=ROOT, text=True
    ).strip()
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


DEFAULT_CACHE_ROOT = _git_common_dir() / "chemworld-private/live-llm-dev-v0.4.6"


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
    return payload


def _git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


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


def _paired_method_seed(stage: str, world_seed: int) -> int:
    digest = hashlib.sha256(f"live-llm-v0.4:{stage}:{world_seed}".encode()).digest()
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
    seeds = tuple(range(start, start + count)) if supplied is None else tuple(supplied)
    if not seeds or len(seeds) != len(set(seeds)):
        raise ValueError("live-LLM development seeds must be unique and non-empty")
    if any(isinstance(seed, bool) or seed < start or seed > stop for seed in seeds):
        raise ValueError(f"{split} seed is outside the public formal range")
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
            task_recipe_event_count(get_task(task_id).to_dict())
            * complete_experiments
            * multiplier
        )
        for task_id in tasks
    }


def build_live_llm_development_bundle(
    *,
    stage: str,
    seeds: Sequence[int] | None = None,
    tasks: Sequence[str] = CORE_TASKS,
    methods: Sequence[str] = ("live_llm_a", "live_llm_b"),
    spectrum_conditions: Sequence[str] = ("assigned", "unassigned", "masked"),
) -> LiveLLMDevelopmentBundle:
    """Build an issued development matrix without reading Bench/reference-search state."""

    if stage not in LIVE_STAGES:
        raise ValueError(f"stage must be one of {LIVE_STAGES}")
    plan = load_live_llm_development_plan()
    protocol = load_formal_protocol()
    freeze = load_live_llm_method_freeze()
    if audit_live_llm_method_freeze(freeze)["controls_ready"] is not True:
        raise RuntimeError("live-LLM method freeze must pass before development")
    stage_card = plan["stages"][stage]
    if stage_card.get("live_provider_calls") is not True:
        raise ValueError("selected stage is not a live-provider development stage")
    split = str(stage_card["world_split"])
    selected_seeds = _stage_seeds(protocol, stage_card, seeds)
    if not set(tasks).issubset(set(CORE_TASKS)) or not tasks:
        raise ValueError("live-LLM development tasks must be frozen formal core tasks")
    bindings = formal_live_llm_method_bindings(freeze)
    if not set(methods).issubset(bindings) or not methods:
        raise ValueError("live-LLM development methods must be frozen roles")
    conditions = tuple(spectrum_conditions)
    if set(conditions) != {"assigned", "unassigned", "masked"} or len(conditions) != 3:
        raise ValueError("live-LLM development requires all three spectrum conditions")
    complete_experiments = int(stage_card["complete_experiments"])
    operation_limits = _operation_limits_by_task(
        stage_card,
        tasks=tasks,
        complete_experiments=complete_experiments,
    )
    resource_contract = freeze.get("resource_contract")
    if not isinstance(resource_contract, Mapping):
        raise ValueError("live-LLM freeze is missing its resource contract")
    provider_attempt_limit = int(
        resource_contract["provider_attempt_limit_per_operation"]
    )
    source_commit = _git_commit()
    global_identity = {
        "schema_version": LIVE_LLM_DEVELOPMENT_VERSION,
        "stage": stage,
        "split": split,
        "tasks": list(tasks),
        "methods": list(methods),
        "spectrum_conditions": list(conditions),
        "pair_ids": [_pair_id(stage, seed) for seed in selected_seeds],
        "complete_experiments": complete_experiments,
        "operation_limits_by_task": operation_limits,
        "source_commit": source_commit,
        "formal_protocol_sha256": canonical_sha256(protocol),
        "llm_freeze_sha256": file_sha256(DEFAULT_LLM_FREEZE_PATH),
    }
    run_id = canonical_sha256(global_identity)
    protocol_sha256 = canonical_sha256(protocol)
    backend_semantic_sha256 = _backend_semantic_sha256()
    evaluator_sha256 = file_sha256(ROOT / "src/chemworld/eval/verify.py")
    interaction_sha256 = file_sha256(
        ROOT / "configs/benchmark/interaction_strata_v0.4.json"
    )
    statistics_sha256 = file_sha256(
        ROOT / "configs/benchmark/statistical_analysis_plan_v0.4.json"
    )
    reference_sha256 = file_sha256(
        ROOT / "configs/benchmark/reference_portfolio_v0.4.json"
    )
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
        for task_id in tasks:
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
            for method_id in methods:
                for condition in conditions:
                    operation_limit = operation_limits[task_id]
                    spec = FormalCellSpec(
                        run_id=run_id,
                        task_id=task_id,
                        pair_id=pair_id,
                        spectrum_condition=condition,  # type: ignore[arg-type]
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
    per_cell_cost_limit = float(
        resource_contract["monetary_cost_usd_limit_per_cell"]
    )
    manifest = issue_run_manifest(
        cells,
        metadata={
            "matrix_contract": {
                "tasks": list(tasks),
                "methods": list(methods),
                "pair_ids": pair_ids,
                "spectrum_conditions_by_method": {
                    method_id: list(conditions) for method_id in methods
                },
                "checkpoints": [
                    point
                    for point in (1, 2, 4, 8, 12, 20, 40)
                    if point <= complete_experiments
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
                "matrix_monetary_cost_usd_limit": cell_count * per_cell_cost_limit,
            },
            "rl_training_resources": [],
            "development_contract": {
                "schema_version": LIVE_LLM_DEVELOPMENT_VERSION,
                "stage": stage,
                "split": split,
                "seed_count": len(selected_seeds),
                "bench_accessed": False,
                "reference_search_accessed": False,
                "private_reasoning_retained": False,
                "maximum_provider_call_count": sum(
                    cell.operation_limit * provider_attempt_limit for cell in cells
                ),
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
    report_path: str | Path | None = DEFAULT_REPORT_PATH,
    stop_after_new_terminals: int | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run or resume a live Train/Dev matrix; never reads Bench/reference-search."""

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
        adapter_factory=(
            "chemworld.eval.formal_llm:create_formal_live_llm_adapter"
        ),
        python_executable=sys.executable,
        cell_script=str((ROOT / "scripts/run_formal_cell.py").resolve()),
        private_diagnostic_root=str(
            (runtime_root.parent / "private-diagnostics").resolve()
        ),
    )
    outcome = run_formal_matrix(
        plan=plan,
        executor=executor,
        output_root=output_root,
        progress_callback=progress_callback,
        stop_after_new_terminals=stop_after_new_terminals,
    )
    full_scope = stage == "development_matrix" and seeds is None
    report = {
        "schema_version": LIVE_LLM_DEVELOPMENT_VERSION,
        "status": (
            "formal_live_llm_development_ready"
            if full_scope and outcome.report["audit"]["aggregation_ready"] is True
            else outcome.report["status"]
        ),
        "formal_live_llm_development_ready": full_scope
        and outcome.report["audit"]["aggregation_ready"] is True,
        "benchmark_claim_allowed": False,
        "bench_results_present": False,
        "reference_search_results_used": False,
        "private_reasoning_retained": False,
        "stage": stage,
        "source_commit": _git_commit(),
        "method_freeze_audit": audit_live_llm_method_freeze(),
        "manifest_sha256": bundle.manifest["run_manifest_sha256"],
        "cell_count": bundle.cell_count,
        "pair_count": bundle.pair_count,
        "maximum_provider_call_count": bundle.maximum_provider_call_count,
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
    "LiveLLMDevelopmentBundle",
    "build_live_llm_development_bundle",
    "load_live_llm_development_plan",
    "prepare_live_llm_development",
    "run_live_llm_development",
]
