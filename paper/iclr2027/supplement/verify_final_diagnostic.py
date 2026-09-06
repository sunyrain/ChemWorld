"""Independently reconstruct the final diagnostic's counts and paired world interval."""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT / "data/final_diagnostic.json").read_text(encoding="utf-8"))
protocol = json.loads((ROOT / "protocols/final_diagnostic.json").read_text(encoding="utf-8"))
rows = report["rows"]
assert len(rows) == report["scheduled"] == 120
assert Counter(row["status"] for row in rows) == report["counts"]
assert report["execution_complete"] and report["formal_result"]
worlds = list(dict.fromkeys(row["cluster_id"] for row in rows))
assert len(worlds) == report["worlds"] == 5
assert report["additional_independent_worlds"] == report["participant_physics"] == 0
assert len({(r["cluster_id"], r["arm"], r["model"], r["tool"], r["repeat"]) for r in rows}) == 120
for row in rows:
    available = row["status"] == "completed"
    joint = int(
        available
        and row["post_family"] == "FAMILY_B_POWER"
        and abs(row["post_exponent"] - 1.75) <= 0.10
    )
    assert joint == row["joint_recovery"]
    if not available:
        assert row["normalized_regret"] == 1 and row["top1"] == 0
    else:
        action = row["action"]
        raw = action["best_action_score"] - action["true_score"]
        span = action["best_action_score"] - action["worst_action_score"]
        assert math.isclose(raw, row["raw_regret"], abs_tol=1e-12)
        assert math.isclose(raw / span if span else 0, row["normalized_regret"], abs_tol=1e-12)
for group in report["by_prior"]:
    selected = [r for r in rows if all(r[k] == group[k] for k in ("model", "tool", "arm"))]
    assert len(selected) == group["scheduled"] == 10
    assert sum(r["joint_recovery"] for r in selected) == group["joint_recovery"]
effects = []
for world in worlds:
    selected = [r for r in rows if r["cluster_id"] == world]
    assert len(selected) == 24
    effect = mean(r["joint_recovery"] for r in selected if r["tool"] == "on") - mean(
        r["joint_recovery"] for r in selected if r["tool"] == "off"
    )
    effects.append(effect)
    stored = next(r for r in report["world_contrasts"] if r["cluster_id"] == world)
    assert math.isclose(effect, stored["tool_on_minus_off"], abs_tol=1e-12)
primary = report["primary"]
assert math.isclose(mean(effects), primary["mean"], abs_tol=1e-12)
if "--full" in sys.argv:
    import numpy as np

    rng = np.random.default_rng(protocol["bootstrap_seed"])
    draws = rng.choice(effects, size=(protocol["bootstrap_draws"], len(effects))).mean(axis=1)
    np.testing.assert_allclose(
        np.percentile(draws, [2.5, 97.5]), primary["approximate_world_bootstrap_95"], atol=1e-12
    )
    print("verified final diagnostic world-bootstrap interval")
assert sum(r["turns"] for r in report["resources"]) == 240
assert len(report["failures"]) == 3
print(
    "verified final diagnostic: 120 sessions, failures, joint scores, action losses and paired mean"
)
