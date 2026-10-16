"""Draw manuscript quantitative figures directly from retained review data."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / "paper/venues/nature/evidence"
OUT = ROOT / "paper/venues/nature/figures/integrated-20261016"
BLUE, ORANGE, GREEN, GREY = "#276A9B", "#C46C36", "#32856D", "#64727E"
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "pdf.fonttype": 42,
        "savefig.facecolor": "white",
    }
)


def read(name):
    return json.loads((E / name).read_text(encoding="utf-8"))


def rows(name):
    with (E / name).open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def save(fig, name):
    fig.savefig(OUT / (name + ".pdf"), bbox_inches="tight")
    fig.savefig(OUT / (name + ".png"), bbox_inches="tight", dpi=170)
    plt.close(fig)
    print("Drawn " + name, flush=True)


def title(ax, text):
    ax.set_title(text, loc="left", fontweight="bold", pad=12)


def main():
    eq = rows("focal_equilibrium_assays.csv")
    fig = plt.figure(figsize=(9.1, 6.5), layout="constrained")
    grid = fig.add_gridspec(2, 3, height_ratios=[1, 1.23], hspace=0.15)
    for i, (metric, label) in enumerate(
        (
            ("pH_normalized", "Normalized pH"),
            ("acid_dissociation_fraction", "Dissociation fraction"),
            ("precipitation_signal", "Precipitation signal"),
        )
    ):
        ax = fig.add_subplot(grid[0, i])
        for command, marker, color in (("reagent", "o", BLUE), ("component", "s", ORANGE)):
            rr = [r for r in eq if r["feed_command"] == command]
            ax.scatter(
                [float(r["nominal_concentration_M"]) for r in rr],
                [float(r[metric]) for r in rr],
                color=color,
                marker=marker,
                s=30,
                label=command + " command",
            )
        ax.set(xlabel="Nominal final loading (mol/L)", ylabel=label, xlim=(0, 0.87))
        title(ax, "abc"[i] + "  " + label)
        if i == 0:
            ax.legend(fontsize=7, loc="upper right")
    ax = fig.add_subplot(grid[1, :2])
    ax.axis("off")
    title(ax, "d  One explanation history, including its unresolved end")
    blocks = [
        (
            "Before research",
            "Weak-acid expectation:\nhigher loading lowers\npH and dissociation.",
            BLUE,
        ),
        (
            "After 6 assays",
            "Component 0 may set loading.\nA concentration response supports;\n"
            "flatness favours background\nor weak coupling.",
            ORANGE,
        ),
        (
            "After 12 assays",
            "Plateau retained; fixed\nbackground, saturation and\nweak trends unresolved.",
            GREEN,
        ),
        (
            "Later prediction",
            "Fixed background favoured\nas experimentally supported;\ndilute regime untested.",
            GREY,
        ),
    ]
    for j, (head, body, color) in enumerate(blocks):
        x, y = (0.02 + (j % 2) * 0.50, 0.90 - (j // 2) * 0.49)
        ax.text(x, y, head, color=color, weight="bold", transform=ax.transAxes, va="top")
        ax.text(x, y - 0.11, body, fontsize=8.3, transform=ax.transAxes, va="top", linespacing=1.5)
    ax.text(
        0.02,
        -0.05,
        (
            "Both feed commands add the same species: no acid-identity "
            "contrast.\nBroader dilution was proposed in the terminal note but "
            "not executed."
        ),
        fontsize=8,
        transform=ax.transAxes,
        color=GREY,
    )
    ax = fig.add_subplot(grid[1, 2])
    rr = [
        r
        for r in rows("opportunity_query_predictions.csv")
        if r["repeat"] == "repeat-01"
        and r["world"] == "W01"
        and r["query_id"] == "Q08"
        and r["response"] == "acid_dissociation_fraction"
    ]
    for j, arm in enumerate(("Research", "NoResearch")):
        r = next(x for x in rr if x["opportunity"] == arm)
        v, lo, hi = [float(r[k]) for k in ("estimate", "lower80", "upper80")]
        ax.errorbar(v, j, xerr=[[v - lo], [hi - v]], fmt="o", color=[BLUE, ORANGE][j], capsize=4)
    ax.axvline(float(rr[0]["reference_mean"]), color=GREEN, linestyle="--", label="Withheld mean")
    ax.set(
        yticks=[0, 1],
        yticklabels=["Research", "No research"],
        xlabel="Dilute dissociation forecast",
        xlim=(0, 1),
        ylim=(-0.65, 1.65),
    )
    ax.legend(fontsize=7, loc="upper center")
    title(ax, "e  New use of local evidence")
    save(fig, "explanation_history")

    sessions = read("process_public_records.json")["sessions"]
    fig = plt.figure(figsize=(9.1, 6.2), layout="constrained")
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1.05])
    for i, (repeat, batch_ids, xkey, xlab) in enumerate(
        (
            ("repeat-01", [11, 12], "nominal_reagent_added_mol", "Reagent charge (mol)"),
            ("repeat-02", [4, 11, 12], "nominal_solvent_added_L", "Solvent volume (L)"),
        )
    ):
        s = next(s for s in sessions if s["repeat"] == repeat and s["id"] == "C-W05-Aligned")
        ax = fig.add_subplot(grid[0, i])
        for batch in batch_ids:
            b = next(b for b in s["batches"] if b["batch"] == batch)
            e = next(
                e
                for e in s["events"]
                if e["batch"] == batch and e["action"].get("instrument") == "final_assay"
            )
            ax.scatter(
                b[xkey],
                e["observations"]["crystal_fines_fraction"],
                s=50,
                color=GREEN if batch == 12 and i == 0 else ORANGE if batch == 12 else BLUE,
                zorder=3,
            )
            ax.annotate(
                f"Batch {batch}",
                (b[xkey], e["observations"]["crystal_fines_fraction"]),
                xytext=(4, 6),
                textcoords="offset points",
                fontsize=8,
            )
        ax.axhline(0.5, color=GREY, linestyle="--", label="Fines limit")
        ax.set(
            xlabel=xlab,
            ylabel="Fines fraction",
            ylim=(0.34, 0.66),
            xlim=(0.017, 0.036) if i == 0 else (0.057, 0.087),
        )
        ax.legend(loc="lower right", fontsize=8)
        title(ax, ["a  Prospective lower-charge test", "b  Prospective interpolation test"][i])
    ax = fig.add_subplot(grid[1, :])
    ax.axis("off")
    title(ax, "c  What the experiments change")
    columns = [
        "Judgment",
        "Test intention",
        "Executed evidence",
        "Supported standing",
        "Subsequent use",
    ]
    data = [
        [
            "EQ component\nexplanation",
            "Change the\nacid source",
            "Same species via\ntwo command names",
            "Local plateau;\nmechanism unresolved",
            "Background favoured\nin dilute forecast",
        ],
        [
            "Lower-charge\nexpectation",
            "Cross fines limit\nwith useful recovery",
            "Fines 0.529 to 0.387;\nratio also changes",
            "Local recipe\nimprovement",
            "Select tested\nbatch 12",
        ],
        [
            "Interpolation\nexpectation",
            "Retain recovery;\nrestore fines <0.50",
            "Fines 0.512 to 0.601\nat intermediate volume",
            "Expectation\nretracted",
            "Return to feasible\nbatch 4",
        ],
    ]
    table = ax.table(
        cellText=data,
        colLabels=columns,
        cellLoc="left",
        colLoc="left",
        bbox=[0, 0.04, 1, 0.88],
        colWidths=[0.17, 0.20, 0.23, 0.20, 0.20],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.8)
    for (r, _), cell in table.get_celld().items():
        cell.set_edgecolor("#DAE1E6")
        cell.set_facecolor("#EAF0F4" if r == 0 else "white")
        if r == 0:
            cell.set_text_props(weight="bold")
    save(fig, "tests_and_revision")

    opportunity = rows("opportunity_session_responses.csv")
    c = rows("corrected_c_session_responses.csv")
    fig, axs = plt.subplots(2, 2, figsize=(9.1, 6.4), layout="constrained")
    for ax, group, tag, label in (
        (axs[0, 0], "all", "a", "All 12 queries"),
        (axs[0, 1], "dilute", "b", "Extreme-dilution 3 queries"),
    ):
        all_values = []
        for w in range(1, 6):
            for arm, offset, color in (("Research", -0.13, BLUE), ("NoResearch", 0.13, ORANGE)):
                values = []
                for repeat in ("repeat-01", "repeat-02", "repeat-03"):
                    rr = [
                        r
                        for r in opportunity
                        if r["world"] == f"W0{w}"
                        and r["opportunity"] == arm
                        and r["repeat"] == repeat
                        and r["query_group"] == group
                        and r["mae"]
                    ]
                    if rr:
                        values.append(np.mean([float(r["mae"]) for r in rr]))
                ax.scatter([w + offset] * len(values), values, s=23, color=color, alpha=0.55)
                all_values.extend(values)
                ax.plot(
                    [w + offset - 0.07, w + offset + 0.07],
                    [np.mean(values)] * 2,
                    color=color,
                    lw=2.5,
                )
        ax.scatter([], [], color=BLUE, label="Research (14)")
        ax.scatter([], [], color=ORANGE, label="No research (15)")
        ax.set(
            xlabel="Fixed world",
            ylabel="Macro MAE",
            xticks=range(1, 6),
            ylim=(0, max(all_values) * 1.13),
        )
        if group == "all":
            ax.legend(fontsize=7)
        title(ax, tag + "  " + label)
    ax = axs[1, 0]
    for i, metric in enumerate(
        ("crystal_yield", "crystal_purity", "crystal_size", "crystal_fines_fraction")
    ):
        rr = [r for r in c if r["response"] == metric]
        for field, offset, color in (("agent_mae", -0.10, BLUE), ("source_mean_mae", 0.10, GREY)):
            ws = [
                np.mean([float(r[field]) for r in rr if r["world"] == f"W0{w}"])
                for w in range(1, 6)
            ]
            ax.scatter([i + offset] * 5, ws, color=color, s=25)
            ax.plot([i + offset - 0.07, i + offset + 0.07], [np.mean(ws)] * 2, color=color, lw=2)
    ax.scatter([], [], color=BLUE, label="Agent")
    ax.scatter([], [], color=GREY, label="Own source mean")
    ax.set(
        xticks=range(4),
        xticklabels=["Recovery", "Purity", "Size index", "Fines"],
        ylabel="Response-specific MAE",
        ylim=(0, 0.4),
    )
    ax.legend(fontsize=7)
    title(ax, "c  Different uses of the same C history")
    ax = axs[1, 1]
    rr = [r for r in c if r["response"] == "crystal_purity"]
    for i, field, color in (
        (0, "source_mean", GREY),
        (1, "target_mean", GREEN),
        (2, "prediction_mean", BLUE),
    ):
        vals = [float(r[field]) for r in rr]
        ax.scatter(i + np.linspace(-0.15, 0.15, len(vals)), vals, s=14, color=color, alpha=0.60)
        ax.plot([i - 0.22, i + 0.22], [np.mean(vals)] * 2, color=color, lw=2)
    ax.set(
        xticks=range(3),
        xticklabels=["Source", "Targets", "Forecasts"],
        ylabel="Session-mean purity",
        ylim=(0.86, 1.01),
    )
    title(ax, "d  Purity in corrected C (42 sessions)")
    save(fig, "consequences_of_inquiry")

    fig, axs = plt.subplots(1, 3, figsize=(9.1, 3.3), layout="constrained")
    for ax, vals, labels, heading in (
        (
            axs[0],
            [45, 45, 39, 41, 41, 42],
            ["EQ planned", "C planned", "EQ chains", "C chains", "EQ Q", "C Q"],
            "a  Current process cohort",
        ),
        (
            axs[1],
            [34, 44, 58, 42],
            ["EQ included", "EQ terminal", "C included", "C terminal"],
            "b  178 adjacent note pairs",
        ),
        (
            axs[2],
            [83, 7, 2],
            ["Matched", "Partial", "No explicit plan"],
            "c  92 selected immediate plans",
        ),
    ):
        ax.barh(labels[::-1], vals[::-1], color=BLUE)
        for i, v in enumerate(vals[::-1]):
            ax.text(v + 0.7, i, str(v), va="center", fontsize=8)
        ax.set_xlim(0, max(vals) * 1.2)
        ax.set_xlabel("Count")
        title(ax, heading)
    save(fig, "process_coverage")

    qrows = rows("corrected_c_query_responses.csv")
    sources = rows("corrected_c_source_assays.csv")
    fig, axs = plt.subplots(2, 4, figsize=(9.1, 5.8), layout="constrained")
    for i, (metric, label) in enumerate(
        (
            ("crystal_yield", "Recovery"),
            ("crystal_purity", "Purity"),
            ("crystal_size", "Size index"),
            ("crystal_fines_fraction", "Fines"),
        )
    ):
        rr = [r for r in qrows if r["response"] == metric]
        values = [
            [float(r[metric]) for r in sources],
            [float(r["truth"]) for r in rr],
            [float(r["prediction"]) for r in rr],
        ]
        ax = axs[0, i]
        ax.boxplot(
            values,
            tick_labels=["Source", "Target", "Agent"],
            showfliers=False,
            widths=0.5,
            whis=(0, 100),
        )
        ax.tick_params(axis="x", labelsize=7)
        title(ax, "abcd"[i] + "  " + label)
        ax.set_ylabel("Public response scale")
        ax = axs[1, i]
        ax.hist([float(r["signed_error"]) for r in rr], bins=18, color=BLUE)
        ax.axvline(0, color=ORANGE, lw=1)
        ax.set(xlabel="Prediction minus truth", ylabel="Query count")
        title(ax, "efgh"[i] + "  Signed errors")
    save(fig, "corrected_c_distributions")

    quench = json.loads(
        (
            ROOT / "workstreams/flagship_tasks/reports/research-extension-20261014/analysis.json"
        ).read_text(encoding="utf-8")
    )["quench"]
    fig, axs = plt.subplots(1, 3, figsize=(9.1, 3.4), layout="constrained")
    axs[0].bar(
        ["Both valid", "Absent fails", "Present fails"], [75, 5, 10], color=[GREEN, GREY, ORANGE]
    )
    axs[0].set_ylabel("Pairs")
    axs[0].tick_params(axis="x", labelsize=7)
    title(axs[0], "a  All 90 matched pairs")
    for i, metric in enumerate(("crystal_fines_fraction", "crystal_yield")):
        vals = [w["mean_present_minus_absent"][metric] for w in quench["by_world"].values()]
        axs[1].scatter([i] * 5, vals, color=[ORANGE, BLUE][i], s=30)
        axs[1].plot([i - 0.15, i + 0.15], [np.mean(vals)] * 2, color=GREY)
    axs[1].set(xticks=[0, 1], xticklabels=["Fines", "Recovery"], ylabel="Present minus absent")
    title(axs[1], "b  Five world means")
    axs[2].bar(["Absent", "Present"], [34, 4], color=[BLUE, ORANGE])
    axs[2].set(ylabel="Joint successes / 75 complete pairs", ylim=(0, 75))
    title(axs[2], "c  Physical consequence")
    save(fig, "quench_control")


if __name__ == "__main__":
    main()
