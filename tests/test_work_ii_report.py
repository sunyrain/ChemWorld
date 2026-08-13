from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_cost as work_ii_cost
import chemworld.eval.work_ii_formal as work_ii_formal
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_cost import build_formal_cost_contract
from chemworld.eval.work_ii_formal import authorize_formal_preflight, build_formal_preflight
from chemworld.eval.work_ii_report import build_formal_analysis_dataset
from chemworld.eval.work_ii_truth import build_evaluator_truth_plan

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


@pytest.fixture(autouse=True)
def _qualified_formal_prerequisites(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(work_ii_formal, "_validate_environment_binding", lambda *_: [])
    # Binding integrity is covered by the formal-runner suite.  This module's
    # virtual C2 artifacts isolate downstream report denominator semantics.
    monkeypatch.setattr(work_ii_formal, "validate_formal_bindings", lambda *_: [])
    monkeypatch.setattr(work_ii_cost, "validate_formal_bindings", lambda *_: [])

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
    terminal_specs = []
    task_rows = {"A_P": [], "A_S": []}
    for locus, tasks in roster.items():
        for task_id, config_path in tasks:
            binding = {
                "path": config_path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(config_path),
            }
            selection = {
                "path": config_path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(config_path),
                "embedded_sha256": canonical_json_sha256(
                    {"locus": locus, "task_id": task_id, "protected": True}
                ),
            }
            terminal_specs.append(
                {
                    "c2_locus": locus,
                    "task_id": task_id,
                    "campaign_config": binding,
                    "task_admission_receipt": binding,
                    "outcome_blind_selection": selection,
                }
            )
            task_rows[locus].append({"task_id": task_id, "passed": True})

    def ready_c2(_root, _plan, _design, cells):
        report = {
            "schema_version": "chemworld-work-ii-c2-admission-report-0.1",
            "status": "ready_for_formal_authorization",
            "formal_execution_allowed": True,
            "blocking_requirements": [],
            "evidence_validation_errors": [],
            "plan_binding": {
                "path": Path(_plan).resolve().relative_to(_root).as_posix(),
            },
            "blocks": {
                "A_E": {"public_schedule": {
                    "public_schedule_cell_count": len(cells),
                    "public_schedule_sha256": canonical_json_sha256(cells),
                }},
                "A_P": {"task_admissions": task_rows["A_P"], "passed": True},
                "A_S": {"task_admissions": task_rows["A_S"], "passed": True},
            },
        }
        report["admission_sha256"] = canonical_json_sha256(report)
        return report

    monkeypatch.setattr(work_ii_formal, "build_c2_admission_report", ready_c2)
    monkeypatch.setattr(work_ii_formal, "validate_c2_admission_report", lambda *_: [])
    monkeypatch.setattr(
        work_ii_formal,
        "_resolve_c2_terminal_task_specs",
        lambda *_: (deepcopy(terminal_specs), []),
    )


def _authorized_manifest() -> dict[str, object]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    qualification = {
        "schema_version": "chemworld-work-ii-method-qualification-receipt-0.4",
        "status": "passed",
        "formal_execution_authorized": False,
        "qualification_manifest_sha256": "q" * 64,
    }
    qualification["receipt_sha256"] = canonical_json_sha256(qualification)
    cost = build_formal_cost_contract(
        ROOT,
        manifest,
        formal_currency_ceiling_usd=30.0,
        pricing_source="https://provider.example/pricing",
        pricing_observed_at="2026-08-10T12:00:00+08:00",
        cache_hit_input_usd_per_million=0.0028,
        cache_miss_input_usd_per_million=0.14,
        output_usd_per_million=0.28,
    )
    freeze = {
        "schema_version": "chemworld-work-ii-preregistration-freeze-receipt-0.2",
        "status": "passed_final_freeze",
        "formal_execution_authorized": True,
        "bindings": {
            "formal_preflight_sha256": manifest["preflight_sha256"],
            "method_qualification": {
                "receipt_sha256": qualification["receipt_sha256"],
                "manifest_sha256": qualification["qualification_manifest_sha256"],
            },
        },
        "formal_currency_budget": cost,
    }
    freeze["receipt_sha256"] = canonical_json_sha256(freeze)
    return authorize_formal_preflight(
        manifest,
        qualification_receipt=qualification,
        preregistration_freeze_receipt=freeze,
        formal_cost_contract=cost,
    )


def _failed_receipt(cell: dict[str, object]) -> dict[str, object]:
    result = {
        "return_code": 1,
        "summary": None,
        "report": None,
        "trajectory": None,
        "blind_evaluation_plan": None,
        "completed": False,
        "analysis": {"operation_attempt_count": 0, "belief_snapshots": []},
        "method_resources": {},
        "exact_replay": {"verified": False},
        "qualification": {"passed": False},
        "provider_receipt_count": 0,
    }
    receipt: dict[str, object] = {
        "schema_version": "chemworld-work-ii-formal-cell-receipt-0.1",
        "cell_key_sha256": cell["cell_key_sha256"],
        "cell": cell,
        "state": "failed",
        "reason_domain": "method",
        "reason_code": "method_failed_unscorable_before_first_operation",
        "result": result,
        "result_sha256": canonical_json_sha256(result),
    }
    receipt["receipt_sha256"] = canonical_json_sha256(receipt)
    return receipt


def _truth_packs(manifest: dict[str, object]) -> dict[str, dict[str, object]]:
    packs: dict[str, dict[str, object]] = {}
    seen: set[str] = set()
    for cell in manifest["cells"]:
        cluster_id = str(cell["world_cluster_id"])
        if cluster_id in seen:
            continue
        seen.add(cluster_id)
        config = json.loads(
            (ROOT / str(cell["campaign_config_path"])).read_text(encoding="utf-8")
        )
        plan_cell = cell
        plan_config = config
        if str(cell["task_id"]).startswith("c2-"):
            # Synthetic C2 task identities test locus-qualified report grouping.
            # Compile their default four-query action layer through a real task,
            # then restore the synthetic identity before self-hashing the plan.
            plan_cell = dict(cell)
            plan_cell["task_id"] = "electrochemical-conversion"
            plan_config = dict(config)
            plan_config["task_id"] = "electrochemical-conversion"
        plan = build_evaluator_truth_plan(
            plan_cell,
            plan_config,
            formal_result=True,
            formal_preflight_sha256=str(manifest["preflight_sha256"]),
        )
        if plan_cell is not cell:
            plan["task_id"] = cell["task_id"]
            plan["plan_sha256"] = canonical_json_sha256(
                {key: value for key, value in plan.items() if key != "plan_sha256"}
            )
        truth = {
            query["query_id"]: dict.fromkeys(query["metric_ids"], 0.5)
            for query in plan["queries"]
        }
        report: dict[str, object] = {
            "schema_version": "chemworld-work-ii-evaluator-truth-report-0.1",
            "formal_result": True,
            "formal_preflight_sha256": manifest["preflight_sha256"],
            "plan_sha256": plan["plan_sha256"],
            "world_cluster_id": cluster_id,
            "task_id": plan["task_id"],
            "world_seed": plan["world_seed"],
            "status": "completed",
            "truth_query_count": 4,
            "completed_truth_query_count": 4,
            "failed_truth_query_count": 0,
            "truth_query_metric_count": plan["truth_query_metric_count"],
            "completed_truth_query_metric_count": plan[
                "truth_query_metric_count"
            ],
            "evaluator_provider_call_count": 0,
            "participant_operation_denominator_impact": 0,
            "participant_feedback_emitted": False,
            "truth": truth,
            "receipts": [{"status": "completed"} for _ in range(4)],
        }
        report["report_sha256"] = canonical_json_sha256(report)
        packs[cluster_id] = {"plan": plan, "report": report}
    return packs


def test_formal_analysis_dataset_retains_failed_cells_and_zero_improvement() -> None:
    manifest = _authorized_manifest()
    receipts = [_failed_receipt(cell) for cell in manifest["cells"]]
    dataset = build_formal_analysis_dataset(
        manifest,
        receipts,
        _truth_packs(manifest),
        {},
    )
    assert dataset["status"] == "passed"
    assert dataset["errors"] == []
    assert dataset["retained_cell_count"] == 135
    assert dataset["cluster_contrast_count"] == 45
    assert dataset["state_counts"] == {
        "completed": 0,
        "failed": 135,
        "right_censored": 0,
    }
    assert dataset["evaluator_truth_execution_count"] == 180
    assert dataset["evaluator_truth_query_metric_count"] == 580
    assert dataset["expected_cell_count"] == 135
    assert dataset["expected_cluster_count"] == 45
    assert dataset["blind_scheduled_execution_count"] == 810
    assert dataset["blind_completed_execution_count"] == 0
    assert dataset["blind_failed_or_unstarted_execution_count"] == 810
    assert all(
        row["final_law_summary"]["status"] == "missing_final_law_summary"
        for row in dataset["cell_rows"]
    )
    assert all(row["H3_primary_contrast"] == 0.0 for row in dataset["cluster_rows"])
    assert dataset["dataset_sha256"] == canonical_json_sha256(
        {key: value for key, value in dataset.items() if key != "dataset_sha256"}
    )


def test_formal_analysis_dataset_rejects_tampered_terminal_receipt() -> None:
    manifest = _authorized_manifest()
    receipts = [_failed_receipt(cell) for cell in manifest["cells"]]
    tampered = deepcopy(receipts)
    tampered[0]["reason_code"] = "method_failed_tampered"
    dataset = build_formal_analysis_dataset(
        manifest,
        tampered,
        _truth_packs(manifest),
        {},
    )
    assert dataset["status"] == "failed"
    assert any("self-hash mismatch" in error for error in dataset["errors"])


def test_formal_analysis_dataset_rejects_malformed_present_process_profile() -> None:
    manifest = _authorized_manifest()
    receipts = [_failed_receipt(cell) for cell in manifest["cells"]]
    result = receipts[0]["result"]
    result["analysis"]["process_profile"] = {"profile_sha256": "tampered"}
    receipts[0]["result_sha256"] = canonical_json_sha256(result)
    receipts[0]["receipt_sha256"] = canonical_json_sha256(
        {
            key: value
            for key, value in receipts[0].items()
            if key != "receipt_sha256"
        }
    )
    dataset = build_formal_analysis_dataset(
        manifest,
        receipts,
        _truth_packs(manifest),
        {},
    )
    assert dataset["status"] == "failed"
    assert any("process profile" in error for error in dataset["errors"])
