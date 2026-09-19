import json
from pathlib import Path

import scripts.parallel_recover_work_ii_rx_ps_five_world_dual_goal as parallel


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_resolve_result_prefers_latest_repair(tmp_path: Path) -> None:
    cell = "cell-a"
    dump(
        tmp_path / "sources" / cell / "result.json",
        {"cell_id": cell, "status": "retained_nonconforming"},
    )
    dump(
        tmp_path / "sources" / cell / "posttest-repair-v10" / "effective-result.json",
        {"cell_id": cell, "status": "completed", "posttest_chain_sealed": True},
    )

    path, result = parallel.resolve_result(tmp_path, cell)

    assert path.name == "effective-result.json"
    assert "posttest-repair-v10" in str(path)
    assert result["status"] == "completed"


def test_classify_schedule_allows_only_task_26_repair(tmp_path: Path) -> None:
    complete_cell = "cell-complete"
    dump(
        tmp_path / "sources" / complete_cell / "result.json",
        {
            "cell_id": complete_cell,
            "status": "completed",
            "posttest_chain_sealed": True,
        },
    )
    dump(
        tmp_path / "sources" / next(iter(parallel.POSTTEST_REPAIRS)) / "result.json",
        {
            "cell_id": next(iter(parallel.POSTTEST_REPAIRS)),
            "status": "retained_nonconforming",
            "source_status": "completed",
            "posttest_chain_sealed": False,
        },
    )
    schedule = [
        {"cell_id": complete_cell},
        {"cell_id": next(iter(parallel.POSTTEST_REPAIRS))},
        {"cell_id": "cell-new"},
    ]

    complete, pending = parallel.classify_schedule(tmp_path, schedule)

    assert [row["cell_id"] for row in complete] == [complete_cell]
    assert [row["cell_id"] for row in pending] == [
        next(iter(parallel.POSTTEST_REPAIRS)),
        "cell-new",
    ]


def test_preaction_partial_requires_only_retained_v7_metadata(tmp_path: Path) -> None:
    folder = tmp_path / "sources" / "cell-a"
    dump(folder / "attempt.json", {})
    dump(folder / "public-prior-binding.json", {})

    assert parallel.is_preaction_partial(folder) is True

    dump(folder / "trajectory.jsonl", {})
    assert parallel.is_preaction_partial(folder) is False


def test_v8_zero_action_provider_failure_is_repairable(tmp_path: Path) -> None:
    folder = tmp_path / "sources" / "cell-a"
    dump(folder / "attempt.json", {})
    dump(folder / "public-prior-binding.json", {})
    dump(
        folder / "source-repair-v8" / "effective-result.json",
        {
            "status": "retained_nonconforming",
            "source_status": "failed",
            "operations": 0,
            "batches": [],
            "posttest_chain_sealed": False,
        },
    )

    kind, paths = parallel.source_repair_provenance(folder)

    assert kind == "v8_old_account_provider_failure"
    assert paths[-1].name == "effective-result.json"
