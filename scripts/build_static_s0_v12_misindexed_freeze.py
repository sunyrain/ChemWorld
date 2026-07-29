"""Build the paired S0 v1.2 targeted-misindexed-material-information freeze."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256 as canonical_sha256
from chemworld.eval.provenance import write_json_atomic
from chemworld.materials import (
    STATIC_MATERIAL_INFORMATION_MISINDEXED,
    STATIC_MATERIAL_INFORMATION_NOMINAL,
    static_material_information_dossier,
)

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-29"
NOMINAL_MANIFEST = (
    ROOT
    / "configs"
    / "benchmark"
    / "scientific_optimization_s0_v1.1_nominal_information_freeze_manifest.json"
)
MISINDEXED_MANIFEST = (
    ROOT
    / "configs"
    / "benchmark"
    / "scientific_optimization_s0_v1.2_misindexed_information_freeze_manifest.json"
)

TRACKS = {
    "electrochemical": {
        "task_id": "electrochemical-conversion",
        "target_field": "electrolyte_profile",
        "descriptor_permutation": [0, 3, 2, 1],
        "nominal_source_action_value": 1,
        "misleading_action_value": 3,
        "nominal_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.1_"
            "electrochemical_material_nominal_20x10_formal.json"
        ),
        "misindexed_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.2_"
            "electrochemical_material_misindexed_20x10_formal.json"
        ),
        "nominal_method": (
            "configs/methods/llm_v1.1/"
            "participant_methods_s0_codex_subscription_sol_"
            "electrochemical_material_nominal_20x10_v11.json"
        ),
        "misindexed_method": (
            "configs/methods/llm_v1.2/"
            "participant_methods_s0_codex_subscription_sol_"
            "electrochemical_material_misindexed_20x10_v12.json"
        ),
        "nominal_method_id": (
            "s0_codex_subscription_sol_medium_"
            "electrochemical_material_nominal_20"
        ),
        "misindexed_method_id": (
            "s0_codex_subscription_sol_medium_"
            "electrochemical_material_misindexed_20"
        ),
        "protocol_family_id": (
            "chemworld-static-s0-electrochemical-material-misindexed-v1.2"
        ),
        "protocol_id": (
            "chemworld-static-s0-electrochemical-material-misindexed-"
            f"v1.2-20x10-{DATE}"
        ),
        "scaffold_id": (
            "direct_known_horizon_named_electrochemical_material_"
            "misindexed_full_history_predictive_v12"
        ),
        "primary_track": (
            "static_scientific_optimization_material_misindexed_horizon"
        ),
        "qualification_report": (
            "workstreams/flagship_tasks/reports/"
            "static-s0-material-family-v2-qualification-v0.3.json"
        ),
        "selection_evidence": {
            "qualification_world_seeds": list(range(100, 115)),
            "nominal_source_winner_count": 9,
            "misleading_target_winner_count": 0,
            "selection_rule": (
                "swap the most frequent qualification winner with a never-winning "
                "but reachable material while leaving the other material field correct"
            ),
        },
    },
    "crystallization": {
        "task_id": "reaction-to-crystallization",
        "target_field": "catalyst",
        "descriptor_permutation": [0, 2, 1, 3],
        "nominal_source_action_value": 1,
        "misleading_action_value": 2,
        "nominal_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.1_"
            "crystallization_material_nominal_20x10_formal.json"
        ),
        "misindexed_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.2_"
            "crystallization_material_misindexed_20x10_formal.json"
        ),
        "nominal_method": (
            "configs/methods/llm_v1.1/"
            "participant_methods_s0_codex_subscription_sol_"
            "crystallization_material_nominal_20x10_v11.json"
        ),
        "misindexed_method": (
            "configs/methods/llm_v1.2/"
            "participant_methods_s0_codex_subscription_sol_"
            "crystallization_material_misindexed_20x10_v12.json"
        ),
        "nominal_method_id": (
            "s0_codex_subscription_sol_medium_"
            "crystallization_material_nominal_20"
        ),
        "misindexed_method_id": (
            "s0_codex_subscription_sol_medium_"
            "crystallization_material_misindexed_20"
        ),
        "protocol_family_id": (
            "chemworld-static-s0-crystallization-material-misindexed-v1.2"
        ),
        "protocol_id": (
            "chemworld-static-s0-crystallization-material-misindexed-"
            f"v1.2-20x10-{DATE}"
        ),
        "scaffold_id": (
            "direct_known_horizon_named_crystallization_material_"
            "misindexed_full_history_predictive_v12"
        ),
        "primary_track": (
            "static_scientific_optimization_"
            "crystallization_material_misindexed_horizon"
        ),
        "qualification_report": (
            "workstreams/flagship_tasks/reports/"
            "static-s0-crystallization-material-family-v1-qualification-v0.1.json"
        ),
        "selection_evidence": {
            "qualification_world_seeds": list(range(100, 115)),
            "standardized_nominal_source_is_a_winner": True,
            "standardized_misleading_target_is_a_winner": False,
            "selection_rule": (
                "swap a standardized-design winner with the only catalyst absent "
                "from the qualification winners while leaving solvent information correct"
            ),
        },
    },
}


def _load(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    if not target.is_absolute():
        target = ROOT / target
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {target}")
    return payload


def _material_family_id(protocol: dict[str, Any], task_id: str) -> str:
    world_policy = protocol["world_policy"]
    key = (
        "crystallization_material_family_id"
        if task_id == "reaction-to-crystallization"
        else "electrochemical_material_family_id"
    )
    return str(world_policy[key])


def _misindexed_protocol(track: dict[str, Any]) -> dict[str, Any]:
    protocol = copy.deepcopy(_load(track["nominal_protocol"]))
    protocol.update(
        {
            "schema_version": (
                "chemworld-static-scientific-optimization-protocol-1.2-s0"
            ),
            "protocol_family_id": track["protocol_family_id"],
            "protocol_id": track["protocol_id"],
            "condition_id": STATIC_MATERIAL_INFORMATION_MISINDEXED,
            "material_information": {
                "mode": STATIC_MATERIAL_INFORMATION_MISINDEXED,
                "target_field": track["target_field"],
                "descriptor_permutation": track["descriptor_permutation"],
            },
            "method_config_path": track["misindexed_method"],
            "method_ids": [track["misindexed_method_id"]],
        }
    )
    protocol["information_intervention"] = {
        "estimand": (
            "paired world-level change caused by a fixed targeted misindexing "
            "of one anonymous material-property field"
        ),
        "paired_nominal_protocol_path": track["nominal_protocol"],
        "paired_opaque_protocol_path": protocol["information_intervention"][
            "paired_opaque_protocol_path"
        ],
        "paired_world_seeds": list(range(10)),
        "same_model": True,
        "same_reasoning_effort": True,
        "same_exploration_budget": True,
        "same_measurement_interface": True,
        "same_observation_noise_namespace": True,
        "world_and_outcome_law_unchanged": True,
        "only_scientific_information_change": (
            f"{track['target_field']} nominal property rows "
            f"{track['nominal_source_action_value']} and "
            f"{track['misleading_action_value']} are transposed; all other "
            "dossier rows are unchanged"
        ),
    }
    protocol["objective"] = (
        str(protocol["objective"])
        .replace("material-nominal", "material-misindexed")
        .replace(
            "paired information-value extension",
            "paired wrong-prior recovery stress test",
        )
    )
    return protocol


def _misindexed_methods(track: dict[str, Any]) -> dict[str, Any]:
    methods = copy.deepcopy(_load(track["nominal_method"]))
    source = methods["methods"].pop(track["nominal_method_id"])
    methods.update(
        {
            "schema_version": (
                "chemworld-static-scientific-optimization-methods-1.2-s0"
            ),
            "freeze_id": (
                f"chemworld-static-s0-codex-subscription-sol-"
                f"{track['task_id']}-material-misindexed-20x10-v1.2-{DATE}"
            ),
        }
    )
    methods["architecture_candidate"].update(
        {
            "primary_track": track["primary_track"],
            "material_information": STATIC_MATERIAL_INFORMATION_MISINDEXED,
            "paired_nominal_control": track["nominal_method"],
        }
    )
    source["static_optimization_scaffold_id"] = track["scaffold_id"]
    source["static_optimization_prompt_budget_contract"][
        "preflight_status"
    ] = "passed_misindexed_full_20_round_mock_and_exact_replay_2026_07_29"
    methods["methods"] = {track["misindexed_method_id"]: source}
    return methods


def _assert_public_blindness(
    *,
    protocol: dict[str, Any],
    track: dict[str, Any],
) -> dict[str, Any]:
    task_id = track["task_id"]
    family_id = _material_family_id(protocol, task_id)
    misindexed = static_material_information_dossier(
        protocol["material_information"],
        task_id=task_id,
        material_family_id=family_id,
    )
    nominal = static_material_information_dossier(
        {"mode": STATIC_MATERIAL_INFORMATION_NOMINAL},
        task_id=task_id,
        material_family_id=family_id,
    )
    if misindexed is None or nominal is None:
        raise RuntimeError("material dossier unexpectedly missing")
    serialized = json.dumps(misindexed, sort_keys=True).lower()
    forbidden = ("misindexed", "permutation", "target_field", "shuffled")
    if any(term in serialized for term in forbidden):
        raise RuntimeError("public dossier leaks the information intervention")
    target_field = track["target_field"]
    permutation = track["descriptor_permutation"]
    expected_target_rows = [
        nominal["choices"][target_field][source]["nominal_properties"]
        for source in permutation
    ]
    actual_target_rows = [
        row["nominal_properties"]
        for row in misindexed["choices"][target_field]
    ]
    if actual_target_rows != expected_target_rows:
        raise RuntimeError("target dossier rows do not match the frozen transposition")
    for field in nominal["choices"]:
        if field == target_field:
            continue
        if misindexed["choices"][field] != nominal["choices"][field]:
            raise RuntimeError(f"non-target field changed unexpectedly: {field}")
    return misindexed


def build_freeze() -> dict[str, Any]:
    nominal_manifest = _load(NOMINAL_MANIFEST)
    nominal_tracks = {
        str(track["track_id"]): track
        for track in nominal_manifest["participant_tracks"]
    }
    participant_tracks = []
    for track_id, track in TRACKS.items():
        nominal_track = nominal_tracks[track_id]
        protocol = _misindexed_protocol(track)
        methods = _misindexed_methods(track)
        protocol_path = ROOT / track["misindexed_protocol"]
        method_path = ROOT / track["misindexed_method"]
        write_json_atomic(protocol_path, protocol)
        write_json_atomic(method_path, methods)
        dossier = _assert_public_blindness(protocol=protocol, track=track)
        qualification = _load(track["qualification_report"])
        participant_tracks.append(
            {
                "track_id": track_id,
                "task_id": track["task_id"],
                "protocol_path": track["misindexed_protocol"],
                "protocol_sha256": canonical_sha256(protocol),
                "method_path": track["misindexed_method"],
                "method_sha256": canonical_sha256(methods),
                "method_id": track["misindexed_method_id"],
                "world_understanding_reference_path": nominal_track[
                    "world_understanding_reference_path"
                ],
                "world_understanding_reference_sha256": nominal_track[
                    "world_understanding_reference_sha256"
                ],
                "material_information_contract_version": dossier[
                    "contract_version"
                ],
                "material_information_sha256": canonical_sha256(dossier),
                "misindexing_contract": {
                    "target_field": track["target_field"],
                    "source_index_by_action_value": track[
                        "descriptor_permutation"
                    ],
                    "nominal_source_action_value": track[
                        "nominal_source_action_value"
                    ],
                    "misleading_action_value": track[
                        "misleading_action_value"
                    ],
                    "fixed_across_worlds": True,
                    "single_two_row_transposition": True,
                    "non_target_material_field_remains_correct": True,
                    "selection_evidence": track["selection_evidence"],
                    "qualification_report_path": track[
                        "qualification_report"
                    ],
                    "qualification_report_sha256": canonical_sha256(
                        qualification
                    ),
                },
                "paired_nominal_protocol_path": track["nominal_protocol"],
                "paired_nominal_method_path": track["nominal_method"],
                "provider": "codex_subscription",
                "model_id": "gpt-5.6-sol",
                "reasoning_effort": "medium",
                "world_count": 10,
                "exploration_rounds_per_world": 20,
                "predictive_physical_experiments_per_world": 12,
                "blind_validation_experiments_per_world": 6,
            }
        )
    baseline_tracks = copy.deepcopy(nominal_manifest["baseline_tracks"])
    for track in baseline_tracks:
        track["reuse_only"] = True
        track["reuse_reason"] = (
            "same worlds and outcome contract; the information intervention "
            "does not require baseline reruns"
        )
    manifest = {
        "schema_version": (
            "chemworld-static-s0-misindexed-information-freeze-manifest-1.0"
        ),
        "freeze_id": (
            f"chemworld-static-s0-two-flagships-misindexed-information-v1.2-{DATE}"
        ),
        "status": "owner_authorized_frozen_formal_pending_execution",
        "formal_result": True,
        "benchmark_claim_allowed": False,
        "source_commit_binding": "recorded_by_campaign_orchestrator_at_execution",
        "freeze_timing": (
            "frozen after the v1.1 nominal campaign completed but before any "
            "v1.2 provider call"
        ),
        "world_seeds": list(range(10)),
        "participant_tracks": participant_tracks,
        "baseline_tracks": baseline_tracks,
        "paired_opaque_evidence": nominal_manifest["paired_opaque_evidence"],
        "paired_nominal_evidence": {
            "campaign_root": (
                "runs/formal/static-s0-v11-nominal-codex-subscription-20260729"
            ),
            "campaign_index": (
                "runs/formal/static-s0-v11-nominal-codex-subscription-20260729/"
                "campaign_execution_index.json"
            ),
            "freeze_manifest": str(NOMINAL_MANIFEST.relative_to(ROOT)),
            "freeze_manifest_sha256": canonical_sha256(nominal_manifest),
        },
        "planned_accounting": {
            "new_participant_world_cells": 20,
            "new_participant_provider_calls": 420,
            "new_participant_exploration_experiments": 400,
            "new_participant_predictive_physical_experiments": 240,
            "new_participant_blind_validation_experiments": 120,
            "new_participant_total_physical_experiments": 760,
            "reused_nominal_participant_world_cells": 20,
            "reused_opaque_participant_world_cells": 20,
            "newly_executed_baseline_cells": 0,
        },
        "preflight": {
            "status": "passed",
            "provider": "mock",
            "world_seed": 0,
            "participant_cells": 2,
            "exploration_rounds_per_cell": 20,
            "physical_experiments_per_cell": 38,
            "provider_calls_per_cell": 21,
            "all_cells_exact_replay_verified": True,
            "output_root": (
                "runs/development/"
                "static-s0-v12-misindexed-mock-preflight-20260729"
            ),
        },
        "confirmatory_analysis": {
            "unit": "independent_world",
            "pairing_key": "task_id_and_world_seed",
            "primary_estimand_by_task": (
                "paired_world_mean(misindexed_blind_score - nominal_blind_score)"
            ),
            "secondary_net_harm_estimand_by_task": (
                "paired_world_mean(misindexed_blind_score - opaque_blind_score)"
            ),
            "primary_familywise_interval": (
                "paired_world_bootstrap_97.5_percent_per_task_"
                "for_two_task_bonferroni_family"
            ),
            "bootstrap_resamples": 100000,
            "random_seed": 20260729,
            "wrong_prior_cost": (
                "primary_familywise_interval_upper_bound_less_than_zero"
            ),
            "wrong_prior_benefit": (
                "primary_familywise_interval_lower_bound_greater_than_zero"
            ),
            "otherwise": "inconclusive",
        },
        "recovery_analysis": {
            "exploration_action_source": (
                "public_history.plan.recipe_parameters[target_field]"
            ),
            "early_round_indices_zero_based": [0, 1, 2, 3, 4],
            "late_round_indices_zero_based": [15, 16, 17, 18, 19],
            "manipulation_check": (
                "paired early misleading-action share: misindexed - nominal"
            ),
            "differential_action_correction": (
                "(misindexed late-minus-early misleading-action share) - "
                "(nominal late-minus-early misleading-action share)"
            ),
            "action_recovery_rule": (
                "97.5_percent_familywise_upper_bound_of_"
                "differential_action_correction_less_than_zero"
            ),
            "practical_score_margin": 0.05,
            "performance_recovery_to_opaque_rule": (
                "97.5_percent_one_sided_familywise_lower_bound_of_"
                "misindexed_minus_opaque_greater_than_or_equal_to_-0.05"
            ),
            "full_restoration_to_nominal_rule": (
                "97.5_percent_one_sided_familywise_lower_bound_of_"
                "misindexed_minus_nominal_greater_than_or_equal_to_-0.05"
            ),
            "overall_recovery_claim": (
                "requires manipulation check, differential action correction, "
                "and performance recovery to opaque; otherwise report components "
                "without a recovery claim"
            ),
        },
        "reporting_boundaries": {
            **nominal_manifest["reporting_boundaries"],
            "primary_endpoint": (
                "paired_blind_validated_final_recommendation_score_mean"
            ),
            "intervention_scope": (
                "one fixed targeted whole-row transposition per task"
            ),
            "post_nominal_sequential_extension": True,
            "world_specific_adversarial_mapping": False,
            "provider_causal_effect_claim_allowed": False,
            "broad_recovery_generalization_claim_allowed": False,
        },
    }
    write_json_atomic(MISINDEXED_MANIFEST, manifest)
    return manifest


def main() -> None:
    manifest = build_freeze()
    print(
        json.dumps(
            {
                "manifest": str(MISINDEXED_MANIFEST.relative_to(ROOT)),
                "freeze_sha256": canonical_sha256(manifest),
                "participant_track_count": len(
                    manifest["participant_tracks"]
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
