"""Fixed 36-cell process-continuity qualification and once-only Astra pilots."""

from __future__ import annotations

import argparse
import itertools
import json
import threading
import time
from copy import deepcopy
from pathlib import Path

from scripts.run_work_ii_astra_full_process_trial import ROOT, TASKS, reference_actions
from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_phase_resolved_process import CLOSE, PARTICLE, execute, plans

from chemworld.runtime.full_process_contract import FULL_PROCESS_POPULATION_CONTRACT


def continuity_plans():
    original = plans()
    result = []

    def add(cell, task, actions):
        result.append(
            {
                "cell": cell,
                "task": task,
                "actions": deepcopy(actions),
                "kind": "reference",
                "contract": FULL_PROCESS_POPULATION_CONTRACT,
            }
        )

    for i, (amount, extract, wash) in enumerate(
        itertools.product((0.002, 0.005), (0.030, 0.060), (0.008, 0.020)), 1
    ):
        p = deepcopy(next(p["actions"] for p in original if p["cell"] == "P22"))
        for a in p:
            if a["operation"] == "add_reagent":
                a["amount_mol"] = amount
            elif a["operation"] == "add_extractant":
                a.update(extractant=2, volume_L=extract)
            elif a["operation"] == "wash":
                a["wash_volume_L"] = wash
        add(f"P{i:02}", TASKS[0], p)
    for p in original:
        if p["task"] == TASKS[1]:
            add(p["cell"], p["task"], p["actions"])
    for i, (seed, duration) in enumerate(itertools.product((0.006, 0.05), (7200, 14400)), 17):
        add(
            f"C{i:02}",
            TASKS[1],
            [
                *reference_actions(TASKS[1])[:8],
                {"operation": "seed_crystals", "seed_mass_g": seed},
                {
                    "operation": "cool_crystallize",
                    "target_temperature_K": 278.15,
                    "duration_s": 7200,
                },
                PARTICLE,
                {
                    "operation": "heat",
                    "target_temperature_K": 295,
                    "duration_s": 300,
                    "stirring_speed_rpm": 600,
                },
                PARTICLE,
                {
                    "operation": "cool_crystallize",
                    "target_temperature_K": 278.15,
                    "duration_s": duration,
                },
                PARTICLE,
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "filter_crystals"},
                *CLOSE,
            ],
        )
    prefix = next(p["actions"] for p in original if p["cell"] == "D01")[:10]
    for i, (cut, duration, reflux) in enumerate(
        itertools.product((0.05, 0.10), (1800, 3600), (3, 10)), 1
    ):
        add(
            f"D{i:02}",
            TASKS[2],
            [
                *prefix,
                {
                    "operation": "distill",
                    "target_temperature_K": 365,
                    "duration_s": duration,
                    "reflux_ratio": reflux,
                    "cut_fraction": cut,
                },
                {"operation": "collect_fraction", "transfer_fraction": 1.0},
                {"operation": "measure", "instrument": "gc"},
                *CLOSE,
            ],
        )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--phase", choices=("reference", "agent"), default="reference")
    args = parser.parse_args()
    root = (ROOT / args.output).resolve()
    root.mkdir(parents=True, exist_ok=True)
    planned = continuity_plans()
    write(root / "planned_candidates.json", planned)
    selected = (
        planned
        if args.phase == "reference"
        else [
            {
                "cell": f"A{i + 1}",
                "task": t,
                "kind": "agent",
                "contract": FULL_PROCESS_POPULATION_CONTRACT,
            }
            for i, t in enumerate(TASKS)
            if any(
                read(root / p["cell"] / "result.json").get("witness")
                for p in planned
                if p["task"] == t
            )
        ]
    )
    progress = {"stage": "starting", "operations": 0, "completed": 0, "total": len(selected)}
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
