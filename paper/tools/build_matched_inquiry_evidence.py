"""Integrate retained matched-world evidence; no model or simulator execution."""

from __future__ import annotations

import csv
import json
import shutil
import textwrap
from collections import defaultdict
from pathlib import Path

from plot_abductive_evidence import BLUE, GREEN, GREY, ORANGE, plt, save, title

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper/venues/nature"
DEST = PAPER / "evidence"
RESPONSES = {
    "pH_normalized": "Normalized pH",
    "acid_dissociation_fraction": "Free dissociation",
    "precipitation_signal": "Precipitation",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def table(headers, rows):
    return "\n".join(
        ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        + ["| " + " | ".join(map(str, row)) + " |" for row in rows]
    )


def diagram_box(ax, x, y, heading, body, color, width=0.94, height=0.18):
    from matplotlib.patches import FancyBboxPatch

    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.01",
            transform=ax.transAxes,
            facecolor=color,
            edgecolor="none",
            alpha=0.09,
        )
    )
    ax.text(
        x + 0.02,
        y + height - 0.015,
        heading,
        color=color,
        weight="bold",
        va="top",
        transform=ax.transAxes,
        fontsize=9,
    )
    ax.text(
        x + 0.02,
        y + height - 0.06,
        body,
        va="top",
        transform=ax.transAxes,
        fontsize=8,
        linespacing=1.35,
    )


def main():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_263_abductive_completion"]
    source = ROOT / binding["report_root"]
    exp = source / "experiment"
    quant = read(ROOT / binding["quantitative_summary"])
    sessions = [read(p) for p in sorted((exp / "sessions").glob("repeat-*/*.json"))]
    assert len(sessions) == 30
    assert sum(len(s["batches"]) for s in sessions) == 360
    assert sum(len(s["versions"]) for s in sessions) == 80
    assert all(s["status"] == "completed" for s in sessions)
    fields = [
        "repeat",
        "id",
        "world",
        "pair",
        "mechanism",
        "arm",
        "model",
        "status",
        "failure",
        "public_initial_context",
        "versions",
        "events",
        "batches",
        "prediction_evaluation",
        "exact_replay",
        "counterfactual",
    ]
    public = []
    for s in sessions:
        row = {k: s[k] for k in fields}
        row["posttests"] = {k: v["payload"] for k, v in s["posttests"].items()}
        public.append(row)
    (DEST / "matched_world_public_histories.json").write_text(
        json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    exports = {
        "quantitative-summary.json": "matched_world_quantitative_summary.json",
        "predictions.csv": "matched_world_predictions.csv",
        "selected-experiment-separation.csv": "matched_world_separation.csv",
        "reading-summary.json": "matched_world_reading_summary.json",
        "resource-summary.json": "matched_world_resource_summary.json",
        "semantic_repeat01.json": "matched_world_semantic_repeat01.json",
        "semantic_repeat02.json": "matched_world_semantic_repeat02.json",
        "semantic_repeat03.json": "matched_world_semantic_repeat03.json",
    }
    for src, dst in exports.items():
        shutil.copyfile(exp / src, DEST / dst)
    for src, dst in {
        "histories_verified.json": "retrospective_histories_verified.json",
        "sealed_followups.json": "retrospective_sealed_followups.json",
    }.items():
        shutil.copyfile(source / "histories" / src, DEST / dst)

    with (exp / "selected-experiment-separation.csv").open(encoding="utf-8") as f:
        sep = list(csv.DictReader(f))
    by_session = defaultdict(list)
    for row in sep:
        by_session[row["id"], row["repeat"]].append(int(row["channels_at_least_3sd"]))
    assert len(sep) == 360 and len(by_session) == 30
    assert sum(v >= 2 for row in by_session.values() for v in row) == 158
    assert all(any(v >= 2 for v in row) for row in by_session.values())
    lookup = {(s["repeat"], s["id"]): s for s in sessions}
    focal = lookup["repeat-03", "EQ-P03-A-Opaque"]
    dilution = lookup["repeat-02", "EQ-P01-A-Opaque"]
    assert [v["public_cursor"] for v in focal["versions"]] == [0, 36, 72]
    quote = (
        "Precipitation estimates use a smooth monotone concentration response "
        "because no sharp threshold was resolved."
    )
    assert quote in json.dumps(focal["posttests"]["Q"]["payload"])
    assert (
        "Persistent high-loading behavior would suggest path dependence"
        in dilution["versions"][1]["text"]
    )

    fig = plt.figure(figsize=(9.1, 7.2), layout="constrained")
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], hspace=0.13, wspace=0.08)
    ax = fig.add_subplot(grid[0, 0])
    for pi in range(1, 6):
        for mechanism, color, dx in [("A", BLUE, -0.15), ("B", ORANGE, 0.15)]:
            world = f"EQ-P{pi:02d}-{mechanism}-Opaque"
            vals = [
                sum(x >= 2 for x in by_session[world, f"repeat-{r:02d}"]) / 12 for r in range(1, 4)
            ]
            ax.scatter(
                [pi + dx + (r - 1) * 0.045 for r in range(3)],
                vals,
                c=color,
                s=32,
                label=("Direct network" if mechanism == "A" else "Ion-pair network")
                if pi == 1
                else None,
            )
    ax.set(
        xticks=range(1, 6),
        xticklabels=[f"Pair {i}" for i in range(1, 6)],
        ylim=(-0.03, 1.05),
        ylabel="Fraction of assays separating ≥2 channels",
    )
    ax.legend(fontsize=8, loc="upper right")
    title(ax, "a  Information in self-selected experiments")
    ax = fig.add_subplot(grid[0, 1])
    plot_rows = []
    for b in focal["batches"]:
        actions = [
            e["action"]
            for e in focal["events"]
            if e["batch"] == b["ordinal"] and e["transaction_status"] == "committed"
        ]
        amount = sum(a.get("amount_mol", 0) for a in actions if a["operation"] == "add_reagent")
        volume = sum(a.get("volume_L", 0) for a in actions if a["operation"] == "add_solvent")
        c = amount / volume
        y = b["metrics"]["precipitation_signal"]
        col = BLUE if b["ordinal"] <= 6 else ORANGE
        ax.scatter(c, y, c=col, s=32)
        ax.annotate(
            str(b["ordinal"]),
            (c, y),
            xytext={8: (7, 9), 12: (-18, -12), 11: (3, -12)}.get(b["ordinal"], (3, 5)),
            textcoords="offset points",
            fontsize=7,
            color=col,
        )
        plot_rows.append([b["ordinal"], c, y, b["end_step"]])
    ax.scatter([], [], c=BLUE, label="Before mid-research note")
    ax.scatter([], [], c=ORANGE, label="After mid-research note")
    ax.legend(fontsize=7.5, loc="upper left")
    ax.set(
        xscale="log",
        xlabel="Nominal final concentration (mol/L)",
        ylabel="Measured precipitation signal",
        ylim=(-0.008, 0.10),
    )
    title(ax, "b  Testing the shape of a local relationship")
    ax = fig.add_subplot(grid[1, 0])
    ax.axis("off")
    title(ax, "c  Explanations organize further inquiry")
    for y, heading, body, col in [
        (
            0.72,
            "Initial possibilities",
            "Sharp onset + buffered response: solubility limit.\n"
            "Smooth response: empirical partition also possible.",
            BLUE,
        ),
        (
            0.44,
            "After six assays: next test",
            "Densify the response; repeat a central condition;\n"
            "compare increasing loading with dilution.",
            ORANGE,
        ),
        (
            0.16,
            "After twelve assays and in later forecasts",
            "Retain a smooth concentration relationship.\n"
            "Threshold and microscopic mechanism unresolved.",
            GREEN,
        ),
    ]:
        diagram_box(ax, 0.01, y, heading, body, col, height=0.21)
    ax = fig.add_subplot(grid[1, 1])
    e = {x["cursor"]: x for x in dilution["events"]}
    ys = [e[c]["observations"]["pH_normalized"] for c in (53, 56)]
    ax.plot([0, 1], ys, "o-", color=GREEN)
    for i, val in enumerate(ys):
        ax.annotate(f"{val:.5f}", (i, val), xytext=(0, 9), textcoords="offset points", ha="center")
    ax.set(
        xticks=[0, 1],
        xticklabels=["Before dilution\n0.75 M · pH meter", "After dilution\n0.375 M · final assay"],
        ylabel="Normalized pH",
        ylim=(0.055, 0.15),
        xlim=(-0.35, 1.35),
    )
    title(ax, "d  A prospective test of reversibility")
    ax.text(
        0.04,
        0.94,
        "Prediction before the test:\nReversible concentration control\n"
        "versus persistence of the high-loading state.",
        va="top",
        fontsize=8,
        transform=ax.transAxes,
    )
    ax.text(
        0.04,
        0.03,
        "Approximate reversibility supported;\nsmall hysteresis unresolved.",
        fontsize=8,
        transform=ax.transAxes,
        color=GREEN,
    )
    save(fig, "matched_inquiry")
    with (DEST / "matched_focal_assays.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["batch", "nominal_concentration_M", "precipitation_signal", "end_cursor"])
        writer.writerows(plot_rows)

    fig, axes = plt.subplots(1, 2, figsize=(9.1, 6.4), layout="constrained")
    timelines = [
        (
            "a  Apparent anomaly retained",
            ORANGE,
            [
                (
                    "Executed history",
                    "Solvent addition rejected.\nActual concentration near 0.025 M.",
                ),
                (
                    "Reconstructed comparison",
                    "Note counts rejected volume: 0.0083 M.\n"
                    "Comparison with 0.0125 M appears reversed.",
                ),
                (
                    "Terminal explanation",
                    "Path or geometry proposed for apparent anomaly.\nNo subsequent source test.",
                ),
                (
                    "Later use",
                    "Qualified alternatives in the scientific account;\n"
                    "comparison enters forecast rationales.",
                ),
            ],
        ),
        (
            "b  Explanation explicitly withdrawn",
            GREEN,
            [
                (
                    "Executed history",
                    "Failed termination; rejected solvent addition;\n"
                    "next reagent added to the same vessel.",
                ),
                (
                    "Initial interpretation",
                    "Actual ~0.10 and 0.05 M treated as equal.\n"
                    "Volume/activity explanation proposed.",
                ),
                (
                    "Final reconstruction",
                    "Genuine matched-concentration series completed.\n"
                    "Earlier loading difference recognized.",
                ),
                (
                    "Later use",
                    "Volume explanation explicitly withdrawn;\n"
                    "corrected account retained in assessment.",
                ),
            ],
        ),
    ]
    for ax, (heading, color, blocks) in zip(axes, timelines, strict=True):
        ax.axis("off")
        title(ax, heading)
        for j, (head, body) in enumerate(blocks):
            y = 0.77 - j * 0.25
            diagram_box(ax, 0.01, y, head, body, color, height=0.19)
            if j < 3:
                ax.annotate(
                    "",
                    xy=(0.48, y - 0.055),
                    xytext=(0.48, y - 0.01),
                    xycoords="axes fraction",
                    arrowprops={"arrowstyle": "->", "color": GREY},
                )
    save(fig, "history_revision")

    lines = [
        "## Matched-world investigations and explanatory histories",
        "",
        "Thirty additional investigations cover five matched parameter pairs, two networks and "
        "three fresh sessions per world. All complete twelve source batches and three sealed "
        "stages. These sessions are separate from the historical 300, current process 90 and "
        "research-opportunity 30. Shared keyed observations are not independent noise "
        "replications. Neither physical separation nor an accurate forecast constitutes "
        "unique mechanism identification.",
        "",
        table(
            ["Quantity", "Observed/planned"],
            [
                ["Full research and assessment chains", "30/30"],
                ["Final assays", "360/360"],
                ["Sealed account/forecast/retrospective stages", "90/90"],
                ["Query-response predictions", "1,080/1,080"],
                ["Notebook versions", "80"],
                ["Source replays", "30/30"],
                ["Own/partner-world replay trajectories", "60/60"],
                ["Assays separating >=1 / >=2 channels by 3 SD", "326/360; 158/360"],
                ["Sessions with >=2-channel separating assay", "30/30"],
            ],
        ),
        "",
        "### Physical information and prediction by world",
        "",
        "Errors average twelve queries within sessions and three sessions within each world. "
        "The fraction is the proportion of actual final assays with at least two channels "
        "separated by three declared assay standard deviations under fixed-action "
        "paired-world replay. "
        "It is neither a significance test nor an agent success rate.",
        "",
        table(
            ["Pair/network", "Separating fraction", *RESPONSES.values()],
            [
                [
                    w.removeprefix("EQ-"),
                    f"{v['separation_session_statistics']['fraction_two_channels_3sigma']['mean']:.3f}",
                    *[f"{v['prediction_groups']['all'][m]['mae']['mean']:.5f}" for m in RESPONSES],
                ]
                for w, v in quant["worlds"].items()
            ],
        ),
        "",
        "### Forecast intervals",
        "",
        "The following average worlds equally. High coverage must be interpreted with widths; "
        "these values do not establish nominal calibration. Reference observations repeat "
        "across the three sessions within a world.",
        "",
        table(
            ["Response", "MAE", "80% coverage", "Mean width"],
            [
                [
                    label,
                    *[
                        f"{quant['world_equal_prediction_groups']['all'][m][k]['mean']:.5f}"
                        for k in ("mae", "empirical_coverage80", "mean_width80")
                    ],
                ]
                for m, label in RESPONSES.items()
            ],
        ),
        "",
        "### Selected process anchors",
        "",
        "Identifiers below locate evidence, not independent explanation counts. All thirty "
        "sessions were read; the selection illustrates distinct transitions rather than "
        "estimating their frequency. Public histories include all notes and sealed payloads.",
        "",
        table(
            ["Session", "Transition", "Temporal anchors"],
            [
                [
                    "Repeat 3 / pair 3A",
                    "Threshold versus smooth relation; prospective tests; scoped forecast",
                    "Notes 0,36,72; subsequent batches 7-12; Q",
                ],
                [
                    "Repeat 2 / pair 1A",
                    "Prospective dilution distinguishes concentration from persistence",
                    "Note 50; actions 51-56; final note 61; Q09",
                ],
                [
                    "Repeat 1 / pair 2B",
                    "Rejected solvent creates apparent anomaly; terminal explanation",
                    "Rejection 11; notes 30 and terminal; K1/Q/K2",
                ],
                [
                    "Repeat 3 / pair 4A",
                    "Incorrect concentration match followed by explicit withdrawal",
                    "Failures 9-11; note 25; final note 64; K1/Q08/K2",
                ],
            ],
        ),
        "",
        "The additional retrospective reading covers 105 existing sessions and 309 notes, "
        "112 selected focal histories and 218 verified note quotations. These 105 are the "
        "current ninety plus fifteen research-opportunity sessions, not new experiments. "
        "Four selected sealed follow-ups add thirteen verified anchors. The new thirty "
        "sessions contain 67 focal histories and 365 verified anchors. Both readings include "
        "terminal revisions, use a single analysis workflow and do not claim independent "
        "rater agreement or an abduction prevalence estimate.",
        "",
        "### Failures and reproducibility",
        "",
        "Source attempts: 1,901 = 1,893 committed + six rolled back + two validation failures. "
        "The 131 recovered tool failures are separately counted. The first launch has four "
        "startup failures, twenty-six unstarted sessions and zero scientific operations; "
        "the entire fixed block restarts after repair. Earlier physical-candidate and canary "
        "failures remain in the source record. No completed scientific outcome is replaced. "
        "The review archive supplies public histories, all 1,080 predictions, 360 separation "
        "rows, per-world/per-session quantitative summaries, semantic readings and resource "
        "accounting. Existing exact replay is preserved; compilation runs no new experiment.",
        "",
    ]
    (PAPER / "matched_inquiry_analysis.md").write_text("\n".join(lines), encoding="utf-8")
    with (DEST / "README.md").open("a", encoding="utf-8") as f:
        f.write(
            textwrap.dedent("""

        ## Matched-world addition

        `matched_world_public_histories.json` contains all thirty public research histories
        and sealed payloads, without raw provider responses. Matching CSVs and quantitative,
        semantic and resource summaries preserve all sessions and failures. The two
        `retrospective_*` files refer to 105 already counted sessions, not new experiments.
        See the manuscript's matched inquiry supplement for units and interpretation.
        Generated by `build_matched_inquiry_evidence.py` from the current binding; no models
        or simulator are executed. Figure 4 uses these retained records; the current
        Extended Data 6 instead draws on the new unified-matrix histories below.
        """)
        )
    print(
        "Matched evidence: 30 sessions, 360 assays, 80 notes; two figures and tables.", flush=True
    )


if __name__ == "__main__":
    main()
