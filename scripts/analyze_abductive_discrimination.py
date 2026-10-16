"""Export public evidence and descriptive results from the fixed W2-263 cohort.

This read-only analysis never calls a provider or simulator. Physical separation,
temporal availability and analyst interpretation remain distinct measurements.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from statistics import fmean

from scripts import run_abductive_discrimination as run
from scripts.analyze_inquiry_trajectories import public_events
from scripts.report_paper_case_notebooks import notebook_record
from scripts.run_paper_case_notebooks import case_folder, emit, read, write


def csv_write(path, rows):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                    for k, v in row.items()
                }
            )


def export_session(root, unit, result):
    folder = case_folder(root / unit["repeat"], unit)
    notes = notebook_record(folder)
    trajectory = folder / "trajectory.jsonl"
    events = public_events(trajectory) if trajectory.exists() else []
    versions = [
        {
            "revision": r["revision"],
            "public_cursor": r["public_cursor"]["event_count"],
            "text": r["text"],
            "recorded_at": r["recorded_at"],
            "reviewed_through": r["reviewed_through"],
        }
        for r in notes["versions"]
    ]
    counterpart = result.get("counterfactual") or {}
    gaps = {row["source_step"]: row for row in counterpart.get("matched_batches", [])}
    batches, previous_end = [], 0
    for batch in result.get("batches", []):
        start, end = previous_end + 1, batch["end_step"]
        preceding = [v for v in versions if v["public_cursor"] < start]
        during = [v for v in versions if start <= v["public_cursor"] < end]
        following = next((v for v in versions if v["public_cursor"] >= end), None)
        gap = gaps.get(end)
        batches.append(
            {
                **batch,
                "start_cursor": start,
                "preceding_note_before_first_action": preceding[-1]["revision"]
                if preceding
                else None,
                "notes_during_batch_before_assay": [v["revision"] for v in during],
                "first_note_at_or_after_assay": following["revision"] if following else None,
                "physical_counterfactual": gap,
                "intended_test_interpretation": (
                    "requires_semantic_reading_not_inferred_from_separation"
                ),
            }
        )
        previous_end = end
    context_path = folder / "private-provider/source/initial-public-context.json"
    context = read(context_path) if context_path.exists() else None
    return {
        **unit,
        "source": str(folder),
        "status": result["status"],
        "failure": result.get("failure"),
        "source_status": result.get("source_status"),
        "public_initial_context": context,
        "versions": versions,
        "notebook_validation": notes["validation"],
        "events": events,
        "batches": batches,
        "posttests": result.get("posttests", {}),
        "posttest_validation": result.get("posttest_validation", {}),
        "prediction_evaluation": result.get("prediction_evaluation"),
        "exact_replay": result.get("exact_replay"),
        "source_usage": result.get("source_usage"),
        "elapsed_s": result.get("elapsed_s"),
        "counterfactual": {
            k: counterpart.get(k)
            for k in (
                "status",
                "source_actions",
                "participant_feedback",
                "own_source_observations_identical",
                "own_operation_outcomes_identical",
                "matched_batches",
            )
        },
        "counterfactual_execution": {
            label: {
                k: world.get(k)
                for k in (
                    "operation_attempts",
                    "rollbacks",
                    "failure",
                    "expected_incomplete_prefix_end",
                    "exact_replay",
                    "all_source_actions_replayed",
                )
            }
            for label, world in counterpart.get("worlds", {}).items()
        },
        "semantic_review_file": f"semantic_{unit['repeat'].replace('-', '')}.json",
        "automatic_semantic_classification": False,
    }


def session_markdown(session):
    lines = [
        f"# {session['repeat']}/{session['id']}",
        "",
        f"Status: {session['status']}; source assays {len(session['batches'])}/12; "
        f"public note versions {len(session['versions'])}.",
        "",
        "Physical differences below describe the selected actions under matched worlds. "
        "They do not establish that an agent proposed or tested an explanation. "
        "All notebook versions, including terminal revisions, follow verbatim.",
        "",
        "| Assay | End event | Prior note | First later note | "
        "Mean gap / assay SD: pH, free acid, precipitate |",
        "| --- | --- | --- | --- | --- |",
    ]
    for batch in session["batches"]:
        gap = (batch.get("physical_counterfactual") or {}).get("gap_in_assay_standard_deviations")
        values = ", ".join(f"{gap[m]:.3f}" for m in run.eq.METRICS) if gap else "unavailable"
        lines.append(
            f"| {batch['ordinal']} | {batch['end_step']} | "
            f"{batch['preceding_note_before_first_action']} | "
            f"{batch['first_note_at_or_after_assay']} | {values} |"
        )
    for note in session["versions"]:
        lines.extend(
            [
                "",
                f"## Revision {note['revision']}",
                "",
                f"Available operation events: {note['public_cursor']}.",
                "",
                note["text"],
            ]
        )
    for stage in run.STAGES:
        turn = session["posttests"].get(stage, {})
        lines.extend(["", f"## Sealed {stage}", ""])
        if turn.get("payload"):
            payload = turn["payload"]
            lines.append(payload.get("report", json.dumps(payload, ensure_ascii=False, indent=2)))
        else:
            lines.append(f"Unavailable. Failure: {turn.get('failure')}")
    return "\n".join(lines) + "\n"


def prediction_rows(session, truth):
    if not (session.get("prediction_evaluation") or {}).get("valid"):
        return []
    rows = []
    payload = session["posttests"]["Q"]["payload"]
    for query in payload["predictions"]:
        for metric, interval in query["metrics"].items():
            observed = [r[metric] for r in truth[query["query_id"]]]
            mean = fmean(observed)
            rows.append(
                {
                    "repeat": session["repeat"],
                    "id": session["id"],
                    "pair": session["pair"],
                    "mechanism": session["mechanism"],
                    "query": query["query_id"],
                    "metric": metric,
                    **interval,
                    "reference_mean": mean,
                    "reference_repeats": len(observed),
                    "signed_error": interval["estimate"] - mean,
                    "absolute_error": abs(interval["estimate"] - mean),
                    "empirical_coverage80": fmean(
                        interval["lower80"] <= y <= interval["upper80"] for y in observed
                    ),
                    "rationale": query.get("rationale"),
                }
            )
    return rows


def analyze(root, report):
    design = read(root / "design.json")
    stopped = read(root / "block-stop.json") if (root / "block-stop.json").exists() else {}
    truth_path = root / "references/truth.json"
    truth = read(truth_path)["EQ"] if truth_path.exists() else {}
    sessions, session_rows, predictions, gaps = [], [], [], []
    for unit in design["schedule"]:
        result_path = run.pool.result_path(root, unit)
        process_failed = stopped.get("unit") == [unit["repeat"], unit["id"]]
        if result_path.exists() or process_failed:
            result = (
                read(result_path)
                if result_path.exists()
                else {
                    "status": "worker_startup_failure",
                    "source_status": "not_started",
                    "failure": stopped.get("reason"),
                    "batches": [],
                    "counterfactual": {"status": "no_source_actions"},
                }
            )
            session = export_session(root, unit, result)
            session["result_origin"] = (
                "retained_result" if result_path.exists() else "retained_worker_exit_marker"
            )
            sessions.append(session)
            write(report / "sessions" / unit["repeat"] / f"{unit['id']}.json", session)
            note_path = report / "notes" / unit["repeat"] / f"{unit['id']}.md"
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(session_markdown(session), encoding="utf-8")
            predictions.extend(prediction_rows(session, truth.get(unit["world"], {})))
            for batch in session["batches"]:
                gap = batch.get("physical_counterfactual")
                if gap:
                    gaps.append(
                        {
                            "repeat": unit["repeat"],
                            "id": unit["id"],
                            "pair": unit["pair"],
                            "mechanism": unit["mechanism"],
                            "batch": batch["ordinal"],
                            "end_cursor": batch["end_step"],
                            "prior_note": batch["preceding_note_before_first_action"],
                            "first_later_note": batch["first_note_at_or_after_assay"],
                            **{
                                f"{m}_gap_sd": v
                                for m, v in gap["gap_in_assay_standard_deviations"].items()
                            },
                            "channels_at_least_3sd": sum(
                                v >= 3 for v in gap["gap_in_assay_standard_deviations"].values()
                            ),
                            "semantic_test_intent": "not_automatically_assigned",
                        }
                    )
        else:
            result = {}
            session = {}
        metrics = (result.get("prediction_evaluation") or {}).get("metrics", {})
        session_rows.append(
            {
                **{k: unit[k] for k in ("repeat", "id", "pair", "mechanism")},
                "status": result.get(
                    "status",
                    "running"
                    if case_folder(root / unit["repeat"], unit).exists()
                    else "not_started",
                ),
                "completed_batches": len(result.get("batches", [])),
                "notebook_versions": len(session.get("versions", [])),
                "source_replay_verified": (result.get("exact_replay") or {}).get("verified"),
                "valid_Q": (result.get("prediction_evaluation") or {}).get("valid", False),
                "macro_mae": fmean(m["mae_to_five_repeat_mean"] for m in metrics.values())
                if metrics
                else None,
                "counterfactual_status": (result.get("counterfactual") or {}).get("status"),
                "failure": result.get("failure"),
            }
        )
    pair_rows = []
    for pair in sorted({r["pair"] for r in session_rows}):
        for mechanism in ("A", "B"):
            group = [r for r in session_rows if r["pair"] == pair and r["mechanism"] == mechanism]
            valid = [r for r in group if r["valid_Q"]]
            pair_rows.append(
                {
                    "pair": pair,
                    "mechanism": mechanism,
                    "planned_sessions": 3,
                    "terminal_sessions": sum(
                        r["status"] not in {"running", "not_started"} for r in group
                    ),
                    "valid_predictions": len(valid),
                    "macro_mae": fmean(r["macro_mae"] for r in valid) if valid else None,
                }
            )
    counterfactuals = [s["counterfactual"] for s in sessions]
    summary = {
        "source_commit": design["source_commit"],
        "planned_sessions": 30,
        "terminal_sessions": len(sessions),
        "session_statuses": dict(Counter(r["status"] for r in session_rows)),
        "planned_source_assays": 360,
        "completed_source_assays": sum(len(s["batches"]) for s in sessions),
        "public_note_versions": sum(len(s["versions"]) for s in sessions),
        "valid_predictions": sum(r["valid_Q"] for r in session_rows),
        "planned_prediction_entries": 1080,
        "observed_prediction_entries": len(predictions),
        "source_replays_verified": sum(bool(r["source_replay_verified"]) for r in session_rows),
        "counterfactual_statuses": dict(Counter(c["status"] for c in counterfactuals)),
        "counterfactual_batch_pairs": len(gaps),
        "notebook_cursor_issues": [
            {"repeat": s["repeat"], "id": s["id"], **v}
            for s in sessions
            for v in s["notebook_validation"]
            if not v["cursor_valid"]
            or not v["reviewed_reference_valid"]
            or v["unavailable_event_citations"]
        ],
        "interpretation": "Descriptive physical and temporal evidence; no automatic abduction rate",
        "semantic_review_summary": "reading-summary.json",
        "automatic_semantic_classification": False,
        "resource_summary": "resource-summary.json",
    }
    write(report / "analysis-summary.json", summary)
    csv_write(report / "session-summary.csv", session_rows)
    csv_write(report / "pair-summary.csv", pair_rows)
    csv_write(report / "predictions.csv", predictions)
    csv_write(report / "selected-experiment-separation.csv", gaps)
    lines = [
        "# Prospective matched-world evidence",
        "",
        "This export separates physical separation from intended hypothesis testing. "
        "Read complete notes and sealed accounts before assigning semantic interpretations.",
        "",
        f"Terminal sessions: {len(sessions)}/30; source assays "
        f"{summary['completed_source_assays']}/360; "
        f"note versions {summary['public_note_versions']}; "
        f"valid Q {summary['valid_predictions']}/30; source replay "
        f"{summary['source_replays_verified']}/30.",
        "",
        "Counterfactual status: " + json.dumps(summary["counterfactual_statuses"]) + ".",
        "",
        "Resource accounting is reported separately in `resource-summary.json`: resumed-thread "
        "token counters are cumulative, and technical failures and canaries remain separate "
        "from the scientific participant cohort. Unknown costs or usage are not zero.",
        "",
        "Each session JSON retains public actions, measured evidence, all note versions, "
        "K1/Q/K2, failures and resource use. Each Markdown file presents the complete "
        "notes with physical separation and temporal anchors. Supplied preliminary assays "
        "are distinct from the 12 agent-selected batches. Source selected actions are "
        "replayed under both worlds without giving these evaluator outcomes to the agent.",
        "",
        "| Session | Status | Assays | Notes | Q valid |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in session_rows:
        key = f"{row['repeat']}/{row['id']}"
        link = (
            f"[ {key} ](notes/{key}.md)" if row["status"] not in {"running", "not_started"} else key
        )
        lines.append(
            f"| {link} | {row['status']} | {row['completed_batches']} | "
            f"{row['notebook_versions']} | {row['valid_Q']} |"
        )
    (report / "EVIDENCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    emit(summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    analyze(args.root.resolve(), args.report.resolve())


if __name__ == "__main__":
    main()
