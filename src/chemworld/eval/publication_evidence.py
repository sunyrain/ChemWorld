"""Compact, fail-closed evidence summaries for publication-candidate runs."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Sequence
from statistics import fmean
from typing import Any

from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.publication_protocol import (
    assert_valid_publication_protocol,
    canonical_protocol_sha256,
)
from chemworld.eval.validity_power import audit_validity_power
from chemworld.tasks import SERIOUS_TASK_IDS

PUBLICATION_EVIDENCE_SCHEMA_VERSION = "chemworld-publication-evidence-0.1"
PUBLICATION_COMPARISONS = (
    ("structured_gp_bo", "random"),
    ("lhs", "random"),
    ("gp_bo", "random"),
    ("structured_gp_bo", "gp_bo"),
    ("structured_safe_gp_bo", "structured_gp_bo"),
)


def payload_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_publication_evidence_summary(
    results: Sequence[dict[str, Any]],
    *,
    run_manifest: dict[str, Any],
    validity_report: dict[str, Any],
    protocol: dict[str, Any],
) -> dict[str, Any]:
    """Validate the formal matrix and retain only publication-relevant evidence."""

    assert_valid_publication_protocol(protocol)
    _validate_matrix(results, run_manifest=run_manifest, protocol=protocol)
    expected_results_sha256 = str(run_manifest["baseline_results_sha256"])
    provenance = validity_report.get("provenance", {})
    if provenance.get("baseline_results_sha256") != expected_results_sha256:
        raise ValueError("validity report and run manifest bind different result matrices")
    if validity_report.get("planned_seed_count") != len(
        protocol["experimental_design"]["seeds"]
    ):
        raise ValueError("validity report does not use the protocol seed depth")

    statistics = protocol["statistics"]
    comparison_audit = audit_validity_power(
        results,
        task_ids=tuple(SERIOUS_TASK_IDS),
        method_pairs=PUBLICATION_COMPARISONS,
        adaptive_method_pairs=(("structured_gp_bo", "random"),),
        practical_effect=float(statistics["sesoi_total_score"]),
        alpha=float(statistics["alpha"]),
        planned_seed_count=int(statistics["prospective_seed_count"]),
        bootstrap_samples=int(statistics["bootstrap_samples"]),
    )

    task_summaries: dict[str, dict[str, Any]] = {}
    primary_positive_count = 0
    primary_sesoi_count = 0
    for task_id in SERIOUS_TASK_IDS:
        primary_field = PRIMARY_METRIC_FIELDS[task_id]
        task_results = [row for row in results if row["task_id"] == task_id]
        primary_audit = audit_validity_power(
            task_results,
            task_ids=(task_id,),
            method_pairs=PUBLICATION_COMPARISONS,
            adaptive_method_pairs=(("structured_gp_bo", "random"),),
            metric=primary_field,
            practical_effect=float(statistics["sesoi_primary_normalized_metric"]),
            alpha=float(statistics["alpha"]),
            planned_seed_count=int(statistics["prospective_seed_count"]),
            bootstrap_samples=int(statistics["bootstrap_samples"]),
        )
        total_comparisons = comparison_audit["tasks"][task_id]["comparisons"]
        primary_comparisons = primary_audit["tasks"][task_id]["comparisons"]
        confirmatory_primary = primary_comparisons[
            "structured_gp_bo__minus__random"
        ]
        primary_positive = confirmatory_primary["paired_bootstrap_ci"][0] > 0.0
        primary_at_sesoi = (
            confirmatory_primary["mean_paired_effect"]
            >= float(statistics["sesoi_primary_normalized_metric"])
        )
        primary_positive_count += int(primary_positive)
        primary_sesoi_count += int(primary_at_sesoi)
        task_summaries[task_id] = {
            "primary_result_field": primary_field,
            "methods": _method_summaries(task_results, primary_field=primary_field),
            "total_score_comparisons": total_comparisons,
            "primary_metric_comparisons": primary_comparisons,
            "claim_gate": {
                "primary_direction_supported": primary_positive,
                "primary_effect_reaches_sesoi": primary_at_sesoi,
                "task_capability_validated": primary_positive and primary_at_sesoi,
            },
        }

    total_confirmatory = [
        task_summaries[task_id]["total_score_comparisons"][
            "structured_gp_bo__minus__random"
        ]
        for task_id in SERIOUS_TASK_IDS
    ]
    risk_signal_observed = any(
        abs(float(row.get("mean_risk", 0.0))) > 1.0e-12
        or int(row.get("safety_violations", 0)) > 0
        for row in results
    )
    gates = {
        "formal_matrix_complete": True,
        "trajectory_results_verified": all(row.get("verified") is True for row in results),
        "total_score_positive_all_tasks": all(
            item["mean_paired_effect"] > 0.0 for item in total_confirmatory
        ),
        "total_score_holm_significant_all_tasks": all(
            item["significant_after_holm"] for item in total_confirmatory
        ),
        "total_score_sesoi_task_count": sum(
            item["mean_paired_effect"] >= float(statistics["sesoi_total_score"])
            for item in total_confirmatory
        ),
        "primary_direction_supported_task_count": primary_positive_count,
        "primary_sesoi_task_count": primary_sesoi_count,
        "primary_claims_validated_all_tasks": primary_sesoi_count == len(SERIOUS_TASK_IDS),
        "safety_risk_signal_informative": risk_signal_observed,
        "generalization_evidence_complete": False,
        "exploit_audit_complete": False,
        "independent_reproduction_complete": False,
    }
    publication_ready = all(
        (
            gates["formal_matrix_complete"],
            gates["trajectory_results_verified"],
            gates["primary_claims_validated_all_tasks"],
            gates["safety_risk_signal_informative"],
            gates["generalization_evidence_complete"],
            gates["exploit_audit_complete"],
            gates["independent_reproduction_complete"],
        )
    )
    return {
        "schema_version": PUBLICATION_EVIDENCE_SCHEMA_VERSION,
        "status": "publication_ready" if publication_ready else "blocked",
        "publication_ready": publication_ready,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_protocol_sha256(protocol),
        "evaluated_source_commit": run_manifest["evaluated_source_commit"],
        "formal_stage": run_manifest["formal_stage"],
        "matrix": {
            "tasks": list(run_manifest["tasks"]),
            "methods": list(run_manifest["methods"]),
            "seeds": list(run_manifest["seeds"]),
            "complete_experiments_per_task_seed": run_manifest[
                "complete_experiments_per_task_seed"
            ],
            "result_count": len(results),
        },
        "integrity": {
            "evaluation_source_tree_dirty": run_manifest[
                "evaluation_source_tree_dirty"
            ],
            "baseline_results_sha256": expected_results_sha256,
            "validity_power_sha256": run_manifest["validity_power_sha256"],
            "verified_result_count": sum(row.get("verified") is True for row in results),
        },
        "gates": gates,
        "tasks": task_summaries,
        "limitations": [
            (
                "Electrochemical and equilibrium total-score gains do not establish "
                "gains in their declared primary metrics."
            ),
            (
                "The formal matrix contains no non-zero safety-risk observations, so "
                "the safety-constrained baseline is not an informative safety test."
            ),
            (
                "No generalization, private-evaluation, exploit-resistance, or "
                "independent-reproduction evidence is attached."
            ),
            "Regret is not reported because no independent reference protocol is frozen.",
        ],
    }


def _validate_matrix(
    results: Sequence[dict[str, Any]],
    *,
    run_manifest: dict[str, Any],
    protocol: dict[str, Any],
) -> None:
    if run_manifest.get("status") != "completed" or run_manifest.get("formal_stage") != "full":
        raise ValueError("publication evidence requires a completed full-stage run")
    if run_manifest.get("evaluation_source_tree_dirty") is not False:
        raise ValueError("publication evidence requires a clean evaluated source tree")
    protocol_sha256 = canonical_protocol_sha256(protocol)
    if run_manifest.get("publication_protocol_sha256") != protocol_sha256:
        raise ValueError("run manifest does not match the publication protocol")
    task_ids = [str(item["task_id"]) for item in protocol["tasks"]]
    method_ids = [str(item["method_id"]) for item in protocol["methods"]]
    seeds = [int(seed) for seed in protocol["experimental_design"]["seeds"]]
    complete_experiments = int(
        protocol["experimental_design"]["complete_experiments_per_task_seed"]
    )
    expected = Counter(
        (task, method, seed)
        for task in task_ids
        for method in method_ids
        for seed in seeds
    )
    actual = Counter(
        (str(row.get("task_id")), str(row.get("baseline_agent")), int(row.get("seed", -1)))
        for row in results
    )
    if actual != expected:
        raise ValueError("formal result matrix has missing, extra, or duplicate cells")
    for row in results:
        if row.get("publication_protocol_sha256") != protocol_sha256:
            raise ValueError("result row has publication protocol drift")
        if row.get("evaluated_source_commit") != run_manifest.get("evaluated_source_commit"):
            raise ValueError("result row has source commit drift")
        if row.get("evaluation_source_tree_dirty") is not False:
            raise ValueError("result row was evaluated from a dirty source tree")
        usage = row.get("resource_usage", {})
        if usage.get("complete_experiment_count") != complete_experiments:
            raise ValueError("result row does not contain the frozen experiment count")
        if row.get("verified") is not True:
            raise ValueError("result row is not replay verified")


def _method_summaries(
    task_results: Sequence[dict[str, Any]],
    *,
    primary_field: str,
) -> dict[str, dict[str, float]]:
    methods = sorted({str(row["baseline_agent"]) for row in task_results})
    summaries: dict[str, dict[str, float]] = {}
    for method in methods:
        rows = [row for row in task_results if row["baseline_agent"] == method]
        summaries[method] = {
            "mean_total_score": fmean(float(row["total_score"]) for row in rows),
            "mean_primary_metric": fmean(float(row[primary_field]) for row in rows),
            "mean_safety_aware_score": fmean(
                float(row["safety_aware_score"]) for row in rows
            ),
            "mean_cost_aware_score": fmean(float(row["cost_aware_score"]) for row in rows),
            "mean_safety_risk": fmean(float(row.get("mean_risk", 0.0)) for row in rows),
            "mean_safety_violations": fmean(
                float(row.get("safety_violations", 0.0)) for row in rows
            ),
            "mean_high_cost_violations": fmean(
                float(row.get("high_cost_violations", 0.0)) for row in rows
            ),
            "mean_run_wall_time_s": fmean(
                float(row["resource_usage"]["run_wall_time_s"]) for row in rows
            ),
            "mean_process_cpu_time_s": fmean(
                float(row["resource_usage"]["process_cpu_time_s"]) for row in rows
            ),
        }
    return summaries


__all__ = [
    "PUBLICATION_COMPARISONS",
    "PUBLICATION_EVIDENCE_SCHEMA_VERSION",
    "build_publication_evidence_summary",
    "payload_sha256",
]
