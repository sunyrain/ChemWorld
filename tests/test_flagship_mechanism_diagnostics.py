from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from chemworld.agents.base import BaseAgent
from chemworld.agents.diagnostic_live_llm import MechanismDiagnosticLiveLLMAgent
from chemworld.agents.interaction import AgentDecisionContext, InteractionCapabilities
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.flagship_diagnostics import (
    DIAGNOSTIC_REPORT_VERSION,
    ContinuingPublicViewAgent,
    build_flagship_diagnostic_report,
    load_flagship_diagnostic_protocol,
    render_flagship_diagnostic_markdown,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario


class _FakeClient:
    model = "deepseek-v4-flash"
    thinking = False
    reasoning_effort = None

    def complete_json(self, **_: Any) -> Any:
        raise AssertionError("the unit test calls normalization directly")

    def pricing_snapshot(self) -> dict[str, Any]:
        return {"access_date": "test"}

    def estimate_cost_usd(self, _: dict[str, Any]) -> float:
        return 0.0


class _RecordingPublicAgent(BaseAgent):
    name = "recording_public"

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.contexts: list[AgentDecisionContext] = []
        self.updates: list[tuple[dict[str, float | None], float, dict[str, Any]]] = []

    def act_with_public_view(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> dict[str, Any]:
        del public_view
        self.contexts.append(context)
        return {"operation": "measure", "instrument": "hplc"}

    def act(self, history: list[Any]) -> dict[str, Any]:
        del history
        raise AssertionError("public-view path required")

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        del action
        self.updates.append((copy.deepcopy(observation), reward, copy.deepcopy(info)))

    def interaction_capabilities(self) -> InteractionCapabilities:
        return InteractionCapabilities(
            consumes_intermediate_observations=True,
            adapts_within_experiment=True,
        )


def _context(*, score: float, experiment_index: int = 0) -> AgentDecisionContext:
    return AgentDecisionContext(
        step=1,
        task_id="reaction-to-crystallization",
        decision_stage="evidence_update",
        campaign_state={
            "remaining_budget": 10,
            "experiment_index": experiment_index,
            "final_assay_count": experiment_index,
            "operation_count": 1,
        },
        visible_metrics={"score": score},
        latest_spectra={"has_spectral_packet": True, "target_fraction": score},
        uncertainty={"score": 0.1},
        constraint_flags={},
        available_operations=("measure",),
        previous_event_type="measurement_result",
    )


def _view(score: float) -> dict[str, Any]:
    return {
        "observation": {"score": score},
        "lab_report": {
            "visible_metrics": {"score": score},
            "spectra_summary": {"has_spectral_packet": True},
        },
        "tool_json": {
            "observation": {"score": score},
            "uncertainty": {"score": 0.1},
            "available_actions": [],
            "lab_report": {
                "visible_metrics": {"score": score},
                "spectra_summary": {"has_spectral_packet": True},
            },
        },
    }


def _info(score: float, experiment_index: int) -> dict[str, Any]:
    return {
        "experiment_index": experiment_index,
        "operation_type": "measure",
        "transaction_status": "committed",
        "leaderboard_score": score,
        "observed_keys": ["score"],
        "observed_mask": {"score": True},
        "constraint_flags": {},
        "experiment_ended": False,
    }


@pytest.mark.parametrize(
    ("task_id", "material_field", "permutation"),
    [
        ("reaction-to-crystallization", "catalyst", [0, 2, 1, 3]),
        ("electrochemical-conversion", "solvent", [2, 1, 0, 3]),
    ],
)
def test_material_law_counterfactual_swaps_hidden_rows_only(
    task_id: str,
    material_field: str,
    permutation: list[int],
) -> None:
    spec = get_scenario(task_id, split="public-test")
    generator = DefaultScenarioGenerator()
    baseline = generator.generate(spec, 0)
    counterfactual = generator.generate(
        spec,
        0,
        (
            {
                "kind": "material_law_counterfactual",
                "material_field": material_field,
                "public_to_baseline": permutation,
            },
        ),
    )
    selected_baseline = (
        baseline.parameters.catalyst_effects
        if material_field == "catalyst"
        else baseline.parameters.solvent_effects
    )
    selected_counterfactual = (
        counterfactual.parameters.catalyst_effects
        if material_field == "catalyst"
        else counterfactual.parameters.solvent_effects
    )
    np.testing.assert_allclose(
        selected_counterfactual,
        selected_baseline[np.asarray(permutation), :],
    )
    np.testing.assert_allclose(
        baseline.parameters.solvent_costs,
        counterfactual.parameters.solvent_costs,
    )
    np.testing.assert_allclose(
        baseline.parameters.solvent_risks,
        counterfactual.parameters.solvent_risks,
    )
    np.testing.assert_allclose(
        baseline.parameters.catalyst_costs,
        counterfactual.parameters.catalyst_costs,
    )
    assert baseline.compiled_mechanism.mechanism_hash == (
        counterfactual.compiled_mechanism.mechanism_hash
    )
    assert "material_law_counterfactual_hash" in counterfactual.initial_state.metadata
    assert "public_to_baseline" not in counterfactual.initial_state.metadata

    baseline_env = ChemWorldEnv(task_id=task_id, seed=0)
    variant_env = ChemWorldEnv(
        task_id=task_id,
        seed=0,
        world_interventions=(
            {
                "kind": "material_law_counterfactual",
                "material_field": material_field,
                "public_to_baseline": permutation,
            },
        ),
    )
    try:
        baseline_env.reset(seed=0)
        variant_env.reset(seed=0)
        assert (
            baseline_env.task_info()["material_catalog"]
            == (variant_env.task_info()["material_catalog"])
        )
        assert baseline_env.action_space == variant_env.action_space
    finally:
        baseline_env.close()
        variant_env.close()


def test_material_law_counterfactual_rejects_identity_and_wrong_length() -> None:
    spec = get_scenario("reaction-to-crystallization", split="public-test")
    generator = DefaultScenarioGenerator()
    with pytest.raises(ValueError, match="non-identity"):
        generator.generate(
            spec,
            0,
            (
                {
                    "kind": "material_law_counterfactual",
                    "material_field": "catalyst",
                    "public_to_baseline": [0, 1, 2, 3],
                },
            ),
        )
    with pytest.raises(ValueError, match="length"):
        generator.generate(
            spec,
            0,
            (
                {
                    "kind": "material_law_counterfactual",
                    "material_field": "catalyst",
                    "public_to_baseline": [1, 0],
                },
            ),
        )


def test_permuted_feedback_changes_agent_input_but_retains_true_score_log() -> None:
    delegate = _RecordingPublicAgent()
    adapter = ContinuingPublicViewAgent(
        delegate,
        method_id="deepseek_v4_flash",
        feedback_condition="permuted_feedback",
        critical_instrument="hplc",
    )
    adapter.begin_phase("iid", experiment_offset=0, operation_offset=0)
    adapter.reset({"task_id": "reaction-to-crystallization"}, 0)
    for experiment, score in enumerate((0.2, 0.8)):
        adapter.act_with_public_view(
            _context(score=score, experiment_index=experiment),
            _view(score),
        )
        adapter.update(
            {"operation": "measure", "instrument": "hplc"},
            {"score": score},
            score,
            _info(score, experiment),
        )
    adapter.begin_phase("shifted", experiment_offset=2, operation_offset=2)
    adapter.reset({"task_id": "reaction-to-crystallization"}, 0)
    adapter.act_with_public_view(_context(score=0.95), _view(0.95))
    adapter.update(
        {"operation": "measure", "instrument": "hplc"},
        {"score": 0.95},
        0.95,
        _info(0.95, 0),
    )

    delivered_observation, delivered_reward, delivered_info = delegate.updates[-1]
    assert delivered_observation["score"] in {0.2, 0.8}
    assert delivered_observation["score"] != 0.95
    assert delivered_reward in {0.2, 0.8}
    assert delivered_info["leaderboard_score"] in {0.2, 0.8}
    assert (
        adapter.feedback_intervention_log[-1]["true_environment_score_retained_for_evaluation"]
        == 0.95
    )


def test_diagnostic_live_llm_requires_normalized_mechanism_belief() -> None:
    agent = MechanismDiagnosticLiveLLMAgent(
        _FakeClient(),
        role_id="test",
        mechanism_candidates=("no_change", "rate_law_family"),
    )
    payload: dict[str, Any] = {
        "action": {"operation": "measure", "instrument": "hplc"},
        "evidence": ["score changed"],
        "spectrum_interpretation": "target fraction changed",
        "hypothesis": "the rate law may have changed",
        "uncertainty": 0.4,
        "rationale": "measure before changing the recipe",
        "diagnostic_report": {
            "mechanism_belief": {"no_change": 0.25, "rate_law_family": 0.75},
            "change_probability": 0.75,
            "expected_information_gain": 0.8,
            "diagnostic_measurement_rationale": "distinguish stable from shifted kinetics",
        },
    }
    decision = agent._normalize_decision(payload, context=_context(score=0.2))
    assert decision["mechanism_prediction"] == "rate_law_family"
    assert decision["change_probability"] == 0.75
    assert sum(decision["mechanism_belief"].values()) == pytest.approx(1.0)

    malformed = copy.deepcopy(payload)
    malformed["diagnostic_report"]["mechanism_belief"] = {
        "no_change": 0.9,
        "rate_law_family": 0.9,
    }
    with pytest.raises(ValueError, match="sum to one"):
        agent._normalize_decision(malformed, context=_context(score=0.2))


def test_protocol_covers_four_experiments_and_two_flagship_tasks() -> None:
    protocol = load_flagship_diagnostic_protocol()
    assert protocol["schema_version"] == DIAGNOSTIC_REPORT_VERSION
    assert set(protocol["tasks"]) == {
        "reaction-to-crystallization",
        "electrochemical-conversion",
    }
    assert set(protocol["feedback_conditions"]) == {
        "true_feedback",
        "permuted_feedback",
        "delayed_feedback",
        "critical_measurement_deleted",
    }
    assert protocol["pre_change_experiments"] == 2
    assert protocol["post_change_experiments"] == 2
    assert protocol["closeout_headroom_per_experiment"] == 6
    assert "ppo_diagnostic" not in protocol["ranking_methods"]
    assert "ppo_diagnostic" in protocol["excluded_methods"]
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["publication_ready"] is False


def _write_trace(path: Path, truth: str) -> None:
    rows = [
        {
            "experiment_index": 0,
            "operation_type": "measure",
            "instrument": "hplc",
            "agent_trace": [
                {
                    "mechanism_belief": {"no_change": 0.6, truth: 0.4},
                    "mechanism_prediction": "no_change",
                    "change_probability": 0.4,
                    "expected_information_gain": 0.8,
                }
            ],
        },
        {
            "experiment_index": 1,
            "operation_type": "measure",
            "instrument": "final_assay",
            "agent_trace": [
                {
                    "mechanism_belief": {"no_change": 0.2, truth: 0.8},
                    "mechanism_prediction": truth,
                    "change_probability": 0.8,
                    "expected_information_gain": 0.2,
                }
            ],
        },
    ]
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def test_report_separates_outcome_and_mechanism_understanding(tmp_path: Path) -> None:
    protocol = load_flagship_diagnostic_protocol()
    truth = "rate_law_family"
    iid_path = tmp_path / "iid.jsonl"
    shifted_path = tmp_path / "shifted.jsonl"
    _write_trace(iid_path, truth)
    _write_trace(shifted_path, truth)
    campaign = {
        "campaign_id": "synthetic",
        "experiment_id": "ranking_shift",
        "task_id": "reaction-to-crystallization",
        "method_id": "deepseek_v4_flash",
        "feedback_condition": "true_feedback",
        "shifted_truth_id": truth,
        "iid": {
            "trajectory_path": str(iid_path),
            "complete_experiment_count": 2,
            "scores": [0.5, 0.6],
            "mean_score": 0.55,
            "best_score": 0.6,
        },
        "shifted": {
            "trajectory_path": str(shifted_path),
            "complete_experiment_count": 2,
            "scores": [0.58, 0.62],
            "mean_score": 0.6,
            "best_score": 0.62,
        },
        "full_method_resources": {},
    }
    report = build_flagship_diagnostic_report(protocol, [campaign])
    diagnostic = report["campaigns"][0]["deepseek_diagnostic"]
    assert diagnostic["mechanism_identified"] is True
    assert diagnostic["final_outcome_high"] is True
    assert diagnostic["outcome_understanding_type"] == "genuine_experimental"
    assert diagnostic["change_detection_experiment"] == 2
    assert report["benchmark_claim_allowed"] is False
    markdown = render_flagship_diagnostic_markdown(report)
    assert "结果与机制理解解耦" in markdown
    assert "genuine_experimental" in markdown
