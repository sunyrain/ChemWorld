from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_d1_execution import D1CellStore


def _store(tmp_path: Path) -> tuple[D1CellStore, str]:
    config = tmp_path / "config.json"
    write_json_atomic(config, {"task_id": "task"})
    store = D1CellStore(
        tmp_path / "output/store",
        config_path=config,
        task_id="task",
        world_seeds=[0],
        arms=["opaque", "aligned_nominal", "misindexed_nominal"],
    )
    return store, store.key(0, "opaque")


def _log(store: D1CellStore, name: str) -> Path:
    path = store.output_root / "logs" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("missing infrastructure\n", encoding="utf-8")
    return path


def test_d1_store_allows_only_one_missing_infrastructure_resume(tmp_path: Path) -> None:
    store, key = _store(tmp_path)
    store.record_provider_attempt_launch(key, attempt_id="first")
    store.record_infrastructure_failure(
        key,
        attempt_id="first",
        error_type="OSError",
        error_message="provider unavailable",
        reason_code="provider_process_launch_failed",
        committed_operation_count=0,
        log_path=_log(store, "first.log"),
    )
    assert any(row["cell_key_sha256"] == key for row in store.pending(resume=True))
    store.record_provider_attempt_launch(key, attempt_id="second")
    store.record_infrastructure_failure(
        key,
        attempt_id="second",
        error_type="OSError",
        error_message="provider unavailable",
        reason_code="provider_process_launch_failed",
        committed_operation_count=0,
        log_path=_log(store, "second.log"),
    )

    with pytest.raises(ValueError, match="attempt cap=2"):
        store.pending(resume=True)


def test_d1_store_rejects_non_infrastructure_resume_and_committed_infra(
    tmp_path: Path,
) -> None:
    store, key = _store(tmp_path)
    store.record_provider_attempt_launch(key, attempt_id="first")
    with pytest.raises(ValueError, match="not eligible"):
        store.pending(resume=True)
    with pytest.raises(ValueError, match="committed operation"):
        store.record_infrastructure_failure(
            key,
            attempt_id="first",
            error_type="OSError",
            error_message="late failure",
            reason_code="provider_process_launch_failed",
            committed_operation_count=1,
            log_path=_log(store, "late.log"),
        )


def test_d1_store_terminal_is_write_once_and_tamper_is_detected(tmp_path: Path) -> None:
    store, key = _store(tmp_path)
    store.record_provider_attempt_launch(key, attempt_id="first")
    attempt = store.output_root / "attempt"
    attempt.mkdir()
    write_json_atomic(attempt / "summary.json", {"completed": True})
    write_json_atomic(attempt / "report.json", {"results": []})
    (attempt / "trajectory.jsonl").write_text(
        json.dumps({"transaction_status": "committed"}) + "\n",
        encoding="utf-8",
    )
    store.write_terminal(
        key,
        attempt_id="first",
        state="completed",
        result_root=attempt,
        committed_operation_count=1,
    )
    with pytest.raises(FileExistsError, match="terminal view"):
        store.write_terminal(
            key,
            attempt_id="first",
            state="completed",
            result_root=attempt,
            committed_operation_count=1,
        )
    receipt_path = store.terminals / f"{key}.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["cell"]["prior_arm"] = "tampered"
    write_json_atomic(receipt_path, receipt)
    assert store.audit()["invalid_receipts"] == [receipt_path.as_posix()]
