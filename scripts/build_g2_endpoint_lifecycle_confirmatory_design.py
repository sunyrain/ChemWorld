"""Build outcome-blind world qualification, schedule, and power artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import chi2
from scripts import run_g2_autonomous_material_matrix as base

from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PILOT_CONFIG = (
    ROOT / "configs/benchmark/g2_autonomous_electrochemical_material_seed1_seed3_r5_v0.5_dev.json"
)
DEFAULT_QUALIFICATION_OUTPUT = (
    ROOT / "configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6_world_qualification.json"
)
DEFAULT_SCHEDULE_OUTPUT = (
    ROOT / "configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6_schedule.json"
)
DEFAULT_POWER_OUTPUT = ROOT / "configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6_power.json"
RANDOMIZATION_SALT = "chemworld-g2-v0.6-confirmatory-world-randomization-2026-08-02"
CANDIDATE_WORLD_SEEDS = tuple(range(10, 50))
SELECTED_WORLD_COUNT = 16
REPLICATE_IDS = ("r01", "r02", "r03", "r04", "r05")
AGENT_SEED_BASE = 600_000


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object required: {path}")
    return payload


def _rank_key(*parts: Any) -> str:
    joined = ":".join(str(part) for part in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def _qualify_worlds(protocol: Mapping[str, Any]) -> dict[str, Any]:
    card = base._campaign_card(protocol, qualification=False)
    limits = base._method_limits(protocol, qualification=False)
    conditions = {str(item["condition_id"]): item for item in protocol["paired_conditions"]}
    rows: list[dict[str, Any]] = []
    for seed in CANDIDATE_WORLD_SEEDS:
        contracts: dict[str, dict[str, Any]] = {}
        for condition_id in (
            "anonymous_nominal_properties",
            "opaque_codes",
        ):
            cell = {
                "cell_id": f"qualification-{seed}-{condition_id}",
                "world_seed": seed,
                "condition_id": condition_id,
                "material_information": deepcopy(
                    dict(conditions[condition_id]["material_information"])
                ),
            }
            contracts[condition_id] = base._inspect_cell_environment(
                protocol=protocol,
                cell=cell,
                card=card,
                operation_limit=int(limits["operation_limit"]),
            )
        nominal = contracts["anonymous_nominal_properties"]
        opaque = contracts["opaque_codes"]
        evaluator_fields = (
            "world_id",
            "mechanism_hash",
            "electrochemical_material_family_id",
            "electrochemical_material_family_sha256",
            "electrochemical_material_instance_sha256",
            "observation_noise_mode",
            "observation_noise_namespace",
        )
        public_fields = (
            "task_contract_hash",
            "runtime_profile_hash",
            "scoring_contract_hash",
            "observation_contract_hash",
            "workflow_mode",
        )
        checks = {
            "both_arms_instantiate": True,
            "finite_bounded_score_contract": all(
                isinstance(item, str) and bool(item)
                for item in (
                    nominal["public_contract"].get("scoring_contract_hash"),
                    opaque["public_contract"].get("scoring_contract_hash"),
                )
            ),
            "paired_evaluator_identity": all(
                nominal["evaluator_identity"].get(field) == opaque["evaluator_identity"].get(field)
                for field in evaluator_fields
            ),
            "paired_public_physics": all(
                nominal["public_contract"].get(field) == opaque["public_contract"].get(field)
                for field in public_fields
            ),
            "k6_resource_lifecycle_available": (
                int(card.vessel_start_limit) == 6
                and int(card.final_assay_limit) == 6
                and int(card.operation_attempt_limit) == 144
            ),
            "agent_outcome_inspected": False,
        }
        passed = all(value for key, value in checks.items() if key != "agent_outcome_inspected")
        rows.append(
            {
                "world_seed": seed,
                "checks": checks,
                "passed": passed,
                "pair_contract_sha256": canonical_json_sha256(contracts),
            }
        )
    qualified = [int(row["world_seed"]) for row in rows if row["passed"]]
    ranked = sorted(
        qualified,
        key=lambda seed: _rank_key(RANDOMIZATION_SALT, "world", seed),
    )
    selected = ranked[:SELECTED_WORLD_COUNT]
    report: dict[str, Any] = {
        "schema_version": "chemworld-g2-outcome-blind-world-qualification-0.1",
        "status": "passed",
        "candidate_world_seeds": list(CANDIDATE_WORLD_SEEDS),
        "development_world_seeds_excluded": list(range(10)),
        "qualification_uses_agent_scores_or_trajectories": False,
        "qualification_rules": [
            "environment instantiates in both material-information arms",
            "score and runtime contracts are finite and bound",
            "arms share physical evaluator and keyed observation identities",
            "the K=6 resource lifecycle is available",
        ],
        "randomization": {
            "algorithm": "ascending SHA-256(salt + ':world:' + decimal_seed)",
            "salt": RANDOMIZATION_SALT,
            "ranked_qualified_world_seeds": ranked,
            "selected_world_count": SELECTED_WORLD_COUNT,
            "selected_world_seeds": selected,
            "replacement_order": ranked[SELECTED_WORLD_COUNT:],
        },
        "campaign_resource_card_sha256": card.card_sha256,
        "rows": rows,
    }
    report["report_sha256"] = canonical_json_sha256(report)
    return report


def _schedule(selected_worlds: Sequence[int]) -> dict[str, Any]:
    world_ranks = {seed: index for index, seed in enumerate(selected_worlds)}
    blocks: list[dict[str, Any]] = []
    pair_order = 0
    for time_block, replicate_id in enumerate(REPLICATE_IDS, start=1):
        round_worlds = sorted(
            selected_worlds,
            key=lambda seed: _rank_key(
                RANDOMIZATION_SALT,
                "time-block",
                time_block,
                seed,
            ),
        )
        for seed in round_worlds:
            pair_order += 1
            nominal_first = (world_ranks[seed] + time_block - 1) % 2 == 0
            order = (
                ["anonymous_nominal_properties", "opaque_codes"]
                if nominal_first
                else ["opaque_codes", "anonymous_nominal_properties"]
            )
            blocks.append(
                {
                    "pair_order": pair_order,
                    "time_block": time_block,
                    "world_seed": int(seed),
                    "replicate_id": replicate_id,
                    "agent_seed": AGENT_SEED_BASE + int(seed) * 100 + time_block,
                    "condition_order": order,
                }
            )
    report: dict[str, Any] = {
        "schema_version": "chemworld-g2-confirmatory-pair-schedule-0.1",
        "randomization_salt": RANDOMIZATION_SALT,
        "world_seeds": list(selected_worlds),
        "replicate_ids": list(REPLICATE_IDS),
        "agent_seed_base": AGENT_SEED_BASE,
        "arm_adjacency": "the two arms of every pair execute sequentially within one worker",
        "time_block_barrier": (
            "all pairs in a replicate block finalize before the next block starts"
        ),
        "pair_blocks": blocks,
    }
    report["schedule_sha256"] = canonical_json_sha256(report)
    return report


def _power_report(*, simulations: int = 20_000) -> dict[str, Any]:
    rng = np.random.default_rng(606_202_608_02)
    worlds = SELECTED_WORLD_COUNT
    pairs = len(REPLICATE_IDS)
    true_sigma = 0.20
    margin = 0.15
    successes = 0
    coverage_passes = 0
    complete_counts: list[int] = []
    for _ in range(simulations):
        retained_flat = np.zeros(worlds * pairs, dtype=bool)
        retained_flat[rng.choice(worlds * pairs, size=64, replace=False)] = True
        retained = retained_flat.reshape((worlds, pairs))
        complete = int(retained.sum())
        worlds_with_three = int((retained.sum(axis=1) >= 3).sum())
        coverage = complete >= math.ceil(0.80 * worlds * pairs) and worlds_with_three >= 10
        complete_counts.append(complete)
        if not coverage:
            continue
        coverage_passes += 1
        residual_df = max(complete - worlds_with_three - 5, 1)
        residual_ss = true_sigma**2 * rng.chisquare(residual_df)
        estimated_variance = residual_ss / residual_df
        lower = math.sqrt(residual_df * estimated_variance / chi2.ppf(0.95, residual_df))
        successes += lower > margin
    report: dict[str, Any] = {
        "schema_version": "chemworld-g2-confirmatory-power-simulation-0.1",
        "status": "passed",
        "random_seed": 60620260802,
        "simulation_count": simulations,
        "design": {
            "world_count": worlds,
            "fresh_pairs_per_world": pairs,
            "planned_pair_count": worlds * pairs,
            "planned_cell_count": worlds * pairs * 2,
            "planned_pair_loss_fraction_sensitivity": 0.20,
            "completed_pairs_in_sensitivity": 64,
            "planning_sigma_unexplained": true_sigma,
            "substantive_margin": margin,
        },
        "approximation": (
            "hierarchical residual-df simulation under an exact 20-percent "
            "pair-loss sensitivity with random missing-pair locations and the "
            "frozen coverage gate; final inference uses REML profile likelihood"
        ),
        "coverage_gate_probability": coverage_passes / simulations,
        "unconditional_success_probability": successes / simulations,
        "conditional_success_probability_given_coverage": successes / max(coverage_passes, 1),
        "completed_pair_count": {
            "mean": float(np.mean(complete_counts)),
            "p05": float(np.quantile(complete_counts, 0.05)),
            "p50": float(np.quantile(complete_counts, 0.50)),
            "p95": float(np.quantile(complete_counts, 0.95)),
        },
        "minimum_unconditional_success_probability": 0.80,
    }
    report["passed"] = report["unconditional_success_probability"] >= 0.80
    report["report_sha256"] = canonical_json_sha256(report)
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-config", type=Path, default=DEFAULT_PILOT_CONFIG)
    parser.add_argument("--qualification-output", type=Path, default=DEFAULT_QUALIFICATION_OUTPUT)
    parser.add_argument("--schedule-output", type=Path, default=DEFAULT_SCHEDULE_OUTPUT)
    parser.add_argument("--power-output", type=Path, default=DEFAULT_POWER_OUTPUT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    protocol = _load_json(args.pilot_config.resolve())
    qualification = _qualify_worlds(protocol)
    selected = qualification["randomization"]["selected_world_seeds"]
    schedule = _schedule(selected)
    power = _power_report()
    if not power["passed"]:
        raise RuntimeError("the ideal confirmatory design did not clear 80-percent power")
    write_json_atomic(args.qualification_output.resolve(), qualification)
    write_json_atomic(args.schedule_output.resolve(), schedule)
    write_json_atomic(args.power_output.resolve(), power)
    print(
        json.dumps(
            {
                "qualification": {
                    "path": str(args.qualification_output.resolve()),
                    "sha256": file_sha256(args.qualification_output.resolve()),
                },
                "schedule": {
                    "path": str(args.schedule_output.resolve()),
                    "sha256": file_sha256(args.schedule_output.resolve()),
                },
                "power": {
                    "path": str(args.power_output.resolve()),
                    "sha256": file_sha256(args.power_output.resolve()),
                },
                "selected_world_seeds": selected,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
