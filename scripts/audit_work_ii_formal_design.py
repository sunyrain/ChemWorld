#!/usr/bin/env python3
"""Audit the Work II five-task fixed-law prior design without provider calls."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_categorical_coordinates,
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification import (
    validate_qualification_report,
)
from chemworld.materials import static_material_information_dossier
from chemworld.tasks import get_task

try:
    from scripts.run_work_ii_campaign_pilot import _campaign_card, _checkpoint_contract
except ModuleNotFoundError:  # direct ``python scripts/...`` execution
    from run_work_ii_campaign_pilot import _campaign_card, _checkpoint_contract

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-formal-world-prior-design-audit.json"
)
EXPECTED_TASKS = (
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "reaction-safety-constrained",
)
EXPECTED_ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
EXPECTED_PRIOR_QUALIFICATION_VERSION = (
    "chemworld-work-ii-ae-prior-distinguishability-qualification-0.1"
)


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256(
        {key: value for key, value in payload.items() if key != field}
    )


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _public_selection(
    *,
    task_ids: tuple[str, ...],
    key: str,
    namespace_start: int,
    namespace_size: int,
    worlds_per_task: int,
) -> dict[str, list[int]]:
    selected: dict[str, list[int]] = {}
    used: set[int] = set()
    for task_id in task_ids:
        values: list[int] = []
        counter = 0
        while len(values) < worlds_per_task:
            digest = hashlib.sha256(f"{key}:{task_id}:{counter}".encode()).digest()
            counter += 1
            value = namespace_start + int.from_bytes(digest[:8], "big") % namespace_size
            if value in used:
                continue
            used.add(value)
            values.append(value)
        selected[task_id] = values
    return selected


def _create_private_seal(
    path: Path,
    *,
    design_id: str,
    task_ids: tuple[str, ...],
    namespace_start: int,
    namespace_size: int,
    worlds_per_task: int,
    forbidden: set[int],
) -> dict[str, Any]:
    private_root = (ROOT / "runs").resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(private_root):
        raise ValueError("private seal output must stay under the ignored runs/ directory")
    if resolved.exists():
        return _load(resolved)
    used = set(forbidden)
    task_world_seeds: dict[str, list[int]] = {}
    for task_id in task_ids:
        values: list[int] = []
        while len(values) < worlds_per_task:
            value = namespace_start + secrets.randbelow(namespace_size)
            if value in used:
                continue
            used.add(value)
            values.append(value)
        task_world_seeds[task_id] = values
    payload = {
        "schema_version": "chemworld-work-ii-private-world-seal-0.1",
        "design_id": design_id,
        "seal_nonce": secrets.token_hex(32),
        "task_world_seeds": task_world_seeds,
    }
    write_json_atomic(resolved, payload)
    return payload


def _property_rows(dossier: Mapping[str, Any], field: str) -> list[dict[str, Any]]:
    choices = dossier.get("choices")
    if not isinstance(choices, Mapping) or field not in choices:
        raise ValueError(f"dossier does not expose the controlled field {field}")
    rows: list[dict[str, Any]] = []
    for item in choices[field]:
        if not isinstance(item, Mapping) or not isinstance(item.get("nominal_properties"), Mapping):
            raise ValueError(f"dossier field {field} contains an invalid property row")
        rows.append(dict(item["nominal_properties"]))
    return rows


def _moved_pair(permutation: list[int]) -> tuple[int, int]:
    moved = [index for index, source in enumerate(permutation) if index != source]
    if len(moved) != 2 or permutation[moved[0]] != moved[1] or permutation[moved[1]] != moved[0]:
        raise ValueError("descriptor_permutation must be exactly one two-row transposition")
    return moved[0], moved[1]


def _category_coordinate(task_id: str, target_field: str) -> int:
    task_info = get_task(task_id).to_dict()
    coordinates = task_recipe_categorical_coordinates(task_info)
    fields = {
        "electrochemical-conversion": {"electrolyte_profile": 0, "solvent": 1},
        "reaction-to-crystallization": {"catalyst": 4, "solvent": 6},
        "reaction-to-distillation": {"catalyst": 4, "solvent": 6},
        "partition-discovery": {"solvent": 0, "extractant": 3},
        "reaction-safety-constrained": {"catalyst": 4, "solvent": 6},
    }
    coordinate = fields[task_id][target_field]
    if coordinate not in {item[0] for item in coordinates}:
        raise ValueError(f"{task_id}.{target_field} is not an executable categorical coordinate")
    return coordinate


def _run_score(config: Mapping[str, Any], *, seed: int, coordinate: int, category: int) -> float:
    task_id = str(config["task_id"])
    kwargs = get_task(task_id).env_kwargs(seed=seed)
    for key in (
        "electrochemical_material_family_id",
        "crystallization_material_family_id",
        "electrochemical_workflow_mode",
        "scoring_contract_id",
    ):
        if config.get(key) is not None:
            kwargs[key] = config[key]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=seed)
        task_info = env.unwrapped.task_info()
        vector = np.full(task_recipe_dimension(task_info), 0.5)
        vector[coordinate] = (category + 0.5) / 4.0
        recipe = task_recipe_from_unit_vector(task_info, vector)
        info: dict[str, Any] = {}
        for action in recipe["steps"]:
            _, _, _, _, info = env.step(action)
        return float(info["leaderboard_score"])
    finally:
        env.close()


def audit(
    design_path: Path,
    *,
    output_path: Path,
    private_seal_path: Path | None,
    create_private_seal: bool,
    prior_qualification_report_path: Path | None = None,
) -> dict[str, Any]:
    design = _load(design_path)
    failures: list[dict[str, Any]] = []
    task_rows = design.get("tasks")
    if not isinstance(task_rows, list):
        raise ValueError("design.tasks must be a list")
    task_ids = tuple(str(item["task_id"]) for item in task_rows)
    if task_ids != EXPECTED_TASKS:
        failures.append({"check": "exact_task_roster", "observed": list(task_ids)})
    if tuple(design.get("prior_arms", ())) != EXPECTED_ARMS:
        failures.append({"check": "exact_prior_arm_roster"})
    qualification = design.get("prior_distinguishability_qualification_contract")
    if not isinstance(qualification, Mapping):
        failures.append({"check": "prior_distinguishability_qualification_contract"})
        qualification = {}
    if qualification.get("schema_version") != EXPECTED_PRIOR_QUALIFICATION_VERSION:
        failures.append({"check": "prior_distinguishability_qualification_version"})
    region_contracts = qualification.get("frozen_counterevidence_regions")
    if not isinstance(region_contracts, list) or len(region_contracts) < 2:
        failures.append({"check": "two_frozen_counterevidence_regions"})
    region_rules = qualification.get("region_pass_rules")
    world_rules = qualification.get("world_pass_rules")
    if (
        not isinstance(region_rules, Mapping)
        or float(region_rules.get("minimum_mean_normalized_L1_metric_vector_separation", 0.0))
        <= 0.0
        or float(region_rules.get("minimum_single_metric_absolute_separation", 0.0)) <= 0.0
        or float(region_rules.get("minimum_paired_noise_signal_to_noise_ratio", 0.0)) <= 0.0
    ):
        failures.append({"check": "frozen_metric_vector_and_noise_thresholds"})
    if (
        not isinstance(world_rules, Mapping)
        or int(world_rules.get("minimum_independent_counterevidence_regions_passed", 0)) < 2
        or int(world_rules.get("participant_complete_experiment_budget", -1)) != 8
        or world_rules.get("eight_round_falsifiability_required") is not True
    ):
        failures.append({"check": "eight_round_two_region_falsifiability_contract"})

    # This script validates the static contract and legacy scalar reachability only.
    # The strengthened qualification requires a separate immutable report containing
    # registered metric-vector, paired-noise, counterevidence-region and replay rows.
    # Do not turn an existing scalar delta into a scientific qualification result.
    qualification_status = "pending_provider_free_qualification_execution"
    qualification_ready = not any(
        item["check"]
        in {
            "prior_distinguishability_qualification_contract",
            "prior_distinguishability_qualification_version",
            "two_frozen_counterevidence_regions",
            "frozen_metric_vector_and_noise_thresholds",
            "eight_round_two_region_falsifiability_contract",
        }
        for item in failures
    )
    qualification_result: dict[str, Any] = {
        "provided": prior_qualification_report_path is not None,
        "status": qualification_status,
        "report_sha256": None,
        "validation_errors": [],
    }
    if prior_qualification_report_path is not None:
        if not prior_qualification_report_path.is_file():
            qualification_errors = ["A-E prior-qualification report is missing"]
            qualification_report: dict[str, Any] = {}
        else:
            qualification_report = _load(prior_qualification_report_path)
            qualification_errors = validate_qualification_report(
                ROOT,
                qualification_report,
                design,
                report_path=prior_qualification_report_path,
            )
        if qualification_report.get("status") != "passed":
            qualification_errors.append("A-E prior-qualification report did not pass")
        if qualification_report.get("failures") != []:
            qualification_errors.append("A-E prior-qualification report retains failures")
        qualification_errors = sorted(set(qualification_errors))
        qualification_result = {
            "provided": True,
            "path": (
                prior_qualification_report_path.resolve().relative_to(ROOT).as_posix()
            ),
            "file_sha256": (
                file_sha256(prior_qualification_report_path)
                if prior_qualification_report_path.is_file()
                else None
            ),
            "status": (
                "passed" if not qualification_errors else "failed_validation"
            ),
            "report_sha256": qualification_report.get("report_sha256"),
            "tested_commit": qualification_report.get("source_binding", {}).get(
                "tested_commit"
            ),
            "validation_errors": qualification_errors,
            "denominators": qualification_report.get("denominators"),
        }
        if qualification_errors:
            failures.append(
                {
                    "check": "prior_distinguishability_qualification_report",
                    "errors": qualification_errors,
                }
            )
        else:
            qualification_status = "passed"

    cohort = design["world_cohort"]
    development = [int(item) for item in cohort["development_and_qualification"]["world_seeds"]]
    public = cohort["public_formal"]
    expected_public = _public_selection(
        task_ids=task_ids,
        key=str(public["selection_key"]),
        namespace_start=int(public["namespace_start"]),
        namespace_size=int(public["namespace_size"]),
        worlds_per_task=int(public["worlds_per_task"]),
    )
    observed_public = {
        str(task_id): [int(seed) for seed in seeds]
        for task_id, seeds in public["task_world_seeds"].items()
    }
    if observed_public != expected_public:
        failures.append({"check": "public_world_selection_reproducible"})
    public_flat = [seed for seeds in observed_public.values() for seed in seeds]
    if len(public_flat) != len(set(public_flat)) or set(public_flat) & set(development):
        failures.append({"check": "public_worlds_unique_and_development_disjoint"})

    private = cohort["private_confirmation"]
    private_result: dict[str, Any] = {
        "provided": private_seal_path is not None,
        "identity_count": 0,
        "commitment_sha256": None,
        "commitment_matches": False,
        "disjoint": False,
    }
    if private_seal_path is None:
        failures.append({"check": "private_world_seal_provided"})
    else:
        if create_private_seal:
            seal = _create_private_seal(
                private_seal_path,
                design_id=str(design["design_id"]),
                task_ids=task_ids,
                namespace_start=int(private["namespace_start"]),
                namespace_size=int(private["namespace_size"]),
                worlds_per_task=int(private["worlds_per_task"]),
                forbidden=set(development) | set(public_flat),
            )
        else:
            seal = _load(private_seal_path)
        private_seeds = {
            str(task_id): [int(seed) for seed in seeds]
            for task_id, seeds in seal["task_world_seeds"].items()
        }
        private_flat = [seed for seeds in private_seeds.values() for seed in seeds]
        private_hash = canonical_json_sha256(seal)
        private_result = {
            "provided": True,
            "identity_count": len(private_flat),
            "commitment_sha256": private_hash,
            "commitment_matches": private_hash
            == private["sealed_identity_commitment_sha256"],
            "disjoint": not (
                set(private_flat) & (set(development) | set(public_flat))
            )
            and len(private_flat) == len(set(private_flat)),
        }
        if set(private_seeds) != set(task_ids) or any(
            len(seeds) != int(private["worlds_per_task"])
            for seeds in private_seeds.values()
        ):
            failures.append({"check": "private_world_roster_and_denominator"})
        if not private_result["commitment_matches"]:
            failures.append({"check": "private_world_commitment_matches"})
        if not private_result["disjoint"]:
            failures.append({"check": "private_worlds_unique_and_disjoint"})

    task_results: list[dict[str, Any]] = []
    diagnostic_count = 0
    for task_row in task_rows:
        task_id = str(task_row["task_id"])
        config_path = ROOT / str(task_row["campaign_config"])
        config = _load(config_path)
        target_field = str(task_row["target_field"])
        permutation = [int(item) for item in task_row["descriptor_permutation"]]
        moved = _moved_pair(permutation)
        material_family_id = config.get("electrochemical_material_family_id") or config.get(
            "crystallization_material_family_id"
        )
        nominal = static_material_information_dossier(
            config["prior_arms"]["aligned_nominal"],
            task_id=task_id,
            material_family_id=material_family_id,
        )
        misindexed = static_material_information_dossier(
            config["prior_arms"]["misindexed_nominal"],
            task_id=task_id,
            material_family_id=material_family_id,
        )
        if nominal is None or misindexed is None:
            raise ValueError(f"{task_id} informed arms must expose dossiers")
        nominal_rows = _property_rows(nominal, target_field)
        misindexed_rows = _property_rows(misindexed, target_field)
        multiset_matched = sorted(map(canonical_json_sha256, nominal_rows)) == sorted(
            map(canonical_json_sha256, misindexed_rows)
        )
        exact_transposition = misindexed_rows == [nominal_rows[index] for index in permutation]
        swapped_rows_distinct = nominal_rows[moved[0]] != nominal_rows[moved[1]]
        checkpoint_matched = _checkpoint_contract(
            config, "aligned_nominal"
        ) == _checkpoint_contract(config, "misindexed_nominal")
        card = _campaign_card(config)
        card_valid = (
            int(config["campaign"]["complete_experiments"]) == 8
            and card.vessel_start_limit == 8
            and card.final_assay_limit == 8
            and tuple(config["campaign"]["checkpoint_complete_experiments"])
            == (0, 2, 4, 6, 8)
            and int(config.get("qualification", {}).get("minimum_unique_recipes", -1)) == 6
            and int(config.get("qualification", {}).get("maximum_exact_repeats", -1)) == 2
        )
        for name, passed in (
            ("dossier_multiset_matched", multiset_matched),
            ("exact_two_row_transposition", exact_transposition),
            ("swapped_property_rows_distinct", swapped_rows_distinct),
            ("informed_checkpoint_contract_matched", checkpoint_matched),
            ("eight_lifecycle_resource_card", card_valid),
        ):
            if not passed:
                failures.append({"check": name, "task_id": task_id})

        coordinate = _category_coordinate(task_id, target_field)
        split_results: dict[str, Any] = {}
        for split, seeds in (
            ("development", development),
            ("public_formal", observed_public[task_id]),
        ):
            deltas: list[float] = []
            for seed in seeds:
                left = _run_score(config, seed=seed, coordinate=coordinate, category=moved[0])
                right = _run_score(config, seed=seed, coordinate=coordinate, category=moved[1])
                delta = abs(right - left)
                diagnostic_count += 1
                deltas.append(delta)
                print(
                    json.dumps(
                        {
                            "stage": "prior_identifiability",
                            "completed": diagnostic_count,
                            "total": len(task_rows)
                            * (len(development) + int(public["worlds_per_task"])),
                            "task_id": task_id,
                            "split": split,
                            "world_seed": seed,
                            "absolute_score_delta": delta,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
                if not np.isfinite(delta):
                    failures.append(
                        {
                            "check": "target_field_changes_executable_response",
                            "task_id": task_id,
                            "split": split,
                            "world_seed": seed,
                            "absolute_score_delta": delta,
                        }
                    )
            split_results[split] = {
                "world_count": len(seeds),
                "minimum_absolute_score_delta": min(deltas),
                "maximum_absolute_score_delta": max(deltas),
                "all_finite_legacy_scalar_diagnostics": all(np.isfinite(delta) for delta in deltas),
            }
        task_results.append(
            {
                "task_id": task_id,
                "mechanism_family": task_row["mechanism_family"],
                "campaign_config": str(task_row["campaign_config"]),
                "campaign_config_sha256": canonical_json_sha256(config),
                "target_field": target_field,
                "moved_pair": list(moved),
                "dossier_multiset_matched": multiset_matched,
                "exact_two_row_transposition": exact_transposition,
                "informed_checkpoint_contract_matched": checkpoint_matched,
                "eight_lifecycle_resource_card": card_valid,
                "prior_identifiability": split_results,
            }
        )

    report = {
        "schema_version": "chemworld-work-ii-formal-design-audit-0.1",
        "design_id": design["design_id"],
        "design_path": str(design_path.resolve().relative_to(ROOT)).replace("\\", "/"),
        "design_sha256": canonical_json_sha256(design),
        "status": (
            "failed"
            if failures
            else "passed"
            if qualification_status == "passed"
            else "pending_provider_free_prior_distinguishability_qualification"
        ),
        "formal_result": False,
        "participant_provider_calls": 0,
        "task_count": len(task_rows),
        "prior_arm_count": len(design["prior_arms"]),
        "development_world_count": len(task_rows) * len(development),
        "public_formal_world_count": len(public_flat),
        "planned_public_participant_cell_count": len(public_flat) * len(design["prior_arms"]),
        "prior_identifiability_diagnostic_count": diagnostic_count,
        "prior_distinguishability_qualification": {
            "status": qualification_status,
            "static_contract_ready": qualification_ready,
            "formal_execution_gate_satisfied": qualification_status == "passed",
            "required_result_axes": [
                "registered_metric_vector_separation",
                "paired_noise_signal_to_noise",
                "two_independent_counterevidence_regions",
                "eight_round_falsifiability",
                "all_executions_exact_replayable",
            ],
            "participant_provider_calls": 0,
            "participant_outcomes_used": False,
            "qualification_report": qualification_result,
        },
        "private_confirmation": private_result,
        "task_results": task_results,
        "failures": failures,
        "claim_boundary": (
            (
                "This audit validates the static matched-prior/world/resource contract, "
                "legacy scalar reachability, and the supplied frozen metric-vector, "
                "paired-noise, two-region, eight-round prior-distinguishability report. "
            )
            if qualification_status == "passed"
            else (
                "This audit validates the static matched-prior/world/resource contract and "
                "reports legacy scalar reachability. It does not satisfy the frozen "
                "metric-vector, paired-noise, two-region, eight-round "
                "prior-distinguishability qualification. "
            )
        )
        + "It does not execute a participant or estimate H3.",
    }
    report["audit_sha256"] = _self_hash(report, "audit_sha256")
    write_json_atomic(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--private-seal", type=Path)
    parser.add_argument("--create-private-seal", action="store_true")
    parser.add_argument("--prior-qualification-report", type=Path)
    args = parser.parse_args()
    if args.create_private_seal and args.private_seal is None:
        parser.error("--create-private-seal requires --private-seal")
    report = audit(
        args.design.resolve(),
        output_path=args.output.resolve(),
        private_seal_path=args.private_seal.resolve() if args.private_seal else None,
        create_private_seal=bool(args.create_private_seal),
        prior_qualification_report_path=(
            args.prior_qualification_report.resolve()
            if args.prior_qualification_report
            else None
        ),
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "task_count": report["task_count"],
                "diagnostic_count": report["prior_identifiability_diagnostic_count"],
                "private_commitment_sha256": report["private_confirmation"][
                    "commitment_sha256"
                ],
                "failure_count": len(report["failures"]),
                "output": str(args.output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
