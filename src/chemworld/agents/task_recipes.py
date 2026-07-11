"""Task-aware search recipes for official optimization baselines.

The public benchmark contains several different operation families.  A reaction
recipe is not a valid candidate for a partition, flow, electrochemical, or
equilibrium task, so official search baselines use the adapters in this module
instead of sending one universal reaction sequence to every environment.
"""

from __future__ import annotations

from typing import Any

import numpy as np

TASK_RECIPE_SPACE_VERSION = "chemworld-task-recipe-space-0.2"

_CONSERVATIVE_BASE_VECTORS = {
    "equilibrium": (0.5, 0.12, 0.12, 0.5),
    "flow": (0.0, 0.15, 0.0, 0.15, 0.70, 0.15, 0.10, 0.12),
    "electrochemical": (0.0, 0.15, 0.10, 0.10, 0.12),
    "partition": (0.0, 0.35, 0.50, 0.0, 0.35, 0.15, 0.65, 0.15),
    "reaction_crystallization": (
        0.10,
        0.15,
        0.15,
        0.30,
        0.0,
        0.10,
        0.0,
        0.50,
        0.50,
        0.30,
    ),
    "reaction_distillation": (
        0.10,
        0.15,
        0.15,
        0.30,
        0.0,
        0.10,
        0.0,
        0.20,
        0.20,
        0.50,
        0.60,
    ),
    "reaction": (0.10, 0.15, 0.15, 0.30, 0.0, 0.10, 0.0),
}


def task_recipe_kind(task_info: dict[str, Any]) -> str:
    operations = set(task_info.get("allowed_operations", ()))
    instruments = set(task_info.get("allowed_instruments", ()))
    if "ph_meter" in instruments:
        return "equilibrium"
    if "run_flow" in operations:
        return "flow"
    if "electrolyze" in operations:
        return "electrochemical"
    if "add_phase" in operations and "heat" not in operations:
        return "partition"
    if "cool_crystallize" in operations:
        return "reaction_crystallization"
    if "distill" in operations:
        return "reaction_distillation"
    return "reaction"


def task_recipe_dimension(task_info: dict[str, Any]) -> int:
    return {
        "equilibrium": 4,
        "flow": 8,
        "electrochemical": 5,
        "partition": 8,
        "reaction_crystallization": 10,
        "reaction_distillation": 11,
        "reaction": 7,
    }[task_recipe_kind(task_info)]


def sample_task_recipe(
    task_info: dict[str, Any],
    rng: np.random.Generator,
) -> dict[str, Any]:
    vector = rng.random(task_recipe_dimension(task_info))
    return task_recipe_from_unit_vector(task_info, vector)


def sample_conservative_task_recipe(
    task_info: dict[str, Any],
    rng: np.random.Generator,
    *,
    perturbation_scale: float = 0.06,
) -> dict[str, Any]:
    """Sample around a public low-intensity starting design for safe exploration."""

    if not 0.0 <= perturbation_scale <= 0.25:
        raise ValueError("perturbation_scale must be between zero and 0.25")
    base = np.asarray(_CONSERVATIVE_BASE_VECTORS[task_recipe_kind(task_info)], dtype=float)
    perturbation = rng.normal(0.0, perturbation_scale, size=base.shape)
    return task_recipe_from_unit_vector(task_info, np.clip(base + perturbation, 0.0, 1.0))


def task_recipe_from_unit_vector(
    task_info: dict[str, Any],
    vector: np.ndarray,
) -> dict[str, Any]:
    dimension = task_recipe_dimension(task_info)
    raw_values = np.asarray(vector, dtype=float).reshape(-1)
    if raw_values.size != dimension:
        raise ValueError(
            f"Expected {dimension} task-recipe coordinates, got {raw_values.size}"
        )
    values = np.asarray(np.clip(raw_values, 0.0, 1.0), dtype=float).reshape(-1)
    kind = task_recipe_kind(task_info)
    if kind == "equilibrium":
        steps = _equilibrium_steps(values)
    elif kind == "flow":
        steps = _flow_steps(values)
    elif kind == "electrochemical":
        steps = _electrochemical_steps(values)
    elif kind == "partition":
        steps = _partition_steps(values)
    else:
        steps = _reaction_steps(values, kind=kind)
    return {
        "steps": steps,
        "metadata": {
            "search_space_version": TASK_RECIPE_SPACE_VERSION,
            "search_space_kind": kind,
            "task_id": task_info.get("task_id"),
            "search_vector": [float(value) for value in values],
        },
    }


def task_recipe_to_vector(recipe: dict[str, Any]) -> np.ndarray:
    metadata = recipe.get("metadata")
    if not isinstance(metadata, dict) or "search_vector" not in metadata:
        raise ValueError("Task search recipe is missing metadata.search_vector")
    values = np.asarray(metadata["search_vector"], dtype=float).reshape(-1)
    if values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("Task search vector must contain finite coordinates")
    return values


def task_recipe_to_model_vector(
    task_info: dict[str, Any],
    recipe: dict[str, Any],
) -> np.ndarray:
    """Encode a recipe without imposing ordinal distance on material choices."""

    values = task_recipe_to_vector(recipe)
    categorical_coordinates = {
        "equilibrium": (),
        "flow": ((0, 4), (2, 4)),
        "electrochemical": ((0, 4),),
        "partition": ((0, 4), (3, 4)),
        "reaction_crystallization": ((4, 4), (6, 4)),
        "reaction_distillation": ((4, 4), (6, 4)),
        "reaction": ((4, 4), (6, 4)),
    }[task_recipe_kind(task_info)]
    categorical_indices = {coordinate for coordinate, _ in categorical_coordinates}
    continuous = np.asarray(
        [value for index, value in enumerate(values) if index not in categorical_indices],
        dtype=float,
    )
    encoded = [continuous]
    for coordinate, category_count in categorical_coordinates:
        one_hot = np.zeros(category_count, dtype=float)
        one_hot[_choice(float(values[coordinate]), category_count)] = 1.0
        encoded.append(one_hot)
    return np.concatenate(encoded)


def task_recipe_event_count(task_info: dict[str, Any]) -> int:
    vector = np.full(task_recipe_dimension(task_info), 0.5, dtype=float)
    return len(task_recipe_from_unit_vector(task_info, vector)["steps"])


def _scale(value: float, low: float, high: float) -> float:
    return low + float(value) * (high - low)


def _choice(value: float, count: int) -> int:
    return min(int(float(value) * count), count - 1)


def _reaction_charge_steps(values: np.ndarray) -> list[dict[str, Any]]:
    temperature_K = _scale(values[0], 333.15, 423.15)
    duration_s = _scale(values[1], 900.0, 7200.0)
    amount_mol = _scale(values[2], 0.003, 0.030)
    stirring_speed_rpm = _scale(values[3], 300.0, 1050.0)
    catalyst = _choice(values[4], 4)
    solvent = _choice(values[6], 4)
    return [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": solvent},
        {"operation": "add_reagent", "amount_mol": amount_mol},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": _scale(values[5], 0.00008, 0.00055),
            "catalyst": catalyst,
        },
        {
            "operation": "heat",
            "target_temperature_K": temperature_K,
            "duration_s": duration_s,
            "stirring_speed_rpm": stirring_speed_rpm,
        },
        {"operation": "quench"},
    ]


def _reaction_steps(values: np.ndarray, *, kind: str) -> list[dict[str, Any]]:
    steps = _reaction_charge_steps(values)
    if kind == "reaction_crystallization":
        steps.extend(
            [
                {
                    "operation": "seed_crystals",
                    "seed_mass_g": _scale(values[7], 0.001, 0.015),
                },
                {
                    "operation": "cool_crystallize",
                    "target_temperature_K": _scale(values[8], 273.15, 296.15),
                    "duration_s": _scale(values[9], 600.0, 4200.0),
                },
                {"operation": "filter_crystals"},
                {"operation": "measure", "instrument": "hplc"},
            ]
        )
    elif kind == "reaction_distillation":
        steps.extend(
            [
                {
                    "operation": "evaporate",
                    "target_temperature_K": _scale(values[7], 315.0, 350.0),
                    "duration_s": _scale(values[8], 300.0, 1500.0),
                },
                {
                    "operation": "distill",
                    "target_temperature_K": _scale(values[7], 345.0, 395.0),
                    "duration_s": _scale(values[8], 900.0, 3600.0),
                    "reflux_ratio": _scale(values[9], 0.5, 5.0),
                },
                {
                    "operation": "collect_fraction",
                    "transfer_fraction": _scale(values[10], 0.55, 0.99),
                },
                {"operation": "measure", "instrument": "gc"},
            ]
        )
    else:
        steps.append({"operation": "measure", "instrument": "hplc"})
    steps.extend(
        [
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
    )
    return steps


def _partition_steps(values: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "operation": "add_solvent",
            "volume_L": _scale(values[1], 0.012, 0.028),
            "solvent": _choice(values[0], 4),
        },
        {
            "operation": "add_phase",
            "phase": "aqueous",
            "volume_L": _scale(values[2], 0.006, 0.024),
        },
        {
            "operation": "add_extractant",
            "extractant": _choice(values[3], 4),
            "volume_L": _scale(values[4], 0.008, 0.030),
        },
        {
            "operation": "mix",
            "duration_s": _scale(values[5], 60.0, 600.0),
            "stirring_speed_rpm": _scale(values[7], 300.0, 1100.0),
        },
        {"operation": "settle", "duration_s": _scale(values[6], 120.0, 1200.0)},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _flow_steps(values: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "operation": "add_solvent",
            "volume_L": 0.025,
            "solvent": _choice(values[0], 4),
        },
        {"operation": "add_reagent", "amount_mol": _scale(values[1], 0.003, 0.030)},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": _scale(values[3], 0.00008, 0.00055),
            "catalyst": _choice(values[2], 4),
        },
        {
            "operation": "set_flow_rate",
            "flow_rate_mL_min": _scale(values[4], 0.2, 4.0),
            "residence_time_s": _scale(values[5], 180.0, 2400.0),
        },
        {
            "operation": "run_flow",
            "target_temperature_K": _scale(values[6], 330.0, 430.0),
            "duration_s": _scale(values[7], 600.0, 3600.0),
        },
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _electrochemical_steps(values: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "operation": "add_solvent",
            "volume_L": 0.025,
            "solvent": _choice(values[0], 4),
        },
        {"operation": "add_reagent", "amount_mol": _scale(values[1], 0.003, 0.030)},
        {
            "operation": "set_potential",
            "potential_V": _scale(values[2], 0.35, 2.25),
            "current_mA": _scale(values[3], 15.0, 220.0),
        },
        {"operation": "electrolyze", "duration_s": _scale(values[4], 300.0, 4200.0)},
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _equilibrium_steps(values: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "operation": "add_solvent",
            "volume_L": _scale(values[0], 0.018, 0.040),
            "solvent": 0,
        },
        {"operation": "add_reagent", "amount_mol": _scale(values[1], 0.001, 0.018)},
        {"operation": "measure", "instrument": "ph_meter"},
        {"operation": "add_reagent", "amount_mol": _scale(values[2], 0.001, 0.018)},
        {"operation": "measure", "instrument": "ph_meter"},
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


__all__ = [
    "TASK_RECIPE_SPACE_VERSION",
    "sample_conservative_task_recipe",
    "sample_task_recipe",
    "task_recipe_dimension",
    "task_recipe_event_count",
    "task_recipe_from_unit_vector",
    "task_recipe_kind",
    "task_recipe_to_model_vector",
    "task_recipe_to_vector",
]
