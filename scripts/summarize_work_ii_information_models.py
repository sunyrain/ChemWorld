"""Combine the two fixed disclosure contrasts while retaining world clustering."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean

import numpy as np
from scripts.run_work_ii_final_diagnostic import digest, read, write

ROOT = Path(__file__).resolve().parents[1]
MODELS = ("deepseek", "gpt")
INFORMATION = ("original", "complete")


def combine(reports: dict[str, dict]) -> dict:
    rows = []
    coverage = None
    for model in MODELS:
        report = reports[model]
        if not report["formal_result"] or report["status"] != "terminal":
            raise ValueError("both formal model blocks must reach a terminal result")
        if report["scheduled"] != 60 or report["worlds"] != 10:
            raise ValueError("expected the fixed ten-world, sixty-session block per model")
        current = {(r["cluster_id"], r["arm"], r["information"]) for r in report["rows"]}
        if (
            len(report["rows"]) != 60
            or len(current) != 60
            or (coverage is not None and current != coverage)
        ):
            raise ValueError("model blocks have different or duplicate coverage")
        if any(r["model"] != model for r in report["rows"]):
            raise ValueError("model label mismatch")
        if (
            report["primary"]["bootstrap_seed"] != 90870
            or report["primary"]["bootstrap_draws"] != 20000
        ):
            raise ValueError("bootstrap protocol mismatch")
        coverage = current
        rows.extend(report["rows"])
    groups = []
    for model in MODELS:
        for info in INFORMATION:
            for analysis in ("recovery", "retention"):
                selected = [
                    r
                    for r in rows
                    if r["model"] == model
                    and r["information"] == info
                    and (r["arm"] == "aligned_nominal") == (analysis == "retention")
                ]
                group = {
                    "model": model,
                    "information": info,
                    "analysis": analysis,
                    "scheduled": len(selected),
                    "counts": dict(Counter(r["status"] for r in selected)),
                    "joint_recovery": sum(r["joint_recovery"] for r in selected),
                    "mean_normalized_regret_failure_aware": mean(
                        r["normalized_regret"] for r in selected
                    ),
                    "top1": sum(r["top1"] for r in selected),
                    "tool_use_sessions": sum(r["tool_used"] for r in selected),
                }
                for metric in ("pre_mae", "post_mae", "post_exponent_abs_error"):
                    available = [r[metric] for r in selected if metric in r]
                    group[metric + "_available_n"] = len(available)
                    group[metric + "_mean"] = mean(available) if available else None
                groups.append(group)
    worlds = list(dict.fromkeys(r["cluster_id"] for r in rows))
    contrasts = []
    for world in worlds:
        row = {"world": world}
        for model in MODELS:
            selected = [
                r
                for r in rows
                if r["cluster_id"] == world
                and r["model"] == model
                and r["arm"] != "aligned_nominal"
            ]
            row[model] = mean(
                r["joint_recovery"] for r in selected if r["information"] == "complete"
            ) - mean(r["joint_recovery"] for r in selected if r["information"] == "original")
        row["model_mean"] = mean(row[m] for m in MODELS)
        contrasts.append(row)
    values = np.array([r["model_mean"] for r in contrasts])
    interval = np.quantile(
        np.random.default_rng(90870).choice(values, (20000, 10)).mean(axis=1), [0.025, 0.975]
    ).tolist()
    return {
        "schema_version": "work-ii-information-two-configurations-1",
        "formal_result": True,
        "status": "terminal",
        "scheduled": 120,
        "worlds": 10,
        "models": list(MODELS),
        "providers": {m: reports[m]["provider"] for m in MODELS},
        "budgets": {m: reports[m]["budgets"] for m in MODELS},
        "counts": dict(Counter(r["status"] for r in rows)),
        "groups": groups,
        "primary": {
            "contrast": "complete_minus_original_joint_recovery_unknown_and_wrong_priors",
            "mean": float(values.mean()),
            "approximate_world_bootstrap_95": interval,
            "bootstrap_seed": 90870,
            "bootstrap_draws": 20000,
            "aggregation": "equal priors within model/world; "
            "equal configurations within world; equal worlds",
        },
        "model_primary": {m: reports[m]["primary"] for m in MODELS},
        "world_contrasts": contrasts,
        "rows": rows,
        "failures": [r for r in rows if r["status"] != "completed"],
        "resources_by_model": {m: reports[m]["resources"] for m in MODELS},
        "interpretation": "Within-configuration disclosure effects under matched stimuli "
        "and task budgets. DeepSeek Flash/low and GPT/medium are distinct configurations, "
        "not equal-compute competitors. The two models share ten worlds, "
        "not twenty independent worlds. Retention is separate from recovery. "
        "Disclosure length and paired observation noise are part of the setting. "
        "Historical Flash/high and historical B3 runtime results are not pooled here.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, required=True)
    args = parser.parse_args()
    if args.export.exists() or args.export.with_suffix(".md").exists():
        raise FileExistsError("preserve an existing exported analysis")
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_87_information_completeness"]
    reports, sources = {}, {}
    for model in MODELS:
        key = model + "_formal_report"
        path = ROOT / binding[key]
        if digest(path) != binding[key + "_sha256"]:
            raise ValueError("source report differs from current binding")
        reports[model] = read(path)
        sources[model] = {"report": binding[key], "sha256": binding[key + "_sha256"]}
    report = combine(reports)
    report["sources"] = sources
    write(args.export, report)
    lines = [
        "# W2-87: information completeness in two configurations",
        "",
        report["interpretation"],
        "",
        "| Configuration | Information | Analysis | Joint recovery / scheduled | "
        "Prediction MAE (available n) | Regret |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for group in report["groups"]:
        provider = report["providers"][group["model"]]
        mae = group["post_mae_mean"]
        text = "unavailable" if mae is None else f"{mae:.6f}"
        lines.append(
            f"| {provider['model']} / {provider['reasoning_effort']} | "
            f"{group['information']} | {group['analysis']} | "
            f"{group['joint_recovery']}/{group['scheduled']} | "
            f"{text} ({group['post_mae_available_n']}) | "
            f"{group['mean_normalized_regret_failure_aware']:.6f} |"
        )
    lines.extend(
        [
            "",
            "Primary (80 recovery sessions; ten world clusters):",
            "```json",
            json.dumps(report["primary"], indent=2),
            "```",
            "",
            "Resources by configuration (CLI-reported usage; unavailable usage is a lower bound):",
            "```json",
            json.dumps(report["resources_by_model"], indent=2),
            "```",
            "",
            "All failed sessions:",
        ]
    )
    lines.extend(
        f"- {r['cell_id']}: {r['status']} / {r.get('failure')}" for r in report["failures"]
    )
    if not report["failures"]:
        lines.append("- None; all 120 scheduled sessions completed.")
    args.export.with_suffix(".md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"Combined terminal analysis: {report['counts']}; ten paired worlds.")


if __name__ == "__main__":
    main()
