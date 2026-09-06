"""Recompute descriptive contrasts from released paired public observations."""

import json
from pathlib import Path
from statistics import mean

root = Path(__file__).resolve().parent
report = json.loads((root / "data/public_information.json").read_text(encoding="utf-8"))
assert report["worlds"] == 5
assert report["scheduled_pairs"] == 40
assert report["scheduled_metric_pairs"] == report["completed_metric_pairs"] == 160
assert report["failures"] == []
assert report["formal_qualification"] is False
for summary in report["summaries"]:
    selected = [
        r
        for r in report["rows"]
        if r["metric"] == summary["metric"]
        and (summary["world"] is None or r["world"] == summary["world"])
    ]
    differences = [abs(r["target"] - r["reference"]) for r in selected]
    assert len(selected) == summary["scheduled"] == summary["completed"]
    assert abs(mean(differences) - summary["mean_absolute_difference"]) < 1e-12
    assert max(differences) == summary["max_absolute_difference"]
    assert differences.count(0) == summary["exact_equal_count"]
print("Public information: 160/160 paired values; 24 descriptive summaries reproduced")
