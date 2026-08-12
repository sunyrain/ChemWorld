from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import file_sha256
from chemworld.eval.work_ii_crystallization_reversible_q0 import (
    PLANNED_EXECUTIONS,
    QUALIFICATION_VERSION,
    SUMMARY_VERSION,
    TASK_ID,
    TASK_REPORT_VERSION,
    self_hash,
    validate_summary,
    validate_task_report,
)
from chemworld.eval.work_ii_static_topology_q0 import LAW_IDS, analyze_task, registered_cells


def _rows() -> list[dict[str, Any]]:
    rows = []
    for cell in registered_cells(TASK_ID):
        for law_id in LAW_IDS:
            gap = 0.0 if law_id == "baseline" else 0.08 + 0.07 * int(cell["time_index"])
            metrics = {"yield": 0.75 - gap, "conversion": 0.72 - gap, "selectivity": 0.70 - gap}
            rows.append(
                {
                    **cell,
                    "task_id": TASK_ID,
                    "law_id": law_id,
                    "status": "completed",
                    "safe": True,
                    "exact_replay": True,
                    "action_plan_sha256": f"action-{cell['cell_id']}",
                    "direct_noise_key_sha256": f"noise-{cell['cell_id']}",
                    "direct_metrics": metrics,
                    "direct_observed_mask": dict.fromkeys(metrics, True),
                    "participant_visible_payload": {"metrics": metrics},
                }
            )
    return rows


def _audit() -> dict[str, Any]:
    return {
        "added_reaction_count": 1,
        "mechanism_hash_changed": True,
        "reversible_hash_deterministic": True,
        "execution_mechanism_binding_matches": True,
    }


def _source_binding() -> dict[str, Any]:
    return {
        "schema_version": "chemworld-work-ii-c2-source-binding-0.1",
        "tested_commit": "a" * 40,
        "material_tree": {
            "relative_roots": [],
            "excluded_relative_paths": [],
            "sha256": "b" * 64,
        },
    }


def test_task_report_is_rebuilt_and_tamper_evident() -> None:
    rows = _rows()
    report = {
        "schema_version": TASK_REPORT_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "task_id": TASK_ID,
        "world_seed": 0,
        "c2_source_binding": _source_binding(),
        "mechanism_audit": _audit(),
        "rows": rows,
        "analysis": analyze_task(TASK_ID, rows, _audit()),
    }
    report["report_sha256"] = self_hash(report, "report_sha256")
    assert validate_task_report(report) == []
    altered = copy.deepcopy(report)
    altered["rows"][0]["direct_metrics"]["yield"] += 0.1
    assert validate_task_report(altered)


def test_summary_binds_raw_report_and_source(monkeypatch: Any, tmp_path: Path) -> None:
    rows = _rows()
    binding = _source_binding()
    analysis = analyze_task(TASK_ID, rows, _audit())
    report = {
        "schema_version": TASK_REPORT_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "task_id": TASK_ID,
        "world_seed": 0,
        "c2_source_binding": binding,
        "mechanism_audit": _audit(),
        "rows": rows,
        "analysis": analysis,
    }
    report["report_sha256"] = self_hash(report, "report_sha256")
    raw = tmp_path / "report.json"
    raw.write_text(json.dumps(report), encoding="utf-8")
    summary = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "task_id": TASK_ID,
        "world_seed": 0,
        "c2_source_binding": binding,
        "coverage": {
            "law_ids": list(LAW_IDS),
            "grid_cell_count": len(registered_cells(TASK_ID)),
            "planned_execution_count": PLANNED_EXECUTIONS,
        },
        "denominators": analysis["denominators"],
        "analysis": analysis,
        "five_world_expansion_authorized": True,
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "raw_binding": {
            "path": "report.json",
            "sha256": file_sha256(raw),
            "report_sha256": report["report_sha256"],
        },
    }
    summary["summary_sha256"] = self_hash(summary, "summary_sha256")
    monkeypatch.setattr(
        "chemworld.eval.work_ii_crystallization_reversible_q0.validate_c2_source_binding",
        lambda _root, observed: [] if observed == binding else ["wrong binding"],
    )
    assert validate_summary(tmp_path, summary, expected_source_binding=binding) == []
    changed = copy.deepcopy(summary)
    changed["c2_source_binding"]["tested_commit"] = "c" * 40
    changed["summary_sha256"] = self_hash(changed, "summary_sha256")
    assert validate_summary(tmp_path, changed, expected_source_binding=binding)
