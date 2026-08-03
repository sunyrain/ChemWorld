from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.latent_terminal_contract import (
    EXPECTED_ARM_COUNTS,
    EXPECTED_ASSAY_COUNT,
    EXPECTED_CELL_COUNT,
    EXPECTED_DISCARD_COUNT,
    EXPECTED_LIFECYCLE_COUNT,
    FROZEN_CAMPAIGN_AUDIT_SHA256,
    FROZEN_COMPARISON_SHA256,
    FROZEN_MATRIX_MANIFEST_SHA256,
    FROZEN_PUBLIC_ARCHIVE_SHA256,
    FROZEN_TERMINAL_INDEX_SHA256,
    PRIMARY_RELATIVE_THRESHOLD,
    REGISTERED_TASK_THRESHOLD,
    RELATIVE_THRESHOLD_SENSITIVITY,
    build_latent_terminal_contract,
    latent_terminal_contract_sha256,
    validate_latent_terminal_contract,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/work_i_latent_terminal_contract_v0.1.json"


def test_contract_rebuilds_the_frozen_terminal_census() -> None:
    contract = build_latent_terminal_contract(ROOT)
    assert validate_latent_terminal_contract(contract, root=ROOT) == []
    assert contract["contract_sha256"] == latent_terminal_contract_sha256(contract)
    population = contract["population"]
    assert population["counts"] == {
        "cells": EXPECTED_CELL_COUNT,
        "closed_lifecycles": EXPECTED_LIFECYCLE_COUNT,
        "observed_assays": EXPECTED_ASSAY_COUNT,
        "observed_discards": EXPECTED_DISCARD_COUNT,
        "accepted_primitive_operations": 889,
        "shadow_evaluations_planned": EXPECTED_DISCARD_COUNT,
        "agent_provider_calls_planned": 0,
    }
    assert population["arm_counts"] == EXPECTED_ARM_COUNTS
    assert population["latent_outcomes_accessed"] is False
    assert population["hidden_states_accessed"] is False


def test_population_enumerates_all_36_unique_discard_units() -> None:
    population = build_latent_terminal_contract(ROOT)["population"]
    cells = population["cells"]
    assert len(cells) == 10
    discards = [unit for cell in cells for unit in cell["discard_units"]]
    assays = [unit for cell in cells for unit in cell["observed_assays"]]
    assert len(discards) == 36
    assert len(assays) == 24
    assert len({unit["discard_id"] for unit in discards}) == 36
    assert all(
        unit["shadow_outcome_status_at_freeze"] == "unobserved"
        for unit in discards
    )
    assert all(len(unit["public_prefix_sha256"]) == 64 for unit in discards)
    assert all(len(unit["terminal_action_sha256"]) == 64 for unit in discards)
    assert all(
        unit["discard_id"].endswith(f"terminal-step-{unit['terminal_step']:03d}")
        for unit in discards
    )
    assert all(len(cell["terminal_sequence"]) == 6 for cell in cells)
    assert all(cell["observed_assay_count"] >= 1 for cell in cells)
    assert all(0.0 <= cell["campaign_best_assayed_score"] <= 1.0 for cell in cells)


def test_contract_binds_all_existing_terminal_evidence() -> None:
    bindings = build_latent_terminal_contract(ROOT)["evidence_bindings"]
    assert bindings["campaign_audit_sha256"] == FROZEN_CAMPAIGN_AUDIT_SHA256
    assert bindings["matrix_manifest_sha256"] == FROZEN_MATRIX_MANIFEST_SHA256
    assert bindings["public_archive_sha256"] == FROZEN_PUBLIC_ARCHIVE_SHA256
    assert bindings["terminal_file_index_sha256"] == FROZEN_TERMINAL_INDEX_SHA256
    assert bindings["complete_system_comparison_sha256"] == FROZEN_COMPARISON_SHA256
    assert bindings["source_manifest_sha256"]
    assert len(bindings["source_manifest"]) == 8


def test_thresholds_estimands_and_entry_rules_are_outcome_independent() -> None:
    contract = build_latent_terminal_contract(ROOT)
    reference = contract["quality_reference"]
    assert reference["primary_near_best_fraction"] == PRIMARY_RELATIVE_THRESHOLD
    assert reference["primary_threshold_formula"] == "q_c = 0.90 B_c"
    assert reference["registered_absolute_threshold"] == REGISTERED_TASK_THRESHOLD
    assert contract["sensitivity_analysis"]["relative_near_best_fractions"] == list(
        RELATIVE_THRESHOLD_SENSITIVITY
    )
    estimand_ids = [item["estimand_id"] for item in contract["estimands"]]
    assert estimand_ids == [
        "latent_terminal_score",
        "discard_to_observed_best_delta",
        "positive_discard_regret",
        "campaign_oracle_regret",
        "false_discard_fraction",
        "assay_commitment_precision",
        "assay_commitment_recall",
        "decision_time_discard_regret",
    ]
    entry = contract["entry_rules"]
    assert entry["result_direction_gate"] is False
    assert entry["significance_gate"] is False
    assert entry["arm_difference_gate"] is False
    assert entry["threshold_selection_after_outcomes"] is False
    assert contract["missingness_and_failure"][
        "all_36_required_for_primary_point_estimates"
    ] is True
    assert contract["missingness_and_failure"]["complete_case_primary_allowed"] is False


def test_counterfactual_is_read_only_evaluator_work_not_an_agent_action() -> None:
    rule = build_latent_terminal_contract(ROOT)["counterfactual_terminal_rule"]
    assert rule["evaluator_only"] is True
    assert rule["public_agent_action"] is False
    assert rule["additional_process_operations_allowed"] == []
    assert rule["branch_accounting"] == {
        "original_trajectory_mutated": False,
        "original_resource_ledger_mutated": False,
        "shadow_branch_receipt_required": True,
        "shadow_evaluations": 36,
        "agent_provider_calls": 0,
        "count_as_original_agent_experiment": False,
        "count_as_agent_assay_decision": False,
    }
    assert rule["terminal_noise"]["borrow_noise_from_observed_assays"] is False


def test_validator_rejects_population_threshold_and_freeze_tampering() -> None:
    original = build_latent_terminal_contract(ROOT)

    bad_count = deepcopy(original)
    bad_count["population"]["counts"]["observed_discards"] = 35
    bad_count["contract_sha256"] = latent_terminal_contract_sha256(bad_count)
    assert "population counts are not the frozen census" in validate_latent_terminal_contract(
        bad_count
    )

    bad_threshold = deepcopy(original)
    bad_threshold["quality_reference"]["primary_near_best_fraction"] = 0.95
    bad_threshold["contract_sha256"] = latent_terminal_contract_sha256(bad_threshold)
    assert "primary near-best threshold changed" in validate_latent_terminal_contract(
        bad_threshold
    )

    leaked = deepcopy(original)
    leaked["freeze"]["latent_outcomes_read"] = True
    leaked["contract_sha256"] = latent_terminal_contract_sha256(leaked)
    assert "L01 freeze boundary was crossed" in validate_latent_terminal_contract(leaked)


def test_committed_machine_contract_matches_deterministic_rebuild() -> None:
    committed = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    rebuilt = build_latent_terminal_contract(ROOT)
    assert committed == rebuilt
    assert validate_latent_terminal_contract(committed, root=ROOT) == []
