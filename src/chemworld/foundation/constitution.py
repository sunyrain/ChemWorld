"""Executable physical constitution for ChemWorld environments."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, ClassVar

from chemworld.foundation.ontology import Instrument, Substance, Vessel
from chemworld.foundation.state import (
    Observation,
    WorldState,
    equipment_settings,
    has_phase_system,
    instrument_completed,
    phases_are_settled,
)
from chemworld.foundation.units import canonical_unit


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    message: str = ""
    value: float | None = None
    tolerance: float | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "value": self.value,
            "tolerance": self.tolerance,
        }


@dataclass(frozen=True)
class ConstitutionReport:
    checks: list[CheckResult]

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)

    def failures(self) -> list[CheckResult]:
        return [check for check in self.checks if not check.passed]

    def to_list(self) -> list[dict[str, object]]:
        return [check.to_dict() for check in self.checks]


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
            *self._check_nonnegative(state),
            *self._check_units(state),
            *self._check_vessel_bounds(state),
            *self._check_typed_ledgers(state),
            self._check_risk_range(state),
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
        has_volume = state.volume_L > self.tolerance
        has_material = sum(state.species_amounts.values()) > self.tolerance
        is_terminated = state.terminated
        instrument_id = str(payload.get("instrument", "hplc"))
        instrument = self.instruments.get(instrument_id)
        if instrument is None and instrument_id.isdigit():
            instrument = list(self.instruments.values())[int(instrument_id) % len(self.instruments)]
        requires_terminated = (
            bool(instrument.requires_terminated) if instrument is not None else False
        )
        final_assay_done = instrument_completed(state.equipment, "final_assay")
        is_final_assay = operation_type == "measure" and instrument_id == "final_assay"
        phase_system = has_phase_system(state.phases)
        phase_settled = phases_are_settled(state.phases)
        crystallized = (
            state.phases is not None
            and "solid" in state.phases.phases
            and sum(state.phases.phases["solid"].species_amounts_mol.values()) > self.tolerance
        )
        distillate_ready = bool(state.metadata.get("distillation_active", False))
        flow_settings = equipment_settings(state.equipment, "flow_reactor")
        potential_settings = equipment_settings(state.equipment, "electrochemical_cell")
        flow_ready = {"flow_rate_mL_min", "residence_time_s"} <= set(flow_settings)
        potential_ready = {"potential_V", "current_mA"} <= set(potential_settings)
        phase_operations = {
            "add_extractant",
            "mix",
            "settle",
            "separate_phase",
            "wash",
            "dry",
            "concentrate",
            "transfer",
        }
        needs_volume = operation_type in {
            "heat",
            "wait",
            "sample",
            "quench",
            "measure",
            "add_extractant",
            "mix",
            "settle",
            "separate_phase",
            "wash",
            "dry",
            "concentrate",
            "transfer",
            "seed_crystals",
            "cool_crystallize",
            "filter_crystals",
            "evaporate",
            "distill",
            "collect_fraction",
            "set_potential",
            "run_flow",
            "electrolyze",
        }
        needs_material = operation_type in {
            "heat",
            "wait",
            "terminate",
            "add_extractant",
            "mix",
            "settle",
            "separate_phase",
            "wash",
            "dry",
            "concentrate",
            "transfer",
            "cool_crystallize",
            "filter_crystals",
            "distill",
            "collect_fraction",
            "set_potential",
            "run_flow",
            "electrolyze",
        }
        needs_not_terminated = operation_type in {
            "add_reagent",
            "add_solvent",
            "add_catalyst",
            "heat",
            "wait",
            "sample",
            "quench",
            "add_phase",
            "add_extractant",
            "mix",
            "settle",
            "separate_phase",
            "wash",
            "dry",
            "concentrate",
            "transfer",
            "seed_crystals",
            "cool_crystallize",
            "filter_crystals",
            "evaporate",
            "distill",
            "collect_fraction",
            "set_flow_rate",
            "run_flow",
            "set_potential",
            "electrolyze",
        }
        return {
            "instrument_available": operation_type != "measure" or instrument is not None,
            "has_volume": not needs_volume or has_volume,
            "has_material": not needs_material or has_material,
            "not_terminated": not needs_not_terminated or not state.terminated,
            "has_phase_system": operation_type not in phase_operations or phase_system,
            "phase_settled": operation_type != "separate_phase" or phase_settled,
            "measure_final_requires_terminated": operation_type != "measure"
            or not requires_terminated
            or is_terminated,
            "measure_final_not_repeated": not is_final_assay or not final_assay_done,
            "terminate_requires_material": operation_type != "terminate" or has_material,
            "filter_requires_crystallization": operation_type != "filter_crystals"
            or crystallized,
            "collect_fraction_requires_distillation": operation_type != "collect_fraction"
            or distillate_ready,
            "run_flow_requires_flow_setup": operation_type != "run_flow" or flow_ready,
            "electrolyze_requires_potential": operation_type != "electrolyze"
            or potential_ready,
        }

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

    def _check_nonnegative(self, state: WorldState) -> list[CheckResult]:
        values = {
            **{f"amount:{key}": value for key, value in state.species_amounts.items()},
            "volume_L": state.volume_L,
            "temperature_K": state.temperature_K,
            "pressure_Pa": state.pressure_Pa,
            "ledger.time_s": state.ledger.time_s,
            "ledger.cost": state.ledger.cost,
            "ledger.risk": state.ledger.risk,
            "ledger.sample_consumed_L": state.ledger.sample_consumed_L,
        }
        return [
            CheckResult(
                f"nonnegative:{key}",
                isfinite(value) and value >= -self.tolerance,
                f"{key}={value}",
                value=value,
                tolerance=self.tolerance,
            )
            for key, value in values.items()
        ]

    def _check_units(self, state: WorldState) -> list[CheckResult]:
        del state
        checks: list[CheckResult] = []
        for key, unit in self.required_state_units.items():
            try:
                canonical_unit(unit)
                passed = True
            except ValueError:
                passed = False
            checks.append(CheckResult(f"unit:{key}", passed, unit))
        return checks

    def _check_vessel_bounds(self, state: WorldState) -> list[CheckResult]:
        return [
            CheckResult(
                "vessel_volume_bound",
                state.volume_L <= self.vessel.max_volume_L + self.tolerance,
                f"volume={state.volume_L}",
                state.volume_L,
                self.tolerance,
            ),
            CheckResult(
                "vessel_temperature_bound",
                state.temperature_K <= self.vessel.max_temperature_K + self.tolerance,
                f"temperature_K={state.temperature_K}",
                state.temperature_K,
                self.tolerance,
            ),
            CheckResult(
                "vessel_pressure_bound",
                state.pressure_Pa <= self.vessel.max_pressure_Pa + self.tolerance,
                f"pressure_Pa={state.pressure_Pa}",
                state.pressure_Pa,
                self.tolerance,
            ),
        ]

    def _check_typed_ledgers(self, state: WorldState) -> list[CheckResult]:
        checks: list[CheckResult] = [
            CheckResult(
                "metadata_no_primary_phase_ledger",
                "phase_ledger" not in state.metadata,
                "Phase material state must live in typed PhaseLedger.",
            ),
            CheckResult(
                "metadata_no_primary_reactor_settings",
                self.primary_reactor_metadata_keys.isdisjoint(state.metadata),
                "Batch-reactor operation settings must live in typed EquipmentLedger.",
            ),
            CheckResult(
                "metadata_no_primary_phase_status",
                self.primary_phase_metadata_keys.isdisjoint(state.metadata),
                "Phase-system readiness, settled status, and selection must "
                "live in typed PhaseLedger.",
            ),
            CheckResult(
                "metadata_no_primary_instrument_status",
                self.primary_instrument_metadata_keys.isdisjoint(state.metadata),
                "Instrument completion state must live in typed EquipmentLedger.",
            ),
            CheckResult(
                "metadata_no_primary_crystallizer_seed_status",
                self.primary_crystallizer_metadata_keys.isdisjoint(state.metadata),
                "Crystallizer seed status and seed mass must live in typed EquipmentLedger.",
            ),
            CheckResult(
                "metadata_no_primary_crystallization_output",
                self.primary_crystallization_output_metadata_keys.isdisjoint(state.metadata),
                "Crystallized material amounts must live in typed PhaseLedger.",
            )
        ]
        if state.phases is not None:
            for phase_id, phase in state.phases.phases.items():
                checks.append(
                    CheckResult(
                        f"phase_volume_nonnegative:{phase_id}",
                        isfinite(phase.volume_L) and phase.volume_L >= -self.tolerance,
                        f"volume_L={phase.volume_L}",
                        phase.volume_L,
                        self.tolerance,
                    )
                )
                for species_id, amount in phase.species_amounts_mol.items():
                    checks.append(
                        CheckResult(
                            f"phase_amount_nonnegative:{phase_id}:{species_id}",
                            isfinite(amount) and amount >= -self.tolerance,
                            f"amount={amount}",
                            amount,
                            self.tolerance,
                        )
                    )
                if state.vessels is not None:
                    checks.append(
                        CheckResult(
                            f"phase_attached_vessel_exists:{phase_id}",
                            phase.vessel_id in state.vessels.vessels,
                            f"vessel_id={phase.vessel_id}",
                        )
                    )
        if state.vessels is not None:
            known_phases = set(state.phases.phases) if state.phases is not None else set()
            for vessel_id, vessel in state.vessels.vessels.items():
                missing = sorted(set(vessel.phase_ids) - known_phases)
                checks.append(
                    CheckResult(
                        f"vessel_phase_reverse_index:{vessel_id}",
                        not missing,
                        "" if not missing else f"missing phase ids: {missing}",
                    )
                )
        if state.equipment is not None and state.vessels is not None:
            for equipment_id, equipment in state.equipment.equipment.items():
                checks.append(
                    CheckResult(
                        f"equipment_attached_vessel_exists:{equipment_id}",
                        equipment.attached_vessel_id in state.vessels.vessels,
                        f"attached_vessel_id={equipment.attached_vessel_id}",
                    )
                )
        return checks

    def _check_risk_range(self, state: WorldState) -> CheckResult:
        return CheckResult(
            "risk_range",
            0.0 <= state.ledger.risk <= 1.0,
            f"risk={state.ledger.risk}",
            state.ledger.risk,
            self.tolerance,
        )
