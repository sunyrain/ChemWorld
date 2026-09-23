"""Export retained data for the editable English figure deck; no new experiments."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "paper/figures/academic-ppt"
REPORTS = ROOT / "workstreams/flagship_tasks/reports"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    with (ROOT / "paper/figures/integrated-results/campaign_metrics.csv").open(
        encoding="utf-8"
    ) as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        row["budget"] = int(row["budget"])
        row["conforming"] = row["conforming"] == "True"
        for key in ("mae", "coverage", "retest", "retest_purity", "width"):
            row[key] = float(row[key]) if row[key] else None
    assert len({row["id"] for row in rows}) == 240
    by_id = {}
    for row in rows:
        by_id.setdefault(row["id"], []).append(row)
    macro = [
        {**group[0], "metric": "macro", "mae": fmean(row["mae"] for row in group)}
        for group in by_id.values()
    ]
    closeout = REPORTS / "work-ii-evidence-closeout-20260921"
    output = {
        "campaigns": rows,
        "macro_campaigns": macro,
        "goals": read(ROOT / "paper/figures/integrated-results/analysis.json"),
        "regimes": read(closeout / "STORY_WORLD_ANALYSIS.json")["eq_p_query_regimes"],
        "eq_process": read(closeout / "EQ_AUTONOMOUS_PROCESS.json")["rows"],
        "crystal": read(
            REPORTS / "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json"
        )["rows"],
    }
    assert len(output["eq_process"]) == 15 and len(output["crystal"]) == 30
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "retained-figure-data.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Retained figure inputs: 240 campaigns, 15 EQ sessions, 30 C sessions; no new data")


if __name__ == "__main__":
    main()
