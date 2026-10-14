"""Read-only export of the fixed 30-session research-opportunity comparison."""

from __future__ import annotations

import argparse
import copy
import json
import time
from pathlib import Path
from statistics import fmean

from scripts.analyze_inquiry_completion import OUTPUT, mean
from scripts.analyze_inquiry_trajectories import public_events
from scripts.report_paper_case_notebooks import notebook_record, posttest_record, token_accounting
from scripts.run_inquiry_completion import ARMS, STAGES, eq
from scripts.run_paper_case_notebooks import case_folder, read, write

METRICS = eq.METRICS
DILUTE = {"Q03", "Q08", "Q09"}


def scientific_public_context(value):
    value = copy.deepcopy(value)
    # Random run label is public bookkeeping, with no chemical or budget semantics.
    value["initial_public_state"]["campaign_state"].pop("campaign_id", None)
    return value


def score_queries(payload, truth):
    rows = []
    for prediction in payload["predictions"]:
        qid = prediction["query_id"]
        response = {}
        for metric in METRICS:
            interval = prediction["metrics"][metric]
            point, low, high = (interval[k] for k in ("estimate", "lower80", "upper80"))
            observations = [r[metric] for r in truth[qid]]
            response[metric] = {
                "estimate": point,
                "lower80": low,
                "upper80": high,
                "reference_mean": fmean(observations),
                "reference_observations": observations,
                "mae": abs(point - fmean(observations)),
                "coverage80": fmean(low <= x <= high for x in observations),
                "width80": high - low,
                "interval_score80": fmean(
                    high - low + 10 * max(low - x, x - high, 0) for x in observations
                ),
            }
        rows.append({"query_id": qid, "dilute": qid in DILUTE, "metrics": response})
    groups = {}
    for name in ("all", "dilute", "other"):
        selected = [r for r in rows if name == "all" or r["dilute"] == (name == "dilute")]
        metric_scores = {
            m: {
                k: fmean(r["metrics"][m][k] for r in selected)
                for k in ("mae", "coverage80", "width80", "interval_score80")
            }
            for m in METRICS
        }
        groups[name] = {
            "queries": len(selected),
            "metrics": metric_scores,
            "macro_mae": fmean(v["mae"] for v in metric_scores.values()),
        }
    return {"queries": rows, "groups": groups}


def aggregate(rows):
    worlds = []
    for world in (f"W{x:02d}" for x in range(1, 6)):
        arms = {}
        for arm in ARMS:
            group = [r for r in rows if r["world"] == world and r["opportunity"] == arm]
            valid = [r for r in group if r.get("scores")]
            arms[arm] = {
                "planned": 3,
                "terminal": sum(r["status"] != "not_started" for r in group),
                "valid_Q": len(valid),
                "values": [
                    {
                        "repeat": r["repeat"],
                        "status": r["status"],
                        "macro_mae": r["scores"]["groups"]["all"]["macro_mae"]
                        if r.get("scores")
                        else None,
                    }
                    for r in group
                ],
                "groups": {
                    g: {
                        "macro_mae": mean([r["scores"]["groups"][g]["macro_mae"] for r in valid]),
                        "metrics": {
                            m: {
                                k: mean([r["scores"]["groups"][g]["metrics"][m][k] for r in valid])
                                for k in ("mae", "coverage80", "width80", "interval_score80")
                            }
                            for m in METRICS
                        },
                    }
                    for g in ("all", "dilute", "other")
                },
            }
        delta = {
            g: (
                arms["Research"]["groups"][g]["macro_mae"]
                - arms["NoResearch"]["groups"][g]["macro_mae"]
            )
            if all(arms[a]["valid_Q"] for a in ARMS)
            else None
            for g in ("all", "dilute", "other")
        }
        worlds.append({"world": world, "arms": arms, "research_minus_no_research": delta})
    equal = {
        a: {
            g: {
                "macro_mae": mean([w["arms"][a]["groups"][g]["macro_mae"] for w in worlds]),
                "metrics": {
                    m: {
                        k: mean([w["arms"][a]["groups"][g]["metrics"][m][k] for w in worlds])
                        for k in ("mae", "coverage80", "width80", "interval_score80")
                    }
                    for m in METRICS
                },
            }
            for g in ("all", "dilute", "other")
        }
        for a in ARMS
    }
    return {
        "worlds": worlds,
        "equal_world_means": equal,
        "paired_world_differences": {
            g: {
                "n": sum(w["research_minus_no_research"][g] is not None for w in worlds),
                "mean": mean([w["research_minus_no_research"][g] for w in worlds]),
            }
            for g in ("all", "dilute", "other")
        },
    }


def retained_attempt(parent, output):
    root = parent / "attempt-01"
    design = read(root / "design.json")
    units = []
    for unit in design["schedule"]:
        folder = case_folder(root / unit["repeat"], unit)
        if not folder.exists():
            continue
        trajectory = folder / "trajectory.jsonl"
        events = public_events(trajectory) if trajectory.exists() else []
        records = (
            [json.loads(line) for line in trajectory.read_text(encoding="utf-8").splitlines()]
            if trajectory.exists()
            else []
        )
        world = eq.world_by_id(design["eq_config"], f"EQ-{unit['world']}")
        replay = (
            eq.verify_records(
                records, tolerance=0, world_interventions=world["world_interventions"]
            ).to_dict()
            if records
            else None
        )
        receipts_path = folder / "private-provider/source-receipts.json"
        source = read(receipts_path)[-1] if receipts_path.exists() else {}
        units.append(
            {
                **unit,
                "disposition": "executor_startup_defect_retained_not_pooled",
                "operations": len(events),
                "completed_batches": sum(
                    e["action"].get("instrument") == "final_assay"
                    and e["transaction_status"] == "committed"
                    for e in events
                ),
                "exact_replay": replay,
                "source_usage": source.get("usage"),
                "source_elapsed_s": source.get("session_elapsed_s"),
                "sealed_posttests": 0,
            }
        )
    check = parent / "transport-check-01/provider"
    smoke = {
        stage: {
            k: v
            for k, v in read(check / stage / "receipt.json").items()
            if k in ("usage", "failure", "exit_code", "elapsed_s")
        }
        for stage in ("K1", "K2")
    }
    result = {
        "attempt": "attempt-01",
        "planned": 30,
        "launched": len(units),
        "not_started": 30 - len(units),
        "complete_chains": 0,
        "source_batches": sum(r["completed_batches"] for r in units),
        "reference": read(root / "references/complete.json"),
        "units": units,
        "transport_qualification": smoke,
        "interpretation": "Intact source data retained. Whole-block restart follows fixed policy; "
        "not a claim that every source or reference was contaminated.",
    }
    write(output / "retained_attempt.json", result)
    return result


def export(root, output, require_complete=False):
    design = read(root / "design.json")
    truth = read(root / "references/truth.json")["EQ"]
    rows = []
    for unit in design["schedule"]:
        result_path = root / unit["repeat"] / "results" / f"{unit['id']}.json"
        if not result_path.exists():
            rows.append({**unit, "status": "not_started", "scores": None})
            continue
        result = read(result_path)
        folder = case_folder(root / unit["repeat"], unit)
        posttests = {
            stage: posttest_record(folder, stage, turn)
            for stage, turn in result["posttests"].items()
        }
        source_usage = result.get("source_usage")
        if unit["opportunity"] == "NoResearch":
            source_usage = {
                "provider_token_accounting_complete": True,
                "input_token_count": 0,
                "cached_input_token_count": 0,
                "output_token_count": 0,
                "basis": "No source stage by design; known zero",
            }
        notes = notebook_record(folder)
        events = (
            public_events(folder / "trajectory.jsonl")
            if (folder / "trajectory.jsonl").exists()
            else []
        )
        valid = (result.get("prediction_evaluation") or {}).get("valid")
        scores = (
            score_queries(posttests["Q"]["payload"], truth[result["world_id"]]) if valid else None
        )
        if scores:
            for m in METRICS:
                original = result["prediction_evaluation"]["metrics"][m]["mae_to_five_repeat_mean"]
                if abs(scores["groups"]["all"]["metrics"][m]["mae"] - original) > 1e-12:
                    raise ValueError("Scoring mismatch")
        sealed = [
            s
            for s in STAGES
            if result["posttest_validation"].get(s, {}).get("valid")
            and not posttests.get(s, {}).get("failure")
        ]
        resources = {}
        for s in posttests:
            receipt = read(folder / "private-provider" / s / "receipt.json")
            resources[s] = {
                k: receipt.get(k)
                for k in (
                    "exit_code",
                    "failure",
                    "elapsed_s",
                    "numerics_budget",
                    "numerics_attempts",
                )
            }
        context_path = (
            folder
            / "private-provider"
            / (
                "source/initial-public-context.json"
                if unit["opportunity"] == "Research"
                else "initial-state/initial-public-context.json"
            )
        )
        row = {
            **unit,
            "status": result["status"],
            "failure": result.get("failure"),
            "source_status": result["source_status"],
            "source_batches": len(result["batches"]),
            "operations": result["operations"],
            "exact_replay": result.get("exact_replay"),
            "rollbacks": result["rollbacks"],
            "sealed_stages": sealed,
            "missing_stages": [s for s in STAGES if s not in sealed],
            "posttests": posttests,
            "posttest_validation": result["posttest_validation"],
            "posttest_resources": resources,
            "notebook_versions": notes["versions"],
            "notebook_validation": notes["validation"],
            "public_events": events,
            "initial_public_context": read(context_path),
            "scores": scores,
            "token_accounting": token_accounting(source_usage, posttests, equilibrium=True),
        }
        if unit["opportunity"] == "NoResearch" and (
            events or result["batches"] or notes["versions"]
        ):
            raise ValueError("NoResearch accessed source experiments")
        write(output / "sessions" / unit["repeat"] / f"{unit['id']}.json", row)
        rows.append(
            {
                k: v
                for k, v in row.items()
                if k
                not in (
                    "posttests",
                    "notebook_versions",
                    "notebook_validation",
                    "public_events",
                    "initial_public_context",
                )
            }
        )
    terminal = [r for r in rows if r["status"] != "not_started"]
    if require_complete and len(terminal) != 30:
        raise ValueError("Comparison not terminal")
    checks = []
    for repeat in sorted({r["repeat"] for r in rows}):
        for world in (f"W{x:02d}" for x in range(1, 6)):
            pair = [r for r in terminal if r["repeat"] == repeat and r["world"] == world]
            if len(pair) == 2:
                public = [
                    read(output / "sessions" / r["repeat"] / f"{r['id']}.json")[
                        "initial_public_context"
                    ]
                    for r in pair
                ]
                checks.append(
                    {
                        "repeat": repeat,
                        "world": world,
                        "exact_equal": public[0] == public[1],
                        "scientific_input_equal": scientific_public_context(public[0])
                        == scientific_public_context(public[1]),
                        "excluded_field": "initial_public_state/campaign_state/campaign_id",
                    }
                )
    result = {
        "scope": "EQ research-opportunity total package; common evaluation protocol",
        "provisional": len(terminal) != 30,
        "planned": 30,
        "terminal": len(terminal),
        "complete_chains": sum(r["status"] == "completed" for r in terminal),
        "valid_Q": sum(bool(r.get("scores")) for r in rows),
        "source_batches": sum(r.get("source_batches", 0) for r in terminal),
        "sealed_posttests": sum(len(r.get("sealed_stages", [])) for r in terminal),
        "reference": read(root / "references/complete.json"),
        "public_input_checks": checks,
        "source_commit": design["source_commit"],
        "runtime_surface": design["runtime_surface"],
        "experiment_note": design["experiment_note"],
        "sessions": rows,
        "comparison": aggregate(rows),
    }
    write(output / "opportunity_comparison.json", result)

    def fmt(v):
        return "missing" if v is None else f"{v:.6f}"

    lines = [
        "# Research-opportunity comparison",
        "",
        f"{'PROVISIONAL' if result['provisional'] else 'TERMINAL'}: {len(terminal)}/30 sessions; "
        f"{result['complete_chains']} complete chains; {result['valid_Q']} valid forecasts.",
        f"Source batches {result['source_batches']}/180; "
        f"sealed stages {result['sealed_posttests']}/120.",
        "",
        "Lower macro MAE is better. World means have equal weight; repeats are not worlds.",
        "",
        "| World | Research Q /3 | NoResearch Q /3 | Research MAE | NoResearch MAE | Difference |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for w in result["comparison"]["worlds"]:
        a, b = (w["arms"][arm] for arm in ARMS)
        lines.append(
            f"| {w['world']} | {a['valid_Q']} | {b['valid_Q']} | "
            f"{fmt(a['groups']['all']['macro_mae'])} | {fmt(b['groups']['all']['macro_mae'])} | "
            f"{fmt(w['research_minus_no_research']['all'])} |"
        )
    lines += [
        "",
        "| Query group | Research | NoResearch | Paired world difference |",
        "|---|---:|---:|---:|",
    ]
    for g in ("all", "dilute", "other"):
        means = result["comparison"]["equal_world_means"]
        diff = result["comparison"]["paired_world_differences"][g]
        lines.append(
            f"| {g} | {fmt(means['Research'][g]['macro_mae'])} | "
            f"{fmt(means['NoResearch'][g]['macro_mae'])} | {fmt(diff['mean'])} (n={diff['n']}) |"
        )
    lines += [
        "",
        "The package includes source experiments, observation history and notebook opportunity.",
        "Selection, feedback, notebook effects and internal learning are not isolated.",
        "Missing stages are retained. Model sampling seed is not controlled.",
        "Initial-public-input equality is reported per pair in the JSON; all scientific outputs",
        "and resource counts are exported without provider conversations or credentials.",
        "",
    ]
    (output / "OPPORTUNITY.md").write_text("\n".join(lines), encoding="utf-8")
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path, default=OUTPUT)
    p.add_argument("--watch", action="store_true")
    p.add_argument("--require-complete", action="store_true")
    p.add_argument("--include-retained-attempt", action="store_true")
    a = p.parse_args()
    if a.include_retained_attempt:
        retained_attempt(a.root.parent, a.output)
    while True:
        r = export(a.root, a.output, a.require_complete)
        print(
            json.dumps(
                {
                    k: r[k]
                    for k in (
                        "terminal",
                        "planned",
                        "complete_chains",
                        "valid_Q",
                        "source_batches",
                        "sealed_posttests",
                    )
                }
            ),
            flush=True,
        )
        if not a.watch or not r["provisional"]:
            return
        time.sleep(30)


if __name__ == "__main__":
    main()
