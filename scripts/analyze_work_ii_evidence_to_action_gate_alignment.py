#!/usr/bin/env python3
# ruff: noqa: E501, RUF001
"""Relate retained oracle ranking quality to the frozen action endpoint."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean, median
from typing import Any

import run_work_ii_multi_task_open_action_pilot as task_runner

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import (
    evaluate_oracle_law_candidate_order,
    predict_candidate_ranking_from_law,
    score_terminal_ranking,
    split_registered_query_pool_maximin,
)

ROOT = Path(__file__).resolve().parents[1]
FORMAL_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json"
)
LARGE_GRID_PROTOCOL = ROOT / "configs/benchmark/work_ii_evidence_to_action_large_grid_v1.0.json"
FORMAL_ROOT = ROOT / "runs/formal/w2-51-e2a-20260824-restart1"
CONSTRUCTION_ROOT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-large-grid-v1.0"
    / "construction-screen-restart1"
)
PROSPECTIVE_ROOT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-large-grid-v1.0"
    / "prospective-qualification-v0.1"
)
OUTPUT_JSON = (
    ROOT
    / "workstreams/flagship_tasks/reports"
    / "work-ii-evidence-to-action-gate-alignment-v0.1.json"
)
OUTPUT_MD = (
    ROOT / "workstreams/flagship_tasks/reports" / "WORK_II_EVIDENCE_TO_ACTION_GATE_ALIGNMENT_ZH.md"
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain an object")
    return payload


def _truth(path: Path) -> dict[str, dict[str, Any]]:
    report = _load(path)
    truth = report.get("truth")
    if report.get("status") != "completed" or not isinstance(truth, dict):
        raise ValueError(f"{path}: retained truth report is incomplete")
    return {str(query_id): dict(metrics) for query_id, metrics in truth.items()}


def _task_contracts(protocol_path: Path) -> dict[str, dict[str, Any]]:
    protocol = _load(protocol_path)
    contracts: dict[str, dict[str, Any]] = {}
    for task_id, source_path in protocol["task_runtime_sources"].items():
        source = _load((ROOT / str(source_path)).resolve())
        checkpoint = source.get("belief_checkpoint")
        if not isinstance(checkpoint, dict):
            raise ValueError(f"{task_id}: belief checkpoint is missing")
        registered = checkpoint.get("held_out_queries")
        if not isinstance(registered, list):
            raise ValueError(f"{task_id}: registered query pool is missing")
        feature_ids = [str(item) for item in checkpoint.get("allowed_feature_ids", [])]
        candidates, _ = split_registered_query_pool_maximin(
            registered,
            allowed_feature_ids=feature_ids,
        )
        contracts[str(task_id)] = {
            "candidates": candidates,
            "candidate_ids": [str(row["query_id"]) for row in candidates],
            "feature_ids": feature_ids,
            "metric_ids": task_runner._task_metrics(source),
        }
    return contracts


def _analyze_row(
    *,
    group_id: str,
    evidence_role: str,
    grid_query_count: int,
    task_id: str,
    world_seed: int,
    artifact_path: Path,
    truth_path: Path,
    contract: dict[str, Any],
    recorded_spearman: float,
    recorded_top1: bool,
    construction_role: str | None = None,
) -> dict[str, Any]:
    artifact = _load(artifact_path)
    all_truth = _truth(truth_path)
    candidate_ids = contract["candidate_ids"]
    if not set(candidate_ids).issubset(all_truth):
        raise ValueError(f"{task_id}/seed-{world_seed}: retained candidate truth is incomplete")
    candidate_truth = {query_id: all_truth[query_id] for query_id in candidate_ids}
    fit_ids = [str(item) for item in artifact.get("fit_query_ids", [])]
    overlap = len(set(fit_ids) & set(candidate_ids))
    if overlap:
        raise ValueError(f"{task_id}/seed-{world_seed}: fit/candidate overlap is nonzero")
    if artifact.get("fit_used_candidate_outcomes") is not False:
        raise ValueError(f"{task_id}/seed-{world_seed}: candidate-outcome-free fit is not proven")
    candidate_outcomes_used = artifact.get(
        "candidate_outcomes_used", artifact.get("fit_used_candidate_outcomes")
    )
    if candidate_outcomes_used is not False:
        raise ValueError(f"{task_id}/seed-{world_seed}: artifact reports candidate outcome use")
    if artifact.get("candidate_information_included") is not False:
        raise ValueError(f"{task_id}/seed-{world_seed}: artifact includes candidate information")

    implied = predict_candidate_ranking_from_law(
        artifact["law_summary"],
        candidate_queries=contract["candidates"],
        allowed_feature_ids=contract["feature_ids"],
        allowed_metric_ids=contract["metric_ids"],
        evidence_catalog=fit_ids,
    )
    qualification = evaluate_oracle_law_candidate_order(
        artifact,
        candidate_queries=contract["candidates"],
        candidate_truth=candidate_truth,
        allowed_feature_ids=contract["feature_ids"],
        allowed_metric_ids=contract["metric_ids"],
        minimum_rank_correlation=0.80,
    )
    scored = score_terminal_ranking(
        implied["law_implied_ranking"],
        candidate_truth,
    )
    recomputed_spearman = float(qualification["spearman_rank_correlation"])
    recomputed_top1 = bool(qualification["top1_agreement"])
    if not math.isclose(recomputed_spearman, recorded_spearman, abs_tol=1.0e-12):
        raise ValueError(f"{task_id}/seed-{world_seed}: retained Spearman does not reproduce")
    if recomputed_top1 != recorded_top1:
        raise ValueError(f"{task_id}/seed-{world_seed}: retained Top-1 does not reproduce")

    return {
        "group_id": group_id,
        "evidence_role": evidence_role,
        "construction_role": construction_role,
        "task_id": task_id,
        "world_seed": world_seed,
        "grid_query_count": grid_query_count,
        "candidate_count": len(candidate_ids),
        "spearman_rank_correlation": recomputed_spearman,
        "rank_gate_passed": recomputed_spearman >= 0.80,
        "top1": int(scored["top1"]),
        "selected_rank": scored["selected_rank"],
        "within_0_01_of_best": int(scored["within_0_01_of_best"]),
        "raw_regret": scored["raw_regret"],
        "normalized_regret": scored["failure_aware_normalized_regret"],
        "pairwise_ranking_agreement_excluding_near_ties": scored[
            "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01"
        ],
        "qualified_pair_count": scored["qualified_pair_count"],
        "fit_candidate_overlap_count": overlap,
        "candidate_outcomes_used": False,
        "recorded_metrics_reproduced": True,
        "new_truth_execution_count": 0,
        "provider_call_count": 0,
        "physical_experiment_count": 0,
    }


def _formal_rows() -> list[dict[str, Any]]:
    contracts = _task_contracts(FORMAL_PROTOCOL)
    summary = _load(FORMAL_ROOT / "provider-free-preparation-summary.json")
    rows: list[dict[str, Any]] = []
    for retained in summary["qualification_rows"]:
        task_id = str(retained["task_id"])
        world_seed = int(retained["world_seed"])
        cluster_root = FORMAL_ROOT / "prepared/clusters" / task_id / f"seed-{world_seed}" / task_id
        artifact_path = cluster_root / "oracle-artifact.json"
        if not artifact_path.is_file():
            artifact_path = cluster_root / "rejected-oracle-artifact.json"
        oracle = retained["oracle_qualification"]
        rows.append(
            _analyze_row(
                group_id="w2_51_96_grid_fresh_formal_preparation",
                evidence_role="fresh_formal_preparation",
                grid_query_count=96,
                task_id=task_id,
                world_seed=world_seed,
                artifact_path=artifact_path,
                truth_path=cluster_root / "candidate-truth/report.json",
                contract=contracts[task_id],
                recorded_spearman=float(oracle["spearman_rank_correlation"]),
                recorded_top1=bool(oracle["top1_agreement"]),
            )
        )
    return rows


def _large_grid_rows(root: Path, group_id: str, evidence_role: str) -> list[dict[str, Any]]:
    contracts = _task_contracts(LARGE_GRID_PROTOCOL)
    summary = _load(root / "summary.json")
    retained_rows = summary.get("unit_rows", summary.get("cluster_rows"))
    if not isinstance(retained_rows, list):
        raise ValueError(f"{root}: unit rows are missing")
    rows: list[dict[str, Any]] = []
    for retained in retained_rows:
        task_id = str(retained["task_id"])
        world_seed = int(retained["world_seed"])
        rows.append(
            _analyze_row(
                group_id=group_id,
                evidence_role=evidence_role,
                grid_query_count=320,
                task_id=task_id,
                world_seed=world_seed,
                artifact_path=root / task_id / f"seed-{world_seed}" / "oracle_artifact.json",
                truth_path=(
                    root
                    / "registered-truth"
                    / task_id
                    / f"seed-{world_seed}"
                    / "grid-truth-summary.json"
                ),
                contract=contracts[task_id],
                recorded_spearman=float(retained["spearman_rank_correlation"]),
                recorded_top1=bool(retained["top1_agreement"]),
                construction_role=(
                    str(retained["role"]) if isinstance(retained.get("role"), str) else None
                ),
            )
        )
    return rows


def _group_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "unit_version_count": len(rows),
        "rank_gate_pass_count": sum(bool(row["rank_gate_passed"]) for row in rows),
        "top1_count": sum(int(row["top1"]) for row in rows),
        "within_0_01_of_best_count": sum(int(row["within_0_01_of_best"]) for row in rows),
        "median_selected_rank": median(float(row["selected_rank"]) for row in rows),
        "mean_normalized_regret": mean(float(row["normalized_regret"]) for row in rows),
        "mean_tie_aware_pairwise_agreement": mean(
            float(row["pairwise_ranking_agreement_excluding_near_ties"]) for row in rows
        ),
        "rank_pass_but_wrong_top1_count": sum(
            bool(row["rank_gate_passed"]) and not bool(row["top1"]) for row in rows
        ),
        "rank_fail_but_top1_count": sum(
            not bool(row["rank_gate_passed"]) and bool(row["top1"]) for row in rows
        ),
    }


def _repair_rows(construction_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    previous = {
        "retained_v0.2_failure": (0.7857142857142857, False),
        "retained_v0.4_failure": (0.7857142857142857, False),
        "retained_w2_51_failure": (0.7380952380952381, False),
        "retained_v0.3_failure": (0.5952380952380952, False),
    }
    rows: list[dict[str, Any]] = []
    for row in construction_rows:
        role = row.get("construction_role")
        if role not in previous:
            continue
        previous_spearman, previous_top1 = previous[str(role)]
        rows.append(
            {
                "task_id": row["task_id"],
                "world_seed": row["world_seed"],
                "previous_96_grid_spearman": previous_spearman,
                "large_320_grid_spearman": row["spearman_rank_correlation"],
                "spearman_change": row["spearman_rank_correlation"] - previous_spearman,
                "previous_96_grid_top1": int(previous_top1),
                "large_320_grid_top1": row["top1"],
                "large_320_grid_normalized_regret": row["normalized_regret"],
                "evidence_role": "exposed_construction_only",
            }
        )
    if len(rows) != 4:
        raise ValueError("the four frozen historical-failure repairs were not all recovered")
    return rows


def _render_markdown(summary: dict[str, Any]) -> str:
    groups = summary["group_summaries"]
    formal = groups["w2_51_96_grid_fresh_formal_preparation"]
    construction = groups["w2_52_320_grid_exposed_construction"]
    prospective = groups["w2_52_320_grid_fresh_prospective"]
    lines = [
        "# Work II oracle gate 与动作目标对齐分析",
        "",
        "## 结论",
        "",
        "冻结的完整排序门槛与真正的动作目标并不等价。96-grid 的 W2-51 已完成单元中，",
        f"`{formal['rank_gate_pass_count']}/{formal['unit_version_count']}` 通过 `rho>=0.80`，但仅",
        f"`{formal['top1_count']}/{formal['unit_version_count']}` 选中真实第一名；反过来，320-grid",
        "在首个全新 prospective world 上虽因 `rho=0.714286` 被合法拒绝，却选中了真实第一名，",
        "其动作 regret 为零。W2-51/W2-52 的终态不改变，但这一分离应成为论文的核心结果，",
        "而不是继续解释成 grid 仍不够大。",
        "",
        "## Programme 收束",
        "",
        "- W2-51 与 W2-52 均按完整固定分母形成终态结果，工作包状态为 `completed`；完成不等于科学门槛通过。",
        "- 两项历史 `rho>=0.80` stop rule 原样保留，但不再是当前 ICLR 写稿、图表或其他独立实验的前置阻断。",
        "- 原 225-session cohort 仍不获 participant 授权；不能用本分析把未执行的五条件因果对比写成已完成。",
        "- 若未来新建 action-aligned prospective control，failure-aware normalized regret、距最优 `<=0.01`",
        "  与 near-tie-aware ordering 是决策指标，complete-ranking Spearman 仅作辅助诊断；新 control 不复用这 16 个已暴露单元。",
        "",
        "## 固定分母结果",
        "",
        "| 证据组 | 单元版本 | rank gate 通过 | Top-1 | 距最优 <=0.01 | 平均 normalized regret | rank过但Top-1错 | rank不过但Top-1对 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, values in (
        ("W2-51 96-grid fresh formal preparation", formal),
        ("W2-52 320-grid exposed construction", construction),
        ("W2-52 320-grid fresh prospective", prospective),
    ):
        lines.append(
            f"| {label} | {values['unit_version_count']} | {values['rank_gate_pass_count']} | "
            f"{values['top1_count']} | {values['within_0_01_of_best_count']} | "
            f"{values['mean_normalized_regret']:.4f} | "
            f"{values['rank_pass_but_wrong_top1_count']} | {values['rank_fail_but_top1_count']} |"
        )
    lines.extend(
        [
            "",
            "320-grid 在 7/7 exposed construction 单元上通过，并修复四个已知 96-grid 失败；这只证明",
            "对已暴露 world 的覆盖改善。首个全新 world 随即出现低完整排序相关但零动作损失，说明",
            "主要问题已从‘是否能拟合已知失败’转为‘oracle 定义是否与研究的动作 estimand 对齐’。",
            "",
            "## 边界",
            "",
            "- 本分析复算 `16/16` 固定单元版本，未删除失败，未产生新 truth、provider call 或物理实验。",
            "- 7 个 construction 单元不能估计泛化；1 个 prospective 单元也不能估计成功率。",
            "- 不回溯修改 `rho>=0.80`、stop rule 或 W2-51/W2-52 disposition，不据此启动原 225-session cohort。",
            "- 投稿主张应是‘完整排序泛化与动作充分性分离’，不是‘320-grid oracle 已经泛化成功’。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=OUTPUT_MD)
    args = parser.parse_args()

    formal_rows = _formal_rows()
    construction_rows = _large_grid_rows(
        CONSTRUCTION_ROOT,
        "w2_52_320_grid_exposed_construction",
        "exposed_construction_only",
    )
    prospective_rows = _large_grid_rows(
        PROSPECTIVE_ROOT,
        "w2_52_320_grid_fresh_prospective",
        "fresh_prospective_qualification",
    )
    rows = [*formal_rows, *construction_rows, *prospective_rows]
    if len(rows) != 16:
        raise ValueError(f"fixed analysis expected 16 unit-version rows, got {len(rows)}")
    grouped = {
        group_id: _group_summary([row for row in rows if row["group_id"] == group_id])
        for group_id in (
            "w2_51_96_grid_fresh_formal_preparation",
            "w2_52_320_grid_exposed_construction",
            "w2_52_320_grid_fresh_prospective",
        )
    }
    summary = {
        "schema_version": "chemworld-work-ii-evidence-to-action-gate-alignment-0.1",
        "status": "completed",
        "analysis_role": "retrospective_provider_free_gate_diagnostic",
        "fixed_unit_version_count": 16,
        "completed_unit_version_count": len(rows),
        "recorded_metric_reproduction_count": sum(
            bool(row["recorded_metrics_reproduced"]) for row in rows
        ),
        "fit_candidate_overlap_count": sum(row["fit_candidate_overlap_count"] for row in rows),
        "candidate_outcome_read_count": 0,
        "new_truth_execution_count": 0,
        "provider_call_count": 0,
        "physical_experiment_count": 0,
        "w2_51_disposition_changed": False,
        "w2_52_disposition_changed": False,
        "rank_threshold_changed": False,
        "programme_closure": {
            "w2_51_work_package_status": "completed_terminal_scientific_rejection_before_provider",
            "w2_52_work_package_status": (
                "completed_terminal_construction_pass_and_prospective_rank_rejection"
            ),
            "blocks_current_iclr_submission": False,
            "blocks_independent_experiment_progress": False,
            "participant_execution_authorized": False,
            "historical_rank_gate_retained": True,
            "future_action_aligned_control": {
                "prospective_only": True,
                "reuses_exposed_unit_versions": False,
                "complete_ranking_spearman_role": "secondary_diagnostic",
                "decision_metrics": [
                    "failure_aware_normalized_regret",
                    "within_0.01_of_best",
                    "pairwise_ordering_excluding_truth_gaps_below_0.01",
                ],
            },
        },
        "group_summaries": grouped,
        "historical_failure_repairs": _repair_rows(construction_rows),
        "unit_rows": rows,
        "interpretation": (
            "Complete-ranking generalization and action sufficiency are distinct: the 96-grid route "
            "often passed the rank gate while missing Top-1, whereas the first fresh 320-grid world "
            "failed the rank gate while selecting the true Top-1 with zero regret."
        ),
        "claim_boundary": (
            "Construction repairs are exposed diagnostics and one prospective unit cannot estimate "
            "a generalization rate or authorize participant execution."
        ),
    }
    write_json_atomic(args.output_json.resolve(), summary)
    args.output_md.resolve().write_text(_render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
