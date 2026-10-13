"""W2-251: execute only the 42 missing cells, retaining W2-249 unchanged."""

from __future__ import annotations

import argparse
import copy
import subprocess
import threading
from pathlib import Path

from scripts import run_research_formation as base
from scripts.run_paper_case_notebooks import ROOT, case_folder, emit, execute_case, read, write

NOTE = "workstreams/flagship_tasks/WORK_II_RESEARCH_EXTENSION_20261014.md"
MODE = "research-formation-coverage-extension-42"
REPEATS = base.REPEATS
ARMS = ("Opaque", "Aligned", "MisIndexed")


def full_cases():
    return [
        {
            "id": f"{system}-W{world:02d}-{arm}",
            "system": system,
            "world": f"W{world:02d}",
            "arm": arm,
            "cell": (
                f"EQ-W{world:02d}--{arm}" if system == "EQ" else f"C-W{world:02d}-B12-E-{arm}"
            ),
            "model": "gpt-5.6-sol",
            "batches": 12,
        }
        for world in range(1, 6)
        for system in ("EQ", "C")
        for arm in ARMS
    ]


def cases():
    retained = {r["id"] for r in base.cases()}
    return [r for r in full_cases() if r["id"] not in retained]


def schedule():
    lookup = {(c["system"], c["world"], c["arm"]): c for c in cases()}
    rows = []
    for index, repeat in enumerate(REPEATS):
        worlds = [1, 2, 3, 4, 5]
        worlds = worlds[index * 2 :] + worlds[: index * 2]
        arms = (ARMS, ("MisIndexed", "Aligned", "Opaque"), ("Aligned", "Opaque", "MisIndexed"))[
            index
        ]
        for world in worlds:
            for system in ("EQ", "C"):
                for arm in arms:
                    row = lookup.get((system, f"W{world:02d}", arm))
                    if row:
                        rows.append({"repeat": repeat, **row})
    return rows


def prepare(root, parent):
    from scripts import run_work_ii_c_formal as c
    from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq

    previous = read(parent / "design.json")
    state = read(parent / "summary.json")
    if state["terminal_sources"] != 48 or state["active_units"]:
        raise ValueError("Parent must retain all 48 terminal dispositions")
    retained = {(u["repeat"], u["id"]) for u in previous["schedule"]}
    additions = {(u["repeat"], u["id"]) for u in schedule()}
    if len(retained | additions) != 90 or retained & additions:
        raise ValueError("Extension must cover exactly the 42 missing slots")
    original = ROOT / previous["C_original"]["path"]
    c_design = read(original)
    wanted = {r["cell"] for r in cases() if r["system"] == "C"}
    c_design["schedule"] = [r for r in c_design["schedule"] if r["id"] in wanted]
    if c_design["protocol"] != "c-quality-recovery-formal-v3-en" or len(c_design["schedule"]) != 9:
        raise ValueError("Original C inputs do not cover all nine extension conditions")
    config = previous["eq_config"]
    available = {r["cell_id"] for r in eq.validate_design(config)["schedule"]}
    if not {r["cell"] for r in cases() if r["system"] == "EQ"} <= available:
        raise ValueError("Original EQ inputs do not cover MisIndexed")
    if previous["provider"] != c.pilot.ec.PROVIDER or c_design["model"] != previous["provider"]:
        raise ValueError("Preserve the parent model and effort")
    c_design.update(
        planned_sources=9,
        planned_batches=108,
        planned_posttests=27,
        planned_retests=9,
        mode=MODE,
        automatic_retries=0,
        experiment_note=NOTE,
    )
    root.mkdir(parents=True, exist_ok=False)
    design = {
        "mode": MODE,
        "experiment_note": NOTE,
        "parent_root": str(parent.resolve()),
        "parent_source_commit": previous["source_commit"],
        "parent_schedule": previous["schedule"],
        "schedule": schedule(),
        "cases": cases(),
        "full_cases": full_cases(),
        "repeats": REPEATS,
        "concurrency": 4,
        "planned_sources": 42,
        "planned_source_batches": 504,
        "planned_posttests": 141,
        "planned_reference_batches": 24,
        "reused_reference_batches": 336,
        "maximum_recommendation_retests": 27,
        "source_retries": 0,
        "provider_sampling_seed_control": "unavailable; fresh independent sessions",
        "provider": previous["provider"],
        "eq_config": config,
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "runtime_surface": c.runtime_surface(),
        "worker_module": "scripts.run_research_extension",
        "cohort_limitation": "48 retained + 42 later sessions, not a concurrent randomized block",
    }
    write(root / "design.json", design)
    for repeat in REPEATS:
        write(
            root / repeat / "design.json",
            {
                "source_commit": design["source_commit"],
                "eq_config": config,
                "mode": MODE,
                "cases": cases(),
                "experiment_note": NOTE,
            },
        )
        write(root / repeat / "C/design.json", copy.deepcopy(c_design))


def references(root, progress):
    from scripts import run_work_ii_c_formal as c

    parent = Path(read(root / "design.json")["parent_root"])
    truth = read(parent / "references/truth.json")
    write(root / "references/truth.json", truth)
    for repeat in REPEATS:
        write(root / repeat / "references/truth.json", truth)
    design = read(root / REPEATS[0] / "C/design.json")
    completed, operations = 0, 0
    for world in range(1, 6):
        if world in base.C_WORLDS:
            result = read(parent / "references" / f"C-W{world:02d}/result.json")
            write(root / "references" / f"C-W{world:02d}/result.json", result)
        else:
            progress.update(stage="references", unit=f"C-W{world:02d}")
            result = c.fixed(
                root / "references" / f"C-W{world:02d}",
                [a for q in design["queries"] for a in q["actions"]],
                world_seed=world - 1,
                batches=12,
            )
            completed += len(result["batches"])
            operations += result["operations"]
        if not result["passed"] or len(result["batches"]) != 12:
            raise RuntimeError(f"C reference defect: W{world:02d}")
        for repeat in REPEATS:
            write(root / repeat / "C/qualification" / f"W{world:02d}/queries/result.json", result)
        progress.update(reference_batches=completed, reference_operations=operations)
        write(root / "references/progress.json", progress)
        emit(progress)
    write(
        root / "references/complete.json",
        {
            "completed_batches": completed,
            "operations": operations,
            "trajectories": 2,
            "reused_batches": 336,
            "reused_trajectories": 28,
            "available_batches": 360,
            "replay_verified": True,
            "shared_by_all_source_repetitions": True,
            "reused_from": str(parent / "references/complete.json"),
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--parent", type=Path)
    parser.add_argument("--unit", choices=["references", *(c["id"] for c in cases())])
    parser.add_argument("--repeat", choices=REPEATS)
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.summarize:
        emit(base.snapshot(root))
        return 0
    if not args.unit:
        if args.parent is None:
            parser.error("--parent is required when preparing the extension")
        prepare(root, args.parent)
        return base.coordinate_prepared(root)
    progress, stop = {"stage": args.unit}, threading.Event()

    def heartbeat():
        while not stop.wait(30):
            emit(progress)

    threading.Thread(target=heartbeat, daemon=True).start()
    try:
        if args.unit == "references":
            references(root, progress)
        else:
            if not args.repeat:
                parser.error("--repeat is required for sources")
            unit = next(
                u for u in schedule() if u["id"] == args.unit and u["repeat"] == args.repeat
            )
            if (
                case_folder(root / args.repeat, unit).exists()
                or base.result_path(root, unit).exists()
            ):
                raise RuntimeError("Source already started; no overwrite or retry")
            result = execute_case(root / args.repeat, unit, progress)
            write(base.result_path(root, unit), result)
            base.validate_result(result)
    finally:
        stop.set()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
