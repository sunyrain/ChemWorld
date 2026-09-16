"""Contract regressions without new physical experiments or provider calls.

Actual runtime coverage is the recorded 32-unit E0 block, not these unit tests.
"""

import itertools
import math

import pytest
from scripts.run_work_ii_astra_corrected_pilot import (
    BOUNDS,
    StateResolvedRecipeAgent,
    actions,
    cooling_temperature,
    current_temperature,
    hull_distance,
    plan,
    product_utility,
    public_contract,
    qualification_plans,
    queries,
    swapped_package,
    validate_plan,
)


def test_obsolete_optional_assay_field_is_rejected():
    p = plan((350, 1200, 1, 7200))
    p["intermediate_hplc"] = False
    with pytest.raises(ValueError):
        actions(p)


def test_mandatory_assays_and_closed_lifecycle_at_all_corners():
    for values in itertools.product(*BOUNDS.values()):
        p = plan(values)
        steps = actions(p)
        assert len(steps) == 12
        assert steps[4]["operation"] == "quench"
        assert steps[5] == {"operation": "measure", "instrument": "hplc"}
        assert steps[6]["operation"] == "seed_crystals"
        assert steps[8] == {"operation": "measure", "instrument": "hplc"}
        assert steps[9]["operation"] == "filter_crystals"
        assert steps[-2:] == [
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
        for actual in (298.15, 302.573791, 345.8):
            assert 275 <= cooling_temperature(p, actual) <= min(310, actual)


def test_warm_cooling_regression_is_resolved_by_public_coordinate():
    p = plan((350, 5400, 1, 7200))
    assert cooling_temperature(p, 302.573791) == 302.573791
    p["reaction_temperature_K"] = 405
    assert cooling_temperature(p, 348.75) == 310
    assert "current_temperature_K" in public_contract()["cooling_coordinate"]


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -0.1, 1.1, True, "0.5"])
def test_invalid_cooling_coordinate_is_rejected_without_clipping(bad):
    p = plan((350, 1200, 0, 7200))
    p["cooling_fraction"] = bad
    with pytest.raises(ValueError):
        validate_plan(p)


def test_utility_has_no_reward_without_new_crystal_recovery():
    assert product_utility(0.4, 0, 1, 3000) == {
        "quality_adjusted_recovery_estimate": 0,
        "utility_per_hour": 0,
    }
    positive = product_utility(0.4, 0.5, 0.99, 3600)
    assert math.isclose(positive["utility_per_hour"], 0.4 * 0.992 * 0.5 * 0.99)
    assert (
        product_utility(0.4, 0.5, 0.99, 7200)["utility_per_hour"]
        == positive["utility_per_hour"] / 2
    )
    with pytest.raises(ValueError):
        product_utility(0.4, 0.5, 0.99, 0)


def test_qualification_pairwise_coverage_and_fixed_query_denominator():
    design = qualification_plans()
    assert len(design) == 8
    for a, b in itertools.combinations(BOUNDS, 2):
        assert {(p[a], p[b]) for p in design} == set(itertools.product(BOUNDS[a], BOUNDS[b]))
    q = queries()
    assert len(q) == 12
    for value in q.values():
        validate_plan(value["plan"])


def test_joint_support_rejects_marginally_inside_but_jointly_outside():
    points = [[0, 0], [1, 1]]
    assert hull_distance(points, [0.5, 0.5]) == pytest.approx(0)
    assert hull_distance(points, [0, 1]) == pytest.approx(0.5)


def test_identity_swap_is_consistent_and_does_not_mutate_source():
    base = {"R1": "R1 slow", "R2": "R2 fast", "C1": "C1 responds", "interface": "R1 feeds C1"}
    swapped = swapped_package(base, "R")
    assert swapped["R1"] == "R1 fast"
    assert swapped["R2"] == "R2 slow"
    assert swapped["C1"] == base["C1"]
    assert swapped["interface"] == "R2 feeds C1"
    assert base["R1"] == "R1 slow"


def test_whole_schedule_once_and_no_target_feedback(tmp_path, monkeypatch):
    from scripts import run_work_ii_astra_corrected_pilot as pilot

    physical_names, model_names = [], []

    def fake_batch(root, name, world, p, seed):
        assert name not in physical_names
        physical_names.append(name)
        validate_plan(p)
        upstream = {
            "yield": 0.25 + (p["reaction_temperature_K"] - 350) / 250,
            "conversion": 0.8,
            "selectivity": 0.6,
        }
        terminal = {
            "yield": 0.1,
            "crystal_yield": 0.4 if world.endswith("C1") else 0.2,
            "crystal_purity": 0.99,
            "score": 0.5,
        }
        duration = p["reaction_duration_s"] + p["cooling_duration_s"] + 500
        terminal.update(
            product_utility(upstream["yield"], terminal["crystal_yield"], 0.99, duration)
        )
        return {
            "name": name,
            "world": world,
            "plan": p,
            "status": "completed",
            "public": {
                "world": world,
                "plan": p,
                "upstream_hplc": upstream,
                "terminal": terminal,
                "resources": {"process_time_s": duration},
                "actual_quench_temperature_K": p["reaction_temperature_K"] - 47,
                "actual_cooling_temperature_K": cooling_temperature(
                    p, p["reaction_temperature_K"] - 47
                ),
            },
        }

    def fake_invoke(root, name, prompt, schema, *, deadline):
        import json

        assert name not in model_names
        model_names.append(name)
        supplied = json.loads(prompt.split("PUBLIC INPUT:\n")[1])
        assert "blind_truth" not in supplied
        if name.startswith("acquire"):
            assert "blind_queries" not in supplied
            payload = {
                k: plan((355 + 6 * i, 1300 + 500 * i, i / 7, 1500 + 600 * i))
                for i, k in enumerate(schema["properties"])
            }
        elif name.startswith("encode"):
            assert "blind_queries" not in supplied
            payload = dict.fromkeys(
                schema["properties"], "Measured evidence, uncertain beyond support."
            )
        else:
            assert set(supplied["blind_queries"]) == set(queries())
            assert all("truth" not in q for q in supplied["blind_queries"].values())
            payload = {
                "predictions": {q: dict.fromkeys(pilot.METRICS, 0.5) for q in queries()},
                "deployments": {w: plan((380, 2400, 0.4, 3600)) for w in pilot.WORLDS},
            }
        return {"status": "completed", "payload": payload}

    monkeypatch.setattr(pilot, "execute_batch", fake_batch)
    monkeypatch.setattr(pilot, "invoke", fake_invoke)
    pilot.write(tmp_path / "private_inputs.json", {"seed": 10, "deadline": float(10**12)})
    pilot.run(tmp_path)
    assert len(model_names) == 20
    assert len(physical_names) == 164
    deliveries = pilot.read(tmp_path / "deliveries.json")
    assert len(deliveries) == 12
    assert deliveries["task_only"] == {}


def test_state_resolved_controller_uses_only_public_current_temperature():
    from types import SimpleNamespace

    p = plan((350, 1200, 1, 7200))
    view = {
        "tool_json": {
            "available_actions": [
                {
                    "operation": "cool_crystallize",
                    "schema": {
                        "constraints": [
                            {
                                "id": "payload_coupling:maximum_cooling_rate_K_s",
                                "parameters": {"current_temperature_K": 302.57379134754575},
                            }
                        ]
                    },
                }
            ]
        }
    }
    agent = StateResolvedRecipeAgent(p)
    agent.reset({}, 0)
    for _ in range(7):
        agent.act([])
    action = agent.act([SimpleNamespace(public_view=view)])
    assert action["target_temperature_K"] == current_temperature(view)
    assert action["target_temperature_K"] != 305
