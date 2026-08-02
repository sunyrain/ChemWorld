from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.g2_agent_system_comparison import (
    G2AgentSystemComparisonError,
    build_g2_agent_system_comparison,
    render_g2_agent_system_comparison_markdown,
)
from chemworld.eval.provenance import canonical_json_sha256


def _audit(*, direct: bool) -> dict[str, object]:
    cells: list[dict[str, object]] = []
    pairs: list[dict[str, object]] = []
    for seed in range(5):
        for arm in ("opaque", "nominal"):
            final_assays = 6 if not direct else (2 if arm == "opaque" else 4)
            operations = 70 + seed if not direct else 80 + seed + (10 if arm == "nominal" else 0)
            cells.append(
                {
                    "world_seed": seed,
                    "arm": arm,
                    "identity": {
                        "world_seed": seed,
                        "world_id": f"world-{seed}",
                        "world_family_version": "world-v1",
                        "mechanism_hash": f"mechanism-{seed}",
                        "material_family_id": "material-family",
                        "material_family_sha256": "material-family-hash",
                        "material_instance_sha256": f"material-{seed}",
                        "scoring_contract_hash": "score-hash",
                        "workflow_mode": "autonomous",
                        "observation_noise_mode": "keyed",
                        "observation_noise_namespace": "g2",
                        "observation_seed": 1000 + seed,
                        "resource_card_sha256": "resource-card-hash",
                    },
                    "resource_ledger": {
                        "closed_batches": 6,
                        "final_assays": final_assays,
                        "discarded_batches": 6 - final_assays,
                        "nonfinal_instrument_uses": 3,
                    },
                    "operations": {"count": operations, "invalid_count": 0},
                    "scores": {
                        "best_final_score": 0.3 + 0.01 * seed,
                        "operation_attempt_running_best_auc": 0.2 + 0.01 * seed,
                    },
                    "provider_sessions": {
                        "qualification_kind": (
                            "primitive_operation_decision"
                            if direct
                            else "experiment_session"
                        )
                    },
                }
            )
        pairs.append(
            {
                "world_seed": seed,
                "nominal_minus_opaque": {
                    "best_final_score": 0.1 if seed != 1 else -0.1,
                    "operation_attempt_running_best_auc": 0.02,
                },
            }
        )
    audit: dict[str, object] = {
        "schema_version": "fixture-audit",
        "status": "completed_audited_descriptive_matrix",
        "matrix": {
            "cell_count": 10,
            "all_cells_complete": True,
            "all_resource_ledgers_verified": True,
            "all_exact_replays_verified": True,
            "all_provider_sessions_verified": True,
            "all_pairs_physically_matched": True,
        },
        "cells": cells,
        "paired_worlds": pairs,
    }
    audit["audit_sha256"] = canonical_json_sha256(audit)
    return audit


def _write(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )


def test_comparison_matches_physics_and_profiles_complete_systems(
    tmp_path: Path,
) -> None:
    codex_path = tmp_path / "codex.json"
    deepseek_path = tmp_path / "deepseek.json"
    _write(codex_path, _audit(direct=False))
    _write(deepseek_path, _audit(direct=True))

    report = build_g2_agent_system_comparison(codex_path, deepseek_path)

    assert report["physical_matching"]["all_cells_matched"] is True
    assert report["physical_matching"]["matched_cell_count"] == 10
    codex = report["systems"]["codex_sol_medium_mcp"]
    deepseek = report["systems"]["deepseek_v4_flash_direct"]
    assert codex["closed_batch_count"] == 60
    assert codex["final_assay_count"] == 60
    assert deepseek["closed_batch_count"] == 60
    assert deepseek["final_assay_count"] == 30
    assert deepseek["discarded_batch_count"] == 30
    assert deepseek["within_system_information_contrast"][
        "nominal_higher_best_world_count"
    ] == 4
    assert report["claim_boundary"]["leaderboard_interpretation"] is False
    assert "does not isolate" in report["claim_boundary"]["not_allowed"]
    rendered = render_g2_agent_system_comparison_markdown(report)
    assert "not a model leaderboard" in rendered


def test_comparison_rejects_cross_system_physical_mismatch(tmp_path: Path) -> None:
    codex = _audit(direct=False)
    deepseek = _audit(direct=True)
    deepseek["cells"][0]["identity"]["mechanism_hash"] = "different"
    deepseek.pop("audit_sha256")
    deepseek["audit_sha256"] = canonical_json_sha256(deepseek)
    codex_path = tmp_path / "codex.json"
    deepseek_path = tmp_path / "deepseek.json"
    _write(codex_path, codex)
    _write(deepseek_path, deepseek)

    with pytest.raises(
        G2AgentSystemComparisonError,
        match="identical physical cells",
    ):
        build_g2_agent_system_comparison(codex_path, deepseek_path)


def test_comparison_rejects_invalid_source_self_hash(tmp_path: Path) -> None:
    codex = _audit(direct=False)
    deepseek = _audit(direct=True)
    deepseek["cells"][0]["operations"]["count"] = 999
    codex_path = tmp_path / "codex.json"
    deepseek_path = tmp_path / "deepseek.json"
    _write(codex_path, codex)
    _write(deepseek_path, deepseek)

    with pytest.raises(G2AgentSystemComparisonError, match="self-hash"):
        build_g2_agent_system_comparison(codex_path, deepseek_path)
