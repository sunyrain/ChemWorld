from __future__ import annotations

from chemworld.agents.bo import GaussianProcessBOAgent
from chemworld.agents.interaction import (
    DecisionAuditRecord,
    InteractionCapabilities,
)
from chemworld.agents.random import RandomAgent


def test_recipe_agents_honestly_declare_interaction_limits() -> None:
    capabilities = RandomAgent().interaction_capabilities()
    assert capabilities.decision_scope == "experiment_recipe"
    assert capabilities.consumes_spectra is False
    assert capabilities.adapts_within_experiment is False
    assert capabilities.adapts_across_experiments is False
    bo_capabilities = GaussianProcessBOAgent().interaction_capabilities()
    assert bo_capabilities.decision_scope == "experiment_recipe"
    assert bo_capabilities.adapts_across_experiments is True
    assert bo_capabilities.adapts_within_experiment is False


def test_capabilities_and_decision_audits_fail_closed() -> None:
    try:
        InteractionCapabilities(
            consumes_intermediate_observations=False,
            consumes_spectra=True,
        )
    except ValueError as exc:
        assert "spectra" in str(exc)
    else:
        raise AssertionError("invalid capabilities were accepted")
    try:
        DecisionAuditRecord.from_payload(
            {
                "action": {"operation": "wait"},
                "evidence": [],
                "hypothesis": "test",
                "uncertainty": 1.5,
                "rationale": "test",
                "adaptation_source": "none",
            },
            action={"operation": "wait"},
        )
    except ValueError as exc:
        assert "uncertainty" in str(exc)
    else:
        raise AssertionError("invalid decision audit was accepted")


def test_decision_audit_retains_public_spectrum_fields() -> None:
    audit = DecisionAuditRecord.from_payload(
        {
            "action": {"operation": "wait"},
            "evidence": ["The current HPLC packet contains a target peak."],
            "spectrum_interpretation": "The target peak dominates the impurity peak.",
            "hypothesis": "Waiting will test whether the signal is stable.",
            "uncertainty": 0.3,
            "rationale": "Use one bounded observation interval.",
            "adaptation_source": "spectrum",
            "request_historical_spectrum_id": "spectrum-e001-s0003",
        },
        action={"operation": "wait"},
    ).to_dict()

    assert audit["spectrum_interpretation"] == (
        "The target peak dominates the impurity peak."
    )
    assert audit["requested_historical_spectrum_id"] == "spectrum-e001-s0003"
