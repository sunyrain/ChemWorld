#!/usr/bin/env python3
"""Create a real-data Figure 5 evidence-gap candidate.

Panel a summarizes all 60 withheld reference values as 12 query-level means
and sample standard deviations across five physical worlds, against the pooled
range of all 180 source assays. Panel b shows mean macro MAE and sample standard
deviation across the five worlds for each information arm. Panel c retains the
approved five-world comparison, redrawn without grid lines. The current
manuscript asset is never overwritten.
"""

from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pymupdf
from matplotlib.patches import Patch
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
OUT_STEM = ROOT / "paper/figures/venue-results/figure05-panel-b-bars-candidate"
SOURCE_CSV = OUT_STEM.with_name(f"{OUT_STEM.name}-source-data.csv")
PANEL_A_SOURCE_CSV = OUT_STEM.with_name(f"{OUT_STEM.name}-panel-a-source-data.csv")
PANEL_C_SOURCE_CSV = OUT_STEM.with_name(f"{OUT_STEM.name}-panel-c-source-data.csv")

ARMS = ("Opaque", "Aligned", "MisIndexed")
GROUPS = ("other_nine", "three_most_dilute")
GROUP_LABELS = ("Other nine", "Dilute three")
INK = "#111111"
FINAL_WIDTH_MM = 183.0
DISPLAY_COLORS = {
    "Opaque": "#5B7DA5",
    "Aligned": "#49A88F",
    "MisIndexed": "#E98743",
}
REFERENCE_COLOR = "#555555"
SOURCE_BAND_COLOR = "#D9DEE2"
DILUTE_REGION_COLOR = "#EAF3F8"
DILUTE_BOUNDARY_COLOR = "#6B9FC3"

EXPECTED_MEANS = {
    ("other_nine", "Opaque"): 0.010076250577326171,
    ("other_nine", "Aligned"): 0.004647301928643827,
    ("other_nine", "MisIndexed"): 0.004389850205011723,
    ("three_most_dilute", "Opaque"): 0.01833210026545114,
    ("three_most_dilute", "Aligned"): 0.15862426151816295,
    ("three_most_dilute", "MisIndexed"): 0.14396808374038517,
}
DILUTE_QUERIES = {"Q03", "Q08", "Q09"}


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 11.5,
            "axes.labelsize": 12.5,
            "xtick.labelsize": 11.5,
            "ytick.labelsize": 11.0,
            "legend.fontsize": 11.5,
            "axes.linewidth": 0.8,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "xtick.major.size": 3.5,
            "ytick.major.size": 3.5,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
        }
    )


def style_boxed_axis(ax: plt.Axes) -> None:
    ax.grid(False)
    for side in ("left", "bottom", "top", "right"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color(INK)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(axis="both", colors=INK, direction="out", width=0.8, length=3.5)


def load_panel_b_data() -> tuple[dict[tuple[str, str], np.ndarray], list[dict[str, object]]]:
    path = REPORT / "STORY_WORLD_ANALYSIS.json"
    payload = json.loads(path.read_text(encoding="utf-8"))["eq_p_query_regimes"]
    cells = {(row["world"], row["arm"]): row for row in payload["cells"]}
    aggregates = {(row["group"], row["arm"]): row for row in payload["aggregate"]}
    if len(cells) != 15 or len(aggregates) != 6:
        raise RuntimeError("Figure 5b requires 15 world-arm cells and six retained aggregates")

    values: dict[tuple[str, str], np.ndarray] = {}
    source_rows: list[dict[str, object]] = []
    for group in GROUPS:
        for arm in ARMS:
            world_values = np.asarray(
                [
                    cells[(f"W{world:02d}", arm)]["groups"][group]["mae"]
                    for world in range(1, 6)
                ],
                dtype=float,
            )
            if not np.all(np.isfinite(world_values)) or np.any(world_values <= 0):
                raise RuntimeError(f"Log-scale MAE values must be finite and positive: {group}/{arm}")
            mean = float(np.mean(world_values))
            expected = EXPECTED_MEANS[(group, arm)]
            retained = float(aggregates[(group, arm)]["mae"])
            if abs(mean - expected) > 1e-12 or abs(retained - expected) > 1e-12:
                raise RuntimeError(f"Retained Figure 5 value changed: {group}/{arm}")
            values[(group, arm)] = world_values
            sample_sd = float(np.std(world_values, ddof=1))
            for world, value in enumerate(world_values, start=1):
                source_rows.append(
                    {
                        "regime": GROUP_LABELS[GROUPS.index(group)],
                        "arm": arm,
                        "world": f"W{world:02d}",
                        "macro_mae": float(value),
                        "mean_across_worlds": mean,
                        "sample_sd_across_worlds": sample_sd,
                        "n_worlds": 5,
                    }
                )
    return values, source_rows


def load_panel_a_data() -> tuple[list[dict[str, object]], float, float, float]:
    process = json.loads((REPORT / "EQ_AUTONOMOUS_PROCESS.json").read_text(encoding="utf-8"))
    study = json.loads((REPORT / "STORY_WORLD_ANALYSIS.json").read_text(encoding="utf-8"))[
        "eq_p_query_regimes"
    ]
    rows = process["rows"]
    if len(rows) != 15 or sum(len(row["batches"]) for row in rows) != 180:
        raise RuntimeError("Figure 5a requires 15 campaigns and 180 retained source assays")

    source_assays = [
        (
            float(batch["nominal_concentration_mol_L"]),
            100.0 * float(batch["final_responses"]["acid_dissociation_fraction"]),
        )
        for row in rows
        for batch in row["batches"]
    ]
    source_low = min(value for _, value in source_assays)
    source_high = max(value for _, value in source_assays)
    source_min_concentration = min(concentration for concentration, _ in source_assays)
    if not (5.4 < source_low < 5.6 and 9.1 < source_high < 9.3):
        raise RuntimeError("Unexpected source-observation range")

    opaque_cells = [cell for cell in study["cells"] if cell["arm"] == "Opaque"]
    if len(opaque_cells) != 5:
        raise RuntimeError("Figure 5a requires one retained reference set for each world")
    by_query: dict[str, list[float]] = {}
    for cell in opaque_cells:
        for group in cell["groups"].values():
            for point in group["points"]:
                if point["metric"] != "acid_dissociation_fraction":
                    continue
                by_query.setdefault(point["query"], []).append(100.0 * float(point["truth_mean"]))
    if len(by_query) != 12 or any(len(values) != 5 for values in by_query.values()):
        raise RuntimeError("Figure 5a requires 12 queries and five world references per query")

    query_rows: list[dict[str, object]] = []
    for query in sorted(by_query):
        values = np.asarray(by_query[query], dtype=float)
        concentration = float(process["query_concentrations"][query])
        for world, value in enumerate(values, start=1):
            query_rows.append(
                {
                    "query": query,
                    "regime": "Dilute three" if query in DILUTE_QUERIES else "Other nine",
                    "nominal_concentration_M": concentration,
                    "world": f"W{world:02d}",
                    "withheld_reference_percent": float(value),
                    "mean_across_worlds_percent": float(np.mean(values)),
                    "sample_sd_across_worlds_percent": float(np.std(values, ddof=1)),
                    "n_worlds": 5,
                    "source_observation_min_percent": source_low,
                    "source_observation_max_percent": source_high,
                    "minimum_source_assay_concentration_M": source_min_concentration,
                }
            )
    return query_rows, source_low, source_high, source_min_concentration


def load_panel_c_data() -> tuple[list[float], dict[str, list[float]], float, float, list[dict[str, object]]]:
    path = REPORT / "EQ_AUTONOMOUS_PROCESS.json"
    rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
    if len(rows) != 15 or sum(len(row["batches"]) for row in rows) != 180:
        raise RuntimeError("Figure 5c requires 15 campaigns and 180 retained source assays")

    source_values = [
        100.0 * float(batch["final_responses"]["acid_dissociation_fraction"])
        for row in rows
        for batch in row["batches"]
    ]
    low, high = min(source_values), max(source_values)
    if not (5.4 < low < 5.6 and 9.1 < high < 9.3):
        raise RuntimeError("Unexpected source-observation range")

    references: list[float] = []
    predictions = {arm: [] for arm in ARMS}
    source_rows: list[dict[str, object]] = []
    for world in range(1, 6):
        world_name = f"W{world:02d}"
        world_rows = [row for row in rows if row["world"] == world_name]
        if len(world_rows) != 3:
            raise RuntimeError(f"Incomplete Figure 5c world: {world_name}")
        reference_values = {
            float(row["q08"]["reference_means"]["acid_dissociation_fraction"])
            for row in world_rows
        }
        if len(reference_values) != 1:
            raise RuntimeError(f"Reference mismatch in {world_name}")
        reference = 100.0 * reference_values.pop()
        references.append(reference)
        source_rows.append(
            {
                "world": world_name,
                "series": "Withheld reference",
                "dissociation_percent": reference,
                "source_observation_min_percent": low,
                "source_observation_max_percent": high,
            }
        )
        for arm in ARMS:
            row = next(item for item in world_rows if item["arm"] == arm)
            value = 100.0 * float(row["q08"]["predictions"]["acid_dissociation_fraction"]["estimate"])
            predictions[arm].append(value)
            source_rows.append(
                {
                    "world": world_name,
                    "series": arm,
                    "dissociation_percent": value,
                    "source_observation_min_percent": low,
                    "source_observation_max_percent": high,
                }
            )
    return references, predictions, low, high, source_rows


def draw_ratio_bracket(ax: plt.Axes, x1: float, x2: float, y: float, text: str) -> None:
    lower = y / 1.27
    ax.plot([x1, x1, x2, x2], [lower, y, y, lower], color=INK, linewidth=0.8, clip_on=False)
    ax.text((x1 + x2) / 2.0, y * 1.17, text, ha="center", va="bottom", fontsize=10.0, color=INK)


def render_panel_a(
    path: Path,
    source_rows: list[dict[str, object]],
    source_low: float,
    source_high: float,
    source_min_concentration: float,
) -> None:
    fig = plt.figure(figsize=(6.5, 4.0), facecolor="white")
    ax = fig.add_axes([0.16, 0.18, 0.81, 0.72])
    style_boxed_axis(ax)

    summaries: list[dict[str, object]] = []
    for query in sorted({str(row["query"]) for row in source_rows}):
        selected = [row for row in source_rows if row["query"] == query]
        summaries.append(
            {
                "query": query,
                "regime": selected[0]["regime"],
                "concentration": float(selected[0]["nominal_concentration_M"]),
                "mean": float(selected[0]["mean_across_worlds_percent"]),
                "sd": float(selected[0]["sample_sd_across_worlds_percent"]),
            }
        )

    # Slight multiplicative offsets separate independent queries sharing a concentration.
    concentrations = sorted({float(row["concentration"]) for row in summaries})
    plotted_x: dict[str, float] = {}
    for concentration in concentrations:
        tied = [row for row in summaries if float(row["concentration"]) == concentration]
        factors = np.power(10.0, np.linspace(-0.035, 0.035, len(tied)))
        for row, factor in zip(tied, factors):
            plotted_x[str(row["query"])] = concentration * float(factor)

    dilute_concentrations = [
        float(row["concentration"]) for row in summaries if row["regime"] == "Dilute three"
    ]
    shade_low = min(dilute_concentrations) / 1.18
    shade_high = max(dilute_concentrations) * 1.18
    ax.axvspan(shade_low, shade_high, color=DILUTE_REGION_COLOR, zorder=0)
    ax.axhspan(source_low, source_high, color=SOURCE_BAND_COLOR, alpha=0.72, zorder=0)
    ax.axvline(shade_low, color=DILUTE_BOUNDARY_COLOR, linewidth=0.75, linestyle=(0, (4, 3)), zorder=1)
    ax.axvline(shade_high, color=DILUTE_BOUNDARY_COLOR, linewidth=0.75, linestyle=(0, (4, 3)), zorder=1)

    for row in summaries:
        is_dilute = row["regime"] == "Dilute three"
        ax.errorbar(
            plotted_x[str(row["query"])],
            float(row["mean"]),
            yerr=float(row["sd"]),
            fmt="D",
            markersize=5.4 if is_dilute else 4.8,
            markerfacecolor=REFERENCE_COLOR,
            markeredgecolor="white",
            markeredgewidth=0.45,
            ecolor=REFERENCE_COLOR,
            elinewidth=0.7,
            capsize=2.0,
            zorder=3,
        )

    ax.annotate(
        "Dilute-three regime",
        xy=(shade_low, 77.0),
        xytext=(shade_high, 77.0),
        ha="center",
        va="center",
        fontsize=9.4,
        color="#31536B",
        arrowprops={"arrowstyle": "<->", "color": DILUTE_BOUNDARY_COLOR, "linewidth": 0.75},
    )
    ax.annotate(
        "No source assay\nentered this regime",
        xy=(shade_high, 66.0),
        xytext=(4.0e-4, 66.0),
        ha="left",
        va="center",
        fontsize=9.1,
        color="#31536B",
        arrowprops={"arrowstyle": "-|>", "color": DILUTE_BOUNDARY_COLOR, "linewidth": 0.75},
    )
    ax.text(
        2.0e-5,
        45.0,
        "Withheld reference means\n(dilute three)",
        ha="left",
        va="center",
        fontsize=9.0,
        color="#363A3D",
    )
    ax.text(
        0.012,
        19.0,
        "Withheld reference means\n(other nine)",
        ha="center",
        va="center",
        fontsize=9.0,
        color="#363A3D",
    )
    ax.text(
        5.0,
        source_high + 2.0,
        f"Source observations\n({source_low:.1f}–{source_high:.1f}%)",
        ha="right",
        va="bottom",
        fontsize=9.0,
        color="#363A3D",
    )

    ax.set_xscale("log")
    ax.set_xlim(8.0e-6, 10.0)
    ax.set_ylim(0.0, 82.0)
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_xlabel("Nominal concentration (M)")
    ax.set_ylabel("Dissociation (%)")
    fig.text(0.015, 0.94, "a", fontsize=17.0, fontweight="bold", color=INK)
    fig.text(0.16, 0.94, "Evidence coverage gap", fontsize=13.8, fontweight="bold", color=INK)
    fig.savefig(path, bbox_inches=None, pad_inches=0)
    plt.close(fig)


def render_panel_b(path: Path, values: dict[tuple[str, str], np.ndarray]) -> None:
    fig = plt.figure(figsize=(6.2, 4.0), facecolor="white")
    # Match panel a's plot-bottom and plot-top coordinates exactly.
    ax = fig.add_axes([0.19, 0.18, 0.775, 0.72])
    style_boxed_axis(ax)

    centers = np.asarray([0.0, 1.0])
    width = 0.18
    offsets = {"Opaque": -0.22, "Aligned": 0.0, "MisIndexed": 0.22}

    for arm in ARMS:
        means = np.asarray([np.mean(values[(group, arm)]) for group in GROUPS], dtype=float)
        sds = np.asarray([np.std(values[(group, arm)], ddof=1) for group in GROUPS], dtype=float)
        lower = means - sds
        if np.any(lower <= 0):
            raise RuntimeError(f"Mean - s.d. must remain positive on the log axis: {arm}")
        bars = ax.bar(
            centers + offsets[arm],
            means,
            width=width,
            color=DISPLAY_COLORS[arm],
            edgecolor="none",
            yerr=sds,
            error_kw={"ecolor": INK, "elinewidth": 0.8, "capsize": 3.0, "capthick": 0.8},
            zorder=2,
        )
        for index, (bar, mean, sd) in enumerate(zip(bars, means, sds)):
            label_y = (mean + sd) * (1.22 if index == 0 else 1.16)
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                label_y,
                f"{mean:.5f}",
                ha="center",
                va="bottom",
                fontsize=9.6,
                color=INK,
                clip_on=False,
            )

    ratios = {
        group: float(np.mean(values[(group, "Aligned")]) / np.mean(values[(group, "Opaque")]))
        for group in GROUPS
    }
    draw_ratio_bracket(
        ax,
        centers[0] + offsets["Opaque"] - width / 2.0,
        centers[0] + offsets["Aligned"] + width / 2.0,
        0.42,
        f"Aligned / Opaque ≈ {ratios['other_nine']:.2f}×",
    )
    draw_ratio_bracket(
        ax,
        centers[1] + offsets["Opaque"] - width / 2.0,
        centers[1] + offsets["Aligned"] + width / 2.0,
        0.42,
        f"Aligned / Opaque ≈ {ratios['three_most_dilute']:.2f}×",
    )

    ax.set_yscale("log")
    ax.set_xlim(-0.48, 1.48)
    ax.set_ylim(1e-3, 1.0)
    ax.set_xticks(centers, GROUP_LABELS)
    ax.set_ylabel("Macro MAE")
    ax.set_yticks([1e-3, 1e-2, 1e-1, 1.0])
    ax.yaxis.set_major_formatter(mpl.ticker.LogFormatterMathtext(base=10))
    fig.text(0.02, 0.94, "b", fontsize=17.0, fontweight="bold", color=INK)
    fig.text(0.19, 0.94, "Error reversal across regimes", fontsize=13.8, fontweight="bold", color=INK)
    fig.legend(
        handles=[
            Patch(facecolor=DISPLAY_COLORS[arm], edgecolor=INK, linewidth=0.5, label=arm)
            for arm in ARMS
        ],
        loc="lower center",
        bbox_to_anchor=(0.58, 0.005),
        ncol=3,
        frameon=False,
        fontsize=11.3,
        handlelength=1.25,
        handleheight=0.72,
        columnspacing=1.8,
        handletextpad=0.55,
    )
    fig.savefig(path, bbox_inches=None, pad_inches=0)
    plt.close(fig)


def render_panel_c(
    path: Path,
    references: list[float],
    predictions: dict[str, list[float]],
    low: float,
    high: float,
) -> None:
    fig = plt.figure(figsize=(13.625, 3.76), facecolor="white")
    # Align the left edge with panel a and the right edge with panel b after
    # composition onto the 981-pt-wide figure canvas.
    ax = fig.add_axes([0.082, 0.25, 0.900, 0.61])
    style_boxed_axis(ax)
    ax.tick_params(axis="x", length=0, pad=8)

    x = np.arange(5, dtype=float)
    width = 0.17
    groups = [
        ("Withheld reference", references, REFERENCE_COLOR),
        ("Opaque", predictions["Opaque"], DISPLAY_COLORS["Opaque"]),
        ("Aligned", predictions["Aligned"], DISPLAY_COLORS["Aligned"]),
        ("MisIndexed", predictions["MisIndexed"], DISPLAY_COLORS["MisIndexed"]),
    ]
    offsets = np.asarray([-1.5, -0.5, 0.5, 1.5]) * (width + 0.012)

    ax.axhspan(low, high, color=SOURCE_BAND_COLOR, alpha=0.72, zorder=0)
    for offset, (_, values, color) in zip(offsets, groups):
        bars = ax.bar(
            x + offset,
            values,
            width=width,
            color=color,
            edgecolor="white",
            linewidth=0.45,
            zorder=2,
        )
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                value + 1.35,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=10.8,
                color=INK,
                clip_on=False,
            )

    ax.set_xlim(-0.53, 4.70)
    ax.set_ylim(0.0, 87.0)
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_xticks(x, [f"World {world}" for world in range(1, 6)])
    ax.set_ylabel("Dissociation (%)")
    fig.text(0.008, 0.93, "c", fontsize=17.0, fontweight="bold", color=INK)
    fig.text(
        0.085,
        0.93,
        "Original forecasts at the most dilute condition",
        ha="left",
        va="top",
        fontsize=13.8,
        fontweight="bold",
        color=INK,
    )
    fig.text(0.985, 0.93, "13.3 µM", ha="right", va="top", fontsize=11.8, color=INK)
    ax.annotate(
        f"Source assay range\n({low:.1f}–{high:.1f}%)",
        xy=(4.57, high),
        xytext=(4.57, 18.0),
        ha="right",
        va="bottom",
        fontsize=9.0,
        color="#31536B",
        arrowprops={"arrowstyle": "-|>", "color": "#70828E", "linewidth": 0.75},
    )
    fig.legend(
        handles=[
            Patch(facecolor=REFERENCE_COLOR, edgecolor=INK, linewidth=0.5, label="Withheld reference"),
            *[
                Patch(facecolor=DISPLAY_COLORS[arm], edgecolor=INK, linewidth=0.5, label=arm)
                for arm in ARMS
            ],
        ],
        loc="lower center",
        bbox_to_anchor=(0.53, 0.005),
        ncol=4,
        frameon=False,
        fontsize=11.3,
        handlelength=1.25,
        handleheight=0.72,
        columnspacing=1.9,
        handletextpad=0.55,
    )
    fig.savefig(path, bbox_inches=None, pad_inches=0)
    plt.close(fig)


def compose_candidate(
    panel_a_pdf: Path,
    panel_b_pdf: Path,
    panel_c_pdf: Path,
) -> None:
    base = pymupdf.open()
    page = base.new_page(width=981.0, height=585.75)
    panel_a = pymupdf.open(panel_a_pdf)
    panel = pymupdf.open(panel_b_pdf)
    panel_c = pymupdf.open(panel_c_pdf)
    if (
        panel_a.page_count != 1
        or panel.page_count != 1
        or panel_c.page_count != 1
    ):
        raise RuntimeError("Figure 5 composition requires one-page PDFs")

    # Coordinates are in points in the current 981 x 585.75 pt manuscript asset.
    # These rectangles replace panels a and b but stop above the shared legend.
    target_a = pymupdf.Rect(0.0, 0.0, 500.0, 315.0)
    page.draw_rect(target_a, color=None, fill=(1.0, 1.0, 1.0), overlay=True)
    page.show_pdf_page(target_a, panel_a, 0, keep_proportion=False, overlay=True)

    target = pymupdf.Rect(505.0, 0.0, 981.0, 315.0)
    page.draw_rect(target, color=None, fill=(1.0, 1.0, 1.0), overlay=True)
    page.show_pdf_page(target, panel, 0, keep_proportion=False, overlay=True)

    # Panel c carries its own four-item legend, matching the panel-specific
    # legend strategy used in the visual reference.
    target_c = pymupdf.Rect(0.0, 315.0, 981.0, 585.75)
    page.draw_rect(target_c, color=None, fill=(1.0, 1.0, 1.0), overlay=True)
    page.show_pdf_page(target_c, panel_c, 0, keep_proportion=False, overlay=True)

    OUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    pdf_path = OUT_STEM.with_suffix(".pdf")
    base.set_metadata(
        {
            "title": "ChemWorld Figure 5 candidate",
            "subject": "Evidence coverage, regime reversal and retained forecasts",
            "producer": "Matplotlib and PyMuPDF",
        }
    )
    base.save(pdf_path, garbage=4, deflate=True)
    base.close()
    panel_a.close()
    panel.close()
    panel_c.close()

    rendered = pymupdf.open(pdf_path)
    svg_path = OUT_STEM.with_suffix(".svg")
    svg_path.write_text(rendered[0].get_svg_image(text_as_path=0), encoding="utf-8")

    raster_dpi = 600
    raster_scale = raster_dpi / 72.0
    pixmap = rendered[0].get_pixmap(matrix=pymupdf.Matrix(raster_scale, raster_scale), alpha=False)
    png_path = OUT_STEM.with_suffix(".png")
    pixmap.save(png_path)
    rendered.close()

    with Image.open(png_path) as image:
        image.save(
            OUT_STEM.with_suffix(".tiff"),
            compression="tiff_lzw",
            dpi=(raster_dpi, raster_dpi),
        )


def write_source_csv(rows: list[dict[str, object]]) -> None:
    with SOURCE_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_panel_c_source_csv(rows: list[dict[str, object]]) -> None:
    with PANEL_C_SOURCE_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_panel_a_source_csv(rows: list[dict[str, object]]) -> None:
    with PANEL_A_SOURCE_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    configure_matplotlib()
    panel_a_source_rows, source_low, source_high, source_min_concentration = load_panel_a_data()
    values, source_rows = load_panel_b_data()
    references, predictions, low, high, panel_c_source_rows = load_panel_c_data()
    OUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chemworld-figure05b-") as temp_dir:
        panel_a_pdf = Path(temp_dir) / "panel-a.pdf"
        panel_b_pdf = Path(temp_dir) / "panel-b.pdf"
        panel_c_pdf = Path(temp_dir) / "panel-c.pdf"
        render_panel_a(
            panel_a_pdf,
            panel_a_source_rows,
            source_low,
            source_high,
            source_min_concentration,
        )
        render_panel_b(panel_b_pdf, values)
        render_panel_c(panel_c_pdf, references, predictions, low, high)
        compose_candidate(panel_a_pdf, panel_b_pdf, panel_c_pdf)
    write_panel_a_source_csv(panel_a_source_rows)
    write_source_csv(source_rows)
    write_panel_c_source_csv(panel_c_source_rows)
    print(OUT_STEM.with_suffix(".pdf"))
    print(OUT_STEM.with_suffix(".svg"))
    print(OUT_STEM.with_suffix(".png"))
    print(OUT_STEM.with_suffix(".tiff"))
    print(PANEL_A_SOURCE_CSV)
    print(SOURCE_CSV)
    print(PANEL_C_SOURCE_CSV)
    print("Panel b: bars are means; error bars are sample s.d. across five worlds (n=5).")


if __name__ == "__main__":
    main()
