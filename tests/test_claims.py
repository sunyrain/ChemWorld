from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from scripts.manage_claims import check_claims, complete_claim, create_claim


def _prepare(root: Path) -> None:
    (root / "claims" / "active").mkdir(parents=True)
    (root / "claims" / "completed").mkdir(parents=True)


def test_claim_lifecycle_preserves_completed_history(tmp_path: Path) -> None:
    _prepare(tmp_path)
    active = create_claim(
        tmp_path,
        task_id="wf-20-instruments",
        owner="chemist-a",
        branch="team/wf-20",
        scope="Instrument reference cases",
        owned_paths=["src/chemworld/physchem/spectroscopy.py"],
    )
    assert active.is_file()
    assert check_claims(tmp_path)["active_claim_count"] == 1

    completed = complete_claim(
        tmp_path,
        task_id="wf-20-instruments",
        owner="chemist-a",
        summary="Reference cases passed",
    )
    assert completed.is_file()
    assert not active.exists()
    report = check_claims(tmp_path)
    assert report["passed"] is True
    assert report["completed_claim_count"] == 1


def test_claim_rejects_owned_path_overlap(tmp_path: Path) -> None:
    _prepare(tmp_path)
    create_claim(
        tmp_path,
        task_id="wf-10-reaction",
        owner="chemist-a",
        branch="team/wf-10",
        scope="Reaction core",
        owned_paths=["src/chemworld/physchem/reaction"],
    )
    with pytest.raises(ValueError, match="overlaps active task"):
        create_claim(
            tmp_path,
            task_id="wf-11-reactor",
            owner="chemist-b",
            branch="team/wf-11",
            scope="Reactor child path",
            owned_paths=["src/chemworld/physchem/reaction/reactors.py"],
        )


def test_claim_check_rejects_expired_active_claim(tmp_path: Path) -> None:
    _prepare(tmp_path)
    expired = datetime.now(UTC) - timedelta(days=1)
    payload = {
        "schema_version": "chemworld-task-claim-0.1",
        "task_id": "expired-task",
        "owner": "chemist-a",
        "branch": "team/expired",
        "status": "active",
        "scope": "Expired work",
        "owned_paths": ["src/expired.py"],
        "claimed_at": (expired - timedelta(days=1)).isoformat(),
        "expires_at": expired.isoformat(),
        "notes": "",
    }
    path = tmp_path / "claims" / "active" / "expired-task.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    report = check_claims(tmp_path)
    assert report["passed"] is False
    assert any("expired" in error for error in report["errors"])
