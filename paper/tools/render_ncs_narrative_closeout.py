"""Draw the two retained-data figures for the final Chinese author manuscript."""

# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from collect_current_figure_vectors import collect
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from ncs_figure_style import ARM_COLORS
from render_figure05_bar_b_overlay_candidate import (
    ARMS,
    GROUPS,
    REPORT,
    load_panel_a_data,
    load_panel_b_data,
)
from render_figure05_readable import configure

ROOT = Path(__file__).resolve().parents[2]
ASTRA = ROOT / "workstreams/flagship_tasks/reports/eq-astra-medium-20260927"
PREVIOUS = ROOT / "workstreams/flagship_tasks/reports/eq-three-model-matrix-20260927"
MODELS = ("Sol", "Luna", "Terra", "GPT-5.5", "Astra")
MODEL_NAMES = ("gpt-5.6-sol", "gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.5", "gpt-6-astra")
INK = "#111111"
REF = "#444B50"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(direction="out", length=4, pad=6)
    ax.grid(False)


def header(fig, letter, title, x, y):
    fig.text(x - 0.06, y, letter, fontsize=20, weight="bold", va="bottom")
    fig.text(x, y, title, fontsize=18, weight="bold", va="bottom")


def save(fig, build, name):
    for ext in ("svg", "pdf", "png"):
        fig.savefig(build / f"{name}.{ext}", dpi=180, facecolor="white")
    data = {"name": name, "kind": "vector", **collect(build / f"{name}.svg")}
    assert {o["font"] for o in data["objects"] if o["kind"] == "text"} == {"Times New Roman"}
    (build / f"{name}-vector.json").write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8"
    )
    plt.close(fig)
    print(f"Rendered {name}: {len(data['objects'])} editable objects", flush=True)


def data():
    process = json.loads((REPORT / "EQ_AUTONOMOUS_PROCESS.json").read_text(encoding="utf-8"))
    sol_values, _ = load_panel_b_data()
    values = {("Sol", group, arm): sol_values[(group, arm)] for group in GROUPS for arm in ARMS}
    joint = read_csv(ASTRA / "joint_cell_metrics.csv")
    assert len(joint) == 60 and all(r["valid_Q"] == "True" for r in joint)
    for short, model in zip(MODELS[1:], MODEL_NAMES[1:], strict=True):
        for arm in ARMS:
            rows = sorted(
                [r for r in joint if r["model"] == model and r["arm"] == arm],
                key=lambda r: r["world_id"],
            )
            assert len(rows) == 5
            for group, field in zip(
                GROUPS, ("other_nine_macro_mae", "dilute_three_macro_mae"), strict=True
            ):
                values[(short, group, arm)] = np.array([float(r[field]) for r in rows])
    batches = read_csv(PREVIOUS / "source_batches.csv") + read_csv(ASTRA / "source_batches.csv")
    assert len(batches) == 720
    coverage = []
    for row in process["rows"]:
        coverage.append(
            {
                "model": "Sol",
                "arm": row["arm"],
                "world": row["world"],
                "minimum": min(
                    b["nominal_concentration_mol_L"] for b in row["batches"] if b["amount_mol"] > 0
                ),
            }
        )
    for short, model in zip(MODELS[1:], MODEL_NAMES[1:], strict=True):
        for arm in ARMS:
            for w in range(1, 6):
                selected = [
                    r
                    for r in batches
                    if r["model"] == model
                    and r["arm"] == arm
                    and r["world_id"] == f"EQ-W{w:02d}"
                    and float(r["reagent_mol"]) > 0
                ]
                coverage.append(
                    {
                        "model": short,
                        "arm": arm,
                        "world": f"W{w:02d}",
                        "minimum": min(float(r["nominal_input_concentration_M"]) for r in selected),
                    }
                )
    assert len(coverage) == 75
    assert [
        sum(r["minimum"] <= 0.001 + 1e-12 for r in coverage if r["model"] == m) for m in MODELS
    ] == [0, 0, 0, 0, 11]
    case = [
        r
        for r in batches
        if r["model"] == "gpt-6-astra" and r["world_id"] == "EQ-W03" and r["arm"] == "MisIndexed"
    ]
    case.sort(key=lambda r: int(r["batch"]))
    assert len(case) == 12
    summary = json.loads((ASTRA / "summary.json").read_text(encoding="utf-8"))
    q = next(
        r["Q08_dissociation"]
        for r in summary["cells"]
        if r["world_id"] == "EQ-W03" and r["arm"] == "MisIndexed"
    )
    return process, values, coverage, case, q


def figure4(build, process, values):
    fig = plt.figure(figsize=(14.25, 10.4), facecolor="white")
    a = fig.add_axes([0.085, 0.61, 0.385, 0.29])
    b = fig.add_axes([0.59, 0.61, 0.39, 0.29])
    c = fig.add_axes([0.085, 0.14, 0.385, 0.29])
    d = fig.add_axes([0.59, 0.14, 0.39, 0.29])
    for ax in (a, b, c, d):
        style(ax)
    header(fig, "a", "Sol observations and withheld conditions", 0.085, 0.957)
    header(fig, "b", "Sol prior benefits reverse", 0.59, 0.957)
    header(fig, "c", "Across models: other nine queries", 0.085, 0.49)
    header(fig, "d", "Across models: dilute three queries", 0.59, 0.49)
    rows, low, high, minimum = load_panel_a_data()
    refs = [next(r for r in rows if r["query"] == q) for q in sorted({r["query"] for r in rows})]
    source = np.array(
        [
            (
                b["nominal_concentration_mol_L"],
                b["final_responses"]["acid_dissociation_fraction"] * 100,
            )
            for r in process["rows"]
            for b in r["batches"]
        ]
    )
    dilute = [r["nominal_concentration_M"] for r in refs if r["regime"] == "Dilute three"]
    a.axvspan(min(dilute) / 1.2, max(dilute) * 1.2, color="#EFF2F4", zorder=0)
    a.add_patch(
        Rectangle(
            (minimum, low),
            source[:, 0].max() - minimum,
            high - low,
            facecolor="#E6EAED",
            edgecolor="none",
        )
    )
    a.scatter(source[:, 0], source[:, 1], s=13, c="#8D99A1", alpha=0.6, linewidths=0)
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
        ylabel="Dissociation (%)",
        xlabel="Nominal concentration (M)",
    )
    a.set_xticks([1e-5, 1e-3, 1e-1, 10], ["10⁻⁵", "10⁻³", "10⁻¹", "10¹"])
    a.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    a.set_yticks([0, 20, 40, 60, 80])
    a.text(0.004, 56, "Source assays (180)\n5.5–9.2% dissociation", fontsize=16)
    a.text(4.8e-5, 77, "Dilute tests", ha="center", fontsize=16)
    fig.text(0.085, 0.923, "Reference diamonds: 5-world mean ± SD", fontsize=16)
    fig.text(0.59, 0.923, "Bars: 5-world mean ± SD; dots: worlds", fontsize=16)
    centers = np.array([0, 1.35])
    for ai, arm in enumerate(ARMS):
        x = centers + (ai - 1) * 0.35
        vs = [values[("Sol", g, arm)] for g in GROUPS]
        means = np.array([v.mean() for v in vs])
        sd = [v.std(ddof=1) for v in vs]
        b.bar(x, means - 0.001, bottom=0.001, width=0.26, color=ARM_COLORS[arm])
        b.errorbar(x, means, yerr=sd, fmt="none", ecolor=INK, capsize=3, elinewidth=1)
        for j, v in enumerate(vs):
            b.scatter(
                x[j] + np.linspace(-0.08, 0.08, 5),
                v,
                s=17,
                facecolors="white",
                edgecolors=ARM_COLORS[arm],
                zorder=4,
            )
    b.set(yscale="log", ylim=(0.001, 0.6), xlim=(-0.65, 2), ylabel="Macro MAE (log scale)")
    b.set_yticks([0.001, 0.01, 0.1], ["10⁻³", "10⁻²", "10⁻¹"])
    b.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    b.set_xticks(centers, ["Other nine", "Dilute three"])
    b.text(0, 0.36, "Aligned / Opaque  0.46×", ha="center", fontsize=16)
    b.text(1.35, 0.36, "8.65×", ha="center", fontsize=18, weight="bold")
    for ax, group in ((c, GROUPS[0]), (d, GROUPS[1])):
        for mi, model in enumerate(MODELS):
            for ai, arm in enumerate(ARMS):
                v = values[(model, group, arm)]
                x = mi + (ai - 1) * 0.23
                ax.scatter(
                    x + np.linspace(-0.055, 0.055, 5),
                    v,
                    s=23,
                    facecolors="none",
                    edgecolors=ARM_COLORS[arm],
                    linewidths=1,
                    alpha=0.8,
                )
                ax.plot([x - 0.085, x + 0.085], [v.mean()] * 2, color=ARM_COLORS[arm], lw=2.8)
        ax.set(yscale="log", ylim=(0.00025, 0.4), xlim=(-0.6, 4.6), ylabel="Macro MAE (log scale)")
        ax.set_yticks([0.001, 0.01, 0.1], ["10⁻³", "10⁻²", "10⁻¹"])
        ax.yaxis.set_minor_locator(mpl.ticker.NullLocator())
        ax.set_xticks(range(5), MODELS)
        ax.tick_params(axis="x", labelsize=16)
    fig.text(0.085, 0.456, "All configurations: medium; 5 worlds × 3 arms", fontsize=16)
    fig.text(0.59, 0.456, "Open dots: worlds; horizontal marks: means", fontsize=16)
    fig.legend(
        handles=[Patch(color=ARM_COLORS[a], label=a) for a in ARMS],
        loc="lower center",
        bbox_to_anchor=(0.53, 0.008),
        ncol=3,
        frameon=False,
    )
    save(fig, build, "figure04")


def figure5(build, process, coverage, case, q):
    fig = plt.figure(figsize=(14.25, 11.3), facecolor="white")
    a = fig.add_axes([0.125, 0.66, 0.34, 0.245])
    b = fig.add_axes([0.59, 0.735, 0.39, 0.17])
    bc = fig.add_axes([0.59, 0.62, 0.39, 0.075])
    c = fig.add_axes([0.085, 0.105, 0.385, 0.29])
    d = fig.add_axes([0.64, 0.105, 0.34, 0.13])
    for ax in (a, b, bc, c, d):
        style(ax)
    header(fig, "a", "Evidence acquired during research", 0.085, 0.952)
    header(fig, "b", "Astra: observations across 12 batches", 0.59, 0.952)
    header(fig, "c", "Sol/Opaque: extrapolation from local evidence", 0.085, 0.45)
    header(fig, "d", "Astra: report and sealed prediction", 0.59, 0.45)
    a.axvspan(1.3333333e-5, 1.6666667e-4, color="#EFF2F4", zorder=0)
    for mi, model in enumerate(MODELS):
        for ai, arm in enumerate(ARMS):
            selected = sorted(
                [r for r in coverage if r["model"] == model and r["arm"] == arm],
                key=lambda r: r["world"],
            )
            a.scatter(
                [r["minimum"] for r in selected],
                mi + (ai - 1) * 0.22 + np.linspace(-0.07, 0.07, 5),
                s=25,
                c=ARM_COLORS[arm],
                linewidths=0,
            )
    a.set(
        xscale="log", xlim=(7e-6, 0.5), ylim=(4.5, -0.5), xlabel="Minimum assayed concentration (M)"
    )
    a.set_xticks([1e-5, 1e-3, 1e-1], ["10⁻⁵", "10⁻³", "10⁻¹"])
    a.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    a.set_yticks(range(5), MODELS)
    a.tick_params(axis="y", labelsize=16)
    fig.text(0.085, 0.921, "15 studies/model; positive loading only", fontsize=16)
    fig.text(0.125, 0.567, "Shading: dilute test concentrations", fontsize=16)
    fig.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor=ARM_COLORS[arm],
                markeredgecolor="none",
                label=arm,
            )
            for arm in ARMS
        ],
        loc="center",
        bbox_to_anchor=(0.283, 0.528),
        ncol=3,
        fontsize=16,
        frameon=False,
        handletextpad=0.2,
        columnspacing=0.8,
    )
    x = np.arange(1, 13)
    alpha = np.array([float(r["acid_dissociation_fraction"]) * 100 for r in case])
    conc = np.array([float(r["nominal_input_concentration_M"]) for r in case])
    colour = ARM_COLORS["MisIndexed"]
    b.plot(x, alpha, "o-", color=colour, markersize=5, lw=1)
    b.set(xlim=(0.6, 12.4), ylim=(0, 72), ylabel="Dissociation (%)")
    b.set_yticks([0, 20, 40, 60])
    b.set_xticks([])
    b.annotate(
        "53.8%",
        (5, alpha[4]),
        xytext=(5.8, 62),
        fontsize=18,
        arrowprops={"arrowstyle": "-", "lw": 0.7, "color": INK},
    )
    b.text(1, 31, "6.3–7.4%\n(batches 1–3)", fontsize=16)
    fig.text(0.59, 0.921, "World 3 / MisIndexed; all final assays", fontsize=16)
    bc.plot(x, conc, "o-", color=REF, markersize=3.5, lw=1)
    bc.set(yscale="log", xlim=(0.6, 12.4), ylim=(7e-6, 5), xlabel="Batch", ylabel="Conc. (M)")
    bc.set_xticks([1, 3, 5, 7, 9, 12])
    bc.set_yticks([1e-5, 1e-2, 1], ["10⁻⁵", "10⁻²", "10⁰"])
    bc.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    bc.tick_params(labelsize=16)
    fig.text(
        0.59,
        0.525,
        "B9: staged dilution   B10: added reagent\nB12: extended hold",
        fontsize=16,
        linespacing=1.3,
    )
    opaque = sorted([r for r in process["rows"] if r["arm"] == "Opaque"], key=lambda r: r["world"])
    for wi, r in enumerate(opaque):
        pred = r["q08"]["predictions"]["acid_dissociation_fraction"]
        y = pred["estimate"] * 100
        c.errorbar(
            wi - 0.09,
            y,
            yerr=np.array([[y - 100 * pred["lower80"]], [100 * pred["upper80"] - y]]),
            fmt="o",
            color=ARM_COLORS["Opaque"],
            elinewidth=1,
            markersize=6,
            capsize=4,
        )
        c.plot(
            wi + 0.09,
            100 * r["q08"]["reference_means"]["acid_dissociation_fraction"],
            "D",
            color=INK,
            markersize=5,
        )
    all_alpha = [
        100 * b["final_responses"]["acid_dissociation_fraction"]
        for r in opaque
        for b in r["batches"]
    ]
    c.axhspan(min(all_alpha), max(all_alpha), color="#E6EAED", zorder=0)
    c.text(1.95, 10.5, "Source observation range", ha="center", fontsize=16)
    c.set(xlim=(-0.5, 4.5), ylim=(0, 100), ylabel="Dissociation (%)", xlabel="World")
    c.set_xticks(range(5), ["1", "2", "3", "4", "5"])
    c.set_yticks([0, 20, 40, 60, 80, 100])
    fig.text(0.085, 0.414, "13.3 µM; original 80% prediction intervals", fontsize=16)
    c.legend(
        handles=[
            Line2D([0], [0], marker="o", color=ARM_COLORS["Opaque"], label="Prediction"),
            Line2D([0], [0], marker="D", color=INK, linestyle="none", label="Reference"),
        ],
        loc="upper right",
        fontsize=16,
        frameon=False,
        ncol=2,
        handletextpad=0.3,
        columnspacing=0.8,
    )
    fig.text(0.59, 0.407, "After experiments: public report (K1)", fontsize=16, weight="bold")
    fig.text(
        0.59,
        0.345,
        "High loading: apparent plateau\nLow loading: concentration-dependent response",
        fontsize=16,
        linespacing=1.45,
    )
    fig.text(0.59, 0.289, "Then sealed prediction (Q): 13.3 µM", fontsize=16, weight="bold")
    estimate, lower, upper, truth = [
        100 * q[k] for k in ("estimate", "lower80", "upper80", "reference_mean")
    ]
    d.errorbar(
        estimate,
        1,
        xerr=[[estimate - lower], [upper - estimate]],
        fmt="o",
        color=colour,
        capsize=5,
        markersize=7,
        lw=1.5,
    )
    d.plot(truth, 0, "D", color=INK, markersize=6)
    d.set(xlim=(40, 75), ylim=(-0.8, 2.1), xlabel="Dissociation (%)")
    d.set_yticks([1, 0], ["Prediction", "Reference"])
    d.tick_params(axis="y", labelsize=16)
    d.set_xticks([40, 50, 60, 70])
    d.text(estimate, 1.55, "58.80% [54.20, 63.40]", ha="center", fontsize=16)
    d.text(truth + 1.2, 0, "57.97%", va="center", fontsize=16)
    fig.text(0.59, 0.018, "Report wording condensed; reference withheld from agent", fontsize=16)
    save(fig, build, "figure05")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", required=True, type=Path)
    args = parser.parse_args()
    args.build.mkdir(parents=True, exist_ok=True)
    configure()
    mpl.rcParams["lines.linewidth"] = 1
    process, values, coverage, case, q = data()
    figure4(args.build, process, values)
    figure5(args.build, process, coverage, case, q)
    records = [
        {"model": m, "group": g, "arm": a, "world": f"W{wi + 1:02d}", "mae": float(v)}
        for (m, g, a), vals in values.items()
        for wi, v in enumerate(vals)
    ]
    payload = {
        "model_errors": records,
        "minimum_source_concentrations": coverage,
        "astra_case_batches": case,
        "astra_Q08": q,
        "sources": [
            str(REPORT.relative_to(ROOT)),
            str(ASTRA.relative_to(ROOT)),
            str(PREVIOUS.relative_to(ROOT)),
        ],
    }
    (args.build / "source-data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    assert len(records) == 150


if __name__ == "__main__":
    main()
