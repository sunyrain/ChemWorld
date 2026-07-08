"""Reaction-network specs and equation parsing helpers."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from chemworld.physchem.elements import parse_formula

Arrow = Literal["=>", "<=>"]
SUPPORTED_RATE_LAW_EQUATION_IDS = (
    "mass_action",
    "arrhenius",
    "modified_arrhenius",
    "reversible_arrhenius",
    "catalytic_activity",
    "catalyst_deactivation",
    "langmuir_hinshelwood",
    "michaelis_menten",
)


@dataclass(frozen=True)
class SpeciesSpec:
    species_id: str
    formula: str
    phase: str = "liquid"
    charge: int = 0
    catalyst: bool = False
    observable_aliases: tuple[str, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.species_id:
            raise ValueError("species_id cannot be empty")
        parse_formula(self.formula)
        object.__setattr__(self, "observable_aliases", tuple(self.observable_aliases))

    @property
    def composition(self) -> dict[str, float]:
        return parse_formula(self.formula)

    def to_dict(self) -> dict[str, object]:
        return {
            "species_id": self.species_id,
            "formula": self.formula,
            "composition": self.composition,
            "phase": self.phase,
            "charge": self.charge,
            "catalyst": self.catalyst,
            "observable_aliases": list(self.observable_aliases),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class RateLawSpec:
    rate_law_id: str
    equation_id: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.rate_law_id:
            raise ValueError("rate_law_id cannot be empty")
        if self.equation_id not in SUPPORTED_RATE_LAW_EQUATION_IDS:
            raise ValueError(f"Unsupported rate law: {self.equation_id}")

    def to_dict(self) -> dict[str, object]:
        return {
            "rate_law_id": self.rate_law_id,
            "equation_id": self.equation_id,
            "parameters": dict(self.parameters),
        }


@dataclass(frozen=True)
class ReactionSpec:
    reaction_id: str
    equation: str
    stoichiometry: dict[str, float]
    reversible: bool
    rate_law: RateLawSpec
    delta_h_J_per_mol: float = 0.0
    equilibrium_model_id: str = ""
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.reaction_id:
            raise ValueError("reaction_id cannot be empty")
        if not self.stoichiometry:
            raise ValueError("Reaction stoichiometry cannot be empty")
        if not any(value < 0 for value in self.stoichiometry.values()):
            raise ValueError("Reaction must contain at least one reactant")
        if not any(value > 0 for value in self.stoichiometry.values()):
            raise ValueError("Reaction must contain at least one product")
        if any(value == 0 for value in self.stoichiometry.values()):
            raise ValueError("Zero stoichiometric coefficients are not stored")

    @classmethod
    def from_equation(
        cls,
        *,
        reaction_id: str,
        equation: str,
        rate_law: RateLawSpec,
        delta_h_J_per_mol: float = 0.0,
        equilibrium_model_id: str = "",
        metadata: dict[str, object] | None = None,
    ) -> ReactionSpec:
        stoichiometry, reversible = parse_reaction_equation(equation)
        return cls(
            reaction_id=reaction_id,
            equation=equation,
            stoichiometry=stoichiometry,
            reversible=reversible,
            rate_law=rate_law,
            delta_h_J_per_mol=delta_h_J_per_mol,
            equilibrium_model_id=equilibrium_model_id,
            metadata={} if metadata is None else dict(metadata),
        )

    @property
    def reactants(self) -> dict[str, float]:
        return {
            species_id: -coefficient
            for species_id, coefficient in self.stoichiometry.items()
            if coefficient < 0
        }

    @property
    def products(self) -> dict[str, float]:
        return {
            species_id: coefficient
            for species_id, coefficient in self.stoichiometry.items()
            if coefficient > 0
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "reaction_id": self.reaction_id,
            "equation": self.equation,
            "stoichiometry": dict(self.stoichiometry),
            "reversible": self.reversible,
            "rate_law": self.rate_law.to_dict(),
            "delta_h_J_per_mol": self.delta_h_J_per_mol,
            "equilibrium_model_id": self.equilibrium_model_id,
            "metadata": dict(self.metadata),
        }


def parse_reaction_equation(equation: str) -> tuple[dict[str, float], bool]:
    if "<=>" in equation:
        left, right = equation.split("<=>", 1)
        reversible = True
    elif "=>" in equation:
        left, right = equation.split("=>", 1)
        reversible = False
    elif "->" in equation:
        left, right = equation.split("->", 1)
        reversible = False
    else:
        raise ValueError(f"Reaction equation is missing an arrow: {equation}")
    stoichiometry: dict[str, float] = {}
    _merge_side(stoichiometry, left, sign=-1.0)
    _merge_side(stoichiometry, right, sign=1.0)
    cleaned = {
        species_id: value
        for species_id, value in stoichiometry.items()
        if value != 0.0
    }
    return cleaned, reversible


def species_from_dict(payload: Mapping[str, Any]) -> SpeciesSpec:
    return SpeciesSpec(
        species_id=str(payload["species_id"]),
        formula=str(payload["formula"]),
        phase=str(payload.get("phase", "liquid")),
        charge=int(payload.get("charge", 0)),
        catalyst=bool(payload.get("catalyst", False)),
        observable_aliases=tuple(
            str(value) for value in payload.get("observable_aliases", ())
        ),
        metadata=dict(payload.get("metadata", {})),
    )


def reaction_from_dict(payload: Mapping[str, Any]) -> ReactionSpec:
    rate_payload = payload["rate_law"]
    rate_law = RateLawSpec(
        rate_law_id=str(rate_payload["rate_law_id"]),
        equation_id=str(rate_payload["equation_id"]),
        parameters=dict(rate_payload.get("parameters", {})),
    )
    if "stoichiometry" in payload:
        stoichiometry = {
            str(key): float(value) for key, value in payload["stoichiometry"].items()
        }
        reversible = bool(payload.get("reversible", "<=>" in str(payload.get("equation", ""))))
        return ReactionSpec(
            reaction_id=str(payload["reaction_id"]),
            equation=str(payload.get("equation", "")),
            stoichiometry=stoichiometry,
            reversible=reversible,
            rate_law=rate_law,
            delta_h_J_per_mol=float(payload.get("delta_h_J_per_mol", 0.0)),
            equilibrium_model_id=str(payload.get("equilibrium_model_id", "")),
            metadata=dict(payload.get("metadata", {})),
        )
    return ReactionSpec.from_equation(
        reaction_id=str(payload["reaction_id"]),
        equation=str(payload["equation"]),
        rate_law=rate_law,
        delta_h_J_per_mol=float(payload.get("delta_h_J_per_mol", 0.0)),
        equilibrium_model_id=str(payload.get("equilibrium_model_id", "")),
        metadata=dict(payload.get("metadata", {})),
    )


def _merge_side(stoichiometry: dict[str, float], side: str, *, sign: float) -> None:
    for token in side.split("+"):
        token = token.strip()
        if not token:
            continue
        coefficient, species_id = _parse_species_term(token)
        stoichiometry[species_id] = stoichiometry.get(species_id, 0.0) + sign * coefficient


_TERM_RE = re.compile(r"^(?:(\d+(?:\.\d*)?|\.\d+)\s+)?([A-Za-z_][A-Za-z0-9_().-]*)$")


def _parse_species_term(token: str) -> tuple[float, str]:
    match = _TERM_RE.match(token)
    if not match:
        raise ValueError(f"Invalid reaction term: {token}")
    coefficient = 1.0 if match.group(1) is None else float(match.group(1))
    if coefficient <= 0:
        raise ValueError(f"Reaction coefficients must be positive: {token}")
    return coefficient, match.group(2)


__all__ = [
    "SUPPORTED_RATE_LAW_EQUATION_IDS",
    "Arrow",
    "RateLawSpec",
    "ReactionSpec",
    "SpeciesSpec",
    "parse_reaction_equation",
    "reaction_from_dict",
    "species_from_dict",
]
