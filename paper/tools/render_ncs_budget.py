"""Readable paired budget changes from retained data; no new experiments."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ARMS = ("Opaque", "Aligned", "MisIndexed")
INK, GOOD, BAD = "#243542", "#397a75", "#a26651"
DEFINITIONS = [
    ("EC", "discovery", "score", "mae", "a  EC\nDiscovery", "Score MAE", 1, -1),
    ("EC", "optimization", "score", "mae", "b  EC\nOptimization", "Score MAE", 1, -1),
    (
        "PA",
        "discovery",
        "product_in_organic",
        "mae",
        "c  Partitioning",
        "Organic-fraction\nMAE",
        1,
        -1,
    ),
    (
        "C",
        "delivery",
        "crystal_yield",
        "mae",
        "d  Crystallization\nRecovery prediction",
        "Recovery MAE",
        1,
        -1,
    ),
    (
        "C",
        "delivery",
        "crystal_fines_fraction",
        "coverage",
        "e  Crystallization\nInterval coverage",
        "Fines coverage (%)",
        100,
        1,
    ),
    (
        "C",
        "delivery",
        "crystal_yield",
        "retest",
        "f  Crystallization\nOperating delivery",
        "Retested recovery",
        1,
        1,
    ),
]


def prepare(rows):
    panels = []
    for system, goal, metric, field, title, label, scale, direction in DEFINITIONS:
        paired = {}
        for r in rows:
            if (r["system"], r["goal"], r["metric"]) == (system, goal, metric):
                key = (r["world"], r["arm"])
                assert r["budget"] not in paired.setdefault(key, {})
                paired[key][r["budget"]] = r
        assert len(paired) == 15 and all(set(v) == {12, 24} for v in paired.values())
        ordered = sorted(paired, key=lambda k: (k[0], ARMS.index(k[1])))
        pairs = []
        for world, arm in ordered:
            p = paired[world, arm]
            x, y = (p[b][field] * scale for b in (12, 24))
            pairs.append(
                {
                    "system": system,
                    "goal": goal,
                    "metric": metric,
                    "field": field,
                    "world": world,
                    "arm": arm,
                    "value12": x,
                    "value24": y,
                    "favorable_change": direction * (y - x),
                    "conforming12": p[12]["conforming"],
                    "conforming24": p[24]["conforming"],
                    "source12": p[12]["id"],
                    "source24": p[24]["id"],
                }
            )
        if field == "coverage":
            assert all(p["value12"] < 80 and p["value24"] < 80 for p in pairs)
        improvements = sum(p["favorable_change"] > 1e-12 for p in pairs)
        worsens = sum(p["favorable_change"] < -1e-12 for p in pairs)
        panels.append(
            {
                "pairs": pairs,
                "title": title,
                "label": label,
                "scale": scale,
                "field": field,
                "direction": direction,
                "mean12": fmean(p["value12"] for p in pairs),
                "mean24": fmean(p["value24"] for p in pairs),
                "improvements": improvements,
                "worsens": worsens,
                "ties": 15 - improvements - worsens,
            }
        )
    assert [p["improvements"] for p in panels[:3]] == [11, 12, 13]
    return panels


def render_budget_figure(rows, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    panels = prepare(rows)
    plt.rcParams.update({"font.family": "Arial", "pdf.fonttype": 42, "svg.fonttype": "none"})
    fig = plt.figure(figsize=(7.35, 5.65), facecolor="white")
    left, right, gap = 0.112, 0.985, 0.023
    width = (right - left - 5 * gap) / 6
    data_bottom, data_height = 0.178, 0.473
    ys = np.array([w * 3.7 + a for w in range(5) for a in range(3)])
    mean_y = ys[-1] + 1.8
    data_min, data_max = -0.7, mean_y + 0.7
    axes = []
    export = []
    stats = []
    for i, panel in enumerate(panels):
        x0 = left + i * (width + gap)
        center = x0 + width / 2
        pairs = panel["pairs"]
        changes = [p["favorable_change"] for p in pairs]
        max_change = max(abs(x) for x in changes)
        step = 25 if panel["field"] == "coverage" else (0.2 if max_change > 0.3 else 0.1)
        limit = 0.3 if i < 2 else np.ceil(max_change / step) * step
        ax = fig.add_axes((x0, data_bottom, width, data_height))
        axes.append(ax)
        ax.set(xlim=(-limit * 1.14, limit * 1.14), ylim=(data_max, data_min))
        for w in range(5):
            if w % 2 == 0:
                ax.axhspan(w * 3.7 - 0.45, w * 3.7 + 2.45, color="#f2f5f6", lw=0, zorder=0)
        ax.axvline(0, color="#8e9ca5", lw=0.6, zorder=1)
        for y, p, delta in zip(ys, pairs, changes, strict=True):
            color = GOOD if delta > 1e-12 else BAD if delta < -1e-12 else "#75828a"
            ax.hlines(y, 0, delta, color=color, lw=1.35, zorder=2)
            shortfall = not (p["conforming12"] and p["conforming24"])
            ax.scatter(
                delta,
                y,
                s=13 if shortfall else 9,
                marker="x" if shortfall else "o",
                color=color,
                linewidths=0.85,
                zorder=3,
            )
            export.append({"panel": "abcdef"[i], **p})
        mean_change = fmean(changes)
        ax.axhline(mean_y - 0.85, color="#ccd4d9", lw=0.5)
        ax.hlines(mean_y, 0, mean_change, color=INK, lw=1.4, zorder=4)
        ax.scatter(mean_change, mean_y, s=22, marker="D", color=INK, zorder=5)
        ticks = [-limit, 0, limit]
        fmt = (
            (lambda v: f"{v:+.0f}" if v else "0")
            if panel["field"] == "coverage"
            else (lambda v: f"{v:+.1f}" if v else "0")
        )
        ax.set_xticks(ticks, [fmt(t) for t in ticks])
        ax.tick_params(axis="x", labelsize=6.6, length=2.5, pad=3, width=0.55)
        ax.set_yticks([])
        for s in ("top", "left", "right"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set(color="#8e9ca5", linewidth=0.55)
        label = (
            "MAE reduction"
            if panel["direction"] == -1
            else "Coverage gain\n(percentage points)"
            if panel["field"] == "coverage"
            else "Recovery gain"
        )
        ax.set_xlabel(label, fontsize=6.8, labelpad=6, color=INK)
        fig.text(
            center,
            0.969,
            panel["title"],
            ha="center",
            va="top",
            fontsize=7.7,
            weight="bold",
            color=INK,
            linespacing=1.5,
        )
        fig.text(
            center,
            0.883,
            panel["label"],
            ha="center",
            va="top",
            fontsize=6.8,
            color="#576976",
            linespacing=1.3,
        )
        value_fmt = (
            (lambda v: f"{v:.1f}%") if panel["field"] == "coverage" else (lambda v: f"{v:.4f}")
        )
        fig.text(
            center,
            0.816,
            value_fmt(panel["mean12"]),
            ha="center",
            va="center",
            fontsize=8.3,
            color=INK,
        )
        fig.text(
            center,
            0.778,
            value_fmt(panel["mean24"]),
            ha="center",
            va="center",
            fontsize=8.3,
            color=INK,
        )
        fig.text(
            center,
            0.733,
            f"{panel['improvements']} / 15",
            ha="center",
            va="center",
            fontsize=8.2,
            weight="bold",
            color=INK,
        )
        fig.add_artist(
            Line2D(
                [x0, x0 + width], [0.700, 0.700], transform=fig.transFigure, color="#b9c4ca", lw=0.6
            )
        )
        stats.append(
            {
                "pairs": 15,
                "mean12": panel["mean12"],
                "mean24": panel["mean24"],
                "decreases": sum(p["value24"] < p["value12"] for p in pairs),
                "improves": panel["improvements"],
                "worsens": panel["worsens"],
                "ties": panel["ties"],
                "mean_favorable_change": mean_change,
                "display_change": "value12 - value24"
                if panel["direction"] == -1
                else "value24 - value12",
            }
        )
    for y, text in ((0.816, "Mean, 12"), (0.778, "Mean, 24"), (0.733, "Improved")):
        fig.text(left - 0.014, y, text, ha="right", va="center", fontsize=7, color=INK)
    # One aligned row key replaces ninety crossing lines and six repeated legends.
    first = axes[0]
    row_transform = first.get_yaxis_transform()
    for w in range(5):
        first.text(
            -0.48,
            w * 3.7 + 1,
            f"W{w + 1}",
            transform=row_transform,
            ha="right",
            va="center",
            fontsize=7,
            weight="bold",
            color=INK,
            clip_on=False,
        )
        for a, abbr in enumerate(("O", "A", "M")):
            first.text(
                -0.12,
                w * 3.7 + a,
                abbr,
                transform=row_transform,
                ha="right",
                va="center",
                fontsize=7,
                color="#526370",
                clip_on=False,
            )
    first.text(
        -0.12,
        mean_y,
        "Mean",
        transform=row_transform,
        ha="right",
        va="center",
        fontsize=7,
        weight="bold",
        color=INK,
        clip_on=False,
    )
    fig.text(
        left,
        0.675,
        "Paired change: left = worse; right = better",
        fontsize=7.4,
        weight="bold",
        color=INK,
        va="center",
    )
    fig.legend(
        handles=[
            Line2D([], [], color=GOOD, marker="o", ms=3, lw=1.1, label="Improved"),
            Line2D([], [], color=BAD, marker="o", ms=3, lw=1.1, label="Worsened"),
            Line2D([], [], color="#75828a", marker="o", ms=3, lw=0, label="Unchanged"),
            Line2D([], [], color=INK, marker="D", ms=4, lw=0, label="Mean change"),
            Line2D([], [], color=INK, marker="x", ms=4, lw=0, label="Source shortfall"),
        ],
        loc="lower center",
        bbox_to_anchor=(0.55, 0.053),
        ncol=5,
        frameon=False,
        fontsize=6.7,
        handlelength=1.3,
        columnspacing=1.25,
    )
    fig.text(
        0.014,
        0.038,
        "O: Opaque   A: Aligned   M: MisIndexed. Each column contains 15 matched pairs; "
        "world labels are system-specific.",
        fontsize=6.25,
        color="#526370",
    )
    fig.text(
        0.014,
        0.013,
        "Independent sessions; 24 batches also allow more operations and computation. "
        "All C coverage values remain below the nominal 80%.",
        fontsize=6.1,
        color="#526370",
    )
    stem = "figure03-research-envelope"
    for ext in ("pdf", "svg", "png"):
        fig.savefig(
            out / f"{stem}.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.08, facecolor="white"
        )
    plt.close(fig)
    with (out / f"{stem}-pairs.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(export[0]))
        writer.writeheader()
        writer.writerows(export)
    assert len(export) == 90
    (out / f"{stem}-design.json").write_text(
        json.dumps(
            {
                "design": "paired favorable changes by world and arm",
                "new_experiments": 0,
                "panels": stats,
                "plotted_paired_comparisons": 90,
                "unique_source_campaigns": len(
                    {r[k] for r in export for k in ("source12", "source24")}
                ),
                "note": "C panels reuse the same thirty campaigns; "
                "90 comparisons are not independent.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        "Budget figure: 6/6 panels, 90/90 paired comparisons; "
        f"improved counts {[s['improves'] for s in stats]}",
        flush=True,
    )
    return stats


def main():
    from render_ncs_full_figures import OUT, load_metrics, read

    stats = render_budget_figure(load_metrics(), OUT)
    path = OUT / "figure-data-summary.json"
    summary = read(path)
    old = summary["figures"]["03-budgets"]
    for a, b in zip(old, stats, strict=True):
        for key in ("pairs", "mean12", "mean24", "decreases"):
            assert np.isclose(a[key], b[key], atol=1e-12, rtol=0), (key, a[key], b[key])
    summary["figures"]["03-budgets"] = stats
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
