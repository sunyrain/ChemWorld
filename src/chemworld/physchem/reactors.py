"""Mechanism-backed reactor models for ChemWorld.

The models in this module are deliberately compact, but they are real numerical
reactor kernels: they integrate arbitrary balanced ``ReactionNetworkSpec``
objects and return material/energy ledgers that can be audited by world-law
checks and benchmark metrics.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

from chemworld.physchem.reaction_network import ReactionNetworkSpec


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
) -> float:
    rates = network.reaction_rates(
        amounts_mol,
        volume_L=volume_L,
        temperature_K=temperature_K,
    )
    return sum(
        reaction.delta_h_J_per_mol * rates[reaction.reaction_id] * volume_L
        for reaction in network.reactions
    )


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


__all__ = [
    "BatchReactorModel",
    "CSTRModel",
    "FeedStreamSpec",
    "HeatTransferSpec",
    "PFRModel",
    "ReactorResult",
    "ReactorState",
    "SemiBatchFeedSpec",
    "SemiBatchReactorModel",
]
