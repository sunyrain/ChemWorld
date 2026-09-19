from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import scripts.export_work_ii_eq_bounded_equilibrium_reports as exporter
import scripts.recover_work_ii_eq_bounded_equilibrium as recovery
import scripts.run_work_ii_eq_bounded_equilibrium as eq


def config() -> dict:
    return eq.load_config()


def prediction_payload(value: float = 0.25) -> dict:
    return {
        "predictions": [
            {
                "query_id": f"Q{index:02d}",
                "metrics": {
                    metric: {
                        "estimate": value,
                        "lower80": max(0.0, value - 0.1),
                        "upper80": min(1.0, value + 0.1),
                    }
                    for metric in eq.METRICS
                },
                "rationale": "An English rationale based on the sealed campaign evidence.",
            }
            for index in range(1, 13)
        ],
        "rationale": "Shared English uncertainty rationale.",
    }


def test_eq_design_has_five_worlds_three_arms_and_one_task() -> None:
    frozen = config()
    validated = eq.validate_design(frozen)

    assert frozen["task"] == "bounded_aqueous_equilibrium_characterization"
    assert len(validated["schedule"]) == 15
    assert {row["world_id"] for row in validated["schedule"]} == {
        f"EQ-W{index:02d}" for index in range(1, 6)
    }
    assert {row["arm"] for row in validated["schedule"]} == set(eq.ARMS)
    assert {row["goal"] for row in validated["schedule"]} == {"characterization"}


def test_strict_opaque_has_no_instance_prior_and_a_m_are_matched() -> None:
    frozen = config()

    for world in frozen["worlds"]:
        world_id = world["world_id"]
        assert eq.public_prior(frozen, world_id, "Opaque") is None
        aligned = eq.public_prior(frozen, world_id, "Aligned")
        wrong = eq.public_prior(frozen, world_id, "MisIndexed")
        assert aligned is not None and wrong is not None

        comparable_a = copy.deepcopy(aligned)
        comparable_m = copy.deepcopy(wrong)
        claim_a = comparable_a.pop("claim")
        claim_m = comparable_m.pop("claim")
        assert comparable_a == comparable_m
        assert claim_a.keys() == claim_m.keys()
        assert claim_a["dilution_response"]["anchor"] == claim_m["dilution_response"]["anchor"]
        assert claim_a != claim_m


def test_aligned_covers_truth_and_misindexed_is_publicly_refutable() -> None:
    frozen = config()
    threshold = frozen["provider_free_gate"]["minimum_misindexed_pka_center_gap"]

    for world in frozen["worlds"]:
        actual = world["private_authoring"]["effective_pka"]
        aligned = eq.public_prior(frozen, world["world_id"], "Aligned")
        wrong = eq.public_prior(frozen, world["world_id"], "MisIndexed")
        assert aligned is not None and wrong is not None
        low, high = aligned["claim"]["effective_pka_interval80"]
        wrong_low, wrong_high = wrong["claim"]["effective_pka_interval80"]
        assert low <= actual <= high
        assert min(abs(actual - wrong_low), abs(actual - wrong_high)) >= threshold


def test_q_is_fixed_complete_and_not_exposed_by_source_prompt() -> None:
    frozen = config()
    rows = eq.queries(frozen)
    coverage = {tag for row in rows for tag in row["coverage"]}

    assert [row["query_id"] for row in rows] == [f"Q{index:02d}" for index in range(1, 13)]
    assert {
        "near_domain",
        "concentration_volume_decoupling",
        "two_stage_dosing",
        "dissociation_precipitation_competition",
        "boundary_extrapolation",
        "equivalent_explanation",
        "interval_calibration",
    } <= coverage
    serialized_queries = json.dumps(rows, sort_keys=True)
    assert serialized_queries not in eq.SYSTEM
    assert "Q01" not in eq.SYSTEM


def test_equilibrium_confidence_is_not_a_prediction_or_agent_uncertainty_metric() -> None:
    frozen = config()

    assert "equilibrium_confidence" not in eq.METRICS
    assert "equilibrium_confidence" not in frozen["prediction_metrics"]
    assert frozen["excluded_prediction_fields"]["equilibrium_confidence"]
    assert "not your uncertainty" in eq.SYSTEM
    assert "not a task score" in eq.SYSTEM


def test_q_validation_requires_english_complete_intervals() -> None:
    rows = eq.queries(config())
    payload = prediction_payload()

    assert eq.validate_posttest("Q", payload, rows)["valid"]
    payload["predictions"][0]["metrics"][eq.METRICS[0]]["lower80"] = 0.5
    assert not eq.validate_posttest("Q", payload, rows)["valid"]

    cjk = prediction_payload()
    cjk["predictions"][0]["rationale"] = "中文"
    assert not eq.validate_posttest("Q", cjk, rows)["valid"]


def test_prediction_evaluator_uses_five_repeats_and_no_confidence_score() -> None:
    rows = eq.queries(config())
    payload = prediction_payload(0.25)
    truth = {
        row["query_id"]: [
            dict.fromkeys(eq.METRICS, 0.25 + offset)
            for offset in (-0.02, -0.01, 0.0, 0.01, 0.02)
        ]
        for row in rows
    }

    result = eq.evaluate_predictions(payload, rows, truth)

    assert result["valid"]
    assert result["equilibrium_confidence_used_as_agent_uncertainty_or_score"] is False
    assert set(result["metrics"]) == set(eq.METRICS)
    assert all(row["reference_observation_count"] == 60 for row in result["metrics"].values())
    assert all(
        row["empirical_coverage80"] == pytest.approx(1.0)
        for row in result["metrics"].values()
    )


def test_freeze_validation_fails_closed_without_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = tmp_path / "provider-free-gate" / "gate.json"
    eq.write(gate, {"passed": True})
    monkeypatch.setattr(eq, "FREEZE", tmp_path / "absent-freeze.json")

    with pytest.raises(RuntimeError, match="freeze manifest is absent"):
        eq.validate_freeze(tmp_path, config())


def test_nonzero_prefreeze_calls_accept_exact_post_source_pretruth_evidence() -> None:
    repair = {
        "repair_phase": "post_source_pre_truth",
        "provider_api_turn_attempts": 5,
        "affected_cells": ["EQ-W01--Opaque"],
        "accepted_source_model_calls": 1,
        "scientific_actions": 60,
        "source_batches": 12,
        "source_exact_replay": True,
        "completed_posttest_payloads": 0,
        "truth_generated": False,
        "scientific_contract_changed": False,
        "source_rerun_required": False,
    }

    eq.validate_execution_repair_evidence(5, repair)
    broken = copy.deepcopy(repair)
    broken["source_rerun_required"] = True
    with pytest.raises(RuntimeError, match="execution-repair"):
        eq.validate_execution_repair_evidence(5, broken)


def test_interrupted_snapshot_selects_fresh_source_when_no_result(tmp_path: Path) -> None:
    frozen = config()
    cell = eq.validate_design(frozen)["schedule"][0]
    folder = tmp_path / "sources" / cell["cell_id"]
    folder.mkdir(parents=True)

    snapshot, actual = recovery.interrupted_snapshot(tmp_path, frozen, cell)

    assert actual == folder
    assert snapshot is not None
    assert snapshot["source_status"] == "failed"
    assert recovery.recovery_kind(snapshot, folder) == "fresh_source"


def test_cell_folder_setup_precreates_private_source_output(tmp_path: Path) -> None:
    folder = tmp_path / "cell"

    private = eq.create_cell_folders(folder)

    assert private == folder / "private-provider"
    assert (private / "source").is_dir()


def test_eq_mcp_startup_timeout_is_materials_safe_and_unique() -> None:
    command = ["codex", "-c", "mcp_servers.chemworld_lab.startup_timeout_sec=30"]

    adjusted = eq.with_eq_mcp_startup_timeout(command)

    assert "mcp_servers.chemworld_lab.startup_timeout_sec=180" in adjusted
    assert "mcp_servers.chemworld_lab.startup_timeout_sec=30" not in adjusted


def test_latest_recovery_can_select_retained_complete_source(tmp_path: Path) -> None:
    result_path = (
        tmp_path
        / "recoveries"
        / "EQ-W01--Opaque"
        / "attempt-04"
        / "execution"
        / "sources"
        / "EQ-W01--Opaque"
        / "RESULT.json"
    )
    eq.write(
        result_path,
        {
            "status": "retained_nonconforming",
            "source_status": "completed",
            "posttest_chain_sealed": False,
        },
    )
    eq.write(
        tmp_path / "recoveries" / "EQ-W01--Opaque" / "attempt-04" / "recovery.json",
        {
            "result_path": str(result_path.relative_to(tmp_path)),
            "status": "retained_nonconforming",
        },
    )

    assert recovery.latest_recovery(tmp_path, "EQ-W01--Opaque") is None
    selected = recovery.latest_recovery(
        tmp_path, "EQ-W01--Opaque", completed_only=False
    )
    assert selected is not None
    assert selected[0]["source_status"] == "completed"
    assert selected[1] == result_path


def test_source_receipts_can_precede_latest_posttest_context(tmp_path: Path) -> None:
    latest = tmp_path / "recoveries" / "EQ-W01--Opaque" / "attempt-05"
    source = (
        tmp_path
        / "recoveries"
        / "EQ-W01--Opaque"
        / "attempt-04"
        / "execution"
        / "sources"
        / "EQ-W01--Opaque"
    )
    eq.write(source / "private-provider" / "source-receipts.json", [{"thread_id": "private"}])
    result_path = source / "RESULT.json"
    eq.write(result_path, {"status": "retained_nonconforming"})
    eq.write(
        source.parents[2] / "recovery.json",
        {"result_path": str(result_path.relative_to(tmp_path))},
    )

    assert recovery.source_receipt_folder(
        tmp_path, "EQ-W01--Opaque", latest
    ) == source


def test_public_export_rejects_private_field_names() -> None:
    with pytest.raises(RuntimeError, match="private field"):
        exporter._assert_public({"thread_id_sha256": "hidden"})


def test_public_result_omits_thread_usage_and_raw_provider_material() -> None:
    result = {
        "cell_id": "EQ-W01-Opaque-characterization",
        "world_id": "EQ-W01",
        "arm": "Opaque",
        "goal": "characterization",
        "status": "completed",
        "source_status": "completed",
        "operations": 12,
        "posttest_chain_sealed": True,
        "batches": [],
        "exact_replay": {"verified": True},
        "rollbacks": [],
        "posttests": {stage: {"payload": {"report": "English"}} for stage in ("K1", "K2")},
        "posttest_validation": {},
        "thread_id_sha256": "must-not-export",
        "source_usage": {"input_tokens": 999},
    }
    result["posttests"]["Q"] = {"payload": prediction_payload()}

    public = exporter.public_result(result, {"valid": True}, {}, "original")

    serialized = json.dumps(public).lower()
    assert "thread_id" not in serialized
    assert "input_tokens" not in serialized
    assert "raw model event streams" in serialized
