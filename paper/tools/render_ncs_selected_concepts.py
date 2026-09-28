"""Reconstruct the selected F4-C/F5-B designs from retained numerical evidence."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from render_ncs_narrative_closeout import (
    ARM_COLORS,
    ARMS,
    GROUPS,
    INK,
    REF,
    configure,
    data,
    load_panel_a_data,
    save,
    style,
)

ORDER = ("GPT-5.5", "Luna", "Terra", "Sol", "Astra")
NAMES = ("GPT-5.5", "GPT-5.6 Luna", "GPT-5.6 Terra", "GPT-5.6 Sol", "GPT-6 Astra")


def heading(fig, letter, title, x, y):
    fig.text(x - 0.052, y, letter, fontsize=20, weight="bold", va="bottom")
    fig.text(x, y, title, fontsize=18, weight="bold", va="bottom")


def rule(fig, xs, ys):
    fig.add_artist(Line2D(xs, ys, transform=fig.transFigure, color="#9AA2A8", lw=0.6))


def legend(fig, x, y, columns=3):
    fig.legend(
        handles=[Patch(color=ARM_COLORS[a], label=a) for a in ARMS],
        loc="center",
        bbox_to_anchor=(x, y),
        ncol=columns,
        frameon=False,
        fontsize=16,
        handlelength=0.85,
        columnspacing=1.8,
    )


def figure4(build, process, values):
    fig = plt.figure(figsize=(14.25, 9.5), facecolor="white")
    a = fig.add_axes([0.066, 0.565, 0.35, 0.36])
    b = fig.add_axes([0.515, 0.565, 0.47, 0.36])
    for ax in (a, b):
        style(ax)
    heading(fig, "a", "Local evidence and dilute tests", 0.066, 0.958)
    heading(fig, "b", "Prior benefits can reverse for GPT-5.6 Sol", 0.515, 0.958)
    rule(fig, [0.445, 0.445], [0.445, 0.984])
    rows, _, _, _ = load_panel_a_data()
    refs = [next(r for r in rows if r["query"] == q) for q in sorted({r["query"] for r in rows})]
    source = np.array(
        [
            (
                b["nominal_concentration_mol_L"],
                100 * b["final_responses"]["acid_dissociation_fraction"],
            )
            for r in process["rows"]
            for b in r["batches"]
        ]
    )
    a.axvspan(1.3333333e-5, 1.6666667e-4, color="#EEF2F4", zorder=0)
    a.scatter(source[:, 0], source[:, 1], s=15, c="#8999A6", alpha=0.7, linewidths=0)
    for r in refs:
        a.errorbar(
            r["nominal_concentration_M"],
            r["mean_across_worlds_percent"],
            yerr=r["sample_sd_across_worlds_percent"],
            fmt="D",
            color=REF,
            markersize=5,
            capsize=3,
            elinewidth=1,
        )
    a.set(
        xscale="log",
        xlim=(8e-6, 10),
        ylim=(0, 85),
        xlabel="Nominal concentration (M)",
        ylabel="Dissociation (%)",
    )
    a.set_xticks([1e-5, 1e-3, 0.1, 10], ["10⁻⁵", "10⁻³", "10⁻¹", "10¹"])
    a.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    a.set_yticks([0, 20, 40, 60, 80])
    a.text(1.4e-5, 81, "Lowest\nconcentrations", fontsize=16, va="top")
    a.text(0.0018, 24, "Source assays (180)\n0.0185–2 M\n5.5–9.2% dissociation", fontsize=16)
    fig.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                ls="none",
                color="#8999A6",
                label="Source assays: observed by agents",
            ),
            Line2D(
                [0], [0], marker="D", ls="none", color=REF, label="Reference: 5-world mean ± SD"
            ),
        ],
        loc="center left",
        bbox_to_anchor=(0.058, 0.461),
        frameon=False,
        fontsize=16,
        handletextpad=0.5,
    )
    for gi, group in enumerate(GROUPS):
        for ai, arm in enumerate(ARMS):
            x = gi * 4 + ai
            mean = float(values[("Sol", group, arm)].mean())
            b.bar(x, mean - 0.001, bottom=0.001, width=0.65, color=ARM_COLORS[arm])
            b.text(x, mean * 1.18, f"{mean:.5f}", ha="center", va="bottom", fontsize=16, color=INK)
    b.set(yscale="log", ylim=(0.001, 1), xlim=(-0.65, 6.65), ylabel="Macro MAE (log scale)")
    b.set_yticks([0.001, 0.01, 0.1, 1], ["10⁻³", "10⁻²", "10⁻¹", "10⁰"])
    b.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    b.set_xticks([1, 5], ["Remaining conditions\n(n = 9)", "Lowest concentrations\n(n = 3)"])
    b.axvline(3, color="#CCD2D6", linestyle="--", lw=0.7)
    for x, y, ratio in [(1, 0.065, "0.46×"), (5, 0.62, "8.65×")]:
        b.text(x, y, ratio, ha="center", fontsize=20, weight="bold")
        b.text(x, y / 1.55, "Aligned / Opaque", ha="center", fontsize=16)
    fig.text(0.75, 0.485, "Bars: mean across 5 worlds", ha="center", fontsize=16)
    legend(fig, 0.75, 0.45)
    heading(fig, "c", "Five model configurations show heterogeneous behavior", 0.066, 0.384)
    for mi, (model, name) in enumerate(zip(ORDER, NAMES, strict=True)):
        left = 0.077 + mi * 0.184
        ax = fig.add_axes([left, 0.125, 0.168, 0.205])
        style(ax)
        fig.text(left + 0.084, 0.346, name, ha="center", fontsize=16, weight="bold")
        for gi, group in enumerate(GROUPS):
            for ai, arm in enumerate(ARMS):
                y = 1 - gi - ai * 0.24
                v = float(values[(model, group, arm)].mean())
                ax.barh(y, v - 0.001, left=0.001, height=0.16, color=ARM_COLORS[arm])
                ax.annotate(
                    f"{v:.5f}",
                    (v, y),
                    xytext=(7, 0),
                    textcoords="offset points",
                    va="center",
                    color=INK,
                    fontsize=16,
                )
        ax.set(xscale="log", xlim=(0.001, 1.5), ylim=(-0.70, 1.30))
        ax.axhline(0.26, color="#CCD2D6", linestyle="--", lw=0.7)
        ax.set_xticks([0.001, 0.01, 0.1, 1], ["10⁻³", "10⁻²", "10⁻¹", "10⁰"])
        ax.xaxis.set_minor_locator(mpl.ticker.NullLocator())
        ax.set_yticks([])
        ax.tick_params(labelsize=16)
    fig.text(0.069, 0.275, "Other\n(n = 9)", fontsize=16, va="center", ha="right")
    fig.text(0.069, 0.17, "Lowest\n(n = 3)", fontsize=16, va="center", ha="right")
    fig.text(0.535, 0.055, "Macro MAE (log scale)", fontsize=18, ha="center")
    legend(fig, 0.535, 0.02)
    save(fig, build, "figure04")


def figure5(build, process, coverage, case, q):
    fig = plt.figure(figsize=(14.25, 9.5), facecolor="white")
    heading(fig, "a", "Lowest concentration assayed in each campaign", 0.066, 0.96)
    fig.text(
        0.066,
        0.934,
        "Five worlds per information condition; 15 campaigns per model",
        fontsize=16,
    )
    a = fig.add_axes([0.111, 0.744, 0.859, 0.169])
    style(a)
    legend(fig, 0.805, 0.97)
    a.axhline(0.001, color="#B8BEC2", linestyle="--", linewidth=0.7, zorder=0)
    for mi, model in enumerate(ORDER):
        rows = [r for r in coverage if r["model"] == model]
        for ai, arm in enumerate(ARMS):
            minima = [r["minimum"] for r in rows if r["arm"] == arm]
            assert len(minima) == 5
            color = ARM_COLORS[arm]
            quartiles = np.quantile(minima, [0.25, 0.75])
            collapsed = quartiles[0] == quartiles[1]
            a.boxplot(
                [minima],
                positions=[mi + (ai - 1) * 0.23],
                widths=0.17,
                whis=(0, 100),
                showfliers=False,
                patch_artist=True,
                manage_ticks=False,
                boxprops={"facecolor": color, "edgecolor": color, "linewidth": 1},
                medianprops={"color": color if collapsed else INK, "linewidth": 1.6},
                whiskerprops={"color": color, "linewidth": 1},
                capprops={"color": color, "linewidth": 1},
            )
        n = sum(r["minimum"] <= 0.001 + 1e-12 for r in rows)
        fig.text(
            0.111 + 0.859 * (mi + 0.5) / 5,
            0.689,
            f"{n} / 15",
            fontsize=16,
            ha="center",
            va="center",
        )
    a.set(
        yscale="log",
        ylim=(7e-6, 0.5),
        xlim=(-0.5, 4.5),
        ylabel="Minimum assayed\nconcentration (M)",
    )
    a.set_yticks([1e-5, 1e-3, 0.1], ["10⁻⁵", "10⁻³", "10⁻¹"])
    a.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    a.set_xticks(range(5), NAMES)
    a.tick_params(labelsize=16)
    fig.text(0.11, 0.689, "≤ 1 mM:", fontsize=16, ha="right", va="center")
    rule(fig, [0, 1], [0.656, 0.656])
    rule(fig, [0.474, 0.474], [0.025, 0.648])
    opaque = sorted([r for r in process["rows"] if r["arm"] == "Opaque"], key=lambda r: r["world"])
    heading(fig, "b", "Local evidence and extrapolation", 0.066, 0.615)
    fig.text(0.066, 0.589, "GPT-5.6 Sol / Opaque", fontsize=16)
    fig.text(0.066, 0.55, "Source observations (World 1)", fontsize=16, weight="bold")
    b = fig.add_axes([0.073, 0.414, 0.363, 0.115])
    style(b)
    batches = opaque[0]["batches"]
    b.scatter(
        [r["nominal_concentration_mol_L"] for r in batches],
        [100 * r["final_responses"]["acid_dissociation_fraction"] for r in batches],
        s=24,
        color=ARM_COLORS["Opaque"],
    )
    b.set(
        xscale="log",
        xlim=(0.012, 3),
        ylim=(0, 30),
        ylabel="Dissociation (%)",
        xlabel="Nominal concentration (M)",
    )
    b.set_xticks([0.02, 0.1, 1], ["0.02", "0.1", "1"])
    b.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    b.set_yticks([0, 10, 20, 30])
    b.tick_params(labelsize=16)
    b.text(0.07, 17, "12 assays: apparent plateau", fontsize=16)
    heading(fig, "c", "Five-world predictions at 13.3 µM", 0.066, 0.325)
    c = fig.add_axes([0.073, 0.096, 0.363, 0.201])
    style(c)
    for wi, row in enumerate(opaque):
        pred = row["q08"]["predictions"]["acid_dissociation_fraction"]
        y = 100 * pred["estimate"]
        c.errorbar(
            wi - 0.09,
            y,
            yerr=[[y - 100 * pred["lower80"]], [100 * pred["upper80"] - y]],
            fmt="o",
            color=ARM_COLORS["Opaque"],
            markersize=5,
            capsize=3,
            lw=1,
        )
        c.plot(
            wi + 0.09,
            100 * row["q08"]["reference_means"]["acid_dissociation_fraction"],
            "D",
            color=INK,
            markersize=5,
        )
    observed = [
        100 * b["final_responses"]["acid_dissociation_fraction"]
        for r in opaque
        for b in r["batches"]
    ]
    c.axhspan(min(observed), max(observed), color="#E6EAED", zorder=0)
    c.text(2, 11, "Source observation range", fontsize=16, ha="center")
    c.set(xlim=(-0.5, 4.5), ylim=(0, 105), xlabel="World", ylabel="Dissociation (%)")
    c.set_xticks(range(5), ["1", "2", "3", "4", "5"])
    c.set_yticks([0, 20, 40, 60, 80, 100])
    c.tick_params(labelsize=16)
    fig.legend(
        handles=[
            Line2D([0], [0], marker="o", color=ARM_COLORS["Opaque"], ls="none", label="Prediction"),
            Line2D([0], [0], marker="D", color=INK, ls="none", label="Reference"),
        ],
        loc="center",
        bbox_to_anchor=(0.265, 0.305),
        ncol=2,
        frameon=False,
        fontsize=16,
        handletextpad=0.25,
        columnspacing=1,
    )
    fig.text(0.075, 0.005, "Intervals: original 80% prediction intervals", fontsize=16)
    heading(fig, "d", "Expanded evidence and prediction", 0.529, 0.615)
    fig.text(0.529, 0.589, "GPT-6 Astra (World 3, MisIndexed)", fontsize=16)
    d = fig.add_axes([0.552, 0.438, 0.375, 0.122])
    style(d)
    dr = d.twinx()
    dr.spines["top"].set_visible(False)
    x = np.arange(1, 13)
    alpha = np.array([100 * float(r["acid_dissociation_fraction"]) for r in case])
    conc = np.array([float(r["nominal_input_concentration_M"]) for r in case])
    color = ARM_COLORS["MisIndexed"]
    dr.plot(x, conc, "s-", color=ARM_COLORS["Opaque"], markersize=4, lw=0.8, zorder=1)
    d.plot(x, alpha, "o-", color=color, markersize=5, lw=1.1, zorder=3)
    d.set(xlim=(0.6, 12.4), ylim=(0, 72), xlabel="Batch", ylabel="Dissociation (%)")
    d.set_xticks(range(1, 13))
    d.set_yticks([0, 20, 40, 60])
    d.tick_params(labelsize=16)
    dr.set(yscale="log", ylim=(6e-6, 5), ylabel="Concentration (M)")
    dr.set_yticks([1e-5, 0.001, 1], ["10⁻⁵", "10⁻³", "10⁰"])
    dr.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    dr.tick_params(labelsize=16)
    d.yaxis.label.set_color(color)
    dr.yaxis.label.set_color(ARM_COLORS["Opaque"])
    fig.legend(
        handles=[
            Line2D([0], [0], marker="o", color=color, label="Dissociation"),
            Line2D([0], [0], marker="s", color=ARM_COLORS["Opaque"], label="Concentration"),
        ],
        loc="center",
        bbox_to_anchor=(0.749, 0.352),
        ncol=2,
        frameon=False,
        fontsize=16,
        handlelength=1.2,
        columnspacing=1.5,
    )
    fig.text(0.529, 0.289, "After experiments: public report (K1)", fontsize=16, weight="bold")
    fig.text(
        0.657,
        0.234,
        "High loading: apparent plateau\nLow loading: responsive regime",
        fontsize=16,
        linespacing=1.3,
        bbox={"facecolor": "#EEF2F4", "edgecolor": "none", "pad": 3},
    )
    fig.text(0.529, 0.193, "Sealed forecast (Q): 13.3 µM", fontsize=16, weight="bold")
    forecast = fig.add_axes([0.58, 0.063, 0.324, 0.091])
    style(forecast)
    est, lower, upper, truth = [
        100 * q[k] for k in ("estimate", "lower80", "upper80", "reference_mean")
    ]
    forecast.errorbar(
        est,
        1,
        xerr=[[est - lower], [upper - est]],
        fmt="o",
        color=color,
        capsize=4,
        markersize=6,
        lw=1.1,
    )
    forecast.plot(truth, 0, "D", color=INK, markersize=5)
    forecast.set(xlim=(40, 74), ylim=(-0.7, 2), xlabel="Dissociation (%)")
    forecast.set_xticks([40, 50, 60, 70])
    forecast.set_yticks([1, 0], ["Prediction", "Reference"])
    forecast.tick_params(labelsize=16)
    forecast.text(est, 1.55, "58.80% [54.20, 63.40]", ha="center", fontsize=16)
    forecast.text(truth + 1.5, 0, "57.97%", va="center", fontsize=16)
    fig.text(0.929, 0.09, "Reference\nwithheld\nfrom agent", fontsize=16)
    save(fig, build, "figure05")
    # The selected concept's small illustration remains a separate raster object.
    (build / "figure05-image.json").write_text(
        json.dumps(
            {
                "path": str(
                    Path(__file__).resolve().parents[2]
                    / "output/imagegen/figure45-concepts-20260928/F5-B.png"
                ),
                "position": {
                    "left": 0.529 * 1026,
                    "top": (1 - 0.274) * 684,
                    "width": 0.088 * 1026,
                    "height": 0.044 * 1026,
                },
                "crop": {
                    "left": 812 / 1536,
                    "top": 729 / 1024,
                    "right": (1536 - 962) / 1536,
                    "bottom": (1024 - 804) / 1024,
                },
            }
        ),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, required=True)
    args = parser.parse_args()
    args.build.mkdir(parents=True, exist_ok=True)
    configure()
    mpl.rcParams["lines.linewidth"] = 1
    process, values, coverage, case, q = data()
    figure4(args.build, process, values)
    figure5(args.build, process, coverage, case, q)


if __name__ == "__main__":
    main()
