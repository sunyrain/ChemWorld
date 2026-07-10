"""Reaction ODE kernel for the shared ChemWorld law."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from chemworld.foundation import WorldState, equipment_settings
from chemworld.physchem.solver_backend import (
    RUNTIME_REACTION_KERNEL_ODE_POLICY,
    solve_ode,
)

R_GAS = 8.31446261815324


@dataclass(frozen=True)
class ReactionIntegrationResult:
    species_amounts: dict[str, float]
    temperature_K: float
    duration_s: float
    cost_delta: float
    energy_jacket_J: float
    heat_reaction_J: float
    heat_loss_J: float
    stirring_speed_rpm: float
    solver_diagnostic: dict[str, object] = field(default_factory=dict)


def integrate_compiled_reaction_ode(
    *,
    state: WorldState,
    world: Any,
    compiled_mechanism: Any,
    duration_s: float,
    target_temperature_K: float,
    heat: bool,
    stirring_speed_rpm: float,
) -> ReactionIntegrationResult | None:
    """Integrate a mechanism-compiled reaction network and thermal balance.

    The transactional runtime treats mechanism YAML as the owner of species and reactions. The
    seven-slot ODE remains available only as an explicit reference fixture in
    :mod:`chemworld.world.reaction_reference`.
    """

    if compiled_mechanism is None:
        raise ValueError("compiled_mechanism is required for reaction integration")

    duration = float(np.clip(duration_s, 0.0, 14_400.0))
    if duration <= 0.0 or state.volume_L <= 0.0:
        return None

    network = compiled_mechanism.network
    species_ids = network.species_ids
    target_temperature = float(np.clip(target_temperature_K, 250.0, 520.0))
    stirring_speed = float(np.clip(stirring_speed_rpm, 100.0, 1200.0))
    y0 = np.array(
        [state.species_amounts.get(species_id, 0.0) for species_id in species_ids]
        + [state.temperature_K, 0.0, 0.0, 0.0],
    )
    report = solve_ode(
        lambda _t, y: compiled_reaction_ode_rhs(
            y=y,
            state=state,
            world=world,
            compiled_mechanism=compiled_mechanism,
            target_temperature_K=target_temperature,
            heat=heat,
            stirring_speed_rpm=stirring_speed,
        ),
        y0,
        time_span_s=(0.0, duration),
        policy=RUNTIME_REACTION_KERNEL_ODE_POLICY,
    )
    report.raise_for_failure("Compiled mechanism integration")
    result = report.raw_result
    y = np.maximum(result.y[:, -1], 0.0)
    species_amounts = state.species_amounts.copy()
    for index, species_id in enumerate(species_ids):
        species_amounts[species_id] = float(y[index])
    offset = len(species_ids)
    return ReactionIntegrationResult(
        species_amounts=species_amounts,
        temperature_K=float(np.clip(y[offset], 250.0, 520.0)),
        duration_s=duration,
        cost_delta=duration / 3600.0 * (0.03 if heat else 0.01),
        energy_jacket_J=float(y[offset + 1]),
        heat_reaction_J=float(y[offset + 2]),
        heat_loss_J=float(y[offset + 3]),
        stirring_speed_rpm=stirring_speed,
        solver_diagnostic=report.diagnostic.to_dict(),
    )


def compiled_reaction_ode_rhs(
    *,
    y: np.ndarray,
    state: WorldState,
    world: Any,
    compiled_mechanism: Any,
    target_temperature_K: float,
    heat: bool,
    stirring_speed_rpm: float,
) -> np.ndarray:
    network = compiled_mechanism.network
    species_ids = network.species_ids
    species_count = len(species_ids)
    amounts_array = np.maximum(y[:species_count], 0.0)
    temperature = float(np.clip(y[species_count], 250.0, 520.0))
    volume = max(state.volume_L, 1.0e-6)
    amounts = {
        species_id: float(amount)
        for species_id, amount in zip(species_ids, amounts_array, strict=True)
    }
    rates_mol_L_s = network.reaction_rates(
        amounts,
        volume_L=volume,
        temperature_K=temperature,
    )
    reactor_settings = equipment_settings(state.equipment, "batch_reactor")
    catalyst = int(reactor_settings.get("catalyst", 0))
    solvent = int(reactor_settings.get("solvent", 0))
    stirring_factor = 0.70 + 0.30 * (1.0 - np.exp(-stirring_speed_rpm / 420.0))

    derivatives = np.zeros(species_count + 4)
    reaction_heat_W = 0.0
    for reaction_index, reaction in enumerate(network.reactions):
        hidden_modifier = _hidden_reaction_modifier(
            world,
            catalyst=catalyst,
            solvent=solvent,
            reaction_index=reaction_index,
            stirring_factor=stirring_factor,
        )
        rate_mol_s = rates_mol_L_s[reaction.reaction_id] * volume * hidden_modifier
        for species_id, coefficient in reaction.stoichiometry.items():
            derivatives[network.species_index[species_id]] += coefficient * rate_mol_s
        reaction_heat_W += reaction.delta_h_J_per_mol * rate_mol_s

    q_jacket = 0.0
    if heat:
        q_jacket = float(np.clip((target_temperature_K - temperature) * 4.0, -70.0, 90.0))
    heat_loss = world.ua_W_per_K * (temperature - world.environment_temperature_K)
    heat_capacity = max(world.rho_cp_J_per_L_K * volume, 1.0e-6)
    derivatives[species_count] = (q_jacket - heat_loss - reaction_heat_W) / heat_capacity
    derivatives[species_count + 1] = q_jacket
    derivatives[species_count + 2] = reaction_heat_W
    derivatives[species_count + 3] = heat_loss
    return derivatives


def _hidden_reaction_modifier(
    world: Any,
    *,
    catalyst: int,
    solvent: int,
    reaction_index: int,
    stirring_factor: float,
) -> float:
    catalyst_effects = np.asarray(world.catalyst_effects, dtype=float)
    solvent_effects = np.asarray(world.solvent_effects, dtype=float)
    catalyst_index = int(np.clip(catalyst, 0, catalyst_effects.shape[0] - 1))
    solvent_index = int(np.clip(solvent, 0, solvent_effects.shape[0] - 1))
    catalyst_reaction_index = min(reaction_index, catalyst_effects.shape[-1] - 1)
    solvent_reaction_index = min(reaction_index, solvent_effects.shape[-1] - 1)
    catalyst_factor = (
        catalyst_effects[catalyst_index, catalyst_reaction_index]
        if catalyst_effects.ndim == 2
        else catalyst_effects[catalyst_index]
    )
    solvent_factor = (
        solvent_effects[solvent_index, solvent_reaction_index]
        if solvent_effects.ndim == 2
        else solvent_effects[solvent_index]
    )
    return float(catalyst_factor * solvent_factor * stirring_factor)


@dataclass(frozen=True)
class ReactionModuleSpec:
    module_id: str = "reaction"
    version: str = "0.3"
    laws: tuple[str, ...] = (
        "arrhenius_kinetics",
        "catalyst_solvent_effects",
        "byproduct_formation",
        "product_degradation",
        "catalyst_deactivation",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "laws": list(self.laws),
            "gas_constant_J_per_mol_K": R_GAS,
            "runtime": "compiled_mechanism",
            "mechanism_contract": {
                "species": "loaded from CompiledMechanism.network.species_ids",
                "stoichiometry": "loaded from CompiledMechanism.network.reactions",
                "rate_laws": "enumerated rate-law evaluators from mechanism YAML",
            },
        }


__all__ = [
    "R_GAS",
    "ReactionIntegrationResult",
    "ReactionModuleSpec",
    "compiled_reaction_ode_rhs",
    "integrate_compiled_reaction_ode",
]
