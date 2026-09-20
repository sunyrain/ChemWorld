"""Provider-free C domain accessibility diagnostic; never launches source agents."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import statistics
import time
from pathlib import Path

from scripts import run_work_ii_c_formal as c
from scripts.run_work_ii_c_world_redesign import precondition
from scripts.run_work_ii_final_diagnostic import read, write

SEEDS = (0, 1, 2, 3, 4, 41, 47)


def candidates():
    return [
        {
            "id": f"G{i:02d}",
            "solvent": solvent,
            "reagent_mol": reagent,
            "volume_L": volume,
            "actions": precondition(
                c.process(
                    solvent=solvent,
                    reagent=reagent,
                    volume=volume,
                    seed=0.045,
                    path=c.gentle(segments=16),
                )
            ),
        }
        for i, (solvent, reagent, volume) in enumerate(
            itertools.product(range(4), (0.004, 0.006, 0.008), (0.020, 0.028, 0.040)), 1
        )
    ]


def initial_supersaturation(result):
    rows = result.get("host_diagnostics", [])
    if not rows:
        return None
    first = rows[0]
    temperature = first["temperature_history_K"][0]
    solubility = first["reference_solubility_mol_L"] * math.exp(
        -20000 / 8.314462618 * (1 / temperature - 1 / 298.15)
    )
    return first["feed_concentration_mol_L"] / solubility


def export(root, report):
    design, results = read(root / "design.json"), read(root / "results.json")
    units = [r for world in results.values() for r in world.values()]
    summary = {
        "development_only": True,
        "provider_calls": 0,
        "planned_batches": len(design["seeds"]) * len(design["candidates"]),
        "attempted_batches": len(units),
        "completed_batches": sum(len(r["batches"]) for r in units),
        "execution_replay_passes": sum(r["passed"] for r in units),
        "operations": sum(r["operations"] for r in units),
        "replay_steps": sum(r["exact_replay"].get("checked_steps", 0) for r in units),
        "recipe_wall_s": sum(r["elapsed_s"] for r in units),
        "worlds": {},
        "failures": [],
        "formal_launch": "hold: accessibility diagnostic is not twelve-query qualification",
    }
    lines = [
        "# Crystallization operating-domain diagnostic",
        "",
        "Development only; material laws, residuals, quality thresholds and agent budgets "
        "unchanged. All 36 recipes per world were declared before execution. "
        "No source agents or provider calls.",
        "",
        "| World seed | Completed / planned | Quality positive | Feasible recovery >= 0.10 "
        "| Best feasible recovery |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    detail = [
        "",
        "## Complete grid",
        "",
        "| World | Recipe | Solvent | Reagent (mol) | Volume (L) | Initial supersaturation "
        "| Recovery | Purity | Size | Fines | Feasible |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for seed in design["seeds"]:
        world = results.get(str(seed), {})
        feasible = []
        positive = 0
        entries = []
        for row in design["candidates"]:
            result = world.get(row["id"])
            if result is None:
                continue
            truth = result["truth"][0] if len(result["truth"]) == 1 else {}
            quality = result["passed"] and c.pilot.quality(truth)
            positive += quality
            is_feasible = quality and truth.get("crystal_yield", 0) >= 0.10
            if is_feasible:
                feasible.append((row["id"], truth["crystal_yield"]))
            ratio = initial_supersaturation(result)
            entries.append(
                {
                    "id": row["id"],
                    "truth": truth,
                    "initial_supersaturation": ratio,
                    "quality": quality,
                    "feasible": is_feasible,
                    "passed": result["passed"],
                    "solvent": row["solvent"],
                    "reagent_mol": row["reagent_mol"],
                    "volume_L": row["volume_L"],
                }
            )
            if not result["passed"]:
                summary["failures"].append(
                    {
                        "world": seed,
                        "recipe": row["id"],
                        "failure": result["failure"],
                        "replay": result["exact_replay"],
                    }
                )
            detail.append(
                f"| {seed} | {row['id']} | S{row['solvent']} "
                f"| {row['reagent_mol']} | {row['volume_L']} | "
                + (f"{ratio:.4f}" if ratio is not None else "missing")
                + " | "
                + " | ".join(f"{truth[m]:.6f}" if m in truth else "missing" for m in c.METRICS)
                + f" | {is_feasible} |"
            )
        best = max(feasible, key=lambda v: v[1]) if feasible else None
        summary["worlds"][str(seed)] = {
            "attempted": len(world),
            "quality_positive": positive,
            "feasible": len(feasible),
            "best_feasible": best,
            "recipes": entries,
        }
        best_text = f"{best[1]:.6f} ({best[0]})" if best else "none"
        lines.append(f"| {seed} | {len(world)} / 36 | {positive} | {len(feasible)} | {best_text} |")
    complete = len(units) == summary["planned_batches"]
    common = (
        sorted(
            set.intersection(
                *[
                    {row["id"] for row in world["recipes"] if row["feasible"]}
                    for world in summary["worlds"].values()
                ]
            )
        )
        if complete
        else []
    )
    summary["common_feasible_recipes"] = common
    summary["timing"] = {
        "median_recipe_s": statistics.median(r["elapsed_s"] for r in units) if units else None,
        "maximum_recipe_s": max((r["elapsed_s"] for r in units), default=None),
        "seconds_by_solvent": {
            str(solvent): sum(
                world[row["id"]]["elapsed_s"]
                for world in results.values()
                for row in design["candidates"]
                if row["id"] in world and row["solvent"] == solvent
            )
            for solvent in range(4)
        },
    }
    lines += [
        "",
        f"Completed {summary['completed_batches']}/{summary['planned_batches']} batches; "
        f"{summary['execution_replay_passes']} execution/replay passes; "
        f"{summary['operations']} operations and {summary['replay_steps']} replay steps. "
        f"Summed recipe wall time including replay: {summary['recipe_wall_s']:.3f} s.",
        "",
        "These results establish accessibility only in this declared grid. They do not "
        "prove that a 12-batch autonomous agent will find the feasible region. A separate "
        "query design and full qualification remain necessary before formal source launch.",
    ]
    if complete:
        lines += [
            "",
            "Common feasible recipes in all seven development worlds: "
            + (", ".join(common) if common else "none in this grid")
            + ".",
            "The median recipe plus replay took "
            f"{summary['timing']['median_recipe_s']:.3f} s; the slowest took "
            f"{summary['timing']['maximum_recipe_s']:.3f} s. "
            "These are diagnostic run times, not a controlled performance benchmark.",
        ]
        if "G01" in common:
            matches = [
                next(r for r in w["recipes"] if r["id"] == "G01")
                for w in summary["worlds"].values()
            ]
            yields = [r["truth"]["crystal_yield"] for r in matches]
            fines = [r["truth"]["crystal_fines_fraction"] for r in matches]
            lines += [
                "",
                "G01 uses S0, 0.004 mol reagent, 0.020 L solvent, catalyst 1, "
                "0.045 g seed, explicit 300 K preconditioning and sixteen 14,400 s "
                "cooling stages to 278.15 K. Recovery ranges from "
                f"{min(yields):.4f} to {max(yields):.4f}; fines from "
                f"{min(fines):.4f} to {max(fines):.4f}. "
                "It is a host feasibility witness, not a prescribed agent recipe. "
                "It was identified in development and is not an independent confirmation.",
                "",
                "Design decision: retain the physical family and quality limits. "
                "Use the accessible domain to redesign the six paired prediction contrasts "
                "before formal qualification. Preserve S1/S3 information-only perturbation, "
                "history contrasts and low/zero recovery cases; do not make the agent's "
                "exploration follow the host witness. Keep the failed original query set.",
            ]
    lines += [*detail, ""]
    write(report / "summary.json", summary)
    (report / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def run(root, report):
    root.mkdir(parents=True, exist_ok=False)
    rows = candidates()
    write(root / "design.json", {"seeds": SEEDS, "candidates": rows})
    results, started = {}, time.monotonic()
    total = len(SEEDS) * len(rows)
    for seed in SEEDS:
        results[str(seed)] = {}
        for row in rows:
            results[str(seed)][row["id"]] = c.fixed(
                root / f"world-{seed}" / row["id"],
                row["actions"],
                world_seed=seed,
                capture_diagnostics=True,
            )
            write(root / "results.json", results)
            done = sum(len(world) for world in results.values())
            elapsed = time.monotonic() - started
            print(
                json.dumps(
                    {
                        "stage": "domain diagnostic",
                        "completed": done,
                        "total": total,
                        "recipes_per_minute": 60 * done / elapsed,
                        "eta_s": elapsed / done * (total - done),
                    }
                ),
                flush=True,
            )
        export(root, report)
    export(root, report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    if args.report_only:
        export(args.root, args.report)
    else:
        run(args.root, args.report)
