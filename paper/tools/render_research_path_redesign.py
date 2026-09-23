"""Connect retained C experiments to the original agent's public K1/Q/K2 accounts."""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Patch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto"
PREVIOUS = ROOT / "output/figures/research-case-v16/data.json"
OUT = ROOT / "output/figures/research-path-redesign"
INK, MUTED, GRID = "#34434C", "#697781", "#E5E9EC"
COLORS = ("#607D95", "#337F89")
FAIL = "#BA8066"
REFERENCE = {"Q07": 0.35005782200125907, "Q08": 1.0}


def public_accounts(source_text, budget):
    stages = {}
    for name in ("K1", "Q", "K2"):
        match = re.search(
            rf"^## {name}\s*\n```json\s*\n(.*?)\n```", source_text, re.M | re.S
        )
        retained = json.loads(match.group(1))
        assert retained["failure"] is None
        stages[name] = retained["payload"]
    if budget == 12:
        interpretation = (
            "Deeper cooling raises recovery but promotes\n"
            "nucleation and narrows the fines margin."
        )
        uncertainty = (
            "Batch 12 has better particle quality; its\n"
            "recovery gap to batch 10 remains unresolved."
        )
        critique = (
            "Preferential fines dissolution was untested;\n"
            "heating could erase the crystal population."
        )
        proposed = "Repeat the selected recipe, adding a quench\nbefore seeding."
        exact = {
            "K1_interpretation": (
                "This is the central recovery–quality tradeoff: deeper cooling increased "
                "thermodynamic recovery but also increased nucleation and approached the fines limit."
            ),
            "K1_uncertainty": (
                "The 0.007 recovery difference between batches 10 and 12 is therefore not "
                "statistically resolved by single measurements."
            ),
            "Q_rationale": (
                "The heat cycle should dissolve fines and improve size distribution and purity, "
                "but its short recooling period may not restore all dissolved product."
            ),
            "K2_critique": (
                "Consequently, my sealed estimates for its surviving particles, recovery, size "
                "improvement, and reduced fines depend on an unverified assumption that heating "
                "preferentially dissolves fines without fully erasing the crystal population."
            ),
        }
    else:
        interpretation = (
            "Slower cooling alone was insufficient;\n"
            "upstream chemistry and cooling must be coupled."
        )
        uncertainty = (
            "Seed conditioning was not directly measured;\n"
            "batches 22–24 suggest a recovery plateau."
        )
        critique = (
            "Batch 8’s null result was underused; even\n"
            "the sign of the reheating forecast is uncertain."
        )
        proposed = "Keep the upstream recipe; replace staged\ncooling with direct cooling to 250 K."
        exact = {
            "K1_interpretation": (
                "Therefore the major revision was not simply “cool more slowly”; it was to "
                "combine favorable upstream composition, high-temperature seeding, staged "
                "removal of supersaturation, and a final low-temperature growth/ripening hold."
            ),
            "K1_uncertainty": (
                "This interpretation is consistent with the data but seed survival or partial "
                "dissolution was not directly measured."
            ),
            "Q_rationale": (
                "Q07–Q08: the 315 K temperature cycle is expected to dissolve preferentially "
                "small particles and improve size and fines, at the cost of unrecovered "
                "dissolved product after the relatively fast recool."
            ),
            "K2_critique": (
                "I mentioned this negative result but still treated thermal cycling mainly "
                "through the favorable textbook mechanism of preferential fines dissolution."
            ),
        }
    k2 = stages["K2"]["report"]
    exact["K2_proposed"] = k2[k2.index("I would repeat"):].split("\n\n")[0]
    for name, quote in exact.items():
        stage = name.split("_")[0]
        original = stages[stage]["rationale" if stage == "Q" else "report"]
        assert quote in original, (budget, name)
    return {
        "interpretation": interpretation,
        "uncertainty": uncertainty,
        "critique": critique,
        "proposed": proposed,
        "exact_excerpts": exact,
        "forecast": {
            r["query_id"]: r["crystal_fines_fraction"]
            for r in stages["Q"]["predictions"] if r["query_id"] in REFERENCE
        },
        "timing": "Experiments and sealed recommendation -> K1 -> sealed Q -> K2; no target feedback.",
    }


def prepare():
    retained = json.loads((SOURCE / "summary.json").read_text(encoding="utf-8"))
    previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))["pair"]
    result = []
    for old in previous:
        text = (ROOT / old["source"]).read_text(encoding="utf-8")
        batches = {
            int(n): json.loads(raw)
            for n, raw in re.findall(
                r"^## Batch (\d+)\s*\n```json\s*\n(.*?)\n```", text, re.M | re.S
            )
        }
        rr = next(r for r in retained["results"] if r["id"] == old["session"])
        retest = rr["recommendation_retest"]
        assert retest["passed"] and len(retest["batches"]) == 1
        selected = rr["recommendation"]["selected_experiment_index"]
        assert selected == old["best_feasible_batch"]
        for row in old["rows"]:
            metrics = batches[row["batch"]]["metrics"]
            for key, metric in (
                ("recovery_pct", "crystal_yield"),
                ("purity_pct", "crystal_purity"),
                ("fines_pct", "crystal_fines_fraction"),
            ):
                assert abs(row[key] - 100 * metrics[metric]) < 1e-10
        actions = rr["recommendation_recipe"]["actions"]
        assert actions == retest["batches"][0]["actions"]
        public = public_accounts(text, old["budget"])
        contrast = next(
            c for c in rr["prediction_evaluation"]["contrasts"]
            if c["factor"] == "thermal_history" and c["metric"] == "crystal_fines_fraction"
        )
        assert abs(REFERENCE["Q08"] - REFERENCE["Q07"] - contrast["true_delta"]) < 1e-12
        assert abs(
            public["forecast"]["Q08"]["estimate"] - public["forecast"]["Q07"]["estimate"]
            - contrast["predicted_delta"]
        ) < 1e-12
        result.append(
            {
                **old,
                "selected": selected,
                "selected_metrics": batches[selected]["metrics"],
                "selected_actions": actions,
                "retest_metrics": retest["batches"][0]["metrics"],
                "excluded_attempts": rr["recommendation_recipe"]["excluded_rejected_attempts"],
                "public_accounts": public,
                "withheld_reference": REFERENCE,
                "transitions": {
                    str(n): batches[n] for n in ([9, 10] if old["budget"] == 12 else [19, 20])
                },
            }
        )
    assert [r["completed_batches"] for r in result] == [12, 24]
    assert [r["first_feasible_batch"] for r in result] == [1, 20]
    assert [r["selected"] for r in result] == [10, 23]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "data.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Original public accounts used in the thinking-inclusive preview", "",
        "Displayed figure text is condensed by the authors, not a verbatim quotation. "
        "The exact supporting excerpts below are checked against the retained source reports. "
        "K1 follows research; Q is sealed before K2. Neither Q nor K2 receives target feedback.", "",
    ]
    for row in result:
        lines.extend([f"## {row['budget']}-batch session", "",
                      f"[Retained report](../../../{row['source']})", ""])
        for name, quote in row["public_accounts"]["exact_excerpts"].items():
            lines.extend([f"### {name.replace('_', ' ')}", "", f"> {quote}", ""])
        lines.extend(["### Original fines forecasts", "",
                      "| Query | Estimate | Original 80% interval | Withheld reference |",
                      "|---|---:|---:|---:|"])
        for name, values in row["public_accounts"]["forecast"].items():
            lines.append(
                f"| {name} | {100 * values['estimate']:g}% | "
                f"[{100 * values['lower80']:g}%, {100 * values['upper80']:g}%] | "
                f"{100 * REFERENCE[name]:.5f}% |"
            )
        lines.append("")
    (OUT / "PUBLIC_ACCOUNTS.md").write_text("\n".join(lines), encoding="utf-8")
    return result


def thermal(actions):
    heat = next(a for a in actions if a["operation"] == "heat")
    cool = [a["target_temperature_K"] for a in actions if a["operation"] == "cool_crystallize"]
    return heat, cool


def style(ax):
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.spines["left"].set_color("#ADB8BE")
    ax.tick_params(length=0, pad=7)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def draw(data):
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 16,
            "font.weight": "normal",
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.linewidth": 0.7,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
        }
    )
    fig = plt.figure(figsize=(14.4, 15.2), facecolor="white")

    def text(x, y, label, size=16, color=INK, **kwargs):
        return fig.text(x, y, label, fontsize=size, color=color, **kwargs)

    def panel(letter, y, title):
        text(0.025, y, letter, size=21.5, weight="bold")
        text(0.052, y, title, size=18)

    panel("a", 0.975, "Two independent research trajectories in the same world")
    handles = [
        Line2D([], [], marker="o", ls="none", color=COLORS[0], label="Quality-feasible"),
        Line2D([], [], marker="x", ls="none", color=FAIL, label="Quality-infeasible"),
        Line2D([], [], color=COLORS[0], lw=1.5, label="Best feasible recovery"),
    ]
    fig.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(0.047, 0.946),
        frameon=False,
        ncol=3,
        fontsize=15,
        columnspacing=2.2,
    )
    for i, row in enumerate(data):
        color, x = COLORS[i], 0.078 + i * 0.49
        text(x, 0.914, f"{row['budget']}-batch session", color=color, size=17)
        ax = fig.add_axes([x, 0.747, 0.39, 0.151])
        style(ax)
        good = [r for r in row["rows"] if r["quality_feasible"]]
        bad = [r for r in row["rows"] if not r["quality_feasible"]]
        ax.scatter(
            [r["batch"] for r in good],
            [r["recovery_pct"] for r in good],
            s=31,
            color=color,
            zorder=3,
        )
        ax.scatter(
            [r["batch"] for r in bad],
            [r["recovery_pct"] for r in bad],
            s=34,
            marker="x",
            color=FAIL,
            linewidths=1.05,
            zorder=3,
        )
        valid = [r for r in row["rows"] if r["best_feasible_recovery_pct"] is not None]
        ax.step(
            [r["batch"] for r in valid],
            [r["best_feasible_recovery_pct"] for r in valid],
            where="post",
            color=color,
            lw=1.7,
        )
        selected = next(r for r in row["rows"] if r["batch"] == row["selected"])
        ax.scatter(
            [row["selected"]],
            [selected["recovery_pct"]],
            s=85,
            facecolor="none",
            edgecolor=color,
            linewidths=1.3,
            zorder=4,
        )
        ax.set(xlim=(0.5, row["budget"] + 0.7), ylim=(0, 68), ylabel="Recovery (%)")
        ax.set_yticks([0, 20, 40, 60])
        ax.set_xticks([1, 4, 8, 12] if i == 0 else [1, 4, 8, 12, 16, 20, 24])
        ax.set_xlabel("Batch", labelpad=7)
        ax.annotate(
            f"Selected: batch {row['selected']}",
            (row["selected"], selected["recovery_pct"]),
            xytext=(4.9 if i == 0 else 10.2, 62),
            fontsize=14,
            arrowprops={"arrowstyle": "-", "color": color, "lw": 0.8},
        )
        text(
            x,
            0.697,
            f"{row['feasible_batches']}/{row['budget']} feasible; "
            f"first feasible at batch {row['first_feasible_batch']}",
            size=15,
            color=MUTED,
        )

    panel("b", 0.659, "Recorded changes between successive experiments")
    for i, row in enumerate(data):
        x, color = 0.052 + i * 0.50, COLORS[i]
        indices = [9, 10] if i == 0 else [19, 20]
        before, after = [row["transitions"][str(n)] for n in indices]
        hb, cb = thermal(before["actions"])
        ha, ca = thermal(after["actions"])
        text(
            x,
            0.628,
            f"{row['budget']} batches: experiment {indices[0]} → {indices[1]}",
            size=17,
            color=color,
        )
        heat_string = f"Heat: {hb['target_temperature_K']} K, {hb['duration_s'] / 60:g} min" + (
            " (unchanged)"
            if hb == ha
            else f" → {ha['target_temperature_K']} K, {ha['duration_s'] / 60:g} min"
        )
        text(x, 0.599, heat_string, size=15.3, color=MUTED if hb == ha else INK)
        if i == 0:
            text(x, 0.574, f"Cooling endpoint: {cb[0]} K → {ca[0]} K", size=17, color=color)
            text(x, 0.550, "Other process settings unchanged", size=15, color=MUTED)
        else:
            text(x, 0.574, f"Cooling: direct {cb[0]} K → staged targets", size=17, color=color)
            text(x, 0.550, " → ".join(str(v) for v in ca) + " K", size=17, color=color)
        for k, (label, metric) in enumerate(
            (("Recovery", "crystal_yield"), ("Fines", "crystal_fines_fraction"))
        ):
            start, end = (100 * v["metrics"][metric] for v in (before, after))
            text(x + 0.229 * k, 0.517, f"{label}: {start:.1f}% → {end:.1f}%", size=16)
        text(
            x,
            0.490,
            "Feasible → feasible" if i == 0 else "Infeasible → first feasible",
            color=color,
            size=15,
        )

    panel("c", 0.444, "The final selected procedures")
    for i, row in enumerate(data):
        color, y = COLORS[i], 0.398 - i * 0.072
        actions = row["selected_actions"]
        heat, cool = thermal(actions)
        solvent = next(a["solvent"] for a in actions if a["operation"] == "add_solvent")
        catalyst = next(a["catalyst"] for a in actions if a["operation"] == "add_catalyst")
        seed = next(a["seed_mass_g"] * 1000 for a in actions if a["operation"] == "seed_crystals")
        wait = next(a["duration_s"] / 3600 for a in actions if a["operation"] == "wait")
        quenched = any(a["operation"] == "quench" for a in actions)
        text(
            0.052,
            y + 0.008,
            f"{row['budget']} batches\nBatch {row['selected']}",
            size=15,
            color=color,
            linespacing=1.55,
            va="center",
        )
        nodes = [
            f"Charge\nS{solvent} / C{catalyst}",
            f"Heat\n{heat['target_temperature_K']} K · {heat['duration_s'] / 60:g} min",
            "Quench" if quenched else "No quench",
            f"Seed\n{seed:g} mg",
            "Cool\n" + " → ".join(str(v) for v in cool) + " K",
            f"Hold\n{wait:g} h",
            "Filter\n+ assay",
        ]
        centers = [0.208, 0.341, 0.474, 0.58, 0.727, 0.87, 0.95]
        widths = [0.085, 0.125, 0.098, 0.070, 0.186, 0.054, 0.079]
        for j, (cx, width, label) in enumerate(zip(centers, widths, nodes, strict=True)):
            if j != 2 or quenched:
                fig.add_artist(
                    Rectangle(
                        (cx - width / 2, y - 0.014),
                        width,
                        0.047,
                        transform=fig.transFigure,
                        facecolor="white",
                        edgecolor="#B7C3CA",
                        lw=0.7,
                    )
                )
            text(
                cx,
                y + 0.008,
                label,
                size=14 if j == 4 else 15,
                ha="center",
                va="center",
                color=MUTED if j == 2 and not quenched else INK,
                linespacing=1.5,
            )
            if j < len(nodes) - 1:
                fig.add_artist(
                    FancyArrowPatch(
                        (cx + width / 2 + 0.001, y + 0.008),
                        (centers[j + 1] - widths[j + 1] / 2 - 0.001, y + 0.008),
                        transform=fig.transFigure,
                        arrowstyle="-|>",
                        mutation_scale=9,
                        color="#8D9CA6",
                        linewidth=0.8,
                    )
                )

    panel("d", 0.272, "Selected-batch observations and independent retests")
    fig.legend(
        handles=[
            Patch(facecolor="white", edgecolor=MUTED, label="Source observation"),
            Patch(facecolor=MUTED, label="Independent retest"),
        ],
        loc="center left",
        bbox_to_anchor=(0.047, 0.241),
        ncol=2,
        frameon=False,
        fontsize=15,
        columnspacing=2,
    )
    for col, (metric, label, limit, ticks) in enumerate(
        (
            ("crystal_yield", "Recovery (%)", 70, [0, 20, 40, 60]),
            ("crystal_fines_fraction", "Fines (%) · limit ≤ 50%", 65, [0, 20, 40, 60]),
            ("crystal_purity", "Purity (%) · limit ≥ 80%", 115, [0, 50, 100]),
        )
    ):
        ax = fig.add_axes([0.078 + 0.32 * col, 0.056, 0.247, 0.143])
        style(ax)
        for i, row in enumerate(data):
            color = COLORS[i]
            vals = [100 * row[k][metric] for k in ("selected_metrics", "retest_metrics")]
            for j, val in enumerate(vals):
                bar = ax.bar(
                    i + (-0.17 if j == 0 else 0.17),
                    val,
                    width=0.29,
                    color="white" if j == 0 else color,
                    edgecolor=color,
                    linewidth=1.1,
                )
                ax.bar_label(bar, labels=[f"{val:.1f}"], size=13.7, padding=4)
        ax.set(ylim=(0, limit), xlim=(-0.6, 1.6))
        ax.set_yticks(ticks)
        ax.set_title(label, fontsize=16, loc="left", pad=11)
        ax.set_xticks([0, 1], ["12 batches", "24 batches"], fontsize=14)
        if metric in ("crystal_fines_fraction", "crystal_purity"):
            threshold = 50 if metric == "crystal_fines_fraction" else 80
            ax.axhline(threshold, color="#8D9CA6", lw=0.8, linestyle=(0, (3, 3)), zorder=0)
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"figure02-research-paths-preview.{ext}", dpi=230)
    plt.close(fig)


if __name__ == "__main__":
    data = prepare()
    draw(data)
    print(
        "Preview: 36 source batches, two selected canonical recipes, two retained retests verified."
    )
