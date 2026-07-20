"""Independent reference portfolio plan for the sealed v0.5 Bench cohort."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PORTFOLIO_PATH = configuration_root() / "benchmark" / "reference_portfolio_v0.4.json"
DEFAULT_REGRET_PATH = configuration_root() / "benchmark" / "reference_regret_v0.4.json"
PORTFOLIO_VERSION = "chemworld-reference-portfolio-plan-0.4"
REGRET_VERSION = "chemworld-reference-regret-protocol-0.4"
CORE_TASKS = (
    "partition-discovery",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "flow-reaction-optimization",
)
METRICS = ("task_primary", "task_score")
SOURCE_PROFILES = (
    "global_space_filling",
    "ensemble_surrogate",
    "evolutionary_search",
    "risk_aware_global",
)
EXPECTED_METHODS = (
    "random",
    "lhs",
    "greedy_local",
    "structured_gp_ei",
    "structured_gp_pi",
    "structured_gp_ucb",
    "structured_rf_ei",
    "structured_safe_gp_ei",
    "operation_random",
    "observation_blind",
    "rule_based",
    "ppo",
    "sac",
    "live_llm_a",
    "live_llm_b",
)


class ReferencePlanError(RuntimeError):
    """Raised when reference planning could contaminate or under-cover Bench."""


def load_reference_portfolio_v0_4(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_PORTFOLIO_PATH if path is None else path
    payload = _read_object(resolved)
    if payload.get("schema_version") != PORTFOLIO_VERSION:
        raise ReferencePlanError("unsupported reference portfolio plan")
    return payload


def load_reference_regret_v0_4(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_REGRET_PATH if path is None else path
    payload = _read_object(resolved)
    if payload.get("schema_version") != REGRET_VERSION:
        raise ReferencePlanError("unsupported reference regret protocol")
    return payload


def build_reference_run_plan(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Enumerate source runs using opaque pair indices, never private Bench seeds."""

    _validate_portfolio_shape(plan)
    target = plan["target_grid"]
    namespace = plan["reference_search_namespace"]
    run_config = plan["run_plan"]
    pair_count = int(target["private_bench_pair_count"])
    base_start = int(namespace["public_base_seed_range"]["start"])
    budget = int(run_config["complete_experiments_per_source_run"])
    sources = tuple(str(item["source_id"]) for item in plan["source_profiles"])
    runs: list[dict[str, Any]] = []
    for task_id in target["formal_core_tasks"]:
        operation_count = int(run_config["task_recipe_operation_counts"][task_id]) * budget
        for pair_index in range(pair_count):
            for source_id in sources:
                identity = (
                    f"{plan['plan_id']}|{task_id}|pair-{pair_index:03d}|{source_id}"
                )
                runs.append(
                    {
                        "run_id": hashlib.sha256(identity.encode("utf-8")).hexdigest(),
                        "task_id": str(task_id),
                        "opaque_pair_index": pair_index,
                        "target_binding": "private_bench_manifest_lookup_only",
                        "source_id": source_id,
                        "builder_id": plan["builder_contract"]["builder_id"],
                        "reference_search_base_seed": base_start + pair_index,
                        "builder_seed": _derived_builder_seed(
                            str(namespace["namespace_id"]),
                            str(task_id),
                            pair_index,
                            source_id,
                        ),
                        "complete_experiment_budget": budget,
                        "maximum_operation_count": operation_count,
                    }
                )
    return runs


def signed_regret(reference_estimate: float, method_value: float) -> float:
    reference = _finite(reference_estimate, "reference_estimate")
    method = _finite(method_value, "method_value")
    return reference - method


def audit_reference_plan(
    plan: Mapping[str, Any],
    regret: Mapping[str, Any],
    *,
    workspace: Path = ROOT,
) -> dict[str, Any]:
    controls: dict[str, bool] = {}
    try:
        runs = build_reference_run_plan(plan)
        shape_valid = True
    except (KeyError, TypeError, ValueError, ReferencePlanError):
        runs = []
        shape_valid = False
    controls["plans_are_frozen_nonclaiming_and_result_free"] = (
        shape_valid
        and plan.get("schema_version") == PORTFOLIO_VERSION
        and plan.get("status") == "frozen_plan_evidence_not_generated"
        and plan.get("formal_results_present") is False
        and plan.get("benchmark_claim_allowed") is False
        and regret.get("schema_version") == REGRET_VERSION
        and regret.get("status") == "frozen_controls_reference_evidence_pending"
        and regret.get("formal_results_present") is False
        and regret.get("benchmark_claim_allowed") is False
    )
    controls["formal_and_statistical_parents_are_hash_bound"] = _parents_ready(
        plan.get("parent_bindings"), workspace
    )
    controls["backend_evaluator_and_replay_are_exact"] = _backend_ready(
        plan.get("backend_binding"), workspace
    )
    controls["target_grid_binds_private_core4_without_seed_exposure"] = _target_ready(
        plan.get("target_grid"), workspace
    )
    controls["reference_builder_identity_code_and_rng_are_independent"] = (
        _builder_ready(plan.get("builder_contract"))
    )
    controls["reference_search_namespace_is_new_and_disjoint"] = _namespace_ready(
        plan.get("reference_search_namespace"), workspace
    )
    controls["four_source_profiles_are_unique_and_independent"] = _sources_ready(
        plan.get("source_profiles")
    )

    run_ids = [str(row["run_id"]) for row in runs]
    builder_seeds = [int(row["builder_seed"]) for row in runs]
    source_counts = Counter(
        (str(row["task_id"]), int(row["opaque_pair_index"])) for row in runs
    )
    controls["exact_run_grid_is_unique_and_has_four_sources_per_target"] = (
        len(runs) == 1_600
        and len(set(run_ids)) == len(runs)
        and len(set(builder_seeds)) == len(runs)
        and len(source_counts) == 400
        and set(source_counts.values()) == {4}
    )
    controls["resource_plan_matches_executable_task_recipes"] = _resource_plan_ready(
        plan.get("run_plan"), runs
    )
    controls["evidence_requires_four_replayed_accounted_sources_before_scoring"] = (
        _evidence_contract_ready(plan.get("evidence_contract"))
    )
    controls["reference_is_best_known_not_oracle_and_may_be_exceeded"] = (
        _reference_semantics_ready(plan.get("reference_semantics"))
    )
    controls["regret_protocol_matches_portfolio_and_preserves_negative_regret"] = (
        _regret_ready(plan, regret)
    )
    controls["reference_is_frozen_before_any_method_bench_scoring"] = (
        tuple(plan.get("execution_order", ()))
        == (
            "freeze_reference_builder_code_and_source_profiles",
            "preflight_private_target_bindings_without_printing_seed_values",
            "run_and_replay_verify_all_1600_source_runs",
            "freeze_all_800_reference_cells_and_uncertainty_intervals",
            "only_then_start_evaluated_method_bench_scoring",
        )
    )
    probes = _adversarial_probes(plan, regret)
    controls["adversarial_plan_probes_fail_closed"] = all(probes.values())
    controls_ready = all(controls.values())
    commit, dirty = _git_provenance(workspace)
    run_config = plan.get("run_plan", {})
    target = plan.get("target_grid", {})
    return {
        "schema_version": "chemworld-reference-plan-audit-0.4",
        "plan_id": plan.get("plan_id"),
        "regret_protocol_id": regret.get("protocol_id"),
        "status": "reference_plan_frozen_evidence_not_generated"
        if controls_ready
        else "reference_plan_controls_failed",
        "controls_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": commit,
        "source_tree_dirty": dirty,
        "portfolio_plan_sha256": _canonical_sha256(plan),
        "regret_protocol_sha256": _canonical_sha256(regret),
        "run_plan_sha256": _canonical_sha256({"runs": runs}),
        "run_counts": {
            "private_pair_count": target.get("private_bench_pair_count")
            if isinstance(target, Mapping)
            else None,
            "reference_cell_count": target.get("expected_reference_cell_count")
            if isinstance(target, Mapping)
            else None,
            "source_run_count": len(runs),
            "source_metric_record_count": run_config.get(
                "planned_source_metric_record_count"
            )
            if isinstance(run_config, Mapping)
            else None,
            "complete_experiment_count": run_config.get(
                "planned_complete_experiment_count"
            )
            if isinstance(run_config, Mapping)
            else None,
            "maximum_operation_count": sum(
                int(row["maximum_operation_count"]) for row in runs
            ),
        },
        "source_profiles": list(SOURCE_PROFILES),
        "minimum_sources_per_task_pair_metric": 4,
        "private_seed_values_reported": False,
        "private_world_parameters_reported": False,
        "reference_semantics": plan.get("reference_semantics", {}),
        "adversarial_probes": probes,
        "controls": controls,
        "limitations": [
            "This is an exact run plan; no reference source run or estimate exists yet.",
            "Best-known references are empirical achieved values, not hidden-state optima.",
            "The 800 cells must be frozen before any evaluated method receives a Bench score.",
        ],
        "next_gates": [
            "implement and hash the dedicated reference builder",
            "bind private target identities through formal preflight without printing them",
            "execute all 1,600 runs after method freeze and before method Bench scoring",
        ],
    }


def _validate_portfolio_shape(plan: Mapping[str, Any]) -> None:
    if plan.get("schema_version") != PORTFOLIO_VERSION:
        raise ReferencePlanError("unsupported portfolio schema")
    if plan.get("formal_results_present") is not False or plan.get(
        "benchmark_claim_allowed"
    ) is not False:
        raise ReferencePlanError("reference plan must remain nonclaiming")
    target = plan.get("target_grid")
    if not isinstance(target, Mapping):
        raise ReferencePlanError("target grid is required")
    if tuple(target.get("formal_core_tasks", ())) != CORE_TASKS:
        raise ReferencePlanError("reference task scope drifted")
    if int(target.get("private_bench_pair_count", 0)) != 100:
        raise ReferencePlanError("reference target requires 100 private pairs")
    if tuple(target.get("metrics", ())) != METRICS:
        raise ReferencePlanError("reference metrics drifted")
    sources = plan.get("source_profiles")
    if not isinstance(sources, list | tuple):
        raise ReferencePlanError("source profiles must be a list")
    source_ids = [
        str(item.get("source_id", "")) if isinstance(item, Mapping) else ""
        for item in sources
    ]
    if tuple(source_ids) != SOURCE_PROFILES or len(set(source_ids)) != 4:
        raise ReferencePlanError("exactly four independent source profiles are required")


def _parents_ready(raw: Any, workspace: Path) -> bool:
    if not isinstance(raw, Mapping) or set(raw) != {
        "formal_protocol",
        "statistical_plan",
        "statistical_plan_report",
    }:
        return False
    loaded: dict[str, dict[str, Any]] = {}
    for name, binding in raw.items():
        if not isinstance(binding, Mapping):
            return False
        path = _resolve_workspace_path(workspace, binding.get("path"))
        if path is None or not path.is_file() or _file_sha256(path) != binding.get(
            "file_sha256"
        ):
            return False
        loaded[str(name)] = _read_object(path)
    return (
        _canonical_sha256(loaded["formal_protocol"])
        == raw["formal_protocol"].get("protocol_sha256")
        and _canonical_sha256(loaded["statistical_plan"])
        == raw["statistical_plan"].get("protocol_sha256")
        and loaded["statistical_plan_report"].get("controls_ready") is True
        and loaded["statistical_plan_report"].get("protocol_sha256")
        == raw["statistical_plan"].get("protocol_sha256")
    )


def _backend_ready(raw: Any, workspace: Path) -> bool:
    if not isinstance(raw, Mapping):
        return False
    formal = _read_object(workspace / "configs" / "benchmark" / "formal_protocol_v0.4.json")
    binding = formal["backend_binding"]
    return (
        raw.get("release_manifest_id") == binding["release_manifest_id"]
        and raw.get("backend_semantic_sha256") == binding["backend_semantic_sha256"]
        and raw.get("evaluation_contract_version")
        == binding["evaluation_contract_version"]
        and raw.get("result_schema_version") == binding["result_schema_version"]
        and raw.get("score_replay_binding_version")
        == binding["score_replay_binding_version"]
    )


def _target_ready(raw: Any, workspace: Path) -> bool:
    if not isinstance(raw, Mapping):
        return False
    formal = _read_object(workspace / "configs" / "benchmark" / "formal_protocol_v0.4.json")
    commitment = formal["private_bench_manifest"]["commitment_sha256"]
    return (
        tuple(raw.get("formal_core_tasks", ())) == CORE_TASKS
        and raw.get("private_bench_pair_count") == 100
        and raw.get("private_bench_commitment_sha256") == commitment
        and raw.get("target_world")
        == "same_private_bench_task_pair_world_cell_as_evaluated_methods"
        and raw.get("target_seed_values") == "private_formal_manifest_only"
        and tuple(raw.get("metrics", ())) == METRICS
        and raw.get("expected_reference_cell_count") == 800
        and not any(
            isinstance(value, (int, float))
            for key, value in raw.items()
            if "seed" in str(key).lower()
        )
    )


def _builder_ready(raw: Any) -> bool:
    if not isinstance(raw, Mapping):
        return False
    evaluated = tuple(str(item) for item in raw.get("evaluated_method_ids", ()))
    builder = str(raw.get("builder_id", ""))
    return (
        builder == "independent_reference_portfolio_v0_4"
        and evaluated == EXPECTED_METHODS
        and builder not in set(evaluated)
        and raw.get("implementation_namespace") == "chemworld.reference.builders.v0_4"
        and raw.get("may_import_evaluated_agent_implementations") is False
        and raw.get("hidden_state_access") is False
        and raw.get("builder_identity_must_not_equal_evaluated_method") is True
        and raw.get("builder_code_digest_must_not_equal_evaluated_adapter_digest") is True
        and raw.get("reference_trajectory_must_not_equal_method_trajectory") is True
        and raw.get("training_search_and_evaluation_rng_streams_disjoint") is True
    )


def _namespace_ready(raw: Any, workspace: Path) -> bool:
    if not isinstance(raw, Mapping):
        return False
    formal = _read_object(workspace / "configs" / "benchmark" / "formal_protocol_v0.4.json")
    expected = formal["split_contract"]["reference_search"]
    seed_range = raw.get("public_base_seed_range", {})
    return (
        raw.get("namespace_id") == expected["namespace_id"]
        and isinstance(seed_range, Mapping)
        and seed_range == expected["base_seeds"]
        and raw.get("base_seed_count") == 100
        and raw.get("bench_seed_is_never_used_as_builder_rng") is True
    )


def _sources_ready(raw: Any) -> bool:
    if not _is_sequence(raw):
        return False
    ids: list[str] = []
    for item in raw:
        if not isinstance(item, Mapping):
            return False
        ids.append(str(item.get("source_id", "")))
        if not str(item.get("algorithm_role", "")).strip() or item.get(
            "independent_rng_stream"
        ) is not True:
            return False
    return tuple(ids) == SOURCE_PROFILES and len(set(ids)) == 4


def _resource_plan_ready(raw: Any, runs: Sequence[Mapping[str, Any]]) -> bool:
    if not isinstance(raw, Mapping) or len(runs) != 1_600:
        return False
    expected_events = {
        task_id: task_recipe_event_count(get_task(task_id).to_dict()) for task_id in CORE_TASKS
    }
    actual_operations = sum(int(row["maximum_operation_count"]) for row in runs)
    expected_operations = sum(
        expected_events[str(row["task_id"])]
        * int(row["complete_experiment_budget"])
        for row in runs
    )
    return (
        raw.get("complete_experiments_per_source_run") == 40
        and raw.get("source_runs_per_task_pair") == 4
        and raw.get("minimum_independent_sources_per_task_pair_metric") == 4
        and raw.get("planned_source_run_count") == 1_600
        and raw.get("planned_complete_experiment_count") == 64_000
        and raw.get("planned_source_metric_record_count") == 3_200
        and raw.get("task_recipe_operation_counts") == expected_events
        and raw.get("planned_maximum_operation_count")
        == actual_operations
        == expected_operations
        and raw.get("planned_wall_time_upper_bound_s_serial")
        == 1_600 * float(raw.get("maximum_wall_time_s_per_source_run", math.nan))
    )


def _evidence_contract_ready(raw: Any) -> bool:
    return (
        isinstance(raw, Mapping)
        and raw.get("every_source_run_replay_verified") is True
        and raw.get("every_source_run_resource_accounting_complete") is True
        and raw.get("exact_result_and_trajectory_digests_required") is True
        and raw.get("missing_or_failed_source_run")
        == "reference_cell_incomplete_no_method_scoring"
        and raw.get("duplicate_source_run") == "reject_manifest"
        and raw.get("source_count_below_four") == "reference_cell_incomplete"
        and raw.get("freeze_complete_manifest_before_any_evaluated_method_bench_score")
        is True
        and raw.get("formal_reference_results_present_now") is False
    )


def _reference_semantics_ready(raw: Any) -> bool:
    return (
        isinstance(raw, Mapping)
        and raw.get("kind") == "independent_best_known_estimate"
        and raw.get("is_oracle") is False
        and raw.get("evaluated_method_may_exceed_reference") is True
        and raw.get("negative_regret_preserved_and_reported") is True
        and raw.get("reference_is_not_ground_truth") is True
        and raw.get("update_rule")
        == "new_protocol_version_new_reference_manifest_and_recompute_every_method"
    )


def _regret_ready(plan: Mapping[str, Any], regret: Mapping[str, Any]) -> bool:
    semantics = regret.get("reference_semantics", {})
    coverage = regret.get("coverage_policy", {})
    independence = regret.get("independence_policy", {})
    reporting = regret.get("reporting", {})
    return (
        regret.get("portfolio_plan_id") == plan.get("plan_id")
        and tuple(regret.get("formal_core_tasks", ())) == CORE_TASKS
        and regret.get("private_pair_count") == 100
        and tuple(regret.get("metrics", {})) == METRICS
        and isinstance(semantics, Mapping)
        and semantics.get("is_oracle") is False
        and semantics.get("may_be_exceeded_by_evaluated_methods") is True
        and semantics.get("signed_regret") == "reference_estimate_minus_method_value"
        and semantics.get("negative_regret_policy") == "preserve_and_report"
        and isinstance(coverage, Mapping)
        and coverage.get("expected_reference_cell_count") == 800
        and coverage.get("minimum_independent_source_count_per_cell") == 4
        and isinstance(independence, Mapping)
        and independence.get("builder_id") == plan["builder_contract"]["builder_id"]
        and independence.get("reference_frozen_before_method_scoring") is True
        and independence.get("evaluated_methods_receive_no_reference_value_during_episode")
        is True
        and isinstance(reporting, Mapping)
        and reporting.get("cross_task_regret_scalar") is None
    )


def _adversarial_probes(
    plan: Mapping[str, Any], regret: Mapping[str, Any]
) -> dict[str, bool]:
    probes: dict[str, bool] = {}
    overlap = json.loads(json.dumps(plan))
    overlap["builder_contract"]["builder_id"] = "random"
    probes["builder_method_overlap_rejected"] = not _builder_ready(
        overlap["builder_contract"]
    )
    duplicate_source = json.loads(json.dumps(plan))
    duplicate_source["source_profiles"][1]["source_id"] = duplicate_source[
        "source_profiles"
    ][0]["source_id"]
    try:
        build_reference_run_plan(duplicate_source)
    except ReferencePlanError:
        probes["duplicate_source_profile_rejected"] = True
    else:
        probes["duplicate_source_profile_rejected"] = False
    oracle = json.loads(json.dumps(plan))
    oracle["reference_semantics"]["is_oracle"] = True
    probes["oracle_semantics_rejected"] = not _reference_semantics_ready(
        oracle["reference_semantics"]
    )
    too_few = json.loads(json.dumps(plan))
    too_few["evidence_contract"]["source_count_below_four"] = "accept_three"
    probes["source_count_below_four_rejected"] = not _evidence_contract_ready(
        too_few["evidence_contract"]
    )
    changed_regret = json.loads(json.dumps(regret))
    changed_regret["reference_semantics"]["negative_regret_policy"] = "clip_to_zero"
    probes["negative_regret_clipping_rejected"] = not _regret_ready(plan, changed_regret)
    return probes


def _derived_builder_seed(
    namespace: str, task_id: str, pair_index: int, source_id: str
) -> int:
    material = f"{namespace}|{task_id}|{pair_index}|{source_id}".encode()
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big") & ((1 << 63) - 1)


def _finite(value: Any, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ReferencePlanError(f"{label} must be finite") from exc
    if not math.isfinite(result):
        raise ReferencePlanError(f"{label} must be finite")
    return result


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _resolve_workspace_path(workspace: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip() or Path(raw).is_absolute():
        return None
    resolved = (workspace / raw).resolve()
    try:
        resolved.relative_to(workspace.resolve())
    except ValueError:
        return None
    return resolved


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReferencePlanError("JSON object required")
    return payload


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_provenance(workspace: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=workspace,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


__all__ = [
    "ReferencePlanError",
    "audit_reference_plan",
    "build_reference_run_plan",
    "load_reference_portfolio_v0_4",
    "load_reference_regret_v0_4",
    "signed_regret",
]
