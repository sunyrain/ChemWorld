#!/usr/bin/env python
"""Render the final B3 diagnostic from its bound report, without new inference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import render_prior_discovery_figures as style
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter

MODELS = ("gpt", "deepseek")
LABELS = ("GPT-5.6-sol", "DeepSeek-v4-flash")
COLORS = ("#8755A1", "#286B9B")
ARMS = ("opaque", "misindexed_nominal", "aligned_nominal")


def render(report: dict, output: Path) -> None:
    if not report["formal_result"] or not report["execution_complete"]:
        raise ValueError("publication plot requires a terminal formal block")
    style.configure_matplotlib()
    fig, (recovery, effect) = plt.subplots(1, 2, figsize=(7.4, 4.6))
    fig.subplots_adjust(left=0.16, right=0.98, bottom=0.26, top=0.83, wspace=0.95)
    lookup = {(r["model"], r["tool"], r["arm"]): r for r in report["by_prior"]}
    yticks, ylabels = [], []
    for mi, (model, label, color) in enumerate(zip(MODELS, LABELS, COLORS, strict=True)):
        start = mi * 4.2
        recovery.text(
            0,
            start - 0.9,
            label,
            color=color,
            fontsize=9.3,
            transform=recovery.get_yaxis_transform(),
        )
        for ai, arm in enumerate(ARMS):
            y = start + ai
            group = [lookup[model, tool, arm] for tool in ("off", "on")]
            rates = [r["joint_recovery"] / r["scheduled"] for r in group]
            recovery.plot(rates, [y - 0.10, y + 0.10], color=color, lw=0.8, alpha=0.65)
            for ti, rate in enumerate(rates):
                recovery.scatter(
                    rate,
                    y + (ti - 0.5) * 0.20,
                    s=28,
                    facecolors=color if ti else "white",
                    edgecolors=color,
                    linewidths=1.0,
                    zorder=3,
                )
            recovery.text(
                1.09,
                y,
                " / ".join(str(r["joint_recovery"]) for r in group),
                va="center",
                fontsize=8.4,
                color=color,
            )
            yticks.append(y)
            ylabels.append(
                {
                    "opaque": "Opaque",
                    "misindexed_nominal": "Misindexed",
                    "aligned_nominal": "Aligned*",
                }[arm]
            )
        recovery.axhspan(start + 1.6, start + 2.4, color="#EAECEF", alpha=0.65, zorder=0)
    recovery.text(1.09, -0.70, "Off / On", fontsize=8.2, color=style.COLORS["muted"])
    recovery.set(
        yticks=yticks,
        yticklabels=ylabels,
        ylim=(7.1, -1.35),
        xlim=(-0.06, 1.52),
        xlabel="Joint family + exponent recovery",
    )
    recovery.set_xticks([0, 0.5, 1])
    recovery.xaxis.set_major_formatter(PercentFormatter(1))
    recovery.set_title("a   Recovery by initial description", loc="left", fontsize=10, pad=24)
    worlds = report["world_contrasts"]
    for wi, row in enumerate(worlds):
        effect.scatter(row["tool_on_minus_off"], wi, marker="D", color="#293544", s=26, zorder=4)
        for mi, color in enumerate(COLORS):
            paired = report["model_contrasts"][mi]["worlds"][wi]
            effect.scatter(
                paired["tool_on_minus_off"],
                wi + (mi - 0.5) * 0.28,
                color=color,
                s=15,
                alpha=0.75,
                zorder=3,
            )
    primary = report["primary"]
    ci = primary["approximate_world_bootstrap_95"]
    effect.plot(ci, [6, 6], color="#293544", lw=1.7)
    effect.scatter(primary["mean"], 6, marker="D", color="#293544", s=36, zorder=4)
    extent = max(
        0.20,
        abs(primary["mean"]),
        *map(abs, ci),
        *[abs(r["tool_on_minus_off"]) for m in report["model_contrasts"] for r in m["worlds"]],
    )
    effect.set(
        yticks=[0, 1, 2, 3, 4, 6],
        yticklabels=["World 1", "World 2", "World 3", "World 4", "World 5", "Mean + 95% CI"],
        ylim=(7.1, -1.35),
        xlim=(-extent * 1.23, extent * 1.23),
        xlabel="Tool-on minus tool-off",
    )
    effect.axvline(0, color="#8B95A1", lw=0.8)
    effect.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    effect.set_title("b   Paired world effects", loc="left", fontsize=10, pad=24)
    for ax in (recovery, effect):
        ax.grid(axis="x", lw=0.5, color=style.COLORS["grid"])
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0, labelsize=8.7)
    fig.legend(
        handles=[
            Line2D(
                [],
                [],
                marker="o",
                color="none",
                markeredgecolor="#45515F",
                markerfacecolor="white",
                label="Tool off",
            ),
            Line2D(
                [],
                [],
                marker="o",
                color="none",
                markeredgecolor="#45515F",
                markerfacecolor="#45515F",
                label="Tool on",
            ),
            Line2D(
                [],
                [],
                marker="D",
                color="none",
                markerfacecolor="#293544",
                markeredgecolor="#293544",
                label="Models pooled equally",
            ),
        ],
        loc="lower left",
        bbox_to_anchor=(0.02, 0.125),
        ncol=3,
        fontsize=8.5,
        columnspacing=1.7,
    )
    denominator = next(iter(lookup.values()))["scheduled"]
    completed = report["counts"].get("completed", 0)
    fig.text(
        0.035,
        0.082,
        f"Each prior/model/tool: {denominator} scheduled sessions. "
        f"Complete sessions: {completed}/{report['scheduled']}; failures remain in denominators.",
        fontsize=8.2,
        color=style.COLORS["muted"],
    )
    fig.text(
        0.035,
        0.035,
        "*Aligned prior supplies the correct law: success here is retention. "
        "Five reused worlds; the interval is a small-sample approximation.",
        fontsize=8.1,
        color=style.COLORS["muted"],
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        fig.savefig(output.with_suffix("." + extension), dpi=240, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    current = json.loads((style.ROOT / "configs/current.json").read_text(encoding="utf-8"))
    binding = current["work_ii"]["w2_77_final_diagnostic"]
    path = style.ROOT / binding["report"]
    if style.sha256_file(path) != binding["report_sha256"]:
        raise ValueError("current diagnostic report binding mismatch")
    render(json.loads(path.read_text(encoding="utf-8")), args.output)


if __name__ == "__main__":
    main()
