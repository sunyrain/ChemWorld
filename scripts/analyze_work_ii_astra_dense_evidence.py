"""Plot and independently check closed W2-101 records, without new experiments."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scripts import run_work_ii_astra_corrected_pilot as base

ROOT = Path(__file__).resolve().parents[1]


def main():
    current = base.read(ROOT / "configs/current.json")["work_ii"]
    early = base.read(ROOT / current["w2_101_early_time_screen"]["report"])
    path = ROOT / current["w2_101_astra_dense_evidence"]["report"]
    dense = base.read(path)
    lookup = {(r["world"], int(r["name"].rsplit("/", 1)[1])): r for r in early["rows"]}
    assert len(lookup) == 288
    assert sum(r["exact_replay"] for r in early["rows"]) == 288
    for row in early["rows"]:
        public = row["public"]
        h, terminal = public["upstream_hplc"], public["terminal"]
        expected = h["yield"] * 0.992 * terminal["crystal_yield"] * terminal["crystal_purity"]
        utility = expected * 3600 / row["resources"]["process_time_s"]
        assert math.isclose(utility, terminal["utility_per_hour"], abs_tol=1e-12)
        p = row["plan"]
        expected_cooling = 275 + p["cooling_fraction"] * (
            min(310, public["actual_quench_temperature_K"]) - 275
        )
        assert math.isclose(expected_cooling, public["actual_cooling_temperature_K"], abs_tol=1e-9)
    for condition in dense["conditions"]:
        if condition["status"] != "completed":
            continue
        scores = condition["prediction_scores"]
        assert len(scores["rows"]) == 18
        for metric in base.METRICS:
            error = np.mean(
                [abs(r["prediction"][metric] - r["truth"][metric]) for r in scores["rows"]]
            )
            assert math.isclose(error, scores["metrics"]["all"]["mae"][metric], abs_tol=1e-12)
        for world, i in condition["payload"]["selections"].items():
            assert (
                lookup[world, i]["public"]["terminal"]["utility_per_hour"]
                == condition["selection_utility"][world]
            )
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.2), layout="constrained")
    colors = ("#0072B2", "#D55E00", "#009E73", "#CC79A7")
    for color, world in zip(colors, base.WORLDS, strict=True):
        rows = sorted(
            [
                r
                for r in early["rows"]
                if r["world"] == world
                and r["plan"]["reaction_temperature_K"] == 405
                and r["plan"]["cooling_fraction"] == 0
                and r["plan"]["cooling_duration_s"] == 1200
            ],
            key=lambda r: r["plan"]["reaction_duration_s"],
        )
        axes[0, 0].plot(
            [r["plan"]["reaction_duration_s"] for r in rows],
            [r["public"]["terminal"]["utility_per_hour"] for r in rows],
            "o-",
            color=color,
            label=world,
            linewidth=1.5,
        )
    axes[0, 0].set(
        xscale="log",
        xlabel="Reaction duration (s)",
        ylabel="Public utility per hour",
        title="A  Earlier times, fixed 405 K / cold / 1200 s",
    )
    axes[0, 0].legend(ncols=2, frameon=False)
    distances = sorted(r["distance"] for r in early["support"])
    axes[0, 1].plot(distances, np.arange(1, 145) / 144, color="#0072B2", linewidth=2)
    axes[0, 1].axvline(0.05, color="#888888", linestyle="--", label="Near-support threshold")
    axes[0, 1].set(
        xlabel="Public interface distance to source convex hull",
        ylabel="Fraction of all 144 heldout grid points",
        ylim=(0, 1.03),
        title=f"B  Support: {early['near_support']['count']}/144 near",
    )
    axes[0, 1].legend(frameon=False, fontsize=9)
    labels = {
        "raw": "Raw",
        "whole": "Whole",
        "component": "Components",
        "raw_scaffold": "Raw + steps",
        "task_only": "No evidence",
    }
    rows = [r for r in dense["conditions"] if r["status"] == "completed"]
    positions = np.arange(len(rows))
    for j, (group, label) in enumerate(
        (("all", "All 18 queries"), ("near_support", "17 near-support queries"))
    ):
        axes[1, 0].scatter(
            positions + (j - 0.5) * 0.15,
            [r["prediction_scores"]["metrics"][group]["mae"]["crystal_yield"] for r in rows],
            s=48,
            color=colors[j],
            label=label,
        )
    axes[1, 0].set(
        xticks=positions,
        xticklabels=[labels[r["condition"]] for r in rows],
        ylabel="Crystal recovery MAE (log scale)",
        yscale="log",
        ylim=(0.001, 1),
        title="C  Same-evidence recovery prediction",
    )
    axes[1, 0].tick_params(axis="x", labelrotation=15)
    axes[1, 0].legend(frameon=False)
    utility = [np.mean([r["selection_utility"][w] for w in base.WORLDS[2:]]) for r in rows]
    axes[1, 1].bar(positions, utility, color="#0072B2")
    for i, value in enumerate(utility):
        if value == 0:
            axes[1, 1].annotate("0", (i, 0.006), ha="center")
    upper = np.mean([early["action_value"]["best_by_world"][w]["utility"] for w in base.WORLDS[2:]])
    source_winners = early["action_value"]["source_winner_indices"]
    copied = np.mean(
        [
            max(lookup[w, i]["public"]["terminal"]["utility_per_hour"] for i in source_winners)
            for w in base.WORLDS[2:]
        ]
    )
    axes[1, 1].axhline(upper, color="#222222", linestyle="--", label="Grid upper reference")
    axes[1, 1].axhline(copied, color="#D55E00", linestyle=":", label="Better of two source winners")
    axes[1, 1].set(
        xticks=positions,
        xticklabels=[labels[r["condition"]] for r in rows],
        ylabel="Mean heldout utility per hour",
        title="D  Selection among 72 measured recipes",
    )
    axes[1, 1].tick_params(axis="x", labelrotation=15)
    axes[1, 1].legend(frameon=False, fontsize=8, loc="lower left")
    fig.suptitle("Development pilot: one mechanism group, one session per condition", fontsize=14)
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)
    print(
        "Verified 288 utilities/temperature mappings, replay counts and every valid "
        "readout score; figure saved."
    )


if __name__ == "__main__":
    main()
