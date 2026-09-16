import numpy as np
import pytest
from scripts import run_work_ii_astra_corrected_pilot as base
from scripts import run_work_ii_early_time_screen as screen


def test_new_domain_does_not_change_closed_default():
    p = base.plan((405, 30, 0, 1200))
    with pytest.raises(ValueError):
        base.actions(p)
    actions = base.actions(p, bounds=screen.BOUNDS)
    assert len(actions) == 12
    assert actions[3]["duration_s"] == 30
    assert actions[5]["instrument"] == actions[8]["instrument"] == "hplc"
    assert base.BOUNDS["reaction_duration_s"] == (1200, 5400)


def test_factorial_and_regret_pairing():
    assert len(screen.grid()) == len({tuple(p.values()) for p in screen.grid()}) == 72
    u = np.ones((4, 72))
    assert screen.action_value(u)["best_common_recipe_mean_relative_loss"] == 0
    # Only R identity changes the preferred action: R1 rows 0,2; R2 rows 1,3.
    u[:, :] = 0.1
    u[[0, 2], 0] = 1
    u[[1, 3], 1] = 1
    value = screen.action_value(u)
    assert value["axis_common_recipe_mean_relative_loss"]["R"] == pytest.approx(0.45)
    assert value["axis_common_recipe_mean_relative_loss"]["C"] == 0
    assert value["best_of_two_source_winners_heldout_mean_relative_loss"] == 0
