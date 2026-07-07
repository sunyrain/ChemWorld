"""Centralized operation validation for ChemWorld environments and wrappers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.action_codec import ActionCodec
from chemworld.foundation import PhysicalConstitution, WorldState
from chemworld.schemas import validate_action_schema
from chemworld.world.operations import OPERATION_TYPES


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_type": self.operation_type,
            "valid": self.is_valid,
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
        operation_types: tuple[str, ...] = OPERATION_TYPES,
        action_codec: ActionCodec | None = None,
    ) -> None:
        self.constitution = constitution
        self.allowed_operations = allowed_operations
        self.allowed_instruments = allowed_instruments
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
        canonical = self.action_codec.canonicalize(action)
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
            payload = self._default_payload(operation_type)
            checks = self._preconditions(
                operation_type,
                payload,
                state,
                check_payload=False,
            )
            if all(checks.values()):
                valid.append(operation_type)
        return tuple(valid)

    def action_mask(self, state: WorldState) -> tuple[bool, ...]:
        valid = set(self.valid_operations(state))
        return tuple(operation_type in valid for operation_type in self.operation_types)

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
        if operation_type == "measure" and self.allowed_instruments is not None:
            preconditions["instrument_allowed_by_task"] = (
                str(payload.get("instrument", "hplc")) in self.allowed_instruments
            )
        if check_payload:
            preconditions.update(self._payload_checks(operation_type, payload, state))
        return preconditions

    def _default_payload(self, operation_type: str) -> dict[str, Any]:
        payload: dict[str, Any] = {"operation": operation_type}
        if operation_type == "measure":
            instrument_priority = ("hplc", "uvvis", "gc", "final_assay")
            payload["instrument"] = next(
                (
                    instrument
                    for instrument in instrument_priority
                    if self.allowed_instruments is None
                    or instrument in self.allowed_instruments
                ),
                "hplc",
            )
        if operation_type == "add_phase":
            payload["phase"] = "aqueous"
        if operation_type == "separate_phase":
            payload["target_phase"] = "organic"
        return payload

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
            "set_potential": ("potential_V", "current_mA"),
            "electrolyze": ("duration_s",),
            "measure": ("instrument",),
        }.get(operation_type, ())
        for field in required_fields:
            checks[f"payload_has:{field}"] = field in payload

        if operation_type == "add_reagent" and "amount_mol" in payload:
            checks["payload_bounds:amount_mol"] = self._in_range(
                payload,
                "amount_mol",
                0.0,
                0.040,
            )
        if (
            operation_type in {"add_solvent", "add_phase", "add_extractant"}
            and "volume_L" in payload
        ):
            added_volume = self._float(payload.get("volume_L"))
            checks["payload_bounds:volume_L"] = self._in_range(
                payload,
                "volume_L",
                0.0,
                0.080,
            )
            checks["payload_bounds:total_volume_L"] = (
                added_volume is not None
                and state.volume_L + added_volume <= self.constitution.vessel.max_volume_L
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
            checks["payload_bounds:target_temperature_K"] = self._in_range(
                payload,
                "target_temperature_K",
                250.0,
                self.constitution.vessel.max_temperature_K,
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
            checks["payload_bounds:duration_s"] = self._in_range(
                payload,
                "duration_s",
                0.0,
                14_400.0,
                inclusive_low=True,
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
            checks["payload_bounds:wash_volume_L"] = self._in_range(
                payload,
                "wash_volume_L",
                0.0,
                0.040,
                inclusive_low=True,
            )
        if operation_type == "transfer" and "transfer_fraction" in payload:
            checks["payload_bounds:transfer_fraction"] = self._in_range(
                payload,
                "transfer_fraction",
                0.0,
                1.0,
                inclusive_low=True,
            )
        if operation_type == "collect_fraction" and "transfer_fraction" in payload:
            checks["payload_bounds:transfer_fraction"] = self._in_range(
                payload,
                "transfer_fraction",
                0.0,
                1.0,
                inclusive_low=True,
            )
        if operation_type == "seed_crystals" and "seed_mass_g" in payload:
            checks["payload_bounds:seed_mass_g"] = self._in_range(
                payload,
                "seed_mass_g",
                0.0,
                1.0,
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
            if "potential_V" in payload:
                checks["payload_bounds:potential_V"] = self._in_range(
                    payload,
                    "potential_V",
                    -3.0,
                    3.0,
                    inclusive_low=True,
                )
            if "current_mA" in payload:
                checks["payload_bounds:current_mA"] = self._in_range(
                    payload,
                    "current_mA",
                    0.0,
                    500.0,
                    inclusive_low=True,
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
