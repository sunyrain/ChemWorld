from __future__ import annotations

from scripts.run_rl_staged_development import _gate_passed, load_staged_protocol


def test_staged_protocol_is_train_dev_only_and_nonclaiming() -> None:
    protocol = load_staged_protocol()
    assert protocol["training"]["allocation"] == "train"
    assert protocol["world_family_dev_evaluation"]["allocation"] == "dev"
    assert protocol["replay_evaluation"]["world_family_allocation"] is None
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["training"]["action_contract_schema"] == (
        "chemworld-continuous-event-action-0.3"
    )


def test_100k_gate_requires_world_dev_replay_completion_validity_and_score() -> None:
    gate = load_staged_protocol()["escalation_gate"]
    dev = {"episode_completion_rate": 0.8, "invalid_action_rate": 0.04}
    replay = {
        "all_replay_verified": True,
        "episode_completion_rate": 0.8,
        "invalid_action_rate": 0.04,
        "mean_final_best_score_including_failures": 0.01,
    }
    assert _gate_passed(dev, replay, gate=gate)
    for key, failed_value in (
        ("episode_completion_rate", 0.4),
        ("invalid_action_rate", 0.1),
        ("mean_final_best_score_including_failures", 0.0),
    ):
        changed = dict(replay)
        changed[key] = failed_value
        assert not _gate_passed(dev, changed, gate=gate)
    assert not _gate_passed(
        {"episode_completion_rate": 0.5, "invalid_action_rate": 0.04},
        replay,
        gate=gate,
    )
