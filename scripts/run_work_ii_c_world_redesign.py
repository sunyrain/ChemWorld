"""Multi-world development calibration of complete crystallization references."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

from scripts import run_work_ii_c_formal as c
from scripts.run_work_ii_final_diagnostic import read, write

DEVELOPMENT_SEEDS = (17, 23, 31)


def precondition(actions):
    """Make the declared 300 K cooling start an actual charged operation."""
    rows = [dict(a) for a in actions]
    index = next(i for i, a in enumerate(rows) if a["operation"] == "seed_crystals")
    if rows[index - 1]["operation"] != "quench":
        raise ValueError("reference preconditioning must follow quench and precede seed")
    rows.insert(index, c.reheat(300.0, 300.0))
    return rows


def candidates():
    rows = c.calibration_candidates()
    mature = c.gentle(segments=16)
    extra = [
        ("solvent", [c.process(solvent=s, seed=0.045, path=mature) for s in (1, 3)]),
        ("seed", [c.process(seed=s, path=c.gentle(end=280, segments=16)) for s in (0.01, 0.045)]),
        (
            "cooling_history",
            [
                c.process(seed=0.04, path=mature),
                c.process(
                    seed=0.04,
                    path=[
                        c.pilot.cool(278.15, 120),
                        *[c.pilot.cool(278.15, 14400)] * 15,
                        c.pilot.cool(278.15, 14280),
                    ],
                ),
            ],
        ),
        (
            "thermal_history",
            [
                c.process(
                    seed=0.035, path=[*c.gentle(end=282, segments=16), c.pilot.cool(282, 7200)]
                ),
                c.process(
                    seed=0.035,
                    path=[
                        *c.gentle(end=282, segments=16),
                        c.reheat(315, 3600),
                        c.pilot.cool(282, 3600),
                    ],
                ),
            ],
        ),
        (
            "continue_growth",
            [
                c.process(seed=0.04, path=c.gentle(end=281, segments=16, duration=7200)),
                c.process(
                    seed=0.04,
                    path=[
                        *c.gentle(end=281, segments=16, duration=7200),
                        *[c.pilot.cool(281, 14400)] * 4,
                    ],
                ),
            ],
        ),
        (
            "upstream_loading",
            [c.process(reagent=r, seed=0.045, path=mature) for r in (0.008, 0.018)],
        ),
    ]
    for factor, pair in extra:
        for side, actions in enumerate(pair):
            rows.append(
                {
                    "id": f"D{len(rows) + 1:02d}",
                    "factor": factor,
                    "variant": "mature",
                    "side": side,
                    "actions": actions,
                }
            )
    for row in rows:
        row["actions"] = precondition(row["actions"])
        if len(row["actions"]) > 60:
            raise ValueError("reference exceeds the existing operation envelope")
    return rows


def acceptable(coverage):
    return (
        coverage["quality_positive"] >= 3
        and coverage["quality_negative"] >= 3
        and coverage["feasible"] >= 1
        and coverage["resolved_pairs"] >= 4
    )


def select(rows, results):
    options = [
        [
            [r for r in rows if r["factor"] == factor and r["variant"] == variant]
            for variant in dict.fromkeys(r["variant"] for r in rows if r["factor"] == factor)
        ]
        for factor in c.FACTORS
    ]
    best, combinations = None, 0
    for pairs in itertools.product(*options):
        chosen = [r for pair in pairs for r in pair]
        if len({json.dumps(r["actions"], sort_keys=True) for r in chosen}) != 12:
            continue
        if not all(
            results[str(seed)][r["id"]]["passed"] for seed in DEVELOPMENT_SEEDS for r in chosen
        ):
            continue
        combinations += 1
        cov = {
            str(seed): c.coverage([results[str(seed)][r["id"]]["truth"][0] for r in chosen])
            for seed in DEVELOPMENT_SEEDS
        }
        strength = sum(
            min(abs(p["deltas"][m]) / c.RESOLUTION[m], 5)
            for item in cov.values()
            for p in item["contrasts"]
            for m in c.METRICS
        )
        rank = (
            all(acceptable(v) for v in cov.values()),
            min(v["resolved_pairs"] for v in cov.values()),
            min(v["feasible"] for v in cov.values()),
            min(min(v["quality_positive"], v["quality_negative"]) for v in cov.values()),
            strength,
        )
        if best is None or rank > best[0]:
            best = rank, chosen, cov
    if best is None:
        return {"acceptable": False, "reason": "no complete unique candidate combination"}
    rank, chosen, cov = best
    return {
        "acceptable": rank[0],
        "rank": rank,
        "development_coverage": cov,
        "complete_unique_combinations": combinations,
        "queries": [
            {
                "query_id": f"Q{i:02d}",
                "pair": r["factor"],
                "calibration_id": r["id"],
                "actions": r["actions"],
            }
            for i, r in enumerate(chosen, 1)
        ],
    }


def export(root, report):
    design = read(root / "design.json")
    results = read(root / "results.json")
    selected = read(root / "selection.json") if (root / "selection.json").exists() else None
    acceptance = (
        read(root / "acceptance/qualification/result.json")
        if (root / "acceptance/qualification/result.json").exists()
        else None
    )
    units = [v for world in results.values() for v in world.values()]
    summary = {
        "development_only": True,
        "provider_calls": 0,
        "planned_calibration_batches": 108,
        "completed_calibration_batches": sum(len(r["batches"]) for r in units),
        "attempted_calibration_recipes": len(units),
        "passed_calibration_recipes": sum(r["passed"] for r in units),
        "calibration_operations": sum(r["operations"] for r in units),
        "calibration_replay_steps": sum(r["exact_replay"].get("checked_steps", 0) for r in units),
        "selection": selected,
        "acceptance": None
        if acceptance is None
        else {
            "status": acceptance["status"],
            "passed": acceptance["passed"],
            "worlds": {
                f"C-W{int(k) + 1:02d}": {
                    "checks": v["checks"],
                    "coverage": {
                        name: v["coverage"].get(name)
                        for name in (
                            "quality_positive",
                            "quality_negative",
                            "feasible",
                            "resolved_pairs",
                        )
                    },
                    "passed": v["passed"],
                }
                for k, v in acceptance["worlds"].items()
            },
            "completed_batches": sum(
                len(unit["batches"])
                for w in acceptance["worlds"].values()
                for unit in [w["reference"], *w["mapping"].values()]
            ),
            "operations": sum(
                unit["operations"]
                for w in acceptance["worlds"].values()
                for unit in [w["reference"], *w["mapping"].values()]
            ),
        },
        "failures": [
            {
                "world": seed,
                "candidate": key,
                "failure": r["failure"],
                "exact_replay": r["exact_replay"],
            }
            for seed, world in results.items()
            for key, r in world.items()
            if not r["passed"]
        ],
        "acceptance_failures": []
        if acceptance is None
        else [
            {
                "world": f"C-W{int(k) + 1:02d}",
                "failed_checks": [name for name, passed in v["checks"].items() if not passed],
            }
            for k, v in acceptance["worlds"].items()
            if not v["passed"]
        ],
    }
    write(report / "summary.json", summary)
    lines = [
        "# Crystallization world/task setting repair",
        "",
        "Development only. Physical laws and material/world distributions unchanged. "
        "References explicitly equilibrate the quenched mixture to 300 K before seeding. "
        "This reference operation is charged; it is not imposed on autonomous agents.",
        "",
        f"Calibration: {len(units)}/108 recipes attempted; "
        f"{summary['passed_calibration_recipes']} execution/replay passes. Provider calls: 0.",
        f"Selection acceptable across all three development worlds: "
        f"{selected['acceptable'] if selected else 'pending'}.",
        "",
        "| World | Candidate | Factor | Variant | Passed | Recovery | Purity | Size | Fines |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for seed in design["development_seeds"]:
        for row in design["candidates"]:
            value = results.get(str(seed), {}).get(row["id"])
            if value is None:
                continue
            truth = value["truth"][0] if value["truth"] else {}
            lines.append(
                f"| {seed} | {row['id']} | {row['factor']} | {row['variant']} | "
                f"{value['passed']} | "
                + " | ".join(f"{truth[m]:.6f}" if m in truth else "missing" for m in c.METRICS)
                + " |"
            )
    if selected:
        lines += [
            "",
            "Selected common candidate set: "
            + ", ".join(q["calibration_id"] for q in selected.get("queries", []))
            + ".",
        ]
    if summary["acceptance"]:
        a = summary["acceptance"]
        lines += [
            "",
            f"Five-world development acceptance: {a['status']}; passed={a['passed']}; "
            f"{a['completed_batches']}/75 reference batches.",
            "",
            "| World | Quality positive | Negative | Feasible recovery | Resolved pairs | Passed |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ]
        for world, values in a["worlds"].items():
            cov = values["coverage"]
            lines.append(
                f"| {world} | {cov['quality_positive']} | {cov['quality_negative']} | "
                f"{cov['feasible']} | {cov['resolved_pairs']} | {values['passed']} |"
            )
    lines += [
        "",
        "Old calibration, pilot and interrupted formal qualification are retained. "
        "These previously inspected five acceptance worlds are not a fresh confirmation set. "
        "No query or threshold changes are made after acceptance starts. "
        "No formal agent source has been launched by this block.",
        "",
    ]
    domain_path = report / "domain/summary.json"
    if domain_path.exists():
        domain = read(domain_path)
        lines += [
            "## Separate operating-domain diagnostic",
            "",
            f"Completed {domain['completed_batches']}/{domain['planned_batches']} batches; "
            f"{domain['execution_replay_passes']} execution/replay passes. "
            "See [complete domain results](domain/REPORT.md). "
            f"{sum(w['feasible'] > 0 for w in domain['worlds'].values())}/"
            f"{len(domain['worlds'])} development worlds have feasible recipes under unchanged "
            "physical laws and quality limits. This establishes accessibility, "
            "not twelve-query qualification.",
            "",
            "The first query acceptance failure is retained. Before a formal launch, "
            "redesign the six paired references around the demonstrated accessible domain, "
            "save them as a new block and qualify that block from its first unit. "
            "Do not prescribe these reference recipes to autonomous source agents.",
            "",
        ]
    (report / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def run(root, report):
    root.mkdir(parents=True, exist_ok=False)
    rows = candidates()
    write(
        root / "design.json",
        {"development_seeds": DEVELOPMENT_SEEDS, "candidates": rows, "resolution": c.RESOLUTION},
    )
    results, started = {}, time.monotonic()
    for seed in DEVELOPMENT_SEEDS:
        results[str(seed)] = {}
        for row in rows:
            value = c.fixed(root / f"world-{seed}" / row["id"], row["actions"], world_seed=seed)
            results[str(seed)][row["id"]] = value
            write(root / "results.json", results)
            done = sum(len(v) for v in results.values())
            elapsed = time.monotonic() - started
            print(
                json.dumps(
                    {
                        "stage": "multi-world calibration",
                        "completed": done,
                        "total": 108,
                        "recipes_per_minute": 60 * done / elapsed,
                        "eta_s": elapsed / done * (108 - done),
                    }
                ),
                flush=True,
            )
            export(root, report)
    selection = select(rows, results)
    write(root / "selection.json", selection)
    export(root, report)
    if not selection["acceptable"]:
        print("Calibration did not meet coverage; acceptance and model launch held.", flush=True)
        return
    c.configure(root / "acceptance", root, [12, 24])
    design = read(root / "acceptance/design.json")
    design.update(mode="development-acceptance", protocol="c-world-setting-development-v2-en")
    write(root / "acceptance/design.json", design)
    c.qualify(root / "acceptance", report / "acceptance")
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
