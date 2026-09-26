"""Render the selected Figure 5 layout at editable-source point sizes.

Retain the remote three-panel/bar composition, original arm colours, all
source assays and five-world points. This is retained-data presentation only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle
from ncs_figure_style import ARM_COLORS
from render_figure05_bar_b_overlay_candidate import (
    ARMS,
    GROUPS,
    REPORT,
    load_panel_a_data,
    load_panel_b_data,
    load_panel_c_data,
)

ROOT = Path(__file__).resolve().parents[2]
INK = "#111111"
REFERENCE = "#BFC9CF"
BAND = "#E6EAED"


def configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 18,
            "axes.labelsize": 18,
            "xtick.labelsize": 18,
            "ytick.labelsize": 18,
            "legend.fontsize": 18,
            "axes.linewidth": 1,
            "text.color": INK,
            "axes.labelcolor": INK,
            "axes.edgecolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "axes.unicode_minus": False,
            "savefig.facecolor": "white",
        }
    )


def axis_style(ax: plt.Axes) -> None:
    ax.grid(False)
    ax.tick_params(direction="out", length=5, width=1, pad=6)
    for spine in ax.spines.values():
        spine.set_linewidth(1)


def header(fig: plt.Figure, letter: str, title: str, x: float, y: float) -> None:
    fig.text(x - 0.065, y, letter, fontsize=20, fontweight="bold", va="bottom")
    fig.text(x, y, title, fontsize=18, fontweight="bold", va="bottom")


def render(out: Path) -> None:
    configure()
    a_rows, low, high, source_min = load_panel_a_data()
    b_values, _ = load_panel_b_data()
    refs, forecasts, _, _, _ = load_panel_c_data()
    process = json.loads((REPORT / "EQ_AUTONOMOUS_PROCESS.json").read_text(encoding="utf-8"))
    source = np.asarray(
        [
            (
                batch["nominal_concentration_mol_L"],
                100 * batch["final_responses"]["acid_dissociation_fraction"],
            )
            for row in process["rows"]
            for batch in row["batches"]
        ]
    )
    assert len(source) == 180
    # 1026 pt becomes 1368 px in the native 1440 px slide without changing type sizes.
    fig = plt.figure(figsize=(14.25, 10.4), facecolor="white")
    a = fig.add_axes([0.085, 0.58, 0.385, 0.335])
    b = fig.add_axes([0.59, 0.58, 0.39, 0.335])
    c = fig.add_axes([0.085, 0.115, 0.895, 0.26])
    for ax in (a, b, c):
        axis_style(ax)
    header(fig, "a", "Evidence coverage gap", 0.085, 0.957)
    header(fig, "b", "Error reversal across regimes", 0.59, 0.957)
    header(fig, "c", "Original forecasts at the most dilute condition", 0.085, 0.423)
    fig.text(0.98, 0.423, "13.3 µM", ha="right", va="bottom", fontsize=18)

    # a: actual x coverage is retained, rather than an all-concentration band.
    summaries = [
        next(row for row in a_rows if row["query"] == q)
        for q in sorted({row["query"] for row in a_rows})
    ]
    dilute = [
        row["nominal_concentration_M"] for row in summaries if row["regime"] == "Dilute three"
    ]
    a.axvspan(min(dilute) / 1.18, max(dilute) * 1.18, color="#EFF2F4", zorder=0)
    a.add_patch(
        Rectangle(
            (source_min, low),
            float(source[:, 0].max()) - source_min,
            high - low,
            facecolor=BAND,
            edgecolor="none",
            zorder=0,
        )
    )
    a.scatter(source[:, 0], source[:, 1], s=13, color="#8D99A1", alpha=0.60, linewidths=0, zorder=2)
    for row in summaries:
        # Recipe coordinates stay exact, even where distinct recipes overlap.
        a.errorbar(
            row["nominal_concentration_M"],
            row["mean_across_worlds_percent"],
            yerr=row["sample_sd_across_worlds_percent"],
            fmt="D",
            markersize=6,
            color="#444B50",
            markeredgecolor="white",
            markeredgewidth=0.6,
            elinewidth=1,
            capsize=3,
            zorder=3,
        )
    a.set_xscale("log")
    a.set_xlim(8e-6, 10)
    a.set_ylim(0, 82)
    a.set_xticks([1e-5, 1e-3, 1e-1, 10], ["10⁻⁵", "10⁻³", "10⁻¹", "10¹"])
    a.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    a.set_yticks([0, 20, 40, 60, 80])
    a.set_xlabel("Nominal concentration (M; log scale)", labelpad=10)
    a.set_ylabel("Dissociation (%)", labelpad=9)
    a.text(5e-5, 75, "Dilute tests", ha="center", fontsize=16)
    a.text(0.0013, 63, "No source assays\nin dilute regime", fontsize=18)
    a.text(0.025, 23, "Source assays (180)\n0.0185\u20132 M\n5.5\u20139.2%", fontsize=16)
    fig.text(0.085, 0.93, "12 withheld queries: mean ± SD across 5 worlds", fontsize=16)

    # b: keep bars, supplement them with every original world-level estimate.
    centres = np.asarray([0.0, 1.35])
    width = 0.26
    offsets = [-0.35, 0, 0.35]
    jitter = np.asarray([-0.08, -0.04, 0, 0.04, 0.08])
    for arm, offset in zip(ARMS, offsets, strict=True):
        means = np.asarray([np.mean(b_values[(g, arm)]) for g in GROUPS])
        sd = np.asarray([np.std(b_values[(g, arm)], ddof=1) for g in GROUPS])
        assert np.all(means - sd > 0)
        b.bar(
            centres + offset,
            means - 0.001,
            bottom=0.001,
            width=width,
            color=ARM_COLORS[arm],
            edgecolor="none",
            zorder=2,
        )
        b.errorbar(
            centres + offset,
            means,
            yerr=sd,
            fmt="none",
            color=INK,
            elinewidth=1,
            capsize=4,
            capthick=1,
            zorder=4,
        )
        for index, group in enumerate(GROUPS):
            b.scatter(
                centres[index] + offset + jitter,
                b_values[(group, arm)],
                s=19,
                facecolors="white",
                edgecolors=ARM_COLORS[arm],
                linewidths=1,
                zorder=5,
            )
            label_offset = 1.55 if arm == "MisIndexed" else 1.20
            y = max(means[index] + sd[index], max(b_values[(group, arm)])) * label_offset
            b.text(
                centres[index] + offset,
                y,
                f"{means[index]:.5f}",
                ha="center",
                va="bottom",
                fontsize=16,
            )
    for centre, group in zip(centres, GROUPS, strict=True):
        ratio = np.mean(b_values[(group, "Aligned")]) / np.mean(b_values[(group, "Opaque")])
        b.text(
            centre, 0.64, f"Aligned / Opaque: {ratio:.2f}\u00d7",
            fontsize=16, ha="center", va="center"
        )
    b.set_yscale("log")
    b.set_ylim(0.001, 1)
    b.set_xlim(-0.63, 1.98)
    b.set_yticks([0.001, 0.01, 0.1, 1], ["10⁻³", "10⁻²", "10⁻¹", "10⁰"])
    b.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    b.set_xticks(centres, ["Other nine", "Dilute three"])
    b.set_ylabel("Macro MAE (log scale)", labelpad=9)
    fig.text(0.59, 0.93, "Bars: mean ± SD; dots: 5 worlds", fontsize=16)
    fig.legend(
        handles=[Patch(facecolor=ARM_COLORS[arm], label=arm) for arm in ARMS],
        loc="center",
        bbox_to_anchor=(0.785, 0.505),
        ncol=3,
        frameon=False,
        fontsize=16,
        handlelength=1.2,
        handletextpad=0.4,
        columnspacing=1.2,
    )

    # c: original forecasts, unchanged values and the original neutral reference colour.
    x = np.arange(5)
    width = 0.17
    series = [("Withheld reference", refs, REFERENCE)] + [
        (arm, forecasts[arm], ARM_COLORS[arm]) for arm in ARMS
    ]
    c.axhspan(low, high, color=BAND, zorder=0)
    for offset, (_, values, color) in zip(
        np.asarray([-1.5, -0.5, 0.5, 1.5]) * 0.184, series, strict=True
    ):
        bars = c.bar(
            x + offset, values, width=width, color=color, edgecolor="white", linewidth=0.7, zorder=2
        )
        for bar, value in zip(bars, values, strict=True):
            c.text(
                bar.get_x() + bar.get_width() / 2,
                value + 1.5,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=16,
            )
    c.set_xlim(-0.55, 4.62)
    c.set_ylim(0, 87)
    c.set_yticks([0, 20, 40, 60, 80])
    c.set_xticks(x, [f"World {w}" for w in range(1, 6)])
    c.set_ylabel("Dissociation (%)", labelpad=9)
    c.tick_params(axis="x", length=0)
    c.annotate(
        "Source range\n5.5\u20139.2%",
        xy=(4.47, high),
        xytext=(4.47, 23),
        fontsize=16,
        ha="right",
        va="bottom",
        arrowprops={"arrowstyle": "-", "color": "#75838C", "lw": 0.8},
    )
    fig.legend(
        handles=[Patch(facecolor=color, label=name) for name, _, color in series],
        loc="center",
        bbox_to_anchor=(0.535, 0.032),
        ncol=4,
        frameon=False,
        fontsize=18,
        handlelength=1.3,
        handletextpad=0.5,
        columnspacing=1.8,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ("svg", "pdf", "png"):
        fig.savefig(out.with_suffix("." + suffix), dpi=300)
    plt.close(fig)
    print(
        "Figure 5: 180 assays, 60 reference values, 30 world errors, "
        f"20 forecasts/references; {out}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "paper/figures/venue-results/figure05-readable"
    )
    args = parser.parse_args()
    render(args.output)
