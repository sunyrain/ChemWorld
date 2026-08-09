#!/usr/bin/env python3
"""Build/check the Work II formal matrix preflight; execution remains fail-closed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_formal import (
    build_formal_preflight,
    validate_formal_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
DEFAULT_PREFLIGHT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-formal-matrix-runner-preflight-v0.1.json"
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--analysis", type=Path, default=DEFAULT_ANALYSIS)
    parser.add_argument("--output", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--allow-formal-execution", action="store_true")
    parser.add_argument("--qualification-receipt", type=Path)
    parser.add_argument("--currency-ceiling-usd", type=float)
    return parser.parse_args()


def _run_preflight(args: argparse.Namespace) -> int:
    if any(
        (
            args.manifest is not None,
            args.output_root is not None,
            args.resume,
            args.allow_formal_execution,
            args.qualification_receipt is not None,
            args.currency_ceiling_usd is not None,
        )
    ):
        raise RuntimeError("execution-only options cannot be used with --preflight")
    report = build_formal_preflight(ROOT, args.design, args.analysis)
    errors = validate_formal_preflight(report)
    if errors or report["errors"]:
        raise RuntimeError(
            "formal preflight validation failed: "
            + "; ".join([*report["errors"], *errors])
        )
    output = args.output.resolve()
    if args.check:
        if not output.is_file():
            raise RuntimeError(f"missing committed formal preflight: {output}")
        committed = json.loads(output.read_text(encoding="utf-8"))
        if committed != report:
            raise RuntimeError("committed formal preflight differs from deterministic rebuild")
    else:
        write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "formal_execution_allowed": report["formal_execution_allowed"],
                "tasks": report["expected_counts"]["tasks"],
                "clusters": report["expected_counts"]["independent_task_world_clusters"],
                "cells": report["expected_counts"]["participant_cells"],
                "complete_experiments": report["expected_counts"]["complete_experiments"],
                "blocking_requirement_count": len(report["blocking_requirements"]),
                "preflight_sha256": report["preflight_sha256"],
                "output": str(output),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


def _run_execute(args: argparse.Namespace) -> int:
    if args.check or args.output != DEFAULT_PREFLIGHT:
        raise RuntimeError("--check and --output apply only to --preflight")
    required = {
        "--manifest": args.manifest,
        "--output-root": args.output_root,
        "--qualification-receipt": args.qualification_receipt,
        "--currency-ceiling-usd": args.currency_ceiling_usd,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        raise RuntimeError("--execute is missing required options: " + ", ".join(missing))
    if not args.allow_formal_execution:
        raise RuntimeError("--execute requires --allow-formal-execution")
    manifest = json.loads(args.manifest.resolve().read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise RuntimeError("formal manifest must contain an object")
    errors = validate_formal_preflight(manifest)
    if errors:
        raise RuntimeError("formal manifest validation failed: " + "; ".join(errors))
    if manifest.get("formal_execution_allowed") is not True:
        blockers = manifest.get("blocking_requirements", [])
        raise RuntimeError(
            "formal execution remains blocked by the committed manifest: "
            + "; ".join(str(item) for item in blockers)
        )
    raise RuntimeError(
        "formal execution apparatus is not qualified yet; W2-09/W2-10 must complete "
        "before provider use"
    )


def main() -> int:
    args = _parse_args()
    return _run_preflight(args) if args.preflight else _run_execute(args)


if __name__ == "__main__":
    raise SystemExit(main())
