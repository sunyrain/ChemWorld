"""Shared physical-chemical world law specification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WorldLawSpec:
    law_version: str
    ontology_registry: dict[str, Any]
    physical_constitution: str
    operation_registry: tuple[str, ...]
    transition_kernel_registry: tuple[str, ...]
    observation_kernel_registry: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "law_version": self.law_version,
            "ontology_registry": self.ontology_registry,
            "physical_constitution": self.physical_constitution,
            "operation_registry": list(self.operation_registry),
            "transition_kernel_registry": list(self.transition_kernel_registry),
            "observation_kernel_registry": list(self.observation_kernel_registry),
        }
