#!/usr/bin/env python3
"""Run the frozen Work II confirmatory analysis on a completed formal dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_confirmatory import (
    build_confirmatory_analysis,
    validate_confirmatory_analysis,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ANALYSIS_PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--analysis-plan", type=Path, default=DEFAULT_ANALYSIS_PLAN)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    dataset = _load_object(args.dataset.resolve())
    analysis_plan = _load_object(args.analysis_plan.resolve())
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite confirmatory analysis: {output}")
    report = build_confirmatory_analysis(dataset, analysis_plan)
    errors = validate_confirmatory_analysis(report)
    if errors:
        raise RuntimeError("confirmatory analysis validation failed: " + "; ".join(errors))
    write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "formal_result": report["formal_result"],
                "retained_cells": report["denominators"]["retained_cell_count"],
                "clusters": report["denominators"]["independent_cluster_count"],
                "H3_passed": report["primary_H3"]["passed"],
                "report_sha256": report["report_sha256"],
                "output": str(output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
