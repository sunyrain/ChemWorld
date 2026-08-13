from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from scripts.audit_work_ii_formal_design import (
    EXPECTED_TASKS,
    _public_selection,
    _self_hash,
)

from chemworld.eval.work_ii_formal import (
    EXPECTED_METHOD_QUALIFICATION_CONTRACT,
    EXPECTED_PARTICIPANT_EXECUTION_CONTRACT,
)

ROOT = Path(__file__).resolve().parents[1]


def _design() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json").read_text(encoding="utf-8")
    )


def _design_v02() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json").read_text(
            encoding="utf-8"
        )
    )


def test_public_formal_world_selection_is_reproducible_and_unique() -> None:
    design = _design()
    cohort = design["world_cohort"]
    public = cohort["public_formal"]
    selected = _public_selection(
        task_ids=EXPECTED_TASKS,
        key=public["selection_key"],
        namespace_start=public["namespace_start"],
        namespace_size=public["namespace_size"],
        worlds_per_task=public["worlds_per_task"],
    )
    assert selected == public["task_world_seeds"]
    flattened = [seed for seeds in selected.values() for seed in seeds]
    assert len(flattened) == len(set(flattened)) == 25
    assert not set(flattened) & set(cohort["development_and_qualification"]["world_seeds"])


def test_formal_design_freezes_five_tasks_three_arms_and_seventy_five_cells() -> None:
    design = _design()
    assert tuple(item["task_id"] for item in design["tasks"]) == EXPECTED_TASKS
    assert design["prior_arms"] == [
        "opaque",
        "aligned_nominal",
        "misindexed_nominal",
    ]
    assert design["world_cohort"]["public_formal"]["participant_cell_count"] == 75
    assert design["campaign_contract"]["complete_experiments_per_cell"] == 8
    assert design["campaign_contract"]["checkpoint_complete_experiments"] == [0, 2, 4, 6, 8]
    assert design["campaign_contract"]["minimum_unique_recipes_per_cell"] == 6
    assert design["campaign_contract"]["maximum_participant_selected_exact_repeats_per_cell"] == 2
    assert design["campaign_contract"]["matched_evidence_probe_in_primary_matrix"] is False
    assert design["participant_execution_contract"] == EXPECTED_PARTICIPANT_EXECUTION_CONTRACT
    assert design["method_qualification_contract"] == EXPECTED_METHOD_QUALIFICATION_CONTRACT
    assert design["participant_execution_contract"]["separate_reported_denominators"] == [
        "host_provider_process_attempt",
        "provider_session",
        "mcp_tool_call",
        "operation_attempt",
        "committed_operation",
        "complete_experiment",
        "participant_cell",
        "blind_evaluator_execution",
    ]


def test_ae_prior_qualification_is_multimetric_two_region_and_fail_closed() -> None:
    contract = _design()["prior_distinguishability_qualification_contract"]
    assert contract["participant_provider_calls"] == 0
    assert contract["participant_outcomes_used"] is False
    assert len(contract["frozen_counterevidence_regions"]) == 2
    assert (
        contract["region_pass_rules"][
            "minimum_mean_normalized_L1_metric_vector_separation"
        ]
        > 0
    )
    assert contract["region_pass_rules"]["minimum_paired_noise_signal_to_noise_ratio"] > 0
    assert contract["world_pass_rules"]["eight_round_falsifiability_required"] is True
    assert contract["task_pass_rule"] == "all_five_frozen_public_worlds_pass"
    assert "qualification_report_missing_or_stale" in contract["fail_closed_conditions"]


def test_full_program_and_w2_26_gates_fail_closed_before_as_admission() -> None:
    design = _design()
    program = design["full_program_protocol_contract"]
    assert program["primary_registered_scope"] == "C2"
    assert set(program["C2"]["blocks"]) == {"A_E", "A_P", "A_S"}
    assert program["C2"]["partial_AE_launch_while_AP_or_AS_can_still_change_runtime"] is False
    assert program["C3"]["conditional"] is True
    assert program["C4"]["conditional"] is True

    calibration = design["resource_calibration_contract"]
    assert calibration["status"] == "not_ready_fail_closed"
    assert [row["rounds"] for row in calibration["triplets"]] == [8, 10, 12]
    assert calibration["triplets"][2]["representative_task_status"] == (
        "pending_two_terminal_AS_admissions"
    )
    assert calibration["twelve_round_proxy_substitution_before_AS_selection_forbidden"] is True


def test_v02_resource_calibration_contract_covers_every_c2_task() -> None:
    calibration = _design_v02()["resource_calibration_contract"]
    triplets = calibration["task_triplets"]
    assert calibration["manifest"].endswith("manifest_v0.2.json")
    assert len(triplets) == 9
    assert [row["rounds"] for row in triplets] == [8, 8, 8, 8, 8, 10, 10, 12, 12]
    assert len({(row["locus"], row["task_id"], row["rounds"]) for row in triplets}) == 9
    assert calibration["expected_denominators"]["complete_experiments"] == 252
    assert calibration["cross_task_or_same_round_proxy_substitution_forbidden"] is True


def test_static_design_audit_cannot_claim_prior_qualification_pass(
    tmp_path: Path, monkeypatch
) -> None:
    from scripts import audit_work_ii_formal_design as audit_module

    monkeypatch.setattr(audit_module, "_run_score", lambda *args, **kwargs: 0.5)

    # A missing private seal already makes this invocation fail, but the important
    # invariant is independent: the strengthened scientific gate is never reported
    # as passed by legacy scalar reachability diagnostics.
    report = audit_module.audit(
        ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json",
        output_path=tmp_path / "audit.json",
        private_seal_path=None,
        create_private_seal=False,
    )
    qualification = report["prior_distinguishability_qualification"]
    assert qualification["status"] == "pending_provider_free_qualification_execution"
    assert qualification["formal_execution_gate_satisfied"] is False
    assert report["audit_sha256"] == _self_hash(report, "audit_sha256")

    tampered = deepcopy(report)
    tampered["status"] = "passed"
    assert tampered["audit_sha256"] != _self_hash(tampered, "audit_sha256")
