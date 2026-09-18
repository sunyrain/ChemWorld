#!/usr/bin/env python3
"""Execute one sealed five-World Experiment 1 confirmation locus in its own process."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np
from scripts import run_experiment_1_c_qualification as c_runner
from scripts import run_experiment_1_ec_qualification as ec_runner
from scripts import run_experiment_1_ec_qualification_repair as ec_repair_runner
from scripts import run_experiment_1_pa_qualification as pa_runner
from scripts import run_experiment_1_rx_qualification as rx_runner
from scripts import run_work_ii_structural_candidate_qualification as structural_runner

from chemworld.agents.task_recipes import electrochemical_recipe_parameters_from_unit_vector
from chemworld.eval.experiment_1_confirmation import (
    ELIGIBLE_LOCI,
    SOURCE_CONTRACTS,
    resolve_source_contract,
    validate_public_contract,
    validate_secret_plan,
)
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_electrochemical_matched_prior_qualification import (
    _context_vector as ec_context_vector,
)
from chemworld.eval.work_ii_matched_prior_qualification import _unscale
from chemworld.eval.work_ii_structural_candidate_qualification import candidate_specs

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _keyed_normal(namespace: str, *parts: object) -> float:
    left = hashlib.sha256(
        ":".join((namespace, *(str(part) for part in parts), "left")).encode()
    ).digest()
    right = hashlib.sha256(
        ":".join((namespace, *(str(part) for part in parts), "right")).encode()
    ).digest()
    u1 = max(int.from_bytes(left[:8], "big") / float(2**64), 1.0e-15)
    u2 = int.from_bytes(right[:8], "big") / float(2**64)
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def _noisy_evaluator(
    base: type, namespace: str, sigma_by_world: dict[int, float], metrics: tuple[str, ...]
):
    class ConfirmationEvaluator(base):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self._confirmation_world_seed = int(kwargs["world_seed"])
            super().__init__(*args, **kwargs)

        def evaluate(self, vector: Any, *, phase: str, extra: dict[str, Any]) -> dict[str, Any]:
            row = super().evaluate(vector, phase=phase, extra=extra)
            sigma = float(sigma_by_world[self._confirmation_world_seed])
            query_id = str(extra["query_id"])
            if row.get("status") == "completed":
                for metric in metrics:
                    value = row.get(metric)
                    if isinstance(value, int | float) and not isinstance(value, bool):
                        noisy = float(value) + sigma * _keyed_normal(
                            namespace,
                            self._confirmation_world_seed,
                            query_id,
                            metric,
                        )
                        row[metric] = min(1.0, max(0.0, noisy))
            seed_digest = hashlib.sha256(
                f"{namespace}:{self._confirmation_world_seed}:{query_id}".encode()
            ).hexdigest()
            row["observation_noise_namespace"] = namespace
            row["observation_seed_commitment"] = seed_digest
            row["confirmation_noise_sigma"] = sigma
            return row

    return ConfirmationEvaluator


def _ec_surface(context: dict[str, Any], coordinates: dict[str, Any]) -> list[dict[str, Any]]:
    base = ec_context_vector(context)
    rows = []
    for grid_i, potential in enumerate(coordinates["potential_coordinates"]):
        for grid_j, current in enumerate(coordinates["current_coordinates"]):
            vector = np.array(base, copy=True)
            vector[6] = float(potential)
            vector[7] = float(current)
            params = electrochemical_recipe_parameters_from_unit_vector(vector)
            rows.append(
                {
                    "query_id": f"p{grid_i:02d}-i{grid_j:02d}",
                    "grid_i": grid_i,
                    "grid_j": grid_j,
                    "split": "fit" if grid_i % 2 == 0 and grid_j % 2 == 0 else "held_out",
                    "potential_coordinate": float(potential),
                    "current_coordinate": float(current),
                    "controlled_potential_V": float(params["controlled_potential_V"]),
                    "controlled_current_mA": float(params["controlled_current_mA"]),
                    "vector": vector.tolist(),
                }
            )
    return rows


def _rx_surface(
    context: dict[str, Any],
    coordinates: dict[str, Any],
    original_surface: Any,
) -> list[dict[str, Any]]:
    base = original_surface(context)[0]["vector"]
    tail = list(base[2:])
    rows = []
    for grid_i, temperature in enumerate(coordinates["temperature_grid_K"]):
        for grid_j, duration in enumerate(coordinates["duration_grid_s"]):
            rows.append(
                {
                    "query_id": f"t{grid_i:02d}-d{grid_j:02d}",
                    "grid_i": grid_i,
                    "grid_j": grid_j,
                    "split": "fit" if grid_i % 2 == 0 and grid_j % 2 == 0 else "held_out",
                    "temperature_K": float(temperature),
                    "duration_s": float(duration),
                    "vector": [
                        _unscale(float(temperature), 250.0, 470.0),
                        _unscale(float(duration), 1.0, 14_400.0),
                        *tail,
                    ],
                }
            )
    return rows


def _ec_structural_queries(
    contract: dict[str, Any], coordinates: dict[str, Any]
) -> list[dict[str, Any]]:
    locus = contract["loci"]["structural"]
    spec = candidate_specs()[str(locus["candidate_id"])]
    axis_a, axis_b = spec["axis_names"]
    levels_a = coordinates["potential_levels_V"]
    levels_b = coordinates["current_levels_mA"]
    rows: list[dict[str, Any]] = []
    for axis_a_index, axis_a_value in enumerate(levels_a):
        for axis_b_index, axis_b_value in enumerate(levels_b):
            rows.append(
                {
                    "query_id": f"a{axis_a_index}-b{axis_b_index}",
                    "phase": "main_grid",
                    "axis_a_index": axis_a_index,
                    "axis_b_index": axis_b_index,
                    "feature_values": {
                        **spec["fixed_context"],
                        axis_a: axis_a_value,
                        axis_b: axis_b_value,
                    },
                    "metric_ids": list(spec["metrics"]),
                }
            )
    for group_index, (axis_a_index, axis_b_index) in enumerate(locus["validation_groups"]):
        for replicate in range(1, int(locus["validation_replicates"]) + 1):
            rows.append(
                {
                    "query_id": f"validation-g{group_index}-r{replicate}",
                    "phase": "noisy_validation",
                    "validation_group": group_index,
                    "replicate": replicate,
                    "axis_a_index": axis_a_index,
                    "axis_b_index": axis_b_index,
                    "feature_values": {
                        **spec["fixed_context"],
                        axis_a: levels_a[axis_a_index],
                        axis_b: levels_b[axis_b_index],
                    },
                    "metric_ids": list(spec["metrics"]),
                }
            )
    return rows


def _run_ec_entity(
    contract: dict[str, Any], coordinates: dict[str, Any], output: Path
) -> dict[str, Any]:
    runtime = deepcopy(contract)
    runtime["loci"]["entity"]["nuisance_design"]["namespace"] = coordinates["nuisance_namespace"]
    runtime["loci"]["entity"]["observation_noise_namespace"] = coordinates[
        "observation_noise_namespace"
    ]
    return ec_repair_runner.run_entity(runtime, output)


def _run_ec_parametric(
    contract: dict[str, Any], coordinates: dict[str, Any], output: Path
) -> dict[str, Any]:
    runtime = deepcopy(contract)
    runtime["loci"]["parametric"]["grid_coordinates"] = coordinates["potential_coordinates"]
    references, noises, _bindings = ec_runner._parametric_frozen_sources(runtime)
    sigma = {
        int(reference["world_seed"]): float(noise["analysis"]["validation_noise"]["sigma"] or 0.0)
        for reference, noise in zip(references, noises, strict=True)
    }
    original_surface = ec_runner.surface_design
    original_evaluator = ec_runner.InMemoryMechanismEvaluator
    ec_runner.surface_design = lambda context: _ec_surface(context, coordinates)
    ec_runner.InMemoryMechanismEvaluator = _noisy_evaluator(
        original_evaluator,
        str(coordinates["observation_noise_namespace"]),
        sigma,
        ("score",),
    )
    try:
        return ec_runner.run_parametric(runtime, output)
    finally:
        ec_runner.surface_design = original_surface
        ec_runner.InMemoryMechanismEvaluator = original_evaluator


def _run_ec_structural(
    contract: dict[str, Any], coordinates: dict[str, Any], output: Path
) -> dict[str, Any]:
    runtime = deepcopy(contract)
    namespace = str(coordinates["observation_noise_namespace"])
    original_queries = ec_repair_runner.structural_repair_queries
    original_execute = ec_repair_runner.execute_structural_query
    ec_repair_runner.structural_repair_queries = lambda supplied: _ec_structural_queries(
        supplied, coordinates
    )

    def execute_with_confirmation_noise(**kwargs: Any) -> dict[str, Any]:
        query = kwargs["query_spec"]
        seed = (
            int.from_bytes(
                hashlib.sha256(
                    f"{namespace}:{kwargs['world_seed']}:{query['query_id']}".encode()
                ).digest()[:8],
                "big",
            )
            % 2_147_483_647
        )
        return structural_runner._execute_query(
            **kwargs,
            observation_seed=seed,
            observation_noise_namespace=namespace,
        )

    ec_repair_runner.execute_structural_query = execute_with_confirmation_noise
    try:
        return ec_repair_runner.run_structural(runtime, output)
    finally:
        ec_repair_runner.structural_repair_queries = original_queries
        ec_repair_runner.execute_structural_query = original_execute


def _run_rx_parametric(
    contract: dict[str, Any], coordinates: dict[str, Any], output: Path
) -> dict[str, Any]:
    runtime = deepcopy(contract)
    runtime["loci"]["parametric"]["temperature_grid_K"] = coordinates["temperature_grid_K"]
    runtime["loci"]["parametric"]["duration_grid_s"] = coordinates["duration_grid_s"]
    references, noises = rx_runner._source_worlds(runtime)
    sigma = {
        int(reference["world_seed"]): float(noise["analysis"]["validation_noise"]["sigma"] or 0.0)
        for reference, noise in zip(references, noises, strict=True)
    }
    original_surface = rx_runner.surface_design
    original_evaluator = rx_runner.InMemoryMechanismEvaluator
    rx_runner.surface_design = lambda context: _rx_surface(context, coordinates, original_surface)
    rx_runner.InMemoryMechanismEvaluator = _noisy_evaluator(
        original_evaluator,
        str(coordinates["observation_noise_namespace"]),
        sigma,
        ("score", "safety_risk"),
    )
    try:
        return rx_runner.run_parametric(runtime, output)
    finally:
        rx_runner.surface_design = original_surface
        rx_runner.InMemoryMechanismEvaluator = original_evaluator


def _run_pa_entity(
    contract: dict[str, Any], coordinates: dict[str, Any], output: Path
) -> dict[str, Any]:
    runtime = deepcopy(contract)
    runtime["loci"]["entity"]["solvent_anchors"] = coordinates["solvent_anchors"]
    runtime["loci"]["entity"]["observation_noise_namespace"] = coordinates[
        "observation_noise_namespace"
    ]
    return pa_runner.run_entity(runtime, output)


def _run_c(
    contract: dict[str, Any], coordinates: dict[str, Any], output: Path, *, locus: str
) -> dict[str, Any]:
    runtime = deepcopy(contract)
    if locus == "entity":
        runtime["loci"]["entity"]["cooling_anchors_K"] = coordinates["cooling_anchors_K"]
        runtime["loci"]["entity"]["observation_noise_namespace"] = coordinates[
            "observation_noise_namespace"
        ]
        return c_runner.run_entity(runtime, output)
    runtime["loci"]["parametric"]["temperature_levels_K"] = coordinates["temperature_levels_K"]
    runtime["loci"]["parametric"]["observation_noise_namespace"] = coordinates[
        "observation_noise_namespace"
    ]
    return c_runner.run_parametric(runtime, output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--secret-plan", type=Path, required=True)
    parser.add_argument("--locus", choices=ELIGIBLE_LOCI, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    public_contract = _load(args.contract.resolve())
    validate_public_contract(ROOT, public_contract)
    plan = _load(args.secret_plan.resolve())
    validate_secret_plan(ROOT, plan)
    if plan["plan_sha256"] != public_contract["generator"]["realized_plan_sha256"]:
        raise ValueError("secret plan commitment mismatch")
    if args.output.exists():
        raise FileExistsError("refusing to overwrite one-shot locus output")
    block = args.locus
    source = resolve_source_contract(ROOT, SOURCE_CONTRACTS[block])
    coordinates = dict(plan["loci"][block])
    runners = {
        "EC-E": _run_ec_entity,
        "EC-P": _run_ec_parametric,
        "EC-S": _run_ec_structural,
        "RX-P": _run_rx_parametric,
        "PA-E": _run_pa_entity,
    }
    if block == "C-E":
        summary = _run_c(source, coordinates, args.output.resolve(), locus="entity")
    elif block == "C-P":
        summary = _run_c(source, coordinates, args.output.resolve(), locus="parametric")
    else:
        summary = runners[block](source, coordinates, args.output.resolve())
    receipt: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-confirmation-locus-receipt-1.0",
        "formal_result": True,
        "qualification_stage": "confirmation",
        "block": block,
        "world_denominator": 5,
        "five_world_qualified": summary.get("five_world_qualified") is True,
        "source_summary_sha256": summary["summary_sha256"],
        "public_contract_sha256": public_contract["contract_sha256"],
        "realized_plan_sha256": plan["plan_sha256"],
    }
    receipt["receipt_sha256"] = canonical_json_sha256(receipt)
    write_json_atomic(args.output.resolve() / "confirmation-receipt.json", receipt)
    print(
        json.dumps(
            {
                "block": block,
                "world_denominator": 5,
                "five_world_qualified": receipt["five_world_qualified"],
                "receipt_sha256": receipt["receipt_sha256"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
