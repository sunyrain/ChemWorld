from __future__ import annotations

from pathlib import Path

import pytest
from scripts.qualify_static_s0_five_tasks import (
    _load_object,
    _participant_protocol,
    _participant_provider_matches,
    _recipe_design_checks,
    _strengthened_baseline_readiness,
    _task_protocol,
)

from chemworld.eval.static_optimization_protocol import (
    validate_development_seed_policy,
    validate_static_optimization_protocol,
)
from chemworld.tasks import get_task
from chemworld.world.scoring import TaskScoringContract

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs/benchmark/static_s0_five_task_single_seed_qualification_v0.1_dev.json"
STRENGTHENED_PLAN_PATH = (
    ROOT / "configs/benchmark/static_s0_five_task_single_seed_qualification_v0.2_dev.json"
)
PORTFOLIO_PLAN_PATH = (
    ROOT / "configs/benchmark/static_s0_five_task_single_seed_qualification_v0.3_dev.json"
)
NONDUPLICATE_PORTFOLIO_PLAN_PATH = (
    ROOT / "configs/benchmark/static_s0_five_task_single_seed_qualification_v0.4_dev.json"
)
SCHEDULED_PORTFOLIO_PLAN_PATH = (
    ROOT / "configs/benchmark/static_s0_five_task_single_seed_qualification_v0.5_dev.json"
)
EXPECTED_TASK_IDS = [
    "electrochemical-conversion",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "partition-discovery",
    "flow-reaction-optimization",
]


def test_five_task_qualification_plan_is_seed0_only() -> None:
    plan = _load_object(PLAN_PATH)

    assert plan["task_ids"] == EXPECTED_TASK_IDS
    assert list(plan["tasks"]) == EXPECTED_TASK_IDS
    assert plan["seed_policy"] == {
        "world_seeds": [0],
        "algorithm_seeds": [0],
        "multi_seed_execution_allowed": False,
        "release_condition": (
            "every task must pass every single-seed qualification gate before "
            "any multi-seed execution"
        ),
    }
    for task_id in EXPECTED_TASK_IDS:
        protocol = _task_protocol(plan, task_id)
        validate_static_optimization_protocol(protocol)
        validate_development_seed_policy(protocol, algorithm_seed=0)
        with pytest.raises(ValueError, match="algorithm seed is outside"):
            validate_development_seed_policy(protocol, algorithm_seed=1)


def test_strengthened_qualification_adds_shared_participant_gates_without_more_seeds() -> None:
    plan = _load_object(STRENGTHENED_PLAN_PATH)

    assert plan["task_ids"] == EXPECTED_TASK_IDS
    assert plan["seed_policy"]["world_seeds"] == [0]
    assert plan["seed_policy"]["algorithm_seeds"] == [0]
    assert plan["seed_policy"]["multi_seed_execution_allowed"] is False
    assert plan["participant"] == {
        "provider": "codex_subscription",
        "method_config_path": (
            "configs/methods/llm_v1.6/"
            "participant_methods_s0_codex_subscription_sol_five_task_seed0_v16.json"
        ),
        "method_id": (
            "s0_codex_subscription_sol_medium_five_task_shared_seed0_v16"
        ),
        "shared_task_neutral_scaffold": True,
        "task_specific_hidden_guidance": False,
    }
    gates = plan["qualification_gates"]
    assert (
        gates[
            "at_least_two_adaptive_baseline_families_reach_validated_threshold"
        ]
        is True
    )
    assert gates["best_baseline_validated_threshold_margin_at_least"] == pytest.approx(
        0.02
    )
    assert gates["participant_initial_continuous_extremes_covered"] is True
    assert gates["participant_initial_nominal_categories_covered"] is True
    assert gates["participant_initial_nominal_pairs_maximally_distinct"] is True
    assert gates["participant_first_eight_recipes_committed_by_protocol_executor"] is True
    assert gates["participant_remaining_twelve_recipes_selected_by_model"] is True
    assert gates["participant_validated_threshold_reached"] is True
    assert gates["participant_regret_to_best_baseline_at_most"] == pytest.approx(0.06)
    assert "lowering a frozen task threshold" in plan["claim_boundary"]

    for task_id in EXPECTED_TASK_IDS:
        protocol = _task_protocol(plan, task_id)
        validate_static_optimization_protocol(protocol)
        validate_development_seed_policy(protocol, algorithm_seed=0)
        participant_protocol = _participant_protocol(plan, task_id)
        validate_static_optimization_protocol(participant_protocol)
        validate_development_seed_policy(participant_protocol, algorithm_seed=0)
        assert participant_protocol["world_policy"]["world_seed"] == 0
        assert participant_protocol["candidate_order_seed"] == 0
        assert participant_protocol["method_ids"] == [plan["participant"]["method_id"]]
        assert participant_protocol["final_synthesis"]["calls"] == 1
        assert (
            participant_protocol["reward_contract"]["final_selection"]
            == "committed_model_final_recommendation"
        )


def test_portfolio_qualification_keeps_model_authority_and_hidden_world_boundary() -> None:
    plan = _load_object(PORTFOLIO_PLAN_PATH)

    assert plan["task_ids"] == EXPECTED_TASK_IDS
    assert plan["seed_policy"]["world_seeds"] == [0]
    assert plan["seed_policy"]["multi_seed_execution_allowed"] is False
    assert plan["observation_noise_namespace_base"] == (
        "static-s0-five-task-single-seed-qualification-v0.2-2026-07-30"
    )
    assert plan["participant"] == {
        "provider": "codex_subscription",
        "method_config_path": (
            "configs/methods/llm_v1.7/"
            "participant_methods_s0_codex_subscription_sol_five_task_seed0_v17.json"
        ),
        "method_id": (
            "s0_codex_subscription_sol_medium_five_task_shared_seed0_v17"
        ),
        "shared_task_neutral_scaffold": True,
        "task_specific_hidden_guidance": False,
    }
    gates = plan["qualification_gates"]
    assert (
        gates[
            "participant_experiments_9_through_17_selected_by_model_from_public_history_portfolio"
        ]
        is True
    )
    assert gates["participant_experiments_18_through_20_freely_selected_by_model"] is True
    assert gates["participant_candidate_generation_uses_no_hidden_world_fields"] is True
    assert gates["participant_provider_matches_frozen_provider"] is True
    assert gates["participant_remaining_twelve_recipes_selected_by_model"] is True
    assert "does not use hidden world fields" in plan["claim_boundary"]
    assert "model selects every recipe after experiment eight" in plan["claim_boundary"]

    for task_id in EXPECTED_TASK_IDS:
        baseline_protocol = _task_protocol(plan, task_id)
        participant_protocol = _participant_protocol(plan, task_id)
        validate_static_optimization_protocol(baseline_protocol)
        validate_static_optimization_protocol(participant_protocol)
        assert "qualification-0.3-s0-dev" in participant_protocol["schema_version"]
        assert participant_protocol["world_policy"]["world_seed"] == 0
        assert participant_protocol["observation_noise_namespace"] == (
            "static-s0-five-task-single-seed-qualification-v0.2-2026-07-30"
            f"--{task_id}"
        )


def test_mock_provider_cannot_satisfy_frozen_participant_provider_gate() -> None:
    plan = _load_object(PORTFOLIO_PLAN_PATH)

    assert _participant_provider_matches(
        plan,
        {"provider_mode": "codex_subscription"},
    )
    assert not _participant_provider_matches(
        plan,
        {"provider_mode": "mock"},
    )


def test_nonduplicate_portfolio_qualification_keeps_all_model_rounds_bound() -> None:
    plan = _load_object(NONDUPLICATE_PORTFOLIO_PLAN_PATH)

    assert plan["task_ids"] == EXPECTED_TASK_IDS
    assert plan["seed_policy"]["world_seeds"] == [0]
    assert plan["seed_policy"]["multi_seed_execution_allowed"] is False
    assert plan["observation_noise_namespace_base"] == (
        "static-s0-five-task-single-seed-qualification-v0.2-2026-07-30"
    )
    assert plan["participant"] == {
        "provider": "codex_subscription",
        "method_config_path": (
            "configs/methods/llm_v1.8/"
            "participant_methods_s0_codex_subscription_sol_five_task_seed0_v18.json"
        ),
        "method_id": (
            "s0_codex_subscription_sol_medium_five_task_shared_seed0_v18"
        ),
        "shared_task_neutral_scaffold": True,
        "task_specific_hidden_guidance": False,
    }
    gates = plan["qualification_gates"]
    assert (
        gates[
            "participant_experiments_9_through_20_selected_by_model_from_public_history_portfolio"
        ]
        is True
    )
    assert gates["participant_all_twenty_exploration_recipes_distinct"] is True
    assert gates["participant_remaining_twelve_recipes_selected_by_model"] is True
    assert gates["participant_candidate_generation_uses_no_hidden_world_fields"] is True
    assert gates["participant_provider_matches_frozen_provider"] is True
    assert "Blind validation, not campaign duplication" in plan["claim_boundary"]
    assert "model selects every recipe after experiment eight" in plan["claim_boundary"]

    for task_id in EXPECTED_TASK_IDS:
        baseline_protocol = _task_protocol(plan, task_id)
        participant_protocol = _participant_protocol(plan, task_id)
        validate_static_optimization_protocol(baseline_protocol)
        validate_static_optimization_protocol(participant_protocol)
        assert "qualification-0.4-s0-dev" in participant_protocol["schema_version"]
        assert participant_protocol["world_policy"]["world_seed"] == 0
        assert participant_protocol["observation_noise_namespace"] == (
            "static-s0-five-task-single-seed-qualification-v0.2-2026-07-30"
            f"--{task_id}"
        )


def test_scheduled_portfolio_qualification_reports_recipe_authority_honestly() -> None:
    plan = _load_object(SCHEDULED_PORTFOLIO_PLAN_PATH)

    assert plan["task_ids"] == EXPECTED_TASK_IDS
    assert plan["seed_policy"]["world_seeds"] == [0]
    assert plan["seed_policy"]["multi_seed_execution_allowed"] is False
    assert plan["observation_noise_namespace_base"] == (
        "static-s0-five-task-single-seed-qualification-v0.2-2026-07-30"
    )
    assert plan["participant"] == {
        "provider": "codex_subscription",
        "method_config_path": (
            "configs/methods/llm_v1.9/"
            "participant_methods_s0_codex_subscription_sol_five_task_seed0_v19.json"
        ),
        "method_id": (
            "s0_codex_subscription_sol_medium_five_task_shared_seed0_v19"
        ),
        "shared_task_neutral_scaffold": True,
        "task_specific_hidden_guidance": False,
    }
    gates = plan["qualification_gates"]
    assert (
        gates[
            "participant_experiments_9_through_20_committed_by_public_task_neutral_schedule"
        ]
        is True
    )
    assert gates["participant_model_call_consumed_for_every_experiment"] is True
    assert gates["participant_all_twenty_exploration_recipes_distinct"] is True
    assert gates["participant_candidate_generation_uses_no_hidden_world_fields"] is True
    assert "not the language model, commits all 20" in plan["claim_boundary"]
    assert (
        "must not be described as language-model recipe-selection performance"
        in plan["claim_boundary"]
    )

    for task_id in EXPECTED_TASK_IDS:
        baseline_protocol = _task_protocol(plan, task_id)
        participant_protocol = _participant_protocol(plan, task_id)
        validate_static_optimization_protocol(baseline_protocol)
        validate_static_optimization_protocol(participant_protocol)
        assert "qualification-0.5-s0-dev" in participant_protocol["schema_version"]
        assert participant_protocol["world_policy"]["world_seed"] == 0
        assert participant_protocol["observation_noise_namespace"] == (
            "static-s0-five-task-single-seed-qualification-v0.2-2026-07-30"
            f"--{task_id}"
        )


def test_strengthened_baseline_gate_distinguishes_adaptive_readiness_from_controls() -> None:
    plan = _load_object(STRENGTHENED_PLAN_PATH)
    flow = _strengthened_baseline_readiness(
        plan=plan,
        task_id="flow-reaction-optimization",
        task_report={
            "validated_scores_by_algorithm": {
                "random": 0.1686,
                "lhs": 0.1585,
                "greedy": 0.2061,
                "structured_gp_ei": 0.2123,
                "structured_rf_ei": 0.1754,
            }
        },
    )
    partition = _strengthened_baseline_readiness(
        plan=plan,
        task_id="partition-discovery",
        task_report={
            "validated_scores_by_algorithm": {
                "random": 0.5548,
                "lhs": 0.5518,
                "greedy": 0.5810,
                "structured_gp_ei": 0.5599,
                "structured_rf_ei": 0.5637,
            }
        },
    )

    assert all(flow["checks"].values())
    assert flow["passing_adaptive_algorithm_ids"] == [
        "greedy",
        "structured_gp_ei",
    ]
    assert not any(partition["checks"].values())


@pytest.mark.parametrize("task_id", EXPECTED_TASK_IDS)
def test_five_task_qualification_design_and_score_contracts_are_live(
    task_id: str,
) -> None:
    plan = _load_object(PLAN_PATH)
    task = get_task(task_id)
    task_plan = plan["tasks"][task_id]

    design = _recipe_design_checks(
        task_id,
        task.to_dict(),
        int(task_plan["dimension"]),
    )
    scoring = TaskScoringContract.from_success_metrics(
        objective=task.objective,
        success_metrics=task.success_metrics,
        contract_id=task_plan["scoring_contract_id"],
    )

    assert design["passed"] is True
    assert design["dead_recipe_coordinates"] == []
    assert scoring.contract_id == task_plan["scoring_contract_id"]
    if task_id in {"partition-discovery", "flow-reaction-optimization"}:
        assert "reaction_score" not in scoring.component_weights
