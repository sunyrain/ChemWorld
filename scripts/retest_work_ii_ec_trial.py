"""Re-evaluate sealed EC recommendations under the original source resource envelope."""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_ec_dual_goal_trial import reference_run, summaries

from chemworld.data.logging import load_jsonl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, required=True)
    args = parser.parse_args()
    root = args.sources.resolve()
    source = read(root / "summary.json")
    if len(source["results"]) != 18:
        raise RuntimeError("finish the single-executor source block first")
    sources = [
        cell for cell in source["results"] if cell["status"] != "not_started_scope_reduced"
    ]
    rows = []
    for cell in sources:
        folder = root / cell["cell_id"] / "recommendation-retest-source-budget"
        selection = (cell.get("recommendation") or {}).get("selected_experiment_index")
        trajectory = root / cell["cell_id"] / "trajectory.jsonl"
        batches = summaries(load_jsonl(trajectory)) if trajectory.exists() else []
        selected = next((b for b in batches if b["lifecycle_index"] == selection), None)
        if selected is None:
            result = {"status": "unavailable", "reason": "no valid sealed recommendation"}
            folder.mkdir(parents=True, exist_ok=True)
            write(folder / "result.json", result)
        else:
            result = (
                read(folder / "result.json")
                if (folder / "result.json").exists()
                else reference_run(
                    folder,
                    selected["actions"],
                    observation_seed=101,
                    source_envelope=True,
                )
            )
            result["status"] = (
                "completed"
                if (
                    not result["failure"]
                    and len(result["batches"]) == 1
                    and not result["rollbacks"]
                    and result["exact_replay"].get("verified")
                )
                else "failed"
            )
            write(folder / "result.json", result)
        rows.append({"cell_id": cell["cell_id"], **result})
        write(
            root / "recommendation-retest-summary.json",
            {
                "planned": len(sources),
                "attempted": len(rows),
                "completed": sum(r["status"] == "completed" for r in rows),
                "results": rows,
            },
        )
        print(
            f"recommendation retests {len(rows)}/{len(sources)}; "
            f"{cell['cell_id']}: {result['status']}",
            flush=True,
        )


if __name__ == "__main__":
    main()
