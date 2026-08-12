#!/usr/bin/env python3
"""Evaluate paired eight-round real-provider catalyst-law campaigns."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    TASK_ID,
    WORLD_SEED,
    stable_catalyst_intervention,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_VERSION = "chemworld-work-ii-catalyst-deactivation-paired-provider-summary-0.1"
LAW_IDS = ("deactivating_baseline", "stable_catalyst")
PRIMARY_GATES = {"yield": 0.050, "conversion": 0.050, "selectivity": 0.054}
DEFAULT_CONFIGS = {
    "deactivating_baseline": ROOT
    / (
        "configs/benchmark/"
        "work_ii_catalyst_deactivation_real_provider_deactivating_campaign_seed0.json"
    ),
    "stable_catalyst": ROOT
    / (
        "configs/benchmark/"
        "work_ii_catalyst_deactivation_real_provider_stable_campaign_seed0.json"
    ),
}
DEFAULT_PARTICIPANT_SUMMARIES = {
    "deactivating_baseline": ROOT
    / (
        "runs/development/"
        "work-ii-catalyst-deactivation-paired-provider-deactivating-seed0-20260812/"
        "summary.json"
    ),
    "stable_catalyst": ROOT
    / (
        "runs/development/"
        "work-ii-catalyst-deactivation-paired-provider-stable-seed0-20260812/"
        "summary.json"
    ),
}
DEFAULT_OUTPUT_ROOT = (
    ROOT
    / "runs/development/work-ii-catalyst-deactivation-paired-provider-counterfactual-seed0-20260812"
)
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-catalyst-deactivation-paired-provider-seed0-20260812.json"
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _validate_configs(configs: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    if set(configs) != set(LAW_IDS):
        raise ValueError("paired configs must contain exactly the two frozen law IDs")
    baseline = deepcopy(dict(configs["deactivating_baseline"]))
    stable = deepcopy(dict(configs["stable_catalyst"]))
    baseline_law = baseline.pop("world_law_id", None)
    stable_law = stable.pop("world_law_id", None)
    baseline_interventions = baseline.pop("world_interventions", None)
    stable_interventions = stable.pop("world_interventions", None)
    if baseline_law != "deactivating_baseline" or stable_law != "stable_catalyst":
        raise ValueError("paired config law identities are invalid")
    if baseline_interventions != []:
        raise ValueError("deactivating baseline must not carry a world intervention")
    if stable_interventions != [stable_catalyst_intervention()]:
        raise ValueError("stable config does not carry the frozen catalyst intervention")
    if baseline != stable:
        raise ValueError("paired public/provider/resource configs differ outside the hidden law")
    if int(baseline["world_seed"]) != WORLD_SEED:
        raise ValueError("paired campaign world seed is not zero")
    if int(baseline["campaign"]["complete_experiments"]) != 8:
        raise ValueError("paired campaign does not require eight experiments")
    if list(baseline["prior_arms"]) != ["opaque"]:
        raise ValueError("paired campaign must expose one opaque public arm")
    return {
        "matched_outside_hidden_law": True,
        "world_seed": WORLD_SEED,
        "complete_experiments_per_campaign": 8,
        "participant_campaign_count": 2,
        "provider": {
            key: baseline["provider"].get(key)
            for key in ("id", "model", "reasoning_effort", "wire_api")
        },
    }


def _campaign_row(
    law_id: str,
    summary: Mapping[str, Any],
    source_path: Path,
) -> dict[str, Any]:
    analysis = summary.get("analysis")
    analysis = analysis if isinstance(analysis, Mapping) else {}
    experiments = analysis.get("experiments")
    experiments = experiments if isinstance(experiments, list) else []
    recipes = []
    for item in experiments:
        if not isinstance(item, Mapping):
            continue
        actions = item.get("committed_operations")
        if not isinstance(actions, list) or not actions:
            continue
        recipes.append(
            {
                "source_law_id": law_id,
                "experiment_index": int(item["experiment_index"]),
                "actions": [dict(action) for action in actions if isinstance(action, Mapping)],
                "recipe_sha256": item.get("recipe_sha256"),
                "provider_final_metrics": dict(item.get("final_metrics", {})),
                "provider_leaderboard_score": item.get("leaderboard_score"),
            }
        )
    resources = summary.get("method_resources")
    resources = resources if isinstance(resources, Mapping) else {}
    receipts = summary.get("provider_receipts")
    receipts = receipts if isinstance(receipts, list) else []
    receipt = receipts[0] if len(receipts) == 1 and isinstance(receipts[0], Mapping) else {}
    replay = summary.get("exact_replay")
    replay = replay if isinstance(replay, Mapping) else {}
    qualification = summary.get("qualification")
    qualification = qualification if isinstance(qualification, Mapping) else {}
    scores = [
        float(recipe["provider_leaderboard_score"])
        for recipe in recipes
        if isinstance(recipe.get("provider_leaderboard_score"), int | float)
        and not isinstance(recipe.get("provider_leaderboard_score"), bool)
    ]
    return {
        "law_id": law_id,
        "source": {
            "path": source_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(source_path),
        },
        "operationally_complete": summary.get("completed") is True,
        "failure": summary.get("failure"),
        "qualification_failed_checks": list(qualification.get("failed_checks", [])),
        "operation_attempt_count": analysis.get("operation_attempt_count"),
        "complete_experiment_count": analysis.get("complete_experiment_count"),
        "unique_recipe_count": analysis.get("unique_recipe_count"),
        "exact_repeat_count": analysis.get("exact_repeat_count"),
        "exact_replay": dict(replay),
        "recipes": recipes,
        "score_summary": {
            "count": len(scores),
            "mean": sum(scores) / len(scores) if scores else None,
            "maximum": max(scores) if scores else None,
            "sequence": scores,
        },
        "final_recommendation": analysis.get("final_recommendation"),
        "belief_snapshots": list(analysis.get("belief_snapshots", [])),
        "provider_usage": {
            key: resources.get(key)
            for key in (
                "provider_session_count",
                "logical_codex_turn_count",
                "input_token_count",
                "cached_input_token_count",
                "uncached_input_token_count",
                "output_token_count",
                "input_cache_hit_ratio",
                "session_elapsed_s",
                "recovered_mcp_tool_failure_count",
                "maximum_consecutive_mcp_tool_failure_count",
                "provider_error_event_count",
                "provider_usage_accounting_complete",
            )
        },
        "provider_receipt": {
            key: receipt.get(key)
            for key in (
                "status",
                "return_code",
                "usage",
                "usage_complete",
                "session_elapsed_s",
                "recovered_mcp_tool_failure_count",
                "maximum_consecutive_mcp_tool_failure_count",
                "provider_error_event_count",
                "belief_snapshot_count",
                "final_recommendation_source",
            )
        },
        "recovered_mcp_failures": [
            {
                key: call.get(key)
                for key in (
                    "tool",
                    "status",
                    "error_type",
                    "error_code",
                    "error_detail",
                )
            }
            for call in receipt.get("mcp_tool_calls", [])
            if isinstance(call, Mapping) and call.get("status") == "failed"
        ],
    }


def _binding(source_law_id: str, experiment_index: int) -> tuple[int, str]:
    digest = hashlib.sha256(
        (
            "work-ii-catalyst-deactivation-paired-provider-counterfactual:"
            f"{source_law_id}:{experiment_index}"
        ).encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"work-ii-catalyst-paired-{source_law_id}-e{experiment_index}-{digest[:12]}",
    )


def _terminal_metrics(records: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    finals = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(finals) != 1:
        raise ValueError("counterfactual trajectory must contain one committed final assay")
    observation = finals[0].get("observation")
    if not isinstance(observation, Mapping):
        raise ValueError("counterfactual final assay lacks a public observation")
    return {
        "yield": float(observation["yield"]),
        "conversion": float(observation["conversion"]),
        "selectivity": float(observation["selectivity"]),
        "safety_risk": float(observation["safety_risk"]),
        "score": float(finals[0]["leaderboard_score"]),
    }


def _execute(
    *,
    recipe: Mapping[str, Any],
    target_law_id: str,
    output_root: Path,
) -> dict[str, Any]:
    source_law_id = str(recipe["source_law_id"])
    experiment_index = int(recipe["experiment_index"])
    actions = [dict(action) for action in recipe["actions"]]
    if canonical_json_sha256(actions) != recipe.get("recipe_sha256"):
        raise ValueError("provider-selected recipe hash does not match its committed actions")
    interventions = (
        [] if target_law_id == "deactivating_baseline" else [stable_catalyst_intervention()]
    )
    observation_seed, namespace = _binding(source_law_id, experiment_index)
    target_root = output_root / source_law_id / f"experiment-{experiment_index}" / target_law_id
    target_root.mkdir(parents=True, exist_ok=False)
    trajectory = target_root / "trajectory.jsonl"
    started = perf_counter()
    run_agent(
        env_id=get_task(TASK_ID).env_id,
        agent=_FrozenTruthReplayAgent(actions),
        world_split=str(get_task(TASK_ID).world_split),
        budget=len(actions),
        objective="safe",
        seed=WORLD_SEED,
        agent_seed=0,
        observation_seed=observation_seed,
        task_id=TASK_ID,
        output_path=trajectory,
        budget_override=len(actions),
        episode_mode_override="single_experiment",
        observation_noise_mode="keyed",
        observation_noise_namespace=namespace,
        world_interventions=interventions,
    )
    records = load_jsonl(trajectory)
    noncommitted = [row for row in records if row.get("transaction_status") != "committed"]
    if noncommitted:
        raise ValueError("provider-selected recipe did not complete under a counterfactual law")
    replay = verify_records(
        records,
        tolerance=0.0,
        world_interventions=interventions,
    ).to_dict()
    if replay.get("verified") is not True:
        raise ValueError("counterfactual trajectory failed exact replay")
    hashes = {str(row.get("mechanism_hash")) for row in records if row.get("mechanism_hash")}
    if len(hashes) != 1:
        raise ValueError("counterfactual execution lacks one fixed mechanism hash")
    metrics = _terminal_metrics(records)
    return {
        "source_law_id": source_law_id,
        "experiment_index": experiment_index,
        "target_law_id": target_law_id,
        "action_plan_sha256": canonical_json_sha256(actions),
        "observation_seed": observation_seed,
        "observation_noise_namespace": namespace,
        "mechanism_hash": next(iter(hashes)),
        "metrics": metrics,
        "safe": metrics["safety_risk"] < float(get_task(TASK_ID).safety_limit),
        "exact_replay": replay,
        "trajectory_sha256": file_sha256(trajectory),
        "elapsed_s": round(perf_counter() - started, 6),
    }


def _paired_analysis(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    keys = sorted(
        {(str(row["source_law_id"]), int(row["experiment_index"])) for row in rows}
    )
    pairs = []
    for source_law_id, experiment_index in keys:
        selected = [
            row
            for row in rows
            if row["source_law_id"] == source_law_id
            and int(row["experiment_index"]) == experiment_index
        ]
        by_law = {str(row["target_law_id"]): row for row in selected}
        if set(by_law) != set(LAW_IDS):
            raise ValueError("counterfactual recipe pair does not contain both laws")
        baseline = by_law["deactivating_baseline"]
        stable = by_law["stable_catalyst"]
        if baseline["action_plan_sha256"] != stable["action_plan_sha256"]:
            raise ValueError("counterfactual pair action plans differ")
        if baseline["observation_seed"] != stable["observation_seed"]:
            raise ValueError("counterfactual pair noise bindings differ")
        gaps = {
            metric: float(stable["metrics"][metric]) - float(baseline["metrics"][metric])
            for metric in baseline["metrics"]
        }
        passed_metrics = [
            metric for metric, gate in PRIMARY_GATES.items() if abs(gaps[metric]) >= gate
        ]
        positive_passed_metrics = [
            metric for metric, gate in PRIMARY_GATES.items() if gaps[metric] >= gate
        ]
        pairs.append(
            {
                "source_law_id": source_law_id,
                "experiment_index": experiment_index,
                "action_plan_sha256": baseline["action_plan_sha256"],
                "deactivating_metrics": baseline["metrics"],
                "stable_metrics": stable["metrics"],
                "stable_minus_deactivating": gaps,
                "gate_ratios": {
                    metric: abs(gaps[metric]) / gate for metric, gate in PRIMARY_GATES.items()
                },
                "metrics_exceeding_absolute_gate": passed_metrics,
                "metrics_exceeding_positive_gate": positive_passed_metrics,
                "at_least_two_metrics_exceed_absolute_gate": len(passed_metrics) >= 2,
                "at_least_two_metrics_exceed_positive_gate": (
                    len(positive_passed_metrics) >= 2
                ),
                "both_safe": baseline["safe"] and stable["safe"],
                "mechanism_hash_changed": (
                    baseline["mechanism_hash"] != stable["mechanism_hash"]
                ),
            }
        )
    metric_reports = {}
    for metric, gate in PRIMARY_GATES.items():
        values = [float(pair["stable_minus_deactivating"][metric]) for pair in pairs]
        metric_reports[metric] = {
            "gate": gate,
            "maximum_absolute_gap": max(abs(value) for value in values),
            "maximum_positive_gap": max(values),
            "minimum_signed_gap": min(values),
            "absolute_gate_exceedance_count": sum(abs(value) >= gate for value in values),
            "positive_gate_exceedance_count": sum(value >= gate for value in values),
            "paired_recipe_count": len(values),
        }
    return {
        "expected_provider_selected_recipe_count": 16,
        "paired_recipe_count": len(pairs),
        "expected_counterfactual_execution_count": 32,
        "counterfactual_execution_count": len(rows),
        "provider_call_count": 0,
        "frozen_reference_gates": PRIMARY_GATES,
        "metric_reports": metric_reports,
        "pairs": pairs,
        "any_primary_metric_exceeds_gate": any(
            report["absolute_gate_exceedance_count"] > 0 for report in metric_reports.values()
        ),
        "any_recipe_has_two_metrics_above_gate": any(
            pair["at_least_two_metrics_exceed_absolute_gate"] for pair in pairs
        ),
        "any_recipe_has_two_positive_metrics_above_gate": any(
            pair["at_least_two_metrics_exceed_positive_gate"] for pair in pairs
        ),
        "all_pairs_change_mechanism_hash": all(
            pair["mechanism_hash_changed"] for pair in pairs
        ),
    }


def _agent_system_contrast(campaigns: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    baseline = campaigns["deactivating_baseline"]
    stable = campaigns["stable_catalyst"]
    baseline_recipes = baseline.get("recipes", [])
    stable_recipes = stable.get("recipes", [])
    if not isinstance(baseline_recipes, list) or not isinstance(stable_recipes, list):
        raise ValueError("participant campaign recipes must be lists")
    if len(baseline_recipes) != 8 or len(stable_recipes) != 8:
        raise ValueError("agent-system contrast requires eight rounds per law")
    round_rows = []
    for baseline_recipe, stable_recipe in zip(
        baseline_recipes,
        stable_recipes,
        strict=True,
    ):
        baseline_metrics = baseline_recipe["provider_final_metrics"]
        stable_metrics = stable_recipe["provider_final_metrics"]
        gaps = {
            metric: float(stable_metrics[metric]) - float(baseline_metrics[metric])
            for metric in (*PRIMARY_GATES, "safety_risk", "score")
        }
        absolute_metrics = [
            metric for metric, gate in PRIMARY_GATES.items() if abs(gaps[metric]) >= gate
        ]
        positive_metrics = [
            metric for metric, gate in PRIMARY_GATES.items() if gaps[metric] >= gate
        ]
        round_rows.append(
            {
                "round": int(baseline_recipe["experiment_index"]),
                "stable_minus_deactivating": gaps,
                "metrics_exceeding_absolute_reference_gate": absolute_metrics,
                "metrics_exceeding_positive_reference_gate": positive_metrics,
                "at_least_two_metrics_exceed_absolute_reference_gate": (
                    len(absolute_metrics) >= 2
                ),
                "recipes_identical": (
                    baseline_recipe.get("recipe_sha256")
                    == stable_recipe.get("recipe_sha256")
                ),
            }
        )
    metric_reports = {}
    for metric, gate in PRIMARY_GATES.items():
        values = [float(row["stable_minus_deactivating"][metric]) for row in round_rows]
        maximum_index = max(range(len(values)), key=lambda index: abs(values[index]))
        metric_reports[metric] = {
            "reference_gate": gate,
            "mean_signed_gap": sum(values) / len(values),
            "maximum_absolute_gap": abs(values[maximum_index]),
            "signed_gap_at_maximum": values[maximum_index],
            "maximum_absolute_gap_round": maximum_index + 1,
            "absolute_gate_round_count": sum(abs(value) >= gate for value in values),
            "positive_gate_round_count": sum(value >= gate for value in values),
            "negative_gate_round_count": sum(value <= -gate for value in values),
        }
    baseline_scores = [
        float(recipe["provider_leaderboard_score"]) for recipe in baseline_recipes
    ]
    stable_scores = [float(recipe["provider_leaderboard_score"]) for recipe in stable_recipes]
    return {
        "estimand": "independent_closed_loop_agent_system_trajectory_contrast",
        "causal_physics_effect": False,
        "reason_not_pure_physics": (
            "The two independent Codex sessions selected different recipes from round 1, "
            "before either session observed a physical outcome."
        ),
        "round_count": len(round_rows),
        "rounds_with_any_primary_metric_above_reference_gate": sum(
            bool(row["metrics_exceeding_absolute_reference_gate"]) for row in round_rows
        ),
        "rounds_with_two_primary_metrics_above_reference_gate": sum(
            row["at_least_two_metrics_exceed_absolute_reference_gate"]
            for row in round_rows
        ),
        "all_round_recipes_identical": all(
            row["recipes_identical"] for row in round_rows
        ),
        "closed_loop_above_reference_gate_observed": any(
            row["metrics_exceeding_absolute_reference_gate"] for row in round_rows
        ),
        "metric_reports": metric_reports,
        "score_summary": {
            "deactivating_mean": sum(baseline_scores) / len(baseline_scores),
            "stable_mean": sum(stable_scores) / len(stable_scores),
            "stable_minus_deactivating_mean": (
                sum(stable_scores) / len(stable_scores)
                - sum(baseline_scores) / len(baseline_scores)
            ),
            "deactivating_best": max(baseline_scores),
            "stable_best": max(stable_scores),
            "stable_minus_deactivating_best": max(stable_scores) - max(baseline_scores),
            "first_four_mean_gap": (
                sum(stable_scores[:4]) / 4.0 - sum(baseline_scores[:4]) / 4.0
            ),
            "last_four_mean_gap": (
                sum(stable_scores[4:]) / 4.0 - sum(baseline_scores[4:]) / 4.0
            ),
        },
        "rounds": round_rows,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if git_worktree_dirty(ROOT):
        raise RuntimeError("paired evaluation requires a clean committed worktree")
    if args.output_root.exists() or args.summary.exists():
        raise FileExistsError("refusing to overwrite paired provider outputs")
    config_paths = {
        "deactivating_baseline": args.deactivating_config.resolve(),
        "stable_catalyst": args.stable_config.resolve(),
    }
    configs = {law_id: _load_object(path) for law_id, path in config_paths.items()}
    config_audit = _validate_configs(configs)
    participant_paths = {
        "deactivating_baseline": args.deactivating_summary.resolve(),
        "stable_catalyst": args.stable_summary.resolve(),
    }
    campaigns = {
        law_id: _campaign_row(law_id, _load_object(path), path)
        for law_id, path in participant_paths.items()
    }
    recipes = [recipe for campaign in campaigns.values() for recipe in campaign["recipes"]]
    args.output_root.mkdir(parents=True)
    started = perf_counter()
    rows = []
    expected = len(recipes) * len(LAW_IDS)
    failures = []
    for recipe in recipes:
        for target_law_id in LAW_IDS:
            try:
                row = _execute(
                    recipe=recipe,
                    target_law_id=target_law_id,
                    output_root=args.output_root,
                )
            except Exception as error:
                failures.append(
                    {
                        "source_law_id": recipe["source_law_id"],
                        "experiment_index": recipe["experiment_index"],
                        "target_law_id": target_law_id,
                        "type": type(error).__name__,
                        "message": str(error)[:1000],
                    }
                )
            else:
                rows.append(row)
            elapsed = perf_counter() - started
            completed = len(rows) + len(failures)
            rate = completed / elapsed if elapsed > 0.0 else 0.0
            print(
                json.dumps(
                    {
                        "stage": "counterfactual_execution",
                        "completed": completed,
                        "successful": len(rows),
                        "total": expected,
                        "failures": len(failures),
                        "throughput_per_min": round(rate * 60.0, 3),
                        "eta_s": round((expected - completed) / rate, 1) if rate else None,
                        "source_law_id": recipe["source_law_id"],
                        "experiment_index": recipe["experiment_index"],
                        "target_law_id": target_law_id,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                flush=True,
            )
    paired = _paired_analysis(rows) if not failures and rows else None
    campaign_complete = all(
        campaign["operationally_complete"]
        and campaign["complete_experiment_count"] == 8
        and campaign["exact_replay"].get("verified") is True
        and campaign["provider_usage"].get("provider_usage_accounting_complete") is True
        for campaign in campaigns.values()
    )
    counterfactual_complete = (
        not failures
        and paired is not None
        and paired["paired_recipe_count"] == 16
        and paired["counterfactual_execution_count"] == 32
        and paired["all_pairs_change_mechanism_hash"] is True
    )
    requested_claim = bool(
        campaign_complete
        and counterfactual_complete
        and paired is not None
        and paired["any_primary_metric_exceeds_gate"]
    )
    w2_33_cell_gate = bool(
        campaign_complete
        and counterfactual_complete
        and paired is not None
        and paired["any_recipe_has_two_metrics_above_gate"]
    )
    agent_system = _agent_system_contrast(campaigns)
    summary = {
        "schema_version": SUMMARY_VERSION,
        "source_commit": git_source_commit(ROOT),
        "formal_result": False,
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "config_audit": config_audit,
        "config_bindings": {
            law_id: {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(path),
            }
            for law_id, path in config_paths.items()
        },
        "participant_campaigns": campaigns,
        "agent_system_closed_loop_contrast": agent_system,
        "participant_denominators": {
            "campaigns_expected": 2,
            "campaigns_operationally_complete": sum(
                campaign["operationally_complete"] for campaign in campaigns.values()
            ),
            "complete_experiments_expected": 16,
            "complete_experiments_observed": sum(
                int(campaign["complete_experiment_count"] or 0)
                for campaign in campaigns.values()
            ),
            "provider_sessions_expected": 2,
            "provider_sessions_observed": sum(
                int(campaign["provider_usage"].get("provider_session_count") or 0)
                for campaign in campaigns.values()
            ),
            "provider_input_tokens": sum(
                int(campaign["provider_usage"].get("input_token_count") or 0)
                for campaign in campaigns.values()
            ),
            "provider_cached_input_tokens": sum(
                int(campaign["provider_usage"].get("cached_input_token_count") or 0)
                for campaign in campaigns.values()
            ),
            "provider_uncached_input_tokens": sum(
                int(campaign["provider_usage"].get("uncached_input_token_count") or 0)
                for campaign in campaigns.values()
            ),
            "provider_output_tokens": sum(
                int(campaign["provider_usage"].get("output_token_count") or 0)
                for campaign in campaigns.values()
            ),
            "provider_errors": sum(
                int(campaign["provider_usage"].get("provider_error_event_count") or 0)
                for campaign in campaigns.values()
            ),
            "recovered_mcp_failures": sum(
                int(campaign["provider_usage"].get("recovered_mcp_tool_failure_count") or 0)
                for campaign in campaigns.values()
            ),
        },
        "counterfactual": paired,
        "counterfactual_failures": failures,
        "checks": {
            "both_provider_campaigns_operationally_complete": campaign_complete,
            "closed_loop_agent_system_difference_exceeds_reference_gate": agent_system[
                "closed_loop_above_reference_gate_observed"
            ],
            "all_32_counterfactual_executions_complete": counterfactual_complete,
            "at_least_one_primary_metric_exceeds_frozen_gate": requested_claim,
            "w2_33_two_metrics_same_recipe_effect_gate": w2_33_cell_gate,
        },
        "requested_claim_supported": requested_claim,
        "closed_loop_agent_system_difference_over_gate_observed": agent_system[
            "closed_loop_above_reference_gate_observed"
        ],
        "fixed_recipe_physics_difference_over_gate_observed": bool(
            paired is not None and paired["any_primary_metric_exceeds_gate"]
        ),
        "w2_33_same_cell_effect_gate_supported": w2_33_cell_gate,
        "full_w2_33_qualification_retested": False,
        "interpretation_boundary": (
            "The direct two-campaign contrast is an agent-system outcome because independent "
            "sessions may choose different recipes. The 32-execution evaluator replay isolates "
            "the physical-law effect on the 16 real-provider-selected recipes."
        ),
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(args.summary, summary)
    return summary


def augment_existing_summary(path: Path) -> dict[str, Any]:
    """Add the frozen closed-loop view without rerunning provider or physics executions."""

    summary = _load_object(path)
    campaigns = summary.get("participant_campaigns")
    if not isinstance(campaigns, Mapping):
        raise ValueError("existing paired summary lacks participant campaigns")
    counterfactual = summary.get("counterfactual")
    if not isinstance(counterfactual, Mapping):
        raise ValueError("existing paired summary lacks its counterfactual analysis")
    if int(counterfactual.get("counterfactual_execution_count", -1)) != 32:
        raise ValueError("existing paired summary does not contain 32 executions")
    if summary.get("counterfactual_failures") != []:
        raise ValueError("existing paired summary contains counterfactual failures")
    agent_system = _agent_system_contrast(campaigns)
    summary["agent_system_closed_loop_contrast"] = agent_system
    checks = summary.get("checks")
    if not isinstance(checks, dict):
        raise ValueError("existing paired summary lacks checks")
    checks["closed_loop_agent_system_difference_exceeds_reference_gate"] = agent_system[
        "closed_loop_above_reference_gate_observed"
    ]
    summary["closed_loop_agent_system_difference_over_gate_observed"] = agent_system[
        "closed_loop_above_reference_gate_observed"
    ]
    summary["fixed_recipe_physics_difference_over_gate_observed"] = bool(
        counterfactual.get("any_primary_metric_exceeds_gate")
    )
    summary.pop("summary_sha256", None)
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(path, summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deactivating-config",
        type=Path,
        default=DEFAULT_CONFIGS["deactivating_baseline"],
    )
    parser.add_argument("--stable-config", type=Path, default=DEFAULT_CONFIGS["stable_catalyst"])
    parser.add_argument(
        "--deactivating-summary",
        type=Path,
        default=DEFAULT_PARTICIPANT_SUMMARIES["deactivating_baseline"],
    )
    parser.add_argument(
        "--stable-summary",
        type=Path,
        default=DEFAULT_PARTICIPANT_SUMMARIES["stable_catalyst"],
    )
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--augment-existing-summary", action="store_true")
    args = parser.parse_args()
    summary = (
        augment_existing_summary(args.summary.resolve())
        if args.augment_existing_summary
        else run(args)
    )
    print(
        json.dumps(
            {
                "requested_claim_supported": summary["requested_claim_supported"],
                "w2_33_same_cell_effect_gate_supported": summary[
                    "w2_33_same_cell_effect_gate_supported"
                ],
                "counterfactual_failures": len(summary["counterfactual_failures"]),
                "output": str(args.summary),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
