#!/usr/bin/env python
"""Export sealed M1 results and scientific source data; never execute or refit a session."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_work_ii_factorial import read  # noqa: E402
from scripts.run_work_ii_factorial_replication import DEFAULT_OUTPUT, write_markdown  # noqa: E402


def export_report(root: Path, destination: Path) -> dict:
    sealed_summary = read(root / "summary.json")
    report = dict(sealed_summary)
    selections = read(root / "selections.json")
    protocol = read(root / "protocol.json")
    physical = read(root / "physical.json")
    report["representation_scope"] = (
        "Quadratic describes the permitted representation family on two-dimensional control "
        "coordinates. Simulator utilities are not assumed to be exact quadratic functions."
    )
    attempted = [row for row in selections["calls"] if row["status"] != "not_attempted"]
    usage_available = sum(
        all(key in row.get("usage", {}) for key in ("input_tokens", "output_tokens"))
        for row in attempted
    )
    report["provider_usage_coverage"] = {
        "attempted_calls": len(attempted),
        "with_input_and_output_usage": usage_available,
        "missing_usage_calls": len(attempted) - usage_available,
        "scope": "Token totals sum reported receipt usage. Missing usage is unknown, not zero "
        "billing; no currency or unreported billing overhead is estimated.",
    }
    report["physical_resources_by_role"] = []
    for task in sorted({row["task"] for row in physical["receipts"]}):
        for prefix, role in (("e", "public_evidence"), ("c", "hidden_evaluation")):
            receipts = [
                row
                for row in physical["receipts"]
                if row["task"] == task and row["id"].startswith(prefix)
            ]
            report["physical_resources_by_role"].append(
                {
                    "task": task,
                    "role": role,
                    "scheduled": len(receipts),
                    "completed": sum(row["status"] == "completed" for row in receipts),
                    **{
                        key: sum(row.get(key, 0) for row in receipts)
                        for key in (
                            "operation_count",
                            "measurement_cost",
                            "recipe_duration_s",
                            "reagent_amount_mol",
                            "wall_s",
                            "cpu_s",
                        )
                    },
                }
            )
    report["scientific_source_data"] = {
        "availability": "completed execution" if report["execution_valid"] else "stopped block",
        "source_artifacts": selections["artifacts"],
        "public_packets": {
            world["cluster_id"]: read(root / "public" / f"{world['cluster_id']}.json")
            for world in protocol["worlds"]
            if (root / "public" / f"{world['cluster_id']}.json").exists()
        },
        "candidate_scores_after_selections_sealed": read(root / "private_scores.json")
        if (root / "private_scores.json").exists()
        else {},
        "provider_calls": [
            {
                key: row[key]
                for key in (
                    "call_id",
                    "state_id",
                    "cluster_id",
                    "model",
                    "stage",
                    "status",
                    "usage",
                    "elapsed_s",
                    "failure_type",
                )
                if key in row
            }
            for row in selections["calls"]
        ],
        "scope": "Public-test worlds. Candidate scores were hidden throughout participant "
        "execution and are released only after choices were sealed. Scientific artifacts "
        "and token/timing totals are included; raw provider events, identities and credentials "
        "are excluded. This export changes no execution, selection, score or inference.",
    }
    if destination.exists():
        previous = read(destination)
        if any(previous.get(key) != value for key, value in sealed_summary.items()):
            raise ValueError("Publication destination already contains a different sealed result")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    markdown_path = destination.with_suffix(".md")
    with tempfile.TemporaryDirectory(prefix="chemworld-m1-export-") as scratch:
        draft = Path(scratch) / "report.md"
        write_markdown(draft, report)
        markdown_text = draft.read_text(encoding="utf-8")
    markdown_path.write_text(
        markdown_text.replace(
            "Contrast (negative favors first condition)", "Prespecified contrast"
        ).replace(
            report["interpretation"],
            report["interpretation"] + "\n\n" + report["representation_scope"],
            1,
        ),
        encoding="utf-8",
        newline="\n",
    )
    lines = [
        "",
        "For each simple contrast, negative regret favors the first condition. Interaction is "
        "(F-X minus L-X) minus (F-A minus L-A): a negative value means the representation "
        "replacement is more favorable under the maximizer than under the fresh agent.",
        "",
        "## Per-world paired effects",
        "",
        "Each value averages the two models and two repeats within one world. "
        "Repeats do not increase the independent-world denominator.",
        "",
    ]
    if report.get("statistics"):
        contrasts = [row["contrast"] for row in report["statistics"]["contrasts"]]
        lines += [
            "| World | " + " | ".join(contrasts) + " |",
            "| --- | " + " | ".join(["---:"] * len(contrasts)) + " |",
        ]
        for world in protocol["worlds"]:
            values = {
                row["contrast"]: row["mean_difference"]
                for row in report["statistics"]["world_contrasts"]
                if row["cluster_id"] == world["cluster_id"]
            }
            lines.append(
                "| "
                + world["cluster_id"]
                + " | "
                + " | ".join(f"{values[key]:.6f}" for key in contrasts)
                + " |"
            )
        lines += [
            "",
            "| Task mean (five worlds each) | " + " | ".join(contrasts) + " |",
            "| --- | " + " | ".join(["---:"] * len(contrasts)) + " |",
        ]
        for task in sorted({world["task"] for world in protocol["worlds"]}):
            values = [
                row["task_means"][task] for row in report["statistics"]["contrasts"]
            ]
            lines.append("| " + task + " | " + " | ".join(f"{v:.6f}" for v in values) + " |")
    lines += [
        "",
        "## Shared public baselines",
        "",
        "| World | Nearest evidence regret | Uniform random expected regret |",
        "| --- | ---: | ---: |",
    ]
    for row in report.get("baselines", []):
        nearest = row["nearest_public_regret"]
        lines.append(
            f"| {row['cluster_id']} | "
            + (f"{nearest:.6f}" if nearest is not None else "unavailable")
            + f" | {row['uniform_random_expected_regret']:.6f} |"
        )
    lines += [
        "",
        "## Artifact prediction and decision agreement",
        "",
        "Candidate MAE is descriptive, conditional on finite available predictions. "
        "Models/repeats remain nested within their shared world; fitted-law copies are "
        "not new evidence. Agreement uses pairs with both A and X available.",
        "",
        "| Model | Artifact | Finite MAE/scheduled | Mean candidate MAE | A/X agree/eligible |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for agreement in report.get("agreement", []):
        selected = [
            row
            for row in report["artifact_metrics"]
            if row["model"] == agreement["model"] and row["artifact"] == agreement["artifact"]
        ]
        finite = [row["candidate_mae"] for row in selected if row["candidate_mae"] is not None]
        error = f"{mean(finite):.6f}" if finite else "unavailable"
        lines.append(
            f"| {agreement['model']} | {agreement['artifact']} | {len(finite)}/{len(selected)} "
            f"| {error} | {agreement['agree']}/{agreement['eligible']} |"
        )
    lines += [
        "",
        "## Physical resources by role",
        "",
        "| Task | Role | Completed/scheduled | CPU seconds | Wall seconds | Measurement units |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in report["physical_resources_by_role"]:
        lines.append(
            f"| {row['task']} | {row['role']} | {row['completed']}/{row['scheduled']} "
            f"| {row['cpu_s']:.1f} | {row['wall_s']:.1f} | {row['measurement_cost']:g} |"
        )
    lines += [
        "",
        f"Input/output usage is reported for {usage_available}/{len(attempted)} attempted calls. "
        + report["provider_usage_coverage"]["scope"],
        "",
        report["scientific_source_data"]["scope"],
        "",
    ]
    with markdown_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = export_report(args.root.resolve(), args.report.resolve())
    print(f"Exported {report['condition_scheduled']} scheduled slots and scientific source data.")


if __name__ == "__main__":
    main()
