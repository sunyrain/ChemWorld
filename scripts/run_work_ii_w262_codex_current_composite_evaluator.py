#!/usr/bin/env python3
"""Evaluate the complete W2-62 Codex C2 cohort without provider calls."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_current_composite import (
    execute_current_composite_evaluator,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COHORT = (
    ROOT / "runs/development/work-ii-w2-62-codex-c2-full-replication-v0.1-20260902"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/"
    "work-ii-w2-62-codex-c2-current-composite-evaluator-v0.1-20260902"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-62-codex-c2-current-composite-evaluation-v0.1.json"
)
DEFAULT_MARKDOWN = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "WORK_II_W2_62_CODEX_C2_CURRENT_COMPOSITE_EVALUATION_ZH.md"
)
ANALYSIS_PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.2.json"
FORMAL_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
COHORT_ID = "work-ii-w2-62-codex-c2-current-composite-v0.1"


def _render(report: Mapping[str, Any]) -> str:
    denominator = report["denominators"]
    prediction = report["prediction_correction"]
    law = report["executable_law"]
    blind = report["blind_action"]
    lines = [
        "# Work II W2-62 Codex C2 current-composite 评估",
        "",
        "本报告对完整 Codex C2 participant cohort 使用与 DeepSeek 相同的 provider-free "
        "current-composite evaluator; 不产生新的 provider 调用。",
        "",
        "## 精确分母",
        "",
        f"- cells: `{denominator['cell_count']}/135`",
        f"- task-world clusters: `{denominator['cluster_count']}/45`",
        f"- truth: `{denominator['truth_completed_execution_count']}/420`",
        f"- checkpoints: `{denominator['checkpoint_scored_count']}/675`",
        f"- laws: `{denominator['law_summary_evaluated_count']}/135`",
        f"- blind launched: `{denominator['blind_launched_execution_count']}/810`",
        "",
        "## 机器结果入口",
        "",
        f"- prediction loci: `{', '.join(sorted(prediction['locus_results']))}`",
        f"- law loci: `{', '.join(sorted(key for key in law if key != 'overall'))}`",
        f"- blind loci: `{', '.join(sorted(key for key in blind if key != 'overall'))}`",
        "",
        "统计估计、失败单元和完整分层结果以同名 JSON 为准。",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort", type=Path, default=DEFAULT_COHORT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.preflight and args.resume:
        raise ValueError("--preflight and --resume are mutually exclusive")
    cohort = args.cohort.resolve()
    report_path = args.report.resolve()
    markdown_path = args.markdown.resolve()
    if not args.preflight and not args.resume:
        for path in (report_path, markdown_path):
            if path.exists():
                raise FileExistsError(f"refusing to overwrite tracked result: {path}")

    progress_path = args.progress_file.resolve() if args.progress_file else None

    def progress(payload: Mapping[str, Any]) -> None:
        rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
        if progress_path is not None:
            progress_path.parent.mkdir(parents=True, exist_ok=True)
            with progress_path.open("a", encoding="utf-8") as handle:
                handle.write(rendered + "\n")
        print(rendered, flush=True)

    result = execute_current_composite_evaluator(
        ROOT,
        base_run=cohort,
        replacement_run=cohort,
        cohort_id=COHORT_ID,
        analysis_plan_path=ANALYSIS_PLAN,
        formal_design_path=FORMAL_DESIGN,
        output_root=args.output_root.resolve(),
        resume=args.resume,
        preflight_only=args.preflight,
        progress=progress,
    )
    if args.preflight:
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "cohort_id": result["cohort_id"],
                    "composition": result["composition"],
                    "provider_call_count": result["provider_call_count"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )
        return 0 if result["status"] == "passed" else 1
    write_json_atomic(report_path, result)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(_render(result), encoding="utf-8")
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
