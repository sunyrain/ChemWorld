"""Build the sanitized, provider-free Work II publication reanalysis.

This script reads retained local execution evidence once and writes a tracked derived-data report.
The report, rather than ignored provider run roots, is the publication/figure input.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.work_ii_evidence_to_action import (
    evaluate_law_action_agreement,
    predict_candidate_ranking_from_law,
    score_terminal_ranking,
)

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "workstreams/flagship_tasks/reports"
W2_61 = REPORT_DIR / "work-ii-w2-61-cross-model-action-aligned-causal-extension-v0.1.json"
C2_DEEPSEEK = REPORT_DIR / "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
C2_GPT = REPORT_DIR / "work-ii-w2-62-codex-c2-current-composite-evaluation-v0.1.json"
C2_CROSS_MODEL = REPORT_DIR / "work-ii-w2-62-c2-cross-model-current-composite-v0.1.json"
B3_CROSS_MODEL = REPORT_DIR / "work-ii-w2-63-b3-failure-aware-cross-model-v0.1.json"
B2_RESULTS = {
    "deepseek_v4_flash_high": REPORT_DIR / "work-ii-as-study-b2-phase-process-results-v0.1.json",
    "gpt_5_6_sol_medium": REPORT_DIR / "work-ii-as-study-b2-gpt56-sol-medium-results-v0.1.json",
    "deepseek_v4_flash_low": REPORT_DIR
    / "work-ii-as-study-b2-deepseek-v4-flash-low-results-v0.1.json",
}
B2_IDENTIFIABILITY_AUDIT = (
    REPORT_DIR / "work-ii-b2-participant-visible-identifiability-audit-v0.1.json"
)
B2_EXPRESSION_ANALYZER = ROOT / "scripts/analyze_work_ii_study_b2_results.py"
W2_50_ROOT = ROOT / (
    "runs/formal/work-ii-deepseek-multi-task-open-action-five-world-v0.1-20260817-formal2"
)
W2_50_SUMMARY = W2_50_ROOT / "summary.json"
W2_50_MANIFEST = W2_50_ROOT / "input_manifest.json"
W2_50_RUNTIME_ROOT = REPORT_DIR / "work-ii-w2-26-deepseek-runtime-configs-v0.1"
W2_50_RUNTIME_FILES = {
    "electrochemical-conversion": "a_p--electrochemical-conversion--r10.json",
    "reaction-to-crystallization": "a_s--reaction-to-crystallization--r12.json",
    "reaction-safety-constrained": "a_p--reaction-safety-constrained--r10.json",
}
OUTPUT = REPORT_DIR / "work-ii-w2-64-publication-reanalysis-v0.1.json"

MODEL_LABELS = {
    "deepseek": "DeepSeek-v4-flash (reasoning effort: high)",
    "codex": "GPT-5.6-sol (reasoning effort: medium)",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
    ).hexdigest()


def mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def require_close(actual: float, expected: float, label: str, *, tolerance: float = 5e-5) -> None:
    if not math.isclose(actual, expected, abs_tol=tolerance, rel_tol=0.0):
        raise ValueError(f"{label}: {actual!r} != {expected!r}")


def contrast_lookup(block: Mapping[str, Any], contrast: str) -> dict[str, Any]:
    for row in block["contrasts"]:
        if row["contrast"] == contrast:
            return dict(row)
    raise ValueError(f"missing contrast: {contrast}")


def project_b2_expression_and_identifiability(
    results: Mapping[str, Mapping[str, Any]],
    identifiability_audit: Mapping[str, Any],
) -> dict[str, Any]:
    arms = ("opaque", "aligned_nominal", "misindexed_nominal")
    reference_worlds = sorted(
        int(row["world_seed"]) for row in results["deepseek_v4_flash_high"]["world_rows"]
    )
    if len(reference_worlds) != 5:
        raise ValueError("B2 publication projection requires five matched worlds")
    world_index = {seed: index + 1 for index, seed in enumerate(reference_worlds)}

    public_summary_rows: list[dict[str, Any]] = []
    configuration_summaries: dict[str, Any] = {}
    for configuration, result in results.items():
        observed_worlds = sorted(int(row["world_seed"]) for row in result["world_rows"])
        if observed_worlds != reference_worlds:
            raise ValueError(f"B2 worlds differ for {configuration}")
        audit_by_arm = result["public_summary_audit"]["by_arm"]
        flags_by_cell: dict[tuple[str, int], dict[str, Any]] = {}
        public_audit: dict[str, Any] = {}
        for arm in arms:
            arm_audit = audit_by_arm[arm]
            if int(arm_audit["world_count"]) != 5:
                raise ValueError(f"B2 arm denominator differs from five: {configuration}/{arm}")
            public_audit[arm] = {
                key: value for key, value in arm_audit.items() if key != "world_rows"
            }
            for row in arm_audit["world_rows"]:
                seed = int(row["world_seed"])
                flags_by_cell[(arm, seed)] = {
                    key: value for key, value in row.items() if key != "world_seed"
                }

        run_root = ROOT / str(result["run_root"])
        cell_paths = sorted((run_root / "cells").glob("*.json"))
        if len(cell_paths) != 15:
            raise ValueError(f"B2 retained cell denominator differs from 15: {configuration}")
        seen: set[tuple[str, int]] = set()
        for cell_path in cell_paths:
            cell = load_json(cell_path)
            arm = str(cell["arm"])
            seed = int(cell["world_seed"])
            key = (arm, seed)
            if arm not in arms or seed not in world_index or key in seen:
                raise ValueError(f"unexpected B2 cell identity: {configuration}/{key}")
            seen.add(key)
            post = cell["post_prediction"]
            public_summary_rows.append(
                {
                    "configuration": configuration,
                    "world_index": world_index[seed],
                    "arm": arm,
                    "model_summary": str(post["model_summary"]),
                    "evidence_assessment": str(post["evidence_assessment"]),
                    **flags_by_cell[key],
                }
            )
        if seen != set(flags_by_cell):
            raise ValueError(f"B2 public summaries and expression audit differ: {configuration}")
        configuration_summaries[configuration] = {
            "session_count": len(seen),
            "primary_contrast": dict(result["primary_contrast"]),
            "public_expression_audit_by_arm": public_audit,
        }

    decision = dict(identifiability_audit["decision"])
    if decision.get("structural_family_identification_supported") is not False:
        raise ValueError("B2 participant-visible structural identifiability must remain rejected")
    if identifiability_audit["exact_alias"].get("present") is not True:
        raise ValueError("B2 exact linear/power alias must remain recorded")
    if (
        identifiability_audit["positive_control"].get("readout_positive_control_passed")
        is not False
    ):
        raise ValueError("B2 expression readout positive control must remain failed")

    return {
        "schema_version": "chemworld-b2-public-expression-and-identifiability-0.1",
        "world_count": 5,
        "session_count_per_configuration": 15,
        "configuration_summaries": configuration_summaries,
        "public_summary_rows": sorted(
            public_summary_rows,
            key=lambda row: (row["configuration"], row["world_index"], row["arm"]),
        ),
        "expression_coding": {
            "status": "retrospective_keyword_coding_not_preregistered",
            "source_fields": ["model_summary", "evidence_assessment"],
            "private_reasoning_used": False,
            "analyzer_sha256": sha256_file(B2_EXPRESSION_ANALYZER),
        },
        "participant_visible_identifiability": {
            "decision": decision,
            "participant_visible_design": dict(identifiability_audit["participant_visible_design"]),
            "exact_alias": dict(identifiability_audit["exact_alias"]),
            "positive_control": dict(identifiability_audit["positive_control"]),
            "constant_endpoint_baseline": {
                key: identifiability_audit["empirical_alternative"][key]
                for key in (
                    "model",
                    "mean_scoring_error",
                    "minimum_scoring_error",
                    "maximum_scoring_error",
                )
            },
            "provider_call_count": int(identifiability_audit["provider_call_count"]),
            "new_participant_session_count": int(
                identifiability_audit["new_participant_session_count"]
            ),
        },
        "interpretation": (
            "B2 supports low post-packet error and an exact-law-expression dissociation on an "
            "underidentifying free-text surface. Participant-level structural identification is "
            "evaluated only by the separate typed, reference-fitter-identifiable B3 control."
        ),
    }


def project_action_extension(report: Mapping[str, Any]) -> dict[str, Any]:
    if report["denominators"]["scheduled_condition_slots_total"] != 360:
        raise ValueError("four-condition scheduled denominator must be 360")
    projected_models: dict[str, Any] = {}
    required_primary = {"deepseek": -0.0913, "codex": 0.1102}
    rows = report["condition_rows"]
    for model in ("deepseek", "codex"):
        scheduled = report["per_model"][model]["scheduled_failure_aware"]
        eligible = report["per_model"][model]["donor_eligible"]
        primary = contrast_lookup(scheduled, "autonomous_exploration_minus_no_evidence")
        estimate = float(primary["mean_failure_aware_normalized_regret_difference"])
        require_close(estimate, required_primary[model], f"{model} scheduled primary")

        model_rows = [row for row in rows if row["participant"] == model]
        by_stratum: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
        for row in model_rows:
            by_stratum[str(row["stratum_id"])][str(row["condition"])] = row
        eligible_differences: list[dict[str, Any]] = []
        for stratum_id, condition_rows in sorted(by_stratum.items()):
            autonomy = condition_rows["autonomous_exploration"]
            if not autonomy["admitted_stratum"]:
                continue
            no_evidence = condition_rows["no_evidence"]
            eligible_differences.append(
                {
                    "stratum_id": stratum_id,
                    "task_id": str(autonomy["task_id"]),
                    "cluster_id": str(autonomy["cluster_id"]),
                    "prior_arm": str(autonomy["prior_arm"]),
                    "regret_difference": float(
                        autonomy["failure_aware_normalized_regret"]
                        - no_evidence["failure_aware_normalized_regret"]
                    ),
                }
            )

        by_task: dict[str, list[float]] = defaultdict(list)
        by_cluster: dict[str, list[float]] = defaultdict(list)
        cluster_task: dict[str, str] = {}
        for row in eligible_differences:
            by_task[row["task_id"]].append(row["regret_difference"])
            by_cluster[row["cluster_id"]].append(row["regret_difference"])
            cluster_task[row["cluster_id"]] = row["task_id"]
        task_means = {key: float(mean(value)) for key, value in sorted(by_task.items())}
        cluster_means = {key: float(mean(value)) for key, value in sorted(by_cluster.items())}
        task_cluster_means: dict[str, list[float]] = defaultdict(list)
        for cluster_id, value in cluster_means.items():
            task_cluster_means[cluster_task[cluster_id]].append(value)

        eligible_primary = contrast_lookup(eligible, "autonomous_exploration_minus_no_evidence")
        eligible_weighted = float(
            eligible_primary["mean_failure_aware_normalized_regret_difference"]
        )
        require_close(
            eligible_weighted,
            float(mean([row["regret_difference"] for row in eligible_differences])),
            f"{model} eligible reconstruction",
            tolerance=1e-12,
        )
        projected_models[model] = {
            "model_label": MODEL_LABELS[model],
            "primary_all_scheduled": {
                "condition_summaries": scheduled["condition_summaries"],
                "contrasts": scheduled["contrasts"],
                "estimand": "all-scheduled failure-aware strategy estimand",
                "scheduled_stratum_count": 45,
                "independent_task_world_cluster_count": 15,
            },
            "donor_eligible_sensitivity": {
                "condition_summaries": eligible["condition_summaries"],
                "contrasts": eligible["contrasts"],
                "eligible_stratum_count": int(eligible["stratum_count"]),
                "autonomy_minus_no_evidence": {
                    "eligible_stratum_weighted_mean": eligible_weighted,
                    "equal_task_mean": float(mean(list(task_means.values()))),
                    "equal_cluster_mean": float(mean(list(cluster_means.values()))),
                    "equal_task_equal_cluster_mean": float(
                        mean(
                            [
                                float(mean(values))
                                for _, values in sorted(task_cluster_means.items())
                            ]
                        )
                    ),
                    "task_means": task_means,
                    "eligible_cluster_count": len(cluster_means),
                    "interpretation": (
                        "Availability-conditioned sensitivity; donor eligibility is a "
                        "post-treatment variable and is not the primary strategy estimand."
                    ),
                },
            },
        }
    return {
        "scheduled_condition_slots_total": 360,
        "scheduled_condition_slots_per_model": 180,
        "models": projected_models,
        "primary_population": "all 45 scheduled strata within model",
        "failure_rule": (
            "Missing donor, unstarted donor-dependent recipient, participant/schema failure or "
            "missing ranking retains failure-aware normalized regret 1."
        ),
    }


def project_c2(
    deepseek: Mapping[str, Any],
    gpt: Mapping[str, Any],
    cross_model: Mapping[str, Any],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "inference_unit": "45 independent task-world clusters per model",
        "session_structure": "135 separate sessions nested within 45 task-world clusters",
        "models": {},
    }
    for model, report in (("deepseek", deepseek), ("codex", gpt)):
        denominator = report["denominators"]
        overall = cross_model["models"][model]["overall"]
        result["models"][model] = {
            "model_label": MODEL_LABELS[model],
            "scheduled_session_count": int(denominator["cell_count"]),
            "terminal_state_counts": denominator["terminal_state_counts"],
            "completed_cell_count": int(denominator["terminal_state_counts"].get("completed", 0)),
            "checkpoint_scored_count": int(denominator["checkpoint_scored_count"]),
            "checkpoint_scheduled_count": int(denominator["checkpoint_scheduled_count"]),
            "law_evaluated_count": int(denominator["law_summary_evaluated_count"]),
            "law_scheduled_count": int(denominator["law_summary_scheduled_count"]),
            "blind_gain_evaluable_count": int(overall["blind_gain_evaluable_count"]),
            "blind_scheduled_cell_count": int(overall["scheduled_cell_count"]),
            "mean_prediction_improvement": float(overall["mean_prediction_improvement"]),
            "mean_law_mae": float(overall["mean_law_mae"]),
            "mean_law_compression_loss": float(overall["mean_law_compression_loss"]),
            "mean_blind_gain": float(overall["mean_blind_gain"]),
        }
    expected = {
        "deepseek": (121, 675, 135, 121),
        "codex": (126, 669, 129, 126),
    }
    for model, values in expected.items():
        row = result["models"][model]
        actual = (
            row["completed_cell_count"],
            row["checkpoint_scored_count"],
            row["law_evaluated_count"],
            row["blind_gain_evaluable_count"],
        )
        if actual != values:
            raise ValueError(f"{model} C2 denominators: {actual!r} != {values!r}")
    return result


def project_b3(report: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "inference_unit": "five shared task-world clusters; intervals are descriptive",
        "scheduled_action_opportunity_count_per_model": 18,
        "models": {},
    }
    for model in ("deepseek", "codex"):
        overall = report["models"][model]["overall"]
        if overall["scheduled_cell_count"] != 30:
            raise ValueError(f"{model} B3 scheduled denominator must be 30")
        result["models"][model] = {
            "model_label": MODEL_LABELS[model],
            "scheduled_cell_count": int(overall["scheduled_cell_count"]),
            "completed_cell_count": int(overall["completed_cell_count"]),
            "failed_cell_count": int(overall["failed_cell_count"]),
            "failure_classification_counts": overall["failure_classification_counts"],
            "joint_law_recovery_count": int(overall["failure_aware_joint_recovery_count"]),
            "top1_count": int(overall["failure_aware_top1_count"]),
            "mean_failure_aware_regret": float(overall["failure_aware_mean_regret"]),
            "completed_mean_post_mae": float(overall["completed_mean_post_mae"]),
            "useful_gain_completed_opportunity": {
                "count": int(overall["eligible_gain_at_least_0_02_count"]),
                "denominator": int(overall["eligible_gain_denominator"]),
            },
            "useful_gain_scheduled_opportunity": {
                "count": int(overall["eligible_gain_at_least_0_02_count"]),
                "denominator": 18,
                "failure_or_unavailable_counted_as_zero": True,
            },
        }
    if result["models"]["deepseek"]["completed_cell_count"] != 17:
        raise ValueError("DeepSeek B3 completed denominator must be 17")
    if result["models"]["codex"]["completed_cell_count"] != 30:
        raise ValueError("GPT B3 completed denominator must be 30")
    return result


def final_law(cell: Mapping[str, Any]) -> Mapping[str, Any] | None:
    campaign = cell.get("campaign_summary")
    if not isinstance(campaign, Mapping):
        return None
    analysis = campaign.get("analysis")
    if not isinstance(analysis, Mapping):
        return None
    snapshots = analysis.get("belief_snapshots")
    if not isinstance(snapshots, list):
        return None
    for snapshot in reversed(snapshots):
        if isinstance(snapshot, Mapping) and isinstance(snapshot.get("law_summary"), Mapping):
            return snapshot["law_summary"]
    return None


def summarize_decision_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    evaluated = [row for row in rows if row["law_status"] == "evaluated"]
    action_agreement = [row for row in evaluated if row["law_implied_top1_followed"] is not None]
    quadrants = Counter(str(row["law_action_quadrant"]) for row in evaluated)
    return {
        "scheduled_cell_count": len(rows),
        "law_evaluated_count": len(evaluated),
        "law_unavailable_or_invalid_count": len(rows) - len(evaluated),
        "law_implied_top1_count": sum(int(row["law_implied_top1"]) for row in evaluated),
        "participant_top1_count": sum(int(row["participant_top1"]) for row in evaluated),
        "law_implied_top1_followed_count": sum(
            int(row["law_implied_top1_followed"]) for row in action_agreement
        ),
        "law_action_agreement_evaluable_count": len(action_agreement),
        "mean_law_implied_normalized_regret": mean(
            [float(row["law_implied_normalized_regret"]) for row in evaluated]
        ),
        "mean_participant_normalized_regret": mean(
            [float(row["participant_normalized_regret"]) for row in evaluated]
        ),
        "mean_action_utilization_delta": mean(
            [float(row["action_utilization_delta"]) for row in evaluated]
        ),
        "law_action_quadrant_counts": dict(sorted(quadrants.items())),
    }


def project_w2_50(
    summary: Mapping[str, Any],
    manifest: Mapping[str, Any],
    candidate_features_by_task: Mapping[str, Mapping[str, Mapping[str, Any]]],
) -> dict[str, Any]:
    if summary["scheduled_cell_count"] != 45 or manifest["cell_count"] != 45:
        raise ValueError("W2-50 scheduled denominator must be 45")
    if summary["provider_free_truth_query_count"] != 240:
        raise ValueError("W2-50 truth denominator must be 240")
    if summary["provider_free_exact_replay_count"] != 240:
        raise ValueError("W2-50 replay denominator must be 240")
    manifest_rows = {str(row["cell_id"]): row for row in manifest["cells"]}
    if set(manifest_rows) != {str(row["cell_id"]) for row in summary["cell_rows"]}:
        raise ValueError("W2-50 summary and manifest cell identities differ")

    open_action_rows: list[dict[str, Any]] = []
    decision_rows: list[dict[str, Any]] = []
    for raw in sorted(summary["cell_rows"], key=lambda row: str(row["cell_id"])):
        cell_id = str(raw["cell_id"])
        manifest_row = manifest_rows[cell_id]
        open_action_rows.append(
            {
                "participant_model": "deepseek_v4_flash",
                "cell_id": cell_id,
                "cluster_id": str(raw["cluster_id"]),
                "task_id": str(manifest_row["task_id"]),
                "world_seed": int(raw["world_seed"]),
                "arm": str(raw["arm"]),
                "status": str(raw["status"]),
                "eligible": raw["status"] == "completed_uncontaminated",
                "selected_rank": raw.get("selected_rank"),
                "normalized_regret": raw.get("normalized_regret"),
                "top1_selected": raw.get("top1_selected"),
                "law_adequate": raw.get("law_adequate"),
                "law_normalized_mae": raw.get("law_normalized_mae"),
                "mechanism_action_category": raw.get("mechanism_action_category"),
                "selected_minus_random_candidate_mean": raw.get(
                    "selected_minus_random_candidate_mean"
                ),
            }
        )

        base = {
            "participant_model": "deepseek_v4_flash",
            "law_source": "last_available_executable_law",
            "cell_id": cell_id,
            "cluster_id": str(raw["cluster_id"]),
            "task_id": str(manifest_row["task_id"]),
            "world_seed": int(raw["world_seed"]),
            "prior_arm": str(raw["arm"]),
            "law_normalized_mae": raw.get("law_normalized_mae"),
        }
        law_payload = final_law(raw)
        ranking = raw.get("participant_ranking")
        contract = manifest_row["checkpoint_truth_plan"]["law_summary_contract"]
        task_id = str(manifest_row["task_id"])
        public_queries = manifest_row["terminal_action_readout"]["candidate_queries"]
        task_features = candidate_features_by_task[task_id]
        queries = [
            {
                "query_id": str(query["query_id"]),
                "feature_values": task_features[str(query["query_id"])]["feature_values"],
            }
            for query in public_queries
        ]
        truth = manifest_row["candidate_truth"]
        if law_payload is None:
            decision_rows.append(
                {
                    **base,
                    "law_status": "unavailable",
                    "law_error": None,
                    "law_implied_top1": None,
                    "law_implied_normalized_regret": None,
                    "participant_top1": int(raw.get("top1_selected") or 0),
                    "participant_normalized_regret": raw.get("normalized_regret", 1.0),
                    "law_implied_top1_followed": None,
                    "law_action_complete_ranking_agreement": None,
                    "law_action_spearman_rank_correlation": None,
                    "law_action_pairwise_agreement": None,
                    "action_utilization_delta": None,
                    "law_action_quadrant": None,
                }
            )
            continue
        try:
            implied = predict_candidate_ranking_from_law(
                law_payload,
                candidate_queries=queries,
                allowed_feature_ids=contract["allowed_feature_ids"],
                allowed_metric_ids=contract["allowed_metric_ids"],
                evidence_catalog=contract["evidence_catalog"],
            )
            law_score = score_terminal_ranking(implied["law_implied_ranking"], truth)
            participant_score = score_terminal_ranking(ranking, truth)
            agreement = evaluate_law_action_agreement(ranking, implied["law_implied_ranking"])
        except (KeyError, TypeError, ValueError) as exc:
            decision_rows.append(
                {
                    **base,
                    "law_status": "invalid",
                    "law_error": type(exc).__name__,
                    "law_implied_top1": None,
                    "law_implied_normalized_regret": None,
                    "participant_top1": int(raw.get("top1_selected") or 0),
                    "participant_normalized_regret": raw.get("normalized_regret", 1.0),
                    "law_implied_top1_followed": None,
                    "law_action_complete_ranking_agreement": None,
                    "law_action_spearman_rank_correlation": None,
                    "law_action_pairwise_agreement": None,
                    "action_utilization_delta": None,
                    "law_action_quadrant": None,
                }
            )
            continue

        useful = int(law_score["top1"]) == 1
        followed_value = agreement["law_implied_top1_followed"]
        if followed_value is None:
            quadrant = "decision_useful_law_no_action" if useful else "decision_poor_law_no_action"
        else:
            followed = int(followed_value) == 1
            quadrant = ("decision_useful_law" if useful else "decision_poor_law") + (
                "_followed" if followed else "_not_followed"
            )
        decision_rows.append(
            {
                **base,
                "law_status": "evaluated",
                "law_error": None,
                "law_implied_top1": int(law_score["top1"]),
                "law_implied_normalized_regret": float(
                    law_score["failure_aware_normalized_regret"]
                ),
                "participant_top1": int(participant_score["top1"]),
                "participant_normalized_regret": float(
                    participant_score["failure_aware_normalized_regret"]
                ),
                "law_implied_top1_followed": (
                    None if followed_value is None else int(followed_value)
                ),
                "law_action_complete_ranking_agreement": agreement[
                    "law_action_complete_ranking_agreement"
                ],
                "law_action_spearman_rank_correlation": agreement[
                    "law_action_spearman_rank_correlation"
                ],
                "law_action_pairwise_agreement": agreement["law_action_pairwise_agreement"],
                "action_utilization_delta": float(
                    participant_score["failure_aware_normalized_regret"]
                    - law_score["failure_aware_normalized_regret"]
                ),
                "law_action_quadrant": quadrant,
            }
        )

    by_task = {
        task_id: summarize_decision_rows(
            [row for row in decision_rows if row["task_id"] == task_id]
        )
        for task_id in sorted({row["task_id"] for row in decision_rows})
    }
    return {
        "scheduled_cell_count": 45,
        "eligible_cell_count": int(summary["eligible_cell_count"]),
        "independent_task_world_cluster_count": 15,
        "provider_free_truth_query_count": 240,
        "provider_free_exact_replay_count": 240,
        "open_action_rows": open_action_rows,
        "decision_aligned_law_action": {
            "participant_model": "deepseek_v4_flash",
            "law_selection_rule": (
                "Use the last available executable law in each frozen DeepSeek longitudinal cell; "
                "three cells have no terminal action ranking but retain an earlier executable law."
            ),
            "definition": (
                "Truth-law error is the normalized regret of the law-implied Top-1; "
                "action-utilization delta is participant regret minus law-implied regret."
            ),
            "overall": summarize_decision_rows(decision_rows),
            "by_task": by_task,
            "cell_rows": decision_rows,
            "interpretation": (
                "Descriptive association on retained frozen cells; neither executable-law quality "
                "nor law following was randomized."
            ),
        },
    }


def main() -> int:
    runtime_paths = tuple(
        W2_50_RUNTIME_ROOT / filename for filename in W2_50_RUNTIME_FILES.values()
    )
    source_paths = (
        W2_61,
        C2_DEEPSEEK,
        C2_GPT,
        C2_CROSS_MODEL,
        B3_CROSS_MODEL,
        *B2_RESULTS.values(),
        B2_IDENTIFIABILITY_AUDIT,
        B2_EXPRESSION_ANALYZER,
        W2_50_SUMMARY,
        W2_50_MANIFEST,
        *runtime_paths,
    )
    missing = [str(path) for path in source_paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing retained source evidence: {missing}")
    w2_61 = load_json(W2_61)
    deepseek_c2 = load_json(C2_DEEPSEEK)
    gpt_c2 = load_json(C2_GPT)
    cross_model_c2 = load_json(C2_CROSS_MODEL)
    b3 = load_json(B3_CROSS_MODEL)
    b2_results = {name: load_json(path) for name, path in B2_RESULTS.items()}
    b2_identifiability_audit = load_json(B2_IDENTIFIABILITY_AUDIT)
    w2_50_summary = load_json(W2_50_SUMMARY)
    w2_50_manifest = load_json(W2_50_MANIFEST)
    candidate_features_by_task: dict[str, dict[str, dict[str, Any]]] = {}
    for task_id, filename in W2_50_RUNTIME_FILES.items():
        runtime = load_json(W2_50_RUNTIME_ROOT / filename)
        held_out = runtime["belief_checkpoint"]["held_out_queries"]
        candidate_features_by_task[task_id] = {str(row["query_id"]): dict(row) for row in held_out}

    report: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-publication-reanalysis-0.1",
        "status": "completed_provider_free_publication_reanalysis",
        "formal_result": False,
        "formal_result_scope": (
            "No new formal execution was performed; retained formal and development source "
            "evidence keeps its original role."
        ),
        "new_formal_execution": False,
        "provider_calls": 0,
        "physics_executions": 0,
        "action_extension": project_action_extension(w2_61),
        "c2_denominators": project_c2(deepseek_c2, gpt_c2, cross_model_c2),
        "b3_denominators": project_b3(b3),
        "b2_expression_and_identifiability": (
            project_b2_expression_and_identifiability(
                b2_results,
                b2_identifiability_audit,
            )
        ),
        "w2_50": project_w2_50(w2_50_summary, w2_50_manifest, candidate_features_by_task),
        "source_bindings": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256_file(path),
            }
            for path in source_paths
        ],
        "claim_boundaries": {
            "initial_model_assignment_manipulated": True,
            "stochastic_participant_effect_identified": False,
            "matched_evidence_conditional_post_packet_response_supported": True,
            "matched_evidence_pure_packet_effect_supported": False,
            "b2_structural_family_identification_supported": False,
            "b3_participant_visible_structural_identification_test": True,
            "w2_50_law_action_association_descriptive": True,
            "w2_61_development_strategy_estimate": True,
            "oracle_and_gate_results_are_evaluator_diagnostics": True,
            "provider_effect_supported": False,
            "model_superiority_supported": False,
            "causal_law_to_action_effect_supported": False,
        },
    }
    report["summary_sha256"] = canonical_sha(report)
    OUTPUT.write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "output": OUTPUT.relative_to(ROOT).as_posix(),
                "w2_50_law_evaluated": report["w2_50"]["decision_aligned_law_action"]["overall"][
                    "law_evaluated_count"
                ],
                "summary_sha256": report["summary_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
