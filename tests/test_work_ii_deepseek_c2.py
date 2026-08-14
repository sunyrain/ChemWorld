from __future__ import annotations

import json
from pathlib import Path

import scripts.run_work_ii_deepseek_c2 as runner


def _summary(
    cell_id: str,
    *,
    completed: bool = False,
    experiments: int = 0,
    operations: int = 0,
    committed: int = 0,
    provider_errors: int = 0,
) -> dict[str, object]:
    return {
        "prospective_formal_result": True,
        "prospective_cohort_cell": {"cell_id": cell_id},
        "completed": completed,
        "failure": None if completed else {"type": "retained"},
        "analysis": {
            "complete_experiment_count": experiments,
            "operation_attempt_count": operations,
            "committed_operation_count": committed,
        },
        "method_resources": {"provider_error_event_count": provider_errors},
        "provider_receipts": [
            {
                "provider_error_event_count": provider_errors,
                "provider_errors": (
                    [{"category": "quota_or_balance", "http_status_codes": [402]}]
                    if provider_errors
                    else []
                ),
            }
        ],
    }


def _write_cell(root: Path, cell_id: str, summary: dict[str, object]) -> None:
    cell_root = root / "cells" / cell_id
    cell_root.mkdir(parents=True)
    (cell_root / "summary.json").write_text(
        json.dumps(summary), encoding="utf-8"
    )


def test_only_zero_operation_provider_failures_are_resumable() -> None:
    zero_operation = _summary("zero", provider_errors=7)
    scientific_trajectory = _summary(
        "scientific",
        experiments=1,
        operations=4,
        committed=4,
        provider_errors=1,
    )
    participant_failure = _summary("participant")

    assert runner._is_zero_operation_provider_failure(zero_operation) is True
    assert runner._is_reusable_terminal_summary(zero_operation) is False
    assert runner._is_zero_operation_provider_failure(scientific_trajectory) is False
    assert runner._is_reusable_terminal_summary(scientific_trajectory) is True
    assert runner._is_zero_operation_provider_failure(participant_failure) is False
    assert runner._is_reusable_terminal_summary(participant_failure) is True


def test_archive_preserves_failed_attempt_and_companion_logs(tmp_path: Path) -> None:
    cell_id = "A_P--reaction-safety-constrained--seed1--opaque"
    _write_cell(tmp_path, cell_id, _summary(cell_id, provider_errors=7))
    log = tmp_path / "logs" / f"{cell_id}.log"
    progress = tmp_path / "cell_progress" / f"{cell_id}.jsonl"
    log.parent.mkdir()
    progress.parent.mkdir()
    log.write_text("402\n", encoding="utf-8")
    progress.write_text('{"event":"cell_completed"}\n', encoding="utf-8")

    attempt = runner._archive_recoverable_attempt(tmp_path, cell_id)

    assert attempt == tmp_path / "cell_attempts" / cell_id / "attempt-0001"
    assert not (tmp_path / "cells" / cell_id).exists()
    assert json.loads((attempt / "summary.json").read_text(encoding="utf-8"))[
        "analysis"
    ]["operation_attempt_count"] == 0
    assert (attempt / "runner.log").read_text(encoding="utf-8") == "402\n"
    assert (attempt / "progress.jsonl").is_file()


def test_root_summary_separates_attempt_terminal_from_cohort_terminal(
    tmp_path: Path,
) -> None:
    triplet = {
        "block": "A_P",
        "task_id": "reaction-safety-constrained",
        "world_seed": 1,
        "rounds": 10,
    }
    opaque = runner._cell_id("A_P", triplet["task_id"], 1, "opaque")
    aligned = runner._cell_id("A_P", triplet["task_id"], 1, "aligned_nominal")
    misindexed = runner._cell_id(
        "A_P", triplet["task_id"], 1, "misindexed_nominal"
    )
    _write_cell(
        tmp_path,
        opaque,
        _summary(
            opaque, completed=True, experiments=10, operations=40, committed=40
        ),
    )
    _write_cell(
        tmp_path,
        aligned,
        _summary(aligned, experiments=9, operations=36, committed=36),
    )
    _write_cell(
        tmp_path,
        misindexed,
        _summary(misindexed, provider_errors=7),
    )

    report = runner._write_summary({}, [triplet], tmp_path)

    assert report["attempt_terminal_sessions"] == 3
    assert report["terminal_sessions"] == 2
    assert report["completed_sessions"] == 1
    assert report["retained_noncompleted_sessions"] == 1
    assert report["missing_sessions"] == 1
    assert report["recoverable_infrastructure_sessions"] == 1
    assert report["prospective_formal_result"] is False
