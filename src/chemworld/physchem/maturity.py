"""Maturity metadata for ChemWorld physical-chemistry models.

The classes in this module are deliberately small and JSON-friendly. They do
not make a model professional by declaration; they make maturity claims
auditable by tasks, docs, and tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MaturityLevel(StrEnum):
    PROXY = "proxy"
    LITE = "lite"
    REFERENCE_VALIDATED = "reference_validated"
    PROFESSIONAL_CANDIDATE = "professional_candidate"
    PROFESSIONAL = "professional"

    @classmethod
    def normalize(cls, value: str | MaturityLevel) -> MaturityLevel:
        if isinstance(value, cls):
            return value
        try:
            return cls(value)
        except ValueError as exc:
            allowed = ", ".join(level.value for level in cls)
            raise ValueError(f"unknown maturity level {value!r}; allowed={allowed}") from exc

    @property
    def rank(self) -> int:
        return _MATURITY_RANK[self]


_MATURITY_RANK = {
    MaturityLevel.PROXY: 0,
    MaturityLevel.LITE: 1,
    MaturityLevel.REFERENCE_VALIDATED: 2,
    MaturityLevel.PROFESSIONAL_CANDIDATE: 3,
    MaturityLevel.PROFESSIONAL: 4,
}

PROXY_ALLOWED_TAGS = frozenset({"teaching", "smoke", "exploratory", "education"})
PROFESSIONAL_LEVELS = frozenset(
    {MaturityLevel.PROFESSIONAL_CANDIDATE, MaturityLevel.PROFESSIONAL}
)


@dataclass(frozen=True)
class ValidationEvidence:
    evidence_id: str
    evidence_type: str
    description: str
    status: str = "planned"
    reference_backend: str | None = None
    command_or_path: str | None = None
    tolerance: str | None = None

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id cannot be empty")
        if not self.evidence_type.strip():
            raise ValueError("evidence_type cannot be empty")
        if not self.description.strip():
            raise ValueError("description cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type,
            "description": self.description,
            "status": self.status,
            "reference_backend": self.reference_backend,
            "command_or_path": self.command_or_path,
            "tolerance": self.tolerance,
        }


@dataclass(frozen=True)
class ModelCardTemplate:
    template_id: str
    module_id: str
    title: str
    required_sections: tuple[str, ...]
    reference_targets: tuple[str, ...] = ()
    validation_expectations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.template_id.strip():
            raise ValueError("template_id cannot be empty")
        if not self.module_id.strip():
            raise ValueError("module_id cannot be empty")
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if not self.required_sections:
            raise ValueError("required_sections cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "template_id": self.template_id,
            "module_id": self.module_id,
            "title": self.title,
            "required_sections": list(self.required_sections),
            "reference_targets": list(self.reference_targets),
            "validation_expectations": list(self.validation_expectations),
        }


@dataclass(frozen=True)
class ModelCard:
    model_id: str
    module_id: str
    title: str
    maturity: MaturityLevel
    summary: str
    equations: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    validity_limits: tuple[str, ...] = ()
    failure_modes: tuple[str, ...] = ()
    units: dict[str, str] = field(default_factory=dict)
    reference_reading: tuple[str, ...] = ()
    validation_evidence: tuple[ValidationEvidence, ...] = ()
    model_limit_notes: tuple[str, ...] = ()
    intended_use: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "maturity", MaturityLevel.normalize(self.maturity))
        for field_name in ("model_id", "module_id", "title", "summary"):
            if not str(getattr(self, field_name)).strip():
                raise ValueError(f"{field_name} cannot be empty")
        if self.maturity in PROFESSIONAL_LEVELS and not self.validation_evidence:
            raise ValueError(
                "professional maturity claims require validation_evidence"
            )
        if self.maturity in PROFESSIONAL_LEVELS and not self.validity_limits:
            raise ValueError("professional maturity claims require validity_limits")

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "module_id": self.module_id,
            "title": self.title,
            "maturity": self.maturity.value,
            "summary": self.summary,
            "equations": list(self.equations),
            "assumptions": list(self.assumptions),
            "validity_limits": list(self.validity_limits),
            "failure_modes": list(self.failure_modes),
            "units": dict(self.units),
            "reference_reading": list(self.reference_reading),
            "validation_evidence": [
                evidence.to_dict() for evidence in self.validation_evidence
            ],
            "model_limit_notes": list(self.model_limit_notes),
            "intended_use": list(self.intended_use),
        }


@dataclass(frozen=True)
class ModuleMaturity:
    module_id: str
    level: MaturityLevel
    model_ids: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "level", MaturityLevel.normalize(self.level))
        if not self.module_id.strip():
            raise ValueError("module_id cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "level": self.level.value,
            "model_ids": list(self.model_ids),
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class TaskMaturitySpec:
    modules: tuple[ModuleMaturity, ...]
    proxy_allowed: bool = False
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.modules:
            raise ValueError("TaskMaturitySpec requires at least one module")
        module_ids = [module.module_id for module in self.modules]
        if len(module_ids) != len(set(module_ids)):
            raise ValueError("duplicate module maturity entries are not allowed")
        if self.contains_proxy and not self.proxy_allowed:
            raise ValueError("proxy module maturity requires proxy_allowed=True")

    @property
    def contains_proxy(self) -> bool:
        return any(module.level is MaturityLevel.PROXY for module in self.modules)

    @property
    def lowest_level(self) -> MaturityLevel:
        return min((module.level for module in self.modules), key=lambda level: level.rank)

    def to_dict(self) -> dict[str, Any]:
        return {
            "modules": [module.to_dict() for module in self.modules],
            "lowest_level": self.lowest_level.value,
            "proxy_allowed": self.proxy_allowed,
            "notes": list(self.notes),
        }


def model_card_templates() -> tuple[ModelCardTemplate, ...]:
    common = (
        "equations_or_algorithm",
        "assumptions",
        "validity_limits",
        "failure_modes",
        "units",
        "reference_reading",
        "validation_evidence",
        "intended_use",
    )
    return (
        ModelCardTemplate(
            "property_model_card",
            "properties",
            "Property Correlation Model Card",
            common,
            ("chemicals", "thermo", "CoolProp"),
            ("reference property points", "validity range checks"),
        ),
        ModelCardTemplate(
            "eos_model_card",
            "eos",
            "Equation Of State Model Card",
            common,
            ("CoolProp", "thermo", "teqp", "thermopack"),
            ("compressibility/fugacity cases", "root-selection checks"),
        ),
        ModelCardTemplate(
            "phase_equilibrium_model_card",
            "phase_equilibrium",
            "Phase Equilibrium Model Card",
            common,
            ("thermo", "phasepy", "thermopack"),
            ("bubble/dew/flash cases", "mass-balance checks"),
        ),
        ModelCardTemplate(
            "reaction_kinetics_model_card",
            "reaction_kinetics",
            "Reaction Kinetics Model Card",
            common,
            ("Cantera", "RMG-Py", "thermo"),
            ("ODE reference cases", "stoichiometric balance checks"),
        ),
        ModelCardTemplate(
            "reactor_model_card",
            "reactors",
            "Reactor Model Card",
            common,
            ("Cantera", "IDAES"),
            ("analytical or reference reactor cases", "ledger invariants"),
        ),
        ModelCardTemplate(
            "separation_model_card",
            "separations",
            "Separation Unit Model Card",
            common,
            ("IDAES", "thermo", "phasepy", "fluids"),
            ("material-balance checks", "purity/recovery tradeoffs"),
        ),
        ModelCardTemplate(
            "transport_model_card",
            "transport",
            "Transport And Heat-Transfer Model Card",
            common,
            ("fluids", "IDAES", "CoolProp"),
            ("dimensionless-number checks", "equipment calculation checks"),
        ),
        ModelCardTemplate(
            "instrument_model_card",
            "spectroscopy_instruments",
            "Instrument And Spectroscopy Model Card",
            common,
            ("public instrument equations", "public calibration examples"),
            ("calibration checks", "detection-limit checks"),
        ),
    )


def model_card_template_map() -> dict[str, ModelCardTemplate]:
    return {template.module_id: template for template in model_card_templates()}


def validate_model_card(card: ModelCard) -> list[str]:
    issues: list[str] = []
    if card.maturity in PROFESSIONAL_LEVELS:
        if not card.validation_evidence:
            issues.append("professional maturity requires validation_evidence")
        if not card.validity_limits:
            issues.append("professional maturity requires validity_limits")
        if not card.reference_reading:
            issues.append("professional maturity requires reference_reading")
        if not card.failure_modes:
            issues.append("professional maturity requires failure_modes")
    if card.maturity is MaturityLevel.PROXY and not card.model_limit_notes:
        issues.append("proxy model cards must include model_limit_notes")
    return issues


def validate_task_maturity_policy(
    *,
    task_id: str,
    tags: tuple[str, ...],
    maturity: TaskMaturitySpec,
) -> None:
    tag_set = set(tags)
    if maturity.proxy_allowed and not tag_set.intersection(PROXY_ALLOWED_TAGS):
        allowed = ", ".join(sorted(PROXY_ALLOWED_TAGS))
        raise ValueError(
            f"{task_id} sets proxy_allowed=True but lacks an allowed tag: {allowed}"
        )
    if maturity.contains_proxy and not maturity.proxy_allowed:
        raise ValueError(f"{task_id} contains proxy modules without proxy_allowed=True")
