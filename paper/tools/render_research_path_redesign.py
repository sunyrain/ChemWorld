"""Connect retained C experiments to the original agent's public K1/Q/K2 accounts."""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto"
PREVIOUS = ROOT / "output/figures/research-case-v16/data.json"
OUT = ROOT / "output/figures/research-path-redesign"
INK, MUTED, GRID = "#34434C", "#697781", "#E5E9EC"
COLORS = ("#607D95", "#337F89")
FAIL = "#BA8066"
# Retained W05 qualification queries, noise-free fines; never shown to the agent.
REFERENCE = {"Q07": 0.35005782200125907, "Q08": 1.0}


def public_accounts(source_text, budget):
    stages = {}
    for name in ("K1", "Q", "K2"):
        match = re.search(rf"^## {name}\s*\n```json\s*\n(.*?)\n```", source_text, re.M | re.S)
        retained = json.loads(match.group(1))
        assert retained["failure"] is None
        stages[name] = retained["payload"]
    if budget == 12:
        interpretation = (
            "Deeper cooling raises recovery but promotes\nnucleation and narrows the fines margin."
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
                "This is the central recovery\u2013quality tradeoff: deeper cooling increased "
                "thermodynamic recovery but also increased nucleation "
                "and approached the fines limit."
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
            "batches 22\u201324 suggest a recovery plateau."
        )
        critique = (
            "Batch 8\u2019s null result was underused; even\n"
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
            "K1_plateau": (
                "Batch 23 remains the sealed recommendation, but the evidence supports a "
                "broad near-optimal plateau rather than a precisely located temperature optimum."
            ),
            "Q_rationale": (
                "Q07\u2013Q08: the 315 K temperature cycle is expected to dissolve preferentially "
                "small particles and improve size and fines, at the cost of unrecovered "
                "dissolved product after the relatively fast recool."
            ),
            "K2_critique": (
                "I mentioned this negative result but still treated thermal cycling mainly "
                "through the favorable textbook mechanism of preferential fines dissolution."
            ),
            "K2_uncertainty": (
                "Thus even the sign of its fines change relative to Q07 is uncertain."
            ),
        }
    k2 = stages["K2"]["report"]
    exact["K2_proposed"] = k2[k2.index("I would repeat") :].split("\n\n")[0]
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
            for r in stages["Q"]["predictions"]
            if r["query_id"] in REFERENCE
        },
        "timing": (
            "Experiments and sealed recommendation -> K1 -> sealed Q -> K2; no target feedback."
        ),
    }


def prepare():
    retained = json.loads((SOURCE / "summary.json").read_text(encoding="utf-8"))
    reference_path = (
        ROOT
        / "runs/formal/work-ii-c-five-world-20260920-v3-auto/qualification"
        / "W05/queries/result.json"
    )
    if reference_path.exists():
        original = json.loads(reference_path.read_text(encoding="utf-8"))
        for index, name in ((6, "Q07"), (7, "Q08")):
            assert original["truth"][index]["crystal_fines_fraction"] == REFERENCE[name]
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
            c
            for c in rr["prediction_evaluation"]["contrasts"]
            if c["factor"] == "thermal_history" and c["metric"] == "crystal_fines_fraction"
        )
        assert abs(REFERENCE["Q08"] - REFERENCE["Q07"] - contrast["true_delta"]) < 1e-12
        assert (
            abs(
                public["forecast"]["Q08"]["estimate"]
                - public["forecast"]["Q07"]["estimate"]
                - contrast["predicted_delta"]
            )
            < 1e-12
        )
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
        "# Original public accounts used in the thinking-inclusive preview",
        "",
        "Displayed figure text is condensed by the authors, not a verbatim quotation. "
        "The exact supporting excerpts below are checked against the retained source reports. "
        "K1 follows research; Q is sealed before K2. Neither Q nor K2 receives target feedback.",
        "",
    ]
    for row in result:
        lines.extend(
            [
                f"## {row['budget']}-batch session",
                "",
                f"[Retained report](../../../{row['source']})",
                "",
            ]
        )
        for name, quote in row["public_accounts"]["exact_excerpts"].items():
            lines.extend([f"### {name.replace('_', ' ')}", "", f"> {quote}", ""])
        lines.extend(
            [
                "### Original fines forecasts",
                "",
                "| Query | Estimate | Original 80% interval | Withheld reference |",
                "|---|---:|---:|---:|",
            ]
        )
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
    fig = plt.figure(figsize=(14.4, 16.0), facecolor="white")

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

    for i, row in enumerate(data):
        retest = row["retest_metrics"]
        text(
            0.078 + i * 0.49,
            0.672,
            f"Retest: recovery {100 * retest['crystal_yield']:.1f}%; "
            f"fines {100 * retest['crystal_fines_fraction']:.1f}%",
            size=15,
            color=COLORS[i],
        )

    panel("b", 0.630, "Agent\u2019s mechanistic interpretation (K1, after research)")
    for i, row in enumerate(data):
        x, color = 0.052 + i * 0.50, COLORS[i]
        account = row["public_accounts"]
        if i == 0:
            observed = [row["rows"][n - 1] for n in (8, 10)]
            first, last = observed
            evidence = "Deeper cooling: 270 → 250 K (batches 8\u201310)"
        else:
            first, last = [row["rows"][n - 1] for n in (19, 20)]
            evidence = "Hotter heating + staged cooling (batches 19\u201320)"
        text(x, 0.599, evidence, size=16, color=color)
        text(
            x,
            0.576,
            f"Recovery {first['recovery_pct']:.1f} → {last['recovery_pct']:.1f}%; "
            f"fines {first['fines_pct']:.1f} → {last['fines_pct']:.1f}%",
            size=15.5,
            color=MUTED,
        )
        text(x, 0.543, account["interpretation"], size=17, linespacing=1.45, va="top")
        text(x, 0.485, account["uncertainty"], size=16, color=MUTED, linespacing=1.4, va="top")

    panel("c", 0.428, "Using a mechanistic explanation to predict a new intervention (Q)")
    text(
        0.052,
        0.402,
        "Test: replace a 2-h cold hold with heating toward 315 K for 1 h and recooling for 1 h.",
        size=15.5,
    )
    text(
        0.052,
        0.378,
        "Agent rationale: preferential dissolution of fines. "
        "Error bars: original 80% prediction intervals.",
        size=15.5,
        color=MUTED,
    )
    fig.add_artist(
        Rectangle(
            (0.722, 0.207),
            0.27,
            0.153,
            transform=fig.transFigure,
            facecolor="#F2F4F4",
            edgecolor="none",
            zorder=0,
        )
    )
    for col in range(3):
        color = COLORS[col] if col < 2 else MUTED
        ax = fig.add_axes([0.078 + col * 0.32, 0.233, 0.238, 0.103])
        style(ax)
        if col < 2:
            forecasts = data[col]["public_accounts"]["forecast"]
            values = [100 * forecasts[q]["estimate"] for q in ("Q07", "Q08")]
            errors = [
                [
                    100 * (forecasts[q]["estimate"] - forecasts[q]["lower80"])
                    for q in ("Q07", "Q08")
                ],
                [
                    100 * (forecasts[q]["upper80"] - forecasts[q]["estimate"])
                    for q in ("Q07", "Q08")
                ],
            ]
            ax.errorbar(
                [0, 1],
                values,
                yerr=errors,
                fmt="o-",
                color=color,
                capsize=4,
                elinewidth=1.1,
                linewidth=1.5,
                markersize=5,
            )
            title = f"{data[col]['budget']}-batch agent"
        else:
            values = [100 * REFERENCE[q] for q in ("Q07", "Q08")]
            ax.set_facecolor("#F2F4F4")
            ax.plot([0, 1], values, "s-", color=color, markersize=5, lw=1.5)
            title = "Withheld reference"
        for xx, value in enumerate(values):
            offset = 16 if col == 2 and xx == 0 else 8
            ax.text(xx + 0.07, value + offset, f"{value:.0f}%", fontsize=15, color=color)
        ax.set(xlim=(-0.32, 1.43), ylim=(0, 120))
        ax.set_yticks([0, 50, 100])
        ax.set_xticks([0, 1], ["Cold hold", "Heat + recool"], fontsize=13.5)
        ax.set_title(title, fontsize=16, color=color, loc="left", pad=10)
        if col == 0:
            ax.set_ylabel("Fines (%)", fontsize=15)

    panel("d", 0.176, "Agent\u2019s retrospective critique (K2, without reference feedback)")
    for i, row in enumerate(data):
        x, color = 0.052 + i * 0.50, COLORS[i]
        account = row["public_accounts"]
        text(x, 0.144, account["critique"], size=17, va="top", linespacing=1.4)
        text(x, 0.082, "Proposed next experiment · not executed", size=15, color=color)
        text(x, 0.059, account["proposed"], size=16.5, va="top", linespacing=1.4)
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"figure02-research-paths-preview.{ext}", dpi=230)
    plt.close(fig)


if __name__ == "__main__":
    data = prepare()
    draw(data)
    print(
        "Preview: 36 batches, 2 retests, original K1/Q/K2 excerpts "
        "and 4 forecast intervals verified."
    )
