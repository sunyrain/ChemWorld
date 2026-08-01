from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from scripts.build_g2_v05_release_artifacts import (
    G2ReleaseArtifactError,
    build_terminal_file_index,
    compact_replay_record,
)

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.schemas.validation import TRAJECTORY_REQUIRED_KEYS


def _manifest() -> dict[str, object]:
    cells = [
        {
            "cell": {
                "cell_id": f"cell-{index:03d}",
                "world_seed": 1 if index <= 10 else 3,
                "trajectory_replicate_id": f"r{((index - 1) // 2) % 5 + 1:02d}",
                "condition_id": ("opaque_codes" if index % 2 else "anonymous_nominal_properties"),
            },
            "state": "completed",
            "authoritative_attempt_dir": f"cell-{index:03d}/attempt-01",
        }
        for index in range(1, 21)
    ]
    manifest: dict[str, object] = {
        "schema_version": "chemworld-g2-trajectory-replication-run-0.1",
        "cells": cells,
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    return manifest


def _audit() -> dict[str, object]:
    return {
        "schema_version": ("chemworld-autonomous-material-trajectory-replication-audit-0.1"),
        "audit_sha256": "a" * 64,
        "matrix": {
            "completed_cell_count": 20,
            "right_censored_cell_count": 0,
            "all_attempt_selection_policies_verified": True,
            "all_physical_pairs_verified": True,
            "all_terminal_cells_resource_replay_verified": True,
        },
    }


def test_terminal_file_index_is_deterministic_and_excludes_live_preview(
    tmp_path: Path,
) -> None:
    (tmp_path / "cell-001").mkdir()
    (tmp_path / "cell-001" / "trajectory.jsonl").write_text(
        "{}\n",
        encoding="utf-8",
    )
    (tmp_path / "matrix_manifest.json").write_text("{}", encoding="utf-8")
    (tmp_path / "arxiv_remaining_audit.json").write_text(
        "live",
        encoding="utf-8",
    )
    first = build_terminal_file_index(
        tmp_path,
        manifest=_manifest(),
        audit=_audit(),
    )
    second = build_terminal_file_index(
        tmp_path,
        manifest=_manifest(),
        audit=_audit(),
    )
    assert first == second
    assert first["file_count"] == 2
    assert first["content_included"] is False
    assert all(row["path"] != "arxiv_remaining_audit.json" for row in first["files"])
    assert str(tmp_path) not in str(first)


def test_terminal_file_index_fails_closed_when_a_cell_is_pending(
    tmp_path: Path,
) -> None:
    manifest = _manifest()
    manifest["cells"][0]["state"] = "pending"
    unhashed = dict(manifest)
    unhashed.pop("manifest_sha256")
    manifest["manifest_sha256"] = canonical_json_sha256(unhashed)
    with pytest.raises(G2ReleaseArtifactError, match="not terminal"):
        build_terminal_file_index(
            tmp_path,
            manifest=manifest,
            audit=_audit(),
        )


def test_compact_record_removes_v02_outcome_layers_and_provider_trace() -> None:
    source = dict.fromkeys(TRAJECTORY_REQUIRED_KEYS)
    source.update(
        {
            "schema_version": "chemworld-trajectory-0.2",
            "action": {"operation": "terminate"},
            "observation": {"score": 0.5},
            "environment_outcome": {"observation": {"score": 0.5}},
            "agent_visible_observation": {"large": "x" * 1000},
            "evaluation_outcome": {"online_transition_reward": 0.0},
            "agent_metadata": {"provider_response": "private"},
            "constitution_checks": [{"large": "private"}],
            "explanation": {"provider_trace": "private"},
            "material_information_config": {"mode": "opaque_codes"},
        }
    )
    compact = compact_replay_record(deepcopy(source))
    assert compact["schema_version"] == "chemworld-trajectory-0.1"
    assert "environment_outcome" not in compact
    assert "agent_visible_observation" not in compact
    assert "evaluation_outcome" not in compact
    assert "run_id" not in compact
    assert compact["agent_metadata"] == {}
    assert compact["constitution_checks"] == []
    assert compact["explanation"] == {}
    assert compact["action"] == source["action"]
    assert compact["observation"] == source["observation"]
    assert compact["material_information_config"] == {"mode": "opaque_codes"}
