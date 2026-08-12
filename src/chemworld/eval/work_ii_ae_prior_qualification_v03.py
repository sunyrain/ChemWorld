"""Development-only A-E v0.3 candidate screen and blind confirmation.

The module deliberately has no release mode.  It freezes a candidate screen, selects
one locus per task with an outcome-independent ordering, and builds a disjoint
confirmation plan.  Hidden pair truth enters only :func:`score_blind_world`.
"""

from __future__ import annotations

import hashlib
import json
import math
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
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_formal import build_checkpoint_contract
from chemworld.materials import static_material_information_dossier
from chemworld.tasks import get_task

CONTRACT_VERSION = (
    "chemworld-work-ii-ae-prior-distinguishability-candidate-contract-0.3"
)
PLAN_VERSION = "chemworld-work-ii-ae-prior-candidate-plan-0.3"
SELECTION_VERSION = "chemworld-work-ii-ae-prior-candidate-selection-0.3"
REPORT_VERSION = "chemworld-work-ii-ae-prior-candidate-report-0.3"
RECEIPT_VERSION = "chemworld-work-ii-ae-prior-candidate-receipt-0.3"
EXPECTED_TASKS = (
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "reaction-safety-constrained",
)
PHASES = ("candidate_screen", "confirmation")
TRANSPOSITIONS = tuple((left, right) for left in range(4) for right in range(left + 1, 4))
FORBIDDEN_CLASSIFIER_KEYS = frozenset(
    {
        "descriptor_permutation",
        "target_pair",
        "true_pair",
        "world_parameters",
        "hidden_outcomes",
        "world_seed",
    }
)


class AEPriorQualificationV03Error(ValueError):
    """Raised when v0.3 candidate-development semantics are violated."""


class _FrozenRecipeAgent(BaseAgent):
    name = "work_ii_ae_prior_candidate_v03_frozen_recipe"

    def __init__(self, actions: Sequence[Mapping[str, Any]]) -> None:
        self._actions = [deepcopy(dict(action)) for action in actions]

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._index = 0

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        if self._index >= len(self._actions):
            raise RuntimeError("frozen v0.3 candidate recipe exhausted")
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
        raise AEPriorQualificationV03Error(f"{path} must contain an object")
    return value


def _stable_seed(*parts: object) -> int:
    digest = hashlib.sha256(":".join(str(part) for part in parts).encode()).digest()
    return int.from_bytes(digest[:8], "big") % 2_147_483_647


def _cohort_seed(namespace: str, task_id: str, index: int) -> int:
    digest = hashlib.sha256(f"{namespace}:{task_id}:{index}".encode()).digest()
    return 1_000_000_000 + int.from_bytes(digest[:8], "big") % 900_000_000


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
        raise AEPriorQualificationV03Error(
            f"unsupported candidate locus: {task_id}.{target_field}"
        ) from error


def moved_pair(permutation: Sequence[Any]) -> tuple[int, int]:
    values = [int(value) for value in permutation]
    moved = [index for index, source in enumerate(values) if index != source]
    if (
        len(values) != 4
        or sorted(values) != [0, 1, 2, 3]
        or len(moved) != 2
        or values[moved[0]] != moved[1]
        or values[moved[1]] != moved[0]
    ):
        raise AEPriorQualificationV03Error(
            "candidate descriptor permutation must be one four-category transposition"
        )
    return moved[0], moved[1]


def _known_earlier_seeds(root: Path) -> set[int]:
    seeds = {0, 1, 2, 3, 4}
    v01 = _load_object(root / "configs/benchmark/work_ii_formal_design_v0.1.json")
    for values in v01["world_cohort"]["public_formal"]["task_world_seeds"].values():
        seeds.update(int(value) for value in values)
    v02 = _load_object(
        root / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.2.json"
    )
    for cohort in v02["cohorts"].values():
        for values in cohort["task_world_seeds"].values():
            seeds.update(int(value) for value in values)
    return seeds


def _material_family_id(task_id: str, config: Mapping[str, Any]) -> object | None:
    if task_id == "electrochemical-conversion":
        return config.get("electrochemical_material_family_id")
    if task_id == "reaction-to-crystallization":
        return config.get("crystallization_material_family_id")
    return None


def _candidate_dossier(
    task_id: str,
    target_field: str,
    permutation: Sequence[int],
    config: Mapping[str, Any],
) -> dict[str, Any]:
    dossier = static_material_information_dossier(
        {
            "mode": "anonymous_misindexed_properties",
            "target_field": target_field,
            "descriptor_permutation": list(permutation),
        },
        task_id=task_id,
        material_family_id=_material_family_id(task_id, config),
    )
    if not isinstance(dossier, dict):
        raise AEPriorQualificationV03Error(
            f"candidate locus has no agent-visible dossier: {task_id}.{target_field}"
        )
    choices = dossier.get("choices")
    rows = choices.get(target_field) if isinstance(choices, Mapping) else None
    if not isinstance(rows, list) or len(rows) != 4:
        raise AEPriorQualificationV03Error(
            f"candidate dossier lacks four categories: {task_id}.{target_field}"
        )
    return dossier


def validate_contract(root: Path, contract: Mapping[str, Any]) -> list[str]:
    """Validate scientific coverage before any environment execution."""

    errors: list[str] = []
    expected = {
        "schema_version": CONTRACT_VERSION,
        "contract_id": "work-ii-ae-prior-distinguishability-v0.3-candidate-development",
        "status": "candidate_development_not_executed",
        "development_only": True,
        "participant_provider_calls": 0,
        "participant_outcomes_read": False,
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            errors.append(f"invalid v0.3 scalar contract field: {key}")
    note = contract.get("experiment_note")
    if not isinstance(note, str) or not (root / note).is_file():
        errors.append("v0.3 experiment note is missing")
    classifier = contract.get("classifier")
    if not isinstance(classifier, Mapping):
        errors.append("blind classifier contract is missing")
    else:
        if set(classifier.get("forbidden_inputs", [])) != (
            FORBIDDEN_CLASSIFIER_KEYS - {"world_seed"}
        ):
            errors.append("blind classifier forbidden-input contract changed")
        if classifier.get("minimum_nll_margin") != 2.0:
            errors.append("blind classifier NLL margin changed")
    coverage = contract.get("coverage")
    frozen_coverage = {
        "anchors_per_candidate_world": 2,
        "categories_per_anchor": 4,
        "independent_replicates_per_anchor_category": 3,
        "screen_worlds_per_task": 5,
        "confirmation_worlds_per_task": 5,
        "candidates_per_task": 2,
    }
    if not isinstance(coverage, Mapping) or any(
        coverage.get(key) != value for key, value in frozen_coverage.items()
    ):
        errors.append("v0.3 2x5x2x4x3 coverage changed")
    thresholds = contract.get("thresholds")
    if not isinstance(thresholds, Mapping) or (
        thresholds.get("minimum_absolute_primary_endpoint_separation") != 0.05
        or thresholds.get("minimum_primary_endpoint_signal_to_noise_ratio") != 2.0
        or thresholds.get("all_five_screen_worlds_must_pass") is not True
        or thresholds.get("all_five_confirmation_worlds_must_pass") is not True
    ):
        errors.append("v0.3 scientific thresholds changed")
    denominators = contract.get("denominators")
    expected_denominators = {
        "tasks": 5,
        "screen_candidates": 10,
        "screen_task_candidate_worlds": 50,
        "screen_primary_executions": 1200,
        "screen_exact_replays": 1200,
        "confirmation_selected_loci": 5,
        "confirmation_task_locus_worlds": 25,
        "confirmation_primary_executions": 600,
        "confirmation_exact_replays": 600,
    }
    if denominators != expected_denominators:
        errors.append("v0.3 exact denominators changed")

    tasks = contract.get("tasks")
    if not isinstance(tasks, list) or tuple(
        str(row.get("task_id")) for row in tasks if isinstance(row, Mapping)
    ) != EXPECTED_TASKS:
        errors.append("v0.3 requires the exact five-task roster")
        tasks = []
    for row in tasks:
        task_id = str(row["task_id"])
        try:
            config_path = (root / str(row["campaign_config"])).resolve()
            if not config_path.is_relative_to(root.resolve()) or not config_path.is_file():
                raise AEPriorQualificationV03Error("campaign config is missing or escapes root")
            config = _load_object(config_path)
            if config.get("task_id") != task_id:
                raise AEPriorQualificationV03Error("campaign config task mismatch")
            allowed = set(
                build_checkpoint_contract(config, "aligned_nominal")["allowed_metric_ids"]
            )
            primary = row.get("primary_endpoint_ids")
            secondary = row.get("secondary_metric_ids")
            if (
                not isinstance(primary, list)
                or not primary
                or not isinstance(secondary, list)
                or set(primary) & set(secondary)
                or set(primary) | set(secondary) != allowed
            ):
                raise AEPriorQualificationV03Error(
                    "primary endpoints and secondary metrics do not partition allowed metrics"
                )
            candidates = row.get("candidates")
            if not isinstance(candidates, list) or len(candidates) != 2:
                raise AEPriorQualificationV03Error("task does not have exactly two candidates")
            candidate_ids: set[str] = set()
            priorities: set[int] = set()
            fields: set[str] = set()
            for candidate in candidates:
                candidate_id = str(candidate["candidate_id"])
                priority = int(candidate["scientific_priority"])
                field = str(candidate["target_field"])
                _target_coordinate(task_id, field)
                moved_pair(candidate["descriptor_permutation"])
                _candidate_dossier(
                    task_id, field, candidate["descriptor_permutation"], config
                )
                candidate_ids.add(candidate_id)
                priorities.add(priority)
                fields.add(field)
            if len(candidate_ids) != 2 or priorities != {1, 2} or len(fields) != 2:
                raise AEPriorQualificationV03Error(
                    "candidate IDs, priorities, and loci must be unique"
                )
        except (KeyError, TypeError, ValueError) as error:
            errors.append(f"invalid candidate design for {task_id}: {error}")

    cohorts = contract.get("cohorts")
    cohorts = cohorts if isinstance(cohorts, Mapping) else {}
    earlier = _known_earlier_seeds(root)
    phase_sets: dict[str, set[int]] = {}
    for phase in PHASES:
        cohort = cohorts.get(phase)
        cohort = cohort if isinstance(cohort, Mapping) else {}
        namespace = cohort.get("selection_namespace")
        by_task = cohort.get("task_world_seeds")
        phase_seeds: set[int] = set()
        if not isinstance(namespace, str) or not isinstance(by_task, Mapping):
            errors.append(f"{phase} cohort is malformed")
            continue
        for task_id in EXPECTED_TASKS:
            values = by_task.get(task_id)
            expected_values = [_cohort_seed(namespace, task_id, index) for index in range(5)]
            if values != expected_values:
                errors.append(f"{phase} seeds are not the frozen five for {task_id}")
                continue
            phase_seeds.update(int(value) for value in values)
        if phase_seeds & earlier:
            errors.append(f"{phase} collides with a v0.1/v0.2 seed")
        phase_sets[phase] = phase_seeds
    if phase_sets.get("candidate_screen", set()) & phase_sets.get("confirmation", set()):
        errors.append("screen and confirmation seeds collide")
    return errors


def _anchors(
    task_id: str,
    candidate_id: str,
    target_coordinate: int,
    dimension: int,
    coverage: Mapping[str, Any],
) -> tuple[np.ndarray, np.ndarray]:
    namespace = str(coverage["anchor_namespace"])
    lower = float(coverage["anchor_lower_bound"])
    upper = float(coverage["anchor_upper_bound"])
    first = np.empty(dimension, dtype=float)
    for coordinate in range(dimension):
        digest = hashlib.sha256(
            f"{namespace}:{task_id}:{candidate_id}:coordinate-{coordinate}".encode()
        ).digest()
        unit = int.from_bytes(digest[:8], "big") / float(2**64)
        first[coordinate] = round(lower + (upper - lower) * unit, 9)
    second = np.asarray(
        [round(lower + upper - float(value), 9) for value in first], dtype=float
    )
    first[target_coordinate] = second[target_coordinate] = 0.5
    return first, second


def build_candidate_schedule(
    *,
    task_id: str,
    candidate_id: str,
    target_field: str,
    coverage: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Build two task/candidate-aware anchors without accepting truth or outcomes."""

    target_coordinate = _target_coordinate(task_id, target_field)
    task_info = get_task(task_id).to_dict()
    anchors = _anchors(
        task_id,
        candidate_id,
        target_coordinate,
        task_recipe_dimension(task_info),
        coverage,
    )
    schedule: list[dict[str, Any]] = []
    for anchor_id, vector in enumerate(anchors):
        for category in range(4):
            candidate_vector = vector.copy()
            candidate_vector[target_coordinate] = (category + 0.5) / 4.0
            recipe = task_recipe_from_unit_vector(task_info, candidate_vector)
            schedule.append(
                {
                    "anchor_id": anchor_id,
                    "target_category": category,
                    "target_coordinate": target_coordinate,
                    "recipe_id": f"{task_id}:{candidate_id}:a{anchor_id}:c{category}",
                    "recipe": recipe,
                }
            )
    return schedule


def _build_plan(
    root: Path,
    contract_path: Path,
    contract: Mapping[str, Any],
    phase: str,
    selected: Mapping[str, str] | None,
) -> dict[str, Any]:
    tasks = {str(row["task_id"]): row for row in contract["tasks"]}
    executions: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    for task_id in EXPECTED_TASKS:
        task_row = tasks[task_id]
        config = _load_object(root / task_row["campaign_config"])
        candidates = list(task_row["candidates"])
        if phase == "confirmation":
            if selected is None or task_id not in selected:
                continue
            candidates = [
                item for item in candidates if item["candidate_id"] == selected[task_id]
            ]
            if len(candidates) != 1:
                raise AEPriorQualificationV03Error(
                    f"selected candidate is not frozen for {task_id}"
                )
        allowed = list(build_checkpoint_contract(config, "aligned_nominal")["allowed_metric_ids"])
        bindings.append(
            {
                "task_id": task_id,
                "campaign_config": task_row["campaign_config"],
                "campaign_config_sha256": canonical_json_sha256(config),
                "allowed_metric_ids": allowed,
                "primary_endpoint_ids": list(task_row["primary_endpoint_ids"]),
                "secondary_metric_ids": list(task_row["secondary_metric_ids"]),
            }
        )
        for candidate in candidates:
            dossier = _candidate_dossier(
                task_id,
                candidate["target_field"],
                candidate["descriptor_permutation"],
                config,
            )
            schedule = build_candidate_schedule(
                task_id=task_id,
                candidate_id=candidate["candidate_id"],
                target_field=candidate["target_field"],
                coverage=contract["coverage"],
            )
            for world_seed in contract["cohorts"][phase]["task_world_seeds"][task_id]:
                for replicate in range(3):
                    for item in schedule:
                        coordinate = (
                            phase,
                            task_id,
                            candidate["candidate_id"],
                            world_seed,
                            item["anchor_id"],
                            item["target_category"],
                            replicate,
                        )
                        noise_namespace = contract["noise"]["seed_namespace"]
                        executions.append(
                            {
                                "execution_index": len(executions),
                                "execution_id": "v0.3:" + ":".join(map(str, coordinate)),
                                "phase": phase,
                                "task_id": task_id,
                                "candidate_id": candidate["candidate_id"],
                                "scientific_priority": candidate["scientific_priority"],
                                "target_field": candidate["target_field"],
                                "descriptor_permutation": list(
                                    candidate["descriptor_permutation"]
                                ),
                                "world_seed": world_seed,
                                "anchor_id": item["anchor_id"],
                                "target_category": item["target_category"],
                                "replicate": replicate,
                                "allowed_metric_ids": allowed,
                                "primary_endpoint_ids": list(
                                    task_row["primary_endpoint_ids"]
                                ),
                                "secondary_metric_ids": list(
                                    task_row["secondary_metric_ids"]
                                ),
                                "agent_visible_dossier": dossier,
                                "agent_visible_dossier_sha256": canonical_json_sha256(
                                    dossier
                                ),
                                "observation_seed": _stable_seed(
                                    noise_namespace, *coordinate
                                ),
                                "observation_noise_namespace": (
                                    f"{noise_namespace}:" + ":".join(map(str, coordinate))
                                ),
                                "recipe_id": item["recipe_id"],
                                "recipe": item["recipe"],
                            }
                        )
    expected = 1200 if phase == "candidate_screen" else 600
    if len(executions) != expected:
        raise AEPriorQualificationV03Error(
            f"{phase} plan has {len(executions)} executions, expected {expected}"
        )
    payload = {
        "schema_version": PLAN_VERSION,
        "development_only": True,
        "phase": phase,
        "contract_binding": {
            "path": contract_path.relative_to(root).as_posix(),
            "canonical_sha256": canonical_json_sha256(contract),
        },
        "participant_provider_calls": 0,
        "task_bindings": bindings,
        "selected_candidate_ids": dict(selected or {}),
        "denominators": {
            "primary_executions": expected,
            "exact_replays": expected,
        },
        "executions": executions,
    }
    payload["plan_sha256"] = canonical_json_sha256(payload)
    return payload


def build_screen_plan(root: Path, contract_path: Path) -> dict[str, Any]:
    root = root.resolve()
    contract_path = contract_path.resolve()
    contract = _load_object(contract_path)
    errors = validate_contract(root, contract)
    if errors:
        raise AEPriorQualificationV03Error("invalid v0.3 contract: " + "; ".join(errors))
    return _build_plan(root, contract_path, contract, "candidate_screen", None)


def build_confirmation_plan(
    root: Path,
    contract_path: Path,
    selection: Mapping[str, Any],
    screen_report: Mapping[str, Any],
) -> dict[str, Any]:
    root = root.resolve()
    contract_path = contract_path.resolve()
    contract = _load_object(contract_path)
    errors = validate_contract(root, contract)
    if errors:
        raise AEPriorQualificationV03Error("invalid v0.3 contract: " + "; ".join(errors))
    if (
        screen_report.get("schema_version") != REPORT_VERSION
        or screen_report.get("phase") != "candidate_screen"
        or screen_report.get("development_only") is not True
    ):
        raise AEPriorQualificationV03Error(
            "confirmation requires the complete v0.3 screen report"
        )
    world_results = screen_report.get("world_results")
    if not isinstance(world_results, list) or len(world_results) != 50:
        raise AEPriorQualificationV03Error(
            "confirmation requires all 50 screen candidate-world results"
        )
    expected_selection = select_screen_candidates(contract, world_results)
    if dict(selection) != expected_selection:
        raise AEPriorQualificationV03Error(
            "confirmation selection differs from the registered screen rule"
        )
    selected = selection.get("selected_candidate_ids")
    if not isinstance(selected, Mapping) or set(selected) != set(EXPECTED_TASKS):
        raise AEPriorQualificationV03Error(
            "confirmation requires one screen-selected candidate for every task"
        )
    return _build_plan(
        root, contract_path, contract, "confirmation", {str(k): str(v) for k, v in selected.items()}
    )


def _find_forbidden_key(value: object, path: str = "classifier_input") -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key) in FORBIDDEN_CLASSIFIER_KEYS:
                return f"{path}.{key}"
            found = _find_forbidden_key(item, f"{path}.{key}")
            if found is not None:
                return found
    elif isinstance(value, Sequence) and not isinstance(value, str | bytes):
        for index, item in enumerate(value):
            found = _find_forbidden_key(item, f"{path}[{index}]")
            if found is not None:
                return found
    return None


def _descriptor_vectors(dossier: Mapping[str, Any], target_field: str) -> np.ndarray:
    choices = dossier.get("choices")
    rows = choices.get(target_field) if isinstance(choices, Mapping) else None
    if not isinstance(rows, list) or len(rows) != 4:
        raise AEPriorQualificationV03Error("classifier dossier lacks four target choices")
    vectors: list[dict[str, float]] = []
    for category, row in enumerate(rows):
        if not isinstance(row, Mapping) or row.get("action_value") != category:
            raise AEPriorQualificationV03Error("classifier dossier category order is invalid")
        properties = row.get("nominal_properties")
        if not isinstance(properties, Mapping) or not properties:
            raise AEPriorQualificationV03Error("classifier dossier properties are missing")
        numeric: dict[str, float] = {}
        for key, value in properties.items():
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise AEPriorQualificationV03Error("classifier dossier is not numeric")
            number = float(value)
            if not math.isfinite(number):
                raise AEPriorQualificationV03Error("classifier dossier is not finite")
            numeric[str(key)] = number
        vectors.append(numeric)
    keys = sorted(vectors[0])
    if not keys or any(sorted(row) != keys for row in vectors):
        raise AEPriorQualificationV03Error("classifier dossier property schema differs by category")
    matrix = np.asarray([[row[key] for key in keys] for row in vectors], dtype=float)
    spread = np.std(matrix, axis=0)
    usable = spread > 1.0e-12
    if not bool(np.any(usable)):
        raise AEPriorQualificationV03Error("classifier dossier has no varying descriptor")
    return (matrix[:, usable] - np.mean(matrix[:, usable], axis=0)) / spread[usable]


def _hypothesis_permutation(pair: tuple[int, int] | None) -> np.ndarray:
    permutation = np.arange(4)
    if pair is not None:
        permutation[pair[0]], permutation[pair[1]] = permutation[pair[1]], permutation[pair[0]]
    return permutation


def blind_classify_transposition(
    *,
    dossier: Mapping[str, Any],
    task_id: str,
    target_field: str,
    anchor_ids: Sequence[int],
    support_observations: Sequence[Mapping[str, Any]],
    observation_sigma: Mapping[str, Any],
    minimum_nll_margin: float = 2.0,
) -> dict[str, Any]:
    """Classify H0 plus six swaps without accepting or reading hidden truth."""

    payload = {
        "dossier": dossier,
        "task_id": task_id,
        "target_field": target_field,
        "anchor_ids": list(anchor_ids),
        "support_observations": list(support_observations),
        "observation_sigma": observation_sigma,
    }
    forbidden = _find_forbidden_key(payload)
    if forbidden is not None:
        raise AEPriorQualificationV03Error(
            f"forbidden blind-classifier input: {forbidden}"
        )
    if tuple(anchor_ids) != (0, 1):
        raise AEPriorQualificationV03Error("classifier requires exact anchor IDs [0, 1]")
    descriptors = _descriptor_vectors(dossier, target_field)
    rows: list[tuple[int, int, int, Mapping[str, Any]]] = []
    metric_ids: set[str] | None = None
    for row in support_observations:
        if set(row) != {"anchor_id", "target_category", "replicate", "metrics"}:
            raise AEPriorQualificationV03Error("classifier observation exposes unregistered fields")
        anchor = int(row["anchor_id"])
        category = int(row["target_category"])
        replicate = int(row["replicate"])
        metrics = row["metrics"]
        if anchor not in {0, 1} or category not in range(4) or replicate not in range(3):
            raise AEPriorQualificationV03Error("classifier observation coordinate is invalid")
        if not isinstance(metrics, Mapping) or not metrics:
            raise AEPriorQualificationV03Error("classifier primary endpoints are missing")
        current = {str(key) for key in metrics}
        if metric_ids is None:
            metric_ids = current
        elif current != metric_ids:
            raise AEPriorQualificationV03Error("classifier endpoint coverage is inconsistent")
        if any(
            isinstance(value, bool)
            or not isinstance(value, int | float)
            or not math.isfinite(float(value))
            for value in metrics.values()
        ):
            raise AEPriorQualificationV03Error("classifier endpoints must be finite numbers")
        rows.append((anchor, category, replicate, metrics))
    expected_coordinates = {(a, c, r) for a in range(2) for c in range(4) for r in range(3)}
    if {(a, c, r) for a, c, r, _ in rows} != expected_coordinates or len(rows) != 24:
        raise AEPriorQualificationV03Error("classifier requires exact 2x4x3 observations")
    assert metric_ids is not None

    hypotheses: list[tuple[str, tuple[int, int] | None]] = [("H0", None)] + [
        (f"swap-{left}-{right}", (left, right)) for left, right in TRANSPOSITIONS
    ]
    nll_by_hypothesis: dict[str, float] = {}
    for hypothesis_id, pair in hypotheses:
        permutation = _hypothesis_permutation(pair)
        total = 0.0
        for anchor in (0, 1):
            observed_distances: list[float] = []
            descriptor_distances: list[float] = []
            for left, right in TRANSPOSITIONS:
                normalized_differences: list[float] = []
                for metric in sorted(metric_ids):
                    left_values = [
                        float(row[3][metric])
                        for row in rows
                        if row[0] == anchor and row[1] == left
                    ]
                    right_values = [
                        float(row[3][metric])
                        for row in rows
                        if row[0] == anchor and row[1] == right
                    ]
                    left_sigma = float(observation_sigma[str(anchor)][str(left)][metric])
                    right_sigma = float(observation_sigma[str(anchor)][str(right)][metric])
                    standard_error = math.sqrt(
                        left_sigma**2 / 3.0 + right_sigma**2 / 3.0
                    )
                    if not math.isfinite(standard_error) or standard_error <= 0.0:
                        raise AEPriorQualificationV03Error(
                            "classifier sigma must be finite and positive"
                        )
                    normalized_differences.append(
                        (fmean(right_values) - fmean(left_values)) / standard_error
                    )
                observed_distances.append(float(np.linalg.norm(normalized_differences)))
                descriptor_distances.append(
                    float(
                        np.linalg.norm(
                            descriptors[permutation[right]]
                            - descriptors[permutation[left]]
                        )
                    )
                )
            observed_vector = np.asarray(observed_distances)
            descriptor_vector = np.asarray(descriptor_distances)
            denominator = float(descriptor_vector @ descriptor_vector)
            if denominator <= 0.0:
                raise AEPriorQualificationV03Error(
                    "classifier descriptor geometry is degenerate"
                )
            scale = max(0.0, float(descriptor_vector @ observed_vector) / denominator)
            residual = observed_vector - scale * descriptor_vector
            total += float(
                0.5 * np.sum(residual**2 + math.log(2.0 * math.pi))
            )
        nll_by_hypothesis[hypothesis_id] = total
    ordered = sorted(nll_by_hypothesis.items(), key=lambda item: (item[1], item[0]))
    margin = ordered[1][1] - ordered[0][1]
    best = ordered[0][0]
    classified = best.startswith("swap-") and margin >= minimum_nll_margin
    pair = tuple(int(value) for value in best.split("-")[1:]) if classified else None
    return {
        "classifier_id": "blind-dossier-weighted-linear-nll-v0.1",
        "task_id": task_id,
        "target_field": target_field,
        "hypothesis_nll": nll_by_hypothesis,
        "best_hypothesis": best,
        "nll_margin": margin,
        "decision": "pair" if classified else "abstain",
        "predicted_pair": list(pair) if pair is not None else None,
    }


def _empirical_sigma(
    observations: Sequence[Mapping[str, Any]], metric_ids: Sequence[str], floor: float
) -> dict[str, dict[str, dict[str, float]]]:
    output: dict[str, dict[str, dict[str, float]]] = {}
    for anchor in range(2):
        output[str(anchor)] = {}
        for category in range(4):
            subset = [
                row
                for row in observations
                if row["anchor_id"] == anchor and row["target_category"] == category
            ]
            output[str(anchor)][str(category)] = {
                metric: max(
                    floor,
                    math.sqrt(variance([float(row["metrics"][metric]) for row in subset])),
                )
                for metric in metric_ids
            }
    return output


def score_blind_world(
    *,
    dossier: Mapping[str, Any],
    task_id: str,
    target_field: str,
    primary_endpoint_ids: Sequence[str],
    observations: Sequence[Mapping[str, Any]],
    true_pair: Sequence[int],
    thresholds: Mapping[str, Any],
    sigma_floor: float,
) -> dict[str, Any]:
    """Score a blind decision; truth is isolated here and never passed to classifier."""

    pair = moved_pair(_hypothesis_permutation(tuple(int(value) for value in true_pair)))
    sigma = _empirical_sigma(observations, primary_endpoint_ids, sigma_floor)
    classification = blind_classify_transposition(
        dossier=dossier,
        task_id=task_id,
        target_field=target_field,
        anchor_ids=[0, 1],
        support_observations=observations,
        observation_sigma=sigma,
        minimum_nll_margin=float(thresholds["minimum_classifier_nll_margin"]),
    )
    anchor_results: list[dict[str, Any]] = []
    for anchor in range(2):
        endpoint_results: dict[str, Any] = {}
        for metric in primary_endpoint_ids:
            left = [
                float(row["metrics"][metric])
                for row in observations
                if row["anchor_id"] == anchor and row["target_category"] == pair[0]
            ]
            right = [
                float(row["metrics"][metric])
                for row in observations
                if row["anchor_id"] == anchor and row["target_category"] == pair[1]
            ]
            standard_error = math.sqrt(variance(left) / 3.0 + variance(right) / 3.0)
            separation = abs(fmean(right) - fmean(left))
            snr = separation / max(standard_error, sigma_floor)
            endpoint_results[metric] = {
                "absolute_separation": separation,
                "welch_standard_error": standard_error,
                "signal_to_noise_ratio": snr,
                "passed": separation
                >= float(thresholds["minimum_absolute_primary_endpoint_separation"])
                and snr
                >= float(thresholds["minimum_primary_endpoint_signal_to_noise_ratio"]),
            }
        anchor_results.append(
            {
                "anchor_id": anchor,
                "primary_endpoint_results": endpoint_results,
                "passed": all(item["passed"] for item in endpoint_results.values()),
            }
        )
    classifier_correct = classification["predicted_pair"] == list(pair)
    return {
        "classification": classification,
        "classifier_correct": classifier_correct,
        "anchor_results": anchor_results,
        "passed": classifier_correct and all(row["passed"] for row in anchor_results),
    }


def select_screen_candidates(
    contract: Mapping[str, Any], screen_results: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Select by frozen priority/ID only; observed effect sizes never rank candidates."""

    indexed: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for row in screen_results:
        indexed[(str(row["task_id"]), str(row["candidate_id"]))].append(row)
    selected: dict[str, str] = {}
    disposition: list[dict[str, Any]] = []
    for task in contract["tasks"]:
        task_id = str(task["task_id"])
        ordered = sorted(
            task["candidates"],
            key=lambda row: (int(row["scientific_priority"]), str(row["candidate_id"])),
        )
        eligible: list[str] = []
        for candidate in ordered:
            candidate_id = str(candidate["candidate_id"])
            worlds = indexed[(task_id, candidate_id)]
            is_eligible = (
                len(worlds) == 5
                and len({int(row["world_seed"]) for row in worlds}) == 5
                and all(row.get("passed") is True for row in worlds)
            )
            if is_eligible:
                eligible.append(candidate_id)
            disposition.append(
                {
                    "task_id": task_id,
                    "candidate_id": candidate_id,
                    "screen_worlds": len(worlds),
                    "eligible": is_eligible,
                }
            )
        if eligible:
            selected[task_id] = eligible[0]
    payload = {
        "schema_version": SELECTION_VERSION,
        "development_only": True,
        "selection_rule": deepcopy(contract["selection_rule"]),
        "selected_candidate_ids": selected,
        "all_tasks_selected": set(selected) == set(EXPECTED_TASKS),
        "candidate_disposition": disposition,
        "screen_results_sha256": canonical_json_sha256(list(screen_results)),
    }
    payload["selection_sha256"] = canonical_json_sha256(payload)
    return payload


def build_phase_report(
    contract: Mapping[str, Any],
    plan: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build exact-denominator world decisions and retain every failed attempt."""

    errors = validate_receipt_denominator(plan, receipts)
    if errors:
        raise AEPriorQualificationV03Error("invalid phase evidence: " + "; ".join(errors))
    planned = {row["execution_id"]: row for row in plan["executions"]}
    grouped: dict[tuple[str, str, int], list[Mapping[str, Any]]] = defaultdict(list)
    for receipt in receipts:
        row = planned[str(receipt["execution_id"])]
        grouped[
            (str(row["task_id"]), str(row["candidate_id"]), int(row["world_seed"]))
        ].append(receipt)
    thresholds = contract["thresholds"]
    task_specs = {str(row["task_id"]): row for row in contract["tasks"]}
    world_results: list[dict[str, Any]] = []
    for key in sorted(grouped):
        task_id, candidate_id, world_seed = key
        rows = grouped[key]
        first_plan = planned[str(rows[0]["execution_id"])]
        completed = [row for row in rows if row.get("status") == "completed"]
        result: dict[str, Any] = {
            "task_id": task_id,
            "candidate_id": candidate_id,
            "world_seed": world_seed,
            "planned_primary_executions": 24,
            "completed_primary_executions": len(completed),
            "exact_replays_verified": sum(
                1
                for row in completed
                if isinstance(row.get("exact_replay"), Mapping)
                and row["exact_replay"].get("verified") is True
            ),
            "failures": [deepcopy(row["failure"]) for row in rows if row.get("failure")],
        }
        if len(completed) != 24:
            result.update(
                {
                    "classification": None,
                    "classifier_correct": False,
                    "anchor_results": [],
                    "passed": False,
                }
            )
        else:
            observations = [
                {
                    "anchor_id": int(row["anchor_id"]),
                    "target_category": int(row["target_category"]),
                    "replicate": int(row["replicate"]),
                    "metrics": dict(row["primary_endpoints"]),
                }
                for row in completed
            ]
            scored = score_blind_world(
                dossier=first_plan["agent_visible_dossier"],
                task_id=task_id,
                target_field=str(first_plan["target_field"]),
                primary_endpoint_ids=task_specs[task_id]["primary_endpoint_ids"],
                observations=observations,
                true_pair=moved_pair(first_plan["descriptor_permutation"]),
                thresholds=thresholds,
                sigma_floor=float(contract["noise"]["sigma_floor"]),
            )
            result.update(scored)
        world_results.append(result)
    expected_worlds = 50 if plan["phase"] == "candidate_screen" else 25
    if len(world_results) != expected_worlds:
        raise AEPriorQualificationV03Error(
            f"phase report has {len(world_results)} worlds, expected {expected_worlds}"
        )
    candidate_results: list[dict[str, Any]] = []
    for (task_id, candidate_id), worlds in sorted(
        {
            (row["task_id"], row["candidate_id"]): [
                other
                for other in world_results
                if other["task_id"] == row["task_id"]
                and other["candidate_id"] == row["candidate_id"]
            ]
            for row in world_results
        }.items()
    ):
        candidate_results.append(
            {
                "task_id": task_id,
                "candidate_id": candidate_id,
                "worlds_passed": sum(1 for row in worlds if row["passed"]),
                "worlds_total": len(worlds),
                "passed": len(worlds) == 5 and all(row["passed"] for row in worlds),
            }
        )
    report = {
        "schema_version": REPORT_VERSION,
        "development_only": True,
        "phase": plan["phase"],
        "plan_sha256": plan["plan_sha256"],
        "denominators": {
            "planned_primary_executions": len(plan["executions"]),
            "attempted_primary_executions": len(receipts),
            "completed_primary_executions": sum(
                1 for row in receipts if row.get("status") == "completed"
            ),
            "exact_replays_verified": sum(
                1
                for row in receipts
                if isinstance(row.get("exact_replay"), Mapping)
                and row["exact_replay"].get("verified") is True
            ),
            "worlds": len(world_results),
        },
        "world_results": world_results,
        "candidate_results": candidate_results,
        "failures": [
            {
                "execution_id": row.get("execution_id"),
                "failure": deepcopy(row.get("failure")),
            }
            for row in receipts
            if row.get("failure") is not None
        ],
    }
    if plan["phase"] == "candidate_screen":
        passed = all(
            any(
                row["task_id"] == task_id and row["passed"]
                for row in candidate_results
            )
            for task_id in EXPECTED_TASKS
        )
    else:
        passed = len(candidate_results) == 5 and all(
            row["passed"] for row in candidate_results
        )
    report["status"] = "passed" if passed else "scientifically_rejected"
    report["report_sha256"] = canonical_json_sha256(report)
    return report


def execute_one(
    root: Path, plan: Mapping[str, Any], row: Mapping[str, Any], output_root: Path
) -> dict[str, Any]:
    """Execute and exact-replay one provider-free candidate recipe."""

    binding = next(
        item for item in plan["task_bindings"] if item["task_id"] == row["task_id"]
    )
    config = _load_object(root / binding["campaign_config"])
    execution_root = output_root / "executions" / str(row["execution_index"])
    execution_root.mkdir(parents=True, exist_ok=False)
    trajectory = execution_root / "trajectory.jsonl"
    receipt = {
        key: deepcopy(value)
        for key, value in row.items()
        if key not in {"agent_visible_dossier", "descriptor_permutation"}
    }
    receipt.update({"schema_version": RECEIPT_VERSION, "plan_sha256": plan["plan_sha256"]})
    try:
        actions = row["recipe"]["steps"]
        material_information = {
            "mode": "anonymous_misindexed_properties",
            "target_field": row["target_field"],
            "descriptor_permutation": row["descriptor_permutation"],
        }
        run_agent(
            env_id=get_task(str(row["task_id"])).env_id,
            agent=_FrozenRecipeAgent(actions),
            world_split=str(config["world_split"]),
            budget=len(actions),
            objective=str(config["objective"]),
            seed=int(row["world_seed"]),
            observation_seed=int(row["observation_seed"]),
            task_id=str(row["task_id"]),
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            material_information=material_information,
            electrochemical_material_family_id=config.get("electrochemical_material_family_id"),
            crystallization_material_family_id=config.get("crystallization_material_family_id"),
            electrochemical_workflow_mode=config.get("electrochemical_workflow_mode"),
            scoring_contract_id=config.get("scoring_contract_id"),
            observation_noise_mode="keyed",
            observation_noise_namespace=str(row["observation_noise_namespace"]),
            world_interventions=config.get("world_interventions", []),
        )
        records = load_jsonl(trajectory)
        final = [
            item
            for item in records
            if item.get("instrument") == "final_assay"
            and item.get("transaction_status") == "committed"
        ]
        if len(final) != 1:
            raise AEPriorQualificationV03Error("execution lacks one committed final assay")
        observation = final[0].get("observation")
        if not isinstance(observation, Mapping):
            raise AEPriorQualificationV03Error("execution lacks final observation")
        metrics = {metric: float(observation[metric]) for metric in row["allowed_metric_ids"]}
        if any(not math.isfinite(value) or not 0.0 <= value <= 1.0 for value in metrics.values()):
            raise AEPriorQualificationV03Error("allowed metric is outside finite [0,1]")
        replay = verify_records(
            records, tolerance=0.0, world_interventions=config.get("world_interventions", [])
        ).to_dict()
        if replay.get("verified") is not True:
            raise AEPriorQualificationV03Error("tolerance-zero exact replay failed")
        receipt.update(
            {
                "status": "completed",
                "primary_endpoints": {
                    metric: metrics[metric] for metric in row["primary_endpoint_ids"]
                },
                "secondary_metrics": {
                    metric: metrics[metric] for metric in row["secondary_metric_ids"]
                },
                "exact_replay": replay,
                "trajectory": {
                    "path": trajectory.relative_to(output_root).as_posix(),
                    "sha256": file_sha256(trajectory),
                },
                "failure": None,
            }
        )
    except Exception as error:
        receipt.update(
            {
                "status": "failed",
                "primary_endpoints": None,
                "secondary_metrics": None,
                "exact_replay": None,
                "trajectory": None,
                "failure": {"type": type(error).__name__, "message": str(error)},
            }
        )
    receipt["receipt_sha256"] = canonical_json_sha256(receipt)
    return receipt


def validate_plan(plan: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != PLAN_VERSION or plan.get("development_only") is not True:
        errors.append("plan is not development-only v0.3")
    phase = plan.get("phase")
    expected = 1200 if phase == "candidate_screen" else 600 if phase == "confirmation" else -1
    executions = plan.get("executions")
    if not isinstance(executions, list) or len(executions) != expected:
        errors.append("plan execution denominator is invalid")
        executions = []
    if len({row.get("execution_id") for row in executions}) != len(executions):
        errors.append("plan execution IDs are not unique")
    coordinates = {
        (
            row.get("task_id"),
            row.get("candidate_id"),
            row.get("world_seed"),
            row.get("anchor_id"),
            row.get("target_category"),
            row.get("replicate"),
        )
        for row in executions
    }
    if len(coordinates) != len(executions):
        errors.append("plan execution coordinates are not unique")
    for row in executions:
        forbidden = _find_forbidden_key(
            {
                "dossier": row.get("agent_visible_dossier"),
                "task_id": row.get("task_id"),
                "target_field": row.get("target_field"),
            }
        )
        if forbidden is not None:
            errors.append(f"agent-visible classifier payload leaks {forbidden}")
            break
    return errors


def validate_phase_progress(
    plan: Mapping[str, Any], receipts: Sequence[Mapping[str, Any]]
) -> list[str]:
    """Validate a prefix of receipts without authorizing result-directed resume."""

    errors = validate_plan(plan)
    if len(receipts) > len(plan.get("executions", [])):
        errors.append("receipt prefix exceeds the plan denominator")
        return errors
    expected = [row["execution_id"] for row in plan.get("executions", [])[: len(receipts)]]
    observed = [row.get("execution_id") for row in receipts]
    if observed != expected:
        errors.append("receipts are not the exact immutable plan prefix")
    for row in receipts:
        if row.get("status") not in {"completed", "failed"}:
            errors.append("receipt status is neither completed nor failed")
        if row.get("status") == "failed" and not isinstance(row.get("failure"), Mapping):
            errors.append("failed receipt lacks structured failure")
    return errors


def validate_receipt_denominator(
    plan: Mapping[str, Any], receipts: Sequence[Mapping[str, Any]]
) -> list[str]:
    errors = validate_plan(plan)
    if len(receipts) != len(plan.get("executions", [])):
        errors.append("receipt count differs from exact plan denominator")
    planned = {row["execution_id"] for row in plan.get("executions", [])}
    observed = [row.get("execution_id") for row in receipts]
    if len(set(observed)) != len(observed) or set(observed) != planned:
        errors.append("receipts do not cover each planned execution exactly once")
    failed = [row for row in receipts if row.get("status") != "completed"]
    if any(not isinstance(row.get("failure"), Mapping) for row in failed):
        errors.append("failed receipts must retain a structured failure")
    return errors


__all__ = [
    "CONTRACT_VERSION",
    "PLAN_VERSION",
    "REPORT_VERSION",
    "SELECTION_VERSION",
    "AEPriorQualificationV03Error",
    "blind_classify_transposition",
    "build_candidate_schedule",
    "build_confirmation_plan",
    "build_phase_report",
    "build_screen_plan",
    "execute_one",
    "moved_pair",
    "score_blind_world",
    "select_screen_candidates",
    "validate_contract",
    "validate_phase_progress",
    "validate_plan",
    "validate_receipt_denominator",
]
