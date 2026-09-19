#!/usr/bin/env python3
"""Export readable, pre-truth RX P/S reports without provider-private payloads."""
# ruff: noqa: E501

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

RESULT_VERSIONS = (
    "posttest-repair-v10",
    "posttest-repair-v9",
    "posttest-repair-v8",
    "posttest-repair-v7",
    "posttest-repair-v3",
    "source-repair-v9",
    "source-repair-v8",
    "source-repair-v3",
)
METRICS = (
    "yield",
    "selectivity",
    "conversion",
    "byproduct_signal",
    "degradation_warning",
    "safety_risk",
    "score",
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def resolve_result(root: Path, cell_id: str) -> tuple[Path, dict[str, Any]]:
    folder = root / "sources" / cell_id
    candidates = [folder / version / "effective-result.json" for version in RESULT_VERSIONS]
    candidates.append(folder / "result.json")
    for path in candidates:
        if path.exists():
            return path, load(path)
    raise FileNotFoundError(f"no retained result for {cell_id}")


def fmt_number(value: Any, digits: int = 4) -> str:
    if value is None:
        return "—"
    if isinstance(value, (int, float)):
        return f"{float(value):.{digits}f}"
    return str(value)


def action_summary(actions: Sequence[Mapping[str, Any]]) -> dict[str, str]:
    solvents: list[str] = []
    reagents: list[str] = []
    catalysts: list[str] = []
    heats: list[str] = []
    quenched = False
    for action in actions:
        operation = action.get("operation")
        if operation == "add_solvent":
            solvents.append(f"S{action.get('solvent')} ({float(action.get('volume_L', 0)):.4f} L)")
        elif operation == "add_reagent":
            reagents.append(f"{float(action.get('amount_mol', 0)):.6f} mol")
        elif operation == "add_catalyst":
            catalysts.append(
                f"C{action.get('catalyst')} ({float(action.get('catalyst_amount_mol', 0)):.6f} mol)"
            )
        elif operation == "heat":
            heats.append(
                f"{action.get('target_temperature_K')} K x {action.get('duration_s')} s @ "
                f"{action.get('stirring_speed_rpm')} rpm"
            )
        elif operation == "quench":
            quenched = True
    return {
        "solvent": " + ".join(solvents) or "—",
        "reagent": " + ".join(reagents) or "—",
        "catalyst": " + ".join(catalysts) or "—",
        "heat": " → ".join(heats) or "—",
        "quench": "yes" if quenched else "no",
    }


def render_recovery(result: Mapping[str, Any], result_path: Path) -> list[str]:
    recovery = result.get("recovery")
    if not isinstance(recovery, Mapping):
        return ["No recovery override was required for this task."]
    stages = ", ".join(str(stage) for stage in recovery.get("repair_stages", [])) or "source"
    return [
        f"- Effective result location: `{result_path.parent.name}`",
        f"- Recovery version: `{recovery.get('recovery_version', 'unknown')}`",
        f"- Repaired stages: `{stages}`",
        f"- Source experiments rerun: `{bool(recovery.get('source_experiments_rerun'))}`",
        f"- Original source thread reused: `{bool(recovery.get('thread_reused'))}`",
        f"- Truth revealed during recovery: `{bool(recovery.get('truth_revealed_to_agent'))}`",
    ]


def render_q(payload: Mapping[str, Any] | None) -> list[str]:
    if not payload:
        return ["No valid Q payload was produced."]
    lines = ["### Overall rationale", "", str(payload.get("rationale") or "No overall rationale supplied.")]
    for prediction in payload.get("predictions", []):
        lines.extend(["", f"### {prediction.get('query_id', 'unknown')}", "", str(prediction.get("rationale") or "")])
        metrics = prediction.get("metrics") or {}
        lines.extend(["", "| Metric | Point estimate | 80% lower | 80% upper |", "|---|---:|---:|---:|"])
        for metric in sorted(metrics):
            values = metrics[metric]
            lines.append(
                f"| {metric} | {fmt_number(values.get('estimate'))} | "
                f"{fmt_number(values.get('lower80'))} | {fmt_number(values.get('upper80'))} |"
            )
    return lines


def render_report(result_path: Path, result: Mapping[str, Any]) -> str:
    cell_id = str(result["cell_id"])
    batches = list(result.get("batches", []))
    validations = result.get("posttest_validation") or {}
    posttests = result.get("posttests") or {}
    lines = [
        f"# {cell_id}",
        "",
        "## Run summary",
        "",
        f"- World: `{result.get('world_id')}`",
        f"- Locus: `{result.get('locus')}`",
        f"- Goal: `{result.get('goal')}`",
        f"- Arm: `{result.get('arm')}`",
        f"- Status: `{result.get('status')}`",
        f"- Source status: `{result.get('source_status')}`",
        f"- Experimental sessions: `{len(batches)}/12`",
        f"- Operations: `{result.get('operations')}`",
        f"- Exact replay verified: `{bool((result.get('exact_replay') or {}).get('verified'))}`",
        f"- Rollbacks: `{result.get('rollbacks', 0)}`",
        f"- Posttest chain sealed: `{bool(result.get('posttest_chain_sealed'))}`",
        "",
        "### Recovery status",
        "",
        *render_recovery(result, result_path),
        "",
        "## Sealed recommendation",
        "",
    ]
    recommendation = result.get("recommendation") or {}
    if recommendation:
        lines.extend(
            [
                f"- Selected batch: `{recommendation.get('selected_experiment_index')}`",
                f"- Rationale: {recommendation.get('selection_rationale') or 'Not supplied.'}",
            ]
        )
    else:
        lines.append("No sealed recommendation was retained.")

    lines.extend(
        [
            "",
            "## Twelve-session experiment table",
            "",
            "| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |",
            "|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for batch in batches:
        summary = action_summary(batch.get("actions", []))
        metrics = batch.get("metrics") or {}
        lines.append(
            f"| {batch.get('ordinal')} | {summary['solvent']} | {summary['reagent']} | "
            f"{summary['catalyst']} | {summary['heat']} | {summary['quench']} | "
            f"{fmt_number(metrics.get('yield'))} | {fmt_number(metrics.get('selectivity'))} | "
            f"{fmt_number(metrics.get('conversion'))} | {fmt_number(metrics.get('byproduct_signal'))} | "
            f"{fmt_number(metrics.get('degradation_warning'))} | {fmt_number(metrics.get('safety_risk'))} | "
            f"{fmt_number(metrics.get('score'))} |"
        )

    lines.extend(["", "## Complete experimental actions and observations", ""])
    for batch in batches:
        lines.extend(
            [
                f"### Batch {batch.get('ordinal')}",
                "",
                f"Lifecycle index: `{batch.get('lifecycle_index')}`; end step: `{batch.get('end_step')}`.",
                "",
                "```json",
                json.dumps(batch, ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
            ]
        )

    k1 = (posttests.get("K1") or {}).get("payload")
    k1_failure = (posttests.get("K1") or {}).get("failure")
    lines.extend(["## K1 — Mechanistic report", ""])
    if isinstance(k1, Mapping) and k1.get("report"):
        lines.extend([str(k1["report"]), ""])
    else:
        lines.extend(
            [
                "No valid K1 payload was produced.",
                "",
                f"Retained failure: `{k1_failure or 'missing_payload'}`. The missing report is not inferred or reconstructed.",
                "",
            ]
        )

    q = (posttests.get("Q") or {}).get("payload")
    lines.extend(["## Q — Blind predictions", "", *render_q(q if isinstance(q, Mapping) else None), ""])

    k2 = (posttests.get("K2") or {}).get("payload")
    lines.extend(["## K2 — Retrospective analysis", ""])
    if isinstance(k2, Mapping) and k2.get("report"):
        lines.extend([str(k2["report"]), ""])
    else:
        lines.extend(
            [
                "No valid K2 payload was produced.",
                "",
                f"Retained failure: `{(posttests.get('K2') or {}).get('failure') or 'missing_payload'}`.",
                "",
            ]
        )

    lines.extend(
        [
            "## Posttest validation and execution metadata",
            "",
            "| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |",
            "|---|:---:|---:|---:|---|---:|",
        ]
    )
    for stage in ("K1", "Q", "K2"):
        turn = posttests.get(stage) or {}
        valid = bool((validations.get(stage) or {}).get("valid"))
        failure = turn.get("failure") or (validations.get(stage) or {}).get("failure") or "none"
        lines.append(
            f"| {stage} | {'yes' if valid else 'no'} | {turn.get('exit_code', '—')} | "
            f"{fmt_number(turn.get('elapsed_s'), 1)} | {failure} | {len(turn.get('provider_errors') or [])} |"
        )

    if not result.get("posttest_chain_sealed"):
        lines.extend(
            [
                "",
                "## Retained incomplete-chain notice",
                "",
                "This cell is not counted as a complete K1/Q/K2 chain. Its twelve source experiments, recommendation, and any valid posttest payloads are preserved, but the missing stage must be repaired in the frozen order before the cell can enter the effective denominator. No missing text has been synthesized for this export.",
            ]
        )

    lines.extend(
        [
            "",
            "## Scope note",
            "",
            "This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.",
            "",
        ]
    )
    return "\n".join(lines)


def status_label(result: Mapping[str, Any]) -> str:
    if result.get("posttest_chain_sealed") is True and result.get("status") == "completed":
        return "complete (recovered)" if result.get("recovery") else "complete"
    missing = [
        stage
        for stage in ("K1", "Q", "K2")
        if not ((result.get("posttests") or {}).get(stage) or {}).get("payload")
    ]
    suffix = f"; missing {', '.join(missing)}" if missing else ""
    return f"retained incomplete{suffix}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--world", action="append", required=True)
    args = parser.parse_args()

    root = args.run_root.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"write-once export already exists: {output}")
    schedule = load(root / "design.json")["schedule"]
    selected = [row for row in schedule if row["world_id"] in set(args.world)]
    expected = len(set(args.world)) * 12
    if len(selected) != expected:
        raise RuntimeError(f"expected {expected} selected cells, found {len(selected)}")

    output.mkdir(parents=True)
    summary_rows: list[dict[str, Any]] = []
    for cell in selected:
        result_path, result = resolve_result(root, cell["cell_id"])
        if len(result.get("batches", [])) != 12 or result.get("source_status") != "completed":
            raise RuntimeError(f"selected cell lacks twelve completed source batches: {cell['cell_id']}")
        destination = output / cell["world_id"] / cell["cell_id"] / "EXPERIMENT_REPORT.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_report(result_path, result), encoding="utf-8")
        validations = result.get("posttest_validation") or {}
        summary_rows.append(
            {
                "arm": result.get("arm"),
                "cell_id": result.get("cell_id"),
                "goal": result.get("goal"),
                "locus": result.get("locus"),
                "operations": result.get("operations"),
                "posttest_chain_sealed": result.get("posttest_chain_sealed") is True,
                "posttest_valid": {
                    stage: bool((validations.get(stage) or {}).get("valid"))
                    for stage in ("K1", "Q", "K2")
                },
                "recovered": bool(result.get("recovery")),
                "source_batches": len(result.get("batches", [])),
                "source_status": result.get("source_status"),
                "status": result.get("status"),
                "world_id": result.get("world_id"),
            }
        )

    for world in args.world:
        rows = [row for row in summary_rows if row["world_id"] == world]
        index = [f"# {world} report index", ""]
        for row in rows:
            index.append(
                f"- [{row['cell_id']}]({row['cell_id']}/EXPERIMENT_REPORT.md) — {status_label({'status': row['status'], 'posttest_chain_sealed': row['posttest_chain_sealed'], 'recovery': row['recovered'], 'posttests': {stage: {'payload': row['posttest_valid'][stage]} for stage in ('K1', 'Q', 'K2')}})}"
            )
        index.append("")
        (output / world / "WORLD_INDEX.md").write_text("\n".join(index), encoding="utf-8")

    complete = sum(row["posttest_chain_sealed"] for row in summary_rows)
    valid_posttests = sum(sum(row["posttest_valid"].values()) for row in summary_rows)
    snapshot = {
        "schema_version": "work-ii-rx-ps-readable-interim-export-1.0",
        "development_evidence": True,
        "truth_embargo_active": True,
        "worlds": args.world,
        "planned_cells": len(summary_rows),
        "complete_cells": complete,
        "retained_incomplete_cells": len(summary_rows) - complete,
        "completed_source_batches": sum(row["source_batches"] for row in summary_rows),
        "planned_source_batches": len(summary_rows) * 12,
        "valid_posttest_payloads": valid_posttests,
        "planned_posttests": len(summary_rows) * 3,
        "cells": summary_rows,
        "excluded": [
            "credentials",
            "provider event streams",
            "thread identifiers",
            "token accounting",
            "reference truth",
            "prediction scores",
            "recommendation retests",
        ],
    }
    dump(output / "SNAPSHOT.json", snapshot)
    readme = [
        "# RX P/S five-world dual-goal block — W03/W04 interim reports",
        "",
        "Date: 2026-09-19. Status: development evidence; the full 60-task block remains incomplete and truth-embargoed.",
        "",
        "This directory extends the existing W01/W02 report package with the next 24 scheduled cells:",
        "",
        f"- {complete}/24 complete K1/Q/K2 chains;",
        "- 288/288 source experiments (12 per cell);",
        f"- {valid_posttests}/72 valid posttest payloads;",
        "- all source actions, observations, recommendations, available K1/Q/K2 text, validation state, and recovery status.",
        "",
        "The final scheduled cell in this snapshot, `RX-W04--S--safety_constrained_optimization--MisIndexed`, completed 12/12 source experiments and retained valid Q/K2 payloads, but K1 failed at the provider with no payload. It is exported as retained incomplete evidence and is not counted as a sealed chain. A future repair must rerun K1→Q→K2 in order without rerunning the source experiments or revealing truth.",
        "",
        "Raw provider streams, credentials, thread identifiers, token accounting, ignored run directories, and machine-private payloads are intentionally excluded. Reference truth, prediction scores, and recommendation retests remain absent until all 60 effective chains are sealed.",
        "",
        "Execution and interpretation are governed by the [master protocol](../../WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_PROTOCOL_V1_0_1.md), [canonical K1-Q-K2 protocol](../../WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md), [RX-P profile](../../WORK_II_RX_P_K1_Q_K2_PROFILE_V1_2.md), [RX-S profile](../../WORK_II_RX_S_K1_Q_K2_PROFILE_V1_0.md), and the retained [v9](../../WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V9_PARALLEL4.md)/[v10](../../WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V10_CONTINUE.md) recovery records.",
        "",
        "Start with [W03](RX-W03/WORLD_INDEX.md), [W04](RX-W04/WORLD_INDEX.md), or the [sanitized snapshot](SNAPSHOT.json). The earlier reports remain in the sibling `work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02` directory.",
        "",
    ]
    (output / "README.md").write_text("\n".join(readme), encoding="utf-8")


if __name__ == "__main__":
    main()
