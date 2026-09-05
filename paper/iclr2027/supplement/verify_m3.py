"""Recompute M3 losses, source reuse, contrasts and information projections offline."""

from __future__ import annotations

import json
import math
import runpy
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT / "data/m3_portability.json").read_text(encoding="utf-8"))
source = report["scientific_source_data"]
protocol = json.loads((ROOT / "protocols/m3_portability.json").read_text(encoding="utf-8"))
m1 = json.loads((ROOT / "data/m1_replication.json").read_text(encoding="utf-8"))
rows = report["slots"]
calls = source["provider_calls"]
conditions = ("none", "raw", "L", "F")
weights = {
    "L_minus_none": {"L": 1, "none": -1},
    "raw_minus_none": {"raw": 1, "none": -1},
    "F_minus_none": {"F": 1, "none": -1},
    "L_minus_raw": {"L": 1, "raw": -1},
    "F_minus_raw": {"F": 1, "raw": -1},
    "F_minus_L": {"F": 1, "L": -1},
}
assert report["execution_valid"]
assert (
    len(rows)
    == len(calls)
    == report["condition_scheduled"]
    == report["provider_opportunities"]
    == 160
)
assert len({(row["state_id"], row["condition"]) for row in rows}) == 160
assert len({row["cluster_id"] for row in rows}) == report["independent_world_clusters"] == 10
assert report["additional_independent_worlds"] == report["recipient_measurements"] == 0
assert len(source["source_artifacts"]) == report["reused_source_states"] == 40
assert source["source_artifacts"] == m1["scientific_source_data"]["source_artifacts"]
assert sum(row["status"] == "completed" for row in rows) == report["condition_completed"]
assert sum(row["status"] == "completed" for row in calls) == report["provider_completed"]
assert (
    sum(len(scores) for scores in source["candidate_scores_after_selections_sealed"].values()) == 80
)
assert report["physical_completed"] == report["exact_replay_completed"] == 80

for cluster, packet in source["public_packets"].items():
    old = m1["scientific_source_data"]["public_packets"][cluster]
    assert packet["evidence"] == old["evidence"]
    assert packet["axes"] == old["axes"]
    assert not {tuple(row["xy"]) for row in packet["candidates"]} & {
        tuple(row["xy"]) for key in ("evidence", "candidates") for row in old[key]
    }
    for arm in conditions:
        assert sorted(
            row["serial_position"]
            for row in calls
            if row["cluster_id"] == cluster and row["condition"] == arm
        ) == [1, 2, 3, 4]

information = runpy.run_path(str(ROOT / "methods/m3_information.py"))
for call in calls:
    if call["prompt_bytes"] is None:
        continue
    packet = source["public_packets"][call["cluster_id"]]
    law = source["source_artifacts"][call["state_id"]].get(call["condition"])
    prompt = information["recipient_prompt"](packet, call["condition"], law)
    public = json.loads(prompt.split("\nINPUT:\n")[1])
    assert len(prompt.encode("utf-8")) == call["prompt_bytes"]
    assert ("evidence" in public) == (call["condition"] == "raw")
    assert ("artifact" in public) == (call["condition"] in ("L", "F"))
    assert all("score" not in candidate for candidate in public["candidates"])

states = defaultdict(dict)
for row in rows + report["deterministic_controls"]:
    scores = source["candidate_scores_after_selections_sealed"][row["cluster_id"]]
    available = row["status"] == "completed"
    regret = max(scores.values()) - scores[row["candidate_id"]] if available else 1.0
    assert math.isclose(regret, row["failure_aware_regret"], abs_tol=1e-12)
    assert row["near_optimal"] == (available and regret <= 0.01)
    assert row["top1"] == (available and regret <= 1e-12)
    if available:
        assert math.isclose(regret, row["raw_regret"], abs_tol=1e-12)
    else:
        assert row["raw_regret"] is None
    if row["condition"] in conditions:
        states[row["state_id"]][row["condition"]] = row
        continue
    if not available:
        continue
    packet = source["public_packets"][row["cluster_id"]]
    predictions = {}
    for candidate in packet["candidates"]:
        if row["condition"] == "nearest":
            nearest = min(
                packet["evidence"],
                key=lambda evidence: sum(
                    (x - y) ** 2 for x, y in zip(evidence["xy"], candidate["xy"], strict=True)
                ),
            )
            predictions[candidate["id"]] = nearest["score"]
        else:
            law = source["source_artifacts"][row["state_id"]][row["condition"][0]]
            x, y = candidate["xy"]
            predictions[candidate["id"]] = sum(
                value * weight
                for value, weight in zip((1, x, y, x * x, x * y, y * y), law, strict=True)
            )
    assert math.isclose(
        predictions[row["candidate_id"]], max(predictions.values()), rel_tol=1e-10, abs_tol=1e-10
    )

for baseline in report["random_baselines"]:
    scores = source["candidate_scores_after_selections_sealed"][baseline["cluster_id"]]
    assert math.isclose(
        max(scores.values()) - mean(scores.values()),
        baseline["uniform_random_expected_regret"],
        abs_tol=1e-12,
    )

for published in report["statistics"]["contrasts"]:
    task_worlds = defaultdict(lambda: defaultdict(list))
    for state in states.values():
        metadata = state["none"]
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

for resource in report["provider_resources"]:
    selected = [
        row
        for row in calls
        if row["model"] == resource["model"] and row["condition"] == resource["condition"]
    ]
    assert len(selected) == resource["scheduled"] == 20
    for key, value in resource["usage"].items():
        assert sum(row["usage"].get(key, 0) for row in selected) == value
    assert sum(row["prompt_bytes"] or 0 for row in selected) == resource["prompt_bytes"]

print(
    "verified M3: 160 recipient slots, 80 candidates, ten reused worlds, original artifacts, "
    "information isolation, costs, deterministic controls and six paired means"
)

if "--full" in sys.argv:
    import numpy as np

    primitives = runpy.run_path(str(ROOT / "methods/m1_public_primitives.py"))
    analysis = runpy.run_path(str(ROOT / "methods/m1_analysis.py"))
    assert primitives["normalized_design"](8, 90608) == protocol["candidate_xy"]
    for row in report["deterministic_controls"]:
        if row["condition"] not in ("L-X", "F-X") or row["status"] != "completed":
            continue
        packet = source["public_packets"][row["cluster_id"]]
        law = source["source_artifacts"][row["state_id"]][row["condition"][0]]
        assert primitives["maximize"](law, packet["candidates"]) == row["candidate_id"]
    recomputed = analysis["summarize_factorial"](
        rows, protocol, conditions=conditions, contrasts=weights
    )
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
        "verified M3 with NumPy: outcome-blind candidate design, exact maximizers "
        "and six world-bootstrap intervals"
    )
