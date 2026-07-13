from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.live_llm import (
    LiveLLMAgent,
    LiveLLMProviderUnavailableError,
)
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records


def _decision(action: dict[str, Any], *, evidence: str = "public measurement") -> dict[str, Any]:
    return {
        "action": action,
        "evidence": [evidence],
        "spectrum_interpretation": "One supplied public peak changed amplitude.",
        "hypothesis": "The next operation will test the observed response.",
        "uncertainty": 0.4,
        "rationale": "Use the public response to choose one reproducible operation.",
    }


class FakeClient:
    model = "deepseek-v4-pro"
    thinking = True
    reasoning_effort = "max"

    def __init__(self, decisions: list[dict[str, Any] | Exception]) -> None:
        self.decisions = list(decisions)
        self.prompts: list[dict[str, Any]] = []

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> Any:
        del system_prompt, max_tokens
        self.prompts.append(json.loads(user_prompt))
        item = self.decisions.pop(0)
        if isinstance(item, Exception):
            raise item
        return SimpleNamespace(
            payload=item,
            model=self.model,
            attempts=2,
            usage={
                "prompt_tokens": 100,
                "completion_tokens": 25,
                "total_tokens": 125,
                "prompt_cache_hit_tokens": 40,
                "prompt_cache_miss_tokens": 60,
            },
        )

    def pricing_snapshot(self) -> dict[str, Any]:
        return {
            "model_id": self.model,
            "access_date": "2026-07-11",
            "input_cache_hit_per_million_usd": 0.003625,
            "input_cache_miss_per_million_usd": 0.435,
            "output_per_million_usd": 0.87,
        }

    def estimate_cost_usd(self, usage: dict[str, Any]) -> float:
        return (int(usage.get("prompt_tokens", 0)) + int(usage.get("completion_tokens", 0))) / (
            1_000_000
        )


class FakeProviderError(RuntimeError):
    def __init__(self) -> None:
        super().__init__("secret transport detail must not be retained")
        self.attempts = 3
        self.usage = {"prompt_tokens": 30, "completion_tokens": 0, "total_tokens": 30}


class FakeUnbillableProviderError(RuntimeError):
    def __init__(self) -> None:
        super().__init__("private provider rejection")
        self.attempts = 1
        self.usage: dict[str, int] = {}
        self.status_code = 402
        self.retryable = False
        self.attempt_records = (
            {
                "attempt_index": 1,
                "status": "failed",
                "request_id": None,
                "model_id": "deepseek-v4-pro",
                "usage": {},
                "usage_complete": False,
                "billable": False,
                "failure_type": "FakeUnbillableProviderError",
            },
        )


def _context(*, step: int, previous: str | None, spectra: bool = True) -> AgentDecisionContext:
    return AgentDecisionContext(
        step=step,
        task_id="flow-reaction-optimization",
        decision_stage="evidence_update" if previous else "experiment_setup",
        campaign_state={"remaining_budget": 20, "final_assay_count": step - 1},
        visible_metrics={"conversion": 0.4},
        latest_spectra=(
            {
                "has_spectral_packet": True,
                "raw_signal": {"kind": "uvvis_spectrum", "peaks": [{"center": 420.0}]},
                "processed_estimate": {"peak_count": 1},
            }
            if spectra
            else {}
        ),
        uncertainty={"conversion": 0.1},
        constraint_flags={},
        available_operations=("heat", "terminate"),
        previous_event_type=previous,
    )


def _public_view() -> dict[str, Any]:
    return {
        "tool_json": {
            "available_actions": [{"operation": "heat"}, {"operation": "terminate"}],
            "raw_signal": {
                "kind": "uvvis_spectrum",
                "peaks": [{"center": 420.0, "assignment": "public-species"}],
            },
            "processed_estimate": {"peak_count": 1},
            "lab_report": {"spectra_summary": {"has_spectral_packet": True}},
        }
    }


def _composite_public_view() -> dict[str, Any]:
    return {
        "tool_json": {
            "available_actions": [{"operation": "terminate"}],
            "raw_signal": {
                "kind": "final_assay_packet",
                "channels": ["hplc", "nmr"],
                "spectra": {"hplc": {"peaks": [{"assignment": "target"}]}},
                "mass_balance": {"process_mass_balance_error": 0.0},
                "energy_efficiency": 0.72,
            },
            "processed_estimate": {
                "yield": 0.41,
                "peak_count": 3,
                "spectrum_assignment_confidence": 0.8,
            },
            "constraints": {"unsafe": False},
            "cost": 0.2,
            "lab_report": {
                "visible_metrics": {"yield": 0.41},
                "spectra_summary": {"has_spectral_packet": True},
                "campaign_state": {"remaining_budget": 4},
            },
        }
    }


def test_live_llm_consumes_spectra_and_carries_experiment_memory() -> None:
    client = FakeClient(
        [
            _decision({"operation": "terminate"}, evidence="public UV-Vis peak at 420 nm"),
            _decision({"operation": "heat", "target_temperature_K": 350.0, "duration_s": 60.0}),
        ]
    )
    agent = LiveLLMAgent(client, role_id="live_llm_a", spectrum_disclosure="assigned")
    agent.reset({"task_id": "flow-reaction-optimization"}, seed=7)

    first = agent.act_with_public_view(_context(step=1, previous=None), _public_view())
    agent.update(
        first,
        {"score": 0.2},
        0.0,
        {
            "experiment_ended": True,
            "leaderboard_score": 0.2,
            "observed_keys": ["score"],
        },
    )
    agent.act_with_public_view(
        _context(step=2, previous="experiment_end"),
        _public_view(),
    )

    assert client.prompts[0]["decision_context"]["latest_spectra"][
        "has_spectral_packet"
    ]
    assert client.prompts[1]["completed_experiment_memory"][0]["score"] == 0.2
    assert agent.decision_audit()["adaptation_source"] == "spectrum"  # type: ignore[index]
    usage = agent.method_resource_usage()
    assert usage["model_call_count"] == 4
    assert usage["input_token_count"] == 200
    assert usage["accounting_complete"] is True
    assert len(agent.agent_trace()) == 1


def test_masked_spectral_ablation_removes_raw_and_processed_spectral_features() -> None:
    client = FakeClient([_decision({"operation": "terminate"})])
    agent = LiveLLMAgent(client, role_id="live_llm_a", spectrum_disclosure="masked")
    agent.reset({"task_id": "flow-reaction-optimization"}, seed=2)

    agent.act_with_public_view(_context(step=1, previous=None), _public_view())

    prompt = client.prompts[0]
    assert prompt["decision_context"]["latest_spectra"] == {
        "spectrum_condition": "masked",
        "available": False,
    }
    assert "raw_signal" not in prompt["public_tool_view"]
    assert "peak_count" not in prompt["public_tool_view"]["processed_estimate"]
    assert "lab_report" not in prompt["public_tool_view"]
    assert agent.interaction_capabilities().consumes_spectra is False


def test_masked_ablation_preserves_non_spectral_composite_evidence() -> None:
    client = FakeClient([_decision({"operation": "terminate"})])
    agent = LiveLLMAgent(client, role_id="live_llm_a", spectrum_disclosure="masked")
    agent.reset({"task_id": "flow-reaction-optimization"}, seed=2)

    agent.act_with_public_view(
        _context(step=1, previous="measurement_result"),
        _composite_public_view(),
    )

    tool_view = client.prompts[0]["public_tool_view"]
    assert tool_view["raw_signal"] == {
        "kind": "final_assay_packet",
        "mass_balance": {"process_mass_balance_error": 0.0},
        "energy_efficiency": 0.72,
    }
    assert tool_view["processed_estimate"] == {"yield": 0.41}
    assert tool_view["constraints"] == {"unsafe": False}
    assert tool_view["cost"] == 0.2
    assert "lab_report" not in tool_view


def test_unassigned_condition_preserves_curve_but_removes_identity() -> None:
    client = FakeClient([_decision({"operation": "terminate"})])
    agent = LiveLLMAgent(client, role_id="live_llm_a", spectrum_disclosure="unassigned")
    agent.reset({"task_id": "flow-reaction-optimization"}, seed=2)

    agent.act_with_public_view(_context(step=1, previous=None), _public_view())

    prompt = client.prompts[0]
    peak = prompt["public_tool_view"]["raw_signal"]["peaks"][0]
    assert peak == {"center": 420.0, "assignment": "unassigned"}
    assert prompt["public_tool_view"]["processed_estimate"]["peak_count"] == 1
    assert agent.interaction_capabilities().consumes_spectra is True


def test_provider_failure_is_redacted_retained_and_counted() -> None:
    client = FakeClient([FakeProviderError()])
    agent = LiveLLMAgent(client, role_id="live_llm_a")
    agent.reset({"task_id": "flow-reaction-optimization"}, seed=3)

    action = agent.act_with_public_view(_context(step=1, previous=None), _public_view())

    assert action == {"operation": "model_failure"}
    assert agent.method_resource_usage()["model_call_count"] == 3
    serialized = json.dumps(agent.agent_trace())
    assert "secret transport detail" not in serialized
    assert "FakeProviderError" in serialized


def test_formal_unbillable_provider_failure_raises_resumable_interruption() -> None:
    client = FakeClient([FakeUnbillableProviderError()])
    agent = LiveLLMAgent(
        client,
        role_id="live_llm_a",
        fail_fast_on_unbillable_provider_failure=True,
    )
    agent.reset({"task_id": "flow-reaction-optimization"}, seed=3)

    with pytest.raises(LiveLLMProviderUnavailableError) as caught:
        agent.act_with_public_view(_context(step=1, previous=None), _public_view())

    assert caught.value.status_code == 402
    assert caught.value.retryable is False
    assert agent.method_resource_usage()["model_provenance"]["provider_failure_count"] == 1
    assert agent.provider_receipts()[0]["billable"] is False


def test_invalid_model_decision_does_not_double_count_provider_attempts() -> None:
    client = FakeClient([{"action": {"operation": "terminate"}}])
    agent = LiveLLMAgent(client, role_id="live_llm_a")
    agent.reset({"task_id": "flow-reaction-optimization"}, seed=3)

    action = agent.act_with_public_view(
        _context(step=1, previous=None), _public_view()
    )

    assert action == {"operation": "model_failure"}
    assert agent.method_resource_usage()["model_call_count"] == 2
    assert agent.method_resource_usage()["model_provenance"]["provider_failure_count"] == 1


def test_official_runner_ledgers_live_usage_and_replays_trajectory(tmp_path: Path) -> None:
    client = FakeClient(
        [
            _decision({"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}),
            _decision({"operation": "add_reagent", "amount_mol": 0.006}),
            _decision({"operation": "terminate"}),
            _decision({"operation": "measure", "instrument": "final_assay"}),
        ]
    )
    agent = LiveLLMAgent(client, role_id="live_llm_a")
    trajectory = tmp_path / "live.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=agent,
        world_split="public-test",
        budget=4,
        objective="balanced",
        seed=1200,
        task_id="flow-reaction-optimization",
        output_path=trajectory,
        budget_override=4,
        episode_mode_override="campaign",
        method_resource_limits={
            "operation_limit": 4,
            "complete_experiment_limit": 4,
            "wall_time_limit_s": 30.0,
            "model_call_limit": 12,
            "input_token_limit": 10_000,
            "output_token_limit": 10_000,
            "monetary_cost_limit_usd": 1.0,
        },
    )

    records = load_jsonl(trajectory)
    verified = verify_records(records)
    assert verified.verified, verified.mismatches
    assert len(history) == len(records) == 4
    assert records[-1]["method_resources"]["agent_usage"]["model_call_count"] == 8
    assert records[-1]["explanation"]["decision_audit"]["status"] == "provided"
    assert all(len(record["agent_trace"]) == 1 for record in records)
    prompt = client.prompts[0]
    assert len(json.dumps(prompt)) < 20_000
    assert prompt["task_contract"]["method_budget_contract"] == {
        "operation_limit": 4,
        "complete_experiment_limit": 4,
    }
    lifecycle = prompt["task_contract"]["experiment_lifecycle"]
    assert "does not by itself complete" in lifecycle["terminate_effect"]
    assert "instrument=final_assay" in lifecycle["final_assay_precondition"]
    assert "fresh experiment" in lifecycle["final_assay_effect"]
    assert prompt["task_contract"]["termination_policy"] == "budget"
    assert prompt["task_contract"]["success_metrics"] == [
        "score",
        "flow_conversion",
        "yield",
        "safety_risk",
    ]
    assert client.prompts[3]["decision_context"]["decision_stage"] == (
        "experiment_closeout"
    )
    assert "recommended_strategy" not in prompt["task_contract"]
    assert "runtime" not in prompt["task_contract"]
    assert "world_law" not in prompt["task_contract"]
    assert "constitution" not in prompt["task_contract"]


def test_official_runner_delivers_only_explicitly_requested_historical_spectrum(
    tmp_path: Path,
) -> None:
    request = _decision({"operation": "terminate"})
    request["request_historical_spectrum_id"] = "spectrum-e001-s0003"
    client = FakeClient(
        [
            _decision({"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}),
            _decision({"operation": "add_reagent", "amount_mol": 0.006}),
            _decision({"operation": "measure", "instrument": "hplc"}),
            request,
            _decision({"operation": "measure", "instrument": "final_assay"}),
        ]
    )
    agent = LiveLLMAgent(client, role_id="live_llm_a", spectrum_disclosure="assigned")

    run_agent(
        env_id="ChemWorld",
        agent=agent,
        world_split="public-test",
        budget=5,
        objective="balanced",
        seed=1200,
        task_id="flow-reaction-optimization",
        output_path=tmp_path / "history.jsonl",
        budget_override=5,
        episode_mode_override="campaign",
        method_resource_limits={
            "operation_limit": 5,
            "complete_experiment_limit": 5,
            "wall_time_limit_s": 30.0,
            "model_call_limit": 15,
            "input_token_limit": 10_000,
            "output_token_limit": 10_000,
            "monetary_cost_limit_usd": 1.0,
        },
    )

    assert client.prompts[2]["public_tool_view"]["historical_spectrum_catalog"] == []
    catalog = client.prompts[3]["public_tool_view"]["historical_spectrum_catalog"]
    assert [item["spectrum_id"] for item in catalog] == ["spectrum-e001-s0003"]
    assert "requested_historical_spectrum" not in client.prompts[3]["public_tool_view"]
    retrieved = client.prompts[4]["public_tool_view"]["requested_historical_spectrum"]
    assert retrieved["status"] == "retrieved"
    assert retrieved["spectrum_id"] == "spectrum-e001-s0003"
    assert retrieved["raw_signal"]["kind"] == "hplc_chromatogram"
