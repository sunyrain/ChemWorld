from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_execution_mode as execution_mode
from chemworld.eval.work_ii_execution_mode import (
    ExecutionMode,
    build_execution_envelope,
    build_release_manifest,
    prepare_execution_context,
    release_manifest_sha256,
    validate_execution_envelope,
    validate_release_d1_config,
    validate_release_manifest,
)


def test_development_mode_never_checks_git_or_hashes_tree(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def unexpected(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("development mode performed a release provenance check")

    monkeypatch.setattr(execution_mode, "git_worktree_dirty", unexpected)
    monkeypatch.setattr(execution_mode, "git_source_commit", unexpected)
    monkeypatch.setattr(execution_mode, "work_ii_material_tree_sha256", unexpected)
    context = prepare_execution_context(tmp_path, mode="development")
    envelope = build_execution_envelope(context)
    assert envelope == {
        "execution_mode": "development",
        "evidence_status": "development_only",
        "release_eligible": False,
        "c2_admission_authorized": False,
        "tested_commit": None,
        "freeze_id": None,
        "release_manifest_sha256": None,
        "execution_surface_sha256": None,
    }
    assert validate_execution_envelope(tmp_path, envelope, context) == []


def test_development_mode_rejects_release_manifest(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must not bind"):
        prepare_execution_context(
            tmp_path,
            mode=ExecutionMode.DEVELOPMENT,
            release_manifest={},
        )


def _release_manifest(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> dict[str, object]:
    source = tmp_path / "runtime.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    monkeypatch.setattr(execution_mode, "git_worktree_dirty", lambda _root: False)
    monkeypatch.setattr(execution_mode, "git_source_commit", lambda _root: "a" * 40)
    return build_release_manifest(tmp_path, execution_surface=["runtime.py"])


def test_release_requires_manifest_clean_exact_head_and_surface(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    with pytest.raises(ValueError, match="requires a release manifest"):
        prepare_execution_context(tmp_path, mode="release")
    manifest = _release_manifest(monkeypatch, tmp_path)
    context = prepare_execution_context(
        tmp_path, mode=ExecutionMode.RELEASE, release_manifest=manifest
    )
    envelope = build_execution_envelope(context)
    assert envelope["execution_mode"] == "release"
    assert envelope["release_eligible"] is True
    assert envelope["c2_admission_authorized"] is True
    assert envelope["tested_commit"] == "a" * 40
    assert envelope["release_manifest_sha256"] == manifest["manifest_sha256"]
    assert validate_execution_envelope(tmp_path, envelope, context) == []

    monkeypatch.setattr(execution_mode, "git_source_commit", lambda _root: "b" * 40)
    assert "Work II release execution requires the exact frozen HEAD" in (
        validate_release_manifest(tmp_path, manifest)
    )
    monkeypatch.setattr(execution_mode, "git_source_commit", lambda _root: "a" * 40)
    monkeypatch.setattr(execution_mode, "git_worktree_dirty", lambda _root: True)
    assert validate_release_manifest(tmp_path, manifest) == []


def test_release_rejects_surface_or_manifest_tampering(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    manifest = _release_manifest(monkeypatch, tmp_path)
    source = tmp_path / "runtime.py"
    source.write_text("VALUE = 2\n", encoding="utf-8")
    assert "Work II release execution surface changed after freeze" in (
        validate_release_manifest(tmp_path, manifest)
    )

    source.write_text("VALUE = 1\n", encoding="utf-8")
    tampered = deepcopy(manifest)
    tampered["formal_result"] = True
    assert "Work II execution release manifest self-hash mismatch" in (
        validate_release_manifest(tmp_path, tampered)
    )
    tampered["manifest_sha256"] = release_manifest_sha256(tampered)
    assert "Work II execution release manifest crossed its freeze boundary" in (
        validate_release_manifest(tmp_path, tampered)
    )


def test_release_envelope_rejects_cross_freeze_context(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    manifest = _release_manifest(monkeypatch, tmp_path)
    context = prepare_execution_context(
        tmp_path, mode="release", release_manifest=manifest
    )
    envelope = build_execution_envelope(context)
    envelope["freeze_id"] = "f" * 64
    assert "Work II execution envelope differs from the expected context" in (
        validate_execution_envelope(tmp_path, envelope, context)
    )


def test_release_envelope_validation_allows_generated_outputs_after_preflight(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    manifest = _release_manifest(monkeypatch, tmp_path)
    context = prepare_execution_context(
        tmp_path, mode="release", release_manifest=manifest
    )
    monkeypatch.setattr(
        execution_mode,
        "git_worktree_dirty",
        lambda _root: (_ for _ in ()).throw(
            AssertionError("envelope validation repeated the launch-time clean check")
        ),
    )
    assert validate_execution_envelope(
        tmp_path, build_execution_envelope(context), context
    ) == []


def test_release_prepare_allows_new_non_surface_artifacts_but_rejects_surface_drift(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    manifest = _release_manifest(monkeypatch, tmp_path)
    monkeypatch.setattr(
        execution_mode,
        "git_worktree_dirty",
        lambda _root: (_ for _ in ()).throw(
            AssertionError("post-freeze validation repeated the global clean check")
        ),
    )
    (tmp_path / "generated-report.json").write_text("{}\n", encoding="utf-8")
    prepare_execution_context(tmp_path, mode="release", release_manifest=manifest)

    (tmp_path / "runtime.py").write_text("VALUE = 2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="execution surface changed"):
        prepare_execution_context(tmp_path, mode="release", release_manifest=manifest)


def test_release_d1_config_requires_same_freeze_nonlegacy_q2_authorization(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    manifest = _release_manifest(monkeypatch, tmp_path)
    context = prepare_execution_context(
        tmp_path, mode="release", release_manifest=manifest
    )
    config = {
        "execution_context": build_execution_envelope(context),
        "legacy_source_evidence": False,
        "qualification": {
            "q2_passed": True,
            "execution_authorized": False,
            "formal_r5_authorized": False,
        },
    }
    assert validate_release_d1_config(
        tmp_path,
        config,
        manifest,
        require_provider_authorized=False,
    ) == []
    assert "Work II release D1 is not provider-authorized" in validate_release_d1_config(
        tmp_path,
        config,
        manifest,
        require_provider_authorized=True,
    )

    authorized = deepcopy(config)
    authorized["qualification"]["execution_authorized"] = True
    assert validate_release_d1_config(
        tmp_path,
        authorized,
        manifest,
        require_provider_authorized=True,
    ) == []

    development = deepcopy(config)
    development["execution_context"] = build_execution_envelope(
        prepare_execution_context(tmp_path, mode="development")
    )
    assert any(
        "execution context" in error
        for error in validate_release_d1_config(
            tmp_path,
            development,
            manifest,
            require_provider_authorized=False,
        )
    )

    legacy = deepcopy(config)
    legacy["legacy_source_evidence"] = True
    assert "Work II release D1 uses legacy source evidence" in validate_release_d1_config(
        tmp_path,
        legacy,
        manifest,
        require_provider_authorized=False,
    )

    cross_freeze = deepcopy(config)
    cross_freeze["execution_context"]["freeze_id"] = "f" * 64
    assert any(
        "execution context" in error
        for error in validate_release_d1_config(
            tmp_path,
            cross_freeze,
            manifest,
            require_provider_authorized=False,
        )
    )
