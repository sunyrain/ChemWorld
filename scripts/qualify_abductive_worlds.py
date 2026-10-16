"""Execute the fixed, provider-free W2-263 physical qualification block."""

from __future__ import annotations

import argparse
import copy
import json
import time
from pathlib import Path

from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq

from chemworld.data.logging import load_jsonl
from chemworld.physchem.abductive_worlds import (
    ASSAY_STD,
    METRICS,
    NOTE,
    build_config,
    build_queries,
    build_worlds,
    diagnostic_queries,
    initial_queries,
    solve_query,
)


def write(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def kernel_qualification() -> dict:
    queries = initial_queries() + diagnostic_queries() + build_queries()
    states, failures = [], []
    for world in build_worlds():
        for query in queries:
            try:
                row = solve_query(world, query)
                states.append(row)
                if row["physical_state"]["equilibrium_residual"] > 1e-7:
                    failures.append(
                        {
                            "world_id": world["world_id"],
                            "query_id": query["query_id"],
                            "reason": "closure residual exceeds 1e-7",
                        }
                    )
            except Exception as exc:
                failures.append(
                    {
                        "world_id": world["world_id"],
                        "query_id": query["query_id"],
                        "reason": f"{type(exc).__name__}: {exc}",
                    }
                )
    by_key = {(r["world_id"], r["query_id"]): r for r in states}
    pairs = []
    for pair in range(1, 6):
        gaps = []
        for query in initial_queries() + diagnostic_queries():
            try:
                a = by_key[(f"EQ-P{pair:02d}-A", query["query_id"])]["metrics"]
                b = by_key[(f"EQ-P{pair:02d}-B", query["query_id"])]["metrics"]
            except KeyError:
                continue
            scaled = {m: abs(a[m] - b[m]) / ASSAY_STD[m] for m in METRICS}
            gaps.append(
                {
                    "query_id": query["query_id"],
                    "gap_sigma": scaled,
                    "channels_above_three_sigma": sum(v >= 3 for v in scaled.values()),
                }
            )
        anchors = [r for r in gaps if r["query_id"].startswith("I")]
        diagnostic = [r for r in gaps if r["query_id"].startswith("D")]
        overlap = len(anchors) == 2 and all(max(r["gap_sigma"].values()) <= 1 for r in anchors)
        one = sum(r["channels_above_three_sigma"] >= 1 for r in diagnostic)
        two = sum(r["channels_above_three_sigma"] >= 2 for r in diagnostic)
        passed = overlap and one >= 3 and two >= 2
        pairs.append(
            {
                "match_id": f"P{pair:02d}",
                "initial_overlap": overlap,
                "one_channel_diagnostic_conditions": one,
                "two_channel_diagnostic_conditions": two,
                "gaps": gaps,
                "passed": passed,
            }
        )
        if not passed:
            failures.append({"match_id": f"P{pair:02d}", "reason": "pair acceptance failed"})
    controls = []
    for world in build_worlds():
        for target, controls_ids in (
            ("Q04", ("Q07", "Q08")),
            ("Q05", ("Q09", "Q10")),
            ("Q06", ("Q11", "Q12")),
        ):
            for control in controls_ids:
                try:
                    left = by_key[(world["world_id"], target)]["metrics"]
                    right = by_key[(world["world_id"], control)]["metrics"]
                    gap = max(abs(left[m] - right[m]) for m in METRICS)
                except KeyError:
                    gap = None
                passed = gap is not None and gap <= 1e-9
                controls.append(
                    {
                        "world_id": world["world_id"],
                        "target": target,
                        "control": control,
                        "max_gap": gap,
                        "passed": passed,
                    }
                )
                if not passed:
                    failures.append(
                        {
                            "world_id": world["world_id"],
                            "query_id": control,
                            "reason": "scale/path equality failed",
                        }
                    )
    return {
        "note": NOTE,
        "status": "development_qualification",
        "planned_states": len(build_worlds()) * len(queries),
        "completed_states": len(states),
        "states": states,
        "pairs": pairs,
        "controls": controls,
        "failures": failures,
        "passed": not failures,
    }


def runtime_qualification(raw_root: Path, report: Path) -> dict:
    config = build_config(eq.load_config())
    planned = len(config["worlds"]) * (
        len(initial_queries()) + len(diagnostic_queries()) + len(build_queries())
    )
    rows, failures = [], []
    started = time.monotonic()
    for world in config["worlds"]:
        for group, queries in (
            ("initial", initial_queries()),
            ("diagnostic", diagnostic_queries()),
            ("heldout", build_queries()),
        ):
            folder = raw_root / world["world_id"] / group
            match_id = world["private_authoring"]["match_id"]
            run_config = copy.deepcopy(config)
            if group == "initial":
                run_config["source_resource_card"]["solvent_L"] = 0.96
            result = eq.reference_run(
                folder,
                [a for q in queries for a in q["actions"]],
                config=run_config,
                world=world,
                batches=len(queries),
                observation_seed=eq.deterministic_seed("abductive-qualification", match_id, group),
                observation_namespace=f"abductive-qualification-{match_id}-{group}",
            )
            records = (
                load_jsonl(folder / "trajectory.jsonl")
                if (folder / "trajectory.jsonl").exists()
                else []
            )
            batches = result["batches"]
            passed = (
                result["failure"] is None
                and len(batches) == len(queries)
                and not result["rollbacks"]
                and result["exact_replay"].get("verified", False)
            )
            row = {
                "world_id": world["world_id"],
                "group": group,
                "planned_assays": len(queries),
                "completed_assays": len(batches),
                "operation_attempts": result["operation_attempts"],
                "rollbacks": result["rollbacks"],
                "failure": result["failure"],
                "exact_replay": result["exact_replay"],
                "passed": passed,
                "observations": [
                    {
                        "query_id": query["query_id"],
                        "metrics": {m: batch["metrics"].get(m) for m in METRICS},
                        "submitted_actions": batch["actions"],
                    }
                    for query, batch in zip(queries, batches, strict=False)
                ],
                "operation_state_deltas": [
                    {
                        "operation": r.get("operation_type"),
                        "action": r.get("action"),
                        "transaction_status": r.get("transaction_status"),
                        "delta": r.get("state_delta_summary"),
                        "patches": r.get("state_patches_summary"),
                    }
                    for r in records
                    if r.get("operation_type") in {"add_reagent", "add_solvent"}
                ],
            }
            rows.append(row)
            if group == "initial" and passed:
                write(
                    report.parent / "starter-observations" / f"{world['world_id']}.json",
                    {
                        "source": (
                            "Two standardized preliminary assays, before your autonomous research."
                        ),
                        "scope": (
                            "These are actual observations of this world; "
                            "they do not establish a mechanism."
                        ),
                        "instrument": "final_assay",
                        "measurement_standard_deviation": ASSAY_STD,
                        "reference_assays": [
                            {
                                "reference_id": f"R{i:02d}",
                                "actions": query["actions"],
                                "observed": {m: batch["metrics"].get(m) for m in METRICS},
                            }
                            for i, (query, batch) in enumerate(
                                zip(queries, batches, strict=True), 1
                            )
                        ],
                    },
                )
            if not passed:
                failures.append(
                    {
                        "world_id": world["world_id"],
                        "group": group,
                        "reason": "runtime acceptance failed",
                    }
                )
            elapsed = time.monotonic() - started
            summary = {
                "note": NOTE,
                "planned_campaigns": 30,
                "completed_campaigns": len(rows),
                "planned_assays": planned,
                "completed_assays": sum(r["completed_assays"] for r in rows),
                "rows": rows,
                "failures": failures,
                "passed": len(rows) == 30 and not failures,
            }
            write(report, summary)
            print(
                json.dumps(
                    {
                        "stage": "physical-runtime",
                        "campaigns": f"{len(rows)}/30",
                        "assays": f"{summary['completed_assays']}/{planned}",
                        "failures": len(failures),
                        "campaigns_per_minute": 60 * len(rows) / max(elapsed, 0.01),
                        "eta_seconds": elapsed / len(rows) * (30 - len(rows)),
                    }
                ),
                flush=True,
            )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--kernel-only", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if (args.output / "kernel.json").exists():
        raise FileExistsError("Retain the previous attempt; choose a fresh output directory")
    kernel = kernel_qualification()
    write(args.output / "kernel.json", kernel)
    print(
        json.dumps(
            {
                "stage": "physical-kernel",
                "states": f"{kernel['completed_states']}/{kernel['planned_states']}",
                "passed": kernel["passed"],
                "failures": kernel["failures"],
            }
        ),
        flush=True,
    )
    if not args.kernel_only:
        runtime = runtime_qualification(args.raw_root, args.output / "runtime.json")
        write(
            args.output / "summary.json",
            {
                "note": NOTE,
                "kernel_passed": kernel["passed"],
                "runtime_passed": runtime["passed"],
                "passed": kernel["passed"] and runtime["passed"],
                "planned_kernel_states": kernel["planned_states"],
                "completed_kernel_states": kernel["completed_states"],
                "planned_runtime_assays": runtime["planned_assays"],
                "completed_runtime_assays": runtime["completed_assays"],
                "failures": kernel["failures"] + runtime["failures"],
            },
        )


if __name__ == "__main__":
    main()
