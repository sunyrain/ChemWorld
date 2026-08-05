from __future__ import annotations

import json

from chemworld.eval.composition_qualification_design import (
    EXPECTED_GENERATED_CASE_COUNT,
    EXPECTED_PATTERN_CASE_COUNTS,
    UNSEEN_PATTERN_ID,
    build_generated_suites,
)


def test_frozen_generated_suite_denominators_and_coverage() -> None:
    suites = build_generated_suites()
    counts = {
        str(suite.cases[0].compiled.compatibility.pattern): len(suite.cases)
        for suite in suites
    }

    assert counts == EXPECTED_PATTERN_CASE_COUNTS
    assert sum(counts.values()) == EXPECTED_GENERATED_CASE_COUNT == 52
    assert counts[UNSEEN_PATTERN_ID] == 8
    assert all(suite.report["denominators"] == suite.report["covered"] for suite in suites)
    assert all(suite.report["failure_count"] == 0 for suite in suites)
    json.dumps([suite.to_dict() for suite in suites], allow_nan=False)


def test_generated_composition_ids_do_not_reuse_reference_task_ids() -> None:
    from chemworld.tasks import list_tasks

    registered = {task.task_id for task in list_tasks()}
    generated = {
        case.request["composition_id"]
        for suite in build_generated_suites()
        for case in suite.cases
    }

    assert len(generated) == EXPECTED_GENERATED_CASE_COUNT
    assert generated.isdisjoint(registered)


def test_process_time_limits_are_derived_per_pattern() -> None:
    suites = build_generated_suites()
    limits = {}
    for suite in suites:
        case = suite.cases[0]
        resources = case.request["task"]["resources"]
        policy = resources["process_time_policy"]
        assert resources["time_s"] == policy["process_time_limit_s"]
        assert policy["process_time_limit_s"] == (
            policy["required_stage_max_s"] + policy["repeat_allowance_s"]
        )
        assert policy["required_stage_max_s"] == (
            policy["timed_stage_max_s"] + policy["implicit_stage_reserve_s"]
        )
        assert policy["schema_version"] == "chemworld-process-time-budget-policy-0.2"
        assert set(policy["required_operation_counts"]).issuperset(
            policy["operation_repeat_limits"]
        )
        limits[str(case.compiled.compatibility.pattern)] = resources["time_s"]

    assert limits == {
        "phase-observation": 0.0,
        "reaction-thermal-observation": 3600.0,
        "phase-separation-observation": 1860.0,
        "reaction-crystallization-observation": 11100.0,
        "reaction-distillation-observation": 10440.0,
        "reaction-continuous-flow-observation": 7200.0,
        "reaction-electrochemistry-observation": 5400.0,
        "reaction-phase-separation-observation": 7500.0,
    }


def test_composed_world_exposes_and_enforces_process_time_headroom() -> None:
    import gymnasium as gym

    suite = next(
        suite
        for suite in build_generated_suites()
        if suite.cases[0].compiled.compatibility.pattern
        == "reaction-distillation-observation"
    )
    case = suite.cases[0]
    env = gym.make("ChemWorld", composition=case.request, seed=0)
    try:
        env.reset(seed=0)
        initial = env.unwrapped.campaign_state()["declared_process_resources"]
        assert initial["used_s"] == 0.0
        assert initial["limit_s"] == 10440.0
        env.step({"operation": "add_solvent", "volume_L": 0.025, "solvent": 1})
        env.step({"operation": "add_reagent", "amount_mol": 0.010})
        env.step(
            {
                "operation": "heat",
                "target_temperature_K": 375.0,
                "duration_s": 7200.0,
                "stirring_speed_rpm": 650.0,
            }
        )
        _observation, _reward, _terminated, _truncated, info = env.step(
            {
                "operation": "heat",
                "target_temperature_K": 375.0,
                "duration_s": 3600.0,
                "stirring_speed_rpm": 650.0,
            }
        )
        assert info["declared_process_time_preflight"]["allowed"] is False
        assert info["declared_process_time_preflight"]["rejection_reasons"] == [
            "process_time_limit"
        ]
        assert info["transaction_status"] != "committed"
    finally:
        env.close()
