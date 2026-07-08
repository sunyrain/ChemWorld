"""Mechanism-aware species role helpers for Runtime v2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from chemworld.foundation import WorldState
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.world.species_roles import (
    LEGACY_ACTIVE_CATALYST_SPECIES,
    LEGACY_BYPRODUCT_SPECIES,
    LEGACY_DEGRADATION_SPECIES,
    LEGACY_IMPURITY_SPECIES,
    LEGACY_INITIAL_REACTANT_METADATA_KEY,
    LEGACY_REACTANT_SPECIES,
    LEGACY_TARGET_SPECIES,
)


@dataclass(frozen=True)
class MechanismSpeciesView:
    """Resolve semantic species roles from a compiled mechanism.

    The current semi-mechanistic backend still has a legacy batch-reaction
    integrator. This view isolates legacy fallback names in one place while
    allowing runtime services to ask for reactant, product, impurity, catalyst,
    and degradation amounts by role.
    """

    mechanism: CompiledMechanism | None = None

    @property
    def target_species(self) -> tuple[str, ...]:
        if self.mechanism is None or not self.mechanism.score_spec.target_species:
            return (LEGACY_TARGET_SPECIES,)
        return self.mechanism.score_spec.target_species

    @property
    def impurity_species(self) -> tuple[str, ...]:
        if self.mechanism is None or not self.mechanism.score_spec.impurity_species:
            return LEGACY_IMPURITY_SPECIES
        return self.mechanism.score_spec.impurity_species

    @property
    def byproduct_species(self) -> tuple[str, ...]:
        if self.mechanism is None:
            return LEGACY_BYPRODUCT_SPECIES
        species = self.mechanism.observable_mapping.get("byproduct", ())
        return species or tuple(
            species_id
            for species_id in self.impurity_species
            if species_id not in self.degradation_species
        )

    @property
    def degradation_species(self) -> tuple[str, ...]:
        if self.mechanism is None:
            return LEGACY_DEGRADATION_SPECIES
        return (
            self.mechanism.observable_mapping.get("degradation", ())
            or LEGACY_DEGRADATION_SPECIES
        )

    @property
    def catalyst_species(self) -> tuple[str, ...]:
        if self.mechanism is None:
            return (LEGACY_ACTIVE_CATALYST_SPECIES,)
        return self.mechanism.observable_mapping.get("catalyst", ()) or (
            LEGACY_ACTIVE_CATALYST_SPECIES,
        )

    @property
    def primary_target_species(self) -> str:
        return self.target_species[0]

    @property
    def primary_impurity_species(self) -> str:
        return self.impurity_species[0] if self.impurity_species else LEGACY_IMPURITY_SPECIES[0]

    def reactant_species(self, state: WorldState | None = None) -> str:
        if self.mechanism is not None and self.mechanism.score_spec.initial_limiting_species:
            species_id = self.mechanism.score_spec.initial_limiting_species
            if state is None or species_id in state.species_amounts:
                return species_id
        if self.mechanism is not None:
            reactants = self.mechanism.observable_mapping.get("reactant", ())
            for species_id in reactants:
                if state is None or species_id in state.species_amounts:
                    return species_id
        return LEGACY_REACTANT_SPECIES

    def active_catalyst_species(self, state: WorldState | None = None) -> str:
        for species_id in self.catalyst_species:
            is_active = "active" in species_id.lower()
            is_present = state is None or species_id in state.species_amounts
            if is_active and is_present:
                return species_id
        for species_id in self.catalyst_species:
            if state is None or species_id in state.species_amounts:
                return species_id
        return LEGACY_ACTIVE_CATALYST_SPECIES

    def reaction_backend_species_map(self, state: WorldState) -> dict[str, str]:
        """Map the lite reaction backend slots onto mechanism-owned species.

        The current ODE backend still integrates a compact seven-slot reaction
        scaffold. This method keeps that scaffold behind semantic species roles
        so runtime state no longer has to be initialized with ``A/P/B/D/E``.
        """

        target = self._first_existing(self.target_species_for_state(state))
        reactant = self.reactant_species(state)
        impurity_candidates = tuple(
            species_id
            for species_id in self.impurity_species_for_state(state)
            if species_id != reactant and species_id != target
        )
        byproduct = self._first_existing(
            self.byproduct_species_for_state(state),
            exclude={reactant, target},
        ) or self._first_existing(impurity_candidates)
        degradation = self._first_existing(
            self.degradation_species_for_state(state),
            exclude={reactant, target, byproduct} if byproduct else {reactant, target},
        ) or self._first_existing(
            impurity_candidates,
            exclude={byproduct} if byproduct else set(),
        )
        coupled = self._first_existing(
            impurity_candidates,
            exclude={species_id for species_id in (byproduct, degradation) if species_id},
        )
        active_catalyst = self.active_catalyst_species(state)
        catalyst_dead = "Cat_dead"
        if active_catalyst != LEGACY_ACTIVE_CATALYST_SPECIES:
            candidate = active_catalyst.replace("active", "dead").replace("Active", "Dead")
            catalyst_dead = candidate if candidate in state.species_amounts else "Cat_dead"
        return {
            LEGACY_REACTANT_SPECIES: reactant,
            LEGACY_TARGET_SPECIES: target,
            LEGACY_IMPURITY_SPECIES[0]: byproduct or LEGACY_IMPURITY_SPECIES[0],
            LEGACY_DEGRADATION_SPECIES[0]: degradation or LEGACY_DEGRADATION_SPECIES[0],
            "E": coupled or "E",
            LEGACY_ACTIVE_CATALYST_SPECIES: active_catalyst,
            "Cat_dead": catalyst_dead,
        }

    @staticmethod
    def _first_existing(
        species_ids: tuple[str, ...],
        *,
        exclude: set[str | None] | None = None,
    ) -> str:
        excluded = set(exclude or set())
        for species_id in species_ids:
            if species_id not in excluded:
                return species_id
        return ""

    def target_species_for_state(self, state: WorldState) -> tuple[str, ...]:
        species = tuple(
            species_id
            for species_id in self.target_species
            if species_id in state.species_amounts
        )
        if species:
            return species
        return (LEGACY_TARGET_SPECIES,)

    def impurity_species_for_state(self, state: WorldState) -> tuple[str, ...]:
        species = tuple(
            species_id
            for species_id in self.impurity_species
            if species_id in state.species_amounts
        )
        if species:
            return species
        return tuple(
            species_id
            for species_id in LEGACY_IMPURITY_SPECIES
            if species_id in state.species_amounts
        )

    def byproduct_species_for_state(self, state: WorldState) -> tuple[str, ...]:
        species = tuple(
            species_id
            for species_id in self.byproduct_species
            if species_id in state.species_amounts
        )
        return species or tuple(
            species_id
            for species_id in LEGACY_BYPRODUCT_SPECIES
            if species_id in state.species_amounts
        )

    def degradation_species_for_state(self, state: WorldState) -> tuple[str, ...]:
        species = tuple(
            species_id
            for species_id in self.degradation_species
            if species_id in state.species_amounts
        )
        return species or tuple(
            species_id
            for species_id in LEGACY_DEGRADATION_SPECIES
            if species_id in state.species_amounts
        )

    def amount(self, state: WorldState, species_ids: tuple[str, ...]) -> float:
        return sum(float(state.species_amounts.get(species_id, 0.0)) for species_id in species_ids)

    def target_amount(self, state: WorldState) -> float:
        return self.amount(state, self.target_species_for_state(state))

    def impurity_amount(self, state: WorldState) -> float:
        return self.amount(state, self.impurity_species_for_state(state))

    def byproduct_amount(self, state: WorldState) -> float:
        return self.amount(state, self.byproduct_species_for_state(state))

    def degradation_amount(self, state: WorldState) -> float:
        return self.amount(state, self.degradation_species_for_state(state))

    def reactant_amount(self, state: WorldState) -> float:
        return float(state.species_amounts.get(self.reactant_species(state), 0.0))

    def initial_reactant_amount(self, state: WorldState) -> float:
        reactant = self.reactant_species(state)
        candidates = (
            f"initial_{reactant}_mol",
            "initial_reactant_mol",
            LEGACY_INITIAL_REACTANT_METADATA_KEY,
        )
        for key in candidates:
            if key in state.metadata:
                return max(float(state.metadata.get(key, 0.0)), 0.0)
        if state.species is not None:
            amount = state.species.initial_amounts_mol.get(reactant)
            if amount is not None:
                return max(float(amount), 0.0)
        return max(
            self.reactant_amount(state) + self.target_amount(state) + self.impurity_amount(state),
            0.0,
        )

    def record_added_reactant(
        self,
        metadata: dict[str, Any],
        *,
        reactant_species: str,
        amount_mol: float,
    ) -> dict[str, Any]:
        metadata[f"initial_{reactant_species}_mol"] = (
            float(metadata.get(f"initial_{reactant_species}_mol", 0.0)) + amount_mol
        )
        metadata["initial_reactant_mol"] = (
            float(metadata.get("initial_reactant_mol", 0.0)) + amount_mol
        )
        if reactant_species == LEGACY_REACTANT_SPECIES:
            metadata[LEGACY_INITIAL_REACTANT_METADATA_KEY] = (
                float(metadata.get(LEGACY_INITIAL_REACTANT_METADATA_KEY, 0.0)) + amount_mol
            )
        return metadata

    def reagent_charge_amounts(
        self,
        state: WorldState,
        *,
        limiting_amount_mol: float,
    ) -> dict[str, float]:
        """Return mechanism-ratio reagent additions for one charge operation."""

        reactant = self.reactant_species(state)
        if self.mechanism is None:
            return {reactant: limiting_amount_mol}
        policy = self.mechanism.initial_amount_policy
        reference = float(policy.get(reactant, 0.0))
        if reference <= 0.0:
            return {reactant: limiting_amount_mol}
        return {
            species_id: limiting_amount_mol * float(amount) / reference
            for species_id, amount in policy.items()
            if amount > 0.0 and species_id in state.species_amounts
        } or {reactant: limiting_amount_mol}

    def truth_values(self, state: WorldState) -> dict[str, float]:
        initial = max(self.initial_reactant_amount(state), 1.0e-12)
        target = self.target_amount(state)
        impurity = self.impurity_amount(state)
        remaining = self.reactant_amount(state)
        consumed = max(initial - remaining, 1.0e-12)
        return {
            "yield": float(np.clip(target / initial, 0.0, 1.0)),
            "selectivity": float(np.clip(target / consumed, 0.0, 1.0)),
            "conversion": float(np.clip(consumed / initial, 0.0, 1.0)),
            "byproduct_signal": float(np.clip(impurity / initial, 0.0, 1.0)),
            "degradation_warning": float(
                np.clip(self.degradation_amount(state) / initial, 0.0, 1.0)
            ),
        }


__all__ = [
    "LEGACY_ACTIVE_CATALYST_SPECIES",
    "LEGACY_BYPRODUCT_SPECIES",
    "LEGACY_DEGRADATION_SPECIES",
    "LEGACY_IMPURITY_SPECIES",
    "LEGACY_REACTANT_SPECIES",
    "LEGACY_TARGET_SPECIES",
    "MechanismSpeciesView",
]
