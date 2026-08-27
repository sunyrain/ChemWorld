#!/usr/bin/env python
# ruff: noqa: RUF001
"""Close out the replicated B3 canary without additional provider calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_reviewer_followup import summarize_b3_canary_closeout

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-as-study-b3-identifiable-law-action-v0.2-20260827-restart1"
)
DEFAULT_JSON_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b3-replicated-canary-closeout-v0.1.json"
)
DEFAULT_REPORT_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "WORK_II_AS_STUDY_B3_REPLICATED_CANARY_CLOSEOUT_ZH.md"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def _show(value: Any, digits: int = 4) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _write_report(summary: dict[str, Any], path: Path) -> None:
    eligible_worlds = summary["preparation"][
        "action_opportunity_eligible_world_count"
    ]
    lines = [
        "# Work II A-S Study B3 replicated canary 终态收束",
        "",
        f"状态：`{summary['status']}`。canary 完成记录 "
        f"`{summary['observed_canary_session_count']}/"
        f"{summary['scheduled_canary_session_count']}`，其中 completed "
        f"`{summary['completed_canary_session_count']}`、failed "
        f"`{summary['failed_canary_session_count']}`。formal participant sessions "
        f"`{summary['launched_formal_session_count']}/"
        f"{summary['scheduled_formal_session_count']}`，其余全部未启动。",
        "",
        "Provider-free preparation 已完成 5-world structural qualification、"
        "public truth 与 30-cell manifest；5 个 world 都进入 structural denominator，"
        f"其中 action-opportunity eligible 为 `{eligible_worlds}/5`。",
        "",
        "| arm | status | post family | exponent | post MAE | true rank | "
        "Top-1 | regret | failure |",
        "|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary["cell_rows"]:
        lines.append(
            f"| {row['arm']} | {row['status']} | {_show(row['post_family'])} | "
            f"{_show(row['post_exponent'])} | {_show(row['post_prediction_mae'])} | "
            f"{_show(row['selected_true_rank'])} | {_show(row['top1_selected'])} | "
            f"{_show(row['normalized_regret'])} | {_show(row['failure_message'])} |"
        )
    lines.extend(
        [
            "",
            "三个 session 均只尝试一次，6/6 provider turns 返回 completed receipt，"
            f"tool events 为 `{summary['tool_event_count']}`。opaque 完成完整两轮；aligned 与 "
            "misindexed 的 post payload 均未给出 scoring roster 内的有效 action ID，"
            "因此按冻结规则记为 participant-schema failures。它们不是基础设施 retry，"
            "也不以新 session 替换。",
            "",
            "## 证据边界",
            "",
            "该 canary 的 scientific answers 事前声明不用于改设计。由于 canary gate 未通过，"
            "本 block 没有形成 30-session structural-recovery、arm-level 或 replicate-level 估计，"
            "也不进入 Figure 4 的 participant scientific claim。它只支持 apparatus 终态："
            "same-thread two-turn 路径在 opaque 可完成，但当前 DeepSeek participant 在另外两臂"
            "未满足冻结的新动作选择契约。GPT replication 仅完成 provider-free preparation，"
            "未启动 participant call。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    args = parser.parse_args()

    run_root = args.run_root.resolve()
    manifest = _load(run_root / "input_manifest.json")
    qualification = _load(run_root / "qualification_summary.json")
    public_truth = _load(run_root / "public_truth_manifest.json")
    static = _load(run_root / "provider_static_check.json")
    canary_summary = _load(run_root / "canary_summary.json")
    results = [_load(path) for path in sorted((run_root / "canary").glob("*.json"))]
    if qualification.get("status") != "qualified":
        raise ValueError("B3 provider-free qualification is unavailable")
    if public_truth.get("status") != "preflight_passed":
        raise ValueError("B3 public truth preflight is unavailable")
    if static.get("ready") is not True or static.get("provider_calls") != 0:
        raise ValueError("B3 provider static check is not ready and zero-call")
    formal_dir = run_root / "cells"
    if formal_dir.is_dir() and any(formal_dir.glob("*.json")):
        raise ValueError("B3 formal cells exist; canary-only closeout is invalid")

    summary = summarize_b3_canary_closeout(manifest, results, canary_summary)
    summary.pop("summary_sha256", None)
    summary["analysis_role"] = "terminal_development_canary_closeout"
    summary["formal_result"] = False
    summary["provider"] = {
        "id": manifest["provider"]["id"],
        "model": manifest["provider"]["model"],
        "reasoning_effort": manifest["provider"]["reasoning_effort"],
        "static_ready": static["ready"],
    }
    summary["preparation"] = {
        "qualification_status": qualification["status"],
        "development_world_count": qualification["development_world_count"],
        "candidate_grid_truth_execution_count": qualification[
            "linear_and_power_truth_execution_count"
        ],
        "exponent_grid_truth_execution_count": qualification[
            "exponent_grid_truth_execution_count"
        ],
        "public_world_count": public_truth["public_world_count"],
        "public_truth_execution_count": public_truth[
            "linear_and_power_truth_execution_count"
        ],
        "action_opportunity_eligible_world_count": public_truth[
            "action_opportunity_eligible_world_count"
        ],
        "failed_public_world_count": public_truth["failed_public_world_count"],
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(args.json_output.resolve(), summary)
    _write_report(summary, args.report_output.resolve())
    print(
        json.dumps(
            {
                "status": summary["status"],
                "completed_canary_sessions": summary[
                    "completed_canary_session_count"
                ],
                "failed_canary_sessions": summary["failed_canary_session_count"],
                "launched_formal_sessions": summary["launched_formal_session_count"],
                "provider_turns": summary["provider_turn_count"],
                "tool_events": summary["tool_event_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
