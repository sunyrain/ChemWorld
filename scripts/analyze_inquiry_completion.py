"""Retrospective path comparisons and fixed source-only C prediction references."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean

from scripts.analyze_inquiry_trajectories import committed, final_assay, public_events
from scripts.recover_work_ii_ec_pa_network import effective_row, recovery_records
from scripts.run_paper_case_notebooks import ROOT, read, write

REPORTS = ROOT / "workstreams/flagship_tasks/reports"
C_REPORT = REPORTS / "c-recovery-aligned-20261014"
C_RAW = ROOT.parent / "ChemWorld-local-research/20261014-c-recovery-aligned/attempt-01"
OUTPUT = REPORTS / "inquiry-completion-20261015"
METRICS = ("crystal_yield", "crystal_purity", "crystal_size", "crystal_fines_fraction")
METHODS = ("agent", "source_mean", "same_solvent_mean")
SOLVENT_ADDITIONS = {"add_solvent", "resuspend_crystals"}


def mean(values):
    values = [x for x in values if x is not None]
    return fmean(values) if values else None


def solvent_set(actions):
    return tuple(sorted({a["solvent"] for a in actions if a["operation"] in SOLVENT_ADDITIONS}))


def batch_records(events):
    grouped = defaultdict(list)
    for e in events:
        grouped[e["batch"]].append(e)
    records = []
    for number, attempted in sorted(grouped.items()):
        actions = [e["action"] for e in attempted if committed(e)]
        assays = [e for e in attempted if final_assay(e)]
        if len(assays) > 1:
            raise ValueError("Multiple successful final assays in a batch")
        records.append(
            {
                "batch": number,
                "actions": actions,
                "solvents": solvent_set(actions),
                "observations": assays[0]["observations"] if assays else None,
            }
        )
    return records


def preparation(actions):
    """Exclude measurements/end markers; preserve container topology with canonical IDs."""
    identifiers = {}
    result = []
    for action in actions:
        if action["operation"] in ("measure", "terminate"):
            continue
        cleaned = dict(action)
        for key, value in action.items():
            if "container" in key and isinstance(value, (int, str)):
                cleaned[key] = identifiers.setdefault(value, len(identifiers))
        result.append(cleaned)
    return json.dumps(result, sort_keys=True)


def path_record(events):
    batches = batch_records(events)
    actions = [e["action"] for e in events if committed(e)]
    solvents = [a["solvent"] for a in actions if a["operation"] in SOLVENT_ADDITIONS]
    catalysts = [a["catalyst"] for a in actions if a["operation"] == "add_catalyst"]
    electrolyte = [a["electrolyte"] for a in actions if a["operation"] == "add_electrolyte"]
    volumes, loadings, ratios = [], [], []
    signatures = []
    for b in batches:
        volume = sum(
            a.get("volume_L", 0) for a in b["actions"] if a["operation"] in SOLVENT_ADDITIONS
        )
        loading = sum(
            a.get("amount_mol", 0)
            for a in b["actions"]
            if a["operation"] == "add_reagent"
            or (a["operation"] == "add_component" and a.get("component") == 0)
        )
        volumes.append(volume)
        loadings.append(loading)
        if volume > 0:
            ratios.append(loading / volume)
        if b["observations"] is not None:
            signatures.append(preparation(b["actions"]))
    result = {
        "operations": len(events),
        "committed_operations": len(actions),
        "rejected_operations": len(events) - len(actions),
        "completed_batches": len(signatures),
        "exact_preparation_repeats": len(signatures) - len(set(signatures)),
        "first_solvent": solvents[0] if solvents else None,
        "first_catalyst": catalysts[0] if catalysts else None,
        "first_electrolyte": electrolyte[0] if electrolyte else None,
        "distinct_solvents": len(set(solvents)),
        "distinct_catalysts": len(set(catalysts)),
        "distinct_electrolytes": len(set(electrolyte)),
        "intermediate_measurements": sum(
            committed(e) and e["action"]["operation"] == "measure" and not final_assay(e)
            for e in events
        ),
    }
    for name, values in (
        ("nominal_reagent_mol", loadings),
        ("added_solvent_L", volumes),
        ("nominal_reagent_per_added_solvent_M", ratios),
    ):
        result[name + "_min"] = min(values) if values else None
        result[name + "_max"] = max(values) if values else None
    return result


def fit_references(events, queries):
    """No test truth or agent prediction is available to this function."""
    batches = [b for b in batch_records(events) if b["observations"] is not None]
    result = []
    for q in queries:
        matched = [b for b in batches if b["solvents"] == solvent_set(q["actions"])]
        chosen = matched or batches
        result.append(
            {
                "query_id": q["query_id"],
                "source_batches": len(batches),
                "same_solvent_batches": len(matched),
                "fallback": not bool(matched),
                "source_mean": {
                    m: mean([b["observations"].get(m) for b in batches]) for m in METRICS
                },
                "same_solvent_mean": {
                    m: mean([b["observations"].get(m) for b in chosen]) for m in METRICS
                },
            }
        )
    return result


def baselines():
    queries = read(C_RAW / "repeat-01/C/design.json")["queries"]
    rows = []
    for case in read(C_REPORT / "analysis.json")["cases"]:
        session = read(C_REPORT / "sessions" / case["repeat"] / f"{case['id']}.json")
        export = read(C_REPORT / case["repeat"] / f"{case['id']}.json")
        identity = {k: case[k] for k in ("repeat", "id", "world", "arm", "status", "failure")}
        fitted = fit_references(session["events"], queries)
        if not (case.get("prediction_evaluation") or {}).get("valid"):
            rows.append(
                {
                    **identity,
                    "valid_Q": False,
                    "queries": [],
                    "source_reference_predictions": fitted,
                }
            )
            continue
        truth = read(C_RAW / "references" / f"C-{case['world']}" / "result.json")["truth"]
        predictions = {p["query_id"]: p for p in export["posttests"]["Q"]["payload"]["predictions"]}
        scores = []
        for fit, target in zip(fitted, truth, strict=True):
            point = {m: predictions[fit["query_id"]][m]["estimate"] for m in METRICS}
            estimates = {"agent": point, **{method: fit[method] for method in METHODS[1:]}}
            errors = {
                method: {m: abs(estimates[method][m] - target[m]) for m in METRICS}
                for method in METHODS
            }
            scores.append(
                {**fit, "agent": point, "reference_truth": target, "absolute_errors": errors}
            )
        maes = {
            method: {m: mean([q["absolute_errors"][method][m] for q in scores]) for m in METRICS}
            for method in METHODS
        }
        for m in METRICS:
            if abs(maes["agent"][m] - case["prediction_evaluation"]["metrics"][m]["mae"]) > 1e-12:
                raise ValueError("Retained agent MAE mismatch")
        rows.append({**identity, "valid_Q": True, "queries": scores, "mae": maes})
    groups = []
    for arm in ("all", "Opaque", "Aligned", "MisIndexed"):
        group = [r for r in rows if r["valid_Q"] and (arm == "all" or r["arm"] == arm)]
        worlds = []
        for world in sorted({r["world"] for r in rows}):
            selected = [r for r in group if r["world"] == world]
            worlds.append(
                {
                    "world": world,
                    "sessions": len(selected),
                    "mae": {
                        method: {m: mean([r["mae"][method][m] for r in selected]) for m in METRICS}
                        for method in METHODS
                    },
                }
            )
        groups.append(
            {
                "arm": arm,
                "valid_sessions": len(group),
                "worlds": worlds,
                "equal_world_mae": {
                    method: {m: mean([w["mae"][method][m] for w in worlds]) for m in METRICS}
                    for method in METHODS
                },
                "fallback_queries": sum(q["fallback"] for r in group for q in r["queries"]),
                "query_count": sum(len(r["queries"]) for r in group),
                "agent_strict_wins": {
                    method: {
                        m: sum(r["mae"]["agent"][m] < r["mae"][method][m] for r in group)
                        for m in METRICS
                    }
                    for method in METHODS[1:]
                },
            }
        )
    return {
        "planned_sessions": 45,
        "valid_sessions": sum(r["valid_Q"] for r in rows),
        "fitting": "Source final assays; exact solvent-set matching, overall-mean fallback.",
        "limitations": "Descriptive; materials do not match thermal history. No intervals.",
        "groups": groups,
        "sessions": rows,
    }


def paths():
    rows = []
    for report, cohort, system, goal in (
        (C_REPORT, "corrected_recovery_45", "C", "optimization"),
        (REPORTS / "inquiry-trajectories-20261014", "retained_EQ45", "EQ", "characterization"),
    ):
        for path in sorted((report / "sessions").glob(f"repeat-*/*{system}-*.json")):
            s = read(path)
            rows.append(
                {
                    "cohort": cohort,
                    "id": s["id"],
                    "repeat": s["repeat"],
                    "system": system,
                    "world": s["world"],
                    "arm": s["arm"],
                    "goal": goal,
                    "budget": 12,
                    "status": s["status"],
                    "failure": s["failure"],
                    "features": path_record(s["events"]),
                }
            )
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_132_ec_pa_english_matrix"]
    ecroot = ROOT / binding["run_root"]
    raw = read(ecroot / "summary.json")
    for original in raw["results"]:
        if original["system"] != "EC" or original["locus"] != "E":
            continue
        row = effective_row(original)
        physical = (
            ecroot / "sources" / original["unit_id"] / f"{original['goal']}-E-{original['arm']}"
        )
        for rec in recovery_records(original):
            if rec["kind"] != "posttests":
                physical = Path(rec["result_path"]).parent
        events = public_events(physical / "trajectory.jsonl")
        if len(events) != row["operations"]:
            raise ValueError(f"EC canonical trajectory mismatch: {original['unit_id']}")
        rows.append(
            {
                "cohort": "retained_EC60",
                "id": original["unit_id"],
                "repeat": None,
                "system": "EC",
                "world": original["world"]["world_id"],
                "arm": original["arm"],
                "goal": original["goal"],
                "budget": original["budget"],
                "status": row["status"],
                "failure": row.get("failure"),
                "historical_recoveries": len(recovery_records(original)),
                "first_attempt_status": original["status"],
                "features": path_record(events),
            }
        )
    if Counter(r["system"] for r in rows) != {"C": 45, "EQ": 45, "EC": 60}:
        raise ValueError("Path cohort coverage mismatch")
    grouped = defaultdict(list)
    for r in rows:
        grouped[(r["cohort"], r["system"], r["goal"], r["budget"], r["arm"])].append(r)
    groups = []
    for key, group in sorted(grouped.items()):
        fields = list(group[0]["features"])
        groups.append(
            {
                **dict(zip(("cohort", "system", "goal", "budget", "arm"), key, strict=True)),
                "n": len(group),
                "worlds": sorted({r["world"] for r in group}),
                "first_choices": {
                    k: dict(Counter(str(r["features"][k]) for r in group))
                    for k in fields
                    if k.startswith("first_")
                },
                "means": {
                    k: mean([r["features"][k] for r in group])
                    for k in fields
                    if not k.startswith("first_")
                },
            }
        )
    comparisons = []
    fields = [k for k in rows[0]["features"] if not k.startswith("first_")]
    for system in ("EC", "C", "EQ"):
        source = [r for r in rows if r["system"] == system]
        targets = (
            [("goal", "optimization", "discovery")]
            if system == "EC"
            else [("arm", "Aligned", "Opaque"), ("arm", "MisIndexed", "Opaque")]
        )
        for axis, left, right in targets:
            fixed = ("world", "budget", "arm") if axis == "goal" else ("world", "budget", "goal")
            for key in sorted({tuple(r[k] for k in fixed) for r in source}):
                selected = [r for r in source if tuple(r[k] for k in fixed) == key]
                a = [r for r in selected if r[axis] == left]
                b = [r for r in selected if r[axis] == right]
                ma = {k: mean([r["features"][k] for r in a]) for k in fields}
                mb = {k: mean([r["features"][k] for r in b]) for k in fields}
                comparisons.append(
                    {
                        "system": system,
                        **dict(zip(fixed, key, strict=True)),
                        "contrast": f"{left} minus {right}",
                        "left_n": len(a),
                        "right_n": len(b),
                        "left_means": ma,
                        "right_means": mb,
                        "differences": {
                            k: ma[k] - mb[k] if ma[k] is not None and mb[k] is not None else None
                            for k in fields
                        },
                    }
                )
    return {
        "sessions": rows,
        "groups": groups,
        "within_world_contrasts": comparisons,
        "limitations": [
            "EC uses historical effective sources; original failures and recoveries retained.",
            "EQ information arms span two periods; corrected C is a separate cohort.",
            "Nominal loading is cumulative added reagent/solvent, not instantaneous concentration.",
            "No causal attribution to notes, goal or information from these path summaries alone.",
        ],
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    b = baselines()
    write(OUTPUT / "source_references.json", b)
    p = paths()
    write(OUTPUT / "research_paths.json", p)
    lines = [
        "# Source-only references and research paths",
        "",
        "Retrospective analysis under W2-257. Cohorts and worlds are kept separate.",
        "",
        f"Corrected crystallization: {b['valid_sessions']}/45 valid Q; missing sessions retained.",
        "All means below weight the five world means equally. Lower MAE is better.",
        "",
        "| Arm | Response | Agent | Source mean | Same-solvent mean |",
        "|---|---|---:|---:|---:|",
    ]
    for g in b["groups"]:
        for m in METRICS:
            vals = " | ".join(f"{g['equal_world_mae'][method][m]:.6f}" for method in METHODS)
            lines.append(f"| {g['arm']} | {m} | {vals} |")
    lines += [
        "",
        "Solvent matching includes committed additions/resuspension, but not thermal history.",
        "References assess retention of observed levels, not an optimal learned model.",
        "",
        "| Cohort | Goal | Budget | Arm | n | Solvents | Interim measurements | Prep repeats |",
        "|---|---|---:|---|---:|---:|---:|---:|",
    ]
    for g in p["groups"]:
        f = g["means"]
        lines.append(
            f"| {g['cohort']} | {g['goal']} | {g['budget']} | {g['arm']} | {g['n']} | "
            f"{f['distinct_solvents']:.2f} | {f['intermediate_measurements']:.2f} | "
            f"{f['exact_preparation_repeats']:.2f} |"
        )
    lines += [
        "",
        *p["limitations"],
        "",
        "Session paths, failures, first choices and ranges: research_paths.json.",
        "Query predictions, fitting denominators, fallbacks and errors: source_references.json.",
        "",
    ]
    (OUTPUT / "RETROSPECTIVE.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"valid_C_Q": b["valid_sessions"], "paths": len(p["sessions"])}), flush=True)


if __name__ == "__main__":
    main()
