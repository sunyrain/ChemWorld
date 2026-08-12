#!/usr/bin/env python3
"""Run the frozen provider-free five-world paired-law Work II A-S qualification."""

from __future__ import annotations

import argparse
import copy
import json
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

try:
    from scripts.run_work_ii_campaign_pilot import _campaign_card
except ModuleNotFoundError:
    from run_work_ii_campaign_pilot import _campaign_card  # type: ignore[no-redef]

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_constitutive_structural_qualification import (
    CANDIDATE_IDS,
    COORDINATES_PER_CANDIDATE_WORLD,
    CRYSTALLIZATION_CANDIDATE_ID,
    EXACT_REPLAYS_TOTAL,
    PACKAGE_VERSION,
    PARTITION_CANDIDATE_ID,
    PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD,
    PRIMARY_EXECUTIONS_TOTAL,
    QUALIFICATION_VERSION,
    SUMMARY_VERSION,
    WORLD_REPORT_VERSION,
    WORLD_SEEDS,
    analyze_candidate_world,
    build_prior_arms,
    candidate_specs,
    observation_binding,
    registered_coordinates,
    report_sha256,
    selected_q2_queries,
    summary_sha256,
    validate_summary,
    validate_world_report,
)
from chemworld.eval.work_ii_crystallization_reversible_q0 import (
    validate_summary as validate_crystallization_q0,
)
from chemworld.eval.work_ii_execution_mode import (
    ExecutionMode,
    WorkIIExecutionContext,
    build_execution_envelope,
    prepare_execution_context,
)
from chemworld.eval.work_ii_formal import build_checkpoint_contract
from chemworld.eval.work_ii_partition_constitutive_q0 import (
    validate_summary as validate_partition_q0,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import MechanismFamilyIntervention
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario
from chemworld.world.scoring import PARTITION_S0_EXTRACTION_EFFICIENCY_V3

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "runs/development/work-ii-as-paired-law-q1-q2-20260812"
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-as-paired-law-q1-q2-five-world-20260812.json"
)
DEFAULT_PACKAGE = ROOT / "configs/benchmark/work_ii_as_paired_law_q2_package_v0.1.json"
DEFAULT_PARTITION_Q0 = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-partition-constitutive-q0-seed0-20260812.json"
)
DEFAULT_CRYSTALLIZATION_Q0 = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-crystallization-reversible-topology-q0-seed0-20260812.json"
)
DEFAULT_DEVELOPMENT_PARTITION_Q0 = (
    ROOT / "runs/development/work-ii-partition-constitutive-q0-seed0-20260812/summary.json"
)
DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0 = (
    ROOT
    / "runs/development/work-ii-crystallization-reversible-q0-seed0-20260812/summary.json"
)
D1_PATHS = {
    PARTITION_CANDIDATE_ID: ROOT / "configs/benchmark/work_ii_as_partition_d1_v0.1.json",
    CRYSTALLIZATION_CANDIDATE_ID: (
        ROOT / "configs/benchmark/work_ii_as_crystallization_d1_v0.1.json"
    ),
}
BASE_CONFIGS = {
    PARTITION_CANDIDATE_ID: ROOT / "configs/benchmark/work_ii_partition_campaign.json",
    CRYSTALLIZATION_CANDIDATE_ID: (
        ROOT / "configs/benchmark/work_ii_crystallization_campaign.json"
    ),
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _compile_actions(candidate_id: str, features: Mapping[str, Any]) -> list[dict[str, Any]]:
    if candidate_id == PARTITION_CANDIDATE_ID:
        return [
            {
                "operation": "add_solvent",
                "volume_L": 0.020,
                "solvent": int(features["solvent"]),
            },
            {
                "operation": "add_phase",
                "phase": "aqueous",
                "volume_L": float(features["aqueous_phase_volume_L"]),
            },
            {
                "operation": "add_extractant",
                "extractant": int(features["extractant"]),
                "volume_L": float(features["extractant_volume_L"]),
            },
            {
                "operation": "mix",
                "duration_s": float(features["mix_duration_s"]),
                "stirring_speed_rpm": float(features["stirring_speed_rpm"]),
            },
            {"operation": "settle", "duration_s": float(features["settle_duration_s"])},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "separate_phase", "target_phase": "organic"},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
    return [
        {
            "operation": "add_solvent",
            "volume_L": 0.025,
            "solvent": int(features["solvent"]),
        },
        {"operation": "add_reagent", "amount_mol": float(features["reagent_amount_mol"])},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": float(features["catalyst_amount_mol"]),
            "catalyst": int(features["catalyst"]),
        },
        {
            "operation": "heat",
            "target_temperature_K": float(features["reaction_temperature_K"]),
            "duration_s": float(features["reaction_duration_s"]),
            "stirring_speed_rpm": float(features["stirring_speed_rpm"]),
        },
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "seed_crystals", "seed_mass_g": float(features["seed_mass_g"])},
        {
            "operation": "cool_crystallize",
            "target_temperature_K": float(features["crystallization_temperature_K"]),
            "duration_s": float(features["crystallization_duration_s"]),
        },
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "filter_crystals"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _visible_leakage_matches(records: Sequence[Mapping[str, Any]]) -> list[str]:
    tokens = (
        "mechanism_family",
        "world_intervention",
        "private_seed",
        "hidden_state",
        "evaluator_truth",
    )
    matches = set()
    for row in records:
        public = {
            key: row.get(key)
            for key in (
                "observation",
                "observed_mask",
                "processed_estimate",
                "raw_signal",
                "agent_visible_observation",
                "agent_view",
            )
        }
        rendered = json.dumps(public, ensure_ascii=False, sort_keys=True)
        matches.update(token for token in tokens if token in rendered)
    return sorted(matches)


def _finite_metrics(
    candidate_id: str, records: Sequence[Mapping[str, Any]]
) -> dict[str, float]:
    spec = candidate_specs()[candidate_id]
    if candidate_id == PARTITION_CANDIDATE_ID:
        candidates = [
            row
            for row in records
            if row.get("transaction_status") == "committed"
            and row.get("operation_type") == "measure"
            and row.get("instrument") == "final_assay"
        ]
        if len(candidates) != 1:
            raise ValueError("partition execution must have one committed final assay")
        payload = candidates[0].get("processed_estimate")
    else:
        candidates = [
            row
            for row in records
            if row.get("transaction_status") == "committed"
            and row.get("operation_type") == "measure"
            and row.get("instrument") == "hplc"
        ]
        if len(candidates) != 2:
            raise ValueError("crystallization execution must have two committed HPLC assays")
        payload = candidates[0].get("processed_estimate")
    if not isinstance(payload, Mapping):
        raise ValueError("registered measurement lacks processed estimates")
    metrics: dict[str, float] = {}
    for metric in spec["metric_ids"]:
        value = payload.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"registered measurement lacks numeric {metric}")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"registered measurement {metric} is not finite")
        metrics[str(metric)] = number
    return metrics


def _law_audit(candidate_id: str, world_seed: int) -> dict[str, Any]:
    spec = candidate_specs()[candidate_id]
    intervention = MechanismFamilyIntervention.from_dict(spec["world_intervention"])
    if intervention.to_dict() != spec["world_intervention"]:
        raise ValueError("registered A-S intervention contract drifted")
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(str(spec["task_id"]))
    baseline = generator.generate(scenario, world_seed)
    altered = generator.generate(scenario, world_seed, (intervention.to_dict(),))
    repeated = generator.generate(scenario, world_seed, (intervention.to_dict(),))
    audit: dict[str, Any] = {
        "candidate_id": candidate_id,
        "world_seed": world_seed,
        "registered_law_ids": list(spec["law_ids"]),
        "world_intervention": spec["world_intervention"],
        "baseline_mechanism_hash": baseline.compiled_mechanism.mechanism_hash,
        "altered_mechanism_hash": altered.compiled_mechanism.mechanism_hash,
        "altered_hash_deterministic": (
            altered.compiled_mechanism.mechanism_hash
            == repeated.compiled_mechanism.mechanism_hash
        ),
        "mechanism_hash_changed": (
            baseline.compiled_mechanism.mechanism_hash
            != altered.compiled_mechanism.mechanism_hash
        ),
        "altered_intervention_hash": altered.initial_state.metadata.get(
            "mechanism_family_intervention_hash"
        ),
    }
    if candidate_id == PARTITION_CANDIDATE_ID:
        baseline_domain = dict(baseline.parameters.domain_parameters)
        altered_domain = dict(altered.parameters.domain_parameters)
        changed = sorted(
            key
            for key in set(baseline_domain) | set(altered_domain)
            if baseline_domain.get(key) != altered_domain.get(key)
        )
        audit.update(
            {
                "changed_domain_parameter_keys": changed,
                "baseline_partition_coefficient_exponent": baseline.parameters.domain_parameter(
                    "partition_coefficient_exponent"
                ),
                "altered_partition_coefficient_exponent": altered.parameters.domain_parameter(
                    "partition_coefficient_exponent"
                ),
                "only_registered_constitutive_parameter_changed": (
                    changed == ["partition_coefficient_exponent"]
                ),
            }
        )
    else:
        audit.update(
            {
                "added_reaction_count": len(altered.compiled_mechanism.network.reactions)
                - len(baseline.compiled_mechanism.network.reactions),
                "target_reaction_id": altered.compiled_mechanism.network.metadata.get(
                    "derived_family_target_reaction_id"
                ),
                "transform_id": altered.compiled_mechanism.network.metadata.get(
                    "derived_family_transform_id"
                ),
            }
        )
    return audit


def _execute(
    *,
    candidate_id: str,
    world_seed: int,
    coordinate: Mapping[str, Any],
    law_id: str,
    output_root: Path,
) -> dict[str, Any]:
    spec = candidate_specs()[candidate_id]
    task_id = str(spec["task_id"])
    actions = _compile_actions(candidate_id, coordinate["feature_values"])
    action_hash = report_sha256({"actions": actions})
    observation_seed, namespace = observation_binding(
        candidate_id, world_seed, str(coordinate["coordinate_id"])
    )
    interventions = [] if law_id == spec["law_ids"][0] else [spec["world_intervention"]]
    law_root = (
        output_root
        / candidate_id
        / f"world-{world_seed}"
        / str(coordinate["coordinate_id"])
        / law_id
    )
    law_root.mkdir(parents=True, exist_ok=False)
    trajectory = law_root / "trajectory.jsonl"
    started = perf_counter()
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] | None = None
    failure: dict[str, str] | None = None
    physical_failure: dict[str, Any] | None = None
    metrics: dict[str, float] | None = None
    safe: bool | None = None
    leakage: list[str] = []
    try:
        kwargs: dict[str, Any] = {}
        if candidate_id == CRYSTALLIZATION_CANDIDATE_ID:
            kwargs["crystallization_material_family_id"] = (
                "reaction-crystallization-latent-materials-v1"
            )
        if candidate_id == PARTITION_CANDIDATE_ID:
            kwargs["scoring_contract_id"] = PARTITION_S0_EXTRACTION_EFFICIENCY_V3
        run_agent(
            env_id=get_task(task_id).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task(task_id).world_split),
            budget=len(actions),
            objective="balanced",
            seed=world_seed,
            agent_seed=0,
            observation_seed=observation_seed,
            task_id=task_id,
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
            **kwargs,
        )
        records = load_jsonl(trajectory)
        noncommitted = [row for row in records if row.get("transaction_status") != "committed"]
        if noncommitted:
            if all(row.get("rollback_reason") == "constitution_failed" for row in noncommitted):
                physical_failure = {
                    "rollback_count": len(noncommitted),
                    "operations": sorted(
                        {str(row.get("operation_type")) for row in noncommitted}
                    ),
                    "attribution": "protocol_owned_physical_boundary",
                }
            else:
                first = noncommitted[0]
                raise ValueError(
                    "paired-law execution contains a non-constitution rollback: "
                    f"{first.get('operation_type')}/{first.get('rollback_reason')}"
                )
        replay = verify_records(
            records, tolerance=0.0, world_interventions=interventions
        ).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("paired-law trajectory failed exact replay")
        leakage = _visible_leakage_matches(records)
        if physical_failure is None:
            metrics = _finite_metrics(candidate_id, records)
            finals = [
                row
                for row in records
                if row.get("transaction_status") == "committed"
                and row.get("operation_type") == "measure"
                and row.get("instrument") == "final_assay"
            ]
            if len(finals) != 1:
                raise ValueError("paired-law execution lacks one final assay")
            risk = finals[0].get("observation", {}).get("safety_risk")
            if isinstance(risk, bool) or not isinstance(risk, int | float):
                raise ValueError("paired-law final assay lacks finite safety_risk")
            safe = float(risk) < float(get_task(task_id).safety_limit)
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        if trajectory.is_file() and not records:
            records = load_jsonl(trajectory)
        if records:
            leakage = _visible_leakage_matches(records)
    status = (
        "platform_failure"
        if failure is not None
        else "physical_failure"
        if physical_failure is not None
        else "completed"
    )
    mechanism_hashes = {
        str(row["mechanism_hash"])
        for row in records
        if isinstance(row.get("mechanism_hash"), str)
    }
    intervention_hashes = {
        str(row["mechanism_family_intervention_hash"])
        for row in records
        if isinstance(row.get("mechanism_family_intervention_hash"), str)
    }
    row = {
        **dict(coordinate),
        "candidate_id": candidate_id,
        "task_id": task_id,
        "world_seed": world_seed,
        "law_id": law_id,
        "status": status,
        "attribution": (
            "platform_defect_candidate"
            if status == "platform_failure"
            else "protocol_owned_physical_boundary"
            if status == "physical_failure"
            else "protocol_owned_completed_outcome"
        ),
        "safe": safe,
        "metrics": metrics,
        "action_plan_sha256": action_hash,
        "observation_coordinate_sha256": report_sha256(
            {
                "observation_seed": observation_seed,
                "observation_noise_namespace": namespace,
            }
        ),
        "mechanism_hash": next(iter(mechanism_hashes)) if len(mechanism_hashes) == 1 else None,
        "intervention_hash": (
            next(iter(intervention_hashes)) if len(intervention_hashes) == 1 else None
        ),
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "physical_failure": physical_failure,
        "platform_failure": failure,
        "participant_visible_leakage_matches": leakage,
        "trajectory": (
            {
                "path": trajectory.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(trajectory),
            }
            if trajectory.is_file()
            else None
        ),
        "elapsed_s": round(perf_counter() - started, 6),
    }
    write_json_atomic(law_root / "receipt.json", row)
    return row


class Progress:
    def __init__(self, progress_file: Path, status_file: Path) -> None:
        self.progress_file = progress_file
        self.status_file = status_file
        self.started = perf_counter()
        self.completed = 0
        self.physical_failures = 0
        self.platform_failures = 0

    def update(self, row: Mapping[str, Any]) -> None:
        self.completed += 1
        self.physical_failures += row.get("status") == "physical_failure"
        self.platform_failures += row.get("status") == "platform_failure"
        elapsed = perf_counter() - self.started
        rate = self.completed / max(elapsed, 1.0e-9)
        payload = {
            "event": "work_ii_as_paired_law_progress",
            "stage": "provider_free_primary_and_exact_replay",
            "candidate_id": row["candidate_id"],
            "world_seed": row["world_seed"],
            "coordinate_id": row["coordinate_id"],
            "law_id": row["law_id"],
            "status": row["status"],
            "completed_primary_and_replay_pairs": self.completed,
            "total_primary_and_replay_pairs": PRIMARY_EXECUTIONS_TOTAL,
            "throughput_pairs_per_minute": round(rate * 60.0, 2),
            "eta_s": round((PRIMARY_EXECUTIONS_TOTAL - self.completed) / rate, 1),
            "physical_failure_count": self.physical_failures,
            "platform_failure_count": self.platform_failures,
            "elapsed_s": round(elapsed, 1),
        }
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        with self.progress_file.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
        write_json_atomic(self.status_file, payload)
        print(rendered, flush=True)


def _d1_config(
    candidate_id: str,
    base: Mapping[str, Any],
    *,
    package_sha256: str,
    execution_context: WorkIIExecutionContext,
) -> dict[str, Any]:
    spec = candidate_specs()[candidate_id]
    task_id = str(spec["task_id"])
    config = copy.deepcopy(dict(base))
    config.update(
        {
            "schema_version": "chemworld-work-ii-campaign-pilot-0.5",
            "pilot_id": f"work-ii-as-{candidate_id}-d1",
            "formal_result": False,
            "execution_context": build_execution_envelope(execution_context),
            "task_id": task_id,
            "world_seed": 0,
            "world_interventions": [spec["world_intervention"]],
            "episode_mode": "campaign",
            "observation_noise_mode": "keyed",
            "observation_noise_namespace": f"work-ii-as-{candidate_id}-d1",
            "snapshot_stages": [
                "pre_evidence",
                "after_experiment_3",
                "after_experiment_6",
                "after_experiment_9",
                "final",
            ],
            "prior_arms": {
                arm_id: {
                    "material_information": {"mode": "opaque_codes"},
                    "initial_world_model": model,
                }
                for arm_id, model in build_prior_arms(candidate_id).items()
            },
            "intervention": {
                "locus": "structural_mechanistic",
                "candidate_id": candidate_id,
                "registered_truth_law_id": spec["altered_law_id"],
                "intervention_families": list(spec["intervention_families"]),
                "world_and_resource_contract_matched": True,
                "q2_package_sha256": package_sha256,
            },
        }
    )
    config["belief_checkpoint"] = {
        "allowed_feature_ids": list(spec["allowed_feature_ids"]),
        "allowed_metric_ids": list(spec["metric_ids"]),
        "allowed_prior_fields": list(spec["allowed_prior_fields"]),
        "held_out_queries": [
            {
                "query_id": row["coordinate_id"],
                "feature_values": row["feature_values"],
                "metric_ids": list(spec["metric_ids"]),
                "intervention_family": row["intervention_family"],
                "q2_coordinate_sha256": row["coordinate_sha256"],
            }
            for row in selected_q2_queries(candidate_id)
        ],
    }
    if candidate_id == PARTITION_CANDIDATE_ID:
        operation_limit = 144
        process_time_limit_s = 41_400.0
        stock_limits = {
            "solvent_L": 0.276,
            "phase_liquid_L": 0.3312,
            "extractant_L": 0.414,
        }
        repeat_limits = {"mix": 12, "settle": 12, "separate_phase": 12}
        policy = {
            "pattern_id": "partition-as-k12-ten-unique-two-repeat-planning",
            "formula": "10 unique + 2 exact-repeat partition stages + 15% protected reserve",
            "required_stage_max_s": 27_000.0,
            "repeat_allowance_s": 5_400.0,
            "protected_reserve_s": 4_860.0,
            "protected_reserve_fraction": 0.15,
            "implicit_stage_reserve_s": 0.0,
            "resource_status": "planning_envelope_pending_w2_26_calibration",
        }
    else:
        operation_limit = 168
        process_time_limit_s = 307_800.0
        stock_limits = {
            "reagent_mol": 0.276,
            "solvent_L": 0.552,
            "catalyst_mol": 0.0276,
            "seed_g": 0.69,
        }
        repeat_limits = {
            "heat": 12,
            "cool_crystallize": 12,
            "seed_crystals": 12,
            "filter_crystals": 12,
            "quench": 12,
        }
        policy = {
            "pattern_id": "crystallization-as-k12-ten-unique-two-repeat-planning",
            "formula": "10 unique + 2 exact-repeat full stages plus 15% protected reserve",
            "required_stage_max_s": 266_400.0,
            "repeat_allowance_s": 44_400.0,
            "protected_reserve_s": 46_620.0,
            "protected_reserve_fraction": 0.15,
            "implicit_stage_reserve_s": 7_200.0,
            "quench_transfer_allowance_s": 1_440.0,
            "implicit_operation_time_s": {"filter_crystals": 480.0, "quench": 120.0},
            "resource_status": "planning_envelope_pending_w2_26_calibration",
        }
    config["campaign"] = {
        "card_id": policy["pattern_id"],
        "checkpoint_complete_experiments": [0, 3, 6, 9, 12],
        "complete_experiments": 12,
        "final_assay_limit": 12,
        "nonfinal_instrument_use_limit": 36,
        "operation_attempt_limit": operation_limit,
        "operation_repeat_limits": repeat_limits,
        "process_time_limit_s": process_time_limit_s,
        "process_time_policy": policy,
        "stock_limits": stock_limits,
        "vessel_start_limit": 12,
        "implicit_operation_time_s": dict(policy.get("implicit_operation_time_s", {})),
        "closeout_policy": {
            "policy": "participant_controlled_advisory_no_hidden_allocation",
            "automatic_action_repair": False,
            "automatic_closeout": False,
            "planned_batches": 12,
            "final_assay_path_operations_per_batch": 2,
            "discard_path_operations_per_batch": 1,
            "final_assay_path_total_operation_reserve": 24,
            "discard_path_total_operation_reserve": 12,
            "resource_status": "planning_envelope_pending_w2_26_calibration",
        },
    }
    config["method_resources"] = {
        "checkpoint_complete_experiments": [3, 6, 9, 12],
        "complete_experiment_limit": 12,
        "operation_limit": operation_limit,
        "model_call_limit": 1,
        "input_token_limit": 5_760_000,
        "uncached_input_token_limit": 768_000,
        "output_token_limit": 57_600,
        "wall_time_limit_s": 9_000.0,
        "training_environment_step_limit": 0,
        "resource_status": "development_d1_envelope_pending_w2_26_calibration",
    }
    config["qualification"] = {
        "q0_q1_q2_passed": True,
        "minimum_unique_recipes": 10,
        "maximum_exact_repeats": 2,
        "execution_authorized": False,
        "formal_r5_authorized": False,
        "resource_calibration_status": "pending_w2_26",
    }
    config["analysis"] = {
        "final_metric_ids": list(spec["metric_ids"]),
        "primary_effect": "misspecified_pre_to_final_error_reduction_minus_aligned",
        "aligned_noninferiority_margin": -0.05,
        "typed_executable_law_required": True,
        "action_evaluation_required": True,
        "safety_violations_reported": True,
        "cluster_unit": "task_x_world_seed",
    }
    config["execution"] = {
        "max_concurrency": 3,
        "parallelization_unit": "same_seed_prior_arm_triplet",
        "within_cell_concurrency": 1,
        "failure_semantics": "finish the in-flight seed triplet, then stop before next world",
    }
    # These constructors are the runtime acceptance checks, not just schema decoration.
    for arm_id in ("opaque", "aligned_nominal", "misindexed_nominal"):
        build_checkpoint_contract(config, arm_id)
    _campaign_card(config)
    return config


def _validate_q0_inputs(
    args: argparse.Namespace,
    execution_context: WorkIIExecutionContext,
) -> dict[str, Any]:
    partition = _load(args.partition_q0_summary)
    crystallization = _load(args.crystallization_q0_summary)
    errors = validate_partition_q0(
        partition,
        root=ROOT,
        expected_execution_context=execution_context,
    )
    errors.extend(
        validate_crystallization_q0(
            ROOT,
            crystallization,
            expected_execution_context=execution_context,
        )
    )
    if partition.get("analysis", {}).get("passed") is not True:
        errors.append("partition constitutive Q0 did not pass")
    if crystallization.get("analysis", {}).get("passed") is not True:
        errors.append("crystallization reversible Q0 did not pass")
    if errors:
        raise RuntimeError("A-S Q0 input validation failed: " + "; ".join(errors))
    return {
        PARTITION_CANDIDATE_ID: {
            "path": args.partition_q0_summary.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(args.partition_q0_summary),
            "summary_sha256": partition["summary_sha256"],
        },
        CRYSTALLIZATION_CANDIDATE_ID: {
            "path": args.crystallization_q0_summary.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(args.crystallization_q0_summary),
            "summary_sha256": crystallization["summary_sha256"],
        },
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    execution_context = prepare_execution_context(
        ROOT,
        mode=args.execution_mode,
        release_manifest=args.release_manifest,
    )
    d1_paths = (
        D1_PATHS
        if execution_context.mode is ExecutionMode.RELEASE
        else {
            PARTITION_CANDIDATE_ID: args.output_root / "partition-d1.json",
            CRYSTALLIZATION_CANDIDATE_ID: args.output_root / "crystallization-d1.json",
        }
    )
    protected = [args.output_root, args.summary, args.package, *d1_paths.values()]
    if any(path.exists() for path in protected):
        raise FileExistsError("refusing to overwrite A-S qualification artifacts")
    q0_bindings = _validate_q0_inputs(args, execution_context)
    args.output_root.mkdir(parents=True)
    progress = Progress(args.progress_file, args.status_file)
    started = perf_counter()
    reports: list[dict[str, Any]] = []
    for candidate_id in CANDIDATE_IDS:
        for world_seed in WORLD_SEEDS:
            rows = []
            audit = _law_audit(candidate_id, world_seed)
            for coordinate in registered_coordinates(candidate_id):
                for law_id in candidate_specs()[candidate_id]["law_ids"]:
                    row = _execute(
                        candidate_id=candidate_id,
                        world_seed=world_seed,
                        coordinate=coordinate,
                        law_id=str(law_id),
                        output_root=args.output_root,
                    )
                    rows.append(row)
                    progress.update(row)
                    if row["status"] == "platform_failure":
                        raise RuntimeError(
                            "A-S platform failure stopped the frozen block; repair the "
                            "platform and rerun all 10,240 primary executions from the start"
                        )
            analysis = analyze_candidate_world(candidate_id, world_seed, rows, audit)
            report: dict[str, Any] = {
                "schema_version": WORLD_REPORT_VERSION,
                "qualification_schema_version": QUALIFICATION_VERSION,
                "formal_result": False,
                "provider_call_count": 0,
                "participant_session_count": 0,
                "execution_context": build_execution_envelope(execution_context),
                "candidate_id": candidate_id,
                "task_id": candidate_specs()[candidate_id]["task_id"],
                "world_seed": world_seed,
                "law_audit": audit,
                "rows": rows,
                "analysis": analysis,
            }
            report["report_sha256"] = report_sha256(report)
            report_path = (
                args.output_root / candidate_id / f"world-{world_seed}" / "world-report.json"
            )
            write_json_atomic(report_path, report)
            errors = validate_world_report(
                report, root=ROOT, expected_execution_context=execution_context
            )
            if errors:
                raise RuntimeError("invalid A-S world report: " + "; ".join(errors))
            reports.append(report)

    all_passed = all(report["analysis"]["passed"] for report in reports)
    package: dict[str, Any] = {
        "schema_version": PACKAGE_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "q0_bindings": q0_bindings,
        "candidate_laws": {
            candidate_id: {
                "task_id": candidate_specs()[candidate_id]["task_id"],
                "law_ids": list(candidate_specs()[candidate_id]["law_ids"]),
                "registered_truth_law_id": candidate_specs()[candidate_id]["altered_law_id"],
                "world_intervention": candidate_specs()[candidate_id]["world_intervention"],
                "prior_arms": build_prior_arms(candidate_id),
                "outcome_blind_q2_queries": selected_q2_queries(candidate_id),
                "world_evidence": [
                    {
                        "world_seed": report["world_seed"],
                        "passed": report["analysis"]["passed"],
                        "q2": report["analysis"]["q2"],
                    }
                    for report in reports
                    if report["candidate_id"] == candidate_id
                ],
            }
            for candidate_id in CANDIDATE_IDS
        },
        "all_five_world_cohorts_passed": all_passed,
    }
    package["package_sha256"] = report_sha256(package)
    write_json_atomic(args.package, package)

    generated_d1: dict[str, Any] = {}
    if all_passed:
        bases = {candidate_id: _load(path) for candidate_id, path in BASE_CONFIGS.items()}
        for candidate_id in CANDIDATE_IDS:
            config = _d1_config(
                candidate_id,
                bases[candidate_id],
                package_sha256=package["package_sha256"],
                execution_context=execution_context,
            )
            path = d1_paths[candidate_id]
            write_json_atomic(path, config)
            generated_d1[candidate_id] = {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(path),
                "execution_authorized": False,
            }

    raw_bindings = []
    for report in reports:
        path = (
            args.output_root
            / str(report["candidate_id"])
            / f"world-{report['world_seed']}"
            / "world-report.json"
        )
        raw_bindings.append(
            {
                "candidate_id": report["candidate_id"],
                "world_seed": report["world_seed"],
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(path),
                "report_sha256": report["report_sha256"],
                "passed": report["analysis"]["passed"],
            }
        )
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "q0_bindings": q0_bindings,
        "coverage": {
            "candidate_count": 2,
            "worlds_per_candidate": 5,
            "coordinates_per_candidate_world": COORDINATES_PER_CANDIDATE_WORLD,
            "laws_per_coordinate": 2,
            "primary_executions_per_candidate_world": PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD,
            "planned_primary_execution_count": PRIMARY_EXECUTIONS_TOTAL,
            "planned_exact_replay_count": EXACT_REPLAYS_TOTAL,
            "q2_queries_per_candidate_world": 16,
        },
        "denominators": {
            "planned_primary_executions": PRIMARY_EXECUTIONS_TOTAL,
            "attempted_primary_executions": sum(len(report["rows"]) for report in reports),
            "completed_primary_executions": sum(
                report["analysis"]["denominators"]["completed_primary_executions"]
                for report in reports
            ),
            "planned_exact_replays": EXACT_REPLAYS_TOTAL,
            "completed_exact_replays": sum(
                report["analysis"]["denominators"]["exact_replays"] for report in reports
            ),
            "physical_failures": sum(
                report["analysis"]["denominators"]["physical_failures"] for report in reports
            ),
            "platform_failures": sum(
                report["analysis"]["denominators"]["platform_failures"] for report in reports
            ),
            "unsafe_completed": sum(
                report["analysis"]["denominators"]["unsafe_completed"] for report in reports
            ),
        },
        "candidates": {
            candidate_id: {
                "task_id": candidate_specs()[candidate_id]["task_id"],
                "passed_world_count": sum(
                    report["analysis"]["passed"]
                    for report in reports
                    if report["candidate_id"] == candidate_id
                ),
                "qualification_passed": all(
                    report["analysis"]["passed"]
                    for report in reports
                    if report["candidate_id"] == candidate_id
                ),
                "worlds": [
                    {
                        "world_seed": report["world_seed"],
                        "passed": report["analysis"]["passed"],
                        "failures": report["analysis"]["failures"],
                        "q1": report["analysis"]["q1"],
                        "q2": report["analysis"]["q2"],
                    }
                    for report in reports
                    if report["candidate_id"] == candidate_id
                ],
            }
            for candidate_id in CANDIDATE_IDS
        },
        "all_candidates_passed": all_passed,
        "generated_package": {
            "path": args.package.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(args.package),
            "package_sha256": package["package_sha256"],
        },
        "participant_d1_configs_generated": generated_d1,
        "provider_execution_authorized": False,
        "formal_r5_authorized": False,
        "decision": (
            "generate_locked_d1_readiness_for_both_candidates"
            if all_passed
            else "retain_full_five_world_qualification_and_do_not_generate_d1"
        ),
        "raw_bindings": raw_bindings,
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = summary_sha256(summary)
    write_json_atomic(args.summary, summary)
    errors = validate_summary(
        ROOT,
        summary,
        expected_execution_context=execution_context,
    )
    if errors:
        raise RuntimeError("invalid A-S summary: " + "; ".join(errors))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--package", type=Path)
    parser.add_argument("--partition-q0-summary", type=Path)
    parser.add_argument(
        "--crystallization-q0-summary", type=Path
    )
    parser.add_argument("--progress-file", type=Path, required=True)
    parser.add_argument("--status-file", type=Path, required=True)
    parser.add_argument(
        "--execution-mode",
        choices=[mode.value for mode in ExecutionMode],
        default=ExecutionMode.DEVELOPMENT.value,
    )
    parser.add_argument("--release-manifest", type=Path)
    args = parser.parse_args()
    args.output_root = args.output_root.resolve()
    development = args.execution_mode == ExecutionMode.DEVELOPMENT.value
    defaults = {
        "summary": args.output_root / "summary.json" if development else DEFAULT_SUMMARY,
        "package": args.output_root / "q2-package.json" if development else DEFAULT_PACKAGE,
        "partition_q0_summary": (
            DEFAULT_DEVELOPMENT_PARTITION_Q0 if development else DEFAULT_PARTITION_Q0
        ),
        "crystallization_q0_summary": (
            DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0
            if development
            else DEFAULT_CRYSTALLIZATION_Q0
        ),
    }
    for field, default in defaults.items():
        value = getattr(args, field)
        setattr(args, field, (value if value is not None else default).resolve())
    args.progress_file = args.progress_file.resolve()
    args.status_file = args.status_file.resolve()
    if args.release_manifest is not None:
        args.release_manifest = args.release_manifest.resolve()
    result = run(args)
    print(
        json.dumps(
            {
                "completed": result["denominators"]["completed_primary_executions"],
                "planned": PRIMARY_EXECUTIONS_TOTAL,
                "exact_replays": result["denominators"]["completed_exact_replays"],
                "decision": result["decision"],
                "elapsed_s": result["elapsed_s"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if result["all_candidates_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
