from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.agents.bo import GaussianProcessBOAgent
from chemworld.agents.interaction import (
    DecisionAuditRecord,
    InteractionCapabilities,
)
from chemworld.agents.random import RandomAgent
from chemworld.eval.interaction_contract_audit import (
    audit_agent_interaction_contract,
    load_interaction_protocol,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "agent-interaction-contract.json"
)


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


def test_interaction_protocol_drift_fails_closed() -> None:
    protocol = deepcopy(load_interaction_protocol())
    protocol["interaction_contract_version"] = "wrong"
    report = audit_agent_interaction_contract(protocol)
    assert report["checks"]["contract_version"] is False
    assert report["controls_ready"] is False


def test_frozen_interaction_control_report_is_ready_but_non_claiming() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["checks"]["spectra_reaches_next_decision"] is True
    assert report["checks"]["raw_spectrum_reaches_next_decision"] is True
    assert report["checks"]["structured_audit_retained"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
