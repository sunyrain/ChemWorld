#!/usr/bin/env python3
"""Screen additional Work II structural and parametric initial-model candidates."""

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
THRESHOLD = 0.10


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _final_metrics(records: list[dict[str, Any]], metric_ids: list[str]) -> dict[str, float]:
    final_rows = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(final_rows) != 1:
        raise ValueError("diagnostic recipe must contain exactly one final assay")
    row = final_rows[0]
    observation = row.get("observation")
    if not isinstance(observation, dict):
        raise ValueError("diagnostic final assay lacks its observation")
    result = {"score": float(row["leaderboard_score"])}
    for metric in metric_ids:
        if metric == "score":
            continue
        value = observation.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"diagnostic metric is unavailable: {metric}")
        result[metric] = float(value)
    return result


def _run_queries(
    *,
    base: dict[str, Any],
    queries: list[dict[str, Any]],
    output_root: Path,
    namespace: str,
) -> list[dict[str, Any]]:
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {output_root}")
    output_root.mkdir(parents=True)
    rows: list[dict[str, Any]] = []
    started = perf_counter()
    for index, query_spec in enumerate(queries, start=1):
        query = compile_evaluator_truth_query(base, query_spec)
        cell = output_root / str(query["query_id"])
        cell.mkdir()
        trajectory = cell / "trajectory.jsonl"
        failure: dict[str, str] | None = None
        metrics: dict[str, float] | None = None
        replay: dict[str, Any] | None = None
        try:
            run_agent(
                env_id=get_task(str(base["task_id"])).env_id,
                agent=_FrozenTruthReplayAgent(query["action_plan"]),
                world_split=str(base["world_split"]),
                budget=len(query["action_plan"]),
                objective=str(base["objective"]),
                seed=0,
                agent_seed=0,
                observation_seed=0,
                task_id=str(base["task_id"]),
                output_path=trajectory,
                budget_override=len(query["action_plan"]),
                episode_mode_override="single_experiment",
                electrochemical_material_family_id=base.get("electrochemical_material_family_id"),
                crystallization_material_family_id=base.get("crystallization_material_family_id"),
                scoring_contract_id=base.get("scoring_contract_id"),
                observation_noise_mode=str(base["observation_noise_mode"]),
                observation_noise_namespace=namespace,
            )
            records = load_jsonl(trajectory)
            metrics = _final_metrics(records, list(query_spec["metric_ids"]))
            replay = verify_records(records, tolerance=0.0).to_dict()
            if replay.get("verified") is not True:
                raise ValueError("diagnostic trajectory failed exact replay")
        except Exception as error:
            failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        rows.append(
            {
                "query_id": query_spec["query_id"],
                "feature_values": query_spec["feature_values"],
                "status": "completed" if failure is None else "failed",
                "metrics": metrics,
                "failure": failure,
                "trajectory_sha256": file_sha256(trajectory) if trajectory.is_file() else None,
                "exact_replay": replay,
            }
        )
        elapsed = perf_counter() - started
        rate = 60.0 * index / max(elapsed, 1.0e-9)
        print(
            json.dumps(
                {
                    "stage": "candidate_recipe",
                    "completed": index,
                    "total": len(queries),
                    "throughput_per_minute": round(rate, 2),
                    "eta_minutes": round((len(queries) - index) / rate, 2) if rate else None,
                    "last_status": rows[-1]["status"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    return rows


def _structural_initial_model(
    *, modules: tuple[str, str], dominant_module: str | None
) -> dict[str, Any]:
    if dominant_module is None:
        return {
            "schema_version": "chemworld-work-ii-initial-world-model-0.1",
            "locus": "structural_mechanistic",
            "availability": "opaque_for_target_locus",
            "model": None,
            "interpretation": (
                "No task-specific dominant-module hypothesis is supplied. "
                "Experimental evidence is authoritative."
            ),
        }
    secondary = modules[1] if dominant_module == modules[0] else modules[0]
    return {
        "schema_version": "chemworld-work-ii-initial-world-model-0.1",
        "locus": "structural_mechanistic",
        "availability": "supplied_incomplete_model",
        "model": {
            "modules": list(modules),
            "dominant_module": dominant_module,
            "secondary_module": secondary,
            "expected_relation": (
                f"Local endpoint variation is expected to be more sensitive to {dominant_module} "
                f"than to {secondary}."
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


def _structural_config(
    *,
    base: dict[str, Any],
    candidate_id: str,
    modules: tuple[str, str],
    dominant_module: str,
    factorial: dict[str, Any],
) -> dict[str, Any]:
    wrong_module = modules[1] if dominant_module == modules[0] else modules[0]
    config = deepcopy(base)
    config.update(
        {
            "schema_version": "chemworld-work-ii-campaign-pilot-0.3",
            "pilot_id": f"work-ii-{candidate_id}-structural-initial-model-pilot",
            "formal_result": False,
            "observation_noise_namespace": (
                f"work-ii-{candidate_id}-structural-initial-model-pilot"
            ),
            "intervention": {
                "locus": "structural_mechanistic",
                "target": "dominant_module",
                "modules": list(modules),
                "material_information_matched_opaque": True,
                "world_and_resource_contract_matched": True,
                "diagnostic_factorial": factorial,
            },
            "prior_arms": {
                "opaque": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _structural_initial_model(
                        modules=modules, dominant_module=None
                    ),
                },
                "aligned_nominal": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _structural_initial_model(
                        modules=modules, dominant_module=dominant_module
                    ),
                },
                "misindexed_nominal": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _structural_initial_model(
                        modules=modules, dominant_module=wrong_module
                    ),
                },
            },
        }
    )
    config["belief_checkpoint"]["allowed_prior_fields"] = list(modules)
    return config


def _structural_summary(
    *,
    candidate_id: str,
    base: dict[str, Any],
    rows: list[dict[str, Any]],
    module_a: str,
    module_b: str,
    a_levels: tuple[str, str],
    b_levels: tuple[str, str],
    config_path: Path,
    factorial: dict[str, Any],
) -> dict[str, Any]:
    keyed = {
        (
            str(row["feature_values"]["_module_a_level"]),
            str(row["feature_values"]["_module_b_level"]),
        ): row
        for row in rows
    }
    for row in rows:
        row["feature_values"].pop("_module_a_level", None)
        row["feature_values"].pop("_module_b_level", None)
    all_completed = len(rows) == 4 and all(row["status"] == "completed" for row in rows)
    influence_a = influence_b = None
    if all_completed:

        def score(a: str, b: str) -> float:
            return float(keyed[(a, b)]["metrics"]["score"])

        influence_a = 0.5 * (
            abs(score(a_levels[1], b_levels[0]) - score(a_levels[0], b_levels[0]))
            + abs(score(a_levels[1], b_levels[1]) - score(a_levels[0], b_levels[1]))
        )
        influence_b = 0.5 * (
            abs(score(a_levels[0], b_levels[1]) - score(a_levels[0], b_levels[0]))
            + abs(score(a_levels[1], b_levels[1]) - score(a_levels[1], b_levels[0]))
        )
    gap = abs(influence_a - influence_b) if influence_a is not None else None
    dominant = (
        (module_a if influence_a is not None and influence_a >= float(influence_b) else module_b)
        if all_completed
        else None
    )
    qualified = bool(all_completed and gap is not None and gap >= THRESHOLD)
    config = (
        _structural_config(
            base=base,
            candidate_id=candidate_id,
            modules=(module_a, module_b),
            dominant_module=str(dominant),
            factorial=factorial,
        )
        if qualified and dominant is not None
        else None
    )
    if config is not None:
        write_json_atomic(config_path, config)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-nonentity-candidate-screen-0.1",
        "formal_result": False,
        "candidate_id": candidate_id,
        "locus": "structural_mechanistic",
        "task_id": base["task_id"],
        "world_seed": 0,
        "planned_recipe_count": 4,
        "completed_recipe_count": sum(row["status"] == "completed" for row in rows),
        "failed_recipe_count": sum(row["status"] == "failed" for row in rows),
        "all_exact_replay": all_completed
        and all(row["exact_replay"].get("verified") is True for row in rows),
        "qualification_threshold": THRESHOLD,
        "module_influences": {module_a: influence_a, module_b: influence_b},
        "influence_gap": gap,
        "dominant_module": dominant,
        "qualified": qualified,
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
    return summary


def _crystallization_queries() -> list[dict[str, Any]]:
    reaction = {
        "mild": {"reaction_temperature_K": 340.0, "reaction_duration_s": 900.0},
        "strong": {"reaction_temperature_K": 410.0, "reaction_duration_s": 7200.0},
    }
    crystallization = {
        "mild": {
            "crystallization_temperature_K": 285.0,
            "crystallization_duration_s": 900.0,
        },
        "strong": {
            "crystallization_temperature_K": 270.0,
            "crystallization_duration_s": 7200.0,
        },
    }
    rows = []
    for a_name, a_values in reaction.items():
        for b_name, b_values in crystallization.items():
            rows.append(
                {
                    "query_id": f"reaction-{a_name}--crystallization-{b_name}",
                    "feature_values": {
                        "catalyst": 0,
                        "solvent": 0,
                        "reagent_amount_mol": 0.01,
                        "seed_mass_g": 0.005,
                        **a_values,
                        **b_values,
                        "_module_a_level": a_name,
                        "_module_b_level": b_name,
                    },
                    "metric_ids": ["crystal_yield", "crystal_purity", "crystal_csd_quality"],
                }
            )
    return rows


def _partition_queries() -> list[dict[str, Any]]:
    contact = {
        "mild": {"mix_duration_s": 60.0, "stirring_speed_rpm": 300.0},
        "strong": {"mix_duration_s": 600.0, "stirring_speed_rpm": 1100.0},
    }
    settling = {"mild": {"settle_duration_s": 120.0}, "strong": {"settle_duration_s": 1200.0}}
    rows = []
    for a_name, a_values in contact.items():
        for b_name, b_values in settling.items():
            rows.append(
                {
                    "query_id": f"contact-{a_name}--settling-{b_name}",
                    "feature_values": {
                        "solvent": 0,
                        "aqueous_phase_volume_L": 0.015,
                        "extractant": 0,
                        "extractant_volume_L": 0.018,
                        **a_values,
                        **b_values,
                        "_module_a_level": a_name,
                        "_module_b_level": b_name,
                    },
                    "metric_ids": ["phase_ratio", "product_in_organic", "product_in_aqueous"],
                }
            )
    return rows


def _parametric_model(temperature: float | None, duration: float | None) -> dict[str, Any]:
    if temperature is None or duration is None:
        return {
            "schema_version": "chemworld-work-ii-initial-world-model-0.1",
            "locus": "parametric",
            "availability": "opaque_for_target_locus",
            "model": None,
            "interpretation": (
                "No task-specific temperature-duration operating point is supplied. "
                "Experimental evidence is authoritative."
            ),
        }
    return {
        "schema_version": "chemworld-work-ii-initial-world-model-0.1",
        "locus": "parametric",
        "availability": "supplied_incomplete_model",
        "model": {
            "claim": {
                "reaction_temperature_K": temperature,
                "reaction_duration_s": duration,
                "temperature_tolerance_K": 15.0,
                "duration_tolerance_s": 300.0,
                "expected_relation": (
                    "At the stated material context, safe balanced performance is more likely near "
                    "this approximate operating point than far from it."
                ),
            },
            "confidence": 0.70,
            "reference_context": {
                "catalyst": 0,
                "solvent": 0,
                "reagent_amount_mol": 0.01,
                "catalyst_amount_mol": 0.0003,
            },
            "scope_limit": "This is an incomplete local process model, not ground truth.",
        },
        "interpretation": (
            "The supplied model may be reliable or shifted. Experimental evidence is authoritative."
        ),
    }


def _safety_queries() -> list[dict[str, Any]]:
    rows = []
    for temperature in (340.0, 360.0, 390.0, 420.0):
        for duration in (900.0, 1800.0, 3600.0, 7200.0):
            rows.append(
                {
                    "query_id": f"t{temperature:.0f}-d{duration:.0f}",
                    "feature_values": {
                        "catalyst": 0,
                        "solvent": 0,
                        "reagent_amount_mol": 0.01,
                        "catalyst_amount_mol": 0.0003,
                        "reaction_temperature_K": temperature,
                        "reaction_duration_s": duration,
                    },
                    "metric_ids": ["yield", "selectivity", "safety_risk", "score"],
                }
            )
    return rows


def _safety_config(
    base: dict[str, Any], *, best: dict[str, Any], worst: dict[str, Any]
) -> dict[str, Any]:
    config = deepcopy(base)
    best_values = best["feature_values"]
    worst_values = worst["feature_values"]
    config.update(
        {
            "schema_version": "chemworld-work-ii-campaign-pilot-0.3",
            "pilot_id": "work-ii-reaction-safety-parametric-initial-model-pilot",
            "formal_result": False,
            "observation_noise_namespace": (
                "work-ii-reaction-safety-parametric-initial-model-pilot"
            ),
            "intervention": {
                "locus": "parametric",
                "target": "reaction_temperature_duration_operating_point",
                "material_information_matched_opaque": True,
                "world_and_resource_contract_matched": True,
                "diagnostic_grid": {
                    "reaction_temperature_K": [340.0, 360.0, 390.0, 420.0],
                    "reaction_duration_s": [900.0, 1800.0, 3600.0, 7200.0],
                },
            },
            "prior_arms": {
                "opaque": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _parametric_model(None, None),
                },
                "aligned_nominal": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _parametric_model(
                        float(best_values["reaction_temperature_K"]),
                        float(best_values["reaction_duration_s"]),
                    ),
                },
                "misindexed_nominal": {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": _parametric_model(
                        float(worst_values["reaction_temperature_K"]),
                        float(worst_values["reaction_duration_s"]),
                    ),
                },
            },
        }
    )
    config["belief_checkpoint"]["allowed_prior_fields"] = [
        "reaction_temperature_K",
        "reaction_duration_s",
    ]
    config["belief_checkpoint"]["held_out_queries"] = [
        row
        for row in _safety_queries()
        if row["query_id"] in {"t340-d900", "t340-d7200", "t420-d900", "t420-d7200"}
    ]
    return config


def _safety_summary(
    *, base: dict[str, Any], rows: list[dict[str, Any]], config_path: Path
) -> dict[str, Any]:
    completed = [row for row in rows if row["status"] == "completed"]
    best = (
        max(
            completed,
            key=lambda row: (
                float(row["metrics"]["score"]),
                -float(row["feature_values"]["reaction_temperature_K"]),
                -float(row["feature_values"]["reaction_duration_s"]),
            ),
        )
        if completed
        else None
    )
    worst = (
        min(
            completed,
            key=lambda row: (
                float(row["metrics"]["score"]),
                float(row["feature_values"]["reaction_temperature_K"]),
                float(row["feature_values"]["reaction_duration_s"]),
            ),
        )
        if completed
        else None
    )
    gap = (
        float(best["metrics"]["score"]) - float(worst["metrics"]["score"])
        if best is not None and worst is not None
        else None
    )
    all_completed = len(completed) == len(rows) == 16
    qualified = bool(all_completed and best != worst and gap is not None and gap >= THRESHOLD)
    config = _safety_config(base, best=best, worst=worst) if qualified else None
    if config is not None:
        write_json_atomic(config_path, config)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-nonentity-candidate-screen-0.1",
        "formal_result": False,
        "candidate_id": "reaction-safety-parametric",
        "locus": "parametric",
        "task_id": base["task_id"],
        "world_seed": 0,
        "planned_recipe_count": 16,
        "completed_recipe_count": len(completed),
        "failed_recipe_count": len(rows) - len(completed),
        "all_exact_replay": all_completed
        and all(row["exact_replay"].get("verified") is True for row in rows),
        "qualification_threshold": THRESHOLD,
        "best_cell": best,
        "worst_cell": worst,
        "score_gap": gap,
        "qualified": qualified,
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
    return summary


def build_candidate(
    candidate: str, output_root: Path, summary_path: Path, config_path: Path
) -> dict[str, Any]:
    if summary_path.exists() or config_path.exists():
        raise FileExistsError("refusing to overwrite an existing summary or pilot config")
    if candidate == "crystallization-structural":
        base = _load(ROOT / "configs/benchmark/work_ii_crystallization_campaign.json")
        queries = _crystallization_queries()
        clean_queries = deepcopy(queries)
        for query in clean_queries:
            query["feature_values"].pop("_module_a_level")
            query["feature_values"].pop("_module_b_level")
        rows = _run_queries(
            base=base,
            queries=clean_queries,
            output_root=output_root,
            namespace="work-ii-crystallization-structural-screen-seed0",
        )
        for row, query in zip(rows, queries, strict=True):
            row["feature_values"]["_module_a_level"] = query["feature_values"]["_module_a_level"]
            row["feature_values"]["_module_b_level"] = query["feature_values"]["_module_b_level"]
        result = _structural_summary(
            candidate_id="crystallization",
            base=base,
            rows=rows,
            module_a="reaction_module",
            module_b="crystallization_module",
            a_levels=("mild", "strong"),
            b_levels=("mild", "strong"),
            config_path=config_path,
            factorial={
                "reaction": {
                    "mild": {"temperature_K": 340.0, "duration_s": 900.0},
                    "strong": {"temperature_K": 410.0, "duration_s": 7200.0},
                },
                "crystallization": {
                    "mild": {"temperature_K": 285.0, "duration_s": 900.0},
                    "strong": {"temperature_K": 270.0, "duration_s": 7200.0},
                },
            },
        )
    elif candidate == "partition-structural":
        base = _load(ROOT / "configs/benchmark/work_ii_partition_campaign.json")
        queries = _partition_queries()
        clean_queries = deepcopy(queries)
        for query in clean_queries:
            query["feature_values"].pop("_module_a_level")
            query["feature_values"].pop("_module_b_level")
        rows = _run_queries(
            base=base,
            queries=clean_queries,
            output_root=output_root,
            namespace="work-ii-partition-structural-screen-seed0",
        )
        for row, query in zip(rows, queries, strict=True):
            row["feature_values"]["_module_a_level"] = query["feature_values"]["_module_a_level"]
            row["feature_values"]["_module_b_level"] = query["feature_values"]["_module_b_level"]
        result = _structural_summary(
            candidate_id="partition",
            base=base,
            rows=rows,
            module_a="contact_mass_transfer_module",
            module_b="settling_separation_module",
            a_levels=("mild", "strong"),
            b_levels=("mild", "strong"),
            config_path=config_path,
            factorial={
                "contact": {
                    "mild": {"mix_duration_s": 60.0, "stirring_speed_rpm": 300.0},
                    "strong": {"mix_duration_s": 600.0, "stirring_speed_rpm": 1100.0},
                },
                "settling": {
                    "mild": {"settle_duration_s": 120.0},
                    "strong": {"settle_duration_s": 1200.0},
                },
            },
        )
    elif candidate == "reaction-safety-parametric":
        base = _load(ROOT / "configs/benchmark/work_ii_safety_campaign.json")
        rows = _run_queries(
            base=base,
            queries=_safety_queries(),
            output_root=output_root,
            namespace="work-ii-reaction-safety-parametric-screen-seed0",
        )
        result = _safety_summary(base=base, rows=rows, config_path=config_path)
    else:
        raise ValueError(f"unsupported candidate: {candidate}")
    write_json_atomic(summary_path, result)
    return result


def _default_paths(candidate: str) -> tuple[Path, Path, Path]:
    stem = candidate.replace("-", "_")
    return (
        ROOT / "runs/development" / f"work-ii-{candidate}-screen-20260811",
        ROOT / "workstreams/flagship_tasks/reports" / f"work-ii-{candidate}-screen-20260811.json",
        ROOT / "configs/benchmark" / f"work_ii_{stem}_initial_model_pilot.json",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate",
        required=True,
        choices=(
            "crystallization-structural",
            "partition-structural",
            "reaction-safety-parametric",
        ),
    )
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--config-output", type=Path)
    args = parser.parse_args()
    default_output, default_summary, default_config = _default_paths(args.candidate)
    result = build_candidate(
        args.candidate,
        (args.output_root or default_output).resolve(),
        (args.summary or default_summary).resolve(),
        (args.config_output or default_config).resolve(),
    )
    print(
        json.dumps(
            {
                "candidate_id": result["candidate_id"],
                "qualified": result["qualified"],
                "completed_recipe_count": result["completed_recipe_count"],
                "failed_recipe_count": result["failed_recipe_count"],
                "influence_gap": result.get("influence_gap"),
                "score_gap": result.get("score_gap"),
                "summary_sha256": result["summary_sha256"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if result["qualified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
