"""Publication figure for the original two-configuration disclosure experiment."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "paper/figures/prior-discovery"
COLORS = ("#94A3B0", "#007C91")
MODELS = ("gpt", "deepseek")
LABELS = ("GPT / medium", "DeepSeek Flash / low")
INFORMATION = ("original", "complete")


def load_report() -> tuple[dict, Path]:
    binding = json.loads((ROOT / "configs/current.json").read_text(encoding="utf-8"))["work_ii"][
        "w2_87_information_completeness"
    ]
    path = ROOT / binding["combined_report"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != binding["combined_report_sha256"]:
        raise ValueError("current combined report changed")
    report = json.loads(path.read_text(encoding="utf-8"))
    if not report["formal_result"] or report["scheduled"] != 120 or report["worlds"] != 10:
        raise ValueError("use the original formal denominator, never selected retry outcomes")
    return report, path


def render(report: dict) -> list[dict]:
    stem = "figure-10-information-models"
    groups = [g for g in report["groups"] if g["analysis"] == "recovery"]
    paired = {(g["model"], g["information"]): g for g in groups}
    data = OUTPUT / "source_data" / f"{stem}-groups.csv"
    with data.open("w", encoding="utf-8", newline="") as handle:
        keys = [
            "model",
            "information",
            "scheduled",
            "joint_recovery",
            "top1",
            "post_mae_mean",
            "post_mae_available_n",
            "mean_normalized_regret_failure_aware",
        ]
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: g[k] for k in keys} for g in groups)
    with plt.rc_context(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": "#7D8B94",
            "axes.linewidth": 0.65,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
        }
    ):
        fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.15))
        fig.subplots_adjust(
            left=0.095, right=0.975, top=0.80, bottom=0.16, wspace=0.37, hspace=0.60
        )
        fig.text(
            0.095,
            0.97,
            "Information helps structure; action gains differ",
            fontsize=14,
            weight="bold",
            va="top",
            color="#20343F",
        )
        fig.legend(
            handles=[
                Patch(facecolor=color, label=label)
                for color, label in zip(
                    COLORS, ("Original formula", "Complete observation mapping"), strict=True
                )
            ],
            loc="upper left",
            bbox_to_anchor=(0.082, 0.925),
            ncol=2,
            frameon=False,
            fontsize=9,
            handlelength=1.2,
            columnspacing=1.8,
        )
        panels = (
            ("joint_recovery", "A  Structure recovery", "Success / scheduled", True),
            ("top1", "B  Optimal action choice", "Top-1 / scheduled", True),
            ("post_mae_mean", "C  Held-out prediction", "Mean absolute error", False),
            (
                "mean_normalized_regret_failure_aware",
                "D  Decision loss",
                "Normalized regret",
                False,
            ),
        )
        for ax, (metric, title, ylabel, rate) in zip(axes.flat, panels, strict=True):
            for i, model in enumerate(MODELS):
                for j, info in enumerate(INFORMATION):
                    group = paired[model, info]
                    value = group[metric] / group["scheduled"] if rate else group[metric]
                    x = i + (j - 0.5) * 0.32
                    ax.bar(x, value, width=0.27, color=COLORS[j], zorder=3)
                    label = f"{group[metric]}/{group['scheduled']}" if rate else f"{value:.3f}"
                    if metric == "post_mae_mean":
                        label += f"\nn={group['post_mae_available_n']}"
                    ax.annotate(
                        label,
                        (x, value),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        fontsize=8,
                        color="#20343F",
                    )
            ax.set(xticks=[0, 1], xticklabels=LABELS, ylabel=ylabel, xlim=(-0.55, 1.55))
            ax.set_title(title, loc="left", pad=9)
            ax.grid(axis="y", color="#E8EEF1", linewidth=0.6, zorder=0)
            ax.tick_params(axis="both", length=3, color="#7D8B94", labelsize=8)
            if rate:
                ax.set(ylim=(0, 1.18), yticks=[0, 0.5, 1])
                ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
            elif metric == "post_mae_mean":
                ax.set(ylim=(0, 0.068), yticks=[0, 0.02, 0.04, 0.06])
            else:
                ax.set(ylim=(0, 0.30), yticks=[0, 0.1, 0.2, 0.3])
        fig.text(
            0.095,
            0.075,
            "Unknown / wrong priors; 10 shared worlds. All original failures retained.",
            fontsize=8.3,
            color="#526570",
        )
        fig.text(
            0.095,
            0.037,
            "Recovery gain: +70 pp in each configuration; pooled approximate 95% CI [+52.5, +85].",
            fontsize=8.3,
            color="#526570",
        )
        outputs = []
        for suffix in ("pdf", "svg", "png"):
            path = OUTPUT / f"{stem}.{suffix}"
            fig.savefig(path, dpi=300)
            if suffix == "svg":
                path.write_text(
                    "\n".join(
                        line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
                    )
                    + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
            outputs.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
            )
        plt.close(fig)
    return outputs


if __name__ == "__main__":
    report, _ = load_report()
    print(json.dumps(render(report), indent=2))
