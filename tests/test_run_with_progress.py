from __future__ import annotations

import json
from pathlib import Path

from scripts.run_with_progress import composition_progress, u05_progress


def test_composition_progress_reports_reference_and_generated_denominators(
    tmp_path: Path,
) -> None:
    scratch = tmp_path / "chemworld-composition-qualification-test"
    scratch.mkdir()
    for index in range(3):
        (scratch / f"reference-{index}.jsonl").write_text("{}\n", encoding="utf-8")
    progress = composition_progress(
        temp_root=tmp_path,
        started_at=0.0,
        elapsed_s=60.0,
        output=tmp_path / "report.json",
    )
    assert progress["stage"] == "reference_recipes"
    assert progress["completed"] == 3
    assert progress["denominator"] == 1786
    assert progress["rate_per_minute"] == 3.0

    for index in range(1783):
        (scratch / f"remaining-{index}.jsonl").write_text("{}\n", encoding="utf-8")
    for index in range(2):
        (scratch / f"qualification-{index}.jsonl").write_text("{}\n", encoding="utf-8")
    progress = composition_progress(
        temp_root=tmp_path,
        started_at=0.0,
        elapsed_s=120.0,
        output=tmp_path / "report.json",
    )
    assert progress["stage"] == "generated_compositions"
    assert progress["completed"] == 2
    assert progress["denominator"] == 52


def test_u05_progress_reports_mcp_actions_and_resource_state(tmp_path: Path) -> None:
    scratch = tmp_path / "chemworld-first-paper-u05-test"
    workspace = scratch / "interactive-workspace"
    session = workspace / ".ipc" / "sessions" / "experiment-0001"
    public = workspace / "public"
    session.mkdir(parents=True)
    public.mkdir(parents=True)
    (session / "mcp_tool_calls.jsonl").write_text(
        json.dumps({"tool": "material_information"})
        + "\n"
        + json.dumps({"tool": "step"})
        + "\n",
        encoding="utf-8",
    )
    (public / "history.jsonl").write_text(
        json.dumps(
            {
                "action": {"operation": "heat"},
                "transaction_status": "committed",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (public / "current.json").write_text(
        json.dumps(
            {
                "stage": "experiment_control",
                "remaining_operations": 15,
                "campaign_state": {"operation_count": 1, "done": False},
                "campaign_resources": {
                    "state": {
                        "instrument_uses": {"hplc": 1},
                        "final_assays": 0,
                        "report_only": {"process_time_s": 1800.0},
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    (scratch / "trajectory.jsonl").write_text("{}\n", encoding="utf-8")

    progress = u05_progress(
        temp_root=tmp_path,
        started_at=0.0,
        output=tmp_path / "report.json",
    )
    assert progress["stage"] == "experiment_control"
    assert progress["mcp_tool_call_count"] == 2
    assert progress["mcp_step_count"] == 1
    assert progress["submitted_action_count"] == 1
    assert progress["committed_action_count"] == 1
    assert progress["process_time_used_s"] == 1800.0
