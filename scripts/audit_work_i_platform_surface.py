"""Audit the exact publication counting rules for the ChemWorld platform surface."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from chemworld.eval.task_metric_endpoints import build_task_metric_contract
from chemworld.tasks import list_tasks
from chemworld.world.instruments import instrument_contracts
from chemworld.world.operations import INSTRUMENTS, OPERATION_TYPES, operation_contracts

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "workstreams/flagship_tasks/reports/task-design-matrix-v1.json"
DEFAULT_JSON = ROOT / "workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json"
DEFAULT_MARKDOWN = ROOT / "workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.md"


def _sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_audit() -> dict[str, Any]:
    tasks = list_tasks()
    task_ids = tuple(task.task_id for task in tasks)
    operation_registry = operation_contracts()
    instrument_registry = instrument_contracts()
    operation_tasks: dict[str, list[str]] = defaultdict(list)
    instrument_tasks: dict[str, list[str]] = defaultdict(list)
    endpoint_rows: list[dict[str, Any]] = []
    task_rows: list[dict[str, Any]] = []
    for task in tasks:
        metric_contract = build_task_metric_contract(task.success_metrics)
        for operation in task.allowed_operations:
            operation_tasks[operation].append(task.task_id)
        for instrument in task.allowed_instruments:
            instrument_tasks[instrument].append(task.task_id)
        endpoints = []
        for endpoint in metric_contract["endpoints"]:
            row = {
                "task_id": task.task_id,
                "metric_id": endpoint["metric_id"],
                "source_layer": endpoint["source_layer"],
                "evaluator_id": endpoint["evaluator_id"],
                "implementation_status": endpoint["implementation_status"],
            }
            endpoint_rows.append(row)
            endpoints.append(row)
        task_rows.append(
            {
                "task_id": task.task_id,
                "task_contract_hash": task.contract_hash,
                "allowed_operation_count": len(task.allowed_operations),
                "allowed_instrument_count": len(task.allowed_instruments),
                "declared_endpoint_count": len(endpoints),
                "all_endpoints_bound": metric_contract["all_metrics_bound"],
                "metric_contract_hash": metric_contract["contract_hash"],
            }
        )

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    matrix_task_ids = tuple(sorted(row["task_id"] for row in matrix["tasks"]))
    validation = matrix["design_validation"]
    registered_operations = tuple(OPERATION_TYPES)
    registered_instruments = tuple(INSTRUMENTS)
    live_task_operation_union = tuple(sorted(operation_tasks))
    live_task_instrument_union = tuple(sorted(instrument_tasks))
    endpoint_keys = tuple((row["task_id"], row["metric_id"]) for row in endpoint_rows)
    unique_metric_ids = tuple(sorted({row["metric_id"] for row in endpoint_rows}))
    gates = {
        "fifteen_registered_task_contracts": len(tasks) == 15,
        "task_ids_match_frozen_design_matrix": tuple(sorted(task_ids)) == matrix_task_ids,
        "all_twenty_eight_operations_reachable": (
            len(registered_operations) == 28
            and set(registered_operations) == set(live_task_operation_union)
            and set(registered_operations) == set(operation_registry)
        ),
        "all_five_instruments_reachable": (
            len(registered_instruments) == 5
            and set(registered_instruments) == set(live_task_instrument_union)
            and set(registered_instruments) == set(instrument_registry)
        ),
        "sixty_two_task_metric_bindings": len(endpoint_rows) == 62,
        "all_task_metric_bindings_executable": all(
            row["implementation_status"] == "executable" for row in endpoint_rows
        ),
        "endpoint_keys_not_duplicated": len(endpoint_keys) == len(set(endpoint_keys)),
        "frozen_matrix_counts_agree": (
            matrix["task_count"] == len(tasks)
            and validation["declared_success_metric_count"] == len(endpoint_rows)
            and validation["bound_success_metric_count"] == len(endpoint_rows)
        ),
        "all_tasks_have_midpoint_and_boundary_execution": (
            validation["executable_midpoint_task_count"] == len(tasks)
            and validation["executable_boundary_task_count"] == len(tasks)
        ),
        "no_dead_coordinates_or_formalization_blockers": (
            validation["dead_recipe_coordinate_count"] == 0
            and validation["formalization_blocker_count"] == 0
        ),
    }
    core: dict[str, Any] = {
        "schema_version": "chemworld-work-i-platform-surface-audit-0.1",
        "source_bindings": {
            "task_registry": "chemworld.tasks.list_tasks",
            "operation_registry": "chemworld.world.operations.OPERATION_TYPES",
            "instrument_registry": "chemworld.world.operations.INSTRUMENTS",
            "endpoint_registry": "chemworld.eval.task_metric_endpoints",
            "frozen_task_design_matrix_path": MATRIX.relative_to(ROOT).as_posix(),
            "frozen_task_design_matrix_file_sha256": _file_sha256(MATRIX),
            "frozen_task_design_matrix_schema_version": matrix["schema_version"],
        },
        "display_counts": {
            "registered_task_contracts": len(tasks),
            "typed_operation_kinds": len(registered_operations),
            "instrument_contracts": len(registered_instruments),
            "task_specific_evaluator_endpoint_bindings": len(endpoint_rows),
            "complete_experiment_boundary_cases": validation["boundary_recipe_case_count"],
        },
        "counting_rules": {
            "tasks": "one entry in the live TASK_REGISTRY; aliases are not counted",
            "operations": (
                "one globally typed OPERATION_TYPES entry, counted once even when exposed by "
                "multiple tasks"
            ),
            "instruments": (
                "one public INSTRUMENTS contract, counted once even when exposed by multiple tasks"
            ),
            "endpoints": (
                "one ordered (task_id, success_metric_id) evaluator binding; repeated metric "
                "names in different task contracts are distinct bindings"
            ),
            "boundary_cases": (
                "one executed complete-experiment boundary recipe in the frozen design matrix; "
                "these are qualification executions, not additional tasks or agent trials"
            ),
        },
        "task_rows": task_rows,
        "operation_rows": [
            {
                "operation_id": operation,
                "contract_kind": operation_registry[operation].kind,
                "reachable_task_ids": sorted(operation_tasks[operation]),
            }
            for operation in registered_operations
        ],
        "instrument_rows": [
            {
                "instrument_id": instrument,
                "contract_sha256": _sha256(instrument_registry[instrument].to_dict()),
                "reachable_task_ids": sorted(instrument_tasks[instrument]),
            }
            for instrument in registered_instruments
        ],
        "endpoint_rows": endpoint_rows,
        "diagnostics": {
            "unique_metric_id_count": len(unique_metric_ids),
            "unique_metric_ids": list(unique_metric_ids),
            "dead_recipe_coordinate_count": validation["dead_recipe_coordinate_count"],
            "formalization_blocker_count": validation["formalization_blocker_count"],
            "executable_midpoint_task_count": validation["executable_midpoint_task_count"],
            "executable_boundary_task_count": validation["executable_boundary_task_count"],
        },
        "gates": gates,
        "passed": all(gates.values()),
        "approved_display_wording": (
            "ChemWorld exposes 15 registered task contracts spanning all 28 typed operation "
            "kinds and five instrument contracts; qualification executed 415 complete-"
            "experiment boundary recipes and bound all 62 task-specific metric endpoints to "
            "executable evaluators."
        ),
        "claim_boundary": {
            "registered_and_qualified_platform_surface": True,
            "all_registered_tasks_empirically_compared_with_agents": False,
            "sixty_two_unique_metric_definitions": False,
            "physical_laboratory_validation": False,
        },
    }
    digest = _sha256(core)
    return {
        **core,
        "audit_id": f"chemworld-work-i-platform-surface-{digest[:16]}",
        "audit_sha256": digest,
    }


def build_markdown(audit: dict[str, Any]) -> str:
    counts = audit["display_counts"]
    unique_metric_count = audit["diagnostics"]["unique_metric_id_count"]
    return "\n".join(
        [
            "# Work I Platform Surface Audit",
            "",
            f"Audit: `{audit['audit_id']}`  ",
            f"SHA-256: `{audit['audit_sha256']}`",
            "",
            "## Approved display statement",
            "",
            audit["approved_display_wording"],
            "",
            "## Exact count meanings",
            "",
            "| Display number | Meaning | Qualification |",
            "| ---: | --- | --- |",
            (
                f"| {counts['registered_task_contracts']} | live registered task contracts | "
                "all have executable midpoint and boundary recipes |"
            ),
            (
                f"| {counts['typed_operation_kinds']} | globally unique typed operation kinds | "
                "every kind is reachable from at least one registered task |"
            ),
            (
                f"| {counts['instrument_contracts']} | globally unique public instrument "
                "contracts | every instrument is reachable from at least one task |"
            ),
            (
                f"| {counts['task_specific_evaluator_endpoint_bindings']} | ordered task-metric "
                "evaluator bindings | all bindings resolve to executable evaluators |"
            ),
            (
                f"| {counts['complete_experiment_boundary_cases']} | executed boundary recipes | "
                "qualification executions, not tasks or agent trials |"
            ),
            "",
            "The 62 endpoint count is deliberately task-specific. The same metric name in two "
            "task contracts contributes two evaluator bindings; it does not imply 62 unique "
            f"metric definitions (the live registry contains {unique_metric_count} "
            "unique metric identifiers).",
            "",
            "## Publication boundary",
            "",
            "These numbers describe the registered and executable platform surface. They do not "
            "claim that autonomous agents were empirically compared on all 15 tasks, and they do "
            "not constitute physical-laboratory validation.",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_audit()
    json_text = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    markdown_text = build_markdown(audit)
    if args.check:
        if args.json_output.read_text(encoding="utf-8") != json_text:
            raise SystemExit("machine platform audit does not match deterministic rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("human platform audit does not match deterministic rebuild")
    else:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json_text, encoding="utf-8")
        args.markdown_output.write_text(markdown_text, encoding="utf-8")
    print(
        json.dumps(
            {
                **audit["display_counts"],
                "audit_sha256": audit["audit_sha256"],
                "passed": audit["passed"],
            },
            sort_keys=True,
        )
    )
    return 0 if audit["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
