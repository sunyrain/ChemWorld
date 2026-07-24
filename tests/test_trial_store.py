from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.trial_store import (
    ConfirmatoryTrialKey,
    ConfirmatoryTrialStore,
    DuplicateTrialKeyError,
    TrialBatchInfrastructureError,
    execute_jobs_resumable,
)

_FAILED_ONCE: set[int] = set()


def _sometimes_fails(job: dict[str, Any]) -> dict[str, int]:
    value = int(job["value"])
    if value == 2 and value not in _FAILED_ONCE:
        _FAILED_ONCE.add(value)
        raise OSError("transient worker failure")
    return {"square": value * value}


def _key(value: int) -> ConfirmatoryTrialKey:
    return ConfirmatoryTrialKey(
        task_id="task",
        truth_family="truth",
        world_cluster=str(value),
        changepoint=8,
        arm="reference",
    )


def test_trial_store_resumes_only_missing_and_never_overwrites(tmp_path: Path) -> None:
    _FAILED_ONCE.clear()
    store = ConfirmatoryTrialStore(tmp_path / "store")
    jobs = [{"value": 1}, {"value": 2}, {"value": 3}]
    keys = [_key(1), _key(2), _key(3)]

    with pytest.raises(TrialBatchInfrastructureError):
        execute_jobs_resumable(
            _sometimes_fails,
            jobs,
            keys,
            workers=1,
            store=store,
            resume=False,
        )
    first = store.audit(keys)
    assert first["completed_count"] == 2
    assert len(first["missing_trial_key_sha256"]) == 1

    results, manifest = execute_jobs_resumable(
        _sometimes_fails,
        jobs,
        keys,
        workers=1,
        store=store,
        resume=True,
    )
    assert results == [{"square": 1}, {"square": 4}, {"square": 9}]
    assert manifest["complete"] is True
    assert manifest["recovered_infrastructure_failure_count"] == 1

    with pytest.raises(DuplicateTrialKeyError):
        store.write_result(keys[0], {"square": 999})

