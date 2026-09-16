"""Fixed 24-cell crystallization qualification after quenched dissolution repair."""

from __future__ import annotations

import argparse
import itertools
import json
import threading
import time
from pathlib import Path

from scripts.run_work_ii_astra_full_process_trial import ROOT, TASKS, reference_actions
from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_phase_resolved_process import CLOSE, PARTICLE, execute
from scripts.run_work_ii_process_continuity import continuity_plans

from chemworld.runtime.full_process_contract import (
    FULL_PROCESS_SEED_CONTRACT,
    FULL_PROCESS_THERMAL_CONTRACT,
)


def thermal_plans(contract=FULL_PROCESS_THERMAL_CONTRACT):
    result = [p for p in continuity_plans() if p["task"] == TASKS[1]]
    for i, (seed, segments) in enumerate(itertools.product((0.006, 0.050), (12, 24)), 21):
        actions = [
            *reference_actions(TASKS[1])[:8],
            {"operation": "seed_crystals", "seed_mass_g": seed},
        ]
        initial = (
            301.78284041654524  # Historical public thermometer reading, not latent parameters.
        )
        for j in range(1, segments + 1):
            actions.append(
                {
                    "operation": "cool_crystallize",
                    "target_temperature_K": initial + (278.15 - initial) * j / segments,
                    "duration_s": 14400,
                }
            )
            if j % (segments // 4) == 0:
                actions.append(PARTICLE)
        actions += [
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "filter_crystals"},
            *CLOSE,
        ]
        result.append(
            {"cell": f"C{i:02}", "task": TASKS[1], "kind": "reference", "actions": actions}
        )
    return [{**p, "contract": contract, "process_time_limit_s": 360000} for p in result]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--phase", choices=("reference", "agent"), default="reference")
    parser.add_argument(
        "--contract",
        choices=(FULL_PROCESS_THERMAL_CONTRACT, FULL_PROCESS_SEED_CONTRACT),
        default=FULL_PROCESS_THERMAL_CONTRACT,
    )
    args = parser.parse_args()
    root = (ROOT / args.output).resolve()
    root.mkdir(parents=True, exist_ok=True)
    planned = thermal_plans(args.contract)
    write(root / "planned_candidates.json", planned)
    selected = (
        planned
        if args.phase == "reference"
        else (
            [
                {
                    "cell": "A2",
                    "task": TASKS[1],
                    "kind": "agent",
                    "contract": args.contract,
                    "process_time_limit_s": 360000,
                }
            ]
            if any(read(root / p["cell"] / "result.json").get("witness") for p in planned)
            else []
        )
    )
    progress = {"stage": "starting", "completed": 0, "total": len(selected), "operations": 0}
    stop, started = threading.Event(), time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            rate = progress["completed"] / elapsed
            print(
                json.dumps(
                    {
                        **progress,
                        "elapsed_s": round(elapsed),
                        "units_per_min": 60 * rate,
                        "eta_s": (len(selected) - progress["completed"]) / rate if rate else None,
                    }
                ),
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    try:
        for plan in selected:
            execute(root, plan, progress)
    finally:
        stop.set()
        worker.join()


if __name__ == "__main__":
    main()
