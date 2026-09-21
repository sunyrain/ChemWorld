from __future__ import annotations

import json
from pathlib import Path

import scripts.recover_work_ii_eq_structural_v0_3 as recover


def test_latest_result_prefers_latest_recovery(tmp_path: Path) -> None:
    cell = "EQ-S-W02--Aligned"
    source = tmp_path / "sources" / cell
    source.mkdir(parents=True)
    (source / "RESULT.json").write_text(json.dumps({"status": "retained_nonconforming"}))
    attempt = tmp_path / "recoveries" / cell / "attempt-01"
    attempt.mkdir(parents=True)
    (attempt / "RESULT.json").write_text(json.dumps({"status": "completed"}))

    result, path = recover._latest_result(tmp_path, cell)

    assert result["status"] == "completed"
    assert path == attempt / "RESULT.json"
