#!/usr/bin/env python3
"""Qualify and materialize the Work II structural initial-model pilot."""

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
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent, compile_evaluator_truth_query
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
BASE_CONFIG = ROOT / "configs/benchmark/work_ii_distillation_campaign.json"
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-structural-initial-model-diagnostic-20260811"
)
DEFAULT_SUMMARY = (
    ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-structural-initial-model-diagnostic-20260811.json"
)
DEFAULT_CONFIG_OUTPUT = (
    ROOT / "configs/benchmark/work_ii_distillation_structural_initial_model_pilot.json"
)

REACTION_LEVELS = {
    "low": {"reaction_temperature_K": 340.0, "reaction_duration_s": 1800.0},
    "high": {"reaction_temperature_K": 410.0, "reaction_duration_s": 6000.0},
}
SEPARATION_LEVELS = {
    "low": {
        "distillation_temperature_K": 355.0,
        "distillation_duration_s": 1200.0,
        "reflux_ratio": 0.8,
    },
    "high": {
        "distillation_temperature_K": 390.0,
        "distillation_duration_s": 3300.0,
        "reflux_ratio": 4.5,
    },
}
BASE_FEATURES = {"catalyst": 0, "solvent": 0, "reagent_amount_mol": 0.01}
METRICS = ("distillate_purity", "distillate_recovery", "solvent_loss", "score")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _query(reaction_level: str, separation_level: str) -> dict[str, Any]:
    return {
        "query_id": f"reaction-{reaction_level}--separation-{separation_level}",
        "feature_values": {
            **BASE_FEATURES,
            **REACTION_LEVELS[reaction_level],
            **SEPARATION_LEVELS[separation_level],
        },
        "metric_ids": list(METRICS),
    }


def _final_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    rows = [
        row for row in records
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
    result: dict[str, float] = {}
    for metric in METRICS:
        value = row.get("leaderboard_score") if metric == "score" else observation.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"diagnostic metric is unavailable: {metric}")
        result[metric] = float(value)
    return result


def _initial_model(dominant_module: str | None) -> dict[str, Any]:
    if dominant_module is None:
        return {
            "schema_version": "chemworld-work-ii-initial-world-model-0.1",
            "locus": "structural_mechanistic",
            "availability": "opaque_for_target_locus",
            "model": None,
            "interpretation": (
                "No task-specific claim about the dominant reaction-versus-separation module is "
                "supplied. Experimental evidence is authoritative."
            ),
        }
    secondary = "separation" if dominant_module == "reaction" else "reaction"
    return {
        "schema_version": "chemworld-work-ii-initial-world-model-0.1",
        "locus": "structural_mechanistic",
        "availability": "supplied_incomplete_model",
        "model": {
            "modules": ["reaction", "separation"],
            "dominant_module": dominant_module,
            "secondary_module": secondary,
            "expected_relation": (
                "Local endpoint variation is expected to be more sensitive to the "
                f"{dominant_module} "
                f"module than to the {secondary} module in this task family."
            ),
            "confidence": 0.70,
            "scope_limit": (
                "This is an incomplete local dominance hypothesis, not a disclosed mechanism or "
                "ground-truth causal graph."
            ),
        },
        "interpretation": (
            "The supplied model may be reliable or reversed. "
            "Experimental evidence is authoritative."
        ),
    }


def _pilot_config(base: dict[str, Any], dominant_module: str) -> dict[str, Any]:
    wrong_module = "separation" if dominant_module == "reaction" else "reaction"
    config = deepcopy(base)
    config.update({
        "schema_version": "chemworld-work-ii-campaign-pilot-0.3",
        "pilot_id": "work-ii-distillation-structural-initial-model-pilot",
        "formal_result": False,
        "observation_noise_namespace": "work-ii-distillation-structural-initial-model-pilot",
        "intervention": {
            "locus": "structural_mechanistic",
            "target": "dominant_reaction_vs_separation_module",
            "material_information_matched_opaque": True,
            "world_and_resource_contract_matched": True,
            "diagnostic_factorial": {
                "reaction_levels": REACTION_LEVELS,
                "separation_levels": SEPARATION_LEVELS,
            },
        },
        "prior_arms": {
            "opaque": {
                "material_information": {"mode": "opaque_codes"},
                "initial_world_model": _initial_model(None),
            },
            "aligned_nominal": {
                "material_information": {"mode": "opaque_codes"},
                "initial_world_model": _initial_model(dominant_module),
            },
            "misindexed_nominal": {
                "material_information": {"mode": "opaque_codes"},
                "initial_world_model": _initial_model(wrong_module),
            },
        },
    })
    config["belief_checkpoint"]["allowed_prior_fields"] = [
        "reaction_module",
        "separation_module",
    ]
    return config


def build(output_root: Path, summary_path: Path, config_path: Path) -> dict[str, Any]:
    base = _load(BASE_CONFIG)
    for path in (output_root, summary_path, config_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite existing output: {path}")
    output_root.mkdir(parents=True)
    rows: list[dict[str, Any]] = []
    started = perf_counter()
    for reaction_level in REACTION_LEVELS:
        for separation_level in SEPARATION_LEVELS:
            query = compile_evaluator_truth_query(
                base, _query(reaction_level, separation_level)
            )
            cell = output_root / query["query_id"]
            cell.mkdir()
            trajectory = cell / "trajectory.jsonl"
            failure: dict[str, str] | None = None
            metrics: dict[str, float] | None = None
            replay: dict[str, Any] | None = None
            try:
                run_agent(
                    env_id=get_task(base["task_id"]).env_id,
                    agent=_FrozenTruthReplayAgent(query["action_plan"]),
                    world_split=base["world_split"],
                    budget=len(query["action_plan"]),
                    objective=base["objective"],
                    seed=0,
                    agent_seed=0,
                    observation_seed=0,
                    task_id=base["task_id"],
                    output_path=trajectory,
                    budget_override=len(query["action_plan"]),
                    episode_mode_override="single_experiment",
                    scoring_contract_id=base.get("scoring_contract_id"),
                    observation_noise_mode=str(base["observation_noise_mode"]),
                    observation_noise_namespace="work-ii-structural-diagnostic-seed0",
                )
                records = load_jsonl(trajectory)
                metrics = _final_metrics(records)
                replay = verify_records(records, tolerance=0.0).to_dict()
                if replay.get("verified") is not True:
                    raise ValueError("diagnostic trajectory failed exact replay")
            except Exception as error:
                failure = {"type": type(error).__name__, "message": str(error)[:1000]}
            rows.append({
                "reaction_level": reaction_level,
                "separation_level": separation_level,
                "status": "completed" if failure is None else "failed",
                "metrics": metrics,
                "failure": failure,
                "trajectory_sha256": file_sha256(trajectory) if trajectory.is_file() else None,
                "exact_replay": replay,
            })
            completed = len(rows)
            elapsed_s = perf_counter() - started
            rate = 60.0 * completed / max(elapsed_s, 1.0e-9)
            print(json.dumps({
                "stage": "diagnostic_recipe",
                "completed": completed,
                "total": 4,
                "throughput_per_minute": round(rate, 2),
                "eta_minutes": round((4 - completed) / rate, 2) if rate else None,
                "last_status": rows[-1]["status"],
            }, sort_keys=True), flush=True)

    keyed = {(row["reaction_level"], row["separation_level"]): row for row in rows}
    all_completed = all(row["status"] == "completed" for row in rows)
    reaction_influence = separation_influence = None
    dominant_module = None
    if all_completed:
        def score(reaction: str, separation: str) -> float:
            return float(keyed[(reaction, separation)]["metrics"]["score"])

        reaction_influence = 0.5 * (
            abs(score("high", "low") - score("low", "low"))
            + abs(score("high", "high") - score("low", "high"))
        )
        separation_influence = 0.5 * (
            abs(score("low", "high") - score("low", "low"))
            + abs(score("high", "high") - score("high", "low"))
        )
        dominant_module = (
            "reaction" if reaction_influence >= separation_influence else "separation"
        )
    influence_gap = (
        abs(reaction_influence - separation_influence)
        if reaction_influence is not None and separation_influence is not None
        else None
    )
    qualified = bool(all_completed and influence_gap is not None and influence_gap >= 0.10)
    config = _pilot_config(base, dominant_module) if qualified and dominant_module else None
    if config is not None:
        write_json_atomic(config_path, config)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-structural-initial-model-diagnostic-0.1",
        "formal_result": False,
        "task_id": base["task_id"],
        "world_seed": 0,
        "planned_recipe_count": 4,
        "completed_recipe_count": sum(row["status"] == "completed" for row in rows),
        "failed_recipe_count": sum(row["status"] == "failed" for row in rows),
        "all_exact_replay": all_completed and all(
            row["exact_replay"].get("verified") is True for row in rows
        ),
        "qualification_threshold_influence_gap": 0.10,
        "reaction_influence": reaction_influence,
        "separation_influence": separation_influence,
        "influence_gap": influence_gap,
        "dominant_module": dominant_module,
        "qualified": qualified,
        "recipes": rows,
        "generated_config": (
            {
                "path": config_path.relative_to(ROOT).as_posix(),
                "sha256": canonical_json_sha256(config),
            }
            if config is not None else None
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build(args.output_root, args.summary, args.config_output)
    print(json.dumps({
        "qualified": result["qualified"],
        "reaction_influence": result["reaction_influence"],
        "separation_influence": result["separation_influence"],
        "influence_gap": result["influence_gap"],
        "dominant_module": result["dominant_module"],
        "summary_sha256": result["summary_sha256"],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["qualified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
