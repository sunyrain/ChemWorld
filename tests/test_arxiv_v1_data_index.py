from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from scripts.build_arxiv_v1_data_index import RawRootSpec, build_index


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(tmp_path: Path) -> tuple[Path, RawRootSpec]:
    root = tmp_path / "runs/formal/example"
    root.mkdir(parents=True)
    index = root / "campaign_execution_index.json"
    index.write_text(
        json.dumps({"source_commit": "a" * 40}),
        encoding="utf-8",
    )
    (root / "payload.bin").write_bytes(b"chemworld")
    files = list(root.iterdir())
    spec = RawRootSpec(
        root_id="example",
        relative_path="runs/formal/example",
        source_commit="a" * 40,
        expected_file_count=2,
        expected_byte_count=sum(path.stat().st_size for path in files),
        expected_campaign_index_sha256=_sha256(index),
    )
    return tmp_path, spec


def test_build_index_is_deterministic_and_contains_no_absolute_paths(
    tmp_path: Path,
) -> None:
    repository_root, spec = _fixture(tmp_path)

    first = build_index(repository_root, specs=(spec,))
    second = build_index(repository_root, specs=(spec,))

    assert first == second
    assert first["root_count"] == 1
    assert first["file_count"] == 2
    assert first["content_included"] is False
    assert first["roots"][0]["checks"] == {
        "file_count": True,
        "byte_count": True,
        "campaign_index_sha256": True,
        "source_commit": True,
    }
    serialized = json.dumps(first)
    assert str(repository_root) not in serialized


def test_build_index_fails_closed_on_raw_root_drift(tmp_path: Path) -> None:
    repository_root, spec = _fixture(tmp_path)
    (repository_root / spec.relative_path / "payload.bin").write_bytes(b"drift")

    with pytest.raises(RuntimeError, match="byte_count"):
        build_index(repository_root, specs=(spec,))
