"""Outcome-blind A-E prior-distinguishability qualification.

The qualification executes only evaluator-owned frozen recipes. It never reads a
participant artifact and never calls a model provider.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import time
from collections import defaultdict
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_formal import build_checkpoint_contract
from chemworld.eval.work_ii_source_binding import work_ii_material_tree_sha256
from chemworld.tasks import get_task

AE_PRIOR_QUALIFICATION_PLAN_VERSION = (
    "chemworld-work-ii-ae-prior-distinguishability-plan-0.1"
)
AE_PRIOR_QUALIFICATION_REPORT_VERSION = (
    "chemworld-work-ii-ae-prior-distinguishability-report-0.1"
)
EXPECTED_TASKS = (
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "reaction-safety-constrained",
)
EXPECTED_TASK_COUNT = 5
EXPECTED_WORLD_COUNT = 25
EXPECTED_REGION_COUNT = 50
EXPECTED_PAIR_COUNT = 150
EXPECTED_EXECUTION_COUNT = 300
EXPECTED_REGISTERED_METRIC_VALUE_COUNT = 1020
EXPECTED_PAIRED_METRIC_DIFFERENCE_COUNT = 510
AE_SOURCE_BINDING_VERSION = "chemworld-work-ii-ae-source-binding-0.1"
AE_MATERIAL_SOURCE_ROOTS = (
    "configs",
    "pyproject.toml",
    "scripts",
    "src/chemworld",
    "tests",
    "uv.lock",
)
AE_MATERIAL_SOURCE_EXCLUSIONS = (
    # Evidence paths are populated here after qualification. Including this
    # one coordination file would make that registration self-invalidating.
    "configs/benchmark/work_ii_c2_admission_manifest_v0.1.json",
)


class AEPriorQualificationError(ValueError):
    """Raised when a frozen A-E qualification artifact violates its contract."""


class _FrozenRecipeAgent(BaseAgent):
    name = "work_ii_ae_prior_distinguishability_frozen_recipe"

    def __init__(self, actions: Sequence[Mapping[str, Any]]) -> None:
        self._actions = [deepcopy(dict(action)) for action in actions]

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._index = 0

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        if self._index >= len(self._actions):
            raise RuntimeError("frozen qualification recipe exhausted")
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
        raise AEPriorQualificationError(f"{path} must contain an object")
    return value


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256({key: value for key, value in payload.items() if key != field})


def _replay_verified(row: Mapping[str, Any]) -> bool:
    replay = row.get("exact_replay")
    return isinstance(replay, Mapping) and replay.get("verified") is True


def _stable_seed(*parts: object) -> int:
    digest = hashlib.sha256(":".join(str(part) for part in parts).encode()).digest()
    return int.from_bytes(digest[:8], "big") % 2_147_483_647


def _source_binding(root: Path) -> dict[str, Any]:
    """Bind the qualification to the exact committed runtime material."""

    try:
        tested_commit = git_source_commit(root)
        worktree_clean = not git_worktree_dirty(root)
        material_sha256 = work_ii_material_tree_sha256(
            root,
            relative_roots=AE_MATERIAL_SOURCE_ROOTS,
            excluded_relative_paths=AE_MATERIAL_SOURCE_EXCLUSIONS,
        )
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        raise AEPriorQualificationError(
            f"cannot bind A-E qualification source: {type(error).__name__}: {error}"
        ) from error
    return {
        "schema_version": AE_SOURCE_BINDING_VERSION,
        "tested_commit": tested_commit,
        "worktree_clean_before_execution": worktree_clean,
        "material_tree": {
            "relative_roots": list(AE_MATERIAL_SOURCE_ROOTS),
            "excluded_relative_paths": list(AE_MATERIAL_SOURCE_EXCLUSIONS),
            "sha256": material_sha256,
        },
    }


def _commit_is_ancestor(root: Path, ancestor: str, descendant: str) -> tuple[bool, str | None]:
    try:
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        return False, f"{type(error).__name__}: {error}"
    if completed.returncode == 0:
        return True, None
    if completed.returncode == 1:
        return False, None
    detail = (completed.stderr or completed.stdout).strip()
    return False, detail or f"git merge-base exited {completed.returncode}"


def _validate_source_binding(root: Path, binding: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(binding, Mapping):
        return ["A-E qualification source binding is missing"]
    if binding.get("schema_version") != AE_SOURCE_BINDING_VERSION:
        errors.append("unexpected A-E qualification source-binding schema")
    tested_commit = binding.get("tested_commit")
    if not isinstance(tested_commit, str) or re.fullmatch(r"[0-9a-f]{40}", tested_commit) is None:
        errors.append("A-E qualification tested commit is invalid")
        tested_commit = None
    if binding.get("worktree_clean_before_execution") is not True:
        errors.append("A-E qualification lacks a clean-launch attestation")
    material = binding.get("material_tree")
    material = material if isinstance(material, Mapping) else {}
    if (
        material.get("relative_roots") != list(AE_MATERIAL_SOURCE_ROOTS)
        or material.get("excluded_relative_paths")
        != list(AE_MATERIAL_SOURCE_EXCLUSIONS)
    ):
        errors.append("A-E qualification material-source roster mismatch")
    try:
        observed_tree_sha256 = work_ii_material_tree_sha256(
            root,
            relative_roots=AE_MATERIAL_SOURCE_ROOTS,
            excluded_relative_paths=AE_MATERIAL_SOURCE_EXCLUSIONS,
        )
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        errors.append(
            "A-E qualification material-source tree cannot be rebuilt: "
            f"{type(error).__name__}"
        )
    else:
        if material.get("sha256") != observed_tree_sha256:
            errors.append("A-E qualification material-source tree is stale")
    try:
        current_commit = git_source_commit(root)
    except (OSError, subprocess.SubprocessError) as error:
        errors.append(
            f"A-E qualification current commit cannot be resolved: {type(error).__name__}"
        )
    else:
        if tested_commit is not None:
            is_ancestor, diagnostic = _commit_is_ancestor(
                root,
                tested_commit,
                current_commit,
            )
            if diagnostic is not None:
                errors.append(
                    "A-E qualification tested-commit ancestry cannot be checked: "
                    + diagnostic
                )
            elif not is_ancestor:
                errors.append(
                    "A-E qualification tested commit is not an ancestor of current HEAD"
                )
    return errors


def _validate_trajectory_commit(
    records: Sequence[Mapping[str, Any]], source_binding: Mapping[str, Any]
) -> list[str]:
    tested_commit = source_binding.get("tested_commit")
    observed = {
        (row.get("agent_metadata") or {}).get("git_commit")
        for row in records
        if isinstance(row.get("agent_metadata"), Mapping)
    }
    if len(observed) != 1 or tested_commit not in observed:
        return ["trajectory commit does not match the A-E qualification tested commit"]
    if any(
        not isinstance(row.get("agent_metadata"), Mapping)
        or row["agent_metadata"].get("git_commit") != tested_commit
        for row in records
    ):
        return ["trajectory commit does not match the A-E qualification tested commit"]
    return []


def _require_clean_launch(root: Path) -> None:
    try:
        dirty = git_worktree_dirty(root)
    except (OSError, subprocess.SubprocessError) as error:
        raise AEPriorQualificationError(
            f"cannot verify clean A-E qualification launch: {type(error).__name__}: {error}"
        ) from error
    if dirty:
        raise AEPriorQualificationError(
            "A-E qualification requires a clean worktree before execution"
        )


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
        raise AEPriorQualificationError(
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
        raise AEPriorQualificationError(
            "descriptor_permutation must be exactly one four-category transposition"
        )
    return moved[0], moved[1]


def build_qualification_plan(
    root: Path,
    design_path: Path,
    *,
    source_binding: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the exact 300-execution plan without executing the environment."""

    root = root.resolve()
    design_path = design_path.resolve()
    design = _load_object(design_path)
    contract = design.get("prior_distinguishability_qualification_contract")
    if not isinstance(contract, Mapping):
        raise AEPriorQualificationError("formal design lacks the qualification contract")
    note_path = (root / str(contract.get("experiment_note", ""))).resolve()
    if not note_path.is_file():
        raise AEPriorQualificationError("frozen qualification experiment note is missing")
    tasks = design.get("tasks")
    if not isinstance(tasks, list) or tuple(str(row.get("task_id")) for row in tasks) != (
        EXPECTED_TASKS
    ):
        raise AEPriorQualificationError("qualification requires the exact five-task A-E roster")
    public_worlds = design["world_cohort"]["public_formal"]["task_world_seeds"]
    regions = contract.get("frozen_counterevidence_regions")
    if not isinstance(regions, list) or len(regions) != 2:
        raise AEPriorQualificationError("qualification requires exactly two frozen regions")
    replicates = int(contract.get("noise_replicates_per_target_category_region", -1))
    if replicates != 3:
        raise AEPriorQualificationError("qualification requires exactly three noise replicates")

    executions: list[dict[str, Any]] = []
    config_bindings: list[dict[str, Any]] = []
    metric_count_by_task: dict[str, int] = {}
    for task_row in tasks:
        task_id = str(task_row["task_id"])
        config_path = (root / str(task_row["campaign_config"])).resolve()
        config = _load_object(config_path)
        checkpoint = build_checkpoint_contract(config, "aligned_nominal")
        metric_ids = [str(metric) for metric in checkpoint["allowed_metric_ids"]]
        if not metric_ids:
            raise AEPriorQualificationError(f"{task_id} has no registered metrics")
        metric_count_by_task[task_id] = len(metric_ids)
        config_bindings.append(
            {
                "task_id": task_id,
                "path": config_path.relative_to(root).as_posix(),
                "sha256": canonical_json_sha256(config),
                "registered_metric_ids": metric_ids,
            }
        )
        target_coordinate = _target_coordinate(task_id, str(task_row["target_field"]))
        left_category, right_category = _moved_pair(task_row["descriptor_permutation"])
        dimension = task_recipe_dimension(get_task(task_id).to_dict())
        seeds = public_worlds.get(task_id)
        if not isinstance(seeds, list) or len(seeds) != 5:
            raise AEPriorQualificationError(f"{task_id} does not have five frozen public worlds")
        for world_seed in seeds:
            for region in regions:
                region_id = str(region["region_id"])
                background = float(region["non_target_recipe_coordinate"])
                if not 0.0 <= background <= 1.0:
                    raise AEPriorQualificationError(f"{region_id} background is outside [0,1]")
                pair_prefix = f"{task_id}:world-{world_seed}:{region_id}"
                for replicate_index in range(replicates):
                    pair_id = f"{pair_prefix}:replicate-{replicate_index}"
                    observation_seed = _stable_seed(
                        AE_PRIOR_QUALIFICATION_PLAN_VERSION,
                        pair_id,
                    )
                    for side, category in (
                        ("left", left_category),
                        ("right", right_category),
                    ):
                        vector = np.full(dimension, background, dtype=float)
                        vector[target_coordinate] = (category + 0.5) / 4.0
                        recipe = task_recipe_from_unit_vector(
                            get_task(task_id).to_dict(), vector
                        )
                        execution_id = f"{pair_id}:{side}"
                        executions.append(
                            {
                                "execution_index": len(executions),
                                "execution_id": execution_id,
                                "pair_id": pair_id,
                                "task_id": task_id,
                                "world_seed": int(world_seed),
                                "region_id": region_id,
                                "background_coordinate": background,
                                "replicate_index": replicate_index,
                                "side": side,
                                "target_field": str(task_row["target_field"]),
                                "target_coordinate": target_coordinate,
                                "target_category": category,
                                "registered_metric_ids": metric_ids,
                                "observation_seed": observation_seed,
                                "observation_noise_namespace": (
                                    "work-ii-ae-prior-qualification-v0.1:"
                                    f"{task_id}:world-{world_seed}:{region_id}"
                                ),
                                "recipe": recipe,
                                "recipe_sha256": canonical_json_sha256(recipe),
                            }
                        )

    metric_values = sum(
        metric_count_by_task[task_id] * 5 * 2 * 2 * 3 for task_id in EXPECTED_TASKS
    )
    paired_metric_differences = sum(
        metric_count_by_task[task_id] * 5 * 2 * 3 for task_id in EXPECTED_TASKS
    )
    from chemworld.eval.work_ii_c2_admission import build_c2_source_binding

    plan: dict[str, Any] = {
        "schema_version": AE_PRIOR_QUALIFICATION_PLAN_VERSION,
        "design_binding": {
            "path": design_path.relative_to(root).as_posix(),
            "sha256": canonical_json_sha256(design),
        },
        "contract_sha256": canonical_json_sha256(contract),
        "experiment_note_binding": {
            "path": note_path.relative_to(root).as_posix(),
            "sha256": file_sha256(note_path),
        },
        "source_binding": dict(source_binding or _source_binding(root)),
        "c2_source_binding": build_c2_source_binding(root),
        "campaign_config_bindings": config_bindings,
        "participant_provider_calls": 0,
        "participant_outcomes_read": False,
        "denominators": {
            "tasks": EXPECTED_TASK_COUNT,
            "task_worlds": EXPECTED_WORLD_COUNT,
            "regions": EXPECTED_REGION_COUNT,
            "paired_noise_replicates": EXPECTED_PAIR_COUNT,
            "evaluator_executions": EXPECTED_EXECUTION_COUNT,
            "registered_metric_values": metric_values,
            "paired_metric_differences": paired_metric_differences,
        },
        "executions": executions,
    }
    plan["plan_sha256"] = _self_hash(plan, "plan_sha256")
    errors = validate_qualification_plan(root, plan, design)
    if errors:
        raise AEPriorQualificationError("invalid generated plan: " + "; ".join(errors))
    return plan


def validate_qualification_plan(
    root: Path,
    plan: Mapping[str, Any],
    design: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != AE_PRIOR_QUALIFICATION_PLAN_VERSION:
        errors.append("unexpected A-E qualification plan schema")
    if plan.get("plan_sha256") != _self_hash(plan, "plan_sha256"):
        errors.append("A-E qualification plan self-hash mismatch")
    if plan.get("participant_provider_calls") != 0:
        errors.append("A-E qualification plan permits provider calls")
    if plan.get("participant_outcomes_read") is not False:
        errors.append("A-E qualification plan does not forbid participant outcomes")
    errors.extend(_validate_source_binding(root, plan.get("source_binding")))
    from chemworld.eval.work_ii_c2_admission import validate_c2_source_binding

    errors.extend(validate_c2_source_binding(root, plan.get("c2_source_binding")))
    binding = plan.get("design_binding")
    binding = binding if isinstance(binding, Mapping) else {}
    if binding.get("sha256") != canonical_json_sha256(design):
        errors.append("A-E qualification design binding is stale")
    contract = design.get("prior_distinguishability_qualification_contract")
    if not isinstance(contract, Mapping) or plan.get("contract_sha256") != (
        canonical_json_sha256(contract)
    ):
        errors.append("A-E qualification contract binding is stale")
    note = plan.get("experiment_note_binding")
    note = note if isinstance(note, Mapping) else {}
    note_path = root / str(note.get("path", ""))
    if not note_path.is_file() or note.get("sha256") != file_sha256(note_path):
        errors.append("A-E qualification experiment-note binding is stale")
    config_bindings = plan.get("campaign_config_bindings")
    if not isinstance(config_bindings, list) or len(config_bindings) != EXPECTED_TASK_COUNT:
        errors.append("A-E qualification campaign bindings are incomplete")
        config_bindings = []
    binding_by_task: dict[str, Mapping[str, Any]] = {}
    for binding_row in config_bindings:
        if not isinstance(binding_row, Mapping):
            errors.append("A-E qualification campaign binding is not an object")
            continue
        task_id = str(binding_row.get("task_id", ""))
        if task_id in binding_by_task:
            errors.append("A-E qualification campaign binding task is duplicated")
            continue
        binding_by_task[task_id] = binding_row
        config_path = root / str(binding_row.get("path", ""))
        if not config_path.is_file():
            errors.append(f"A-E qualification campaign config is missing: {task_id}")
            continue
        config = _load_object(config_path)
        if canonical_json_sha256(config) != binding_row.get("sha256"):
            errors.append(f"A-E qualification campaign config binding is stale: {task_id}")
        expected_metrics = build_checkpoint_contract(
            config, "aligned_nominal"
        )["allowed_metric_ids"]
        if binding_row.get("registered_metric_ids") != expected_metrics:
            errors.append(f"A-E qualification registered metrics are stale: {task_id}")
    if set(binding_by_task) != set(EXPECTED_TASKS):
        errors.append("A-E qualification campaign binding task roster mismatch")
    denominators = plan.get("denominators")
    denominators = denominators if isinstance(denominators, Mapping) else {}
    expected_denominators = {
        "tasks": EXPECTED_TASK_COUNT,
        "task_worlds": EXPECTED_WORLD_COUNT,
        "regions": EXPECTED_REGION_COUNT,
        "paired_noise_replicates": EXPECTED_PAIR_COUNT,
        "evaluator_executions": EXPECTED_EXECUTION_COUNT,
        "registered_metric_values": EXPECTED_REGISTERED_METRIC_VALUE_COUNT,
        "paired_metric_differences": EXPECTED_PAIRED_METRIC_DIFFERENCE_COUNT,
    }
    if dict(denominators) != expected_denominators:
        errors.append("A-E qualification plan denominator mismatch")
    executions = plan.get("executions")
    if not isinstance(executions, list) or len(executions) != EXPECTED_EXECUTION_COUNT:
        errors.append("A-E qualification plan execution denominator mismatch")
        return errors
    ids = [str(row.get("execution_id")) for row in executions if isinstance(row, Mapping)]
    if len(ids) != len(set(ids)) or len(ids) != EXPECTED_EXECUTION_COUNT:
        errors.append("A-E qualification execution IDs are missing or duplicated")
    pair_sides: dict[str, set[str]] = defaultdict(set)
    pair_seeds: dict[str, set[int]] = defaultdict(set)
    observed_execution_keys: set[tuple[str, int, str, int, str]] = set()
    observed_execution_indexes: set[int] = set()
    task_rows = {
        str(row["task_id"]): row for row in design.get("tasks", [])
    }
    regions = {
        str(row["region_id"]): float(row["non_target_recipe_coordinate"])
        for row in contract.get("frozen_counterevidence_regions", [])
    } if isinstance(contract, Mapping) else {}
    for row in executions:
        if not isinstance(row, Mapping):
            errors.append("A-E qualification execution row is not an object")
            continue
        pair_id = str(row.get("pair_id"))
        pair_sides[pair_id].add(str(row.get("side")))
        pair_seeds[pair_id].add(int(row.get("observation_seed", -1)))
        task_id = str(row.get("task_id", ""))
        world_seed = int(row.get("world_seed", -1))
        region_id = str(row.get("region_id", ""))
        replicate = int(row.get("replicate_index", -1))
        side = str(row.get("side", ""))
        execution_index = int(row.get("execution_index", -1))
        observed_execution_indexes.add(execution_index)
        execution_key = (task_id, world_seed, region_id, replicate, side)
        if execution_key in observed_execution_keys:
            errors.append("A-E qualification cartesian execution key is duplicated")
        observed_execution_keys.add(execution_key)
        design_task = task_rows.get(task_id)
        if design_task is None:
            errors.append(f"A-E qualification execution has unknown task: {task_id}")
            continue
        coordinate = _target_coordinate(task_id, str(design_task["target_field"]))
        moved = _moved_pair(design_task["descriptor_permutation"])
        expected_category = moved[0] if side == "left" else moved[1]
        expected_metrics = binding_by_task.get(task_id, {}).get("registered_metric_ids")
        expected_pair_id = (
            f"{task_id}:world-{world_seed}:{region_id}:replicate-{replicate}"
        )
        expected_execution_id = f"{expected_pair_id}:{side}"
        expected_observation_seed = _stable_seed(
            AE_PRIOR_QUALIFICATION_PLAN_VERSION,
            expected_pair_id,
        )
        expected_namespace = (
            "work-ii-ae-prior-qualification-v0.1:"
            f"{task_id}:world-{world_seed}:{region_id}"
        )
        expected_recipe: Mapping[str, Any] | None = None
        if region_id in regions and side in {"left", "right"}:
            vector = np.full(
                task_recipe_dimension(get_task(task_id).to_dict()),
                regions[region_id],
                dtype=float,
            )
            vector[coordinate] = (expected_category + 0.5) / 4.0
            expected_recipe = task_recipe_from_unit_vector(
                get_task(task_id).to_dict(), vector
            )
        if (
            world_seed
            not in design["world_cohort"]["public_formal"]["task_world_seeds"].get(
                task_id, []
            )
            or region_id not in regions
            or replicate not in range(3)
            or side not in {"left", "right"}
            or row.get("background_coordinate") != regions.get(region_id)
            or row.get("target_field") != design_task["target_field"]
            or row.get("target_coordinate") != coordinate
            or row.get("target_category") != expected_category
            or row.get("registered_metric_ids") != expected_metrics
            or row.get("pair_id") != expected_pair_id
            or row.get("execution_id") != expected_execution_id
            or row.get("observation_seed") != expected_observation_seed
            or row.get("observation_noise_namespace") != expected_namespace
            or row.get("recipe") != expected_recipe
            or row.get("recipe_sha256") != canonical_json_sha256(row.get("recipe"))
        ):
            errors.append(
                "A-E qualification execution violates frozen cartesian recipe contract: "
                + str(row.get("execution_id"))
            )
    expected_execution_keys = {
        (task_id, int(seed), region_id, replicate, side)
        for task_id in EXPECTED_TASKS
        for seed in design["world_cohort"]["public_formal"]["task_world_seeds"][task_id]
        for region_id in regions
        for replicate in range(3)
        for side in ("left", "right")
    }
    if observed_execution_keys != expected_execution_keys:
        errors.append("A-E qualification cartesian execution coverage mismatch")
    if observed_execution_indexes != set(range(EXPECTED_EXECUTION_COUNT)):
        errors.append("A-E qualification execution-index coverage mismatch")
    if (
        len(pair_sides) != EXPECTED_PAIR_COUNT
        or any(sides != {"left", "right"} for sides in pair_sides.values())
        or any(len(seeds) != 1 for seeds in pair_seeds.values())
    ):
        errors.append("A-E qualification paired-noise schedule mismatch")
    return errors


def _config_for_task(
    root: Path, plan: Mapping[str, Any], task_id: str
) -> dict[str, Any]:
    bindings = plan.get("campaign_config_bindings", [])
    matches = [row for row in bindings if row.get("task_id") == task_id]
    if len(matches) != 1:
        raise AEPriorQualificationError(f"{task_id} lacks one campaign config binding")
    config = _load_object(root / str(matches[0]["path"]))
    if canonical_json_sha256(config) != matches[0].get("sha256"):
        raise AEPriorQualificationError(f"{task_id} campaign config binding is stale")
    return config


def execute_one(
    root: Path,
    plan: Mapping[str, Any],
    row: Mapping[str, Any],
    output_root: Path,
) -> dict[str, Any]:
    """Execute and replay one provider-free frozen recipe."""

    task_id = str(row["task_id"])
    config = _config_for_task(root, plan, task_id)
    execution_root = output_root / "executions" / str(row["execution_index"])
    execution_root.mkdir(parents=True, exist_ok=False)
    trajectory_path = execution_root / "trajectory.jsonl"
    actions = row["recipe"]["steps"]
    receipt: dict[str, Any] = {
        key: row[key]
        for key in (
            "execution_index",
            "execution_id",
            "pair_id",
            "task_id",
            "world_seed",
            "region_id",
            "background_coordinate",
            "replicate_index",
            "side",
            "target_field",
            "target_coordinate",
            "target_category",
            "registered_metric_ids",
            "observation_seed",
            "observation_noise_namespace",
            "recipe_sha256",
        )
    }
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
        commit_errors = _validate_trajectory_commit(records, plan["source_binding"])
        if commit_errors:
            raise AEPriorQualificationError("; ".join(commit_errors))
        if [record.get("action") for record in records] != actions:
            raise AEPriorQualificationError("trajectory differs from frozen recipe")
        if any(record.get("transaction_status") != "committed" for record in records):
            raise AEPriorQualificationError("physical execution contains a noncommitted action")
        final_rows = [
            record
            for record in records
            if record.get("instrument") == "final_assay"
            and record.get("transaction_status") == "committed"
        ]
        if len(final_rows) != 1:
            raise AEPriorQualificationError("execution lacks exactly one committed final assay")
        observation = final_rows[0].get("observation")
        observation = observation if isinstance(observation, Mapping) else {}
        metrics: dict[str, float] = {}
        for metric_id in row["registered_metric_ids"]:
            value = observation.get(metric_id)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise AEPriorQualificationError(f"missing registered metric {metric_id}")
            number = float(value)
            if not math.isfinite(number) or not 0.0 <= number <= 1.0:
                raise AEPriorQualificationError(
                    f"registered metric {metric_id} is outside finite [0,1] bounds"
                )
            metrics[str(metric_id)] = number
        replay = verify_records(
            records,
            tolerance=0.0,
            world_interventions=config.get("world_interventions", []),
        ).to_dict()
        if replay.get("verified") is not True:
            raise AEPriorQualificationError("execution does not replay exactly")
        receipt.update(
            {
                "status": "completed",
                "registered_metrics": metrics,
                "exact_replay": replay,
                "trajectory": {
                    "path": trajectory_path.relative_to(output_root).as_posix(),
                    "sha256": file_sha256(trajectory_path),
                },
                "failure": None,
            }
        )
    except Exception as error:
        receipt.update(
            {
                "status": "failed",
                "registered_metrics": None,
                "exact_replay": None,
                "trajectory": (
                    None
                    if not trajectory_path.is_file()
                    else {
                        "path": trajectory_path.relative_to(output_root).as_posix(),
                        "sha256": file_sha256(trajectory_path),
                    }
                ),
                "failure": {
                    "type": type(error).__name__,
                    "message": str(error),
                },
            }
        )
    receipt["receipt_sha256"] = _self_hash(receipt, "receipt_sha256")
    write_json_atomic(execution_root / "receipt.json", receipt)
    return receipt


def build_qualification_report(
    plan: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
    design: Mapping[str, Any],
) -> dict[str, Any]:
    """Calculate frozen metric-vector/noise gates from all retained receipts."""

    contract = design["prior_distinguishability_qualification_contract"]
    region_rules = contract["region_pass_rules"]
    world_rules = contract["world_pass_rules"]
    failures: list[dict[str, Any]] = []
    receipt_by_id: dict[str, Mapping[str, Any]] = {}
    plan_by_id = {str(row["execution_id"]): row for row in plan["executions"]}
    for receipt in receipts:
        execution_id = str(receipt.get("execution_id", ""))
        if not execution_id or execution_id in receipt_by_id:
            failures.append({"check": "unexpected_or_duplicate_execution_receipt"})
            continue
        if receipt.get("receipt_sha256") != _self_hash(receipt, "receipt_sha256"):
            failures.append(
                {"check": "execution_receipt_self_hash", "execution_id": execution_id}
            )
        plan_row = plan_by_id.get(execution_id)
        immutable_fields = (
            "execution_index",
            "execution_id",
            "pair_id",
            "task_id",
            "world_seed",
            "region_id",
            "background_coordinate",
            "replicate_index",
            "side",
            "target_field",
            "target_coordinate",
            "target_category",
            "registered_metric_ids",
            "observation_seed",
            "observation_noise_namespace",
            "recipe_sha256",
        )
        if plan_row is None or any(
            receipt.get(field) != plan_row.get(field) for field in immutable_fields
        ):
            failures.append(
                {"check": "execution_receipt_plan_binding", "execution_id": execution_id}
            )
        receipt_by_id[execution_id] = receipt
    expected_ids = {str(row["execution_id"]) for row in plan["executions"]}
    if set(receipt_by_id) != expected_ids:
        failures.append(
            {
                "check": "exact_execution_denominator",
                "missing": sorted(expected_ids - set(receipt_by_id)),
                "unexpected": sorted(set(receipt_by_id) - expected_ids),
            }
        )
    for execution_id, receipt in receipt_by_id.items():
        if (
            receipt.get("status") != "completed"
            or receipt.get("provider_call_count") != 0
            or receipt.get("failure") is not None
            or not _replay_verified(receipt)
        ):
            failures.append(
                {
                    "check": "execution_completed_provider_free_exact_replay",
                    "execution_id": execution_id,
                    "failure": receipt.get("failure"),
                }
            )

    region_groups: dict[tuple[str, int, str], list[Mapping[str, Any]]] = defaultdict(list)
    for receipt in receipt_by_id.values():
        region_groups[
            (
                str(receipt.get("task_id")),
                int(receipt.get("world_seed", -1)),
                str(receipt.get("region_id")),
            )
        ].append(receipt)
    region_rows: list[dict[str, Any]] = []
    for task_id in EXPECTED_TASKS:
        worlds = design["world_cohort"]["public_formal"]["task_world_seeds"][task_id]
        metric_ids = next(
            row["registered_metric_ids"]
            for row in plan["campaign_config_bindings"]
            if row["task_id"] == task_id
        )
        for world_seed in worlds:
            for region in contract["frozen_counterevidence_regions"]:
                region_id = str(region["region_id"])
                rows = region_groups.get((task_id, int(world_seed), region_id), [])
                region_failures: list[str] = []
                differences_by_metric: dict[str, list[float]] = {
                    metric_id: [] for metric_id in metric_ids
                }
                means_by_side: dict[str, dict[str, float]] = {"left": {}, "right": {}}
                if len(rows) != 6:
                    region_failures.append("six_execution_denominator")
                keyed = {
                    (int(row.get("replicate_index", -1)), str(row.get("side"))): row
                    for row in rows
                }
                if set(keyed) != {
                    (replicate, side)
                    for replicate in range(3)
                    for side in ("left", "right")
                }:
                    region_failures.append("three_complete_paired_replicates")
                for metric_id in metric_ids:
                    side_values: dict[str, list[float]] = {"left": [], "right": []}
                    for replicate in range(3):
                        pair_values: dict[str, float] = {}
                        for side in ("left", "right"):
                            receipt = keyed.get((replicate, side), {})
                            metrics = receipt.get("registered_metrics")
                            metrics = metrics if isinstance(metrics, Mapping) else {}
                            value = metrics.get(metric_id)
                            if (
                                isinstance(value, bool)
                                or not isinstance(value, int | float)
                                or not math.isfinite(float(value))
                            ):
                                region_failures.append(f"finite_registered_metric:{metric_id}")
                                continue
                            pair_values[side] = float(value)
                            side_values[side].append(float(value))
                        if set(pair_values) == {"left", "right"}:
                            differences_by_metric[metric_id].append(
                                pair_values["right"] - pair_values["left"]
                            )
                    for side in ("left", "right"):
                        if len(side_values[side]) == 3:
                            means_by_side[side][metric_id] = float(
                                np.mean(side_values[side])
                            )
                complete_metrics = all(
                    len(differences_by_metric[metric_id]) == 3 for metric_id in metric_ids
                )
                if complete_metrics:
                    absolute_mean_differences = [
                        abs(
                            means_by_side["right"][metric_id]
                            - means_by_side["left"][metric_id]
                        )
                        for metric_id in metric_ids
                    ]
                    vector_separation = float(np.mean(absolute_mean_differences))
                    maximum_metric_separation = float(max(absolute_mean_differences))
                    paired_noise = float(
                        math.sqrt(
                            np.mean(
                                [
                                    np.var(differences_by_metric[metric_id], ddof=1)
                                    for metric_id in metric_ids
                                ]
                            )
                        )
                    )
                    snr = vector_separation / max(paired_noise, 1.0e-12)
                else:
                    vector_separation = math.nan
                    maximum_metric_separation = math.nan
                    paired_noise = math.nan
                    snr = math.nan
                checks = {
                    "mean_metric_vector_separation": (
                        math.isfinite(vector_separation)
                        and vector_separation
                        >= float(
                            region_rules[
                                "minimum_mean_normalized_L1_metric_vector_separation"
                            ]
                        )
                    ),
                    "single_metric_separation": (
                        math.isfinite(maximum_metric_separation)
                        and maximum_metric_separation
                        >= float(region_rules["minimum_single_metric_absolute_separation"])
                    ),
                    "paired_noise_snr": (
                        math.isfinite(snr)
                        and snr
                        >= float(region_rules["minimum_paired_noise_signal_to_noise_ratio"])
                    ),
                    "all_executions_completed_and_replayable": (
                        len(rows) == 6
                        and all(
                            row.get("status") == "completed"
                            and _replay_verified(row)
                            for row in rows
                        )
                    ),
                }
                region_failures.extend(name for name, passed in checks.items() if not passed)
                region_passed = not region_failures
                if not region_passed:
                    failures.append(
                        {
                            "check": "counterevidence_region_pass",
                            "task_id": task_id,
                            "world_seed": world_seed,
                            "region_id": region_id,
                            "failed_rules": sorted(set(region_failures)),
                        }
                    )
                region_rows.append(
                    {
                        "task_id": task_id,
                        "world_seed": world_seed,
                        "region_id": region_id,
                        "registered_metric_ids": metric_ids,
                        "execution_count": len(rows),
                        "paired_replicate_count": 3 if complete_metrics else 0,
                        "mean_metric_vector_separation": (
                            vector_separation if math.isfinite(vector_separation) else None
                        ),
                        "maximum_single_metric_separation": (
                            maximum_metric_separation
                            if math.isfinite(maximum_metric_separation)
                            else None
                        ),
                        "paired_noise": paired_noise if math.isfinite(paired_noise) else None,
                        "paired_noise_snr": snr if math.isfinite(snr) else None,
                        "checks": checks,
                        "passed": region_passed,
                    }
                )

    world_rows: list[dict[str, Any]] = []
    for task_id in EXPECTED_TASKS:
        worlds = design["world_cohort"]["public_formal"]["task_world_seeds"][task_id]
        for world_seed in worlds:
            rows = [
                row
                for row in region_rows
                if row["task_id"] == task_id and row["world_seed"] == world_seed
            ]
            passed_regions = sum(row["passed"] is True for row in rows)
            recipes_needed = len(rows) * 2
            world_passed = (
                len(rows) == 2
                and passed_regions
                >= int(world_rules["minimum_independent_counterevidence_regions_passed"])
                and recipes_needed
                <= int(
                    world_rules[
                        "maximum_registered_experiments_needed_to_visit_both_choice_pairs"
                    ]
                )
                and recipes_needed <= int(world_rules["participant_complete_experiment_budget"])
                and int(world_rules["participant_minimum_unique_recipe_budget"])
                - recipes_needed
                >= 2
            )
            if not world_passed:
                failures.append(
                    {
                        "check": "task_world_prior_distinguishability",
                        "task_id": task_id,
                        "world_seed": world_seed,
                    }
                )
            world_rows.append(
                {
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "region_count": len(rows),
                    "passed_region_count": passed_regions,
                    "registered_recipes_needed": recipes_needed,
                    "participant_round_budget": int(
                        world_rules["participant_complete_experiment_budget"]
                    ),
                    "passed": world_passed,
                }
            )
    task_rows = [
        {
            "task_id": task_id,
            "world_count": 5,
            "passed_world_count": sum(
                row["passed"] is True for row in world_rows if row["task_id"] == task_id
            ),
            "passed": all(
                row["passed"] is True for row in world_rows if row["task_id"] == task_id
            ),
        }
        for task_id in EXPECTED_TASKS
    ]
    for row in task_rows:
        if not row["passed"]:
            failures.append({"check": "all_five_task_worlds_pass", "task_id": row["task_id"]})

    report: dict[str, Any] = {
        "schema_version": AE_PRIOR_QUALIFICATION_REPORT_VERSION,
        "status": "passed" if not failures else "failed",
        "formal_result": False,
        "participant_provider_calls": 0,
        "participant_outcomes_read": False,
        "plan_sha256": plan["plan_sha256"],
        "plan_binding": {"path": "plan.json", "sha256": plan["plan_sha256"]},
        "design_binding": dict(plan["design_binding"]),
        "contract_sha256": plan["contract_sha256"],
        "experiment_note_binding": dict(plan["experiment_note_binding"]),
        "source_binding": dict(plan["source_binding"]),
        "c2_source_binding": dict(plan["c2_source_binding"]),
        "campaign_config_bindings": list(plan["campaign_config_bindings"]),
        "execution_receipt_bindings": [
            {
                "execution_id": receipt.get("execution_id"),
                "path": f"executions/{receipt.get('execution_index')}/receipt.json",
                "receipt_sha256": receipt.get("receipt_sha256"),
            }
            for receipt in sorted(
                receipt_by_id.values(), key=lambda row: int(row.get("execution_index", -1))
            )
        ],
        "denominators": {
            **dict(plan["denominators"]),
            "received_execution_receipts": len(receipt_by_id),
            "completed_execution_receipts": sum(
                row.get("status") == "completed" for row in receipt_by_id.values()
            ),
            "passed_regions": sum(row["passed"] is True for row in region_rows),
            "passed_task_worlds": sum(row["passed"] is True for row in world_rows),
            "passed_tasks": sum(row["passed"] is True for row in task_rows),
        },
        "region_results": region_rows,
        "world_results": world_rows,
        "task_results": task_rows,
        "failures": failures,
        "claim_boundary": (
            "Provider-free prior distinguishability and eight-round falsifiability only; "
            "no participant method or H3 outcome is evaluated."
        ),
    }
    report["report_sha256"] = _self_hash(report, "report_sha256")
    return report


def validate_qualification_report(
    root: Path,
    report: Mapping[str, Any],
    design: Mapping[str, Any],
    *,
    report_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    if report.get("schema_version") != AE_PRIOR_QUALIFICATION_REPORT_VERSION:
        errors.append("unexpected A-E prior-qualification report schema")
    if report.get("report_sha256") != _self_hash(report, "report_sha256"):
        errors.append("A-E prior-qualification report self-hash mismatch")
    if report.get("participant_provider_calls") != 0:
        errors.append("A-E prior-qualification report contains provider calls")
    if report.get("participant_outcomes_read") is not False:
        errors.append("A-E prior-qualification report used participant outcomes")
    errors.extend(_validate_source_binding(root, report.get("source_binding")))
    from chemworld.eval.work_ii_c2_admission import validate_c2_source_binding

    errors.extend(validate_c2_source_binding(root, report.get("c2_source_binding")))
    plan_binding = report.get("plan_binding")
    plan_binding = plan_binding if isinstance(plan_binding, Mapping) else {}
    if (
        plan_binding.get("path") != "plan.json"
        or plan_binding.get("sha256") != report.get("plan_sha256")
    ):
        errors.append("A-E prior-qualification report plan binding is incomplete")

    binding = report.get("design_binding")
    binding = binding if isinstance(binding, Mapping) else {}
    if binding.get("sha256") != canonical_json_sha256(design):
        errors.append("A-E prior-qualification report design binding is stale")
    contract = design.get("prior_distinguishability_qualification_contract")
    if not isinstance(contract, Mapping):
        errors.append("A-E prior-qualification design lacks its contract")
        contract = {}
    elif report.get("contract_sha256") != canonical_json_sha256(contract):
        errors.append("A-E prior-qualification report contract binding is stale")
    note = report.get("experiment_note_binding")
    note = note if isinstance(note, Mapping) else {}
    note_path = root / str(note.get("path", ""))
    if not note_path.is_file() or note.get("sha256") != file_sha256(note_path):
        errors.append("A-E prior-qualification experiment-note binding is stale")

    config_bindings = report.get("campaign_config_bindings")
    binding_by_task: dict[str, Mapping[str, Any]] = {}
    config_by_task: dict[str, dict[str, Any]] = {}
    if not isinstance(config_bindings, list) or len(config_bindings) != EXPECTED_TASK_COUNT:
        errors.append("A-E prior-qualification campaign bindings are incomplete")
        config_bindings = []
    for config_binding in config_bindings:
        if not isinstance(config_binding, Mapping):
            errors.append("A-E prior-qualification campaign binding is not an object")
            continue
        task_id = str(config_binding.get("task_id", ""))
        if task_id in binding_by_task:
            errors.append("A-E prior-qualification campaign binding task is duplicated")
            continue
        binding_by_task[task_id] = config_binding
        path = root / str(config_binding.get("path", ""))
        if not path.is_file():
            errors.append(f"A-E prior-qualification campaign config is missing: {task_id}")
            continue
        config = _load_object(path)
        config_by_task[task_id] = config
        expected_metrics = build_checkpoint_contract(
            config, "aligned_nominal"
        )["allowed_metric_ids"]
        if (
            canonical_json_sha256(config) != config_binding.get("sha256")
            or config_binding.get("registered_metric_ids") != expected_metrics
        ):
            errors.append(f"A-E prior-qualification campaign binding is stale: {task_id}")
    if set(binding_by_task) != set(EXPECTED_TASKS):
        errors.append("A-E prior-qualification campaign binding task roster mismatch")

    receipt_bindings = report.get("execution_receipt_bindings")
    if not isinstance(receipt_bindings, list):
        receipt_bindings = []
    receipt_ids = [
        str(row.get("execution_id", ""))
        for row in receipt_bindings
        if isinstance(row, Mapping)
    ]
    if (
        len(receipt_bindings) != EXPECTED_EXECUTION_COUNT
        or len(receipt_ids) != EXPECTED_EXECUTION_COUNT
        or len(set(receipt_ids)) != EXPECTED_EXECUTION_COUNT
    ):
        errors.append("A-E prior-qualification receipt bindings are incomplete")

    evidence_plan: dict[str, Any] | None = None
    evidence_receipts: list[dict[str, Any]] = []
    if report_path is not None:
        output_root = report_path.resolve().parent
        plan_path = (output_root / str(plan_binding.get("path", ""))).resolve()
        try:
            plan_path.relative_to(output_root)
        except ValueError:
            errors.append("A-E prior-qualification plan binding escapes output root")
        else:
            if not plan_path.is_file():
                errors.append("A-E prior-qualification bound plan is missing")
            else:
                evidence_plan = _load_object(plan_path)
                errors.extend(validate_qualification_plan(root, evidence_plan, design))
                if (
                    evidence_plan.get("plan_sha256") != plan_binding.get("sha256")
                    or evidence_plan.get("plan_sha256") != report.get("plan_sha256")
                ):
                    errors.append("A-E prior-qualification plan binding is stale")

        plan_by_id = (
            {
                str(row["execution_id"]): row
                for row in evidence_plan.get("executions", [])
            }
            if evidence_plan is not None
            else {}
        )
        immutable_fields = (
            "execution_index",
            "execution_id",
            "pair_id",
            "task_id",
            "world_seed",
            "region_id",
            "background_coordinate",
            "replicate_index",
            "side",
            "target_field",
            "target_coordinate",
            "target_category",
            "registered_metric_ids",
            "observation_seed",
            "observation_noise_namespace",
            "recipe_sha256",
        )
        for receipt_binding in receipt_bindings:
            if not isinstance(receipt_binding, Mapping):
                errors.append("A-E prior-qualification receipt binding is not an object")
                continue
            execution_id = str(receipt_binding.get("execution_id", ""))
            receipt_path = (
                output_root / str(receipt_binding.get("path", ""))
            ).resolve()
            try:
                receipt_path.relative_to(output_root)
            except ValueError:
                errors.append("A-E prior-qualification receipt binding escapes output root")
                continue
            if not receipt_path.is_file():
                errors.append(
                    f"A-E prior-qualification receipt binding is missing: {execution_id}"
                )
                continue
            receipt = _load_object(receipt_path)
            evidence_receipts.append(receipt)
            if (
                receipt.get("receipt_sha256") != _self_hash(receipt, "receipt_sha256")
                or receipt.get("receipt_sha256")
                != receipt_binding.get("receipt_sha256")
                or receipt.get("execution_id") != execution_id
            ):
                errors.append(
                    f"A-E prior-qualification receipt binding is stale: {execution_id}"
                )
            plan_row = plan_by_id.get(execution_id)
            if plan_row is None or any(
                receipt.get(field) != plan_row.get(field) for field in immutable_fields
            ):
                errors.append(
                    f"A-E prior-qualification receipt differs from plan: {execution_id}"
                )
            trajectory = receipt.get("trajectory")
            if not isinstance(trajectory, Mapping):
                if receipt.get("status") == "completed":
                    errors.append(
                        "A-E prior-qualification completed receipt lacks trajectory: "
                        + execution_id
                    )
                continue
            trajectory_path = (
                output_root / str(trajectory.get("path", ""))
            ).resolve()
            try:
                trajectory_path.relative_to(output_root)
            except ValueError:
                errors.append("A-E prior-qualification trajectory escapes output root")
                continue
            if (
                not trajectory_path.is_file()
                or trajectory.get("sha256") != file_sha256(trajectory_path)
            ):
                errors.append(
                    f"A-E prior-qualification trajectory binding is stale: {execution_id}"
                )
                continue
            if plan_row is None:
                continue
            if receipt.get("status") != "completed":
                continue
            try:
                records = load_jsonl(trajectory_path)
                commit_errors = _validate_trajectory_commit(
                    records,
                    report.get("source_binding", {}),
                )
                errors.extend(
                    "A-E prior-qualification " + error + ": " + execution_id
                    for error in commit_errors
                )
                replay = verify_records(
                    records,
                    tolerance=0.0,
                    world_interventions=config_by_task[
                        str(plan_row["task_id"])
                    ].get("world_interventions", []),
                ).to_dict()
                final_rows = [
                    row
                    for row in records
                    if row.get("instrument") == "final_assay"
                    and row.get("transaction_status") == "committed"
                ]
                final_observation = (
                    final_rows[0].get("observation", {})
                    if len(final_rows) == 1
                    else {}
                )
                expected_metrics = {
                    metric_id: final_observation.get(metric_id)
                    for metric_id in plan_row["registered_metric_ids"]
                }
                if (
                    [row.get("action") for row in records]
                    != plan_row["recipe"]["steps"]
                    or any(
                        row.get("transaction_status") != "committed"
                        for row in records
                    )
                    or replay.get("verified") is not True
                    or not _replay_verified(receipt)
                    or receipt.get("registered_metrics") != expected_metrics
                ):
                    errors.append(
                        "A-E prior-qualification trajectory does not prove receipt: "
                        + execution_id
                    )
            except Exception as error:
                errors.append(
                    "A-E prior-qualification trajectory validation failed: "
                    f"{execution_id}: {type(error).__name__}"
                )

    denominators = report.get("denominators")
    denominators = denominators if isinstance(denominators, Mapping) else {}
    fixed_denominators = {
        "tasks": EXPECTED_TASK_COUNT,
        "task_worlds": EXPECTED_WORLD_COUNT,
        "regions": EXPECTED_REGION_COUNT,
        "paired_noise_replicates": EXPECTED_PAIR_COUNT,
        "evaluator_executions": EXPECTED_EXECUTION_COUNT,
        "registered_metric_values": EXPECTED_REGISTERED_METRIC_VALUE_COUNT,
        "paired_metric_differences": EXPECTED_PAIRED_METRIC_DIFFERENCE_COUNT,
    }
    for key, value in fixed_denominators.items():
        if denominators.get(key) != value:
            errors.append(f"A-E prior-qualification denominator mismatch: {key}")

    region_rows = report.get("region_results")
    world_rows = report.get("world_results")
    task_rows = report.get("task_results")
    if not isinstance(region_rows, list) or len(region_rows) != EXPECTED_REGION_COUNT:
        errors.append("A-E prior-qualification region denominator mismatch")
        region_rows = []
    if not isinstance(world_rows, list) or len(world_rows) != EXPECTED_WORLD_COUNT:
        errors.append("A-E prior-qualification world denominator mismatch")
        world_rows = []
    if not isinstance(task_rows, list) or len(task_rows) != EXPECTED_TASK_COUNT:
        errors.append("A-E prior-qualification task denominator mismatch")
        task_rows = []

    region_rules = contract.get("region_pass_rules", {})
    region_rules = region_rules if isinstance(region_rules, Mapping) else {}
    minimum_vector = float(
        region_rules.get(
            "minimum_mean_normalized_L1_metric_vector_separation", math.inf
        )
    )
    minimum_single = float(
        region_rules.get("minimum_single_metric_absolute_separation", math.inf)
    )
    minimum_snr = float(
        region_rules.get("minimum_paired_noise_signal_to_noise_ratio", math.inf)
    )
    expected_region_keys = {
        (task_id, int(seed), str(region["region_id"]))
        for task_id in EXPECTED_TASKS
        for seed in design["world_cohort"]["public_formal"]["task_world_seeds"][
            task_id
        ]
        for region in contract.get("frozen_counterevidence_regions", [])
    }
    region_by_key: dict[tuple[str, int, str], Mapping[str, Any]] = {}
    check_names = {
        "mean_metric_vector_separation",
        "single_metric_separation",
        "paired_noise_snr",
        "all_executions_completed_and_replayable",
    }
    for row in region_rows:
        key = (
            str(row.get("task_id", "")),
            int(row.get("world_seed", -1)),
            str(row.get("region_id", "")),
        )
        if key in region_by_key:
            errors.append("A-E prior-qualification region identity is duplicated")
        region_by_key[key] = row
        metric_binding = binding_by_task.get(key[0], {})
        if row.get("registered_metric_ids") != metric_binding.get(
            "registered_metric_ids"
        ):
            errors.append(f"A-E prior-qualification region metric binding mismatch: {key}")
        vector = row.get("mean_metric_vector_separation")
        single = row.get("maximum_single_metric_separation")
        noise = row.get("paired_noise")
        snr = row.get("paired_noise_snr")
        values = (vector, single, noise, snr)
        numeric = all(
            isinstance(value, int | float)
            and not isinstance(value, bool)
            and math.isfinite(float(value))
            and float(value) >= 0.0
            for value in values
        )
        checks = row.get("checks")
        checks = checks if isinstance(checks, Mapping) else {}
        expected_numeric_checks = {
            "mean_metric_vector_separation": (
                numeric and float(vector) >= minimum_vector
            ),
            "single_metric_separation": numeric and float(single) >= minimum_single,
            "paired_noise_snr": numeric and float(snr) >= minimum_snr,
            "all_executions_completed_and_replayable": (
                row.get("execution_count") == 6
                and row.get("paired_replicate_count") == 3
            ),
        }
        if set(checks) != check_names or any(
            checks.get(name) is not expected
            for name, expected in expected_numeric_checks.items()
        ):
            errors.append(f"A-E prior-qualification region checks mismatch: {key}")
        recomputed_pass = set(checks) == check_names and all(
            value is True for value in checks.values()
        )
        if row.get("passed") is not recomputed_pass:
            errors.append(f"A-E prior-qualification region pass mismatch: {key}")
    if set(region_by_key) != expected_region_keys:
        errors.append("A-E prior-qualification region identity mismatch")

    world_rules = contract.get("world_pass_rules", {})
    world_rules = world_rules if isinstance(world_rules, Mapping) else {}
    expected_world_keys = {
        (task_id, int(seed))
        for task_id in EXPECTED_TASKS
        for seed in design["world_cohort"]["public_formal"]["task_world_seeds"][
            task_id
        ]
    }
    world_by_key: dict[tuple[str, int], Mapping[str, Any]] = {}
    for row in world_rows:
        key = (str(row.get("task_id", "")), int(row.get("world_seed", -1)))
        if key in world_by_key:
            errors.append("A-E prior-qualification world identity is duplicated")
        world_by_key[key] = row
        child_rows = [
            child for child_key, child in region_by_key.items() if child_key[:2] == key
        ]
        passed_regions = sum(child.get("passed") is True for child in child_rows)
        recipes_needed = len(child_rows) * 2
        recomputed_pass = (
            len(child_rows) == 2
            and passed_regions
            >= int(
                world_rules.get(
                    "minimum_independent_counterevidence_regions_passed", 10**9
                )
            )
            and recipes_needed
            <= int(
                world_rules.get(
                    "maximum_registered_experiments_needed_to_visit_both_choice_pairs",
                    -1,
                )
            )
            and recipes_needed
            <= int(world_rules.get("participant_complete_experiment_budget", -1))
            and int(world_rules.get("participant_minimum_unique_recipe_budget", -1))
            - recipes_needed
            >= 2
        )
        expected_fields = {
            "region_count": len(child_rows),
            "passed_region_count": passed_regions,
            "registered_recipes_needed": recipes_needed,
            "participant_round_budget": int(
                world_rules.get("participant_complete_experiment_budget", -1)
            ),
            "passed": recomputed_pass,
        }
        if any(row.get(name) != value for name, value in expected_fields.items()):
            errors.append(f"A-E prior-qualification world aggregation mismatch: {key}")
    if set(world_by_key) != expected_world_keys:
        errors.append("A-E prior-qualification world identity mismatch")

    task_by_id: dict[str, Mapping[str, Any]] = {}
    for row in task_rows:
        task_id = str(row.get("task_id", ""))
        if task_id in task_by_id:
            errors.append("A-E prior-qualification task identity is duplicated")
        task_by_id[task_id] = row
        child_rows = [
            child for key, child in world_by_key.items() if key[0] == task_id
        ]
        passed_worlds = sum(child.get("passed") is True for child in child_rows)
        recomputed_pass = len(child_rows) == 5 and passed_worlds == 5
        if (
            row.get("world_count") != len(child_rows)
            or row.get("passed_world_count") != passed_worlds
            or row.get("passed") is not recomputed_pass
        ):
            errors.append(f"A-E prior-qualification task aggregation mismatch: {task_id}")
    if set(task_by_id) != set(EXPECTED_TASKS):
        errors.append("A-E prior-qualification task identity mismatch")

    recomputed_counts = {
        "received_execution_receipts": len(receipt_bindings),
        "passed_regions": sum(row.get("passed") is True for row in region_rows),
        "passed_task_worlds": sum(row.get("passed") is True for row in world_rows),
        "passed_tasks": sum(row.get("passed") is True for row in task_rows),
    }
    for key, value in recomputed_counts.items():
        if denominators.get(key) != value:
            errors.append(f"A-E prior-qualification derived denominator mismatch: {key}")
    completed = denominators.get("completed_execution_receipts")
    if (
        isinstance(completed, bool)
        or not isinstance(completed, int)
        or not 0 <= completed <= EXPECTED_EXECUTION_COUNT
    ):
        errors.append("A-E prior-qualification completed receipt count is invalid")
    if evidence_receipts:
        evidence_completed = sum(
            receipt.get("status") == "completed" for receipt in evidence_receipts
        )
        if completed != evidence_completed:
            errors.append(
                "A-E prior-qualification completed receipt denominator differs from evidence"
            )

    failures = report.get("failures")
    if not isinstance(failures, list):
        errors.append("A-E prior-qualification failures must be a list")
        failures = []
    all_tasks_pass = (
        len(task_by_id) == EXPECTED_TASK_COUNT
        and all(row.get("passed") is True for row in task_by_id.values())
    )
    expected_status = "passed" if all_tasks_pass and not failures else "failed"
    if report.get("status") != expected_status:
        errors.append("A-E prior-qualification status/failures mismatch")
    if not all_tasks_pass and not failures:
        errors.append("failed A-E prior-qualification report omits failures")
    if report.get("status") == "passed" and completed != EXPECTED_EXECUTION_COUNT:
        errors.append("passed A-E prior-qualification report has incomplete executions")

    if evidence_plan is not None and len(evidence_receipts) == EXPECTED_EXECUTION_COUNT:
        evidence_report = build_qualification_report(
            evidence_plan, evidence_receipts, design
        )
        if report != evidence_report:
            errors.append(
                "A-E prior-qualification report does not match bound execution evidence"
            )
    return sorted(set(errors))


def markdown_summary(report: Mapping[str, Any]) -> str:
    denominators = report["denominators"]
    lines = [
        "# Work II A-E prior-distinguishability qualification",
        "",
        f"Status: **{report['status']}**",
        "",
        (
            f"Coverage: {denominators['tasks']} tasks, {denominators['task_worlds']} "
            f"task-worlds, {denominators['regions']} regions, "
            f"{denominators['paired_noise_replicates']} paired replicates and "
            f"{denominators['evaluator_executions']} zero-provider executions."
        ),
        "",
        (
            f"Passed: {denominators['passed_tasks']}/{denominators['tasks']} tasks, "
            f"{denominators['passed_task_worlds']}/{denominators['task_worlds']} worlds and "
            f"{denominators['passed_regions']}/{denominators['regions']} regions."
        ),
        "",
        f"Failures: {len(report['failures'])}.",
        "",
        (
            "This is an outcome-blind evaluator qualification; no participant "
            "outcome or H3 result is included."
        ),
        "",
    ]
    if report["failures"]:
        lines.extend(["## Failures", ""])
        for failure in report["failures"]:
            lines.append(f"- `{failure.get('check')}`: {json.dumps(failure, sort_keys=True)}")
        lines.append("")
    return "\n".join(lines)


def execute_qualification(
    root: Path, design_path: Path, output_root: Path
) -> dict[str, Any]:
    root = root.resolve()
    output_root = output_root.resolve()
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite qualification output: {output_root}")
    _require_clean_launch(root)
    design = _load_object(design_path.resolve())
    source_binding = _source_binding(root)
    if source_binding["tested_commit"] != git_source_commit(root):
        raise AEPriorQualificationError(
            "A-E qualification source commit changed during launch preflight"
        )
    plan = build_qualification_plan(
        root,
        design_path.resolve(),
        source_binding=source_binding,
    )
    plan_errors = validate_qualification_plan(root, plan, design)
    if plan_errors:
        raise AEPriorQualificationError(
            "qualification plan validation failed: " + "; ".join(plan_errors)
        )
    if git_worktree_dirty(root) or git_source_commit(root) != source_binding["tested_commit"]:
        raise AEPriorQualificationError(
            "A-E qualification source changed during launch preflight"
        )
    output_root.mkdir(parents=True)
    write_json_atomic(output_root / "plan.json", plan)
    receipts: list[dict[str, Any]] = []
    total = len(plan["executions"])
    started = time.perf_counter()
    for row in plan["executions"]:
        receipts.append(execute_one(root, plan, row, output_root))
        completed = len(receipts)
        elapsed_s = time.perf_counter() - started
        throughput = completed / elapsed_s if elapsed_s > 0.0 else 0.0
        eta_s = (
            (total - completed) / throughput
            if throughput > 0.0 and completed < total
            else 0.0
        )
        print(
            json.dumps(
                {
                    "stage": "ae_prior_qualification",
                    "completed": completed,
                    "total": total,
                    "task_id": row["task_id"],
                    "world_seed": row["world_seed"],
                    "throughput_fraction": completed / total,
                    "elapsed_s": round(elapsed_s, 3),
                    "throughput_executions_per_minute": round(throughput * 60.0, 3),
                    "eta_s": round(eta_s, 3),
                },
                sort_keys=True,
            ),
            flush=True,
        )
    report = build_qualification_report(plan, receipts, design)
    report_path = output_root / "report.json"
    write_json_atomic(report_path, report)
    errors = validate_qualification_report(
        root,
        report,
        design,
        report_path=report_path,
    )
    if errors:
        raise AEPriorQualificationError(
            "qualification report validation failed: " + "; ".join(errors)
        )
    (output_root / "summary.md").write_text(markdown_summary(report), encoding="utf-8")
    return report


__all__ = [
    "AE_MATERIAL_SOURCE_EXCLUSIONS",
    "AE_MATERIAL_SOURCE_ROOTS",
    "AE_PRIOR_QUALIFICATION_PLAN_VERSION",
    "AE_PRIOR_QUALIFICATION_REPORT_VERSION",
    "AE_SOURCE_BINDING_VERSION",
    "AEPriorQualificationError",
    "build_qualification_plan",
    "build_qualification_report",
    "execute_one",
    "execute_qualification",
    "markdown_summary",
    "validate_qualification_plan",
    "validate_qualification_report",
]
