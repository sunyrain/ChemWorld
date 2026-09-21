from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import scripts.export_work_ii_eq_bounded_equilibrium_reports_v2_2 as export


def _raw_step() -> dict[str, object]:
    return {
        "step": 7,
        "experiment_index": 2,
        "action": {"operation": "measure", "instrument": "pH_meter"},
        "explanation": {
            "decision_context": {
                "decision_stage": "measurement",
                "visible_metrics": {"score": 0.0},
            },
            "decision_audit": {
                "diagnostic_target": "acid-base state",
                "status": "provided",
            },
        },
        "agent_visible_observation": {
            "observation": {"pH_normalized": 0.42},
            "observed_keys": ["pH_normalized"],
        },
        "transaction_status": "committed",
        "rollback_reason": None,
    }


def test_public_agent_io_step_preserves_complete_visible_exchange() -> None:
    payload = export.public_agent_io_step("EQ-W01--Opaque", _raw_step())

    assert payload["step"] == 7
    assert payload["agent_input"]["decision_stage"] == "measurement"
    assert payload["agent_output"]["action"]["instrument"] == "pH_meter"
    assert payload["agent_output"]["decision_audit"]["status"] == "provided"
    assert payload["environment_output"]["observation"]["pH_normalized"] == 0.42
    assert payload["transaction"] == {"status": "committed", "rollback_reason": None}


def test_public_agent_io_step_rejects_private_nested_keys() -> None:
    raw = _raw_step()
    raw["agent_visible_observation"] = {"provider_token": "must-not-export"}

    with pytest.raises(RuntimeError, match="private field reached public export"):
        export.public_agent_io_step("EQ-W01--Opaque", raw)


def test_write_jsonl_is_one_record_per_operation(tmp_path: Path) -> None:
    path = tmp_path / "trajectory.jsonl"
    rows = [export.public_agent_io_step("EQ-W01--Opaque", _raw_step())]

    export._write_jsonl(path, rows)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == rows[0]


def test_effective_source_trajectory_follows_posttest_recovery_provenance(
    tmp_path: Path, monkeypatch: Any
) -> None:
    cell_id = "EQ-W01--Opaque"
    result_path = tmp_path / "recoveries" / cell_id / "attempt-04" / "RESULT.json"
    source_folder = (
        tmp_path
        / "recoveries"
        / cell_id
        / "attempt-03"
        / "execution"
        / "sources"
        / cell_id
    )
    source_folder.mkdir(parents=True)
    result_path.parent.mkdir(parents=True)
    (result_path.parent / "recovery.json").write_text(
        json.dumps(
            {
                "source_receipt_folder": source_folder.relative_to(tmp_path).as_posix()
            }
        ),
        encoding="utf-8",
    )
    (source_folder / "trajectory.jsonl").write_text(
        '{"step":1}\n{"step":2}\n', encoding="utf-8"
    )
    monkeypatch.setattr(export.eq.shared, "summaries", lambda records: ["batch"])

    path, records = export.effective_source_trajectory(
        tmp_path,
        cell_id,
        {"operations": 2, "batches": ["batch"]},
        result_path,
    )

    assert path == (source_folder / "trajectory.jsonl").resolve()
    assert [record["step"] for record in records] == [1, 2]
