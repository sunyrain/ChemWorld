#!/usr/bin/env python3
"""Materialize the nine provider-free Work II formal runtime configs."""

from __future__ import annotations

import argparse
from pathlib import Path

from chemworld.eval.work_ii_formal_runtime import build_formal_runtime_manifest

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--w2-26-manifest", type=Path, required=True)
    parser.add_argument("--w2-26-summary", type=Path, required=True)
    parser.add_argument(
        "--formal-design",
        type=Path,
        default=ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json",
    )
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    manifest = build_formal_runtime_manifest(
        ROOT,
        w2_26_manifest_path=args.w2_26_manifest,
        w2_26_summary_path=args.w2_26_summary,
        formal_design_path=args.formal_design,
        output_root=args.output_root,
    )
    print(
        "[work-ii-formal-runtime] "
        f"status={manifest['status']} tasks={len(manifest['task_configs'])} "
        f"provider_calls={manifest['provider_calls_executed']} "
        f"output={args.output_root.resolve()}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
