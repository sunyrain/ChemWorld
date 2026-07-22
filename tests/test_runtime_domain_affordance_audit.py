from __future__ import annotations

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.eval.runtime_domain_affordance_audit import (
    _candidate_actions,
    audit_runtime_domain_affordances,
)
from chemworld.tasks import SERIOUS_TASK_IDS


def test_candidate_actions_cover_public_midpoint_and_field_boundaries() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        env.unwrapped._state = env.unwrapped._state.replace(temperature_K=260.0)
        schema = env.unwrapped.action_schema("cool_crystallize")
        candidates = dict(_candidate_actions(schema))

        assert schema["schema_version"] == "chemworld-public-action-affordance-0.2"
        assert candidates["midpoint"] == {
            "operation": "cool_crystallize",
            "target_temperature_K": 255.0,
            "duration_s": 7200.5,
        }
        assert candidates["target_temperature_K:low"]["target_temperature_K"] == 250.0
        assert candidates["target_temperature_K:high"]["target_temperature_K"] == 260.0
        assert candidates["duration_s:low"]["duration_s"] == 1.0
        assert candidates["duration_s:high"]["duration_s"] == 14_400.0
    finally:
        env.close()


def test_all_serious_task_public_affordances_conform_to_runtime_domains() -> None:
    report = audit_runtime_domain_affordances(source_commit="test-source", seed=0)

    assert report["passed"] is True
    assert report["task_ids"] == list(SERIOUS_TASK_IDS)
    assert report["summary"]["candidate_count"] > 200
    assert report["summary"]["finding_count"] == 0
    assert report["findings"] == []
    assert report["benchmark_claim_allowed"] is False
