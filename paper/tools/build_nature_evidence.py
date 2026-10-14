"""Render Nature manuscript evidence from retained exports, without experiments."""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "workstreams/flagship_tasks/reports/research-extension-20261014"
DEST = ROOT / "paper/venues/nature"
FIG = DEST / "figures"
ARMS = ("Opaque", "Aligned", "MisIndexed")
COLORS = {"Opaque": "#426C8D", "Aligned": "#A65E2E", "MisIndexed": "#477C67"}
INK = "#202A33"
GREY = "#697780"
BLUE = "#426C8D"
RED = "#A65E2E"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


ANALYSIS = read(REPORT / "analysis.json")
PROCESS = read(REPORT / "process_analysis.json")
ROWS = [read(REPORT / r["repeat"] / f"{r['id']}.json") for r in ANALYSIS["cases"]]
LOOKUP = {(r["repeat"], r["id"]): r for r in ROWS}


def case(rep, identity):
    return LOOKUP[(f"repeat-{rep:02d}", identity)]


def batch(row, number):
    return next(b for b in row["batch_outcomes"] if b["lifecycle_index"] == number)


def base_style():
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 9,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.65,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "text.color": INK,
            "axes.labelcolor": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": "white",
            "legend.fontsize": 7,
            "legend.frameon": False,
        }
    )


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", pad_inches=0.08)
    fig.savefig(FIG / f"{name}.png", dpi=220, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"Rendered {name}", flush=True)


def panel(ax, letter, title):
    ax.set_title(title, pad=9)
    ax.text(-0.14, 1.06, letter, transform=ax.transAxes, weight="bold", fontsize=11)


def box(ax, xy, width, height, title, body, color=BLUE, fontsize=8):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.014",
            facecolor=color + "0D",
            edgecolor=color,
            linewidth=0.8,
        )
    )
    ax.text(x + 0.035, y + height - 0.055, title, weight="bold", va="top", fontsize=9)
    ax.text(x + 0.035, y + height - 0.22, body, va="top", fontsize=fontsize, linespacing=1.35)


def arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=9, linewidth=0.8, color=GREY)
    )


def figure1():
    fig = plt.figure(figsize=(7.1, 5.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.08], hspace=0.48, wspace=0.30)
    ax = fig.add_subplot(gs[0, :])
    ax.set_axis_off()
    ax.set_xlim(-0.025, 1.025)
    panel(ax, "a", "Autonomous choices and independently known consequences")
    box(
        ax,
        (0.00, 0.15),
        0.28,
        0.69,
        "Researcher",
        "Choose an intervention\nMeasure or continue\nRepeat, revise, recommend",
    )
    box(
        ax,
        (0.36, 0.15),
        0.28,
        0.69,
        "Virtual sample",
        "Persistent physical state\nAccepted or rejected actions\nPublic instrument feedback",
        fontsize=7.3,
    )
    box(
        ax,
        (0.72, 0.15),
        0.27,
        0.69,
        "Evaluator",
        "Control world and information\nRetain actual execution\nEvaluate withheld outcomes",
        color=GREY,
        fontsize=7.6,
    )
    arrow(ax, (0.29, 0.57), (0.35, 0.57))
    arrow(ax, (0.35, 0.34), (0.29, 0.34))
    arrow(ax, (0.65, 0.48), (0.71, 0.48))
    ax = fig.add_subplot(gs[1, 0])
    ax.set_axis_off()
    panel(ax, "b", "Public chronology")
    items = [
        "Initial expectation",
        "Self-chosen experiments and note revisions",
        "Sealed scientific account",
        "New-intervention forecasts",
        "Retrospective review",
    ]
    for i, label in enumerate(items):
        y = 0.93 - i * 0.19
        ax.scatter([0.035], [y], s=28, color=BLUE if i < 2 else INK)
        ax.text(0.095, y, textwrap.fill(label, 34), va="center", fontsize=8)
        if i < 4:
            arrow(ax, (0.035, y - 0.045), (0.035, y - 0.14))
    ax.set_xlim(-0.02, 1)
    ax.set_ylim(0, 1.05)
    ax = fig.add_subplot(gs[1, 1])
    panel(ax, "c", "Repeated process cohort")
    for si, system in enumerate(("EQ", "C")):
        for ai, arm in enumerate(ARMS):
            y = 5 - (si * 3 + ai)
            for wi in range(1, 6):
                for rep in range(1, 4):
                    r = case(rep, f"{system}-W{wi:02d}-{arm}")
                    x = wi + (rep - 2) * 0.2
                    good = not r["missing_stages"] and r["completed_batches"] == 12
                    ax.scatter(
                        x,
                        y,
                        s=19,
                        facecolor=COLORS[arm] if good else "white",
                        edgecolor=COLORS[arm],
                        linewidth=0.85,
                    )
    ax.set_xticks(range(1, 6), [f"World {i}" for i in range(1, 6)], fontsize=6.5)
    ax.set_yticks(range(6), [f"{s} {a}" for s in ("EQ", "C") for a in ARMS][::-1])
    ax.set_ylim(-0.65, 5.65)
    ax.set_xlim(0.55, 5.45)
    ax.spines[["left", "bottom"]].set_visible(False)
    ax.tick_params(length=0)
    ax.text(
        0,
        -0.22,
        "90 sessions | 84 complete chains | 284 note revisions",
        transform=ax.transAxes,
        fontsize=7,
    )
    fig.text(
        0.12,
        0.00,
        "Separate broad evidence: 300 campaigns across six chemical families "
        "and five model configurations",
        fontsize=7.5,
        color=GREY,
    )
    save(fig, "figure01")


def figure2():
    fig = plt.figure(figsize=(7.1, 5.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[0.95, 1.15], hspace=0.65, wspace=0.44)
    ax = fig.add_subplot(gs[0, :])
    panel(ax, "a", "A mapping conjecture is proposed and tested")
    r = case(1, "EQ-W04-MisIndexed")
    vals = [b["metrics"]["acid_dissociation_fraction"] for b in r["batch_outcomes"]]
    ax.plot(range(1, 13), vals, color="#B8C2C8", lw=0.8)
    ax.scatter(range(1, 11), vals[:10], s=17, color=GREY)
    ax.scatter([11, 12], vals[10:], s=28, color=BLUE)
    ax.axvline(10.5, color=BLUE, lw=0.8, ls="--")
    ax.set(
        ylim=(0.02, 0.15),
        xlim=(0.6, 12.4),
        ylabel="Dissociation fraction",
        xlabel="Completed batch",
    )
    ax.set_xticks(range(1, 13))
    ax.text(2, 0.131, "Conjecture: another component is the active coordinate", fontsize=7.8)
    ax.annotate(
        "Prospective note",
        xy=(10.5, 0.085),
        xytext=(7.3, 0.108),
        fontsize=7,
        arrowprops={"arrowstyle": "->", "lw": 0.7},
    )
    ax.text(10.6, 0.037, "Component tests", fontsize=7)
    ax = fig.add_subplot(gs[1, 0])
    panel(ax, "b", "A rescue expectation is withdrawn")
    r = case(3, "C-W01-MisIndexed")
    vals = [batch(r, i)["metrics"]["crystal_fines_fraction"] for i in (10, 12)]
    ax.scatter([0.02, 0.05], vals, s=45, color=BLUE, zorder=3)
    ax.axhline(0.5, color=GREY, lw=0.8, ls="--")
    ax.text(0.019, 0.55, "Fines limit", fontsize=7, color=GREY)
    ax.set(
        xlim=(0.01, 0.06),
        ylim=(0, 1.12),
        xlabel="Successfully added seed (g)",
        ylabel="Fines fraction",
    )
    ax.set_xticks([0.02, 0.05])
    ax.text(0.025, 0.76, "Both tests fail\nRescue hypothesis withdrawn", fontsize=7.4)
    ax = fig.add_subplot(gs[1, 1])
    panel(ax, "c", "A working region guides another test")
    r = case(2, "C-W01-MisIndexed")
    vals = [batch(r, i)["metrics"]["crystal_fines_fraction"] for i in (10, 11, 12)]
    vals += [r["retest"]["truth"][0]["crystal_fines_fraction"]]
    ax.plot(range(4), vals, lw=0.8, color=BLUE)
    ax.scatter(range(3), vals[:3], s=32, color=BLUE)
    ax.scatter([3], [vals[3]], s=40, marker="D", color=INK)
    ax.axhline(0.5, color=GREY, lw=0.8, ls="--")
    ax.set_xticks(
        range(4), ["35 ml\nbatch 10", "32.5 ml\nbatch 11", "35 ml\nbatch 12", "35 ml\nretest"]
    )
    ax.set(ylim=(0, 0.59), ylabel="Fines fraction", xlabel="Prospective test, repeat and retest")
    ax.text(0.12, 0.40, "All four remain feasible", fontsize=7.5)
    save(fig, "figure02")


def scatter_groups(ax, system, metric, ylabel, logarithmic=False):
    for ai, arm in enumerate(ARMS):
        group = [r for r in ROWS if r["system"] == system and r["arm"] == arm]
        valid = [r for r in group if r["measurements"].get(metric) is not None]
        for j, r in enumerate(valid):
            x = ai + ((j % 5) - 2) * 0.055
            ax.scatter(x, r["measurements"][metric], s=15, color=COLORS[arm], alpha=0.65)
        means = [
            fmean(r["measurements"][metric] for r in valid if r["world"] == w)
            for w in sorted({r["world"] for r in valid})
        ]
        ax.scatter(
            ai,
            fmean(means),
            s=52,
            marker="D",
            facecolor="white",
            edgecolor=COLORS[arm],
            linewidth=1.4,
            zorder=5,
        )
    ax.set_xticks(range(3), ["Opaque", "Aligned", "Misindexed"], rotation=20, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_xlim(-0.45, 2.45)
    if logarithmic:
        ax.set_yscale("log")


def figure3():
    fig = plt.figure(figsize=(7.1, 5.2))
    gs = fig.add_gridspec(2, 6, hspace=0.70, wspace=1.2)
    ax = fig.add_subplot(gs[0, :3])
    panel(ax, "a", "A local test enters a dilute forecast")
    r = case(1, "EQ-W04-MisIndexed")
    source = [b["metrics"]["acid_dissociation_fraction"] for b in r["batch_outcomes"]]
    p = next(
        r for r in PROCESS["cases"] if r["repeat"] == "repeat-01" and r["id"] == "EQ-W04-MisIndexed"
    )
    q = p["q08"]["metrics"]["acid_dissociation_fraction"]
    ax.scatter(np.linspace(-0.13, 0.13, 12), source, s=14, color=GREY)
    ax.errorbar(
        1,
        q["estimate"],
        yerr=[[q["estimate"] - q["lower80"]], [q["upper80"] - q["estimate"]]],
        fmt="o",
        color=BLUE,
        capsize=3,
        markersize=4,
    )
    ax.scatter(
        2, p["q08_reference_mean"]["acid_dissociation_fraction"], color=INK, marker="D", s=36
    )
    ax.set_xticks([0, 1, 2], ["Source\nobservations", "Dilute\nforecast", "Dilute\nreference"])
    ax.set(ylabel="Dissociation fraction", ylim=(0, 0.65), xlim=(-0.45, 2.4))
    ax = fig.add_subplot(gs[0, 3:])
    panel(ax, "c", "Different continuations of the same world")
    for ai, arm in enumerate(ARMS[:2]):
        for rep in range(1, 4):
            p = next(
                r
                for r in PROCESS["cases"]
                if r["repeat"] == f"repeat-{rep:02d}" and r["id"] == f"EQ-W03-{arm}"
            )
            v = p["q08"]["metrics"]["acid_dissociation_fraction"]
            x = ai + (rep - 2) * 0.18
            ax.scatter(x, v["estimate"], s=27, color=COLORS[arm])
            ax.text(x, v["estimate"] + 0.025, str(rep), ha="center", fontsize=6.5)
    ax.axhline(p["q08_reference_mean"]["acid_dissociation_fraction"], color=INK, ls="--", lw=0.8)
    ax.text(0.35, 0.61, "Reference", fontsize=7)
    ax.set_xticks([0, 1], ARMS[:2])
    ax.set(ylabel="Dilute dissociation forecast", ylim=(0, 0.75), xlim=(-0.5, 1.5))
    for j, (metric, label) in enumerate(
        [
            ("remaining_nine_macro_mae", "Other nine queries: MAE"),
            ("lowest_three_macro_mae", "Most dilute queries: MAE"),
            ("lowest_three_coverage80", "Dilute interval coverage"),
        ]
    ):
        ax = fig.add_subplot(gs[1, j * 2 : j * 2 + 2])
        panel(ax, "b" if j == 0 else "", "")
        scatter_groups(ax, "EQ", metric, label, logarithmic=j < 2)
        if j == 2:
            ax.axhline(0.8, color=GREY, ls="--", lw=0.7)
            ax.set_ylim(-0.04, 1.05)
    save(fig, "figure03")


def figure4():
    fig = plt.figure(figsize=(7.1, 5.6))
    gs = fig.add_gridspec(2, 6, height_ratios=[1, 1.05], hspace=0.68, wspace=1.3)
    ax = fig.add_subplot(gs[0, :])
    panel(ax, "a", "High source purity and lower forecasts in three successful studies")
    for rep in range(1, 4):
        r = case(rep, "C-W04-MisIndexed")
        d = r["purity_detail"]
        center = (rep - 1) * 3
        src = [b["metrics"]["crystal_purity"] * 100 for b in r["batch_outcomes"]]
        pred = [
            p["crystal_purity"]["estimate"] * 100
            for p in r["posttests"]["Q"]["payload"]["predictions"]
        ]
        for pos, values, color in [(center, src, GREY), (center + 1, pred, BLUE)]:
            ax.scatter(pos + np.linspace(-0.15, 0.15, 12), values, color=color, s=13, alpha=0.65)
            ax.scatter(pos, fmean(values), color=color, marker="D", s=40)
        ax.hlines(d["query_truth"]["mean"] * 100, center - 0.35, center + 1.35, color=INK, lw=1)
        ax.text(
            center + 0.5,
            -0.24,
            f"Session {rep}",
            transform=ax.get_xaxis_transform(),
            ha="center",
            fontsize=7.5,
        )
    ax.set_xticks([0, 1, 3, 4, 6, 7], ["Source", "Forecast"] * 3)
    ax.set(ylabel="Crystal purity (%)", ylim=(78, 102), xlim=(-0.55, 7.55))
    ax.text(7.45, 99.5, "Reference mean", ha="right", fontsize=7)
    ax = fig.add_subplot(gs[1, :2])
    panel(ax, "b", "Recommendation success")
    for ai, arm in enumerate(ARMS):
        for wi in range(1, 6):
            for rep in range(1, 4):
                r = case(rep, f"C-W{wi:02d}-{arm}")
                good = r["measurements"]["recommendation_quality_and_yield_target"]
                ax.scatter(
                    ai + (rep - 2) * 0.20,
                    wi,
                    s=25,
                    edgecolor=COLORS[arm],
                    facecolor=COLORS[arm] if good else "white",
                    linewidth=0.8,
                )
    ax.set_xticks(range(3), ["Opaque", "Aligned", "Misindexed"], rotation=25, ha="right")
    ax.set_yticks(range(1, 6), [f"World {i}" for i in range(1, 6)])
    ax.set_xlim(-0.45, 2.45)
    ax.set_ylim(0.6, 5.4)
    ax.invert_yaxis()
    ax.spines[["left", "bottom"]].set_visible(False)
    ax.tick_params(length=0)
    for j, (metric, label) in enumerate(
        [("crystal_purity_mae", "Purity MAE"), ("crystal_yield_mae", "Recovery MAE")]
    ):
        ax = fig.add_subplot(gs[1, 2 + j * 2 : 4 + j * 2])
        panel(ax, "c" if j == 0 else "", "")
        scatter_groups(ax, "C", metric, label)
        ax.set_ylim(bottom=0)
    save(fig, "figure04")


def extended():
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 3.1), gridspec_kw={"wspace": 0.18})
    boxes = [
        (
            "a",
            "Proposed test",
            "About 2 g of seed",
            "40 requests of 0.05 g\n1 successful addition\n39 rejected additions\n\n"
            "Actual total: 0.05 g",
        ),
        (
            "b",
            "Later public account",
            "Treated as a dose test",
            "Large dose said to be ineffective\nClaim retained in:\n- later notes\n- "
            "scientific account\n- retrospective review\n\nNo completed 2 g test",
        ),
        (
            "c",
            "Contrasting response",
            "Rejection recognized",
            "Another agent records the\nfailed additional seed calls\nand limits "
            "subsequent dosing\n\nAn execution failure need not\nbecome negative "
            "evidence",
        ),
    ]
    for ax, (letter, title, subtitle, body) in zip(axes, boxes, strict=True):
        ax.set_axis_off()
        ax.set_xlim(-0.025, 1.025)
        panel(ax, letter, title)
        box(
            ax,
            (0.01, 0.08),
            0.96,
            0.82,
            subtitle,
            body,
            fontsize=7.5,
            color=RED if letter == "b" else BLUE,
        )
    save(fig, "extended01")
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.65), gridspec_kw={"wspace": 0.34})
    for ax, (rep, cid, letter, title) in zip(
        axes,
        [
            (3, "C-W02-Aligned", "a", "Margin stated, boundary selected"),
            (2, "C-W04-Aligned", "b", "Margin enters the recommendation"),
        ],
        strict=True,
    ):
        panel(ax, letter, title)
        r = case(rep, cid)
        i = r["recommendation"]["selected_experiment_index"]
        values = [
            batch(r, i)["metrics"]["crystal_fines_fraction"],
            r["retest"]["truth"][0]["crystal_fines_fraction"],
        ]
        ax.plot([0, 1], values, color=BLUE, lw=0.9)
        ax.scatter([0, 1], values, color=[BLUE, INK], s=36)
        ax.axhline(0.5, color=RED, ls="--", lw=0.8)
        ax.set_xticks([0, 1], ["Public measurement", "Noiseless retest"])
        ax.set(ylabel="Fines fraction", xlim=(-0.3, 1.3), ylim=(0.475, 0.52))
    save(fig, "extended02")
    pairs = read(REPORT / "quench_pairs.json")
    valid = [p for p in pairs if p["paired_effect"] is not None]
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.7), gridspec_kw={"wspace": 0.55})
    ax = axes[0]
    panel(ax, "a", "Complete matched pairs")
    ax.plot([0, 1], [0, 1], color=GREY, ls="--", lw=0.7)
    ax.scatter(
        [p["absent"]["truth"]["crystal_fines_fraction"] for p in valid],
        [p["present"]["truth"]["crystal_fines_fraction"] for p in valid],
        s=18,
        alpha=0.65,
        color=BLUE,
    )
    ax.set(
        xlabel="Fines without quench",
        ylabel="Fines with quench",
        xlim=(-0.03, 1.03),
        ylim=(-0.03, 1.03),
    )
    ax = axes[1]
    panel(ax, "b", "Effects across worlds")
    for wi in range(1, 6):
        group = [
            p["paired_effect"]["crystal_fines_fraction"]
            for p in valid
            if p["world"] == f"W{wi:02d}"
        ]
        ax.scatter(wi + np.linspace(-0.12, 0.12, len(group)), group, color=BLUE, s=14, alpha=0.6)
        ax.scatter(wi, fmean(group), marker="D", s=34, color=INK)
    ax.axhline(0, color=GREY, lw=0.7)
    ax.set_xticks(range(1, 6))
    ax.set(xlabel="World", ylabel="Fines change (with - without)")
    ax = axes[2]
    panel(ax, "c", "All planned pairs")
    vals = [
        len(valid),
        sum(not p["absent"]["passed"] for p in pairs),
        sum(not p["present"]["passed"] for p in pairs),
    ]
    ax.barh(range(3), vals, color=[BLUE, GREY, RED], height=0.6)
    ax.set_yticks(
        range(3),
        ["Complete", "No particles\n(absent arm)", "Illegal cooling\n(present arm)"],
        fontsize=6.6,
    )
    ax.invert_yaxis()
    ax.set(xlim=(0, 88), xlabel="Pairs")
    for y, v in enumerate(vals):
        ax.text(v + 2, y, str(v), va="center", fontsize=8)
    save(fig, "extended03")


def markdown_table(headers, rows):
    return "\n".join(
        ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        + ["| " + " | ".join(str(v) for v in row) + " |" for row in rows]
    )


def process_evidence():
    """Inventory record availability and verify the selected, human-interpreted quotations."""
    cases = read(DEST / "process_cases.json")["cases"]
    lines = [
        "## Record availability across all process sessions",
        "",
        "This inventory reports available records, not the presence or absence of a scientific "
        "mechanism. All initial notes precede physical operations under the prompted notebook "
        "role. Notes counts include the initial version. K1 is the sealed source account, Q "
        "the forecast, K2 the retrospective, and EQS the equilibrium supplement. Unavailable "
        "stages remain missing. A session not selected below has not been classified as a "
        "negative case. World and arm labels have the same meaning as in the outcome tables.",
        "",
        markdown_table(
            ["System", "World", "Arm", "Repeat", "Notes", "Initial before action", "Stages"],
            [
                [
                    r["system"],
                    r["world"][1:],
                    r["arm"][0],
                    r["repeat"][-1],
                    r["notebook"]["version_count"],
                    "Yes" if r["notebook"]["initial_note_before_action"] else "No",
                    ", ".join(r["sealed_stages"]) or "None",
                ]
                for r in sorted(
                    ROWS,
                    key=lambda r: (r["system"], r["world"], ARMS.index(r["arm"]), r["repeat"]),
                )
            ],
        ),
        "",
        "## Structured focal relationships",
        "",
        "Nine selected sessions are organized below by the relationship under examination. "
        "Cases 4-6 retain all three sessions in one crystallization world/information cell. "
        "Other cases are selected trajectories or counterexamples, not a random sample. "
        "Each record separates prior expectation, successful execution, explicit revision, "
        "evidential scope and later use. A pre-test claim not established by the focal analysis "
        "is labelled accordingly; it is not scored as absent. Quotations are checked against "
        "their specified note version or sealed stage. Interpretation remains by one analyst, "
        "without independent reliability assessment. All figures remain illustrative previews; "
        "these records and the outcome tables carry the retained evidence.",
        "",
    ]
    checked = 0
    labels = {
        "expectation": "Prior expectation",
        "execution": "Executed test or observations",
        "revision": "Recorded revision or characterization",
        "supported_scope": "What the evidence supports",
        "later_use": "Subsequent use",
        "coverage": "Extent of support",
    }
    for record in cases:
        row = LOOKUP[(record["repeat"], record["id"])]
        lines += [
            f"### Process case {record['number']}: {record['title']}",
            "",
            f"{row['system']}, world {int(row['world'][1:])}, {row['arm']}, "
            f"session {int(row['repeat'].split('-')[1])}. "
            + ("First cohort." if row["cohort"] == "retained_48" else "Extension cohort."),
            "",
        ]
        for key, label in labels.items():
            lines += [f"**{label}.** {record[key]}", ""]
        for quote in record["quotes"]:
            filename = REPORT / row["repeat"] / f"{row['id']}-{quote['document']}.md"
            text = filename.read_text(encoding="utf-8")
            if quote["document"] == "notebook":
                marker = f"## Revision {quote['revision']}\n"
                section = text.split(marker, 1)[1].split("\n## Revision ", 1)[0]
                location = f"note version {quote['revision']}"
            else:
                marker = f"## {quote['stage']}\n"
                section = text.split(marker, 1)[1]
                section = re.split(r"\n## (?:K1|Q|K2|EQS)\n", section, maxsplit=1)[0]
                location = quote["stage"]
            if quote["quote"] not in section:
                raise ValueError(f"Quotation absent from {filename}: {location}")
            lines += [f"**Recorded wording ({location}).** \"{quote['quote']}\"", ""]
            checked += 1
    print(f"Process evidence: {len(ROWS)}/90 inventories; {len(cases)} focal sessions; "
          f"{checked} version/stage-specific quotations verified", flush=True)
    return lines


def supplementary():
    lines = [
        "# Supplementary Information",
        "",
        "## Study organization",
        "",
        "The broad study (300 campaigns), earlier selected notebook studies (24 sessions), "
        "and repeated process cohort (90 sessions) retain separate denominators"
        " and execution provenance. "
        "Reference batches, recommendation retests and fixed-recipe controls "
        "are not researcher sessions. "
        "The process cohort retains 84 complete chains, 1,079/1,080 source "
        "batches, 298/315 assessment "
        "stages and 86 valid forecast stages. Notebook reading covers all 284 "
        "revisions, but qualitative "
        "interpretation is by one analyst and selected cases do not establish "
        "mechanism prevalence. The separate main-text PDF and this Supplementary Information "
        "form one reading package; the main-text file alone does not contain the full tables.",
        "",
        "## Recovery definitions and the affected readouts",
        "",
        "The full-process observation response used in source assays, recommendation retests "
        "and prediction references is seed-excluded solid target divided by the tracked "
        "initial reagent amount, clipped to [0,1]. It is distinct from the internal "
        "crystallization-stage metric and from the definition in the saved participant prompts.",
        "",
        markdown_table(
            ["Quantity or interface", "Denominator", "Role in the retained study"],
            [
                ["Internal crystallization module", "Target product before separation",
                 "Stage-recovery metric, subsequently overridden for full-process observation"],
                ["Source final assay", "Tracked initial reagent amount",
                 "Noisy full-process observation provided to the researcher"],
                ["Recommendation and query reference", "Tracked initial reagent amount",
                 "Noiseless full-process response captured before final-assay sampling"],
                ["Forecast evaluator", "Same captured initial-charge response",
                 "Original errors and interval coverage; scores retained unchanged"],
                ["Source and forecast prompts", "Target product before separation",
                 "Participant-facing description mismatched to the observed/scored output"],
            ],
        ),
        "",
        "The numerator excludes seed, but matching numerators do not make these denominators "
        "equivalent. This mismatch occurs in both recorded process execution versions; it is "
        "not a verified historical-to-current normalization change. Recovery scores and joint "
        "quality/recovery counts remain reproducible protocol-affected diagnostics. They are "
        "not evidence of performance on an unambiguously specified recovery target. "
        "Particle/purity/fines feasibility is reported separately: 10/15 Opaque, 9/15 Aligned "
        "and 14/15 MisIndexed, compared with retained joint counts 9/15, 7/15 and 14/15. "
        "Purity and fines do not use the disputed denominator, but the research paths were "
        "generated under the original instructions. No original prediction, reference or score "
        "has been changed.",
        "",
        "## Complete equilibrium process outcomes",
        "",
        "Each row is one independent model session within a fixed world and information condition. "
        "O/A/M denote Opaque/Aligned/MisIndexed. A dash is a missing forecast. "
        "All M sessions belong "
        "to the extension cohort; O/A sessions belong to the first cohort. MAEs average the three "
        "equilibrium response channels. The other-nine group is not an in-distribution control.",
        "",
    ]

    def fmt(v):
        return "-" if v is None else f"{v:.5f}"

    eq = []
    for r in sorted(
        (r for r in ROWS if r["system"] == "EQ"),
        key=lambda r: (r["world"], ARMS.index(r["arm"]), r["repeat"]),
    ):
        m = r["measurements"]
        eq.append(
            [
                r["world"][1:],
                r["arm"][0],
                r["repeat"][-1],
                r["completed_batches"],
                fmt(m.get("remaining_nine_macro_mae")),
                fmt(m.get("lowest_three_macro_mae")),
                fmt(m.get("lowest_three_coverage80")),
            ]
        )
    lines += [
        markdown_table(
            [
                "World",
                "Arm",
                "Repeat",
                "Batches",
                "Other-nine MAE",
                "Dilute MAE",
                "Dilute coverage",
            ],
            eq,
        ),
        "",
        "## Complete crystallization process outcomes",
        "",
        "All rows have twelve source batches and valid forecasts. Success applies the original "
        "joint recommendation criteria to the noiseless retest. All M sessions, and all W02/W04 "
        "sessions, belong to the extension cohort. Other O/A sessions belong to the first cohort. "
        "Recovery MAE and Success retain the implemented initial-charge target under the "
        "mismatched prompt, as detailed above; neither is a clean recovery-understanding readout.",
        "",
    ]
    cs = []
    for r in sorted(
        (r for r in ROWS if r["system"] == "C"),
        key=lambda r: (r["world"], ARMS.index(r["arm"]), r["repeat"]),
    ):
        m = r["measurements"]
        cs.append(
            [
                r["world"][1:],
                r["arm"][0],
                r["repeat"][-1],
                "Yes" if m["recommendation_quality_and_yield_target"] else "No",
                fmt(m["crystal_purity_mae"]),
                fmt(m["crystal_yield_mae"]),
                fmt(m["crystal_fines_fraction_mae"]),
            ]
        )
    lines += [
        markdown_table(
            ["World", "Arm", "Repeat", "Success", "Purity MAE", "Recovery MAE", "Fines MAE"], cs
        ),
        "",
        "## Incomplete chains",
        "",
        "All six incomplete chains are retained. Missing stages do not imply a forecast of zero. "
        "K1 is the scientific account, Q the prediction, K2 the retrospective, and EQS the "
        "structured equilibrium supplement. Five chains lose one or more assessment payloads. "
        "The extension W01/M repeat 2 terminates after eleven batches on a resource-accounting "
        "validation failure; none of its assessment stages is available.",
        "",
    ]
    lines += [
        markdown_table(
            ["World", "Arm", "Repeat", "Cohort", "Missing stages"],
            [
                [
                    r["id"].split("-")[1][1:],
                    r["id"].split("-")[2][0],
                    r["repeat"][-1],
                    "First" if r["cohort"] == "retained_48" else "Extension",
                    ", ".join(r["missing_stages"]),
                ]
                for r in ANALYSIS["failures"]
            ],
        ),
        "",
        "## Scope of process cases",
        "",
        "Main Figures 2-4 and Extended Data Figures 1-2 connect original public records to "
        "executed actions. The equilibrium mapping case is world 4, M, repeat 1; the seed-rescue "
        "case world 1, M, repeat 3; the volume-window case world 1, M, repeat 2. The purity "
        "comparison retains all three world-4/M sessions. The incorrect cumulative-seed account "
        "is world 4, A, repeat 3; the rejection-recognizing counterexample is "
        "world 2, A, repeat 2. "
        "Risk-choice examples are world 2, A, repeat 3 and world 4, A, repeat 2. These labels "
        "locate evidence; they do not define participant subpopulations or "
        "prevalence denominators.",
        "",
    ]
    lines += process_evidence()
    lines += [
        "## All matched quench dispositions",
        "",
        "Donor numbers below identify the eighteen first-cohort recommendations in a fixed "
        "sorted order. Five worlds are reused for each donor. A dash is a missing final paired "
        "effect, with the failed arm retained. Effects are present minus absent and use noiseless "
        "fines. They describe the complete pairs, not all planned recipes. "
        "Invalid arms are not repaired.",
        "",
    ]
    pairs = read(REPORT / "quench_pairs.json")
    donors = sorted({p["recipe"] for p in pairs})
    lines += [
        markdown_table(
            ["Donor", "Source world", "Information", "Repeat"],
            [
                [i + 1, d.split("-")[-2][1:], d.split("-")[-1], d.split("-")[1]]
                for i, d in enumerate(donors)
            ],
        ),
        "",
    ]
    qr = []
    for donor in donors:
        group = sorted((p for p in pairs if p["recipe"] == donor), key=lambda p: p["world"])
        vals = []
        for p in group:
            vals.append(
                fmt(p["paired_effect"]["crystal_fines_fraction"])
                if p["paired_effect"] is not None
                else ("Absent fails" if not p["absent"]["passed"] else "Present fails")
            )
        qr.append([donors.index(donor) + 1, *vals])
    lines += [
        markdown_table(["Donor", "World 1", "World 2", "World 3", "World 4", "World 5"], qr),
        "",
        "## Retained broad-study tables",
        "",
        "The following numerical tables retain the earlier cross-system and targeted-model "
        "results without pooling them with the process cohort. Their original descriptive "
        "groupings, task-specific response scales and sample units remain unchanged. E, P and S "
        "as information loci denote entity, parameter and structure information; P as a system "
        "denotes purification. EC is electrochemistry, PA partitioning, RX "
        "reaction, EQ equilibrium "
        "and C crystallization. Tables with example trajectories refer to the earlier study, "
        "not to the new process cases. SD is descriptive variation, not a confidence interval.",
        "",
    ]
    legacy = (ROOT / "paper/venues/ncs/supplementary_en.md").read_text(encoding="utf-8")
    legacy_lines = legacy.splitlines()
    heading = ""
    counter = 0
    i = 0
    while i < len(legacy_lines):
        line = legacy_lines[i]
        if line.startswith("#"):
            heading = line.lstrip("# ")
        if (
            line.startswith("|")
            and i + 1 < len(legacy_lines)
            and re.match(r"\|[ :|\-]+$", legacy_lines[i + 1])
        ):
            previous = i - 1
            while previous >= 0 and not legacy_lines[previous].strip():
                previous -= 1
            caption = legacy_lines[previous] if previous >= 0 else ""
            table = []
            while i < len(legacy_lines) and legacy_lines[i].startswith("|"):
                table.append(legacy_lines[i])
                i += 1
            counter += 1
            if counter == 3:
                lines += [
                    "Tables 3-18 report MAE / empirical interval coverage (%), averaged "
                    "over five world sessions. All scheduled sessions remain included. "
                    "PA intervals are nominally 90%; all others are 80%. Response scales "
                    "and reference targets differ across systems.",
                    "",
                ]
            lines += [f"### Retained table {counter}: {heading}", ""]
            if caption.startswith(("**Table", "**Supplementary Table")):
                lines += [caption, ""]
            if counter == 33:
                lines += [
                    "For each campaign, prediction error decomposes as "
                    r"$\operatorname{MSE}=\overline{p-y}^{\,2}+"
                    r"\frac{1}{12}\sum_i[(p_i-\bar p)-(y_i-\bar y)]^2$. "
                    "Centred RMSE is the square root of the second term. Demeaning "
                    "uses withheld references for diagnosis, not as an available predictor.",
                    "",
                ]
            lines += ["\n".join(table), ""]
            note_start = i
            while note_start < len(legacy_lines) and not legacy_lines[note_start].strip():
                note_start += 1
            note = []
            while note_start < len(legacy_lines):
                value = legacy_lines[note_start]
                if not value.strip() or value.startswith(
                    ("#", "|", "![", "**Table", "**Supplementary")
                ):
                    break
                note.append(value)
                note_start += 1
            if note:
                note_text = " ".join(note)
                note_text = re.sub(
                    r"The source-observation band in Supplementary Figure S8"
                    r".*?specific to each campaign\.",
                    "The displayed source ranges are specific to each campaign.",
                    note_text,
                )
                note_text = re.sub(r"Figure 4b shows.*?separately\.", "", note_text).strip()
                note_text = note_text.replace(
                    "Public explanation categories and K1/Q chronology are in section C.4.",
                    "Public explanation categories appear in retained table 21 above.",
                )
                lines += [note_text, ""]
            continue
        i += 1
    lines += [
        "## Executed process relationships",
        "",
        "The following equations describe the retained virtual-world laws, not mechanisms "
        "inferred by the participants. The initial-charge final-assay recovery formula below "
        "also describes the checked full-process observation route in the repeated cohort. "
        "The internal stage-recovery metric and mismatched participant description are "
        "distinguished above; they must not be substituted for the observed/scored response.",
        "",
    ]
    for start, end in (("## H.1 ", "## H.2 "), ("## H.3 ", "## H.4 ")):
        section = legacy.split(start, 1)[1].split(end, 1)[0]
        section = "### " + section
        section = section.replace(
            "The concentration in Figure 4a and Supplementary Figure S8a",
            "Nominal concentration in the retained source comparisons",
        )
        section = section.replace("Appendix G separately tests", "The retained diagnostics test")
        lines += [section.strip(), ""]
    text = "\n".join(lines)
    (DEST / "supplementary.md").write_text(text, encoding="utf-8")
    return counter


def main():
    base_style()
    figure1()
    figure2()
    figure3()
    figure4()
    extended()
    tables = supplementary()
    assert len(ROWS) == 90 and sum(r["notebook"]["version_count"] for r in ROWS) == 284
    print(
        "Evidence complete: 4 main figures, 3 Extended Data figures, "
        f"90 session rows, {tables} retained tables."
    )


if __name__ == "__main__":
    main()
