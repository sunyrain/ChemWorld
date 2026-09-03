#!/usr/bin/env python3
"""Combine terminal DeepSeek and Codex W2-61 four-condition evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = (
    "no_evidence",
    "yoked_evidence",
    "autonomous_exploration",
    "learned_law_only",
)
CONTRASTS = (
    ("autonomous_exploration", "no_evidence"),
    ("yoked_evidence", "no_evidence"),
    ("learned_law_only", "no_evidence"),
    ("autonomous_exploration", "yoked_evidence"),
)
ORIGINAL_ROOTS = {
    "deepseek": ROOT
    / "runs/development/"
    "work-ii-w2-61-deepseek-action-aligned-recipients-v0.1-20260902",
    "codex": ROOT
    / "runs/development/"
    "work-ii-w2-61-codex-action-aligned-recipients-v0.1-20260902-restart2",
}
RECOVERY_ROOTS = {
    participant: ROOT
    / "runs/development/"
    / f"work-ii-w2-61-{participant}-yoked-recovery-v0.1-20260902"
    for participant in ("deepseek", "codex")
}
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-61-cross-model-action-aligned-causal-extension-v0.1.json"
)
BOOTSTRAP_SEED = 20260902
BOOTSTRAP_REPLICATES = 10_000
COMPLETED_STATUSES = frozenset({"completed", "completed_uncontaminated"})


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_summary(path: Path, *, expected_status: str = "terminal_complete") -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"required terminal summary is missing: {path}")
    payload = _load(path)
    if payload.get("status") != expected_status:
        raise ValueError(f"summary is not {expected_status}: {path}")
    embedded = payload.get("summary_sha256")
    without_hash = {key: value for key, value in payload.items() if key != "summary_sha256"}
    if embedded != canonical_json_sha256(without_hash):
        raise ValueError(f"summary self-hash drifted: {path}")
    return payload


def _mean(values: Sequence[float]) -> float | None:
    return statistics.fmean(values) if values else None


def _quantile(values: Sequence[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(float(value) for value in values)
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _flat_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    regret = [float(row["failure_aware_normalized_regret"]) for row in rows]
    ranks = [float(row["selected_rank"]) for row in rows if row.get("selected_rank") is not None]
    pairwise = [
        float(row["pairwise_ranking_agreement_excluding_truth_gaps_below_0_01"])
        for row in rows
        if row.get("pairwise_ranking_agreement_excluding_truth_gaps_below_0_01")
        is not None
    ]
    return {
        "row_count": len(rows),
        "completed_count": sum(str(row["status"]) in COMPLETED_STATUSES for row in rows),
        "failed_blocked_or_incomplete_count": sum(
            str(row["status"]) not in COMPLETED_STATUSES for row in rows
        ),
        "scored_ranking_count": len(ranks),
        "status_counts": dict(sorted(Counter(str(row["status"]) for row in rows).items())),
        "mean_failure_aware_normalized_regret": _mean(regret),
        "mean_selected_rank_scored": _mean(ranks),
        "top1_count": sum(int(row["top1"]) for row in rows),
        "top1_rate": _mean([float(row["top1"]) for row in rows]),
        "within_0_01_count": sum(int(row["within_0_01_of_best"]) for row in rows),
        "within_0_01_rate": _mean(
            [float(row["within_0_01_of_best"]) for row in rows]
        ),
        "mean_near_tie_aware_pairwise_agreement_scored": _mean(pairwise),
    }


def _population_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        **_flat_summary(rows),
        "by_task": {
            task_id: _flat_summary([row for row in rows if row["task_id"] == task_id])
            for task_id in sorted({str(row["task_id"]) for row in rows})
        },
        "by_prior_arm": {
            prior_arm: _flat_summary(
                [row for row in rows if row["prior_arm"] == prior_arm]
            )
            for prior_arm in sorted({str(row["prior_arm"]) for row in rows})
        },
    }


def _cluster_bootstrap_interval(
    records: Sequence[Mapping[str, Any]],
    *,
    value_key: str,
    seed_label: str,
) -> list[float | None]:
    by_task_cluster: dict[str, dict[str, list[Mapping[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for record in records:
        by_task_cluster[str(record["task_id"])][str(record["cluster_id"])].append(record)
    if not by_task_cluster:
        return [None, None]
    rng = random.Random(f"{BOOTSTRAP_SEED}:{seed_label}")
    estimates: list[float] = []
    for _ in range(BOOTSTRAP_REPLICATES):
        sampled: list[Mapping[str, Any]] = []
        for task_id in sorted(by_task_cluster):
            clusters = by_task_cluster[task_id]
            cluster_ids = sorted(clusters)
            for cluster_id in rng.choices(cluster_ids, k=len(cluster_ids)):
                sampled.extend(clusters[cluster_id])
        estimates.append(statistics.fmean(float(row[value_key]) for row in sampled))
    return [_quantile(estimates, 0.025), _quantile(estimates, 0.975)]


def _paired_condition_contrast(
    rows: Sequence[Mapping[str, Any]],
    *,
    treatment: str,
    control: str,
    population: str,
) -> dict[str, Any]:
    by_stratum: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_stratum[str(row["stratum_id"])][str(row["condition"])] = row
    pairs: list[dict[str, Any]] = []
    for stratum_id, condition_rows in sorted(by_stratum.items()):
        if treatment not in condition_rows or control not in condition_rows:
            continue
        treatment_row = condition_rows[treatment]
        control_row = condition_rows[control]
        pairs.append(
            {
                "stratum_id": stratum_id,
                "cluster_id": str(treatment_row["cluster_id"]),
                "task_id": str(treatment_row["task_id"]),
                "prior_arm": str(treatment_row["prior_arm"]),
                "regret_difference": float(
                    treatment_row["failure_aware_normalized_regret"]
                )
                - float(control_row["failure_aware_normalized_regret"]),
                "top1_difference": int(treatment_row["top1"])
                - int(control_row["top1"]),
                "within_0_01_difference": int(treatment_row["within_0_01_of_best"])
                - int(control_row["within_0_01_of_best"]),
            }
        )
    regret = [float(pair["regret_difference"]) for pair in pairs]
    return {
        "contrast": f"{treatment}_minus_{control}",
        "population": population,
        "negative_regret_difference_favors": treatment,
        "paired_stratum_count": len(pairs),
        "task_world_cluster_count": len({str(pair["cluster_id"]) for pair in pairs}),
        "mean_failure_aware_normalized_regret_difference": _mean(regret),
        "task_stratified_task_world_cluster_bootstrap_95_interval": (
            _cluster_bootstrap_interval(
                pairs,
                value_key="regret_difference",
                seed_label=f"{population}:{treatment}:{control}",
            )
        ),
        "mean_top1_difference": _mean(
            [float(pair["top1_difference"]) for pair in pairs]
        ),
        "mean_within_0_01_difference": _mean(
            [float(pair["within_0_01_difference"]) for pair in pairs]
        ),
        "wins_ties_losses_on_regret": {
            "wins": sum(value < 0.0 for value in regret),
            "ties": sum(value == 0.0 for value in regret),
            "losses": sum(value > 0.0 for value in regret),
        },
        "by_task": {
            task_id: {
                "paired_stratum_count": len(task_pairs),
                "mean_regret_difference": _mean(
                    [float(pair["regret_difference"]) for pair in task_pairs]
                ),
            }
            for task_id in sorted({str(pair["task_id"]) for pair in pairs})
            for task_pairs in [[pair for pair in pairs if pair["task_id"] == task_id]]
        },
        "by_prior_arm": {
            prior_arm: {
                "paired_stratum_count": len(arm_pairs),
                "mean_regret_difference": _mean(
                    [float(pair["regret_difference"]) for pair in arm_pairs]
                ),
            }
            for prior_arm in sorted({str(pair["prior_arm"]) for pair in pairs})
            for arm_pairs in [[pair for pair in pairs if pair["prior_arm"] == prior_arm]]
        },
    }


def _merge_model_rows(
    *,
    participant: str,
    original: Mapping[str, Any],
    recovery: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    original_rows = [deepcopy(dict(row)) for row in original["condition_rows"]]
    if len(original_rows) != 180:
        raise ValueError(f"{participant}: original four-condition denominator drifted")
    by_key = {
        (str(row["stratum_id"]), str(row["condition"])): row for row in original_rows
    }
    if len(by_key) != 180:
        raise ValueError(f"{participant}: original condition rows are not unique")
    incident_rows = [
        deepcopy(row) for row in original_rows if row["condition"] == "yoked_evidence"
    ]
    recovery_rows = [deepcopy(dict(row)) for row in recovery["condition_rows"]]
    expected_recovery = int(recovery["denominators"]["admitted_yoked_recovery_sessions"])
    if len(recovery_rows) != expected_recovery:
        raise ValueError(f"{participant}: recovery yoked denominator drifted")
    for row in recovery_rows:
        if row.get("condition") != "yoked_evidence" or not row.get("admitted_stratum"):
            raise ValueError(f"{participant}: recovery contains an out-of-scope row")
        key = (str(row["stratum_id"]), "yoked_evidence")
        if key not in by_key:
            raise ValueError(f"{participant}: recovery stratum is outside the original design")
        prior = by_key[key]
        row["source"] = "new_w2_61_yoked_recovery_primary"
        row["superseded_platform_incident_status"] = prior["status"]
        by_key[key] = row
    merged = [by_key[key] for key in sorted(by_key)]
    if len(merged) != 180:
        raise ValueError(f"{participant}: combined four-condition denominator drifted")
    return merged, incident_rows


def _model_analysis(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    scheduled_rows = list(rows)
    admitted_rows = [row for row in rows if row["admitted_stratum"]]
    return {
        "scheduled_failure_aware": {
            "condition_summaries": {
                condition: _population_summary(
                    [row for row in scheduled_rows if row["condition"] == condition]
                )
                for condition in CONDITIONS
            },
            "contrasts": [
                _paired_condition_contrast(
                    scheduled_rows,
                    treatment=treatment,
                    control=control,
                    population="all_45_scheduled_strata",
                )
                for treatment, control in CONTRASTS
            ],
        },
        "donor_eligible": {
            "stratum_count": len({str(row["stratum_id"]) for row in admitted_rows}),
            "condition_summaries": {
                condition: _population_summary(
                    [row for row in admitted_rows if row["condition"] == condition]
                )
                for condition in CONDITIONS
            },
            "contrasts": [
                _paired_condition_contrast(
                    admitted_rows,
                    treatment=treatment,
                    control=control,
                    population="model_specific_donor_eligible_strata",
                )
                for treatment, control in CONTRASTS
            ],
        },
    }


def _cross_model_common_analysis(
    model_rows: Mapping[str, Sequence[Mapping[str, Any]]]
) -> dict[str, Any]:
    eligible = {
        participant: {
            str(row["stratum_id"])
            for row in rows
            if row["admitted_stratum"]
        }
        for participant, rows in model_rows.items()
    }
    common_ids = set.intersection(*eligible.values())
    common_rows = {
        participant: [row for row in rows if row["stratum_id"] in common_ids]
        for participant, rows in model_rows.items()
    }
    by_model_condition = {
        participant: {
            condition: {
                str(row["stratum_id"]): row
                for row in rows
                if row["condition"] == condition
            }
            for condition in CONDITIONS
        }
        for participant, rows in common_rows.items()
    }
    condition_differences: list[dict[str, Any]] = []
    for condition in CONDITIONS:
        records: list[dict[str, Any]] = []
        for stratum_id in sorted(common_ids):
            deepseek = by_model_condition["deepseek"][condition][stratum_id]
            codex = by_model_condition["codex"][condition][stratum_id]
            records.append(
                {
                    "stratum_id": stratum_id,
                    "cluster_id": str(deepseek["cluster_id"]),
                    "task_id": str(deepseek["task_id"]),
                    "prior_arm": str(deepseek["prior_arm"]),
                    "codex_minus_deepseek_regret": float(
                        codex["failure_aware_normalized_regret"]
                    )
                    - float(deepseek["failure_aware_normalized_regret"]),
                }
            )
        condition_differences.append(
            {
                "condition": condition,
                "paired_stratum_count": len(records),
                "negative_difference_favors": "codex",
                "mean_codex_minus_deepseek_failure_aware_regret": _mean(
                    [float(row["codex_minus_deepseek_regret"]) for row in records]
                ),
                "task_stratified_task_world_cluster_bootstrap_95_interval": (
                    _cluster_bootstrap_interval(
                        records,
                        value_key="codex_minus_deepseek_regret",
                        seed_label=f"cross-model:{condition}",
                    )
                ),
            }
        )

    difference_in_contrasts: list[dict[str, Any]] = []
    for treatment, control in CONTRASTS:
        records = []
        for stratum_id in sorted(common_ids):
            deep_t = by_model_condition["deepseek"][treatment][stratum_id]
            deep_c = by_model_condition["deepseek"][control][stratum_id]
            codex_t = by_model_condition["codex"][treatment][stratum_id]
            codex_c = by_model_condition["codex"][control][stratum_id]
            records.append(
                {
                    "stratum_id": stratum_id,
                    "cluster_id": str(deep_t["cluster_id"]),
                    "task_id": str(deep_t["task_id"]),
                    "prior_arm": str(deep_t["prior_arm"]),
                    "codex_minus_deepseek_difference_in_contrast": (
                        float(codex_t["failure_aware_normalized_regret"])
                        - float(codex_c["failure_aware_normalized_regret"])
                        - float(deep_t["failure_aware_normalized_regret"])
                        + float(deep_c["failure_aware_normalized_regret"])
                    ),
                }
            )
        difference_in_contrasts.append(
            {
                "contrast": f"{treatment}_minus_{control}",
                "paired_stratum_count": len(records),
                "mean_codex_minus_deepseek_difference_in_contrast": _mean(
                    [
                        float(row["codex_minus_deepseek_difference_in_contrast"])
                        for row in records
                    ]
                ),
                "task_stratified_task_world_cluster_bootstrap_95_interval": (
                    _cluster_bootstrap_interval(
                        records,
                        value_key="codex_minus_deepseek_difference_in_contrast",
                        seed_label=f"cross-model-contrast:{treatment}:{control}",
                    )
                ),
            }
        )
    return {
        "common_eligible_stratum_count": len(common_ids),
        "common_eligible_task_world_cluster_count": len(
            {
                str(row["cluster_id"])
                for row in common_rows["deepseek"]
                if row["condition"] == "no_evidence"
            }
        ),
        "common_stratum_ids": sorted(common_ids),
        "condition_summaries_by_model": {
            participant: {
                condition: _population_summary(
                    [row for row in rows if row["condition"] == condition]
                )
                for condition in CONDITIONS
            }
            for participant, rows in common_rows.items()
        },
        "within_model_contrasts_on_common_strata": {
            participant: [
                _paired_condition_contrast(
                    rows,
                    treatment=treatment,
                    control=control,
                    population="cross_model_common_eligible_strata",
                )
                for treatment, control in CONTRASTS
            ]
            for participant, rows in common_rows.items()
        },
        "cross_model_condition_differences": condition_differences,
        "cross_model_differences_in_causal_contrasts": difference_in_contrasts,
    }


def _turn_ledger(root: Path, *, include_conditions: set[str] | None = None) -> dict[str, Any]:
    usage: Counter[str] = Counter()
    condition_counts: Counter[str] = Counter()
    thread_ids: set[str] = set()
    tool_events = 0
    provider_errors = 0
    selected_files = []
    for path in sorted((root / "provider-turns").glob("**/turn-*.json")):
        payload = _load(path)
        receipt = payload.get("receipt")
        receipt = receipt if isinstance(receipt, Mapping) else {}
        condition = str(receipt.get("condition", "unknown"))
        if include_conditions is not None and condition not in include_conditions:
            continue
        selected_files.append(path)
        condition_counts[condition] += 1
        thread_id = receipt.get("thread_id")
        if isinstance(thread_id, str):
            thread_ids.add(thread_id)
        tool_events += int(receipt.get("tool_event_count", 0) or 0)
        errors = receipt.get("provider_errors")
        provider_errors += len(errors) if isinstance(errors, list) else 0
        turn_usage = receipt.get("usage")
        if isinstance(turn_usage, Mapping):
            for key, value in turn_usage.items():
                if isinstance(value, int) and not isinstance(value, bool):
                    usage[str(key)] += value
    return {
        "provider_turn_record_count": len(selected_files),
        "turn_count_by_condition": dict(sorted(condition_counts.items())),
        "unique_thread_count": len(thread_ids),
        "tool_event_count": tool_events,
        "provider_error_event_count": provider_errors,
        "usage": dict(sorted(usage.items())),
    }


def _failure_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            key: deepcopy(row.get(key))
            for key in (
                "stratum_id",
                "cluster_id",
                "task_id",
                "world_seed",
                "prior_arm",
                "condition",
                "status",
                "source",
                "admitted_stratum",
                "provider_call_count",
                "failure_aware_normalized_regret",
            )
        }
        for row in rows
        if str(row["status"]) not in COMPLETED_STATUSES
    ]


def build_combined_summary() -> dict[str, Any]:
    originals: dict[str, dict[str, Any]] = {}
    recoveries: dict[str, dict[str, Any]] = {}
    model_rows: dict[str, list[dict[str, Any]]] = {}
    incident_rows: dict[str, list[dict[str, Any]]] = {}
    source_bindings: dict[str, Any] = {}
    for participant in ("deepseek", "codex"):
        original_path = ORIGINAL_ROOTS[participant] / "summary.json"
        recovery_path = RECOVERY_ROOTS[participant] / "summary.json"
        originals[participant] = _validate_summary(original_path)
        recoveries[participant] = _validate_summary(recovery_path)
        merged, incident = _merge_model_rows(
            participant=participant,
            original=originals[participant],
            recovery=recoveries[participant],
        )
        model_rows[participant] = merged
        incident_rows[participant] = incident
        source_bindings[participant] = {
            "original_summary": str(original_path.relative_to(ROOT)).replace("\\", "/"),
            "original_summary_sha256": _sha256_file(original_path),
            "recovery_summary": str(recovery_path.relative_to(ROOT)).replace("\\", "/"),
            "recovery_summary_sha256": _sha256_file(recovery_path),
            "donor_source": deepcopy(dict(originals[participant]["source_binding"])),
        }

    all_rows = [
        {"participant": participant, **deepcopy(row)}
        for participant, rows in model_rows.items()
        for row in rows
    ]
    if len(all_rows) != 360:
        raise ValueError("cross-model scheduled condition-slot denominator drifted")
    primary_recipient_ledgers = {
        participant: {
            "original_no_evidence_and_learned_law": _turn_ledger(
                ORIGINAL_ROOTS[participant],
                include_conditions={"no_evidence", "learned_law_only"},
            ),
            "recovered_yoked": _turn_ledger(
                RECOVERY_ROOTS[participant], include_conditions={"yoked_evidence"}
            ),
            "retained_platform_incident_yoked": _turn_ledger(
                ORIGINAL_ROOTS[participant], include_conditions={"yoked_evidence"}
            ),
        }
        for participant in ("deepseek", "codex")
    }
    donor_summaries = {
        participant: _load(ROOT / str(originals[participant]["source_binding"]["summary"]))
        for participant in ("deepseek", "codex")
    }
    payload = {
        "schema_version": "chemworld-work-ii-w2-61-cross-model-combined-0.1",
        "study_id": "work-ii-w2-61-cross-model-action-aligned-causal-extension-v0.1",
        "formal_result": False,
        "prospective_development_experiment": True,
        "status": "terminal_complete",
        "models": {
            "deepseek": {
                "model": originals["deepseek"]["model"],
                "reasoning_effort": originals["deepseek"]["reasoning_effort"],
            },
            "codex": {
                "model": originals["codex"]["model"],
                "reasoning_effort": originals["codex"]["reasoning_effort"],
            },
        },
        "denominators": {
            "models": 2,
            "scheduled_strata_per_model": 45,
            "conditions_per_stratum": 4,
            "scheduled_condition_slots_per_model": 180,
            "scheduled_condition_slots_total": 360,
            "deepseek_donor_eligible_strata": sum(
                row["admitted_stratum"]
                for row in model_rows["deepseek"]
                if row["condition"] == "no_evidence"
            ),
            "codex_donor_eligible_strata": sum(
                row["admitted_stratum"]
                for row in model_rows["codex"]
                if row["condition"] == "no_evidence"
            ),
            "new_truth_executions": 0,
            "new_physical_experiments_in_recipient_and_recovery_blocks": 0,
            "deepseek_autonomous_donor_physical_experiments": int(
                donor_summaries["deepseek"]["participant_physical_experiment_count"]
            ),
            "codex_autonomous_donor_physical_experiments": int(
                donor_summaries["codex"]["participant_physical_experiment_count"]
            ),
        },
        "primary_analysis_rule": {
            "no_evidence_learned_law_and_autonomous": "retained original W2-61 rows",
            "yoked_evidence": "full-condition recovery rows",
            "original_yoked_rows": "retained platform-incident sensitivity only",
            "failure_aware_regret_for_missing_ranking": 1.0,
            "oracle_condition_included": False,
        },
        "per_model": {
            participant: _model_analysis(rows)
            for participant, rows in model_rows.items()
        },
        "cross_model_common_eligible": _cross_model_common_analysis(model_rows),
        "platform_incident_sensitivity": {
            participant: {
                "interpretation": "not a participant-capability estimate",
                "scheduled_yoked": _population_summary(rows),
                "admitted_yoked": _population_summary(
                    [row for row in rows if row["admitted_stratum"]]
                ),
                "category_value_key_error_count": int(
                    recoveries[participant]["source_incident"][
                        "category_value_key_error_count"
                    ]
                ),
            }
            for participant, rows in incident_rows.items()
        },
        "resource_ledger": {
            "primary_recipient_turns": primary_recipient_ledgers,
            "autonomous_donors": {
                participant: {
                    "scheduled_sessions": int(summary["scheduled_cell_count"]),
                    "eligible_sessions": int(summary["eligible_cell_count"]),
                    "retained_failures": int(summary["failed_or_ineligible_cell_count"]),
                    "participant_physical_experiments": int(
                        summary["participant_physical_experiment_count"]
                    ),
                }
                for participant, summary in donor_summaries.items()
            },
            "tools_authorized_in_recipient_blocks": 0,
            "new_truth_executions": 0,
        },
        "failure_records_primary_360_slots": _failure_rows(all_rows),
        "bootstrap": {
            "unit": "task_world_cluster_with_prior_arms_as_repeated_factors",
            "task_stratified": True,
            "replicates": BOOTSTRAP_REPLICATES,
            "seed": BOOTSTRAP_SEED,
        },
        "source_bindings": source_bindings,
        "condition_rows": all_rows,
    }
    payload["summary_sha256"] = canonical_json_sha256(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    payload = build_combined_summary()
    write_json_atomic(output, payload)
    print(json.dumps(payload["denominators"], ensure_ascii=False, sort_keys=True))
    print(payload["summary_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
