"""Build the Chinese full-paper figures from retained public analysis tables.

No model or simulator calls. Run with uv run --no-sync python.
"""

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
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "paper/figures/ncs-full"
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
ARMS = ("Opaque", "Aligned", "MisIndexed")
COLORS = dict(zip(ARMS, ("#536e86", "#148b8f", "#c4754c"), strict=True))
BLUE, TEAL, RUST, INK = "#2864cc", "#098e98", "#bf593e", "#17293a"
SUMMARY: dict = {"new_experiments": 0, "figures": {}}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def style():
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "axes.labelcolor": INK,
            "text.color": INK,
            "axes.edgecolor": "#7e8d9a",
            "axes.linewidth": 0.7,
            "xtick.color": "#465563",
            "ytick.color": "#465563",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": "#d9e1e7",
            "grid.linewidth": 0.5,
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
            "legend.frameon": False,
            "legend.fontsize": 9,
        }
    )


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=240, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"figures stage=render completed={len(SUMMARY['figures'])}/5 output={name}", flush=True)


def clean(ax):
    ax.grid(axis="y", alpha=0.7)
    ax.set_axisbelow(True)


def legend_arms(fig, extra=()):
    handles = [Line2D([], [], marker="o", ls="", color=COLORS[a], label=a) for a in ARMS]
    fig.legend(
        handles=[*handles, *extra], loc="outside lower center", ncol=len(handles) + len(extra)
    )


def load_metrics():
    with (ROOT / "paper/figures/integrated-results/campaign_metrics.csv").open(
        encoding="utf-8"
    ) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["budget"] = int(r["budget"])
        for k in ("mae", "coverage", "width", "retest", "retest_purity"):
            r[k] = float(r[k]) if r[k] else None
        r["conforming"] = r["conforming"] == "True"
        r["quality_pass"] = r["quality_pass"] in ("True", "1") if r["quality_pass"] else None
    assert len({r["id"] for r in rows}) == 240
    return rows


def operation_figure(rows):
    analysis = read(ROOT / "paper/figures/integrated-results/analysis.json")
    fig, axs = plt.subplots(
        1, 3, figsize=(11.2, 4.4), layout="constrained", gridspec_kw={"width_ratios": [1, 1, 0.88]}
    )
    for j, system in enumerate(("EC", "RX")):
        ax = axs[j]
        points = analysis["goal_contrasts"][system]
        xs = [r["delta_retest"] for r in points]
        ys = [r["delta_mae"] for r in points]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        dx, dy = (xmax - xmin) * 0.14, (ymax - ymin) * 0.17
        ax.set_xlim(xmin - dx, xmax + dx)
        ax.set_ylim(ymin - dy, ymax + dy)
        ax.add_patch(Rectangle((0, 0), xmax + dx, ymax + dy, color="#fbefe8", zorder=0))
        ax.axhline(0, color="#82909a", lw=0.8)
        ax.axvline(0, color="#82909a", lw=0.8)
        for r in points:
            ax.scatter(
                r["delta_retest"],
                r["delta_mae"],
                color=COLORS[r["arm"]],
                s=38,
                edgecolor="white",
                linewidth=0.5,
                zorder=3,
            )
        count = sum(r["delta_retest"] > 0 and r["delta_mae"] > 0 for r in points)
        assert count == (13 if system == "EC" else 5)
        ax.set_title(
            f"{chr(97 + j)}  {'Electrochemistry' if system == 'EC' else 'Reaction processing'}",
            loc="left",
        )
        ax.set_xlabel("Change in recommendation score\nOptimization - discovery")
        ax.set_ylabel("Change in score-prediction MAE")
        ax.text(
            0.98,
            0.96,
            f"Better delivery,\nworse prediction\n{count}/30 pairs",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            color=RUST,
        )
        counts = analysis["goal_counts"][system]
        ax.text(
            0.03,
            0.04,
            f"Delivery improves: {counts['better_retest']}/30\n"
            f"Prediction improves: {counts['lower_mae']}/30",
            transform=ax.transAxes,
            fontsize=9,
            bbox={"facecolor": "white", "alpha": 0.88, "edgecolor": "none", "pad": 2},
        )
    ax = axs[2]
    p = [r for r in rows if r["system"] == "P" and r["metric"] == "recovery"]
    assert len(p) == 15
    ax.axhspan(0.8, 1.02, color="#eaf5f3", zorder=0)
    ax.axhline(0.8, color=TEAL, ls="--", lw=0.9)
    for r in p:
        ax.scatter(
            r["retest"],
            r["retest_purity"],
            s=44,
            color=COLORS[r["arm"]],
            edgecolor="white",
            linewidth=0.5,
            zorder=3,
        )
    ax.set(
        xlim=(-0.02, max(r["retest"] for r in p) + 0.06),
        ylim=(0, 1.03),
        xlabel="Original-charge recovery",
        ylabel="Retested purity",
    )
    ax.set_title("c  Purification constraints", loc="left")
    ax.text(0.02, 0.97, "Purity requirement ≥0.80", transform=ax.transAxes, fontsize=8.7, va="top")
    ax.text(
        0.04,
        0.08,
        "Recommendations meeting purity\nOpaque: 0/5  |  Aligned: 3/5\nMisIndexed: 0/5",
        transform=ax.transAxes,
        fontsize=8.6,
        bbox={"facecolor": "white", "alpha": 0.86, "edgecolor": "none", "pad": 2},
    )
    legend_arms(fig)
    SUMMARY["figures"]["02-operation"] = analysis["goal_counts"]
    save(fig, "figure02-operation-prediction")


def budget_figure(rows):
    from render_ncs_budget import render_budget_figure

    SUMMARY["figures"]["03-budgets"] = render_budget_figure(rows, OUT)


def prior_figure():
    study = read(REPORTS / "work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json")
    eq = study["eq_p_query_regimes"]
    aggregate, cells = eq["aggregate"], eq["cells"]
    fig, axs = plt.subplots(2, 2, figsize=(10.5, 7.3), layout="constrained")
    for i, (group, title) in enumerate(
        (
            ("other_nine", "a  Equilibrium · other nine queries"),
            ("three_most_dilute", "b  Equilibrium · dilute three queries"),
        )
    ):
        ax = axs[0, i]
        for j, arm in enumerate(ARMS):
            vals = [c["groups"][group]["mae"] for c in cells if c["arm"] == arm]
            mean = next(r["mae"] for r in aggregate if r["arm"] == arm and r["group"] == group)
            ax.bar(j, mean, width=0.58, color=COLORS[arm], alpha=0.72, zorder=2)
            ax.scatter(
                j + np.linspace(-0.14, 0.14, 5),
                vals,
                color="white",
                edgecolor=COLORS[arm],
                s=29,
                zorder=3,
            )
            ax.annotate(
                f"Mean {mean:.5f}",
                (j, max(vals)),
                xytext=(0, 7),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                weight="bold",
            )
        ax.set_xticks(range(3), ARMS)
        ax.set_ylabel("Macro mean absolute error")
        ax.set_title(title, loc="left")
        ax.set_ylim(0, max(c["groups"][group]["mae"] for c in cells) * 1.23)
        clean(ax)
    ax = axs[1, 0]
    for i, arm in enumerate(ARMS):
        x = np.array([0, 1]) + (i - 1) * 0.22
        vals = [
            next(r["coverage"] * 100 for r in aggregate if r["arm"] == arm and r["group"] == g)
            for g in ("other_nine", "three_most_dilute")
        ]
        ax.bar(x, vals, width=0.20, color=COLORS[arm], alpha=0.75)
        for j, g in enumerate(("other_nine", "three_most_dilute")):
            points = [c["groups"][g]["coverage"] * 100 for c in cells if c["arm"] == arm]
            ax.scatter(
                x[j] + np.linspace(-0.055, 0.055, 5),
                points,
                s=15,
                facecolor="white",
                edgecolor=COLORS[arm],
                zorder=3,
            )
    ax.axhline(80, color=RUST, ls="--", lw=1)
    ax.set(ylim=(0, 109), ylabel="Interval coverage (%)")
    ax.set_xticks([0, 1], ["Other nine", "Dilute three"])
    ax.set_title("c  Uncertainty fails in the dilute regime", loc="left")
    ax.text(0.99, 0.74, "Nominal 80%", transform=ax.transAxes, ha="right", fontsize=8, color=RUST)
    clean(ax)
    with (ROOT / "paper/figures/venue-results/c_response_pairs.csv").open(encoding="utf-8") as f:
        pairs = list(csv.DictReader(f))
    ax = axs[1, 1]
    for r in pairs:
        ax.scatter(
            float(r["recovery_delta"]),
            float(r["purity_delta"]),
            color=COLORS[r["arm"]],
            marker="o" if r["both_conforming"] == "True" else "x",
            s=50,
            zorder=3,
        )
    ax.axhline(0, color="#82909a", lw=0.8)
    ax.axvline(0, color="#82909a", lw=0.8)
    ax.set_xlabel("Recovery MAE change vs Opaque\nNegative: better")
    ax.set_ylabel("Purity MAE change vs Opaque\nPositive: worse")
    ax.set_title("d  Crystallization · 12 batches", loc="left")
    ax.text(
        0.03,
        0.06,
        "Both dossiers: 5/5 worlds\nbetter recovery, worse purity",
        transform=ax.transAxes,
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.88, "edgecolor": "none"},
    )
    ax.margins(0.17)
    legend_arms(
        fig, [Line2D([], [], marker="x", color="#555", ls="", label="Source-shortfall pair")]
    )
    SUMMARY["figures"]["05-priors"] = {
        "equilibrium_aggregate": aggregate,
        "crystal_pairs": len(pairs),
    }
    save(fig, "figure05-prior-regimes")


def preserve_figure():
    data = read(REPORTS / "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json")["rows"]
    fig = plt.figure(figsize=(10.6, 8.0), layout="constrained")
    grid = fig.add_gridspec(2, 4, height_ratios=[1, 1.0])
    wins = {}
    for i, (metric, label) in enumerate(
        (
            ("crystal_yield", "Recovery"),
            ("crystal_purity", "Purity"),
            ("crystal_size", "Size index"),
            ("crystal_fines_fraction", "Fines"),
        )
    ):
        ax = fig.add_subplot(grid[0, i])
        lim = (
            max(
                max(r["agent_mae"][metric], r["public_baselines"]["mae"]["public_mean"][metric])
                for r in data
            )
            * 1.13
        )
        ax.plot([0, lim], [0, lim], ls="--", color="#8c99a3", lw=0.8)
        count = 0
        for r in data:
            x, y = r["public_baselines"]["mae"]["public_mean"][metric], r["agent_mae"][metric]
            count += y < x
            marker = ("o" if r["budget"] == 12 else "^") if r["conforming"] else "x"
            ax.scatter(x, y, s=29, color=COLORS[r["arm"]], marker=marker, alpha=0.9)
        wins[metric] = count
        ax.set(xlim=(0, lim), ylim=(0, lim), xlabel="Observed-mean MAE", ylabel="Agent MAE")
        ax.set_title(f"{chr(97 + i)}  {label}\nAgent better: {count}/30", loc="left", fontsize=10)
        ax.tick_params(labelsize=8)
    assert wins["crystal_yield"] == 26 and wins["crystal_purity"] == 0 and wins["crystal_size"] == 4
    ax = fig.add_subplot(grid[1, :2])
    pure = [r["response_diagnostics"]["crystal_purity"] for r in data]
    groups = [
        [r["source_observed_mean"] for r in pure],
        [r["reference_mean"] for r in pure],
        [
            r["response_diagnostics"]["crystal_purity"]["prediction_mean"]
            for r in data
            if r["budget"] == 12
        ],
        [
            r["response_diagnostics"]["crystal_purity"]["prediction_mean"]
            for r in data
            if r["budget"] == 24
        ],
    ]
    colors = ["#8b99a4", "#485e6e", BLUE, TEAL]
    for i, (values, color) in enumerate(zip(groups, colors, strict=True)):
        ax.scatter(i + np.linspace(-0.15, 0.15, len(values)), values, s=20, color=color, alpha=0.45)
        mean = fmean(values)
        ax.plot([i - 0.22, i + 0.22], [mean, mean], color=color, lw=3)
        ax.annotate(
            f"{mean:.4f}",
            (i, mean),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            weight="bold",
        )
    under = sum(r["underestimated_queries"] for r in pure)
    assert under == 335
    ax.set_title("e  Purity forecasts depart from stability", loc="left")
    ax.set_xticks(
        range(4),
        [
            "Source\nobserved",
            "Withheld\nreference",
            "Predicted\n12 batches",
            "Predicted\n24 batches",
        ],
    )
    ax.set(ylim=(0.84, 1.017), ylabel="Mean purity within each campaign")
    clean(ax)
    ax.text(
        0.02,
        0.06,
        f"{under}/360 point forecasts are below reference",
        transform=ax.transAxes,
        fontsize=9,
    )
    ax = fig.add_subplot(grid[1, 2:])
    ax.set_axis_off()
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.set_title("f  Which relationship should change?", loc="left")
    x0, w, h, y0 = 0.31, 0.33, 0.31, 0.18
    texts = [
        ["Appropriate\npreservation", "Unnecessary change\nCrystallization purity"],
        ["Unwarranted extension\nDilute equilibrium", "Appropriate\nchange"],
    ]
    for row in range(2):
        for col in range(2):
            y = y0 + (1 - row) * h
            ax.add_patch(
                Rectangle(
                    (x0 + col * w, y),
                    w - 0.012,
                    h - 0.012,
                    color="#edf5f3" if row == col else "#f8ede7",
                )
            )
            ax.text(
                x0 + col * w + (w - 0.012) / 2,
                y + (h - 0.012) / 2,
                texts[row][col],
                ha="center",
                va="center",
                fontsize=8.8,
            )
    ax.text(x0 + w / 2, 0.85, "Forecast preserves", ha="center", fontsize=9)
    ax.text(x0 + w * 1.5, 0.85, "Forecast changes", ha="center", fontsize=9)
    ax.text(0.28, y0 + 1.5 * h, "Reference stays\nnear source", ha="right", va="center", fontsize=9)
    ax.text(
        0.28, y0 + 0.5 * h, "Reference leaves\nsource regime", ha="right", va="center", fontsize=9
    )
    ax.text(0.61, 0.08, "Conceptual synthesis; no quadrant frequencies", ha="center", fontsize=8.2)
    legend_arms(
        fig,
        [
            Line2D([], [], marker="o", color="#555", ls="", label="12 batches"),
            Line2D([], [], marker="^", color="#555", ls="", label="24 batches"),
            Line2D([], [], marker="x", color="#555", ls="", label="Source shortfall"),
        ],
    )
    SUMMARY["figures"]["06-preserve-revise"] = {
        "agent_beats_source_mean": wins,
        "purity_means": [fmean(g) for g in groups],
        "underestimated_purity": under,
        "queries": 360,
    }
    save(fig, "figure06-preserve-revise")


def infrastructure_figure():
    fig, ax = plt.subplots(figsize=(10.5, 6.9), layout="constrained")
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.set_axis_off()
    layers = [
        (
            "a  Physical causal world",
            "Typed state · process laws · instruments · private parameters",
        ),
        (
            "b  Experimental interaction runtime",
            "Validate · commit or reject · measure · account · replay",
        ),
        (
            "c  Task and evaluation contract",
            "Public goal · legal operations · budget · termination · metrics",
        ),
    ]
    for i, (title, desc) in enumerate(layers):
        y = 0.87 - i * 0.14
        ax.add_patch(Rectangle((0.03, y - 0.065), 0.72, 0.115, fill=False, ec="#a7bac8", lw=0.8))
        ax.text(0.05, y + 0.005, title, weight="bold", fontsize=13, va="center")
        ax.text(0.05, y - 0.03, desc, fontsize=10, va="center")
    ax.add_patch(Rectangle((0.79, 0.57), 0.19, 0.33, fill=False, ec=TEAL, lw=1))
    ax.text(
        0.885, 0.805, "External\nresearcher", ha="center", va="center", weight="bold", fontsize=13
    )
    ax.text(
        0.885,
        0.67,
        "LLM agent\nClassical optimizer\nHuman researcher",
        ha="center",
        va="center",
        fontsize=10,
    )
    ax.annotate("", (0.79, 0.72), (0.75, 0.72), arrowprops={"arrowstyle": "<->", "color": TEAL})
    ax.text(0.03, 0.46, "d  Frozen platform qualification", fontsize=13, weight="bold")
    cards = [
        ("64", "Task-world units"),
        ("1,786", "Boundary / categorical recipes"),
        ("192", "Invalid-action probes"),
        ("52", "Generated compositions"),
    ]
    for i, (num, label) in enumerate(cards):
        x = 0.03 + i * 0.244
        ax.plot([x, x + 0.22], [0.40, 0.40], color=TEAL, lw=1)
        ax.text(x + 0.11, 0.34, num, fontsize=26, weight="bold", ha="center", color=TEAL)
        ax.text(x + 0.11, 0.285, label, fontsize=9, ha="center")
    ax.text(
        0.03,
        0.20,
        "Generated cases: 18 new topologies + 8 new identities + 26 coverage cases",
        fontsize=11,
    )
    ax.text(
        0.03,
        0.14,
        "Additional checks: 32 module probes · 7 valid interfaces · 7 invalid compositions",
        fontsize=11,
    )
    ax.text(
        0.03,
        0.055,
        "Finite-domain execution consistency; separate from 240 autonomous campaigns "
        "and wet-lab validity.",
        fontsize=10,
    )
    SUMMARY["figures"]["S1-infrastructure"] = {
        "task_world_units": 64,
        "recipes": 1786,
        "invalid_probes": 192,
        "generated": 52,
        "generated_subgroups": [18, 8, 26],
        "module_probes": 32,
        "valid_interfaces": 7,
        "invalid_compositions": 7,
    }
    save(fig, "figureS1-infrastructure")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    rows = load_metrics()
    operation_figure(rows)
    budget_figure(rows)
    prior_figure()
    preserve_figure()
    infrastructure_figure()
    (OUT / "figure-data-summary.json").write_text(
        json.dumps(SUMMARY, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
