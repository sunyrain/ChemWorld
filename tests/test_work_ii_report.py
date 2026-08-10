from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_formal import authorize_formal_preflight, build_formal_preflight
from chemworld.eval.work_ii_report import build_formal_analysis_dataset
from chemworld.eval.work_ii_truth import build_evaluator_truth_plan

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def _authorized_manifest() -> dict[str, object]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    return authorize_formal_preflight(
        manifest,
        qualification_receipt_sha256="a" * 64,
        preregistration_freeze_receipt_sha256="b" * 64,
        formal_cost_contract_sha256="c" * 64,
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
        plan = build_evaluator_truth_plan(
            cell,
            config,
            formal_result=True,
            formal_preflight_sha256=str(manifest["preflight_sha256"]),
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
    assert dataset["retained_cell_count"] == 75
    assert dataset["cluster_contrast_count"] == 25
    assert dataset["state_counts"] == {
        "completed": 0,
        "failed": 75,
        "right_censored": 0,
    }
    assert dataset["evaluator_truth_execution_count"] == 100
    assert dataset["evaluator_truth_query_metric_count"] == 340
    assert dataset["blind_scheduled_execution_count"] == 450
    assert dataset["blind_completed_execution_count"] == 0
    assert dataset["blind_failed_or_unstarted_execution_count"] == 450
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
