"""Outcome-blind manifest construction for the Work II formal matrix."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256

FORMAL_PREFLIGHT_VERSION = "chemworld-work-ii-formal-matrix-preflight-0.1"
FORMAL_CELL_VERSION = "chemworld-work-ii-formal-cell-0.1"
FORMAL_ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
FORMAL_SNAPSHOT_STAGES = (
    "pre_evidence",
    "after_experiment_1",
    "after_experiment_2",
    "final",
)
FORMAL_CHECKPOINT_EXPERIMENTS = (0, 1, 2, 4)

_SOURCE_PATHS = (
    "src/chemworld/agents/interactive_codex_experiment.py",
    "src/chemworld/agents/experiment_codex_ipc.py",
    "src/chemworld/agents/experiment_codex_mcp.py",
    "src/chemworld/campaign_resources.py",
    "src/chemworld/eval/runner.py",
    "src/chemworld/eval/verify.py",
    "src/chemworld/eval/work_ii_analysis.py",
    "src/chemworld/eval/work_ii_formal.py",
    "src/chemworld/eval/work_ii_prior_discovery.py",
    "scripts/run_work_ii_campaign_pilot.py",
    "scripts/run_work_ii_formal_matrix.py",
    "pyproject.toml",
    "uv.lock",
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _object(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _string_list(value: object, label: str) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ValueError(f"{label} must be a list")
    result = [str(item) for item in value]
    if not result or len(set(result)) != len(result):
        raise ValueError(f"{label} must be a non-empty unique list")
    return result


def build_checkpoint_contract(config: Mapping[str, Any], arm: str) -> dict[str, Any]:
    """Materialize the complete public checkpoint contract used by one cell."""

    if arm not in FORMAL_ARMS:
        raise ValueError(f"unknown prior arm: {arm}")
    nominal = arm != "opaque"
    configured = config.get("belief_checkpoint")
    if isinstance(configured, Mapping):
        held_out_queries = [
            dict(_object(item, "held_out_query"))
            for item in configured["held_out_queries"]
        ]
        metric_ids = _string_list(configured["allowed_metric_ids"], "allowed_metric_ids")
        feature_ids = _string_list(configured["allowed_feature_ids"], "allowed_feature_ids")
        prior_fields = _string_list(configured["allowed_prior_fields"], "allowed_prior_fields")
    else:
        metric_ids = ["selective_product_yield", "energy_efficiency", "safety_risk"]
        feature_ids = [
            "electrolyte_profile",
            "solvent",
            "reagent_amount_mol",
            "potential_V",
            "current_mA",
            "duration_s",
        ]
        prior_fields = ["electrolyte_profile", "solvent"]
        held_out_queries = [
            {
                "query_id": query_id,
                "feature_values": {
                    "electrolyte_profile": electrolyte_profile,
                    "solvent": solvent,
                    "reagent_amount_mol": 0.01,
                    "potential_V": 0.8,
                    "current_mA": 100.0,
                    "duration_s": 1800.0,
                },
                "metric_ids": metric_ids,
            }
            for query_id, electrolyte_profile, solvent in (
                ("q-low", 0, 0),
                ("q-electrolyte", 3, 0),
                ("q-solvent", 0, 3),
                ("q-high", 3, 3),
            )
        ]
    query_metric_contract = {
        str(item["query_id"]): [str(metric) for metric in item.get("metric_ids", metric_ids)]
        for item in held_out_queries
    }
    complete_experiments = int(_object(config["campaign"], "campaign")["complete_experiments"])
    snapshot_stages = [
        str(item)
        for item in config.get(
            "snapshot_stages",
            ["pre_evidence", "post_neutral", "post_discriminating", "final"],
        )
    ]
    if len(snapshot_stages) != 4 or len(set(snapshot_stages)) != 4:
        raise ValueError("snapshot_stages must contain four unique stage IDs")
    checkpoint_experiments = [
        int(item)
        for item in _object(config["campaign"], "campaign")[
            "checkpoint_complete_experiments"
        ]
    ]
    return {
        "schema_version": "chemworld-work-ii-campaign-checkpoint-contract-0.1",
        "snapshot_stages": snapshot_stages,
        "checkpoint_complete_experiments": checkpoint_experiments,
        "query_metric_contract": query_metric_contract,
        "held_out_queries": held_out_queries,
        "allowed_feature_ids": feature_ids,
        "allowed_metric_ids": metric_ids,
        "allowed_prior_fields": prior_fields,
        "evidence_catalog": [
            f"experiment-{index}-final-assay"
            for index in range(1, complete_experiments + 1)
        ],
        "nominal_information_available": nominal,
        "stage_labels_are_checkpoint_ids_only": True,
        "physical_experiment_selection_authority": "participant",
    }


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"formal binding is outside the repository: {path}") from error


def _binding(root: Path, relative_path: str) -> dict[str, str]:
    path = root / relative_path
    if not path.is_file():
        raise ValueError(f"missing formal dependency: {relative_path}")
    return {"path": relative_path, "sha256": file_sha256(path)}


def _self_hash(payload: Mapping[str, Any]) -> str:
    return canonical_json_sha256(
        {key: value for key, value in payload.items() if key != "preflight_sha256"}
    )


def build_formal_preflight(
    root: Path,
    design_path: Path,
    analysis_path: Path,
) -> dict[str, Any]:
    """Build the deterministic 75-cell public schedule without provider execution."""

    root = root.resolve()
    design_path = design_path.resolve()
    analysis_path = analysis_path.resolve()
    design = _load_object(design_path)
    analysis = _load_object(analysis_path)
    errors: list[str] = []

    design_digest = canonical_json_sha256(design)
    analysis_digest = canonical_json_sha256(analysis)
    analysis_binding = _object(analysis.get("design_binding"), "analysis.design_binding")
    if analysis_binding.get("sha256") != design_digest:
        errors.append("analysis plan does not bind the current formal design")
    arms = tuple(_string_list(design.get("prior_arms"), "design.prior_arms"))
    if arms != FORMAL_ARMS:
        errors.append("formal prior-arm order differs from the frozen three-arm contract")
    population = _object(analysis.get("analysis_population"), "analysis_population")
    if tuple(population.get("prior_arms", [])) != FORMAL_ARMS:
        errors.append("analysis population prior arms differ from the formal design")

    world_cohort = _object(design.get("world_cohort"), "world_cohort")
    public = _object(world_cohort.get("public_formal"), "world_cohort.public_formal")
    task_world_seeds = _object(public.get("task_world_seeds"), "task_world_seeds")
    raw_tasks = design.get("tasks")
    if isinstance(raw_tasks, (str, bytes)) or not isinstance(raw_tasks, Sequence):
        raise ValueError("design.tasks must be a list")
    tasks = [dict(_object(item, "design task")) for item in raw_tasks]
    if len(tasks) != 5:
        errors.append("formal design must contain exactly five tasks")

    cells: list[dict[str, Any]] = []
    task_bindings: list[dict[str, Any]] = []
    provider_contract: dict[str, Any] | None = None
    total_query_count = 0
    total_query_metric_count = 0
    for task_index, task in enumerate(tasks, start=1):
        task_id = str(task.get("task_id"))
        relative_config = str(task.get("campaign_config"))
        config_path = root / relative_config
        config = _load_object(config_path)
        if config.get("task_id") != task_id:
            errors.append(f"{task_id}: campaign task identity mismatch")
        if tuple(config.get("prior_arms", {})) != FORMAL_ARMS:
            errors.append(f"{task_id}: campaign prior-arm order mismatch")
        opaque_contract = build_checkpoint_contract(config, "opaque")
        aligned_contract = build_checkpoint_contract(config, "aligned_nominal")
        misindexed_contract = build_checkpoint_contract(config, "misindexed_nominal")
        if aligned_contract != misindexed_contract:
            errors.append(f"{task_id}: informed checkpoint contracts are not matched")
        if tuple(opaque_contract["snapshot_stages"]) != FORMAL_SNAPSHOT_STAGES:
            errors.append(f"{task_id}: checkpoint stage IDs are not the neutral formal IDs")
        if (
            tuple(opaque_contract["checkpoint_complete_experiments"])
            != FORMAL_CHECKPOINT_EXPERIMENTS
        ):
            errors.append(f"{task_id}: checkpoint experiment schedule differs from formal design")
        if int(_object(config["campaign"], "campaign")["complete_experiments"]) != 4:
            errors.append(f"{task_id}: formal campaign must contain four experiments")
        provider = dict(_object(config.get("provider"), f"{task_id}.provider"))
        reduced_provider = {
            key: provider.get(key)
            for key in ("id", "name", "base_url", "wire_api", "model", "reasoning_effort")
        }
        if provider_contract is None:
            provider_contract = reduced_provider
        elif provider_contract != reduced_provider:
            errors.append(f"{task_id}: provider/model/scaffold axis drift")
        seeds = [int(item) for item in task_world_seeds.get(task_id, [])]
        if len(seeds) != 5 or len(set(seeds)) != 5:
            errors.append(f"{task_id}: public world schedule must contain five unique seeds")
        config_binding = _binding(root, relative_config)
        checkpoint_digest = canonical_json_sha256(opaque_contract)
        query_count = len(opaque_contract["query_metric_contract"])
        query_metric_count = sum(
            len(metric_ids)
            for metric_ids in opaque_contract["query_metric_contract"].values()
        )
        task_bindings.append(
            {
                "task_id": task_id,
                "campaign_config": config_binding,
                "checkpoint_contract_sha256": checkpoint_digest,
                "held_out_query_count_per_snapshot": query_count,
                "held_out_query_metric_count_per_snapshot": query_metric_count,
            }
        )
        for world_index, world_seed in enumerate(seeds, start=1):
            cluster_id = f"work-ii-public-{task_index:02d}-{world_index:02d}"
            for arm_index, arm in enumerate(FORMAL_ARMS, start=1):
                cell_id = f"{cluster_id}-arm-{arm_index:02d}"
                checkpoint = build_checkpoint_contract(config, arm)
                cell = {
                    "schema_version": FORMAL_CELL_VERSION,
                    "schedule_index": len(cells) + 1,
                    "cell_id": cell_id,
                    "world_cluster_id": cluster_id,
                    "task_id": task_id,
                    "world_index": world_index,
                    "world_seed": world_seed,
                    "prior_arm": arm,
                    "campaign_config_path": relative_config,
                    "campaign_config_sha256": config_binding["sha256"],
                    "checkpoint_contract_sha256": canonical_json_sha256(checkpoint),
                    "complete_experiment_count": 4,
                    "belief_checkpoint_count": 4,
                    "held_out_query_count_per_snapshot": query_count,
                    "held_out_query_metric_count_per_snapshot": query_metric_count,
                    "provider_session_limit": 1,
                    "provider_repeat": 1,
                    "terminal_states": ["completed", "right_censored", "failed"],
                }
                cell["cell_key_sha256"] = canonical_json_sha256(cell)
                cells.append(cell)
                total_query_count += query_count * 4
                total_query_metric_count += query_metric_count * 4

    cell_ids = [str(cell["cell_id"]) for cell in cells]
    cell_keys = [str(cell["cell_key_sha256"]) for cell in cells]
    cluster_ids = {str(cell["world_cluster_id"]) for cell in cells}
    if len(cells) != 75 or len(set(cell_ids)) != 75 or len(set(cell_keys)) != 75:
        errors.append("formal schedule does not contain 75 unique cells")
    if len(cluster_ids) != 25:
        errors.append("formal schedule does not contain 25 independent world clusters")
    if int(population.get("scheduled_public_cells", -1)) != len(cells):
        errors.append("analysis cell denominator differs from the generated schedule")
    if int(population.get("independent_task_world_clusters", -1)) != len(cluster_ids):
        errors.append("analysis cluster denominator differs from the generated schedule")

    source_bindings = [_binding(root, path) for path in _SOURCE_PATHS]
    blockers = [
        "blind evaluator and final-recommendation denominator are not yet frozen",
        "persistent-session provider-attempt cap is not yet frozen",
        "formal currency ceiling is not yet approved",
        "current design and analysis plan explicitly forbid formal execution",
        "current persistent-session method lacks its final qualification receipt",
    ]
    if (
        design.get("formal_execution_allowed") is True
        or analysis.get("formal_execution_allowed") is True
    ):
        errors.append("pre-registration inputs unexpectedly allow formal execution")
    report: dict[str, Any] = {
        "schema_version": FORMAL_PREFLIGHT_VERSION,
        "status": "failed" if errors else "passed_execution_blocked",
        "formal_result": False,
        "formal_execution_allowed": False,
        "design_binding": {
            "path": _relative(root, design_path),
            "sha256": design_digest,
        },
        "analysis_binding": {
            "path": _relative(root, analysis_path),
            "sha256": analysis_digest,
        },
        "provider_contract": provider_contract,
        "schedule_policy": {
            "order": "task_then_public_world_then_prior_arm",
            "same_world_arm_triplet_max_concurrency": 3,
            "within_cell_concurrency": 1,
            "one_persistent_session_per_cell": True,
            "missing_only_resume": True,
            "accepted_terminal_cells_are_immutable": True,
            "result_direction_early_stopping_forbidden": True,
        },
        "prompt_boundary": {
            "world_seed_exposed_to_participant": False,
            "world_cluster_id_exposed_to_participant": False,
            "prior_arm_label_exposed_to_participant": False,
            "private_identity_exposed_to_participant_or_manifest": False,
            "evaluator_truth_exposed_to_participant": False,
        },
        "expected_counts": {
            "tasks": len(tasks),
            "independent_task_world_clusters": len(cluster_ids),
            "participant_cells": len(cells),
            "provider_sessions": len(cells),
            "provider_repeats_per_cell": 1,
            "complete_experiments": len(cells) * 4,
            "belief_checkpoints": len(cells) * 4,
            "checkpoint_held_out_queries": total_query_count,
            "checkpoint_held_out_query_metrics": total_query_metric_count,
            "blind_final_recommendations": None,
        },
        "task_bindings": task_bindings,
        "source_bindings": source_bindings,
        "cells": cells,
        "blocking_requirements": blockers,
        "errors": errors,
    }
    report["preflight_sha256"] = _self_hash(report)
    return report


def validate_formal_preflight(report: Mapping[str, Any]) -> list[str]:
    """Validate self-hash, schedule uniqueness, and outcome-blind boundaries."""

    errors: list[str] = []
    if report.get("schema_version") != FORMAL_PREFLIGHT_VERSION:
        errors.append("unexpected formal preflight schema")
    if report.get("preflight_sha256") != _self_hash(report):
        errors.append("formal preflight self-hash mismatch")
    cells = report.get("cells")
    if not isinstance(cells, list):
        errors.append("formal preflight cells are missing")
        return errors
    ids = [cell.get("cell_id") for cell in cells if isinstance(cell, Mapping)]
    keys = [cell.get("cell_key_sha256") for cell in cells if isinstance(cell, Mapping)]
    if len(cells) != 75 or len(set(ids)) != 75 or len(set(keys)) != 75:
        errors.append("formal preflight must contain 75 unique cell identities")
    counts = report.get("expected_counts")
    if not isinstance(counts, Mapping) or counts.get("participant_cells") != len(cells):
        errors.append("formal preflight cell count is inconsistent")
    prompt = report.get("prompt_boundary")
    if not isinstance(prompt, Mapping) or any(
        prompt.get(key) is not False
        for key in (
            "world_seed_exposed_to_participant",
            "world_cluster_id_exposed_to_participant",
            "prior_arm_label_exposed_to_participant",
            "private_identity_exposed_to_participant_or_manifest",
            "evaluator_truth_exposed_to_participant",
        )
    ):
        errors.append("formal preflight prompt boundary is not fail-closed")
    if report.get("formal_result") is not False:
        errors.append("a preflight cannot be a formal result")
    return errors


__all__ = [
    "FORMAL_ARMS",
    "FORMAL_CELL_VERSION",
    "FORMAL_CHECKPOINT_EXPERIMENTS",
    "FORMAL_PREFLIGHT_VERSION",
    "FORMAL_SNAPSHOT_STAGES",
    "build_checkpoint_contract",
    "build_formal_preflight",
    "validate_formal_preflight",
]
