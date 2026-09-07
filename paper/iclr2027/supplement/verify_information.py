"""Recompute disclosure counts and world effects; keep selected retries separate."""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT / "data/information_disclosure.json").read_text(encoding="utf-8"))
rows = report["rows"]
assert report["formal_result"] and report["status"] == "terminal"
assert len(rows) == report["scheduled"] == 120
assert Counter(r["status"] for r in rows) == report["counts"] == {"completed": 112, "failed": 8}
assert len({r["cell_id"] for r in rows}) == 120
worlds = list(dict.fromkeys(r["cluster_id"] for r in rows))
assert len(worlds) == report["worlds"] == 10
for row in rows:
    joint = int(
        row["status"] == "completed"
        and row["post_family"] == "FAMILY_B_POWER"
        and row["post_exponent_abs_error"] <= 0.10
    )
    assert joint == row["joint_recovery"]
    if row["status"] != "completed":
        assert row["top1"] == 0 and row["normalized_regret"] == 1
    else:
        assert row["top1"] == int(row["raw_regret"] <= 1e-8)
for group in report["groups"]:
    selected = [
        r
        for r in rows
        if r["model"] == group["model"]
        and r["information"] == group["information"]
        and (r["arm"] == "aligned_nominal") == (group["analysis"] == "retention")
    ]
    assert len(selected) == group["scheduled"]
    for metric in ("joint_recovery", "top1"):
        assert sum(r[metric] for r in selected) == group[metric]
    assert math.isclose(
        mean(r["normalized_regret"] for r in selected),
        group["mean_normalized_regret_failure_aware"],
        abs_tol=1e-12,
    )
    available = [r["post_mae"] for r in selected if "post_mae" in r]
    assert len(available) == group["post_mae_available_n"]
    assert math.isclose(mean(available), group["post_mae_mean"], abs_tol=1e-12)
effects = []
for world in worlds:
    by_model = []
    for model in report["models"]:
        selected = [
            r
            for r in rows
            if r["cluster_id"] == world and r["model"] == model and r["arm"] != "aligned_nominal"
        ]
        assert len(selected) == 4
        effect = mean(r["joint_recovery"] for r in selected if r["information"] == "complete")
        effect -= mean(r["joint_recovery"] for r in selected if r["information"] == "original")
        stored = next(r for r in report["world_contrasts"] if r["world"] == world)
        assert math.isclose(effect, stored[model], abs_tol=1e-12)
        by_model.append(effect)
    effects.append(mean(by_model))
assert math.isclose(mean(effects), report["primary"]["mean"], abs_tol=1e-12)
if "--full" in sys.argv:
    import numpy as np

    primary = report["primary"]
    draws = (
        np.random.default_rng(primary["bootstrap_seed"])
        .choice(effects, (primary["bootstrap_draws"], len(effects)))
        .mean(axis=1)
    )
    np.testing.assert_allclose(
        np.quantile(draws, [0.025, 0.975]), primary["approximate_world_bootstrap_95"], atol=1e-12
    )
retry_path = ROOT / "data/information_failure_retry.json"
if retry_path.exists():
    retry = json.loads(retry_path.read_text(encoding="utf-8"))
    assert not retry["formal_result"] and retry["scheduled"] == 8
    original = {r["cell_id"]: r for r in rows if r["model"] == "deepseek"}
    expected = {key for key, row in original.items() if row["status"] == "failed"}
    assert {r["cell_id"] for r in retry["rows"]} == expected
    assert {r["cell_id"] for r in retry["selection"]} == expected
    alternative = original | {r["cell_id"]: r for r in retry["rows"] if r["status"] != "unstarted"}
    assert list(alternative.values()) == retry["one_retry_sensitivity"]["rows"]
    assert Counter(r["status"] for r in retry["rows"]) == retry["counts"]
    print("verified selected one-retry sensitivity separately from original formal evidence")
print(
    "verified disclosure: 120 original sessions, all failures, "
    "ten-world effect and action summaries"
)
