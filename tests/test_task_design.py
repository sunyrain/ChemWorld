from __future__ import annotations

from dataclasses import replace

from chemworld.physchem.maturity import MaturityLevel, ModuleMaturity, TaskMaturitySpec
from chemworld.schemas import validate_task_schema
from chemworld.task_design import (
    SERIOUS_TASK_DESIGNS,
    SeriousTaskDesign,
    review_task_design,
    serious_task_readiness_manifest,
)
from chemworld.tasks import SERIOUS_TASK_IDS, get_task


def test_serious_task_designs_cover_frozen_suite() -> None:
    assert tuple(SERIOUS_TASK_DESIGNS) == SERIOUS_TASK_IDS
    assert all(not get_task(task_id).kernel_maturity.proxy_allowed for task_id in SERIOUS_TASK_IDS)
    assert all(
        validate_task_schema(get_task(task_id).to_dict()).valid
        for task_id in SERIOUS_TASK_IDS
    )


def test_serious_task_contracts_pass_machine_readable_review() -> None:
    manifest = serious_task_readiness_manifest()

    assert manifest["suite_status"] == "candidate"
    assert manifest["contract_ready_count"] == len(SERIOUS_TASK_IDS)
    assert manifest["benchmark_ready_count"] == 0
    for task_id in SERIOUS_TASK_IDS:
        review = manifest["reviews"][task_id]
        assert review["contract_ready"] is True
        assert review["benchmark_ready"] is False
        assert review["empirical_status"] == "candidate"
        assert all(check["passed"] for check in review["checks"])


def test_serious_task_review_rejects_proxy_and_unimplemented_metric() -> None:
    proxy_task = replace(
        get_task("reaction-to-purification"),
        tags=("chemworld", "exploratory"),
        kernel_maturity=TaskMaturitySpec(
            modules=(
                ModuleMaturity(
                    "separations",
                    MaturityLevel.PROXY,
                    model_ids=("test_proxy",),
                ),
            ),
            proxy_allowed=True,
        ),
    )
    proxy_design = SeriousTaskDesign(
        task_id=proxy_task.task_id,
        research_question="Can an agent purify a virtual product?",
        capability_claim="multi-step purification planning",
        primary_metric="purity",
        secondary_metrics=("recovery",),
        generalization_axes=("partition", "feed impurity"),
        required_baselines=("random", "scripted_chemistry", "gp_bo"),
        required_evidence=("baseline", "replay", "failure analysis"),
        anti_gaming_checks=("hidden-state ban", "final assay boundary"),
    )
    proxy_review = review_task_design(proxy_task, proxy_design)
    assert not proxy_review.contract_ready
    assert not next(
        check for check in proxy_review.checks if check.check_id == "proxy_policy"
    ).passed

    partition = get_task("partition-discovery")
    unsupported = replace(
        partition,
        success_metrics=(*partition.success_metrics, "unimplemented_metric"),
    )
    metric_review = review_task_design(
        unsupported,
        SERIOUS_TASK_DESIGNS[partition.task_id],
    )
    assert not metric_review.contract_ready
    assert not next(
        check for check in metric_review.checks if check.check_id == "metric_implementation"
    ).passed


def test_task_schema_rejects_shallow_or_malformed_contracts() -> None:
    payload = get_task("flow-reaction-optimization").to_dict()
    payload["seeds"] = [0, 0]
    payload["contract_hash"] = "not-a-digest"

    result = validate_task_schema(payload)
    assert not result.valid
    assert any("seeds" in error for error in result.errors)
    assert any("contract_hash" in error for error in result.errors)
