from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
import scripts.build_work_ii_electrochemical_d1_execution as builder
import scripts.build_work_ii_reaction_safety_d1_execution as reaction_builder
from scripts.build_work_ii_electrochemical_d1_execution import build

import chemworld.eval.work_ii_execution_mode as execution_mode
from chemworld.eval.work_ii_execution_mode import (
    build_execution_envelope,
    build_release_manifest,
    prepare_execution_context,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "configs/benchmark/work_ii_electrochemical_matched_prior_d1.json"
REACTION_SOURCE = ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_d1.json"


def _release_source(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[dict[str, object], dict[str, object]]:
    runtime = tmp_path / "runtime.py"
    runtime.write_text("VALUE = 1\n", encoding="utf-8")
    monkeypatch.setattr(builder, "ROOT", tmp_path)
    monkeypatch.setattr(execution_mode, "git_worktree_dirty", lambda _root: False)
    monkeypatch.setattr(execution_mode, "git_source_commit", lambda _root: "a" * 40)
    manifest = build_release_manifest(tmp_path, execution_surface=["runtime.py"])
    context = prepare_execution_context(tmp_path, mode="release", release_manifest=manifest)
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    source["execution_context"] = build_execution_envelope(context)
    source["legacy_source_evidence"] = False
    source["qualification"].update(
        {
            "q2_passed": True,
            "execution_authorized": False,
            "formal_r5_authorized": False,
        }
    )
    return source, manifest


def test_electrochemical_d1_execution_builder_preserves_release_q2_pattern(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source, manifest = _release_source(monkeypatch, tmp_path)
    source_path = tmp_path / "d1.json"
    source_path.write_text(json.dumps(source), encoding="utf-8")
    config = build(source, source_path=source_path, release_manifest=manifest)

    assert config["task_id"] == "electrochemical-conversion"
    assert config["world_seed"] == 0
    assert config["campaign"]["complete_experiments"] == 10
    assert config["campaign"]["operation_attempt_limit"] == 110
    assert config["campaign"]["process_time_limit_s"] == 45_000.0
    assert config["provider"]["model"] == "gpt-5.6-sol"
    assert config["provider"]["reasoning_effort"] == "medium"
    assert config["provider"]["session_wall_time_limit_s"] == 6_600.0
    assert config["method_resources"]["input_token_limit"] == 12_000_000
    assert config["method_resources"]["uncached_input_token_limit"] == 1_200_000
    assert config["method_resources"]["output_token_limit"] == 96_000
    assert config["qualification"]["execution_authorized"] is True
    assert config["qualification"]["formal_r5_authorized"] is False
    assert "resource_status" not in config["method_resources"]


@pytest.mark.parametrize("defect", ["development", "legacy", "cross_freeze"])
def test_electrochemical_d1_execution_builder_rejects_nonrelease_q2(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    defect: str,
) -> None:
    source, manifest = _release_source(monkeypatch, tmp_path)
    if defect == "development":
        source["execution_context"] = build_execution_envelope(
            prepare_execution_context(tmp_path, mode="development")
        )
    elif defect == "legacy":
        source["legacy_source_evidence"] = True
    else:
        source = deepcopy(source)
        source["execution_context"]["freeze_id"] = "f" * 64
    source_path = tmp_path / "d1.json"
    source_path.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(ValueError, match="release D1 source validation failed"):
        build(source, source_path=source_path, release_manifest=manifest)


def test_reaction_d1_execution_builder_uses_the_same_release_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    electro_source, manifest = _release_source(monkeypatch, tmp_path)
    source = json.loads(REACTION_SOURCE.read_text(encoding="utf-8"))
    source["execution_context"] = electro_source["execution_context"]
    source["legacy_source_evidence"] = False
    source["qualification"].update(
        {
            "q2_passed": True,
            "execution_authorized": False,
            "formal_r5_authorized": False,
        }
    )
    source_path = tmp_path / "reaction-d1.json"
    source_path.write_text(json.dumps(source), encoding="utf-8")
    monkeypatch.setattr(reaction_builder, "ROOT", tmp_path)

    config = reaction_builder.build(
        source,
        source_path=source_path,
        release_manifest=manifest,
    )
    assert config["qualification"]["execution_authorized"] is True
    assert config["execution_context"]["freeze_id"] == manifest["freeze_id"]

    source["legacy_source_evidence"] = True
    with pytest.raises(ValueError, match="release D1 source validation failed"):
        reaction_builder.build(
            source,
            source_path=source_path,
            release_manifest=manifest,
        )
