"""Qualify the nominal-prior electrochemical material family with local simulation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc, spearmanr

from chemworld.agents.electrochemical_single_stage import (
    electrochemical_single_stage_parameters_from_unit_vector,
)
from chemworld.agents.static_optimization import StaticOptimizationPlan
from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.static_optimization_execution import (
    StaticOptimizationExperimentSession,
)
from chemworld.world.electrochemical_material_family import (
    NOMINAL_PRIOR_MATERIAL_FAMILY,
    electrochemical_material_family,
)
from chemworld.world.parameters import load_chemworld_parameters
from chemworld.world.scoring import ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2

QUALIFICATION_VERSION = "chemworld-electrochemical-material-family-qualification-0.3"
QUALIFICATION_COHORT_ID = "public-qualification-q-v1"
DEFAULT_QUALIFICATION_SEED_START = 100
DEFAULT_VALIDATION_REPLICATES = 5
_MATERIAL_PAIRS = tuple(itertools.product(range(4), repeat=2))
_MEASUREMENT_SLOTS = (
    "diagnostic-01-ph_meter",
    "diagnostic-02-uvvis",
)
_SOURCE_CONTRACT_PATHS = (
    "src/chemworld/world/electrochemical_material_family.py",
    "src/chemworld/world/parameters.py",
    "src/chemworld/runtime/electrochemical_services.py",
    "src/chemworld/runtime/observation_services.py",
    "src/chemworld/world/scoring.py",
    "scripts/qualify_electrochemical_material_family.py",
)


@dataclass(frozen=True)
class Candidate:
    electrolyte: int
    solvent: int
    continuous: tuple[float, float, float, float]

    def vector(self) -> np.ndarray:
        return np.asarray(
            (
                (self.electrolyte + 0.5) / 4.0,
                (self.solvent + 0.5) / 4.0,
                *self.continuous,
            ),
            dtype=float,
        )


def _plan(candidate: Candidate) -> StaticOptimizationPlan:
    vector = candidate.vector()
    parameters = electrochemical_single_stage_parameters_from_unit_vector(vector)
    return StaticOptimizationPlan(
        experiment_intent=(
            "qualify one anonymous material pair under the fixed-world cell fixture"
        ),
        search_vector=tuple(float(value) for value in vector),
        requested_measurement_slots=_MEASUREMENT_SLOTS,
        measurement_objective=(
            "estimate the best attainable terminal score for this material pair"
        ),
        expected_effect="continuous controls may reveal a material-specific optimum",
        uncertainty=0.5,
        recipe_parameters=parameters,
    )


def _execute_candidates(
    *,
    world_seed: int,
    candidates: list[Candidate],
    experiment_index_offset: int,
) -> list[float]:
    scores: list[float] = []
    with StaticOptimizationExperimentSession(
        task_id="electrochemical-conversion",
        seed=world_seed,
        experiment_horizon=len(candidates),
        experiment_index_offset=experiment_index_offset,
        observation_seed=world_seed + 80_000,
        observation_noise_namespace=(f"material-family-qualification-world-{world_seed:04d}"),
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        scoring_contract_id=ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2,
    ) as session:
        for candidate in candidates:
            result = session.execute(_plan(candidate))
            scores.append(float(result.terminal_summary["leaderboard_score"]))
    return scores


def _standardized_material_responses(
    *,
    world_seed: int,
    experiment_index_offset: int,
) -> list[dict[str, Any]]:
    candidates = [
        Candidate(electrolyte, solvent, (0.55, 0.55, 0.55, 0.55))
        for electrolyte, solvent in _MATERIAL_PAIRS
    ]
    rows: list[dict[str, Any]] = []
    with StaticOptimizationExperimentSession(
        task_id="electrochemical-conversion",
        seed=world_seed,
        experiment_horizon=len(candidates),
        experiment_index_offset=experiment_index_offset,
        observation_seed=world_seed + 90_000,
        observation_noise_namespace=(f"material-family-standardized-world-{world_seed:04d}"),
        electrochemical_material_family_id=NOMINAL_PRIOR_MATERIAL_FAMILY,
        scoring_contract_id=ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2,
    ) as session:
        for candidate in candidates:
            result = session.execute(_plan(candidate)).to_dict()
            final_assay = result["measurement_evidence"][-1]["processed_estimate"]
            rows.append(
                {
                    "material_pair": [candidate.electrolyte, candidate.solvent],
                    "metrics": {
                        metric: float(final_assay[metric])
                        for metric in (
                            "ohmic_efficiency",
                            "transport_efficiency",
                            "faradaic_efficiency",
                            "electrochemical_selectivity",
                        )
                    },
                }
            )
    return rows


def _initial_continuous_design(count: int, seed: int) -> np.ndarray:
    if count < 4:
        raise ValueError("initial design count must be at least four")
    power = math.ceil(math.log2(count))
    design = qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)[:count]
    anchors = np.asarray(
        (
            (0.50, 0.55, 0.55, 0.50),
            (0.80, 0.65, 0.80, 0.80),
            (0.80, 0.80, 0.55, 0.75),
            (0.35, 0.45, 0.75, 0.65),
        ),
        dtype=float,
    )
    return np.vstack((design, anchors))


def _descriptor_prior_scores() -> np.ndarray:
    family = electrochemical_material_family(NOMINAL_PRIOR_MATERIAL_FAMILY)
    electrolyte_raw = np.asarray(
        [
            (
                math.log10(row["electrolyte_conductivity_S_m"]),
                math.log10(row["diffusivity_m2_s"]),
                -math.log10(row["diffusion_layer_thickness_m"]),
            )
            for row in family.electrolyte_profiles
        ],
        dtype=float,
    )
    solvent_raw = np.asarray(
        [
            (
                math.log10(row["conductivity_multiplier"]),
                math.log10(row["diffusivity_multiplier"]),
            )
            for row in family.solvent_profiles
        ],
        dtype=float,
    )

    def normalize(values: np.ndarray) -> np.ndarray:
        minimum = values.min(axis=0)
        span = values.max(axis=0) - minimum
        return np.divide(
            values - minimum,
            span,
            out=np.zeros_like(values),
            where=span > 0.0,
        )

    electrolyte_transport = normalize(electrolyte_raw).mean(axis=1)
    solvent_transport = normalize(solvent_raw).mean(axis=1)
    electrolyte_chemistry = normalize(
        np.asarray(
            [
                (
                    row["acid_concentration_mol_L"],
                    -row["electrolyte_acid_pka"],
                    -math.log10(row["electrolyte_ksp"]),
                )
                for row in family.electrolyte_profiles
            ],
            dtype=float,
        )
    ).mean(axis=1)
    solvent_chemistry = normalize(
        np.asarray(
            [
                (
                    row["proton_activity_multiplier"],
                    -math.log10(row["ksp_multiplier"]),
                    row["diffusivity_multiplier"],
                )
                for row in family.solvent_profiles
            ],
            dtype=float,
        )
    ).mean(axis=1)
    return np.asarray(
        [
            0.65 * (electrolyte_transport[electrolyte_id] + solvent_transport[solvent_id])
            + 0.35 * (electrolyte_chemistry[electrolyte_id] + solvent_chemistry[solvent_id])
            for electrolyte_id, solvent_id in _MATERIAL_PAIRS
        ],
        dtype=float,
    )


def _mechanistic_predictor_vectors() -> dict[str, np.ndarray]:
    family = electrochemical_material_family(NOMINAL_PRIOR_MATERIAL_FAMILY)
    values: dict[str, list[float]] = {
        "ohmic_efficiency": [],
        "transport_efficiency": [],
    }
    for electrolyte, solvent in _MATERIAL_PAIRS:
        electrolyte_row = family.electrolyte_profiles[electrolyte]
        solvent_row = family.solvent_profiles[solvent]
        relative_diffusivity = solvent_row["diffusivity_multiplier"]
        values["ohmic_efficiency"].append(
            electrolyte_row["electrolyte_conductivity_S_m"] * solvent_row["conductivity_multiplier"]
        )
        values["transport_efficiency"].append(
            electrolyte_row["diffusivity_m2_s"]
            * relative_diffusivity**1.5
            / electrolyte_row["diffusion_layer_thickness_m"]
        )
    return {
        metric: np.asarray(metric_values, dtype=float) for metric, metric_values in values.items()
    }


def _derangements() -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in itertools.permutations(range(4))
        if all(index != source for index, source in enumerate(permutation))
    )


def _world_scan(
    world_seed: int,
    initial_count: int,
    refinement_count: int,
    validation_replicates: int,
) -> dict[str, Any]:
    hidden_world = load_chemworld_parameters("public-test", world_seed)
    initial_continuous = _initial_continuous_design(initial_count, world_seed + 13_000)
    initial_candidates = [
        Candidate(electrolyte, solvent, tuple(float(value) for value in continuous))
        for electrolyte, solvent in _MATERIAL_PAIRS
        for continuous in initial_continuous
    ]
    initial_scores = _execute_candidates(
        world_seed=world_seed,
        candidates=initial_candidates,
        experiment_index_offset=0,
    )
    by_pair: dict[tuple[int, int], list[tuple[float, tuple[float, ...]]]] = {
        pair: [] for pair in _MATERIAL_PAIRS
    }
    for candidate, score in zip(initial_candidates, initial_scores, strict=True):
        by_pair[(candidate.electrolyte, candidate.solvent)].append((score, candidate.continuous))

    rng = np.random.default_rng(world_seed + 29_000)
    refinement_candidates: list[Candidate] = []
    if refinement_count:
        for electrolyte, solvent in _MATERIAL_PAIRS:
            _score, center = max(by_pair[(electrolyte, solvent)], key=lambda row: row[0])
            refinements = np.clip(
                rng.normal(
                    np.asarray(center, dtype=float),
                    0.085,
                    size=(refinement_count, 4),
                ),
                0.0,
                1.0,
            )
            refinement_candidates.extend(
                Candidate(
                    electrolyte,
                    solvent,
                    tuple(float(value) for value in continuous),
                )
                for continuous in refinements
            )
        refinement_scores = _execute_candidates(
            world_seed=world_seed,
            candidates=refinement_candidates,
            experiment_index_offset=len(initial_candidates),
        )
        for candidate, score in zip(refinement_candidates, refinement_scores, strict=True):
            by_pair[(candidate.electrolyte, candidate.solvent)].append(
                (score, candidate.continuous)
            )

    incumbent_candidates: list[Candidate] = []
    exploration_best_by_pair: dict[tuple[int, int], float] = {}
    for electrolyte, solvent in _MATERIAL_PAIRS:
        best_score, best_continuous = max(by_pair[(electrolyte, solvent)], key=lambda row: row[0])
        incumbent_candidates.append(Candidate(electrolyte, solvent, best_continuous))
        exploration_best_by_pair[(electrolyte, solvent)] = float(best_score)

    validation_candidates = [
        candidate
        for candidate in incumbent_candidates
        for _replicate in range(validation_replicates)
    ]
    validation_scores = _execute_candidates(
        world_seed=world_seed,
        candidates=validation_candidates,
        experiment_index_offset=len(initial_candidates) + len(refinement_candidates),
    )
    rows = []
    validation_by_pair: dict[tuple[int, int], list[float]] = {}
    for pair_index, candidate in enumerate(incumbent_candidates):
        start = pair_index * validation_replicates
        replicate_scores = [
            float(value)
            for value in validation_scores[start : start + validation_replicates]
        ]
        pair = (candidate.electrolyte, candidate.solvent)
        validation_by_pair[pair] = replicate_scores
        rows.append(
            {
                "material_pair": list(pair),
                "best_score": float(np.mean(replicate_scores)),
                "validation_score_std": float(np.std(replicate_scores, ddof=1)),
                "validation_replicates": validation_replicates,
                "validation_scores": replicate_scores,
                "exploration_best_score": exploration_best_by_pair[pair],
                "best_recipe_parameters": (
                    electrochemical_single_stage_parameters_from_unit_vector(candidate.vector())
                ),
            }
        )
    rows.sort(key=lambda row: row["best_score"], reverse=True)
    best_score = float(rows[0]["best_score"])
    winner_pair = tuple(int(value) for value in rows[0]["material_pair"])
    replicate_winners = [
        max(
            _MATERIAL_PAIRS,
            key=lambda pair: validation_by_pair[pair][replicate],
        )
        for replicate in range(validation_replicates)
    ]
    standardized_responses = _standardized_material_responses(
        world_seed=world_seed,
        experiment_index_offset=(
            len(initial_candidates) + len(refinement_candidates) + len(validation_candidates)
        ),
    )
    return {
        "world_seed": world_seed,
        "world_fixture": {
            "electrode_gap_m": hidden_world.electrochemical_electrode_gap_m,
            "electrode_area_m2": hidden_world.electrochemical_electrode_area_m2,
            "base_contact_resistance_ohm": (
                hidden_world.electrochemical_base_contact_resistance_ohm
            ),
            "exchange_current_density_A_m2": (
                hidden_world.electrochemical_exchange_current_density_A_m2
            ),
        },
        "winner": rows[0]["material_pair"],
        "best_score": best_score,
        "top1_top2_validated_gap": best_score - float(rows[1]["best_score"]),
        "winner_replicate_stability": (
            sum(pair == winner_pair for pair in replicate_winners) / validation_replicates
        ),
        "replicate_winner_probabilities": {
            f"E{pair[0]}-S{pair[1]}": replicate_winners.count(pair) / validation_replicates
            for pair in _MATERIAL_PAIRS
            if pair in replicate_winners
        },
        "near_optimal_pairs_0p02": [
            row["material_pair"] for row in rows if best_score - float(row["best_score"]) <= 0.02
        ],
        "material_pairs": rows,
        "standardized_material_responses": standardized_responses,
        "physical_experiment_count": (
            len(initial_candidates)
            + len(refinement_candidates)
            + len(validation_candidates)
            + len(standardized_responses)
        ),
    }


def _spearman(left: np.ndarray, right: np.ndarray) -> float:
    value = float(spearmanr(left, right).statistic)
    return value if math.isfinite(value) else 0.0


def _source_contract_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parents[1]
    return {
        relative_path: hashlib.sha256((root / relative_path).read_bytes()).hexdigest()
        for relative_path in _SOURCE_CONTRACT_PATHS
    }


def _summarize(worlds: list[dict[str, Any]]) -> dict[str, Any]:
    prior = _descriptor_prior_scores()
    score_matrix = np.asarray(
        [
            [
                next(
                    float(row["best_score"])
                    for row in world["material_pairs"]
                    if tuple(row["material_pair"]) == pair
                )
                for pair in _MATERIAL_PAIRS
            ]
            for world in worlds
        ],
        dtype=float,
    )
    nominal_correlations = [_spearman(prior, row) for row in score_matrix]
    derangements = _derangements()
    shuffled_correlations: list[float] = []
    for electrolyte_permutation in derangements:
        for solvent_permutation in derangements:
            shuffled = np.asarray(
                [
                    prior[
                        _MATERIAL_PAIRS.index(
                            (
                                electrolyte_permutation[electrolyte],
                                solvent_permutation[solvent],
                            )
                        )
                    ]
                    for electrolyte, solvent in _MATERIAL_PAIRS
                ],
                dtype=float,
            )
            shuffled_correlations.extend(_spearman(shuffled, row) for row in score_matrix)

    mechanistic_predictors = _mechanistic_predictor_vectors()
    mechanistic_correlations: dict[str, list[float]] = {
        metric: [] for metric in mechanistic_predictors
    }
    shuffled_mechanistic_correlations: dict[str, list[float]] = {
        metric: [] for metric in mechanistic_predictors
    }
    for world in worlds:
        response_by_pair = {
            tuple(row["material_pair"]): row["metrics"]
            for row in world["standardized_material_responses"]
        }
        for metric, predictor in mechanistic_predictors.items():
            response = np.asarray(
                [response_by_pair[pair][metric] for pair in _MATERIAL_PAIRS],
                dtype=float,
            )
            mechanistic_correlations[metric].append(_spearman(predictor, response))
            for electrolyte_permutation in derangements:
                for solvent_permutation in derangements:
                    shuffled = np.asarray(
                        [
                            predictor[
                                _MATERIAL_PAIRS.index(
                                    (
                                        electrolyte_permutation[electrolyte],
                                        solvent_permutation[solvent],
                                    )
                                )
                            ]
                            for electrolyte, solvent in _MATERIAL_PAIRS
                        ],
                        dtype=float,
                    )
                    shuffled_mechanistic_correlations[metric].append(_spearman(shuffled, response))
    mechanistic_mean = float(
        np.mean([value for values in mechanistic_correlations.values() for value in values])
    )
    shuffled_mechanistic_mean = float(
        np.mean(
            [value for values in shuffled_mechanistic_correlations.values() for value in values]
        )
    )

    winner_counts: dict[str, int] = {}
    electrolyte_winner_counts = {f"E{index}": 0 for index in range(4)}
    solvent_winner_counts = {f"S{index}": 0 for index in range(4)}
    for world in worlds:
        key = f"E{world['winner'][0]}-S{world['winner'][1]}"
        winner_counts[key] = winner_counts.get(key, 0) + 1
        electrolyte_winner_counts[f"E{world['winner'][0]}"] += 1
        solvent_winner_counts[f"S{world['winner'][1]}"] += 1

    near_optimal_electrolytes = {
        int(pair[0])
        for world in worlds
        for pair in world["near_optimal_pairs_0p02"]
    }
    near_optimal_solvents = {
        int(pair[1])
        for world in worlds
        for pair in world["near_optimal_pairs_0p02"]
    }
    ambiguous_worlds = [
        world for world in worlds if float(world["winner_replicate_stability"]) < 0.60
    ]

    dominated_pairs = []
    for candidate_index, candidate in enumerate(_MATERIAL_PAIRS):
        for challenger_index, challenger in enumerate(_MATERIAL_PAIRS):
            if candidate == challenger:
                continue
            candidate_scores = score_matrix[:, candidate_index]
            challenger_scores = score_matrix[:, challenger_index]
            if np.all(challenger_scores >= candidate_scores) and np.any(
                challenger_scores > candidate_scores
            ):
                dominated_pairs.append(
                    {
                        "material_pair": list(candidate),
                        "dominated_by": list(challenger),
                    }
                )
                break

    component_envelopes = {
        "electrolyte": np.asarray(
            [
                [
                    max(
                        score_matrix[world_index, pair_index]
                        for pair_index, pair in enumerate(_MATERIAL_PAIRS)
                        if pair[0] == electrolyte
                    )
                    for electrolyte in range(4)
                ]
                for world_index in range(len(worlds))
            ],
            dtype=float,
        ),
        "solvent": np.asarray(
            [
                [
                    max(
                        score_matrix[world_index, pair_index]
                        for pair_index, pair in enumerate(_MATERIAL_PAIRS)
                        if pair[1] == solvent
                    )
                    for solvent in range(4)
                ]
                for world_index in range(len(worlds))
            ],
            dtype=float,
        ),
    }
    dominated_components: dict[str, list[dict[str, int]]] = {}
    for component_kind, envelopes in component_envelopes.items():
        dominated_components[component_kind] = []
        for candidate in range(4):
            for challenger in range(4):
                if candidate == challenger:
                    continue
                if np.all(envelopes[:, challenger] >= envelopes[:, candidate]) and np.any(
                    envelopes[:, challenger] > envelopes[:, candidate]
                ):
                    dominated_components[component_kind].append(
                        {"material": candidate, "dominated_by": challenger}
                    )
                    break

    fixture_fields = tuple(worlds[0]["world_fixture"])
    fixture_ranges = {
        field: [
            min(float(world["world_fixture"][field]) for world in worlds),
            max(float(world["world_fixture"][field]) for world in worlds),
        ]
        for field in fixture_fields
    }
    return {
        "world_count": len(worlds),
        "world_fixture_ranges": fixture_ranges,
        "distinct_winner_count": len(winner_counts),
        "winner_counts": winner_counts,
        "electrolyte_winner_counts": electrolyte_winner_counts,
        "solvent_winner_counts": solvent_winner_counts,
        "minimum_world_best_score": float(score_matrix.max(axis=1).min()),
        "median_near_optimal_pair_count_0p02": float(
            np.median([len(world["near_optimal_pairs_0p02"]) for world in worlds])
        ),
        "optimized_score_transport_heuristic_spearman_mean": float(np.mean(nominal_correlations)),
        "optimized_score_transport_heuristic_spearman_by_world": (nominal_correlations),
        "optimized_score_shuffled_heuristic_spearman_mean": float(np.mean(shuffled_correlations)),
        "optimized_score_shuffled_heuristic_spearman_mean_absolute": float(
            np.mean(np.abs(shuffled_correlations))
        ),
        "nominal_mechanistic_spearman_mean": mechanistic_mean,
        "nominal_mechanistic_spearman_by_metric": {
            metric: float(np.mean(values)) for metric, values in mechanistic_correlations.items()
        },
        "shuffled_mechanistic_spearman_mean": shuffled_mechanistic_mean,
        "outcome_adjacent_channels_excluded_from_mechanistic_gate": [
            "faradaic_efficiency",
            "electrochemical_selectivity",
        ],
        "minimum_winner_replicate_stability": float(
            min(float(world["winner_replicate_stability"]) for world in worlds)
        ),
        "ambiguous_world_count": len(ambiguous_worlds),
        "near_optimal_electrolyte_coverage": sorted(near_optimal_electrolytes),
        "near_optimal_solvent_coverage": sorted(near_optimal_solvents),
        "median_top1_top2_validated_gap": float(
            np.median([float(world["top1_top2_validated_gap"]) for world in worlds])
        ),
        "dominated_material_pairs": dominated_pairs,
        "dominated_material_components": dominated_components,
        "qualification_checks": {
            "no_universal_winner": max(winner_counts.values()) < len(worlds),
            "at_least_four_distinct_winners": len(winner_counts) >= 4,
            "no_material_component_globally_dominated": not any(dominated_components.values()),
            "at_least_three_electrolytes_win": sum(
                count > 0 for count in electrolyte_winner_counts.values()
            )
            >= 3,
            "at_least_three_solvents_win": sum(
                count > 0 for count in solvent_winner_counts.values()
            )
            >= 3,
            "nominal_mechanistic_descriptors_positive_on_average": (mechanistic_mean > 0.10),
            "nominal_mechanistic_descriptors_exceed_shuffled": (
                mechanistic_mean > shuffled_mechanistic_mean
            ),
            "world_score_floor_above_0p20": float(score_matrix.max(axis=1).min()) > 0.20,
            "all_material_components_enter_an_epsilon_optimal_set": (
                near_optimal_electrolytes == set(range(4))
                and near_optimal_solvents == set(range(4))
            ),
            "ambiguous_worlds_are_reported_as_epsilon_optimal_sets": all(
                float(world["top1_top2_validated_gap"]) <= 0.02
                and len(world["near_optimal_pairs_0p02"]) >= 2
                and abs(sum(world["replicate_winner_probabilities"].values()) - 1.0) < 1.0e-12
                for world in ambiguous_worlds
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world-seed", action="append", type=int)
    parser.add_argument("--world-count", type=int, default=15)
    parser.add_argument("--initial-count", type=int, default=32)
    parser.add_argument("--refinement-count", type=int, default=8)
    parser.add_argument("--validation-replicates", type=int, default=DEFAULT_VALIDATION_REPLICATES)
    parser.add_argument("--allow-development-seeds", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    world_seeds = list(
        args.world_seed
        or range(
            DEFAULT_QUALIFICATION_SEED_START,
            DEFAULT_QUALIFICATION_SEED_START + args.world_count,
        )
    )
    if not world_seeds:
        raise ValueError("at least one world seed is required")
    if not args.allow_development_seeds and any(
        seed < DEFAULT_QUALIFICATION_SEED_START for seed in world_seeds
    ):
        raise ValueError(
            f"qualification seeds must be >= {DEFAULT_QUALIFICATION_SEED_START}; "
            "use --allow-development-seeds only for non-claimable debugging"
        )
    if args.validation_replicates < 3:
        raise ValueError("validation-replicates must be at least three")
    worker_arguments = [
        (seed, args.initial_count, args.refinement_count, args.validation_replicates)
        for seed in world_seeds
    ]
    if args.workers == 1:
        worlds = [_world_scan(*arguments) for arguments in worker_arguments]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            worlds = list(executor.map(_world_scan_star, worker_arguments))
    worlds.sort(key=lambda row: int(row["world_seed"]))
    family = electrochemical_material_family(NOMINAL_PRIOR_MATERIAL_FAMILY)
    summary = _summarize(worlds)
    report = {
        "schema_version": QUALIFICATION_VERSION,
        "qualification_cohort_id": QUALIFICATION_COHORT_ID,
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "qualification_pass": all(summary["qualification_checks"].values()),
        "source_contract_sha256": _source_contract_hashes(),
        "world_seeds": world_seeds,
        "material_family": family.to_dict(),
        "search_contract": {
            "material_pair_count": len(_MATERIAL_PAIRS),
            "initial_continuous_design_count_per_pair": args.initial_count + 4,
            "local_refinement_count_per_pair": args.refinement_count,
            "validation_replicates_per_pair": args.validation_replicates,
            "standardized_mechanistic_probe_count_per_world": len(_MATERIAL_PAIRS),
            "continuous_design": "scrambled_sobol_plus_four_fixed_anchors",
            "refinement": "bounded_gaussian_around_pair_incumbent",
            "observation_noise": "keyed_local_simulation",
        },
        "summary": summary,
        "worlds": worlds,
    }
    if args.output is not None:
        write_json_atomic(args.output, report)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


def _world_scan_star(arguments: tuple[int, int, int, int]) -> dict[str, Any]:
    return _world_scan(*arguments)


if __name__ == "__main__":
    main()
