"""Observation and scoring services for the transactional runtime."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import Observation, PhysicalConstitution, WorldState
from chemworld.foundation.state import ProcessLedger, selected_phase_id
from chemworld.physchem.equilibrium_chemistry import (
    SolubilityProductSpec,
    apply_precipitation_hooks,
    solve_monoprotic_acid_base,
)
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.observation_contracts import TaskObservationContract
from chemworld.world.observation_kernel import (
    base_observed_mask,
    base_public_values,
    observation_units,
    processed_estimate,
    raw_signal,
)
from chemworld.world.operations import instrument_name, operation_name
from chemworld.world.scoring import TaskScoringContract, task_score_observation
from chemworld.world.separation_kernel import downstream_truth_values


class ChemWorldObservationKernel:
    """Generate partial, noisy public observations from hidden state."""

    def __init__(
        self,
        constitution: PhysicalConstitution,
        objective: str,
        compiled_mechanism: CompiledMechanism,
        scoring_contract: TaskScoringContract | None = None,
        observation_contract: TaskObservationContract | None = None,
    ) -> None:
        self.constitution = constitution
        self.objective = objective
        self.compiled_mechanism = compiled_mechanism
        self.scoring_contract = scoring_contract or TaskScoringContract.from_success_metrics(
            objective=objective,
        )
        self.observation_contract = observation_contract
        self.species_view = MechanismSpeciesView(compiled_mechanism)

    def observe(
        self,
        state: WorldState,
        action: dict[str, Any],
        rng: np.random.Generator,
    ) -> Observation:
        operation = operation_name(action["operation"])
        if operation != "measure":
            process = state.process or ProcessLedger()
            last = dict(process.last_observation)
            last_mask = dict(process.last_observed_mask)
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
        observable_keys = (
            instrument.observable_keys
            if self.observation_contract is None
            else self.observation_contract.observable_keys_for_instrument(
                instrument_id,
                instrument.observable_keys,
            )
        )
        selected_keys = set(observable_keys)
        for key in instrument.observable_keys:
            std = instrument.noise_std.get(key, 0.0)
            value = float(np.clip(truth_values[key] + rng.normal(0.0, std), 0.0, 1.0))
            if key in selected_keys:
                noisy[key] = value
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
        public_species_amounts = self._public_species_amounts(
            state,
            observable_keys=observable_keys,
        )
        return Observation(
            values=noisy,
            units=self._observation_units(),
            observed_mask=observed_mask,
            raw_signal=self._raw_signal(
                instrument_id,
                noisy,
                state,
                rng,
                species_amounts_mol=public_species_amounts,
            ),
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

    def _raw_signal(
        self,
        instrument_id: str,
        values: dict[str, float | None],
        state: WorldState,
        rng: np.random.Generator,
        *,
        species_amounts_mol: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        replicate_count = 3 if instrument_id == "final_assay" else 2
        packet = raw_signal(
            instrument_id,
            values,
            species_amounts_mol=species_amounts_mol,
            volume_L=state.volume_L,
            seed=int(rng.integers(0, 2**31 - 1)),
            replicate_count=replicate_count,
        )
        if species_amounts_mol is not None:
            packet["source"] = "task_public_species_calibration"
            packet["visibility"] = "task_observation_contract"
        return packet

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
        return task_score_observation(
            contract=self.scoring_contract,
            values=values,
        )

    def _truth_values(self, state: WorldState) -> dict[str, float]:
        truth = self.species_view.truth_values(state)
        truth.update(
            downstream_truth_values(
                state,
                product_amount_mol=self.species_view.target_amount(state),
                impurity_amount_mol=self.species_view.impurity_amount(state),
                initial_product_mol=max(self.species_view.initial_reactant_amount(state), 1.0e-12),
                target_species=self.species_view.target_species_for_state(state),
                impurity_species=self.species_view.impurity_species_for_state(state),
            )
        )
        truth.update(self._equilibrium_truth_values(state))
        return truth

    def _equilibrium_truth_values(self, state: WorldState) -> dict[str, float]:
        """Return public equilibrium-characterization signals in [0, 1].

        The underlying weak-acid and precipitation calculations use D4
        equilibrium-chemistry kernels, but only normalized instrument-facing
        estimates are returned here. Hidden equilibrium constants and mechanism
        species ids remain outside the public observation.
        """

        volume_L = max(float(state.volume_L), 1.0e-9)
        acid_total = max(self.species_view.initial_reactant_amount(state), 0.0)
        if acid_total <= 0.0:
            return {
                "pH_normalized": 7.0 / 14.0,
                "acid_dissociation_fraction": 0.0,
                "precipitation_signal": 0.0,
                "equilibrium_residual": 1.0,
                "equilibrium_confidence": 0.0,
            }

        pka = self._hidden_acid_pka(state)
        strong_cation = min(0.020, 0.15 * acid_total)
        strong_anion = min(0.020, 0.08 * acid_total)
        acid = solve_monoprotic_acid_base(
            acid_total_mol=acid_total,
            volume_L=volume_L,
            pka=pka,
            temperature_K=state.temperature_K,
            strong_cation_mol=strong_cation,
            strong_anion_mol=strong_anion,
        )
        precipitation = apply_precipitation_hooks(
            {
                "Ag+": strong_cation + 0.10 * acid.species_amounts_mol.get("A-", 0.0),
                "Cl-": strong_anion + 0.08 * acid.species_amounts_mol.get("HA", 0.0),
            },
            (
                SolubilityProductSpec(
                    precipitate_id="AgCl_public",
                    cation_id="Ag+",
                    anion_id="Cl-",
                    ksp=1.8e-10,
                ),
            ),
            volume_L=volume_L,
        )
        precipitation_signal = float(
            np.clip(precipitation.total_precipitated_mol / max(acid_total, 1.0e-12), 0.0, 1.0)
        )
        residual = float(
            np.clip(
                abs(acid.charge_balance_error_eq) / max(acid_total / volume_L, 1.0e-12),
                0.0,
                1.0,
            )
        )
        confidence = float(
            np.clip(
                0.55 * (1.0 - residual)
                + 0.25 * acid.acid_dissociation_fraction
                + 0.20 * (1.0 - min(abs(acid.pH - 4.5) / 4.5, 1.0)),
                0.0,
                1.0,
            )
        )
        return {
            "pH_normalized": float(np.clip(acid.pH / 14.0, 0.0, 1.0)),
            "acid_dissociation_fraction": float(
                np.clip(acid.acid_dissociation_fraction, 0.0, 1.0)
            ),
            "precipitation_signal": precipitation_signal,
            "equilibrium_residual": residual,
            "equilibrium_confidence": confidence,
        }

    @staticmethod
    def _hidden_acid_pka(state: WorldState) -> float:
        scenario_id = str(state.metadata.get("scenario_id", "equilibrium-characterization"))
        jitter = (sum(ord(char) for char in scenario_id) % 13) / 100.0
        temperature_shift = np.clip((state.temperature_K - 298.15) / 600.0, -0.25, 0.25)
        return float(4.55 + jitter - temperature_shift)

    def _public_species_amounts(
        self,
        state: WorldState,
        *,
        observable_keys: tuple[str, ...],
    ) -> dict[str, float] | None:
        if self.observation_contract is None:
            return state.species_amounts
        keys = set(observable_keys)
        downstream_public_amounts = self._selected_phase_public_species_amounts(
            state,
            observable_keys=keys,
        )
        if downstream_public_amounts is not None:
            return downstream_public_amounts
        public_amounts: dict[str, float] = {}
        reaction_keys = {
            "yield",
            "selectivity",
            "conversion",
            "byproduct_signal",
            "degradation_warning",
        }
        target_keys = {
            "yield",
            "selectivity",
            "purity",
            "recovery",
            "phase_ratio",
            "product_in_organic",
            "product_in_aqueous",
            "crystal_yield",
            "crystal_purity",
            "distillate_purity",
            "distillate_recovery",
            "flow_conversion",
            "electrochemical_selectivity",
        }
        impurity_keys = {
            "selectivity",
            "byproduct_signal",
            "purity",
            "impurity_signal",
            "process_mass_balance_error",
            "crystal_purity",
            "distillate_purity",
        }
        if keys.intersection(reaction_keys):
            public_amounts["reactant_public"] = self.species_view.reactant_amount(state)
        if keys.intersection(target_keys):
            public_amounts["target_public"] = self.species_view.target_amount(state)
        if keys.intersection(impurity_keys):
            public_amounts["impurity_public"] = max(
                self.species_view.byproduct_amount(state),
                self.species_view.impurity_amount(state)
                - self.species_view.degradation_amount(state),
                0.0,
            )
        if "degradation_warning" in keys:
            public_amounts["degradation_public"] = self.species_view.degradation_amount(state)
        return {
            species_id: amount
            for species_id, amount in public_amounts.items()
            if amount > 0.0
        } or None

    def _selected_phase_public_species_amounts(
        self,
        state: WorldState,
        *,
        observable_keys: set[str],
    ) -> dict[str, float] | None:
        downstream_keys = {
            "purity",
            "recovery",
            "phase_ratio",
            "product_in_organic",
            "product_in_aqueous",
            "impurity_signal",
            "process_mass_balance_error",
            "crystal_yield",
            "crystal_purity",
            "distillate_purity",
            "distillate_recovery",
        }
        if not observable_keys.intersection(downstream_keys):
            return None
        if state.phases is None:
            return None
        selected_id = selected_phase_id(state.phases)
        if selected_id is None:
            return None
        selected = state.phases.phases.get(selected_id)
        if selected is None:
            return None

        phase_amounts = selected.species_amounts_mol
        target_amount = self._phase_amount(phase_amounts, self.species_view.target_species)
        byproduct_amount = self._phase_amount(phase_amounts, self.species_view.byproduct_species)
        degradation_amount = self._phase_amount(
            phase_amounts,
            self.species_view.degradation_species,
        )
        impurity_amount = self._phase_amount(phase_amounts, self.species_view.impurity_species)
        reactant_amount = float(
            phase_amounts.get(self.species_view.reactant_species(state), 0.0)
        )

        public_amounts: dict[str, float] = {}
        if reactant_amount > 0.0:
            public_amounts["reactant_public"] = reactant_amount
        if target_amount > 0.0:
            public_amounts["target_public"] = target_amount
        if impurity_amount > 0.0 or byproduct_amount > 0.0:
            public_amounts["impurity_public"] = max(
                impurity_amount - degradation_amount,
                byproduct_amount,
                0.0,
            )
        if degradation_amount > 0.0:
            public_amounts["degradation_public"] = degradation_amount
        return public_amounts or None

    @staticmethod
    def _phase_amount(
        phase_amounts: dict[str, float],
        species_ids: tuple[str, ...],
    ) -> float:
        return sum(float(phase_amounts.get(species_id, 0.0)) for species_id in species_ids)


__all__ = ["ChemWorldObservationKernel"]
