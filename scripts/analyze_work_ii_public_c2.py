#!/usr/bin/env python3
"""Build the manifest-bound, provider-free Work II public C2 analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_public_c2 import (
    LOCUS_IDS,
    build_public_c2_analysis,
    validate_public_c2_analysis,
    validate_public_c2_analysis_plan,
    validate_public_c2_source_files,
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
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--analysis-plan", type=Path, default=DEFAULT_ANALYSIS_PLAN)
    parser.add_argument("--a-e-report", type=Path, required=True)
    parser.add_argument("--a-p-report", type=Path, required=True)
    parser.add_argument("--a-s-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = _load_object(args.manifest.resolve())
    analysis_plan = _load_object(args.analysis_plan.resolve())
    preflight_errors = validate_public_c2_source_files(manifest, root=ROOT)
    preflight_errors.extend(validate_public_c2_analysis_plan(manifest, analysis_plan))
    if preflight_errors:
        raise RuntimeError(
            "public C2 analysis preflight failed: "
            + "; ".join(preflight_errors)
        )
    locus_reports = {
        "A_E": _load_object(args.a_e_report.resolve()),
        "A_P": _load_object(args.a_p_report.resolve()),
        "A_S": _load_object(args.a_s_report.resolve()),
    }
    if set(locus_reports) != set(LOCUS_IDS):
        raise RuntimeError("internal public C2 locus roster drifted")
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite public C2 analysis: {output}")
    report = build_public_c2_analysis(manifest, locus_reports)
    errors = validate_public_c2_analysis(
        report,
        manifest=manifest,
        locus_reports=locus_reports,
    )
    if errors:
        raise RuntimeError("public C2 analysis validation failed: " + "; ".join(errors))
    write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "formal_result": report["formal_result"],
                "tasks": report["denominators"]["task_count"],
                "clusters": report["denominators"]["independent_cluster_count"],
                "retained_cells": report["denominators"]["retained_cell_count"],
                "failures": report["denominators"]["failure_count"],
                "C2_passed": report["C2_intersection_union"]["passed"],
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
