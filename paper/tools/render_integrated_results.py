"""Render the integrated paper from retained evidence; no experiment execution.

Run from the repository root with uv run --no-sync python
paper/tools/render_integrated_results.py. EQ exports are read at the closure's
explicit Git commit, without checking out or importing that runtime.
"""

from __future__ import annotations

import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
OUT = ROOT / "paper/figures/integrated-results"
ARMS = ("Opaque", "Aligned", "MisIndexed")
COLORS = dict(zip(ARMS, ("#536879", "#167c80", "#c36b3c"), strict=True))
MARKERS = ("o", "s", "^", "D", "v")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_metrics(metrics):
    result = {}
    for name, v in metrics.items():
        result[name] = {
            "mae": v.get("mae", v.get("mae_to_five_repeat_mean")),
            "coverage": v.get("coverage90", v.get("coverage80", v.get("empirical_coverage80"))),
            "width": v.get(
                "mean_width90", v.get("mean_width80", v.get("width80", v.get("interval_width")))
            ),
        }
        assert all(isinstance(x, (int, float)) for x in result[name].values()), (name, v)
    return result


def load_rows():
    closure = read(REPORTS / "work-ii-evidence-closeout-20260921/summary.json")
    ec = read(REPORTS / "work-ii-ec-pa-five-world-en-20260919/completed-block-analysis.json")
    rx = read(REPORTS / "work-ii-rx-ps-five-world-dual-goal-20260919-final/SUMMARY.json")
    rows = []

    def add(identifier, system, locus, goal, budget, arm, world, metrics, **extra):
        rows.append(
            dict(
                id=identifier,
                system=system,
                locus=locus,
                goal=goal,
                budget=budget,
                arm=arm,
                world=world,
                conforming=True,
                nominal=0.9 if system == "PA" else 0.8,
                reference_target=(
                    "noiseless_pre_sampling"
                    if system in ("PA", "C")
                    else "five_repeat_mean_and_observation_coverage"
                    if system in ("RX", "EQ")
                    else "single_seeded_observation"
                ),
                metrics=normalize_metrics(metrics),
                **extra,
            )
        )

    for r in ec["rows"]:
        add(
            r["unit_id"],
            r["system"],
            "E",
            r["goal"],
            r["budget"],
            r["arm"],
            r["world"],
            r["metrics"],
            retest=r.get("retest_score"),
            recovered=r["recovered"],
        )
    for r in rx["cells"]:
        add(
            r["cell_id"],
            "RX",
            r["locus"],
            "discovery" if r["goal"] == "mechanism_discovery" else "optimization",
            12,
            r["arm"],
            r["world_id"],
            r["prediction_evaluation"]["metrics"],
            retest=r["recommendation_retest_score"],
            recovered=r.get("recovered"),
        )
    for r in closure["eq_bounded_p_v2"]["rows"]:
        path = (
            "workstreams/flagship_tasks/reports/"
            "work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/" + r["id"] + "/RESULT.json"
        )
        data = json.loads(
            subprocess.check_output(
                ["git", "show", closure["remote_commit"] + ":" + path], cwd=ROOT
            )
        )
        add(
            r["id"],
            "EQ",
            "P",
            "characterization",
            12,
            r["arm"],
            r["world"],
            data["prediction_evaluation"]["metrics"],
        )
    for r in closure["eq_s_canonical_v03"]["cells"]:
        c = r["cell"]
        add(
            c["cell_id"],
            "EQ",
            "S",
            "characterization",
            12,
            c["arm"],
            c["world_id"],
            r["prediction_evaluation"]["metrics"],
        )
    c_retest = {r["id"]: r for r in closure["c_current"]["descriptive"]["retests"]}
    for r in closure["c_current"]["rows"]:
        t = c_retest[r["id"]]
        add(
            r["id"],
            "C",
            "E",
            "delivery",
            r["budget"],
            r["arm"],
            "-".join(r["id"].split("-")[:2]),
            r["prediction_evaluation"]["metrics"],
            retest=t["recovery"],
            quality_pass=t["quality_pass"],
        )
        rows[-1]["conforming"] = not r["source_nonconformance"]
    for r in closure["p_current"]["results"]:
        t = r["retest_metrics"][0]
        add(
            r["id"],
            "P",
            "E",
            "delivery",
            12,
            r["arm"],
            r["world_id"],
            r["prediction_evaluation"]["metrics"],
            retest=t["recovery"],
            retest_purity=t["purity"],
            quality_pass=int(t["purity"] >= 0.8),
        )
        rows[-1]["conforming"] = r["source_batches"] == 12
    assert len(rows) == 225 and len({r["id"] for r in rows}) == 225
    assert sum(r["conforming"] for r in rows) == 223
    return rows, closure


def save(fig, name):
    fig.savefig(OUT / (name + ".pdf"), bbox_inches="tight")
    fig.savefig(OUT / (name + ".png"), dpi=190, bbox_inches="tight")
    plt.close(fig)


def framework():
    fig, ax = plt.subplots(figsize=(10.7, 4.4))
    ax.set(xlim=(0, 10.7), ylim=(0, 4.4))
    ax.axis("off")

    def box(x, y, w, h, title, body, color="#eef3f5"):
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.08",
                linewidth=0.8,
                edgecolor="#9aadb6",
                facecolor=color,
            )
        )
        ax.text(x + 0.13, y + h - 0.18, title, weight="bold", va="top", fontsize=11)
        ax.text(x + 0.13, y + h - 0.56, body, va="top", fontsize=9.6, linespacing=1.5)

    box(
        0.1,
        2.0,
        2.85,
        2.12,
        "Programmable world",
        "Composable process laws\nPersistent material and samples\n"
        "Instruments and resource costs\nEvaluator-owned private laws",
    )
    box(
        3.43,
        2.0,
        3.7,
        2.12,
        "Autonomous research",
        "Opaque / Aligned / MisIndexed\nTask-specific goals and budgets\n"
        "Agent selects each operation\nObservations inform new choices",
        "#e9f3f0",
    )
    box(
        7.61,
        2.0,
        2.87,
        2.12,
        "Sealed assessment",
        "Seal operating recommendation\nK1: free-form mechanism\n"
        "Q: predict 12 new conditions\nK2: reflect on the evidence",
        "#f9f0e6",
    )
    box(
        0.1,
        0.15,
        4.97,
        1.32,
        "Two distinct controls",
        "Change laws under a matched interface\nOr change dossiers in the same world",
    )
    box(
        5.55,
        0.15,
        4.93,
        1.32,
        "Separate readouts",
        "Prediction error, intervals, and task retests\nLink claims to observed experiments",
    )
    for x1, x2 in [(2.99, 3.37), (7.18, 7.55)]:
        ax.add_patch(
            FancyArrowPatch(
                (x1, 3.05),
                (x2, 3.05),
                arrowstyle="-|>",
                mutation_scale=16,
                color="#415566",
                linewidth=1.3,
            )
        )
    ax.text(
        5.35,
        1.71,
        "Full action-observation history is retained; Q uses the original agent context",
        ha="center",
        fontsize=9.5,
        color="#415566",
    )
    save(fig, "framework")


def goal_pairs(rows, system, metric="score"):
    selected = [r for r in rows if r["system"] == system]
    grouped = defaultdict(dict)
    for r in selected:
        grouped[r["world"], r["locus"], r["budget"], r["arm"]][r["goal"]] = r
    result = []
    for (world, locus, budget, arm), pair in grouped.items():
        d, o = pair["discovery"], pair["optimization"]

        def error(r):
            return (
                r["metrics"][metric]["mae"]
                if metric != "macro"
                else fmean(m["mae"] for m in r["metrics"].values())
            )

        result.append(
            {
                "system": system,
                "world": world,
                "locus": locus,
                "budget": budget,
                "arm": arm,
                "delta_retest": o["retest"] - d["retest"],
                "delta_mae": error(o) - error(d),
                "first_attempt": not d.get("recovered") and not o.get("recovered"),
            }
        )
    return result


def goal_figure(rows):
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.4), layout="constrained")
    for ax, system in zip(axs, ("EC", "RX"), strict=True):
        pairs = goal_pairs(rows, system)
        ax.axhline(0, color="#a4afb5", lw=1)
        ax.axvline(0, color="#a4afb5", lw=1)
        for arm in ARMS:
            for wi in range(1, 6):
                a = [r for r in pairs if r["arm"] == arm and r["world"].endswith(f"{wi:02d}")]
                ax.scatter(
                    [r["delta_retest"] for r in a],
                    [r["delta_mae"] for r in a],
                    c=COLORS[arm],
                    marker=MARKERS[wi - 1],
                    alpha=0.86,
                    s=39,
                    edgecolors="white",
                    linewidths=0.4,
                    label=arm if wi == 1 else None,
                )
        ax.set_xlabel("Change in recommendation retest score")
        ax.set_ylabel("Change in score-prediction MAE")
        n = sum(r["delta_retest"] > 0 and r["delta_mae"] > 0 for r in pairs)
        ax.set_title(
            f"{system}: discovery to optimization\nBetter retest, worse prediction: {n}/30",
            loc="left",
            fontsize=10,
            pad=10,
        )
        ax.legend(frameon=False, fontsize=8, loc="lower left")
    save(fig, "goals")


def budget_figure(rows):
    fig, axs = plt.subplots(1, 4, figsize=(10.6, 3.7), layout="constrained")
    conditions = [
        ("EC", "discovery", "score", "EC discovery"),
        ("EC", "optimization", "score", "EC optimization"),
        ("PA", "discovery", "product_in_organic", "PA partitioning"),
        ("C", "delivery", "crystal_fines_fraction", "C fines fraction"),
    ]
    for ax, (s, g, m, title) in zip(axs, conditions, strict=True):
        subset = [r for r in rows if r["system"] == s and r["goal"] == g]
        group = defaultdict(dict)
        for r in subset:
            group[r["world"], r["arm"]][r["budget"]] = r
        for (_world, arm), pair in group.items():
            ax.plot(
                [12, 24],
                [pair[b]["metrics"][m]["mae"] for b in (12, 24)],
                c=COLORS[arm],
                lw=0.8,
                alpha=0.4,
                marker="o",
                markersize=3,
            )
            for b in (12, 24):
                if not pair[b]["conforming"]:
                    ax.scatter(
                        b, pair[b]["metrics"][m]["mae"], marker="x", c="black", s=60, zorder=4
                    )
        means = [
            fmean(r["metrics"][m]["mae"] for r in subset if r["budget"] == b) for b in (12, 24)
        ]
        ax.plot([12, 24], means, color="#152c3b", lw=2.4, marker="D", ms=5, label="Mean")
        ax.set(
            title=title,
            xticks=[12, 24],
            xlim=(10, 26),
            xlabel="Batch budget",
            ylabel="Prediction MAE",
            ylim=(0, None),
        )
        ax.spines[["top", "right"]].set_visible(False)
    save(fig, "budgets")


def prior_figure(rows):
    panels = [
        ("EC", "E", "discovery", 12, "score"),
        ("EC", "E", "discovery", 24, "score"),
        ("EC", "E", "optimization", 12, "score"),
        ("EC", "E", "optimization", 24, "score"),
        ("PA", "E", "discovery", 12, "product_in_organic"),
        ("PA", "E", "discovery", 24, "product_in_organic"),
        ("RX", "P", "discovery", 12, "macro"),
        ("RX", "S", "discovery", 12, "macro"),
        ("RX", "P", "optimization", 12, "macro"),
        ("RX", "S", "optimization", 12, "macro"),
        ("EQ", "P", "characterization", 12, "macro"),
        ("EQ", "S", "characterization", 12, "macro"),
        ("C", "E", "delivery", 12, "crystal_fines_fraction"),
        ("C", "E", "delivery", 24, "crystal_fines_fraction"),
        ("P", "E", "delivery", 12, "purity"),
        ("P", "E", "delivery", 12, "recovery"),
    ]
    fig, axs = plt.subplots(4, 4, figsize=(7.3, 8.3), layout="constrained")
    for ax, (s, locus, g, b, metric) in zip(axs.flat, panels, strict=True):
        ss = [
            r for r in rows if (r["system"], r["locus"], r["goal"], r["budget"]) == (s, locus, g, b)
        ]

        def val(r, metric=metric):
            return (
                r["metrics"][metric]["mae"]
                if metric != "macro"
                else fmean(v["mae"] for v in r["metrics"].values())
            )

        for world in sorted({r["world"] for r in ss}):
            by_arm = {r["arm"]: r for r in ss if r["world"] == world}
            ax.plot(range(3), [val(by_arm[a]) for a in ARMS], c="#ccd2d6", lw=0.7, zorder=1)
        for i, arm in enumerate(ARMS):
            a = sorted([r for r in ss if r["arm"] == arm], key=lambda r: r["world"])
            for wi, r in enumerate(a):
                ax.scatter(
                    i,
                    val(r),
                    s=20,
                    marker=MARKERS[wi] if r["conforming"] else "x",
                    c=COLORS[arm],
                    zorder=3,
                )
            ax.plot(
                [i - 0.17, i + 0.17], [fmean(map(val, a))] * 2, color=COLORS[arm], lw=2.6, zorder=4
            )
        goal = {
            "discovery": "disc.",
            "optimization": "opt.",
            "characterization": "char.",
            "delivery": "delivery",
        }[g]
        subtitle = {
            "macro": "mean across metrics",
            "score": "score",
            "crystal_fines_fraction": "fines",
            "product_in_organic": "organic fraction",
        }.get(metric, metric)
        ax.set_title(f"{s}/{locus} {goal}, {b} batches\n{subtitle}", fontsize=8.5, loc="left")
        ax.set(xticks=range(3), xticklabels=["O", "A", "M"], xlim=(-0.45, 2.45), ylim=(0, None))
        ax.tick_params(labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
    save(fig, "priors")


def purification_figure(rows):
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.7), layout="constrained")
    ss = [r for r in rows if r["system"] == "P"]
    axs[0].axvline(0.8, color="#89979f", ls="--", lw=1)
    for arm in ARMS:
        a = sorted([r for r in ss if r["arm"] == arm], key=lambda r: r["world"])
        for wi, r in enumerate(a):
            axs[0].scatter(
                r["retest_purity"],
                r["retest"],
                c=COLORS[arm],
                marker=MARKERS[wi] if r["conforming"] else "x",
                s=50,
                label=arm if wi == 0 else None,
            )
        for j, metric in enumerate(("purity", "recovery")):
            offset = (ARMS.index(arm) - 1) * 0.20
            vals = [r["metrics"][metric]["coverage"] for r in a]
            axs[1].scatter([j + offset] * 5, vals, s=24, c=COLORS[arm], alpha=0.65)
            axs[1].plot(
                [j + offset - 0.065, j + offset + 0.065], [fmean(vals)] * 2, c=COLORS[arm], lw=3
            )
    axs[0].set(
        xlabel="Recommended-process purity",
        ylabel="Original-charge recovery",
        title="Quality-constrained delivery",
        xlim=(0, 1),
        ylim=(0, 0.7),
    )
    axs[0].legend(frameon=False, fontsize=8)
    axs[1].axhline(0.8, color="#89979f", ls="--", lw=1, label="Nominal 80%")
    axs[1].set(
        xticks=[0, 1],
        xticklabels=["Purity", "Recovery"],
        ylim=(0, 1.05),
        ylabel="Empirical interval coverage",
        title="Uncertainty remains undercalibrated",
    )
    axs[1].legend(frameon=False, fontsize=8)
    save(fig, "purification")


def export(rows, closure):
    flat = []
    for r in rows:
        for metric, values in r["metrics"].items():
            flat.append(
                {**{k: v for k, v in r.items() if k != "metrics"}, "metric": metric, **values}
            )
    keys = list(dict.fromkeys(k for r in flat for k in r))
    with (OUT / "campaign_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(flat)
    contrasts = {system: goal_pairs(rows, system) for system in ("EC", "RX")}
    contrasts["RX_macro"] = goal_pairs(rows, "RX", "macro")
    counts = {
        key: {
            "pairs": len(a),
            "better_retest": sum(r["delta_retest"] > 0 for r in a),
            "lower_mae": sum(r["delta_mae"] < 0 for r in a),
            "better_retest_worse_prediction": sum(
                r["delta_retest"] > 0 and r["delta_mae"] > 0 for r in a
            ),
        }
        for key, a in contrasts.items()
    }
    assert counts["EC"] == {
        "pairs": 30,
        "better_retest": 26,
        "lower_mae": 14,
        "better_retest_worse_prediction": 13,
    }
    assert counts["RX"] == {
        "pairs": 30,
        "better_retest": 9,
        "lower_mae": 8,
        "better_retest_worse_prediction": 5,
    }
    assert counts["RX_macro"]["lower_mae"] == 6
    groups = defaultdict(list)
    for r in flat:
        groups[r["system"], r["locus"], r["goal"], r["budget"], r["metric"]].append(r)
    names = {
        "electrochemical_selectivity": "Electrochemical selectivity",
        "energy_efficiency": "Energy efficiency",
        "faradaic_efficiency": "Faradaic efficiency",
        "selective_product_yield": "Selective product yield",
        "transport_efficiency": "Transport efficiency",
        "score": "Public score",
        "product_in_organic": "Organic fraction",
        "product_in_aqueous": "Aqueous fraction",
        "crystal_yield": "Net crystal recovery",
        "crystal_purity": "Crystal purity",
        "crystal_size": "Particle-size index",
        "crystal_fines_fraction": "Fines fraction",
        "pH_normalized": "Normalized pH",
        "acid_dissociation_fraction": "Dissociation fraction",
        "precipitation_signal": "Precipitation signal",
    }
    table = [
        "# Appendix B. Complete metric-specific arm means",
        "",
        "Each entry is mean absolute error / empirical interval coverage (%), "
        "averaged over five world sessions. All scheduled sessions are retained, "
        "including the two source-budget shortfalls. PA uses nominal 90% intervals; "
        "all other studies use 80%. Metric scales and reference targets differ across systems. "
        "The machine-readable table includes each campaign's interval width and protocol status.",
        "",
    ]
    last = None
    for (system, locus, goal, budget, metric), a in groups.items():
        group = (system, locus, goal, budget)
        if group != last:
            table += [
                f"## {system}, {locus} prior: {goal}, {budget} batches",
                "",
                "| Readout | Opaque | Aligned | MisIndexed |",
                "|---|---:|---:|---:|",
            ]
            last = group
        cells = []
        for arm in ARMS:
            v = [r for r in a if r["arm"] == arm]
            assert len(v) == 5
            cells.append(
                f"{fmean(r['mae'] for r in v):.4f} / {100 * fmean(r['coverage'] for r in v):.1f}"
            )
        table.append(
            "| "
            + names.get(metric, metric.replace("_", " ").capitalize())
            + " | "
            + " | ".join(cells)
            + " |"
        )
        # Blank lines are inserted at group boundaries below, not between table rows.
    content = "\n".join(table).replace("\n## ", "\n\n## ") + "\n"
    (ROOT / "paper/chemworld_integrated_results_appendix.md").write_text(content, encoding="utf-8")
    summary = {
        "source_snapshot": closure["generated_at"],
        "remote_commit": closure["remote_commit"],
        "scope": closure["current_primary_pool"],
        "goal_counts": counts,
        "goal_contrasts": contrasts,
        "note": "Retained-data descriptive reanalysis. RX score-only goal comparison "
        "added for endpoint alignment; original six-metric macro comparison retained.",
    }
    (OUT / "analysis.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"campaigns": len(rows), "metric_rows": len(flat), "goal_counts": counts}))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    rows, closure = load_rows()
    export(rows, closure)
    framework()
    goal_figure(rows)
    budget_figure(rows)
    prior_figure(rows)
    purification_figure(rows)
    print("Five figures and complete campaign tables rendered from retained results.")


if __name__ == "__main__":
    main()
