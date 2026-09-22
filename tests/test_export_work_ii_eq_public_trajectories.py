from __future__ import annotations

import json
from pathlib import Path

import pytest
import scripts.export_work_ii_eq_public_trajectories as export


def test_effective_source_trajectory_accepts_only_matching_batches(tmp_path: Path) -> None:
    cell_id = "EQ-S-W01--Opaque"
    result_path = tmp_path / "recoveries" / cell_id / "attempt-01" / "RESULT.json"
    result_path.parent.mkdir(parents=True)
    source = tmp_path / "sources" / cell_id
    source.mkdir(parents=True)
    (result_path.parent / "trajectory.jsonl").write_text('{"step":99}\n', encoding="utf-8")
    (source / "trajectory.jsonl").write_text(
        '{"step":1}\n{"step":2}\n', encoding="utf-8"
    )

    path, rows = export.effective_source_trajectory(
        tmp_path,
        cell_id,
        {"operations": 2, "batches": [{"ordinal": 1}]},
        result_path,
        lambda records: [{"ordinal": 1}] if len(records) == 2 else [],
    )

    assert path == (source / "trajectory.jsonl").resolve()
    assert [row["step"] for row in rows] == [1, 2]


def test_effective_source_trajectory_fails_closed_on_summary_mismatch(
    tmp_path: Path,
) -> None:
    cell_id = "EQ-E-W01--Opaque"
    source = tmp_path / "sources" / cell_id
    source.mkdir(parents=True)
    path = source / "trajectory.jsonl"
    path.write_text('{"step":1}\n', encoding="utf-8")

    with pytest.raises(RuntimeError, match="no trajectory matches"):
        export.effective_source_trajectory(
            tmp_path,
            cell_id,
            {"operations": 1, "batches": [{"ordinal": 1}]},
            source / "RESULT.json",
            lambda records: [{"ordinal": 2}],
        )


def test_report_link_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "EXPERIMENT_REPORT.md"
    path.write_text("# Report\n\n## K1 — report\n", encoding="utf-8")

    export._add_report_link(path)
    export._add_report_link(path)

    text = path.read_text(encoding="utf-8")
    assert text.count("[trajectory](trajectory.jsonl)") == 1
    assert text.index("[trajectory](trajectory.jsonl)") < text.index("## K1")


def test_update_reproduction_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "REPRODUCE.md"
    path.write_text("# Reproduction\n", encoding="utf-8")

    export._update_reproduction(path, "S")
    export._update_reproduction(path, "S")

    text = path.read_text(encoding="utf-8")
    assert text.count("## Public agent-visible source trajectories") == 1
    assert "No source campaign, posttest, prediction, truth value, or score" in text


def test_adapter_rejects_unknown_locus() -> None:
    with pytest.raises(ValueError, match="unsupported EQ locus"):
        export._adapter("P")


def test_candidate_recovery_source_is_resolved(tmp_path: Path) -> None:
    cell_id = "EQ-S-W02--Aligned"
    result_path = tmp_path / "recoveries" / cell_id / "attempt-01" / "RESULT.json"
    result_path.parent.mkdir(parents=True)
    receipt = tmp_path / "receipts" / cell_id
    receipt.mkdir(parents=True)
    (result_path.parent / "recovery.json").write_text(
        json.dumps({"source_receipt_folder": receipt.relative_to(tmp_path).as_posix()}),
        encoding="utf-8",
    )

    candidates = export._candidate_trajectory_paths(tmp_path, cell_id, result_path)

    assert (receipt / "trajectory.jsonl").resolve() in candidates
