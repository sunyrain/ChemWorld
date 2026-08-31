#!/usr/bin/env python
# ruff: noqa: E501, RUF001
"""Close W2-59 from preserved DeepSeek and GPT main-evidence outputs."""

from __future__ import annotations

import argparse
import itertools
import json
import statistics
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "configs/benchmark/work_ii_cross_model_main_evidence_completion_v0.1.json"
DEEPSEEK_AP = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-study-b-matched-evidence-results-v0.1.json"
)
DEEPSEEK_B2 = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b2-phase-process-results-v0.1.json"
)
GPT_B2 = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b2-gpt56-sol-medium-results-v0.1.json"
)
DEEPSEEK_C2 = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
)
DEEPSEEK_W2_50 = ROOT / (
    "workstreams/flagship_tasks/reports/work-ii-reviewer-control-analyses-v0.1.json"
)
GPT_AP_ROOT = ROOT / (
    "runs/formal/work-ii-w2-59-study-b-ap-gpt56-sol-medium-v0.1-20260831"
)
GPT_B2_ROOT = ROOT / (
    "runs/formal/work-ii-w2-59-study-b2-gpt56-sol-medium-v0.1-20260831"
)
GPT_C2_ROOT = ROOT / (
    "runs/formal/work-ii-w2-59-c2-gpt56-sol-medium-replication-v0.1-20260831"
)
GPT_W2_50_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-w2-59-gpt56-sol-medium-multi-task-open-action-five-world-v0.1-"
    "20260831-restart1"
)
B3_DEEPSEEK_ROOT = ROOT / (
    "runs/formal/work-ii-w2-59-b3-main-evidence-successor-deepseek-v0.1-20260831"
)
B3_GPT_FIRST_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-w2-59-b3-main-evidence-successor-gpt56-sol-medium-v0.1-20260831"
)
B3_GPT_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-w2-59-b3-main-evidence-successor-gpt56-sol-medium-v0.1-"
    "20260831-restart1"
)
DEFAULT_JSON = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-w2-59-cross-model-main-evidence-closeout-v0.1.json"
)
DEFAULT_REPORT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "WORK_II_CROSS_MODEL_MAIN_EVIDENCE_COMPLETION_CLOSEOUT_ZH.md"
)
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("cannot average an empty sequence")
    return statistics.mean(values)


def _exact_sign_flip(values: Sequence[float]) -> dict[str, Any]:
    observed = _mean(values)
    null = [
        _mean([value * sign for value, sign in zip(values, signs, strict=True)])
        for signs in itertools.product((-1.0, 1.0), repeat=len(values))
    ]
    return {
        "values": list(values),
        "mean": observed,
        "positive_world_count": sum(value > 0.0 for value in values),
        "zero_world_count": sum(value == 0.0 for value in values),
        "negative_world_count": sum(value < 0.0 for value in values),
        "exact_sign_flip_p_one_sided_greater": sum(
            value >= observed - 1.0e-15 for value in null
        )
        / len(null),
    }


def _ap_gpt_analysis(run_root: Path) -> dict[str, Any]:
    summary = _load(run_root / "summary.json")
    cells = [_load(path) for path in sorted((run_root / "cells").glob("*.json"))]
    canary = _load(run_root / "canary_summary.json")
    if (
        canary.get("qualified") is not True
        or summary.get("status") != "completed"
        or summary.get("scheduled_cell_count") != 15
        or summary.get("completed_cell_count") != 15
        or summary.get("failed_cell_count") != 0
        or len(cells) != 15
    ):
        raise ValueError("GPT A-P is not the frozen complete 15/15 block")
    seeds = sorted({int(cell["world_seed"]) for cell in cells})
    if len(seeds) != 5:
        raise ValueError("GPT A-P world denominator drifted")
    arm_summary: dict[str, Any] = {}
    for arm in ARMS:
        members = [cell for cell in cells if cell["arm"] == arm]
        if len(members) != 5:
            raise ValueError(f"GPT A-P {arm} denominator drifted")
        pre = [float(cell["scores"]["pre"]["mean_normalized_absolute_error"]) for cell in members]
        post = [
            float(cell["scores"]["post"]["mean_normalized_absolute_error"])
            for cell in members
        ]
        arm_summary[arm] = {
            "cell_count": len(members),
            "mean_pre_error": _mean(pre),
            "mean_post_error": _mean(post),
            "mean_update_gain": _mean(
                [before - after for before, after in zip(pre, post, strict=True)]
            ),
        }
    world_rows: list[dict[str, Any]] = []
    primary_values: list[float] = []
    for seed in seeds:
        world = {cell["arm"]: cell for cell in cells if int(cell["world_seed"]) == seed}
        if set(world) != set(ARMS):
            raise ValueError("GPT A-P cluster does not contain all arms")
        gains = {
            arm: float(world[arm]["scores"]["pre"]["mean_normalized_absolute_error"])
            - float(world[arm]["scores"]["post"]["mean_normalized_absolute_error"])
            for arm in ARMS
        }
        primary = gains["misindexed_nominal"] - gains["aligned_nominal"]
        primary_values.append(primary)
        world_rows.append(
            {"world_seed": seed, "update_gains": gains, "primary_contrast": primary}
        )
    misindexed = [cell for cell in cells if cell["arm"] == "misindexed_nominal"]
    audit_rows = []
    for cell in sorted(misindexed, key=lambda item: int(item["world_seed"])):
        text = (
            str(cell["post_prediction"]["model_summary"])
            + " "
            + str(cell["post_prediction"]["evidence_assessment"])
        ).lower()
        audit_rows.append(
            {
                "world_seed": int(cell["world_seed"]),
                "explicit_direction_rejection": (
                    "contradict" in text or "opposite to the initial" in text
                ),
                "peak_and_collapse_response": (
                    "collapse" in text and ("1.1" in text or "1.107" in text)
                ),
            }
        )
    return {
        "status": "matched_cross_model_formal_complete",
        "scheduled_sessions": 15,
        "completed_sessions": 15,
        "failed_sessions": 0,
        "world_count": 5,
        "arm_summary": arm_summary,
        "primary_contrast": _exact_sign_flip(primary_values),
        "world_rows": world_rows,
        "public_summary_audit": {
            "explicit_direction_rejection_count": sum(
                row["explicit_direction_rejection"] for row in audit_rows
            ),
            "peak_and_collapse_response_count": sum(
                row["peak_and_collapse_response"] for row in audit_rows
            ),
            "world_rows": audit_rows,
        },
    }


def _ap_deepseek_analysis(source: Mapping[str, Any]) -> dict[str, Any]:
    row = next(item for item in source["locus_results"] if item["locus"] == "A_P")
    audit = source["public_summary_audit"]["A_P_misindexed"]
    return {
        "status": "matched_cross_model_formal_complete",
        "scheduled_sessions": 15,
        "completed_sessions": 15,
        "failed_sessions": 0,
        "world_count": 5,
        "arm_summary": {
            arm: {
                "cell_count": int(row["arm_summary"][arm]["cell_count"]),
                "mean_pre_error": float(row["arm_summary"][arm]["pre_error"]["mean"]),
                "mean_post_error": float(row["arm_summary"][arm]["post_error"]["mean"]),
                "mean_update_gain": float(row["arm_summary"][arm]["update_gain"]["mean"]),
            }
            for arm in ARMS
        },
        "primary_contrast": dict(row["primary_contrast"]),
        "world_rows": list(row["world_rows"]),
        "public_summary_audit": {
            "explicit_direction_rejection_count": int(
                audit["explicit_direction_rejection_count"]
            ),
            "peak_and_collapse_response_count": int(
                audit["peak_and_collapse_response_count"]
            ),
        },
    }


def _b2_analysis(source: Mapping[str, Any]) -> dict[str, Any]:
    audit = source["public_summary_audit"]["by_arm"]["misindexed_nominal"]
    return {
        "status": "matched_cross_model_formal_complete",
        "scheduled_sessions": 15,
        "completed_sessions": int(source["integrity"]["completed_sessions"]),
        "failed_sessions": int(source["integrity"]["failed_sessions"]),
        "world_count": int(source["integrity"]["complete_clusters"]),
        "arm_summary": {
            arm: {
                "cell_count": int(source["arm_summary"][arm]["cell_count"]),
                "mean_pre_error": float(source["arm_summary"][arm]["pre_error"]["mean"]),
                "mean_post_error": float(source["arm_summary"][arm]["post_error"]["mean"]),
                "mean_update_gain": float(source["arm_summary"][arm]["update_gain"]["mean"]),
            }
            for arm in ARMS
        },
        "primary_contrast": dict(source["primary_contrast"]),
        "world_rows": list(source["world_rows"]),
        "misindexed_exact_1_75_law_recovery_count": int(
            audit["exact_1_75_power_law_recovery_count"]
        ),
    }


def _paired_delta(left: Mapping[str, Any], right: Mapping[str, Any]) -> dict[str, Any]:
    left_rows = {int(row["world_seed"]): row for row in left["world_rows"]}
    right_rows = {int(row["world_seed"]): row for row in right["world_rows"]}
    if set(left_rows) != set(right_rows) or len(left_rows) != 5:
        raise ValueError("matched-evidence cross-model worlds differ")
    values = [
        float(right_rows[seed]["primary_contrast"])
        - float(left_rows[seed]["primary_contrast"])
        for seed in sorted(left_rows)
    ]
    return {
        "orientation": "gpt_minus_deepseek",
        "paired_world_count": 5,
        "primary_contrast_difference": _exact_sign_flip(values),
        "inferential_model_superiority_test": False,
    }


def _gpt_c2(root: Path) -> dict[str, Any]:
    summary = _load(root / "summary.json")
    cells = list(summary["cells"])
    if len(cells) != 3 or summary.get("expected_sessions") != 3:
        raise ValueError("GPT C2 canary triplet denominator drifted")
    failed = [cell for cell in cells if not cell["completed"]]
    if len(failed) != 1:
        raise ValueError("GPT C2 retained failure count drifted")
    failed_summary = _load(root / "cells" / failed[0]["cell_id"] / "summary.json")
    provider_errors = sum(
        len(list(receipt.get("provider_errors", [])))
        for receipt in failed_summary.get("provider_receipts", [])
    )
    return {
        "status": "in_denominator_canary_rejected_before_scale",
        "scheduled_sessions": 135,
        "terminal_sessions": 3,
        "qualified_sessions": int(summary["completed_sessions"]),
        "retained_failure_sessions": int(summary["retained_noncompleted_sessions"]),
        "unstarted_sessions": 132,
        "scheduled_complete_physical_experiments": 1260,
        "observed_complete_physical_experiments": int(
            summary["observed_complete_experiments"]
        ),
        "qualified_complete_physical_experiments": 8
        * int(summary["completed_sessions"]),
        "retained_failure_complete_physical_experiments": 8
        * int(summary["retained_noncompleted_sessions"]),
        "failed_cell_id": failed[0]["cell_id"],
        "failed_checks": list(failed_summary["qualification"]["failed_checks"]),
        "provider_error_event_count": provider_errors,
        "recoverable_zero_action_infrastructure_failure": False,
        "disposition": "terminal_retained_stop_rule",
    }


def _gpt_w2_50(root: Path) -> dict[str, Any]:
    summary = _load(root / "summary.json")
    campaigns = [
        _load(path)
        for path in sorted((root / "formal" / "campaigns").glob("*/summary.json"))
    ]
    if summary.get("scheduled_cell_count") != 45 or len(campaigns) != 3:
        raise ValueError("GPT W2-50 canary triplet denominator drifted")
    failed = [cell for cell in campaigns if cell.get("completed") is not True]
    if len(failed) != 1:
        raise ValueError("GPT W2-50 retained failure count drifted")
    failed_rows = [
        row
        for row in summary["cell_rows"]
        if row.get("status") != "completed_uncontaminated"
    ]
    if len(failed_rows) != 1:
        raise ValueError("GPT W2-50 failed cell row denominator drifted")
    failure = failed[0].get("failure") or {}
    return {
        "status": str(summary["execution_status"]),
        "scheduled_sessions": 45,
        "terminal_sessions": 3,
        "eligible_sessions": int(summary["eligible_cell_count"]),
        "retained_failure_sessions": int(summary["failed_or_ineligible_cell_count"]),
        "unstarted_sessions": 42,
        "scheduled_complete_physical_experiments": int(
            summary["participant_physical_experiment_denominator"]
        ),
        "eligible_complete_physical_experiments": int(
            summary["participant_physical_experiment_count"]
        ),
        "observed_complete_physical_experiments_including_partial": sum(
            int(cell["analysis"]["complete_experiment_count"]) for cell in campaigns
        ),
        "provider_free_truth_query_count": int(summary["provider_free_truth_query_count"]),
        "provider_free_exact_replay_count": int(
            summary["provider_free_exact_replay_count"]
        ),
        "failed_cell_id": str(failed_rows[0]["cell_id"]),
        "failure_type": failure.get("type"),
        "failure_message": failure.get("message"),
        "recoverable_zero_action_infrastructure_failure": False,
        "disposition": "terminal_retained_stop_rule",
    }


def _b3(root: Path) -> dict[str, Any]:
    closeout = _load(root / "canary_closeout.json")
    return {
        key: closeout[key]
        for key in (
            "status",
            "canary_qualified",
            "scheduled_canary_session_count",
            "observed_canary_session_count",
            "completed_canary_session_count",
            "failed_canary_session_count",
            "participant_schema_failure_count",
            "infrastructure_failure_count",
            "provider_turn_count",
            "completed_provider_turn_count",
            "scheduled_formal_session_count",
            "launched_formal_session_count",
            "unstarted_formal_session_count",
            "outcome_replacement_count",
        )
    } | {
        "failures": [
            {
                "cell_id": row["cell_id"],
                "failure_classification": row["failure_classification"],
                "failure_type": row["failure_type"],
                "failure_message": row["failure_message"],
            }
            for row in closeout["cell_rows"]
            if row["status"] != "completed"
        ]
    }


def build_closeout() -> dict[str, Any]:
    plan = _load(PLAN)
    deepseek_ap = _ap_deepseek_analysis(_load(DEEPSEEK_AP))
    gpt_ap = _ap_gpt_analysis(GPT_AP_ROOT)
    deepseek_b2 = _b2_analysis(_load(DEEPSEEK_B2))
    gpt_b2 = _b2_analysis(_load(GPT_B2))
    if gpt_b2["completed_sessions"] != 15 or gpt_b2["failed_sessions"] != 0:
        raise ValueError("GPT B2 formal block is incomplete")
    deepseek_c2 = _load(DEEPSEEK_C2)
    deepseek_w2_50 = _load(DEEPSEEK_W2_50)["w2_50_continuous_action"]
    gpt_c2 = _gpt_c2(GPT_C2_ROOT)
    gpt_w2_50 = _gpt_w2_50(GPT_W2_50_ROOT)
    b3_deepseek = _b3(B3_DEEPSEEK_ROOT)
    b3_gpt_first = _b3(B3_GPT_FIRST_ROOT)
    b3_gpt = _b3(B3_GPT_ROOT)
    if b3_gpt_first["provider_turn_count"] != 0 or b3_gpt["canary_qualified"] is not True:
        raise ValueError("GPT B3 platform restart disposition drifted")
    if b3_deepseek["canary_qualified"] is not False:
        raise ValueError("DeepSeek B3 canary disposition drifted")
    payload: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-w2-59-cross-model-closeout-0.1",
        "study_id": plan["study_id"],
        "status": "terminal_with_block_specific_cross_model_coverage",
        "formal_result": False,
        "analysis_provider_call_count": 0,
        "providers": {
            "deepseek": {"model": "deepseek-v4-flash", "reasoning_effort": "high"},
            "gpt": {"model": "gpt-5.6-sol", "reasoning_effort": "medium"},
        },
        "planned_denominators": {
            "formal_sessions": int(plan["execution"]["formal_sessions_total"]),
            "excluded_canary_sessions": int(
                plan["execution"]["excluded_canary_sessions_total"]
            ),
            "participant_complete_physical_experiments": 1800,
        },
        "observed_denominators": {
            "formal_terminal_sessions": 36,
            "formal_qualified_or_eligible_sessions": 34,
            "formal_retained_failure_sessions": 2,
            "formal_unstarted_sessions": 234,
            "excluded_canary_observed_sessions": 12,
            "excluded_canary_completed_sessions": 11,
            "excluded_canary_retained_failure_sessions": 1,
            "observed_complete_physical_experiments_including_partial": (
                gpt_c2["observed_complete_physical_experiments"]
                + gpt_w2_50["observed_complete_physical_experiments_including_partial"]
            ),
            "qualified_or_eligible_complete_physical_experiments": (
                gpt_c2["qualified_complete_physical_experiments"]
                + gpt_w2_50["eligible_complete_physical_experiments"]
            ),
            "retained_failure_complete_physical_experiments": (
                gpt_c2["retained_failure_complete_physical_experiments"]
                + gpt_w2_50["observed_complete_physical_experiments_including_partial"]
                - gpt_w2_50["eligible_complete_physical_experiments"]
            ),
        },
        "blocks": {
            "matched_a_p": {
                "status": "matched_cross_model_formal_complete",
                "deepseek": deepseek_ap,
                "gpt": gpt_ap,
                "paired_descriptive_difference": _paired_delta(deepseek_ap, gpt_ap),
            },
            "matched_a_s_b2": {
                "status": "matched_cross_model_formal_complete",
                "deepseek": deepseek_b2,
                "gpt": gpt_b2,
                "paired_descriptive_difference": _paired_delta(deepseek_b2, gpt_b2),
            },
            "public_c2": {
                "status": "deepseek_complete_gpt_canary_rejected",
                "deepseek": {
                    "scheduled_sessions": int(deepseek_c2["denominators"]["cell_count"]),
                    "completed_sessions": int(
                        deepseek_c2["denominators"]["terminal_state_counts"]["completed"]
                    ),
                    "failed_sessions": int(
                        deepseek_c2["denominators"]["terminal_state_counts"]["failed"]
                    ),
                    "right_censored_sessions": int(
                        deepseek_c2["denominators"]["terminal_state_counts"]["right_censored"]
                    ),
                    "truth_executions": int(
                        deepseek_c2["denominators"]["truth_completed_execution_count"]
                    ),
                    "law_evaluations": int(
                        deepseek_c2["denominators"]["law_summary_evaluated_count"]
                    ),
                    "blind_completed_executions": int(
                        deepseek_c2["denominators"]["blind_completed_execution_count"]
                    ),
                },
                "gpt": gpt_c2,
                "matched_cross_model_effect_estimable": False,
            },
            "w2_50_open_action": {
                "status": "deepseek_complete_gpt_canary_rejected",
                "deepseek": {
                    "scheduled_sessions": int(deepseek_w2_50["scheduled_cell_count"]),
                    "eligible_sessions": int(deepseek_w2_50["eligible_cell_count"]),
                    "retained_failure_sessions": int(
                        deepseek_w2_50["retained_failure_count"]
                    ),
                    "top1_count": sum(
                        bool(row["top1_selected"])
                        for row in deepseek_w2_50["cell_rows"]
                    ),
                },
                "gpt": gpt_w2_50,
                "matched_cross_model_effect_estimable": False,
            },
            "b3_successor": {
                "status": "deepseek_excluded_canary_rejected_formal_unstarted",
                "deepseek": b3_deepseek,
                "gpt_initial_platform_defect": b3_gpt_first,
                "gpt_qualified_restart": b3_gpt,
                "formal_completed_by_provider": {"deepseek": 0, "gpt": 0},
                "matched_cross_model_effect_estimable": False,
            },
        },
        "reviewer_control_recomputation": {
            "provider_call_count": 0,
            "deepseek_w2_55_remains_complete": True,
            "gpt_w2_50_continuous_law_action": {
                "status": "not_estimable_after_frozen_canary_stop",
                "eligible_sessions": gpt_w2_50["eligible_sessions"],
                "required_complete_frozen_denominator": "45 scheduled / 42 eligible / 3 retained failures",
            },
            "gpt_c2_typed_law_capacity": {
                "status": "not_estimable_after_frozen_canary_stop",
                "terminal_sessions": gpt_c2["terminal_sessions"],
                "required_complete_frozen_denominator": "135 participant cells with current-composite dataset",
            },
            "cross_provider_w2_55_pooling_performed": False,
        },
        "provider_free_controls": {
            "w2_51_w2_52_w2_53_duplicated": False,
            "reason": "model-independent truth, replay, oracle qualification and gate-action diagnostics",
        },
        "incidents": [
            {
                "block": "GPT C2 aligned in-denominator canary cell",
                "impact_class": "S",
                "evidence": "8/8 experiments complete; qualification failed with retained provider/session errors",
                "decision": "terminal_scientific_or_participant_outcome",
                "action": "stop remaining 132 sessions; preserve all raw evidence",
            },
            {
                "block": "GPT W2-50 misindexed in-denominator canary cell",
                "impact_class": "B_with_frozen_retention_rule",
                "evidence": "5/12 experiments complete before provider/session interruption",
                "decision": "terminal_operational_outcome",
                "action": "stop remaining 42 sessions; do not replace partial trajectory",
            },
            {
                "block": "DeepSeek B3 excluded canary",
                "impact_class": "S",
                "evidence": "6/6 provider turns completed; one post payload unavailable under participant schema",
                "decision": "terminal_canary_rejected_before_formal",
                "action": "leave both providers at 0/30 formal",
            },
            {
                "block": "GPT B3 first canary root",
                "impact_class": "A_zero_action_platform_defect",
                "evidence": "0 provider turns; duplicated provider configuration caused three immediate OSError failures",
                "decision": "full_canary_restart",
                "action": "preserve first root; restart from first canary unit after platform repair",
            },
        ],
        "claim_boundaries": {
            "matched_a_p_cross_model_replication_supported": True,
            "matched_a_s_b2_cross_model_replication_supported": True,
            "matched_c2_cross_model_effect_supported": False,
            "matched_w2_50_cross_model_effect_supported": False,
            "matched_b3_cross_model_effect_supported": False,
            "model_superiority_leaderboard_supported": False,
            "general_llm_claim_supported": False,
            "all_scheduled_main_evidence_attempted_under_frozen_stop_rules": True,
            "all_scheduled_main_evidence_completed_for_both_models": False,
        },
        "source_artifacts": {
            "plan": PLAN.relative_to(ROOT).as_posix(),
            "deepseek_a_p": DEEPSEEK_AP.relative_to(ROOT).as_posix(),
            "deepseek_b2": DEEPSEEK_B2.relative_to(ROOT).as_posix(),
            "gpt_b2": GPT_B2.relative_to(ROOT).as_posix(),
            "deepseek_c2": DEEPSEEK_C2.relative_to(ROOT).as_posix(),
            "deepseek_w2_50": DEEPSEEK_W2_50.relative_to(ROOT).as_posix(),
            "gpt_a_p_root": GPT_AP_ROOT.relative_to(ROOT).as_posix(),
            "gpt_b2_root": GPT_B2_ROOT.relative_to(ROOT).as_posix(),
            "gpt_c2_root": GPT_C2_ROOT.relative_to(ROOT).as_posix(),
            "gpt_w2_50_root": GPT_W2_50_ROOT.relative_to(ROOT).as_posix(),
            "b3_deepseek_root": B3_DEEPSEEK_ROOT.relative_to(ROOT).as_posix(),
            "b3_gpt_root": B3_GPT_ROOT.relative_to(ROOT).as_posix(),
        },
    }
    payload["summary_sha256"] = canonical_json_sha256(payload)
    return payload


def _f(value: float) -> str:
    return f"{value:.4f}"


def _render(payload: Mapping[str, Any]) -> str:
    blocks = payload["blocks"]
    ap = blocks["matched_a_p"]
    b2 = blocks["matched_a_s_b2"]
    observed = payload["observed_denominators"]
    lines = [
        "# Work II W2-59 双模型主证据补齐收束",
        "",
        "状态：`terminal_with_block_specific_cross_model_coverage`。全部预定主证据块均按冻结协议启动或接受 stop-rule 判定；只有 A-P 与 A-S B2 形成 DeepSeek + GPT 的完整 matched formal 分母。C2、W2-50 与 B3 的不完整性是保留的 canary 终态，不是待补跑队列。",
        "",
        "## 总分母",
        "",
        "| 项目 | 计划 | 终态观察 | 合格/可评分 | 保留失败 | 未启动 |",
        "|---|---:|---:|---:|---:|---:|",
        f"| formal sessions | 270 | {observed['formal_terminal_sessions']} | {observed['formal_qualified_or_eligible_sessions']} | {observed['formal_retained_failure_sessions']} | {observed['formal_unstarted_sessions']} |",
        f"| 排除式 canary sessions | 12 | {observed['excluded_canary_observed_sessions']} | {observed['excluded_canary_completed_sessions']} | {observed['excluded_canary_retained_failure_sessions']} | 0 |",
        f"| participant complete physical experiments | 1,800 | {observed['observed_complete_physical_experiments_including_partial']} | {observed['qualified_or_eligible_complete_physical_experiments']} | {observed['retained_failure_complete_physical_experiments']} | 1,747 |",
        "",
        "## 完整 matched cross-model 结果",
        "",
        "主指标均为 `misindexed update gain − aligned update gain`，统计单位为同一个 fresh world。跨模型差值只作配对描述，不作模型排行榜。",
        "",
        "| Block | 模型 | sessions | primary contrast | positive worlds | exact one-sided p | 结构恢复 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for block_name, block in (("A-P", ap), ("A-S B2", b2)):
        for provider in ("deepseek", "gpt"):
            row = block[provider]
            structural = (
                str(row["misindexed_exact_1_75_law_recovery_count"]) + "/5"
                if "misindexed_exact_1_75_law_recovery_count" in row
                else "—"
            )
            lines.append(
                f"| {block_name} | {provider} | {row['completed_sessions']}/15 | "
                f"{_f(float(row['primary_contrast']['mean']))} | "
                f"{row['primary_contrast']['positive_world_count']}/5 | "
                f"{float(row['primary_contrast']['exact_sign_flip_p_one_sided_greater']):.3f} | {structural} |"
            )
    lines.extend(
        [
            "",
            f"A-P 在 DeepSeek 上为 {_f(float(ap['deepseek']['primary_contrast']['mean']))}（3/5 worlds），在 GPT 上为 {_f(float(ap['gpt']['primary_contrast']['mean']))}（5/5 worlds）。两个配置都支持反证到达后的数值纠错；GPT 的 5/5 方向一致增强了跨配置复现，但 n=5 仍不支持一般 LLM 结论。",
            "",
            f"A-S B2 在 DeepSeek/GPT 上分别为 {_f(float(b2['deepseek']['primary_contrast']['mean']))} 与 {_f(float(b2['gpt']['primary_contrast']['mean']))}；两者的 misindexed exact 1.75-law recovery 都是 0/5。因而“数值收敛不等于结构识别”现在由两个模型配置在完全匹配的 15-session 分母上共同支持。",
            "",
            "## 被 stop rule 收束的块",
            "",
            "| Block | DeepSeek | GPT | 结论 |",
            "|---|---|---|---|",
            "| Public C2 | 135 cells 完整 evaluator | 3/135 terminal、2 合格、1 provider/session qualification failure、132 未启动 | 无 matched effect；DeepSeek 主结果保留 |",
            "| W2-50 | 45 scheduled、42 eligible、11/42 Top-1 | 3/45 terminal、2 eligible、1 session interruption、42 未启动 | 无 matched action effect |",
            "| B3 successor | excluded canary 2/3 | 修复平台零调用缺陷后 canary 3/3 | 共同门要求双方通过，故 formal 均 0/30 |",
            "",
            "GPT C2 三个 sessions 均完成 8/8 physical experiments；aligned session 因 provider/session 错误触发资格失败。GPT W2-50 的 opaque 与 aligned 各完成 12/12，misindexed 在 5/12 后中断。两者都不是零行动基础设施失败，因此不能按冻结规则补跑或替换。",
            "",
            "## W2-55 零 provider 重算",
            "",
            "DeepSeek 的原 W2-55 仍完整。GPT 新输出经过同一分母可用性检查后，W2-50 只有 2 个 eligible cells，C2 只有 3 个 terminal cells且没有 135-cell current-composite dataset；连续 law-action 相关和 typed-law capacity 因此均为 `not_estimable_after_frozen_canary_stop`。本次新增 provider calls=0，也没有将 DeepSeek 结果拼入 GPT 分母。",
            "",
            "## 事件处置",
            "",
            "| 事件 | 分类 | 决策 |",
            "|---|---|---|",
        ]
    )
    for incident in payload["incidents"]:
        lines.append(
            f"| {incident['block']} | {incident['impact_class']} | {incident['decision']}：{incident['action']} |"
        )
    lines.extend(
        [
            "",
            "## 论文边界",
            "",
            "可以升级的表述是：A-P evidence acquisition/numerical correction 与 A-S numerical revision/structural identification 的断裂已在两个匹配模型配置上复现。不能升级的表述是：C2、W2-50 或 B3 已有完整双模型 formal 分母，或某个模型总体优于另一个模型。",
            "",
            "Launch decision：`terminal_outcome`。W2-59 不再有可合法继续的 provider session；下一步仅是论文、图表和发布整合。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    payload = build_closeout()
    output_json = args.output_json.resolve()
    output_report = args.output_report.resolve()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(output_json, payload)
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(_render(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "formal_terminal_sessions": payload["observed_denominators"][
                    "formal_terminal_sessions"
                ],
                "formal_unstarted_sessions": payload["observed_denominators"][
                    "formal_unstarted_sessions"
                ],
                "analysis_provider_call_count": payload["analysis_provider_call_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
