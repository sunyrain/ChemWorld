"""Fixed retained 210-state W2-263 development calibration, before candidate 2."""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.qualify_abductive_worlds import write

from chemworld.physchem.abductive_worlds import (
    ASSAY_STD,
    METRICS,
    NOTE,
    build_worlds,
    recipe,
    solve_query,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    candidates = []
    for amount in (6e-7, 8e-7, 1e-6):
        for volume in (0.04, 0.06, 0.075, 0.08):
            candidates.append(recipe(f"R{len(candidates) + 1:02d}", amount / volume, volume))
    diagnostics = [
        recipe(f"D{i:02d}", c, 0.02)
        for i, c in enumerate((0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 0.25, 0.5), 1)
    ]
    states, failures = [], []
    for world in build_worlds():
        for query in candidates + diagnostics:
            try:
                states.append(solve_query(world, query))
            except Exception as exc:
                failures.append(
                    {
                        "world_id": world["world_id"],
                        "query_id": query["query_id"],
                        "failure": f"{type(exc).__name__}: {exc}",
                    }
                )
    by_key = {(r["world_id"], r["query_id"]): r["metrics"] for r in states}
    ranked = []
    for query in candidates:
        gaps = []
        for pair in range(1, 6):
            left = by_key.get((f"EQ-P{pair:02d}-A", query["query_id"]))
            right = by_key.get((f"EQ-P{pair:02d}-B", query["query_id"]))
            if left is None or right is None:
                gaps.append(float("inf"))
            else:
                gaps.extend(abs(left[m] - right[m]) / ASSAY_STD[m] for m in METRICS)
        ranked.append({"query": query, "max_pair_channel_gap_sigma": max(gaps)})
    ranked.sort(key=lambda r: r["max_pair_channel_gap_sigma"])
    selected = []
    for row in ranked:
        if row["max_pair_channel_gap_sigma"] > 1:
            continue
        volume = row["query"]["final_state"]["solvent_L"]
        if volume + sum(r["query"]["final_state"]["solvent_L"] for r in selected) <= 0.16:
            selected.append(row)
        if len(selected) == 2:
            break
    result = {
        "note": NOTE,
        "planned_states": 210,
        "completed_states": len(states),
        "states": states,
        "failures": failures,
        "ranked_references": ranked,
        "selected_references": selected,
        "passed": len(selected) == 2 and not failures,
    }
    write(args.output, result)
    print({"states": len(states), "failures": failures, "selected": selected}, flush=True)


if __name__ == "__main__":
    main()
