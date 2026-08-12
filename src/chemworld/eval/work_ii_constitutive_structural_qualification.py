"""Frozen five-world paired-law qualification for the Work II A-S locus.

This module deliberately contains no fitted generic response surrogate.  The two
candidate hypotheses are executable ChemWorld laws: the registered partition
coefficient power transform and the registered reversible target-pathway
topology transform.  Qualification compares their paired provider-free
executions at an outcome-blind held-out roster.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from hashlib import sha256
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_c2_admission import validate_c2_source_binding

QUALIFICATION_VERSION = "chemworld-work-ii-constitutive-structural-q1-q2-0.1"
WORLD_REPORT_VERSION = "chemworld-work-ii-constitutive-structural-world-report-0.1"
PACKAGE_VERSION = "chemworld-work-ii-constitutive-structural-q2-package-0.1"
SUMMARY_VERSION = "chemworld-work-ii-constitutive-structural-five-world-summary-0.1"
WORLD_SEEDS = (0, 1, 2, 3, 4)
COORDINATES_PER_CANDIDATE_WORLD = 512
LAWS_PER_COORDINATE = 2
PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD = 1024
PRIMARY_EXECUTIONS_TOTAL = 10_240
EXACT_REPLAYS_TOTAL = 10_240
Q1_COORDINATES_PER_FAMILY = 192
Q2_COORDINATES_PER_FAMILY = 64
Q2_QUERY_COUNT_PER_FAMILY = 8
Q2_QUERY_COUNT_PER_CANDIDATE = 16
MINIMUM_SUPPORT_PER_Q2_FAMILY = 4
MINIMUM_RESOLVED_METRICS_PER_WORLD = 2

PARTITION_CANDIDATE_ID = "partition_power_response"
CRYSTALLIZATION_CANDIDATE_ID = "crystallization_reversible_topology"
CANDIDATE_IDS = (PARTITION_CANDIDATE_ID, CRYSTALLIZATION_CANDIDATE_ID)


def partition_intervention() -> dict[str, Any]:
    return {
        "kind": "mechanism_family",
        "mode": "constitutive_law_family",
        "severity": 1.0,
        "constitutive_law_change": {
            "transform_id": "partition_power_response_stress_v1",
            "partition_coefficient_exponent_at_full_severity": 1.75,
        },
    }


def crystallization_intervention() -> dict[str, Any]:
    return {
        "kind": "mechanism_family",
        "mode": "topology_family",
        "severity": 0.8,
        "topology_change": {
            "reaction_role": "primary_target_pathway",
            "transform_id": "reversible_target_pathway_stress_v1",
            "reverse_rate_constant_s_inv_at_full_severity": 0.000625,
        },
    }


def candidate_specs() -> dict[str, dict[str, Any]]:
    """Return the immutable executable-law and measurement contracts."""

    return {
        PARTITION_CANDIDATE_ID: {
            "task_id": "partition-discovery",
            "law_ids": ("linear_response", "power_response"),
            "altered_law_id": "power_response",
            "world_intervention": partition_intervention(),
            "intervention_families": ("identity", "phase_process"),
            "metric_ids": (
                "product_in_organic",
                "product_in_aqueous",
                "phase_ratio",
            ),
            "declared_sigma": {
                "product_in_organic": 0.010,
                "product_in_aqueous": 0.010,
                "phase_ratio": 0.012,
            },
            "effect_floor": 0.03,
            "noise_multiplier": 6.0,
            "allowed_feature_ids": (
                "solvent",
                "aqueous_phase_volume_L",
                "extractant",
                "extractant_volume_L",
                "mix_duration_s",
                "settle_duration_s",
                "stirring_speed_rpm",
            ),
            "allowed_prior_fields": (
                "partition_law_family",
                "partition_coefficient_exponent",
            ),
        },
        CRYSTALLIZATION_CANDIDATE_ID: {
            "task_id": "reaction-to-crystallization",
            "law_ids": ("baseline", "reversible_target_pathway"),
            "altered_law_id": "reversible_target_pathway",
            "world_intervention": crystallization_intervention(),
            "intervention_families": ("temperature", "duration"),
            "metric_ids": ("yield", "conversion", "selectivity"),
            "declared_sigma": {
                "yield": 0.012,
                "conversion": 0.012,
                "selectivity": 0.018,
            },
            "effect_floor": 0.05,
            "noise_multiplier": 3.0,
            "allowed_feature_ids": (
                "catalyst",
                "solvent",
                "reagent_amount_mol",
                "reaction_temperature_K",
                "reaction_duration_s",
                "stirring_speed_rpm",
                "catalyst_amount_mol",
                "seed_mass_g",
                "crystallization_temperature_K",
                "crystallization_duration_s",
            ),
            "allowed_prior_fields": (
                "target_pathway_topology",
                "reverse_rate_constant_s_inv",
            ),
        },
    }


def _design_seed(candidate_id: str) -> int:
    digest = sha256(f"{QUALIFICATION_VERSION}:{candidate_id}:roster".encode()).hexdigest()
    return int(digest[:8], 16)


def _category(value: float, count: int) -> int:
    return min(int(float(value) * count), count - 1)


def _scale(value: float, low: float, high: float) -> float:
    return round(low + float(value) * (high - low), 12)


def _partition_features(family: str, vector: Sequence[float]) -> dict[str, Any]:
    if family == "identity":
        return {
            "solvent": _category(vector[0], 4),
            "aqueous_phase_volume_L": 0.015,
            "extractant": _category(vector[1], 4),
            "extractant_volume_L": 0.019,
            "mix_duration_s": 420.0,
            "settle_duration_s": 900.0,
            "stirring_speed_rpm": 800.0,
        }
    return {
        "solvent": 0,
        "aqueous_phase_volume_L": _scale(vector[0], 0.006, 0.024),
        "extractant": 1,
        "extractant_volume_L": _scale(vector[1], 0.008, 0.030),
        "mix_duration_s": _scale(vector[2], 120.0, 900.0),
        "settle_duration_s": _scale(vector[3], 420.0, 1800.0),
        "stirring_speed_rpm": _scale(vector[4], 400.0, 1100.0),
    }


def _crystallization_features(family: str, vector: Sequence[float]) -> dict[str, Any]:
    temperature = _scale(vector[0], 350.0, 420.0) if family == "temperature" else 385.0
    duration = _scale(vector[1], 1200.0, 7200.0) if family == "duration" else 3600.0
    return {
        "catalyst": _category(vector[2], 4),
        "solvent": _category(vector[3], 4),
        "reagent_amount_mol": _scale(vector[4], 0.010, 0.020),
        "reaction_temperature_K": temperature,
        "reaction_duration_s": duration,
        "stirring_speed_rpm": 675.0,
        "catalyst_amount_mol": 0.000315,
        "seed_mass_g": 0.008,
        "crystallization_temperature_K": 290.0,
        "crystallization_duration_s": 7200.0,
    }


def registered_coordinates(candidate_id: str) -> list[dict[str, Any]]:
    """Return 512 immutable coordinates, split evenly across two families.

    The roster is independent of world outcomes and is identical across all five
    worlds.  Within each family the first 192 positions are Q1 coverage and the
    remaining 64 are the frozen Q2 held-out pool.
    """

    spec = candidate_specs()[candidate_id]
    design = qmc.Sobol(d=5, scramble=True, seed=_design_seed(candidate_id)).random_base2(m=9)
    rows: list[dict[str, Any]] = []
    family_counts = dict.fromkeys(spec["intervention_families"], 0)
    for coordinate_index, vector in enumerate(design):
        family = str(spec["intervention_families"][coordinate_index % 2])
        family_index = int(family_counts[family])
        family_counts[family] += 1
        phase = "q1_coverage" if family_index < Q1_COORDINATES_PER_FAMILY else "q2_heldout"
        features = (
            _partition_features(family, vector)
            if candidate_id == PARTITION_CANDIDATE_ID
            else _crystallization_features(family, vector)
        )
        rows.append(
            {
                "coordinate_id": f"c{coordinate_index:03d}",
                "coordinate_index": coordinate_index,
                "family_index": family_index,
                "phase": phase,
                "intervention_family": family,
                "feature_values": features,
                "coordinate_sha256": canonical_json_sha256(
                    {
                        "candidate_id": candidate_id,
                        "coordinate_index": coordinate_index,
                        "phase": phase,
                        "intervention_family": family,
                        "feature_values": features,
                    }
                ),
            }
        )
    if len(rows) != COORDINATES_PER_CANDIDATE_WORLD:
        raise AssertionError("paired-law coordinate denominator drifted")
    return rows


def selected_q2_queries(candidate_id: str) -> list[dict[str, Any]]:
    """Select 16 held-out queries using coordinates only, never outcomes."""

    rows = registered_coordinates(candidate_id)
    selected: list[dict[str, Any]] = []
    for family in candidate_specs()[candidate_id]["intervention_families"]:
        pool = [
            row
            for row in rows
            if row["phase"] == "q2_heldout" and row["intervention_family"] == family
        ]
        indices = np.linspace(0, len(pool) - 1, Q2_QUERY_COUNT_PER_FAMILY, dtype=int)
        selected.extend(pool[int(index)] for index in indices)
    return [dict(row) for row in selected]


def observation_binding(
    candidate_id: str, world_seed: int, coordinate_id: str
) -> tuple[int, str]:
    digest = sha256(
        f"{QUALIFICATION_VERSION}:{candidate_id}:{world_seed}:{coordinate_id}".encode()
    ).hexdigest()
    return (
        int(digest[:8], 16) % 2_147_483_647,
        f"work-ii-as-{candidate_id}-w{world_seed}-{digest[:12]}",
    )


def build_prior_arms(candidate_id: str) -> dict[str, dict[str, Any]]:
    spec = candidate_specs()[candidate_id]
    if candidate_id == PARTITION_CANDIDATE_ID:
        aligned_claim = (
            "Extraction follows a nonlinear power response in the solvent-extractant partition "
            "coefficient; phase balance and mixing conditions modulate the observable separation."
        )
        misspecified_claim = (
            "Extraction follows a linear reference response in the solvent-extractant partition "
            "coefficient; phase balance and mixing conditions modulate the observable separation."
        )
        aligned_law = {
            "law_id": "power_response",
            "world_interventions": [partition_intervention()],
        }
        misspecified_law = {"law_id": "linear_response", "world_interventions": []}
    else:
        aligned_claim = (
            "The primary target pathway is reversible; temperature and reaction duration jointly "
            "expose accumulated reverse flux before crystallization and terminal assay."
        )
        misspecified_claim = (
            "The primary target pathway is irreversible; temperature and reaction duration jointly "
            "expose accumulated forward flux before crystallization and terminal assay."
        )
        aligned_law = {
            "law_id": "reversible_target_pathway",
            "world_interventions": [crystallization_intervention()],
        }
        misspecified_law = {"law_id": "baseline", "world_interventions": []}
    common = {
        "schema_version": "chemworld-work-ii-initial-world-model-0.4",
        "locus": "structural_mechanistic",
        "confidence": 0.70,
        "intervention_families": list(spec["intervention_families"]),
        "scope_limit": (
            "This is an incomplete local law. Public experimental evidence is authoritative."
        ),
    }
    return {
        "opaque": {
            **common,
            "availability": "opaque_for_target_locus",
            "claim": None,
            "executable_law": None,
        },
        "aligned_nominal": {
            **common,
            "availability": "supplied_incomplete_executable_law",
            "claim": aligned_claim,
            "executable_law": aligned_law,
        },
        "misindexed_nominal": {
            **common,
            "availability": "supplied_incomplete_executable_law",
            "claim": misspecified_claim,
            "executable_law": misspecified_law,
        },
    }


def effect_gate(candidate_id: str, metric: str) -> float:
    spec = candidate_specs()[candidate_id]
    return max(
        float(spec["effect_floor"]),
        float(spec["noise_multiplier"]) * float(spec["declared_sigma"][metric]),
    )


def _pairs(
    candidate_id: str, rows: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    spec = candidate_specs()[candidate_id]
    pairs = []
    for coordinate in registered_coordinates(candidate_id):
        selected = [
            row for row in rows if row.get("coordinate_id") == coordinate["coordinate_id"]
        ]
        laws = {str(row.get("law_id")): row for row in selected}
        if len(selected) != LAWS_PER_COORDINATE or set(laws) != set(spec["law_ids"]):
            raise ValueError(
                f"{candidate_id}/{coordinate['coordinate_id']} lacks exactly two registered laws"
            )
        pairs.append({**coordinate, "laws": laws})
    return pairs


def denominators(rows: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    return {
        "planned_primary_executions": PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD,
        "attempted_primary_executions": len(rows),
        "completed_primary_executions": sum(row.get("status") == "completed" for row in rows),
        "physical_failures": sum(row.get("status") == "physical_failure" for row in rows),
        "platform_failures": sum(row.get("status") == "platform_failure" for row in rows),
        "unsafe_completed": sum(
            row.get("status") == "completed" and row.get("safe") is False for row in rows
        ),
        "exact_replays": sum(row.get("exact_replay") is True for row in rows),
    }


def _registered_bindings(
    candidate_id: str, world_seed: int, rows: Sequence[Mapping[str, Any]]
) -> bool:
    coordinates = {
        row["coordinate_id"]: row for row in registered_coordinates(candidate_id)
    }
    try:
        return all(
            row.get("candidate_id") == candidate_id
            and row.get("task_id") == candidate_specs()[candidate_id]["task_id"]
            and row.get("world_seed") == world_seed
            and row.get("coordinate_id") in coordinates
            and row.get("coordinate_sha256")
            == coordinates[str(row["coordinate_id"])]["coordinate_sha256"]
            and row.get("feature_values")
            == coordinates[str(row["coordinate_id"])]["feature_values"]
            for row in rows
        )
    except (KeyError, TypeError):
        return False


def _paired_binding_checks(pairs: Sequence[Mapping[str, Any]]) -> dict[str, bool]:
    return {
        "paired_action_plans": all(
            len({law.get("action_plan_sha256") for law in pair["laws"].values()}) == 1
            and next(iter(pair["laws"].values())).get("action_plan_sha256") is not None
            for pair in pairs
        ),
        "paired_observation_noise": all(
            len({law.get("observation_coordinate_sha256") for law in pair["laws"].values()})
            == 1
            and next(iter(pair["laws"].values())).get("observation_coordinate_sha256")
            is not None
            for pair in pairs
        ),
        "all_trajectories_hash_bound": all(
            isinstance(law.get("trajectory"), Mapping)
            and isinstance(law["trajectory"].get("path"), str)
            and isinstance(law["trajectory"].get("sha256"), str)
            for pair in pairs
            for law in pair["laws"].values()
        ),
        "paired_safety_classified": all(
            all(isinstance(law.get("safe"), bool) for law in pair["laws"].values())
            for pair in pairs
        ),
    }


def _law_binding_check(
    candidate_id: str,
    rows: Sequence[Mapping[str, Any]],
    law_audit: Mapping[str, Any],
) -> bool:
    spec = candidate_specs()[candidate_id]
    baseline, altered = spec["law_ids"]
    baseline_rows = [row for row in rows if row.get("law_id") == baseline]
    altered_rows = [row for row in rows if row.get("law_id") == altered]
    common = (
        law_audit.get("altered_hash_deterministic") is True
        and law_audit.get("mechanism_hash_changed") is True
        and law_audit.get("world_intervention") == spec["world_intervention"]
        and law_audit.get("registered_law_ids") == list(spec["law_ids"])
    )
    if candidate_id == PARTITION_CANDIDATE_ID:
        return (
            common
            and law_audit.get("only_registered_constitutive_parameter_changed") is True
            and law_audit.get("changed_domain_parameter_keys")
            == ["partition_coefficient_exponent"]
            and
            {row.get("intervention_hash") for row in baseline_rows} == {None}
            and {row.get("intervention_hash") for row in altered_rows}
            == {law_audit.get("altered_intervention_hash")}
            and {row.get("mechanism_hash") for row in rows}
            == {
                law_audit.get("baseline_mechanism_hash"),
                law_audit.get("altered_mechanism_hash"),
            }
        )
    return (
        common
        and law_audit.get("transform_id") == "reversible_target_pathway_stress_v1"
        and {row.get("mechanism_hash") for row in baseline_rows}
        == {law_audit.get("baseline_mechanism_hash")}
        and {row.get("mechanism_hash") for row in altered_rows}
        == {law_audit.get("altered_mechanism_hash")}
        and law_audit.get("added_reaction_count") == 1
    )


def analyze_candidate_world(
    candidate_id: str,
    world_seed: int,
    rows: Sequence[Mapping[str, Any]],
    law_audit: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply Q1 coverage and Q2 actual-law identifiability gates."""

    spec = candidate_specs()[candidate_id]
    checks: dict[str, bool] = {
        "registered_world": world_seed in WORLD_SEEDS,
        "fixed_primary_denominator": len(rows) == PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD,
        "all_outcomes_classified": all(
            row.get("status") in {"completed", "physical_failure", "platform_failure"}
            for row in rows
        ),
        "all_primary_executions_completed": all(row.get("status") == "completed" for row in rows),
        "zero_physical_failures": not any(row.get("status") == "physical_failure" for row in rows),
        "zero_platform_failures": not any(row.get("status") == "platform_failure" for row in rows),
        "all_exact_replays": all(row.get("exact_replay") is True for row in rows),
        "registered_coordinate_bindings": _registered_bindings(candidate_id, world_seed, rows),
        "executable_law_binding": _law_binding_check(candidate_id, rows, law_audit),
        "participant_visible_leakage_free": not any(
            row.get("participant_visible_leakage_matches") for row in rows
        ),
    }
    try:
        pairs = _pairs(candidate_id, rows)
    except (KeyError, TypeError, ValueError):
        pairs = []
        checks["complete_paired_law_roster"] = False
    else:
        checks["complete_paired_law_roster"] = len(pairs) == COORDINATES_PER_CANDIDATE_WORLD
        checks.update(_paired_binding_checks(pairs))
    if not all(checks.values()):
        return {
            "candidate_id": candidate_id,
            "world_seed": world_seed,
            "passed": False,
            "checks": checks,
            "failures": sorted(key for key, passed in checks.items() if not passed),
            "denominators": denominators(rows),
            "law_audit": dict(law_audit),
            "q1": None,
            "q2": None,
        }

    baseline_law, altered_law = spec["law_ids"]
    q1_pairs = [pair for pair in pairs if pair["phase"] == "q1_coverage"]
    q2_ids = {row["coordinate_id"] for row in selected_q2_queries(candidate_id)}
    q2_pairs = [pair for pair in pairs if pair["coordinate_id"] in q2_ids]
    q1_family_counts = {
        family: sum(pair["intervention_family"] == family for pair in q1_pairs)
        for family in spec["intervention_families"]
    }
    finite = all(
        all(
            math.isfinite(float(law["metrics"][metric]))
            for metric in spec["metric_ids"]
        )
        for pair in pairs
        for law in pair["laws"].values()
    )
    family_reports: dict[str, Any] = {}
    resolved_metrics: set[str] = set()
    for family in spec["intervention_families"]:
        selected = [pair for pair in q2_pairs if pair["intervention_family"] == family]
        query_reports = []
        supporting = 0
        for pair in selected:
            metric_gaps = {
                metric: float(pair["laws"][altered_law]["metrics"][metric])
                - float(pair["laws"][baseline_law]["metrics"][metric])
                for metric in spec["metric_ids"]
            }
            passed_metrics = [
                metric
                for metric, gap in metric_gaps.items()
                if abs(gap) >= effect_gate(candidate_id, metric)
            ]
            resolved_metrics.update(passed_metrics)
            is_supporting = bool(passed_metrics)
            supporting += is_supporting
            query_reports.append(
                {
                    "coordinate_id": pair["coordinate_id"],
                    "coordinate_sha256": pair["coordinate_sha256"],
                    "metric_gaps": metric_gaps,
                    "passed_metrics": passed_metrics,
                    "supports_law_contrast": is_supporting,
                    "candidate_predictions": {
                        "blind_law_a": dict(pair["laws"][baseline_law]["metrics"]),
                        "blind_law_b": dict(pair["laws"][altered_law]["metrics"]),
                    },
                    "altered_world_observation": dict(
                        pair["laws"][altered_law]["metrics"]
                    ),
                }
            )
        family_reports[family] = {
            "selected_query_count": len(selected),
            "supporting_query_count": supporting,
            "passed": len(selected) == Q2_QUERY_COUNT_PER_FAMILY
            and supporting >= MINIMUM_SUPPORT_PER_Q2_FAMILY,
            "queries": query_reports,
        }

    q2_roster = selected_q2_queries(candidate_id)
    q2 = {
        "selection_policy": "coordinate_only_even_spread_within_each_frozen_heldout_family",
        "selection_reads_outcomes": False,
        "query_count": len(q2_pairs),
        "query_roster_sha256": canonical_json_sha256(q2_roster),
        "candidate_laws": {
            "blind_law_a": {
                "registered_law_id": baseline_law,
                "world_interventions": [],
                "prediction_source": "direct_provider_free_execution",
            },
            "blind_law_b": {
                "registered_law_id": altered_law,
                "world_interventions": [spec["world_intervention"]],
                "prediction_source": "direct_provider_free_execution",
            },
        },
        "truth_law_id": altered_law,
        "blind_identified_truth_law": "blind_law_b",
        "family_reports": family_reports,
        "resolved_metrics": sorted(resolved_metrics),
    }
    q1 = {
        "coverage_coordinate_count": len(q1_pairs),
        "family_coordinate_counts": q1_family_counts,
        "all_metrics_finite": finite,
        "paired_law_execution_count": 2 * len(q1_pairs),
    }
    checks.update(
        {
            "q1_fixed_coverage": len(q1_pairs) == 384
            and set(q1_family_counts.values()) == {Q1_COORDINATES_PER_FAMILY},
            "all_registered_metrics_finite": finite,
            "q2_outcome_blind_selection": q2["selection_reads_outcomes"] is False,
            "q2_fixed_query_denominator": len(q2_pairs) == Q2_QUERY_COUNT_PER_CANDIDATE,
            "both_intervention_families_resolve_laws": all(
                report["passed"] for report in family_reports.values()
            ),
            "multiple_metrics_resolve_laws": len(resolved_metrics)
            >= MINIMUM_RESOLVED_METRICS_PER_WORLD,
            "actual_registered_laws_compared": all(
                candidate["prediction_source"] == "direct_provider_free_execution"
                for candidate in q2["candidate_laws"].values()
            ),
        }
    )
    return {
        "candidate_id": candidate_id,
        "world_seed": world_seed,
        "passed": all(checks.values()),
        "checks": checks,
        "failures": sorted(key for key, passed in checks.items() if not passed),
        "denominators": denominators(rows),
        "law_audit": dict(law_audit),
        "q1": q1,
        "q2": q2,
    }


def report_sha256(report: Mapping[str, Any]) -> str:
    return canonical_json_sha256(
        {key: value for key, value in report.items() if key != "report_sha256"}
    )


def summary_sha256(summary: Mapping[str, Any]) -> str:
    return canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )


def validate_world_report(report: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("schema_version") != WORLD_REPORT_VERSION:
        errors.append("unexpected A-S world-report schema")
    if report.get("qualification_schema_version") != QUALIFICATION_VERSION:
        errors.append("A-S qualification schema mismatch")
    if report.get("formal_result") is not False:
        errors.append("A-S qualification must not be formal")
    if report.get("provider_call_count") != 0 or report.get("participant_session_count") != 0:
        errors.append("A-S qualification must remain provider-free")
    if report.get("report_sha256") != report_sha256(report):
        errors.append("A-S world-report self-hash mismatch")
    candidate_id = report.get("candidate_id")
    world_seed = report.get("world_seed")
    rows = report.get("rows")
    audit = report.get("law_audit")
    if (
        candidate_id not in CANDIDATE_IDS
        or world_seed not in WORLD_SEEDS
        or not isinstance(rows, list)
        or not isinstance(audit, Mapping)
    ):
        errors.append("A-S world report lacks a registered candidate/world/rows/audit")
    else:
        try:
            rebuilt = analyze_candidate_world(str(candidate_id), int(world_seed), rows, audit)
        except (KeyError, TypeError, ValueError) as error:
            errors.append(f"A-S world analysis cannot be rebuilt: {error}")
        else:
            if report.get("analysis") != rebuilt:
                errors.append("A-S world analysis mismatch")
    return errors


def validate_summary(
    root: Path,
    summary: Mapping[str, Any],
    *,
    expected_source_binding: Mapping[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if summary.get("schema_version") != SUMMARY_VERSION:
        errors.append("unexpected A-S five-world summary schema")
    if summary.get("qualification_schema_version") != QUALIFICATION_VERSION:
        errors.append("A-S five-world qualification schema mismatch")
    if summary.get("summary_sha256") != summary_sha256(summary):
        errors.append("A-S five-world summary self-hash mismatch")
    if summary.get("formal_result") is not False:
        errors.append("A-S five-world summary must not be formal")
    if summary.get("provider_call_count") != 0 or summary.get("participant_session_count") != 0:
        errors.append("A-S five-world summary must remain provider-free")
    expected_coverage = {
        "candidate_count": 2,
        "worlds_per_candidate": 5,
        "coordinates_per_candidate_world": COORDINATES_PER_CANDIDATE_WORLD,
        "laws_per_coordinate": LAWS_PER_COORDINATE,
        "primary_executions_per_candidate_world": PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD,
        "planned_primary_execution_count": PRIMARY_EXECUTIONS_TOTAL,
        "planned_exact_replay_count": EXACT_REPLAYS_TOTAL,
        "q2_queries_per_candidate_world": Q2_QUERY_COUNT_PER_CANDIDATE,
    }
    if summary.get("coverage") != expected_coverage:
        errors.append("A-S five-world coverage mismatch")
    source_binding = summary.get("c2_source_binding")
    errors.extend(validate_c2_source_binding(root, source_binding))
    if expected_source_binding is not None and source_binding != expected_source_binding:
        errors.append("A-S C2 source binding differs from the required cohort")
    raw_bindings = summary.get("raw_bindings")
    if not isinstance(raw_bindings, list) or len(raw_bindings) != 10:
        errors.append("A-S summary must bind all ten candidate-world reports")
    else:
        seen: set[tuple[str, int]] = set()
        for binding in raw_bindings:
            try:
                path = (root / str(binding["path"])).resolve()
                path.relative_to(root.resolve())
                if not path.is_file():
                    raise ValueError("world report is missing")
                if binding.get("sha256") != file_sha256(path):
                    errors.append("A-S raw world-report file hash mismatch")
                payload = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("world report is not an object")
                errors.extend(validate_world_report(payload))
                if binding.get("report_sha256") != payload.get("report_sha256"):
                    errors.append("A-S raw embedded world-report hash mismatch")
                if payload.get("c2_source_binding") != source_binding:
                    errors.append("A-S raw/source binding mismatch")
                seen.add((str(payload["candidate_id"]), int(payload["world_seed"])))
            except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
                errors.append(f"A-S raw binding cannot be read: {error}")
        expected = {(candidate, world) for candidate in CANDIDATE_IDS for world in WORLD_SEEDS}
        if seen != expected:
            errors.append("A-S raw report roster mismatch")
    denominators_value = summary.get("denominators")
    if not isinstance(denominators_value, Mapping):
        errors.append("A-S summary lacks denominators")
    else:
        if denominators_value.get("planned_primary_executions") != PRIMARY_EXECUTIONS_TOTAL:
            errors.append("A-S primary denominator mismatch")
        if denominators_value.get("planned_exact_replays") != EXACT_REPLAYS_TOTAL:
            errors.append("A-S replay denominator mismatch")
    passed = summary.get("all_candidates_passed") is True
    if summary.get("participant_d1_configs_generated") not in ({}, None) and not passed:
        errors.append("A-S summary generated D1 configs without complete qualification")
    if summary.get("provider_execution_authorized") is not False:
        errors.append("A-S qualification cannot authorize provider execution")
    if summary.get("formal_r5_authorized") is not False:
        errors.append("A-S qualification cannot authorize formal R5")
    return errors


__all__ = [
    "CANDIDATE_IDS",
    "COORDINATES_PER_CANDIDATE_WORLD",
    "CRYSTALLIZATION_CANDIDATE_ID",
    "EXACT_REPLAYS_TOTAL",
    "PACKAGE_VERSION",
    "PARTITION_CANDIDATE_ID",
    "PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD",
    "PRIMARY_EXECUTIONS_TOTAL",
    "Q2_QUERY_COUNT_PER_CANDIDATE",
    "QUALIFICATION_VERSION",
    "SUMMARY_VERSION",
    "WORLD_REPORT_VERSION",
    "WORLD_SEEDS",
    "analyze_candidate_world",
    "build_prior_arms",
    "candidate_specs",
    "crystallization_intervention",
    "denominators",
    "effect_gate",
    "observation_binding",
    "partition_intervention",
    "registered_coordinates",
    "report_sha256",
    "selected_q2_queries",
    "summary_sha256",
    "validate_summary",
    "validate_world_report",
]
