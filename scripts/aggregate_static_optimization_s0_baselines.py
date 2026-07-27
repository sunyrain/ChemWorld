"""Aggregate audited S0 classic-baseline reports across static world seeds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)
from chemworld.eval.static_optimization_baselines import aggregate_baseline_cells


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sources: list[dict[str, Any]] = []
    cells: list[dict[str, Any]] = []
    seen_world_seeds: set[int] = set()
    protocol_ids: set[str] = set()
    freeze_ids: set[str] = set()
    receipt_hashes_match = True
    for root in args.run_root:
        report_path = root / "report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        world_seed = int(report["world_seed"])
        if world_seed in seen_world_seeds:
            raise ValueError(f"duplicate baseline world seed: {world_seed}")
        seen_world_seeds.add(world_seed)
        protocol_ids.add(str(report["protocol_id"]))
        freeze_ids.add(str(report["method_config_freeze_id"]))
        for cell in report["cells"]:
            key = f"{cell['method_id']}:{cell['cell']['task_id']}"
            if report["receipt_sha256"].get(key) != canonical_json_sha256(cell):
                receipt_hashes_match = False
            cells.append(cell)
        sources.append(
            {
                "world_seed": world_seed,
                "run_root": str(root),
                "report_sha256": file_sha256(report_path),
                "cell_count": int(report["cell_count"]),
                "physical_experiment_count": int(report["total_physical_experiment_count"]),
            }
        )
    if len(protocol_ids) != 1 or len(freeze_ids) != 1:
        raise ValueError("baseline reports do not share one frozen protocol")
    sources.sort(key=lambda item: item["world_seed"])
    aggregate = aggregate_baseline_cells(cells)
    payload = {
        "schema_version": "chemworld-static-optimization-baseline-multiseed-0.1-s0",
        "protocol_id": next(iter(protocol_ids)),
        "freeze_id": next(iter(freeze_ids)),
        "world_seeds": sorted(seen_world_seeds),
        "world_seed_count": len(seen_world_seeds),
        "cell_count": len(cells),
        "completed_experiment_count": sum(
            int(cell["completed_experiment_count"]) for cell in cells
        ),
        "completed_validation_experiment_count": sum(
            int(cell["completed_validation_experiment_count"]) for cell in cells
        ),
        "total_physical_experiment_count": sum(
            int(cell["total_physical_experiment_count"]) for cell in cells
        ),
        "receipt_hashes_match": receipt_hashes_match,
        "aggregate": aggregate,
        "sources": sources,
    }
    write_json_atomic(args.output / "multiseed_report.json", payload)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "world_seeds": payload["world_seeds"],
                "cells": payload["cell_count"],
                "receipt_hashes_match": receipt_hashes_match,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
