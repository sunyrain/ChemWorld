from __future__ import annotations

import ast
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
    git_tracked_tree_dirty,
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
    assert not git_tracked_tree_dirty(root)

    (root / "untracked.txt").write_text("ignored\n", encoding="utf-8")
    assert not git_tracked_tree_dirty(root)

    source.write_text("source-v2\n", encoding="utf-8")
    assert git_tracked_tree_dirty(root)
    source.write_text("source-v1\n", encoding="utf-8")
    assert not git_tracked_tree_dirty(root)

    evidence.write_text('{"refreshed":true}\n', encoding="utf-8")
    assert git_tracked_tree_dirty(root)
    assert not git_tracked_tree_dirty(
        root, excluded_paths={"reports/evidence.json"}
    )
    assert not git_tracked_tree_dirty(root, excluded_prefixes={"reports"})

    _git(root, "add", "reports/evidence.json")
    _git(root, "commit", "-m", "evidence only")
    assert git_source_commit(root) != initial_commit
    assert not git_tracked_tree_dirty(root)


@pytest.mark.parametrize(
    "script",
    [
        Path("scripts/run_ppo_v048_preflight.py"),
        Path("scripts/run_sac_v048_preflight.py"),
    ],
)
def test_migrated_preflights_do_not_redefine_shared_helpers(script: Path) -> None:
    tree = ast.parse(script.read_text(encoding="utf-8"))
    local_functions = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert not {"_canonical_sha256", "_file_sha256", "_write_json"} & local_functions
