from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_work_ii_ap_development_results.py"
SPEC = importlib.util.spec_from_file_location("build_work_ii_ap_development_results", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_build_summary_from_retained_terminal_runs() -> None:
    roots = tuple(ROOT / path for path in MODULE.DEFAULT_RUN_ROOTS)
    summary = MODULE.build_summary(roots)

    assert summary["status"] == "terminal_platform_requalification_required"
    assert summary["development_only"] is True
    assert summary["formal_result"] is False
    assert summary["aggregate"] == {
        "active_cells_with_exact_replay": 10,
        "attempted_operations": 725,
        "blocks_terminal": 4,
        "blocks_total": 4,
        "cells_reaching_10_experiments": 9,
        "cells_terminal": 12,
        "cells_total": 12,
        "cells_with_committed_operations": 10,
        "committed_operations": 723,
        "infrastructure_failure_cells": 2,
        "observed_complete_experiments": 99,
        "planned_complete_experiments": 120,
        "provider_error_events": 0,
        "qualification_completed_cells": 4,
        "right_censored_cells": 6,
        "store_invalid_receipts": 0,
        "store_missing_cells": 0,
    }

    markdown = MODULE.render_markdown(summary)
    assert "Terminal therefore does not mean passed" in markdown
    assert "not support a scientific provider/model/arm comparison" in markdown
    assert "missing-infrastructure-only retry" in markdown


def _terminal_result(arm: str) -> dict[str, object]:
    return {
        "arm": arm,
        "completed": True,
        "failure": None,
        "analysis": {
            "complete_experiment_count": 10,
            "committed_operation_count": 10,
            "operation_attempt_count": 10,
            "belief_snapshots": [{}, {}, {}, {}, {}],
            "final_recommendation": {"selected_candidate": "candidate-1"},
        },
        "method_resources": {
            "provider_error_event_count": 0,
            "recovered_mcp_tool_failure_count": 0,
            "maximum_consecutive_mcp_tool_failure_count": 0,
            "input_token_count": 100,
            "uncached_input_token_count": 50,
            "output_token_count": 20,
            "mcp_tool_failure_taxonomy": {
                "counts_by_category": {
                    "provider_network": 0,
                    "transport_ipc_os": 0,
                    "agent_invalid": 0,
                    "unclassified": 0,
                }
            },
        },
        "qualification": {"failed_checks": []},
        "exact_replay": {"verified": True},
    }


def test_build_platform_requalification_summary(tmp_path: Path) -> None:
    source_commit = "f" * 40
    coverage = [
        ("deepseek", "reaction-safety-constrained"),
        ("deepseek", "electrochemical-conversion"),
        ("wellau", "reaction-safety-constrained"),
        ("wellau", "electrochemical-conversion"),
    ]
    roots: list[Path] = []
    for index, (provider_id, task_id) in enumerate(coverage):
        root = tmp_path / f"block-{index}"
        root.mkdir()
        report = {
            "source_commit": source_commit,
            "provider_id": provider_id,
            "model": f"{provider_id}-model",
            "task_id": task_id,
            "world_seeds": [2],
            "terminal_cell_count": 3,
            "expected_cell_count": 3,
            "completed_cell_count": 3,
            "all_cells_terminal": True,
            "store_audit": {
                "missing_cell_key_sha256": [],
                "invalid_receipts": [],
            },
            "seed_reports": [
                {
                    "results": [
                        _terminal_result("aligned_nominal"),
                        _terminal_result("misindexed_nominal"),
                        _terminal_result("opaque"),
                    ]
                }
            ],
        }
        (root / "matrix_report.json").write_text(
            json.dumps(report),
            encoding="utf-8",
        )
        roots.append(root)

    summary = MODULE.build_summary(
        tuple(roots),
        mode=MODULE.PLATFORM_REQUALIFICATION_MODE,
        expected_source_commit=source_commit,
    )

    assert summary["status"] == "terminal_platform_requalification_complete"
    assert summary["platform_requalification"] == {"passed": True, "failed_checks": []}
    assert summary["aggregate"]["typed_mcp_failure_taxonomy_cells"] == 12
    assert summary["aggregate"]["mcp_tool_failures_by_category"] == {
        "provider_network": 0,
        "transport_ipc_os": 0,
        "agent_invalid": 0,
        "unclassified": 0,
    }
    markdown = MODULE.render_markdown(summary)
    assert "platform requalification complete" in markdown
    assert "Typed MCP failure accounting is complete for `12/12` cells" in markdown


def test_platform_requalification_fails_closed_on_replay_or_unclassified_event(
    tmp_path: Path,
) -> None:
    source_commit = "f" * 40
    coverage = [
        ("deepseek", "reaction-safety-constrained"),
        ("deepseek", "electrochemical-conversion"),
        ("wellau", "reaction-safety-constrained"),
        ("wellau", "electrochemical-conversion"),
    ]
    roots: list[Path] = []
    for index, (provider_id, task_id) in enumerate(coverage):
        root = tmp_path / f"block-{index}"
        root.mkdir()
        report = {
            "source_commit": source_commit,
            "provider_id": provider_id,
            "model": f"{provider_id}-model",
            "task_id": task_id,
            "world_seeds": [2],
            "terminal_cell_count": 3,
            "expected_cell_count": 3,
            "completed_cell_count": 3,
            "all_cells_terminal": True,
            "store_audit": {
                "missing_cell_key_sha256": [],
                "invalid_receipts": [],
            },
            "seed_reports": [
                {
                    "results": [
                        _terminal_result("aligned_nominal"),
                        _terminal_result("misindexed_nominal"),
                        _terminal_result("opaque"),
                    ]
                }
            ],
        }
        (root / "matrix_report.json").write_text(json.dumps(report), encoding="utf-8")
        roots.append(root)

    first_report_path = roots[0] / "matrix_report.json"
    first_report = json.loads(first_report_path.read_text(encoding="utf-8"))
    first_report["seed_reports"][0]["results"][0]["exact_replay"]["verified"] = False
    first_report["seed_reports"][0]["results"][1]["method_resources"][
        "mcp_tool_failure_taxonomy"
    ]["counts_by_category"]["unclassified"] = 1
    first_report_path.write_text(json.dumps(first_report), encoding="utf-8")

    summary = MODULE.build_summary(
        tuple(roots),
        mode=MODULE.PLATFORM_REQUALIFICATION_MODE,
        expected_source_commit=source_commit,
    )

    assert summary["status"] == "terminal_platform_requalification_failed"
    assert summary["platform_requalification"] == {
        "passed": False,
        "failed_checks": [
            "active_cell_exact_replay_incomplete",
            "unclassified_mcp_tool_failure_present",
        ],
    }
    markdown = MODULE.render_markdown(summary)
    assert "platform requalification failed" in markdown
    assert "Frozen platform gates: fail" in markdown
