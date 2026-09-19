from scripts.report_work_ii_ec_pa_completed_block import (
    ARMS,
    complete_worlds,
    goal_joint_outcomes,
    prior_comparisons,
)


def world_rows(system, world):
    goals = ("discovery", "optimization") if system == "EC" else ("discovery",)
    return [
        {
            "system": system,
            "world": {"world_id": f"{system}-W{world:02d}"},
            "goal": goal,
            "locus": "E",
            "arm": arm,
            "budget": budget,
            "status": "completed",
        }
        for goal in goals
        for arm in ARMS
        for budget in (12, 24)
    ]


def test_complete_prefix_stops_at_incomplete_world_and_keeps_systems_separate():
    rows = world_rows("EC", 1) + world_rows("EC", 2) + world_rows("PA", 1)
    partial = world_rows("PA", 2)
    partial[-1]["status"] = "failed"
    rows += partial + world_rows("PA", 3)
    assert complete_worlds({"results": rows}) == {"EC": [1, 2], "PA": [1]}


def test_duplicate_condition_does_not_replace_missing_condition():
    rows = world_rows("EC", 1)
    rows[-1] = rows[0].copy()
    assert complete_worlds({"results": rows})["EC"] == []


def test_prior_pairing_preserves_world_and_excludes_whole_recovered_pair():
    rows = []
    for world, errors in (("EC-W01", (0.8, 0.2)), ("EC-W02", (0.1, 0.4))):
        for arm, error in zip(("Opaque", "Aligned"), errors, strict=True):
            rows.append(
                {
                    "system": "EC",
                    "goal": "discovery",
                    "world": world,
                    "arm": arm,
                    "budget": 12,
                    "metrics": {"score": {"mae": error}},
                    "recovered": world == "EC-W01" and arm == "Aligned",
                }
            )
    all_pairs = prior_comparisons(rows)[0]
    assert all_pairs["pairs"] == 2
    assert all_pairs["first_lower_mae"] == 1
    assert abs(all_pairs["mean_mae_first_minus_second"] + 0.15) < 1e-12
    clean = prior_comparisons(rows, first_attempt_only=True)[0]
    assert clean["pairs"] == 1
    assert clean["first_lower_mae"] == 0


def test_joint_outcomes_distinguish_worsening_from_ties():
    pairs = [
        {"delta_retest_opt_minus_discovery": 1, "delta_mae_opt_minus_discovery": error}
        for error in (-1, 0, 1)
    ]
    result = goal_joint_outcomes(pairs)
    assert result == {
        "pairs": 3,
        "better_retest_and_lower_mae": 1,
        "better_retest_and_higher_mae": 1,
        "equal_retest_or_mae": 1,
    }
