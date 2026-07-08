"""Component-level property-package convenience wrapper."""

from __future__ import annotations

from dataclasses import dataclass

from chemworld.physchem.property_equations import (
    _choose_valid_correlation,
    evaluate_correlation,
)
from chemworld.physchem.property_reports import PropertyEvaluation, ValidityPolicy
from chemworld.physchem.specs import ComponentSpec, PropertyCorrelation
from chemworld.physchem.vapor_pressure import VaporPressureReport, vapor_pressure_report


@dataclass(frozen=True)
class ComponentPropertyPackage:
    component: ComponentSpec
    correlations: tuple[PropertyCorrelation, ...]

    def __post_init__(self) -> None:
        ids = [correlation.correlation_id for correlation in self.correlations]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate correlation_id values are not allowed")
        allowed = set(self.component.allowed_property_correlations)
        if allowed:
            disallowed = [
                correlation.correlation_id
                for correlation in self.correlations
                if correlation.correlation_id not in allowed
                and correlation.property_id not in allowed
                and correlation.equation_id not in allowed
            ]
            if disallowed:
                raise ValueError(
                    "Correlations are not allowed by component policy: "
                    f"{disallowed}"
                )

    def by_property(self, property_id: str) -> tuple[PropertyCorrelation, ...]:
        return tuple(
            correlation
            for correlation in self.correlations
            if correlation.property_id == property_id
        )

    def evaluate(
        self,
        property_id: str,
        *,
        temperature_K: float,
        pressure_Pa: float | None = None,
        validity_policy: ValidityPolicy = "warn",
    ) -> PropertyEvaluation:
        candidates = self.by_property(property_id)
        if not candidates:
            raise ValueError(
                f"No correlation for property {property_id!r} on component "
                f"{self.component.identifier!r}"
            )
        chosen = _choose_valid_correlation(
            candidates,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
        )
        return evaluate_correlation(
            chosen,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
            molecular_weight_g_mol=self.component.molecular_weight_g_mol,
            validity_policy=validity_policy,
        )

    def vapor_pressure_report(
        self,
        *,
        temperature_K: float,
        property_id: str = "vapor_pressure",
        validity_policy: ValidityPolicy = "warn",
    ) -> VaporPressureReport:
        candidates = self.by_property(property_id)
        if not candidates:
            raise ValueError(
                f"No correlation for property {property_id!r} on component "
                f"{self.component.identifier!r}"
            )
        chosen = _choose_valid_correlation(
            candidates,
            temperature_K=temperature_K,
            pressure_Pa=None,
        )
        return vapor_pressure_report(
            chosen,
            temperature_K=temperature_K,
            validity_policy=validity_policy,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "component": self.component.to_dict(),
            "correlations": [correlation.to_dict() for correlation in self.correlations],
        }

