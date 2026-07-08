"""Observation and scoring services for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import Observation, PhysicalConstitution, WorldState
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.observation_kernel import (
    base_observed_mask,
    base_public_values,
    observation_units,
    processed_estimate,
    raw_signal,
)
from chemworld.world.operations import instrument_name, operation_name
from chemworld.world.scoring import score_observation
from chemworld.world.separation_kernel import downstream_truth_values


class ChemWorldObservationKernel:
    """Generate partial, noisy public observations from hidden state."""

    def __init__(
        self,
        constitution: PhysicalConstitution,
        objective: str,
        compiled_mechanism: CompiledMechanism | None = None,
    ) -> None:
        self.constitution = constitution
        self.objective = objective
        self.compiled_mechanism = compiled_mechanism
        self.species_view = MechanismSpeciesView(compiled_mechanism)

    def observe(
        self,
        state: WorldState,
        action: dict[str, Any],
        rng: np.random.Generator,
    ) -> Observation:
        operation = operation_name(action["operation"])
        if operation != "measure":
            last = dict(state.metadata.get("last_observation", {}))
            last_mask = dict(state.metadata.get("last_observed_mask", {}))
            values = self._base_public_values(state)
            observed_mask = self._base_observed_mask()
            values.update(last)
            observed_mask.update({str(key): bool(value) for key, value in last_mask.items()})
            values["cost"] = min(1.0, state.ledger.cost)
            values["safety_risk"] = state.ledger.risk
            observed_mask["cost"] = True
            observed_mask["safety_risk"] = True
            values["score"] = self._score(values)
            observed_mask["score"] = True
            return Observation(
                values=values,
                units=self._observation_units(),
                observed_mask=observed_mask,
                processed_estimate=self._processed_estimate(values, observed_mask),
            )

        instrument_id = instrument_name(action.get("instrument", "hplc"))
        instrument = self.constitution.instruments[instrument_id]
        truth_values = self._truth_values(state)
        noisy = self._base_public_values(state)
        observed_mask = self._base_observed_mask()
        for key in instrument.observable_keys:
            std = instrument.noise_std.get(key, 0.0)
            noisy[key] = float(np.clip(truth_values[key] + rng.normal(0.0, std), 0.0, 1.0))
            observed_mask[key] = True

        if observed_mask["byproduct_signal"] and observed_mask["degradation_warning"]:
            byproduct_signal = self._observed_value(noisy, "byproduct_signal")
            degradation_warning = self._observed_value(noisy, "degradation_warning")
            noisy["virtual_spectrum_summary"] = float(
                np.clip(
                    0.55 * byproduct_signal + 0.45 * degradation_warning,
                    0.0,
                    1.0,
                )
            )
            observed_mask["virtual_spectrum_summary"] = True
        noisy["cost"] = min(1.0, state.ledger.cost)
        noisy["safety_risk"] = state.ledger.risk
        observed_mask["cost"] = True
        observed_mask["safety_risk"] = True
        noisy["score"] = self._score(noisy)
        observed_mask["score"] = True
        return Observation(
            values=noisy,
            units=self._observation_units(),
            observed_mask=observed_mask,
            raw_signal=self._raw_signal(instrument_id, noisy, state, rng),
            processed_estimate=self._processed_estimate(noisy, observed_mask),
            uncertainty={
                f"{key}_std": float(std)
                for key, std in instrument.noise_std.items()
                if observed_mask.get(key, False)
            },
            instrument_id=instrument_id,
            cost=instrument.cost,
            sample_consumed_L=instrument.sample_volume_L,
        )

    def failed_observation(self) -> Observation:
        """Return a non-informative observation for failed action preconditions."""

        units = self._observation_units()
        return Observation(
            values=dict.fromkeys(units, None),
            units=units,
            observed_mask=dict.fromkeys(units, False),
            raw_signal={},
            processed_estimate={},
            uncertainty={},
            instrument_id=None,
            cost=0.0,
            sample_consumed_L=0.0,
        )

    @staticmethod
    def _processed_estimate(
        values: dict[str, float | None],
        observed_mask: dict[str, bool],
    ) -> dict[str, float | None]:
        return processed_estimate(values, observed_mask)

    @staticmethod
    def _raw_signal(
        instrument_id: str,
        values: dict[str, float | None],
        state: WorldState,
        rng: np.random.Generator,
    ) -> dict[str, Any]:
        replicate_count = 3 if instrument_id == "final_assay" else 2
        return raw_signal(
            instrument_id,
            values,
            species_amounts_mol=state.species_amounts,
            volume_L=state.volume_L,
            seed=int(rng.integers(0, 2**31 - 1)),
            replicate_count=replicate_count,
        )

    @staticmethod
    def _observation_units() -> dict[str, str]:
        return observation_units()

    @staticmethod
    def _base_public_values(state: WorldState) -> dict[str, float | None]:
        return base_public_values(cost=state.ledger.cost, safety_risk=state.ledger.risk)

    @staticmethod
    def _base_observed_mask() -> dict[str, bool]:
        return base_observed_mask()

    @staticmethod
    def _observed_value(values: dict[str, float | None], key: str) -> float:
        value = values.get(key)
        return 0.0 if value is None else float(value)

    def _score(self, values: dict[str, float | None]) -> float:
        return score_observation(
            objective=self.objective,
            product_yield=self._observed_value(values, "yield"),
            selectivity=self._observed_value(values, "selectivity"),
            conversion=self._observed_value(values, "conversion"),
            cost=self._observed_value(values, "cost"),
            safety_risk=self._observed_value(values, "safety_risk"),
        )

    def _truth_values(self, state: WorldState) -> dict[str, float]:
        truth = self.species_view.truth_values(state)
        truth.update(
            downstream_truth_values(
                state,
                product_amount_mol=self.species_view.target_amount(state),
                impurity_amount_mol=self.species_view.impurity_amount(state),
                initial_product_mol=max(self.species_view.initial_reactant_amount(state), 1.0e-12),
            )
        )
        return truth


__all__ = ["ChemWorldObservationKernel"]
