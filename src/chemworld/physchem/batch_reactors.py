"""Batch and event-driven dynamic batch reactor models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from chemworld.physchem.reaction_network import ReactionNetworkSpec
from chemworld.physchem.reactor_shared import (
    HeatTransferSpec,
    JacketTemperatureProgram,
    ReactorResult,
    ReactorState,
    SamplingEventSpec,
)
from chemworld.physchem.reactor_solvers import (
    _amount_vector,
    _amounts_from_vector,
    _integrate_result,
    _jacket_heat_w,
    _material_balance_error,
    _reaction_heat_w,
    _segment_evaluation_times,
    _solve_interval,
)
from chemworld.physchem.thermochemistry import NASA7SpeciesThermo


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


__all__ = ["BatchReactorModel", "DynamicBatchReactorModel"]
