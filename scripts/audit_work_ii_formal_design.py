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
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
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
            int(config["campaign"]["complete_experiments"]) == 4
            and card.vessel_start_limit == 4
            and card.final_assay_limit == 4
            and tuple(config["campaign"]["checkpoint_complete_experiments"]) == (0, 1, 2, 4)
        )
        for name, passed in (
            ("dossier_multiset_matched", multiset_matched),
            ("exact_two_row_transposition", exact_transposition),
            ("swapped_property_rows_distinct", swapped_rows_distinct),
            ("informed_checkpoint_contract_matched", checkpoint_matched),
            ("four_lifecycle_resource_card", card_valid),
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
                if not np.isfinite(delta) or delta <= 1.0e-8:
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
                "all_distinguishable": all(delta > 1.0e-8 for delta in deltas),
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
                "four_lifecycle_resource_card": card_valid,
                "prior_identifiability": split_results,
            }
        )

    report = {
        "schema_version": "chemworld-work-ii-formal-design-audit-0.1",
        "design_id": design["design_id"],
        "design_path": str(design_path.resolve().relative_to(ROOT)).replace("\\", "/"),
        "design_sha256": canonical_json_sha256(design),
        "status": "passed" if not failures else "failed",
        "formal_result": False,
        "participant_provider_calls": 0,
        "task_count": len(task_rows),
        "prior_arm_count": len(design["prior_arms"]),
        "development_world_count": len(task_rows) * len(development),
        "public_formal_world_count": len(public_flat),
        "planned_public_participant_cell_count": len(public_flat) * len(design["prior_arms"]),
        "prior_identifiability_diagnostic_count": diagnostic_count,
        "private_confirmation": private_result,
        "task_results": task_results,
        "failures": failures,
        "claim_boundary": (
            "This audit qualifies matched prior/world/resource design and deterministic "
            "target-field "
            "reachability. It does not execute a participant or estimate H3."
        ),
    }
    write_json_atomic(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--private-seal", type=Path)
    parser.add_argument("--create-private-seal", action="store_true")
    args = parser.parse_args()
    if args.create_private_seal and args.private_seal is None:
        parser.error("--create-private-seal requires --private-seal")
    report = audit(
        args.design.resolve(),
        output_path=args.output.resolve(),
        private_seal_path=args.private_seal.resolve() if args.private_seal else None,
        create_private_seal=bool(args.create_private_seal),
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
