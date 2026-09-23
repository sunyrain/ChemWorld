"""Render a direct EQ reference/prediction comparison and a separate result table."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
OUT = ROOT / "output/figures/eq-simple-preview"
ARMS = ("Opaque", "Aligned", "MisIndexed")
COLORS = {"Opaque": "#607382", "Aligned": "#287E88", "MisIndexed": "#B87752"}
INK, MUTED = "#334550", "#65747E"


def main():
    process = json.loads((SOURCE / "EQ_AUTONOMOUS_PROCESS.json").read_text(encoding="utf-8"))
    story = json.loads((SOURCE / "STORY_WORLD_ANALYSIS.json").read_text(encoding="utf-8"))
    rows = process["rows"]
    assert len(rows) == 15 and sum(len(r["batches"]) for r in rows) == 180
    worlds = sorted({r["world"] for r in rows})
    assert worlds == [f"W0{i}" for i in range(1, 6)]
    obs = [
        100 * b["final_responses"]["acid_dissociation_fraction"] for r in rows for b in r["batches"]
    ]
    observed = [min(obs), max(obs)]
    assert max(process["query_concentrations"][q] for q in ("Q03", "Q08", "Q09")) < min(
        b["nominal_concentration_mol_L"] for r in rows for b in r["batches"]
    )
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 11,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.edgecolor": "#A9B4BB",
            "axes.linewidth": 0.7,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
        }
    )
    fig = plt.figure(figsize=(12.8, 5.6), facecolor="white")
    ax = fig.add_axes([0.078, 0.215, 0.89, 0.60])
    labels = ["Blind-test reference", *ARMS]
    colors = ["#CBD5DC", *(COLORS[a] for a in ARMS)]
    xx = np.arange(len(worlds))
    width = 0.17
    export = []
    ax.axhspan(*observed, color="#E7EBEE", alpha=0.75, zorder=0)
    for j, (name, color) in enumerate(zip(labels, colors, strict=True)):
        values = []
        for w in worlds:
            rr = [r for r in rows if r["world"] == w]
            refs = [r["q08"]["reference_means"]["acid_dissociation_fraction"] for r in rr]
            assert len(rr) == 3 and max(refs) == min(refs)
            if name == labels[0]:
                values.append(refs[0] * 100)
            else:
                r = next(r for r in rr if r["arm"] == name)
                pred = r["q08"]["predictions"]["acid_dissociation_fraction"]
                values.append(pred["estimate"] * 100)
                export.append(
                    {
                        "world": w,
                        "arm": name,
                        "query": "Q08",
                        "reference_mean": refs[0],
                        **pred,
                        "source_min": r["source_dissociation_range"][0],
                        "source_max": r["source_dissociation_range"][1],
                    }
                )
        x = xx + (j - 1.5) * (width + 0.012)
        bars = ax.bar(x, values, width=width, color=color, linewidth=0, label=name, zorder=3)
        ax.bar_label(
            bars,
            labels=[f"{v:.1f}" for v in values],
            padding=4,
            fontsize=10.3,
            color=MUTED if j == 0 else color,
        )
    ax.set(xlim=(-0.55, 5.05), ylim=(0, 82), ylabel="Dissociation (%)")
    ax.set_xticks(xx, [f"World {i + 1}" for i in range(5)])
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.tick_params(axis="x", length=0, pad=11, labelsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E3E8EB", lw=0.6)
    ax.set_axisbelow(True)
    ax.text(4.50, 16.1, "Observed in\nresearch", size=10.5, color=MUTED, linespacing=1.3)
    ax.text(
        4.50,
        7.6,
        f"{observed[0]:.1f}-{observed[1]:.1f}%",
        size=10.5,
        color=MUTED,
        va="center",
        weight="bold",
    )
    fig.text(0.078, 0.945, "Predictions at the most dilute test", size=16, weight="bold")
    fig.text(
        0.078,
        0.901,
        "Same test recipe across information arms: 13.3 µM nominal concentration",
        size=11.5,
        color=MUTED,
    )
    fig.legend(
        *ax.get_legend_handles_labels(),
        loc="center left",
        bbox_to_anchor=(0.071, 0.853),
        frameon=False,
        ncol=4,
        fontsize=11,
        handlelength=1.3,
        columnspacing=2.2,
    )
    fig.text(
        0.078,
        0.107,
        "Bars show the reference mean and each agent's point prediction; "
        "complete 80% prediction intervals are retained separately.",
        color=MUTED,
        size=9.8,
    )
    fig.text(
        0.078,
        0.064,
        "Shaded band: range of all 180 research observations across 15 campaigns. "
        "Blind-test references were withheld from the agents.",
        color=MUTED,
        size=9.8,
    )
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"eq-predictions-vs-reference.{ext}", dpi=190)
    plt.close(fig)
    with (OUT / "predictions-with-intervals.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(export[0]))
        writer.writeheader()
        writer.writerows(export)

    agg = story["eq_p_query_regimes"]["aggregate"]
    stats = {(r["arm"], r["group"]): r for r in agg}
    reduction = 100 * (
        1 - stats["Aligned", "other_nine"]["mae"] / stats["Opaque", "other_nine"]["mae"]
    )
    ratio = (
        stats["Aligned", "three_most_dilute"]["mae"] / stats["Opaque", "three_most_dilute"]["mae"]
    )
    cells = story["eq_p_query_regimes"]["cells"]
    table_rows = []
    for a in ARMS:
        for g in ("other_nine", "three_most_dilute"):
            for metric in ("mae", "coverage"):
                assert (
                    abs(
                        np.mean([r["groups"][g][metric] for r in cells if r["arm"] == a])
                        - stats[a, g][metric]
                    )
                    < 1e-12
                )
        other, dilute = stats[a, "other_nine"], stats[a, "three_most_dilute"]
        table_rows.append(
            f"| {a} | {other['mae']:.5f} | {dilute['mae']:.5f} | "
            f"{100 * other['coverage']:.1f}% | {100 * dilute['coverage']:.1f}% |"
        )
    table = "\n".join(
        [
            "# Table. Equilibrium prediction performance across test regimes",
            "",
            "| Information arm | Macro MAE: other nine | Macro MAE: dilute three | "
            "80% interval coverage: other nine | 80% interval coverage: dilute three |",
            "| :--- | ---: | ---: | ---: | ---: |",
            *table_rows,
            "",
            "Values are means over five worlds per arm and aggregate three response targets "
            "(normalized pH, acid dissociation fraction and precipitation signal). "
            "The figure separately shows only dissociation at the single most dilute recipe.",
            "",
            "The dilute group contains the three lowest nominal-concentration recipes "
            "(Q03, Q08, Q09); the other nine queries include boundary conditions and are not "
            "all interpolation. Grouping was performed post hoc. Macro MAE is calculated "
            "against the original five-observation reference means. Coverage uses all "
            "reference observations: 225 judgments per arm for the dilute group and 675 "
            "for the other nine. These are not independent world replicates.",
            "",
            "Compared with Opaque, Aligned has lower MAE on the other nine queries and "
            "higher MAE on the dilute three in each of the five worlds. The ratio of the "
            f"across-world mean MAEs corresponds to a {reduction:.1f}% reduction on the other nine "
            f"and {ratio:.2f} times the error on the dilute three. "
            "This is a full-process contrast, "
            "not a causal attribution to an internal reasoning mechanism.",
            "",
            "Source: [retained regime analysis](../../../workstreams/flagship_tasks/reports/"
            "work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json).",
            "",
        ]
    )
    (OUT / "TABLE.md").write_text(table, encoding="utf-8")
    interval_rows = sorted(export, key=lambda r: (r["world"], ARMS.index(r["arm"])))
    interval_table = [
        "# Most-dilute prediction details",
        "",
        "All values are dissociation percentages for the most dilute recipe (Q08). "
        "The source range comes from each campaign's twelve final assays. "
        "Intervals are the original agent-issued 80% prediction intervals, "
        "not uncertainty in the plotted mean. The reference is the mean of the "
        "original five evaluator observations and was withheld from the agent.",
        "",
        "| World | Arm | Observed source range (%) | Point prediction (%) | "
        "80% prediction interval (%) | Reference mean (%) |",
        "| :--- | :--- | ---: | ---: | ---: | ---: |",
    ]
    interval_table.extend(
        f"| {r['world']} | {r['arm']} | {r['source_min'] * 100:.2f}-{r['source_max'] * 100:.2f} "
        f"| {r['estimate'] * 100:.2f} | [{r['lower80'] * 100:.2f}, {r['upper80'] * 100:.2f}] "
        f"| {r['reference_mean'] * 100:.2f} |"
        for r in interval_rows
    )
    (OUT / "PREDICTION_INTERVALS.md").write_text("\n".join(interval_table) + "\n", encoding="utf-8")
    with (OUT / "regime-summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(agg[0]))
        writer.writeheader()
        writer.writerows(agg)
    assert len(export) == 15
    print(
        "Preview ready: 5 reference bars + 15 predictions; 180-observation range; "
        "separate 3-arm table and all 15 original intervals exported."
    )


if __name__ == "__main__":
    main()
