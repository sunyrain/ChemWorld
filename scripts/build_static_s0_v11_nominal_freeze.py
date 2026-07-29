"""Build the paired S0 v1.1 correct-anonymous-material-information freeze."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256 as canonical_sha256,
)
from chemworld.eval.provenance import (
    write_json_atomic,
)
from chemworld.materials import static_material_information_dossier

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-29"
OPAQUE_MANIFEST = (
    ROOT
    / "configs"
    / "benchmark"
    / "scientific_optimization_s0_v1.0_freeze_manifest.json"
)
NOMINAL_MANIFEST = (
    ROOT
    / "configs"
    / "benchmark"
    / "scientific_optimization_s0_v1.1_nominal_information_freeze_manifest.json"
)

TRACKS = {
    "electrochemical": {
        "task_id": "electrochemical-conversion",
        "opaque_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.0_"
            "electrochemical_material_opaque_20x10_formal.json"
        ),
        "nominal_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.1_"
            "electrochemical_material_nominal_20x10_formal.json"
        ),
        "opaque_method": (
            "configs/methods/llm_v1.0/"
            "participant_methods_s0_codex_subscription_sol_"
            "electrochemical_material_opaque_20x10_v10.json"
        ),
        "nominal_method": (
            "configs/methods/llm_v1.1/"
            "participant_methods_s0_codex_subscription_sol_"
            "electrochemical_material_nominal_20x10_v11.json"
        ),
        "opaque_method_id": (
            "s0_codex_subscription_sol_medium_"
            "electrochemical_material_opaque_20"
        ),
        "nominal_method_id": (
            "s0_codex_subscription_sol_medium_"
            "electrochemical_material_nominal_20"
        ),
        "protocol_family_id": (
            "chemworld-static-s0-electrochemical-material-nominal-v1.1"
        ),
        "protocol_id": (
            "chemworld-static-s0-electrochemical-material-nominal-"
            f"v1.1-20x10-{DATE}"
        ),
        "scaffold_id": (
            "direct_known_horizon_named_electrochemical_material_"
            "nominal_full_history_predictive_v11"
        ),
        "primary_track": (
            "static_scientific_optimization_material_nominal_horizon"
        ),
        "reference": (
            "configs/benchmark/"
            "world_understanding_s0_electrochemical_material_v1.0.json"
        ),
    },
    "crystallization": {
        "task_id": "reaction-to-crystallization",
        "opaque_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.0_"
            "crystallization_material_opaque_20x10_formal.json"
        ),
        "nominal_protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v1.1_"
            "crystallization_material_nominal_20x10_formal.json"
        ),
        "opaque_method": (
            "configs/methods/llm_v1.0/"
            "participant_methods_s0_codex_subscription_sol_"
            "crystallization_material_opaque_20x10_v10.json"
        ),
        "nominal_method": (
            "configs/methods/llm_v1.1/"
            "participant_methods_s0_codex_subscription_sol_"
            "crystallization_material_nominal_20x10_v11.json"
        ),
        "opaque_method_id": (
            "s0_codex_subscription_sol_medium_"
            "crystallization_material_opaque_20"
        ),
        "nominal_method_id": (
            "s0_codex_subscription_sol_medium_"
            "crystallization_material_nominal_20"
        ),
        "protocol_family_id": (
            "chemworld-static-s0-crystallization-material-nominal-v1.1"
        ),
        "protocol_id": (
            "chemworld-static-s0-crystallization-material-nominal-"
            f"v1.1-20x10-{DATE}"
        ),
        "scaffold_id": (
            "direct_known_horizon_named_crystallization_material_"
            "nominal_full_history_predictive_v11"
        ),
        "primary_track": (
            "static_scientific_optimization_"
            "crystallization_material_nominal_horizon"
        ),
        "reference": (
            "configs/benchmark/"
            "world_understanding_s0_crystallization_material_v1.0.json"
        ),
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


def _nominal_protocol(track: dict[str, str]) -> dict[str, Any]:
    protocol = copy.deepcopy(_load(track["opaque_protocol"]))
    protocol.update(
        {
            "schema_version": (
                "chemworld-static-scientific-optimization-protocol-1.1-s0"
            ),
            "protocol_family_id": track["protocol_family_id"],
            "protocol_id": track["protocol_id"],
            "condition_id": "anonymous_nominal_properties",
            "material_information": {
                "mode": "anonymous_nominal_properties",
            },
            "method_config_path": track["nominal_method"],
            "method_ids": [track["nominal_method_id"]],
        }
    )
    protocol["information_intervention"] = {
        "estimand": (
            "paired world-level change caused by adding correct anonymous "
            "nominal material properties to the otherwise unchanged public context"
        ),
        "paired_opaque_protocol_path": track["opaque_protocol"],
        "paired_world_seeds": list(range(10)),
        "same_model": True,
        "same_reasoning_effort": True,
        "same_exploration_budget": True,
        "same_measurement_interface": True,
        "same_observation_noise_namespace": True,
        "only_scientific_information_change": (
            "material_information.mode: opaque_codes -> "
            "anonymous_nominal_properties"
        ),
    }
    protocol["objective"] = (
        str(protocol["objective"]).replace("material-opaque", "material-nominal")
        + "; paired information-value extension"
    )
    return protocol


def _nominal_methods(track: dict[str, str]) -> dict[str, Any]:
    methods = copy.deepcopy(_load(track["opaque_method"]))
    source = methods["methods"].pop(track["opaque_method_id"])
    methods.update(
        {
            "schema_version": (
                "chemworld-static-scientific-optimization-methods-1.1-s0"
            ),
            "freeze_id": (
                f"chemworld-static-s0-codex-subscription-sol-"
                f"{track['task_id']}-material-nominal-20x10-v1.1-{DATE}"
            ),
        }
    )
    architecture = methods["architecture_candidate"]
    architecture.update(
        {
            "primary_track": track["primary_track"],
            "material_information": "anonymous_nominal_properties",
            "paired_opaque_control": track["opaque_method"],
        }
    )
    source["static_optimization_scaffold_id"] = track["scaffold_id"]
    source["static_optimization_prompt_budget_contract"][
        "preflight_status"
    ] = "passed_nominal_full_20_round_mock_and_exact_replay_2026_07_29"
    methods["methods"] = {track["nominal_method_id"]: source}
    return methods


def build_freeze() -> dict[str, Any]:
    opaque_manifest = _load(OPAQUE_MANIFEST)
    participant_tracks: list[dict[str, Any]] = []
    for track_id, track in TRACKS.items():
        protocol = _nominal_protocol(track)
        methods = _nominal_methods(track)
        protocol_path = ROOT / track["nominal_protocol"]
        method_path = ROOT / track["nominal_method"]
        write_json_atomic(protocol_path, protocol)
        write_json_atomic(method_path, methods)
        reference = _load(track["reference"])
        world_policy = protocol["world_policy"]
        material_family_id = (
            world_policy["crystallization_material_family_id"]
            if track["task_id"] == "reaction-to-crystallization"
            else world_policy["electrochemical_material_family_id"]
        )
        dossier = static_material_information_dossier(
            protocol["material_information"],
            task_id=track["task_id"],
            material_family_id=material_family_id,
        )
        if dossier is None:
            raise RuntimeError("nominal freeze did not build a material dossier")
        participant_tracks.append(
            {
                "track_id": track_id,
                "task_id": track["task_id"],
                "protocol_path": track["nominal_protocol"],
                "protocol_sha256": canonical_sha256(protocol),
                "method_path": track["nominal_method"],
                "method_sha256": canonical_sha256(methods),
                "world_understanding_reference_path": track["reference"],
                "world_understanding_reference_sha256": canonical_sha256(
                    reference
                ),
                "method_id": track["nominal_method_id"],
                "material_information_contract_version": dossier[
                    "contract_version"
                ],
                "material_information_sha256": canonical_sha256(dossier),
                "paired_opaque_protocol_path": track["opaque_protocol"],
                "paired_opaque_method_path": track["opaque_method"],
                "provider": "codex_subscription",
                "model_id": "gpt-5.6-sol",
                "reasoning_effort": "medium",
                "world_count": 10,
                "exploration_rounds_per_world": 20,
                "predictive_physical_experiments_per_world": 12,
                "blind_validation_experiments_per_world": 6,
            }
        )
    baseline_tracks = copy.deepcopy(opaque_manifest["baseline_tracks"])
    for track in baseline_tracks:
        track["reuse_only"] = True
        track["reuse_reason"] = (
            "same worlds and outcome contract; no baseline rerun is needed "
            "for the participant information intervention"
        )
    manifest = {
        "schema_version": (
            "chemworld-static-s0-nominal-information-freeze-manifest-1.0"
        ),
        "freeze_id": (
            f"chemworld-static-s0-two-flagships-nominal-information-v1.1-{DATE}"
        ),
        "status": "owner_authorized_frozen_formal_pending_execution",
        "formal_result": True,
        "benchmark_claim_allowed": False,
        "source_commit_binding": "recorded_by_campaign_orchestrator_at_execution",
        "world_seeds": list(range(10)),
        "participant_tracks": participant_tracks,
        "baseline_tracks": baseline_tracks,
        "paired_opaque_evidence": {
            "campaign_root": (
                "runs/formal/static-s0-v10-codex-subscription-20260729"
            ),
            "campaign_index": (
                "runs/formal/static-s0-v10-codex-subscription-20260729/"
                "campaign_execution_index.json"
            ),
            "formal_summary": (
                "workstreams/flagship_tasks/reports/"
                "static-s0-v1.0-formal-campaign-summary.json"
            ),
        },
        "planned_accounting": {
            "new_participant_world_cells": 20,
            "new_participant_provider_calls": 420,
            "new_participant_exploration_experiments": 400,
            "new_participant_predictive_physical_experiments": 240,
            "new_participant_blind_validation_experiments": 120,
            "new_participant_total_physical_experiments": 760,
            "reused_opaque_participant_world_cells": 20,
            "reused_classic_baseline_cells": 1050,
            "newly_executed_baseline_cells": 0,
        },
        "confirmatory_analysis": {
            "primary_estimand_by_task": (
                "paired_world_mean(nominal_blind_score - opaque_blind_score)"
            ),
            "pairing_key": "task_id_and_world_seed",
            "nominal_interval": "paired_world_bootstrap_95_percent",
            "familywise_interval": (
                "paired_world_bootstrap_97.5_percent_per_task_"
                "for_two_task_bonferroni_family"
            ),
            "bootstrap_resamples": 100000,
            "random_seed": 20260729,
            "positive_information_value": (
                "familywise_interval_lower_bound_greater_than_zero"
            ),
            "harmful_information": (
                "familywise_interval_upper_bound_less_than_zero"
            ),
            "otherwise": "inconclusive",
        },
        "reporting_boundaries": {
            "primary_endpoint": (
                "paired_blind_validated_final_recommendation_score_mean"
            ),
            "material_properties": (
                "anonymous_nominal_family_level_priors_only"
            ),
            "hidden_world_residuals_supplied": False,
            "real_material_identity_claim_allowed": False,
            "sampled_world_scope_only": True,
            "provider_causal_effect_claim_allowed": False,
            "broad_generalization_claim_allowed": False,
            "opaque_v1_0_freeze_mutated": False,
        },
    }
    write_json_atomic(NOMINAL_MANIFEST, manifest)
    return manifest


def main() -> None:
    manifest = build_freeze()
    print(
        json.dumps(
            {
                "manifest": str(NOMINAL_MANIFEST.relative_to(ROOT)),
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
