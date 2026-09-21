"""Render the exploratory EQ/C comparison from retained results; no new experiments."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
    / "STORY_WORLD_ANALYSIS.json"
)
OUT = ROOT / "paper/figures/venue-results"
COLORS = {"Opaque": "#34648B", "Aligned": "#21806B", "MisIndexed": "#C66D39"}
GROUPS = ("other_nine", "three_most_dilute")


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


if __name__ == "__main__":
    main()
