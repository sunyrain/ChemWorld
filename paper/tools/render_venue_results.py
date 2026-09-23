"""Render the exploratory EQ/C comparison from retained results; no new experiments."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
    / "STORY_WORLD_ANALYSIS.json"
)
OUT = ROOT / "paper/figures/venue-results"
COLORS = {"Opaque": "#34648B", "Aligned": "#21806B", "MisIndexed": "#C66D39"}
GROUPS = ("other_nine", "three_most_dilute")


def autonomous_figures(data):
    """Keep original-session predictions and conceptual scope labels distinguishable."""
    process = json.loads((SOURCE.parent / "EQ_AUTONOMOUS_PROCESS.json").read_text(encoding="utf-8"))
    rows = process["rows"]
    assert len(rows) == 15 and process["coverage"]["operations"] == 945
    eq = data["eq_p_query_regimes"]["aggregate"]
    cells = data["eq_p_query_regimes"]["cells"]
    fig = plt.figure(figsize=(10.5, 6.1), layout="constrained")
    outer = fig.add_gridspec(2, 1, height_ratios=[1, 1.05])
    upper = outer[0].subgridspec(1, 2)
    for panel, (metric, scale, title, ylabel) in enumerate(
        (
            ("mae", 1, "a  Prediction error by regime", "Macro mean absolute error"),
            ("coverage", 100, "b  Interval coverage by regime", "Coverage (%)"),
        )
    ):
        ax = fig.add_subplot(upper[panel])
        for i, (arm, color) in enumerate(COLORS.items()):
            x = np.arange(2) + (i - 1) * 0.23
            values = [next(r for r in eq if r["arm"] == arm and r["group"] == g) for g in GROUPS]
            ax.bar(x, [r[metric] * scale for r in values], 0.21, color=color, alpha=0.8, label=arm)
            for j, group in enumerate(GROUPS):
                y = [r["groups"][group][metric] * scale for r in cells if r["arm"] == arm]
                ax.scatter(
                    x[j] + np.linspace(-0.06, 0.06, 5),
                    y,
                    s=15,
                    facecolor="white",
                    edgecolor=color,
                    linewidth=0.8,
                    zorder=3,
                )
        ax.set(title=title, ylabel=ylabel)
        ax.set_xticks([0, 1], ["Other nine queries", "Three most dilute queries"])
        ax.grid(axis="y", alpha=0.16)
        ax.set_axisbelow(True)
        if metric == "coverage":
            ax.axhline(80, color="#555555", ls="--", lw=1)
            ax.set_ylim(0, 108)
        else:
            ax.legend(frameon=False, fontsize=8, loc="upper left")
    lower = outer[1].subgridspec(1, 5)
    export = []
    for j, world in enumerate(sorted({r["world"] for r in rows})):
        ax = fig.add_subplot(lower[j])
        reference = None
        for i, (arm, color) in enumerate(COLORS.items()):
            row = next(r for r in rows if r["world"] == world and r["arm"] == arm)
            pred = row["q08"]["predictions"]["acid_dissociation_fraction"]
            target = row["q08"]["reference_means"]["acid_dissociation_fraction"]
            assert reference is None or abs(target - reference) < 1e-12
            reference = target
            lo, hi = row["source_dissociation_range"]
            ax.fill_between([i - 0.25, i + 0.25], lo, hi, color="#b1b7bd", alpha=0.8)
            ax.errorbar(
                i,
                pred["estimate"],
                yerr=[[pred["estimate"] - pred["lower80"]], [pred["upper80"] - pred["estimate"]]],
                fmt="o",
                color=color,
                capsize=3,
                markersize=5,
                lw=1.25,
            )
            export.append(
                {
                    "world": world,
                    "arm": arm,
                    "query": "Q08",
                    "source_min": lo,
                    "source_max": hi,
                    "reference_mean": target,
                    **pred,
                    "public_explanation": row["text_annotation"]["q_extrapolation_code"],
                }
            )
        ax.axhline(reference, color="#262b30", ls="--", lw=1)
        ax.set(ylim=(0, 1), xlim=(-0.5, 2.5), title=f"{chr(99 + j)}  World {j + 1}")
        ax.set_xticks([0, 1, 2], ["O", "A", "M"])
        ax.grid(axis="y", alpha=0.13)
        if j == 0:
            ax.set_ylabel("Most dilute query: dissociation")
        else:
            ax.set_yticklabels([])
    fig.legend(
        handles=[
            Line2D([], [], color="#262b30", ls="--", label="Reference mean"),
            Rectangle((0, 0), 1, 1, color="#b1b7bd", label="Observed source range"),
            Line2D([], [], color="#555555", marker="o", label="Prediction and 80% interval"),
        ],
        loc="outside lower center",
        ncol=3,
        frameon=False,
        fontsize=8,
    )
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"eq_autonomous.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)
    with (OUT / "eq_autonomous_predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(export[0]))
        writer.writeheader()
        writer.writerows(export)

    baseline_path = (
        SOURCE.parent.parent / "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json"
    )
    crystal = json.loads(baseline_path.read_text(encoding="utf-8"))["rows"]
    assert len(crystal) == 30
    fig = plt.figure(figsize=(10.8, 4.2), layout="constrained")
    grid = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.65])
    for i, (metric, label, expected) in enumerate(
        (("crystal_purity", "Purity", 0), ("crystal_yield", "Recovery", 26))
    ):
        ax = fig.add_subplot(grid[i])
        limit = (
            max(
                max(r["agent_mae"][metric], r["public_baselines"]["mae"]["public_mean"][metric])
                for r in crystal
            )
            * 1.1
        )
        ax.plot([0, limit], [0, limit], "--", color="#8a969e", lw=1)
        wins = 0
        for row in crystal:
            x = row["public_baselines"]["mae"]["public_mean"][metric]
            y = row["agent_mae"][metric]
            wins += y < x
            marker = ("o" if row["budget"] == 12 else "^") if row["conforming"] else "x"
            ax.scatter(x, y, color=COLORS[row["arm"]], marker=marker, s=31, alpha=0.85)
        assert wins == expected
        ax.set(
            xlim=(0, limit),
            ylim=(0, limit),
            aspect="equal",
            xlabel="Public-mean MAE",
            ylabel="Agent MAE",
            title=f"{chr(97 + i)}  {label}\nAgent improves: {wins}/30",
        )
        ax.tick_params(labelsize=8)
    ax = fig.add_subplot(grid[2])
    ax.set(xlim=(-0.8, 2.03), ylim=(-0.25, 2.62))
    ax.axis("off")
    ax.text(-0.75, 2.56, "c  Applicability of an observed relationship", fontsize=10, weight="bold")
    for x, label in ((0.5, "Forecast preserves"), (1.5, "Forecast changes")):
        ax.text(x, 2.13, label, ha="center", fontsize=8.5)
    for y, label in (
        (1.5, "Reference\nremains near\nsource response"),
        (0.5, "Reference\nleaves source\nresponse"),
    ):
        ax.text(-0.08, y, label, ha="right", va="center", fontsize=8)
    for x, y, text, color in (
        (0, 1, "Appropriate\npreservation", "#eef4f2"),
        (1, 1, "Unnecessary change\n\nC purity", "#f9ede4"),
        (0, 0, "Unwarranted extension\n\nAligned EQ dilution", "#f9ede4"),
        (1, 0, "Appropriate\ndeparture", "#eef4f2"),
    ):
        ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor="white", lw=2))
        ax.text(x + 0.5, y + 0.5, text, ha="center", va="center", fontsize=8.3)
    ax.text(
        1, -0.14, "Conceptual map; no quadrant frequencies estimated", ha="center", fontsize=7.3
    )
    handles = [
        Line2D([], [], color=color, marker="o", ls="", label=arm) for arm, color in COLORS.items()
    ]
    handles += [
        Line2D([], [], color="#555555", marker=marker, ls="", label=label)
        for marker, label in (("o", "12 batches"), ("^", "24 batches"), ("x", "Source shortfall"))
    ]
    fig.legend(handles=handles, loc="outside lower center", ncol=6, frameon=False, fontsize=8)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"preserve_revise.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("Rendered original EQ predictions (15/15) and C scope comparison (30/30).", flush=True)


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    eq = data["eq_p_query_regimes"]["aggregate"]
    cells = data["eq_p_query_regimes"]["cells"]
    paired = [r for r in data["c_paired_response_tradeoffs"] if r["budget"] == 12]
    assert len(eq) == 6 and len(cells) == 15 and len(paired) == 10
    assert all(r["recovery_delta"] < 0 < r["purity_delta"] for r in paired)
    for world in {r["world"] for r in cells}:
        group = {r["arm"]: r for r in cells if r["world"] == world}
        assert (
            group["Aligned"]["groups"][GROUPS[0]]["mae"]
            < group["Opaque"]["groups"][GROUPS[0]]["mae"]
        )
        assert (
            group["Aligned"]["groups"][GROUPS[1]]["mae"]
            > group["Opaque"]["groups"][GROUPS[1]]["mae"]
        )
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.45), layout="constrained")
    for ax, metric, scale in ((axes[0], "mae", 1), (axes[1], "coverage", 100)):
        for i, (arm, color) in enumerate(COLORS.items()):
            x = np.arange(2) + (i - 1) * 0.23
            rows = [next(r for r in eq if r["arm"] == arm and r["group"] == g) for g in GROUPS]
            ax.bar(
                x, [r[metric] * scale for r in rows], width=0.21, color=color, alpha=0.82, label=arm
            )
            for j, g in enumerate(GROUPS):
                vals = [r["groups"][g][metric] * scale for r in cells if r["arm"] == arm]
                ax.scatter(
                    x[j] + np.linspace(-0.06, 0.06, 5),
                    vals,
                    s=13,
                    facecolor="white",
                    edgecolor=color,
                    linewidth=0.8,
                    zorder=3,
                )
        ax.set_xticks([0, 1], ["Other nine\nqueries", "Three most\ndilute queries"])
        ax.grid(axis="y", alpha=0.16)
        ax.set_axisbelow(True)
    axes[0].set(title="a  EQ: prediction error", ylabel="Macro mean absolute error")
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    axes[1].axhline(80, color="#505050", ls="--", lw=1)
    axes[1].set(title="b  EQ: interval coverage", ylabel="Coverage (%)", ylim=(-2, 105))
    ax = axes[2]
    ax.axhline(0, color="#888888", lw=0.8)
    ax.axvline(0, color="#888888", lw=0.8)
    for arm in ("Aligned", "MisIndexed"):
        rows = [r for r in paired if r["arm"] == arm]
        ax.scatter(
            [r["recovery_delta"] for r in rows],
            [r["purity_delta"] for r in rows],
            color=COLORS[arm],
            marker="o" if arm == "Aligned" else "^",
            s=34,
            label=arm,
        )
        for r in rows:
            if not r["both_conforming"]:
                ax.scatter(r["recovery_delta"], r["purity_delta"], marker="x", color="black", s=60)
    lower_x = min(r["recovery_delta"] for r in paired) - 0.025
    upper_y = max(r["purity_delta"] for r in paired) + 0.015
    ax.set(
        title="c  C: response tradeoff, 12 batches",
        xlabel="Recovery MAE change vs Opaque",
        ylabel="Purity MAE change vs Opaque",
        xlim=(lower_x, 0.01),
        ylim=(-0.005, upper_y),
    )
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.grid(alpha=0.16)
    fig.savefig(OUT / "regimes.pdf", bbox_inches="tight")
    fig.savefig(OUT / "regimes.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    for name, rows in (("eq_regimes.csv", eq), ("c_response_pairs.csv", paired)):
        with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print("Rendered retained-data figure: 15 EQ campaigns, 10 C/12 paired contrasts.", flush=True)
    autonomous_figures(data)


if __name__ == "__main__":
    main()
