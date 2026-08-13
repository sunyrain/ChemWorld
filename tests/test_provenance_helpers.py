from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.provenance import (
    canonical_json_bytes,
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def test_canonical_json_and_atomic_writer_preserve_contract(tmp_path: Path) -> None:
    payload: dict[str, Any] = {"β": [1, True], "a": None}
    encoded = b'{"a":null,"\xce\xb2":[1,true]}'

    assert canonical_json_bytes(payload) == encoded
    assert canonical_json_sha256(payload) == hashlib.sha256(encoded).hexdigest()

    target = tmp_path / "nested" / "report.json"
    write_json_atomic(target, payload)
    assert target.read_bytes() == (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    assert file_sha256(target) == hashlib.sha256(target.read_bytes()).hexdigest()
    assert not target.with_name(f".{target.name}.tmp").exists()

    with pytest.raises(ValueError, match="Out of range float values"):
        canonical_json_bytes({"invalid": float("nan")})


def test_atomic_writer_retries_transient_windows_sharing_violation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "status.json"
    original_replace = Path.replace
    attempts = 0

    def transient_replace(source: Path, destination: Path) -> Path:
        nonlocal attempts
        attempts += 1
        if attempts <= 2:
            raise PermissionError(5, "simulated Windows sharing violation")
        return original_replace(source, destination)

    monkeypatch.setattr(Path, "replace", transient_replace)
    write_json_atomic(target, {"completed": 1})

    assert attempts == 3
    assert json.loads(target.read_text(encoding="utf-8")) == {"completed": 1}
    assert list(tmp_path.glob(".atomic-*.tmp")) == []


def test_atomic_writer_exhaustion_is_fail_closed_and_preserves_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "status.json"
    target.write_text('{"completed":0}\n', encoding="utf-8")

    def blocked_replace(_source: Path, _destination: Path) -> Path:
        raise PermissionError(5, "persistent Windows sharing violation")

    monkeypatch.setattr(Path, "replace", blocked_replace)
    monkeypatch.setattr("chemworld.eval.provenance.sleep", lambda _delay: None)

    with pytest.raises(PermissionError, match="persistent Windows sharing violation"):
        write_json_atomic(target, {"completed": 1})

    assert json.loads(target.read_text(encoding="utf-8")) == {"completed": 0}
    assert list(tmp_path.glob(".atomic-*.tmp")) == []


def test_file_sha256_streams_large_artifacts(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "trajectory.jsonl"
    target.write_bytes((b"trajectory-row\n" * 100_000) + b"final-row\n")
    expected = hashlib.sha256(target.read_bytes()).hexdigest()

    def forbidden_read_bytes(_path: Path) -> bytes:
        raise AssertionError("file hashing must not materialize the complete artifact")

    monkeypatch.setattr(Path, "read_bytes", forbidden_read_bytes)

    assert file_sha256(target) == expected


def test_git_provenance_distinguishes_source_and_evidence_changes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init")
    _git(root, "config", "user.email", "provenance-test@example.invalid")
    _git(root, "config", "user.name", "ChemWorld provenance test")
    source = root / "source.txt"
    evidence = root / "reports" / "evidence.json"
    evidence.parent.mkdir()
    source.write_text("source-v1\n", encoding="utf-8")
    evidence.write_text("{}\n", encoding="utf-8")
    _git(root, "add", "source.txt", "reports/evidence.json")
    _git(root, "commit", "-m", "initial")

    initial_commit = git_source_commit(root)
    assert initial_commit == _git(root, "rev-parse", "HEAD")
    assert not git_worktree_dirty(root)
    untracked = root / "untracked.txt"
    untracked.write_text("material\n", encoding="utf-8")
    assert git_worktree_dirty(root)
    assert git_worktree_dirty(root)
    assert not git_worktree_dirty(root, excluded_paths={"untracked.txt"})
    untracked.unlink()

    source.write_text("source-v2\n", encoding="utf-8")
    assert git_worktree_dirty(root)
    source.write_text("source-v1\n", encoding="utf-8")
    assert not git_worktree_dirty(root)

    evidence.write_text('{"refreshed":true}\n', encoding="utf-8")
    assert git_worktree_dirty(root)
    assert not git_worktree_dirty(root, excluded_paths={"reports/evidence.json"})
    assert not git_worktree_dirty(root, excluded_prefixes={"reports"})

    _git(root, "add", "reports/evidence.json")
    _git(root, "commit", "-m", "evidence only")
    assert git_source_commit(root) != initial_commit
    assert not git_worktree_dirty(root)
