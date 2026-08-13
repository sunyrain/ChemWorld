#!/usr/bin/env python3
"""Build the zero-provider-call readiness gate for Work II method qualification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_method_qualification_local import (
    build_method_qualification_local_manifest,
    build_method_qualification_local_readiness,
    build_w2_27_runtime_config,
)
from chemworld.eval.work_ii_qualification import (
    validate_method_qualification_readiness,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-method-qualification-readiness-v0.2.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--resource-calibration-manifest", type=Path, required=True)
    parser.add_argument("--resource-calibration-summary", type=Path, required=True)
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    calibration_manifest_path = args.resource_calibration_manifest.resolve()
    calibration_summary_path = args.resource_calibration_summary.resolve()
    runtime_config_path = args.runtime_config.resolve()
    try:
        runtime_config_path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RuntimeError("W2-27 runtime config must remain inside the repository") from error
    expected_runtime_config = build_w2_27_runtime_config(
        ROOT,
        DESIGN,
        calibration_summary_path,
    )
    if runtime_config_path.is_file():
        observed_runtime_config = json.loads(
            runtime_config_path.read_text(encoding="utf-8")
        )
        if observed_runtime_config != expected_runtime_config:
            raise RuntimeError("existing W2-27 runtime config differs from the W2-26 card")
    elif args.check:
        raise RuntimeError("W2-27 runtime config is missing")
    else:
        write_json_atomic(runtime_config_path, expected_runtime_config)
    manifest = build_method_qualification_local_manifest(
        ROOT,
        DESIGN,
        runtime_config_path,
    )
    report = build_method_qualification_local_readiness(
        ROOT,
        manifest,
        resource_calibration_manifest_path=calibration_manifest_path,
        resource_calibration_summary_path=calibration_summary_path,
    )
    errors = validate_method_qualification_readiness(report)
    if errors:
        raise RuntimeError("method qualification readiness failed: " + "; ".join(errors))
    output = args.output.resolve()
    if args.check:
        if not output.is_file():
            raise RuntimeError(f"missing committed readiness report: {output}")
        committed = json.loads(output.read_text(encoding="utf-8"))
        if committed != report:
            raise RuntimeError("committed readiness differs from deterministic rebuild")
    else:
        write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "provider_execution_allowed": report["provider_execution_allowed"],
                "provider_calls_executed": report["provider_calls_executed"],
                "qualification_cells": report["expected_counts"]["accepted_scientific_cells"],
                "provider_attempts_hard_cap": report["expected_counts"][
                    "provider_process_attempts_hard_cap"
                ],
                "blocking_requirement_count": len(report["blocking_requirements"]),
                "readiness_sha256": report["readiness_sha256"],
                "output": str(output),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
