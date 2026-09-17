#!/usr/bin/env python3
"""Calibrate one global RX entity transposition on non-benchmark Worlds."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import fmean, variance
from typing import Any

from chemworld.eval.experiment_1_rx_qualification import load_contract
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v02 import execute_one

try:
    from scripts.run_experiment_1_rx_qualification import (
        _entity_row,
        _plan,
        _schedule,
        _stable_seed,
    )
except ModuleNotFoundError:
    from run_experiment_1_rx_qualification import (
        _entity_row,
        _plan,
        _schedule,
        _stable_seed,
    )

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_rx_qualification_v1.0.1.json"
NOTE = (
    ROOT / "workstreams/flagship_tasks/experiment_1/systems/RX/"
    "ENTITY_REPAIR_AUTHORING_NOTE_V1_0_2.md"
)
NOTE_SHA256 = "3ef00f1b8bfd2f0ed668ec37ae5db2824a5173cb3e1a155b5b6931bfec257b6b"
CALIBRATION_SEEDS = (101, 102, 103, 104, 105)
METRICS = ("yield", "selectivity", "conversion", "byproduct_signal")
NAMESPACE = "experiment-1-v1.0.2-rx-entity-pair-authoring"


def _pair_report(
    receipts: Sequence[Mapping[str, Any]],
    pair: tuple[int, int],
    *,
    minimum_mean: float,
    minimum_single: float,
    minimum_snr: float,
    minimum_consequence: float,
) -> dict[str, Any]:
    grouped: dict[tuple[int, int], list[Mapping[str, Any]]] = defaultdict(list)
    for row in receipts:
        if row.get("status") == "completed":
            grouped[(int(row["nuisance_anchor"]), int(row["target_category"]))].append(row)
    anchors = []
    for anchor in (0, 1):
        left = grouped[(anchor, pair[0])]
        right = grouped[(anchor, pair[1])]
        metric_rows = []
        for metric in METRICS:
            left_values = [float(row["allowed_metrics"][metric]) for row in left]
            right_values = [float(row["allowed_metrics"][metric]) for row in right]
            separation = (
                abs(fmean(right_values) - fmean(left_values))
                if len(left_values) == len(right_values) == 3
                else 0.0
            )
            standard_error = (
                math.sqrt(variance(left_values) / 3.0 + variance(right_values) / 3.0)
                if len(left_values) == len(right_values) == 3
                else math.inf
            )
            metric_rows.append(
                {
                    "metric": metric,
                    "absolute_separation": separation,
                    "welch_standard_error": standard_error,
                }
            )
        mean_separation = fmean(row["absolute_separation"] for row in metric_rows)
        maximum_separation = max(row["absolute_separation"] for row in metric_rows)
        rms_standard_error = math.sqrt(
            fmean(float(row["welch_standard_error"]) ** 2 for row in metric_rows)
        )
        snr = mean_separation / max(rms_standard_error, 1.0e-12)
        anchors.append(
            {
                "anchor": anchor,
                "mean_support_separation": mean_separation,
                "maximum_support_separation": maximum_separation,
                "support_signal_to_noise_ratio": snr,
                "passed": bool(
                    mean_separation >= minimum_mean
                    and maximum_separation >= minimum_single
                    and snr >= minimum_snr
                ),
            }
        )
    return {
        "pair": list(pair),
        "anchors": anchors,
        "identifiable": all(row["passed"] for row in anchors),
        "behaviorally_relevant": max(row["mean_support_separation"] for row in anchors)
        >= minimum_consequence,
        "minimum_anchor_mean_separation": min(row["mean_support_separation"] for row in anchors),
        "minimum_anchor_snr": min(row["support_signal_to_noise_ratio"] for row in anchors),
    }


def run(contract_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    if file_sha256(NOTE) != NOTE_SHA256:
        raise ValueError("RX-E authoring note digest changed")
    contract = load_contract(ROOT, contract_path)
    output.mkdir(parents=True)
    plan = _plan(contract)
    schedule = _schedule(contract)
    entity = contract["loci"]["entity"]
    receipts_by_world: dict[str, list[dict[str, Any]]] = {}
    execution_index = 0
    total = len(CALIBRATION_SEEDS) * len(schedule) * 3
    for world_index, seed in enumerate(CALIBRATION_SEEDS, start=1):
        world_id = f"RX-CAL{world_index:02d}"
        world_output = output / world_id
        world_receipts = []
        for schedule_row in schedule:
            for replicate in range(3):
                row = _entity_row(
                    contract,
                    world_id=world_id,
                    world_seed=seed,
                    schedule_row=schedule_row,
                    replicate=replicate,
                    execution_index=execution_index,
                )
                row["observation_noise_namespace"] = NAMESPACE
                row["observation_seed"] = _stable_seed(
                    NAMESPACE,
                    seed,
                    schedule_row["nuisance_anchor"],
                    schedule_row["target_category"],
                    replicate,
                )
                receipt = execute_one(ROOT, plan, row, output)
                world_receipts.append(receipt)
                execution_index += 1
                if execution_index % 8 == 0:
                    print(
                        json.dumps(
                            {
                                "event": "rx_entity_pair_authoring_progress",
                                "completed": execution_index,
                                "total": total,
                                "world_id": world_id,
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
        world_output.mkdir()
        write_json_atomic(world_output / "receipts.json", world_receipts)
        receipts_by_world[world_id] = world_receipts

    candidates = []
    for pair in itertools.combinations(range(4), 2):
        worlds = [
            {
                "world_id": world_id,
                **_pair_report(
                    receipts,
                    pair,
                    minimum_mean=float(entity["minimum_mean_support_separation"]),
                    minimum_single=float(entity["minimum_single_support_separation"]),
                    minimum_snr=float(entity["minimum_support_signal_to_noise_ratio"]),
                    minimum_consequence=float(entity["minimum_observed_endpoint_consequence"]),
                ),
            }
            for world_id, receipts in receipts_by_world.items()
        ]
        candidates.append(
            {
                "pair": list(pair),
                "worlds": worlds,
                "qualified_worlds": sum(
                    row["identifiable"] and row["behaviorally_relevant"] for row in worlds
                ),
                "minimum_anchor_mean_separation": min(
                    row["minimum_anchor_mean_separation"] for row in worlds
                ),
                "minimum_anchor_snr": min(row["minimum_anchor_snr"] for row in worlds),
            }
        )
    ranked = sorted(
        candidates,
        key=lambda row: (
            -int(row["qualified_worlds"]),
            -float(row["minimum_anchor_mean_separation"]),
            -float(row["minimum_anchor_snr"]),
            tuple(row["pair"]),
        ),
    )
    selected = ranked[0] if ranked[0]["qualified_worlds"] == len(CALIBRATION_SEEDS) else None
    summary: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-rx-entity-repair-authoring-1.0.2",
        "formal_result": False,
        "provider_call_count": 0,
        "calibration_world_seeds": list(CALIBRATION_SEEDS),
        "benchmark_denominator": False,
        "planned_executions": total,
        "completed_executions": sum(
            row.get("status") == "completed"
            for receipts in receipts_by_world.values()
            for row in receipts
        ),
        "exact_replays": sum(
            isinstance(row.get("exact_replay"), Mapping)
            and row["exact_replay"].get("verified") is True
            for receipts in receipts_by_world.values()
            for row in receipts
        ),
        "selection_rule": (
            "qualified_worlds_then_minimum_anchor_mean_then_minimum_snr_then_pair_order"
        ),
        "candidates": ranked,
        "selected_pair": None if selected is None else selected["pair"],
        "selected_permutation": (
            None
            if selected is None
            else [
                selected["pair"][1]
                if index == selected["pair"][0]
                else selected["pair"][0]
                if index == selected["pair"][1]
                else index
                for index in range(4)
            ]
        ),
        "note_sha256": NOTE_SHA256,
        "contract_file_sha256": file_sha256(contract_path),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args.contract.resolve(), args.output.resolve())
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if summary["selected_pair"] is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
