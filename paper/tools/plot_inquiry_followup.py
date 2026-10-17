"""Render retained quantitative data for main figures 2, 4 and 5."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper/venues/nature"
EVIDENCE = PAPER / "evidence"
OUT = PAPER / "figures/data-inquiry-20261017"
COLORS = ["#236b8e", "#cf7b25", "#368d75", "#865b9c", "#b34e61"]
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 11,
        "axes.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    }
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(fig, name):
    for suffix in ("png", "pdf", "svg"):
        path = OUT / f"{name}.{suffix}"
        fig.savefig(path, dpi=240, bbox_inches="tight", facecolor="white")
        if suffix == "svg":
            path.write_text(
                "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines())
                + "\n",
                encoding="utf-8",
            )
    plt.close(fig)
    print("Rendered", name, flush=True)


def panel(ax, title, specifications, first, second, ylabel):
    """Each spec supplies label and five (first-session-values, second-values) lists."""
    offsets = [-0.095, -0.0475, 0, 0.0475, 0.095]
    for i, (_label, worlds) in enumerate(specifications):
        for w, (a, b) in enumerate(worlds):
            x1, x2 = i * 2.1 + offsets[w], i * 2.1 + 0.72 + offsets[w]
            for x, values in [(x1, a), (x2, b)]:
                ax.scatter(
                    [x + (j - (len(values) - 1) / 2) * 0.012 for j in range(len(values))],
                    values,
                    s=12,
                    c=COLORS[w],
                    alpha=0.24,
                    edgecolors="none",
                    zorder=2,
                )
            ax.plot(
                [x1, x2],
                [fmean(a), fmean(b)],
                color=COLORS[w],
                lw=1.1,
                marker="o",
                ms=3.8,
                zorder=3,
            )
        lo = fmean(fmean(a) for a, _ in worlds)
        hi = fmean(fmean(b) for _, b in worlds)
        ax.text(
            i * 2.1 + 0.36,
            0.99,
            f"{lo:.3f} → {hi:.3f}",
            ha="center",
            va="top",
            transform=ax.get_xaxis_transform(),
            fontsize=8,
            weight="bold",
        )
    ax.set_xticks(
        [i * 2.1 + 0.36 for i in range(len(specifications))], [label for label, _ in specifications]
    )
    ax.set_title(title, loc="left", weight="bold", pad=10)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(f"Within each response: {first}  →  {second}", fontsize=8, labelpad=7)
    ax.set_ylim(bottom=0, top=ax.get_ylim()[1] * 1.16)
    ax.grid(axis="y", alpha=0.14)


def world_lists(data, metric, field, arms, **filters):
    selected = [r for r in data if all(r[k] == v for k, v in filters.items())]
    return [
        tuple(
            [
                float(r[metric])
                for r in selected
                if r["world"].endswith(f"W{w:02}") and r[field] == arm and r[metric] != ""
            ]
            for arm in arms
        )
        for w in range(1, 6)
    ]


def legend(fig):
    fig.legend(
        [Line2D([], [], color=c, marker="o", ms=4, lw=1) for c in COLORS],
        [f"W{i}" for i in range(1, 6)],
        loc="lower center",
        ncol=5,
        frameon=False,
        bbox_to_anchor=(0.5, -0.015),
        title="Connected solid dots: world means; faint dots: individual sessions",
    )


def fig2(source):
    metrics = rows(source / "session_metrics.csv")
    operating = rows(source / "EC_RX_RECOMMENDATIONS.csv")
    fig, axes = plt.subplots(2, 2, figsize=(11.6, 7.7))
    arms = ["discovery", "optimization"]
    panel(
        axes[0, 0],
        "a  Electrochemistry: effective procedures",
        [
            ("Score", world_lists(operating, "recommendation_score", "goal", arms, system="EC")),
            (
                "Product yield",
                world_lists(operating, "recommendation_yield", "goal", arms, system="EC"),
            ),
        ],
        "Discovery",
        "Optimization",
        "Retested response (higher is better)",
    )
    panel(
        axes[0, 1],
        "b  Electrochemistry: new-condition judgment",
        [
            (label, world_lists(metrics, "mae", "goal", arms, system="EC", response=response))
            for label, response in [
                ("Score", "score"),
                ("Yield", "selective_product_yield"),
                ("Faradaic\nefficiency", "faradaic_efficiency"),
            ]
        ],
        "Discovery",
        "Optimization",
        "Mean absolute error (lower is better)",
    )
    arms = ["Opaque", "Aligned"]
    panel(
        axes[1, 0],
        "c  Reaction processing: information and operation",
        [
            (label, world_lists(operating, metric, "arm", arms, system="RX", goal="optimization"))
            for label, metric in [
                ("Score", "recommendation_score"),
                ("Product yield", "recommendation_yield"),
            ]
        ],
        "Opaque",
        "Aligned",
        "Retested response (higher is better)",
    )
    panel(
        axes[1, 1],
        "d  Reaction processing: response-specific effects",
        [
            (
                label,
                world_lists(
                    metrics, "mae", "arm", arms, system="RX", goal="optimization", response=response
                ),
            )
            for label, response in [("Risk", "safety_risk"), ("Conversion", "conversion")]
        ],
        "Opaque",
        "Aligned",
        "Mean absolute error (lower is better)",
    )
    fig.suptitle(
        "Distinct consequences of research goals and supplied information", weight="bold", y=1.01
    )
    fig.text(
        0.5,
        0.045,
        "Electrochemistry: 45/45 sessions per commission; reaction "
        "comparison: 15/15 per arm. All displayed outcomes available.",
        ha="center",
        fontsize=8,
    )
    fig.subplots_adjust(hspace=0.55, wspace=0.27, bottom=0.16)
    legend(fig)
    save(fig, "fig02_conditions")


def fig5(source):
    metrics = rows(source / "session_metrics.csv")
    refs = rows(EVIDENCE / "new_c_source_references.csv")
    eq = rows(EVIDENCE / "opportunity_session_responses.csv")
    fig, axes = plt.subplots(2, 2, figsize=(11.7, 8.0))
    names = [
        ("Purity", "crystal_purity"),
        ("Size", "crystal_size"),
        ("Recovery", "crystal_yield"),
        ("Fines", "crystal_fines_fraction"),
    ]
    panel(
        axes[0, 0],
        "a  Research opportunity: separate groups",
        [
            (
                label,
                world_lists(
                    metrics,
                    "mae",
                    "opportunity",
                    ["NoResearch", "Research"],
                    system="C",
                    response=response,
                ),
            )
            for label, response in names
        ],
        "NoResearch",
        "Research",
        "Mean absolute error",
    )
    panel(
        axes[0, 1],
        "b  Using the same fifteen research histories",
        [
            (
                label,
                [
                    tuple(
                        [
                            float(r[key])
                            for r in refs
                            if r["response"] == response and r["world"].endswith(f"W{w:02}")
                        ]
                        for key in ["agent_mae", "source_mean_mae"]
                    )
                    for w in range(1, 6)
                ],
            )
            for label, response in names
        ],
        "Research agent",
        "Source mean",
        "Mean absolute error",
    )
    panel(
        axes[1, 0],
        "c  Fines: improved points, poorer intervals",
        [
            (
                "Interval score",
                world_lists(
                    metrics,
                    "interval_score",
                    "opportunity",
                    ["NoResearch", "Research"],
                    system="C",
                    response="crystal_fines_fraction",
                ),
            ),
        ],
        "NoResearch",
        "Research",
        "80% interval score (lower is better)",
    )
    # Macro error averages all three response-level session entries before drawing.
    macro = []
    for arm in ["NoResearch", "Research"]:
        for group in ["all", "dilute"]:
            for world in [f"W{w:02}" for w in range(1, 6)]:
                selected = [
                    r
                    for r in eq
                    if r["world"] == world and r["query_group"] == group and r["opportunity"] == arm
                ]
                for repeat in sorted({r["repeat"] for r in selected}):
                    vals = [float(r["mae"]) for r in selected if r["repeat"] == repeat and r["mae"]]
                    if vals:
                        assert len(vals) == 3
                        macro.append(
                            {"world": world, "arm": arm, "group": group, "mae": fmean(vals)}
                        )
    panel(
        axes[1, 1],
        "d  Equilibrium: overall and regional outcomes",
        [
            (label, world_lists(macro, "mae", "arm", ["NoResearch", "Research"], group=group))
            for label, group in [("All queries", "all"), ("Extreme dilution", "dilute")]
        ],
        "NoResearch",
        "Research",
        "Normalized macro MAE",
    )
    fig.suptitle(
        "Acquiring evidence, using observations and expressing uncertainty", weight="bold", y=1.01
    )
    fig.text(
        0.5,
        0.055,
        "a,c: 15/15 forecasts per arm. b: paired methods on the same "
        "histories, not a third research arm.\nd: Research 14/15 (W3 repeat"
        " 3 missing); NoResearch 15/15. Missing values are not zero.",
        ha="center",
        fontsize=8,
    )
    fig.subplots_adjust(hspace=0.55, wspace=0.28, bottom=0.18)
    legend(fig)
    save(fig, "fig05_opportunity")


def fig4():
    data = rows(EVIDENCE / "matched_world_forecast_contrasts.csv")
    history = read(EVIDENCE / "core_history_review_sources.json")["Matched-world study A"]
    fig = plt.figure(figsize=(11.7, 7.8))
    gs = fig.add_gridspec(2, 3, hspace=0.48, wspace=0.35)
    for index, (response, label) in enumerate(
        [
            ("pH_normalized", "Normalized pH"),
            ("acid_dissociation_fraction", "Free dissociation"),
            ("precipitation_signal", "Precipitation"),
        ]
    ):
        ax = fig.add_subplot(gs[0, index])
        selected = [r for r in data if r["response"] == response]
        limits = [
            float(r[k]) for r in selected for k in ["reference_B_minus_A", "forecast_B_minus_A"]
        ]
        lo, hi = min(limits), max(limits)
        pad = max((hi - lo) * 0.12, 0.002)
        ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="#7c838b", lw=1, ls="--")
        for p in range(1, 6):
            v = [r for r in selected if r["pair"] == f"P{p:02}"]
            ax.scatter(
                [float(r["reference_B_minus_A"]) for r in v],
                [float(r["forecast_B_minus_A"]) for r in v],
                c=COLORS[p - 1],
                s=27,
                alpha=0.8,
                edgecolors="white",
                linewidths=0.3,
            )
        ax.axhline(0, color="#d6dadd", lw=0.7)
        ax.axvline(0, color="#d6dadd", lw=0.7)
        ax.set(
            xlim=(lo - pad, hi + pad),
            ylim=(lo - pad, hi + pad),
            xlabel="Reference difference (B - A)",
            ylabel="Forecast difference (B - A)",
        )
        ax.set_title(f"{'abc'[index]}  {label}", loc="left", weight="bold")
        ax.ticklabel_format(style="plain", useOffset=False)
        ax.grid(alpha=0.12)
    ax = fig.add_subplot(gs[1, :2])
    observed = []
    for b in history["batches"]:
        a = b["actions"]
        c = sum(x.get("amount_mol", 0) for x in a if x["operation"] == "add_reagent") / sum(
            x.get("volume_L", 0) for x in a if x["operation"] == "add_solvent"
        )
        y = b["metrics"]["precipitation_signal"]
        phase = 0 if b["ordinal"] <= 6 else 1
        color = [COLORS[0], COLORS[1]][phase]
        ax.scatter(c, y, c=color, s=42, zorder=3)
        ax.annotate(
            str(b["ordinal"]),
            (c, y),
            xytext={4: (6, -10), 8: (6, 12), 12: (-22, 12), 11: (6, -23)}.get(b["ordinal"], (4, 5)),
            textcoords="offset points",
            fontsize=8,
            color=color,
        )
        observed.append(
            {
                "batch": b["ordinal"],
                "concentration_mol_L": c,
                "precipitation_signal": y,
                "end_operation": b["end_step"],
            }
        )
    write = OUT / "matched_study_A_observations.csv"
    with write.open("w", encoding="utf8", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=list(observed[0]))
        w.writeheader()
        w.writerows(observed)
    ax.set(
        xscale="log",
        xlabel="Nominal final concentration (mol/L)",
        ylabel="Measured precipitation signal",
        ylim=(-0.006, 0.105),
    )
    ax.set_title("d  Matched-world study A: the actual twelve assays", loc="left", weight="bold")
    ax.legend(
        [Line2D([], [], marker="o", ls="", color=c) for c in COLORS[:2]],
        ["Batches 1-6", "Batches 7-12, after next-test note"],
        loc="upper left",
        frameon=False,
        fontsize=8,
    )
    ax.grid(alpha=0.12)
    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    ax.set_title("e  Difference magnitude", loc="left", weight="bold")
    contrasts = read(EVIDENCE / "matched_world_forecast_contrasts.json")["summary"]
    magnitude_table = ax.table(
        cellText=[
            [
                label,
                f"{row['mean_absolute_contrast_error']:.5f}",
                f"{row['zero_difference_mae']:.5f}",
            ]
            for label, row in zip(["pH", "Dissociation", "Precipitation"], contrasts, strict=True)
        ],
        colLabels=["Response", "Forecast", "Zero gap"],
        cellLoc="center",
        bbox=[0, 0.44, 1, 0.42],
        colWidths=[0.42, 0.29, 0.29],
    )
    magnitude_table.auto_set_font_size(False)
    magnitude_table.set_fontsize(8)
    for (row, _), cell in magnitude_table.get_celld().items():
        cell.set_edgecolor("#ccd6df")
        if row == 0:
            cell.set_facecolor("#e9eff5")
            cell.set_text_props(weight="bold")
    ax.text(0, 0.96, "Mean absolute contrast error", va="top", fontsize=9)
    ax.text(
        0,
        0.36,
        "Lower forecast error in all five\nworld pairs for each response.\n\n"
        "Zero gap: identical predictions\nfor both worlds.\n\n"
        "All zero and small gaps retained.",
        va="top",
        fontsize=9,
        linespacing=1.35,
    )
    fig.suptitle(
        "World differences in final predictions and the observations behind a local relation",
        weight="bold",
        y=1.01,
    )
    fig.legend(
        [Line2D([], [], color=c, marker="o", lw=0) for c in COLORS],
        [f"Pair {i}" for i in range(1, 6)],
        loc="lower center",
        ncol=5,
        frameon=False,
        bbox_to_anchor=(0.5, -0.035),
    )
    fig.text(
        0.5,
        0.005,
        "Each top-panel point: 3-session forecast means versus "
        "5-observation references in each world. Correlated query "
        "contrasts; no confidence intervals.",
        ha="center",
        fontsize=8,
    )
    save(fig, "fig04_matched")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    source = ROOT / binding["report_root"]
    fig2(source)
    fig4()
    fig5(source)


if __name__ == "__main__":
    main()
