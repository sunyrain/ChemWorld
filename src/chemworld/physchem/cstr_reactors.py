"""Continuous stirred-tank reactor models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from chemworld.physchem.reaction_network import ReactionNetworkSpec
from chemworld.physchem.reactor_shared import (
    FeedStreamSpec,
    HeatTransferSpec,
    ReactorResult,
)
from chemworld.physchem.reactor_solvers import (
    _amount_vector,
    _amounts_from_vector,
    _integrate_result,
    _reaction_heat_w,
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


__all__ = ["CSTRModel"]
