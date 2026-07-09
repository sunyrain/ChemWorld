"""Executable physical constitution for ChemWorld environments."""

from __future__ import annotations

from typing import Any, ClassVar

from chemworld.foundation.constitution_preconditions import check_operation_preconditions
from chemworld.foundation.constitution_reports import CheckResult, ConstitutionReport
from chemworld.foundation.constitution_state_checks import (
    check_nonnegative,
    check_risk_range,
    check_typed_ledgers,
    check_units,
    check_vessel_bounds,
)
from chemworld.foundation.ontology import Instrument, Substance, Vessel
from chemworld.foundation.state import Observation, WorldState
from chemworld.foundation.units import canonical_unit


class PhysicalConstitution:
    """Executable constraints that every environment state must satisfy."""

    hidden_state_keys: ClassVar[set[str]] = {
        "species_amounts",
        "phase_ledger",
        "rate_constants",
        "theta",
        "temperature_internal",
        "true_yield",
        "true_selectivity",
        "true_conversion",
    }

    primary_reactor_metadata_keys: ClassVar[set[str]] = {
        "catalyst",
        "solvent",
        "stirring_speed_rpm",
    }

    primary_phase_metadata_keys: ClassVar[set[str]] = {
        "phase_system",
        "phase_settled",
        "selected_phase",
    }

    primary_instrument_metadata_keys: ClassVar[set[str]] = {
        "final_assay_done",
        "final_assay_time_s",
    }

    primary_crystallizer_metadata_keys: ClassVar[set[str]] = {
        "crystal_seeded",
        "crystal_seed_mass_g",
    }

    primary_crystallization_output_metadata_keys: ClassVar[set[str]] = {
        "crystallization_active",
        "crystal_product_mol",
        "crystal_impurity_mol",
    }

    primary_distillation_output_metadata_keys: ClassVar[set[str]] = {
        "distillation_active",
        "distillate_product_mol",
        "distillate_impurity_mol",
    }

    primary_process_metric_metadata_keys: ClassVar[set[str]] = {
        "last_observation",
        "last_observed_mask",
        "pre_separation_product_mol",
        "purity",
        "recovery",
        "solvent_loss",
        "crystal_yield",
        "crystal_purity",
        "crystal_size",
        "distillate_purity",
        "distillate_recovery",
        "flow_conversion",
        "flow_campaign_time_s",
        "flow_throughput_mL",
        "electrochemical_model",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "equilibrium_potential_V",
        "overpotential_V",
        "kinetic_current_A",
        "actual_current_A",
        "charge_C",
        "faradaic_charge_C",
        "electrical_work_J",
    }

    required_state_units: ClassVar[dict[str, str]] = {
        "volume_L": "L",
        "temperature_K": "K",
        "pressure_Pa": "Pa",
        "ledger.time_s": "s",
        "ledger.cost": "currency",
        "ledger.risk": "risk",
        "ledger.sample_consumed_L": "L",
    }

    def __init__(
        self,
        *,
        substances: dict[str, Substance],
        vessel: Vessel,
        instruments: dict[str, Instrument],
        max_yield: float = 1.0,
        tolerance: float = 1.0e-8,
    ) -> None:
        self.substances = substances
        self.vessel = vessel
        self.instruments = instruments
        self.max_yield = max_yield
        self.tolerance = tolerance

    def check_state(self, state: WorldState) -> ConstitutionReport:
        checks = [
            *check_nonnegative(self, state),
            *check_units(self),
            *check_vessel_bounds(self, state),
            *check_typed_ledgers(self, state),
            check_risk_range(self, state),
        ]
        return ConstitutionReport(checks)

    def check_observation(
        self,
        observation: Observation,
        *,
        debug_truth: bool = False,
    ) -> ConstitutionReport:
        checks: list[CheckResult] = []
        if not debug_truth:
            leaked = sorted(self.hidden_state_keys & observation.values.keys())
            checks.append(
                CheckResult(
                    "observation_non_omniscient",
                    not leaked,
                    "" if not leaked else f"Hidden keys leaked: {leaked}",
                )
            )
        checks.append(
            CheckResult(
                "measurement_has_cost",
                observation.instrument_id is None
                or observation.cost > 0.0
                or observation.sample_consumed_L > 0.0,
                "Instrument observations must consume cost or sample.",
            )
        )
        for key, unit in observation.units.items():
            try:
                canonical_unit(unit)
                passed = True
            except ValueError:
                passed = False
            checks.append(CheckResult(f"observation_unit:{key}", passed, unit))
        return ConstitutionReport(checks)

    def check_preconditions(
        self,
        operation_type: str,
        state: WorldState,
        payload: dict[str, Any],
    ) -> dict[str, bool]:
        return check_operation_preconditions(self, operation_type, state, payload)

    def check_material_conservation(
        self,
        before: WorldState,
        after: WorldState,
        *,
        allowed_element_delta: dict[str, float] | None = None,
    ) -> CheckResult:
        allowed_element_delta = allowed_element_delta or {}
        before_elements = self.element_totals(before.species_amounts)
        after_elements = self.element_totals(after.species_amounts)
        errors: list[float] = []
        elements = before_elements.keys() | after_elements.keys() | allowed_element_delta.keys()
        for element in sorted(elements):
            expected = before_elements.get(element, 0.0) + allowed_element_delta.get(element, 0.0)
            errors.append(abs(after_elements.get(element, 0.0) - expected))
        max_error = max(errors) if errors else 0.0
        return CheckResult(
            "material_conservation",
            max_error <= self.tolerance,
            f"max element-balance error={max_error:.3g}",
            value=max_error,
            tolerance=self.tolerance,
        )

    def check_yield_upper_bound(self, product_amount: float, limiting_amount: float) -> CheckResult:
        yield_value = 0.0 if limiting_amount <= self.tolerance else product_amount / limiting_amount
        return CheckResult(
            "yield_upper_bound",
            yield_value <= self.max_yield + self.tolerance,
            f"yield={yield_value:.3g}",
            value=yield_value,
            tolerance=self.tolerance,
        )

    def element_totals(self, species_amounts: dict[str, float]) -> dict[str, float]:
        totals: dict[str, float] = {}
        for species_id, amount in species_amounts.items():
            substance = self.substances.get(species_id)
            if substance is None:
                continue
            for element, count in substance.formula.items():
                totals[element] = totals.get(element, 0.0) + amount * count
        return totals


__all__ = ["CheckResult", "ConstitutionReport", "PhysicalConstitution"]
