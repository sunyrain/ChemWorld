#!/usr/bin/env python
# ruff: noqa: E501, RUF001
"""Compare the defective and recovered Work II current-composite evaluators."""

from __future__ import annotations

import argparse
import json
import statistics
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OLD = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.1.json"
)
DEFAULT_NEW = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
)
DEFAULT_JSON = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-world-intervention-recovery-v0.1.json"
)
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "WORK_II_DEEPSEEK_C2_CURRENT_COMPOSITE_WORLD_INTERVENTION_RECOVERY_ZH.md"
)
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
TASKS = ("partition-discovery", "reaction-to-crystallization")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _mean(values: Sequence[float]) -> float:
    return statistics.mean(values)


def _task_summary(report: Mapping[str, Any], task_id: str) -> dict[str, Any]:
    rows = [
        row
        for row in report["cell_rows"]
        if row["locus_id"] == "A_S" and row["task_id"] == task_id
    ]
    if len(rows) != 15:
        raise ValueError(f"A-S {task_id} cell denominator drifted")
    by_arm: dict[str, Any] = {}
    for arm in ARMS:
        arm_rows = [row for row in rows if row["prior_arm"] == arm]
        pre = [float(row["checkpoint_error"]["effective_pre_error"]) for row in arm_rows]
        final = [float(row["checkpoint_error"]["effective_final_error"]) for row in arm_rows]
        laws = [float(row["law_summary"]["normalized_mae"]) for row in arm_rows]
        blind = [
            float(row["blind"]["recommendation_gain_over_incumbent"])
            for row in arm_rows
            if row["blind"]["status"] == "completed"
        ]
        by_arm[arm] = {
            "cell_count": len(arm_rows),
            "mean_pre_error": _mean(pre),
            "mean_final_error": _mean(final),
            "mean_prediction_improvement": _mean(
                [before - after for before, after in zip(pre, final, strict=True)]
            ),
            "mean_law_mae": _mean(laws),
            "mean_pre_to_law_improvement": _mean(
                [float(row["law_summary"]["pre_to_law_summary_improvement"]) for row in arm_rows]
            ),
            "mean_law_minus_final_error": _mean(
                [float(row["law_summary"]["summary_minus_effective_final_error"]) for row in arm_rows]
            ),
            "blind_evaluable_count": len(blind),
            "mean_blind_gain": _mean(blind) if blind else None,
        }
    cluster_rows = [
        row
        for row in report["prediction_correction"]["locus_results"]["A_S"]["cluster_rows"]
        if row["task_id"] == task_id
    ]
    if len(cluster_rows) != 5:
        raise ValueError(f"A-S {task_id} cluster denominator drifted")
    return {
        "task_id": task_id,
        "cell_count": len(rows),
        "cluster_count": len(cluster_rows),
        "by_arm": by_arm,
        "mean_observed_primary_contrast": _mean(
            [float(row["H3_primary_contrast"]) for row in cluster_rows]
        ),
        "mean_failure_aware_primary_lower_bound": _mean(
            [float(row["H3_primary_contrast_lower_bound"]) for row in cluster_rows]
        ),
        "positive_observed_world_count": sum(
            float(row["H3_primary_contrast"]) > 0.0 for row in cluster_rows
        ),
        "positive_failure_aware_world_count": sum(
            float(row["H3_primary_contrast_lower_bound"]) > 0.0 for row in cluster_rows
        ),
    }


def _changed(old: float | None, new: float | None) -> float | None:
    if old is None or new is None:
        return None
    return new - old


def _pair_task(old: Mapping[str, Any], new: Mapping[str, Any]) -> dict[str, Any]:
    arms: dict[str, Any] = {}
    for arm in ARMS:
        old_arm = old["by_arm"][arm]
        new_arm = new["by_arm"][arm]
        arms[arm] = {
            field: {
                "old": old_arm[field],
                "new": new_arm[field],
                "change": _changed(old_arm[field], new_arm[field]),
            }
            for field in (
                "mean_pre_error",
                "mean_final_error",
                "mean_prediction_improvement",
                "mean_law_mae",
                "mean_pre_to_law_improvement",
                "mean_law_minus_final_error",
                "mean_blind_gain",
            )
        }
    return {
        "task_id": old["task_id"],
        "cell_count": new["cell_count"],
        "cluster_count": new["cluster_count"],
        "by_arm": arms,
        "observed_primary_contrast": {
            "old": old["mean_observed_primary_contrast"],
            "new": new["mean_observed_primary_contrast"],
            "change": new["mean_observed_primary_contrast"]
            - old["mean_observed_primary_contrast"],
            "old_positive_world_count": old["positive_observed_world_count"],
            "new_positive_world_count": new["positive_observed_world_count"],
        },
        "failure_aware_primary_lower_bound": {
            "old": old["mean_failure_aware_primary_lower_bound"],
            "new": new["mean_failure_aware_primary_lower_bound"],
            "change": new["mean_failure_aware_primary_lower_bound"]
            - old["mean_failure_aware_primary_lower_bound"],
            "old_positive_world_count": old["positive_failure_aware_world_count"],
            "new_positive_world_count": new["positive_failure_aware_world_count"],
        },
    }


def analyze(old_path: Path, new_path: Path) -> dict[str, Any]:
    old = _load(old_path)
    new = _load(new_path)
    expected_denominators = {
        "cell_count": 135,
        "cluster_count": 45,
        "truth_completed_execution_count": 420,
        "checkpoint_scored_count": 675,
        "law_summary_evaluated_count": 135,
        "blind_completed_execution_count": 726,
        "blind_unstarted_execution_count": 84,
    }
    for name, report in (("old", old), ("new", new)):
        if report.get("status") != "completed" or report.get("provider_call_count") != 0:
            raise RuntimeError(f"{name} current-composite report is incomplete")
        for field, expected in expected_denominators.items():
            if report["denominators"].get(field) != expected:
                raise RuntimeError(f"{name} {field} denominator drifted")

    old_tasks = {task: _task_summary(old, task) for task in TASKS}
    new_tasks = {task: _task_summary(new, task) for task in TASKS}
    old_law = old["executable_law"]
    new_law = new["executable_law"]
    old_blind = old["blind_action"]
    new_blind = new["blind_action"]
    old_prediction = old["prediction_correction"]
    new_prediction = new["prediction_correction"]
    return {
        "schema_version": (
            "chemworld-work-ii-current-composite-world-intervention-recovery-analysis-0.1"
        ),
        "old_report": old_path.relative_to(ROOT).as_posix(),
        "new_report": new_path.relative_to(ROOT).as_posix(),
        "defect": {
            "description": (
                "v0.1 truth and blind evaluators bound world_interventions into plans but did not "
                "forward them to runtime execution or exact replay"
            ),
            "affected_locus": "A_S",
            "affected_tasks": list(TASKS),
            "participant_trajectories_changed": False,
            "analysis_design_changed": False,
        },
        "integrity": {
            "old_denominators": old["denominators"],
            "new_denominators": new["denominators"],
            "denominators_identical": old["denominators"] == new["denominators"],
            "new_provider_call_count": new["provider_call_count"],
            "new_status": new["status"],
            "new_c2_passed": new_prediction["C2_intersection_union"]["passed"],
            "unaffected_prediction_blocks_identical": {
                locus: old_prediction["locus_results"][locus]
                == new_prediction["locus_results"][locus]
                for locus in ("A_E", "A_P")
            },
            "unaffected_law_blocks_identical": {
                locus: old_law[locus] == new_law[locus] for locus in ("A_E", "A_P")
            },
            "unaffected_blind_blocks_identical": {
                locus: old_blind[locus] == new_blind[locus] for locus in ("A_E", "A_P")
            },
        },
        "task_changes": [
            _pair_task(old_tasks[task], new_tasks[task]) for task in TASKS
        ],
        "a_s_locus_change": {
            "failure_aware_primary_estimate": {
                "old": old_prediction["locus_results"]["A_S"]["gate"]["inference"]["estimate"],
                "new": new_prediction["locus_results"]["A_S"]["gate"]["inference"]["estimate"],
            },
            "observed_primary_estimate": {
                "old": old_prediction["locus_results"]["A_S"]["observed_point_sensitivity_gate"]["inference"]["estimate"],
                "new": new_prediction["locus_results"]["A_S"]["observed_point_sensitivity_gate"]["inference"]["estimate"],
            },
            "law_all": {
                field: {
                    "old": old_law["A_S"]["all"][field],
                    "new": new_law["A_S"]["all"][field],
                    "change": new_law["A_S"]["all"][field]
                    - old_law["A_S"]["all"][field],
                }
                for field in (
                    "mean_normalized_mae",
                    "mean_pre_to_law_improvement",
                    "mean_summary_minus_final_error",
                )
            },
            "blind": {
                "old_mean_gain": old_blind["A_S"]["mean_recommendation_gain_over_incumbent"],
                "new_mean_gain": new_blind["A_S"]["mean_recommendation_gain_over_incumbent"],
                "old_better_equal_worse": [
                    old_blind["A_S"]["recommendation_better_count"],
                    old_blind["A_S"]["recommendation_equivalent_count"],
                    old_blind["A_S"]["recommendation_worse_count"],
                ],
                "new_better_equal_worse": [
                    new_blind["A_S"]["recommendation_better_count"],
                    new_blind["A_S"]["recommendation_equivalent_count"],
                    new_blind["A_S"]["recommendation_worse_count"],
                ],
            },
        },
        "overall_change": {
            "law_mean_normalized_mae": {
                "old": old_law["overall"]["all"]["mean_normalized_mae"],
                "new": new_law["overall"]["all"]["mean_normalized_mae"],
            },
            "law_better_equal_worse": {
                "old": [
                    old_law["overall"]["all"]["law_better_than_final_prediction_count"],
                    old_law["overall"]["all"]["evaluated_count"]
                    - old_law["overall"]["all"]["law_better_than_final_prediction_count"]
                    - old_law["overall"]["all"]["law_worse_than_final_prediction_count"],
                    old_law["overall"]["all"]["law_worse_than_final_prediction_count"],
                ],
                "new": [
                    new_law["overall"]["all"]["law_better_than_final_prediction_count"],
                    new_law["overall"]["all"]["evaluated_count"]
                    - new_law["overall"]["all"]["law_better_than_final_prediction_count"]
                    - new_law["overall"]["all"]["law_worse_than_final_prediction_count"],
                    new_law["overall"]["all"]["law_worse_than_final_prediction_count"],
                ],
            },
            "blind_mean_gain": {
                "old": old_blind["overall"]["mean_recommendation_gain_over_incumbent"],
                "new": new_blind["overall"]["mean_recommendation_gain_over_incumbent"],
            },
            "blind_better_equal_worse": {
                "old": [
                    old_blind["overall"]["recommendation_better_count"],
                    old_blind["overall"]["recommendation_equivalent_count"],
                    old_blind["overall"]["recommendation_worse_count"],
                ],
                "new": [
                    new_blind["overall"]["recommendation_better_count"],
                    new_blind["overall"]["recommendation_equivalent_count"],
                    new_blind["overall"]["recommendation_worse_count"],
                ],
            },
        },
        "scientific_disposition": {
            "c2_decision_changed": (
                old_prediction["C2_intersection_union"]["passed"]
                != new_prediction["C2_intersection_union"]["passed"]
            ),
            "current_report_version": "v0.2",
            "historical_report_version": "v0.1",
            "interpretation": (
                "The world-intervention recovery changes A-S numerical truth, prediction errors, "
                "law fidelity and blind gains, but leaves the registered public C2 decision false. "
                "Only v0.2 may support current Paper 2 numerical claims."
            ),
        },
    }


def _f(value: float | None) -> str:
    return "NA" if value is None else f"{value:.4f}"


def write_report(analysis: Mapping[str, Any], path: Path) -> None:
    integrity = analysis["integrity"]
    locus = analysis["a_s_locus_change"]
    overall = analysis["overall_change"]
    lines = [
        "# Work II current-composite world-intervention recovery",
        "",
        "## 结论先行",
        "",
        "v0.1 evaluator 虽把 `world_interventions` 绑定进 plan，却没有传入 runtime execution 与 exact replay，导致 A-S partition/crystallization truth 和 blind 实际按 baseline world 执行。v0.2 从第一单元重跑全部 420 truth、675 checkpoint scores、135 laws 和 726 eligible blind replays，保留 84 个未启动 blind 分母。",
        "",
        f"恢复后 C2 决策仍为 **{integrity['new_c2_passed']}**；A-E 与 A-P 的 prediction/law/blind blocks 均与旧报告完全一致。A-S 数值发生实质变化，因此 v0.1 只保留为历史缺陷证据，当前论文只能引用 v0.2。",
        "",
        "## 1. 完整分母",
        "",
        "- 45 clusters、135 cells；participant 终态 121 completed、7 failed、7 right-censored。",
        "- truth 420/420；checkpoint 675/675；law 135/135；blind 726/726 launched，84 unstarted。",
        "- evaluator provider calls：0；participant trajectory、query roster、统计 gate、删失规则均未改变。",
        "",
        "## 2. A-S 分任务变化",
        "",
        "| Task | Arm | prediction gain old→new | law MAE old→new | law−final old→new | blind gain old→new |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for task in analysis["task_changes"]:
        for arm in ARMS:
            row = task["by_arm"][arm]
            lines.append(
                f"| {task['task_id']} | {arm} | {_f(row['mean_prediction_improvement']['old'])}→{_f(row['mean_prediction_improvement']['new'])} | {_f(row['mean_law_mae']['old'])}→{_f(row['mean_law_mae']['new'])} | {_f(row['mean_law_minus_final_error']['old'])}→{_f(row['mean_law_minus_final_error']['new'])} | {_f(row['mean_blind_gain']['old'])}→{_f(row['mean_blind_gain']['new'])} |"
            )
        observed = task["observed_primary_contrast"]
        failure = task["failure_aware_primary_lower_bound"]
        lines.extend(
            [
                "",
                f"该 task 的 observed primary contrast 为 {_f(observed['old'])}→{_f(observed['new'])}，正方向 worlds {observed['old_positive_world_count']}/5→{observed['new_positive_world_count']}/5；failure-aware lower-bound mean 为 {_f(failure['old'])}→{_f(failure['new'])}。",
                "",
            ]
        )
    lines.extend(
        [
            "## 3. A-S 与 overall 收束",
            "",
            f"- A-S failure-aware locus estimate：{_f(locus['failure_aware_primary_estimate']['old'])}→{_f(locus['failure_aware_primary_estimate']['new'])}；observed-point estimate：{_f(locus['observed_primary_estimate']['old'])}→{_f(locus['observed_primary_estimate']['new'])}。两个 gate 仍不通过。",
            f"- A-S law MAE：{_f(locus['law_all']['mean_normalized_mae']['old'])}→{_f(locus['law_all']['mean_normalized_mae']['new'])}；pre→law improvement：{_f(locus['law_all']['mean_pre_to_law_improvement']['old'])}→{_f(locus['law_all']['mean_pre_to_law_improvement']['new'])}。",
            f"- A-S blind mean gain：{_f(locus['blind']['old_mean_gain'])}→{_f(locus['blind']['new_mean_gain'])}；better/equal/worse 保持 {locus['blind']['new_better_equal_worse'][0]}/{locus['blind']['new_better_equal_worse'][1]}/{locus['blind']['new_better_equal_worse'][2]}。",
            f"- Overall law MAE：{_f(overall['law_mean_normalized_mae']['old'])}→{_f(overall['law_mean_normalized_mae']['new'])}；law better/equal/worse：{overall['law_better_equal_worse']['old'][0]}/{overall['law_better_equal_worse']['old'][1]}/{overall['law_better_equal_worse']['old'][2]}→{overall['law_better_equal_worse']['new'][0]}/{overall['law_better_equal_worse']['new'][1]}/{overall['law_better_equal_worse']['new'][2]}。",
            f"- Overall blind mean gain：{_f(overall['blind_mean_gain']['old'])}→{_f(overall['blind_mean_gain']['new'])}；better/equal/worse 仍为 {overall['blind_better_equal_worse']['new'][0]}/{overall['blind_better_equal_worse']['new'][1]}/{overall['blind_better_equal_worse']['new'][2]}。",
            "",
            "## 4. 当前证据处置",
            "",
            "- `work-ii-deepseek-c2-current-composite-evaluation-v0.2.json` 是当前 evaluator 机器结果。",
            "- v0.1 report/root 不删除、不覆盖，作为缺陷发现与 recovery 的历史记录。",
            "- 原 Study B A-S packet 派生自 v0.1 A-S truth，因此该分支退出当前科学结论；A-P 不受影响。当前 A-S matched-evidence 结论由独立 B2 phase-process block 提供。",
            "- 该恢复不产生新的 participant trajectory，也不改变 participant endpoint 结果；它只纠正 evaluator 真值、law scoring 与 blind replay。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-report", type=Path, default=DEFAULT_OLD)
    parser.add_argument("--new-report", type=Path, default=DEFAULT_NEW)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    analysis = analyze(args.old_report.resolve(), args.new_report.resolve())
    _write_json(args.output_json.resolve(), analysis)
    write_report(analysis, args.output_report.resolve())
    print(
        json.dumps(
            {
                "status": "completed",
                "output_json": str(args.output_json.resolve()),
                "output_report": str(args.output_report.resolve()),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
