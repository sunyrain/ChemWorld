from __future__ import annotations

import hashlib
import json
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "benchmark/releases/chemworld-serious-v1"
ARCHIVE = RELEASE / "g2-deepseek-v0.6-public-trajectory-archive"
INDEX = RELEASE / "g2-deepseek-v0.6-terminal-file-index.json"


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_deepseek_public_archive_is_complete_self_hashed_and_replay_audited() -> None:
    manifest = json.loads((ARCHIVE / "manifest.json").read_text(encoding="utf-8"))
    declared = manifest.pop("archive_sha256")

    assert declared == canonical_json_sha256(manifest)
    assert manifest["status"] == "complete_public_replay_archive"
    assert manifest["provider_content_included"] is False
    assert manifest["hidden_evaluator_identity_included"] is False
    assert manifest["cell_count"] == 10
    assert manifest["record_count"] == 889
    assert len(manifest["cells"]) == 10
    assert sum(row["closed_batch_count"] for row in manifest["cells"]) == 60
    for row in manifest["cells"]:
        path = ARCHIVE / row["compact_path"]
        assert path.stat().st_size == row["compact_bytes"]
        assert _sha(path) == row["compact_sha256"]
        assert row["exact_replay"]["verified"] is True


def test_deepseek_terminal_index_binds_every_formal_source_file() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    declared = index.pop("index_sha256")

    assert declared == canonical_json_sha256(index)
    assert index["file_count"] == 53
    assert index["byte_count"] == 127_883_533
    assert len(index["files"]) == 53
    assert all(len(row["sha256"]) == 64 for row in index["files"])
