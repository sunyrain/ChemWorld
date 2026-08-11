#!/usr/bin/env python3
"""Build a sealed Work II private-confirmation preflight without provider calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.work_ii_private import (
    build_private_confirmation_preflight,
    write_private_preflight_once,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-manifest", type=Path, required=True)
    parser.add_argument("--public-analysis", type=Path, required=True)
    parser.add_argument("--private-seal", type=Path, required=True)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = build_private_confirmation_preflight(
        public_manifest=_load(args.public_manifest.resolve()),
        public_analysis=_load(args.public_analysis.resolve()),
        design=_load(args.design.resolve()),
        seal=_load(args.private_seal.resolve()),
    )
    write_private_preflight_once(ROOT, args.output.resolve(), report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "cells": report["expected_counts"]["participant_cells"],
                "clusters": report["expected_counts"]["independent_task_world_clusters"],
                "private_execution_allowed": report["private_execution_allowed"],
                "provider_calls_executed": report["provider_calls_executed"],
                "preflight_sha256": report["preflight_sha256"],
                "output": str(args.output.resolve()),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
