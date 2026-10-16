"""Read back physical means by replaying existing heldout qualification actions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts import run_abductive_discrimination as runner
from scripts.qualify_abductive_worlds import write

from chemworld.data.logging import load_jsonl
from chemworld.physchem.abductive_worlds import METRICS, build_queries, solve_query


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError(args.report)
    config = runner.build_config()
    runner.configure(config)
    rows = []
    for world in config["worlds"]:
        records = load_jsonl(args.source_root / world["world_id"] / "heldout/trajectory.jsonl")
        first = records[0]
        result = runner.truth_captured_reference(
            args.output_root / world["world_id"],
            [r["action"] for r in records],
            config=config,
            world=world,
            observation_seed=first["observation_seed"],
            namespace=first["observation_noise_namespace"],
        )
        comparisons = []
        for query, mean in zip(build_queries(), result["physical_means"], strict=True):
            expected = solve_query(world, query)["metrics"]
            gaps = {m: abs(mean["metrics"][m] - expected[m]) for m in METRICS}
            comparisons.append(
                {
                    "query_id": query["query_id"],
                    "actual_mean": mean["metrics"],
                    "kernel_prediction": expected,
                    "absolute_gaps": gaps,
                    "passed": max(gaps.values()) <= 1e-10,
                }
            )
        rows.append(
            {
                "world_id": world["world_id"],
                "failure": result["failure"],
                "exact_replay": result["exact_replay"],
                "comparisons": comparisons,
                "passed": len(comparisons) == 12
                and result["failure"] is None
                and result["exact_replay"]["verified"]
                and all(r["passed"] for r in comparisons),
            }
        )
        payload = {
            "scope": "Replay/readback of retained qualification heldouts; no new conditions",
            "planned_means": 120,
            "checked_means": sum(len(r["comparisons"]) for r in rows),
            "worlds": rows,
            "passed": len(rows) == 10 and all(r["passed"] for r in rows),
        }
        write(args.report, payload)
        print(
            json.dumps(
                {
                    "stage": "physical-mean-readback",
                    "worlds": f"{len(rows)}/10",
                    "checked_means": payload["checked_means"],
                    "last_world_passed": rows[-1]["passed"],
                }
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
