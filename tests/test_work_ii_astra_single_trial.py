from copy import deepcopy

import numpy as np
import pytest
from scripts.run_work_ii_astra_single_trial import (
    WORLDS,
    actions,
    clean_data,
    fit_reference,
    interventions,
    plan,
    predict_reference,
    public_contract,
    repaired_package,
)


def synthetic_records():
    rows = []
    for world in ("R1C1", "R2C2"):
        for i in range(6):
            p = plan(
                (350 + i * 10, 1200 + i * 700, 275 + ((i * 3) % 6) * 6, 1200 + ((i * 5) % 6) * 1100)
            )
            y = 0.2 + 0.08 * i
            rows.append(
                {
                    "status": "completed",
                    "public": {
                        "world": world,
                        "plan": p,
                        "upstream_hplc": {"yield": y},
                        "terminal": {
                            "yield": 0.01,
                            "crystal_yield": 0.3 + y * 0.2,
                            "crystal_purity": 0.9,
                            "score": 0.4 + y * 0.1,
                        },
                    },
                }
            )
    return rows


def test_full_lifecycle_and_optional_measurement():
    p = plan((350, 1200, 310, 7200))
    steps = actions(p)
    assert steps[-2:] == [
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]
    assert len(steps) <= 12
    assert steps[5] == {"operation": "measure", "instrument": "hplc"}
    p["intermediate_hplc"] = False
    assert sum(s.get("instrument") == "hplc" for s in actions(p)) == 1
    assert len(actions(p)) == len(steps) - 1
    filtered = actions(p)
    index = next(i for i, s in enumerate(filtered) if s["operation"] == "filter_crystals")
    assert filtered[index - 1] == {"operation": "measure", "instrument": "hplc"}


@pytest.mark.parametrize(
    "field,value",
    [
        ("reaction_temperature_K", 406),
        ("cooling_duration_s", float("nan")),
        ("intermediate_hplc", "yes"),
    ],
)
def test_invalid_plan_is_not_silently_clipped(field, value):
    p = plan((377.5, 3300, 292.5, 4200))
    p[field] = value
    with pytest.raises(ValueError):
        actions(p)


def test_component_laws_persist_across_pairings():
    specs = {w: interventions(w) for w in WORLDS}
    assert specs["R2C1"][0] == specs["R2C2"][0]
    assert specs["R1C1"][-1] == specs["R2C1"][-1]
    assert specs["R1C2"][-1] == specs["R2C2"][-1]
    assert len(specs["R1C1"]) == len(specs["R1C2"]) == 1


def test_public_fit_and_targeted_repair():
    model = fit_reference(synthetic_records())
    p = plan((377.5, 3300, 292.5, 4200))
    prediction = predict_reference(model, "R1C2", p)
    assert prediction is not None
    assert np.isfinite(list(prediction.values())).all()
    package = dict.fromkeys(("R1", "R2", "C1", "C2", "interface"), "original")
    before = deepcopy(package)
    fixed = repaired_package(package, model, "R")
    assert package == before
    assert fixed["R1"] != package["R1"]
    assert all(fixed[k] == package[k] for k in ("C1", "C2", "interface"))
    assert max(map(len, fixed.values())) <= 720
    # The whole-process reference must learn upstream HPLC yield, not terminal yield.
    whole = predict_reference(model, "R1C1", p, "whole")
    assert whole["reaction_yield"] > 0.1


def test_missing_assays_are_not_fabricated_by_reference():
    rows = synthetic_records()
    for row in rows:
        row["public"]["upstream_hplc"] = None
    model = fit_reference(rows)
    assert predict_reference(model, "R1C2", rows[0]["public"]["plan"]) is None
    assert model["whole"] is None


def test_public_delivery_excludes_runner_and_private_fields():
    rows = synthetic_records()
    rows[0].update(private_seed=99, evaluator_truth={"secret": True}, name="private/run")
    public = clean_data(rows)
    assert "private_seed" not in public[0]
    assert "evaluator_truth" not in public[0]
    assert "name" not in public[0]
    contract = public_contract()
    assert contract["learning_pairs"] == ["R1C1", "R2C2"]
    assert contract["instruments"]["hplc"]["sample_consumption_L"] > 0
