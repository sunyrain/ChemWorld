from __future__ import annotations

import copy
import json

import pytest
from scripts import prepare_work_ii_c_reference_v3 as design


def test_reference_set_has_unique_complete_recipes_within_public_envelope():
    rows = design.queries()
    assert len(rows) == len({json.dumps(q["actions"], sort_keys=True) for q in rows}) == 12
    for q in rows:
        assert len(q["actions"]) <= 60
        assert q["actions"][-2:] == design.c.pilot.CLOSE
        seed_index = next(
            i for i, a in enumerate(q["actions"]) if a["operation"] == "seed_crystals"
        )
        assert q["actions"][seed_index - 1] == design.c.reheat(300, 300)


@pytest.mark.parametrize(
    "factor,operation,field",
    [
        ("solvent", "add_solvent", "solvent"),
        ("seed", "seed_crystals", "seed_mass_g"),
        ("upstream_loading", "add_reagent", "amount_mol"),
    ],
)
def test_single_factor_pairs_do_not_change_other_controls(factor, operation, field):
    pair = [copy.deepcopy(q["actions"]) for q in design.queries() if q["pair"] == factor]
    values = []
    for actions in pair:
        action = next(a for a in actions if a["operation"] == operation)
        values.append(action.pop(field))
    assert values[0] != values[1]
    assert pair[0] == pair[1]


@pytest.mark.parametrize("factor", ["cooling_history", "thermal_history"])
def test_path_pairs_match_total_time_and_final_temperature(factor):
    paths = [q["actions"] for q in design.queries() if q["pair"] == factor]
    assert sum(a.get("duration_s", 0) for a in paths[0]) == sum(
        a.get("duration_s", 0) for a in paths[1]
    )
    assert [
        next(a["target_temperature_K"] for a in reversed(p) if "target_temperature_K" in a)
        for p in paths
    ] == [278.15, 278.15]
