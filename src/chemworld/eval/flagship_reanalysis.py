# ruff: noqa: RUF001
"""Strict, non-destructive reanalysis of the exploratory v0.1 flagship study."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.artifact_paths import (
    repository_relative_reference,
    resolve_flagship_trajectory_reference,
)
from chemworld.eval.mechanism_adaptation import declared_distribution_update

ROOT = Path(__file__).resolve().parents[3]
SOURCE_REPORT = ROOT / "workstreams/flagship_tasks/reports/deepseek-mechanism-diagnostics-v0.1.json"
REANALYSIS_VERSION = "chemworld-flagship-mechanism-diagnostics-reanalysis-0.1.1"


def load_v0_1_report(path: Path = SOURCE_REPORT) -> dict[str, Any]:
    """Load the immutable exploratory report used as the reanalysis source."""

    return json.loads(path.read_text(encoding="utf-8"))


def build_flagship_reanalysis(
    source: Mapping[str, Any],
    *,
    source_path: Path = SOURCE_REPORT,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    """Reclassify v0.1 without changing its raw trajectories or original report."""

    campaigns = _unique_deepseek_campaigns(source.get("campaigns", []))
    shifted_traces = [
        (
            _diagnostic_trace(
                resolve_flagship_trajectory_reference(
                    str(campaign["shifted"]["trajectory_path"]),
                    repository_root=repository_root,
                )
            ),
            str(campaign["shifted_truth_id"]),
        )
        for campaign in campaigns
    ]
    all_traces = [
        _diagnostic_trace(
            resolve_flagship_trajectory_reference(
                str(campaign[phase]["trajectory_path"]),
                repository_root=repository_root,
            )
        )
        for campaign in campaigns
        for phase in ("iid", "shifted")
    ]
    clean_update = _clean_update_summary(shifted_traces)
    probability_consistency = _change_probability_consistency(all_traces)
    outcome_rows = _reclassified_outcomes(source)
    lifecycle = _lifecycle_audit(campaigns)
    ranking = _tie_aware_ranking(source)
    integrity = _integrity_audit(
        source_path,
        campaigns,
        repository_root=repository_root,
    )
    old_resources = dict(source.get("resource_summary", {}))
    return {
        "schema_version": REANALYSIS_VERSION,
        "source_schema_version": source.get("schema_version"),
        "source_report": _relative_path(source_path, root=repository_root),
        "source_report_sha256": _sha256(source_path),
        "status": "strict_reanalysis_complete",
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "raw_v0_1_artifacts_modified": False,
        "primary_judgment": (
            "The v0.1 run supports the benchmark-design story but does not establish "
            "reliable mechanism discovery by DeepSeek. Its sole former genuine result is "
            "a provisional threshold-level joint success with assisted campaign history."
        ),
        "confirmed_mechanism_discovery_count": 0,
        "provisional_threshold_joint_success_count": sum(
            row["reanalysis_classification"] == "provisional_threshold_joint_success"
            for row in outcome_rows
        ),
        "outcome_reanalysis": {
            "rows": outcome_rows,
            "counts": dict(
                sorted(Counter(row["reanalysis_classification"] for row in outcome_rows).items())
            ),
            "confirmation_rule": (
                "Threshold crossing is provisional until v0.2 Gates 0 and A-E pass on "
                "multi-seed, paired confirmatory data."
            ),
        },
        "declared_distribution_update_audit": clean_update,
        "change_probability_consistency_audit": probability_consistency,
        "lifecycle_autonomy_audit": lifecycle,
        "ranking_reanalysis": ranking,
        "feedback_interpretation": {
            "legacy_mean_score_contrast_true_minus_permuted": source.get(
                "experiment_2_feedback_ablation", {}
            ).get("mean_evidence_reliance"),
            "causal_interpretation_allowed": False,
            "reason": (
                "Conditions used independent provider samples, so the contrast combines "
                "feedback content, provider variation, initial-action differences, and "
                "downstream trajectory divergence."
            ),
            "required_replacement": (
                "paired local-prefix reaction test plus paired repeated full campaigns"
            ),
        },
        "identifiability_status": {
            "certificate_present_in_v0_1": False,
            "no_change_twin_present_in_v0_1": False,
            "candidate_operational_definitions_present_in_prompt": False,
            "candidate_order_randomized": False,
            "interpretation": (
                "Agent failure and insufficient task information cannot yet be separated."
            ),
        },
        "provider_control_audit": {
            "model_id_recorded": True,
            "request_ids_recorded": True,
            "system_fingerprint_observed": True,
            "thinking_recorded": True,
            "response_max_tokens_recorded": True,
            "temperature_recorded": False,
            "top_p_recorded": False,
            "provider_seed_recorded": False,
            "per_request_timestamp_recorded": False,
            "request_payload_hash_recorded": False,
            "claim_boundary": (
                "The user-side benchmark performs no training or weight updates; hosted "
                "provider internals cannot be proven fixed from these receipts."
            ),
        },
        "resource_summary": old_resources,
        "integrity_audit": integrity,
        "v0_2_required_gates": [
            "Gate 0: integrity, leakage, receipts, exclusions, replay",
            "Gate A: active-oracle and fixed-decoder identifiability",
            "Gate B: paired no-change twins and randomized change time",
            "Gate C: local feedback sensitivity separated from provider noise",
            "Gate D: open-loop world effect, frozen policy, adaptation and recovery",
            "Gate E: procedural autonomy and separate assisted scientific score",
        ],
        "claim_boundary": [
            "one public world seed",
            "two post-change experiments only",
            "exploratory provider sampling",
            "mixed decision interfaces in descriptive ranking",
            "no trained-weight update by ChemWorld",
            "no formal mechanism-identifiability certificate",
        ],
    }


def render_flagship_reanalysis_markdown(report: Mapping[str, Any]) -> str:
    """Render a readable Chinese decision report."""

    updates = report["declared_distribution_update_audit"]
    consistency = report["change_probability_consistency_audit"]
    lifecycle = report["lifecycle_autonomy_audit"]
    outcomes = report["outcome_reanalysis"]
    ranking = report["ranking_reanalysis"]
    resources = report["resource_summary"]
    rows = outcomes["rows"]
    lines = [
        "# DeepSeek 机制诊断 v0.1.1 严格重分析",
        "",
        f"- 状态：`{report['status']}`",
        "- 原始 v0.1 报告和轨迹保持不变；本文件只做可追溯重分析。",
        (
            "- ChemWorld 的角色是 Agent 能力测试/训练环境；本次评测不训练、不微调、"
            "也不更新 DeepSeek 权重。"
        ),
        "- 当前仍不可发表为‘DeepSeek 已具备可靠机制发现能力’。",
        "",
        "## 最终判断",
        "",
        report["primary_judgment"],
        "",
        (
            f"原报告唯一的 `genuine_experimental` 现在降为 "
            f"`provisional_threshold_joint_success`：确认级机制发现为 "
            f"{report['confirmed_mechanism_discovery_count']}，暂定阈值级联合成功为 "
            f"{report['provisional_threshold_joint_success_count']}。原因不是抹掉结果，而是它来自单种子、"
            "两次 post-change 实验、尚无可识别性证书，且其 campaign 历史含系统辅助收尾。"
        ),
        "",
        "## 结果与理解重新分类",
        "",
        _table(
            ["任务", "反馈", "最终得分", "真值概率", "旧分类", "v0.1.1 分类", "自主性"],
            [
                [
                    row["task_id"],
                    row["feedback_condition"],
                    _fmt(row["final_objective"]),
                    _fmt(row["truth_probability"]),
                    row["legacy_classification"],
                    row["reanalysis_classification"],
                    row["autonomy_status"],
                ]
                for row in rows
            ],
        ),
        "",
        f"分类计数：`{json.dumps(outcomes['counts'], ensure_ascii=False, sort_keys=True)}`。",
        "",
        "## 自报分布更新审计",
        "",
        (
            f"旧算法形成 {updates['legacy_pair_count']} 个相邻 belief 对，其中 "
            f"{updates['excluded_failure_involved_pair_count']} 个涉及 `model_failure`，"
            f"{updates['excluded_nonadjacent_pair_count']} 个跨过未产生模型 belief 的生命周期动作。"
            f"清洁口径只保留相邻且两端都是 `model_decision` 的 {updates['clean_pair_count']} 对。"
        ),
        (
            f"清洁口径下，平均自报信息值为 {_fmt(updates['mean_declared_information_value'])}，"
            f"平均 JS 分布变化仅 {_fmt(updates['mean_declared_distribution_js_shift'])}，"
            f"平均 `Δlog q(truth)` 为 {_fmt(updates['mean_truth_log_probability_change'])}。"
        ),
        "这些量只能叫‘自报分布更新’，不能叫已校准 EIG 或 Bayesian posterior 更新。",
        "",
        "## change probability 一致性",
        "",
        (
            f"在 {consistency['decision_count']} 个有效模型决策中，独立上报的 "
            "`change_probability` 与 "
            f"`1-q(no_change)` 的平均绝对差为 {_fmt(consistency['mean_absolute_difference'])}；"
            f"{_pct(consistency['fraction_above_0_2'])} 的决策差异超过 0.2。"
        ),
        "v0.2 已删除这一重复自由度，变化概率一律由 `1-q(no_change)` 推导。",
        "",
        "## 生命周期与自主性",
        "",
        (
            f"共有 {lifecycle['guardrail_action_count']} 次系统收尾动作，影响 "
            f"{lifecycle['affected_experiment_count']}/40 个实验、"
            f"{lifecycle['affected_phase_count']}/20 个阶段和 "
            f"{lifecycle['affected_campaign_count']}/10 个独立 campaign。"
        ),
        "因此不能再用 7/40=17.5% 同时代表动作率和实验覆盖率；正确实验影响率是 10%。",
        (
            "唯一暂定联合成功的最佳当前实验是自主完成的，但此前 shifted 实验有辅助 final assay，"
            "所以标为 `autonomous_current_experiment_with_assisted_history`。"
        ),
        "",
        "## 排名与反馈的解释边界",
        "",
        (
            f"平局改用 average rank；IID/shifted Spearman 仍为 "
            f"{_fmt(ranking['spearman_rank_correlation'])}，严格反转为 "
            f"{ranking['strict_rank_inversion_count']} 对。"
        ),
        "recipe 级方法与 operation 级方法的决策接口不同，因此总体混合排名只保留为描述性结果。",
        (
            "旧的 `J_true-J_permuted` 平均值仍可作为分数对比，但不能解释为错误反馈更好或正确反馈"
            "降低性能；它没有隔离 provider 采样噪声。"
        ),
        "",
        "## 资源与完整性",
        "",
        f"- 独立 DeepSeek campaign：{resources.get('deepseek_campaign_count')}",
        (
            f"- 模型调用：{resources.get('model_call_count')}；provider failure："
            f"{resources.get('provider_failure_count')}；重试：{resources.get('retry_count')}"
        ),
        (
            f"- 输入/输出 token：{resources.get('input_token_count')} / "
            f"{resources.get('output_token_count')}"
        ),
        f"- 估算费用：USD {_fmt(resources.get('monetary_cost_usd'), digits=6)}",
        f"- 20 条阶段轨迹哈希核验：`{report['integrity_audit']['all_trajectory_hashes_match']}`",
        "",
        "## 下一版的确认门槛",
        "",
        *[f"- {item}" for item in report["v0_2_required_gates"]],
        "",
        (
            "在外部多种子 DeepSeek campaign 真正运行并通过全部 Gate 前，v0.2 状态必须保持 "
            "`publication_ready=false`。"
        ),
    ]
    return "\n".join(lines) + "\n"


def _unique_deepseek_campaigns(raw_campaigns: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_campaigns, Sequence):
        return []
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_campaigns:
        if not isinstance(raw, Mapping) or raw.get("method_id") != "deepseek_v4_flash":
            continue
        shifted = raw.get("shifted")
        path = shifted.get("trajectory_path") if isinstance(shifted, Mapping) else None
        if not isinstance(path, str) or path in seen:
            continue
        seen.add(path)
        result.append(dict(raw))
    return result


def _diagnostic_trace(path: Path) -> list[dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    for operation_index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        row = json.loads(line)
        raw_trace = row.get("agent_trace")
        decision = raw_trace[-1] if isinstance(raw_trace, list) and raw_trace else None
        if not isinstance(decision, Mapping):
            continue
        belief = decision.get("mechanism_belief")
        if not isinstance(belief, Mapping):
            continue
        try:
            distribution = {str(key): float(value) for key, value in belief.items()}
            trace.append(
                {
                    "operation_index": operation_index,
                    "experiment_index": int(row.get("experiment_index", 0)),
                    "status": str(decision.get("status") or "unknown"),
                    "operation": row.get("operation_type"),
                    "mechanism_distribution": distribution,
                    "change_probability": float(decision["change_probability"]),
                    "declared_information_value": float(decision["expected_information_gain"]),
                }
            )
        except (KeyError, TypeError, ValueError):
            continue
    return trace


def _clean_update_summary(
    traces: Sequence[tuple[Sequence[Mapping[str, Any]], str]],
) -> dict[str, Any]:
    clean: list[dict[str, float]] = []
    declared_values: list[float] = []
    legacy_count = 0
    failures = 0
    gaps = 0
    for trace, truth in traces:
        for current, following in itertools.pairwise(trace):
            legacy_count += 1
            if current["status"] != "model_decision" or following["status"] != "model_decision":
                failures += 1
                continue
            if int(following["operation_index"]) != int(current["operation_index"]) + 1:
                gaps += 1
                continue
            distribution = current["mechanism_distribution"]
            clean.append(
                declared_distribution_update(
                    distribution,
                    following["mechanism_distribution"],
                    truth=truth,
                )
            )
            declared_values.append(float(current["declared_information_value"]))
    return {
        "legacy_pair_count": legacy_count,
        "clean_pair_count": len(clean),
        "excluded_failure_involved_pair_count": failures,
        "excluded_nonadjacent_pair_count": gaps,
        "mean_declared_information_value": _mean(declared_values),
        "mean_declared_distribution_js_shift": _mean(
            [item["declared_distribution_js_shift"] for item in clean]
        ),
        "mean_declared_distribution_kl_shift": _mean(
            [item["declared_distribution_kl_shift"] for item in clean]
        ),
        "mean_declared_normalized_entropy_change": _mean(
            [item["declared_normalized_entropy_change"] for item in clean]
        ),
        "mean_truth_log_probability_change": _mean(
            [item["truth_log_probability_change"] for item in clean]
        ),
        "mean_brier_improvement": _mean([item["brier_improvement"] for item in clean]),
        "calibration_claim_allowed": False,
    }


def _change_probability_consistency(
    traces: Sequence[Sequence[Mapping[str, Any]]],
) -> dict[str, Any]:
    differences: list[float] = []
    for trace in traces:
        for row in trace:
            if row["status"] != "model_decision":
                continue
            distribution = row["mechanism_distribution"]
            total = sum(float(value) for value in distribution.values())
            derived = 1.0 - float(distribution["no_change"]) / total
            differences.append(abs(float(row["change_probability"]) - derived))
    ordered = sorted(differences)
    return {
        "decision_count": len(differences),
        "mean_absolute_difference": _mean(differences),
        "median_absolute_difference": (
            0.5 * (ordered[(len(ordered) - 1) // 2] + ordered[len(ordered) // 2])
            if ordered
            else None
        ),
        "maximum_absolute_difference": max(differences) if differences else None,
        "fraction_above_0_2": _fraction(differences, 0.2),
        "fraction_above_0_4": _fraction(differences, 0.4),
    }


def _reclassified_outcomes(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = source.get("experiment_4_outcome_understanding", {}).get("rows", [])
    guard_by_id = {
        campaign["campaign_id"]: campaign.get("lifecycle_guardrail_log", [])
        for campaign in _unique_deepseek_campaigns(source.get("campaigns", []))
    }
    result: list[dict[str, Any]] = []
    for raw in rows:
        high = raw.get("type") in {"genuine_experimental", "accidental_optimizer"}
        identified = bool(raw.get("mechanism_identified"))
        if high and identified:
            classification = "provisional_threshold_joint_success"
        elif high:
            classification = "high_outcome_without_identification"
        elif identified:
            classification = "identification_without_recovery"
        else:
            classification = "joint_failure"
        campaign_id = str(raw.get("campaign_id"))
        logs = guard_by_id.get(campaign_id, [])
        if campaign_id == "feedback--electrochemical-conversion--delayed_feedback--seed0" or logs:
            autonomy = "autonomous_current_experiment_with_assisted_history"
        else:
            autonomy = "fully_autonomous_campaign"
        result.append(
            {
                "campaign_id": campaign_id,
                "experiment_id": raw.get("experiment_id"),
                "task_id": raw.get("task_id"),
                "feedback_condition": raw.get("feedback_condition"),
                "final_objective": raw.get("final_objective"),
                "truth_probability": raw.get("truth_probability"),
                "mechanism_identified_at_legacy_threshold": identified,
                "legacy_classification": raw.get("type"),
                "reanalysis_classification": classification,
                "confirmed_mechanism_discovery": False,
                "autonomy_status": autonomy,
            }
        )
    return result


def _lifecycle_audit(campaigns: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    actions: list[dict[str, Any]] = []
    affected_experiments: set[tuple[str, str, int]] = set()
    affected_phases: set[tuple[str, str]] = set()
    affected_campaigns: set[str] = set()
    autonomous_iid_best: list[dict[str, Any]] = []
    for campaign in campaigns:
        campaign_id = str(campaign["campaign_id"])
        raw_log = campaign.get("lifecycle_guardrail_log", [])
        log = [dict(item) for item in raw_log if isinstance(item, Mapping)]
        for item in log:
            phase = str(item.get("phase"))
            experiment = int(item.get("experiment_index", 0))
            actions.append(item)
            affected_experiments.add((campaign_id, phase, experiment))
            affected_phases.add((campaign_id, phase))
            affected_campaigns.add(campaign_id)
        iid_scores = [float(item) for item in campaign["iid"]["scores"]]
        assisted = {
            int(item.get("experiment_index", 0)) for item in log if item.get("phase") == "iid"
        }
        autonomous_scores = [
            score for index, score in enumerate(iid_scores) if index not in assisted
        ]
        autonomous_iid_best.append(
            {
                "campaign_id": campaign_id,
                "assisted_or_mixed_iid_best": max(iid_scores),
                "fully_autonomous_iid_best": (
                    max(autonomous_scores) if autonomous_scores else None
                ),
            }
        )
    return {
        "guardrail_action_count": len(actions),
        "affected_experiment_count": len(affected_experiments),
        "affected_phase_count": len(affected_phases),
        "affected_campaign_count": len(affected_campaigns),
        "total_experiment_count": len(campaigns) * 4,
        "total_phase_count": len(campaigns) * 2,
        "total_campaign_count": len(campaigns),
        "guardrail_actions_per_experiment": len(actions) / (len(campaigns) * 4),
        "affected_experiment_fraction": len(affected_experiments) / (len(campaigns) * 4),
        "affected_phase_fraction": len(affected_phases) / (len(campaigns) * 2),
        "affected_campaign_fraction": len(affected_campaigns) / len(campaigns),
        "iid_best_score_comparison": autonomous_iid_best,
    }


def _tie_aware_ranking(source: Mapping[str, Any]) -> dict[str, Any]:
    original = source.get("experiment_1_ranking_shift", {})
    rows = [dict(item) for item in original.get("rows", [])]
    iid = {str(row["method_id"]): float(row["iid_performance"]) for row in rows}
    shifted = {str(row["method_id"]): float(row["adaptation_performance"]) for row in rows}
    iid_rank = _average_ranks(iid)
    shifted_rank = _average_ranks(shifted)
    interface = {
        "random_recipe": "experiment_recipe",
        "greedy_local": "experiment_recipe",
        "structured_gp_bo": "experiment_recipe",
        "structured_gp_ucb": "experiment_recipe",
        "rule_based": "operation_level",
        "deepseek_v4_flash": "operation_level",
    }
    reanalyzed: list[dict[str, Any]] = []
    for row in rows:
        method = str(row["method_id"])
        reanalyzed.append(
            {
                "method_id": method,
                "decision_interface": interface[method],
                "iid_performance": iid[method],
                "adaptation_performance": shifted[method],
                "iid_average_rank": iid_rank[method],
                "adaptation_average_rank": shifted_rank[method],
            }
        )
    inversions = 0
    methods = list(iid)
    for left, right in itertools.combinations(methods, 2):
        iid_difference = iid[left] - iid[right]
        shifted_difference = shifted[left] - shifted[right]
        if iid_difference * shifted_difference < 0.0:
            inversions += 1
    return {
        "rows": sorted(reanalyzed, key=lambda item: item["iid_average_rank"]),
        "spearman_rank_correlation": original.get("spearman_rank_correlation"),
        "strict_rank_inversion_count": inversions,
        "tie_method": "average_rank",
        "mixed_decision_interfaces": True,
        "primary_overall_ranking_allowed": False,
    }


def _integrity_audit(
    source_path: Path,
    campaigns: Sequence[Mapping[str, Any]],
    *,
    repository_root: Path,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for campaign in campaigns:
        for phase in ("iid", "shifted"):
            artifact = campaign[phase]
            path = resolve_flagship_trajectory_reference(
                str(artifact["trajectory_path"]),
                repository_root=repository_root,
            )
            observed = _sha256(path)
            expected = str(artifact["trajectory_sha256"])
            rows.append(
                {
                    "campaign_id": campaign["campaign_id"],
                    "phase": phase,
                    "path": _relative_path(path, root=repository_root),
                    "expected_sha256": expected,
                    "observed_sha256": observed,
                    "matches": observed == expected,
                }
            )
    return {
        "source_report_exists": source_path.is_file(),
        "trajectory_count": len(rows),
        "all_trajectory_hashes_match": all(row["matches"] for row in rows),
        "trajectories": rows,
    }


def _average_ranks(values: Mapping[str, float]) -> dict[str, float]:
    ordered = sorted(values.items(), key=lambda item: item[1], reverse=True)
    result: dict[str, float] = {}
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and math.isclose(
            ordered[end][1], ordered[index][1], rel_tol=0.0, abs_tol=1e-12
        ):
            end += 1
        average = 0.5 * ((index + 1) + end)
        for key, _ in ordered[index:end]:
            result[key] = average
        index = end
    return result


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _relative_path(path: Path, *, root: Path = ROOT) -> str:
    try:
        return repository_relative_reference(path, repository_root=root)
    except ValueError:
        return str(path)


def _mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _fraction(values: Sequence[float], threshold: float) -> float | None:
    return sum(value > threshold for value in values) / len(values) if values else None


def _fmt(value: Any, *, digits: int = 4) -> str:
    if value is None:
        return "—"
    return f"{float(value):.{digits}f}"


def _pct(value: Any) -> str:
    return "—" if value is None else f"{100.0 * float(value):.2f}%"


def _table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    divider = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join([header, divider, *body])


__all__ = [
    "REANALYSIS_VERSION",
    "SOURCE_REPORT",
    "build_flagship_reanalysis",
    "load_v0_1_report",
    "render_flagship_reanalysis_markdown",
]
