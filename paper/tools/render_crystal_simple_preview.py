"""Redraw retained crystallization results as direct comparisons; no new data."""

# Chinese editorial notes intentionally use Chinese punctuation.
# ruff: noqa: RUF001

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto"
    / "BASELINE_REANALYSIS.json"
)
OUT = ROOT / "output/figures/crystal-simple-preview"
INK, MUTED = "#34434C", "#63717B"
OBSERVED, REFERENCE, AGENT = "#8F9EA8", "#C9D1D7", "#347F8A"


def summarize(rows):
    result = {}
    for budget in (None, 12, 24):
        rr = [r for r in rows if budget is None or r["budget"] == budget]
        group = {"campaigns": len(rr)}
        for metric in ("crystal_yield", "crystal_purity"):
            agent = [100 * r["agent_mae"][metric] for r in rr]
            baseline = [100 * r["public_baselines"]["mae"]["public_mean"][metric] for r in rr]
            group[metric] = {
                "agent_mae_pp": fmean(agent),
                "observed_mean_mae_pp": fmean(baseline),
                "agent_better": sum(a < b for a, b in zip(agent, baseline, strict=True)),
                "baseline_better": sum(b < a for a, b in zip(agent, baseline, strict=True)),
            }
        group["purity_levels_percent"] = {
            field: 100 * fmean(r["response_diagnostics"]["crystal_purity"][field] for r in rr)
            for field in ("source_observed_mean", "reference_mean", "prediction_mean")
        }
        result["all" if budget is None else str(budget)] = group
    result["purity_forecasts_below_reference"] = sum(
        r["response_diagnostics"]["crystal_purity"]["underestimated_queries"] for r in rows
    )
    result["purity_forecasts"] = sum(
        r["response_diagnostics"]["crystal_purity"]["queries"] for r in rows
    )
    result["retained_source_shortfalls"] = [r["id"] for r in rows if not r["conforming"]]
    return result


def export_details(rows, summary):
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    details = []
    for r in rows:
        row = {k: r[k] for k in ("id", "world", "arm", "budget", "conforming")}
        for metric in ("crystal_yield", "crystal_purity"):
            row[f"{metric}_agent_mae_pp"] = r["agent_mae"][metric] * 100
            row[f"{metric}_baseline_mae_pp"] = (
                r["public_baselines"]["mae"]["public_mean"][metric] * 100
            )
        for key, value in r["response_diagnostics"]["crystal_purity"].items():
            row[f"purity_{key}"] = json.dumps(value) if isinstance(value, list) else value
        details.append(row)
    with (OUT / "campaign-details.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(details[0]))
        writer.writeheader()
        writer.writerows(details)


def style_axis(ax, maximum, step):
    ax.set_xlim(0, maximum)
    ax.xaxis.set_major_locator(MultipleLocator(step))
    ax.set_yticks([])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#A9B4BB")
    ax.tick_params(axis="x", length=3, pad=7)
    ax.grid(axis="x", color="#E5E9EC", linewidth=0.65)
    ax.set_axisbelow(True)


def draw(summary):
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 11,
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
    fig = plt.figure(figsize=(14.4, 5.5), facecolor="white")
    left = fig.add_axes([0.19, 0.16, 0.27, 0.67])
    right = fig.add_axes([0.685, 0.16, 0.27, 0.67])
    fig.text(0.026, 0.925, "a", fontsize=21.5, weight="bold")
    fig.text(0.052, 0.925, "Purity: observed and predicted", fontsize=14.2)
    fig.text(0.517, 0.925, "b", fontsize=21.5, weight="bold")
    fig.text(0.543, 0.925, "Prediction error on new conditions", fontsize=14.2)

    levels = summary["all"]["purity_levels_percent"]
    values = [
        levels["source_observed_mean"],
        levels["reference_mean"],
        summary["12"]["purity_levels_percent"]["prediction_mean"],
        summary["24"]["purity_levels_percent"]["prediction_mean"],
    ]
    labels = [
        "Observed in research\n30 campaigns",
        "Actual in blind tests\n30 campaigns",
        "Agent: 12-batch budget\n15 campaigns",
        "Agent: 24-batch budget\n15 campaigns",
    ]
    positions = [3.5, 2.55, 1.3, 0.35]
    style_axis(left, 100, 25)
    left.set_ylim(-0.25, 4.25)
    for y, value, color, label in zip(
        positions, values, [OBSERVED, REFERENCE, AGENT, AGENT], labels, strict=True
    ):
        left.barh(y, value, height=0.50, color=color, linewidth=0)
        left.text(
            -0.045,
            y,
            label,
            transform=left.get_yaxis_transform(),
            ha="right",
            va="center",
            fontsize=11,
            linespacing=1.5,
        )
        left.text(
            value - 2,
            y,
            f"{value:.2f}%",
            color="white" if color == AGENT else INK,
            ha="right",
            va="center",
            fontsize=12,
        )
    left.set_xlabel("Mean crystal purity (%)", labelpad=10)

    style_axis(right, 20, 5)
    right.set_ylim(-0.25, 4.25)
    for metric, group_y, label in [
        ("crystal_yield", 3.5, "Recovery"),
        ("crystal_purity", 1.05, "Purity"),
    ]:
        group = summary["all"][metric]
        winner = (
            f"Agent better in {group['agent_better']}/30 campaigns"
            if metric == "crystal_yield"
            else f"Observed mean better in {group['baseline_better']}/30 campaigns"
        )
        right.text(-0.61, group_y + 0.55, label, transform=right.get_yaxis_transform(), fontsize=12)
        right.text(
            0.0,
            group_y + 0.55,
            winner,
            transform=right.get_yaxis_transform(),
            fontsize=10.5,
            color=MUTED,
        )
        for y, key, color, name in [
            (group_y, "observed_mean_mae_pp", OBSERVED, "Repeat observed mean"),
            (group_y - 0.72, "agent_mae_pp", AGENT, "Agent"),
        ]:
            val = group[key]
            right.barh(y, val, height=0.48, color=color, linewidth=0)
            right.text(
                -0.045,
                y,
                name,
                transform=right.get_yaxis_transform(),
                ha="right",
                va="center",
                fontsize=10.7,
            )
            right.text(val + 0.3, y, f"{val:.2f}", ha="left", va="center", fontsize=12)
    right.set_xlabel(
        "Mean absolute error (percentage points)\nLower is better", labelpad=10, linespacing=1.5
    )
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"crystal-direct-comparison.{ext}", dpi=200)
    plt.close(fig)


def write_readme(summary):
    s = summary
    lines = [
        "# Figure 6: direct comparison preview",
        "",
        "This is a display revision of retained data, not a new experiment. "
        "The manuscript and PowerPoint bindings have not yet been changed.",
        "",
        "![Direct comparison](crystal-direct-comparison.png)",
        "",
        "## 为什么改成这样",
        "",
        "原图的上半部比较纯度，下半部却要求读者解释模型减基线的误差差值；散点的偏移又没有科学含义。"
        "新版只保留两个直接问题：a，实验测到的纯度和模型预测是否一致？b，模型预测比重复此前均值更准吗？"
        "所有条形从零开始，直接标注数值，不用截断坐标夸大约四个百分点的纯度差异。",
        "",
        "经验基线在每个研究会话内独立计算：取该会话已经公开的终检结果的均值，对所有新配方都预测这个值。"
        "例如此前平均纯度为98.5%，后续每道纯度题就预测98.5%。它不访问隐藏答案，也不增加实验。",
        "",
        "## Caption draft",
        "",
        "**Crystallization forecasts improve recovery prediction "
        "but underestimate stable purity.** "
        "**a,** Mean crystal purity measured during research and in withheld reference outcomes "
        "(30 campaigns each), compared with agent forecasts from the 12- and 24-batch campaigns "
        "(15 campaigns each). Each bar equally weights the corresponding campaign means. "
        f"Across the original queries, {s['purity_forecasts_below_reference']} "
        f"of {s['purity_forecasts']} "
        "purity point forecasts lie below their withheld reference means. "
        "**b,** Mean absolute prediction error against the withheld references, averaged over "
        "all 30 campaigns, for recovery and purity. The observation-mean baseline predicts "
        "the mean of the same campaign's public final assays for every withheld recipe; "
        "it uses no additional experiments or withheld outcomes. Agent recovery error is lower "
        "in 26/30 campaigns; the observation-mean purity error is lower in 30/30. "
        "The campaigns comprise five reused worlds, three information arms and two budgets; "
        "they are not thirty independent worlds. The source-assay shortfall is retained. "
        "Bars are descriptive means, not confidence intervals. The tested purity stability "
        "and baseline advantage do not establish a mechanism "
        "or a general rule to copy observations.",
        "",
        "## Budget details (all retained campaigns)",
        "",
        "| Budget | Campaigns | Recovery: agent MAE (pp) | Recovery: baseline MAE (pp) "
        "| Purity: agent MAE (pp) | Purity: baseline MAE (pp) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for key in ("12", "24", "all"):
        group = s[key]
        a, b = group["crystal_yield"], group["crystal_purity"]
        lines.append(
            f"| {key} | {group['campaigns']} | {a['agent_mae_pp']:.4f} "
            f"| {a['observed_mean_mae_pp']:.4f} | {b['agent_mae_pp']:.4f} "
            f"| {b['observed_mean_mae_pp']:.4f} |"
        )
    lines.extend(
        [
            "",
            "All 30 campaign values, arm identities, source ranges, prediction ranges and the "
            "source-shortfall flag remain in [campaign-details.csv](campaign-details.csv). "
            "Aggregates are also available in [summary.json](summary.json). "
            "The figure does not display individual forecast intervals "
            "or infer sampling uncertainty.",
            "",
            "Source: [retained baseline reanalysis](../../../workstreams/flagship_tasks/reports/"
            "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json).",
            "",
            "Rebuild: `uv run --no-sync python paper/tools/render_crystal_simple_preview.py`.",
            "",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    rows = json.loads(SOURCE.read_text(encoding="utf-8"))["rows"]
    previous = json.loads(
        (ROOT / "paper/figures/academic-ppt/retained-figure-data.json").read_text(encoding="utf-8")
    )["crystal"]
    assert rows == previous, "Retained figure export differs from its source reanalysis"
    expected = {
        (f"W{i:02d}", a, b)
        for i in range(1, 6)
        for a in ("Opaque", "Aligned", "MisIndexed")
        for b in (12, 24)
    }
    assert len(rows) == 30 and {(r["world"], r["arm"], r["budget"]) for r in rows} == expected
    summary = summarize(rows)
    assert summary["all"]["crystal_yield"]["agent_better"] == 26
    assert summary["all"]["crystal_purity"]["baseline_better"] == 30
    assert summary["purity_forecasts"] == 360 and summary["purity_forecasts_below_reference"] == 335
    assert summary["retained_source_shortfalls"] == ["C-W02-B12-E-Opaque"]
    OUT.mkdir(parents=True, exist_ok=True)
    export_details(rows, summary)
    draw(summary)
    write_readme(summary)
    print(
        "Rendered direct comparisons: 30/30 campaigns; 360 forecasts; retained source shortfall: 1."
    )


if __name__ == "__main__":
    main()
