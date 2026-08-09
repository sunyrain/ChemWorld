#!/usr/bin/env python3
"""Audit Work II estimands, power and formal resource topology."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scipy.optimize import brentq
from scipy.stats import nct, t

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
DEFAULT_OUTPUT = ROOT / "workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _power(*, effect: float, clusters: int, df: int, alpha: float) -> float:
    critical = t.ppf(1.0 - alpha, df)
    return float(1.0 - nct.cdf(critical, df, effect * clusters**0.5))


def audit(plan_path: Path, output_path: Path) -> dict[str, Any]:
    plan = _load(plan_path)
    failures: list[dict[str, Any]] = []
    binding = plan["design_binding"]
    design_path = ROOT / str(binding["path"])
    design = _load(design_path)
    design_hash = canonical_json_sha256(design)
    if design_hash != binding["sha256"]:
        failures.append({"check": "design_binding_current"})

    public = design["world_cohort"]["public_formal"]
    public_worlds = sum(len(seeds) for seeds in public["task_world_seeds"].values())
    prior_arm_count = len(design["prior_arms"])
    scheduled_cells = public_worlds * prior_arm_count
    attempt_contract = design["provider_attempt_contract"]
    planned_provider_attempts = scheduled_cells * int(
        attempt_contract["initial_attempts_per_cell"]
    )
    provider_attempt_hard_cap = scheduled_cells * int(
        attempt_contract["maximum_total_provider_attempts_per_cell"]
    )
    if planned_provider_attempts != int(
        attempt_contract["public_matrix_initial_attempt_count"]
    ):
        failures.append({"check": "provider_attempt_initial_denominator"})
    if provider_attempt_hard_cap != int(
        attempt_contract["public_matrix_provider_attempt_hard_cap"]
    ):
        failures.append({"check": "provider_attempt_hard_cap"})
    population = plan["analysis_population"]
    if public_worlds != population["independent_task_world_clusters"]:
        failures.append({"check": "independent_cluster_denominator"})
    if scheduled_cells != population["scheduled_public_cells"]:
        failures.append({"check": "scheduled_cell_denominator"})

    resource_rows: list[dict[str, Any]] = []
    total_sessions = 0
    total_experiments = 0
    total_operations = 0
    total_input = 0
    total_uncached = 0
    total_output = 0
    topology_wall = 0.0
    expected_stages = plan["checkpoint_contract"]["stage_ids"]
    for task in design["tasks"]:
        config = _load(ROOT / str(task["campaign_config"]))
        task_id = str(task["task_id"])
        task_worlds = len(public["task_world_seeds"][task_id])
        cells = task_worlds * prior_arm_count
        campaign = config["campaign"]
        resources = config["method_resources"]
        if config.get("snapshot_stages") != expected_stages:
            failures.append({"check": "neutral_snapshot_stages", "task_id": task_id})
        total_sessions += cells
        total_experiments += cells * int(campaign["complete_experiments"])
        total_operations += cells * int(campaign["operation_attempt_limit"])
        total_input += cells * int(resources["input_token_limit"])
        total_uncached += cells * int(resources["uncached_input_token_limit"])
        total_output += cells * int(resources["output_token_limit"])
        task_wall = task_worlds * float(resources["wall_time_limit_s"])
        topology_wall += task_wall
        resource_rows.append(
            {
                "task_id": task_id,
                "worlds": task_worlds,
                "cells": cells,
                "complete_experiments": cells * int(campaign["complete_experiments"]),
                "operation_attempt_limit": cells * int(campaign["operation_attempt_limit"]),
                "input_token_limit": cells * int(resources["input_token_limit"]),
                "uncached_input_token_limit": cells
                * int(resources["uncached_input_token_limit"]),
                "output_token_limit": cells * int(resources["output_token_limit"]),
                "serial_seed_triplet_wall_limit_s": task_wall,
            }
        )

    power = plan["power_design"]
    clusters = int(power["independent_clusters"])
    df = int(power["residual_degrees_of_freedom"])
    alpha = float(power["alpha"])
    planning_effect = float(power["planning_standardized_effect"])
    planning_power = _power(effect=planning_effect, clusters=clusters, df=df, alpha=alpha)
    mde_80 = float(
        brentq(
            lambda effect: _power(
                effect=effect,
                clusters=clusters,
                df=df,
                alpha=alpha,
            )
            - 0.80,
            1.0e-6,
            5.0,
        )
    )
    if planning_power < float(power["minimum_required_power_at_planning_effect"]):
        failures.append({"check": "planning_power"})

    report = {
        "schema_version": "chemworld-work-ii-analysis-power-audit-0.1",
        "analysis_plan_path": str(plan_path.relative_to(ROOT)).replace("\\", "/"),
        "analysis_plan_sha256": canonical_json_sha256(plan),
        "design_sha256": design_hash,
        "status": "passed" if not failures else "failed",
        "formal_result": False,
        "participant_provider_calls": 0,
        "denominators": {
            "tasks": len(design["tasks"]),
            "independent_task_world_clusters": public_worlds,
            "prior_arms": prior_arm_count,
            "scheduled_participant_cells": scheduled_cells,
            "provider_repeats_per_cell": population["provider_repeats_per_cell"],
            "provider_attempts_initial_planned": planned_provider_attempts,
            "provider_attempts_hard_cap": provider_attempt_hard_cap,
        },
        "power": {
            "alpha_one_sided": alpha,
            "clusters": clusters,
            "residual_degrees_of_freedom": df,
            "planning_standardized_effect": planning_effect,
            "power_at_planning_effect": planning_power,
            "minimum_detectable_standardized_effect_80pct": mde_80,
            "sensitivity_table": [
                {
                    "standardized_effect": effect,
                    "power": _power(effect=effect, clusters=clusters, df=df, alpha=alpha),
                }
                for effect in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
            ],
            "interpretation": (
                "The frozen 25-cluster design is powered for moderate-to-large effects, "
                "not small effects."
            ),
        },
        "resource_topology": {
            "task_rows": resource_rows,
            "maximum_provider_sessions": total_sessions,
            "provider_attempts_initial_planned": planned_provider_attempts,
            "provider_attempts_hard_cap": provider_attempt_hard_cap,
            "maximum_provider_attempts_per_cell": attempt_contract[
                "maximum_total_provider_attempts_per_cell"
            ],
            "complete_experiments": total_experiments,
            "operation_attempt_limit": total_operations,
            "input_token_limit": total_input,
            "uncached_input_token_limit": total_uncached,
            "output_token_limit": total_output,
            "serial_seed_triplet_wall_limit_s": topology_wall,
            "serial_seed_triplet_wall_limit_h": topology_wall / 3600.0,
            "wellau_currency_cost_known": False,
            "formal_currency_ceiling_approved": False,
        },
        "w2_05_complete": not failures,
        "w2_07_complete": False,
        "w2_07_remaining_blockers": [
            "user-approved formal currency ceiling",
            "qualified formal runner ETA calibration",
        ],
        "failures": failures,
    }
    write_json_atomic(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit(args.plan.resolve(), args.output.resolve())
    print(
        json.dumps(
            {
                "status": report["status"],
                "clusters": report["denominators"]["independent_task_world_clusters"],
                "cells": report["denominators"]["scheduled_participant_cells"],
                "power_at_d_0_6": report["power"]["power_at_planning_effect"],
                "mde_80": report["power"]["minimum_detectable_standardized_effect_80pct"],
                "failure_count": len(report["failures"]),
                "output": str(args.output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
