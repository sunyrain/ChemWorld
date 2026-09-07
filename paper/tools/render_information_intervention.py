"""Render one terminal disclosure configuration as a standalone research figure."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, PercentFormatter

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "paper/figures/prior-discovery"
COLORS = ("#8595A6", "#0072B2")
INFO = ("original", "complete")
LABELS = ("Original formula", "Complete mapping")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=("gpt", "deepseek"), default="gpt")
    model = parser.parse_args().model
    stem = "figure-10-information-gpt" if model == "gpt" else "figure-11-information-deepseek"
    binding = json.loads((ROOT / "configs/current.json").read_text(encoding="utf-8"))["work_ii"][
        "w2_87_information_completeness"
    ]
    path = ROOT / binding[model + "_formal_report"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != binding[model + "_formal_report_sha256"]:
        raise ValueError("terminal report differs from current binding")
    report = json.loads(path.read_text(encoding="utf-8"))
    if report["status"] != "terminal" or not report["formal_result"] or report["scheduled"] != 60:
        raise ValueError("figure requires the complete fixed formal denominator")
    rows = report["rows"]
    worlds = list(dict.fromkeys(r["cluster_id"] for r in rows))
    primary = [r for r in rows if r["arm"] != "aligned_nominal"]
    paired = []
    for world in worlds:
        row = {"world": world}
        for info in INFO:
            selected = [r for r in primary if r["cluster_id"] == world and r["information"] == info]
            row[info + "_recovery"] = mean(r["joint_recovery"] for r in selected)
            row[info + "_regret"] = mean(r["normalized_regret"] for r in selected)
            available = [r["post_mae"] for r in selected if "post_mae" in r]
            row[info + "_prediction_mae"] = mean(available) if available else None
            row[info + "_prediction_n"] = len(available)
        paired.append(row)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data_path = OUTPUT / "source_data" / f"{stem}-worlds.csv"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with data_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(paired[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(paired)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(9.2, 7.0))
    figure.subplots_adjust(left=0.095, right=0.97, top=0.86, bottom=0.16, wspace=0.32, hspace=0.48)
    figure.suptitle(
        "Observation mapping and structure recovery", x=0.095, y=0.97, ha="left", fontsize=16
    )
    figure.text(
        0.095,
        0.925,
        f"{report['provider']['model']} / {report['provider']['reasoning_effort']}"
        "  |  10 worlds  |  matched observations, priors and tools",
        color="#526170",
        fontsize=10,
    )
    ax = axes[0, 0]
    for j, info in enumerate(INFO):
        for i, analysis in enumerate(("recovery", "retention")):
            group = next(
                g
                for g in report["groups"]
                if g["information"] == info and g["analysis"] == analysis
            )
            rate = group["joint_recovery"] / group["scheduled"]
            x = i + (j - 0.5) * 0.32
            ax.bar(x, rate, width=0.27, color=COLORS[j], label=LABELS[j] if i == 0 else None)
            ax.text(
                x,
                rate + 0.035,
                f"{group['joint_recovery']}/{group['scheduled']}",
                ha="center",
                fontsize=8,
            )
    ax.set(
        xticks=[0, 1],
        xticklabels=["Unknown / wrong prior", "Correct prior"],
        ylim=(0, 1.18),
        yticks=[0, 0.5, 1],
        ylabel="Joint recovery / retention",
    )
    ax.set_title("A  Recovery and retention", loc="left", pad=12)
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0, -0.17), ncol=2)
    ax = axes[0, 1]
    deltas = [r["complete_recovery"] - r["original_recovery"] for r in paired]
    ax.axhline(0, color="#8595A6", lw=0.8)
    ax.vlines(np.arange(1, 11), 0, deltas, color=COLORS[1], lw=2)
    ax.scatter(np.arange(1, 11), deltas, s=32, color=COLORS[1], zorder=3)
    ax.set(
        xlim=(0.4, 10.6),
        ylim=(-1.08, 1.08),
        xticks=[1, 3, 5, 7, 10],
        xlabel="World",
        ylabel="Recovery difference (percentage points)",
    )
    ax.set_title("B  Complete − original by world", loc="left", pad=12)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{100 * value:.0f}"))

    def plot_pair(ax, metric: str, title: str, ylabel: str) -> None:
        valid = [r for r in paired if all(r[i + "_" + metric] is not None for i in INFO)]
        for index, row in enumerate(valid):
            jitter = (index - (len(valid) - 1) / 2) * 0.009
            values = [row[i + "_" + metric] for i in INFO]
            ax.plot([jitter, 1 + jitter], values, color="#CBD2D9", lw=0.9, zorder=1)
            ax.scatter([jitter, 1 + jitter], values, color=COLORS, s=25, zorder=2)
        if valid:
            for j, info in enumerate(INFO):
                value = mean(r[info + "_" + metric] for r in valid)
                ax.plot([j - 0.16, j + 0.16], [value, value], color="#192D40", lw=2.2, zorder=3)
        ax.set(xlim=(-0.3, 1.3), xticks=[0, 1], xticklabels=LABELS, ylabel=ylabel)
        ax.set_ylim(bottom=-0.008 if metric == "regret" else 0)
        ax.set_title(title, loc="left", pad=12)
        ax.grid(axis="y", color="#EDF0F3", lw=0.6)
        ax.set_axisbelow(True)

    plot_pair(axes[1, 0], "prediction_mae", "C  Held-out prediction", "Mean absolute error")
    plot_pair(axes[1, 1], "regret", "D  Unseen action choice", "Normalized regret")
    effect = report["primary"]["mean"]
    interval = report["primary"]["approximate_world_bootstrap_95"]
    failure_count = report["counts"].get("failed", 0)
    figure.text(
        0.095,
        0.07,
        f"Recovery effect: {100 * effect:+.0f} percentage points; approximate world-bootstrap "
        f"95% CI [{100 * interval[0]:+.0f}, {100 * interval[1]:+.0f}]. "
        f"Failed sessions: {failure_count}/60.",
        fontsize=9,
    )
    figure.text(
        0.095,
        0.035,
        "C–D: each pair averages unknown and wrong priors within one world; dark bars show means.\n"
        "Prediction uses available submissions; failures receive worst regret. "
        "Disclosure length is part of the intervention.",
        fontsize=8,
        color="#526170",
    )
    for suffix in ("pdf", "svg", "png"):
        output_path = OUTPUT / f"{stem}.{suffix}"
        figure.savefig(output_path, dpi=300)
        if suffix == "svg":
            output_path.write_text(
                "\n".join(
                    line.rstrip() for line in output_path.read_text(encoding="utf-8").splitlines()
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
    plt.close(figure)
    print(f"Terminal {model} figure exported as PDF, SVG and PNG; world source data exported.")


if __name__ == "__main__":
    main()
