from __future__ import annotations

from chemworld.models import BeliefState


def test_belief_state_from_records_summarizes_public_trajectory() -> None:
    records = [
        {
            "leaderboard_score": None,
            "observed_keys": ["yield"],
            "processed_estimate": {"yield": 0.32},
            "uncertainty": {"yield_std": 0.05},
        },
        {
            "leaderboard_score": 0.61,
            "observed_keys": ["yield", "selectivity"],
            "processed_estimate": {"yield": 0.58, "selectivity": 0.75},
            "uncertainty": {"yield_std": 0.02, "selectivity_std": 0.03},
        },
    ]

    belief = BeliefState.from_records(records)
    assert belief.observations == 2
    assert belief.best_observed_score == 0.61
    assert belief.predictions["yield"] == 0.58
    assert belief.predictions["selectivity"] == 0.75
    assert belief.uncertainties["selectivity_std"] == 0.03
    assert belief.metadata["measured_steps"] == 2
    assert belief.to_dict()["metadata"]["source"] == "trajectory_records"
