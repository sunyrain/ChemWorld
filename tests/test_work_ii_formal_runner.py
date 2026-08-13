from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import ClassVar

import pytest
import scripts.run_work_ii_campaign_pilot as campaign_runner
import scripts.run_work_ii_formal_matrix as formal_runner

import chemworld.eval.work_ii_formal as work_ii_formal
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_blind import BLIND_EVALUATOR_VERSION
from chemworld.eval.work_ii_c2_admission import (
    C2_OUTCOME_BLIND_SELECTION_VERSION,
    C2_TASK_ADMISSION_RECEIPT_VERSION,
    c2_outcome_blind_selection_sha256,
    c2_task_admission_receipt_sha256,
)
from chemworld.eval.work_ii_cost import build_formal_cost_contract
from chemworld.eval.work_ii_formal import (
    EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
    FORMAL_ARMS,
    FORMAL_C2_LOCUS_CONTRACT,
    DuplicateFormalCellError,
    InvalidFormalCellReceiptError,
    ProviderAttemptLimitError,
    WorkIIFormalCellStore,
    authorize_formal_preflight,
    build_checkpoint_contract,
    build_formal_preflight,
    validate_formal_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
_VALIDATE_ENVIRONMENT_BINDING = work_ii_formal._validate_environment_binding
_BUILD_C2_ADMISSION_REPORT = work_ii_formal.build_c2_admission_report


@pytest.fixture(autouse=True)
def _isolate_runner_contract_from_current_gate_a_recertification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Runner unit tests use a qualified environment fixture.

    Current-repository Gate A freshness is tested separately below; the rest of
    this module exercises cell/store behavior independently of that external
    qualification state.
    """

    monkeypatch.setattr(work_ii_formal, "_validate_environment_binding", lambda *_: [])

    fixtures = ROOT / "tests/fixtures"
    roster = {
        "A_P": (
            ("c2-shared-task", fixtures / "work_ii_formal_c2_ap_shared.json"),
            ("c2-parametric-task", fixtures / "work_ii_formal_c2_ap_unique.json"),
        ),
        "A_S": (
            ("c2-shared-task", fixtures / "work_ii_formal_c2_as_shared.json"),
            ("c2-structural-task", fixtures / "work_ii_formal_c2_as_unique.json"),
        ),
    }

    def _binding(path: Path, embedded: str | None = None) -> dict[str, object]:
        value: dict[str, object] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(path),
        }
        if embedded is not None:
            value["embedded_sha256"] = embedded
        return value

    task_rows: dict[str, list[dict[str, object]]] = {"A_P": [], "A_S": []}
    virtual_payloads: dict[Path, dict[str, object]] = {}
    for locus, tasks in roster.items():
        for task_id, config_path in tasks:
            selection_path = config_path.with_name(f"{config_path.stem}_selection.json")
            selection = json.loads(selection_path.read_text(encoding="utf-8"))
            # The current C2 contract requires proof that both the protected
            # protocol and its action-layer selection rule were frozen before
            # evidence review.  These virtual fixtures exercise downstream
            # formal scheduling, so materialize that current receipt field.
            selection["selection_rule_frozen_before_evidence_review"] = True
            selection["schema_version"] = C2_OUTCOME_BLIND_SELECTION_VERSION
            selection["selection_sha256"] = c2_outcome_blind_selection_sha256(selection)
            virtual_payloads[selection_path.resolve()] = selection
            selection_binding = {
                "path": selection_path.relative_to(ROOT).as_posix(),
                "sha256": canonical_json_sha256(selection),
                "embedded_sha256": selection["selection_sha256"],
            }
            receipt = {
                "schema_version": C2_TASK_ADMISSION_RECEIPT_VERSION,
                "status": "passed_terminal_task_admission",
                "formal_result": False,
                "terminal_qualification_passed": True,
                "locus": locus,
                "task_id": task_id,
                "complete_experiments_per_cell": 10 if locus == "A_P" else 12,
                "campaign_config_binding": _binding(config_path),
                "outcome_blind_selection_binding": selection_binding,
                "participant_outcomes_used_for_selection": False,
                "formal_participant_outcomes_observed": 0,
                "validation_errors": [],
            }
            receipt["receipt_sha256"] = c2_task_admission_receipt_sha256(receipt)
            receipt_path = selection_path.with_name(
                selection_path.name.replace("_selection.json", "_receipt.json")
            )
            virtual_payloads[receipt_path.resolve()] = receipt
            task_rows[locus].append(
                {
                    "task_id": task_id,
                    "receipt_binding": {
                        "path": receipt_path.relative_to(ROOT).as_posix(),
                        "sha256": canonical_json_sha256(receipt),
                        "embedded_sha256": receipt["receipt_sha256"],
                    },
                    "passed": True,
                }
            )

    original_load = work_ii_formal._load_object
    original_file_sha = work_ii_formal.file_sha256
    original_bound_object = work_ii_formal._bound_object

    def _virtual_load(path: Path) -> dict[str, object]:
        payload = virtual_payloads.get(path.resolve())
        return deepcopy(payload) if payload is not None else original_load(path)

    def _virtual_file_sha(path: Path) -> str:
        payload = virtual_payloads.get(Path(path).resolve())
        return canonical_json_sha256(payload) if payload is not None else original_file_sha(path)

    def _virtual_bound_object(root, binding, **kwargs):
        relative = binding.get("path")
        path = (root / relative).resolve() if isinstance(relative, str) else None
        payload = virtual_payloads.get(path) if path is not None else None
        if payload is not None and str(path).endswith("_receipt.json"):
            return deepcopy(payload), []
        return original_bound_object(root, binding, **kwargs)

    monkeypatch.setattr(work_ii_formal, "_load_object", _virtual_load)
    monkeypatch.setattr(work_ii_formal, "file_sha256", _virtual_file_sha)
    monkeypatch.setattr(work_ii_formal, "_bound_object", _virtual_bound_object)

    def _ready_c2(root, plan, design, cells):
        del design
        report = {
            "schema_version": "chemworld-work-ii-c2-admission-report-0.1",
            "status": "ready_for_formal_authorization",
            "formal_execution_allowed": True,
            "blocking_requirements": [],
            "evidence_validation_errors": [],
            "plan_binding": {
                "path": Path(plan).resolve().relative_to(root).as_posix(),
                "sha256": file_sha256(Path(plan)),
            },
            "blocks": {
                "A_E": {
                    "public_schedule": {
                        "public_schedule_cell_count": len(cells),
                        "public_schedule_sha256": canonical_json_sha256(cells),
                    }
                },
                "A_P": {"task_admissions": task_rows["A_P"], "passed": True},
                "A_S": {"task_admissions": task_rows["A_S"], "passed": True},
            },
        }
        report["admission_sha256"] = canonical_json_sha256(report)
        return report

    monkeypatch.setattr(work_ii_formal, "build_c2_admission_report", _ready_c2)
    monkeypatch.setattr(work_ii_formal, "validate_c2_admission_report", lambda *_: [])


def test_formal_environment_gate_rejects_stale_runtime_bound_certificates() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    errors = _VALIDATE_ENVIRONMENT_BINDING(ROOT, design)
    assert "current Gate A certificates do not bind the current runtime semantics" in errors

    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    report["prerequisite_errors"] = errors
    report["status"] = "failed_execution_blocked"
    report["preflight_sha256"] = canonical_json_sha256(
        {key: value for key, value in report.items() if key != "preflight_sha256"}
    )
    assert validate_formal_preflight(report) == []
    with pytest.raises(ValueError, match="unresolved prerequisite failures"):
        authorize_formal_preflight(
            report,
            **_authorization_evidence(report),
        )


def test_current_c2_plan_fails_closed_without_terminal_task_receipts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        work_ii_formal,
        "build_c2_admission_report",
        _BUILD_C2_ADMISSION_REPORT,
    )
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)

    assert report["formal_execution_allowed"] is False
    assert report["schedule_policy"]["schedule_complete"] is False
    assert report["expected_counts"]["participant_cells"] == 75
    assert report["expected_counts"]["participant_cells_by_c2_locus"] == {
        "A_E": 75,
        "A_P": 0,
        "A_S": 0,
    }
    assert all(cell["c2_locus"] == "A_E" for cell in report["cells"])
    assert any(
        "terminal task receipts" in error
        for error in report["prerequisite_errors"]
    )
    assert validate_formal_preflight(report) == []


def _fake_blind_plan(cell: dict[str, object]) -> dict[str, object]:
    target_digests = {
        "observed_incumbent": "a" * 64,
        "participant_final_recommendation": "b" * 64,
    }
    targets = [
        {"target": target, "action_plan_sha256": digest}
        for target, digest in target_digests.items()
    ]
    executions = []
    for target, digest in target_digests.items():
        for replicate_index in range(1, 4):
            executions.append(
                {
                    "target": target,
                    "replicate_index": replicate_index,
                    "action_plan_sha256": digest,
                    "paired_noise_id_sha256": f"paired-{replicate_index}",
                    "observation_seed": replicate_index,
                    "observation_noise_namespace": f"namespace-{replicate_index}",
                }
            )
    plan: dict[str, object] = {
        "schema_version": BLIND_EVALUATOR_VERSION,
        "cell_key_sha256": cell["cell_key_sha256"],
        "evaluator_provider_call_count": 0,
        "participant_operation_denominator_impact": 0,
        "participant_feedback_allowed": False,
        "targets": targets,
        "executions": executions,
    }
    plan["plan_sha256"] = canonical_json_sha256(plan)
    return plan


def _authorization_evidence(manifest: dict[str, object]) -> dict[str, object]:
    base = manifest["preflight_sha256"]
    qualification = {
        "schema_version": "chemworld-work-ii-method-qualification-receipt-0.4",
        "status": "passed",
        "formal_execution_authorized": False,
        "qualification_manifest_sha256": "q" * 64,
    }
    qualification["receipt_sha256"] = canonical_json_sha256(qualification)
    cost = {
        "schema_version": "chemworld-work-ii-formal-cost-contract-0.1",
        "formal_preflight_sha256": base,
    }
    cost["formal_cost_contract_sha256"] = canonical_json_sha256(cost)
    freeze = {
        "schema_version": "chemworld-work-ii-preregistration-freeze-receipt-0.2",
        "status": "passed_final_freeze",
        "formal_execution_authorized": True,
        "bindings": {
            "formal_preflight_sha256": base,
            "method_qualification": {
                "receipt_sha256": qualification["receipt_sha256"],
                "manifest_sha256": qualification["qualification_manifest_sha256"],
            },
        },
        "formal_currency_budget": cost,
    }
    freeze["receipt_sha256"] = canonical_json_sha256(freeze)
    return {
        "qualification_receipt": qualification,
        "preregistration_freeze_receipt": freeze,
        "formal_cost_contract": cost,
    }


def _authorized_manifest() -> dict[str, object]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    return authorize_formal_preflight(manifest, **_authorization_evidence(manifest))


def _formal_cost_contract(manifest: dict[str, object]) -> dict[str, object]:
    return build_formal_cost_contract(
        ROOT,
        manifest,
        formal_currency_ceiling_usd=30.0,
        pricing_source="https://api-docs.deepseek.com/quick_start/pricing",
        pricing_observed_at="2026-08-10T12:00:00+08:00",
        cache_hit_input_usd_per_million=0.0028,
        cache_miss_input_usd_per_million=0.14,
        output_usd_per_million=0.28,
    )


class _FakeFormalCellProcess:
    fail_once_keys: ClassVar[set[str]] = set()
    partial_once_keys: ClassVar[set[str]] = set()
    spawn_fail_once_keys: ClassVar[set[str]] = set()
    launched_keys: ClassVar[list[str]] = []

    def __init__(self, command, **kwargs) -> None:
        del kwargs
        key = command[command.index("--formal-cell-key") + 1]
        self.launched_keys.append(key)
        if key in self.spawn_fail_once_keys:
            self.spawn_fail_once_keys.remove(key)
            raise OSError("simulated provider process launch failure")
        output = Path(command[command.index("--output") + 1])
        manifest_path = Path(command[command.index("--formal-manifest") + 1])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        cell = next(row for row in manifest["cells"] if row["cell_key_sha256"] == key)
        if key in self.fail_once_keys:
            self.fail_once_keys.remove(key)
            self.return_code = 2
            return
        if key in self.partial_once_keys:
            self.partial_once_keys.remove(key)
            output.mkdir(parents=True)
            (output / "trajectory.jsonl").write_text("{}\n{", encoding="utf-8")
            self.return_code = 2
            return
        output.mkdir(parents=True)
        arm = cell["prior_arm"]
        completed = arm == "opaque"
        operation_attempt_count = 8 if completed else 2 if arm == "aligned_nominal" else 0
        summary = {
            "formal_result": True,
            "formal_cell": cell,
            "completed": completed,
            "analysis": {"operation_attempt_count": operation_attempt_count},
            "method_resources": {"provider_session_count": 1},
            "provider_receipts": [{"session_id": "test"}],
            "exact_replay": {"verified": completed},
            "qualification": {"passed": completed},
        }
        if completed:
            plan = _fake_blind_plan(cell)
            plan.update(
                {
                    "formal_result": True,
                    "formal_preflight_sha256": manifest["preflight_sha256"],
                    "participant_operational_qualification_passed": True,
                    "development_terminal_trajectory_override": False,
                    "participant_complete_experiment_count": cell[
                        "complete_experiment_count"
                    ],
                    "candidate_experiment_indices": list(
                        range(1, cell["complete_experiment_count"] + 1)
                    ),
                }
            )
            plan["plan_sha256"] = canonical_json_sha256(
                {key: value for key, value in plan.items() if key != "plan_sha256"}
            )
            plan_path = output / "blind_evaluation_plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            summary["blind_evaluation_plan"] = {
                "sha256": file_sha256(plan_path),
                "plan_sha256": plan["plan_sha256"],
            }
        (output / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
        (output / "report.json").write_text("{}", encoding="utf-8")
        if operation_attempt_count:
            (output / "trajectory.jsonl").write_text("{}\n", encoding="utf-8")
        self.return_code = 0 if completed else 1

    def wait(self) -> int:
        return self.return_code

    def poll(self) -> int:
        return self.return_code


def test_formal_preflight_materializes_complete_135_cell_c2_denominators() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)

    assert report["status"] == "passed_execution_blocked"
    assert report["formal_result"] is False
    assert report["formal_execution_allowed"] is False
    assert report["errors"] == []
    assert validate_formal_preflight(report) == []
    assert report["expected_counts"] == {
        "tasks": 9,
        "tasks_by_c2_locus": {"A_E": 5, "A_P": 2, "A_S": 2},
        "independent_task_world_clusters": 45,
        "participant_cells": 135,
        "participant_cells_by_c2_locus": {"A_E": 75, "A_P": 30, "A_S": 30},
        "provider_sessions": 135,
        "provider_attempts_initial_planned": 135,
        "provider_attempts_hard_cap": 270,
        "provider_repeats_per_cell": 1,
        "complete_experiments": 1260,
        "belief_checkpoints": 675,
        "checkpoint_held_out_queries": 2700,
        "checkpoint_held_out_query_metrics": 8700,
        "evaluator_truth_executions": 180,
        "evaluator_truth_query_metrics": 580,
        "participant_final_recommendations": 135,
        "blind_validation_targets": 270,
        "blind_validation_executions": 810,
    }
    assert len(report["blocking_requirements"]) == 4
    assert "source_bindings" not in report
    assert (
        report["law_summary_evaluation_contract"]
        == EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT
    )
    assert report["held_out_evaluator_contract"] == {
        "truth_unit": "task_x_world_cluster_x_registered_query",
        "queries_per_task_world_cluster": 4,
        "public_matrix_truth_execution_count": 100,
        "public_matrix_truth_query_metric_count": 340,
        "shared_across_prior_arms_and_checkpoints": True,
        "one_frozen_complete_experiment_per_query": True,
        "keyed_observation_coordinate_per_query": True,
        "exact_replay_required": True,
        "failed_truth_executions_retained_without_replacement": True,
        "evaluator_provider_calls": 0,
        "participant_feedback_from_truth_evaluator": False,
        "evaluator_trajectory_separate_from_participant": True,
        "evaluator_resources_excluded_from_participant_ledger": True,
        "frozen_unregistered_controls": {
            "reaction-to-crystallization": {
                "stirring_speed_rpm": 675.0,
                "catalyst_amount_mol": 0.000315,
            },
            "reaction-to-distillation": {
                "stirring_speed_rpm": 675.0,
                "catalyst_amount_mol": 0.000315,
                "evaporation_temperature_K": 332.5,
                "evaporation_duration_s": 900.0,
                "transfer_fraction": 0.77,
            },
            "partition-discovery": {"solvent_volume_L": 0.02},
            "reaction-safety-constrained": {"stirring_speed_rpm": 675.0},
        },
        "query_field_aliases": {
            "partition-discovery": {
                "aqueous_phase_volume_L": "aqueous_volume_L"
            }
        },
    }


def test_formal_schedule_is_task_world_arm_ordered_and_unique() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    cells = report["cells"]

    assert [cell["prior_arm"] for cell in cells[:3]] == list(FORMAL_ARMS)
    assert {cell["world_cluster_id"] for cell in cells[:3]} == {
        "work-ii-public-ae-01-01"
    }
    assert cells[0]["world_seed"] == 672326802
    assert cells[74]["world_seed"] == 930008953
    assert len({cell["cell_id"] for cell in cells}) == 135
    assert len({cell["cell_key_sha256"] for cell in cells}) == 135
    assert all(cell["provider_session_limit"] == 1 for cell in cells)
    assert all(cell["provider_attempt_limit"] == 2 for cell in cells)
    assert all(cell["world_split"] == "public_formal" for cell in cells)
    assert all(cell["participant_final_recommendation_count"] == 1 for cell in cells)
    assert all(cell["blind_validation_execution_count"] == 6 for cell in cells)
    assert all(
        cell["terminal_states"] == ["completed", "right_censored", "failed"]
        for cell in cells
    )
    assert not any("private" in cell for cell in cells)


def test_formal_preflight_rejects_rehashed_cross_split_cell() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    tampered = deepcopy(report)
    cell = tampered["cells"][0]
    cell["world_split"] = "private_confirmation"
    cell["world_seed"] = 2_000_000_001
    cell["cell_key_sha256"] = canonical_json_sha256(
        {key: value for key, value in cell.items() if key != "cell_key_sha256"}
    )
    tampered["preflight_sha256"] = canonical_json_sha256(
        {
            key: value
            for key, value in tampered.items()
            if key != "preflight_sha256"
        }
    )
    errors = validate_formal_preflight(tampered)
    assert "formal preflight contains a cross-split world identity" in errors
    assert "formal preflight cell crossed the public/private boundary" in errors


def test_all_formal_task_configs_use_neutral_checkpoint_ids() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    for binding in report["task_bindings"]:
        config_path = ROOT / binding["campaign_config"]["path"]
        config = json.loads(config_path.read_text(encoding="utf-8"))
        contract = build_checkpoint_contract(config, "opaque")
        assert tuple(contract["snapshot_stages"]) == FORMAL_C2_LOCUS_CONTRACT[
            binding["c2_locus"]
        ]["snapshot_stages"]
        assert contract["physical_experiment_selection_authority"] == "participant"


def test_formal_preflight_self_hash_fails_closed() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    tampered = deepcopy(report)
    tampered["cells"][0]["world_seed"] += 1
    assert "formal preflight self-hash mismatch" in validate_formal_preflight(tampered)


def test_formal_cell_store_is_write_once_and_missing_only_resumable(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    first = manifest["cells"][0]
    first_key = first["cell_key_sha256"]

    store.record_infrastructure_failure(first_key, TimeoutError("provider timeout"))
    before = store.audit()
    assert before["terminal_count"] == 0
    assert before["infrastructure_attempt_count"] == 1
    assert len(store.pending_cells(resume=True)) == 135

    store.write_terminal(
        first_key,
        state="completed",
        reason_code="scientific_completed_qualified_campaign",
        result={"summary_sha256": "a" * 64, "exact_replay": True},
    )
    with pytest.raises(DuplicateFormalCellError):
        store.write_terminal(
            first_key,
            state="completed",
            reason_code="scientific_completed_qualified_campaign",
            result={"summary_sha256": "b" * 64, "exact_replay": True},
        )
    with pytest.raises(DuplicateFormalCellError):
        store.pending_cells(resume=False)
    pending = store.pending_cells(resume=True)
    assert len(pending) == 134
    assert all(cell["cell_key_sha256"] != first_key for cell in pending)
    assert store.load_terminal(first_key)["result"]["exact_replay"] is True
    after = store.audit()
    assert after["state_counts"]["completed"] == 1
    assert after["recovered_infrastructure_failure_count"] == 1


def test_formal_cell_store_preserves_right_censored_and_failed_cells(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    censored, failed = manifest["cells"][:2]
    store.write_terminal(
        censored["cell_key_sha256"],
        state="right_censored",
        reason_code="method_right_censored_provider_failure_after_operation",
        result={"operation_attempt_count": 3, "last_checkpoint": "pre_evidence"},
    )
    store.write_terminal(
        failed["cell_key_sha256"],
        state="failed",
        reason_code="method_failed_unscorable_before_first_operation",
        result={"operation_attempt_count": 0, "primary_improvement": 0.0},
    )
    audit = store.audit()
    assert audit["state_counts"] == {
        "completed": 0,
        "failed": 1,
        "right_censored": 1,
    }
    assert audit["terminal_count"] == 2
    assert len(audit["missing_cell_key_sha256"]) == 133


def test_formal_cell_store_enforces_two_launch_provider_attempt_cap(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    cell = manifest["cells"][0]
    key = cell["cell_key_sha256"]
    store.record_provider_attempt_launch(key, attempt_id="attempt-1")
    store.record_provider_attempt_launch(key, attempt_id="attempt-2")
    audit = store.audit()
    assert audit["provider_attempt_count"] == 2
    assert audit["provider_attempt_counts_by_cell_key_sha256"] == {key: 2}
    with pytest.raises(ProviderAttemptLimitError, match="exhausted provider attempt cap"):
        store.record_provider_attempt_launch(key, attempt_id="attempt-3")
    with pytest.raises(ProviderAttemptLimitError, match="missing formal cells exhausted"):
        store.pending_cells(resume=True)


def test_formal_cell_store_fails_closed_on_receipt_tampering(tmp_path: Path) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    store = WorkIIFormalCellStore(tmp_path / "store", manifest)
    cell = manifest["cells"][0]
    receipt = store.write_terminal(
        cell["cell_key_sha256"],
        state="completed",
        reason_code="scientific_completed_qualified_campaign",
        result={"exact_replay": True},
    )
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["result"]["exact_replay"] = False
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    audit = store.audit()
    assert audit["terminal_count"] == 0
    assert audit["invalid_receipts"] == [receipt.as_posix()]
    with pytest.raises(InvalidFormalCellReceiptError):
        store.pending_cells(resume=True)


def test_campaign_cell_formal_mode_requires_exact_authorized_binding(
    tmp_path: Path,
) -> None:
    blocked = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    cell = blocked["cells"][0]
    blocked_path = tmp_path / "blocked.json"
    blocked_path.write_text(json.dumps(blocked), encoding="utf-8")
    args = argparse.Namespace(
        formal_manifest=blocked_path,
        formal_cell_key=cell["cell_key_sha256"],
        allow_formal_execution=True,
        world_seed=cell["world_seed"],
        prior_arm=cell["prior_arm"],
    )
    with pytest.raises(RuntimeError, match="does not authorize"):
        campaign_runner._formal_cell_context(
            args,
            config_path=ROOT / cell["campaign_config_path"],
        )

    authorized = _authorized_manifest()
    authorized_cell = authorized["cells"][0]
    authorized_path = tmp_path / "authorized.json"
    authorized_path.write_text(json.dumps(authorized), encoding="utf-8")
    args.formal_manifest = authorized_path
    args.formal_cell_key = authorized_cell["cell_key_sha256"]
    context = campaign_runner._formal_cell_context(
        args,
        config_path=ROOT / authorized_cell["campaign_config_path"],
    )
    assert context is not None
    assert context[1]["cell_id"] == authorized_cell["cell_id"]
    args.world_seed += 1
    with pytest.raises(RuntimeError, match="world seed"):
        campaign_runner._formal_cell_context(
            args,
            config_path=ROOT / authorized_cell["campaign_config_path"],
        )


def test_manifest_executor_terminalizes_all_cells_without_arm_replacement(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _FakeFormalCellProcess.fail_once_keys = set()
    _FakeFormalCellProcess.partial_once_keys = set()
    _FakeFormalCellProcess.spawn_fail_once_keys = set()
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    report = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert report["status"] == "all_cells_terminal"
    assert report["terminal_count"] == 135
    assert report["state_counts"] == {
        "completed": 45,
        "failed": 45,
        "right_censored": 45,
    }
    assert len(_FakeFormalCellProcess.launched_keys) == 135
    assert len(set(_FakeFormalCellProcess.launched_keys)) == 135
    cost_ledger = json.loads(
        (output / "formal_cost_ledger.json").read_text(encoding="utf-8")
    )
    assert cost_ledger["provider_attempt_count"] == 135
    assert cost_ledger["reserved_cost_usd"] == 11.18208
    assert cost_ledger["within_ceiling"] is True
    assert report["formal_cost_ledger_sha256"] == cost_ledger[
        "formal_cost_ledger_sha256"
    ]


def test_manifest_executor_rejects_blocked_preflight_before_creating_output(
    tmp_path: Path,
) -> None:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output = tmp_path / "formal-output"
    with pytest.raises(RuntimeError, match="does not authorize"):
        formal_runner.execute_manifest(
            manifest=manifest,
            manifest_path=manifest_path,
            output_root=output,
            progress_path=tmp_path / "progress.jsonl",
            resume=False,
            cell_runner=tmp_path / "fake-cell-runner.py",
        )
    assert not output.exists()


def test_formal_execute_requires_preregistration_freeze_receipt(tmp_path: Path) -> None:
    args = argparse.Namespace(
        check=False,
        output=formal_runner.DEFAULT_PREFLIGHT,
        manifest=tmp_path / "manifest.json",
        output_root=tmp_path / "output",
        qualification_receipt=tmp_path / "qualification.json",
        qualification_manifest=tmp_path / "qualification-manifest.json",
        preregistration_freeze_receipt=None,
        formal_currency_ceiling_usd=1.0,
        progress_file=tmp_path / "progress.jsonl",
        allow_formal_execution=True,
        resume=False,
    )
    with pytest.raises(RuntimeError, match="--preregistration-freeze-receipt"):
        formal_runner._run_execute(args)


def test_manifest_executor_never_replaces_unfinalized_partial_trajectory(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    partial_key = manifest["cells"][2]["cell_key_sha256"]
    _FakeFormalCellProcess.fail_once_keys = set()
    _FakeFormalCellProcess.partial_once_keys = {partial_key}
    _FakeFormalCellProcess.spawn_fail_once_keys = set()
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    report = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert report["status"] == "all_cells_terminal"
    assert report["terminal_count"] == 135
    assert report["infrastructure_failure_count_this_attempt"] == 0
    assert report["state_counts"]["right_censored"] == 46
    assert _FakeFormalCellProcess.launched_keys.count(partial_key) == 1
    receipt = json.loads(
        (output / "store" / "terminal_receipts" / f"{partial_key}.json").read_text(
            encoding="utf-8"
        )
    )
    assert receipt["state"] == "right_censored"
    evidence = receipt["result"]["unfinalized_trajectory_evidence"]
    assert evidence["trajectory_byte_count"] > 0
    assert {key: evidence[key] for key in evidence if key != "trajectory_byte_count"} == {
        "nonempty_line_count": 2,
        "valid_json_line_count": 1,
        "malformed_or_partial_line_count": 1,
    }


def test_manifest_executor_records_process_spawn_failure_and_resumes_once(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    failed_key = manifest["cells"][2]["cell_key_sha256"]
    _FakeFormalCellProcess.fail_once_keys = set()
    _FakeFormalCellProcess.partial_once_keys = set()
    _FakeFormalCellProcess.spawn_fail_once_keys = {failed_key}
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    first = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert first["terminal_count"] == 2
    assert first["infrastructure_failure_count_this_attempt"] == 1
    assert first["missing_cell_count"] == 133
    second = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=True,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert second["status"] == "all_cells_terminal"
    assert second["terminal_count"] == 135
    assert _FakeFormalCellProcess.launched_keys.count(failed_key) == 2
    audit = json.loads((output / "store_audit.json").read_text(encoding="utf-8"))
    assert audit["provider_attempt_count"] == 136
    assert audit["provider_attempt_counts_by_cell_key_sha256"][failed_key] == 2


def test_manifest_executor_resumes_only_missing_cells_after_triplet_failure(
    monkeypatch,
    tmp_path: Path,
) -> None:
    manifest = _authorized_manifest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    failed_key = manifest["cells"][2]["cell_key_sha256"]
    _FakeFormalCellProcess.fail_once_keys = {failed_key}
    _FakeFormalCellProcess.partial_once_keys = set()
    _FakeFormalCellProcess.spawn_fail_once_keys = set()
    _FakeFormalCellProcess.launched_keys = []
    monkeypatch.setattr(formal_runner.subprocess, "Popen", _FakeFormalCellProcess)
    output = tmp_path / "formal-output"
    cost_contract = _formal_cost_contract(manifest)
    first = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=False,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert first["status"] == "infrastructure_incomplete_missing_only_resume_required"
    assert first["terminal_count"] == 2
    assert first["missing_cell_count"] == 133
    assert len(_FakeFormalCellProcess.launched_keys) == 3

    second = formal_runner.execute_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
        output_root=output,
        progress_path=tmp_path / "progress.jsonl",
        resume=True,
        cell_runner=tmp_path / "fake-cell-runner.py",
        formal_cost_contract=cost_contract,
    )
    assert second["status"] == "all_cells_terminal"
    assert second["terminal_count"] == 135
    assert len(_FakeFormalCellProcess.launched_keys) == 136
    assert _FakeFormalCellProcess.launched_keys.count(manifest["cells"][0]["cell_key_sha256"]) == 1
    assert _FakeFormalCellProcess.launched_keys.count(manifest["cells"][1]["cell_key_sha256"]) == 1
    assert _FakeFormalCellProcess.launched_keys.count(failed_key) == 2
