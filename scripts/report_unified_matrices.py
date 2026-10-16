"""Recompute sanitized descriptive reports for the fixed 300-session addition.

This reads retained results only. It neither invokes a provider/simulator nor
changes execution status, retries participants, or pools the 150 earlier sessions.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import fmean

TERMINAL = {"completed", "incomplete", "failed", "execution_error"}
STAGES = ("K1", "Q", "K2")
METRICS = {
    "EC": (
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "transport_efficiency",
        "energy_efficiency",
        "score",
    ),
    "RX": ("yield", "conversion", "selectivity", "byproduct_signal", "safety_risk", "score"),
    "PA": ("product_in_organic", "product_in_aqueous"),
    "P": ("purity", "recovery"),
    "C": ("crystal_yield", "crystal_purity", "crystal_size", "crystal_fines_fraction"),
}
REFERENCE = {
    "EC": "single seeded final observation",
    "RX": "MAE to five-observation mean; coverage over 60 reference observations",
    "PA": "noiseless presampling phase fractions",
    "P": "single seeded final observation",
    "C": "noiseless preassay responses; initial-charge crystal recovery",
}
CONDITION = ("matrix", "system", "arm", "goal", "opportunity")
IDENTITY = (*CONDITION, "world", "repeat", "id")
VALUES = ("mae", "coverage", "interval_width", "interval_score")
SESSION_FIELDS = (
    *IDENTITY,
    "status",
    "source_complete",
    "completed_source_batches",
    "sealed_posttests",
    "native_evaluation_valid",
    "forecast_usable",
    "response",
    "interval_level",
    "planned_queries",
    "valid_queries",
    "coverage_reference_count",
    *VALUES,
    "metric_available",
    "metric_issue",
    "reference_semantics",
    "result_path",
    "status_path",
)
FAILURE_FIELDS = (
    *IDENTITY,
    "status",
    "category",
    "stage",
    "detail",
    "result_path",
    "status_path",
)


def read_optional(path):
    """Do not expose exception text or provider payloads in public reports."""
    if not path.exists():
        return {}, None
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}, "unreadable_json"
    if not isinstance(value, dict):
        return {}, "non_object_json"
    return value, None


def validate_design(design):
    units = design.get("schedule", [])
    if len(units) != 300 or len({(u["repeat"], u["id"]) for u in units}) != 300:
        raise ValueError("Expected the fixed 300 distinct session design")
    if Counter(u["system"] for u in units) != {"EC": 90, "RX": 90, "PA": 45, "P": 45, "C": 30}:
        raise ValueError("System denominators differ from the authorized design")
    if sum(u["batches"] for u in units) != 3420:
        raise ValueError("Expected 3,420 planned source batches")
    for key, expected in (("planned_sessions", 300), ("planned_posttests", 900)):
        if design.get(key, expected) != expected:
            raise ValueError(f"Unexpected design denominator: {key}")
    return units


def number(value):
    return value if type(value) in (float, int) and math.isfinite(value) else None


def count(value):
    if isinstance(value, list):
        return len(value)
    return value if type(value) is int and value >= 0 else 0


def dimensions(unit):
    return {
        "matrix": unit.get("matrix", "A" if unit["system"] in {"EC", "RX"} else "B"),
        "system": unit["system"],
        "arm": unit["arm"],
        "goal": unit.get("goal", "optimization" if unit["system"] == "C" else "unspecified"),
        "opportunity": unit.get("opportunity", "Research"),
        "world": unit["world"],
        "repeat": unit["repeat"],
        "id": unit["id"],
    }


def failure_tags(value):
    """Whitelist structural labels; never export a free-text provider error."""
    if not value:
        return []
    if not isinstance(value, dict):
        return [("recorded_failure", "", "See retained result; free text omitted")]
    tags = []
    stage = value.get("stage")
    stage = (
        stage
        if isinstance(stage, str)
        and stage in {*STAGES, "source", "handoff", "recommendation_retest"}
        else ""
    )
    kind = value.get("type", "recorded_failure")
    if (
        not isinstance(kind, str)
        or len(kind) > 80
        or not all(c.isalnum() or c == "_" for c in kind)
    ):
        kind = "recorded_failure"
    allowed = {
        "source_batches",
        "source_replay",
        "sealed_stages",
        "prediction",
        "recommendation_retest",
        "no_failure",
        "posttest_validation",
    }
    checks = [s for s in value.get("failed_checks", []) if isinstance(s, str) and s in allowed]
    tags.append((kind, stage, ";".join(checks) or "See retained result; free text omitted"))
    return tags


def native_metric(system, value):
    """Translate field names without conflating interval or reference semantics."""
    level = 0.9 if system == "PA" else 0.8
    fields = {
        "mae": "mae_to_five_repeat_mean" if system == "RX" else "mae",
        "coverage": "empirical_coverage80" if system == "RX" else f"coverage{round(100 * level)}",
        "interval_width": {
            "P": "width80",
            "C": "interval_width",
            "PA": "mean_width90",
        }.get(system, "mean_width80"),
        "interval_score": {
            "RX": "mean_interval_score_alpha_0_2",
            "PA": "interval_score90",
        }.get(system, "interval_score80"),
    }
    out = {name: number(value.get(key)) for name, key in fields.items()}
    n = value.get("query_count" if system == "RX" else "n")
    available = (
        type(n) is int
        and n == 12
        and out["mae"] is not None
        and out["mae"] >= 0
        and out["coverage"] is not None
        and 0 <= out["coverage"] <= 1
        and out["interval_width"] is not None
        and out["interval_width"] >= 0
    )
    if out["interval_score"] is not None and out["interval_score"] < 0:
        available = False
    references = value.get("reference_observation_count", n)
    available = available and references == (60 if system == "RX" else 12)
    return {
        **out,
        "interval_level": level,
        "planned_queries": 12,
        "valid_queries": n if type(n) is int and n >= 0 else 0,
        "coverage_reference_count": references if type(references) is int else None,
        "metric_available": available,
    }


def collect(root, units, live_summary):
    sessions, metric_rows, failures = [], [], []
    design, _ = read_optional(root / "design.json")
    retained = design.get("retained_units", {})
    projected = {
        (r.get("repeat"), r.get("id")): r
        for r in live_summary.get("cases", [])
        if isinstance(r, dict)
    }
    for unit in units:
        key = f"{unit['repeat']}/{unit['id']}"
        base = Path(retained[key]) if key in retained else root / unit["repeat"] / unit["id"]
        result_path, status_path = base / "result.json", base / "status.json"
        result, result_issue = read_optional(result_path)
        state, state_issue = read_optional(status_path)
        previous = projected.get((unit["repeat"], unit["id"]), {})
        status = state.get("status", result.get("status", "not_started"))
        if status not in TERMINAL | {"running", "queued", "not_started"}:
            status = "unknown"
        tags = []
        for issue, location in ((result_issue, "result"), (state_issue, "status")):
            if issue:
                tags.append((issue, location, "Artifact requires inspection"))
        if status in TERMINAL and not result:
            tags.append(("missing_terminal_result", "", "Terminal status has no readable result"))
        if status in TERMINAL - {"completed"}:
            tags.append(("terminal_incomplete_or_failed", "", status))
        if not state and not result and base.exists():
            status = "unknown"
            tags.append(("started_without_status", "", "Retained directory requires inspection"))
        embedded = result.get("unit", result)
        mismatch = any(
            key in embedded and embedded[key] != unit[key]
            for key in ("id", "repeat", "system", "world", "arm")
            if key in unit
        )
        if mismatch:
            tags.append(("result_identity_mismatch", "", "Excluded numeric result"))
        source = result.get("source") or {}
        stages = result.get("posttests") or {}
        validation = result.get("posttest_validation") or {}
        sealed = [
            s
            for s in STAGES
            if isinstance(stages.get(s), dict)
            and stages[s].get("payload")
            and not stages[s].get("failure")
            and validation.get(s, {}).get("valid", True)
        ]
        acquired = count(source.get("batches"))
        # The live summary counts preserved trajectories after an adapter exception.
        acquired = max(acquired, count(previous.get("completed_batches")))
        replay = source.get("exact_replay") or {}
        source_complete = acquired == unit["batches"] and (
            unit["batches"] == 0 or replay.get("verified") is True
        )
        evaluation = result.get("prediction_evaluation") or {}
        native_valid = evaluation.get("valid") is True
        forecast_usable = native_valid and "Q" in sealed and not mismatch and not result_issue
        if not forecast_usable and status in TERMINAL:
            tags.append(("forecast_unavailable_or_invalid", "Q", "No zero imputation"))
        if status in TERMINAL:
            for stage in STAGES:
                if stage not in sealed:
                    tags.append(
                        ("missing_or_invalid_stage", stage, "Retained in planned denominator")
                    )
            if acquired != unit["batches"]:
                tags.append(("source_batch_shortfall", "source", f"{acquired}/{unit['batches']}"))
            if acquired and not replay.get("verified"):
                tags.append(("source_replay_missing_or_failed", "source", "See retained replay"))
        for failure in (state.get("failure"), result.get("failure"), source.get("failure")):
            tags.extend(failure_tags(failure))
        if result.get("fatal_execution_error"):
            tags.append(("fatal_execution_error", "", "Execution qualification requires review"))
        session = {
            **dimensions(unit),
            "status": status,
            "planned_source_batches": unit["batches"],
            "completed_source_batches": acquired,
            "source_complete": source_complete,
            "sealed_posttests": len(sealed),
            "missing_posttests": [s for s in STAGES if s not in sealed],
            "native_evaluation_valid": native_valid,
            "forecast_usable": forecast_usable,
            "result_path": str(result_path),
            "status_path": str(status_path),
        }
        sessions.append(session)
        for response in METRICS[unit["system"]]:
            values = native_metric(
                unit["system"], (evaluation.get("metrics") or {}).get(response) or {}
            )
            values["metric_available"] = values["metric_available"] and forecast_usable
            issue = (
                ""
                if values["metric_available"]
                else (
                    "forecast_unavailable_or_invalid"
                    if not forecast_usable
                    else "invalid_native_metric"
                )
            )
            if not values["metric_available"]:
                values.update(dict.fromkeys(VALUES))
            if issue == "invalid_native_metric":
                tags.append((issue, "Q", response))
            metric_rows.append(
                {
                    **session,
                    "response": response,
                    **values,
                    "metric_issue": issue,
                    "reference_semantics": REFERENCE[unit["system"]],
                }
            )
        for category, stage, detail in sorted(set(tags)):
            failures.append(
                {
                    **dimensions(unit),
                    "status": status,
                    "category": category,
                    "stage": stage,
                    "detail": detail,
                    "result_path": str(result_path),
                    "status_path": str(status_path),
                }
            )
    return sessions, metric_rows, failures


def grouped_counts(sessions, keys):
    groups = defaultdict(list)
    for row in sessions:
        groups[tuple(row[k] for k in keys)].append(row)
    output = []
    for group, rows in sorted(groups.items()):
        output.append(
            {
                **dict(zip(keys, group, strict=True)),
                "planned_sessions": len(rows),
                "terminal_sessions": sum(r["status"] in TERMINAL for r in rows),
                "completed_sessions": sum(r["status"] == "completed" for r in rows),
                "incomplete_or_failed_sessions": sum(
                    r["status"] in TERMINAL - {"completed"} for r in rows
                ),
                "not_terminal_sessions": sum(r["status"] not in TERMINAL for r in rows),
                "usable_forecasts": sum(r["forecast_usable"] for r in rows),
                "missing_forecasts": sum(not r["forecast_usable"] for r in rows),
                "planned_source_batches": sum(r["planned_source_batches"] for r in rows),
                "completed_source_batches": sum(r["completed_source_batches"] for r in rows),
                "sealed_posttests": sum(r["sealed_posttests"] for r in rows),
            }
        )
    return output


def aggregate_metrics(rows, *, by_repeat=False):
    """Average sessions inside each world, then give observed worlds equal weight."""
    keys = (*CONDITION, "response", "interval_level", *(("repeat",) if by_repeat else ()))
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    output = []
    for group, selected in sorted(groups.items()):
        worlds = defaultdict(list)
        for row in selected:
            worlds[row["world"]].append(row)
        world_rows = []
        for world, sessions in sorted(worlds.items()):
            available = [r for r in sessions if r["metric_available"]]
            values = {}
            for field in VALUES:
                present = [r[field] for r in available if r[field] is not None]
                values[field] = fmean(present) if present else None
                values[f"{field}_sessions"] = len(present)
            world_rows.append(
                {
                    "world": world,
                    "planned_sessions": len(sessions),
                    "available_sessions": len(available),
                    "missing_sessions": len(sessions) - len(available),
                    "coverage_complete": len(available) == len(sessions),
                    **values,
                }
            )
        summary = {
            **dict(zip(keys, group, strict=True)),
            "planned_sessions": len(selected),
            "available_sessions": sum(r["available_sessions"] for r in world_rows),
            "missing_sessions": sum(r["missing_sessions"] for r in world_rows),
            "planned_worlds": len(world_rows),
            "observed_worlds": sum(r["available_sessions"] > 0 for r in world_rows),
            "complete_worlds": sum(r["coverage_complete"] for r in world_rows),
            "coverage_complete": all(r["coverage_complete"] for r in world_rows),
            "reference_semantics": selected[0]["reference_semantics"],
            "worlds": world_rows,
        }
        for field in VALUES:
            present = [r[field] for r in world_rows if r[field] is not None]
            summary[f"{field}_world_equal_available"] = fmean(present) if present else None
            summary[f"{field}_observed_worlds"] = len(present)
            summary[f"{field}_world_equal_complete"] = (
                fmean(present) if summary["coverage_complete"] and present else None
            )
        output.append(summary)
    return output


def build_report(root):
    root = Path(root).resolve()
    design, issue = read_optional(root / "design.json")
    if issue or not design:
        raise ValueError("Missing or unreadable design.json")
    units = validate_design(design)
    live_summary, summary_issue = read_optional(root / "summary.json")
    sessions, metrics, failures = collect(root, units, live_summary)
    totals = grouped_counts(sessions, ())[0]
    terminal = totals["terminal_sessions"] == 300
    retries, retry_issue = read_optional(root / "service-retries.json")
    retry_final = retries.get("final", {})
    retry_state = retries.get("status", "pending" if design.get("service_retry_policy") else "none")
    service = {
        "status": retry_state,
        "ledger_path": str(root / "service-retries.json") if retries else None,
        "ledger_issue": retry_issue if (root / "service-retries.json").exists() else None,
        **{
            key: retry_final.get(key)
            for key in (
                "effective_units",
                "service_retry_attempts",
                "retried_units",
                "service_interruptions_remaining",
                "needs_review",
                "scientific_failures_retained",
                "completed_units",
            )
        },
    }
    service_finished = retry_state in {"none", "completed"}
    phase = "terminal" if service_finished else "service_retries"
    summary = {
        "schema_version": "unified-matrices-descriptive-report-1",
        "generated_at": datetime.now(UTC).isoformat(),
        "phase": phase if terminal else "partial",
        "execution_complete": terminal and service_finished,
        "primary_units_terminal": terminal,
        "service_retries": service,
        "all_sessions_completed": totals["completed_sessions"] == 300,
        "input_root": str(root),
        "design_path": str(root / "design.json"),
        "source_commit": design.get("source_commit"),
        "experiment_note": design.get("experiment_note"),
        "live_summary_issue": summary_issue,
        "scope": "Only the new 300 sessions; retained 150 and earlier broad studies excluded",
        "counts": {
            **totals,
            "planned_posttests": 900,
            "planned_query_conditions": 3600,
            "planned_response_rows": len(metrics),
            "planned_prediction_values": 12 * len(metrics),
            "usable_prediction_values": sum(
                r["valid_queries"] for r in metrics if r["metric_available"]
            ),
            "failure_records": len(failures),
            "sessions_with_failure_records": len({(r["repeat"], r["id"]) for r in failures}),
        },
        "status_counts": dict(sorted(Counter(r["status"] for r in sessions).items())),
        "failure_categories": dict(sorted(Counter(r["category"] for r in failures).items())),
        "by_matrix": grouped_counts(sessions, ("matrix",)),
        "by_system": grouped_counts(sessions, ("system",)),
        "condition_counts": grouped_counts(sessions, CONDITION),
        "world_condition_counts": grouped_counts(sessions, (*CONDITION, "world")),
        "repeat_condition_counts": grouped_counts(sessions, (*CONDITION, "repeat")),
        "metrics": aggregate_metrics(metrics),
        "metrics_by_repeat": aggregate_metrics(metrics, by_repeat=True),
        "interpretation": [
            "Descriptive native evaluator readouts, not scientific-success or abduction rates.",
            "All sessions stay in denominators; absent/invalid metrics are null, never zero.",
            "User-directed service retries retain every interrupted attempt separately; "
            "the effective 300-unit analysis uses the resolved attempt without score selection.",
            "Usable Q responses from otherwise incomplete sessions are retained and flagged.",
            "Means average sessions within each world, then weight observed worlds equally.",
            "Complete-grid means are null until all planned session responses are available.",
            "PA intervals are 90%; others are 80%. Reference semantics stay system-specific.",
            "Responses and experimental conditions are not merged into an ability score.",
            "Raw provider payloads, credentials and free-text failure messages are not exported.",
            "Failures and execution qualification require inspection before a publication claim.",
        ],
    }
    return summary, metrics, failures


def display(value):
    return "missing" if value is None else f"{value:.5g}"


def markdown(summary):
    c = summary["counts"]
    lines = [
        "# Unified six-system matrices: descriptive results",
        "",
        f"Status: **{summary['phase']}**. Generated {summary['generated_at']}.",
        "",
        f"Terminal sessions: {c['terminal_sessions']}/300; completed sessions: "
        f"{c['completed_sessions']}/300; incomplete/failed: {c['incomplete_or_failed_sessions']}; "
        f"not terminal: {c['not_terminal_sessions']}.",
        "",
        f"Source assays: {c['completed_source_batches']}/3,420; sealed K1/Q/K2 stages: "
        f"{c['sealed_posttests']}/900; usable forecasts: {c['usable_forecasts']}/300. "
        f"Missing or invalid forecasts: {c['missing_forecasts']}/300.",
        "",
        "The retained 150 sessions are separate and are not added to these results. "
        "Execution counts do not measure scientific success.",
        "",
        "## Coverage",
        "",
        "| System | Planned | Terminal | Completed | Usable Q | Missing Q | Source assays |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    service = summary.get("service_retries", {})
    if service.get("status", "none") != "none":
        insert_at = lines.index("## Coverage")
        lines[insert_at:insert_at] = [
            f"Service retry phase: {service['status']}; additional technical attempts: "
            f"{service.get('service_retry_attempts')}; units retried: "
            f"{service.get('retried_units')}; service interruptions remaining: "
            f"{service.get('service_interruptions_remaining')}. "
            "Interrupted originals remain in the service-retries.json ledger. "
            "These technical attempts do not enlarge the 300-unit scientific denominator.",
            "",
        ]
    for row in summary["by_system"]:
        lines.append(
            f"| {row['system']} | {row['planned_sessions']} | {row['terminal_sessions']} | "
            f"{row['completed_sessions']} | {row['usable_forecasts']} | "
            f"{row['missing_forecasts']} | "
            f"{row['completed_source_batches']}/{row['planned_source_batches']} |"
        )
    lines += [
        "",
        "## Response-specific prediction readouts",
        "",
        "Each available-case value averages sessions within a world, then weights observed worlds "
        "equally. Coverage reports available/planned sessions and observed/planned worlds. "
        "Incomplete grids remain explicit; complete-grid values are null until every "
        "planned response is available. PA intervals are 90%; all others are 80%. "
        "RX MAE targets five-observation means and its coverage targets individual observations. "
        "Other reference definitions appear in summary.json and session_metrics.csv.",
        "",
        "| System | Information | Goal | Research | Response | Interval | "
        "Sessions; worlds | MAE | Coverage | Width |",
        "| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: |",
    ]
    for row in summary["metrics"]:
        lines.append(
            f"| {row['system']} | {row['arm']} | {row['goal']} | {row['opportunity']} | "
            f"{row['response']} | {row['interval_level']:.0%} | "
            f"{row['available_sessions']}/{row['planned_sessions']}; "
            f"{row['observed_worlds']}/{row['planned_worlds']} | "
            f"{display(row['mae_world_equal_available'])} | "
            f"{display(row['coverage_world_equal_available'])} | "
            f"{display(row['interval_width_world_equal_available'])} |"
        )
    lines += ["", "## Failures and missingness", ""]
    if summary["failure_categories"]:
        lines += ["| Category | Records |", "| --- | ---: |"]
        lines += [f"| {k} | {v} |" for k, v in summary["failure_categories"].items()]
    else:
        lines.append(
            "No recorded failures in currently readable results; pending sessions remain pending."
        )
    lines += [
        "",
        "failures.csv contains structured categories and paths to retained records. "
        "A session may have multiple failure records. Free-text provider messages are omitted.",
        "",
        "## Interpretation and scope",
        "",
        *(f"- {line}" for line in summary["interpretation"]),
        "",
        "Files: summary.json (denominators, world and repeat breakdowns), session_metrics.csv "
        "(one planned session-response row, including missing rows), failures.csv (all recorded "
        "failure categories). This report performs no new experiment or participant call.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(output, summary, metrics, failures):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    for name, fields, rows in (
        ("session_metrics.csv", SESSION_FIELDS, metrics),
        ("failures.csv", FAILURE_FIELDS, failures),
    ):
        with (output / name).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    (output / "REPORT.md").write_text(markdown(summary), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.root.resolve() == args.output.resolve():
        parser.error("Output must not overwrite the execution root summary")
    summary, metrics, failures = build_report(args.root)
    write_outputs(args.output, summary, metrics, failures)
    print(json.dumps({"phase": summary["phase"], **summary["counts"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
