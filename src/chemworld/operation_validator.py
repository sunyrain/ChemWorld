"""Centralized operation validation for ChemWorld environments and wrappers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.action_codec import ActionCodec
from chemworld.foundation import (
    PhysicalConstitution,
    WorldState,
    equipment_settings,
    instrument_equipment_id,
    selected_phase_id,
)
from chemworld.physchem.crystallization_units import (
    DEFAULT_MAXIMUM_COOLING_RATE_K_S,
)
from chemworld.schemas import validate_action_schema
from chemworld.world.operations import (
    OPERATION_FIELD_BOUNDS,
    OPERATION_FIELD_CHOICES,
    OPERATION_TYPES,
)

OPERATION_AFFORDANCE_STATE_MACHINE_VERSION = "chemworld-operation-affordance-state-machine-0.6"


@dataclass(frozen=True)
class OperationValidation:
    operation_type: str
    is_valid: bool
    preconditions: dict[str, bool]
    invalid_reasons: tuple[str, ...]
    valid_operations: tuple[str, ...]
    action_mask: tuple[bool, ...]
    cost_penalty: float
    safety_flags: dict[str, bool]

    @property
    def dispatchable_to_runtime(self) -> bool:
        """Return whether the action can enter transactional runtime handling.

        Schema, task-policy, instrument-policy, and payload-shape failures are
        rejected before runtime dispatch. Stateful physical precondition
        failures are still dispatchable so the transactional runtime can record
        a rollback event and process-only penalty.
        """

        blocking_reasons = {
            "action_schema_valid",
            "operation_allowed_by_task",
            "instrument_allowed_by_task",
        }
        return self.preconditions.get("action_schema_valid", True) and not any(
            reason in blocking_reasons or reason.startswith("payload_")
            for reason in self.invalid_reasons
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_type": self.operation_type,
            "valid": self.is_valid,
            "dispatchable_to_runtime": self.dispatchable_to_runtime,
            "preconditions": self.preconditions,
            "invalid_reasons": list(self.invalid_reasons),
            "valid_operations": list(self.valid_operations),
            "action_mask": list(self.action_mask),
            "cost_penalty": self.cost_penalty,
            "safety_flags": self.safety_flags,
        }


class OperationValidator:
    """Single source of truth for task policy and physical preconditions."""

    def __init__(
        self,
        *,
        constitution: PhysicalConstitution,
        allowed_operations: set[str],
        allowed_instruments: set[str] | None = None,
        target_species: tuple[str, ...] = (),
        reagent_charge_molar_multiplier: float = 1.0,
        task_id: str | None = None,
        operation_types: tuple[str, ...] = OPERATION_TYPES,
        action_codec: ActionCodec | None = None,
    ) -> None:
        self.constitution = constitution
        self.allowed_operations = allowed_operations
        self.allowed_instruments = allowed_instruments
        self.target_species = target_species
        if reagent_charge_molar_multiplier <= 0.0:
            raise ValueError("reagent_charge_molar_multiplier must be positive")
        self.reagent_charge_molar_multiplier = float(reagent_charge_molar_multiplier)
        self.task_id = task_id
        self.operation_types = operation_types
        self.action_codec = action_codec or ActionCodec()

    def validate(self, action: dict[str, Any], state: WorldState) -> OperationValidation:
        schema_result = validate_action_schema(action)
        if not schema_result.valid:
            operation_type = str(action.get("operation", "invalid"))
            valid_operations = self.valid_operations(state)
            return OperationValidation(
                operation_type=operation_type,
                is_valid=False,
                preconditions={"action_schema_valid": False},
                invalid_reasons=tuple(schema_result.errors),
                valid_operations=valid_operations,
                action_mask=tuple(
                    operation in valid_operations for operation in self.operation_types
                ),
                cost_penalty=0.20,
                safety_flags={
                    "operation_allowed_by_task": False,
                    "precondition_failed": True,
                    "action_schema_valid": False,
                },
            )
        try:
            canonical = self.action_codec.canonicalize(action)
        except (IndexError, TypeError, ValueError, OverflowError):
            # Canonicalization is part of public input validation.  A user or
            # agent supplied material label must never escape ``env.step`` as a
            # backend exception: reject it transactionally like any other
            # malformed payload, without exposing codec internals.
            operation_type = str(action.get("operation", "invalid"))
            valid_operations = self.valid_operations(state)
            return OperationValidation(
                operation_type=operation_type,
                is_valid=False,
                preconditions={"action_schema_valid": False},
                invalid_reasons=("payload_canonicalization_failed",),
                valid_operations=valid_operations,
                action_mask=tuple(
                    operation in valid_operations for operation in self.operation_types
                ),
                cost_penalty=0.20,
                safety_flags={
                    "operation_allowed_by_task": False,
                    "precondition_failed": True,
                    "action_schema_valid": False,
                },
            )
        operation_type = str(canonical["operation"])
        preconditions = self._preconditions(operation_type, canonical, state)
        preconditions["action_schema_valid"] = True
        valid_operations = self.valid_operations(state)
        action_mask = tuple(operation in valid_operations for operation in self.operation_types)
        invalid_reasons = tuple(key for key, passed in preconditions.items() if not passed)
        cost_penalty = min(1.0, 0.10 * len(invalid_reasons))
        return OperationValidation(
            operation_type=operation_type,
            is_valid=not invalid_reasons,
            preconditions=preconditions,
            invalid_reasons=invalid_reasons,
            valid_operations=valid_operations,
            action_mask=action_mask,
            cost_penalty=cost_penalty,
            safety_flags={
                "operation_allowed_by_task": preconditions["operation_allowed_by_task"],
                "precondition_failed": bool(invalid_reasons),
            },
        )

    def valid_operations(self, state: WorldState) -> tuple[str, ...]:
        valid: list[str] = []
        for operation_type in self.operation_types:
            affordance = self.operation_affordance(operation_type, state)
            if affordance.is_valid:
                valid.append(operation_type)
        return tuple(valid)

    def action_mask(self, state: WorldState) -> tuple[bool, ...]:
        valid = set(self.valid_operations(state))
        return tuple(operation_type in valid for operation_type in self.operation_types)

    def public_field_bounds(
        self,
        operation_type: str,
        field: str,
        state: WorldState,
        *,
        low: float,
        high: float,
    ) -> tuple[float, float]:
        """Narrow a static schema to its current public feasibility domain."""

        dynamic_low = low
        dynamic_high = high
        if operation_type == "add_reagent" and field == "amount_mol":
            dynamic_high = min(
                dynamic_high,
                self._maximum_safe_reagent_amount_mol(state),
            )
        elif (
            operation_type in {"add_solvent", "add_phase", "add_extractant"}
            and field == "volume_L"
        ):
            dynamic_low = max(
                dynamic_low,
                self._minimum_safe_liquid_addition_volume_l(state),
            )
            dynamic_high = min(
                dynamic_high,
                max(self._max_volume_l(state) - state.volume_L, 0.0),
            )
        elif operation_type == "sample" and field == "sample_volume_L":
            dynamic_high = min(dynamic_high, max(state.volume_L, 0.0))
        elif (
            operation_type in {"heat", "cool_crystallize", "evaporate", "distill", "run_flow"}
            and field == "target_temperature_K"
        ):
            dynamic_high = min(dynamic_high, self._max_temperature_k(state))
            if operation_type == "cool_crystallize":
                # The crystallization kernel accepts only a cooling or
                # isothermal ramp.  Publishing the static 330 K ceiling after
                # the vessel is already colder exposes actions that can only
                # fail inside the runtime.
                dynamic_high = min(dynamic_high, state.temperature_K)
        elif operation_type == "run_flow" and field == "duration_s":
            flow_settings = equipment_settings(state.equipment, "flow_reactor")
            minimum_duration = self._float(flow_settings.get("minimum_run_duration_s"))
            if minimum_duration is not None:
                dynamic_low = max(dynamic_low, minimum_duration)
        elif operation_type == "set_potential" and field == "potential_V":
            # The public action uses the runtime's default 2.5 V cell window.
            # Maintainer-only extended payloads may supply a wider explicit
            # window, but an advertised public action must configure a cell
            # that can subsequently be executed.
            dynamic_low = max(dynamic_low, -2.5)
            dynamic_high = min(dynamic_high, 2.5)
        if dynamic_low > dynamic_high:
            # Equal bounds encode an empty interval because numeric payload
            # lower bounds are exclusive throughout the public validator.
            return dynamic_high, dynamic_high
        return dynamic_low, dynamic_high

    def public_field_choices(
        self,
        operation_type: str,
        field: str,
        state: WorldState,
        *,
        choices: tuple[Any, ...],
    ) -> tuple[Any, ...]:
        """Narrow categorical choices to physically persistent task state."""

        if operation_type == "measure" and field == "instrument":
            choices = tuple(
                choice
                for choice in choices
                if (choice == "final_assay") == state.terminated
            )
        if (
            self.task_id == "electrochemical-conversion"
            and operation_type == "add_solvent"
            and field == "solvent"
        ):
            return tuple(choice for choice in choices if choice == 0)
        if operation_type == "set_potential" and field == "electrolyte_profile":
            settings = equipment_settings(state.equipment, "electrochemical_cell")
            locked = settings.get("electrolyte_profile")
            if isinstance(locked, int) and not isinstance(locked, bool):
                return tuple(choice for choice in choices if choice == locked)
        if (
            self.task_id == "electrochemical-conversion"
            and operation_type == "measure"
            and field == "instrument"
        ):
            required = self._electrochemical_required_instruments(state)
            if required:
                return tuple(choice for choice in choices if choice in required)
        return choices

    def operation_affordance(
        self,
        operation_type: str,
        state: WorldState,
    ) -> OperationValidation:
        payload = self._default_payload(operation_type, state)
        preconditions = self._preconditions(
            operation_type,
            payload,
            state,
            check_payload=False,
        )
        invalid_reasons = tuple(key for key, passed in preconditions.items() if not passed)
        action_mask = tuple(
            self._operation_preconditions_pass(candidate, state)
            for candidate in self.operation_types
        )
        valid_operations = tuple(
            operation
            for operation, is_valid in zip(self.operation_types, action_mask, strict=True)
            if is_valid
        )
        return OperationValidation(
            operation_type=operation_type,
            is_valid=not invalid_reasons,
            preconditions=preconditions,
            invalid_reasons=invalid_reasons,
            valid_operations=valid_operations,
            action_mask=action_mask,
            cost_penalty=min(1.0, 0.10 * len(invalid_reasons)),
            safety_flags={
                "operation_allowed_by_task": preconditions.get(
                    "operation_allowed_by_task",
                    False,
                ),
                "precondition_failed": bool(invalid_reasons),
            },
        )

    def _operation_preconditions_pass(self, operation_type: str, state: WorldState) -> bool:
        payload = self._default_payload(operation_type, state)
        checks = self._preconditions(
            operation_type,
            payload,
            state,
            check_payload=False,
        )
        return all(checks.values())

    def _preconditions(
        self,
        operation_type: str,
        payload: dict[str, Any],
        state: WorldState,
        *,
        check_payload: bool = True,
    ) -> dict[str, bool]:
        preconditions = self.constitution.check_preconditions(operation_type, state, payload)
        preconditions["operation_allowed_by_task"] = operation_type in self.allowed_operations
        crystallizer_settings = equipment_settings(state.equipment, "crystallizer")
        filter_settings = equipment_settings(state.equipment, "crystal_filter")
        crystals_filtered = bool(filter_settings.get("crystals_filtered", False))
        crystal_seeded = bool(crystallizer_settings.get("crystal_seeded", False))
        crystallization_completed = bool(crystallizer_settings.get("execution_history", ()))
        flagship_crystallization = self.task_id == "reaction-to-crystallization"
        current_nonfinal_assay = self._has_current_nonfinal_assay(state)
        if flagship_crystallization and operation_type == "seed_crystals" and not crystal_seeded:
            process_metrics = {} if state.process is None else state.process.metrics
            preconditions["seed_crystals_requires_reaction_advance"] = (
                float(process_metrics.get("reaction_advance_count", 0.0)) > 0.0
            )
            preconditions["seed_crystals_requires_current_reaction_assay"] = (
                current_nonfinal_assay
            )
        if (
            flagship_crystallization
            and crystal_seeded
            and not crystallization_completed
            and not crystals_filtered
        ):
            preconditions["seeded_crystallization_requires_seed_assay_or_cooling"] = (
                operation_type in {"seed_crystals", "measure", "cool_crystallize"}
            )
        if crystallization_completed and not crystals_filtered:
            preconditions["completed_crystallization_requires_assay_or_filter"] = (
                operation_type in {"measure", "filter_crystals"}
            )
            if flagship_crystallization and operation_type == "filter_crystals":
                preconditions["filter_crystals_requires_current_slurry_assay"] = (
                    current_nonfinal_assay
                )
        if crystals_filtered:
            preconditions["isolated_crystals_require_assay_or_termination"] = operation_type in {
                "measure",
                "terminate",
            }
        if operation_type in {"add_solvent", "add_phase", "add_extractant"}:
            maximum_addition = max(self._max_volume_l(state) - state.volume_L, 0.0)
            preconditions["addition_capacity_available"] = maximum_addition > max(
                self._minimum_safe_liquid_addition_volume_l(state),
                self.constitution.tolerance,
            )
        if operation_type == "add_reagent":
            preconditions["reagent_pressure_capacity_available"] = (
                self._maximum_safe_reagent_amount_mol(state) > self.constitution.tolerance
            )
        if (
            self.task_id == "electrochemical-conversion"
            and operation_type == "add_solvent"
            and "solvent" in payload
        ):
            preconditions["electrochemical_task_requires_aqueous_solvent"] = (
                payload.get("solvent") == 0
            )
        if operation_type == "terminate":
            required = self._final_assay_sample_volume()
            preconditions["final_assay_sample_available"] = (
                required == 0.0 or state.volume_L + self.constitution.tolerance >= required
            )
            if flagship_crystallization:
                preconditions["flagship_crystallization_requires_isolated_crystals"] = (
                    crystals_filtered
                )
            if self.task_id == "electrochemical-conversion":
                preconditions["flagship_electrochemistry_requires_outcome_assay"] = (
                    self._electrochemical_outcome_assay_complete(state)
                )
        if self.task_id == "electrochemical-conversion" and not state.terminated:
            preconditions["electrochemical_flagship_phase_allows_operation"] = (
                self._electrochemical_operation_allowed(operation_type, state)
            )
            if operation_type == "measure" and "instrument" in payload:
                required_instruments = self._electrochemical_required_instruments(state)
                preconditions["electrochemical_instrument_matches_workflow_phase"] = (
                    not required_instruments
                    or str(payload.get("instrument")) in required_instruments
                )
        if operation_type == "cool_crystallize":
            seed_target_mol = float(crystallizer_settings.get("seed_target_mol", 0.0))
            primary_target = self.target_species[0] if self.target_species else None
            dissolved_target_mol = (
                float(state.species_amounts.get(primary_target, 0.0)) - seed_target_mol
                if primary_target is not None
                else 0.0
            )
            preconditions["cool_crystallize_target_feed_available"] = (
                dissolved_target_mol > self.constitution.tolerance
            )
        if operation_type == "measure" and self.allowed_instruments is not None:
            preconditions["instrument_allowed_by_task"] = (
                str(payload.get("instrument", "hplc")) in self.allowed_instruments
            )
        if check_payload:
            preconditions.update(self._payload_checks(operation_type, payload, state))
        return preconditions

    def _has_current_nonfinal_assay(self, state: WorldState) -> bool:
        """Return whether a public process assay was taken at the current process time."""

        instrument_ids = (
            set(self.constitution.instruments)
            if self.allowed_instruments is None
            else self.allowed_instruments
        )
        for instrument_id in instrument_ids:
            if instrument_id == "final_assay":
                continue
            settings = equipment_settings(
                state.equipment,
                instrument_equipment_id(instrument_id),
            )
            if int(settings.get("use_count", 0)) <= 0:
                continue
            last_time_s = self._float(settings.get("last_time_s"))
            if last_time_s is not None and abs(last_time_s - state.ledger.time_s) <= max(
                self.constitution.tolerance,
                1.0e-9,
            ):
                return True
        return False

    def _electrochemical_operation_allowed(
        self,
        operation_type: str,
        state: WorldState,
    ) -> bool:
        cell = equipment_settings(state.equipment, "electrochemical_cell")
        setpoint_count = len(tuple(cell.get("setpoint_history", ())))
        electrolysis_count = len(tuple(cell.get("electrolysis_history", ())))
        if setpoint_count == 0:
            return operation_type in {"add_solvent", "add_reagent", "set_potential"}
        if electrolysis_count == 0:
            return operation_type == "electrolyze"
        if electrolysis_count == 1 and setpoint_count == 1:
            if self._electrochemical_probe_diagnostics_complete(state):
                return operation_type == "set_potential"
            return operation_type == "measure"
        if electrolysis_count == 1:
            return operation_type == "electrolyze"
        if self._electrochemical_outcome_assay_complete(state):
            return operation_type == "terminate"
        return operation_type == "measure"

    def _electrochemical_required_instruments(self, state: WorldState) -> tuple[str, ...]:
        cell = equipment_settings(state.equipment, "electrochemical_cell")
        electrolysis_history = tuple(cell.get("electrolysis_history", ()))
        if not electrolysis_history:
            return ()
        if len(electrolysis_history) == 1:
            first_end = self._float(dict(electrolysis_history[0]).get("end_time_s"))
            if first_end is None:
                return ()
            missing = [
                instrument_id
                for instrument_id in ("ph_meter", "uvvis")
                if not self._instrument_used_at_or_after(
                    state,
                    instrument_id,
                    first_end,
                )
            ]
            return tuple(missing)
        last_end = self._float(dict(electrolysis_history[-1]).get("end_time_s"))
        if last_end is None or self._instrument_used_at_or_after(state, "uvvis", last_end):
            return ()
        return ("uvvis",)

    def _electrochemical_probe_diagnostics_complete(self, state: WorldState) -> bool:
        return not self._electrochemical_required_instruments(state)

    def _electrochemical_outcome_assay_complete(self, state: WorldState) -> bool:
        cell = equipment_settings(state.equipment, "electrochemical_cell")
        electrolysis_history = tuple(cell.get("electrolysis_history", ()))
        if len(electrolysis_history) < 2:
            return False
        last_end = self._float(dict(electrolysis_history[-1]).get("end_time_s"))
        return last_end is not None and self._instrument_used_at_or_after(
            state,
            "uvvis",
            last_end,
        )

    def _instrument_used_at_or_after(
        self,
        state: WorldState,
        instrument_id: str,
        time_s: float,
    ) -> bool:
        settings = equipment_settings(
            state.equipment,
            instrument_equipment_id(instrument_id),
        )
        last_time_s = self._float(settings.get("last_time_s"))
        return (
            int(settings.get("use_count", 0)) > 0
            and last_time_s is not None
            and last_time_s + max(self.constitution.tolerance, 1.0e-9) >= time_s
        )

    def _default_payload(
        self,
        operation_type: str,
        state: WorldState,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"operation": operation_type}
        if operation_type == "measure":
            payload["instrument"] = self._default_measurement_instrument(state)
        if operation_type == "add_phase":
            payload["phase"] = "aqueous"
        if operation_type == "separate_phase":
            payload["target_phase"] = "organic"
        return payload

    def _default_measurement_instrument(self, state: WorldState) -> str:
        instrument_priority = ("hplc", "uvvis", "gc", "ph_meter", "final_assay")
        candidates = (*instrument_priority, *sorted(self.constitution.instruments))
        permitted = tuple(
            instrument_id
            for instrument_id in dict.fromkeys(candidates)
            if self.allowed_instruments is None or instrument_id in self.allowed_instruments
        )
        for instrument_id in permitted:
            instrument = self.constitution.instruments.get(instrument_id)
            if instrument is None:
                continue
            if state.terminated != bool(instrument.requires_terminated):
                continue
            if state.volume_L + self.constitution.tolerance < instrument.sample_volume_L:
                continue
            return instrument_id
        return permitted[0] if permitted else "hplc"

    def _payload_checks(
        self,
        operation_type: str,
        payload: dict[str, Any],
        state: WorldState,
    ) -> dict[str, bool]:
        checks: dict[str, bool] = {}
        required_fields = {
            "add_reagent": ("amount_mol",),
            "add_solvent": ("volume_L", "solvent"),
            "add_catalyst": ("catalyst_amount_mol", "catalyst"),
            "heat": ("target_temperature_K", "duration_s", "stirring_speed_rpm"),
            "wait": ("duration_s",),
            "sample": ("sample_volume_L",),
            "add_phase": ("phase", "volume_L"),
            "add_extractant": ("extractant", "volume_L"),
            "mix": ("duration_s", "stirring_speed_rpm"),
            "settle": ("duration_s",),
            "separate_phase": ("target_phase",),
            "wash": ("wash_volume_L",),
            "concentrate": ("duration_s",),
            "transfer": ("transfer_fraction",),
            "seed_crystals": ("seed_mass_g",),
            "cool_crystallize": ("target_temperature_K", "duration_s"),
            "evaporate": ("target_temperature_K", "duration_s"),
            "distill": ("target_temperature_K", "duration_s", "reflux_ratio"),
            "collect_fraction": ("transfer_fraction",),
            "set_flow_rate": ("flow_rate_mL_min", "residence_time_s"),
            "run_flow": ("target_temperature_K", "duration_s"),
            "set_potential": ("potential_V", "current_mA", "electrolyte_profile"),
            "electrolyze": ("duration_s",),
            "measure": ("instrument",),
        }.get(operation_type, ())
        for field in required_fields:
            checks[f"payload_has:{field}"] = field in payload

        for (candidate_operation, field), choices in OPERATION_FIELD_CHOICES.items():
            if operation_type == candidate_operation and field in payload:
                checks[f"payload_choice:{field}"] = payload.get(field) in choices

        lock_contract = {
            "add_solvent": ("solvent", "batch_reactor", "solvent_volume_L"),
            "add_catalyst": ("catalyst", "batch_reactor", "catalyst_amount_mol"),
            "add_extractant": (
                "extractant",
                "liquid_liquid_extractor",
                "extractant_volume_L",
            ),
        }.get(operation_type)
        if lock_contract is not None and lock_contract[0] in payload:
            locked_field, equipment_id, charged_key = lock_contract
            settings = equipment_settings(state.equipment, equipment_id)
            selected = (
                settings.get(locked_field) if float(settings.get(charged_key, 0.0)) > 0.0 else None
            )
            checks[f"payload_locked:{locked_field}"] = (
                selected is None or payload.get(locked_field) == selected
            )

        if operation_type == "add_reagent" and "amount_mol" in payload:
            low, high = self.public_field_bounds(
                operation_type,
                "amount_mol",
                state,
                low=0.0,
                high=0.040,
            )
            checks["payload_bounds:amount_mol"] = self._in_range(
                payload,
                "amount_mol",
                low,
                high,
            )
        if (
            operation_type in {"add_solvent", "add_phase", "add_extractant"}
            and "volume_L" in payload
        ):
            added_volume = self._float(payload.get("volume_L"))
            low, high = OPERATION_FIELD_BOUNDS.get(
                (operation_type, "volume_L"),
                (0.0, 0.080),
            )
            low, high = self.public_field_bounds(
                operation_type,
                "volume_L",
                state,
                low=low,
                high=high,
            )
            checks["payload_bounds:volume_L"] = self._in_range(
                payload,
                "volume_L",
                low,
                high,
            )
            checks["payload_bounds:total_volume_L"] = (
                added_volume is not None
                and state.volume_L + added_volume <= self._max_volume_l(state)
            )
        if operation_type == "add_catalyst" and "catalyst_amount_mol" in payload:
            checks["payload_bounds:catalyst_amount_mol"] = self._in_range(
                payload,
                "catalyst_amount_mol",
                0.0,
                0.005,
            )
        if (
            operation_type in {"heat", "cool_crystallize", "evaporate", "distill", "run_flow"}
            and "target_temperature_K" in payload
        ):
            low, high = OPERATION_FIELD_BOUNDS.get(
                (operation_type, "target_temperature_K"),
                (250.0, self._max_temperature_k(state)),
            )
            low, high = self.public_field_bounds(
                operation_type,
                "target_temperature_K",
                state,
                low=low,
                high=high,
            )
            checks["payload_bounds:target_temperature_K"] = self._in_range(
                payload,
                "target_temperature_K",
                low,
                high,
                inclusive_low=True,
            )
        if (
            operation_type
            in {
                "heat",
                "wait",
                "mix",
                "settle",
                "concentrate",
                "cool_crystallize",
                "evaporate",
                "distill",
                "run_flow",
                "electrolyze",
            }
            and "duration_s" in payload
        ):
            low, high = OPERATION_FIELD_BOUNDS.get(
                (operation_type, "duration_s"),
                (0.0, 14_400.0),
            )
            low, high = self.public_field_bounds(
                operation_type,
                "duration_s",
                state,
                low=low,
                high=high,
            )
            checks["payload_bounds:duration_s"] = self._in_range(
                payload,
                "duration_s",
                low,
                high,
                inclusive_low=True,
            )
        if (
            operation_type == "cool_crystallize"
            and {
                "target_temperature_K",
                "duration_s",
            }
            <= payload.keys()
        ):
            target_temperature = self._float(payload.get("target_temperature_K"))
            duration = self._float(payload.get("duration_s"))
            checks["payload_coupling:maximum_cooling_rate_K_s"] = (
                target_temperature is not None
                and duration is not None
                and duration > 0.0
                and max(state.temperature_K - target_temperature, 0.0) / duration
                <= DEFAULT_MAXIMUM_COOLING_RATE_K_S + self.constitution.tolerance
            )
        if operation_type in {"heat", "wait", "mix"} and "stirring_speed_rpm" in payload:
            checks["payload_bounds:stirring_speed_rpm"] = self._in_range(
                payload,
                "stirring_speed_rpm",
                100.0,
                1200.0,
                inclusive_low=True,
            )
        if operation_type == "sample" and "sample_volume_L" in payload:
            sample_volume = self._float(payload.get("sample_volume_L"))
            checks["payload_bounds:sample_volume_L"] = (
                sample_volume is not None and 0.0 < sample_volume <= state.volume_L
            )
        if operation_type == "wash" and "wash_volume_L" in payload:
            low, high = OPERATION_FIELD_BOUNDS[("wash", "wash_volume_L")]
            checks["payload_bounds:wash_volume_L"] = self._in_range(
                payload,
                "wash_volume_L",
                low,
                high,
                inclusive_low=True,
            )
        if operation_type == "transfer" and "transfer_fraction" in payload:
            low, high = OPERATION_FIELD_BOUNDS[("transfer", "transfer_fraction")]
            checks["payload_bounds:transfer_fraction"] = self._in_range(
                payload,
                "transfer_fraction",
                low,
                high,
                inclusive_low=True,
            )
        if operation_type == "collect_fraction" and "transfer_fraction" in payload:
            low, high = OPERATION_FIELD_BOUNDS[
                (
                    "collect_fraction",
                    "transfer_fraction",
                )
            ]
            checks["payload_bounds:transfer_fraction"] = self._in_range(
                payload,
                "transfer_fraction",
                low,
                high,
                inclusive_low=True,
            )
        if operation_type == "seed_crystals" and "seed_mass_g" in payload:
            low, high = OPERATION_FIELD_BOUNDS[("seed_crystals", "seed_mass_g")]
            checks["payload_bounds:seed_mass_g"] = self._in_range(
                payload,
                "seed_mass_g",
                low,
                high,
                inclusive_low=True,
            )
        if operation_type == "distill" and "reflux_ratio" in payload:
            checks["payload_bounds:reflux_ratio"] = self._in_range(
                payload,
                "reflux_ratio",
                0.0,
                10.0,
                inclusive_low=True,
            )
        if operation_type == "set_flow_rate":
            if "flow_rate_mL_min" in payload:
                checks["payload_bounds:flow_rate_mL_min"] = self._in_range(
                    payload,
                    "flow_rate_mL_min",
                    0.01,
                    20.0,
                    inclusive_low=True,
                )
            if "residence_time_s" in payload:
                checks["payload_bounds:residence_time_s"] = self._in_range(
                    payload,
                    "residence_time_s",
                    1.0,
                    7200.0,
                    inclusive_low=True,
                )
        if operation_type == "set_potential":
            if "electrolyte_profile" in payload:
                profile = payload.get("electrolyte_profile")
                checks["payload_choice:electrolyte_profile"] = (
                    isinstance(profile, int)
                    and not isinstance(profile, bool)
                    and 0 <= profile < 4
                )
                settings = equipment_settings(state.equipment, "electrochemical_cell")
                locked_profile = settings.get("electrolyte_profile")
                checks["payload_locked:electrolyte_profile"] = (
                    locked_profile is None or profile == locked_profile
                )
            if "potential_V" in payload:
                checks["payload_bounds:potential_V"] = self._in_range(
                    payload,
                    "potential_V",
                    -3.0,
                    3.0,
                    inclusive_low=True,
                )
            if "current_mA" in payload:
                low, high = OPERATION_FIELD_BOUNDS[("set_potential", "current_mA")]
                checks["payload_bounds:current_mA"] = self._in_range(
                    payload,
                    "current_mA",
                    low,
                    high,
                    inclusive_low=True,
                )
            if "electrolyte_conductivity_S_m" in payload:
                checks["payload_bounds:electrolyte_conductivity_S_m"] = self._in_range(
                    payload,
                    "electrolyte_conductivity_S_m",
                    0.05,
                    100.0,
                    inclusive_low=True,
                )
            if "electrode_gap_m" in payload:
                checks["payload_bounds:electrode_gap_m"] = self._in_range(
                    payload,
                    "electrode_gap_m",
                    1.0e-5,
                    0.05,
                    inclusive_low=True,
                )
            if "electrode_area_m2" in payload:
                checks["payload_bounds:electrode_area_m2"] = self._in_range(
                    payload,
                    "electrode_area_m2",
                    1.0e-5,
                    0.20,
                    inclusive_low=True,
                )
            if "contact_resistance_ohm" in payload:
                checks["payload_bounds:contact_resistance_ohm"] = self._in_range(
                    payload,
                    "contact_resistance_ohm",
                    0.0,
                    100.0,
                    inclusive_low=True,
                )
            if "voltage_window_V" in payload:
                checks["payload_bounds:voltage_window_V"] = self._in_range(
                    payload,
                    "voltage_window_V",
                    0.1,
                    10.0,
                    inclusive_low=True,
                )
            if "potential_V" in payload:
                potential = self._float(payload.get("potential_V"))
                voltage_window = self._float(payload.get("voltage_window_V", 2.5))
                checks["payload_coupling:potential_within_voltage_window"] = (
                    potential is not None
                    and voltage_window is not None
                    and abs(potential) <= voltage_window
                )
        return checks

    @staticmethod
    def _float(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _in_range(
        self,
        payload: dict[str, Any],
        key: str,
        low: float,
        high: float,
        *,
        inclusive_low: bool = False,
    ) -> bool:
        value = self._float(payload.get(key))
        if value is None:
            return False
        lower_ok = value >= low if inclusive_low else value > low
        return lower_ok and value <= high

    def _max_volume_l(self, state: WorldState) -> float:
        if state.vessels is not None and state.vessel_id in state.vessels.vessels:
            return state.vessels.vessels[state.vessel_id].max_volume_L
        return self.constitution.vessel.max_volume_L

    def _max_temperature_k(self, state: WorldState) -> float:
        if state.vessels is not None and state.vessel_id in state.vessels.vessels:
            return state.vessels.vessels[state.vessel_id].max_temperature_K
        return self.constitution.vessel.max_temperature_K

    def _max_pressure_pa(self, state: WorldState) -> float:
        if state.vessels is not None and state.vessel_id in state.vessels.vessels:
            return state.vessels.vessels[state.vessel_id].max_pressure_Pa
        return self.constitution.vessel.max_pressure_Pa

    def _maximum_safe_reagent_amount_mol(self, state: WorldState) -> float:
        """Invert the public pressure law to bound one reagent charge safely."""

        if state.temperature_K <= 0.0:
            return 0.0
        if state.volume_L <= 0.0:
            # The shared pressure law explicitly defines concentration as zero
            # before a liquid charge exists.  Reagent addition is therefore
            # pressure-neutral in this state; the later solvent action creates
            # the finite-volume concentration domain.
            return 0.040
        active_amounts = state.species_amounts
        active_phase_id = selected_phase_id(state.phases)
        if state.phases is not None and active_phase_id in state.phases.phases:
            active_amounts = state.phases.phases[active_phase_id].species_amounts_mol
        current_amount_mol = sum(
            float(value)
            for species_id, value in active_amounts.items()
            if not species_id.startswith("Cat")
        )
        base_pressure_pa = 101_325.0 * state.temperature_K / 298.15
        maximum_concentration_mol_l = max(
            (self._max_pressure_pa(state) / base_pressure_pa - 1.0) / 0.025,
            0.0,
        )
        remaining_amount_mol = max(
            maximum_concentration_mol_l * state.volume_L - current_amount_mol,
            0.0,
        )
        return remaining_amount_mol / self.reagent_charge_molar_multiplier

    def _minimum_safe_liquid_addition_volume_l(self, state: WorldState) -> float:
        """Invert the pressure law for a material-first liquid charge."""

        if state.temperature_K <= 0.0:
            return float("inf")
        active_amounts = state.species_amounts
        active_phase_id = selected_phase_id(state.phases)
        if state.phases is not None and active_phase_id in state.phases.phases:
            active_amounts = state.phases.phases[active_phase_id].species_amounts_mol
        current_amount_mol = sum(
            float(value)
            for species_id, value in active_amounts.items()
            if not species_id.startswith("Cat")
        )
        if current_amount_mol <= 0.0:
            return 0.0
        base_pressure_pa = 101_325.0 * state.temperature_K / 298.15
        pressure_ceiling_pa = max(self._max_pressure_pa(state) - 1.0, 0.0)
        maximum_concentration_mol_l = (
            (pressure_ceiling_pa / base_pressure_pa - 1.0) / 0.025
            if base_pressure_pa > 0.0
            else 0.0
        )
        if maximum_concentration_mol_l <= 0.0:
            return float("inf")
        required_total_volume_l = current_amount_mol / maximum_concentration_mol_l
        return max(required_total_volume_l - state.volume_L, 0.0)

    def _final_assay_sample_volume(self) -> float:
        if self.allowed_instruments is not None and "final_assay" not in self.allowed_instruments:
            return 0.0
        instrument = self.constitution.instruments.get("final_assay")
        return float("inf") if instrument is None else max(float(instrument.sample_volume_L), 0.0)
