#!/usr/bin/env python3
"""Build one readable summary for the four independent A-P development blocks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_RUN_ROOTS = (
    Path("runs/development/ap-deepseek-reaction-seed2-20260813"),
    Path("runs/development/ap-deepseek-electrochemical-seed2-20260813"),
    Path("runs/development/ap-wellau-reaction-seed2-20260813"),
    Path("runs/development/ap-wellau-electrochemical-seed2-20260813"),
)

HISTORICAL_DIAGNOSIS_MODE = "historical_diagnosis"
PLATFORM_REQUALIFICATION_MODE = "platform_requalification"
MCP_TOOL_FAILURE_CATEGORIES = (
    "provider_network",
    "transport_ipc_os",
    "agent_invalid",
    "unclassified",
)
EXPECTED_PROVIDER_TASK_COVERAGE = {
    ("deepseek", "reaction-safety-constrained"),
    ("deepseek", "electrochemical-conversion"),
    ("wellau", "reaction-safety-constrained"),
    ("wellau", "electrochemical-conversion"),
}
EXPECTED_ARMS = {"aligned_nominal", "misindexed_nominal", "opaque"}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _replay_verified(result: dict[str, Any]) -> bool:
    replay = result.get("exact_replay")
    return isinstance(replay, dict) and replay.get("verified") is True


def _disposition(result: dict[str, Any]) -> str:
    if result.get("completed") is True:
        return "qualification_completed"
    analysis = result.get("analysis") or {}
    complete = int(analysis.get("complete_experiment_count") or 0)
    committed = int(analysis.get("committed_operation_count") or 0)
    if complete == 0 and committed == 0 and result.get("failure"):
        return "infrastructure_failure_retained"
    return "right_censored_retained"


def _mcp_failure_counts(result: dict[str, Any]) -> dict[str, int] | None:
    resources = result.get("method_resources") or {}
    taxonomy = resources.get("mcp_tool_failure_taxonomy")
    if not isinstance(taxonomy, dict):
        return None
    counts = taxonomy.get("counts_by_category")
    if not isinstance(counts, dict) or set(counts) != set(MCP_TOOL_FAILURE_CATEGORIES):
        return None
    if any(isinstance(counts[category], bool) or not isinstance(counts[category], int)
           or counts[category] < 0 for category in MCP_TOOL_FAILURE_CATEGORIES):
        return None
    return {category: counts[category] for category in MCP_TOOL_FAILURE_CATEGORIES}


def _cell_summary(result: dict[str, Any]) -> dict[str, Any]:
    analysis = result.get("analysis") or {}
    resources = result.get("method_resources") or {}
    qualification = result.get("qualification") or {}
    failure = result.get("failure") or None
    return {
        "arm": result["arm"],
        "disposition": _disposition(result),
        "qualification_completed": result.get("completed") is True,
        "complete_experiments": int(analysis.get("complete_experiment_count") or 0),
        "planned_complete_experiments": 10,
        "committed_operations": int(analysis.get("committed_operation_count") or 0),
        "attempted_operations": int(analysis.get("operation_attempt_count") or 0),
        "exact_replay_verified": _replay_verified(result),
        "belief_checkpoint_count": len(analysis.get("belief_snapshots") or []),
        "planned_belief_checkpoint_count": 5,
        "final_recommendation_committed": analysis.get("final_recommendation") is not None,
        "provider_error_events": int(resources.get("provider_error_event_count") or 0),
        "recovered_mcp_tool_failures": int(resources.get("recovered_mcp_tool_failure_count") or 0),
        "maximum_consecutive_mcp_tool_failures": int(
            resources.get("maximum_consecutive_mcp_tool_failure_count") or 0
        ),
        "mcp_tool_failure_counts_by_category": _mcp_failure_counts(result),
        "input_tokens": int(resources.get("input_token_count") or 0),
        "uncached_input_tokens": int(resources.get("uncached_input_token_count") or 0),
        "output_tokens": int(resources.get("output_token_count") or 0),
        "failed_qualification_checks": list(qualification.get("failed_checks") or []),
        "failure": (
            None
            if failure is None
            else {"type": failure.get("type"), "message": failure.get("message")}
        ),
    }


def build_summary(
    run_roots: tuple[Path, ...],
    *,
    mode: str = HISTORICAL_DIAGNOSIS_MODE,
    expected_source_commit: str | None = None,
) -> dict[str, Any]:
    if mode not in {HISTORICAL_DIAGNOSIS_MODE, PLATFORM_REQUALIFICATION_MODE}:
        raise ValueError(f"unsupported result mode: {mode}")
    if mode == PLATFORM_REQUALIFICATION_MODE and not expected_source_commit:
        raise ValueError("platform requalification requires expected_source_commit")
    blocks: list[dict[str, Any]] = []
    for root in run_roots:
        report_path = root / "matrix_report.json"
        if not report_path.is_file():
            raise FileNotFoundError(f"missing terminal matrix report: {report_path}")
        report = _read_json(report_path)
        if report.get("all_cells_terminal") is not True:
            raise ValueError(f"matrix is not terminal: {report_path}")
        store_audit = report.get("store_audit") or {}
        if store_audit.get("missing_cell_key_sha256") or store_audit.get("invalid_receipts"):
            raise ValueError(f"matrix store audit is incomplete: {report_path}")
        seed_reports = report.get("seed_reports") or []
        if len(seed_reports) != 1 or len(seed_reports[0].get("results") or []) != 3:
            raise ValueError(f"unexpected seed/arm coverage: {report_path}")
        cells = [_cell_summary(result) for result in seed_reports[0]["results"]]
        block = {
            "run_root": root.as_posix(),
            "provider_id": report["provider_id"],
            "model": report["model"],
            "task_id": report["task_id"],
            "world_seeds": report["world_seeds"],
            "terminal_cells": int(report["terminal_cell_count"]),
            "expected_cells": int(report["expected_cell_count"]),
            "qualification_completed_cells": int(report["completed_cell_count"]),
            "store_missing_cells": len(store_audit.get("missing_cell_key_sha256") or []),
            "store_invalid_receipts": len(store_audit.get("invalid_receipts") or []),
            "cells": cells,
        }
        if mode == PLATFORM_REQUALIFICATION_MODE:
            source_commit = report.get("source_commit")
            if source_commit != expected_source_commit:
                raise ValueError(
                    f"source commit mismatch in {report_path}: "
                    f"expected {expected_source_commit}, observed {source_commit}"
                )
            if report.get("world_seeds") != [2]:
                raise ValueError(f"unexpected world-seed coverage: {report_path}")
            if {cell["arm"] for cell in cells} != EXPECTED_ARMS:
                raise ValueError(f"unexpected arm coverage: {report_path}")
            if any(cell["mcp_tool_failure_counts_by_category"] is None for cell in cells):
                raise ValueError(f"typed MCP failure taxonomy is incomplete: {report_path}")
            block["source_commit"] = source_commit
        blocks.append(block)

    if mode == PLATFORM_REQUALIFICATION_MODE:
        observed_coverage = {
            (block["provider_id"], block["task_id"])
            for block in blocks
        }
        if len(blocks) != 4 or observed_coverage != EXPECTED_PROVIDER_TASK_COVERAGE:
            raise ValueError(
                "platform requalification does not contain the four expected "
                "provider-by-task blocks"
            )

    cells = [cell for block in blocks for cell in block["cells"]]
    active_cells = [cell for cell in cells if cell["committed_operations"] > 0]
    infrastructure_cells = [
        cell for cell in cells if cell["disposition"] == "infrastructure_failure_retained"
    ]
    aggregate = {
        "blocks_terminal": sum(
            block["terminal_cells"] == block["expected_cells"] for block in blocks
        ),
        "blocks_total": len(blocks),
        "cells_terminal": sum(block["terminal_cells"] for block in blocks),
        "cells_total": sum(block["expected_cells"] for block in blocks),
        "qualification_completed_cells": sum(cell["qualification_completed"] for cell in cells),
        "right_censored_cells": sum(
            cell["disposition"] == "right_censored_retained" for cell in cells
        ),
        "infrastructure_failure_cells": len(infrastructure_cells),
        "planned_complete_experiments": sum(cell["planned_complete_experiments"] for cell in cells),
        "observed_complete_experiments": sum(cell["complete_experiments"] for cell in cells),
        "cells_reaching_10_experiments": sum(
            cell["complete_experiments"] == cell["planned_complete_experiments"] for cell in cells
        ),
        "cells_with_committed_operations": len(active_cells),
        "active_cells_with_exact_replay": sum(
            cell["exact_replay_verified"] for cell in active_cells
        ),
        "committed_operations": sum(cell["committed_operations"] for cell in cells),
        "attempted_operations": sum(cell["attempted_operations"] for cell in cells),
        "provider_error_events": sum(cell["provider_error_events"] for cell in cells),
        "store_missing_cells": sum(block["store_missing_cells"] for block in blocks),
        "store_invalid_receipts": sum(block["store_invalid_receipts"] for block in blocks),
    }

    if mode == PLATFORM_REQUALIFICATION_MODE:
        aggregate.update(
            {
                "typed_mcp_failure_taxonomy_cells": sum(
                    cell["mcp_tool_failure_counts_by_category"] is not None for cell in cells
                ),
                "mcp_tool_failures_by_category": {
                    category: sum(
                        cell["mcp_tool_failure_counts_by_category"][category]
                        for cell in cells
                    )
                    for category in MCP_TOOL_FAILURE_CATEGORIES
                },
            }
        )
        platform_gate_failures: list[str] = []
        if (
            aggregate["active_cells_with_exact_replay"]
            != aggregate["cells_with_committed_operations"]
        ):
            platform_gate_failures.append("active_cell_exact_replay_incomplete")
        if aggregate["mcp_tool_failures_by_category"]["unclassified"] != 0:
            platform_gate_failures.append("unclassified_mcp_tool_failure_present")
        platform_requalification = {
            "passed": not platform_gate_failures,
            "failed_checks": platform_gate_failures,
        }
    else:
        platform_requalification = None

    if mode == PLATFORM_REQUALIFICATION_MODE:
        platform_passed = platform_requalification["passed"]
        interpretation = {
            "supported": [
                (
                    "All four platform-requalification blocks reached immutable "
                    "terminal storage state."
                ),
                "Every cell exposes the frozen typed MCP failure taxonomy.",
                *(
                    [
                        "Every cell with committed physical operations has an exact "
                        "replay record."
                    ]
                    if platform_passed
                    else []
                ),
            ],
            "not_supported": [
                "A provider, model, task, or prior-arm scientific capability comparison.",
                "Formal/R5/C2 admission or any replacement of retained historical outcomes.",
            ],
            "platform_findings": [
                "Platform and agent-invalid MCP failures are reported as separate categories.",
                (
                    "Provider-specific cached, uncached and output-token ledgers are "
                    "retained per cell."
                ),
                (
                    "Zero-operation infrastructure outcomes remain visible rather "
                    "than being overwritten."
                ),
            ],
            "next_action": (
                "Use the complete development result to decide qualification readiness. "
                "Any platform change still requires its affected qualification block to "
                "restart from the first cell; retained scientific failures are not retryable."
                if platform_passed
                else "Platform requalification failed its frozen evidence-integrity gates. "
                "Retain all outcomes and diagnose the failed checks before any formal use."
            ),
        }
    else:
        interpretation = {
            "supported": [
                "All four development blocks reached immutable terminal storage state.",
                "Every cell with committed physical operations has an exact replay record.",
                "No provider error event was observed.",
            ],
            "not_supported": [
                "A provider, model, task, or prior-arm scientific capability comparison.",
                "Formal/R5/C2 admission or any replacement of retained historical outcomes.",
            ],
            "platform_findings": [
                (
                    "Recovered MCP failures currently mix agent-invalid schema/timing "
                    "events with transport and infrastructure events."
                ),
                (
                    "Provider-specific cached, uncached, output-token, and monetary "
                    "accounting need separate frozen envelopes."
                ),
                (
                    "Zero-operation IPC/OS failures need cell-level infrastructure "
                    "classification before terminal disposition."
                ),
                (
                    "The supervisor must use UTF-8 and terminal store receipts rather "
                    "than output-directory presence."
                ),
            ],
            "next_action": (
                "Fix and test the shared execution semantics, freeze the revised "
                "provider-specific resource policy prospectively, then rerun all four "
                "affected qualification blocks from their first cell in new output roots."
            ),
        }
    return {
        "schema_version": (
            "chemworld-work-ii-ap-platform-requalification-results-0.2"
            if mode == PLATFORM_REQUALIFICATION_MODE
            else "chemworld-work-ii-ap-development-results-0.1"
        ),
        "status": (
            (
                "terminal_platform_requalification_complete"
                if platform_requalification["passed"]
                else "terminal_platform_requalification_failed"
            )
            if mode == PLATFORM_REQUALIFICATION_MODE
            else "terminal_platform_requalification_required"
        ),
        "development_only": True,
        "formal_result": False,
        "coverage": {
            "providers": ["deepseek", "wellau"],
            "tasks": ["reaction-safety-constrained", "electrochemical-conversion"],
            "arms": ["aligned_nominal", "misindexed_nominal", "opaque"],
            "world_seed": 2,
            "experiments_per_cell": 10,
            "belief_checkpoints": [0, 2, 4, 7, 10],
        },
        "aggregate": aggregate,
        "blocks": blocks,
        **(
            {"platform_requalification": platform_requalification}
            if platform_requalification is not None
            else {}
        ),
        "interpretation": interpretation,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    requalification_complete = (
        summary["status"] == "terminal_platform_requalification_complete"
    )
    requalification_failed = summary["status"] == "terminal_platform_requalification_failed"
    lines = [
        "# Work II A-P independent terminal D1 development results",
        "",
        (
            "Status: terminal development evidence; platform requalification complete; "
            "not formal/R5/C2 evidence."
            if requalification_complete
            else "Status: terminal development evidence; platform requalification failed; "
            "not formal/R5/C2 evidence."
            if requalification_failed
            else "Status: terminal development evidence; platform requalification required; "
            "not formal/R5/C2 evidence."
        ),
        "",
        "## Coverage and outcome",
        "",
        (
            f"The four frozen provider-by-task blocks reached `{aggregate['blocks_terminal']}/"
            f"{aggregate['blocks_total']}` block terminal state and `{aggregate['cells_terminal']}/"
            f"{aggregate['cells_total']}` immutable cell terminal state. Only "
            f"`{aggregate['qualification_completed_cells']}/"
            f"{aggregate['cells_total']}` cells passed "
            "the complete qualification contract. Terminal therefore does not mean passed."
        ),
        "",
        (
            f"Across the planned `{aggregate['planned_complete_experiments']}` experiments, "
            f"`{aggregate['observed_complete_experiments']}` completed and "
            f"`{aggregate['cells_reaching_10_experiments']}/"
            f"{aggregate['cells_total']}` cells reached "
            "10/10. All "
            f"`{aggregate['active_cells_with_exact_replay']}/"
            f"{aggregate['cells_with_committed_operations']}` "
            "cells with committed physical operations passed exact replay. There were "
            f"`{aggregate['provider_error_events']}` provider error events, "
            f"`{aggregate['store_missing_cells']}` missing cells and "
            f"`{aggregate['store_invalid_receipts']}` invalid store receipts."
        ),
        "",
        "## Cell-level results",
        "",
        (
            "| Provider | Task | Arm | Disposition | Experiments | Ops "
            "committed/attempted | Replay | MCP recovered/max consecutive | Checkpoints "
            "| Final | Failure or failed gates |"
        ),
        "|---|---|---|---|---:|---:|---|---:|---:|---|---|",
    ]
    for block in summary["blocks"]:
        for cell in block["cells"]:
            reason = ""
            if cell["failure"]:
                reason = f"{cell['failure']['type']}: {cell['failure']['message']}"
            if cell["failed_qualification_checks"]:
                gates = ", ".join(cell["failed_qualification_checks"])
                reason = f"{reason}; {gates}" if reason else gates
            lines.append(
                "| "
                + " | ".join(
                    [
                        block["provider_id"],
                        block["task_id"],
                        cell["arm"],
                        cell["disposition"],
                        f"{cell['complete_experiments']}/10",
                        f"{cell['committed_operations']}/{cell['attempted_operations']}",
                        "pass" if cell["exact_replay_verified"] else "not available",
                        (
                            f"{cell['recovered_mcp_tool_failures']}/"
                            f"{cell['maximum_consecutive_mcp_tool_failures']}"
                        ),
                        f"{cell['belief_checkpoint_count']}/5",
                        "yes" if cell["final_recommendation_committed"] else "no",
                        reason or "none",
                    ]
                )
                + " |"
            )
    if requalification_complete or requalification_failed:
        taxonomy = aggregate["mcp_tool_failures_by_category"]
        gate = summary["platform_requalification"]
        lines.extend(
            [
                "",
                "## Platform requalification",
                "",
                (
                    f"Typed MCP failure accounting is complete for "
                    f"`{aggregate['typed_mcp_failure_taxonomy_cells']}/"
                    f"{aggregate['cells_total']}` cells: provider/network "
                    f"`{taxonomy['provider_network']}`, transport/IPC/OS "
                    f"`{taxonomy['transport_ipc_os']}`, agent-invalid "
                    f"`{taxonomy['agent_invalid']}`, and unclassified "
                    f"`{taxonomy['unclassified']}`."
                ),
                "",
                (
                    "Frozen platform gates: pass."
                    if gate["passed"]
                    else "Frozen platform gates: fail — "
                    + ", ".join(gate["failed_checks"])
                    + "."
                ),
            ]
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            (
                "This block supports execution and failure-mode diagnosis only. "
                "Missingness and censoring depend on provider, task and arm, so the "
                "retained trajectories do not support a scientific provider/model/arm "
                "comparison or formal admission."
            ),
            "",
            (
                "The frozen scientific gates remain unchanged: three arms, ten "
                "experiments, checkpoints at 0/2/4/7/10, participant-authored final "
                "recommendation, exact replay, resource accounting, all-failure "
                "retention, immutable terminals and missing-infrastructure-only retry."
            ),
            "",
            summary["interpretation"]["next_action"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", action="append", type=Path)
    parser.add_argument(
        "--mode",
        choices=(HISTORICAL_DIAGNOSIS_MODE, PLATFORM_REQUALIFICATION_MODE),
        default=HISTORICAL_DIAGNOSIS_MODE,
    )
    parser.add_argument("--expected-source-commit")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()
    roots = tuple(args.run_root) if args.run_root else DEFAULT_RUN_ROOTS
    if len(roots) != 4:
        parser.error("exactly four --run-root values are required")
    if args.mode == PLATFORM_REQUALIFICATION_MODE and not args.expected_source_commit:
        parser.error("--expected-source-commit is required for platform requalification")
    summary = build_summary(
        roots,
        mode=args.mode,
        expected_source_commit=args.expected_source_commit,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(render_markdown(summary), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
