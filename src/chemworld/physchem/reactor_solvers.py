"""Shared numerical helpers for zero-dimensional reactor models."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

from chemworld.physchem.reaction_network import ReactionNetworkSpec, ReactionSpec
from chemworld.physchem.reactor_shared import (
    HeatTransferSpec,
    ReactorResult,
    ReactorState,
    SemiBatchFeedSpec,
)
from chemworld.physchem.thermochemistry import (
    NASA7SpeciesThermo,
    reaction_thermochemistry,
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


__all__ = [
    "_amount_vector",
    "_amounts_from_vector",
    "_feed_heat_w",
    "_integrate_result",
    "_jacket_heat_w",
    "_material_balance_error",
    "_reaction_heat_w",
    "_segment_evaluation_times",
    "_solve",
    "_solve_interval",
]
