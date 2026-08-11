#!/usr/bin/env python3
"""Qualify and materialize the Work II parametric initial-model pilot."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import (
    _FrozenTruthReplayAgent,
    compile_evaluator_truth_query,
)
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
BASE_CONFIG = ROOT / "configs/benchmark/work_ii_campaign_pilot.json"
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-parametric-initial-model-diagnostic-20260811"
)
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-parametric-initial-model-diagnostic-20260811.json"
)
DEFAULT_CONFIG_OUTPUT = (
    ROOT
    / "configs/benchmark/"
    "work_ii_electrochemical_parametric_initial_model_pilot.json"
)
POTENTIALS = (0.68, 0.82, 0.96, 1.10, 1.24)
CURRENTS = (25.0, 45.0, 65.0, 85.0)
REFERENCE_CONTEXT = {
    "electrolyte_profile": 0,
    "solvent": 0,
    "reagent_amount_mol": 0.01,
    "duration_s": 1800.0,
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _query(potential: float, current: float) -> dict[str, Any]:
    return {
        "query_id": f"p{potential:.2f}-i{current:.0f}",
        "feature_values": {
            **REFERENCE_CONTEXT,
            "potential_V": potential,
            "current_mA": current,
        },
        "metric_ids": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score",
        ],
    }


def _final_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    rows = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(rows) != 1:
        raise ValueError("diagnostic recipe must contain exactly one final assay")
    row = rows[0]
    observation = row.get("observation")
    if not isinstance(observation, dict):
        raise ValueError("diagnostic final assay lacks its observation")
    metrics: dict[str, float] = {}
    for metric in _query(0.68, 25.0)["metric_ids"]:
        value = row.get("leaderboard_score") if metric == "score" else observation.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"diagnostic metric is unavailable: {metric}")
        metrics[metric] = float(value)
    return metrics


def _public_initial_model(
    *,
    potential: float | None,
    current: float | None,
) -> dict[str, Any]:
    if potential is None or current is None:
        return {
            "schema_version": "chemworld-work-ii-initial-world-model-0.1",
            "locus": "parametric",
            "availability": "opaque_for_target_locus",
            "model": None,
            "interpretation": (
                "No task-specific potential/current operating-window claim is supplied. "
                "Experimental evidence is authoritative."
            ),
        }
    return {
        "schema_version": "chemworld-work-ii-initial-world-model-0.1",
        "locus": "parametric",
        "availability": "supplied_incomplete_model",
        "model": {
            "reference_context": dict(REFERENCE_CONTEXT),
            "claim": {
                "potential_window_V": [round(potential - 0.07, 2), round(potential + 0.07, 2)],
                "current_window_mA": [current - 10.0, current + 10.0],
                "expected_relation": (
                    "At the stated reference context, balanced performance is more likely "
                    "inside than outside this approximate operating window."
                ),
            },
            "confidence": 0.70,
            "scope_limit": (
                "This is an incomplete local process model, not ground truth and not a "
                "material-property claim."
            ),
        },
        "interpretation": (
            "The supplied model may be reliable or shifted. Experimental evidence is authoritative."
        ),
    }


def _pilot_config(
    base: dict[str, Any],
    *,
    aligned: tuple[float, float],
    misspecified: tuple[float, float],
    world_seed: int,
) -> dict[str, Any]:
    config = deepcopy(base)
    config.update(
        {
            "schema_version": "chemworld-work-ii-campaign-pilot-0.3",
            "pilot_id": "work-ii-electrochemical-parametric-initial-model-pilot",
            "formal_result": False,
            "world_seed": world_seed,
            "observation_noise_namespace": (
                "work-ii-electrochemical-parametric-initial-model-pilot"
            ),
            "intervention": {
                "locus": "parametric",
                "target": "potential_current_operating_window",
                "material_information_matched_opaque": True,
                "world_and_resource_contract_matched": True,
                "diagnostic_reference_context": dict(REFERENCE_CONTEXT),
                "diagnostic_grid": {
                    "potential_V": list(POTENTIALS),
                    "current_mA": list(CURRENTS),
                },
            },
            "prior_arms": {
                "opaque": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _public_initial_model(
                        potential=None,
                        current=None,
                    ),
                },
                "aligned_nominal": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _public_initial_model(
                        potential=aligned[0],
                        current=aligned[1],
                    ),
                },
                "misindexed_nominal": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _public_initial_model(
                        potential=misspecified[0],
                        current=misspecified[1],
                    ),
                },
            },
            "belief_checkpoint": {
                "allowed_feature_ids": [
                    "electrolyte_profile",
                    "solvent",
                    "reagent_amount_mol",
                    "potential_V",
                    "current_mA",
                    "duration_s",
                ],
                "allowed_metric_ids": [
                    "selective_product_yield",
                    "electrochemical_selectivity",
                    "faradaic_efficiency",
                    "energy_efficiency",
                    "safety_risk",
                    "score",
                ],
                "allowed_prior_fields": ["potential_V", "current_mA"],
                "held_out_queries": [
                    _query(0.68, 25.0),
                    _query(0.68, 85.0),
                    _query(1.24, 25.0),
                    _query(1.24, 85.0),
                ],
            },
        }
    )
    config["execution"] = {
        "max_concurrency": 3,
        "parallelization_unit": "same_seed_prior_arm_triplet",
        "within_cell_concurrency": 1,
        "failure_semantics": "retain cell failures and continue every scheduled seed triplet",
        "systemic_failure_semantics": (
            "stop only when all three arms fail before the first committed operation"
        ),
        "pilot_expansion_headroom_fraction": 0.2,
    }
    config["provider"].update(
        {
            "session_wall_time_limit_s": 1800.0,
            "max_recovered_mcp_tool_failures": 3,
            "max_consecutive_mcp_tool_failures": 1,
            "max_provider_error_events": 1,
            "progress_interval_s": 30.0,
        }
    )
    config["qualification"] = {"max_resource_rejections": 1}
    return config


def build(
    output_root: Path,
    summary_path: Path,
    config_path: Path,
    *,
    world_seed: int = 0,
    misspecified_selection: str = "reflected",
    reuse_existing_output: bool = False,
) -> dict[str, Any]:
    base = _load(BASE_CONFIG)
    if summary_path.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {summary_path}")
    if output_root.exists() and not reuse_existing_output:
        raise FileExistsError(f"refusing to overwrite existing output: {output_root}")
    if config_path.exists() and not reuse_existing_output:
        raise FileExistsError(f"refusing to overwrite existing output: {config_path}")
    if not output_root.exists():
        output_root.mkdir(parents=True)
    rows: list[dict[str, Any]] = []
    started = perf_counter()
    for p_index, potential in enumerate(POTENTIALS):
        for i_index, current in enumerate(CURRENTS):
            query = compile_evaluator_truth_query(base, _query(potential, current))
            cell = output_root / query["query_id"]
            trajectory = cell / "trajectory.jsonl"
            failure: dict[str, str] | None = None
            metrics: dict[str, float] | None = None
            replay: dict[str, Any] | None = None
            try:
                if reuse_existing_output:
                    if not trajectory.is_file():
                        raise FileNotFoundError(
                            f"existing diagnostic trajectory is missing: {trajectory}"
                        )
                else:
                    cell.mkdir()
                    run_agent(
                        env_id=get_task(base["task_id"]).env_id,
                        agent=_FrozenTruthReplayAgent(query["action_plan"]),
                        world_split=base["world_split"],
                        budget=len(query["action_plan"]),
                        objective=base["objective"],
                        seed=world_seed,
                        agent_seed=0,
                        observation_seed=world_seed,
                        task_id=base["task_id"],
                        output_path=trajectory,
                        budget_override=len(query["action_plan"]),
                        episode_mode_override="single_experiment",
                        electrochemical_material_family_id=base.get(
                            "electrochemical_material_family_id"
                        ),
                        electrochemical_workflow_mode=query["workflow_mode"],
                        scoring_contract_id=base.get("scoring_contract_id"),
                        observation_noise_mode=str(base["observation_noise_mode"]),
                        observation_noise_namespace=(
                            f"work-ii-parametric-diagnostic-seed{world_seed}"
                        ),
                    )
                records = load_jsonl(trajectory)
                metrics = _final_metrics(records)
                replay = verify_records(records, tolerance=0.0).to_dict()
                if replay.get("verified") is not True:
                    raise ValueError("diagnostic trajectory failed exact replay")
            except Exception as error:
                failure = {"type": type(error).__name__, "message": str(error)[:1000]}
            rows.append(
                {
                    "potential_index": p_index,
                    "current_index": i_index,
                    "potential_V": potential,
                    "current_mA": current,
                    "status": "completed" if failure is None else "failed",
                    "metrics": metrics,
                    "failure": failure,
                    "trajectory_sha256": file_sha256(trajectory) if trajectory.is_file() else None,
                    "exact_replay": replay,
                }
            )
            completed_count = len(rows)
            elapsed_s = perf_counter() - started
            rate_per_minute = 60.0 * completed_count / max(elapsed_s, 1.0e-9)
            eta_minutes = (20 - completed_count) / rate_per_minute if rate_per_minute else None
            print(json.dumps({
                "stage": "diagnostic_recipe",
                "completed": completed_count,
                "total": 20,
                "throughput_per_minute": round(rate_per_minute, 2),
                "eta_minutes": None if eta_minutes is None else round(eta_minutes, 2),
                "last_status": rows[-1]["status"],
            }, sort_keys=True), flush=True)
    completed = [row for row in rows if row["status"] == "completed"]
    best = max(
        completed,
        key=lambda row: (
            row["metrics"]["score"],
            -row["potential_index"],
            -row["current_index"],
        ),
    ) if completed else None
    reflected = None
    if best is not None:
        if misspecified_selection == "reflected":
            target_indices = (
                len(POTENTIALS) - 1 - best["potential_index"],
                len(CURRENTS) - 1 - best["current_index"],
            )
            reflected = next(
                (
                    row
                    for row in completed
                    if (row["potential_index"], row["current_index"]) == target_indices
                ),
                None,
            )
        elif misspecified_selection == "worst":
            reflected = min(
                completed,
                key=lambda row: (
                    row["metrics"]["score"],
                    -row["potential_index"],
                    -row["current_index"],
                ),
            )
        else:
            raise ValueError("misspecified_selection must be reflected or worst")
    gap = (
        best["metrics"]["score"] - reflected["metrics"]["score"]
        if best is not None and reflected is not None
        else None
    )
    qualified = len(completed) == 20 and gap is not None and gap >= 0.10
    config = None
    if qualified:
        config = _pilot_config(
            base,
            aligned=(best["potential_V"], best["current_mA"]),
            misspecified=(reflected["potential_V"], reflected["current_mA"]),
            world_seed=world_seed,
        )
        if config_path.exists():
            if canonical_json_sha256(_load(config_path)) != canonical_json_sha256(config):
                raise ValueError("existing generated config differs from diagnostic reconstruction")
        else:
            write_json_atomic(config_path, config)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-parametric-initial-model-diagnostic-0.1",
        "formal_result": False,
        "task_id": base["task_id"],
        "world_seed": world_seed,
        "misspecified_selection": misspecified_selection,
        "planned_recipe_count": 20,
        "completed_recipe_count": len(completed),
        "failed_recipe_count": 20 - len(completed),
        "all_exact_replay": len(completed) == 20 and all(
            row["exact_replay"].get("verified") is True for row in completed
        ),
        "qualification_threshold_score_gap": 0.10,
        "qualified": qualified,
        "aligned_reference_cell": best,
        "misspecified_reference_cell": reflected,
        "aligned_minus_misspecified_score": gap,
        "recipes": rows,
        "generated_config": (
            {
                "path": config_path.relative_to(ROOT).as_posix(),
                "hash_type": "canonical_json_sha256",
                "sha256": canonical_json_sha256(config),
            }
            if config is not None
            else None
        ),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(summary_path, summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--config-output", type=Path, default=DEFAULT_CONFIG_OUTPUT)
    parser.add_argument("--world-seed", type=int, default=0)
    parser.add_argument(
        "--misspecified-selection",
        choices=("reflected", "worst"),
        default="reflected",
    )
    parser.add_argument("--reuse-existing-output", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build(
        args.output_root.resolve(),
        args.summary.resolve(),
        args.config_output.resolve(),
        world_seed=args.world_seed,
        misspecified_selection=args.misspecified_selection,
        reuse_existing_output=args.reuse_existing_output,
    )
    print(json.dumps({
        "qualified": result["qualified"],
        "completed_recipe_count": result["completed_recipe_count"],
        "failed_recipe_count": result["failed_recipe_count"],
        "aligned_minus_misspecified_score": result["aligned_minus_misspecified_score"],
        "summary_sha256": result["summary_sha256"],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["qualified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
