"""Render arXiv v1 figures exclusively from the frozen derived-data JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from itertools import pairwise
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OPAQUE = "#355C7D"
NOMINAL = "#D95F59"
MISINDEXED = "#8A6BBE"
GRID = "#D9DEE5"
TEXT = "#18212B"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != "chemworld-arxiv-v1-derived-data-0.1":
        raise ValueError("unsupported arXiv derived-data schema")
    declared = value.pop("derived_data_sha256")
    actual = hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    value["derived_data_sha256"] = declared
    if actual != declared:
        raise ValueError("derived-data content hash is invalid")
    return value


def _configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "axes.edgecolor": "#6F7782",
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.frameon": False,
            "svg.hashsalt": "chemworld-arxiv-v1",
        }
    )


def _panel(ax: plt.Axes, label: str, title: str) -> None:
    ax.text(
        -0.08,
        1.06,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
    )
    ax.set_title(title, loc="left", fontweight="bold", color=TEXT, pad=12)


def _save(fig: plt.Figure, output_dir: Path, stem: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [output_dir / f"{stem}.svg", output_dir / f"{stem}.png"]
    fig.savefig(
        outputs[0],
        bbox_inches="tight",
        metadata={"Date": None, "Creator": "ChemWorld arXiv v1 figure pipeline"},
    )
    outputs[0].write_text(
        outputs[0].read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )
    fig.savefig(
        outputs[1],
        bbox_inches="tight",
        dpi=240,
        metadata={"Software": "ChemWorld arXiv v1 figure pipeline"},
    )
    plt.close(fig)
    return outputs


def figure_1(data: dict[str, Any], output_dir: Path) -> list[Path]:
    q = data["environment_qualification"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.2))
    fig.suptitle(
        "ChemWorld is a controlled apparatus for experimental intelligence",
        fontsize=15,
        fontweight="bold",
        color=TEXT,
        y=1.01,
    )
    ax = axes[0, 0]
    _panel(ax, "A", "Closed-loop chemical experimentation")
    ax.axis("off")
    labels = [
        "Hidden chemical\nworld",
        "Typed\noperation",
        "State\ntransition",
        "Public\nmeasurement",
    ]
    xs = [0.08, 0.33, 0.58, 0.83]
    for x, label in zip(xs, labels, strict=True):
        ax.text(
            x,
            0.52,
            label,
            ha="center",
            va="center",
            transform=ax.transAxes,
            bbox={"boxstyle": "round,pad=0.5", "fc": "#F4F7FA", "ec": OPAQUE},
        )
    for left, right in pairwise(xs):
        ax.annotate(
            "",
            xy=(right - 0.08, 0.52),
            xytext=(left + 0.08, 0.52),
            xycoords=ax.transAxes,
            arrowprops={"arrowstyle": "->", "color": TEXT, "lw": 1.5},
        )
    ax.annotate(
        "next action",
        xy=(xs[1], 0.38),
        xytext=(xs[3], 0.23),
        xycoords=ax.transAxes,
        ha="center",
        color=NOMINAL,
        arrowprops={"arrowstyle": "->", "color": NOMINAL, "lw": 1.5},
    )

    ax = axes[0, 1]
    _panel(ax, "B", "Independent experimental controls")
    controls = ["physics", "prior", "agency", "evidence", "resources"]
    ax.barh(np.arange(5), [1] * 5, color=[OPAQUE, NOMINAL, "#4D9B8C", "#E2A447", MISINDEXED])
    ax.set_yticks(np.arange(5), controls)
    ax.set_xlim(0, 1.18)
    ax.set_xticks([])
    ax.invert_yaxis()
    ax.text(1.03, 2, "intervene\nwithout changing\nthe others", va="center", color=TEXT)

    ax = axes[1, 0]
    _panel(ax, "C", "An auditable transition spine")
    ax.axis("off")
    spine = ["typed state", "transaction", "resource receipt", "immutable trace", "exact replay"]
    for index, label in enumerate(spine):
        y = 0.83 - index * 0.16
        ax.text(
            0.12,
            y,
            f"{index + 1}",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            bbox={"boxstyle": "circle", "fc": OPAQUE, "ec": OPAQUE},
            transform=ax.transAxes,
        )
        ax.text(0.21, y, label, va="center", transform=ax.transAxes)
        if index < len(spine) - 1:
            ax.plot([0.12, 0.12], [y - 0.12, y - 0.04], color=GRID, lw=2, transform=ax.transAxes)
    ax.text(
        0.72,
        0.5,
        "invalid actions and failures\nremain evidence",
        ha="center",
        va="center",
        color=NOMINAL,
        fontsize=11,
        transform=ax.transAxes,
        bbox={"boxstyle": "round,pad=0.6", "fc": "#FFF5F3", "ec": NOMINAL},
    )

    ax = axes[1, 1]
    _panel(ax, "D", "Qualified environment surface")
    labels = ["tasks", "operations", "instruments", "execution\ncases", "bound\nendpoints"]
    values = [
        q["registered_tasks"],
        q["registered_operations"],
        q["registered_instruments"],
        q["deterministic_complete_experiment_cases"],
        q["bound_success_endpoints"],
    ]
    shown = [np.log10(value + 1) for value in values]
    bars = ax.bar(np.arange(5), shown, color=[OPAQUE, "#4D9B8C", "#E2A447", MISINDEXED, NOMINAL])
    ax.set_xticks(np.arange(5), labels)
    ax.set_ylabel("log10(count + 1)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            str(value),
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    return _save(fig, output_dir, "figure-1-controlled-apparatus")


def figure_2(data: dict[str, Any], output_dir: Path) -> list[Path]:
    demo = data["g2_v0_4"]["one_experiment_demonstration"]
    fig, (ax, ledger_ax) = plt.subplots(
        1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [2.3, 1]}
    )
    fig.suptitle("One agent-directed experiment", fontsize=15, fontweight="bold", color=TEXT)
    _panel(ax, "A", "Seven self-selected primitive operations")
    sequence = demo["operation_signature"]
    x = np.arange(len(sequence))
    colors = ["#4D9B8C", "#4D9B8C", "#E2A447", OPAQUE, MISINDEXED, "#6F7782", NOMINAL]
    ax.scatter(x, [0] * len(x), s=900, c=colors, edgecolor="white", linewidth=2, zorder=3)
    ax.plot(x, [0] * len(x), color=GRID, lw=4, zorder=1)
    for index, label in enumerate(sequence):
        ax.text(
            index, 0, str(index + 1), ha="center", va="center", color="white", fontweight="bold"
        )
        ax.text(
            index,
            -0.18 if index % 2 == 0 else 0.18,
            label.replace("_", "\n"),
            ha="center",
            va="center",
            fontsize=8,
        )
    ax.set_xlim(-0.6, len(x) - 0.4)
    ax.set_ylim(-0.42, 0.42)
    ax.axis("off")
    ax.text(
        0.02,
        0.04,
        f"final assay score = {demo['final_score']:.3f}",
        transform=ax.transAxes,
        fontweight="bold",
        color=NOMINAL,
    )
    ax.text(0.02, -0.05, demo["label"], transform=ax.transAxes, fontsize=8, color="#6F7782")

    _panel(ledger_ax, "B", "Campaign resource receipt")
    ledger = demo["campaign_resource_endpoints"]
    ledger_ax.axis("off")
    entries = [
        ("vessels", f"{ledger['vessel_starts']}/6"),
        ("final assays", f"{ledger['final_assays']}/6"),
        ("nonfinal instruments", f"{ledger['nonfinal_instrument_uses']}/18"),
        ("operation attempts", f"{ledger['operation_attempts']}/144"),
        ("reagent used", f"{ledger['stocks_used']['reagent_mol']:.2f}/0.48 mol"),
        ("solvent used", f"{ledger['stocks_used']['solvent_L']:.2f}/0.96 L"),
    ]
    for index, (label, value) in enumerate(entries):
        y = 0.86 - index * 0.14
        ledger_ax.text(0.02, y, label, transform=ledger_ax.transAxes, color="#6F7782")
        ledger_ax.text(
            0.98, y, value, transform=ledger_ax.transAxes, ha="right", fontweight="bold", color=TEXT
        )
        ledger_ax.plot(
            [0.02, 0.98], [y - 0.05, y - 0.05], color=GRID, lw=0.7, transform=ledger_ax.transAxes
        )
    ledger_ax.text(
        0.02,
        0.01,
        "Receipt is reconstructed from the immutable trajectory.",
        transform=ledger_ax.transAxes,
        fontsize=8,
        color="#6F7782",
    )
    fig.tight_layout()
    return _save(fig, output_dir, "figure-2-one-autonomous-experiment")


def figure_3(data: dict[str, Any], output_dir: Path) -> list[Path]:
    cells = data["g2_v0_4"]["cell_rows"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    fig.suptitle(
        "Endpoint summaries conceal distinct experimental trajectories",
        fontsize=15,
        fontweight="bold",
        color=TEXT,
    )
    for panel_index, (ax, seed) in enumerate(zip(axes, (0, 2, 4), strict=True)):
        _panel(ax, chr(ord("A") + panel_index), f"physical world {seed}")
        for arm, color in (("opaque", OPAQUE), ("nominal", NOMINAL)):
            row = next(item for item in cells if item["world_seed"] == seed and item["arm"] == arm)
            scores = row["final_score_sequence"]
            ax.plot(np.arange(1, len(scores) + 1), scores, "o-", color=color, lw=1.8, label=arm)
            best_index = int(np.argmax(scores))
            ax.scatter(
                best_index + 1,
                scores[best_index],
                s=120,
                facecolors="none",
                edgecolors=color,
                linewidth=2,
            )
        ax.set_xlabel("final assay ordinal")
        ax.set_xticks(range(1, 7))
        ax.set_ylim(-0.03, 0.92)
        ax.grid(color=GRID, lw=0.6)
        if panel_index == 0:
            ax.set_ylabel("final assay score")
            ax.legend(loc="lower right")
    fig.tight_layout()
    return _save(fig, output_dir, "figure-3-behaviorally-distinct-trajectories")


def figure_4(data: dict[str, Any], output_dir: Path) -> list[Path]:
    g0_rows = data["g0"]["task_arm_rows"]
    g2_pairs = data["g2_v0_4"]["paired_world_rows"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.2))
    fig.suptitle(
        "Prior interventions reshape behavior without guaranteeing recovery",
        fontsize=15,
        fontweight="bold",
        color=TEXT,
        y=1.01,
    )
    contrast_rows = [row for row in g0_rows if row["arm"] == "derived_contrasts"]

    ax = axes[0, 0]
    _panel(ax, "A", "Correct material information: task-level effects")
    for index, row in enumerate(contrast_rows):
        mean = row["nominal_minus_opaque_mean"]
        low, high = row["nominal_minus_opaque_familywise_97_5_interval"]
        ax.errorbar(
            mean, index, xerr=[[mean - low], [high - mean]], fmt="o", color=NOMINAL, capsize=4
        )
    ax.axvline(0, color="#6F7782", lw=1)
    ax.set_yticks(
        range(len(contrast_rows)), [row["task_id"].replace("-", " ") for row in contrast_rows]
    )
    ax.set_xlabel("nominal - opaque final score")
    ax.grid(axis="x", color=GRID, lw=0.6)

    ax = axes[0, 1]
    _panel(ax, "B", "Misindexed prior changes actions")
    y = np.arange(len(contrast_rows))
    width = 0.32
    ax.barh(
        y - width / 2,
        [r["early_misleading_share_misindexed"] for r in contrast_rows],
        height=width,
        color=MISINDEXED,
        label="early",
    )
    ax.barh(
        y + width / 2,
        [r["late_misleading_share_misindexed"] for r in contrast_rows],
        height=width,
        color="#C7B5E8",
        label="late",
    )
    ax.set_yticks(y, [row["task_id"].replace("-", " ") for row in contrast_rows])
    ax.set_xlim(0, 1)
    ax.set_xlabel("misleading-action share")
    ax.legend()
    ax.grid(axis="x", color=GRID, lw=0.6)

    ax = axes[1, 0]
    _panel(ax, "C", "Recovery is a conjunction, not a label")
    components = ["manipulation", "action correction", "performance recovery", "joint recovery"]
    matrix = []
    for row in contrast_rows:
        matrix.append(
            [
                row["manipulation_check_passed"],
                row["differential_action_correction_passed"],
                row["performance_recovery_to_opaque_passed"],
                row["overall_recovery_claim_passed"],
            ]
        )
    image = ax.imshow(
        np.asarray(matrix, dtype=float),
        vmin=0,
        vmax=1,
        cmap=mpl.colors.ListedColormap(["#E8EBEF", "#4D9B8C"]),
        aspect="auto",
    )
    del image
    ax.set_xticks(range(4), components, rotation=20, ha="right")
    ax.set_yticks(
        range(len(contrast_rows)), [row["task_id"].replace("-", " ") for row in contrast_rows]
    )
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            ax.text(
                col_index,
                row_index,
                "pass" if value else "fail",
                ha="center",
                va="center",
                color="white" if value else "#6F7782",
                fontweight="bold",
            )

    ax = axes[1, 1]
    _panel(ax, "D", "Autonomous trajectory effects differ by world")
    metrics = [
        ("global_best_discovery_fraction", "discovery time"),
        ("online_incumbent_retention_rate", "retention"),
        ("maximum_absolute_incumbent_drawdown", "drawdown"),
        ("terminal_to_global_best_ratio", "terminal / best"),
    ]
    for metric_index, (key, _label) in enumerate(metrics):
        values = [row[key] for row in g2_pairs]
        jitter = np.linspace(-0.13, 0.13, len(values))
        ax.scatter(
            np.full(len(values), metric_index) + jitter,
            values,
            c=[OPAQUE if value < 0 else NOMINAL for value in values],
            s=48,
            edgecolor="white",
            linewidth=0.6,
        )
        ax.hlines(np.mean(values), metric_index - 0.22, metric_index + 0.22, color=TEXT, lw=2)
    ax.axhline(0, color="#6F7782", lw=1)
    ax.set_xticks(range(len(metrics)), [label for _, label in metrics], rotation=18, ha="right")
    ax.set_ylabel("nominal - opaque")
    ax.grid(axis="y", color=GRID, lw=0.6)
    fig.tight_layout()
    return _save(fig, output_dir, "figure-4-prior-reshapes-behavior")


def figure_5(data: dict[str, Any], output_dir: Path) -> list[Path]:
    replication = data["g2_v0_5"]
    if replication is None:
        return []
    metrics = [
        ("best_final_score", "best score"),
        ("global_best_discovery_fraction", "discovery"),
        ("online_incumbent_retention_rate", "retention"),
        ("maximum_absolute_incumbent_drawdown", "drawdown"),
        ("terminal_to_global_best_ratio", "terminal / best"),
    ]
    classifications = replication["interpretation"]["selected_branch"][
        "world_metric_classifications"
    ]
    fig, axes = plt.subplots(2, 5, figsize=(15, 6.2), sharex="col")
    fig.suptitle(
        "Fresh trajectories test within-world repeatability",
        fontsize=15,
        fontweight="bold",
        color=TEXT,
    )
    for row_index, seed in enumerate((1, 3)):
        pair_rows = [row for row in replication["paired_trajectories"] if row["world_seed"] == seed]
        for col_index, (metric, label) in enumerate(metrics):
            ax = axes[row_index, col_index]
            if row_index == 0:
                _panel(ax, chr(ord("A") + col_index), label)
            values = []
            labels = []
            censored = []
            for row in pair_rows:
                labels.append(row["trajectory_replicate_id"])
                delta = row["nominal_minus_opaque"]
                values.append(None if delta is None else delta[metric])
                censored.append(delta is None)
            y = np.arange(len(values))
            for yi, value, is_censored in zip(y, values, censored, strict=True):
                if is_censored:
                    ax.scatter(0, yi, marker="x", color="#6F7782", s=60)
                else:
                    ax.scatter(
                        value,
                        yi,
                        color=NOMINAL if value >= 0 else OPAQUE,
                        s=55,
                        edgecolor="white",
                        linewidth=0.6,
                    )
            ax.axvline(0, color="#6F7782", lw=1)
            classification = classifications[str(seed)][metric].replace("directionally_", "")
            ax.text(
                0.97,
                1.02,
                classification,
                transform=ax.transAxes,
                ha="right",
                va="bottom",
                fontsize=7.5,
                color="#6F7782",
                bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.8},
            )
            ax.set_yticks(y, labels if col_index == 0 else [])
            if col_index == 0:
                ax.set_ylabel(f"world {seed}\nreplicate")
            ax.grid(axis="x", color=GRID, lw=0.6)
            if row_index == 1:
                ax.set_xlabel("nominal - opaque")
    fig.tight_layout()
    return _save(fig, output_dir, "figure-5-within-world-replication")


def figure_6(data: dict[str, Any], output_dir: Path) -> list[Path]:
    g0_rows = [row for row in data["g0"]["task_arm_rows"] if row["arm"] == "opaque"]
    g2 = data["g2_v0_4"]["arm_descriptive_aggregates"]
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [1.1, 1]})
    fig.suptitle(
        "Experimental intelligence is a profile, not a scalar",
        fontsize=15,
        fontweight="bold",
        color=TEXT,
    )
    _panel(ax, "A", "Compiled control: task profiles")
    compiled_metrics = [
        ("primary_score_mean", "endpoint score"),
        ("heldout_directional_accuracy", "held-out accuracy"),
        ("heldout_brier_score", "Brier score"),
        ("unsupported_claim_rate", "unsupported claims"),
    ]
    width = 0.34
    x = np.arange(len(compiled_metrics))
    for index, row in enumerate(g0_rows):
        values = [row[key] for key, _ in compiled_metrics]
        ax.bar(
            x + (index - 0.5) * width,
            values,
            width=width,
            label=row["task_id"].replace("-", " "),
            color=OPAQUE if index == 0 else NOMINAL,
        )
    ax.set_xticks(x, [label for _, label in compiled_metrics], rotation=18, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("reported metric (no composite score)")
    ax.legend(fontsize=8)
    ax.grid(axis="y", color=GRID, lw=0.6)

    _panel(bx, "B", "Agent-directed control: trajectory profiles")
    trajectory_metrics = [
        ("mean_completion_rate", "completion"),
        ("trajectory_learning.mean_online_retention_rate", "retention"),
        ("trajectory_learning.pooled_recovery_rate", "recovery"),
        ("trajectory_learning.mean_terminal_to_global_best_ratio", "terminal / best"),
    ]
    for index, (arm, color) in enumerate((("opaque", OPAQUE), ("nominal", NOMINAL))):
        values = []
        for key, _ in trajectory_metrics:
            if "." in key:
                parent, child = key.split(".")
                values.append(g2[arm][parent][child])
            else:
                values.append(g2[arm][key])
        bx.bar(x + (index - 0.5) * width, values, width=width, label=arm, color=color)
    bx.set_xticks(x, [label for _, label in trajectory_metrics], rotation=18, ha="right")
    bx.set_ylim(0, 1)
    bx.set_ylabel("reported metric (no composite score)")
    bx.legend()
    bx.grid(axis="y", color=GRID, lw=0.6)
    fig.tight_layout()
    return _save(fig, output_dir, "figure-6-experimental-intelligence-profiles")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "derived_data",
        nargs="?",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("paper/figures/experimental-intelligence-v1"),
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/figure-manifest.json"),
    )
    return parser


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else REPOSITORY_ROOT / path


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data_path = _resolve(args.derived_data)
    data = _load(data_path)
    output_dir = _resolve(args.output_dir)
    _configure()
    outputs = []
    for renderer in (figure_1, figure_2, figure_3, figure_4, figure_5, figure_6):
        outputs.extend(renderer(data, output_dir))
    manifest = {
        "schema_version": "chemworld-arxiv-v1-figure-manifest-0.1",
        "status": data["status"],
        "derived_data_sha256": data["derived_data_sha256"],
        "figure_5_rendered": data["g2_v0_5"] is not None,
        "files": [
            {
                "path": path.relative_to(REPOSITORY_ROOT).as_posix(),
                "sha256": _sha(path),
                "bytes": path.stat().st_size,
            }
            for path in outputs
        ],
    }
    manifest["manifest_sha256"] = hashlib.sha256(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    ).hexdigest()
    manifest_path = _resolve(args.manifest_output)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": data["status"],
                "figure_file_count": len(outputs),
                "figure_5_rendered": manifest["figure_5_rendered"],
                "manifest": manifest_path.as_posix(),
            },
            sort_keys=True,
        )
    )
    return 0 if data["status"] == "frozen_complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
