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
            "expected_effect": "Waiting will test whether the signal is stable.",
            "diagnostic_target": "target-to-impurity response stability",
            "expected_information_gain": 0.2,
            "belief_update_rule": {
                "if_supported": "increase support for a stable response",
                "if_not_supported": "test a shorter interval",
            },
            "uncertainty": 0.3,
            "adaptation_source": "spectrum",
            "request_historical_spectrum_id": "spectrum-e001-s0003",
        },
        action={"operation": "wait"},
    ).to_dict()

    assert audit["diagnostic_target"] == "target-to-impurity response stability"
    assert audit["expected_information_gain"] == 0.2
    assert audit["requested_historical_spectrum_id"] == "spectrum-e001-s0003"
