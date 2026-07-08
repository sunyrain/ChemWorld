"""Plug-flow reactor model."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from chemworld.physchem.reaction_network import ReactionNetworkSpec
from chemworld.physchem.reactor_shared import HeatTransferSpec, ReactorResult, ReactorState
from chemworld.physchem.reactor_solvers import _material_balance_error, _solve


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


__all__ = ["PFRModel"]
