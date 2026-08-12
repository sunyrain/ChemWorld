from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.work_ii_ae_prior_qualification_v02 import (
    build_blind_policy_schedule,
    build_qualification_plan,
    build_qualification_report,
    validate_contract,
    validate_qualification_plan,
    validate_qualification_report,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.2.json"
)


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _plan() -> dict[str, object]:
    return build_qualification_plan(ROOT, CONTRACT_PATH)


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
        receipt = {
            key: deepcopy(row[key])
            for key in (
                "execution_index",
                "execution_id",
                "phase",
                "task_id",
                "world_seed",
                "policy_replicate",
                "round_index",
                "nuisance_anchor",
                "target_category",
                "target_field",
                "target_coordinate",
                "recipe_id",
                "allowed_metric_ids",
                "support_metric_ids",
                "negative_control_metric_ids",
                "observation_seed",
                "observation_noise_namespace",
            )
        }
        if failed:
            receipt.update(
                {
                    "provider_call_count": 0,
                    "status": "failed",
                    "allowed_metrics": None,
                    "support_metrics": None,
                    "negative_control_metrics": None,
                    "exact_replay": None,
                    "trajectory_path": None,
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
                    "trajectory_path": f"executions/{row['execution_index']}/trajectory.jsonl",
                    "failure": None,
                }
            )
        receipts.append(receipt)
    return receipts


def test_contract_and_plan_freeze_exact_denominators_and_heldout_namespace() -> None:
    contract = _contract()
    plan = _plan()

    assert validate_contract(ROOT, contract) == []
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
