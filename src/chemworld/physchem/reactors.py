"""Mechanism-backed reactor models for ChemWorld.

The models in this module are deliberately compact, but they are real numerical
reactor kernels: they integrate arbitrary balanced ``ReactionNetworkSpec``
objects and return material/energy ledgers that can be audited by world-law
checks and benchmark metrics.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from math import exp, isfinite
from typing import Any, Literal

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence
from chemworld.physchem.reaction_network import (
    RateLawSpec,
    ReactionNetworkSpec,
    ReactionSpec,
    SpeciesSpec,
)
from chemworld.physchem.thermochemistry import (
    NASA7SpeciesThermo,
    reaction_thermochemistry,
)

SteadyStateStability = Literal["stable", "unstable", "marginal"]
JacketInterpolationMode = Literal["step", "linear"]


@dataclass(frozen=True)
class HeatTransferSpec:
    rho_cp_J_per_L_K: float = 4180.0
    ua_W_per_K: float = 0.0
    environment_temperature_K: float = 298.15
    jacket_ua_W_per_K: float = 0.0
    jacket_temperature_K: float | None = None
    fixed_heat_W: float = 0.0

    def __post_init__(self) -> None:
        if self.rho_cp_J_per_L_K <= 0:
            raise ValueError("rho_cp_J_per_L_K must be positive")
        if self.ua_W_per_K < 0 or self.jacket_ua_W_per_K < 0:
            raise ValueError("Heat-transfer coefficients cannot be negative")
        if self.environment_temperature_K <= 0:
            raise ValueError("environment_temperature_K must be positive")
        if self.jacket_temperature_K is not None and self.jacket_temperature_K <= 0:
            raise ValueError("jacket_temperature_K must be positive")

    def jacket_heat_w(self, temperature_K: float) -> float:
        jacket = 0.0
        if self.jacket_temperature_K is not None:
            jacket = self.jacket_ua_W_per_K * (self.jacket_temperature_K - temperature_K)
        return self.fixed_heat_W + jacket

    def heat_loss_w(self, temperature_K: float) -> float:
        return self.ua_W_per_K * (temperature_K - self.environment_temperature_K)


@dataclass(frozen=True)
class JacketTemperatureProgram:
    """Time-dependent jacket setpoint for dynamic batch energy balances."""

    setpoints: tuple[tuple[float, float], ...]
    mode: JacketInterpolationMode = "step"

    def __post_init__(self) -> None:
        if not self.setpoints:
            raise ValueError("jacket setpoints cannot be empty")
        previous_time = -1.0
        for time_s, temperature_K in self.setpoints:
            if time_s < 0:
                raise ValueError("jacket setpoint times cannot be negative")
            if time_s < previous_time:
                raise ValueError("jacket setpoints must be sorted by time")
            if temperature_K <= 0:
                raise ValueError("jacket setpoint temperatures must be positive")
            previous_time = time_s
        if self.mode not in {"step", "linear"}:
            raise ValueError("jacket program mode must be 'step' or 'linear'")

    def temperature_at(self, time_s: float) -> float:
        if time_s <= self.setpoints[0][0]:
            return float(self.setpoints[0][1])
        for (left_time, left_temperature), (
            right_time,
            right_temperature,
        ) in zip(self.setpoints, self.setpoints[1:], strict=False):
            if left_time <= time_s <= right_time:
                if self.mode == "step" or right_time == left_time:
                    return float(left_temperature)
                fraction = (time_s - left_time) / (right_time - left_time)
                return float(
                    left_temperature
                    + fraction * (right_temperature - left_temperature)
                )
        return float(self.setpoints[-1][1])

    def to_dict(self) -> dict[str, object]:
        return {
            "setpoints": [
                {"time_s": time_s, "temperature_K": temperature_K}
                for time_s, temperature_K in self.setpoints
            ],
            "mode": self.mode,
        }


@dataclass(frozen=True)
class FeedStreamSpec:
    species_flows_mol_s: dict[str, float]
    volumetric_flow_L_s: float
    temperature_K: float = 298.15

    def __post_init__(self) -> None:
        if self.volumetric_flow_L_s < 0:
            raise ValueError("volumetric_flow_L_s cannot be negative")
        if self.temperature_K <= 0:
            raise ValueError("temperature_K must be positive")
        if any(value < 0 for value in self.species_flows_mol_s.values()):
            raise ValueError("species flows cannot be negative")

    def flow_for(self, species_id: str) -> float:
        return float(self.species_flows_mol_s.get(species_id, 0.0))


@dataclass(frozen=True)
class SemiBatchFeedSpec:
    stream: FeedStreamSpec
    start_s: float = 0.0
    end_s: float = 0.0

    def __post_init__(self) -> None:
        if self.start_s < 0 or self.end_s < 0:
            raise ValueError("feed times cannot be negative")
        if self.end_s < self.start_s:
            raise ValueError("end_s cannot be earlier than start_s")

    def is_active(self, time_s: float) -> bool:
        return self.start_s <= time_s <= self.end_s

    def species_flow(self, species_id: str, time_s: float) -> float:
        if not self.is_active(time_s):
            return 0.0
        return self.stream.flow_for(species_id)

    def volumetric_flow(self, time_s: float) -> float:
        if not self.is_active(time_s):
            return 0.0
        return self.stream.volumetric_flow_L_s


@dataclass(frozen=True)
class SamplingEventSpec:
    """A well-mixed destructive sample removed from a dynamic batch reactor."""

    time_s: float
    volume_L: float
    label: str = "sample"

    def __post_init__(self) -> None:
        if self.time_s < 0:
            raise ValueError("sampling time_s cannot be negative")
        if self.volume_L <= 0:
            raise ValueError("sampling volume_L must be positive")
        if not self.label.strip():
            raise ValueError("sampling label cannot be empty")

    def to_dict(self) -> dict[str, object]:
        return {
            "time_s": self.time_s,
            "volume_L": self.volume_L,
            "label": self.label,
        }


@dataclass(frozen=True)
class ReactorState:
    amounts_mol: dict[str, float]
    volume_L: float
    temperature_K: float
    time_s: float
    energy_jacket_J: float = 0.0
    heat_reaction_J: float = 0.0
    heat_loss_J: float = 0.0
    material_in_mol: dict[str, float] = field(default_factory=dict)
    material_out_mol: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.volume_L <= 0:
            raise ValueError("volume_L must be positive")
        if self.temperature_K <= 0:
            raise ValueError("temperature_K must be positive")
        if self.time_s < 0:
            raise ValueError("time_s cannot be negative")
        for label, values in {
            "amounts_mol": self.amounts_mol,
            "material_in_mol": self.material_in_mol,
            "material_out_mol": self.material_out_mol,
        }.items():
            if any(value < -1e-12 for value in values.values()):
                raise ValueError(f"{label} cannot contain negative amounts")

    def to_dict(self) -> dict[str, object]:
        return {
            "amounts_mol": dict(self.amounts_mol),
            "volume_L": self.volume_L,
            "temperature_K": self.temperature_K,
            "time_s": self.time_s,
            "energy_jacket_J": self.energy_jacket_J,
            "heat_reaction_J": self.heat_reaction_J,
            "heat_loss_J": self.heat_loss_J,
            "material_in_mol": dict(self.material_in_mol),
            "material_out_mol": dict(self.material_out_mol),
        }


@dataclass(frozen=True)
class ReactorResult:
    reactor_id: str
    model_id: str
    network_id: str
    initial_state: ReactorState
    final_state: ReactorState
    times_s: tuple[float, ...]
    amounts_mol: dict[str, tuple[float, ...]]
    temperatures_K: tuple[float, ...]
    material_balance_error_mol: float
    metadata: dict[str, object] = field(default_factory=dict)

    def conversion(self, reactant_id: str) -> float:
        initial = self.initial_state.amounts_mol.get(reactant_id, 0.0)
        final = self.final_state.amounts_mol.get(reactant_id, 0.0)
        if initial <= 0:
            return 0.0
        return max(0.0, min(1.0, (initial - final) / initial))

    def yield_on(self, product_id: str, reactant_id: str) -> float:
        initial_reactant = self.initial_state.amounts_mol.get(reactant_id, 0.0)
        final_product = self.final_state.amounts_mol.get(product_id, 0.0)
        initial_product = self.initial_state.amounts_mol.get(product_id, 0.0)
        if initial_reactant <= 0:
            return 0.0
        return max(0.0, (final_product - initial_product) / initial_reactant)

    def to_dict(self) -> dict[str, object]:
        return {
            "reactor_id": self.reactor_id,
            "model_id": self.model_id,
            "network_id": self.network_id,
            "initial_state": self.initial_state.to_dict(),
            "final_state": self.final_state.to_dict(),
            "times_s": list(self.times_s),
            "amounts_mol": {
                species_id: list(values) for species_id, values in self.amounts_mol.items()
            },
            "temperatures_K": list(self.temperatures_K),
            "material_balance_error_mol": self.material_balance_error_mol,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class CSTRMultiplicitySpec:
    """Scalar exothermic CSTR reference problem for steady-state multiplicity."""

    case_id: str
    feed_concentration_A_mol_L: float
    volumetric_flow_L_s: float
    volume_L: float
    feed_temperature_K: float
    coolant_temperature_K: float
    ua_W_per_K: float
    rho_cp_J_per_L_K: float
    delta_h_J_per_mol: float
    arrhenius_A_s_inv: float
    arrhenius_Ea_J_per_mol: float
    temperature_bounds_K: tuple[float, float]
    species_ids: tuple[str, str] = ("A", "P")

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id cannot be empty")
        _positive(self.feed_concentration_A_mol_L, "feed_concentration_A_mol_L")
        _positive(self.volumetric_flow_L_s, "volumetric_flow_L_s")
        _positive(self.volume_L, "volume_L")
        _positive(self.feed_temperature_K, "feed_temperature_K")
        _positive(self.coolant_temperature_K, "coolant_temperature_K")
        if self.ua_W_per_K < 0:
            raise ValueError("ua_W_per_K cannot be negative")
        _positive(self.rho_cp_J_per_L_K, "rho_cp_J_per_L_K")
        if self.delta_h_J_per_mol >= 0:
            raise ValueError("CSTR multiplicity case requires an exothermic delta_h_J_per_mol")
        _positive(self.arrhenius_A_s_inv, "arrhenius_A_s_inv")
        _positive(self.arrhenius_Ea_J_per_mol, "arrhenius_Ea_J_per_mol")
        if len(self.species_ids) != 2 or len(set(self.species_ids)) != 2:
            raise ValueError("species_ids must contain two distinct labels")
        low, high = self.temperature_bounds_K
        _positive(low, "temperature_bounds_K[0]")
        _positive(high, "temperature_bounds_K[1]")
        if high <= low:
            raise ValueError("temperature_bounds_K must be strictly increasing")

    @property
    def residence_time_s(self) -> float:
        return self.volume_L / self.volumetric_flow_L_s

    def rate_constant_s_inv(self, temperature_K: float) -> float:
        _positive(temperature_K, "temperature_K")
        return self.arrhenius_A_s_inv * exp(
            -self.arrhenius_Ea_J_per_mol / (8.31446261815324 * temperature_K)
        )

    def steady_concentration_a_mol_l(self, temperature_K: float) -> float:
        k = self.rate_constant_s_inv(temperature_K)
        return self.feed_concentration_A_mol_L / (1.0 + k * self.residence_time_s)

    def steady_conversion(self, temperature_K: float) -> float:
        return 1.0 - (
            self.steady_concentration_a_mol_l(temperature_K)
            / self.feed_concentration_A_mol_L
        )

    def reaction_rate_mol_l_s(self, temperature_K: float) -> float:
        return self.rate_constant_s_inv(temperature_K) * self.steady_concentration_a_mol_l(
            temperature_K
        )

    def heat_generation_w(self, temperature_K: float) -> float:
        return (
            -self.delta_h_J_per_mol
            * self.volume_L
            * self.reaction_rate_mol_l_s(temperature_K)
        )

    def heat_removal_w(self, temperature_K: float) -> float:
        return self.rho_cp_J_per_L_K * self.volumetric_flow_L_s * (
            temperature_K - self.feed_temperature_K
        ) + self.ua_W_per_K * (temperature_K - self.coolant_temperature_K)

    def energy_residual_w(self, temperature_K: float) -> float:
        return self.heat_generation_w(temperature_K) - self.heat_removal_w(temperature_K)

    def network(self) -> ReactionNetworkSpec:
        reactant_id, product_id = self.species_ids
        return ReactionNetworkSpec(
            network_id=f"{self.case_id}_network",
            species=(
                SpeciesSpec(reactant_id, "C2H4O2"),
                SpeciesSpec(product_id, "C2H4O2"),
            ),
            reactions=(
                ReactionSpec.from_equation(
                    reaction_id="exothermic_conversion",
                    equation=f"{reactant_id} => {product_id}",
                    rate_law=RateLawSpec(
                        "exothermic_conversion_rate",
                        "arrhenius",
                        {
                            "A": self.arrhenius_A_s_inv,
                            "Ea_J_per_mol": self.arrhenius_Ea_J_per_mol,
                        },
                    ),
                    delta_h_J_per_mol=self.delta_h_J_per_mol,
                ),
            ),
            metadata={"reference_case": self.case_id},
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "feed_concentration_A_mol_L": self.feed_concentration_A_mol_L,
            "volumetric_flow_L_s": self.volumetric_flow_L_s,
            "volume_L": self.volume_L,
            "feed_temperature_K": self.feed_temperature_K,
            "coolant_temperature_K": self.coolant_temperature_K,
            "ua_W_per_K": self.ua_W_per_K,
            "rho_cp_J_per_L_K": self.rho_cp_J_per_L_K,
            "delta_h_J_per_mol": self.delta_h_J_per_mol,
            "arrhenius_A_s_inv": self.arrhenius_A_s_inv,
            "arrhenius_Ea_J_per_mol": self.arrhenius_Ea_J_per_mol,
            "temperature_bounds_K": list(self.temperature_bounds_K),
            "residence_time_s": self.residence_time_s,
            "species_ids": list(self.species_ids),
        }


@dataclass(frozen=True)
class CSTRSteadyStatePoint:
    temperature_K: float
    concentration_A_mol_L: float
    concentration_P_mol_L: float
    conversion: float
    reaction_rate_mol_l_s: float
    heat_generation_w: float
    heat_removal_w: float
    residual_W: float
    eigenvalues: tuple[complex, ...]
    stability: SteadyStateStability

    def to_dict(self) -> dict[str, object]:
        return {
            "temperature_K": self.temperature_K,
            "concentration_A_mol_L": self.concentration_A_mol_L,
            "concentration_P_mol_L": self.concentration_P_mol_L,
            "conversion": self.conversion,
            "reaction_rate_mol_l_s": self.reaction_rate_mol_l_s,
            "heat_generation_w": self.heat_generation_w,
            "heat_removal_w": self.heat_removal_w,
            "residual_W": self.residual_W,
            "eigenvalues": [
                {"real": value.real, "imag": value.imag}
                for value in self.eigenvalues
            ],
            "stability": self.stability,
        }


@dataclass(frozen=True)
class CSTRMultiplicityResult:
    case_id: str
    spec: CSTRMultiplicitySpec
    steady_states: tuple[CSTRSteadyStatePoint, ...]
    scan_step_K: float
    residual_tolerance_W: float

    @property
    def temperatures_k(self) -> tuple[float, ...]:
        return tuple(point.temperature_K for point in self.steady_states)

    @property
    def stable_temperatures_k(self) -> tuple[float, ...]:
        return tuple(
            point.temperature_K
            for point in self.steady_states
            if point.stability == "stable"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "spec": self.spec.to_dict(),
            "steady_states": [point.to_dict() for point in self.steady_states],
            "temperatures_k": list(self.temperatures_k),
            "stable_temperatures_k": list(self.stable_temperatures_k),
            "scan_step_K": self.scan_step_K,
            "residual_tolerance_W": self.residual_tolerance_W,
        }


@dataclass(frozen=True)
class BatchReactorModel:
    network: ReactionNetworkSpec
    reactor_id: str = "batch"

    def simulate(
        self,
        initial_amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
        temperature_K: float,
        duration_s: float,
        heat_transfer: HeatTransferSpec | None = None,
        evaluation_times_s: Sequence[float] | None = None,
    ) -> ReactorResult:
        if duration_s < 0:
            raise ValueError("duration_s cannot be negative")
        thermal = HeatTransferSpec() if heat_transfer is None else heat_transfer
        y0 = np.array(
            [
                *(_amount_vector(self.network, initial_amounts_mol)),
                temperature_K,
                0.0,
                0.0,
                0.0,
            ],
            dtype=float,
        )

        def rhs(_time_s: float, y: np.ndarray) -> np.ndarray:
            amounts = _amounts_from_vector(self.network, y[: len(self.network.species_ids)])
            temperature = max(float(y[len(self.network.species_ids)]), 1.0)
            derivatives = self.network.amount_derivatives(
                amounts,
                volume_L=volume_L,
                temperature_K=temperature,
            )
            heat_reaction_W = _reaction_heat_w(
                self.network,
                amounts,
                volume_L=volume_L,
                temperature_K=temperature,
            )
            q_jacket_W = thermal.jacket_heat_w(temperature)
            q_loss_W = thermal.heat_loss_w(temperature)
            heat_capacity = thermal.rho_cp_J_per_L_K * volume_L
            dtemperature = (q_jacket_W - q_loss_W - heat_reaction_W) / heat_capacity
            return np.array(
                [
                    *(derivatives[species_id] for species_id in self.network.species_ids),
                    dtemperature,
                    q_jacket_W,
                    heat_reaction_W,
                    q_loss_W,
                ],
                dtype=float,
            )

        return _integrate_result(
            model_id="batch",
            reactor_id=self.reactor_id,
            network=self.network,
            initial_amounts_mol=initial_amounts_mol,
            initial_volume_L=volume_L,
            initial_temperature_K=temperature_K,
            y0=y0,
            duration_s=duration_s,
            rhs=rhs,
            volume_getter=lambda _time_s, _y: volume_L,
            evaluation_times_s=evaluation_times_s,
        )


@dataclass(frozen=True)
class DynamicBatchReactorModel:
    """Event-driven batch reactor with thermochemical heat release.

    The model is intentionally compact but follows the professional 0D reactor
    separation used by Cantera/IDAES: reaction rates update species amounts,
    reaction enthalpies define heat release, wall/jacket terms define heat
    exchange, and destructive sampling is an explicit material-out event.
    """

    network: ReactionNetworkSpec
    reactor_id: str = "dynamic_batch"

    def simulate(
        self,
        initial_amounts_mol: Mapping[str, float],
        *,
        initial_volume_L: float,
        temperature_K: float,
        duration_s: float,
        heat_transfer: HeatTransferSpec | None = None,
        species_thermo: Mapping[str, NASA7SpeciesThermo] | None = None,
        jacket_program: JacketTemperatureProgram | None = None,
        sampling_events: Sequence[SamplingEventSpec] = (),
        evaluation_times_s: Sequence[float] | None = None,
    ) -> ReactorResult:
        if duration_s < 0:
            raise ValueError("duration_s cannot be negative")
        if initial_volume_L <= 0:
            raise ValueError("initial_volume_L must be positive")
        thermal = HeatTransferSpec() if heat_transfer is None else heat_transfer
        events = tuple(sorted(sampling_events, key=lambda event: event.time_s))
        if any(event.time_s > duration_s for event in events):
            raise ValueError("sampling events cannot occur after duration_s")
        if evaluation_times_s is not None:
            for time_s in evaluation_times_s:
                if time_s < 0 or time_s > duration_s:
                    raise ValueError("evaluation_times_s must lie inside the simulation")

        n_species = len(self.network.species_ids)
        y_current = np.array(
            [
                *_amount_vector(self.network, initial_amounts_mol),
                temperature_K,
                0.0,
                0.0,
                0.0,
            ],
            dtype=float,
        )
        current_volume = float(initial_volume_L)
        current_time = 0.0
        material_out = dict.fromkeys(self.network.species_ids, 0.0)
        sample_records: list[dict[str, object]] = []
        times: list[float] = []
        states: list[np.ndarray] = []
        volumes: list[float] = []

        def append_solution(segment: Any) -> None:
            for idx, time_value in enumerate(segment.t):
                if times and abs(float(time_value) - times[-1]) < 1e-12:
                    times[-1] = float(time_value)
                    states[-1] = np.array(segment.y[:, idx], dtype=float)
                    volumes[-1] = current_volume
                else:
                    times.append(float(time_value))
                    states.append(np.array(segment.y[:, idx], dtype=float))
                    volumes.append(current_volume)

        def rhs(time_s: float, y: np.ndarray) -> np.ndarray:
            amounts = _amounts_from_vector(self.network, y[:n_species])
            temperature = max(float(y[n_species]), 1.0)
            derivatives = self.network.amount_derivatives(
                amounts,
                volume_L=current_volume,
                temperature_K=temperature,
                species_thermo=species_thermo,
            )
            heat_reaction_W = _reaction_heat_w(
                self.network,
                amounts,
                volume_L=current_volume,
                temperature_K=temperature,
                species_thermo=species_thermo,
            )
            jacket_setpoint = (
                jacket_program.temperature_at(time_s)
                if jacket_program is not None
                else thermal.jacket_temperature_K
            )
            q_jacket_W = _jacket_heat_w(
                thermal,
                temperature_K=temperature,
                jacket_temperature_K=jacket_setpoint,
            )
            q_loss_W = thermal.heat_loss_w(temperature)
            heat_capacity = thermal.rho_cp_J_per_L_K * current_volume
            dtemperature = (q_jacket_W - q_loss_W - heat_reaction_W) / heat_capacity
            return np.array(
                [
                    *(derivatives[species_id] for species_id in self.network.species_ids),
                    dtemperature,
                    q_jacket_W,
                    heat_reaction_W,
                    q_loss_W,
                ],
                dtype=float,
            )

        transition_times = sorted({event.time_s for event in events} | {duration_s})
        for next_time in transition_times:
            if next_time > current_time:
                segment = _solve_interval(
                    rhs,
                    y_current,
                    start_s=current_time,
                    end_s=next_time,
                    evaluation_times_s=_segment_evaluation_times(
                        current_time,
                        next_time,
                        evaluation_times_s,
                    ),
                )
                append_solution(segment)
                y_current = np.array(segment.y[:, -1], dtype=float)
                current_time = next_time
            elif not times:
                times.append(current_time)
                states.append(y_current.copy())
                volumes.append(current_volume)

            events_at_time = [
                event
                for event in events
                if abs(event.time_s - current_time) < 1e-12
            ]
            for event in events_at_time:
                if event.volume_L >= current_volume:
                    raise ValueError("sampling volume cannot remove all reactor volume")
                fraction = event.volume_L / current_volume
                sampled: dict[str, float] = {}
                for index, species_id in enumerate(self.network.species_ids):
                    removed = max(float(y_current[index]), 0.0) * fraction
                    y_current[index] = max(float(y_current[index]) - removed, 0.0)
                    material_out[species_id] += removed
                    sampled[species_id] = removed
                current_volume -= event.volume_L
                sample_records.append(
                    {
                        **event.to_dict(),
                        "fraction_removed": fraction,
                        "sampled_amounts_mol": sampled,
                        "remaining_volume_L": current_volume,
                    }
                )
                if times and abs(times[-1] - current_time) < 1e-12:
                    states[-1] = y_current.copy()
                    volumes[-1] = current_volume

        if not times:
            times.append(0.0)
            states.append(y_current.copy())
            volumes.append(current_volume)

        state_matrix = np.vstack(states).T
        amounts_timeseries = {
            species_id: tuple(
                max(float(value), 0.0) for value in state_matrix[index]
            )
            for index, species_id in enumerate(self.network.species_ids)
        }
        initial_state = ReactorState(
            amounts_mol={
                species_id: max(float(initial_amounts_mol.get(species_id, 0.0)), 0.0)
                for species_id in self.network.species_ids
            },
            volume_L=initial_volume_L,
            temperature_K=temperature_K,
            time_s=0.0,
        )
        final_state = ReactorState(
            amounts_mol={
                species_id: amounts_timeseries[species_id][-1]
                for species_id in self.network.species_ids
            },
            volume_L=current_volume,
            temperature_K=max(float(state_matrix[n_species, -1]), 1.0),
            time_s=duration_s,
            energy_jacket_J=float(state_matrix[n_species + 1, -1]),
            heat_reaction_J=float(state_matrix[n_species + 2, -1]),
            heat_loss_J=float(state_matrix[n_species + 3, -1]),
            material_out_mol=material_out,
        )
        return ReactorResult(
            reactor_id=self.reactor_id,
            model_id="dynamic_batch",
            network_id=self.network.network_id,
            initial_state=initial_state,
            final_state=final_state,
            times_s=tuple(times),
            amounts_mol=amounts_timeseries,
            temperatures_K=tuple(float(value) for value in state_matrix[n_species]),
            material_balance_error_mol=_material_balance_error(
                self.network,
                initial_state,
                final_state,
            ),
            metadata={
                "heat_source": (
                    "nasa7_reaction_enthalpy"
                    if species_thermo is not None
                    else "reaction_delta_h"
                ),
                "sample_events": sample_records,
                "volume_L_timeseries": tuple(volumes),
                "jacket_program": (
                    jacket_program.to_dict() if jacket_program is not None else None
                ),
                "reference_contract": "cantera_idaes_zero_d_energy_balance_slice",
            },
        )


@dataclass(frozen=True)
class SemiBatchReactorModel:
    network: ReactionNetworkSpec
    feeds: tuple[SemiBatchFeedSpec, ...]
    reactor_id: str = "semi_batch"

    def simulate(
        self,
        initial_amounts_mol: Mapping[str, float],
        *,
        initial_volume_L: float,
        temperature_K: float,
        duration_s: float,
        heat_transfer: HeatTransferSpec | None = None,
        evaluation_times_s: Sequence[float] | None = None,
    ) -> ReactorResult:
        if duration_s < 0:
            raise ValueError("duration_s cannot be negative")
        thermal = HeatTransferSpec() if heat_transfer is None else heat_transfer
        n_species = len(self.network.species_ids)
        y0 = np.array(
            [
                *_amount_vector(self.network, initial_amounts_mol),
                initial_volume_L,
                temperature_K,
                0.0,
                0.0,
                0.0,
                *(0.0 for _ in range(n_species)),
            ],
            dtype=float,
        )

        def rhs(time_s: float, y: np.ndarray) -> np.ndarray:
            amounts = _amounts_from_vector(self.network, y[:n_species])
            volume = max(float(y[n_species]), 1e-9)
            temperature = max(float(y[n_species + 1]), 1.0)
            reaction_derivatives = self.network.amount_derivatives(
                amounts,
                volume_L=volume,
                temperature_K=temperature,
            )
            feed = {
                species_id: sum(feed.species_flow(species_id, time_s) for feed in self.feeds)
                for species_id in self.network.species_ids
            }
            volume_flow = sum(feed.volumetric_flow(time_s) for feed in self.feeds)
            heat_reaction_W = _reaction_heat_w(
                self.network,
                amounts,
                volume_L=volume,
                temperature_K=temperature,
            )
            q_jacket_W = thermal.jacket_heat_w(temperature)
            q_loss_W = thermal.heat_loss_w(temperature)
            feed_heat_W = _feed_heat_w(self.feeds, time_s, temperature, thermal)
            heat_capacity = thermal.rho_cp_J_per_L_K * volume
            dtemperature = (
                q_jacket_W + feed_heat_W - q_loss_W - heat_reaction_W
            ) / heat_capacity
            return np.array(
                [
                    *(
                        reaction_derivatives[species_id] + feed[species_id]
                        for species_id in self.network.species_ids
                    ),
                    volume_flow,
                    dtemperature,
                    q_jacket_W,
                    heat_reaction_W,
                    q_loss_W,
                    *(feed[species_id] for species_id in self.network.species_ids),
                ],
                dtype=float,
            )

        return _integrate_result(
            model_id="semi_batch",
            reactor_id=self.reactor_id,
            network=self.network,
            initial_amounts_mol=initial_amounts_mol,
            initial_volume_L=initial_volume_L,
            initial_temperature_K=temperature_K,
            y0=y0,
            duration_s=duration_s,
            rhs=rhs,
            volume_getter=lambda _time_s, y: max(float(y[n_species]), 1e-9),
            evaluation_times_s=evaluation_times_s,
            material_in_slice=slice(n_species + 5, n_species + 5 + n_species),
        )


@dataclass(frozen=True)
class CSTRModel:
    network: ReactionNetworkSpec
    inlet: FeedStreamSpec
    volume_L: float
    outlet_volumetric_flow_L_s: float | None = None
    reactor_id: str = "cstr"

    def __post_init__(self) -> None:
        if self.volume_L <= 0:
            raise ValueError("volume_L must be positive")
        if self.outlet_volumetric_flow_L_s is not None and self.outlet_volumetric_flow_L_s < 0:
            raise ValueError("outlet_volumetric_flow_L_s cannot be negative")

    @property
    def outlet_flow_l_s(self) -> float:
        if self.outlet_volumetric_flow_L_s is None:
            return self.inlet.volumetric_flow_L_s
        return self.outlet_volumetric_flow_L_s

    def simulate_dynamic(
        self,
        initial_amounts_mol: Mapping[str, float],
        *,
        temperature_K: float,
        duration_s: float,
        heat_transfer: HeatTransferSpec | None = None,
        evaluation_times_s: Sequence[float] | None = None,
    ) -> ReactorResult:
        if duration_s < 0:
            raise ValueError("duration_s cannot be negative")
        thermal = HeatTransferSpec() if heat_transfer is None else heat_transfer
        n_species = len(self.network.species_ids)
        y0 = np.array(
            [
                *_amount_vector(self.network, initial_amounts_mol),
                temperature_K,
                0.0,
                0.0,
                0.0,
                *(0.0 for _ in range(n_species)),
                *(0.0 for _ in range(n_species)),
            ],
            dtype=float,
        )

        def rhs(_time_s: float, y: np.ndarray) -> np.ndarray:
            amounts = _amounts_from_vector(self.network, y[:n_species])
            temperature = max(float(y[n_species]), 1.0)
            reaction_derivatives = self.network.amount_derivatives(
                amounts,
                volume_L=self.volume_L,
                temperature_K=temperature,
            )
            outlet = {
                species_id: max(amounts[species_id], 0.0)
                / self.volume_L
                * self.outlet_flow_l_s
                for species_id in self.network.species_ids
            }
            inlet = {
                species_id: self.inlet.flow_for(species_id)
                for species_id in self.network.species_ids
            }
            heat_reaction_W = _reaction_heat_w(
                self.network,
                amounts,
                volume_L=self.volume_L,
                temperature_K=temperature,
            )
            q_jacket_W = thermal.jacket_heat_w(temperature)
            q_loss_W = thermal.heat_loss_w(temperature)
            inlet_heat_W = (
                thermal.rho_cp_J_per_L_K
                * self.inlet.volumetric_flow_L_s
                * (self.inlet.temperature_K - temperature)
            )
            heat_capacity = thermal.rho_cp_J_per_L_K * self.volume_L
            dtemperature = (
                q_jacket_W + inlet_heat_W - q_loss_W - heat_reaction_W
            ) / heat_capacity
            return np.array(
                [
                    *(
                        reaction_derivatives[species_id]
                        + inlet[species_id]
                        - outlet[species_id]
                        for species_id in self.network.species_ids
                    ),
                    dtemperature,
                    q_jacket_W,
                    heat_reaction_W,
                    q_loss_W,
                    *(inlet[species_id] for species_id in self.network.species_ids),
                    *(outlet[species_id] for species_id in self.network.species_ids),
                ],
                dtype=float,
            )

        return _integrate_result(
            model_id="cstr_dynamic",
            reactor_id=self.reactor_id,
            network=self.network,
            initial_amounts_mol=initial_amounts_mol,
            initial_volume_L=self.volume_L,
            initial_temperature_K=temperature_K,
            y0=y0,
            duration_s=duration_s,
            rhs=rhs,
            volume_getter=lambda _time_s, _y: self.volume_L,
            evaluation_times_s=evaluation_times_s,
            material_in_slice=slice(n_species + 4, n_species + 4 + n_species),
            material_out_slice=slice(n_species + 4 + n_species, n_species + 4 + 2 * n_species),
        )

    def simulate_to_steady_state(
        self,
        *,
        temperature_K: float,
        heat_transfer: HeatTransferSpec | None = None,
        residence_times: float = 12.0,
    ) -> ReactorResult:
        if self.inlet.volumetric_flow_L_s <= 0:
            raise ValueError("CSTR steady state requires positive inlet volumetric flow")
        duration_s = residence_times * self.volume_L / self.inlet.volumetric_flow_L_s
        initial = {
            species_id: self.inlet.flow_for(species_id)
            / self.inlet.volumetric_flow_L_s
            * self.volume_L
            for species_id in self.network.species_ids
        }
        return self.simulate_dynamic(
            initial,
            temperature_K=temperature_K,
            duration_s=duration_s,
            heat_transfer=heat_transfer,
            evaluation_times_s=(0.0, duration_s / 2.0, duration_s),
        )


@dataclass(frozen=True)
class PFRModel:
    network: ReactionNetworkSpec
    reactor_volume_L: float
    volumetric_flow_L_s: float
    reactor_id: str = "pfr"

    def __post_init__(self) -> None:
        if self.reactor_volume_L <= 0:
            raise ValueError("reactor_volume_L must be positive")
        if self.volumetric_flow_L_s <= 0:
            raise ValueError("volumetric_flow_L_s must be positive")

    @property
    def residence_time_s(self) -> float:
        return self.reactor_volume_L / self.volumetric_flow_L_s

    def simulate(
        self,
        inlet_concentrations_mol_L: Mapping[str, float],
        *,
        temperature_K: float,
        heat_transfer: HeatTransferSpec | None = None,
        evaluation_times_s: Sequence[float] | None = None,
    ) -> ReactorResult:
        thermal = HeatTransferSpec() if heat_transfer is None else heat_transfer
        initial_amounts = {
            species_id: max(float(inlet_concentrations_mol_L.get(species_id, 0.0)), 0.0)
            * self.reactor_volume_L
            for species_id in self.network.species_ids
        }
        y0 = np.array(
            [
                *(
                    max(float(inlet_concentrations_mol_L.get(species_id, 0.0)), 0.0)
                    for species_id in self.network.species_ids
                ),
                temperature_K,
                0.0,
                0.0,
                0.0,
            ],
            dtype=float,
        )

        def rhs(_tau_s: float, y: np.ndarray) -> np.ndarray:
            concentrations = {
                species_id: max(float(value), 0.0)
                for species_id, value in zip(self.network.species_ids, y, strict=False)
            }
            temperature = max(float(y[len(self.network.species_ids)]), 1.0)
            rates = self.network.reaction_rates(
                concentrations,
                volume_L=1.0,
                temperature_K=temperature,
            )
            dconcentrations = dict.fromkeys(self.network.species_ids, 0.0)
            for reaction in self.network.reactions:
                rate = rates[reaction.reaction_id]
                for species_id, coefficient in reaction.stoichiometry.items():
                    dconcentrations[species_id] += coefficient * rate
            heat_reaction_per_L_W = sum(
                reaction.delta_h_J_per_mol * rates[reaction.reaction_id]
                for reaction in self.network.reactions
            )
            q_jacket_per_L_W = thermal.jacket_heat_w(temperature) / self.reactor_volume_L
            q_loss_per_L_W = thermal.heat_loss_w(temperature) / self.reactor_volume_L
            dtemperature = (
                q_jacket_per_L_W - q_loss_per_L_W - heat_reaction_per_L_W
            ) / thermal.rho_cp_J_per_L_K
            return np.array(
                [
                    *(dconcentrations[species_id] for species_id in self.network.species_ids),
                    dtemperature,
                    thermal.jacket_heat_w(temperature),
                    heat_reaction_per_L_W * self.reactor_volume_L,
                    thermal.heat_loss_w(temperature),
                ],
                dtype=float,
            )

        result = _solve(
            rhs,
            y0,
            duration_s=self.residence_time_s,
            evaluation_times_s=evaluation_times_s,
        )
        n_species = len(self.network.species_ids)
        amounts = {
            species_id: tuple(
                max(float(value), 0.0) * self.reactor_volume_L
                for value in result.y[idx]
            )
            for idx, species_id in enumerate(self.network.species_ids)
        }
        final_amounts = {species_id: values[-1] for species_id, values in amounts.items()}
        final_state = ReactorState(
            amounts_mol=final_amounts,
            volume_L=self.reactor_volume_L,
            temperature_K=max(float(result.y[n_species, -1]), 1.0),
            time_s=self.residence_time_s,
            energy_jacket_J=float(result.y[n_species + 1, -1]),
            heat_reaction_J=float(result.y[n_species + 2, -1]),
            heat_loss_J=float(result.y[n_species + 3, -1]),
        )
        initial_state = ReactorState(
            amounts_mol=initial_amounts,
            volume_L=self.reactor_volume_L,
            temperature_K=temperature_K,
            time_s=0.0,
        )
        return ReactorResult(
            reactor_id=self.reactor_id,
            model_id="pfr",
            network_id=self.network.network_id,
            initial_state=initial_state,
            final_state=final_state,
            times_s=tuple(float(value) for value in result.t),
            amounts_mol=amounts,
            temperatures_K=tuple(float(value) for value in result.y[n_species]),
            material_balance_error_mol=_material_balance_error(
                self.network,
                initial_state,
                final_state,
            ),
            metadata={
                "residence_time_s": self.residence_time_s,
                "volumetric_flow_L_s": self.volumetric_flow_L_s,
            },
        )


def cstr_multiple_steady_state_reference_case() -> CSTRMultiplicitySpec:
    """Return a ChemWorld-owned exothermic CSTR multiplicity case."""

    return CSTRMultiplicitySpec(
        case_id="cstr_exothermic_multiplicity_reference",
        feed_concentration_A_mol_L=1.0,
        volumetric_flow_L_s=0.1,
        volume_L=500.0,
        feed_temperature_K=300.0,
        coolant_temperature_K=270.0,
        ua_W_per_K=1.0,
        rho_cp_J_per_L_K=4180.0,
        delta_h_J_per_mol=-300_000.0,
        arrhenius_A_s_inv=1.0e11,
        arrhenius_Ea_J_per_mol=95_000.0,
        temperature_bounds_K=(290.0, 430.0),
    )


def solve_cstr_multiple_steady_states(
    spec: CSTRMultiplicitySpec | None = None,
    *,
    temperature_step_K: float = 0.25,
    residual_tolerance_W: float = 1e-6,
    stability_tolerance_s_inv: float = 1e-9,
) -> CSTRMultiplicityResult:
    """Solve scalar CSTR energy-balance roots and classify local stability."""

    case = cstr_multiple_steady_state_reference_case() if spec is None else spec
    _positive(temperature_step_K, "temperature_step_K")
    if residual_tolerance_W < 0:
        raise ValueError("residual_tolerance_W cannot be negative")
    if stability_tolerance_s_inv < 0:
        raise ValueError("stability_tolerance_s_inv cannot be negative")

    low, high = case.temperature_bounds_K
    grid = [
        float(value)
        for value in np.arange(low, high + 0.5 * temperature_step_K, temperature_step_K)
    ]
    if grid[-1] < high:
        grid.append(high)
    residuals = [case.energy_residual_w(temperature) for temperature in grid]
    roots = _bracketed_scalar_roots(
        lambda temperature: case.energy_residual_w(temperature),
        tuple(grid),
        tuple(residuals),
    )
    points = tuple(
        _cstr_steady_state_point(
            case,
            temperature_K=root,
            residual_tolerance_W=residual_tolerance_W,
            stability_tolerance_s_inv=stability_tolerance_s_inv,
        )
        for root in roots
    )
    return CSTRMultiplicityResult(
        case_id=case.case_id,
        spec=case,
        steady_states=points,
        scan_step_K=temperature_step_K,
        residual_tolerance_W=residual_tolerance_W,
    )


def reactor_model_cards() -> tuple[ModelCard, ...]:
    return (
        ModelCard(
            model_id="dynamic_batch_heat_release_jacket_sampling",
            module_id="reactors",
            title="Dynamic Batch Reactor With Heat Release And Sampling",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Event-driven dynamic batch reactor slice with material "
                "balances, thermochemistry-derived reaction heat, wall/jacket "
                "heat transfer, destructive sampling events, and auditable "
                "material/energy ledgers."
            ),
            equations=(
                "dn/dt = S r(n, T)",
                "rhoCp V dT/dt = Q_jacket - Q_loss - sum_i DeltaH_i(T) r_i V",
                "Q_jacket = UA_jacket (T_jacket(t) - T) + Q_fixed",
                "Q_loss = UA_env (T - T_env)",
                "sample event: n_j <- n_j(1 - V_sample/V), V <- V - V_sample",
            ),
            assumptions=(
                "well-mixed liquid-phase batch reactor",
                "constant density heat-capacity basis rhoCp V",
                "sampling removes a representative well-mixed fraction",
                "reaction enthalpy uses supplied NASA7 species thermochemistry when available",
            ),
            validity_limits=(
                "no pressure dynamics, vapor-liquid equilibrium, or wall thermal inertia",
                "sample events must leave positive reactor volume",
                "NASA7 reaction enthalpy requires thermochemistry for every reacting species",
            ),
            failure_modes=(
                "negative duration, volume, sample volume, or temperature raises errors",
                "missing species thermochemistry raises a KeyError when NASA7 heat is requested",
                "ODE solver failure raises RuntimeError instead of silently clipping",
            ),
            units={
                "amount": "mol",
                "volume": "L",
                "temperature": "K",
                "heat_capacity_density": "J/(L*K)",
                "heat_duty": "W",
                "energy_ledger": "J",
            },
            reference_reading=(
                (
                    "Cantera: reference_repos/cantera/src/zeroD/Reactor.cpp "
                    "separates species production, wall heat Qdot, inlet/outlet "
                    "enthalpy, and energy-equation terms."
                ),
                (
                    "Cantera: reference_repos/cantera/src/zeroD/"
                    "IdealGasReactor.cpp uses mass*cv*dT/dt as the energy "
                    "equation left-hand side for temperature-state reactors."
                ),
                (
                    "IDAES: modular property packages expose enthalpy/internal "
                    "energy flow and density terms for control-volume energy "
                    "balances."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="dynamic-batch-adiabatic-rise-test",
                    evidence_type="unit_test",
                    description=(
                        "Exothermic reaction with NASA7 enthalpy produces the "
                        "expected adiabatic temperature rise from the integrated "
                        "reaction-heat ledger."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="pytest.approx local tolerances",
                ),
                ValidationEvidence(
                    evidence_id="dynamic-batch-sampling-ledger-test",
                    evidence_type="unit_test",
                    description=(
                        "Destructive sampling reduces volume, records material_out, "
                        "and preserves elemental material balance."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="material balance error < 1e-8 mol",
                ),
            ),
            model_limit_notes=(
                (
                    "This slice closes the dynamic batch heat-release and sampling "
                    "kernel, not a full Cantera/IDAES reactor clone."
                ),
                (
                    "Pressure dynamics, gas expansion work, variable Cp mixtures, "
                    "and vapor-liquid phase change remain explicit future slices."
                ),
            ),
            intended_use=(
                "reaction calorimetry task design",
                "heat-release-aware campaign simulation",
                "safe-operation benchmark scenarios with explicit material and energy ledgers",
            ),
        ),
        ModelCard(
            model_id="cstr_exothermic_multiplicity_reference",
            module_id="reactors",
            title="Exothermic CSTR Multiple-Steady-State Reference Slice",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "ChemWorld-owned steady-state CSTR reference problem for an "
                "exothermic first-order reaction. It solves the coupled "
                "steady-state material and energy balances as scalar energy "
                "roots and classifies local stability using the dynamic CSTR "
                "Jacobian."
            ),
            equations=(
                "0 = q(C_Af - C_A) - V k(T) C_A",
                "C_A(T) = C_Af / (1 + k(T) V/q)",
                "0 = (-DeltaH) V k(T) C_A(T) - rhoCp q(T - Tf) - UA(T - Tc)",
                "k(T) = A exp(-Ea/(RT))",
            ),
            assumptions=(
                "well-mixed liquid-phase CSTR",
                "constant volume and density heat capacity",
                "single irreversible A=>P first-order exothermic reaction",
                "heat removal represented by inlet sensible heat and UA coolant term",
            ),
            validity_limits=(
                "validated only for scalar first-order exothermic CSTR multiplicity",
                (
                    "no pressure dynamics, vapor phase, nonideal heat capacity, "
                    "or full plant hydraulics"
                ),
                "temperature roots must be bracketed inside the declared temperature bounds",
            ),
            failure_modes=(
                (
                    "invalid nonpositive flow, volume, heat capacity, or "
                    "Arrhenius parameters raise errors"
                ),
                "endothermic delta_h is rejected for this multiplicity case",
                "missing roots outside scan bounds are reported as absent rather than extrapolated",
            ),
            units={
                "concentration": "mol/L",
                "volumetric_flow": "L/s",
                "volume": "L",
                "temperature": "K",
                "heat_capacity_density": "J/(L*K)",
                "heat_duty": "W",
                "rate_constant": "1/s",
            },
            reference_reading=(
                (
                    "Cantera: reference_repos/cantera/doc/sphinx/userguide/"
                    "reactor-tutorial.md describes CSTR residence time and "
                    "advance_to_steady_state."
                ),
                (
                    "Cantera: reference_repos/cantera/samples/python/reactors/"
                    "continuous_reactor.py uses reservoirs, MassFlowController, "
                    "PressureController, and ReactorNet for a stirred reactor."
                ),
                (
                    "IDAES: reference_repos/idaes-pse/idaes/models/unit_models/"
                    "cstr.py builds a 0D control volume with material, energy, "
                    "and reaction extent balances."
                ),
                (
                    "IDAES: cstr_performance_eqn sets rate_reaction_extent = "
                    "volume * reaction_rate."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="cstr-multiplicity-root-test",
                    evidence_type="unit_test",
                    description=(
                        "The default case has three energy-balance roots with "
                        "stable/unstable/stable local dynamics."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="root residual <= 1e-6 W",
                ),
                ValidationEvidence(
                    evidence_id="cstr-performance-equation-test",
                    evidence_type="unit_test",
                    description=(
                        "At each root, the material-balance concentration and "
                        "reaction heat satisfy the CSTR performance equation."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="pytest.approx local tolerances",
                ),
            ),
            model_limit_notes=(
                (
                    "This is a professional reference slice for multiplicity, "
                    "not a full IDAES clone."
                ),
                (
                    "Future work should add Cantera dynamic cross-checks and "
                    "plant-scale heat-transfer variants."
                ),
            ),
            intended_use=(
                "CSTR ignition/extinction task design",
                "reactor-model maturity reporting",
                "reference case for agents reasoning about multiple steady states",
            ),
        ),
    )


def _integrate_result(
    *,
    model_id: str,
    reactor_id: str,
    network: ReactionNetworkSpec,
    initial_amounts_mol: Mapping[str, float],
    initial_volume_L: float,
    initial_temperature_K: float,
    y0: np.ndarray,
    duration_s: float,
    rhs: Callable[[float, np.ndarray], np.ndarray],
    volume_getter: Callable[[float, np.ndarray], float],
    evaluation_times_s: Sequence[float] | None,
    material_in_slice: slice | None = None,
    material_out_slice: slice | None = None,
) -> ReactorResult:
    result = _solve(
        rhs,
        y0,
        duration_s=duration_s,
        evaluation_times_s=evaluation_times_s,
    )
    n_species = len(network.species_ids)
    amounts = {
        species_id: tuple(max(float(value), 0.0) for value in result.y[idx])
        for idx, species_id in enumerate(network.species_ids)
    }
    final_amounts = {species_id: values[-1] for species_id, values in amounts.items()}
    final_y = result.y[:, -1]
    final_volume = float(volume_getter(float(result.t[-1]), final_y))
    material_in = _ledger_from_slice(network, final_y, material_in_slice)
    material_out = _ledger_from_slice(network, final_y, material_out_slice)
    initial_state = ReactorState(
        amounts_mol={
            species_id: max(float(initial_amounts_mol.get(species_id, 0.0)), 0.0)
            for species_id in network.species_ids
        },
        volume_L=initial_volume_L,
        temperature_K=initial_temperature_K,
        time_s=0.0,
    )
    final_state = ReactorState(
        amounts_mol=final_amounts,
        volume_L=max(final_volume, 1e-12),
        temperature_K=max(
            float(final_y[n_species if model_id != "semi_batch" else n_species + 1]),
            1.0,
        ),
        time_s=duration_s,
        energy_jacket_J=float(final_y[n_species + (2 if model_id == "semi_batch" else 1)]),
        heat_reaction_J=float(final_y[n_species + (3 if model_id == "semi_batch" else 2)]),
        heat_loss_J=float(final_y[n_species + (4 if model_id == "semi_batch" else 3)]),
        material_in_mol=material_in,
        material_out_mol=material_out,
    )
    return ReactorResult(
        reactor_id=reactor_id,
        model_id=model_id,
        network_id=network.network_id,
        initial_state=initial_state,
        final_state=final_state,
        times_s=tuple(float(value) for value in result.t),
        amounts_mol=amounts,
        temperatures_K=tuple(
            float(value)
            for value in result.y[n_species if model_id != "semi_batch" else n_species + 1]
        ),
        material_balance_error_mol=_material_balance_error(
            network,
            initial_state,
            final_state,
        ),
    )


def _solve(
    rhs: Callable[[float, np.ndarray], np.ndarray],
    y0: np.ndarray,
    *,
    duration_s: float,
    evaluation_times_s: Sequence[float] | None,
) -> Any:
    t_eval = None
    if evaluation_times_s is not None:
        t_eval = np.array(tuple(evaluation_times_s), dtype=float)
    result = solve_ivp(
        rhs,
        (0.0, duration_s),
        y0,
        t_eval=t_eval,
        method="LSODA",
        rtol=1e-8,
        atol=1e-12,
    )
    if not result.success:
        raise RuntimeError(f"Reactor integration failed: {result.message}")
    return result


def _solve_interval(
    rhs: Callable[[float, np.ndarray], np.ndarray],
    y0: np.ndarray,
    *,
    start_s: float,
    end_s: float,
    evaluation_times_s: Sequence[float],
) -> Any:
    t_eval = np.array(tuple(evaluation_times_s), dtype=float)
    result = solve_ivp(
        rhs,
        (start_s, end_s),
        y0,
        t_eval=t_eval,
        method="LSODA",
        rtol=1e-8,
        atol=1e-12,
    )
    if not result.success:
        raise RuntimeError(f"Reactor integration failed: {result.message}")
    return result


def _segment_evaluation_times(
    start_s: float,
    end_s: float,
    requested_times_s: Sequence[float] | None,
) -> tuple[float, ...]:
    if requested_times_s is None:
        return (start_s, end_s) if end_s > start_s else (start_s,)
    selected = [
        float(time_s)
        for time_s in requested_times_s
        if start_s - 1e-12 <= time_s <= end_s + 1e-12
    ]
    selected.extend([start_s, end_s])
    return tuple(sorted(set(selected)))


def _amount_vector(
    network: ReactionNetworkSpec,
    amounts_mol: Mapping[str, float],
) -> tuple[float, ...]:
    return tuple(
        max(float(amounts_mol.get(species_id, 0.0)), 0.0)
        for species_id in network.species_ids
    )


def _amounts_from_vector(
    network: ReactionNetworkSpec,
    values: Sequence[float] | np.ndarray,
) -> dict[str, float]:
    return {
        species_id: max(float(value), 0.0)
        for species_id, value in zip(network.species_ids, values, strict=True)
    }


def _reaction_heat_w(
    network: ReactionNetworkSpec,
    amounts_mol: Mapping[str, float],
    *,
    volume_L: float,
    temperature_K: float,
    species_thermo: Mapping[str, NASA7SpeciesThermo] | None = None,
) -> float:
    rates = network.reaction_rates(
        amounts_mol,
        volume_L=volume_L,
        temperature_K=temperature_K,
        species_thermo=species_thermo,
    )
    return sum(
        _reaction_enthalpy_j_mol(
            reaction,
            temperature_K=temperature_K,
            species_thermo=species_thermo,
        )
        * rates[reaction.reaction_id]
        * volume_L
        for reaction in network.reactions
    )


def _reaction_enthalpy_j_mol(
    reaction: ReactionSpec,
    *,
    temperature_K: float,
    species_thermo: Mapping[str, NASA7SpeciesThermo] | None,
) -> float:
    if species_thermo is None:
        return reaction.delta_h_J_per_mol
    return reaction_thermochemistry(
        reaction_id=reaction.reaction_id,
        stoichiometry=reaction.stoichiometry,
        species_thermo=species_thermo,
        temperature_K=temperature_K,
    ).delta_h_J_mol


def _jacket_heat_w(
    thermal: HeatTransferSpec,
    *,
    temperature_K: float,
    jacket_temperature_K: float | None,
) -> float:
    jacket = 0.0
    if jacket_temperature_K is not None:
        jacket = thermal.jacket_ua_W_per_K * (jacket_temperature_K - temperature_K)
    return thermal.fixed_heat_W + jacket


def _feed_heat_w(
    feeds: tuple[SemiBatchFeedSpec, ...],
    time_s: float,
    temperature_K: float,
    thermal: HeatTransferSpec,
) -> float:
    return sum(
        thermal.rho_cp_J_per_L_K
        * feed.volumetric_flow(time_s)
        * (feed.stream.temperature_K - temperature_K)
        for feed in feeds
    )


def _ledger_from_slice(
    network: ReactionNetworkSpec,
    y: np.ndarray,
    ledger_slice: slice | None,
) -> dict[str, float]:
    if ledger_slice is None:
        return {}
    values = y[ledger_slice]
    return {
        species_id: max(float(value), 0.0)
        for species_id, value in zip(network.species_ids, values, strict=True)
    }


def _element_totals(
    network: ReactionNetworkSpec,
    amounts_mol: Mapping[str, float],
) -> dict[str, float]:
    totals: dict[str, float] = {}
    for species in network.species:
        amount = max(float(amounts_mol.get(species.species_id, 0.0)), 0.0)
        for element, count in species.composition.items():
            totals[element] = totals.get(element, 0.0) + count * amount
    return totals


def _material_balance_error(
    network: ReactionNetworkSpec,
    initial: ReactorState,
    final: ReactorState,
) -> float:
    left = _element_totals(network, initial.amounts_mol)
    _add_element_totals(left, network, final.material_in_mol, sign=1.0)
    right = _element_totals(network, final.amounts_mol)
    _add_element_totals(right, network, final.material_out_mol, sign=1.0)
    elements = set(left) | set(right)
    return max(
        (
            abs(left.get(element, 0.0) - right.get(element, 0.0))
            for element in elements
        ),
        default=0.0,
    )


def _add_element_totals(
    totals: dict[str, float],
    network: ReactionNetworkSpec,
    amounts_mol: Mapping[str, float],
    *,
    sign: float,
) -> None:
    increment = _element_totals(network, amounts_mol)
    for element, value in increment.items():
        totals[element] = totals.get(element, 0.0) + sign * value


def _positive(value: float, name: str) -> None:
    if value <= 0 or not isfinite(value):
        raise ValueError(f"{name} must be finite and positive")


def _bracketed_scalar_roots(
    func: Callable[[float], float],
    grid: tuple[float, ...],
    residuals: tuple[float, ...],
    *,
    dedup_tolerance_K: float = 1e-6,
) -> tuple[float, ...]:
    roots: list[float] = []
    for left, right, residual_left, residual_right in zip(
        grid,
        grid[1:],
        residuals,
        residuals[1:],
        strict=False,
    ):
        if residual_left == 0.0:
            roots.append(left)
        if residual_left * residual_right < 0.0:
            roots.append(brentq(func, left, right))
    if residuals[-1] == 0.0:
        roots.append(grid[-1])
    roots.sort()
    deduped: list[float] = []
    for root in roots:
        if not deduped or abs(root - deduped[-1]) > dedup_tolerance_K:
            deduped.append(root)
    return tuple(deduped)


def _cstr_steady_state_point(
    spec: CSTRMultiplicitySpec,
    *,
    temperature_K: float,
    residual_tolerance_W: float,
    stability_tolerance_s_inv: float,
) -> CSTRSteadyStatePoint:
    residual = spec.energy_residual_w(temperature_K)
    if abs(residual) > residual_tolerance_W:
        raise RuntimeError(
            "CSTR steady-state root residual exceeded tolerance: "
            f"{residual} W at {temperature_K} K"
        )
    concentration_a = spec.steady_concentration_a_mol_l(temperature_K)
    concentration_p = spec.feed_concentration_A_mol_L - concentration_a
    eigenvalues = tuple(
        complex(value)
        for value in np.linalg.eigvals(_cstr_dynamic_jacobian(spec, temperature_K))
    )
    max_real = max(value.real for value in eigenvalues)
    if max_real < -stability_tolerance_s_inv:
        stability: SteadyStateStability = "stable"
    elif max_real > stability_tolerance_s_inv:
        stability = "unstable"
    else:
        stability = "marginal"
    return CSTRSteadyStatePoint(
        temperature_K=temperature_K,
        concentration_A_mol_L=concentration_a,
        concentration_P_mol_L=concentration_p,
        conversion=spec.steady_conversion(temperature_K),
        reaction_rate_mol_l_s=spec.reaction_rate_mol_l_s(temperature_K),
        heat_generation_w=spec.heat_generation_w(temperature_K),
        heat_removal_w=spec.heat_removal_w(temperature_K),
        residual_W=residual,
        eigenvalues=eigenvalues,
        stability=stability,
    )


def _cstr_dynamic_jacobian(
    spec: CSTRMultiplicitySpec,
    temperature_K: float,
) -> np.ndarray:
    k = spec.rate_constant_s_inv(temperature_K)
    dkdT = k * spec.arrhenius_Ea_J_per_mol / (
        8.31446261815324 * temperature_K * temperature_K
    )
    concentration_a = spec.steady_concentration_a_mol_l(temperature_K)
    residence_inverse = spec.volumetric_flow_L_s / spec.volume_L
    heat_factor = -spec.delta_h_J_per_mol / spec.rho_cp_J_per_L_K
    heat_removal_s_inv = spec.ua_W_per_K / (spec.rho_cp_J_per_L_K * spec.volume_L)
    return np.array(
        [
            [-residence_inverse - k, -concentration_a * dkdT],
            [
                heat_factor * k,
                (
                    -residence_inverse
                    - heat_removal_s_inv
                    + heat_factor * concentration_a * dkdT
                ),
            ],
        ],
        dtype=float,
    )


__all__ = [
    "BatchReactorModel",
    "CSTRModel",
    "CSTRMultiplicityResult",
    "CSTRMultiplicitySpec",
    "CSTRSteadyStatePoint",
    "DynamicBatchReactorModel",
    "FeedStreamSpec",
    "HeatTransferSpec",
    "JacketTemperatureProgram",
    "PFRModel",
    "ReactorResult",
    "ReactorState",
    "SamplingEventSpec",
    "SemiBatchFeedSpec",
    "SemiBatchReactorModel",
    "cstr_multiple_steady_state_reference_case",
    "reactor_model_cards",
    "solve_cstr_multiple_steady_states",
]
