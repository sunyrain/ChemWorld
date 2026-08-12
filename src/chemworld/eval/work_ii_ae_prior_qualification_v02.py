"""Development-only A-E prior-distinguishability qualification v0.2.

The blind policy is intentionally separate from the hidden-pair analyzer.  It receives
neither descriptor permutations nor outcomes and makes no provider calls.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections import defaultdict
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from statistics import fmean, variance
from typing import Any

import numpy as np

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_formal import build_checkpoint_contract
from chemworld.tasks import get_task

CONTRACT_VERSION = "chemworld-work-ii-ae-prior-distinguishability-contract-0.2"
PLAN_VERSION = "chemworld-work-ii-ae-prior-distinguishability-plan-0.2"
REPORT_VERSION = "chemworld-work-ii-ae-prior-distinguishability-report-0.2"
EXPECTED_TASKS = (
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "reaction-safety-constrained",
)
EXPECTED_PHASES = ("construction", "heldout_qualification")


class AEPriorQualificationV02Error(ValueError):
    """Raised when the v0.2 frozen design or evidence is malformed."""


class _FrozenRecipeAgent(BaseAgent):
    name = "work_ii_ae_prior_distinguishability_v02_frozen_recipe"

    def __init__(self, actions: Sequence[Mapping[str, Any]]) -> None:
        self._actions = [deepcopy(dict(action)) for action in actions]

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._index = 0

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        if self._index >= len(self._actions):
            raise RuntimeError("frozen v0.2 qualification recipe exhausted")
        action = deepcopy(self._actions[self._index])
        self._index += 1
        return action

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        del action, observation, reward, info


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AEPriorQualificationV02Error(f"{path} must contain an object")
    return value


def _stable_seed(*parts: object) -> int:
    digest = hashlib.sha256(":".join(str(part) for part in parts).encode()).digest()
    return int.from_bytes(digest[:8], "big") % 2_147_483_647


def _heldout_seed(namespace: str, task_id: str, index: int) -> int:
    digest = hashlib.sha256(f"{namespace}:{task_id}:{index}".encode()).digest()
    return 100_000_000 + int.from_bytes(digest[:8], "big") % 900_000_000


def _target_coordinate(task_id: str, target_field: str) -> int:
    fields = {
        "electrochemical-conversion": {"electrolyte_profile": 0, "solvent": 1},
        "reaction-to-crystallization": {"catalyst": 4, "solvent": 6},
        "reaction-to-distillation": {"catalyst": 4, "solvent": 6},
        "partition-discovery": {"solvent": 0, "extractant": 3},
        "reaction-safety-constrained": {"catalyst": 4, "solvent": 6},
    }
    try:
        return fields[task_id][target_field]
    except KeyError as error:
        raise AEPriorQualificationV02Error(
            f"unsupported target coordinate: {task_id}.{target_field}"
        ) from error


def _moved_pair(permutation: Sequence[object]) -> tuple[int, int]:
    values = [int(value) for value in permutation]
    moved = [index for index, source in enumerate(values) if index != source]
    if (
        len(values) != 4
        or len(moved) != 2
        or values[moved[0]] != moved[1]
        or values[moved[1]] != moved[0]
    ):
        raise AEPriorQualificationV02Error(
            "descriptor_permutation must be exactly one four-category transposition"
        )
    return moved[0], moved[1]


def _nuisance_vectors(
    task_id: str,
    target_coordinate: int,
    dimension: int,
    nuisance_design: Mapping[str, Any],
) -> tuple[np.ndarray, np.ndarray]:
    """Create two frozen outcome-blind complementary nuisance anchors."""

    namespace = str(nuisance_design["namespace"])
    lower = float(nuisance_design["lower_bound"])
    upper = float(nuisance_design["upper_bound"])
    digits = int(nuisance_design["round_decimal_places"])
    anchor = np.empty(dimension, dtype=float)
    for coordinate in range(dimension):
        digest = hashlib.sha256(
            f"{namespace}:{task_id}:coordinate-{coordinate}".encode()
        ).digest()
        unit = int.from_bytes(digest[:8], "big") / float(2**64)
        anchor[coordinate] = round(lower + (upper - lower) * unit, digits)
    complement = np.asarray(
        [round(lower + upper - float(value), digits) for value in anchor],
        dtype=float,
    )
    # The policy controls this coordinate categorically, so its nuisance value is unused.
    anchor[target_coordinate] = 0.5
    complement[target_coordinate] = 0.5
    return anchor, complement


def build_blind_policy_schedule(
    *,
    task_id: str,
    target_field: str,
    policy: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Build the eight recipes without accepting a target pair or any outcomes."""

    task_info = get_task(task_id).to_dict()
    target_coordinate = _target_coordinate(task_id, target_field)
    dimension = task_recipe_dimension(task_info)
    anchors = _nuisance_vectors(
        task_id,
        target_coordinate,
        dimension,
        policy["nuisance_design"],
    )
    category_orders = policy["category_order_by_anchor"]
    schedule: list[dict[str, Any]] = []
    for anchor_index, categories in enumerate(category_orders):
        for category in categories:
            vector = anchors[anchor_index].copy()
            vector[target_coordinate] = (int(category) + 0.5) / 4.0
            recipe = task_recipe_from_unit_vector(task_info, vector)
            schedule.append(
                {
                    "round_index": len(schedule),
                    "nuisance_anchor": anchor_index,
                    "target_category": int(category),
                    "target_coordinate": target_coordinate,
                    "recipe_id": f"{task_id}:anchor-{anchor_index}:category-{category}",
                    "recipe": recipe,
                }
            )
    return schedule


def validate_contract(root: Path, contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if contract.get("schema_version") != CONTRACT_VERSION:
        errors.append("unexpected v0.2 contract schema")
    if contract.get("development_only") is not True:
        errors.append("v0.2 runner must remain development-only")
    if contract.get("participant_provider_calls") != 0:
        errors.append("provider calls must be zero")
    if contract.get("participant_outcomes_read") is not False:
        errors.append("participant outcomes must not be read")
    note_path = root / str(contract.get("experiment_note", ""))
    if not note_path.is_file():
        errors.append("v0.2 experiment note is missing")

    policy = contract.get("policy")
    policy = policy if isinstance(policy, Mapping) else {}
    if policy.get("inputs") != ["task_id", "target_field"]:
        errors.append("blind policy inputs are not frozen")
    forbidden = set(policy.get("forbidden_inputs", []))
    required_forbidden = {
        "target_pair",
        "descriptor_permutation",
        "observations",
        "outcomes",
        "metric_values",
        "favorable_region",
    }
    if not required_forbidden <= forbidden:
        errors.append("blind policy forbidden inputs are incomplete")
    if (
        policy.get("policy_replicates_per_world") != 3
        or policy.get("rounds_per_policy_replicate") != 8
        or policy.get("planned_unique_recipes_per_policy_replicate") != 8
        or policy.get("minimum_unique_recipes_per_policy_replicate") != 6
        or policy.get("category_order_by_anchor") != [[0, 1, 2, 3], [0, 1, 2, 3]]
    ):
        errors.append("blind eight-round policy schedule is not frozen")
    noise = contract.get("noise")
    noise = noise if isinstance(noise, Mapping) else {}
    if (
        noise.get("covariance_between_distinct_recipe_executions") != 0.0
        or noise.get("left_right_seed_and_namespace_must_differ") is not True
        or noise.get("replicates_per_anchor_category") != 3
    ):
        errors.append("independent noise contract is not frozen")

    tasks = contract.get("tasks")
    if not isinstance(tasks, list) or tuple(
        str(row.get("task_id")) for row in tasks if isinstance(row, Mapping)
    ) != EXPECTED_TASKS:
        errors.append("v0.2 requires the exact five-task roster")
        tasks = []
    for row in tasks:
        config_path = root / str(row.get("campaign_config", ""))
        if not config_path.is_file():
            errors.append(f"campaign config missing: {row.get('task_id')}")
            continue
        allowed = build_checkpoint_contract(
            _load_object(config_path), "aligned_nominal"
        )["allowed_metric_ids"]
        support = row.get("support_metric_ids")
        controls = row.get("negative_control_metric_ids")
        if (
            not isinstance(support, list)
            or not support
            or not isinstance(controls, list)
            or set(support) & set(controls)
            or set(support) | set(controls) != set(allowed)
        ):
            errors.append(
                f"support/control metrics do not partition allowed metrics: {row.get('task_id')}"
            )
        try:
            _moved_pair(row.get("descriptor_permutation", []))
            schedule = build_blind_policy_schedule(
                task_id=str(row["task_id"]),
                target_field=str(row["target_field"]),
                policy=policy,
            )
            if len(schedule) != 8 or len({item["recipe_id"] for item in schedule}) != 8:
                errors.append(f"blind schedule is not eight unique recipes: {row.get('task_id')}")
        except (KeyError, TypeError, ValueError) as error:
            errors.append(f"invalid task policy contract {row.get('task_id')}: {error}")

    cohorts = contract.get("cohorts")
    cohorts = cohorts if isinstance(cohorts, Mapping) else {}
    seed_sets: dict[str, set[int]] = {}
    for phase in EXPECTED_PHASES:
        cohort = cohorts.get(phase)
        cohort = cohort if isinstance(cohort, Mapping) else {}
        by_task = cohort.get("task_world_seeds")
        by_task = by_task if isinstance(by_task, Mapping) else {}
        flat: set[int] = set()
        for task_id in EXPECTED_TASKS:
            seeds = by_task.get(task_id)
            if not isinstance(seeds, list) or len(seeds) != 5 or len(set(seeds)) != 5:
                errors.append(f"{phase} does not freeze five unique worlds for {task_id}")
                continue
            flat.update(int(seed) for seed in seeds)
        seed_sets[phase] = flat
    if seed_sets.get("construction", set()) & seed_sets.get(
        "heldout_qualification", set()
    ):
        errors.append("construction and held-out worlds overlap")
    heldout = cohorts.get("heldout_qualification")
    heldout = heldout if isinstance(heldout, Mapping) else {}
    namespace = str(heldout.get("selection_namespace", ""))
    by_task = heldout.get("task_world_seeds")
    by_task = by_task if isinstance(by_task, Mapping) else {}
    for task_id in EXPECTED_TASKS:
        expected = [_heldout_seed(namespace, task_id, index) for index in range(5)]
        if by_task.get(task_id) != expected:
            errors.append(f"held-out namespace derivation mismatch: {task_id}")
    construction = cohorts.get("construction")
    construction = construction if isinstance(construction, Mapping) else {}
    if construction.get("results_may_change_v0_2_rules") is not False:
        errors.append("construction results are allowed to change v0.2 rules")
    if construction.get("scientific_admission_denominator") is not False:
        errors.append("construction is incorrectly an admission denominator")
    if heldout.get("scientific_admission_denominator") is not True:
        errors.append("held-out is not the only admission denominator")
    if contract.get("denominators") != {
        "tasks": 5,
        "task_worlds_total": 50,
        "construction_task_worlds": 25,
        "heldout_qualification_task_worlds": 25,
        "policy_replicates_total": 150,
        "primary_executions_total": 1200,
        "construction_primary_executions": 600,
        "heldout_qualification_primary_executions": 600,
        "tolerance_zero_exact_replay_checks": 1200,
    }:
        errors.append("v0.2 denominators are not exactly frozen")
    return errors


def build_qualification_plan(root: Path, contract_path: Path) -> dict[str, Any]:
    root = root.resolve()
    contract_path = contract_path.resolve()
    contract = _load_object(contract_path)
    errors = validate_contract(root, contract)
    if errors:
        raise AEPriorQualificationV02Error("invalid v0.2 contract: " + "; ".join(errors))

    policy = contract["policy"]
    noise_namespace = str(contract["noise"]["seed_namespace"])
    tasks = {str(row["task_id"]): row for row in contract["tasks"]}
    task_bindings: list[dict[str, Any]] = []
    allowed_by_task: dict[str, list[str]] = {}
    for task_id in EXPECTED_TASKS:
        task_row = tasks[task_id]
        config_path = root / str(task_row["campaign_config"])
        allowed = list(
            build_checkpoint_contract(_load_object(config_path), "aligned_nominal")[
                "allowed_metric_ids"
            ]
        )
        allowed_by_task[task_id] = allowed
        task_bindings.append(
            {
                "task_id": task_id,
                "campaign_config": str(task_row["campaign_config"]),
                "target_field": str(task_row["target_field"]),
                "allowed_metric_ids": allowed,
                "support_metric_ids": list(task_row["support_metric_ids"]),
                "negative_control_metric_ids": list(
                    task_row["negative_control_metric_ids"]
                ),
            }
        )

    executions: list[dict[str, Any]] = []
    for phase in EXPECTED_PHASES:
        seeds_by_task = contract["cohorts"][phase]["task_world_seeds"]
        for task_id in EXPECTED_TASKS:
            task_row = tasks[task_id]
            schedule = build_blind_policy_schedule(
                task_id=task_id,
                target_field=str(task_row["target_field"]),
                policy=policy,
            )
            for world_seed in seeds_by_task[task_id]:
                for policy_replicate in range(3):
                    for item in schedule:
                        coordinate = (
                            phase,
                            task_id,
                            int(world_seed),
                            policy_replicate,
                            item["nuisance_anchor"],
                            item["target_category"],
                        )
                        coordinate_text = ":".join(str(value) for value in coordinate)
                        execution_id = f"v0.2:{coordinate_text}"
                        observation_namespace = f"{noise_namespace}:{coordinate_text}"
                        executions.append(
                            {
                                "execution_index": len(executions),
                                "execution_id": execution_id,
                                "phase": phase,
                                "task_id": task_id,
                                "world_seed": int(world_seed),
                                "policy_replicate": policy_replicate,
                                "round_index": int(item["round_index"]),
                                "nuisance_anchor": int(item["nuisance_anchor"]),
                                "target_category": int(item["target_category"]),
                                "target_field": str(task_row["target_field"]),
                                "target_coordinate": int(item["target_coordinate"]),
                                "recipe_id": str(item["recipe_id"]),
                                "allowed_metric_ids": allowed_by_task[task_id],
                                "support_metric_ids": list(task_row["support_metric_ids"]),
                                "negative_control_metric_ids": list(
                                    task_row["negative_control_metric_ids"]
                                ),
                                "observation_seed": _stable_seed(
                                    noise_namespace, *coordinate
                                ),
                                "observation_noise_namespace": observation_namespace,
                                "recipe": item["recipe"],
                            }
                        )
    plan = {
        "schema_version": PLAN_VERSION,
        "development_only": True,
        "contract_path": contract_path.relative_to(root).as_posix(),
        "participant_provider_calls": 0,
        "participant_outcomes_read": False,
        "denominators": deepcopy(contract["denominators"]),
        "task_bindings": task_bindings,
        "executions": executions,
    }
    errors = validate_qualification_plan(root, plan, contract)
    if errors:
        raise AEPriorQualificationV02Error("invalid generated plan: " + "; ".join(errors))
    return plan


def validate_qualification_plan(
    root: Path, plan: Mapping[str, Any], contract: Mapping[str, Any]
) -> list[str]:
    errors = validate_contract(root, contract)
    if plan.get("schema_version") != PLAN_VERSION:
        errors.append("unexpected v0.2 plan schema")
    if plan.get("development_only") is not True:
        errors.append("plan is not development-only")
    if plan.get("participant_provider_calls") != 0:
        errors.append("plan permits provider calls")
    if plan.get("participant_outcomes_read") is not False:
        errors.append("plan permits participant outcomes")
    if plan.get("denominators") != contract.get("denominators"):
        errors.append("plan denominators differ from contract")
    executions = plan.get("executions")
    if not isinstance(executions, list) or len(executions) != 1200:
        errors.append("plan must contain exactly 1200 primary executions")
        return errors
    ids: set[str] = set()
    seeds: set[int] = set()
    namespaces: set[str] = set()
    grouped: dict[tuple[str, str, int, int], list[Mapping[str, Any]]] = defaultdict(list)
    phase_counts: dict[str, int] = defaultdict(int)
    for row in executions:
        if not isinstance(row, Mapping):
            errors.append("execution row is not an object")
            continue
        execution_id = str(row.get("execution_id", ""))
        seed = int(row.get("observation_seed", -1))
        namespace = str(row.get("observation_noise_namespace", ""))
        if execution_id in ids or seed in seeds or namespace in namespaces:
            errors.append("execution id, noise seed, or noise namespace is duplicated")
        ids.add(execution_id)
        seeds.add(seed)
        namespaces.add(namespace)
        phase = str(row.get("phase", ""))
        phase_counts[phase] += 1
        key = (
            phase,
            str(row.get("task_id", "")),
            int(row.get("world_seed", -1)),
            int(row.get("policy_replicate", -1)),
        )
        grouped[key].append(row)
        if set(row.get("support_metric_ids", [])) & set(
            row.get("negative_control_metric_ids", [])
        ):
            errors.append(f"support/control overlap: {execution_id}")
        if set(row.get("support_metric_ids", [])) | set(
            row.get("negative_control_metric_ids", [])
        ) != set(row.get("allowed_metric_ids", [])):
            errors.append(f"support/control coverage mismatch: {execution_id}")
    if dict(phase_counts) != {"construction": 600, "heldout_qualification": 600}:
        errors.append("plan cohort execution counts are not 600/600")
    if len(grouped) != 150:
        errors.append("plan must contain 150 policy replicates")
    for key, rows in grouped.items():
        if (
            len(rows) != 8
            or {int(row["round_index"]) for row in rows} != set(range(8))
            or len({str(row["recipe_id"]) for row in rows}) != 8
            or {
                (int(row["nuisance_anchor"]), int(row["target_category"]))
                for row in rows
            }
            != {(anchor, category) for anchor in range(2) for category in range(4)}
        ):
            errors.append(f"blind eight-round coverage mismatch: {key}")
    return errors


def _config_for_task(
    root: Path, plan: Mapping[str, Any], task_id: str
) -> dict[str, Any]:
    matches = [
        row for row in plan["task_bindings"] if row.get("task_id") == task_id
    ]
    if len(matches) != 1:
        raise AEPriorQualificationV02Error(f"{task_id} lacks one task binding")
    return _load_object(root / str(matches[0]["campaign_config"]))


def execute_one(
    root: Path,
    plan: Mapping[str, Any],
    row: Mapping[str, Any],
    output_root: Path,
) -> dict[str, Any]:
    """Execute and tolerance-zero replay one provider-free recipe."""

    task_id = str(row["task_id"])
    config = _config_for_task(root, plan, task_id)
    execution_root = output_root / "executions" / str(row["execution_index"])
    execution_root.mkdir(parents=True, exist_ok=False)
    trajectory_path = execution_root / "trajectory.jsonl"
    actions = row["recipe"]["steps"]
    copied_fields = (
        "execution_index",
        "execution_id",
        "phase",
        "task_id",
        "world_seed",
        "policy_replicate",
        "round_index",
        "nuisance_anchor",
        "target_category",
        "target_field",
        "target_coordinate",
        "recipe_id",
        "allowed_metric_ids",
        "support_metric_ids",
        "negative_control_metric_ids",
        "observation_seed",
        "observation_noise_namespace",
    )
    receipt = {key: deepcopy(row[key]) for key in copied_fields}
    receipt["provider_call_count"] = 0
    try:
        run_agent(
            env_id=get_task(task_id).env_id,
            agent=_FrozenRecipeAgent(actions),
            world_split=str(config["world_split"]),
            budget=len(actions),
            objective=str(config["objective"]),
            seed=int(row["world_seed"]),
            observation_seed=int(row["observation_seed"]),
            task_id=task_id,
            output_path=trajectory_path,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            electrochemical_material_family_id=config.get(
                "electrochemical_material_family_id"
            ),
            crystallization_material_family_id=config.get(
                "crystallization_material_family_id"
            ),
            electrochemical_workflow_mode=config.get("electrochemical_workflow_mode"),
            scoring_contract_id=config.get("scoring_contract_id"),
            observation_noise_mode="keyed",
            observation_noise_namespace=str(row["observation_noise_namespace"]),
            world_interventions=config.get("world_interventions", []),
        )
        records = load_jsonl(trajectory_path)
        if [record.get("action") for record in records] != actions:
            raise AEPriorQualificationV02Error("trajectory differs from frozen recipe")
        if any(record.get("transaction_status") != "committed" for record in records):
            raise AEPriorQualificationV02Error(
                "physical execution contains a noncommitted action"
            )
        final_rows = [
            record
            for record in records
            if record.get("instrument") == "final_assay"
            and record.get("transaction_status") == "committed"
        ]
        if len(final_rows) != 1:
            raise AEPriorQualificationV02Error(
                "execution lacks exactly one committed final assay"
            )
        observation = final_rows[0].get("observation")
        observation = observation if isinstance(observation, Mapping) else {}
        metrics: dict[str, float] = {}
        for metric_id in row["allowed_metric_ids"]:
            value = observation.get(metric_id)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise AEPriorQualificationV02Error(
                    f"missing allowed metric {metric_id}"
                )
            number = float(value)
            if not math.isfinite(number) or not 0.0 <= number <= 1.0:
                raise AEPriorQualificationV02Error(
                    f"allowed metric {metric_id} is outside finite [0,1] bounds"
                )
            metrics[str(metric_id)] = number
        replay = verify_records(
            records,
            tolerance=0.0,
            world_interventions=config.get("world_interventions", []),
        ).to_dict()
        if replay.get("verified") is not True:
            raise AEPriorQualificationV02Error(
                "tolerance-zero exact replay did not verify"
            )
        receipt.update(
            {
                "status": "completed",
                "allowed_metrics": metrics,
                "support_metrics": {
                    metric: metrics[metric] for metric in row["support_metric_ids"]
                },
                "negative_control_metrics": {
                    metric: metrics[metric]
                    for metric in row["negative_control_metric_ids"]
                },
                "exact_replay": replay,
                "trajectory_path": trajectory_path.relative_to(output_root).as_posix(),
                "failure": None,
            }
        )
    except Exception as error:
        receipt.update(
            {
                "status": "failed",
                "allowed_metrics": None,
                "support_metrics": None,
                "negative_control_metrics": None,
                "exact_replay": None,
                "trajectory_path": (
                    trajectory_path.relative_to(output_root).as_posix()
                    if trajectory_path.is_file()
                    else None
                ),
                "failure": {"type": type(error).__name__, "message": str(error)},
            }
        )
    return receipt


def _contrast_summary(
    rows_by_category: Mapping[int, list[Mapping[str, Any]]],
    left_category: int,
    right_category: int,
    metric_ids: Sequence[str],
) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for metric_id in metric_ids:
        left = [
            float(row["allowed_metrics"][metric_id])
            for row in rows_by_category[left_category]
        ]
        right = [
            float(row["allowed_metrics"][metric_id])
            for row in rows_by_category[right_category]
        ]
        standard_error = math.sqrt(variance(left) / 3.0 + variance(right) / 3.0)
        contrast = fmean(right) - fmean(left)
        metrics[metric_id] = {
            "left_mean": fmean(left),
            "right_mean": fmean(right),
            "contrast": contrast,
            "absolute_contrast": abs(contrast),
            "welch_standard_error": standard_error,
        }
    return metrics


def build_qualification_report(
    plan: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Analyze both cohorts while admitting only universal held-out success."""

    if len(receipts) != 1200:
        raise AEPriorQualificationV02Error("report requires exactly 1200 receipts")
    receipt_by_id = {str(row.get("execution_id")): row for row in receipts}
    if len(receipt_by_id) != 1200:
        raise AEPriorQualificationV02Error("receipt IDs are missing or duplicated")
    plan_by_id = {str(row["execution_id"]): row for row in plan["executions"]}
    if set(receipt_by_id) != set(plan_by_id):
        raise AEPriorQualificationV02Error("receipt coverage differs from plan")
    task_contract = {str(row["task_id"]): row for row in contract["tasks"]}
    thresholds = contract["thresholds"]

    execution_failures: list[dict[str, Any]] = []
    valid_receipts: dict[str, Mapping[str, Any]] = {}
    copied_fields = (
        "phase",
        "task_id",
        "world_seed",
        "policy_replicate",
        "round_index",
        "nuisance_anchor",
        "target_category",
        "observation_seed",
        "observation_noise_namespace",
        "support_metric_ids",
        "negative_control_metric_ids",
    )
    for execution_id, row in receipt_by_id.items():
        planned = plan_by_id[execution_id]
        metadata_matches = all(row.get(key) == planned.get(key) for key in copied_fields)
        allowed = row.get("allowed_metrics")
        metrics_valid = (
            isinstance(allowed, Mapping)
            and set(allowed) == set(planned["allowed_metric_ids"])
            and all(
                isinstance(value, int | float)
                and not isinstance(value, bool)
                and math.isfinite(float(value))
                and 0.0 <= float(value) <= 1.0
                for value in allowed.values()
            )
        )
        replay = row.get("exact_replay")
        replay_ok = isinstance(replay, Mapping) and replay.get("verified") is True
        valid = (
            metadata_matches
            and row.get("provider_call_count") == 0
            and row.get("status") == "completed"
            and metrics_valid
            and replay_ok
        )
        if valid:
            valid_receipts[execution_id] = row
        else:
            execution_failures.append(
                {
                    "level": "execution",
                    "phase": planned["phase"],
                    "execution_id": execution_id,
                    "reason": "incomplete_invalid_metric_or_exact_replay_failure",
                }
            )

    reachability_results: list[dict[str, Any]] = []
    anchor_results: list[dict[str, Any]] = []
    world_results: list[dict[str, Any]] = []
    all_failures = list(execution_failures)
    for phase in EXPECTED_PHASES:
        for task_id in EXPECTED_TASKS:
            task_row = task_contract[task_id]
            left_category, right_category = _moved_pair(
                task_row["descriptor_permutation"]
            )
            seeds = contract["cohorts"][phase]["task_world_seeds"][task_id]
            for world_seed in seeds:
                world_plan = [
                    row
                    for row in plan["executions"]
                    if row["phase"] == phase
                    and row["task_id"] == task_id
                    and row["world_seed"] == world_seed
                ]
                world_receipts = [
                    valid_receipts[row["execution_id"]]
                    for row in world_plan
                    if row["execution_id"] in valid_receipts
                ]
                reach_rows: list[dict[str, Any]] = []
                for policy_replicate in range(3):
                    replicate_rows = [
                        row
                        for row in world_receipts
                        if row["policy_replicate"] == policy_replicate
                    ]
                    visited = {
                        (int(row["nuisance_anchor"]), int(row["target_category"]))
                        for row in replicate_rows
                    }
                    unique_recipes = len(
                        {
                            plan_by_id[str(row["execution_id"])]["recipe_id"]
                            for row in replicate_rows
                        }
                    )
                    reached_pair_both_anchors = all(
                        (anchor, category) in visited
                        for anchor in range(2)
                        for category in (left_category, right_category)
                    )
                    passed = (
                        len(replicate_rows) == 8
                        and unique_recipes >= 6
                        and reached_pair_both_anchors
                    )
                    reach = {
                        "phase": phase,
                        "task_id": task_id,
                        "world_seed": world_seed,
                        "policy_replicate": policy_replicate,
                        "completed_rounds": len(replicate_rows),
                        "unique_recipes": unique_recipes,
                        "reached_hidden_pair_at_both_anchors": reached_pair_both_anchors,
                        "passed": passed,
                    }
                    reachability_results.append(reach)
                    reach_rows.append(reach)
                    if not passed:
                        all_failures.append(
                            {
                                "level": "reachability",
                                "phase": phase,
                                "task_id": task_id,
                                "world_seed": world_seed,
                                "policy_replicate": policy_replicate,
                            }
                        )

                world_anchor_rows: list[dict[str, Any]] = []
                for anchor in range(2):
                    anchor_receipts = [
                        row
                        for row in world_receipts
                        if row["nuisance_anchor"] == anchor
                    ]
                    by_category: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
                    for row in anchor_receipts:
                        by_category[int(row["target_category"])].append(row)
                    complete = (
                        len(anchor_receipts) == 12
                        and all(len(by_category[category]) == 3 for category in range(4))
                    )
                    support_metrics: dict[str, Any] = {}
                    control_metrics: dict[str, Any] = {}
                    if complete:
                        support_metrics = _contrast_summary(
                            by_category,
                            left_category,
                            right_category,
                            task_row["support_metric_ids"],
                        )
                        control_metrics = _contrast_summary(
                            by_category,
                            left_category,
                            right_category,
                            task_row["negative_control_metric_ids"],
                        )
                    separations = [
                        float(row["absolute_contrast"])
                        for row in support_metrics.values()
                    ]
                    standard_errors = [
                        float(row["welch_standard_error"])
                        for row in support_metrics.values()
                    ]
                    mean_support = fmean(separations) if separations else 0.0
                    max_support = max(separations, default=0.0)
                    rms_uncertainty: float | None = (
                        math.sqrt(fmean(value * value for value in standard_errors))
                        if standard_errors
                        else None
                    )
                    snr = (
                        mean_support / max(rms_uncertainty, 1.0e-12)
                        if rms_uncertainty is not None
                        else 0.0
                    )
                    passed = (
                        complete
                        and mean_support
                        >= float(thresholds["minimum_mean_support_separation"])
                        and max_support
                        >= float(
                            thresholds["minimum_single_support_metric_separation"]
                        )
                        and snr
                        >= float(
                            thresholds["minimum_support_signal_to_noise_ratio"]
                        )
                    )
                    anchor_result = {
                        "phase": phase,
                        "task_id": task_id,
                        "world_seed": world_seed,
                        "nuisance_anchor": anchor,
                        "completed_executions": len(anchor_receipts),
                        "support_metric_ids": list(task_row["support_metric_ids"]),
                        "negative_control_metric_ids": list(
                            task_row["negative_control_metric_ids"]
                        ),
                        "support_metric_results": support_metrics,
                        "negative_control_metric_results": control_metrics,
                        "mean_support_separation": mean_support,
                        "maximum_support_separation": max_support,
                        "support_contrast_rms_standard_error": rms_uncertainty,
                        "support_signal_to_noise_ratio": snr,
                        "passed": passed,
                    }
                    anchor_results.append(anchor_result)
                    world_anchor_rows.append(anchor_result)
                    if not passed:
                        all_failures.append(
                            {
                                "level": "anchor",
                                "phase": phase,
                                "task_id": task_id,
                                "world_seed": world_seed,
                                "nuisance_anchor": anchor,
                            }
                        )
                world_passed = all(row["passed"] for row in reach_rows) and all(
                    row["passed"] for row in world_anchor_rows
                )
                world_result = {
                    "phase": phase,
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "passed_policy_replicates": sum(
                        int(row["passed"]) for row in reach_rows
                    ),
                    "passed_nuisance_anchors": sum(
                        int(row["passed"]) for row in world_anchor_rows
                    ),
                    "passed": world_passed,
                }
                world_results.append(world_result)
                if not world_passed:
                    all_failures.append(
                        {
                            "level": "world",
                            "phase": phase,
                            "task_id": task_id,
                            "world_seed": world_seed,
                        }
                    )

    task_results: list[dict[str, Any]] = []
    for task_id in EXPECTED_TASKS:
        construction_worlds = [
            row
            for row in world_results
            if row["phase"] == "construction" and row["task_id"] == task_id
        ]
        heldout_worlds = [
            row
            for row in world_results
            if row["phase"] == "heldout_qualification"
            and row["task_id"] == task_id
        ]
        task_results.append(
            {
                "task_id": task_id,
                "construction_passed_worlds": sum(
                    int(row["passed"]) for row in construction_worlds
                ),
                "construction_status": (
                    "passed" if all(row["passed"] for row in construction_worlds) else "failed"
                ),
                "heldout_passed_worlds": sum(
                    int(row["passed"]) for row in heldout_worlds
                ),
                "heldout_status": (
                    "passed" if all(row["passed"] for row in heldout_worlds) else "failed"
                ),
                "admission_passed": all(row["passed"] for row in heldout_worlds),
            }
        )
    heldout_passed = all(row["admission_passed"] for row in task_results)
    report = {
        "schema_version": REPORT_VERSION,
        "development_only": True,
        "status": "passed" if heldout_passed else "failed",
        "admission_basis": "heldout_qualification_only",
        "construction_can_change_v0_2_rules": False,
        "denominators": deepcopy(plan["denominators"]),
        "completed_primary_executions": len(valid_receipts),
        "verified_tolerance_zero_exact_replays": sum(
            int(
                isinstance(row.get("exact_replay"), Mapping)
                and row["exact_replay"].get("verified") is True
            )
            for row in receipts
        ),
        "reachability_results": reachability_results,
        "anchor_results": anchor_results,
        "world_results": world_results,
        "task_results": task_results,
        "failures": all_failures,
    }
    return report


def validate_qualification_report(
    root: Path,
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
    contract: Mapping[str, Any],
) -> list[str]:
    errors = validate_qualification_plan(root, plan, contract)
    if report.get("schema_version") != REPORT_VERSION:
        errors.append("unexpected v0.2 report schema")
    expected = build_qualification_report(plan, receipts, contract)
    if dict(report) != expected:
        errors.append("v0.2 report does not reproduce from plan and receipts")
    if report.get("admission_basis") != "heldout_qualification_only":
        errors.append("report admission basis is not held-out only")
    if report.get("construction_can_change_v0_2_rules") is not False:
        errors.append("report permits construction-driven rule changes")
    return errors


def markdown_summary(report: Mapping[str, Any]) -> str:
    lines = [
        "# Work II A-E prior distinguishability v0.2",
        "",
        f"Status: **{report['status']}** (development only)",
        "",
        "The admission decision uses held-out qualification worlds only; construction "
        "failures are retained below and cannot change v0.2 rules.",
        "",
        f"Primary executions: {report['completed_primary_executions']}/1200; "
        f"tolerance-zero exact replays: {report['verified_tolerance_zero_exact_replays']}/1200.",
        "",
        "| Task | Construction worlds | Held-out worlds | Admission |",
        "|---|---:|---:|---|",
    ]
    for row in report["task_results"]:
        lines.append(
            f"| {row['task_id']} | {row['construction_passed_worlds']}/5 | "
            f"{row['heldout_passed_worlds']}/5 | {row['heldout_status']} |"
        )
    lines.extend(
        [
            "",
            f"Retained failures: {len(report['failures'])}.",
            "",
            "Support and negative/control metric contrasts and Welch standard errors are "
            "reported separately in report.json.",
        ]
    )
    return "\n".join(lines) + "\n"


def execute_qualification(
    root: Path, contract_path: Path, output_root: Path
) -> dict[str, Any]:
    """Execute the fixed provider-free development block without release semantics."""

    root = root.resolve()
    output_root = output_root.resolve()
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite v0.2 output: {output_root}")
    contract = _load_object(contract_path.resolve())
    plan = build_qualification_plan(root, contract_path.resolve())
    output_root.mkdir(parents=True)
    write_json_atomic(output_root / "plan.json", plan)
    receipts: list[dict[str, Any]] = []
    started = time.perf_counter()
    for row in plan["executions"]:
        receipt = execute_one(root, plan, row, output_root)
        receipts.append(receipt)
        write_json_atomic(
            output_root / "receipts" / f"{row['execution_index']:04d}.json", receipt
        )
        completed = len(receipts)
        elapsed = time.perf_counter() - started
        throughput = completed / elapsed if elapsed else 0.0
        eta = (1200 - completed) / throughput if throughput else None
        print(
            json.dumps(
                {
                    "stage": f"ae_prior_v02_{row['phase']}",
                    "completed": completed,
                    "total": 1200,
                    "throughput_executions_per_minute": round(throughput * 60.0, 3),
                    "eta_s": round(eta, 3) if eta is not None else None,
                },
                sort_keys=True,
            ),
            flush=True,
        )
    report = build_qualification_report(plan, receipts, contract)
    errors = validate_qualification_report(root, report, plan, receipts, contract)
    if errors:
        raise AEPriorQualificationV02Error(
            "v0.2 report validation failed: " + "; ".join(errors)
        )
    write_json_atomic(output_root / "report.json", report)
    (output_root / "summary.md").write_text(
        markdown_summary(report), encoding="utf-8"
    )
    return report


__all__ = [
    "CONTRACT_VERSION",
    "PLAN_VERSION",
    "REPORT_VERSION",
    "AEPriorQualificationV02Error",
    "build_blind_policy_schedule",
    "build_qualification_plan",
    "build_qualification_report",
    "execute_one",
    "execute_qualification",
    "markdown_summary",
    "validate_contract",
    "validate_qualification_plan",
    "validate_qualification_report",
]
