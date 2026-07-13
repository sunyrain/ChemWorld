"""Typed public interaction contract for operation-level benchmark agents."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from chemworld.data.logging import to_builtin

INTERACTION_CONTRACT_VERSION = "chemworld-agent-interaction-0.1"

DecisionScope = Literal["experiment_recipe", "operation"]
AdaptationSource = Literal[
    "none",
    "measurement",
    "spectrum",
    "experiment_memory",
    "validator",
]


@dataclass(frozen=True)
class InteractionCapabilities:
    """Machine-readable declaration of evidence an agent actually consumes."""

    decision_scope: DecisionScope = "operation"
    consumes_intermediate_observations: bool = False
    consumes_spectra: bool = False
    adapts_within_experiment: bool = False
    adapts_across_experiments: bool = False
    emits_structured_decision_audit: bool = False

    def __post_init__(self) -> None:
        if self.decision_scope not in {"experiment_recipe", "operation"}:
            raise ValueError("unsupported decision scope")
        if self.consumes_spectra and not self.consumes_intermediate_observations:
            raise ValueError("spectra consumption requires intermediate observations")
        if self.adapts_within_experiment and self.decision_scope != "operation":
            raise ValueError("within-experiment adaptation requires operation decisions")

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_version": INTERACTION_CONTRACT_VERSION,
            **asdict(self),
        }


@dataclass(frozen=True)
class DecisionAuditRecord:
    """Concise public decision evidence; never a private chain-of-thought field."""

    action: dict[str, Any]
    evidence: tuple[str, ...]
    hypothesis: str
    uncertainty: float | None
    rationale: str
    adaptation_source: AdaptationSource
    status: Literal["provided", "not_provided"] = "provided"

    def __post_init__(self) -> None:
        if self.adaptation_source not in {
            "none",
            "measurement",
            "spectrum",
            "experiment_memory",
            "validator",
        }:
            raise ValueError("unsupported decision adaptation source")
        if self.status not in {"provided", "not_provided"}:
            raise ValueError("unsupported decision audit status")
        if self.uncertainty is not None and not 0.0 <= self.uncertainty <= 1.0:
            raise ValueError("decision uncertainty must be in [0, 1]")
        if self.status == "provided" and (
            not self.action.get("operation")
            or not self.evidence
            or not self.hypothesis
            or not self.rationale
        ):
            raise ValueError(
                "provided decision audits require action, evidence, hypothesis, and rationale"
            )

    @classmethod
    def unavailable(cls, action: dict[str, Any]) -> DecisionAuditRecord:
        return cls(
            action=dict(action),
            evidence=(),
            hypothesis="",
            uncertainty=None,
            rationale="",
            adaptation_source="none",
            status="not_provided",
        )

    @classmethod
    def from_payload(
        cls,
        payload: dict[str, Any] | None,
        *,
        action: dict[str, Any],
    ) -> DecisionAuditRecord:
        if not payload:
            return cls.unavailable(action)
        payload_action = payload.get("action", action)
        if not isinstance(payload_action, dict) or payload_action != action:
            raise ValueError("decision audit action must match the selected action")
        evidence = payload.get("evidence", ())
        if not isinstance(evidence, list | tuple):
            raise ValueError("decision audit evidence must be a list")
        return cls(
            action=dict(action),
            evidence=tuple(str(item) for item in evidence),
            hypothesis=str(payload.get("hypothesis", "")),
            uncertainty=(
                None if payload.get("uncertainty") is None else float(payload["uncertainty"])
            ),
            rationale=str(payload.get("rationale", "")),
            adaptation_source=str(payload.get("adaptation_source", "none")),  # type: ignore[arg-type]
            status=str(payload.get("status", "provided")),  # type: ignore[arg-type]
        )

    def to_dict(self) -> dict[str, Any]:
        return to_builtin(asdict(self))


@dataclass(frozen=True)
class AgentDecisionContext:
    """Public, compact context supplied before one operation decision."""

    step: int
    task_id: str | None
    decision_stage: str
    campaign_state: dict[str, Any]
    visible_metrics: dict[str, Any]
    latest_spectra: dict[str, Any]
    uncertainty: dict[str, Any]
    constraint_flags: dict[str, Any]
    available_operations: tuple[str, ...]
    previous_event_type: str | None
    historical_spectrum_catalog: tuple[dict[str, Any], ...] = ()
    requested_historical_spectrum: dict[str, Any] = field(default_factory=dict)

    @property
    def remaining_operations(self) -> int:
        return max(int(self.campaign_state.get("remaining_budget", 0)), 0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_version": INTERACTION_CONTRACT_VERSION,
            "step": self.step,
            "task_id": self.task_id,
            "decision_stage": self.decision_stage,
            "campaign_state": to_builtin(self.campaign_state),
            "visible_metrics": to_builtin(self.visible_metrics),
            "latest_spectra": to_builtin(self.latest_spectra),
            "uncertainty": to_builtin(self.uncertainty),
            "constraint_flags": to_builtin(self.constraint_flags),
            "available_operations": list(self.available_operations),
            "previous_event_type": self.previous_event_type,
            "remaining_operations": self.remaining_operations,
            "historical_spectrum_catalog": to_builtin(
                self.historical_spectrum_catalog
            ),
            "requested_historical_spectrum": to_builtin(
                self.requested_historical_spectrum
            ),
        }


def build_decision_context(
    *,
    step: int,
    task_info: dict[str, Any],
    campaign_state: dict[str, Any],
    public_view: dict[str, Any],
    previous_event_type: str | None,
) -> AgentDecisionContext:
    """Reduce the standard public view to stable decision-relevant evidence."""

    tool_view = public_view.get("tool_json", {})
    lab_report = tool_view.get("lab_report", {}) if isinstance(tool_view, dict) else {}
    spectra = lab_report.get("spectra_summary", {}) if isinstance(lab_report, dict) else {}
    spectra_context = {
        **(spectra if isinstance(spectra, dict) else {}),
        "raw_signal": to_builtin(tool_view.get("raw_signal", {})),
        "processed_estimate": to_builtin(tool_view.get("processed_estimate", {})),
    }
    catalog = tool_view.get("historical_spectrum_catalog", [])
    requested = tool_view.get("requested_historical_spectrum", {})
    available = tool_view.get("available_actions", []) if isinstance(tool_view, dict) else []
    operations = tuple(
        str(item["operation"])
        for item in available
        if isinstance(item, dict) and item.get("operation")
    )
    if previous_event_type == "experiment_end" or step == 1:
        stage = "experiment_setup"
    elif previous_event_type == "measurement_result":
        stage = "evidence_update"
    elif "final_assay" in operations and "terminate" not in operations:
        stage = "experiment_closeout"
    else:
        stage = "experiment_control"
    return AgentDecisionContext(
        step=step,
        task_id=(None if task_info.get("task_id") is None else str(task_info["task_id"])),
        decision_stage=stage,
        campaign_state=to_builtin(campaign_state),
        visible_metrics=to_builtin(lab_report.get("visible_metrics", {})),
        latest_spectra=to_builtin(spectra_context),
        uncertainty=to_builtin(tool_view.get("uncertainty", {})),
        constraint_flags=to_builtin(tool_view.get("constraints", {})),
        available_operations=operations,
        previous_event_type=previous_event_type,
        historical_spectrum_catalog=tuple(
            to_builtin(item) for item in catalog if isinstance(item, dict)
        )
        if isinstance(catalog, list)
        else (),
        requested_historical_spectrum=(
            to_builtin(requested) if isinstance(requested, dict) else {}
        ),
    )


__all__ = [
    "INTERACTION_CONTRACT_VERSION",
    "AgentDecisionContext",
    "DecisionAuditRecord",
    "InteractionCapabilities",
    "build_decision_context",
]
