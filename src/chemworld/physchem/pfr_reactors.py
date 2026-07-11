"""Plug-flow reactor model."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import pi

import numpy as np

from chemworld.physchem.reaction_network import ReactionNetworkSpec
from chemworld.physchem.reactor_shared import HeatTransferSpec, ReactorResult, ReactorState
from chemworld.physchem.reactor_solvers import _material_balance_error, _solve
from chemworld.physchem.transport import darcy_friction_factor


@dataclass(frozen=True)
class PFRGeometrySpec:
    """Incompressible tube geometry, hydraulics, and thermal boundary for a PFR."""

    length_m: float
    inner_diameter_m: float
    roughness_m: float = 1.0e-6
    fluid_density_kg_m3: float = 1000.0
    fluid_viscosity_Pa_s: float = 1.0e-3
    boundary_ua_W_per_m_K: float = 0.0
    boundary_temperature_K: float | None = None

    def __post_init__(self) -> None:
        if self.length_m <= 0.0:
            raise ValueError("PFR length_m must be positive")
        if self.inner_diameter_m <= 0.0:
            raise ValueError("PFR inner_diameter_m must be positive")
        if self.roughness_m < 0.0:
            raise ValueError("PFR roughness_m cannot be negative")
        if self.fluid_density_kg_m3 <= 0.0:
            raise ValueError("PFR fluid_density_kg_m3 must be positive")
        if self.fluid_viscosity_Pa_s <= 0.0:
            raise ValueError("PFR fluid_viscosity_Pa_s must be positive")
        if self.boundary_ua_W_per_m_K < 0.0:
            raise ValueError("PFR boundary_ua_W_per_m_K cannot be negative")
        if self.boundary_temperature_K is not None and self.boundary_temperature_K <= 0.0:
            raise ValueError("PFR boundary_temperature_K must be positive")

    @property
    def cross_section_area_m2(self) -> float:
        return pi * self.inner_diameter_m**2 / 4.0

    @property
    def volume_l(self) -> float:
        return self.cross_section_area_m2 * self.length_m * 1000.0

    def axial_velocity_m_s(self, volumetric_flow_L_s: float) -> float:
        return volumetric_flow_L_s / 1000.0 / self.cross_section_area_m2

    def reynolds_number(self, volumetric_flow_L_s: float) -> float:
        velocity = self.axial_velocity_m_s(volumetric_flow_L_s)
        return (
            self.fluid_density_kg_m3 * velocity * self.inner_diameter_m / self.fluid_viscosity_Pa_s
        )

    def pressure_gradient_pa_m(self, volumetric_flow_L_s: float) -> float:
        velocity = self.axial_velocity_m_s(volumetric_flow_L_s)
        reynolds = self.reynolds_number(volumetric_flow_L_s)
        friction = darcy_friction_factor(
            reynolds=reynolds,
            relative_roughness=self.roughness_m / self.inner_diameter_m,
        )
        return friction * self.fluid_density_kg_m3 * velocity**2 / (2.0 * self.inner_diameter_m)

    def to_dict(self) -> dict[str, float | None]:
        return {
            "length_m": self.length_m,
            "inner_diameter_m": self.inner_diameter_m,
            "roughness_m": self.roughness_m,
            "fluid_density_kg_m3": self.fluid_density_kg_m3,
            "fluid_viscosity_Pa_s": self.fluid_viscosity_Pa_s,
            "boundary_ua_W_per_m_K": self.boundary_ua_W_per_m_K,
            "boundary_temperature_K": self.boundary_temperature_K,
            "cross_section_area_m2": self.cross_section_area_m2,
            "volume_L": self.volume_l,
        }


@dataclass(frozen=True)
class PFRModel:
    network: ReactionNetworkSpec
    reactor_volume_L: float
    volumetric_flow_L_s: float
    geometry: PFRGeometrySpec | None = None
    inlet_pressure_Pa: float = 101_325.0
    reactor_id: str = "pfr"
    rate_multiplier: float = 1.0

    def __post_init__(self) -> None:
        if self.reactor_volume_L <= 0:
            raise ValueError("reactor_volume_L must be positive")
        if self.volumetric_flow_L_s <= 0:
            raise ValueError("volumetric_flow_L_s must be positive")
        if self.inlet_pressure_Pa <= 0.0:
            raise ValueError("inlet_pressure_Pa must be positive")
        if self.rate_multiplier <= 0.0 or not np.isfinite(self.rate_multiplier):
            raise ValueError("rate_multiplier must be positive and finite")
        if self.geometry is not None and not np.isclose(
            self.geometry.volume_l,
            self.reactor_volume_L,
            rtol=1.0e-6,
            atol=1.0e-12,
        ):
            raise ValueError("PFR geometry volume must match reactor_volume_L")

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
        axial_positions_m: Sequence[float] | None = None,
    ) -> ReactorResult:
        if evaluation_times_s is not None and axial_positions_m is not None:
            raise ValueError("Specify evaluation_times_s or axial_positions_m, not both")
        if axial_positions_m is not None:
            if self.geometry is None:
                raise ValueError("axial_positions_m requires a PFR geometry")
            positions = tuple(float(value) for value in axial_positions_m)
            if any(value < 0.0 or value > self.geometry.length_m for value in positions):
                raise ValueError("axial_positions_m must lie inside the PFR length")
            evaluation_times_s = tuple(
                float(
                    np.clip(
                        self.residence_time_s * value / self.geometry.length_m,
                        0.0,
                        self.residence_time_s,
                    )
                )
                for value in positions
            )
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
                self.inlet_pressure_Pa,
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
                rate = rates[reaction.reaction_id] * self.rate_multiplier
                for species_id, coefficient in reaction.stoichiometry.items():
                    dconcentrations[species_id] += coefficient * rate
            heat_reaction_per_L_W = sum(
                reaction.delta_h_J_per_mol * rates[reaction.reaction_id] * self.rate_multiplier
                for reaction in self.network.reactions
            )
            boundary_heat_W = 0.0
            if self.geometry is not None and self.geometry.boundary_temperature_K is not None:
                boundary_heat_W = (
                    self.geometry.boundary_ua_W_per_m_K
                    * self.geometry.length_m
                    * (self.geometry.boundary_temperature_K - temperature)
                )
            q_jacket_W = thermal.jacket_heat_w(temperature) + boundary_heat_W
            q_jacket_per_L_W = q_jacket_W / self.reactor_volume_L
            q_loss_per_L_W = thermal.heat_loss_w(temperature) / self.reactor_volume_L
            dtemperature = (
                q_jacket_per_L_W - q_loss_per_L_W - heat_reaction_per_L_W
            ) / thermal.rho_cp_J_per_L_K
            pressure_gradient = (
                0.0
                if self.geometry is None
                else self.geometry.pressure_gradient_pa_m(self.volumetric_flow_L_s)
            )
            axial_speed = (
                0.0 if self.geometry is None else self.geometry.length_m / self.residence_time_s
            )
            dpressure = -pressure_gradient * axial_speed
            return np.array(
                [
                    *(dconcentrations[species_id] for species_id in self.network.species_ids),
                    dtemperature,
                    dpressure,
                    q_jacket_W,
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
        pressure_index = n_species + 1
        amounts = {
            species_id: tuple(
                max(float(value), 0.0) * self.reactor_volume_L for value in result.y[idx]
            )
            for idx, species_id in enumerate(self.network.species_ids)
        }
        final_amounts = {species_id: values[-1] for species_id, values in amounts.items()}
        final_state = ReactorState(
            amounts_mol=final_amounts,
            volume_L=self.reactor_volume_L,
            temperature_K=max(float(result.y[n_species, -1]), 1.0),
            time_s=self.residence_time_s,
            energy_jacket_J=float(result.y[n_species + 2, -1]),
            heat_reaction_J=float(result.y[n_species + 3, -1]),
            heat_loss_J=float(result.y[n_species + 4, -1]),
        )
        initial_state = ReactorState(
            amounts_mol=initial_amounts,
            volume_L=self.reactor_volume_L,
            temperature_K=temperature_K,
            time_s=0.0,
        )
        pressures = tuple(float(value) for value in result.y[pressure_index])
        if min(pressures) <= 0.0:
            raise RuntimeError("PFR pressure-drop model reached nonpositive absolute pressure")
        axial_positions: tuple[float, ...]
        geometry_payload: dict[str, object] | None
        if self.geometry is None:
            axial_positions = ()
            pressure_drop = 0.0
            geometry_payload = None
        else:
            axial_positions = tuple(
                self.geometry.length_m * float(value) / self.residence_time_s for value in result.t
            )
            pressure_drop = pressures[0] - pressures[-1]
            geometry_payload = dict[str, object](self.geometry.to_dict())
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
                "rate_multiplier": self.rate_multiplier,
                "geometry": geometry_payload,
                "axial_positions_m": axial_positions,
                "pressures_Pa": pressures,
                "pressure_drop_Pa": pressure_drop,
                "reynolds_number": (
                    None
                    if self.geometry is None
                    else self.geometry.reynolds_number(self.volumetric_flow_L_s)
                ),
                "solver_diagnostic": result.diagnostic.to_dict(),
            },
        )


__all__ = ["PFRGeometrySpec", "PFRModel"]
