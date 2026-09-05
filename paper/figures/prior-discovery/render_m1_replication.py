#!/usr/bin/env python
"""Render the completed independent-world factorial report without new inference."""

from __future__ import annotations

import json

import numpy as np
import render_prior_discovery_figures as style

plt = style.plt
TASKS = ("electrochemical-conversion", "reaction-to-crystallization")
TASK_NAMES = ("Electrochemistry", "Crystallization")
TASK_COLORS = (style.COLORS["blue"], style.COLORS["violet"])
CONTRAST_NAMES = (
    "F-X $-$ L-X  (primary)",
    "L-X $-$ L-A",
    "F-A $-$ L-A",
    "F-X $-$ F-A",
    "Interaction",
)


def load_report() -> tuple[dict, object]:
    current = json.loads((style.ROOT / "configs/current.json").read_text(encoding="utf-8"))
    binding = current["work_ii"]["w2_72_m1_replication"]
    path = style.ROOT / binding["report"]
    if style.sha256_file(path) != binding["report_sha256"]:
        raise ValueError("M1 bound report differs from current artifact")
    report = json.loads(path.read_text(encoding="utf-8"))
    if not report["execution_valid"] or not report["statistics"]:
        raise ValueError("M1 figure requires an execution-valid completed report")
    return report, path


def render(report: dict) -> list:
    style.configure_matplotlib()
    fig, (paired, contrast) = plt.subplots(
        1, 2, figsize=(7.4, 4.2), gridspec_kw={"width_ratios": [1.1, 1.0]}
    )
    fig.subplots_adjust(left=0.08, right=0.975, top=0.82, bottom=0.24, wspace=0.78)
    slots = report["slots"]
    maximum = 0.0
    for task_index, (task, name, color) in enumerate(
        zip(TASKS, TASK_NAMES, TASK_COLORS, strict=True)
    ):
        worlds = sorted({row["cluster_id"] for row in slots if row["task"] == task})
        for world_index, world in enumerate(worlds):
            position = task_index * 6.5 + world_index
            cohorts = [
                [
                    row
                    for row in slots
                    if row["cluster_id"] == world and row["condition"] == condition
                ]
                for condition in ("L-X", "F-X")
            ]
            values = [
                float(np.mean([row["failure_aware_regret"] for row in cohort]))
                for cohort in cohorts
            ]
            maximum = max(maximum, *values)
            paired.plot(values, [position] * 2, color=color, lw=1.3, alpha=0.7, zorder=2)
            for index, (value, cohort) in enumerate(zip(values, cohorts, strict=True)):
                missing = any(row["status"] != "completed" for row in cohort)
                paired.scatter(
                    [value],
                    [position],
                    facecolors=color if index or missing else "white",
                    edgecolors=color,
                    s=16 if index else 40,
                    marker="x" if missing else "o",
                    linewidths=1.0,
                    zorder=3 + index,
                )
        paired.text(
            0.0,
            task_index * 6.5 - 0.95,
            name,
            transform=paired.get_yaxis_transform(),
            ha="left",
            color=color,
            fontsize=9.4,
        )
    paired.set_yticks([*range(5), *[6.5 + i for i in range(5)]], list(range(1, 6)) * 2)
    paired.tick_params(axis="y", length=0, pad=6)
    paired.set_xlim(-max(0.001, maximum * 0.05), max(0.02, maximum * 1.17))
    paired.set_ylim(11.2, -1.5)
    paired.set_ylabel("World", labelpad=5)
    paired.set_xlabel("Regret (fixed utility scale)", labelpad=8)
    paired.grid(axis="x", color=style.COLORS["grid"], lw=0.6, zorder=0)
    paired.spines["left"].set_visible(False)
    paired.set_title("a   Same maximizer, different laws", loc="left", y=1.13, fontsize=10.5)

    statistics = report["statistics"]
    for index, row in enumerate(statistics["contrasts"]):
        for task, color, offset in zip(TASKS, TASK_COLORS, (-0.10, 0.10), strict=True):
            values = [
                world["mean_difference"]
                for world in statistics["world_contrasts"]
                if world["task"] == task and world["contrast"] == row["contrast"]
            ]
            contrast.scatter(
                values,
                index + offset + np.linspace(-0.05, 0.05, len(values)),
                color=color,
                s=12,
                alpha=0.55,
                linewidths=0,
                zorder=2,
            )
        estimate, (low, high) = row["mean_difference"], row["interval"]
        contrast.plot([low, high], [index, index], color=style.COLORS["ink"], lw=1.6, zorder=3)
        contrast.scatter(
            [estimate],
            [index],
            marker="D",
            s=29,
            color=style.COLORS["ink"],
            edgecolors="white",
            linewidths=0.5,
            zorder=4,
        )
    contrast.axvline(0, color=style.COLORS["muted"], lw=0.8, zorder=1)
    contrast.vlines(
        -0.01, -0.42, 0.42, color=style.COLORS["muted"], lw=0.9, ls=(0, (2, 2)), zorder=1
    )
    contrast.set_yticks(range(5), CONTRAST_NAMES)
    contrast.set_ylim(4.6, -0.6)
    contrast.tick_params(axis="y", length=0, pad=7, labelsize=9.5)
    contrast.spines["left"].set_visible(False)
    contrast.grid(axis="x", color=style.COLORS["grid"], lw=0.5, zorder=0)
    contrast.set_xlabel("Regret difference", labelpad=8)
    contrast.set_title("b   Paired factorial effects", loc="left", y=1.13, fontsize=10.5)
    fig.text(
        0.08,
        0.065,
        "L: model law (hollow)   F: public fit (filled)   A: fresh agent   X: maximizer",
        fontsize=8.5,
        color=style.COLORS["ink"],
    )
    fig.text(
        0.08,
        0.012,
        r"10 worlds · 2 models $\times$ 2 repeats/world · "
        f"{report['condition_completed']}/160 available selections",
        fontsize=9.2,
        color=style.COLORS["muted"],
    )
    for stem, rows in (
        ("world-contrasts", statistics["world_contrasts"]),
        ("condition-means", statistics["condition_summaries"]),
        ("slots", slots),
        ("baselines", report["baselines"]),
    ):
        style.write_csv(style.SOURCE_DIR / f"figure-7-m1-{stem}.csv", rows, list(rows[0]))
    return style.export_figure(fig, "figure-7-m1-replication")


if __name__ == "__main__":
    report, _ = load_report()
    render(report)
