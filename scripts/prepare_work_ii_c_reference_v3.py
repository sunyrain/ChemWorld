"""Check one fixed C reference design before freezing the model experiment."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from scripts import run_work_ii_c_formal as c
from scripts.run_work_ii_c_world_redesign import acceptable, precondition
from scripts.run_work_ii_final_diagnostic import read, write

SEEDS = (41, 47)


def recipe(*, solvent=0, reagent=0.004, seed=0.045, path=None):
    return precondition(
        c.process(
            solvent=solvent,
            reagent=reagent,
            volume=0.020,
            seed=seed,
            path=c.gentle(segments=16) if path is None else path,
        )
    )


def queries():
    pairs = [
        [recipe(solvent=s) for s in (1, 3)],
        [recipe(seed=s) for s in (0.001, 0.045)],
        [
            recipe(seed=0.040, path=c.gentle(segments=18)),
            recipe(
                seed=0.040,
                path=[
                    c.pilot.cool(278.15, 120),
                    *[c.pilot.cool(278.15, 14400)] * 17,
                    c.pilot.cool(278.15, 14280),
                ],
            ),
        ],
        [
            recipe(seed=0.035, path=[*c.gentle(segments=20), c.pilot.cool(278.15, 7200)]),
            recipe(
                seed=0.035,
                path=[*c.gentle(segments=20), c.reheat(315, 3600), c.pilot.cool(278.15, 3600)],
            ),
        ],
        [
            recipe(seed=0.025, path=[c.pilot.cool(292, 60)]),
            recipe(seed=0.025, path=[c.pilot.cool(292, 60), c.pilot.cool(292, 7200)]),
        ],
        [recipe(reagent=r, path=c.gentle(segments=19)) for r in (0.004, 0.008)],
    ]
    rows = [
        {"query_id": f"Q{i:02d}", "pair": factor, "actions": actions}
        for i, (factor, actions) in enumerate(
            ((f, a) for f, pair in zip(c.FACTORS, pairs, strict=True) for a in pair), 1
        )
    ]
    assert len({json.dumps(r["actions"], sort_keys=True) for r in rows}) == 12
    assert max(len(r["actions"]) for r in rows) <= 60
    return rows


def export(root, report):
    design, result = read(root / "design.json"), read(root / "result.json")
    lines = [
        "# C reference v3 development acceptance",
        "",
        "Previously inspected development worlds; zero provider calls. Fixed recipes; "
        "unchanged physical laws, materials and thresholds.",
        "",
        f"Status: {result['status']}; passed: {result['passed']}.",
        "",
        "| Seed | Batches | Execution/replay | Quality positive | Negative | Feasible | Resolved |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for seed, world in result["worlds"].items():
        cov = world["coverage"]
        lines.append(
            f"| {seed} | {len(world['reference']['batches'])}/12 | "
            f"{world['reference']['passed']} | {cov.get('quality_positive')} | "
            f"{cov.get('quality_negative')} | {cov.get('feasible')} | "
            f"{cov.get('resolved_pairs')} |"
        )
    lines += [
        "",
        "| Seed | Query | Factor | Recovery | Purity | Size | Fines |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for seed, world in result["worlds"].items():
        for q, truth in zip(design["queries"], world["reference"]["truth"], strict=False):
            lines.append(
                f"| {seed} | {q['query_id']} | {q['pair']} | "
                + " | ".join(f"{truth[m]:.6f}" for m in c.METRICS)
                + " |"
            )
    lines += [
        "",
        "Formal sources require a separately committed/frozen execution surface and "
        "a full five-world qualification. No model source is started by this script.",
        "",
    ]
    write(report / "summary.json", result)
    (report / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def run(root, report):
    root.mkdir(parents=True, exist_ok=False)
    rows = queries()
    write(root / "design.json", {"seeds": SEEDS, "queries": rows, "resolution": c.RESOLUTION})
    result = {
        "status": "running",
        "passed": False,
        "planned_batches": 24,
        "provider_calls": 0,
        "worlds": {},
    }
    started = time.monotonic()
    for seed in SEEDS:
        value = c.fixed(
            root / f"world-{seed}",
            [a for q in rows for a in q["actions"]],
            world_seed=seed,
            batches=12,
        )
        coverage = c.coverage(value["truth"]) if len(value["truth"]) == 12 else {}
        result["worlds"][str(seed)] = {
            "reference": value,
            "coverage": coverage,
            "passed": value["passed"] and bool(coverage) and acceptable(coverage),
        }
        done = len(result["worlds"])
        elapsed = time.monotonic() - started
        print(
            json.dumps(
                {
                    "stage": "reference-v3 development",
                    "worlds": done,
                    "total": 2,
                    "worlds_per_minute": 60 * done / elapsed,
                    "eta_s": elapsed / done * (2 - done),
                }
            ),
            flush=True,
        )
        write(root / "result.json", result)
        export(root, report)
    result.update(
        status="completed",
        elapsed_s=time.monotonic() - started,
        passed=all(w["passed"] for w in result["worlds"].values()),
    )
    write(root / "result.json", result)
    write(
        root / "selection.json",
        {"acceptable": result["passed"], "queries": rows, "development_worlds": SEEDS},
    )
    export(root, report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    run(args.root, args.report)
