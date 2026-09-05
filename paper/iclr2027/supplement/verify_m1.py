"""Recompute M1 decision losses and paired means using only packaged data and stdlib."""

from __future__ import annotations

import json
import math
import runpy
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT / "data/m1_replication.json").read_text(encoding="utf-8"))
source = report["scientific_source_data"]
rows = report["slots"]
assert report["execution_valid"]
assert len(rows) == report["condition_scheduled"] == 160
assert len({(row["state_id"], row["condition"]) for row in rows}) == 160
assert len({row["cluster_id"] for row in rows}) == 10
assert len(source["provider_calls"]) == report["provider_opportunities"] == 120
assert (
    sum(row["status"] == "completed" for row in source["provider_calls"])
    == report["provider_completed"]
)
assert sum(row["status"] == "completed" for row in rows) == report["condition_completed"]

assert len(report["baselines"]) == 10
for baseline in report["baselines"]:
    cluster = baseline["cluster_id"]
    packet = source["public_packets"][cluster]
    scores = source["candidate_scores_after_selections_sealed"][cluster]
    predictions = {}
    for candidate in packet["candidates"]:
        nearest = min(
            packet["evidence"],
            key=lambda evidence: sum(
                (x - y) ** 2 for x, y in zip(evidence["xy"], candidate["xy"], strict=True)
            ),
        )
        predictions[candidate["id"]] = nearest["score"]
    choice = max(predictions, key=predictions.get)
    assert math.isclose(
        max(scores.values()) - scores[choice], baseline["nearest_public_regret"], abs_tol=1e-12
    )
    assert math.isclose(
        max(scores.values()) - mean(scores.values()),
        baseline["uniform_random_expected_regret"],
        abs_tol=1e-12,
    )

states = defaultdict(dict)
for row in rows:
    states[row["state_id"]][row["condition"]] = row
    scores = source["candidate_scores_after_selections_sealed"][row["cluster_id"]]
    assert len(scores) == 8
    available = row["status"] == "completed"
    regret = max(scores.values()) - scores[row["candidate_id"]] if available else 1.0
    assert math.isclose(regret, row["failure_aware_regret"], abs_tol=1e-12)
    assert row["near_optimal"] == (available and regret <= 0.01)
    if not available:
        assert row["raw_regret"] is None
        continue
    assert math.isclose(regret, row["raw_regret"], abs_tol=1e-12)
    if row["condition"].endswith("-X"):
        law = source["source_artifacts"][row["state_id"]][row["condition"][0]]
        candidates = source["public_packets"][row["cluster_id"]]["candidates"]
        predicted = {}
        for candidate in candidates:
            x, y = candidate["xy"]
            basis = (1, x, y, x * x, x * y, y * y)
            predicted[candidate["id"]] = sum(
                value * weight for value, weight in zip(basis, law, strict=True)
            )
        # Dot-product summation may differ from the runtime BLAS in its final bits.
        assert math.isclose(
            predicted[row["candidate_id"]], max(predicted.values()), rel_tol=1e-10, abs_tol=1e-10
        )

weights = {
    "F-X_minus_L-X": {"F-X": 1, "L-X": -1},
    "L-X_minus_L-A": {"L-X": 1, "L-A": -1},
    "F-A_minus_L-A": {"F-A": 1, "L-A": -1},
    "F-X_minus_F-A": {"F-X": 1, "F-A": -1},
    "interaction": {"F-X": 1, "L-X": -1, "F-A": -1, "L-A": 1},
}
for published in report["statistics"]["contrasts"]:
    task_worlds = defaultdict(lambda: defaultdict(list))
    for state in states.values():
        metadata = state["L-A"]
        value = sum(
            state[key]["failure_aware_regret"] * weight
            for key, weight in weights[published["contrast"]].items()
        )
        task_worlds[metadata["task"]][metadata["cluster_id"]].append(value)
    task_means = {
        task: mean(mean(values) for values in worlds.values())
        for task, worlds in task_worlds.items()
    }
    assert math.isclose(mean(task_means.values()), published["mean_difference"], abs_tol=1e-12)
    for task, value in task_means.items():
        assert math.isclose(value, published["task_means"][task], abs_tol=1e-12)
    for worlds in task_worlds.values():
        for world, values in worlds.items():
            assert len(values) == 4
            row = next(
                row
                for row in report["statistics"]["world_contrasts"]
                if row["cluster_id"] == world and row["contrast"] == published["contrast"]
            )
            assert math.isclose(mean(values), row["mean_difference"], abs_tol=1e-12)

print(
    "verified M1: 160 condition slots, 120 session opportunities, 10 worlds, "
    "two public baselines and five paired means"
)

if "--full" in sys.argv:
    import numpy as np

    protocol = json.loads((ROOT / "protocols/m1_replication.json").read_text(encoding="utf-8"))
    primitives = runpy.run_path(str(ROOT / "methods/m1_public_primitives.py"))
    analysis = runpy.run_path(str(ROOT / "methods/m1_analysis.py"))
    for state_id, state in states.items():
        packet = source["public_packets"][state["F-X"]["cluster_id"]]
        fitted = primitives["fit_public_law"](packet["evidence"], ridge=protocol["ridge"])
        np.testing.assert_allclose(
            fitted, source["source_artifacts"][state_id]["F"], rtol=1e-10, atol=1e-10
        )
        for condition in ("L-X", "F-X"):
            row = state[condition]
            if row["status"] == "completed":
                assert primitives["maximize"](
                    source["source_artifacts"][state_id][condition[0]], packet["candidates"]
                ) == row["candidate_id"]
    recomputed = analysis["summarize_factorial"](rows, protocol)
    for actual, expected in zip(
        recomputed["contrasts"], report["statistics"]["contrasts"], strict=True
    ):
        assert actual["contrast"] == expected["contrast"]
        assert actual["interval_level"] == expected["interval_level"]
        np.testing.assert_allclose(actual["interval"], expected["interval"], rtol=1e-12, atol=1e-12)
    assert (
        recomputed["primary_material_benefit_supported"]
        == report["statistics"]["primary_material_benefit_supported"]
    )
    print(
        "verified M1 with NumPy: public fits, exact maximizer choices and five bootstrap intervals"
    )
