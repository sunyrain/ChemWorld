"""Plot individual repetitions from the retained descriptive stability summary."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scripts.run_paper_case_notebooks import read


def plot(summary_path: Path, output: Path):
    summary = read(summary_path)
    stats = summary["case_statistics"]
    panels = [
        (
            "EC: recommended process",
            "Retest score",
            "recommendation_score",
            ("EC-discovery", "EC-optimization"),
        ),
        (
            "EC: withheld prediction",
            "Score MAE (lower is better)",
            "score_mae",
            ("EC-discovery", "EC-optimization"),
        ),
        (
            "EQ: lowest-concentration queries",
            "Macro MAE (lower is better)",
            "lowest_three_macro_mae",
            ("EQ-Sol", "EQ-Astra"),
        ),
        (
            "EQ: autonomous sampling",
            "Minimum positive loading (M)",
            "minimum_positive_concentration_M",
            ("EQ-Sol", "EQ-Astra"),
        ),
        (
            "C: withheld quality decisions",
            "Correct classifications / 12",
            "quality_correct_of_12",
            ("C-12", "C-24"),
        ),
        (
            "C: thermal-intervention prediction",
            "Predicted change in fines fraction",
            "thermal_fines_predicted_delta",
            ("C-12", "C-24"),
        ),
    ]
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(3, 2, figsize=(12, 11), constrained_layout=True)
    colors = ("#277F8A", "#BC7850")
    for ax, (title, ylabel, metric, cases) in zip(axes.flat, panels, strict=True):
        for i, case in enumerate(cases):
            record = stats[case]["measurements"].get(metric, {})
            values = [record.get("previous_separate"), *record.get("new_repeats", [None] * 3)]
            offset = (i - 0.5) * 0.16
            for x, value in enumerate(values):
                if value is not None:
                    ax.scatter(
                        x + offset,
                        value,
                        s=65,
                        marker="D" if x == 0 else "o",
                        facecolors="none" if x == 0 else colors[i],
                        edgecolors=colors[i],
                        linewidths=1.4,
                        zorder=3,
                    )
            ax.scatter([], [], s=55, color=colors[i], label=case)
        ax.set(
            title=title,
            ylabel=ylabel,
            xticks=range(4),
            xticklabels=["Previous", "Repeat 1", "Repeat 2", "Repeat 3"],
            xlim=(-0.5, 3.5),
        )
        ax.axvline(0.5, color="#CCCCCC", linestyle=":", linewidth=1)
        ax.grid(axis="y", color="#E7E7E7", linewidth=0.6)
        ax.legend(frameon=False, fontsize=9, loc="best")
        if metric == "minimum_positive_concentration_M":
            ax.set_yscale("log")
            ax.axhline(0.001, color="#777777", linestyle="--", linewidth=1)
        if metric == "quality_correct_of_12":
            ax.set_ylim(-0.5, 12.5)
        if metric == "thermal_fines_predicted_delta":
            reference = stats["C-12"]["measurements"].get("thermal_fines_true_delta", {})
            value = next((v for v in reference.get("new_repeats", []) if v is not None), None)
            if value is not None:
                ax.axhline(value, color="#555555", linestyle="--", linewidth=1)
                ax.text(
                    0.02,
                    value,
                    "Reference change",
                    transform=ax.get_yaxis_transform(),
                    va="bottom",
                    fontsize=8,
                )
    completed = summary["counts"]["completed_sources"]
    terminal = summary["counts"]["terminal_sources"]
    fig.suptitle(
        f"Same case, three fresh Agent sessions\n"
        f"{terminal}/18 terminal sessions; {completed}/18 complete chains",
        fontsize=16,
        fontweight="bold",
    )
    fig.supxlabel(
        "Individual outcomes; no significance claim. "
        "Previous runs are excluded from repeat statistics.\n"
        "EQ panels compare different fixed cases (world/model/prior), not a model ranking.",
        fontsize=9,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".png"), dpi=180)
    fig.savefig(output.with_suffix(".svg"))
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    plot(args.summary, args.output)
