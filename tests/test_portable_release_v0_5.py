from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.portable_release import (
    PortableReleaseError,
    build_release_audit,
    canonical_sha256,
    documentation_identity,
    file_manifest,
    load_portable_release_protocol,
    release_manifest,
    semantic_identity,
    validate_platform_attestation,
)


def test_protocol_semantics_and_documentation_are_disjoint() -> None:
    protocol = load_portable_release_protocol()
    semantic = semantic_identity(protocol)
    docs = documentation_identity(protocol)
    assert semantic["file_count"] > 100
    assert docs["file_count"] > 10
    assert not set(semantic["files"]).intersection(docs["files"])
    assert semantic["sha256"] != docs["sha256"]


def test_documentation_change_does_not_change_semantic_hash(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "src/model.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "docs/index.md").write_text("first\n", encoding="utf-8")
    semantic_before = file_manifest(tmp_path, ["src/**/*.py"])
    (tmp_path / "docs/index.md").write_text("second\n", encoding="utf-8")
    semantic_after = file_manifest(tmp_path, ["src/**/*.py"])
    assert canonical_sha256(semantic_before) == canonical_sha256(semantic_after)


def test_semantic_change_changes_hash(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    source = tmp_path / "src/model.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    before = canonical_sha256(file_manifest(tmp_path, ["src/**/*.py"]))
    source.write_text("VALUE = 2\n", encoding="utf-8")
    after = canonical_sha256(file_manifest(tmp_path, ["src/**/*.py"]))
    assert before != after


@pytest.mark.parametrize("pattern", ["../secret", "C:/secret", "/tmp/secret"])
def test_file_manifest_rejects_unsafe_patterns(tmp_path: Path, pattern: str) -> None:
    with pytest.raises(PortableReleaseError):
        file_manifest(tmp_path, [pattern])


def test_platform_attestation_rejects_semantic_mismatch() -> None:
    payload = {
        "schema_version": "chemworld-portable-platform-attestation-0.1",
        "protocol_sha256": "protocol",
        "backend_semantic_sha256": "wrong",
        "clean_wheel_replay_passed": True,
        "exact_replay": True,
        "environment": {"platform_key": "windows"},
    }
    failures = validate_platform_attestation(
        payload, semantic_sha256="semantic", protocol_sha256="protocol"
    )
    assert failures == ["platform attestation binds a different backend semantic hash"]


def test_windows_release_records_linux_as_optional_follow_up() -> None:
    protocol = load_portable_release_protocol()
    semantic = semantic_identity(protocol)
    attestation = {
        "schema_version": "chemworld-portable-platform-attestation-0.1",
        "protocol_sha256": canonical_sha256(protocol),
        "backend_semantic_sha256": semantic["sha256"],
        "clean_wheel_replay_passed": True,
        "exact_replay": True,
        "environment": {"platform_key": "windows"},
    }
    report = build_release_audit(protocol, [attestation])
    manifest = release_manifest(report)
    assert report["missing_platforms"] == []
    assert report["missing_optional_platforms"] == ["linux"]
    assert report["required_platforms"] == ["windows"]
    assert report["optional_platforms"] == ["linux"]
    assert report["observed_platforms"] == ["windows"]
    assert report["portable_release_ready"] is True
    assert manifest["release_status"] == "formal_candidate"
    assert manifest["required_platforms"] == ["windows"]
    assert manifest["optional_platforms"] == ["linux"]
    assert manifest["observed_platforms"] == ["windows"]
    assert manifest["missing_optional_platforms"] == ["linux"]
    assert manifest["benchmark_claim_allowed"] is False


def test_protocol_is_packaged_as_json() -> None:
    protocol = load_portable_release_protocol()
    encoded = json.dumps(protocol, sort_keys=True)
    assert "foundation-v05-portable-release" in encoded
