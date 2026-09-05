#!/usr/bin/env python
"""Display sealed M3 information effects; no fitting or inference during rendering."""

from __future__ import annotations

import json

import numpy as np
import render_prior_discovery_figures as style

plt = style.plt
TASKS = ("electrochemical-conversion", "reaction-to-crystallization")
TASK_NAMES = ("Electrochemistry", "Crystallization")
TASK_COLORS = (style.COLORS["blue"], style.COLORS["violet"])
CONDITIONS = ("none", "raw", "L", "F")
LABELS = ("None", "Raw evidence", "Model law", "Fitted law")
CONTRAST_LABELS = (
    "L $-$ none (primary)",
    "Raw $-$ none",
    "F $-$ none",
    "L $-$ raw",
    "F $-$ raw",
    "F $-$ L",
)


def load_report() -> tuple[dict, object]:
    current = json.loads((style.ROOT / "configs/current.json").read_text(encoding="utf-8"))
    binding = current["work_ii"]["w2_69_m3_portability"]
    path = style.ROOT / binding["report"]
    if style.sha256_file(path) != binding["report_sha256"]:
        raise ValueError("M3 report differs from its current binding")
    report = json.loads(path.read_text(encoding="utf-8"))
    if not report["execution_valid"] or not report["statistics"]:
        raise ValueError("M3 figure requires a completed execution-valid report")
    return report, path


def render(report: dict) -> list:
    style.configure_matplotlib()
    fig, (loss, effect) = plt.subplots(
        1, 2, figsize=(7.4, 4.15), gridspec_kw={"width_ratios": [1.0, 1.15]}
    )
    fig.subplots_adjust(left=0.15, right=0.98, top=0.83, bottom=0.23, wspace=0.96)
    world_means = []
    maximum = 0.0
    for task_index, (task, name, color) in enumerate(
        zip(TASKS, TASK_NAMES, TASK_COLORS, strict=True)
    ):
        worlds = sorted({row["cluster_id"] for row in report["slots"] if row["task"] == task})
        start = task_index * 5.4
        loss.text(
            0,
            start - 0.95,
            name,
            transform=loss.get_yaxis_transform(),
            color=color,
            fontsize=9.5,
            ha="left",
        )
        for arm_index, arm in enumerate(CONDITIONS):
            values = []
            for world_index, world in enumerate(worlds):
                cohort = [
                    row
                    for row in report["slots"]
                    if row["cluster_id"] == world and row["condition"] == arm
                ]
                value = float(np.mean([row["failure_aware_regret"] for row in cohort]))
                complete = sum(row["status"] == "completed" for row in cohort)
                values.append(value)
                maximum = max(maximum, value)
                loss.scatter(
                    value,
                    start + arm_index + (world_index - 2) * 0.095,
                    color=color,
                    alpha=0.60,
                    s=18,
                    linewidths=0.8,
                    marker="o" if complete == len(cohort) else "x",
                    zorder=2,
                )
                world_means.append(
                    {
                        "task": task,
                        "cluster_id": world,
                        "condition": arm,
                        "mean_failure_aware_regret": value,
                        "completed": complete,
                        "scheduled": len(cohort),
                    }
                )
            loss.scatter(
                float(np.mean(values)),
                start + arm_index,
                marker="D",
                s=33,
                facecolors=color,
                edgecolors="white",
                linewidths=0.7,
                zorder=4,
            )
        loss.axhspan(start - 0.45, start + 3.45, facecolor=color, alpha=0.035, zorder=0)
    loss.set_yticks([*range(4), *[5.4 + i for i in range(4)]], LABELS * 2)
    loss.set_ylim(9.0, -1.5)
    loss.set_xlim(-max(0.002, maximum * 0.05), max(0.025, maximum * 1.10))
    loss.set_xlabel("Regret (fixed utility scale)", labelpad=8)
    loss.tick_params(axis="y", length=0, labelsize=9.0)
    loss.spines["left"].set_visible(False)
    loss.grid(axis="x", color=style.COLORS["grid"], lw=0.5)
    nearest = [
        row["failure_aware_regret"]
        for row in report["deterministic_controls"]
        if row["condition"] == "nearest"
    ]
    nearest_mean = float(np.mean(nearest)) if nearest else None
    if nearest_mean is not None:
        for start in (0.0, 5.4):
            loss.vlines(
                nearest_mean,
                start - 0.45,
                start + 3.45,
                color=style.COLORS["muted"],
                lw=0.8,
                ls=(0, (2, 2)),
            )
    loss.set_title("a   Decision loss by information", loc="left", y=1.13, fontsize=10.2)

    statistics = report["statistics"]
    for index, row in enumerate(statistics["contrasts"]):
        for task, color, offset in zip(TASKS, TASK_COLORS, (-0.10, 0.10), strict=True):
            values = [
                world["mean_difference"]
                for world in statistics["world_contrasts"]
                if world["task"] == task and world["contrast"] == row["contrast"]
            ]
            effect.scatter(
                values,
                index + offset + np.linspace(-0.055, 0.055, len(values)),
                color=color,
                s=13,
                alpha=0.6,
                linewidths=0,
                zorder=2,
            )
        low, high = row["interval"]
        effect.plot([low, high], [index, index], lw=1.6, color=style.COLORS["ink"], zorder=3)
        effect.scatter(
            row["mean_difference"],
            index,
            marker="D",
            s=30,
            color=style.COLORS["ink"],
            edgecolors="white",
            linewidths=0.5,
            zorder=4,
        )
    effect.axvline(0, color=style.COLORS["muted"], lw=0.8, zorder=1)
    effect.vlines(-0.01, -0.4, 0.4, ls=(0, (2, 2)), color=style.COLORS["muted"], lw=0.9)
    effect.set_yticks(range(6), CONTRAST_LABELS)
    effect.set_ylim(5.55, -0.65)
    effect.tick_params(axis="y", length=0, labelsize=9.2, pad=7)
    effect.spines["left"].set_visible(False)
    effect.grid(axis="x", color=style.COLORS["grid"], lw=0.5)
    effect.set_xlabel("Regret difference", labelpad=8)
    effect.set_title("b   Paired information effects", loc="left", y=1.13, fontsize=10.2)
    fig.text(
        0.03,
        0.07,
        "Dots: individual worlds   Diamonds: means   L: model law   F: fitted law",
        fontsize=8.4,
        color=style.COLORS["ink"],
    )
    fig.text(
        0.03,
        0.02,
        f"10 reused worlds · {report['condition_completed']}/160 selections · " + (
            f"nearest evidence: mean regret {nearest_mean:.3f}"
            if nearest_mean is not None
            else "95% primary / 99% secondary intervals"
        ),
        fontsize=8.6,
        color=style.COLORS["muted"],
    )
    for stem, rows in (
        ("world-means", world_means),
        ("world-contrasts", statistics["world_contrasts"]),
        ("condition-means", statistics["condition_summaries"]),
        ("slots", report["slots"]),
        ("controls", report["deterministic_controls"]),
        ("resources", report["provider_resources"]),
    ):
        if rows:
            fields = list(dict.fromkeys(key for row in rows for key in row))
            style.write_csv(style.SOURCE_DIR / f"figure-8-m3-{stem}.csv", rows, fields)
    return style.export_figure(fig, "figure-8-m3-portability")


if __name__ == "__main__":
    report, _ = load_report()
    render(report)
