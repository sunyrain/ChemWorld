"""Qualify the replacement reaction-crystallization material family locally."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import statistics
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.agents.crystallization_single_stage import (
    crystallization_single_stage_parameters_from_unit_vector,
)
from chemworld.agents.static_optimization import StaticOptimizationPlan
from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.static_optimization_execution import (
    StaticOptimizationExperimentSession,
)
from chemworld.world.crystallization_material_family import (
    REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    crystallization_material_family,
)
from chemworld.world.scoring import CRYSTALLIZATION_S0_BALANCED_PRODUCT_V1

QUALIFICATION_VERSION = "chemworld-reaction-crystallization-material-qualification-0.1"
DEFAULT_OUTPUT = (
    "workstreams/flagship_tasks/reports/"
    "static-s0-crystallization-material-family-v1-qualification-v0.1.json"
)
_MATERIAL_PAIRS = tuple(itertools.product(range(4), repeat=2))
_SOURCE_CONTRACT_PATHS = (
    "src/chemworld/world/crystallization_material_family.py",
    "src/chemworld/world/parameters.py",
    "src/chemworld/world/reaction_kernel.py",
    "src/chemworld/runtime/crystallization_services.py",
    "src/chemworld/world/scoring.py",
    "scripts/qualify_crystallization_material_family.py",
)


def _source_hashes(root: Path) -> dict[str, str]:
    return {
        path: hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in _SOURCE_CONTRACT_PATHS
    }


def _plan(catalyst: int, solvent: int) -> StaticOptimizationPlan:
    vector = np.asarray((0.55, 0.60, 0.60, 0.60, 0.5, 0.55, 0.5, 0.50, 0.45, 0.65))
    vector[4] = (catalyst + 0.5) / 4.0
    vector[6] = (solvent + 0.5) / 4.0
    parameters = crystallization_single_stage_parameters_from_unit_vector(vector)
    parameters["catalyst"] = catalyst
    parameters["solvent"] = solvent
    return StaticOptimizationPlan(
        experiment_intent="standardize one anonymous catalyst-solvent material pair",
        search_vector=tuple(float(value) for value in vector),
        requested_measurement_slots=(
            "diagnostic-01-hplc",
            "diagnostic-02-hplc",
        ),
        measurement_objective="measure reaction and crystallization product quality",
        expected_effect="material-specific runtime laws produce a stable response",
        uncertainty=0.5,
        recipe_parameters=parameters,
    )


def _execute_pair(world_seed: int, catalyst: int, solvent: int) -> dict[str, Any]:
    namespace = f"crystallization-material-qualification-world-{world_seed:04d}"
    with StaticOptimizationExperimentSession(
        task_id="reaction-to-crystallization",
        seed=world_seed,
        experiment_horizon=1,
        experiment_index_offset=0,
        observation_seed=world_seed + 120_000,
        observation_noise_namespace=namespace,
        crystallization_material_family_id=(
            REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY
        ),
        scoring_contract_id=CRYSTALLIZATION_S0_BALANCED_PRODUCT_V1,
    ) as session:
        instance_hash = session.environment.scenario_instance.initial_state.metadata[
            "crystallization_material_instance_sha256"
        ]
        result = session.execute(_plan(catalyst, solvent)).to_dict()
    final_assay = result["measurement_evidence"][-1]["processed_estimate"]
    return {
        "material_pair": [catalyst, solvent],
        "leaderboard_score": float(result["terminal_summary"]["leaderboard_score"]),
        "metrics": {
            metric: float(final_assay[metric])
            for metric in (
                "yield",
                "selectivity",
                "crystal_yield",
                "crystal_purity",
                "crystal_size",
                "crystal_csd_quality",
                "crystal_fines_fraction",
            )
        },
        "material_instance_sha256": str(instance_hash),
    }


def build_qualification_report(root: Path, world_seeds: tuple[int, ...]) -> dict[str, Any]:
    worlds: list[dict[str, Any]] = []
    for world_seed in world_seeds:
        responses = [
            _execute_pair(world_seed, catalyst, solvent)
            for catalyst, solvent in _MATERIAL_PAIRS
        ]
        scores = [float(item["leaderboard_score"]) for item in responses]
        best_index = int(np.argmax(scores))
        worlds.append(
            {
                "world_seed": world_seed,
                "material_instance_sha256": responses[0][
                    "material_instance_sha256"
                ],
                "standardized_material_responses": responses,
                "winning_material_pair": responses[best_index]["material_pair"],
                "winning_score": scores[best_index],
                "score_range": max(scores) - min(scores),
            }
        )

    replay = _execute_pair(world_seeds[0], 0, 0)
    first = worlds[0]["standardized_material_responses"][0]
    winner_pairs = {
        tuple(int(value) for value in world["winning_material_pair"])
        for world in worlds
    }
    score_ranges = [float(world["score_range"]) for world in worlds]
    instance_hashes = {
        str(world["material_instance_sha256"]) for world in worlds
    }
    checks = {
        "all_scores_finite_and_bounded": all(
            np.isfinite(item["leaderboard_score"])
            and 0.0 <= item["leaderboard_score"] <= 1.0
            for world in worlds
            for item in world["standardized_material_responses"]
        ),
        "deterministic_replay_exact": replay == first,
        "material_instance_varies_across_worlds": len(instance_hashes)
        == len(world_seeds),
        "no_universal_standardized_winner": len(winner_pairs) >= 2,
        "minimum_within_world_material_score_range_at_least_0_05": min(
            score_ranges
        )
        >= 0.05,
    }
    family = crystallization_material_family(
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY
    )
    return {
        "schema_version": QUALIFICATION_VERSION,
        "status": (
            "qualified_for_development_pilots"
            if all(checks.values())
            else "qualification_failed"
        ),
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "material_family": family.to_dict(),
        "scoring_contract_id": CRYSTALLIZATION_S0_BALANCED_PRODUCT_V1,
        "world_split": "public-test",
        "world_seeds": list(world_seeds),
        "standardized_design": {
            "material_pair_count": len(_MATERIAL_PAIRS),
            "continuous_vector": [
                0.55,
                0.60,
                0.60,
                0.60,
                "categorical",
                0.55,
                "categorical",
                0.50,
                0.45,
                0.65,
            ],
            "paired_observation_coordinate_across_material_pairs": True,
        },
        "checks": checks,
        "aggregate": {
            "distinct_standardized_winner_count": len(winner_pairs),
            "distinct_standardized_winners": [list(pair) for pair in sorted(winner_pairs)],
            "minimum_score_range": min(score_ranges),
            "median_score_range": statistics.median(score_ranges),
            "maximum_score_range": max(score_ranges),
        },
        "world_reports": worlds,
        "source_contract_sha256": _source_hashes(root),
        "interpretation": (
            "This is a deterministic simulator qualification of material relevance and "
            "world-fixed identity. It is not an agent benchmark result and must not be "
            "reported as blind optimization performance."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--world-seeds", default="0,1,2,3,4")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    world_seeds = tuple(int(value) for value in args.world_seeds.split(","))
    if not world_seeds:
        raise ValueError("at least one world seed is required")
    report = build_qualification_report(root, world_seeds)
    output = root / args.output
    write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "checks": report["checks"],
                "aggregate": report["aggregate"],
                "output": str(output),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
