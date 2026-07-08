"""Phase-equilibrium utilities for ChemWorld.

The functions here provide a compact thermodynamic layer for benchmark tasks:
activity coefficients, Raoult-law K-values, isothermal flash, bubble/dew point
estimates, and a material-conserving liquid-liquid extraction stage.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from math import exp, isfinite
from typing import Literal

ActivityModel = Literal["ideal", "margules", "nrtl_lite"]


@dataclass(frozen=True)
class ActivityModelSpec:
    model_id: str
    component_ids: tuple[str, ...]
    model: ActivityModel = "ideal"
    parameters: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.model_id:
            raise ValueError("model_id cannot be empty")
        if self.model not in {"ideal", "margules", "nrtl_lite"}:
            raise ValueError(f"Unsupported activity model: {self.model}")
        if not self.component_ids:
            raise ValueError("component_ids cannot be empty")
        if len(self.component_ids) != len(set(self.component_ids)):
            raise ValueError("Duplicate component ids are not allowed")
        if any(not isfinite(value) for value in self.parameters.values()):
            raise ValueError("activity-model parameters must be finite")

    def to_dict(self) -> dict[str, object]:
        return {
            "model_id": self.model_id,
            "component_ids": list(self.component_ids),
            "model": self.model,
            "parameters": dict(self.parameters),
        }


@dataclass(frozen=True)
class FlashResult:
    vapor_fraction: float
    liquid_composition: dict[str, float]
    vapor_composition: dict[str, float]
    k_values: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "vapor_fraction": self.vapor_fraction,
            "liquid_composition": dict(self.liquid_composition),
            "vapor_composition": dict(self.vapor_composition),
            "k_values": dict(self.k_values),
        }


@dataclass(frozen=True)
class LLEStageResult:
    organic_amounts_mol: dict[str, float]
    aqueous_amounts_mol: dict[str, float]
    recovery_to_organic: dict[str, float]
    phase_volumes_L: dict[str, float]
    material_balance_error_mol: float

    def to_dict(self) -> dict[str, object]:
        return {
            "organic_amounts_mol": dict(self.organic_amounts_mol),
            "aqueous_amounts_mol": dict(self.aqueous_amounts_mol),
            "recovery_to_organic": dict(self.recovery_to_organic),
            "phase_volumes_L": dict(self.phase_volumes_L),
            "material_balance_error_mol": self.material_balance_error_mol,
        }


def activity_coefficients(
    spec: ActivityModelSpec,
    composition: Mapping[str, float],
    *,
    temperature_K: float,
) -> dict[str, float]:
    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    x = _composition_vector(spec.component_ids, composition)
    if spec.model == "ideal":
        return dict.fromkeys(spec.component_ids, 1.0)
    if spec.model == "margules":
        return _margules_gamma(spec, x)
    if spec.model == "nrtl_lite":
        return _nrtl_lite_gamma(spec, x)
    raise ValueError(f"Unsupported activity model: {spec.model}")


def raoult_k_values(
    activity_model: ActivityModelSpec,
    liquid_composition: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    pressure_Pa: float,
    temperature_K: float,
    vapor_fugacity_coefficients: Mapping[str, float] | None = None,
) -> dict[str, float]:
    if pressure_Pa <= 0:
        raise ValueError("pressure_Pa must be positive")
    gamma = activity_coefficients(
        activity_model,
        liquid_composition,
        temperature_K=temperature_K,
    )
    phi = (
        dict.fromkeys(activity_model.component_ids, 1.0)
        if vapor_fugacity_coefficients is None
        else dict(vapor_fugacity_coefficients)
    )
    k_values = {}
    for component_id in activity_model.component_ids:
        psat = float(vapor_pressures_Pa[component_id])
        if psat < 0:
            raise ValueError("vapor pressures cannot be negative")
        phi_i = max(float(phi.get(component_id, 1.0)), 1e-12)
        k_values[component_id] = gamma[component_id] * psat / (phi_i * pressure_Pa)
    return k_values


def rachford_rice_vapor_fraction(
    overall_composition: Mapping[str, float],
    k_values: Mapping[str, float],
    *,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> float:
    z = _normalize_composition(overall_composition)
    _validate_k_values(z, k_values)

    def objective(beta: float) -> float:
        return sum(
            z[component_id]
            * (k_values[component_id] - 1.0)
            / (1.0 + beta * (k_values[component_id] - 1.0))
            for component_id in z
        )

    f0 = objective(0.0)
    f1 = objective(1.0)
    if f0 <= 0.0:
        return 0.0
    if f1 >= 0.0:
        return 1.0

    low = 0.0
    high = 1.0
    for _ in range(max_iterations):
        mid = 0.5 * (low + high)
        value = objective(mid)
        if abs(value) < tolerance:
            return mid
        if value > 0.0:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def flash_isothermal(
    overall_composition: Mapping[str, float],
    k_values: Mapping[str, float],
) -> FlashResult:
    z = _normalize_composition(overall_composition)
    _validate_k_values(z, k_values)
    beta = rachford_rice_vapor_fraction(z, k_values)
    liquid = {
        component_id: z[component_id]
        / (1.0 + beta * (k_values[component_id] - 1.0))
        for component_id in z
    }
    liquid = _normalize_composition(liquid)
    vapor = {
        component_id: k_values[component_id] * liquid[component_id]
        for component_id in z
    }
    vapor = _normalize_composition(vapor)
    return FlashResult(
        vapor_fraction=beta,
        liquid_composition=liquid,
        vapor_composition=vapor,
        k_values={component_id: float(k_values[component_id]) for component_id in z},
    )


def bubble_pressure_pa(
    liquid_composition: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    activity_model: ActivityModelSpec,
    temperature_K: float,
) -> float:
    x = _normalize_composition(liquid_composition)
    gamma = activity_coefficients(activity_model, x, temperature_K=temperature_K)
    return sum(
        x[component_id] * gamma[component_id] * float(vapor_pressures_Pa[component_id])
        for component_id in x
    )


def dew_pressure_pa(
    vapor_composition: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    activity_model: ActivityModelSpec,
    temperature_K: float,
    iterations: int = 50,
) -> float:
    y = _normalize_composition(vapor_composition)
    pressure = 1.0 / sum(y[key] / max(float(vapor_pressures_Pa[key]), 1e-12) for key in y)
    liquid = dict(y)
    for _ in range(iterations):
        gamma = activity_coefficients(activity_model, liquid, temperature_K=temperature_K)
        pressure = 1.0 / sum(
            y[key] / max(gamma[key] * float(vapor_pressures_Pa[key]), 1e-12)
            for key in y
        )
        liquid = _normalize_composition(
            {
                key: y[key] * pressure / max(gamma[key] * float(vapor_pressures_Pa[key]), 1e-12)
                for key in y
            }
        )
    return pressure


def liquid_liquid_split(
    feed_amounts_mol: Mapping[str, float],
    *,
    partition_coefficients: Mapping[str, float],
    aqueous_volume_L: float,
    organic_volume_L: float,
    stage_efficiency: float = 1.0,
    entrainment_fraction: float = 0.0,
) -> LLEStageResult:
    if aqueous_volume_L <= 0 or organic_volume_L <= 0:
        raise ValueError("phase volumes must be positive")
    if not 0.0 <= stage_efficiency <= 1.0:
        raise ValueError("stage_efficiency must be between 0 and 1")
    if not 0.0 <= entrainment_fraction < 1.0:
        raise ValueError("entrainment_fraction must be in [0, 1)")
    if any(value < 0 for value in feed_amounts_mol.values()):
        raise ValueError("feed amounts cannot be negative")

    organic = {}
    aqueous = {}
    recovery = {}
    for component_id, amount in feed_amounts_mol.items():
        coefficient = float(partition_coefficients.get(component_id, 1.0))
        if coefficient < 0:
            raise ValueError("partition coefficients cannot be negative")
        ideal_organic = amount * coefficient * organic_volume_L
        ideal_organic /= coefficient * organic_volume_L + aqueous_volume_L
        organic_amount = stage_efficiency * ideal_organic
        aqueous_amount = amount - organic_amount
        entrained = entrainment_fraction * aqueous_amount
        organic_amount += entrained
        aqueous_amount -= entrained
        organic[component_id] = max(organic_amount, 0.0)
        aqueous[component_id] = max(aqueous_amount, 0.0)
        recovery[component_id] = 0.0 if amount <= 0 else organic[component_id] / amount
    balance_error = max(
        (
            abs(feed_amounts_mol[key] - organic.get(key, 0.0) - aqueous.get(key, 0.0))
            for key in feed_amounts_mol
        ),
        default=0.0,
    )
    return LLEStageResult(
        organic_amounts_mol=organic,
        aqueous_amounts_mol=aqueous,
        recovery_to_organic=recovery,
        phase_volumes_L={
            "aqueous": aqueous_volume_L * (1.0 - entrainment_fraction),
            "organic": organic_volume_L + aqueous_volume_L * entrainment_fraction,
        },
        material_balance_error_mol=balance_error,
    )


def _margules_gamma(spec: ActivityModelSpec, x: tuple[float, ...]) -> dict[str, float]:
    gamma = {}
    for i, component_id in enumerate(spec.component_ids):
        ln_gamma = 0.0
        for j, other_id in enumerate(spec.component_ids):
            if i == j:
                continue
            ln_gamma += _pair_parameter(spec, component_id, other_id, prefix="A") * x[j] ** 2
        gamma[component_id] = exp(ln_gamma)
    return gamma


def _nrtl_lite_gamma(spec: ActivityModelSpec, x: tuple[float, ...]) -> dict[str, float]:
    n = len(spec.component_ids)
    tau = [[0.0 for _ in range(n)] for _ in range(n)]
    g = [[1.0 for _ in range(n)] for _ in range(n)]
    for i, left in enumerate(spec.component_ids):
        for j, right in enumerate(spec.component_ids):
            if i == j:
                continue
            tau[i][j] = _pair_parameter(spec, left, right, prefix="tau")
            alpha = _pair_parameter(spec, left, right, prefix="alpha", default=0.3)
            g[i][j] = exp(-alpha * tau[i][j])

    gamma = {}
    for i, component_id in enumerate(spec.component_ids):
        first = 0.0
        for j in range(n):
            denominator = sum(x[k] * g[k][j] for k in range(n))
            if denominator > 0:
                first += x[j] * tau[j][i] * g[j][i] / denominator
        second = 0.0
        for j in range(n):
            denominator = sum(x[k] * g[k][j] for k in range(n))
            weighted_tau = sum(x[m] * tau[m][j] * g[m][j] for m in range(n))
            if denominator > 0:
                second += (
                    x[j]
                    * g[i][j]
                    / denominator
                    * (tau[i][j] - weighted_tau / denominator)
                )
        gamma[component_id] = exp(first + second)
    return gamma


def _pair_parameter(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    *,
    prefix: str,
    default: float = 0.0,
) -> float:
    return float(
        spec.parameters.get(
            f"{prefix}:{left}|{right}",
            spec.parameters.get(f"{prefix}:{right}|{left}", default),
        )
    )


def _composition_vector(
    component_ids: tuple[str, ...],
    composition: Mapping[str, float],
) -> tuple[float, ...]:
    normalized = _normalize_composition(composition)
    missing = sorted(set(component_ids) - set(normalized))
    extra = sorted(set(normalized) - set(component_ids))
    if missing or extra:
        raise ValueError(f"Composition ids do not match model: missing={missing}, extra={extra}")
    return tuple(normalized[component_id] for component_id in component_ids)


def _normalize_composition(composition: Mapping[str, float]) -> dict[str, float]:
    if not composition:
        raise ValueError("composition cannot be empty")
    if any(value < 0 or not isfinite(value) for value in composition.values()):
        raise ValueError("composition values must be finite and nonnegative")
    total = sum(composition.values())
    if total <= 0:
        raise ValueError("composition must contain positive material")
    return {component_id: float(value) / total for component_id, value in composition.items()}


def _validate_k_values(
    composition: Mapping[str, float],
    k_values: Mapping[str, float],
) -> None:
    missing = sorted(set(composition) - set(k_values))
    extra = sorted(set(k_values) - set(composition))
    if missing or extra:
        raise ValueError(f"K-value ids do not match composition: missing={missing}, extra={extra}")
    if any(value <= 0 or not isfinite(value) for value in k_values.values()):
        raise ValueError("K-values must be finite and positive")


__all__ = [
    "ActivityModel",
    "ActivityModelSpec",
    "FlashResult",
    "LLEStageResult",
    "activity_coefficients",
    "bubble_pressure_pa",
    "dew_pressure_pa",
    "flash_isothermal",
    "liquid_liquid_split",
    "rachford_rice_vapor_fraction",
    "raoult_k_values",
]
