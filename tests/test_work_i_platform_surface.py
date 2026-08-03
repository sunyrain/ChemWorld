from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_work_i_platform_surface import build_audit, build_markdown

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json"
HUMAN = ROOT / "workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.md"


def test_platform_surface_reports_rebuild_from_live_registries() -> None:
    rebuilt = build_audit()
    committed = json.loads(MACHINE.read_text(encoding="utf-8"))
    assert committed == rebuilt
    assert HUMAN.read_text(encoding="utf-8") == build_markdown(rebuilt)


def test_platform_display_counts_have_exact_scoped_meanings() -> None:
    audit = json.loads(MACHINE.read_text(encoding="utf-8"))
    assert audit["display_counts"] == {
        "complete_experiment_boundary_cases": 415,
        "instrument_contracts": 5,
        "registered_task_contracts": 15,
        "task_specific_evaluator_endpoint_bindings": 62,
        "typed_operation_kinds": 28,
    }
    assert len(audit["task_rows"]) == 15
    assert len(audit["operation_rows"]) == 28
    assert len(audit["instrument_rows"]) == 5
    assert len(audit["endpoint_rows"]) == 62
    assert all(audit["gates"].values())
    assert audit["passed"] is True
    assert audit["claim_boundary"]["all_registered_tasks_empirically_compared_with_agents"] is False
    assert audit["claim_boundary"]["sixty_two_unique_metric_definitions"] is False
