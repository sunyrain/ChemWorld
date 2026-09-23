"""Read retained C reports and plot the selected pair; no new experiments."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto"
OUT = ROOT / "output/figures/research-case-v16"
OUT.mkdir(parents=True, exist_ok=True)
BLUE, TEAL, FAIL, INK = "#0066DB", "#009BB5", "#BA6A56", "#24282C"


def read_session(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    status = re.search(r"^Status: (.+)$", text, re.M).group(1)
    budget = int(re.search(r"-B(\d+)-", path.stem).group(1))
    rows = []
    best = None
    for match in re.finditer(r"^## Batch (\d+)\s*\n```json\s*\n(.*?)\n```", text, re.M | re.S):
        batch = json.loads(match.group(2))
        m = batch["metrics"]
        eligible = m["crystal_purity"] >= 0.8 and m["crystal_fines_fraction"] <= 0.5 and m["crystal_size"] > 0
        recovery = m["crystal_yield"] * 100
        if eligible:
            best = recovery if best is None else max(best, recovery)
        rows.append({
            "batch": int(match.group(1)), "recovery_pct": recovery,
            "purity_pct": m["crystal_purity"] * 100,
            "fines_pct": m["crystal_fines_fraction"] * 100,
            "quality_feasible": eligible, "best_feasible_recovery_pct": best,
        })
    feasible = [r for r in rows if r["quality_feasible"]]
    return {
        "session": path.stem, "source": path.relative_to(ROOT).as_posix(),
        "status": status, "budget": budget, "completed_batches": len(rows),
        "feasible_batches": len(feasible),
        "first_feasible_batch": feasible[0]["batch"] if feasible else None,
        "first_feasible_recovery_pct": feasible[0]["recovery_pct"] if feasible else None,
        "best_feasible_batch": max(feasible, key=lambda r: r["recovery_pct"])["batch"] if feasible else None,
        "best_feasible_recovery_pct": best, "rows": rows,
    }


def main() -> None:
    sessions = [read_session(p) for p in sorted(SOURCE.glob("C-W*-B*-E-*.md"))]
    pair = [next(s for s in sessions if s["session"] == f"C-W05-B{b}-E-Aligned") for b in (12, 24)]
    assert [s["completed_batches"] for s in pair] == [12, 24]
    assert [s["feasible_batches"] for s in pair] == [10, 5]
    assert [s["first_feasible_batch"] for s in pair] == [1, 20]
    assert [s["best_feasible_batch"] for s in pair] == [10, 23]
    assert all(r["purity_pct"] >= 80 for s in pair for r in s["rows"])
    payload = {
        "source_report_count": len(sessions), "status_counts": dict(Counter(s["status"] for s in sessions)),
        "recorded_batch_count": sum(s["completed_batches"] for s in sessions),
        "quality_rule": "purity >= 0.80, fines <= 0.50, crystal_size > 0",
        "series_rule": "All recorded batch results; running maximum over quality-feasible batches only; null before first feasible batch.",
        "pair": pair, "screen": [{k: v for k, v in s.items() if k != "rows"} for s in sessions],
    }
    (OUT / "data.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with (OUT / "batch-progress.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["session", *pair[0]["rows"][0]])
        writer.writeheader()
        writer.writerows({"session": s["session"], **r} for s in pair for r in s["rows"])
    plt.rcParams.update({"font.family": "Arial", "font.size": 11, "text.color": INK,
                         "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42, "svg.fonttype": "none"})
    fig, axes = plt.subplots(2, 2, figsize=(13, 6.7), gridspec_kw={"height_ratios": [1.35, 1]}, sharex="col")
    fig.subplots_adjust(left=.075, right=.985, top=.90, bottom=.18, wspace=.19, hspace=.16)
    for col, (session, color) in enumerate(zip(pair, [BLUE, TEAL], strict=True)):
        rows = session["rows"]
        x = [r["batch"] for r in rows]
        ax, lower = axes[:, col]
        ax.set_title(f'{session["budget"]}-batch session', loc="left", fontsize=13, weight="bold", pad=9)
        ax.plot(x, [r["recovery_pct"] for r in rows], color="#CED3D7", lw=.85, zorder=1)
        good = [r for r in rows if r["quality_feasible"]]
        bad = [r for r in rows if not r["quality_feasible"]]
        for target, field in [(ax, "recovery_pct"), (lower, "fines_pct")]:
            target.scatter([r["batch"] for r in good], [r[field] for r in good], s=32, c=color, zorder=4)
            target.scatter([r["batch"] for r in bad], [r[field] for r in bad], s=34, marker="x", color=FAIL, linewidths=1.2, zorder=4)
            target.grid(axis="y", color="#ECEFF1", lw=.6)
            target.set_axisbelow(True)
        valid = [r for r in rows if r["best_feasible_recovery_pct"] is not None]
        ax.step([r["batch"] for r in valid], [r["best_feasible_recovery_pct"] for r in valid], where="post", color=color, lw=2, zorder=3)
        ax.set_ylim(20, 66)
        ax.set_yticks([20, 30, 40, 50, 60])
        lower.plot(x, [r["fines_pct"] for r in rows], color="#CED3D7", lw=.8, zorder=1)
        lower.axhline(50, color="#68727A", lw=1, ls=(0, (4, 3)))
        lower.set_ylim(0, 108)
        lower.set_yticks([0, 50, 100])
        lower.set_xlim(.5, session["budget"] + .65)
        lower.set_xticks([1, 3, 6, 9, 12] if col == 0 else [1, 4, 8, 12, 16, 20, 24])
        lower.set_xlabel("Batch")
        if col == 0:
            ax.set_ylabel("Recovery (%)")
            lower.set_ylabel("Fines (%)")
            ax.annotate("First feasible: 34.7%", (1, rows[0]["recovery_pct"]), xytext=(2.0, 24.5), fontsize=10,
                        arrowprops={"arrowstyle": "-", "lw": .7, "color": "#7E878D"})
            ax.annotate("Best: 51.2%", (10, rows[9]["recovery_pct"]), xytext=(7.3, 60.3), fontsize=10,
                        arrowprops={"arrowstyle": "-", "lw": .7, "color": "#7E878D"})
        else:
            ax.annotate("First feasible: batch 20", (20, rows[19]["recovery_pct"]), xytext=(6.0, 59.5), fontsize=10,
                        arrowprops={"arrowstyle": "-", "lw": .7, "color": "#7E878D"})
            ax.annotate("57.0%", (23, rows[22]["recovery_pct"]), xytext=(20.3, 64.0), fontsize=10,
                        arrowprops={"arrowstyle": "-", "lw": .7, "color": "#7E878D"})
        lower.text(.03, .58, "Fines limit: 50%", transform=lower.transAxes, fontsize=9, color="#525B62", bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})
    handles = [Line2D([], [], marker="o", ls="none", color=BLUE, label="Quality-feasible batch"),
               Line2D([], [], marker="x", ls="none", color=FAIL, label="Quality-infeasible batch"),
               Line2D([], [], color=BLUE, lw=2, drawstyle="steps-post", label="Best feasible recovery so far")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.53, .065), ncol=3, frameon=False, fontsize=10)
    fig.text(.075, .035, "Independent sessions, not a continuous 36-batch run. All shown batches meet the purity threshold.", fontsize=9, color="#525B62")
    for ext in ("png", "pdf", "svg"):
        fig.savefig(OUT / f"batch-progress.{ext}", dpi=260, facecolor="white")
    plt.close(fig)
    print(json.dumps({"reports": len(sessions), "statuses": payload["status_counts"],
                      "recorded_batches": payload["recorded_batch_count"],
                      "pair": [{k: v for k, v in s.items() if k != "rows"} for s in pair]}, indent=2))


if __name__ == "__main__":
    main()
