"""Read-only scientific export of the fixed notebook block, without provider payloads."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from statistics import fmean

from scripts.run_paper_case_notebooks import CASES, ROOT, case_folder, read, write


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def notebook_record(folder):
    histories = list(folder.glob("**/notebook/experiment_documents/notebook_history"))
    if len(histories) > 1:
        raise ValueError("ambiguous notebook store")
    if not histories:
        return {"versions": [], "calls": [], "validation": []}
    directory = histories[0]
    versions = [read(path) for path in sorted(directory.glob("[0-9]*.json"))]
    ledger = jsonl(directory.parent / "environment_authoritative_ledger.jsonl")
    ids = [row["event_id"] for row in ledger]
    checks = []
    last_count = 0
    for version in versions:
        cursor = version["public_cursor"]
        count = cursor["event_count"]
        checks.append(
            {
                "revision": version["revision"],
                "cursor_valid": last_count <= count <= len(ids)
                and cursor["last_event_id"] == (ids[count - 1] if count else None),
                "reviewed_reference_valid": version["reviewed_through"] is None
                or version["reviewed_through"] in ids[:count],
                "unavailable_event_citations": sorted(
                    set(re.findall(r"runner-operation-\d+", version["text"])) - set(ids[:count])
                ),
            }
        )
        last_count = count
    return {
        "versions": versions,
        "calls": jsonl(directory.parent.parent / "notebook-calls.jsonl"),
        "validation": checks,
    }


def posttest_record(folder, stage, turn):
    record = {
        k: turn.get(k) for k in ("payload", "failure", "elapsed_s", "usage", "method_resources")
    }
    # EQ's historical public exporter omits usage; recover only the numeric usage
    # object, not the provider payload or conversation, from the sealed receipt.
    receipt = folder / "private-provider" / stage / "receipt.json"
    if record["usage"] is None and receipt.is_file():
        record["usage"] = read(receipt).get("usage")
    return record


def reference_differences(root):
    current = read(ROOT / "configs/current.json")["work_ii"]["w2_132_ec_pa_english_matrix"]
    old_ec = read(ROOT / current["run_root"] / "references/EC-W01/reference-result.json")["truth"]
    new_truth = read(root / "references/truth.json")
    old_c = read(
        ROOT
        / "runs/formal/work-ii-c-five-world-20260920-v3-auto/qualification/W05/queries/result.json"
    )["truth"]
    new_c = read(root / "C/qualification/W05/queries/result.json")["truth"]
    old_eq = read(
        ROOT / "runs/development/eq-three-model-matrix-20260927/shared-reference/truth.json"
    )
    pairs = {
        "EC": [(old_ec[q], new_truth["EC"][q]) for q in old_ec],
        "C": list(zip(old_c, new_c, strict=True)),
    }
    for world in ("EQ-W01", "EQ-W03"):
        pairs[world] = [
            (a, b)
            for q in new_truth["EQ"][world]
            for a, b in zip(old_eq[world][q], new_truth["EQ"][world][q], strict=True)
        ]
    return {
        system: {
            "compared_rows": len(rows),
            "max_absolute_difference_by_metric": {
                metric: max(abs(a[metric] - b[metric]) for a, b in rows)
                for metric in rows[0][0]
                if type(rows[0][0][metric]) in (int, float)
            },
            "all_values_equal": all(a == b for a, b in rows),
        }
        for system, rows in pairs.items()
    }


def token_accounting(source_usage, posttests, *, equilibrium=False):
    expected = ["source", "K1", "Q", "K2", *(["EQS"] if equilibrium else [])]
    source_usage = source_usage or {}
    snapshots = {}
    if source_usage.get("provider_token_accounting_complete"):
        snapshots["source"] = {
            "input_tokens": source_usage["input_token_count"],
            "cached_input_tokens": source_usage["cached_input_token_count"],
            "output_tokens": source_usage["output_token_count"],
        }
    fields = ("input_tokens", "cached_input_tokens", "output_tokens")
    for stage in expected[1:]:
        usage = posttests.get(stage, {}).get("usage") or {}
        if all(type(usage.get(field)) is int for field in fields):
            snapshots[stage] = {field: usage[field] for field in fields}
    previous = dict.fromkeys(fields, 0)
    deltas = []
    for stage in expected:
        if stage not in snapshots:
            continue
        current = snapshots[stage]
        delta = {field: current[field] - previous[field] for field in fields}
        if min(delta.values()) < 0 or delta["cached_input_tokens"] > delta["input_tokens"]:
            return {
                "valid": False,
                "complete": False,
                "reason": "nonmonotone usage",
                "stage": stage,
            }
        deltas.append({"stage": stage, **delta})
        previous = current
    return {
        "valid": bool(snapshots),
        "complete": list(snapshots) == expected,
        "basis": "cumulative same-thread snapshots, differenced in original stage order",
        "missing_stages": [stage for stage in expected if stage not in snapshots],
        "stage_deltas": deltas,
        "total": {
            **previous,
            "input_plus_output": previous["input_tokens"] + previous["output_tokens"],
        }
        if snapshots
        else None,
        "monetary_cost_usd": None,
    }


def reference_accounting(root):
    paths = [
        *sorted((root / "references/EC").glob("Q*/result.json")),
        root / "C/qualification/W05/queries/result.json",
        *sorted((root / "references").glob("EQ-W*/repeat-*/result.json")),
    ]
    rows = []
    for path in paths:
        if not path.exists():
            continue
        data = read(path)
        rows.append(
            {
                "path": str(path.relative_to(root)),
                "batches": len(data.get("batches", [])),
                "operations": data.get("operation_attempts", data.get("operations", 0)),
                "failure": data.get("failure"),
                "exact_replay": data.get("exact_replay"),
            }
        )
    return {
        "planned_batches": 144,
        "completed_batches": sum(r["batches"] for r in rows),
        "operations": sum(r["operations"] for r in rows),
        "runs": rows,
    }


def equilibrium_diagnostics(root, folder, case, result):
    if case["system"] != "EQ":
        return None
    concentrations = []
    trajectory = folder / "trajectory.jsonl"
    grouped = {}
    for record in jsonl(trajectory) if trajectory.exists() else []:
        if record.get("transaction_status") == "committed":
            grouped.setdefault(record["experiment_index"], []).append(record)
    for index, records in grouped.items():
        if not any(r.get("instrument") == "final_assay" for r in records):
            continue
        amount = sum(
            r["action"].get("amount_mol", 0)
            for r in records
            if r["action"]["operation"] == "add_reagent"
        )
        volume = sum(
            r["action"].get("volume_L", 0)
            for r in records
            if r["action"]["operation"] == "add_solvent"
        )
        component_feeds = [
            r["action"] for r in records if r["action"]["operation"] == "add_component"
        ]
        concentrations.append(
            {
                "batch": index + 1,
                "nominal_concentration_M": amount / volume
                if volume and not component_feeds
                else None,
                "component_feeds": component_feeds,
                "basis": "nominal add_reagent loading / charged solvent volume; "
                "component-only or mixed-feed substitutions are not treated as zero loading",
            }
        )
    output = {
        "batch_concentrations": concentrations,
        "prediction_groups": None,
        "grouping_basis": (
            "Descriptive Q03/Q08/Q09 partition retained from the paper; "
            "not a new confirmatory analysis"
        ),
    }
    if (result.get("prediction_evaluation") or {}).get("valid") is not True:
        return output
    truth = read(root / "references/truth.json")["EQ"][case["cell"].split("--")[0]]
    predictions = {r["query_id"]: r for r in result["posttests"]["Q"]["payload"]["predictions"]}
    dilute = ("Q03", "Q08", "Q09")
    groups = {}
    for name, queries in (
        ("lowest_three", dilute),
        ("remaining_nine", tuple(q for q in truth if q not in dilute)),
        ("all_twelve", tuple(truth)),
    ):
        errors, covered = [], []
        for query in queries:
            for metric, interval in predictions[query]["metrics"].items():
                values = [r[metric] for r in truth[query]]
                errors.append(abs(interval["estimate"] - fmean(values)))
                covered.extend(interval["lower80"] <= y <= interval["upper80"] for y in values)
        groups[name] = {
            "queries": queries,
            "metric_predictions": len(errors),
            "coverage_denominator": len(covered),
            "covered": sum(covered),
            "macro_mae": fmean(errors),
            "coverage80": fmean(covered),
        }
    output["prediction_groups"] = groups
    return output


def crystallization_quality(case, result):
    if case["system"] != "C":
        return None
    source = result.get("source", {})
    truth = source.get("truth", [])

    def feasible(row):
        return bool(
            row["particles_present"]
            and row["crystal_purity"] >= 0.8
            and row["crystal_fines_fraction"] <= 0.5
        )

    retest = (result.get("recommendation_retest") or {}).get("truth", [])
    return {
        "basis": "Host-only noise-free source/retest values, reviewed after execution; "
        "not provided to the participant or substituted for its public measurements",
        "planned_source_batches": case["batches"],
        "observed_source_batches": len(truth),
        "feasible_source_batches": sum(feasible(row) for row in truth),
        "infeasible_source_ordinals": [i for i, row in enumerate(truth, 1) if not feasible(row)],
        "source_truth": truth,
        "recommended_retest_feasible": feasible(retest[0]) if len(retest) == 1 else None,
    }


def readable_posttests(case, posttests):
    lines = [
        f"# {case['id']} — sealed model reports",
        "",
        "Model-authored answers in their original sequence. These were written after "
        "the source campaign, separately from its contemporary notebook. "
        "No reference answers were supplied during these stages.",
        "",
    ]
    for stage in ("K1", "Q", "K2", "EQS"):
        if stage not in posttests:
            continue
        turn = posttests[stage]
        lines += [f"## {stage}", ""]
        if turn.get("failure"):
            lines += [f"Retained failure: {turn['failure']}", ""]
        payload = turn.get("payload") or {}
        if "report" in payload:
            lines += [payload["report"], ""]
        elif "predictions" in payload:
            lines += [
                "| Query | Metric | Estimate | Lower 80% | Upper 80% |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
            for query in payload["predictions"]:
                for metric, interval in query.get("metrics", query).items():
                    if not isinstance(interval, dict) or "estimate" not in interval:
                        continue
                    values = [
                        "—" if interval[k] is None else f"{interval[k]:.6g}"
                        for k in ("estimate", "lower80", "upper80")
                    ]
                    lines.append(f"| {query['query_id']} | {metric} | " + " | ".join(values) + " |")
            lines += [
                "",
                "Displayed values use six significant digits; the JSON record retains "
                "the original numeric values and particle/quality decisions.",
                "",
            ]
            if payload.get("rationale"):
                lines += [payload["rationale"], ""]
            for query in payload["predictions"]:
                if query.get("rationale"):
                    lines += [f"**{query['query_id']}**: {query['rationale']}", ""]
        else:
            for topic, fields in payload.items():
                lines += [f"### {topic.replace('_', ' ')}", ""]
                if isinstance(fields, dict):
                    for key, value in fields.items():
                        lines += [
                            f"**{key.replace('_', ' ')}**: "
                            + ("not estimated" if value is None else str(value)),
                            "",
                        ]
    return "\n".join(lines)


def export(root, destination, *, review_link="REVIEW.md"):
    destination.mkdir(parents=True, exist_ok=True)
    rows = []
    for case in CASES:
        result_path = root / "results" / f"{case['id']}.json"
        result = read(result_path) if result_path.exists() else {}
        source = result.get("source", result)
        folder = case_folder(root, case)
        notes = notebook_record(folder)
        calls = notes["calls"]
        versions = notes["versions"]
        retest = result.get("recommendation_retest") or {}
        batches = source.get("batches", [])
        row = {
            **case,
            "status": result.get("status", "not_started"),
            "failure": result.get("failure"),
            "completed_batches": len(batches),
            "operations": source.get("operations", 0),
            "exact_replay": source.get("exact_replay"),
            "rollbacks": source.get("rollbacks", []),
            "batch_outcomes": [
                {k: b.get(k) for k in ("lifecycle_index", "metrics", "actions")} for b in batches
            ],
            "posttests": {
                stage: posttest_record(folder, stage, turn)
                for stage, turn in result.get("posttests", {}).items()
            },
            "posttest_validation": result.get("posttest_validation"),
            "prediction_evaluation": result.get("prediction_evaluation"),
            "source_usage": result.get("source_usage", source.get("usage")),
            "elapsed_s": result.get("elapsed_s"),
            "recommendation": result.get("recommendation", result.get("evidentiary_anchor")),
            "retest": {k: retest.get(k) for k in ("passed", "failure", "exact_replay", "truth")},
            "retest_operations": retest.get("operation_attempts", retest.get("operations", 0)),
            "retest_batch_metrics": [b.get("metrics") for b in retest.get("batches", [])],
            "notebook": {
                "version_count": len(versions),
                "read_calls": sum(r["tool"] == "notebook_read" and not r["error"] for r in calls),
                "tool_failures": sum(r["error"] for r in calls),
                "initial_note_before_action": bool(versions)
                and versions[0]["public_cursor"]["event_count"] == 0,
                "validation": notes["validation"],
                "versions": [
                    {k: v for k, v in version.items() if k != "text"} for version in versions
                ],
            },
        }
        row["token_accounting"] = token_accounting(
            row["source_usage"], row["posttests"], equilibrium=case["system"] == "EQ"
        )
        row["equilibrium_diagnostics"] = equilibrium_diagnostics(root, folder, case, result)
        row["crystallization_quality"] = crystallization_quality(case, result)
        rows.append(row)
        if result or versions:
            write(destination / f"{case['id']}.json", row)
            (destination / f"{case['id']}-reports.md").write_text(
                readable_posttests(case, row["posttests"]), encoding="utf-8"
            )
            lines = [
                f"# {case['id']} — model-authored source notebook",
                "",
                "Development replication. Each version is the model's scientific account, "
                "not verified environment truth. Posttest answers are separate in the JSON record.",
                "",
            ]
            for version in versions:
                lines += [
                    f"## Revision {version['revision']}",
                    "",
                    f"Recorded: {version['recorded_at']}; public operations available: "
                    f"{version['public_cursor']['event_count']}; reviewed through: "
                    f"{version['reviewed_through'] or 'not specified'}.",
                    "",
                    version["text"],
                    "",
                    "---",
                    "",
                ]
            if not versions:
                lines += ["No notebook revision was recorded.", ""]
            (destination / f"{case['id']}-notebook.md").write_text(
                "\n".join(lines), encoding="utf-8"
            )
    summary = {
        "scope": "development replication; six selected cases, no notebook-free controls",
        "source_commit": read(root / "design.json")["source_commit"],
        "planned_sources": 6,
        "planned_batches": 84,
        "planned_posttests": 20,
        "planned_reference_batches": 144,
        "reference": read(root / "references/complete.json")
        if (root / "references/complete.json").exists()
        else None,
        "reference_accounting": reference_accounting(root),
        "terminal_sources": sum(r["status"] not in {"not_started", "running"} for r in rows),
        "completed_sources": sum(r["status"] == "completed" for r in rows),
        "completed_batches": sum(r["completed_batches"] for r in rows),
        "completed_posttests": sum(
            bool(t.get("payload")) and not t.get("failure")
            for r in rows
            for t in r["posttests"].values()
        ),
        "source_operations": sum(r["operations"] for r in rows),
        "source_rollbacks": sum(len(r["rollbacks"]) for r in rows),
        "laboratory_tool_failures": sum(
            (r["source_usage"] or {}).get("recovered_mcp_tool_failure_count", 0) for r in rows
        ),
        "notebook_tool_failures": sum(r["notebook"]["tool_failures"] for r in rows),
        "source_provider_process_attempts": sum(
            (r["source_usage"] or {}).get("provider_process_attempt_count", 0) for r in rows
        ),
        "recommendation_retest_batches": sum(len(r["retest_batch_metrics"]) for r in rows),
        "recommendation_retest_operations": sum(r["retest_operations"] for r in rows),
        "recommendation_retests_replayed": sum(
            bool((r["retest"].get("exact_replay") or {}).get("verified")) for r in rows
        ),
        "source_replays_verified": sum(
            bool((r["exact_replay"] or {}).get("verified")) for r in rows
        ),
        "notebook_versions": sum(r["notebook"]["version_count"] for r in rows),
        "notebook_read_calls": sum(r["notebook"]["read_calls"] for r in rows),
        "token_accounting_complete_cases": sum(r["token_accounting"]["complete"] for r in rows),
        "observed_input_plus_output_tokens": sum(
            (r["token_accounting"].get("total") or {}).get("input_plus_output", 0) for r in rows
        ),
        "cases": [
            {k: v for k, v in r.items() if k not in {"batch_outcomes", "posttests"}} for r in rows
        ],
        "block_stop": read(root / "block-stop.json")
        if (root / "block-stop.json").exists()
        else None,
        "historical_reference_comparison": reference_differences(root)
        if (root / "references/complete.json").exists()
        else None,
    }
    write(destination / "summary.json", summary)
    lines = [
        "# Selected case notebook replication — machine summary",
        "",
        "Development evidence; original evidence is preserved. Notebook availability is an "
        "intervention, and there is no fresh matched control. New statements cannot establish "
        "the old agents' unrecorded reasons.",
        "",
        f"Terminal sources: {summary['terminal_sources']}/6; "
        f"full chains: {summary['completed_sources']}/6; "
        f"batches: {summary['completed_batches']}/84; "
        f"posttests: {summary['completed_posttests']}/20.",
        "",
        "| Case | Status | Batches | Operations | Versions | Reads |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['status']} | {row['completed_batches']}/{row['batches']} | "
            f"{row['operations']} | {row['notebook']['version_count']} | "
            f"{row['notebook']['read_calls']} |"
        )
    lines += [
        "",
        f"Source trajectory replays: {summary['source_replays_verified']}/6; "
        f"source operations: {summary['source_operations']}; "
        f"source rollbacks: {summary['source_rollbacks']}.",
        "",
        f"Reference batches: {summary['reference_accounting']['completed_batches']}/144; "
        f"reference operations: {summary['reference_accounting']['operations']}; "
        f"recommendation retest batches: {summary['recommendation_retest_batches']}; "
        f"retest operations: {summary['recommendation_retest_operations']}; "
        f"retests replayed: {summary['recommendation_retests_replayed']}.",
        "",
        f"Retained tool errors: {summary['notebook_tool_failures']} notebook, "
        f"{summary['laboratory_tool_failures']} laboratory. "
        f"Source provider-process attempts: {summary['source_provider_process_attempts']}.",
        "",
        f"Complete token accounts: {summary['token_accounting_complete_cases']}/6; "
        f"observed input + output tokens: {summary['observed_input_plus_output_tokens']:,} "
        "including sealed posttests. Same-thread cumulative snapshots are differenced; "
        "cached input is already included in input. Monetary cost is unknown.",
        "",
        "Failures are retained in the JSON summary and per-case records. Model notebook text "
        "is exported by revision, with public evidence cursors. Cursor/citation checks verify "
        "timing and existence only; they do not certify scientific correctness.",
        "",
        f"See [the scientific review]({review_link}) for interpretation, limitations and links "
        "to all six model notebooks and sealed reports; [summary.json](summary.json) "
        "contains the machine-readable counts and metrics.",
        "",
    ]
    (destination / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = export(args.root.resolve(), args.output.resolve())
    print(
        json.dumps(
            {k: v for k, v in result.items() if not isinstance(v, (dict, list))}, ensure_ascii=True
        )
    )
