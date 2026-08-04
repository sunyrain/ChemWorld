"""Validate the frozen Work I integration queue without executing experiments."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = Path(
    "workstreams/arxiv_v1/integration/work-i-integration-queue-v0.1.json"
)
TODO_PATH = Path("workstreams/arxiv_v1/WORK_I_TODOLIST.md")
TERMINAL_STATUSES = {"DONE", "RELEASED", "CANCELLED"}
TABLE_ROW = re.compile(r"^\| (W1-[A-Z]\d{2}) \| P\d \| ([A-Z_]+) \|")
CLAIM_FIELD = re.compile(r"^(task_id|status|owner|branch):\s*[\"']?([^\"']+?)[\"']?\s*$", re.M)


class IntegrationQueueError(RuntimeError):
    """Raised when the queue is not a faithful, fail-closed staging snapshot."""


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        raise IntegrationQueueError(result.stderr.strip() or "git command failed")
    return result.stdout


def _commit_exists(root: Path, commit: str) -> None:
    _git(root, "cat-file", "-e", f"{commit}^{{commit}}")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrationQueueError(f"cannot read queue: {path}") from exc
    if not isinstance(payload, dict):
        raise IntegrationQueueError("queue root must be an object")
    return payload


def _snapshot_text(root: Path, baseline: str, path: str) -> str:
    return _git(root, "show", f"{baseline}:{path}")


def _todo_statuses(text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in text.splitlines():
        match = TABLE_ROW.match(line)
        if match:
            task_id, status = match.groups()
            if task_id in statuses:
                raise IntegrationQueueError(f"duplicate TODO row: {task_id}")
            statuses[task_id] = status
    if not statuses:
        raise IntegrationQueueError("no Work I task rows found at baseline")
    return statuses


def _claim_fields(text: str) -> dict[str, str]:
    return {key: value.strip() for key, value in CLAIM_FIELD.findall(text)}


def validate_queue(root: Path = ROOT, queue_path: Path = QUEUE_PATH) -> dict[str, Any]:
    """Return a compact validation receipt or fail closed."""

    queue = _read_json(root / queue_path)
    if queue.get("schema_version") != "work-i.integration-queue.v0.1":
        raise IntegrationQueueError("unsupported schema_version")
    if queue.get("coordinator") != "codex-1" or queue.get("concurrency_limit") != 1:
        raise IntegrationQueueError("single-coordinator contract is not frozen")

    baseline = queue.get("baseline_commit")
    if not isinstance(baseline, str) or not re.fullmatch(r"[0-9a-f]{40}", baseline):
        raise IntegrationQueueError("baseline_commit must be a full SHA-1")
    _commit_exists(root, baseline)

    todo = _todo_statuses(_snapshot_text(root, baseline, TODO_PATH.as_posix()))
    expected = {task_id for task_id, status in todo.items() if status not in TERMINAL_STATUSES}
    raw_entries = queue.get("entries")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise IntegrationQueueError("entries must be a non-empty list")
    entries: list[dict[str, Any]] = []
    task_ids: list[str] = []
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict):
            raise IntegrationQueueError("entries must be objects")
        task_id = raw_entry.get("task_id")
        if not isinstance(task_id, str):
            raise IntegrationQueueError("every entry needs a string task_id")
        entries.append(raw_entry)
        task_ids.append(task_id)
    if len(set(task_ids)) != len(task_ids):
        raise IntegrationQueueError("entries must have unique task_id values")
    if set(task_ids) != expected:
        raise IntegrationQueueError(
            f"queue/TODO remaining-task mismatch: queue={sorted(task_ids)} todo={sorted(expected)}"
        )

    orders: list[int] = []
    for entry in entries:
        order = entry.get("order")
        if not isinstance(order, int):
            raise IntegrationQueueError("entry order values must be integers")
        orders.append(order)
    if orders != sorted(orders) or len(set(orders)) != len(orders):
        raise IntegrationQueueError("entry order values must be unique and ascending")
    active = [entry for entry in entries if entry.get("queue_state") == "in_progress"]
    if len(active) != 1 or active[0].get("task_id") != "W1-M05":
        raise IntegrationQueueError("the frozen queue must have only W1-M05 in progress")

    for entry in entries:
        task_id = entry["task_id"]
        if entry.get("todo_status_at_freeze") != todo[task_id]:
            raise IntegrationQueueError(f"TODO status mismatch for {task_id}")
        if entry.get("planned_owner") != "codex-1":
            raise IntegrationQueueError(f"planned owner mismatch for {task_id}")
        source_head = entry.get("source_head")
        if not isinstance(source_head, str):
            raise IntegrationQueueError(f"missing source_head for {task_id}")
        _commit_exists(root, source_head)
        for field in ("handoff_head", "superseded_branch_head"):
            commit = entry.get(field)
            if commit is not None:
                if not isinstance(commit, str):
                    raise IntegrationQueueError(f"invalid {field} for {task_id}")
                _commit_exists(root, commit)

        claim = entry.get("canonical_claim")
        if claim is None:
            if entry.get("owner_at_freeze") is not None:
                raise IntegrationQueueError(f"unclaimed entry has owner_at_freeze: {task_id}")
            continue
        if not isinstance(claim, str):
            raise IntegrationQueueError(f"invalid canonical_claim for {task_id}")
        fields = _claim_fields(_snapshot_text(root, baseline, claim))
        if fields.get("task_id") != task_id:
            raise IntegrationQueueError(f"claim task mismatch for {task_id}")
        if fields.get("owner") != entry.get("owner_at_freeze"):
            raise IntegrationQueueError(f"claim owner mismatch for {task_id}")
        if fields.get("branch") != entry.get("branch"):
            raise IntegrationQueueError(f"claim branch mismatch for {task_id}")

    reservations = queue.get("hot_file_reservations")
    if not isinstance(reservations, list) or len(reservations) != 4:
        raise IntegrationQueueError("all four hot-file reservation classes are required")
    names = {row.get("reservation") for row in reservations if isinstance(row, dict)}
    if names != {"manuscript", "figure-integration", "release", "master-status"}:
        raise IntegrationQueueError("hot-file reservation set mismatch")

    return {
        "status": "PASS",
        "baseline_commit": baseline,
        "remaining_tasks": len(entries),
        "active_task": active[0]["task_id"],
        "externally_blocked_or_deferred": sorted(
            entry["task_id"]
            for entry in entries
            if entry.get("queue_state") in {"external_blocked", "deferred"}
        ),
        "hot_file_reservations": len(reservations),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the committed queue")
    parser.parse_args()
    receipt = validate_queue()
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
