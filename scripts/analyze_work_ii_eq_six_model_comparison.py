"""Export public batch/prediction detail after the six-cell block terminates."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean

from run_work_ii_eq_six_model_comparison import (
    ARMS,
    DILUTE,
    MODELS,
    REPORT,
    folder,
    jobs,
    read,
    write,
)


def csv_write(path, rows):
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    root = args.input.resolve()
    summary = read(root / "summary.json")
    truth = read(root / "shared-reference/truth.json")
    batches, predictions, cells = [], [], []
    accounts = [
        "# Original public scientific accounts",
        "",
        "Verbatim sealed outputs of each original researcher, after its own experiments. "
        "These are public reports and forecast rationales, not internal reasoning traces. "
        "Reference outcomes were not supplied during these stages.",
    ]
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    queries = eq.queries(eq.load_config())
    for job in jobs():
        target = folder(root, job)
        grouped = defaultdict(list)
        trajectory = target / "trajectory.jsonl"
        records = (
            [json.loads(s) for s in trajectory.read_text(encoding="utf-8").splitlines()]
            if trajectory.exists()
            else []
        )
        for record in records:
            grouped[record["experiment_index"]].append(record)
        cell_batches = []
        for index, steps in grouped.items():
            committed = [s for s in steps if s.get("transaction_status") == "committed"]
            finals = [s for s in committed if s.get("instrument") == "final_assay"]
            if not finals:
                continue
            # Input concentration is not a hidden dissolved-state measurement.
            acid = sum(
                s["action"].get("amount_mol", 0)
                for s in committed
                if s["action"].get("operation") == "add_reagent"
            )
            volume = sum(
                s["action"].get("volume_L", 0)
                for s in committed
                if s["action"].get("operation") == "add_solvent"
            )
            row = {
                **job,
                "batch": index + 1,
                "operation_attempts": len(steps),
                "rollbacks": len(steps) - len(committed),
                "reagent_mol": acid,
                "solvent_L": volume,
                "nominal_input_concentration_M": acid / volume if volume else None,
                **{m: finals[-1]["observation"][m] for m in eq.METRICS},
                "operations": " > ".join(s["action"]["operation"] for s in committed),
            }
            cell_batches.append(row)
            batches.append(row)
        result_path = target / "RESULT.json"
        result = read(result_path) if result_path.exists() else {}
        concentrations = [r["nominal_input_concentration_M"] for r in cell_batches]
        cells.append(
            {
                **job,
                "batches": len(cell_batches),
                "operations": len(records),
                "rollbacks": sum(r.get("transaction_status") != "committed" for r in records),
                "concentration_M_range": [min(concentrations), max(concentrations)]
                if concentrations
                else None,
                "dissociation_range": [
                    min(r["acid_dissociation_fraction"] for r in cell_batches),
                    max(r["acid_dissociation_fraction"] for r in cell_batches),
                ]
                if cell_batches
                else None,
                "reagent_mol": sum(r["reagent_mol"] for r in cell_batches),
                "solvent_L": sum(r["solvent_L"] for r in cell_batches),
                "source_usage": {
                    key: result.get("source_usage", {}).get(key)
                    for key in (
                        "input_token_count",
                        "cached_input_token_count",
                        "uncached_input_token_count",
                        "output_token_count",
                        "session_elapsed_s",
                        "provider_process_attempt_count",
                        "provider_token_accounting_complete",
                    )
                },
                "full_chain_elapsed_s": result.get("elapsed_s"),
                "prediction_validation": None,
            }
        )
        accounts.extend(["", f"## {job['model']} / {job['arm']}"])
        for stage in ("K1", "Q", "K2", "EQS"):
            path = target / "sealed" / f"{stage}.json"
            if not path.exists():
                continue
            payload = read(path).get("payload")
            accounts.extend(
                ["", f"### {stage}", "", "```json", json.dumps(payload, indent=2), "```"]
            )
            if stage != "Q" or not eq.validate_posttest(stage, payload, queries)["valid"]:
                continue
            evaluated = eq.evaluate_predictions(payload, queries, truth)
            cells[-1]["prediction_validation"] = evaluated
            for prediction in payload["predictions"]:
                qid = prediction["query_id"]
                for metric in eq.METRICS:
                    p = prediction["metrics"][metric]
                    reference = [r[metric] for r in truth[qid]]
                    predictions.append(
                        {
                            **job,
                            "query_id": qid,
                            "group": "dilute_three" if qid in DILUTE else "other_nine",
                            "response": metric,
                            **p,
                            "reference_mean": fmean(reference),
                            "absolute_error": abs(p["estimate"] - fmean(reference)),
                            "covered_references": sum(
                                p["lower80"] <= y <= p["upper80"] for y in reference
                            ),
                            "reference_count": len(reference),
                        }
                    )
    csv_write(REPORT / "source_batches.csv", batches)
    csv_write(REPORT / "predictions.csv", predictions)
    write(REPORT / "trajectory_summary.json", cells)
    (REPORT / "PUBLIC_ACCOUNTS.md").write_text("\n".join(accounts) + "\n", encoding="utf-8")
    for cell in summary["cells"]:
        if cell["prediction_metrics"] is None:
            continue
        for group, metrics in cell["prediction_metrics"].items():
            rows = [
                p
                for p in predictions
                if p["model"] == cell["model"] and p["arm"] == cell["arm"] and p["group"] == group
            ]
            assert len(rows) == metrics["query_count"] * 3
            assert abs(fmean(p["absolute_error"] for p in rows) - metrics["macro_mae"]) < 1e-12
            assert (
                abs(fmean(p["covered_references"] / 5 for p in rows) - metrics["coverage80"])
                < 1e-12
            )
    plot(summary)
    print(json.dumps({"source_batches": len(batches), "scalar_predictions": len(predictions)}))


def plot(summary):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True, layout="constrained")
    colors = {"Opaque": "#596875", "Aligned": "#2D9A87"}
    ymax = max(
        g["macro_mae"]
        for c in summary["cells"]
        if c["prediction_metrics"]
        for g in c["prediction_metrics"].values()
    )
    for ax, group, title in zip(
        axes,
        ("other_nine", "dilute_three"),
        ("Other nine queries", "Three most dilute queries"),
        strict=True,
    ):
        for index, model in enumerate(MODELS):
            for arm, offset in zip(ARMS, (-0.18, 0.18), strict=True):
                cell = next(c for c in summary["cells"] if c["model"] == model and c["arm"] == arm)
                if not cell["prediction_metrics"]:
                    continue
                y = cell["prediction_metrics"][group]["macro_mae"]
                ax.bar(
                    index + offset,
                    y,
                    width=0.32,
                    color=colors[arm],
                    label=arm if index == 0 else None,
                )
                ax.text(index + offset, y + ymax * 0.025, f"{y:.3f}", ha="center", fontsize=9)
        ax.set_xticks(range(3), ["5.6 Luna", "5.6 Terra", "5.5"])
        ax.set_title(title, fontsize=12)
        ax.set_ylim(0, ymax * 1.2)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color="#E5E5E5", linewidth=0.7)
    axes[0].set_ylabel("Macro MAE (lower is better)")
    axes[0].legend(frameon=False)
    fig.savefig(REPORT / "comparison.png", dpi=180)
    fig.savefig(REPORT / "comparison.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
