"""Plot all individual sessions, with world and information-arm distinctions."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scripts.run_paper_case_notebooks import read

COLORS = {"Opaque": "#287B8E", "Aligned": "#BE6948", "MisIndexed": "#7964A2"}
PANELS = {
    "EQ": [
        ("Lowest-concentration queries", "Macro MAE", "lowest_three_macro_mae"),
        ("Remaining nine queries", "Macro MAE", "remaining_nine_macro_mae"),
        (
            "Autonomous concentration coverage",
            "Minimum positive loading (M)",
            "minimum_positive_concentration_M",
        ),
        (
            "Intervals: lowest-concentration queries",
            "Empirical 80% coverage",
            "lowest_three_coverage80",
        ),
    ],
    "C": [
        ("Recovery predictions", "MAE", "crystal_yield_mae"),
        ("Purity predictions", "MAE", "crystal_purity_mae"),
        ("Fines predictions", "MAE", "crystal_fines_fraction_mae"),
        (
            "Recommended process",
            "Retest recovery (noise-free)",
            "recommendation_true_crystal_yield",
        ),
    ],
}


def plot(path, output):
    data = read(path)
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    for system, panels in PANELS.items():
        worlds = sorted({r["world"] for r in data["cases"] if r["system"] == system})
        arms = [
            a for a in COLORS if any(r["system"] == system and r["arm"] == a for r in data["cases"])
        ]
        offsets = dict(
            zip(arms, {1: (0,), 2: (-0.15, 0.15), 3: (-0.23, 0, 0.23)}[len(arms)], strict=True)
        )
        fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
        for ax, (title, ylabel, metric) in zip(axes.flat, panels, strict=True):
            for arm in arms:
                color = COLORS[arm]
                for row in data["cases"]:
                    if (row["system"], row["arm"]) != (system, arm):
                        continue
                    value = row["measurements"].get(metric)
                    if value is None:
                        continue
                    repeat = int(row["repeat"].split("-")[1]) - 1
                    x = worlds.index(row["world"]) + offsets[arm]
                    x += (repeat - 1) * 0.045
                    ax.scatter(
                        x, value, s=43, color=color, marker=("o", "s", "^")[repeat], alpha=0.9
                    )
                ax.scatter([], [], color=color, label=arm)
            ax.set(
                title=title,
                ylabel=ylabel,
                xticks=range(len(worlds)),
                xticklabels=worlds,
                xlim=(-0.6, len(worlds) - 0.4),
            )
            ax.grid(axis="y", color="#dddddd", linewidth=0.5)
            if metric == "minimum_positive_concentration_M":
                ax.set_yscale("log")
                ax.axhline(0.001, color="#777777", linestyle="--", linewidth=1)
            elif metric == "lowest_three_coverage80":
                ax.set_ylim(-0.05, 1.05)
                ax.axhline(0.8, color="#777777", linestyle=":", linewidth=1)
            elif metric == "recommendation_true_crystal_yield":
                ax.axhline(0.1, color="#777777", linestyle=":", linewidth=1)
            ax.legend(frameon=False, fontsize=9)
        status = "INTERIM — " if data["provisional"] else ""
        fig.suptitle(
            f"{status}{system}: three independent sessions per world and information arm",
            fontsize=13,
        )
        for suffix in ("png", "pdf"):
            fig.savefig(output / f"{system.lower()}-individual-outcomes.{suffix}", dpi=180)
        plt.close(fig)
    pairs_path = path.parent / "quench_pairs.json"
    if pairs_path.exists():
        plot_quench(read(pairs_path), output)


def plot_quench(pairs, output):
    complete = [p for p in pairs if p["absent"]["truth"] and p["present"]["truth"]]
    palette = ("#287B8E", "#BE6948", "#7964A2", "#71863C", "#AF5677")
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), layout="constrained")
    for ax, (metric, label, threshold) in zip(
        axes,
        (
            ("crystal_fines_fraction", "Fines fraction", 0.5),
            ("crystal_yield", "Seed-excluded recovery", 0.1),
        ),
        strict=True,
    ):
        for world, color in zip((f"W{i:02d}" for i in range(1, 6)), palette, strict=True):
            for original_world in (False, True):
                rows = [
                    p
                    for p in complete
                    if p["world"] == world
                    and (p["world"] == p["recipe_source_world"]) == original_world
                ]
                ax.scatter(
                    [p["absent"]["truth"][metric] for p in rows],
                    [p["present"]["truth"][metric] for p in rows],
                    s=45,
                    edgecolors=color,
                    facecolors=color if original_world else "none",
                    alpha=0.8,
                    label=world if original_world else None,
                )
        ax.plot([0, 1], [0, 1], color="#888888", linewidth=1, linestyle="--")
        ax.axhline(threshold, color="#cccccc", linewidth=0.8, linestyle=":")
        ax.axvline(threshold, color="#cccccc", linewidth=0.8, linestyle=":")
        ax.set(
            title=label,
            xlabel="Without quench",
            ylabel="With quench",
            xlim=(-0.025, 1.025),
            ylim=(-0.025, 1.025),
            aspect="equal",
        )
    axes[0].legend(frameon=False, fontsize=8, loc="lower right")
    fig.suptitle(
        f"Matched operation effects: {len(complete)}/{len(pairs)} pairs with both endpoints\n"
        "Filled: recipe's original world; open: other worlds. "
        "Missing endpoints excluded, not zero.",
        fontsize=11,
    )
    for suffix in ("png", "pdf"):
        fig.savefig(output / f"quench-paired-outcomes.{suffix}", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    plot(args.analysis, args.output)
