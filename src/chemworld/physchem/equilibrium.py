"""Phase-equilibrium utilities for ChemWorld.

The functions here provide a compact thermodynamic layer for benchmark tasks:
activity coefficients, Raoult-law K-values, isothermal flash, bubble/dew point
estimates, and a material-conserving liquid-liquid extraction stage.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from math import exp, isfinite, log
from typing import Literal

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence

ActivityModel = Literal["ideal", "margules", "wilson", "nrtl"]


@dataclass(frozen=True)
class ActivityModelSpec:
    model_id: str
    component_ids: tuple[str, ...]
    model: ActivityModel = "ideal"
    parameters: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.model_id:
            raise ValueError("model_id cannot be empty")
        if self.model not in {"ideal", "margules", "wilson", "nrtl"}:
            raise ValueError(f"Unsupported activity model: {self.model}")
        if not self.component_ids:
            raise ValueError("component_ids cannot be empty")
        if len(self.component_ids) != len(set(self.component_ids)):
            raise ValueError("Duplicate component ids are not allowed")
        if any(not isfinite(value) for value in self.parameters.values()):
            raise ValueError("activity-model parameters must be finite")
        _validate_activity_parameter_contract(self)

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
    if spec.model == "wilson":
        return _wilson_gamma(spec, x, temperature_K=temperature_K)
    if spec.model == "nrtl":
        return _nrtl_gamma(spec, x, temperature_K=temperature_K)
    raise ValueError(f"Unsupported activity model: {spec.model}")


def activity_model_cards() -> tuple[ModelCard, ...]:
    """Return model cards for the implemented activity-coefficient models."""

    return (
        ModelCard(
            model_id="wilson_activity_coefficients",
            module_id="phase_equilibrium",
            title="Wilson Activity Coefficients",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "JSON-friendly Wilson gamma model for VLE-oriented benchmark "
                "tasks with explicit asymmetric interaction parameters."
            ),
            equations=(
                "ln(gamma_i) = 1 - ln(sum_j x_j Lambda_ij) - "
                "sum_j x_j Lambda_ji / sum_k x_k Lambda_jk",
                "Lambda_ij = exp(a_ij + b_ij/T + c_ij ln(T) + "
                "d_ij T + e_ij/T**2 + f_ij T**2)",
            ),
            assumptions=(
                "Liquid mole fractions are normalized before evaluation.",
                "All off-diagonal Wilson interactions are directional and must "
                "be declared explicitly.",
                "Wilson is intended for liquid-phase VLE activity coefficients, "
                "not LLE prediction.",
            ),
            validity_limits=(
                "Requires positive finite Lambda values for all off-diagonal "
                "pairs.",
                "Temperature-dependent coefficients are accepted but only "
                "validated on fixed-lambda benchmark cases.",
            ),
            failure_modes=(
                "Missing directional interaction parameters fail during spec "
                "construction.",
                "Nonpositive Lambda values fail before gamma evaluation.",
                "Near-singular composition sums raise validation errors rather "
                "than being clipped.",
            ),
            units={
                "temperature": "K",
                "composition": "mole fraction",
                "gamma": "dimensionless",
                "lambda_a/lambda_c": "dimensionless",
                "lambda_b": "K",
                "lambda_d": "1/K",
                "lambda_e": "K^2",
                "lambda_f": "1/K^2",
            },
            reference_reading=(
                "reference_repos/thermo/thermo/wilson.py: Wilson_gammas and "
                "Wilson class",
                "reference_repos/phasepy/phasepy/actmodels/wilson.py: compact "
                "ln gamma API",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="thermo-wilson-binary-gammas",
                    evidence_type="optional_reference_test",
                    description=(
                        "Compares fixed-lambda Wilson activity coefficients "
                        "against thermo.wilson.Wilson_gammas."
                    ),
                    status="implemented",
                    reference_backend="thermo",
                    command_or_path=(
                        "tests/reference/test_optional_reference_backends.py"
                    ),
                    tolerance="rtol=1e-12",
                ),
            ),
            model_limit_notes=(
                "This card validates the gamma equations and parameter contract; "
                "it is not a complete Wilson parameter database.",
            ),
            intended_use=(
                "Reference-validated nonideal VLE benchmark slices.",
                "Solvent and volatility tasks where liquid nonideality matters.",
            ),
        ),
        ModelCard(
            model_id="nrtl_activity_coefficients",
            module_id="phase_equilibrium",
            title="NRTL Activity Coefficients",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "General asymmetric NRTL gamma model for binary and "
                "multicomponent benchmark mixtures."
            ),
            equations=(
                "tau_ij = A_ij + B_ij/T + E_ij ln(T) + F_ij T + "
                "G_ij/T**2 + H_ij T**2",
                "alpha_ij = c_ij + d_ij T",
                "G_ij = exp(-alpha_ij tau_ij)",
                "ln(gamma_i) follows the standard local-composition NRTL sum "
                "over directional pair interactions.",
            ),
            assumptions=(
                "Liquid mole fractions are normalized before evaluation.",
                "Every off-diagonal tau and alpha interaction is directional "
                "and explicit.",
                "The current validation covers binary fixed-parameter cases; "
                "the implementation supports any number of components.",
            ),
            validity_limits=(
                "Requires positive alpha values for off-diagonal pairs.",
                "Temperature-dependent tau/alpha coefficients are accepted but "
                "need system-specific validation.",
            ),
            failure_modes=(
                "Missing tau or alpha parameters fail during spec construction.",
                "Nonpositive alpha values fail before gamma evaluation.",
                "Singular NRTL denominator states raise validation errors rather "
                "than being clipped.",
            ),
            units={
                "temperature": "K",
                "composition": "mole fraction",
                "gamma": "dimensionless",
                "tau_a/tau_e/alpha_c": "dimensionless",
                "tau_b": "K",
                "tau_f": "1/K",
                "tau_g": "K^2",
                "tau_h": "1/K^2",
                "alpha_d": "1/K",
            },
            reference_reading=(
                "reference_repos/thermo/thermo/nrtl.py: NRTL_gammas_binaries "
                "and NRTL class",
                "reference_repos/phasepy/phasepy/actmodels/nrtl.py: compact "
                "matrix tau/G API",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="thermo-nrtl-binary-gammas",
                    evidence_type="optional_reference_test",
                    description=(
                        "Compares fixed binary NRTL activity coefficients "
                        "against thermo.nrtl.NRTL_gammas_binaries."
                    ),
                    status="implemented",
                    reference_backend="thermo",
                    command_or_path=(
                        "tests/reference/test_optional_reference_backends.py"
                    ),
                    tolerance="rtol=1e-12",
                ),
            ),
            model_limit_notes=(
                "This card validates the NRTL equation path and parameter "
                "contract; it does not provide a public interaction-parameter "
                "database.",
            ),
            intended_use=(
                "Reference-validated nonideal VLE/LLE benchmark slices.",
                "Future solvent-selection and liquid-phase separation tasks.",
            ),
        ),
    )


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


def _wilson_gamma(
    spec: ActivityModelSpec,
    x: tuple[float, ...],
    *,
    temperature_K: float,
) -> dict[str, float]:
    lambdas = _wilson_lambda_matrix(spec, temperature_K)
    n = len(spec.component_ids)
    sums = []
    for i in range(n):
        total = sum(x[j] * lambdas[i][j] for j in range(n))
        if total <= 0.0 or not isfinite(total):
            raise ValueError("Wilson lambda composition sum must be positive")
        sums.append(total)

    gamma = {}
    for i, component_id in enumerate(spec.component_ids):
        log_gamma = 1.0 - log(sums[i])
        log_gamma -= sum(x[j] * lambdas[j][i] / sums[j] for j in range(n))
        gamma[component_id] = exp(log_gamma)
    return gamma


def _nrtl_gamma(
    spec: ActivityModelSpec,
    x: tuple[float, ...],
    *,
    temperature_K: float,
) -> dict[str, float]:
    n = len(spec.component_ids)
    tau = [[0.0 for _ in range(n)] for _ in range(n)]
    g = [[1.0 for _ in range(n)] for _ in range(n)]
    for i, left in enumerate(spec.component_ids):
        for j, right in enumerate(spec.component_ids):
            if i == j:
                continue
            tau[i][j] = _nrtl_tau(spec, left, right, temperature_K)
            alpha = _nrtl_alpha(spec, left, right, temperature_K)
            if alpha <= 0.0:
                raise ValueError("NRTL alpha values must be positive")
            g[i][j] = exp(-alpha * tau[i][j])

    gamma = {}
    for i, component_id in enumerate(spec.component_ids):
        denominator_i = sum(x[k] * g[k][i] for k in range(n))
        if denominator_i <= 0.0 or not isfinite(denominator_i):
            raise ValueError("NRTL denominator must be positive")
        first = sum(x[j] * tau[j][i] * g[j][i] for j in range(n)) / denominator_i
        second = 0.0
        for j in range(n):
            denominator = sum(x[k] * g[k][j] for k in range(n))
            weighted_tau = sum(x[m] * tau[m][j] * g[m][j] for m in range(n))
            if denominator <= 0.0 or not isfinite(denominator):
                raise ValueError("NRTL denominator must be positive")
            second += (
                x[j]
                * g[i][j]
                / denominator
                * (tau[i][j] - weighted_tau / denominator)
            )
        gamma[component_id] = exp(first + second)
    return gamma


def _wilson_lambda_matrix(
    spec: ActivityModelSpec,
    temperature_K: float,
) -> list[list[float]]:
    component_ids = spec.component_ids
    n = len(component_ids)
    matrix = [[1.0 for _ in range(n)] for _ in range(n)]
    for i, left in enumerate(component_ids):
        for j, right in enumerate(component_ids):
            if i == j:
                continue
            value = _wilson_lambda(spec, left, right, temperature_K)
            if value <= 0.0 or not isfinite(value):
                raise ValueError("Wilson Lambda values must be finite and positive")
            matrix[i][j] = value
    return matrix


def _wilson_lambda(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    temperature_K: float,
) -> float:
    direct = _directional_parameter(spec, "lambda", left, right, default=None)
    if direct is not None:
        return direct
    exponent = (
        _directional_value(spec, "lambda_a", left, right, default=0.0)
        + _directional_value(spec, "lambda_b", left, right, default=0.0)
        / temperature_K
        + _directional_value(spec, "lambda_c", left, right, default=0.0)
        * log(temperature_K)
        + _directional_value(spec, "lambda_d", left, right, default=0.0)
        * temperature_K
        + _directional_value(spec, "lambda_e", left, right, default=0.0)
        / temperature_K**2
        + _directional_value(spec, "lambda_f", left, right, default=0.0)
        * temperature_K**2
    )
    return exp(exponent)


def _nrtl_tau(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    temperature_K: float,
) -> float:
    direct = _directional_parameter(spec, "tau", left, right, default=None)
    if direct is not None:
        return direct
    return (
        _directional_value(spec, "tau_a", left, right, default=0.0)
        + _directional_value(spec, "tau_b", left, right, default=0.0)
        / temperature_K
        + _directional_value(spec, "tau_e", left, right, default=0.0)
        * log(temperature_K)
        + _directional_value(spec, "tau_f", left, right, default=0.0)
        * temperature_K
        + _directional_value(spec, "tau_g", left, right, default=0.0)
        / temperature_K**2
        + _directional_value(spec, "tau_h", left, right, default=0.0)
        * temperature_K**2
    )


def _nrtl_alpha(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    temperature_K: float,
) -> float:
    direct = _directional_parameter(spec, "alpha", left, right, default=None)
    if direct is not None:
        return direct
    return (
        _directional_value(spec, "alpha_c", left, right, default=0.0)
        + _directional_value(spec, "alpha_d", left, right, default=0.0)
        * temperature_K
    )


def _validate_activity_parameter_contract(spec: ActivityModelSpec) -> None:
    if spec.model in {"ideal", "margules"}:
        return
    for left in spec.component_ids:
        for right in spec.component_ids:
            if left == right:
                continue
            if spec.model == "wilson":
                _validate_pair_has_any(
                    spec,
                    left,
                    right,
                    (
                        "lambda",
                        "lambda_a",
                        "lambda_b",
                        "lambda_c",
                        "lambda_d",
                        "lambda_e",
                        "lambda_f",
                    ),
                )
                direct = _directional_parameter(spec, "lambda", left, right, default=None)
                if direct is not None and direct <= 0.0:
                    raise ValueError("Wilson Lambda values must be positive")
            if spec.model == "nrtl":
                _validate_pair_has_any(
                    spec,
                    left,
                    right,
                    ("tau", "tau_a", "tau_b", "tau_e", "tau_f", "tau_g", "tau_h"),
                )
                _validate_pair_has_any(
                    spec,
                    left,
                    right,
                    ("alpha", "alpha_c", "alpha_d"),
                )
                direct_alpha = _directional_parameter(
                    spec,
                    "alpha",
                    left,
                    right,
                    default=None,
                )
                if direct_alpha is not None and direct_alpha <= 0.0:
                    raise ValueError("NRTL alpha values must be positive")


def _validate_pair_has_any(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    prefixes: tuple[str, ...],
) -> None:
    if not any(_has_directional_parameter(spec, prefix, left, right) for prefix in prefixes):
        allowed = ", ".join(prefixes)
        raise ValueError(
            f"{spec.model} requires one of {{{allowed}}} for pair {left}|{right}"
        )


def _has_directional_parameter(
    spec: ActivityModelSpec,
    prefix: str,
    left: str,
    right: str,
) -> bool:
    return f"{prefix}:{left}|{right}" in spec.parameters


def _directional_parameter(
    spec: ActivityModelSpec,
    prefix: str,
    left: str,
    right: str,
    *,
    default: float | None,
) -> float | None:
    key = f"{prefix}:{left}|{right}"
    if key not in spec.parameters:
        return default
    return float(spec.parameters[key])


def _directional_value(
    spec: ActivityModelSpec,
    prefix: str,
    left: str,
    right: str,
    *,
    default: float,
) -> float:
    value = _directional_parameter(spec, prefix, left, right, default=None)
    return default if value is None else value


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
    "activity_model_cards",
    "bubble_pressure_pa",
    "dew_pressure_pa",
    "flash_isothermal",
    "liquid_liquid_split",
    "rachford_rice_vapor_fraction",
    "raoult_k_values",
]
