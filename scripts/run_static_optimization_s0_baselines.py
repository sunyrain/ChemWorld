"""Run classic complete-experiment baselines under the S0 static protocol."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import (
    canonical_json_sha256 as canonical_sha256,
)
from chemworld.eval.provenance import (
    write_json_atomic,
)
from chemworld.eval.static_optimization_baselines import (
    aggregate_baseline_cells,
    run_baseline_cell,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--algorithm", action="append")
    parser.add_argument("--algorithm-seed", action="append", type=int)
    parser.add_argument("--world-seed", type=int)
    args = parser.parse_args()
    protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    if args.world_seed is not None:
        protocol["world_policy"] = dict(protocol["world_policy"])
        protocol["world_policy"]["world_seed"] = int(args.world_seed)
    algorithm_ids = list(args.algorithm or protocol["algorithms"])
    algorithm_seeds = list(args.algorithm_seed or protocol["algorithm_seeds"])
    unknown = set(algorithm_ids) - set(protocol["algorithms"])
    if unknown:
        raise ValueError(f"unknown configured baseline algorithms: {sorted(unknown)}")
    cells = []
    for algorithm_id in algorithm_ids:
        for algorithm_seed in algorithm_seeds:
            cell = run_baseline_cell(
                protocol=protocol,
                algorithm_id=algorithm_id,
                algorithm_seed=int(algorithm_seed),
            )
            cells.append(cell)
            filename = f"{cell['method_id']}--{cell['cell']['task_id']}.json"
            write_json_atomic(args.output / "receipts" / filename, cell)
            print(
                json.dumps(
                    {
                        "algorithm": algorithm_id,
                        "algorithm_seed": algorithm_seed,
                        "best_exploration_score": max(cell["scores"]),
                        "validated_final_score": cell["primary_score"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    aggregate = aggregate_baseline_cells(cells)
    protocol_hash = canonical_sha256(protocol)
    report = {
        "schema_version": "chemworld-static-scientific-optimization-baseline-report-0.1-s0-dev",
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": protocol_hash,
        "method_config_freeze_id": protocol["freeze_id"],
        "method_config_sha256": protocol_hash,
        "method_ids": [str(item["method_id"]) for item in cells],
        "provider_mode": "local_classic_optimizer",
        "world_seed": int(protocol["world_policy"]["world_seed"]),
        "cell_count": len(cells),
        "completed_cell_count": len(cells),
        "method_failure_cell_count": 0,
        "planned_experiment_count": sum(
            int(item["planned_experiment_count"]) for item in cells
        ),
        "completed_experiment_count": sum(
            int(item["completed_experiment_count"]) for item in cells
        ),
        "recommendation_stage_present": True,
        "completed_synthesis_call_count": 0,
        "planned_predictive_validation_experiment_count": 0,
        "completed_predictive_validation_experiment_count": 0,
        "completed_validation_experiment_count": sum(
            int(item["completed_validation_experiment_count"]) for item in cells
        ),
        "total_physical_experiment_count": sum(
            int(item["total_physical_experiment_count"]) for item in cells
        ),
        "provider_call_count": 0,
        "provider_attempt_count": 0,
        "provider_reported_total_tokens": 0,
        "accounting_complete": True,
        "known_billed_cost_usd": 0.0,
        "receipt_sha256": {
            f"{item['method_id']}:{item['cell']['task_id']}": canonical_sha256(item)
            for item in cells
        },
        "aggregate": aggregate,
        "cells": cells,
        "interpretation": (
            "Development-only S0 classic-optimizer comparison. Every method receives only "
            "the completed experiment leaderboard score and peak safety risk. Final scores "
            "are paired blind validations of each method's best observed recipe."
        ),
    }
    write_json_atomic(args.output / "report.json", report)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "cells": len(cells),
                "exploration_experiments": report["completed_experiment_count"],
                "physical_experiments": report["total_physical_experiment_count"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
