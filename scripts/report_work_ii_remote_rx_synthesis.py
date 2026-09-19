"""Summarize published RX source records without accessing withheld reference truth."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")


def parse(text, path, commit):
    def field(label):
        found = re.search(rf"^- {re.escape(label)}: `([^`]+)`", text, re.M)
        assert found, (path, label)
        return found.group(1)

    batches = []
    for payload in re.findall(r"```json\s*\n(.*?)\n```", text, re.S):
        obj = json.loads(payload)
        if isinstance(obj, dict) and {"actions", "metrics", "ordinal"} <= obj.keys():
            batches.append(obj)
    assert len(batches) == 12 and {b["ordinal"] for b in batches} == set(range(1, 13)), path
    selected = int(field("Selected batch"))
    chosen = next(b for b in batches if b["ordinal"] == selected)
    valid = dict(re.findall(r"^\| (K1|Q|K2) \| (yes|no) \|", text, re.M))
    assert set(valid) == {"K1", "Q", "K2"}, path
    operations = sum(len(b["actions"]) for b in batches)
    assert operations == int(field("Operations")), (path, operations)
    temps, durations, dose_ratios = set(), set(), set()
    middle_measurements = 0
    total_measurements = 0
    for batch in batches:
        actions = batch["actions"]
        heating = [a for a in actions if a["operation"] == "heat"]
        temps.update(a["target_temperature_K"] for a in heating)
        durations.add(sum(a["duration_s"] for a in heating))
        catalyst = sum(
            a["catalyst_amount_mol"] for a in actions if a["operation"] == "add_catalyst"
        )
        reagent = sum(a["amount_mol"] for a in actions if a["operation"] == "add_reagent")
        dose_ratios.add(round(catalyst / reagent, 12))
        for i, action in enumerate(actions):
            if action["operation"] == "measure" and action["instrument"] != "final_assay":
                total_measurements += 1
                if any(a["operation"] == "heat" for a in actions[:i]) and any(
                    a["operation"] == "heat" for a in actions[i + 1 :]
                ):
                    middle_measurements += 1
    return {
        "cell_id": text.splitlines()[0].removeprefix("# "),
        **{k.lower(): field(k) for k in ("World", "Locus", "Goal", "Arm", "Status")},
        "source_status": field("Source status"),
        "batches": len(batches),
        "operations": operations,
        "replay_verified": bool(
            re.search(r"^- Exact replay.*(?:'verified': True|`True`)", text, re.M)
        ),
        "chain_sealed": field("Posttest chain sealed") == "True",
        "valid_posttests": {k: v == "yes" for k, v in valid.items()},
        "selected_batch": selected,
        "selected_source_metrics": chosen["metrics"],
        "observed_best_score": max(b["metrics"]["score"] for b in batches),
        "nonfinal_measurements": total_measurements,
        "measurements_between_heat_actions": middle_measurements,
        "heat_target_values_K": sorted(temps),
        "total_heat_duration_values_s": sorted(durations),
        "catalyst_reagent_ratio_values": sorted(dose_ratios),
        "source_url": f"https://github.com/sunyrain/ChemWorld/blob/{commit}/{path}",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True)
    args = parser.parse_args()
    commit = git("rev-parse", args.ref).strip()
    paths = [
        p
        for p in git("ls-tree", "-r", "--name-only", commit).splitlines()
        if p.startswith(PREFIX) and p.endswith("/EXPERIMENT_REPORT.md")
    ]
    rows = [parse(git("show", f"{commit}:{p}"), p, commit) for p in paths]
    expected = {
        (f"RX-W{w:02d}", locus, goal, arm)
        for w in range(1, 5)
        for locus in ("P", "S")
        for goal in ("mechanism_discovery", "safety_constrained_optimization")
        for arm in ("Opaque", "Aligned", "MisIndexed")
    }
    assert len(rows) == 48
    assert {(r["world"], r["locus"], r["goal"], r["arm"]) for r in rows} == expected
    assert all(r["source_status"] == "completed" and r["replay_verified"] for r in rows)
    by = {(r["world"], r["locus"], r["goal"], r["arm"]): r for r in rows}
    pairs = []
    for row in rows:
        if row["goal"] != "mechanism_discovery":
            continue
        opt = by[(row["world"], row["locus"], "safety_constrained_optimization", row["arm"])]
        pairs.append(
            {
                "world": row["world"],
                "locus": row["locus"],
                "arm": row["arm"],
                "source_score_opt_minus_discovery": opt["selected_source_metrics"]["score"]
                - row["selected_source_metrics"]["score"],
                "both_chains_sealed": row["chain_sealed"] and opt["chain_sealed"],
            }
        )
    counts = {
        "published_cells": len(rows),
        "source_batches": sum(r["batches"] for r in rows),
        "operations": sum(r["operations"] for r in rows),
        "sealed_chains": sum(r["chain_sealed"] for r in rows),
        "valid_posttests": sum(sum(r["valid_posttests"].values()) for r in rows),
        "nonfinal_measurements": sum(r["nonfinal_measurements"] for r in rows),
        "cells_varying_catalyst_reagent_ratio": sum(
            len(r["catalyst_reagent_ratio_values"]) > 1 for r in rows
        ),
        "cells_measuring_between_heat_actions": sum(
            r["measurements_between_heat_actions"] > 0 for r in rows
        ),
    }
    assert counts["sealed_chains"] == 47 and counts["valid_posttests"] == 143
    groups = []
    for locus in ("P", "S"):
        for goal in ("mechanism_discovery", "safety_constrained_optimization"):
            part = [r for r in rows if (r["locus"], r["goal"]) == (locus, goal)]
            groups.append(
                {
                    "locus": locus,
                    "goal": goal,
                    "cells": len(part),
                    "mean_selected_source_score": mean(
                        r["selected_source_metrics"]["score"] for r in part
                    ),
                    "varying_dose_ratio": sum(
                        len(r["catalyst_reagent_ratio_values"]) > 1 for r in part
                    ),
                    "measuring_between_heats": sum(
                        r["measurements_between_heat_actions"] > 0 for r in part
                    ),
                }
            )
    data = {
        "remote_commit": commit,
        "scope": "Published W01-W04 source records; reference truth remains withheld",
        "counts": counts,
        "groups": groups,
        "goal_pairs": pairs,
        "incomplete_cells": [r["cell_id"] for r in rows if not r["chain_sealed"]],
        "prediction_accuracy": None,
        "recommendation_retest": None,
        "rows": rows,
    }
    out = ROOT / "workstreams/flagship_tasks/reports/work-ii-rx-remote-synthesis-20260919"
    out.mkdir(exist_ok=True)
    (out / "summary.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Published RX source-record synthesis",
        "",
        f"Remote snapshot: `{commit}`.",
        "",
        "This analysis reads the published records only. It does not generate, access or estimate "
        "the withheld reference truth.",
        "",
        "## Coverage",
        "",
        "```json",
        json.dumps(counts, indent=2),
        "```",
        "",
        "All 48 physical sources completed and their reports record verified replay. "
        "One chain is incomplete:",
        "",
        *[
            f"- {s}: missing K1; valid Q/K2 do not repair the sealing order."
            for s in data["incomplete_cells"]
        ],
        "",
        "## Observed source behavior",
        "",
        "Scores below belong to the recommended batch observed during exploration, "
        "not an independent retest. They are not comparable to EC or PA scores.",
        "",
        "| Locus | Goal | Cells | Mean selected source score "
        "| Varying dose ratio | Measurement between heats |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for g in groups:
        lines.append(
            f"| {g['locus']} | {g['goal']} | {g['cells']} "
            f"| {g['mean_selected_source_score']:.5f} | {g['varying_dose_ratio']} "
            f"| {g['measuring_between_heats']} |"
        )
    for locus in ("P", "S"):
        p = [x for x in pairs if x["locus"] == locus]
        lines += [
            "",
            f"{locus}: optimization has a higher selected source score in "
            f"{sum(x['source_score_opt_minus_discovery'] > 0 for x in p)}/{len(p)} "
            "matched conditions.",
        ]
    lines += [
        "",
        "These are descriptive action counts: a measurement between heat calls does not establish "
        "a model reflection or feedback-dependent decision. Dose variation is not a "
        "mechanism-discovery score. P/S Opaque sources have the same prior input but different "
        "prediction questions; their difference is not a prior-locus treatment effect.",
        "",
        "## Complete source index",
        "",
        "| Cell | Sealed chain | Source score |",
        "|---|:---:|---:|",
    ]
    lines += [
        f"| [{r['cell_id']}]({r['source_url']}) | {r['chain_sealed']} "
        f"| {r['selected_source_metrics']['score']:.5f} |"
        for r in rows
    ]
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "RX contributes parameter and structural prior interventions, time/temperature/history "
        "experiments, free mechanism reports and paired research objectives. Prediction errors, "
        "calibrated interval coverage, independently retested recommendations and causal "
        "explanations of failures are not established by these published records. Do not pool "
        "it with the completed EC/PA prediction analysis or call all nine systems completed.",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"output": str(out), **counts, "groups": groups}))


if __name__ == "__main__":
    main()
