"""Recompute C public baselines from retained observations; no simulator/provider calls."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean

from scripts import run_work_ii_c_formal as formal


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def recompute(root, report):
    saved = report / "summary.json"
    inputs = {saved, root / "design.json", root / "release.json"}
    cells = read(saved)["results"]
    queries = read(root / "design.json")["queries"]
    assert len(cells) == len({r["id"] for r in cells}) == 30
    for cell in cells:
        folder = root / "sources" / cell["id"]
        inputs.update(folder / name for name in ("trajectory.jsonl", "result.json"))
        inputs.add(root / "qualification" / cell["id"].split("-")[1] / "queries/result.json")
    before = {p: hashlib.sha256(p.read_bytes()).digest() for p in inputs}
    rows = []
    for index, cell in enumerate(cells, 1):
        records = formal.load_jsonl(root / "sources" / cell["id"] / "trajectory.jsonl")
        reference = read(root / "qualification" / cell["id"].split("-")[1] / "queries/result.json")
        truth = dict(zip((q["query_id"] for q in queries), reference["truth"], strict=True))
        assert cell["source"]["exact_replay"]["verified"]
        assert formal.pilot.ec.summaries(records) == cell["source"]["batches"]
        baseline = formal.public_baselines(records, queries, truth)
        assert baseline["available"]
        old = cell.get("public_baselines", {})
        if old.get("available"):
            assert old == baseline, cell["id"]
        predictions = {q["query_id"]: q for q in cell["posttests"]["Q"]["payload"]["predictions"]}
        response_diagnostics = {}
        for metric in formal.METRICS:
            observed = [b["metrics"][metric] for b in cell["source"]["batches"]]
            target = [truth[q["query_id"]][metric] for q in queries]
            predicted = [predictions[q["query_id"]][metric]["estimate"] for q in queries]
            errors = [a - b for a, b in zip(predicted, target, strict=True)]
            assert (
                abs(
                    fmean(abs(e) for e in errors)
                    - cell["prediction_evaluation"]["metrics"][metric]["mae"]
                )
                < 1e-12
            )
            response_diagnostics[metric] = {
                "source_observed_mean": fmean(observed),
                "source_observed_range": [min(observed), max(observed)],
                "reference_mean": fmean(target),
                "reference_range": [min(target), max(target)],
                "prediction_mean": fmean(predicted),
                "prediction_range": [min(predicted), max(predicted)],
                "signed_bias": fmean(errors),
                "underestimated_queries": sum(e < 0 for e in errors),
                "queries": len(errors),
            }
        rows.append(
            {
                "id": cell["id"],
                "arm": cell["arm"],
                "budget": cell["batches_budget"],
                "world": cell["id"].split("-")[1],
                "conforming": not bool(cell.get("retained_source_nonconformance")),
                "original_baseline": old,
                "public_baselines": baseline,
                "previously_available_unchanged": old == baseline,
                "repaired": not old.get("available", False),
                "resource_rejected_steps": [
                    r["step"]
                    for r in records
                    if r["transaction_status"] == "campaign_resource_rejected"
                ],
                "agent_mae": {
                    m: cell["prediction_evaluation"]["metrics"][m]["mae"] for m in formal.METRICS
                },
                "response_diagnostics": response_diagnostics,
            }
        )
        print(f"stage=baseline-reanalysis completed={index}/30", flush=True)
    assert sum(r["repaired"] for r in rows) == 2
    assert sum(r["previously_available_unchanged"] for r in rows) == 28
    assert all(hashlib.sha256(p.read_bytes()).digest() == h for p, h in before.items())
    groups = defaultdict(list)
    for r in rows:
        for metric in formal.METRICS:
            groups[r["budget"], metric].append(r)
    comparisons = []
    for (budget, metric), group in sorted(groups.items()):
        item = {
            "budget": budget,
            "metric": metric,
            "n": len(group),
            "agent_mae": fmean(r["agent_mae"][metric] for r in group),
        }
        for method in ("public_mean", "public_nearest_neighbor"):
            item[method + "_mae"] = fmean(
                r["public_baselines"]["mae"][method][metric] for r in group
            )
            item["agent_better_than_" + method] = sum(
                r["agent_mae"][metric] < r["public_baselines"]["mae"][method][metric] for r in group
            )
        comparisons.append(item)
    result = {
        "schema": "work-ii-c-baseline-reanalysis-1",
        "source_report": saved.as_posix(),
        "source_execution_commit": read(root / "release.json")["source_commit"],
        "scope": "Post hoc deterministic evaluator repair; original failures retained",
        "available": 30,
        "repaired": 2,
        "previously_available_unchanged": 28,
        "input_files_unchanged": True,
        "provider_calls": 0,
        "simulator_calls": 0,
        "rows": rows,
        "comparisons": comparisons,
    }
    (report / "BASELINE_REANALYSIS.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# C public-baseline reanalysis",
        "",
        "All 30 baselines are available: two omissions repaired and all 28 previously available "
        "results reproduced exactly. No provider or simulator calls; retained inputs unchanged.",
        "",
        "Rejected resource requests consume attempts but do not add material to the executed "
        "recipe. The extractor retains them as rejection provenance. Unknown statuses still fail.",
        "",
        "Original failures remain in `summary.json` and in each correction row. The current "
        "programme inventory explicitly consumes this correction; historical source results "
        "and release bindings are unchanged.",
        "",
        "| Repaired source | Original failure | Training final assays |",
        "|---|---|---:|",
    ]
    for r in rows:
        if r["repaired"]:
            lines.append(
                f"| {r['id']} | {r['original_baseline']['failure']} | "
                f"{r['public_baselines']['training_batches']} |"
            )
    lines += [
        "",
        "## Prediction comparison",
        "",
        "Both baselines fit only the source's public final observations. Saved query "
        "truth is used only for evaluation. They are simple references, not an optimal "
        "system-identification algorithm. All four metrics and both budgets are shown.",
        "",
        "| Budget | Metric | Agent MAE | Mean MAE | Nearest MAE | "
        "Agent wins vs mean | Agent wins vs nearest |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in comparisons:
        lines.append(
            f"| {r['budget']} | {r['metric']} | {r['agent_mae']:.5f} | "
            f"{r['public_mean_mae']:.5f} | {r['public_nearest_neighbor_mae']:.5f} | "
            f"{r['agent_better_than_public_mean']}/{r['n']} | "
            f"{r['agent_better_than_public_nearest_neighbor']}/{r['n']} |"
        )
    lines += [
        "",
        "Five physical world clusters underlie each budget, with three arms each; "
        "the fifteen cells are not fifteen independent worlds. C-W02/12/Opaque remains "
        "an eleven-assay source. Its valid observations are used without imputation. "
        "The nearest-neighbor recipe representation is retained unchanged and is limited; "
        "poor baseline performance does not establish mechanistic understanding.",
        "",
    ]
    (report / "BASELINE_REANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = recompute(args.root, args.report)
    print(
        json.dumps(
            {k: result[k] for k in ("available", "repaired", "previously_available_unchanged")}
        )
    )


if __name__ == "__main__":
    main()
