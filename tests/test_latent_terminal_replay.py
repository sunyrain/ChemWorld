from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.latent_terminal_replay import (
    ALLOWED_WORKFLOW_BYPASS_REASONS,
    FROZEN_CONTRACT_SHA256,
    LatentTerminalReplayError,
    assert_exact_prefix_identity,
    load_frozen_terminal_contract,
    shadow_noise_namespace,
)
from chemworld.eval.provenance import canonical_json_sha256

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-replay-qualification-v0.1.json"
)


def _report() -> dict[str, object]:
    payload = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_frozen_contract_and_noise_namespace_are_exact() -> None:
    contract = load_frozen_terminal_contract(ROOT)
    assert contract["contract_sha256"] == FROZEN_CONTRACT_SHA256
    assert {
        "measure_final_requires_terminated"
    } == ALLOWED_WORKFLOW_BYPASS_REASONS
    assert shadow_noise_namespace("original", "cell-03", 4) == (
        "original::latent-terminal-final-assay-v0.1::cell-03::lifecycle-04"
    )


def test_committed_qualification_is_self_hashed_and_passes_every_gate() -> None:
    report = _report()
    unhashed = deepcopy(report)
    embedded_hash = unhashed.pop("report_sha256")
    assert embedded_hash == canonical_json_sha256(unhashed)
    assert report["status"] == "PASS"
    assert all(report["gates"].values())
    assert all(report["negative_probes"].values())


def test_qualification_never_crosses_the_formal_outcome_boundary() -> None:
    report = _report()
    assert report["formal_execution_owner"] == "W1-L05"
    assert report["census"] == {
        "agent_provider_calls": 0,
        "formal_checkpoint_payloads_loaded": 0,
        "formal_latent_discard_scores_accessed": 0,
        "formal_shadow_terminal_evaluations_executed": 0,
        "negative_fail_closed_probes": 6,
        "synthetic_prefix_replays": 2,
        "synthetic_terminal_evaluations": 2,
    }


def test_independent_receipts_replay_the_same_terminal_result_without_mutation() -> None:
    receipts = _report()["synthetic_receipts"]
    assert len(receipts) == 2
    assert len(
        {receipt["terminal_evaluation_identity_sha256"] for receipt in receipts}
    ) == 1
    assert len({receipt["noise_key_sha256"] for receipt in receipts}) == 1
    for receipt in receipts:
        assert receipt["original_environment_mutated"] is False
        assert receipt["original_prefix_mutated"] is False
        assert receipt["original_resource_ledger_mutated"] is False
        assert receipt["agent_provider_calls"] == 0
        assert receipt["terminal_action_replacement"]["env_step_calls"] == 0
        assert receipt["terminal_action_replacement"][
            "additional_process_operations"
        ] == 0


def test_exact_prefix_guard_rejects_any_bound_field_change() -> None:
    receipt = _report()["synthetic_receipts"][0]
    identity = {
        "discard_id": "synthetic",
        "cell_id": "synthetic-cell",
        "world_seed": 20_003,
        "information_arm": "opaque_codes",
        "lifecycle_index": 0,
        "terminal_step": 6,
        "operation_ordinal": 6,
        "experiment_index": 0,
        "terminal_action_sha256": "1" * 64,
        "public_prefix_sha256": "2" * 64,
        "hidden_state_sha256": "3" * 64,
        "campaign_resource_snapshot_sha256": "4" * 64,
        "campaign_resource_state_sha256": "5" * 64,
        "world_id": "world",
        "mechanism_hash": "6" * 64,
        "material_instance_sha256": "7" * 64,
        "observation_seed": 320_003,
        "observation_noise_mode": "keyed",
        "observation_noise_namespace": "original",
        "campaign_resource_card_sha256": "8" * 64,
        "task_contract_hash": "9" * 64,
        "scoring_contract_hash": receipt["scoring_contract_hash"],
        "observation_contract_hash": receipt["observation_contract_hash"],
    }
    identity["prefix_identity_sha256"] = canonical_json_sha256(identity)
    assert_exact_prefix_identity(identity, deepcopy(identity))
    tampered = deepcopy(identity)
    tampered["hidden_state_sha256"] = "0" * 64
    with pytest.raises(LatentTerminalReplayError, match="hidden_state_sha256"):
        assert_exact_prefix_identity(identity, tampered)
