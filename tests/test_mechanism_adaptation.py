from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.mechanism_adaptation_live_llm import (
    MechanismAdaptationLiveLLMAgent,
    MechanismCandidateSpec,
)
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.mechanism_adaptation import (
    GaussianMechanismOracle,
    OutcomeLayers,
    active_oracle_diagnosis,
    build_paired_campaign_matrix,
    campaign_autonomy_status,
    change_detection_summary,
    conditional_changed_family_distribution,
    declared_change_probability,
    declared_distribution_update,
    evaluate_protocol_gates,
    feedback_effect_summary,
    fixed_trajectory_decode,
    identifiability_certificate,
    operation_aware_action_distance,
    recovery_decomposition,
    validate_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_adaptation_preflight import (
    build_mechanism_adaptation_preflight,
)

ROOT = Path(__file__).resolve().parents[1]


class _FakeClient:
    model = "deepseek-v4-flash"
    thinking = False
    reasoning_effort = None

    def complete_json(self, **_: Any) -> Any:
        raise AssertionError("tests call prompt construction or normalization directly")

    def pricing_snapshot(self) -> dict[str, Any]:
        return {"access_date": "test"}

    def estimate_cost_usd(self, _: dict[str, Any]) -> float:
        return 0.0


def _context() -> AgentDecisionContext:
    return AgentDecisionContext(
        step=1,
        task_id="reaction-to-crystallization",
        decision_stage="experiment_control",
        campaign_state={"remaining_budget": 10, "experiment_index": 0},
        visible_metrics={},
        latest_spectra={},
        uncertainty={},
        constraint_flags={},
        available_operations=("measure",),
        previous_event_type="operation_result",
    )


def _agent(*, label_mode: str = "semantic") -> MechanismAdaptationLiveLLMAgent:
    agent = MechanismAdaptationLiveLLMAgent(
        _FakeClient(),
        role_id="test",
        candidate_specs=(
            MechanismCandidateSpec("no_change", "The hidden law is unchanged."),
            MechanismCandidateSpec("rate_law_family", "Rate dependence changes."),
        ),
        candidate_label_mode=label_mode,  # type: ignore[arg-type]
        candidate_order_seed=19,
    )
    agent.reset({"task_id": "reaction-to-crystallization", "episode_mode": "campaign"}, 7)
    return agent


def test_mechanism_distribution_has_one_derived_change_probability() -> None:
    distribution = {"no_change": 0.25, "rate_law_family": 0.5, "topology_family": 0.25}
    assert declared_change_probability(distribution) == pytest.approx(0.75)
    assert conditional_changed_family_distribution(distribution) == {
        "rate_law_family": pytest.approx(2.0 / 3.0),
        "topology_family": pytest.approx(1.0 / 3.0),
    }


def test_declared_update_is_distribution_change_not_calibrated_eig() -> None:
    update = declared_distribution_update(
        {"no_change": 0.8, "shift": 0.2},
        {"no_change": 0.2, "shift": 0.8},
        truth="shift",
    )
    assert update["declared_distribution_js_shift"] > 0.0
    assert update["truth_log_probability_change"] > 0.0
    assert update["brier_improvement"] > 0.0


def test_change_detection_requires_and_scores_no_change_twins() -> None:
    result = change_detection_summary(
        changed=[True, True, False, False],
        probabilities=[0.9, 0.8, 0.1, 0.2],
        detection_delays=[1, 2, None, None],
    )
    assert result["sensitivity"] == 1.0
    assert result["false_positive_rate"] == 0.0
    assert result["auroc"] == 1.0
    assert result["no_change_twin_count"] == 2
    with pytest.raises(ValueError, match="changed and no-change"):
        change_detection_summary(
            changed=[True],
            probabilities=[0.9],
            detection_delays=[1],
        )


def test_feedback_action_recovery_and_autonomy_decompositions() -> None:
    feedback = feedback_effect_summary(
        within_condition_distances=[0.1, 0.2],
        between_condition_distances=[0.5, 0.6],
    )
    assert feedback["net_feedback_effect"] == pytest.approx(0.4)
    different = operation_aware_action_distance(
        {"operation": "heat", "temperature_K": 330.0},
        {"operation": "measure", "instrument": "hplc"},
    )
    assert different["parameter_distance"] is None
    same = operation_aware_action_distance(
        {"operation": "heat", "temperature_K": 330.0},
        {"operation": "heat", "temperature_K": 350.0},
        parameter_bounds={"temperature_K": (300.0, 400.0)},
    )
    assert same["parameter_distance"] == pytest.approx(0.2)
    recovery = recovery_decomposition(
        iid_replay_iid_world=0.8,
        iid_replay_shifted_world=0.4,
        frozen_policy_shifted_world=0.45,
        adaptive_policy_shifted_world=0.65,
        oracle_shifted_world=0.85,
    )
    assert recovery["world_effect"] == pytest.approx(-0.4)
    assert recovery["adaptation_gain"] == pytest.approx(0.2)
    assert recovery["normalized_recovery"] == pytest.approx(0.5)
    assert (
        campaign_autonomy_status(
            current_experiment_autonomous=True,
            assisted_history=True,
            campaign_complete=True,
        )
        == "autonomous_current_experiment_with_assisted_history"
    )


def test_outcome_layers_do_not_conflate_visible_and_evaluation_values() -> None:
    layers = OutcomeLayers(
        environment_outcome={"score": 0.8},
        agent_visible_observation={"score": 0.2},
        evaluation_outcome={"score": 0.8},
    ).to_dict()
    assert layers["agent_visible_observation"] != layers["evaluation_outcome"]


def test_gaussian_oracle_supports_active_and_fixed_trajectory_diagnosis() -> None:
    def sample(candidate: str, action: str, seed: int) -> list[float]:
        rng = np.random.default_rng(seed)
        mean = 0.0
        if action == "diagnostic":
            mean = -2.0 if candidate == "no_change" else 2.0
        return [float(rng.normal(mean, 0.2))]

    oracle = GaussianMechanismOracle(
        candidate_ids=("no_change", "shift"),
        action_ids=("uninformative", "diagnostic"),
        sample_public_observation=sample,
        samples_per_candidate=64,
        seed=3,
    )
    oracle.fit_predictives()
    exported = oracle.export_predictives()
    reloaded = GaussianMechanismOracle(
        candidate_ids=("no_change", "shift"),
        action_ids=("uninformative", "diagnostic"),
        sample_public_observation=sample,
        samples_per_candidate=4,
        seed=3,
    )
    reloaded.load_predictives(exported)
    assert set(reloaded.expected_information_by_action(draws=8)) == {
        "uninformative",
        "diagnostic",
    }
    assert oracle.select_action(draws=64) == "diagnostic"
    active = active_oracle_diagnosis(
        oracle,
        observe=lambda action, index: sample("shift", action, 100 + index),
        budget=2,
        information_draws=64,
    )
    assert active["prediction"] == "shift"
    decoded = fixed_trajectory_decode(
        oracle,
        action_ids=["diagnostic"],
        observations=[[2.0]],
    )
    assert decoded["prediction"] == "shift"


def test_identifiability_certificate_uses_confidence_bounds() -> None:
    truths = ["a"] * 100 + ["b"] * 100
    certificate = identifiability_certificate(
        truths=truths,
        predictions=truths,
        candidate_ids=("a", "b"),
    )
    assert certificate["gate_pass"] is True
    assert certificate["top1_accuracy_interval"][0] > 0.95


def test_v0_2_1_protocol_is_frozen_but_empirical_gates_are_not_pretended_passed() -> None:
    protocol = json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_v0.2.1.json").read_text(
            encoding="utf-8"
        )
    )
    assert validate_mechanism_adaptation_protocol(protocol) == []
    result = evaluate_protocol_gates(protocol, {})
    assert result["publication_ready"] is False
    assert result["missing_or_failed_gates"] == [
        "gate_0",
        "gate_a",
        "gate_b",
        "gate_c",
        "gate_d",
        "gate_e",
    ]
    matrix = build_paired_campaign_matrix(protocol)
    changed_candidate_count = sum(
        len(contract["candidate_ids"]) - 1
        for contract in protocol["task_mechanism_contracts"].values()
    )
    change_time_count = sum(
        item != "never" for item in protocol["design"]["change_after_experiments"]
    )
    expected_rows = (
        changed_candidate_count
        * change_time_count
        * len(protocol["diagnosis_contract"]["candidate_label_modes"])
        * len(protocol["design"]["public_development_seeds"])
        * len(protocol["design"]["candidate_order_seeds"])
        * 2
    )
    assert len(matrix) == expected_rows == 2400
    pair_ids = {row["pair_id"] for row in matrix}
    assert len(pair_ids) == expected_rows // 2
    for pair_id in pair_ids:
        arms = [row for row in matrix if row["pair_id"] == pair_id]
        assert {row["arm"] for row in arms} == {"changed", "no_change_twin"}
        assert len({row["world_seed"] for row in arms}) == 1
        assert len({row["candidate_order_seed"] for row in arms}) == 1


def test_every_v0_2_1_intervention_is_instantiable_by_the_current_environment() -> None:
    protocol = json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_v0.2.1.json").read_text(
            encoding="utf-8"
        )
    )
    for task_id, contract in protocol["task_mechanism_contracts"].items():
        for interventions in contract["interventions"].values():
            environment = ChemWorldEnv(
                task_id=task_id,
                seed=0,
                world_interventions=tuple(interventions),
            )
            try:
                environment.reset(seed=0)
                assert environment.task_info()["task_id"] == task_id
            finally:
                environment.close()


def test_v0_2_1_preflight_separates_method_freeze_from_external_execution() -> None:
    report = build_mechanism_adaptation_preflight()
    assert report["implementation_complete"] is True
    assert report["design_validity_audit_pass"] is True
    assert report["method_freeze_decision_blocker_count"] == 0
    assert report["external_empirical_run_completed"] is False
    assert set(report["empirical_gate_status"].values()) == {"not_evaluated"}
    assert report["publication_ready"] is False


def test_v0_2_agent_defines_randomizes_and_anonymizes_candidates_without_derived_leakage() -> None:
    agent = _agent(label_mode="anonymous")
    prompt = json.loads(agent._build_prompt(_context(), {"tool_json": {}}))
    candidates = prompt["mechanism_diagnostic_contract"]["candidates"]
    assert {item["label"] for item in candidates} == {"H1", "H2"}
    assert all(item["definition"] for item in candidates)
    assert "change_probability" not in json.dumps(prompt["required_json_shape"])
    public_labels = [item["label"] for item in candidates]
    payload = {
        "action": {"operation": "measure", "instrument": "hplc"},
        "evidence": ["public measurement"],
        "spectrum_interpretation": "No spectrum available.",
        "hypothesis": "The measurement separates candidates.",
        "uncertainty": 0.5,
        "rationale": "Collect diagnostic evidence.",
        "request_historical_spectrum_id": None,
        "mechanism_report": {
            "mechanism_distribution": {
                public_labels[0]: 0.7,
                public_labels[1]: 0.3,
            },
            "declared_information_value": 0.4,
            "diagnostic_rationale": "Separate stable from changed rate dependence.",
        },
    }
    decision = agent._normalize_decision(payload, context=_context())
    agent._last_decision = decision
    derived = agent.derived_diagnostics()
    assert derived is not None
    assert derived["change_probability"] == pytest.approx(
        1.0 - decision["mechanism_distribution"]["no_change"]
    )
