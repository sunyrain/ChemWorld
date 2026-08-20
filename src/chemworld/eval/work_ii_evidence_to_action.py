"""Design compiler for the Work II evidence-to-action causal decomposition.

This module is deliberately provider-free.  It validates the five-condition contract and builds
the dependency-aware scheduled denominator; provider execution belongs to a later runtime layer.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any

import numpy as np

from chemworld.eval.work_ii_prior_discovery import parse_work_ii_law_summary

PROTOCOL_SCHEMA = "chemworld-work-ii-evidence-to-action-protocol-0.1"
MANIFEST_SCHEMA = "chemworld-work-ii-evidence-to-action-design-manifest-0.1"
PRIOR_ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
CONDITIONS = (
    "no_evidence",
    "yoked_evidence",
    "autonomous_exploration",
    "learned_law_only",
    "oracle_law",
)
DONOR_CONDITION = "autonomous_exploration"
DONOR_DERIVED_CONDITIONS = ("yoked_evidence", "learned_law_only")
YOKED_CHECKPOINTS = (3, 6, 9, 12)
CONDITION_STAGES = {
    "no_evidence": ("terminal_ranking",),
    "yoked_evidence": (
        "pre_evidence",
        "after_experiment_3",
        "after_experiment_6",
        "after_experiment_9",
        "final",
        "terminal_ranking",
    ),
    "autonomous_exploration": (
        "pre_evidence",
        "after_experiment_3",
        "after_experiment_6",
        "after_experiment_9",
        "final",
        "terminal_ranking",
    ),
    "learned_law_only": ("artifact_received", "terminal_ranking"),
    "oracle_law": ("artifact_received", "terminal_ranking"),
}
CANDIDATE_REVEAL_GATES = {
    "no_evidence": "session_start",
    "yoked_evidence": "after_evidence_round_12",
    "autonomous_exploration": "after_experiment_12_final_checkpoint",
    "learned_law_only": "session_start_with_artifact",
    "oracle_law": "session_start_with_artifact",
}
PRESPECIFIED_CONTRASTS = (
    ("autonomous_exploration", "no_evidence"),
    ("yoked_evidence", "no_evidence"),
    ("autonomous_exploration", "yoked_evidence"),
    ("learned_law_only", "no_evidence"),
    ("oracle_law", "learned_law_only"),
    ("oracle_law", "no_evidence"),
)
_HALTON_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [str(item) for item in value]


def validate_protocol(protocol: Mapping[str, Any]) -> list[str]:
    """Return all design-contract errors without mutating the protocol."""

    errors: list[str] = []
    if protocol.get("schema_version") != PROTOCOL_SCHEMA:
        errors.append("unexpected protocol schema")
    if protocol.get("status") != "development_design_provider_execution_not_authorized":
        errors.append("design must remain provider-unauthorized")

    tasks = protocol.get("task_runtime_sources")
    if not isinstance(tasks, Mapping) or len(tasks) != 3:
        errors.append("exactly three task runtime sources are required")
    elif any(not str(path).endswith(".json") for path in tasks.values()):
        errors.append("every task runtime source must be a JSON path")

    qualification_worlds = protocol.get("qualification_world_seeds")
    formal_worlds = protocol.get("formal_world_seeds")
    if not isinstance(qualification_worlds, list) or len(set(qualification_worlds)) != 5:
        errors.append("exactly five unique qualification worlds are required")
    if not isinstance(formal_worlds, list) or len(set(formal_worlds)) != 5:
        errors.append("exactly five unique formal worlds are required")
    if (
        isinstance(qualification_worlds, list)
        and isinstance(formal_worlds, list)
        and set(qualification_worlds) & set(formal_worlds)
    ):
        errors.append("qualification and formal worlds must be disjoint")

    if tuple(_string_list(protocol.get("prior_arms"))) != PRIOR_ARMS:
        errors.append("prior arms differ from the frozen triarm contract")

    conditions = protocol.get("conditions")
    if not isinstance(conditions, Mapping) or tuple(conditions) != CONDITIONS:
        errors.append("five information conditions or their order differ from the contract")
    else:
        for condition in CONDITIONS:
            row = conditions.get(condition)
            if not isinstance(row, Mapping):
                errors.append(f"{condition}: condition record is missing")
                continue
            expected_physical = 12 if condition == DONOR_CONDITION else 0
            if row.get("physical_experiments") != expected_physical:
                errors.append(f"{condition}: physical experiment count is invalid")
            if row.get("fresh_context") is not True:
                errors.append(f"{condition}: fresh context is required")
            expected_dependency = condition in DONOR_DERIVED_CONDITIONS
            if row.get("donor_dependency") is not expected_dependency:
                errors.append(f"{condition}: donor dependency is invalid")
            if tuple(_string_list(row.get("checkpoint_stages"))) != CONDITION_STAGES[condition]:
                errors.append(f"{condition}: checkpoint stages differ from the condition contract")

    donor = protocol.get("donor_contract")
    if not isinstance(donor, Mapping):
        errors.append("donor contract is missing")
    else:
        if donor.get("condition") != DONOR_CONDITION:
            errors.append("autonomous exploration must be the donor")
        if tuple(_string_list(donor.get("derived_conditions"))) != DONOR_DERIVED_CONDITIONS:
            errors.append("donor-derived conditions differ from the contract")
        for forbidden in (
            "transfer_donor_reasoning",
            "transfer_hidden_evaluator_fields",
            "transfer_candidate_information",
            "replacement_donor_allowed",
        ):
            if donor.get(forbidden) is not False:
                errors.append(f"donor contract must disable {forbidden}")

    candidate = protocol.get("candidate_contract")
    if not isinstance(candidate, Mapping):
        errors.append("candidate contract is missing")
    else:
        if candidate.get("candidate_count") != 8:
            errors.append("exactly eight candidate ActionPlans are required")
        for required in (
            "selection_reads_truth",
            "complete_action_plans",
            "same_packet_within_task_world_prior_stratum",
            "condition_specific_reveal_gate_required",
            "outcomes_and_ranks_hidden",
            "public_truth_executed_plan_identity_required",
        ):
            expected = required != "selection_reads_truth"
            if candidate.get(required) is not expected:
                errors.append(f"candidate contract has invalid {required}")
        if candidate.get("selection_rule") != (
            "registered_16_query_public_feature_gower_maximin_8_candidate_remainder_checkpoint"
        ):
            errors.append("candidate selection rule differs from the fixed maximin contract")
        if candidate.get("same_packet_across_worlds_within_task") is not True:
            errors.append("candidate packet must be fixed across worlds within task")
        reveal_gates = candidate.get("reveal_gates")
        if not isinstance(reveal_gates, Mapping) or dict(reveal_gates) != CANDIDATE_REVEAL_GATES:
            errors.append("candidate reveal gates differ from the five-condition contract")

    artifact = protocol.get("artifact_contract")
    if not isinstance(artifact, Mapping):
        errors.append("artifact contract is missing")
    else:
        expected_artifact_values = {
            "learned_artifact_source": "autonomous_donor_final_typed_law",
            "oracle_artifact_source": "provider_free_disjoint_grid_fitted_predictive_law",
            "same_schema_required": True,
            "same_feature_and_metric_scope_required": True,
            "oracle_fit_may_not_use_candidate_outcomes": True,
            "candidate_outcomes_may_not_appear": True,
        }
        for key, value in expected_artifact_values.items():
            if artifact.get(key) != value:
                errors.append(f"artifact contract differs for {key}")
        threshold = artifact.get("minimum_oracle_candidate_rank_correlation")
        if not isinstance(threshold, int | float) or isinstance(threshold, bool):
            errors.append("oracle rank-correlation threshold is missing")
        elif not 0.0 <= float(threshold) <= 1.0:
            errors.append("oracle rank-correlation threshold must lie in [0, 1]")
        word_count = artifact.get("shared_maximum_artifact_word_count")
        if not isinstance(word_count, int) or isinstance(word_count, bool) or word_count <= 0:
            errors.append("shared artifact word limit must be a positive integer")

    oracle_grid = protocol.get("oracle_grid_contract")
    if not isinstance(oracle_grid, Mapping):
        errors.append("oracle grid contract is missing")
    else:
        if oracle_grid.get("selection_reads_truth") is not False:
            errors.append("oracle grid construction may not read truth")
        if oracle_grid.get("same_grid_across_worlds_within_task") is not True:
            errors.append("oracle grid must be fixed across worlds within task")
        if oracle_grid.get("candidate_feature_rows_excluded") is not True:
            errors.append("oracle grid must exclude terminal candidate feature rows")
        query_count = oracle_grid.get("query_count_per_task")
        if (
            not isinstance(query_count, int)
            or isinstance(query_count, bool)
            or query_count < 16
        ):
            errors.append("oracle grid must contain at least 16 queries per task")
        oversampling = oracle_grid.get("compile_valid_oversampling_factor")
        if (
            not isinstance(oversampling, int)
            or isinstance(oversampling, bool)
            or oversampling < 1
        ):
            errors.append("oracle grid compile-valid oversampling factor is invalid")

    execution = protocol.get("execution")
    if not isinstance(execution, Mapping):
        errors.append("execution contract is missing")
    else:
        if execution.get("provider_execution_authorized") is not False:
            errors.append("provider execution must remain disabled during design preparation")
        expected = {
            "task_count": 3,
            "formal_world_count_per_task": 5,
            "prior_arm_count": 3,
            "condition_count": 5,
            "scheduled_session_count": 225,
            "autonomous_session_count": 45,
            "participant_physical_experiment_count": 540,
        }
        for key, value in expected.items():
            if execution.get(key) != value:
                errors.append(f"execution denominator differs for {key}")
    return errors


def _cell_id(stratum_id: str, condition: str) -> str:
    return f"{stratum_id}--{condition}"


def split_registered_query_pool(
    registered_queries: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split the registered 16-query coverage order into two balanced, fixed packets."""

    if len(registered_queries) != 16:
        raise ValueError("evidence-to-action query pool must contain exactly 16 registered queries")
    rows = [deepcopy(dict(row)) for row in registered_queries]
    query_ids = [str(row.get("query_id")) for row in rows]
    if any(query_id in {"", "None"} for query_id in query_ids):
        raise ValueError("registered query IDs must be non-empty")
    if len(set(query_ids)) != 16:
        raise ValueError("registered query IDs must be unique")
    candidates = rows[0::2]
    checkpoints = rows[1::2]
    if len(candidates) != 8 or len(checkpoints) != 8:
        raise AssertionError("balanced alternating split denominator is invalid")
    return candidates, checkpoints


def split_registered_query_pool_maximin(
    registered_queries: Sequence[Mapping[str, Any]],
    *,
    allowed_feature_ids: Sequence[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Select eight structurally dispersed candidates without reading evaluator outcomes."""

    if len(registered_queries) != 16:
        raise ValueError("evidence-to-action query pool must contain exactly 16 registered queries")
    rows = [deepcopy(dict(row)) for row in registered_queries]
    query_ids = [str(row.get("query_id")) for row in rows]
    if len(set(query_ids)) != 16 or any(query_id in {"", "None"} for query_id in query_ids):
        raise ValueError("registered query IDs must be 16 unique non-empty strings")
    active_features: list[tuple[str, str, tuple[Any, ...]]] = []
    for feature_id in allowed_feature_ids:
        values = tuple(row.get("feature_values", {}).get(feature_id) for row in rows)
        unique = tuple(sorted(set(values), key=lambda value: (str(type(value)), str(value))))
        if len(unique) <= 1:
            continue
        categorical = len(unique) <= 4 and all(
            isinstance(value, int) and not isinstance(value, bool) for value in unique
        )
        active_features.append((feature_id, "categorical" if categorical else "numeric", unique))
    if not active_features:
        raise ValueError("registered query pool has no varying public features")

    def distance(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
        left_features = left["feature_values"]
        right_features = right["feature_values"]
        terms: list[float] = []
        for feature_id, kind, unique in active_features:
            left_value = left_features[feature_id]
            right_value = right_features[feature_id]
            if kind == "categorical":
                terms.append(float(left_value != right_value))
            else:
                lower = float(min(unique))
                upper = float(max(unique))
                terms.append(abs(float(left_value) - float(right_value)) / (upper - lower))
        return math.sqrt(sum(term * term for term in terms) / len(terms))

    farthest_pairs = [
        (distance(rows[left], rows[right]), query_ids[left], query_ids[right], left, right)
        for left in range(len(rows))
        for right in range(left + 1, len(rows))
    ]
    _, _, _, first, second = max(
        farthest_pairs,
        key=lambda item: (item[0], tuple(sorted((item[1], item[2])))),
    )
    selected = [first, second]
    remaining = set(range(len(rows))) - set(selected)
    while len(selected) < 8:
        next_index = max(
            remaining,
            key=lambda index: (
                min(distance(rows[index], rows[chosen]) for chosen in selected),
                query_ids[index],
            ),
        )
        selected.append(next_index)
        remaining.remove(next_index)
    candidate_set = set(selected)
    candidates = [row for index, row in enumerate(rows) if index in candidate_set]
    checkpoints = [row for index, row in enumerate(rows) if index not in candidate_set]
    return candidates, checkpoints


def evaluate_candidate_packet(
    candidate_truth: Mapping[str, Mapping[str, Any]],
    candidate_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Evaluate the provider-free action-opportunity gates for one development world."""

    expected_count = int(candidate_contract["candidate_count"])
    scores: dict[str, float] = {}
    errors: list[str] = []
    for query_id, row in candidate_truth.items():
        score = row.get("score") if isinstance(row, Mapping) else None
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            errors.append(f"{query_id}: finite numeric score is missing")
            continue
        value = float(score)
        if value != value or value in {float("inf"), float("-inf")}:
            errors.append(f"{query_id}: finite numeric score is missing")
            continue
        scores[str(query_id)] = value
    if len(scores) != expected_count:
        errors.append(f"candidate truth denominator is {len(scores)}, expected {expected_count}")

    raw_range = max(scores.values()) - min(scores.values()) if scores else 0.0
    minimum_range = float(candidate_contract["development_minimum_raw_score_range"])
    if raw_range < minimum_range:
        errors.append(f"candidate raw score range {raw_range:.6f} is below {minimum_range:.6f}")

    best = max(scores.values()) if scores else 0.0
    raw_regrets = {query_id: best - score for query_id, score in scores.items()}
    regret_threshold = 0.05
    count_key = "development_minimum_candidates_with_raw_regret_at_least_0_05"
    minimum_regret_candidates = int(candidate_contract[count_key])
    regret_candidate_count = sum(regret >= regret_threshold for regret in raw_regrets.values())
    if regret_candidate_count < minimum_regret_candidates:
        errors.append(
            "candidate packet has too few meaningfully non-optimal actions: "
            f"{regret_candidate_count} < {minimum_regret_candidates}"
        )

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    top1_gap = ordered[0][1] - ordered[1][1] if len(ordered) > 1 else None
    return {
        "status": "passed" if not errors else "failed",
        "candidate_count": len(scores),
        "raw_score_range": raw_range,
        "top1_gap": top1_gap,
        "raw_regret_at_least_0_05_count": regret_candidate_count,
        "top1_gap_qualified": False,
        "errors": errors,
    }


def build_yoked_evidence_packet(
    trajectory_rows: Sequence[Mapping[str, Any]],
    *,
    donor_cell_id: str,
) -> dict[str, Any]:
    """Extract scientific action/observation evidence without donor reasoning or ledgers."""

    rounds: list[dict[str, Any]] = []
    pending_events: list[dict[str, Any]] = []
    completed_experiments = 0
    for event_index, row in enumerate(trajectory_rows, start=1):
        action = row.get("action")
        visible = row.get("agent_visible_observation")
        if not isinstance(action, Mapping) or not isinstance(visible, Mapping):
            raise ValueError(f"donor trajectory row {event_index} lacks public action/observation")
        scientific = visible.get("observation")
        if not isinstance(scientific, Mapping):
            raise ValueError(f"donor trajectory row {event_index} lacks scientific observation")
        public_observation = {
            str(key): deepcopy(value) for key, value in scientific.items() if value is not None
        }
        event = {
            "evidence_id": (
                f"donor-experiment-{completed_experiments + 1:02d}-"
                f"event-{event_index:03d}"
            ),
            "event_index": event_index,
            "donor_experiment_number": completed_experiments + 1,
            "action": deepcopy(dict(action)),
            "non_null_scientific_observation": public_observation,
            "observed_keys": deepcopy(list(row.get("observed_keys", []))),
            "observed_reward": deepcopy(visible.get("observed_reward")),
            "transaction_status": str(row.get("transaction_status", "unknown")),
            "rollback_reason": deepcopy(row.get("rollback_reason")),
        }
        pending_events.append(event)
        is_final_assay = (
            action.get("operation") == "measure"
            and action.get("instrument") == "final_assay"
            and row.get("transaction_status") == "committed"
        )
        if is_final_assay:
            completed_experiments += 1
            rounds.append(
                {
                    "after_complete_experiment": completed_experiments,
                    "belief_snapshot_due": completed_experiments in YOKED_CHECKPOINTS,
                    "events": pending_events,
                }
            )
            pending_events = []
    if completed_experiments != 12 or pending_events:
        raise ValueError(
            "autonomous donor must end with exactly 12 committed final assays and no open events"
        )
    packet = {
        "schema_version": "chemworld-work-ii-yoked-evidence-packet-0.1",
        "donor_cell_id": donor_cell_id,
        "complete_experiment_count": completed_experiments,
        "checkpoint_rounds": rounds,
        "donor_reasoning_included": False,
        "campaign_resource_state_included": False,
        "candidate_information_included": False,
    }
    rendered = json.dumps(packet, ensure_ascii=False, sort_keys=True).lower()
    for forbidden in ("agent_trace", "private_reasoning", "candidate_truth", "hidden_rank"):
        if forbidden in rendered:
            raise ValueError(f"yoked packet contains forbidden field: {forbidden}")
    return packet


def build_learned_law_artifact(
    campaign_summary: Mapping[str, Any],
    *,
    donor_cell_id: str,
    candidate_query_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Extract only the donor's committed final typed law for a fresh recipient context."""

    analysis = campaign_summary.get("analysis")
    analysis = analysis if isinstance(analysis, Mapping) else {}
    snapshots = analysis.get("belief_snapshots")
    snapshots = snapshots if isinstance(snapshots, list) else []
    finals = [row for row in snapshots if isinstance(row, Mapping) and row.get("stage") == "final"]
    if len(finals) != 1 or not isinstance(finals[0].get("law_summary"), Mapping):
        raise ValueError("autonomous donor lacks one committed final typed law")
    law = deepcopy(dict(finals[0]["law_summary"]))
    rendered = json.dumps(law, ensure_ascii=False, sort_keys=True)
    leaked = [query_id for query_id in candidate_query_ids if str(query_id) in rendered]
    if leaked:
        raise ValueError("learned law artifact contains terminal candidate identifiers")
    return {
        "schema_version": "chemworld-work-ii-learned-law-artifact-0.1",
        "donor_cell_id": donor_cell_id,
        "artifact_type": "participant_final_typed_law",
        "law_summary": law,
        "donor_evidence_included": False,
        "donor_reasoning_included": False,
        "candidate_information_included": False,
    }


def build_oracle_law_artifact(
    law_summary: Mapping[str, Any],
    *,
    fit_query_ids: Sequence[str],
    candidate_query_ids: Sequence[str],
    fitted_from_candidate_outcomes: bool,
) -> dict[str, Any]:
    """Bind an oracle law to a disjoint provider-free fit set without candidate leakage."""

    fit_ids = tuple(str(query_id) for query_id in fit_query_ids)
    candidate_ids = tuple(str(query_id) for query_id in candidate_query_ids)
    if not fit_ids or len(set(fit_ids)) != len(fit_ids):
        raise ValueError("oracle fit query IDs must be a non-empty unique set")
    overlap = sorted(set(fit_ids) & set(candidate_ids))
    if overlap:
        raise ValueError("oracle fit grid overlaps the terminal candidate packet")
    if fitted_from_candidate_outcomes:
        raise ValueError("oracle law may not be fitted from candidate outcomes")
    rendered = json.dumps(law_summary, ensure_ascii=False, sort_keys=True)
    leaked = [query_id for query_id in candidate_ids if query_id in rendered]
    if leaked:
        raise ValueError("oracle law contains terminal candidate identifiers")
    return {
        "schema_version": "chemworld-work-ii-oracle-law-artifact-0.1",
        "artifact_type": "provider_free_disjoint_grid_fitted_predictive_law",
        "fit_query_ids": list(fit_ids),
        "fit_used_candidate_outcomes": False,
        "law_summary": deepcopy(dict(law_summary)),
        "candidate_information_included": False,
    }


def _radical_inverse(index: int, base: int) -> float:
    value = 0.0
    scale = 1.0 / base
    while index:
        index, digit = divmod(index, base)
        value += digit * scale
        scale /= base
    return value


def build_disjoint_oracle_grid(
    registered_queries: Sequence[Mapping[str, Any]],
    *,
    allowed_feature_ids: Sequence[str],
    allowed_metric_ids: Sequence[str],
    candidate_query_ids: Sequence[str],
    query_count: int,
    grid_id: str,
) -> list[dict[str, Any]]:
    """Build a truth-blind dense grid over the registered public feature envelope.

    Continuous coordinates use a deterministic Halton design and small integer-valued
    categorical coordinates cycle over their registered levels. Exact terminal-candidate
    feature rows are skipped, so disjointness is scientific as well as identifier based.
    """

    if query_count < 16:
        raise ValueError("oracle grid must contain at least 16 queries")
    if not registered_queries:
        raise ValueError("registered query pool is empty")
    if not allowed_feature_ids or len(allowed_feature_ids) > len(_HALTON_PRIMES):
        raise ValueError("oracle grid feature denominator is unsupported")
    candidate_ids = {str(query_id) for query_id in candidate_query_ids}
    rows_by_id = {str(row.get("query_id")): row for row in registered_queries}
    if not candidate_ids.issubset(rows_by_id):
        raise ValueError("terminal candidate IDs are outside the registered query pool")

    feature_columns: dict[str, list[Any]] = {}
    for feature_id in allowed_feature_ids:
        values: list[Any] = []
        for row in registered_queries:
            features = row.get("feature_values")
            if not isinstance(features, Mapping) or feature_id not in features:
                raise ValueError("registered query lacks the oracle feature scope")
            values.append(features[feature_id])
        feature_columns[feature_id] = values

    candidate_features = {
        json.dumps(
            {
                feature_id: rows_by_id[query_id]["feature_values"][feature_id]
                for feature_id in allowed_feature_ids
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        for query_id in candidate_ids
    }
    grid: list[dict[str, Any]] = []
    seen_features: set[str] = set()
    design_index = 1
    maximum_attempts = query_count * 100
    while len(grid) < query_count and design_index <= maximum_attempts:
        features: dict[str, Any] = {}
        for feature_index, feature_id in enumerate(allowed_feature_ids):
            values = feature_columns[feature_id]
            unique = sorted(set(values), key=lambda value: (str(type(value)), str(value)))
            if len(unique) == 1:
                features[feature_id] = unique[0]
                continue
            categorical = len(unique) <= 4 and all(
                isinstance(value, int) and not isinstance(value, bool) for value in unique
            )
            if categorical:
                coordinate = _radical_inverse(
                    design_index, _HALTON_PRIMES[feature_index]
                )
                position = min(int(coordinate * len(unique)), len(unique) - 1)
                features[feature_id] = unique[position]
                continue
            if not all(
                isinstance(value, int | float)
                and not isinstance(value, bool)
                and math.isfinite(float(value))
                for value in unique
            ):
                raise ValueError(
                    f"{feature_id}: oracle grid supports only numeric/categorical values"
                )
            low = min(float(value) for value in unique)
            high = max(float(value) for value in unique)
            coordinate = _radical_inverse(
                design_index, _HALTON_PRIMES[feature_index]
            )
            features[feature_id] = low + (high - low) * coordinate
        rendered = json.dumps(features, sort_keys=True, separators=(",", ":"))
        design_index += 1
        if rendered in candidate_features or rendered in seen_features:
            continue
        seen_features.add(rendered)
        grid.append(
            {
                "query_id": f"{grid_id}--q{len(grid) + 1:03d}",
                "feature_values": features,
                "metric_ids": [str(metric_id) for metric_id in allowed_metric_ids],
            }
        )
    if len(grid) != query_count:
        raise ValueError("oracle grid could not realize its registered query denominator")
    for feature_id, values in feature_columns.items():
        unique = set(values)
        categorical = len(unique) <= 4 and all(
            isinstance(value, int) and not isinstance(value, bool) for value in unique
        )
        if categorical and {row["feature_values"][feature_id] for row in grid} != unique:
            raise ValueError(f"{feature_id}: oracle grid omits a registered categorical level")
    return grid


def _oracle_basis_specs(
    fit_queries: Sequence[Mapping[str, Any]],
    allowed_feature_ids: Sequence[str],
) -> list[dict[str, Any]]:
    feature_values = {
        feature_id: [row["feature_values"][feature_id] for row in fit_queries]
        for feature_id in allowed_feature_ids
    }
    numeric: list[str] = []
    specs: list[dict[str, Any]] = []
    for feature_id in allowed_feature_ids:
        values = feature_values[feature_id]
        unique = sorted(set(values), key=lambda value: (str(type(value)), str(value)))
        if len(unique) <= 1:
            continue
        integer_categorical = len(unique) <= 4 and all(
            isinstance(value, int) and not isinstance(value, bool) for value in unique
        )
        if integer_categorical:
            for level in unique[1:]:
                specs.append(
                    {
                        "basis": "categorical_level",
                        "input_ids": [feature_id],
                        "category_value": level,
                    }
                )
            continue
        if not all(
            isinstance(value, int | float)
            and not isinstance(value, bool)
            and math.isfinite(float(value))
            for value in values
        ):
            for level in unique[1:]:
                specs.append(
                    {
                        "basis": "categorical_level",
                        "input_ids": [feature_id],
                        "category_value": level,
                    }
                )
            continue
        numeric.append(feature_id)
        specs.extend(
            [
                {"basis": "linear", "input_ids": [feature_id]},
                {"basis": "quadratic", "input_ids": [feature_id]},
            ]
        )
    for left_index, left_id in enumerate(numeric):
        for right_id in numeric[left_index + 1 :]:
            specs.append(
                {"basis": "interaction", "input_ids": [left_id, right_id]}
            )
    if len(specs) > 64:
        raise ValueError("oracle fit basis exceeds the shared typed-law term limit")
    return specs


def _oracle_basis_value(spec: Mapping[str, Any], features: Mapping[str, Any]) -> float:
    basis = spec["basis"]
    input_ids = spec["input_ids"]
    if basis == "categorical_level":
        return float(features[input_ids[0]] == spec["category_value"])
    values = [float(features[feature_id]) for feature_id in input_ids]
    if basis == "linear":
        return values[0]
    if basis == "quadratic":
        return values[0] ** 2
    return values[0] * values[1]


def _ridge_coefficients(
    matrix: np.ndarray,
    response: np.ndarray,
    penalty: float,
) -> tuple[float, np.ndarray]:
    centers = matrix.mean(axis=0)
    scales = matrix.std(axis=0)
    scales = np.where(scales <= 1.0e-12, 1.0, scales)
    standardized = (matrix - centers) / scales
    centered_response = response - response.mean()
    gram = standardized.T @ standardized + penalty * np.eye(standardized.shape[1])
    beta_standardized = np.linalg.solve(gram, standardized.T @ centered_response)
    coefficients = beta_standardized / scales
    intercept = float(response.mean() - coefficients @ centers)
    return intercept, coefficients


def _select_oracle_ridge_penalty(matrix: np.ndarray, response: np.ndarray) -> float:
    penalties = (1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1, 1.0, 10.0)
    candidates: list[tuple[float, float]] = []
    fold_count = len(response) if len(response) <= 16 else 8
    for penalty in penalties:
        errors: list[float] = []
        for fold in range(fold_count):
            held_out = [
                index for index in range(len(response)) if index % fold_count == fold
            ]
            retained = [
                index for index in range(len(response)) if index % fold_count != fold
            ]
            intercept, coefficients = _ridge_coefficients(
                matrix[retained], response[retained], penalty
            )
            predictions = intercept + matrix[held_out] @ coefficients
            errors.extend(
                abs(float(prediction) - float(response[index]))
                for prediction, index in zip(predictions, held_out, strict=True)
            )
        candidates.append((sum(errors) / len(errors), penalty))
    return min(candidates, key=lambda item: (item[0], -item[1]))[1]


def fit_oracle_law_from_disjoint_grid(
    fit_queries: Sequence[Mapping[str, Any]],
    fit_truth: Mapping[str, Mapping[str, Any]],
    *,
    candidate_query_ids: Sequence[str],
    allowed_feature_ids: Sequence[str],
    allowed_metric_ids: Sequence[str],
    summary_id: str,
) -> dict[str, Any]:
    """Fit a fixed typed predictive law without reading terminal candidate outcomes."""

    if len(fit_queries) < 8:
        raise ValueError("oracle fit grid must contain at least eight registered queries")
    fit_ids = [str(row.get("query_id")) for row in fit_queries]
    if len(set(fit_ids)) != len(fit_queries) or set(fit_ids) != set(map(str, fit_truth)):
        raise ValueError("oracle fit query/truth denominator differs")
    if set(fit_ids) & set(map(str, candidate_query_ids)):
        raise ValueError("oracle fit grid overlaps the terminal candidate packet")
    for row in fit_queries:
        features = row.get("feature_values")
        if not isinstance(features, Mapping) or not set(allowed_feature_ids).issubset(features):
            raise ValueError("oracle fit query lacks the declared feature scope")
    specs = _oracle_basis_specs(fit_queries, allowed_feature_ids)
    if not specs:
        raise ValueError("oracle fit grid has no varying scientific features")
    matrix = np.asarray(
        [
            [_oracle_basis_value(spec, row["feature_values"]) for spec in specs]
            for row in fit_queries
        ],
        dtype=float,
    )
    metric_laws: list[dict[str, Any]] = []
    for metric_id in allowed_metric_ids:
        response = np.asarray(
            [float(fit_truth[query_id][metric_id]) for query_id in fit_ids],
            dtype=float,
        )
        if not np.isfinite(response).all():
            raise ValueError(f"oracle fit truth for {metric_id} is not finite")
        penalty = _select_oracle_ridge_penalty(matrix, response)
        intercept, coefficients = _ridge_coefficients(matrix, response, penalty)
        terms: list[dict[str, Any]] = []
        for term_index, (spec, coefficient) in enumerate(
            zip(specs, coefficients, strict=True), start=1
        ):
            term = {
                "term_id": f"{metric_id}-term-{term_index:02d}",
                **deepcopy(dict(spec)),
                "coefficient": float(coefficient),
            }
            terms.append(term)
        metric_laws.append(
            {
                "metric_id": metric_id,
                "intercept": intercept,
                "link": "identity",
                "lower_bound": 0.0,
                "upper_bound": 1.0,
                "terms": terms,
            }
        )
    law_summary = {
        "schema_version": "chemworld-work-ii-law-summary-0.1",
        "summary_id": summary_id,
        "feature_ids": list(allowed_feature_ids),
        "metric_laws": metric_laws,
        "evidence_ids": fit_ids,
        "applicability": "registered complete-ActionPlan candidate domain",
        "limitations": [
            "provider-free quadratic ridge surrogate fitted only on the disjoint "
            "registered dense grid"
        ],
        "confidence": 1.0,
    }
    return build_oracle_law_artifact(
        law_summary,
        fit_query_ids=fit_ids,
        candidate_query_ids=candidate_query_ids,
        fitted_from_candidate_outcomes=False,
    )


def _average_ranks(values: Sequence[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: (item[1], item[0]))
    ranks = [0.0] * len(indexed)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and indexed[end][1] == indexed[start][1]:
            end += 1
        average = (start + 1 + end) / 2.0
        for position in range(start, end):
            ranks[indexed[position][0]] = average
        start = end
    return ranks


def _pearson_correlation(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or len(left) < 2:
        raise ValueError("rank correlation requires equally sized vectors with at least two values")
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum(
        (left_value - left_mean) * (right_value - right_mean)
        for left_value, right_value in zip(left, right, strict=True)
    )
    left_scale = math.sqrt(sum((value - left_mean) ** 2 for value in left))
    right_scale = math.sqrt(sum((value - right_mean) ** 2 for value in right))
    if left_scale == 0.0 or right_scale == 0.0:
        return 0.0
    return numerator / (left_scale * right_scale)


def evaluate_oracle_law_candidate_order(
    artifact: Mapping[str, Any],
    *,
    candidate_queries: Sequence[Mapping[str, Any]],
    candidate_truth: Mapping[str, Mapping[str, Any]],
    allowed_feature_ids: Sequence[str],
    allowed_metric_ids: Sequence[str],
    minimum_rank_correlation: float,
    score_metric_id: str = "score",
) -> dict[str, Any]:
    """Qualify a fixed oracle law on development candidates without changing the fit."""

    errors: list[str] = []
    fit_query_ids = _string_list(artifact.get("fit_query_ids"))
    law_payload = artifact.get("law_summary")
    candidate_ids = [str(row.get("query_id")) for row in candidate_queries]
    if set(fit_query_ids) & set(candidate_ids):
        errors.append("oracle fit grid overlaps the terminal candidate packet")
    if artifact.get("fit_used_candidate_outcomes") is not False:
        errors.append("oracle artifact does not prove candidate-outcome-free fitting")
    if artifact.get("candidate_information_included") is not False:
        errors.append("oracle artifact includes terminal candidate information")
    if score_metric_id not in set(allowed_metric_ids):
        errors.append("score metric is outside the declared artifact scope")

    law = None
    try:
        law = parse_work_ii_law_summary(
            law_payload,
            allowed_feature_ids=allowed_feature_ids,
            allowed_metric_ids=allowed_metric_ids,
            evidence_catalog=fit_query_ids,
            required_metric_ids=allowed_metric_ids,
        )
    except (TypeError, ValueError) as exc:
        errors.append(f"invalid oracle typed law: {exc}")

    predictions: list[float] = []
    truths: list[float] = []
    evaluated_ids: list[str] = []
    if law is not None:
        for row in candidate_queries:
            query_id = str(row.get("query_id"))
            features = row.get("feature_values")
            truth_row = candidate_truth.get(query_id)
            if not isinstance(features, Mapping) or not isinstance(truth_row, Mapping):
                errors.append(f"{query_id}: candidate features or truth are missing")
                continue
            truth_score = truth_row.get(score_metric_id)
            if isinstance(truth_score, bool) or not isinstance(truth_score, int | float):
                errors.append(f"{query_id}: candidate truth score is missing")
                continue
            try:
                predicted_score = law.predict(features)[score_metric_id]
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(f"{query_id}: oracle prediction failed: {exc}")
                continue
            predictions.append(float(predicted_score))
            truths.append(float(truth_score))
            evaluated_ids.append(query_id)

    correlation = 0.0
    top1_agreement = False
    if len(evaluated_ids) == len(candidate_queries) and len(evaluated_ids) >= 2:
        correlation = _pearson_correlation(_average_ranks(predictions), _average_ranks(truths))
        top1_agreement = evaluated_ids[predictions.index(max(predictions))] == evaluated_ids[
            truths.index(max(truths))
        ]
        if correlation < minimum_rank_correlation:
            errors.append(
                f"oracle candidate rank correlation {correlation:.6f} is below "
                f"{minimum_rank_correlation:.6f}"
            )
    elif not errors:
        errors.append("oracle qualification did not cover the complete candidate packet")
    return {
        "status": "passed" if not errors else "failed",
        "candidate_count": len(candidate_queries),
        "evaluated_candidate_count": len(evaluated_ids),
        "spearman_rank_correlation": correlation,
        "top1_agreement": top1_agreement,
        "fit_candidate_overlap_count": len(set(fit_query_ids) & set(candidate_ids)),
        "errors": errors,
    }


def predict_candidate_ranking_from_law(
    law_payload: Mapping[str, Any],
    *,
    candidate_queries: Sequence[Mapping[str, Any]],
    allowed_feature_ids: Sequence[str],
    allowed_metric_ids: Sequence[str],
    evidence_catalog: Sequence[str],
    score_metric_id: str = "score",
) -> dict[str, Any]:
    """Evaluate an executable participant/oracle law without reading candidate outcomes."""

    if len(candidate_queries) != 8:
        raise ValueError("law-implied ranking requires exactly eight candidates")
    law = parse_work_ii_law_summary(
        law_payload,
        allowed_feature_ids=allowed_feature_ids,
        allowed_metric_ids=allowed_metric_ids,
        evidence_catalog=evidence_catalog,
        required_metric_ids=allowed_metric_ids,
    )
    predictions: dict[str, float] = {}
    for row in candidate_queries:
        query_id = str(row.get("query_id"))
        features = row.get("feature_values")
        if query_id in predictions or not isinstance(features, Mapping):
            raise ValueError("candidate identity or features are invalid")
        prediction = law.predict(features)
        if score_metric_id not in prediction:
            raise ValueError("executable law does not predict the ranking score")
        predictions[query_id] = float(prediction[score_metric_id])
    ranking = sorted(predictions, key=lambda query_id: (-predictions[query_id], query_id))
    return {
        "law_implied_ranking": ranking,
        "law_implied_selected_query_id": ranking[0],
        "candidate_score_predictions": predictions,
        "candidate_outcomes_used": False,
    }


def evaluate_law_action_agreement(
    submitted_ranking: Sequence[str] | None,
    law_implied_ranking: Sequence[str] | None,
) -> dict[str, Any]:
    """Separate failure to use a law from failure of the law itself."""

    if submitted_ranking is None or law_implied_ranking is None:
        return {
            "law_action_complete_ranking_agreement": None,
            "law_action_spearman_rank_correlation": None,
            "law_implied_top1_followed": None,
            "law_action_pairwise_agreement": None,
        }
    submitted = [str(query_id) for query_id in submitted_ranking]
    implied = [str(query_id) for query_id in law_implied_ranking]
    if (
        len(submitted) != 8
        or len(implied) != 8
        or len(set(submitted)) != 8
        or set(submitted) != set(implied)
    ):
        raise ValueError(
            "law and action rankings must be permutations of the same eight candidates"
        )
    submitted_positions = {query_id: index for index, query_id in enumerate(submitted)}
    implied_positions = {query_id: index for index, query_id in enumerate(implied)}
    ordered_ids = sorted(submitted)
    submitted_ranks = [float(submitted_positions[query_id]) for query_id in ordered_ids]
    implied_ranks = [float(implied_positions[query_id]) for query_id in ordered_ids]
    agreements = 0
    pairs = 0
    for left_index, left_id in enumerate(ordered_ids):
        for right_id in ordered_ids[left_index + 1 :]:
            pairs += 1
            submitted_order = submitted_positions[left_id] - submitted_positions[right_id]
            implied_order = implied_positions[left_id] - implied_positions[right_id]
            agreements += int(submitted_order * implied_order > 0)
    return {
        "law_action_complete_ranking_agreement": int(submitted == implied),
        "law_action_spearman_rank_correlation": _pearson_correlation(
            submitted_ranks, implied_ranks
        ),
        "law_implied_top1_followed": int(submitted[0] == implied[0]),
        "law_action_pairwise_agreement": agreements / pairs,
    }


def score_terminal_ranking(
    ranking: Sequence[str] | None,
    candidate_truth: Mapping[str, Mapping[str, Any]],
    *,
    score_metric_id: str = "score",
    tie_tolerance: float = 0.01,
) -> dict[str, Any]:
    """Score one terminal ranking with failure-aware and near-tie-aware endpoints."""

    scores: dict[str, float] = {}
    for query_id, row in candidate_truth.items():
        value = row.get(score_metric_id) if isinstance(row, Mapping) else None
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"{query_id}: candidate truth score is missing")
        numeric = float(value)
        if not math.isfinite(numeric):
            raise ValueError(f"{query_id}: candidate truth score is not finite")
        scores[str(query_id)] = numeric
    if len(scores) != 8:
        raise ValueError("terminal ranking truth must contain exactly eight candidates")
    if ranking is None:
        return {
            "status": "failed_missing_terminal_ranking",
            "selected_action_query_id": None,
            "selected_rank": None,
            "top1": 0,
            "within_0_01_of_best": 0,
            "raw_regret": None,
            "failure_aware_normalized_regret": 1.0,
            "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01": None,
            "qualified_pair_count": 0,
        }
    submitted = [str(query_id) for query_id in ranking]
    if len(submitted) != 8 or set(submitted) != set(scores):
        raise ValueError("terminal ranking must contain every candidate exactly once")
    truth_order = sorted(scores, key=lambda query_id: (-scores[query_id], query_id))
    truth_rank = {query_id: index for index, query_id in enumerate(truth_order, start=1)}
    selected = submitted[0]
    best = scores[truth_order[0]]
    worst = min(scores.values())
    raw_regret = best - scores[selected]
    score_range = best - worst
    normalized_regret = 0.0 if score_range <= 1.0e-12 else raw_regret / score_range
    submitted_position = {query_id: index for index, query_id in enumerate(submitted)}
    agreements = 0
    qualified_pairs = 0
    query_ids = sorted(scores)
    for left_index, left_id in enumerate(query_ids):
        for right_id in query_ids[left_index + 1 :]:
            truth_gap = scores[left_id] - scores[right_id]
            if abs(truth_gap) < tie_tolerance:
                continue
            qualified_pairs += 1
            submitted_gap = submitted_position[right_id] - submitted_position[left_id]
            if (truth_gap > 0 and submitted_gap > 0) or (truth_gap < 0 and submitted_gap < 0):
                agreements += 1
    pairwise = agreements / qualified_pairs if qualified_pairs else None
    return {
        "status": "completed",
        "selected_action_query_id": selected,
        "selected_rank": truth_rank[selected],
        "top1": int(selected == truth_order[0]),
        "within_0_01_of_best": int(raw_regret <= tie_tolerance),
        "raw_regret": raw_regret,
        "failure_aware_normalized_regret": normalized_regret,
        "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01": pairwise,
        "qualified_pair_count": qualified_pairs,
    }


def analyze_terminal_results(
    design_manifest: Mapping[str, Any],
    results: Mapping[str, Mapping[str, Any]],
    *,
    candidate_truth_by_cluster: Mapping[str, Mapping[str, Mapping[str, Any]]],
) -> dict[str, Any]:
    """Score the frozen denominator and aggregate paired contrasts by task-world cluster."""

    if design_manifest.get("schema_version") != MANIFEST_SCHEMA:
        raise ValueError("evidence-to-action design manifest schema is invalid")
    cells = design_manifest.get("cells")
    if not isinstance(cells, list) or not cells:
        raise ValueError("evidence-to-action design manifest has no cells")
    cell_ids = [str(cell.get("cell_id")) for cell in cells if isinstance(cell, Mapping)]
    if len(cell_ids) != len(cells) or len(set(cell_ids)) != len(cells):
        raise ValueError("evidence-to-action design cell identities are invalid")
    if set(map(str, results)) - set(cell_ids):
        raise ValueError("result records contain cells outside the scheduled denominator")

    scored_rows: list[dict[str, Any]] = []
    by_stratum_condition: dict[tuple[str, str], dict[str, Any]] = {}
    for cell in cells:
        cluster_id = str(cell["cluster_id"])
        truth = candidate_truth_by_cluster.get(cluster_id)
        if not isinstance(truth, Mapping):
            raise ValueError(f"{cluster_id}: candidate truth is missing")
        result = results.get(str(cell["cell_id"]))
        result = result if isinstance(result, Mapping) else {}
        submission = result.get("submission")
        submission = submission if isinstance(submission, Mapping) else result
        ranking = submission.get("ranking")
        ranking = (
            list(ranking)
            if isinstance(ranking, Sequence) and not isinstance(ranking, (str, bytes))
            else None
        )
        score = score_terminal_ranking(ranking, truth)
        row = {
            "cell_id": str(cell["cell_id"]),
            "cluster_id": cluster_id,
            "stratum_id": str(cell["stratum_id"]),
            "task_id": str(cell["task_id"]),
            "world_seed": int(cell["world_seed"]),
            "prior_arm": str(cell["prior_arm"]),
            "condition": str(cell["condition"]),
            "scheduled": True,
            "result_status": str(result.get("status", "missing_result")),
            **score,
        }
        scored_rows.append(row)
        by_stratum_condition[(row["stratum_id"], row["condition"])] = row

    paired_rows: list[dict[str, Any]] = []
    strata = design_manifest.get("strata")
    if not isinstance(strata, list):
        raise ValueError("evidence-to-action design strata are missing")
    for stratum in strata:
        stratum_id = str(stratum["stratum_id"])
        for treatment, control in PRESPECIFIED_CONTRASTS:
            treatment_row = by_stratum_condition[(stratum_id, treatment)]
            control_row = by_stratum_condition[(stratum_id, control)]
            paired_rows.append(
                {
                    "contrast": f"{treatment}_minus_{control}",
                    "cluster_id": str(stratum["cluster_id"]),
                    "stratum_id": stratum_id,
                    "prior_arm": str(stratum["prior_arm"]),
                    "failure_aware_normalized_regret_difference": (
                        float(treatment_row["failure_aware_normalized_regret"])
                        - float(control_row["failure_aware_normalized_regret"])
                    ),
                    "top1_difference": int(treatment_row["top1"])
                    - int(control_row["top1"]),
                }
            )

    contrast_summaries: list[dict[str, Any]] = []
    for treatment, control in PRESPECIFIED_CONTRASTS:
        contrast = f"{treatment}_minus_{control}"
        rows = [row for row in paired_rows if row["contrast"] == contrast]
        cluster_ids = sorted({str(row["cluster_id"]) for row in rows})
        cluster_rows: list[dict[str, Any]] = []
        for cluster_id in cluster_ids:
            cluster_values = [row for row in rows if row["cluster_id"] == cluster_id]
            if len(cluster_values) != len(PRIOR_ARMS):
                raise ValueError(f"{cluster_id}: paired contrast lacks all prior arms")
            cluster_rows.append(
                {
                    "cluster_id": cluster_id,
                    "prior_arm_count": len(cluster_values),
                    "mean_failure_aware_normalized_regret_difference": sum(
                        float(row["failure_aware_normalized_regret_difference"])
                        for row in cluster_values
                    )
                    / len(cluster_values),
                    "mean_top1_difference": sum(
                        int(row["top1_difference"]) for row in cluster_values
                    )
                    / len(cluster_values),
                }
            )
        contrast_summaries.append(
            {
                "contrast": contrast,
                "paired_stratum_count": len(rows),
                "independent_cluster_count": len(cluster_rows),
                "mean_failure_aware_normalized_regret_difference": sum(
                    float(row["mean_failure_aware_normalized_regret_difference"])
                    for row in cluster_rows
                )
                / len(cluster_rows),
                "mean_top1_difference": sum(
                    float(row["mean_top1_difference"]) for row in cluster_rows
                )
                / len(cluster_rows),
                "cluster_rows": cluster_rows,
            }
        )
    return {
        "schema_version": "chemworld-work-ii-evidence-to-action-terminal-analysis-0.1",
        "scheduled_session_count": len(cells),
        "received_result_count": len(results),
        "missing_or_unranked_session_count": sum(
            row["status"] == "failed_missing_terminal_ranking" for row in scored_rows
        ),
        "independent_cluster_count": len(design_manifest.get("clusters", [])),
        "cell_rows": scored_rows,
        "paired_rows": paired_rows,
        "contrast_summaries": contrast_summaries,
    }


def build_design_manifest(protocol: Mapping[str, Any]) -> dict[str, Any]:
    """Compile all scheduled cells and donor dependencies for the frozen design."""

    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("invalid evidence-to-action protocol: " + "; ".join(errors))

    tasks = [str(task) for task in protocol["task_runtime_sources"]]
    worlds = [int(seed) for seed in protocol["formal_world_seeds"]]
    conditions: Mapping[str, Mapping[str, Any]] = protocol["conditions"]
    rows: list[dict[str, Any]] = []
    clusters: list[dict[str, Any]] = []
    strata: list[dict[str, Any]] = []
    for task_index, task_id in enumerate(tasks):
        for world_seed in worlds:
            cluster_id = f"E2A--{task_id}--seed{world_seed}"
            cluster_cells: list[str] = []
            cluster_strata: list[str] = []
            packet_seed = (
                int(protocol["candidate_packet_seed_base"]) + task_index * 100
            )
            for prior_arm in PRIOR_ARMS:
                stratum_id = f"{cluster_id}--{prior_arm}"
                donor_cell_id = _cell_id(stratum_id, DONOR_CONDITION)
                stratum_cells: list[str] = []
                for condition in CONDITIONS:
                    cell_id = _cell_id(stratum_id, condition)
                    derived = condition in DONOR_DERIVED_CONDITIONS
                    row = {
                        "cell_id": cell_id,
                        "cluster_id": cluster_id,
                        "stratum_id": stratum_id,
                        "task_id": task_id,
                        "world_seed": world_seed,
                        "candidate_packet_seed": packet_seed,
                        "prior_arm": prior_arm,
                        "condition": condition,
                        "fresh_context": True,
                        "physical_experiment_count": int(
                            conditions[condition]["physical_experiments"]
                        ),
                        "checkpoint_stages": deepcopy(
                            list(conditions[condition]["checkpoint_stages"])
                        ),
                        "candidate_reveal_gate": protocol["candidate_contract"][
                            "reveal_gates"
                        ][condition],
                        "candidate_outcomes_hidden": True,
                        "dependency_cell_ids": [donor_cell_id] if derived else [],
                        "missing_dependency_status": (
                            protocol["donor_contract"]["missing_donor_status"] if derived else None
                        ),
                        "failure_retained": True,
                    }
                    rows.append(row)
                    cluster_cells.append(cell_id)
                    stratum_cells.append(cell_id)
                strata.append(
                    {
                        "stratum_id": stratum_id,
                        "cluster_id": cluster_id,
                        "prior_arm": prior_arm,
                        "donor_cell_id": donor_cell_id,
                        "cell_ids": stratum_cells,
                    }
                )
                cluster_strata.append(stratum_id)
            clusters.append(
                {
                    "cluster_id": cluster_id,
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "candidate_packet_seed": packet_seed,
                    "stratum_ids": cluster_strata,
                    "cell_ids": cluster_cells,
                }
            )

    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "study_id": protocol["study_id"],
        "provider_execution_authorized": False,
        "qualification_world_seeds": deepcopy(protocol["qualification_world_seeds"]),
        "formal_world_seeds": worlds,
        "task_ids": tasks,
        "prior_arms": list(PRIOR_ARMS),
        "conditions": list(CONDITIONS),
        "task_world_cluster_count": len(clusters),
        "task_world_prior_stratum_count": len(strata),
        "scheduled_session_count": len(rows),
        "autonomous_session_count": sum(row["condition"] == DONOR_CONDITION for row in rows),
        "donor_dependent_session_count": sum(bool(row["dependency_cell_ids"]) for row in rows),
        "participant_physical_experiment_count": sum(
            int(row["physical_experiment_count"]) for row in rows
        ),
        "candidate_contract": deepcopy(protocol["candidate_contract"]),
        "artifact_contract": deepcopy(protocol["artifact_contract"]),
        "analysis": deepcopy(protocol["analysis"]),
        "execution": deepcopy(protocol["execution"]),
        "clusters": clusters,
        "strata": strata,
        "cells": rows,
    }
    expected = protocol["execution"]
    if manifest["scheduled_session_count"] != expected["scheduled_session_count"]:
        raise AssertionError("compiled session denominator differs from the protocol")
    if (
        manifest["participant_physical_experiment_count"]
        != expected["participant_physical_experiment_count"]
    ):
        raise AssertionError("compiled physical-experiment denominator differs from the protocol")
    return manifest


__all__ = [
    "CANDIDATE_REVEAL_GATES",
    "CONDITIONS",
    "CONDITION_STAGES",
    "DONOR_CONDITION",
    "DONOR_DERIVED_CONDITIONS",
    "MANIFEST_SCHEMA",
    "PRESPECIFIED_CONTRASTS",
    "PRIOR_ARMS",
    "PROTOCOL_SCHEMA",
    "YOKED_CHECKPOINTS",
    "analyze_terminal_results",
    "build_design_manifest",
    "build_disjoint_oracle_grid",
    "build_learned_law_artifact",
    "build_oracle_law_artifact",
    "build_yoked_evidence_packet",
    "evaluate_candidate_packet",
    "evaluate_law_action_agreement",
    "evaluate_oracle_law_candidate_order",
    "fit_oracle_law_from_disjoint_grid",
    "predict_candidate_ranking_from_law",
    "score_terminal_ranking",
    "split_registered_query_pool",
    "split_registered_query_pool_maximin",
    "validate_protocol",
]
