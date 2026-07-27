from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from scripts.run_mechanism_adaptation import _development_truncated_campaign_rows

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.mechanism_adaptation_live_llm import MechanismCandidateSpec
from chemworld.agents.stateful_scientific import StatefulScientificMechanismAgent
from chemworld.eval.mechanism_adaptation import load_mechanism_adaptation_protocol
from chemworld.eval.mechanism_adaptation_execution import (
    build_mechanism_agent,
    load_json_object,
    selected_campaign_rows,
)

ROOT = Path(__file__).resolve().parents[1]


class _Client:
    model = "deepseek-v4-pro"
    thinking = True
    reasoning_effort = "high"

    def __init__(self, payloads: list[dict[str, Any]]) -> None:
        self.payloads = list(payloads)
        self.prompts: list[dict[str, Any]] = []

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
    ) -> Any:
        del system_prompt, max_tokens
        self.prompts.append(json.loads(user_prompt))
        return SimpleNamespace(
            payload=self.payloads.pop(0),
            model=self.model,
            attempts=1,
            usage={
                "prompt_tokens": 200,
                "completion_tokens": 100,
                "total_tokens": 300,
                "prompt_cache_hit_tokens": 0,
                "prompt_cache_miss_tokens": 200,
            },
            attempt_records=(),
            request_id="test-request",
            system_fingerprint="test-fingerprint",
            finish_reason="stop",
            reasoning_content_present=False,
            reasoning_character_count=0,
        )

    def pricing_snapshot(self) -> dict[str, Any]:
        return {"access_date": "test"}

    def estimate_cost_usd(self, _: dict[str, Any]) -> float:
        return 0.0


def _context(step: int = 1) -> AgentDecisionContext:
    return AgentDecisionContext(
        step=step,
        task_id="reaction-to-crystallization",
        decision_stage="experiment_control",
        campaign_state={"remaining_budget": 20, "experiment_index": 0},
        visible_metrics={"yield": 0.1},
        latest_spectra={},
        uncertainty={"yield": 0.05},
        constraint_flags={},
        available_operations=("measure", "terminate"),
        previous_event_type="operation_result",
    )


def _public_view() -> dict[str, Any]:
    return {
        "tool_json": {
            "available_actions": [
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "terminate"},
            ],
            "lab_report": {"visible_metrics": {"yield": 0.1}},
        }
    }


def _state(*, evidence: bool = False) -> dict[str, Any]:
    labels = (
        "no_change",
        "rate_law_family",
        "topology_family",
        "material_law_counterfactual",
    )
    return {
        "current_question": "Does the latest public response support a changed rate law?",
        "campaign_plan": [
            {
                "step": "Measure a controlled response.",
                "purpose": "Separate rate and topology hypotheses.",
                "status": "active",
            }
        ],
        "mechanism_distribution": dict.fromkeys(labels, 0.25),
        "evidence_ledger": (
            [
                {
                    "evidence_id": "experiment-0001",
                    "supports": ["rate_law_family"],
                    "contradicts": ["no_change"],
                    "interpretation": "The public response changed under matched conditions.",
                }
            ]
            if evidence
            else []
        ),
        "replan_trigger": "Replan after the next public measurement.",
        "uncertainty": 0.5,
    }


def _decision(*, evidence: bool = False) -> dict[str, Any]:
    return {
        "action": {"operation": "measure", "instrument": "hplc"},
        "expected_effect": "Collect one public diagnostic response.",
        "diagnostic_target": "Distinguish no change from a rate-law shift.",
        "expected_information_gain": 0.4,
        "belief_update_rule": {
            "if_supported": "increase rate-law support",
            "if_not_supported": "increase no-change support",
        },
        "uncertainty": 0.5,
        "request_historical_spectrum_id": None,
        "scientific_state": _state(evidence=evidence),
    }


def _agent(client: _Client) -> StatefulScientificMechanismAgent:
    agent = StatefulScientificMechanismAgent(
        client,
        role_id="stateful-test",
        candidate_specs=(
            MechanismCandidateSpec("no_change", "No hidden-law change."),
            MechanismCandidateSpec("rate_law_family", "Rate dependence changes."),
            MechanismCandidateSpec("topology_family", "Network topology changes."),
            MechanismCandidateSpec(
                "material_law_counterfactual",
                "A public material mapping changes.",
            ),
        ),
        candidate_label_mode="semantic",
        candidate_order_seed=11,
        prompt_token_estimate_cap=1500,
    )
    agent.reset(
        {
            "task_id": "reaction-to-crystallization",
            "description": "Development mechanism-adaptation campaign.",
            "episode_mode": "campaign",
            "allowed_operations": ["measure", "terminate"],
        },
        7,
    )
    return agent


def test_stateful_scientific_agent_persists_only_model_authored_state() -> None:
    client = _Client([_decision(), _decision(evidence=True)])
    agent = _agent(client)

    assert agent.act_with_public_view(_context(1), _public_view()) == {
        "operation": "measure",
        "instrument": "hplc",
    }
    first_state = agent.scientific_state()
    assert first_state is not None
    assert client.prompts[0]["prior_scientific_state"] is None
    assert client.prompts[0]["stateful_scientific_contract"][
        "source"
    ].startswith("public evidence only")

    agent.act_with_public_view(_context(2), _public_view())
    assert client.prompts[1]["prior_scientific_state"] == first_state
    assert agent.scientific_state()["evidence_ledger"][0]["evidence_id"] == (
        "experiment-0001"
    )
    assert agent.method_resource_usage()["model_call_count"] == 2
    trace = agent.agent_trace()[0]
    assert trace["scientific_state_update_source"] == "agent_generated"
    assert len(trace["scientific_state_sha256"]) == 64
    assert agent.manifest()["gate_a_oracle_knowledge_supplied"] is False


def test_stateful_scientific_prompt_state_round_trips_and_rejects_tampering() -> None:
    source = _agent(_Client([_decision()]))
    source.act_with_public_view(_context(), _public_view())
    snapshot = source.export_prompt_state()

    branch = _agent(_Client([]))
    branch.restore_prompt_state(snapshot)
    assert branch.scientific_state() == source.scientific_state()

    tampered = copy.deepcopy(snapshot)
    tampered["scientific_state"]["current_question"] = "tampered"
    with pytest.raises(ValueError, match="hash mismatch"):
        branch.restore_prompt_state(tampered)


def test_stateful_scientific_rejects_unfrozen_fields_without_replacing_state() -> None:
    agent = _agent(_Client([_decision()]))
    agent.act_with_public_view(_context(), _public_view())
    before = agent.scientific_state()
    invalid = _decision(evidence=True)
    invalid["scientific_state"]["hidden_truth"] = "rate_law_family"

    with pytest.raises(ValueError, match="frozen fields"):
        agent._normalize_decision(invalid, context=_context(2))
    assert agent.scientific_state() == before


def test_development_method_factory_selects_direct_and_stateful_scaffolds() -> None:
    protocol = load_mechanism_adaptation_protocol(
        ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json"
    )
    row = selected_campaign_rows(protocol, limit=1)[0]
    methods = load_json_object(
        ROOT / "configs/methods/llm_v0.4/participant_methods_development.json"
    )

    stateful = build_mechanism_agent(
        protocol,
        row,
        llm_methods=methods,
        method_id="dev_pro_stateful",
        client=_Client([]),
    )
    direct = build_mechanism_agent(
        protocol,
        row,
        llm_methods=methods,
        method_id="dev_pro_direct",
        client=_Client([]),
    )

    assert isinstance(stateful, StatefulScientificMechanismAgent)
    assert not isinstance(direct, StatefulScientificMechanismAgent)
    assert direct.prompt_token_estimate_cap == 3600
    assert stateful.prompt_token_estimate_cap == 4150
    assert (
        stateful.environment_view_token_estimate_cap
        == direct.environment_view_token_estimate_cap
        == 2050
    )
    assert direct.agent_memory_token_estimate_cap == 950
    assert stateful.agent_memory_token_estimate_cap == 1350


def test_development_campaign_truncation_preserves_reference_and_marks_nonformal() -> None:
    row = {
        "phase_reset_after_experiment": 6,
        "total_experiment_horizon": 18,
        "post_change_checkpoints": [1, 2, 4, 8],
        "ordinary_change_detection_claim_allowed": True,
    }

    [truncated] = _development_truncated_campaign_rows(
        [row],
        post_change_experiments=2,
    )

    assert row["total_experiment_horizon"] == 18
    assert truncated["total_experiment_horizon"] == 8
    assert truncated["post_change_checkpoints"] == [1, 2]
    assert truncated["ordinary_change_detection_claim_allowed"] is False
    assert truncated["development_horizon_override"] == {
        "frozen_total_experiment_horizon": 18,
        "frozen_post_change_experiments": 12,
        "frozen_pre_change_experiments": 6,
        "executed_pre_change_experiments": 6,
        "executed_post_change_experiments": 2,
        "formal_result": False,
    }


def test_development_prechange_truncation_moves_change_and_paired_checkpoint() -> None:
    rows = [
        {
            "arm": "changed",
            "phase_reset_after_experiment": 6,
            "truth_change_time": 6,
            "evaluator_pseudo_checkpoint": None,
            "total_experiment_horizon": 18,
            "post_change_checkpoints": [1, 2, 4, 8],
        },
        {
            "arm": "no_change_twin",
            "phase_reset_after_experiment": 6,
            "truth_change_time": "never",
            "evaluator_pseudo_checkpoint": 6,
            "total_experiment_horizon": 18,
            "post_change_checkpoints": [1, 2, 4, 8],
        },
    ]

    changed, no_change = _development_truncated_campaign_rows(
        rows,
        pre_change_experiments=2,
        post_change_experiments=2,
    )

    assert changed["phase_reset_after_experiment"] == 2
    assert changed["truth_change_time"] == 2
    assert changed["total_experiment_horizon"] == 4
    assert no_change["phase_reset_after_experiment"] == 2
    assert no_change["truth_change_time"] == "never"
    assert no_change["evaluator_pseudo_checkpoint"] == 2
    assert no_change["total_experiment_horizon"] == 4


def test_development_campaign_truncation_cannot_extend_frozen_horizon() -> None:
    with pytest.raises(ValueError, match="cannot exceed"):
        _development_truncated_campaign_rows(
            [
                {
                    "phase_reset_after_experiment": 6,
                    "total_experiment_horizon": 8,
                    "post_change_checkpoints": [1, 2],
                }
            ],
            post_change_experiments=3,
        )
