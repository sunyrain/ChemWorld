from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

import chemworld.eval.work_ii_d1_execution as d1_execution
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_d1_execution import D1CellStore, build_d1_admission_receipt


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


def test_d1_store_claims_provider_attempt_index_atomically(tmp_path: Path) -> None:
    store, key = _store(tmp_path)
    competing_store = D1CellStore(
        store.root,
        config_path=store.config_path,
        task_id="task",
        world_seeds=[0],
        arms=["opaque", "aligned_nominal", "misindexed_nominal"],
    )

    def launch(candidate: tuple[D1CellStore, str]) -> str:
        candidate_store, attempt_id = candidate
        try:
            candidate_store.record_provider_attempt_launch(key, attempt_id=attempt_id)
        except ValueError as error:
            return str(error)
        return "launched"

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(
            pool.map(launch, [(store, "candidate-a"), (competing_store, "candidate-b")])
        )

    assert outcomes.count("launched") == 1
    assert sum("already claimed" in outcome for outcome in outcomes) == 1
    assert store.audit()["provider_attempt_count"] == 1


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


def _hashed(payload: dict[str, object]) -> dict[str, object]:
    payload["report_sha256"] = canonical_json_sha256(payload)
    return payload


def _admission_fixture(
    tmp_path: Path,
) -> tuple[Path, Path, Path, list[Path], Path]:
    config_path = tmp_path / "config.json"
    write_json_atomic(config_path, {"task_id": "task"})
    participant_root = tmp_path / "participant"
    terminal_root = participant_root / "terminal"
    terminal_root.mkdir(parents=True)
    terminal_bindings = []
    blind_paths = []
    blind_keys = []
    for index, arm in enumerate(("opaque", "aligned_nominal", "misindexed_nominal")):
        terminal_path = terminal_root / f"{arm}.json"
        terminal = {
            "receipt_sha256": str(index) * 64,
            "cell": {"task_id": "task", "world_seed": 2, "prior_arm": arm},
        }
        write_json_atomic(terminal_path, terminal)
        terminal_bindings.append(
            {
                "path": terminal_path.relative_to(participant_root).as_posix(),
                "sha256": file_sha256(terminal_path),
                "receipt_sha256": terminal["receipt_sha256"],
            }
        )
        cell_key = f"cell-{index}"
        blind_keys.append(cell_key)
        blind_root = tmp_path / "blind" / str(index)
        blind_root.mkdir(parents=True)
        plan = {
            "task_id": "task",
            "world_seed": 2,
            "plan_sha256": "pending",
        }
        plan["plan_sha256"] = canonical_json_sha256(
            {key: value for key, value in plan.items() if key != "plan_sha256"}
        )
        write_json_atomic(blind_root / "plan.json", plan)
        blind_path = blind_root / "report.json"
        write_json_atomic(
            blind_path,
            _hashed(
                {
                    "cell_key_sha256": cell_key,
                    "plan_sha256": plan["plan_sha256"],
                    "status": "completed",
                }
            ),
        )
        blind_paths.append(blind_path)
    matrix_path = participant_root / "matrix_report.json"
    write_json_atomic(
        matrix_path,
        {"world_seeds": [2], "terminal_receipt_bindings": terminal_bindings},
    )
    truth_path = tmp_path / "truth.json"
    truth = _hashed({"status": "completed", "task_id": "task"})
    write_json_atomic(truth_path, truth)
    evaluation_path = tmp_path / "evaluation.json"
    evaluation = {
        "status": "passed",
        "participant_run": {"matrix_report_sha256": file_sha256(matrix_path)},
        "truth_report_sha256": truth["report_sha256"],
        "cells": [
            {
                "cell_key_sha256": key,
                "blind_evaluation_status": "completed",
            }
            for key in blind_keys
        ],
        "action_layer": {
            "status": "participant_interpretable",
            "submitted_recommendations_replaced": False,
        },
    }
    write_json_atomic(evaluation_path, _hashed(evaluation))
    return config_path, participant_root, truth_path, blind_paths, evaluation_path


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "execution_mode",
            "development",
            "D1 evaluation development report cannot support terminal admission",
        ),
        (
            "release_eligible",
            False,
            "D1 evaluation non-release report cannot support terminal admission",
        ),
    ],
)
def test_d1_admission_rejects_development_or_nonrelease_evaluation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    config, participant, truth, blind, evaluation = _admission_fixture(tmp_path)
    payload = json.loads(evaluation.read_text(encoding="utf-8"))
    payload[field] = value
    payload["report_sha256"] = canonical_json_sha256(
        {key: item for key, item in payload.items() if key != "report_sha256"}
    )
    write_json_atomic(evaluation, payload)
    monkeypatch.setattr(
        d1_execution,
        "validate_d1_qualification_evidence",
        lambda _root, _config: [],
    )

    receipt = build_d1_admission_receipt(
        tmp_path,
        config_path=config,
        participant_root=participant,
        truth_report_path=truth,
        blind_report_paths=blind,
        evaluation_report_path=evaluation,
    )

    assert receipt["status"] == "failed_retained"
    assert message in receipt["validation_errors"]
