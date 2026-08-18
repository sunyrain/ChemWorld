#!/usr/bin/env python
"""Audit whether the completed A-S B2 packet identifies its registered law family."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_b2_identifiability import (
    audit_b2_participant_visible_identifiability,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ROOT = ROOT / "runs/formal/work-ii-as-study-b2-phase-process-v0.1-20260815"
DEFAULT_B2_ANALYSIS = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b2-phase-process-results-v0.1.json"
)
DEFAULT_JSON = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-b2-participant-visible-identifiability-audit-v0.1.json"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "WORK_II_B2_PARTICIPANT_VISIBLE_IDENTIFIABILITY_AUDIT_ZH.md"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _render(audit: dict[str, Any]) -> str:
    alias = audit["exact_alias"]
    positive = audit["positive_control"]
    empirical = audit["empirical_alternative"]
    return "\n".join(
        [
            "# Work II B2 participant-visible alternative-law identifiability audit",
            "",
            "## 结论先行",
            "",
            "B2 的数值更新结果保留，但 participant-visible packet **不能唯一识别** 注册的 "
            "1.75-power family。全部 evidence/scoring queries 固定同一个 nominal pair；指数可被 "
            "一个重新标定的有效分配系数精确吸收。",
            "",
            f"- 固定 nominal pair：solvent `{alias['solvent']}` / extractant `{alias['extractant']}`。",
            f"- effective reference coefficient：`{alias['effective_reference_partition_coefficient']:.6f}`。",
            f"- 与 exponent 1.75 精确等价的 linear multiplier：`{alias['linear_alias_coefficient_multiplier']:.6f}`。",
            f"- aligned exact-law 阳性对照：`{positive['aligned_exact_1_75_count']}/{positive['world_count']}`；"
            f"power-compatible：`{positive['aligned_power_compatible_count']}/{positive['world_count']}`。",
            f"- 仅使用 evidence metric 均值的 endpoint baseline 在 disjoint scoring 上平均 MAE："
            f"`{empirical['mean_scoring_error']:.6f}`。",
            "",
            "## 机制处置",
            "",
            "允许写法：固定 B2 packet 驱动了强数值更新，但 misindexed public summaries 没有恢复 "
            "exact 1.75-law expression。",
            "",
            "禁止写法：B2 已唯一把剩余失败定位到 participant 内部 structural-law identification。",
            "",
            "后续需要跨 nominal coefficients 或公开 coefficient anchors，并独立提交 typed family、"
            "exponent 与 family-diagnostic unseen predictions。",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--b2-analysis", type=Path, default=DEFAULT_B2_ANALYSIS)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    run_root = args.run_root if args.run_root.is_absolute() else ROOT / args.run_root
    cells = [_load(path) for path in sorted((run_root / "cells").glob("*.json"))]
    audit = audit_b2_participant_visible_identifiability(
        _load(run_root / "input_manifest.json"),
        cells,
        _load(args.b2_analysis if args.b2_analysis.is_absolute() else ROOT / args.b2_analysis),
    )
    output_json = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    output_report = (
        args.output_report if args.output_report.is_absolute() else ROOT / args.output_report
    )
    write_json_atomic(output_json, audit)
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(_render(audit), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

