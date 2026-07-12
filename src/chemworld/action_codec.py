"""Action abstraction layer for ChemWorld event and Gym-style actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from chemworld.world.actions import CATALYSTS, SOLVENTS
from chemworld.world.operations import (
    INSTRUMENTS,
    OPERATION_TYPES,
    instrument_name,
    operation_name,
)

PHASES = ("reactor_liquid", "aqueous", "organic")
EXTRACTANTS = SOLVENTS
GYM_ACTION_KEYS = (
    "operation",
    "amount_mol",
    "volume_L",
    "catalyst_amount_mol",
    "target_temperature_K",
    "duration_s",
    "stirring_speed_rpm",
    "sample_volume_L",
    "instrument",
    "catalyst",
    "solvent",
    "phase",
    "target_phase",
    "extractant",
    "wash_volume_L",
    "transfer_fraction",
    "seed_mass_g",
    "reflux_ratio",
    "flow_rate_mL_min",
    "residence_time_s",
    "potential_V",
    "current_mA",
)


@dataclass(frozen=True)
class ActionCodec:
    """Convert between semantic event actions and numeric Gym-style vectors."""

    operation_types: tuple[str, ...] = OPERATION_TYPES
    instruments: tuple[str, ...] = INSTRUMENTS
    catalysts: tuple[str, ...] = CATALYSTS
    solvents: tuple[str, ...] = SOLVENTS
    phases: tuple[str, ...] = PHASES
    extractants: tuple[str, ...] = EXTRACTANTS

    def canonicalize(self, action: dict[str, Any]) -> dict[str, Any]:
        """Normalize event-action JSON into canonical names and flat payload."""

        if "operation" not in action:
            raise ValueError("Event actions must include an operation field")
        canonical = dict(action)
        if isinstance(canonical.get("payload"), dict):
            payload = dict(canonical.pop("payload"))
            payload["operation"] = canonical["operation"]
            payload.update({key: value for key, value in canonical.items() if key != "operation"})
            canonical = payload
        canonical["operation"] = operation_name(canonical["operation"])
        canonical = self._apply_aliases(canonical)
        if "solvent" in canonical:
            canonical["solvent"] = self._choice_index(canonical["solvent"], self.solvents)
        if "catalyst" in canonical:
            canonical["catalyst"] = self._choice_index(
                canonical["catalyst"],
                self.catalysts,
            )
        if "instrument" in canonical:
            canonical["instrument"] = instrument_name(canonical["instrument"])
        if "phase" in canonical:
            canonical["phase"] = self.phase_name(canonical["phase"])
        if "target_phase" in canonical:
            canonical["target_phase"] = self.phase_name(canonical["target_phase"])
        if "extractant" in canonical:
            canonical["extractant"] = self.extractant_name(canonical["extractant"])
        return canonical

    def _apply_aliases(self, action: dict[str, Any]) -> dict[str, Any]:
        """Accept common user-facing names while preserving canonical output."""

        operation = str(action["operation"])
        canonical = dict(action)
        if (
            operation == "add_catalyst"
            and "catalyst_amount_mol" not in canonical
            and "amount_mol" in canonical
        ):
            canonical["catalyst_amount_mol"] = canonical["amount_mol"]
        if (
            operation
            in {"heat", "cool_crystallize", "evaporate", "distill", "run_flow"}
            and "target_temperature_K" not in canonical
            and "temperature_K" in canonical
        ):
            canonical["target_temperature_K"] = canonical["temperature_K"]
        if (
            operation in {"heat", "wait", "mix"}
            and "stirring_speed_rpm" not in canonical
        ):
            if "stirring_rpm" in canonical:
                canonical["stirring_speed_rpm"] = canonical["stirring_rpm"]
            elif "stirring_speed" in canonical:
                canonical["stirring_speed_rpm"] = canonical["stirring_speed"]
        if (
            operation == "sample"
            and "sample_volume_L" not in canonical
            and "volume_L" in canonical
        ):
            canonical["sample_volume_L"] = canonical["volume_L"]
        if (
            operation == "add_extractant"
            and "extractant" not in canonical
            and "solvent" in canonical
        ):
            canonical["extractant"] = canonical["solvent"]
        if (
            operation == "separate_phase"
            and "target_phase" not in canonical
            and "phase" in canonical
        ):
            canonical["target_phase"] = canonical["phase"]
        if operation == "wash" and "wash_volume_L" not in canonical and "volume_L" in canonical:
            canonical["wash_volume_L"] = canonical["volume_L"]
        return canonical

    def encode_vector(self, action: dict[str, Any]) -> np.ndarray:
        """Encode canonical event JSON as a stable numeric vector."""

        action = self.canonicalize(action)
        values = [
            self.operation_types.index(str(action["operation"])),
            self._float(action, "amount_mol", 0.0),
            self._float(action, "volume_L", 0.0),
            self._float(action, "catalyst_amount_mol", 0.0),
            self._float(action, "target_temperature_K", 298.15),
            self._float(action, "duration_s", 0.0),
            self._float(action, "stirring_speed_rpm", 600.0),
            self._float(action, "sample_volume_L", 0.0),
            self._index(action.get("instrument", "hplc"), self.instruments),
            self._float(action, "catalyst", 0.0),
            self._float(action, "solvent", 0.0),
            self._index(action.get("phase", "reactor_liquid"), self.phases),
            self._index(action.get("target_phase", "organic"), self.phases),
            self._index(action.get("extractant", 0), self.extractants),
            self._float(action, "wash_volume_L", 0.0),
            self._float(action, "transfer_fraction", 1.0),
            self._float(action, "seed_mass_g", 0.0),
            self._float(action, "reflux_ratio", 1.5),
            self._float(action, "flow_rate_mL_min", 1.0),
            self._float(action, "residence_time_s", 600.0),
            self._float(action, "potential_V", 1.2),
            self._float(action, "current_mA", 50.0),
        ]
        return np.asarray(values, dtype=np.float32)

    def decode_vector(self, vector: Any) -> dict[str, Any]:
        """Decode a numeric action vector into canonical event JSON."""

        array = np.asarray(vector, dtype=float).reshape(-1)
        if array.size < len(GYM_ACTION_KEYS):
            padded = np.zeros(len(GYM_ACTION_KEYS), dtype=float)
            padded[: array.size] = array
            array = padded
        operation_index = int(np.clip(round(array[0]), 0, len(self.operation_types) - 1))
        instrument_index = int(np.clip(round(array[8]), 0, len(self.instruments) - 1))
        phase_index = int(np.clip(round(array[11]), 0, len(self.phases) - 1))
        target_phase_index = int(np.clip(round(array[12]), 0, len(self.phases) - 1))
        return {
            "operation": self.operation_types[operation_index],
            "amount_mol": float(array[1]),
            "volume_L": float(array[2]),
            "catalyst_amount_mol": float(array[3]),
            "target_temperature_K": float(array[4]),
            "duration_s": float(array[5]),
            "stirring_speed_rpm": float(array[6]),
            "sample_volume_L": float(array[7]),
            "instrument": self.instruments[instrument_index],
            "catalyst": int(np.clip(round(array[9]), 0, len(self.catalysts) - 1)),
            "solvent": int(np.clip(round(array[10]), 0, len(self.solvents) - 1)),
            "phase": self.phases[phase_index],
            "target_phase": self.phases[target_phase_index],
            "extractant": int(np.clip(round(array[13]), 0, len(self.extractants) - 1)),
            "wash_volume_L": float(array[14]),
            "transfer_fraction": float(array[15]),
            "seed_mass_g": float(array[16]),
            "reflux_ratio": float(array[17]),
            "flow_rate_mL_min": float(array[18]),
            "residence_time_s": float(array[19]),
            "potential_V": float(array[20]),
            "current_mA": float(array[21]),
        }

    def phase_name(self, value: Any) -> str:
        if isinstance(value, str):
            # Keep unknown strings intact so validation rejects them atomically
            # instead of silently converting them to the organic phase.
            return value
        index = int(np.asarray(value).reshape(-1)[0])
        return self.phases[int(np.clip(index, 0, len(self.phases) - 1))]

    def extractant_name(self, value: Any) -> int:
        if isinstance(value, str):
            normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
            # Backward-compatible role alias used by early event recipes.
            if normalized == "organic":
                return self.extractants.index("toluene")
        return self._choice_index(value, self.extractants)

    @staticmethod
    def _float(action: dict[str, Any], key: str, default: float) -> float:
        value = action.get(key, default)
        return float(np.asarray(value).reshape(-1)[0])

    @staticmethod
    def _index(value: Any, choices: tuple[str, ...]) -> int:
        if isinstance(value, str) and value in choices:
            return choices.index(value)
        return int(np.clip(int(np.asarray(value).reshape(-1)[0]), 0, len(choices) - 1))

    @staticmethod
    def _choice_index(value: Any, choices: tuple[str, ...]) -> int:
        if isinstance(value, str):
            normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
            if normalized in choices:
                return choices.index(normalized)
            if normalized.isdigit():
                value = int(normalized)
            else:
                allowed = ", ".join(choices)
                raise ValueError(f"Unknown material choice {value!r}; allowed: {allowed}")
        index = int(np.asarray(value).reshape(-1)[0])
        if not 0 <= index < len(choices):
            raise ValueError(f"Material choice index {index} is outside [0, {len(choices) - 1}]")
        return index
