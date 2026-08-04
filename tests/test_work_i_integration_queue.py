from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.audit_work_i_integration_queue import (
    QUEUE_PATH,
    ROOT,
    IntegrationQueueError,
    validate_queue,
)


def test_committed_integration_queue_matches_frozen_todo_and_claims() -> None:
    receipt = validate_queue()
    assert receipt == {
        "status": "PASS",
        "baseline_commit": "9e93316bf1ae20b1403879424abbacd1c5dc3c8e",
        "remaining_tasks": 14,
        "active_task": "W1-M05",
        "externally_blocked_or_deferred": ["W1-D02", "W1-D06", "W1-D09"],
        "hot_file_reservations": 4,
    }


def test_queue_freezes_single_owner_order_and_dependencies() -> None:
    queue = json.loads((ROOT / QUEUE_PATH).read_text(encoding="utf-8"))
    entries = queue["entries"]
    assert all(entry["planned_owner"] == "codex-1" for entry in entries)
    assert [entry["order"] for entry in entries] == list(range(10, 141, 10))
    by_id = {entry["task_id"]: entry for entry in entries}
    assert by_id["W1-S10"]["dependencies"] == ["W1-S03", "W1-S08"]
    assert by_id["W1-P09"]["dependencies"] == ["W1-P08", "W1-S10"]
    assert by_id["W1-D09"]["dependencies"] == [
        "W1-D02",
        "W1-D06",
        "W1-D08",
        "W1-M06",
    ]


def test_tampered_owner_fails_closed(tmp_path: Path) -> None:
    queue = json.loads((ROOT / QUEUE_PATH).read_text(encoding="utf-8"))
    tampered = deepcopy(queue)
    tampered["entries"][0]["planned_owner"] = "someone-else"
    path = tmp_path / "queue.json"
    path.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(IntegrationQueueError, match="planned owner mismatch"):
        validate_queue(queue_path=path)
