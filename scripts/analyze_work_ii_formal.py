#!/usr/bin/env python3
"""Build the traceable Work II formal-analysis dataset after all evaluators finish."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_report import load_formal_analysis_dataset

ROOT = Path(__file__).resolve().parents[1]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--execution-root", type=Path, required=True)
    parser.add_argument("--truth-root", type=Path, required=True)
    parser.add_argument("--blind-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest = json.loads(args.manifest.resolve().read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("formal manifest must contain an object")
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite formal analysis dataset: {output}")
    report = load_formal_analysis_dataset(
        manifest,
        args.execution_root.resolve(),
        args.truth_root.resolve(),
        args.blind_root.resolve(),
    )
    write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "cells": report["retained_cell_count"],
                "clusters": report["cluster_contrast_count"],
                "errors": len(report["errors"]),
                "dataset_sha256": report["dataset_sha256"],
                "output": str(output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
