"""Fixed 45-session C block with one consistent full-process recovery definition."""

from __future__ import annotations

import argparse
import copy
import hashlib
import subprocess
import threading
from pathlib import Path

from scripts import run_research_extension as extension
from scripts import run_research_formation as base
from scripts.run_paper_case_notebooks import ROOT, case_folder, emit, execute_case, read, write

NOTE = "workstreams/flagship_tasks/WORK_II_C_RECOVERY_ALIGNMENT_20261014.md"
MODE = "c-initial-charge-recovery-aligned-45"
REPEATS = base.REPEATS
DEFAULT_INPUT = ROOT / "runs/formal/work-ii-c-five-world-20260920-v3-auto/design.json"
DEFAULT_REFERENCES = Path(
    "D:/Projects/ChemWorld-local-research/20261014-research-extension/attempt-01/references"
)


def cases():
    return [c for c in extension.full_cases() if c["system"] == "C"]


def schedule():
    lookup = {(c["world"], c["arm"]): c for c in cases()}
    rows = []
    for index, repeat in enumerate(REPEATS):
        worlds = list(range(1, 6))
        worlds = worlds[index * 2 :] + worlds[: index * 2]
        arms = (
            extension.ARMS,
            ("MisIndexed", "Aligned", "Opaque"),
            ("Aligned", "Opaque", "MisIndexed"),
        )[index]
        for world in worlds:
            rows.extend({"repeat": repeat, **lookup[(f"W{world:02d}", arm)]} for arm in arms)
    return rows


def prepare(root, original=DEFAULT_INPUT, references_root=DEFAULT_REFERENCES):
    from scripts import run_work_ii_c_formal as c

    original = original.resolve()
    previous = read(original)
    if previous["protocol"] != "c-quality-recovery-formal-v3-en":
        raise ValueError("Expected retained C-v3 design")
    if previous["model"] != c.pilot.ec.PROVIDER:
        raise ValueError("Preserve original Sol medium provider")
    wanted = {row["cell"] for row in cases()}
    study = copy.deepcopy(previous)
    study["schedule"] = [row for row in study["schedule"] if row["id"] in wanted]
    if len(study["schedule"]) != 15 or {r["id"] for r in study["schedule"]} != wanted:
        raise ValueError("Expected all fifteen original C conditions")
    # Keep archived designs immutable; change only explicitly listed public definitions.
    study.update(
        protocol="c-quality-initial-charge-recovery-v4-en",
        systems={"12": c.source_system(12)},
        Q=c.pilot.prediction_question(study["queries"]),
        budgets=[12],
        planned_sources=15,
        planned_batches=180,
        planned_posttests=45,
        planned_retests=15,
        mode=MODE,
        experiment_note=NOTE,
        automatic_retries=0,
        recovery_definition=c.pilot.CRYSTAL_RECOVERY_DEFINITION,
    )
    for world in range(1, 6):
        if not (references_root / f"C-W{world:02d}/result.json").exists():
            raise FileNotFoundError(f"Missing retained reference for world {world}")
    root.mkdir(parents=True, exist_ok=False)
    design = {
        "mode": MODE,
        "experiment_note": NOTE,
        "schedule": schedule(),
        "cases": cases(),
        "repeats": REPEATS,
        "concurrency": 4,
        "planned_sources": 45,
        "planned_source_batches": 540,
        "planned_posttests": 135,
        "planned_reference_batches": 60,
        "planned_reference_trajectories": 5,
        "maximum_recommendation_retests": 45,
        "source_retries": 0,
        "provider_sampling_seed_control": "unavailable; fresh model sessions",
        "provider": previous["model"],
        "recovery_definition": c.pilot.CRYSTAL_RECOVERY_DEFINITION,
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "runtime_surface": c.runtime_surface(),
        "worker_module": "scripts.run_c_recovery_aligned",
        "C_original": {
            "path": str(original),
            "sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
        },
        "retained_references": str(references_root.resolve()),
        "cohort_limitation": "Corrected protocol; not a randomized prompt-effect comparison",
    }
    write(root / "design.json", design)
    for repeat in REPEATS:
        write(
            root / repeat / "design.json",
            {
                "source_commit": design["source_commit"],
                "mode": MODE,
                "cases": cases(),
                "experiment_note": NOTE,
            },
        )
        write(root / repeat / "C/design.json", copy.deepcopy(study))


def references(root, progress):
    from scripts import run_work_ii_c_formal as c

    design = read(root / "design.json")
    study = read(root / REPEATS[0] / "C/design.json")
    completed, operations = 0, 0
    for world in range(1, 6):
        progress.update(stage="references", unit=f"C-W{world:02d}")
        result = c.fixed(
            root / "references" / f"C-W{world:02d}",
            [a for q in study["queries"] for a in q["actions"]],
            world_seed=world - 1,
            batches=12,
        )
        old = read(Path(design["retained_references"]) / f"C-W{world:02d}/result.json")
        if not result["passed"] or len(result["batches"]) != 12:
            raise RuntimeError(f"Reference execution defect in W{world:02d}")
        if result["truth"] != old["truth"]:
            raise RuntimeError(f"Numerical semantics changed in W{world:02d}; stop before sources")
        completed += len(result["batches"])
        operations += result["operations"]
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
            "trajectories": 5,
            "replay_verified": True,
            "retained_truth_equal": True,
            "shared_by_all_source_repetitions": True,
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--unit", choices=["references", *(c["id"] for c in cases())])
    parser.add_argument("--repeat", choices=REPEATS)
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.summarize:
        emit(base.snapshot(root))
        return 0
    if not args.unit:
        prepare(root)
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
                u
                for u in read(root / "design.json")["schedule"]
                if u["id"] == args.unit and u["repeat"] == args.repeat
            )
            if (
                case_folder(root / args.repeat, unit).exists()
                or base.result_path(root, unit).exists()
            ):
                raise RuntimeError("Source already started; no retry or overwrite")
            result = execute_case(root / args.repeat, unit, progress)
            write(base.result_path(root, unit), result)
            base.validate_result(result)
    finally:
        stop.set()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
