"""Render Figure 5 from retained source observations and sealed forecasts only."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
OUT = ROOT / "paper/figures/venue-results"
DATA = ROOT / "output/figures/applicability-closeout"
ARMS = ("Opaque", "Aligned", "MisIndexed")
COLORS = {"Opaque": "#607382", "Aligned": "#287E88", "MisIndexed": "#B87752"}
INK = "#202326"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(name, rows):
    with (DATA / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E3E6E8", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, width=0.7)


def main():
    process = read(REPORT / "EQ_AUTONOMOUS_PROCESS.json")
    study = read(REPORT / "STORY_WORLD_ANALYSIS.json")["eq_p_query_regimes"]
    rows, cells = process["rows"], study["cells"]
    worlds = [f"W0{i}" for i in range(1, 6)]
    assert {(r["world"], r["arm"]) for r in rows} == {
        (world, arm) for world in worlds for arm in ARMS
    }
    source = [
        {
            "world": r["world"],
            "arm": r["arm"],
            "batch": i + 1,
            "nominal_concentration": b["nominal_concentration_mol_L"],
            "dissociation": b["final_responses"]["acid_dissociation_fraction"],
        }
        for r in rows
        for i, b in enumerate(r["batches"])
    ]
    references = []
    for world in worlds:
        cell = next(c for c in cells if c["world"] == world and c["arm"] == "Opaque")
        for group in cell["groups"].values():
            for p in group["points"]:
                if p["metric"] == "acid_dissociation_fraction":
                    references.append(
                        {
                            "world": world,
                            "query": p["query"],
                            "nominal_concentration": process["query_concentrations"][p["query"]],
                            "dissociation": p["truth_mean"],
                        }
                    )
    assert len(source) == 180 and len(references) == 60
    assert len({(r["world"], r["query"]) for r in references}) == 60
    observed = np.array([r["dissociation"] * 100 for r in source])
    stats = {(r["group"], r["arm"]): r for r in study["aggregate"]}
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 11,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.edgecolor": "#8C969C",
            "axes.linewidth": 0.7,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "mathtext.default": "regular",
            "savefig.facecolor": "white",
        }
    )
    fig = plt.figure(figsize=(11.4, 7.1), facecolor="white")
    a = fig.add_axes([0.075, 0.565, 0.40, 0.365])
    b = fig.add_axes([0.610, 0.565, 0.355, 0.365])
    c = fig.add_axes([0.075, 0.095, 0.890, 0.315])
    for ax, letter in ((a, "a"), (b, "b"), (c, "c")):
        style(ax)
        ax.text(
            -0.15 if ax is b else -0.12 if ax is a else -0.054,
            1.025,
            letter,
            transform=ax.transAxes,
            fontsize=15,
            weight="bold",
        )

    a.set_xscale("log")
    a.axvspan(8e-6, 2.2e-4, color="#F0F2F3", zorder=0)
    a.scatter(
        [r["nominal_concentration"] for r in source],
        observed,
        s=16,
        color="#8D9AA3",
        alpha=0.65,
        linewidths=0,
        zorder=3,
    )
    a.scatter(
        [r["nominal_concentration"] for r in references],
        [r["dissociation"] * 100 for r in references],
        s=23,
        marker="D",
        facecolors="none",
        edgecolors=INK,
        linewidths=0.8,
        zorder=4,
    )
    a.set(
        xlim=(8e-6, 3),
        ylim=(0, 85),
        ylabel="Dissociation (%)",
        xlabel="Nominal concentration (mol L$^{-1}$; log scale)",
    )
    a.set_xticks([1e-5, 1e-3, 1e-1, 1], [r"$10^{-5}$", r"$10^{-3}$", r"$10^{-1}$", "1"])
    a.set_yticks([0, 20, 40, 60, 80])
    a.text(4.4e-5, 79, "Dilute tests", ha="center", fontsize=10)
    a.legend(
        handles=[
            Line2D(
                [],
                [],
                marker="o",
                color="#8D9AA3",
                linestyle="none",
                markersize=5,
                label="Source assays (180)",
            ),
            Line2D(
                [],
                [],
                marker="D",
                color=INK,
                markerfacecolor="white",
                linestyle="none",
                markersize=5,
                label="Withheld references (60)",
            ),
        ],
        loc="upper right",
        frameon=False,
        fontsize=9.8,
        handletextpad=0.4,
    )
    a.annotate(
        "Observed plateau\n5.5-9.2%",
        xy=(0.07, 8),
        xytext=(0.003, 30),
        fontsize=10,
        arrowprops={"arrowstyle": "-", "color": "#8C969C", "lw": 0.7},
    )

    b.set_yscale("log")
    b.set(xlim=(-0.53, 1.53), ylim=(0.0013, 0.65), ylabel="Macro MAE (log scale)")
    b.set_xticks([0, 1], ["Other nine", "Dilute three"])
    b.set_yticks([0.002, 0.01, 0.05, 0.2], ["0.002", "0.01", "0.05", "0.2"])
    b.minorticks_off()
    for gi, group in enumerate(("other_nine", "three_most_dilute")):
        for ai, arm in enumerate(ARMS):
            xx = gi + (ai - 1) * 0.24
            vals = [
                next(r for r in cells if (r["world"], r["arm"]) == (w, arm))["groups"][group]["mae"]
                for w in worlds
            ]
            mean = stats[group, arm]["mae"]
            assert abs(float(np.mean(vals)) - mean) < 1e-12
            b.scatter(
                xx + np.linspace(-0.048, 0.048, 5),
                vals,
                s=29,
                facecolors="white",
                edgecolors=COLORS[arm],
                linewidths=1,
                zorder=3,
            )
            b.plot([xx - 0.085, xx + 0.085], [mean, mean], color=COLORS[arm], lw=2.7, zorder=4)
        ratio = stats[group, "Aligned"]["mae"] / stats[group, "Opaque"]["mae"]
        b.text(gi, 0.56, f"Aligned / Opaque\n{ratio:.2f}\u00d7", va="top", ha="center", fontsize=10)

    xx, width = np.arange(5), 0.17
    c.axhspan(observed.min(), observed.max(), color="#E9EDEF", zorder=0)
    exports = []
    for j, label in enumerate(("Reference", *ARMS)):
        values = []
        for world in worlds:
            rr = [r for r in rows if r["world"] == world]
            refs = [r["q08"]["reference_means"]["acid_dissociation_fraction"] for r in rr]
            assert max(refs) == min(refs)
            if label == "Reference":
                values.append(refs[0] * 100)
            else:
                r = next(r for r in rr if r["arm"] == label)
                pred = r["q08"]["predictions"]["acid_dissociation_fraction"]
                values.append(pred["estimate"] * 100)
                exports.append({"world": world, "arm": label, "reference_mean": refs[0], **pred})
        bars = c.bar(
            xx + (j - 1.5) * (width + 0.012),
            values,
            width,
            color="#BFC8CD" if j == 0 else COLORS[label],
            zorder=3,
        )
        c.bar_label(bars, labels=[f"{v:.1f}" for v in values], padding=3, fontsize=9.5, color=INK)
    c.set(xlim=(-0.53, 4.70), ylim=(0, 87), ylabel="Dissociation (%)")
    c.set_xticks(xx, [f"World {i}" for i in range(1, 6)])
    c.set_yticks([0, 20, 40, 60, 80])
    c.tick_params(axis="x", length=0, pad=8)
    c.text(1.0, 1.035, "Most dilute test: 13.3 µM", ha="right", transform=c.transAxes, fontsize=10)
    fig.legend(
        handles=[Line2D([], [], color=COLORS[arm], lw=5, label=arm) for arm in ARMS]
        + [Line2D([], [], color="#BFC8CD", lw=5, label="Withheld reference")],
        loc="center",
        bbox_to_anchor=(0.53, 0.46),
        ncol=4,
        frameon=False,
        fontsize=10.5,
        handlelength=1.1,
        columnspacing=2.5,
    )
    OUT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"figure05-eq-coverage-reversal.{ext}", dpi=240)
    plt.close(fig)
    write_csv("figure05-source-assays.csv", source)
    write_csv("figure05-withheld-references.csv", references)
    write_csv("figure05-most-dilute-forecasts.csv", exports)
    assert len(exports) == 15
    print(
        "Figure 5 complete: 180 source assays, 60 reference means, "
        "30 regime points, 15 forecasts; no new experiments."
    )


if __name__ == "__main__":
    main()
