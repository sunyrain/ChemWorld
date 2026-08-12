from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

import chemworld.eval.work_ii_ae_prior_qualification_v02 as qualification_module
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v02 import (
    RECEIPT_VERSION,
    build_blind_policy_schedule,
    build_partial_audit,
    build_qualification_plan,
    build_qualification_report,
    validate_contract,
    validate_qualification_output,
    validate_qualification_plan,
    validate_qualification_report,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.2.json"
)
SCHEMA_PATH = (
    ROOT / "src/chemworld/schemas/work_ii_ae_prior_qualification_v02_schema.json"
)


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _plan() -> dict[str, object]:
    return build_qualification_plan(ROOT, CONTRACT_PATH)


def _rehash(payload: dict[str, object], field: str) -> None:
    payload.pop(field, None)
    payload[field] = canonical_json_sha256(payload)


def _synthetic_receipts(
    plan: dict[str, object],
    *,
    fail_construction: bool = False,
    fail_heldout_task: str | None = None,
) -> list[dict[str, object]]:
    receipts: list[dict[str, object]] = []
    for row in plan["executions"]:
        failed = (
            fail_construction
            and row["phase"] == "construction"
            and row["execution_index"] == 0
        ) or (
            fail_heldout_task is not None
            and row["phase"] == "heldout_qualification"
            and row["task_id"] == fail_heldout_task
            and row["execution_index"] == 600
        )
        receipt = deepcopy(row)
        receipt.update(
            {
                "schema_version": RECEIPT_VERSION,
                "plan_sha256": plan["plan_sha256"],
            }
        )
        if failed:
            receipt.update(
                {
                    "provider_call_count": 0,
                    "status": "failed",
                    "allowed_metrics": None,
                    "support_metrics": None,
                    "negative_control_metrics": None,
                    "exact_replay": None,
                    "trajectory": None,
                    "failure": {"type": "SyntheticFailure", "message": "test"},
                }
            )
        else:
            # The moved-pair contrast is 0.20 for every support/control metric.
            value = 0.10 + 0.10 * int(row["target_category"])
            metrics = dict.fromkeys(row["allowed_metric_ids"], value)
            receipt.update(
                {
                    "provider_call_count": 0,
                    "status": "completed",
                    "allowed_metrics": metrics,
                    "support_metrics": {
                        metric: metrics[metric] for metric in row["support_metric_ids"]
                    },
                    "negative_control_metrics": {
                        metric: metrics[metric]
                        for metric in row["negative_control_metric_ids"]
                    },
                    "exact_replay": {"verified": True},
                    "trajectory": {
                        "path": f"executions/{row['execution_index']}/trajectory.jsonl",
                        "sha256": "a" * 64,
                    },
                    "failure": None,
                }
            )
        receipt["receipt_sha256"] = canonical_json_sha256(receipt)
        receipts.append(receipt)
    return receipts


def test_contract_and_plan_freeze_exact_denominators_and_heldout_namespace() -> None:
    contract = _contract()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    plan = _plan()

    assert validate_contract(ROOT, contract) == []
    assert schema["properties"]["schema_version"]["const"] == contract[
        "schema_version"
    ]
    assert validate_qualification_plan(ROOT, plan, contract) == []
    assert plan["denominators"] == {
        "tasks": 5,
        "task_worlds_total": 50,
        "construction_task_worlds": 25,
        "heldout_qualification_task_worlds": 25,
        "policy_replicates_total": 150,
        "primary_executions_total": 1200,
        "construction_primary_executions": 600,
        "heldout_qualification_primary_executions": 600,
        "tolerance_zero_exact_replay_checks": 1200,
    }
    assert contract["cohorts"]["heldout_qualification"]["selection_namespace"] == (
        "work-ii-ae-prior-v0.2-heldout-qualification-20260812"
    )
    assert contract["cohorts"]["heldout_qualification"]["task_world_seeds"][
        "electrochemical-conversion"
    ] == [934334899, 222130288, 187256385, 779398037, 533253734]


def test_noise_seed_and_namespace_are_distinct_for_hidden_pair_sides() -> None:
    contract = _contract()
    plan = _plan()
    task = contract["tasks"][0]
    moved = [
        index
        for index, source in enumerate(task["descriptor_permutation"])
        if index != source
    ]
    rows = [
        row
        for row in plan["executions"]
        if row["phase"] == "heldout_qualification"
        and row["task_id"] == task["task_id"]
        and row["world_seed"]
        == contract["cohorts"]["heldout_qualification"]["task_world_seeds"][
            task["task_id"]
        ][0]
        and row["policy_replicate"] == 0
        and row["nuisance_anchor"] == 0
        and row["target_category"] in moved
    ]

    assert len(rows) == 2
    assert rows[0]["observation_seed"] != rows[1]["observation_seed"]
    assert rows[0]["observation_noise_namespace"] != rows[1][
        "observation_noise_namespace"
    ]


def test_blind_policy_signature_and_output_do_not_depend_on_pair_or_outcomes() -> None:
    contract = _contract()
    task = contract["tasks"][0]

    schedule = build_blind_policy_schedule(
        task_id=task["task_id"],
        target_field=task["target_field"],
        policy=contract["policy"],
    )

    assert contract["policy"]["inputs"] == ["task_id", "target_field"]
    assert {"target_pair", "descriptor_permutation", "observations", "outcomes"} <= set(
        contract["policy"]["forbidden_inputs"]
    )
    assert len(schedule) == 8
    assert len({row["recipe_id"] for row in schedule}) == 8
    assert {
        (row["nuisance_anchor"], row["target_category"]) for row in schedule
    } == {(anchor, category) for anchor in range(2) for category in range(4)}


def test_construction_failure_is_retained_but_does_not_fail_final_admission() -> None:
    contract = _contract()
    plan = _plan()
    receipts = _synthetic_receipts(plan, fail_construction=True)

    report = build_qualification_report(plan, receipts, contract)

    assert report["status"] == "passed"
    assert report["construction_can_change_v0_2_rules"] is False
    assert any(
        failure["phase"] == "construction" for failure in report["failures"]
    )
    assert all(row["admission_passed"] for row in report["task_results"])
    assert validate_qualification_report(ROOT, report, plan, receipts, contract) == []


def test_any_heldout_world_failure_fails_task_and_universal_matrix_gate() -> None:
    contract = _contract()
    plan = _plan()
    task_id = "electrochemical-conversion"
    receipts = _synthetic_receipts(plan, fail_heldout_task=task_id)

    report = build_qualification_report(plan, receipts, contract)
    task_result = next(
        row for row in report["task_results"] if row["task_id"] == task_id
    )

    assert report["status"] == "failed"
    assert task_result["heldout_status"] == "failed"
    assert task_result["admission_passed"] is False
    assert any(
        failure["phase"] == "heldout_qualification"
        for failure in report["failures"]
    )


def test_support_and_negative_control_metrics_are_both_reported() -> None:
    contract = _contract()
    plan = _plan()
    receipts = _synthetic_receipts(plan)

    report = build_qualification_report(plan, receipts, contract)
    partition = next(
        row
        for row in report["anchor_results"]
        if row["phase"] == "heldout_qualification"
        and row["task_id"] == "partition-discovery"
    )

    assert partition["support_metric_ids"] == ["product_in_organic"]
    assert partition["negative_control_metric_ids"] == [
        "phase_ratio",
        "product_in_aqueous",
    ]
    assert set(partition["support_metric_results"]) == {"product_in_organic"}
    assert set(partition["negative_control_metric_results"]) == {
        "phase_ratio",
        "product_in_aqueous",
    }


def test_contrast_uncertainty_uses_independent_left_and_right_replicates() -> None:
    contract = _contract()
    plan = _plan()
    receipts = _synthetic_receipts(plan)
    task = contract["tasks"][0]
    world_seed = contract["cohorts"]["heldout_qualification"]["task_world_seeds"][
        task["task_id"]
    ][0]
    moved = [
        index
        for index, source in enumerate(task["descriptor_permutation"])
        if index != source
    ]
    offsets = (-0.01, 0.0, 0.01)
    for receipt in receipts:
        if (
            receipt["phase"] == "heldout_qualification"
            and receipt["task_id"] == task["task_id"]
            and receipt["world_seed"] == world_seed
            and receipt["nuisance_anchor"] == 0
            and receipt["target_category"] in moved
        ):
            offset = offsets[receipt["policy_replicate"]]
            for metric_id in receipt["allowed_metrics"]:
                receipt["allowed_metrics"][metric_id] += offset
            receipt["support_metrics"] = {
                metric: receipt["allowed_metrics"][metric]
                for metric in receipt["support_metric_ids"]
            }
            receipt["negative_control_metrics"] = {
                metric: receipt["allowed_metrics"][metric]
                for metric in receipt["negative_control_metric_ids"]
            }
            receipt["receipt_sha256"] = canonical_json_sha256(
                {
                    key: value
                    for key, value in receipt.items()
                    if key != "receipt_sha256"
                }
            )

    report = build_qualification_report(plan, receipts, contract)
    anchor = next(
        row
        for row in report["anchor_results"]
        if row["phase"] == "heldout_qualification"
        and row["task_id"] == task["task_id"]
        and row["world_seed"] == world_seed
        and row["nuisance_anchor"] == 0
    )

    assert anchor["support_contrast_rms_standard_error"] > 0.0
    assert all(
        row["welch_standard_error"] > 0.0
        for row in anchor["support_metric_results"].values()
    )


@pytest.mark.parametrize(
    ("section", "field", "replacement"),
    [
        ("policy", "rounds_per_policy_replicate", 7),
        ("noise", "seed_namespace", "tampered"),
        ("thresholds", "minimum_mean_support_separation", 0.049),
    ],
)
def test_semantic_contract_rejects_scientific_rule_tampering(
    section: str, field: str, replacement: object
) -> None:
    contract = _contract()
    contract[section][field] = replacement

    assert any("semantic contract changed" in error for error in validate_contract(ROOT, contract))


def test_semantic_contract_rejects_task_seed_support_and_direct_input_tampering() -> None:
    cases = []
    changed_seed = _contract()
    changed_seed["cohorts"]["heldout_qualification"]["task_world_seeds"][
        "electrochemical-conversion"
    ][0] += 1
    cases.append(changed_seed)
    changed_support = _contract()
    changed_support["tasks"][0]["support_metric_ids"] = ["safety_risk"]
    cases.append(changed_support)
    changed_note = _contract()
    changed_note["experiment_note_sha256"] = "0" * 64
    cases.append(changed_note)
    changed_config = _contract()
    changed_config["tasks"][0]["campaign_config_sha256"] = "0" * 64
    cases.append(changed_config)

    for contract in cases:
        assert validate_contract(ROOT, contract)


def test_plan_rebuild_rejects_rehashed_execution_recipe_and_binding_tampering() -> None:
    contract = _contract()
    plan = _plan()

    changed_recipe = deepcopy(plan)
    changed_recipe["executions"][0]["recipe"]["steps"][0]["amount_mol"] = 0.123
    changed_recipe["executions"][0]["recipe_sha256"] = canonical_json_sha256(
        changed_recipe["executions"][0]["recipe"]
    )
    _rehash(changed_recipe, "plan_sha256")
    assert any(
        "does not exactly reconstruct" in error
        for error in validate_qualification_plan(ROOT, changed_recipe, contract)
    )

    changed_binding = deepcopy(plan)
    changed_binding["task_bindings"][0]["campaign_config_sha256"] = "0" * 64
    _rehash(changed_binding, "plan_sha256")
    assert any(
        "does not exactly reconstruct" in error
        for error in validate_qualification_plan(ROOT, changed_binding, contract)
    )


def _write_one_disk_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[dict[str, object], dict[str, object], Path, Path]:
    plan = _plan()
    planned = plan["executions"][0]
    output = tmp_path / "output"
    trajectory_path = output / "executions/0/trajectory.jsonl"
    trajectory_path.parent.mkdir(parents=True)
    trajectory_path.write_text("synthetic trajectory\n", encoding="utf-8")
    metrics = dict.fromkeys(
        planned["allowed_metric_ids"], 0.1 + 0.1 * planned["target_category"]
    )
    records = [
        {
            "action": deepcopy(action),
            "transaction_status": "committed",
            "instrument": "final_assay" if index == len(planned["recipe"]["steps"]) - 1 else None,
            "observation": metrics if index == len(planned["recipe"]["steps"]) - 1 else {},
        }
        for index, action in enumerate(planned["recipe"]["steps"])
    ]
    monkeypatch.setattr(qualification_module, "load_jsonl", lambda path: records)
    monkeypatch.setattr(
        qualification_module,
        "verify_records",
        lambda *args, **kwargs: SimpleNamespace(
            to_dict=lambda: {
                "verified": True,
                "checked_steps": len(records),
                "max_abs_error": 0.0,
                "mismatches": [],
            }
        ),
    )
    receipt = deepcopy(planned)
    receipt.update(
        {
            "schema_version": RECEIPT_VERSION,
            "plan_sha256": plan["plan_sha256"],
            "provider_call_count": 0,
            "status": "completed",
            "allowed_metrics": metrics,
            "support_metrics": {
                metric: metrics[metric] for metric in planned["support_metric_ids"]
            },
            "negative_control_metrics": {
                metric: metrics[metric]
                for metric in planned["negative_control_metric_ids"]
            },
            "exact_replay": {
                "verified": True,
                "checked_steps": len(records),
                "max_abs_error": 0.0,
                "mismatches": [],
            },
            "trajectory": {
                "path": "executions/0/trajectory.jsonl",
                "sha256": file_sha256(trajectory_path),
            },
            "failure": None,
        }
    )
    _rehash(receipt, "receipt_sha256")
    write_json_atomic(output / "plan.json", plan)
    write_json_atomic(output / "receipts/0000.json", receipt)
    return plan, receipt, output, trajectory_path


def test_partial_audit_replays_one_receipt_and_never_resumes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, _, output, _ = _write_one_disk_receipt(tmp_path, monkeypatch)

    audit = build_partial_audit(ROOT, output, CONTRACT_PATH)

    assert audit["status"] == "interrupted"
    assert audit["resume_allowed"] is False
    assert audit["materialized_receipts"] == 1
    assert audit["independently_valid_receipts"] == 1
    assert audit["missing_receipts"] == 1199
    assert audit["errors"] == []


def test_partial_audit_rejects_trajectory_hash_path_and_immutable_receipt_tampering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan, receipt, output, trajectory_path = _write_one_disk_receipt(
        tmp_path, monkeypatch
    )
    trajectory_path.write_text("tampered\n", encoding="utf-8")
    audit = build_partial_audit(ROOT, output, CONTRACT_PATH)
    assert any("trajectory SHA-256 mismatch" in error for error in audit["errors"])

    receipt["trajectory"] = {"path": "../escape.jsonl", "sha256": "0" * 64}
    receipt["world_seed"] = plan["executions"][0]["world_seed"] + 1
    _rehash(receipt, "receipt_sha256")
    write_json_atomic(output / "receipts/0000.json", receipt)
    audit = build_partial_audit(ROOT, output, CONTRACT_PATH)
    assert any("immutable plan field mismatch" in error for error in audit["errors"])
    assert any("escapes its evidence root" in error for error in audit["errors"])


def test_complete_disk_validator_requires_all_1200_and_recomputed_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    contract = _contract()
    plan = _plan()
    receipts = _synthetic_receipts(plan)
    report = build_qualification_report(plan, receipts, contract)
    output = tmp_path / "complete"
    write_json_atomic(output / "plan.json", plan)
    write_json_atomic(output / "report.json", report)
    for index in range(1200):
        write_json_atomic(output / "receipts" / f"{index:04d}.json", {})
    monkeypatch.setattr(
        qualification_module,
        "_audit_disk_receipt",
        lambda root, output_root, disk_plan, planned, receipt_path: (
            receipts[int(planned["execution_index"])],
            [],
        ),
    )

    assert validate_qualification_output(ROOT, output, CONTRACT_PATH) == []

    report["status"] = "failed"
    _rehash(report, "report_sha256")
    write_json_atomic(output / "report.json", report)
    assert any(
        "fresh trajectory-derived report" in error
        for error in validate_qualification_output(ROOT, output, CONTRACT_PATH)
    )
