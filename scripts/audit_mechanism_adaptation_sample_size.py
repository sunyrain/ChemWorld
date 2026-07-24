"""Audit independent-cluster sample size before A2/A3 execution."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Callable
from pathlib import Path
from statistics import NormalDist
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from chemworld.eval.mechanism_adaptation import (  # noqa: E402
    load_mechanism_adaptation_protocol,
    wilson_interval,
)
from chemworld.eval.provenance import (  # noqa: E402
    canonical_json_sha256,
    write_json_atomic,
)

DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0.json"
)
DEFAULT_PLAN = (
    ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "mechanism-adaptation-sample-size-audit-v0.3.0-rc24.json"
)


def _binomial_probability(n: int, k: int, probability: float) -> float:
    return (
        math.comb(n, k)
        * probability**k
        * (1.0 - probability) ** (n - k)
    )


def _binomial_quantile(n: int, probability: float, quantile: float) -> int:
    cumulative = 0.0
    for k in range(n + 1):
        cumulative += _binomial_probability(n, k, probability)
        if cumulative >= quantile - 1e-15:
            return k
    return n


def _binary_cluster_bootstrap_interval(
    hits: int,
    n: int,
    *,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Exact percentile limit for resampling independent binary clusters."""

    empirical = hits / n
    tail = (1.0 - confidence) / 2.0
    return (
        _binomial_quantile(n, empirical, tail) / n,
        _binomial_quantile(n, empirical, 1.0 - tail) / n,
    )


def _pass_probability(
    *,
    n: int,
    true_probability: float,
    passes: Callable[[int, int], bool],
) -> float:
    return sum(
        _binomial_probability(n, hits, true_probability)
        for hits in range(n + 1)
        if passes(hits, n)
    )


def _auc_half_width(
    *,
    clusters_per_class: int,
    auc: float,
    confidence: float = 0.95,
) -> float:
    """Hanley--McNeil planning approximation; not used for gate inference."""

    q1 = auc / (2.0 - auc)
    q2 = 2.0 * auc**2 / (1.0 + auc)
    variance = (
        auc * (1.0 - auc)
        + (clusters_per_class - 1) * (q1 - auc**2)
        + (clusters_per_class - 1) * (q2 - auc**2)
    ) / clusters_per_class**2
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    return z * math.sqrt(max(variance, 0.0))


def build_sample_size_audit(
    protocol: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    requirement = plan["online_attainability_certificate"]
    criteria = requirement["frozen_pass_criteria"]
    selected_n = int(requirement["world_seeds_per_family"])
    confidence = float(criteria["confidence_level"])
    reference_threshold = float(
        criteria["minimum_reference_acquisition_rate_wilson_lower_bound"]
    )
    recall_threshold = float(
        criteria[
            "minimum_changed_detection_recall_cluster_bootstrap_lower_bound"
        ]
    )
    fpr_threshold = float(
        criteria[
            "maximum_no_change_false_positive_rate_cluster_bootstrap_upper_bound"
        ]
    )
    candidate_cluster_counts = [30, 60, 100, 120, 180]
    planning_rows: list[dict[str, Any]] = []
    for n in candidate_cluster_counts:
        reference_power = {
            str(probability): _pass_probability(
                n=n,
                true_probability=probability,
                passes=lambda hits, count: (
                    wilson_interval(
                        hits,
                        count,
                        confidence=confidence,
                    )[0]
                    >= reference_threshold
                ),
            )
            for probability in (0.85, 0.9)
        }
        recall_power = {
            str(probability): _pass_probability(
                n=n,
                true_probability=probability,
                passes=lambda hits, count: (
                    _binary_cluster_bootstrap_interval(
                        hits,
                        count,
                        confidence=confidence,
                    )[0]
                    >= recall_threshold
                ),
            )
            for probability in (0.85, 0.9)
        }
        fpr_power = {
            str(probability): _pass_probability(
                n=n,
                true_probability=probability,
                passes=lambda hits, count: (
                    _binary_cluster_bootstrap_interval(
                        hits,
                        count,
                        confidence=confidence,
                    )[1]
                    <= fpr_threshold
                ),
            )
            for probability in (0.05, 0.1)
        }
        planning_rows.append(
            {
                "independent_world_clusters_per_family": n,
                "reference_wilson_pass_probability": reference_power,
                "changed_recall_cluster_bootstrap_pass_probability": (
                    recall_power
                ),
                "no_change_fpr_cluster_bootstrap_pass_probability": fpr_power,
                "zero_false_alarm_wilson_upper_bound": wilson_interval(
                    0,
                    n,
                    confidence=confidence,
                )[1],
                "auroc_planning_half_width": {
                    str(auc): _auc_half_width(
                        clusters_per_class=n,
                        auc=auc,
                        confidence=confidence,
                    )
                    for auc in (0.8, 0.85)
                },
            }
        )
    selected = next(
        row
        for row in planning_rows
        if row["independent_world_clusters_per_family"] == selected_n
    )
    numeric_change_times = [
        int(item)
        for item in requirement["truth_change_time_support"]
        if item != "never"
    ]
    changed_families_by_task = {
        task_id: [
            candidate_id
            for candidate_id in contract["candidate_ids"]
            if candidate_id != "no_change"
        ]
        for task_id, contract in protocol["task_mechanism_contracts"].items()
    }
    checks = {
        "selected_cluster_count_matches_all_a2_a3_private_declarations": (
            selected_n
            == int(plan["held_out_certificate"]["world_seeds_per_family"])
            == int(
                plan["cohort_partition"]["a2_certification"][
                    "world_seeds_per_family"
                ]
            )
            == int(
                plan["cohort_partition"]["a3_certification"][
                    "world_seeds_per_family"
                ]
            )
            == int(
                plan["cohort_partition"]["private_confirmation"][
                    "world_seeds_per_family"
                ]
            )
        ),
        "balanced_changepoint_allocation_is_exact": (
            selected_n % len(numeric_change_times) == 0
        ),
        "power_at_true_reference_success_0_90_is_at_least_0_80": (
            selected["reference_wilson_pass_probability"]["0.9"] >= 0.8
        ),
        "power_at_true_changed_recall_0_90_is_at_least_0_80": (
            selected[
                "changed_recall_cluster_bootstrap_pass_probability"
            ]["0.9"]
            >= 0.8
        ),
        "power_at_true_fpr_0_05_is_at_least_0_80": (
            selected[
                "no_change_fpr_cluster_bootstrap_pass_probability"
            ]["0.05"]
            >= 0.8
        ),
        "provider_repeats_are_nested_not_independent_clusters": (
            protocol["design"]["provider_repeats_per_paired_cell"] == 5
            and protocol["reporting"]["provider_repeats"]
            == "nested_technical_replicates"
        ),
    }
    passed = all(checks.values())
    report: dict[str, Any] = {
        "schema_version": "chemworld-mechanism-sample-size-audit-0.1",
        "status": "passed" if passed else "failed",
        "pass": passed,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_json_sha256(protocol),
        "gate_a_plan_id": plan["plan_id"],
        "gate_a_plan_sha256": canonical_json_sha256(plan),
        "statistical_unit": "task_id_and_world_seed_cluster",
        "provider_repeat_role": "nested_technical_replicate",
        "selected_independent_world_clusters_per_family": selected_n,
        "changed_families_by_task": changed_families_by_task,
        "no_change_clusters_per_task": selected_n,
        "change_time_support": numeric_change_times,
        "clusters_per_changed_family_per_change_time": (
            selected_n // len(numeric_change_times)
        ),
        "provider_repeats_per_paired_cell": protocol["design"][
            "provider_repeats_per_paired_cell"
        ],
        "planning_method": {
            "reference": "exact binomial power against Wilson lower bound",
            "binary_cluster_metrics": (
                "exact binomial power against the percentile interval induced "
                "by resampling independent binary world clusters"
            ),
            "auroc": (
                "Hanley-McNeil half-width approximation for planning only; "
                "formal inference remains the frozen cluster bootstrap"
            ),
        },
        "planning_rows": planning_rows,
        "selected_design": selected,
        "checks": checks,
        "limitations": [
            (
                "Power at a true reference success rate of 0.85 remains "
                "substantially lower because 0.85 is close to the frozen 0.80 "
                "confidence-bound threshold."
            ),
            (
                "The audit assesses independent world clusters, not the much "
                "larger number of experiment arms or provider completions."
            ),
        ],
    }
    report["audit_sha256"] = canonical_json_sha256(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    protocol = load_mechanism_adaptation_protocol(args.protocol)
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    report = build_sample_size_audit(protocol, plan)
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"missing sample-size audit: {args.output}")
        recorded = json.loads(args.output.read_text(encoding="utf-8"))
        if recorded != report:
            raise SystemExit("mechanism-adaptation sample-size audit is stale")
    else:
        write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "selected_clusters_per_family": (
                    report["selected_independent_world_clusters_per_family"]
                ),
                "output": str(args.output.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
