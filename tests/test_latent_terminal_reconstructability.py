from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.latent_terminal_contract import EXPECTED_DISCARD_COUNT
from chemworld.eval.latent_terminal_reconstructability import (
    REPORT_ID,
    reconstructability_report_sha256,
    validate_reconstructability_report,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-reconstructability-v0.1.json"
)


def _report() -> dict[str, object]:
    payload = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_committed_report_is_self_hashed_and_valid() -> None:
    report = _report()
    assert report["report_id"] == REPORT_ID
    assert report["report_sha256"] == reconstructability_report_sha256(report)
    assert validate_reconstructability_report(report, root=ROOT) == []


def test_report_covers_all_frozen_discards_without_latent_outcomes() -> None:
    report = _report()
    census = report["census"]
    assert census == {
        "cell_count": 10,
        "discard_unit_count": EXPECTED_DISCARD_COUNT,
        "reconstructable_unit_count": EXPECTED_DISCARD_COUNT,
        "unresolved_unit_count": 0,
        "shadow_terminal_evaluations_executed": 0,
        "latent_discard_scores_accessed": 0,
        "agent_provider_calls": 0,
    }
    cells = report["cells"]
    units = [unit for cell in cells for unit in cell["discard_units"]]
    assert len(units) == EXPECTED_DISCARD_COUNT
    assert len({unit["discard_id"] for unit in units}) == EXPECTED_DISCARD_COUNT
    assert all(unit["reconstructable"] for unit in units)
    assert all(unit["shadow_terminal_executed"] is False for unit in units)
    assert all(unit["latent_discard_score_accessed"] is False for unit in units)
    assert all(unit["agent_provider_calls"] == 0 for unit in units)
    forbidden = {"latent_terminal_score", "leaderboard_score", "truth"}
    assert all(not (forbidden & set(unit)) for unit in units)


def test_every_checkpoint_gate_and_source_binding_passes() -> None:
    report = _report()
    assert all(report["gates"].values())
    assert report["raw_root_audit"] == {
        "all_paths_sizes_and_hashes_match": True,
        "byte_count": 127883533,
        "file_count": 53,
        "unindexed_file_count": 0,
    }
    for cell in report["cells"]:
        assert cell["exact_full_trajectory_replay"]["verified"] is True
        assert cell["all_discard_checkpoints_reconstructable"] is True
        for unit in cell["discard_units"]:
            assert all(unit["gates"].values())
            assert len(unit["hidden_state_sha256"]) == 64
            assert len(unit["campaign_resource_snapshot_sha256"]) == 64
            assert len(unit["checkpoint_identity_sha256"]) == 64


def test_validator_rejects_gate_and_outcome_boundary_tampering() -> None:
    original = _report()

    bad_gate = deepcopy(original)
    bad_gate["gates"]["agent_provider_calls_zero"] = False
    bad_gate["report_sha256"] = reconstructability_report_sha256(bad_gate)
    assert "one or more reconstructability gates failed" in (
        validate_reconstructability_report(bad_gate)
    )

    leaked = deepcopy(original)
    leaked["cells"][0]["discard_units"][0]["leaderboard_score"] = 0.5
    leaked["report_sha256"] = reconstructability_report_sha256(leaked)
    assert "report leaks a latent score or hidden-state payload" in (
        validate_reconstructability_report(leaked)
    )

    crossed = deepcopy(original)
    crossed["census"]["shadow_terminal_evaluations_executed"] = 1
    crossed["report_sha256"] = reconstructability_report_sha256(crossed)
    assert "census is incomplete or outcome boundary was crossed" in (
        validate_reconstructability_report(crossed)
    )
