"""Read-only incremental notebook/results export for W2-249; never calls a provider."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from scripts.report_paper_case_notebooks import (
    crystallization_quality,
    equilibrium_diagnostics,
    notebook_record,
    posttest_record,
    readable_posttests,
    token_accounting,
)
from scripts.report_paper_case_stability import describe, measurements, seed_execution
from scripts.run_paper_case_notebooks import case_folder, emit, read, write


def export_case(root, unit, destination):
    repeat_root = root / unit["repeat"]
    result = read(repeat_root / "results" / f"{unit['id']}.json")
    source = result.get("source", result)
    folder = case_folder(repeat_root, unit)
    notes = notebook_record(folder)
    versions, calls = notes["versions"], notes["calls"]
    retest = result.get("recommendation_retest") or {}
    row = {
        **unit,
        "status": result["status"],
        "failure": result.get("failure"),
        "completed_batches": len(source.get("batches", [])),
        "operations": source.get("operations", 0),
        "exact_replay": source.get("exact_replay"),
        "rollbacks": source.get("rollbacks", []),
        "batch_outcomes": [
            {k: b.get(k) for k in ("lifecycle_index", "metrics", "actions")}
            for b in source.get("batches", [])
        ],
        "posttests": {
            stage: posttest_record(folder, stage, turn)
            for stage, turn in result.get("posttests", {}).items()
        },
        "posttest_validation": result.get("posttest_validation"),
        "prediction_evaluation": result.get("prediction_evaluation"),
        "source_usage": result.get("source_usage", source.get("usage")),
        "elapsed_s": result.get("elapsed_s"),
        "recommendation": result.get("recommendation", result.get("evidentiary_anchor")),
        "retest": {k: retest.get(k) for k in ("passed", "failure", "exact_replay", "truth")},
        "retest_operations": retest.get("operation_attempts", retest.get("operations", 0)),
        "retest_batch_metrics": [b.get("metrics") for b in retest.get("batches", [])],
        "notebook": {
            "version_count": len(versions),
            "read_calls": sum(r["tool"] == "notebook_read" and not r["error"] for r in calls),
            "tool_failures": sum(r["error"] for r in calls),
            "initial_note_before_action": versions[0]["public_cursor"]["event_count"] == 0
            if versions
            else None,
            "validation": notes["validation"],
            "versions": [{k: v for k, v in version.items() if k != "text"} for version in versions],
        },
    }
    row["token_accounting"] = token_accounting(
        row["source_usage"], row["posttests"], equilibrium=unit["system"] == "EQ"
    )
    row["equilibrium_diagnostics"] = equilibrium_diagnostics(repeat_root, folder, unit, result)
    row["crystallization_quality"] = crystallization_quality(unit, result)
    row["seed_execution"] = seed_execution(folder) if unit["system"] == "C" else None
    row["measurements"] = measurements(row)
    stages = ("K1", "Q", "K2", "EQS") if unit["system"] == "EQ" else ("K1", "Q", "K2")
    row["sealed_stages"] = [
        stage
        for stage in stages
        if row["posttests"].get(stage, {}).get("payload")
        and not row["posttests"][stage].get("failure")
        and (row["posttest_validation"] or {}).get(stage, {}).get("valid", True)
    ]
    row["missing_stages"] = [stage for stage in stages if stage not in row["sealed_stages"]]
    write(destination / unit["repeat"] / f"{unit['id']}.json", row)
    (destination / unit["repeat"] / f"{unit['id']}-reports.md").write_text(
        readable_posttests(unit, row["posttests"]), encoding="utf-8"
    )
    lines = [
        f"# {unit['repeat']} / {unit['id']} — source notebook",
        "",
        "Model-authored scientific records, not evaluator truth. "
        "Timestamps establish public statements, not private belief or causal influence.",
        "",
    ]
    for v in versions:
        lines += [
            f"## Revision {v['revision']}",
            "",
            f"Recorded: {v['recorded_at']}; available public operations: "
            f"{v['public_cursor']['event_count']}; reviewed through: {v['reviewed_through']}.",
            "",
            v["text"],
            "",
        ]
    if not versions:
        lines += ["No notebook revision recorded; retained as missing, not replaced.", ""]
    (destination / unit["repeat"] / f"{unit['id']}-notebook.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    return row


def build(root, destination):
    design = read(root / "design.json")
    rows = []
    for unit in design["schedule"]:
        if (root / unit["repeat"] / "results" / f"{unit['id']}.json").exists():
            row = export_case(root, unit, destination)
        else:
            row = {
                **unit,
                "status": "pending",
                "completed_batches": 0,
                "sealed_stages": [],
                "measurements": {},
            }
        rows.append(row)
    by_cell = {}
    for cell in design["cases"]:
        matching = [r for r in rows if r["id"] == cell["id"]]
        names = sorted({name for r in matching for name in r["measurements"]})
        by_cell[cell["id"]] = {
            name: describe([r["measurements"].get(name) for r in matching]) for name in names
        }
    terminal = [r for r in rows if r["status"] != "pending"]
    output = {
        "scope": design["mode"],
        "source_commit": design["source_commit"],
        "planned_sources": 48,
        "planned_batches": 576,
        "planned_posttests": 174,
        "planned_reference_batches": 336,
        "terminal_sources": len(terminal),
        "completed_sources": sum(r["status"] == "completed" for r in terminal),
        "completed_batches": sum(r["completed_batches"] for r in terminal),
        "sealed_posttests": sum(len(r["sealed_stages"]) for r in terminal),
        "source_replays_verified": sum(
            bool((r["exact_replay"] or {}).get("verified")) for r in terminal
        ),
        "notebook_versions": sum(r["notebook"]["version_count"] for r in terminal),
        "notebook_reads": sum(r["notebook"]["read_calls"] for r in terminal),
        "source_rollbacks": sum(len(r["rollbacks"]) for r in terminal),
        "notebook_tool_failures": sum(r["notebook"]["tool_failures"] for r in terminal),
        "reference": read(root / "references/complete.json"),
        "block_stop": read(root / "block-stop.json")
        if (root / "block-stop.json").exists()
        else None,
        "cell_descriptives": by_cell,
        "cases": [
            {k: v for k, v in r.items() if k not in {"batch_outcomes", "posttests"}} for r in rows
        ],
    }
    write(destination / "summary.json", output)
    lines = [
        "# Research formation — live scientific export",
        "",
        "Prospective current-core block. Original evidence is preserved. "
        "Three repetitions describe variability; they are not controlled model RNG seeds.",
        "",
        f"Terminal: {len(terminal)}/48; full chains: {output['completed_sources']}/48; "
        f"source batches: {output['completed_batches']}/576; "
        f"sealed stages: {output['sealed_posttests']}/174.",
        "",
        "Counts here describe exported terminal sessions; active batches are in the runner log.",
        "",
        "| Repeat | Cell | Status | Batches | Stages | Notes | Records |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for r in rows:
        prefix = f"{r['repeat']}/{r['id']}"
        link = (
            f"[notebook]({prefix}-notebook.md) / [reports]({prefix}-reports.md)"
            if r in terminal
            else "—"
        )
        lines.append(
            f"| {r['repeat']} | {r['id']} | {r['status']} | {r['completed_batches']}/12 | "
            f"{len(r['sealed_stages'])} | {r.get('notebook', {}).get('version_count', '—')} | "
            f"{link} |"
        )
    lines += [
        "",
        "All failed and missing stages remain in per-session JSON. The shared 336 "
        "reference batches are counted once. Individual outcomes and cell means/SD/ranges "
        "use explicit observed and missing denominators. No result is fed to participants.",
        "",
    ]
    (destination / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    while True:
        summary = build(args.root, args.output)
        emit({k: v for k, v in summary.items() if not isinstance(v, (dict, list))})
        state = read(args.root / "summary.json")
        if (
            not args.watch
            or summary["terminal_sources"] == 48
            or (state.get("block_stop") and not state.get("active_units"))
        ):
            return 0
        time.sleep(30)


if __name__ == "__main__":
    raise SystemExit(main())
