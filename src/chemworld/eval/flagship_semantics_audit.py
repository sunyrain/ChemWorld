"""Fail-closed semantic audit for every flagship experiment component."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from chemworld.eval.mechanism_adaptation import (
    build_paired_campaign_matrix,
    validate_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_relation_graph import (
    validate_diagnostic_relation_graph,
)
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.tasks import FLAGSHIP_TASK_IDS

FLAGSHIP_SEMANTICS_AUDIT_VERSION = "chemworld-flagship-semantics-audit-0.1"


def audit_flagship_experiment_semantics(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
    relation_graph: Mapping[str, Any],
) -> dict[str, Any]:
    """Audit controls, denominators, blinding, cohorts, and frozen decisions."""

    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check": check_id, "pass": bool(passed), "detail": detail})

    validation_errors = validate_mechanism_adaptation_protocol(protocol)
    add(
        "protocol_schema_valid",
        not validation_errors,
        f"validation_errors={validation_errors}",
    )
    protocol_tasks = tuple(str(item) for item in protocol["design"]["tasks"])
    add(
        "formal_flagship_task_scope_explicit",
        set(protocol_tasks) == set(FLAGSHIP_TASK_IDS),
        (
            f"formal_protocol_tasks={protocol_tasks}; "
            f"registered_flagship_tasks={FLAGSHIP_TASK_IDS}"
        ),
    )

    calibrated = protocol["evaluation_tracks"]["calibrated_online_change"]
    requirement = plan["online_policy_feasible_certificate"]
    add(
        "a3_true_no_change_condition",
        calibrated["truth_change_time_support"] == ["never", 6, 8, 10]
        and requirement["truth_change_time_support"] == ["never", 6, 8, 10]
        and requirement["no_change_condition_included"] is True,
        "The calibrated truth support must contain never, 6, 8, and 10.",
    )
    pairs: dict[str, set[str]] = {}
    pair_clusters: dict[str, set[str]] = {}
    matrix_error: str | None = None
    try:
        matrix = build_paired_campaign_matrix(protocol)
    except ValueError as error:
        matrix = []
        matrix_error = str(error)
    for row in matrix:
        pair_id = str(row["pair_id"])
        pairs.setdefault(pair_id, set()).add(str(row["arm"]))
        pair_clusters.setdefault(pair_id, set()).add(
            str(row["statistical_cluster_id"])
        )
    add(
        "a3_no_change_campaigns_are_matched",
        bool(pairs)
        and all(arms == {"changed", "no_change_twin"} for arms in pairs.values()),
        f"paired_cell_count={len(pairs)}; matrix_error={matrix_error}",
    )
    add(
        "a3_changed_and_no_change_twins_share_statistical_cluster",
        bool(pair_clusters)
        and all(len(cluster_ids) == 1 for cluster_ids in pair_clusters.values()),
        (
            f"paired_cell_count={len(pair_clusters)}; "
            "each changed/no-change pair must contribute one dependent cluster"
        ),
    )

    reference = calibrated["reference_sufficiency"]
    add(
        "reference_has_structural_and_predictive_layers",
        reference["basis"]
        == "universal_structural_relation_coverage_and_held_out_predictive_adequacy"
        and reference["all_declared_relations_observed"] is True
        and reference["held_out_old_world_predictive_check_required"] is True,
        f"reference_basis={reference['basis']}",
    )
    add(
        "reference_is_universal_not_truth_conditioned",
        reference["scope"]
        == "universal_all_declared_candidate_families_without_truth_conditioning"
        and requirement["reference_scope"] == reference["scope"],
        f"reference_scope={reference['scope']}",
    )
    primary_metrics = set(calibrated["primary_metrics"])
    add(
        "conditional_and_end_to_end_metrics_both_frozen",
        {
            "family_attribution_conditional_on_reference_sufficiency",
            "p_reference_sufficient",
            "p_detection_given_reference",
            "p_attribution_given_detection_and_reference",
            "end_to_end_reference_detection_attribution_success",
        }.issubset(primary_metrics),
        f"primary_metrics={sorted(primary_metrics)}",
    )

    hidden_timing = set(calibrated["agent_visible_timing_contract"]["hidden"])
    add(
        "agent_timing_and_certificate_blinded",
        {
            "minimum_stable_prefix_experiments",
            "change_after_experiments",
            "truth_change_time",
            "reference_sufficiency_certificate",
        }.issubset(hidden_timing)
        and requirement["policy_receives_change_time_support"] is False
        and requirement["policy_receives_minimum_stable_prefix"] is False
        and requirement["policy_receives_reference_certificate"] is False,
        f"hidden_agent_fields={sorted(hidden_timing)}",
    )
    add(
        "changepoint_index_semantics_frozen",
        requirement["changepoint_semantics"]
        == "tau_is_completed_old_world_experiment_count"
        and calibrated["total_experiment_horizon"] >= 18,
        calibrated["changepoint_semantics"],
    )

    partitions = plan["cohort_partition"]
    cohort_namespaces = {
        cohort_id: int(cohort["seed_namespace_start"])
        for cohort_id, cohort in partitions.items()
        if isinstance(cohort, Mapping) and "seed_namespace_start" in cohort
    }
    add(
        "development_a2_a3_private_cohorts_disjoint",
        set(cohort_namespaces)
        == {
            "development",
            "a2_certification",
            "a3_certification",
            "private_confirmation",
        }
        and len(set(cohort_namespaces.values())) == 4
        and partitions["cross_cohort_world_seed_reuse_allowed"] is False,
        f"seed_namespaces={cohort_namespaces}",
    )
    frozen_criteria = requirement["frozen_pass_criteria"]
    add(
        "a3_pass_criteria_frozen_before_execution",
        {
            "minimum_reference_acquisition_rate_wilson_lower_bound",
            "minimum_changed_detection_recall_cluster_bootstrap_lower_bound",
            "maximum_no_change_false_positive_rate_cluster_bootstrap_upper_bound",
            "minimum_change_detection_auroc_cluster_bootstrap_lower_bound",
            "maximum_change_probability_brier_score",
            "minimum_attribution_given_detection_and_reference_cluster_bootstrap_lower_bound",
            "minimum_end_to_end_success_rate_cluster_bootstrap_lower_bound",
        }.issubset(frozen_criteria),
        f"criteria={sorted(frozen_criteria)}",
    )

    feedback = protocol["paired_feedback_design"]
    local_feedback = feedback["local_prefix_reaction_test"]
    campaign_feedback = feedback["full_campaign_utility_test"]
    add(
        "feedback_local_causal_pairing",
        local_feedback["same_public_history_prefix"] is True
        and local_feedback["only_last_feedback_packet_changes"] is True
        and local_feedback["provider_repeats_required"] is True,
        "Local feedback sensitivity changes only the final feedback packet.",
    )
    add(
        "feedback_campaign_pairing",
        campaign_feedback["paired_world_seed"] is True
        and campaign_feedback["paired_initial_state"] is True
        and campaign_feedback["paired_prompt_and_model_settings"] is True,
        "Full-campaign utility uses matched world, state, prompt, and model settings.",
    )

    recovery = protocol["recovery_design"]
    add(
        "recovery_world_effect_and_adaptation_decomposed",
        all(
            recovery.get(key) is True
            for key in (
                "open_loop_iid_action_replay_on_iid_world",
                "open_loop_iid_action_replay_on_shifted_world",
                "frozen_policy_on_shifted_world",
                "adaptive_policy_on_shifted_world",
                "diagnosis_oracle_on_shifted_world",
            )
        )
        and "world_effect" in recovery
        and "adaptation_gain" in recovery,
        "Recovery separates world effect, frozen policy, adaptive policy, and oracle.",
    )
    autonomy = protocol["autonomy_contract"]
    add(
        "autonomy_and_assisted_science_both_reported",
        autonomy["both_scores_mandatory"] is True
        and "autonomous_score" in autonomy
        and "assisted_scientific_score" in autonomy,
        "Procedural autonomy cannot be hidden by assisted closeout.",
    )
    add(
        "diagnostic_relation_graph_frozen_and_bound",
        not validate_diagnostic_relation_graph(protocol, plan, relation_graph),
        (
            f"graph_sha256={relation_graph.get('graph_sha256')}; "
            f"relation_count={relation_graph.get('relation_count')}"
        ),
    )
    add(
        "publication_claim_fails_closed_before_empirical_gates",
        protocol["publication_ready"] is False
        and protocol["benchmark_claim_allowed"] is False
        and plan["formal_benchmark_result"] is False,
        "Design validation cannot enable a benchmark or publication claim.",
    )

    failures = [item for item in checks if not item["pass"]]
    return {
        "schema_version": FLAGSHIP_SEMANTICS_AUDIT_VERSION,
        "status": "passed" if not failures else "failed",
        "pass": not failures,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_json_sha256(protocol),
        "gate_a_plan_id": plan["plan_id"],
        "gate_a_plan_sha256": canonical_json_sha256(plan),
        "formal_flagship_task_ids": list(protocol_tasks),
        "scope": (
            "all mechanism-adaptation flagship experiment components: "
            "integrity, identifiability, change detection, feedback causality, "
            "recovery, and autonomy"
        ),
        "check_count": len(checks),
        "failure_count": len(failures),
        "failures": failures,
        "checks": checks,
        "claim_boundary": (
            "A pass certifies protocol semantics and frozen controls only. It does "
            "not certify A2, A3, a hosted Agent, or publication readiness."
        ),
    }


__all__ = [
    "FLAGSHIP_SEMANTICS_AUDIT_VERSION",
    "audit_flagship_experiment_semantics",
]
