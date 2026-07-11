from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from chemworld.agents.greedy import GreedyLocalAgent
from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.data.logging import load_jsonl
from chemworld.eval.reference_portfolio import (
    REFERENCE_PORTFOLIO_EVIDENCE_VERSION,
    ReferencePortfolioError,
    audit_reference_portfolio,
    build_reference_run_plan,
    freeze_reference_estimates,
    load_reference_portfolio_plan,
    reference_portfolio_plan_sha256,
)
from chemworld.eval.reference_regret import (
    load_reference_regret_protocol,
    reference_regret_protocol_sha256,
)
from chemworld.eval.result_artifacts import build_verified_evaluation_result
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "reference-portfolio-controls.json"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class _ReferenceGreedyAgent(GreedyLocalAgent):
    name = "independent_reference_portfolio_test"

    def __init__(self, builder_seed: int) -> None:
        super().__init__(warmup=1)
        self.reference_builder_seed = builder_seed

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        del seed
        super().reset(task_info, self.reference_builder_seed)

    def manifest(self) -> dict[str, Any]:
        payload = super().manifest()
        payload["reference_builder_seed"] = self.reference_builder_seed
        return payload


def _small_plan_and_protocol() -> tuple[dict, dict]:
    plan = copy.deepcopy(load_reference_portfolio_plan())
    protocol = copy.deepcopy(load_reference_regret_protocol())
    task = get_task("partition-discovery")
    protocol["formal_task_ids"] = [task.task_id]
    protocol["seed_ids"] = [20]
    plan["builder_id"] = "independent_reference_portfolio_test"
    plan["source_split"] = task.world_split
    protocol["independence_policy"]["reference_source_split"] = task.world_split
    plan["replicate_ids"] = ["r0"]
    plan["minimum_sources_per_cell"] = 1
    plan["experiment_budget"] = 1
    plan["evaluated_method_ids"] = ["random", "structured_gp_ei"]
    plan["uncertainty_policy"]["bootstrap_samples"] = 200
    return plan, protocol


def _real_manifest(tmp_path: Path) -> tuple[dict, dict, dict, Path]:
    plan, protocol = _small_plan_and_protocol()
    run = build_reference_run_plan(plan, protocol)[0]
    task = get_task(run["task_id"])
    trajectory = tmp_path / "trajectory.jsonl"
    operation_budget = task_recipe_event_count(task.to_dict())
    run_agent(
        env_id=task.env_id,
        agent=_ReferenceGreedyAgent(run["builder_seed"]),
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=run["benchmark_seed"],
        task_id=task.task_id,
        output_path=trajectory,
        budget_override=operation_budget,
        evaluation_policy="vnext_risk_cost",
    )
    records = load_jsonl(trajectory)
    result = build_verified_evaluation_result(
        records,
        trajectory_path=trajectory,
    )
    result["resource_usage"] = {
        "schema_version": "chemworld-resource-usage-0.2",
        "complete_experiment_count": result["final_assay_count"],
        "method_ledger": records[-1]["method_resources"],
    }
    result_path = tmp_path / "result.json"
    result_path.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    manifest = {
        "schema_version": REFERENCE_PORTFOLIO_EVIDENCE_VERSION,
        "status": "complete",
        "plan_sha256": reference_portfolio_plan_sha256(plan),
        "reference_protocol_sha256": reference_regret_protocol_sha256(protocol),
        "builder_id": plan["builder_id"],
        "source_split": plan["source_split"],
        "frozen_before_method_scoring": True,
        "records": [
            {
                **run,
                "builder_implementation_sha256": "1" * 64,
                "result_path": result_path.name,
                "result_sha256": _sha(result_path),
                "trajectory_sha256": _sha(trajectory),
            }
        ],
    }
    return plan, protocol, manifest, trajectory


def test_candidate_plan_is_complete_deterministic_and_non_claiming() -> None:
    plan = load_reference_portfolio_plan()
    protocol = load_reference_regret_protocol()
    first = build_reference_run_plan(plan, protocol)
    second = build_reference_run_plan(plan, protocol)
    report = audit_reference_portfolio(plan, reference_protocol=protocol)

    assert first == second
    assert len(first) == 320
    assert len({item["run_id"] for item in first}) == 320
    assert len({item["builder_seed"] for item in first}) == 320
    assert report["controls_ready"] is True
    assert report["status"] == "controls_ready_evidence_missing"
    assert report["expected_reference_cell_count"] == 160
    assert report["candidate_reference_record_count"] == 0
    assert report["formal_results_present"] is False
    assert report["parent_task_complete"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
    assert all(report["adversarial_probes"].values())


def test_complete_real_evidence_is_replayed_and_yields_candidate_records(
    tmp_path: Path,
) -> None:
    plan, protocol, manifest, _ = _real_manifest(tmp_path)
    estimates = freeze_reference_estimates(
        plan,
        protocol,
        manifest,
        workspace_root=tmp_path,
    )
    report = audit_reference_portfolio(
        plan,
        reference_protocol=protocol,
        evidence_manifest=manifest,
        workspace_root=tmp_path,
    )

    assert len(estimates) == 2
    assert {item["metric_id"] for item in estimates} == {"objective", "task_primary"}
    assert all(item["candidate_evidence_only"] is True for item in estimates)
    assert all(item["replay_verified"] is True for item in estimates)
    assert all(item["interval_lower"] == item["estimate"] for item in estimates)
    assert all(item["interval_upper"] == item["estimate"] for item in estimates)
    assert report["evidence_complete"] is True
    assert report["candidate_reference_record_count"] == 2
    assert report["formal_results_present"] is False
    assert report["parent_task_complete"] is False


def test_evidence_fails_closed_on_coverage_identity_split_and_digest(
    tmp_path: Path,
) -> None:
    plan, protocol, manifest, _ = _real_manifest(tmp_path)

    missing = copy.deepcopy(manifest)
    missing["records"] = []
    with pytest.raises(ReferencePortfolioError, match="coverage is incomplete"):
        freeze_reference_estimates(plan, protocol, missing, workspace_root=tmp_path)

    duplicate = copy.deepcopy(manifest)
    duplicate["records"].append(copy.deepcopy(duplicate["records"][0]))
    with pytest.raises(ReferencePortfolioError, match="duplicate run"):
        freeze_reference_estimates(plan, protocol, duplicate, workspace_root=tmp_path)

    wrong_split = copy.deepcopy(manifest)
    wrong_split["source_split"] = "bench"
    with pytest.raises(ReferencePortfolioError, match="source split mismatch"):
        freeze_reference_estimates(plan, protocol, wrong_split, workspace_root=tmp_path)

    wrong_builder = copy.deepcopy(manifest)
    wrong_builder["records"][0]["builder_id"] = "random"
    with pytest.raises(ReferencePortfolioError, match="builder_id mismatch"):
        freeze_reference_estimates(plan, protocol, wrong_builder, workspace_root=tmp_path)

    bad_digest = copy.deepcopy(manifest)
    bad_digest["records"][0]["result_sha256"] = "0" * 64
    with pytest.raises(ReferencePortfolioError, match="result artifact digest mismatch"):
        freeze_reference_estimates(plan, protocol, bad_digest, workspace_root=tmp_path)

    result_path = tmp_path / manifest["records"][0]["result_path"]
    result = json.loads(result_path.read_text(encoding="utf-8"))
    result["resource_usage"]["complete_experiment_count"] = 0
    result_path.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    wrong_budget = copy.deepcopy(manifest)
    wrong_budget["records"][0]["result_sha256"] = _sha(result_path)
    with pytest.raises(ReferencePortfolioError, match="frozen experiment budget"):
        freeze_reference_estimates(plan, protocol, wrong_budget, workspace_root=tmp_path)


def test_evidence_fails_closed_if_bound_trajectory_changes(tmp_path: Path) -> None:
    plan, protocol, manifest, trajectory = _real_manifest(tmp_path)
    trajectory.write_bytes(trajectory.read_bytes() + b"\n")

    with pytest.raises(ReferencePortfolioError, match="replay failed"):
        freeze_reference_estimates(plan, protocol, manifest, workspace_root=tmp_path)


def test_frozen_report_keeps_formal_gates_closed() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))

    assert report["controls_ready"] is True
    assert report["status"] == "controls_ready_evidence_missing"
    assert report["planned_source_run_count"] == 320
    assert report["expected_reference_cell_count"] == 160
    assert report["evidence_complete"] is False
    assert report["formal_results_present"] is False
    assert report["parent_task_complete"] is False
    assert report["publication_ready"] is False
