"""Calibration and audit of vNext operational-risk and resource signals."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import spearmanr

from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import SERIOUS_TASK_IDS

RISK_COST_PROTOCOL_VERSION = "chemworld-risk-cost-protocol-0.1"
RISK_COST_AUDIT_VERSION = "chemworld-risk-cost-signal-audit-0.1"
DEFAULT_RISK_COST_PROTOCOL_PATH = configuration_root() / "benchmark" / "risk_cost_vnext.json"
DEFAULT_FORMAL_RESULTS_PATH = (
    Path(__file__).resolve().parents[3]
    / "runs"
    / "publication"
    / "protocol-v0.1"
    / "full"
    / "baseline_results.json"
)


@dataclass(frozen=True)
class RiskCostTaskPolicy:
    task_id: str
    risk_limit: float
    process_cost_limit: float
    risk_semantics: str = "benchmark_operational_risk_budget_not_real_world_safety"

    def __post_init__(self) -> None:
        if self.task_id not in SERIOUS_TASK_IDS:
            raise ValueError(f"unsupported serious task: {self.task_id}")
        if not math.isfinite(self.risk_limit) or not 0.0 < self.risk_limit < 1.0:
            raise ValueError("risk_limit must be finite and in (0, 1)")
        if not math.isfinite(self.process_cost_limit) or self.process_cost_limit <= 0.0:
            raise ValueError("process_cost_limit must be finite and positive")

    @classmethod
    def from_protocol(
        cls,
        task_id: str,
        protocol: dict[str, Any],
    ) -> RiskCostTaskPolicy:
        tasks = protocol.get("tasks", {})
        if not isinstance(tasks, dict) or not isinstance(tasks.get(task_id), dict):
            raise ValueError(f"risk-cost protocol is missing task {task_id!r}")
        payload = tasks[task_id]
        return cls(
            task_id=task_id,
            risk_limit=float(payload["risk_limit"]),
            process_cost_limit=float(payload["process_cost_limit"]),
            risk_semantics=str(protocol.get("risk_semantics", "")),
        )

    def task_info_overlay(self) -> dict[str, Any]:
        """Return the explicit public policy that a vNext runner gives every agent."""

        return {
            "safety_limit": self.risk_limit,
            "risk_limit": self.risk_limit,
            "risk_limit_semantics": self.risk_semantics,
            "risk_aggregation": "max_operation_risk_per_experiment",
            "process_cost_limit": self.process_cost_limit,
        }


def load_risk_cost_protocol(
    path: str | Path = DEFAULT_RISK_COST_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("risk-cost protocol must be a JSON object")
    return payload


def audit_risk_cost_signal(
    protocol: dict[str, Any],
    *,
    formal_results_path: str | Path = DEFAULT_FORMAL_RESULTS_PATH,
) -> dict[str, Any]:
    results_path = Path(formal_results_path)
    results = json.loads(results_path.read_text(encoding="utf-8"))
    if not isinstance(results, list) or not results:
        raise ValueError("formal results must be a non-empty JSON list")
    rows_by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("formal result rows must be JSON objects")
        trajectory_path = _resolve_trajectory_path(str(result["trajectory_path"]))
        rows_by_task[str(result["task_id"])].extend(_experiment_rows(result, trajectory_path))

    calibration = protocol.get("calibration", {})
    holdout = protocol.get("holdout", {})
    calibration_methods = {str(item) for item in calibration.get("methods", ())}
    calibration_seeds = {int(item) for item in calibration.get("seeds", ())}
    holdout_seeds = {int(item) for item in holdout.get("seeds", ())}
    formal_methods = tuple(str(item) for item in protocol.get("formal_methods", ()))
    risk_quantile = float(calibration.get("risk_quantile", math.nan))
    process_quantile = float(calibration.get("process_cost_quantile", math.nan))
    risk_bounds = _pair(holdout.get("risk_activation_rate_bounds"), "risk bounds")
    cost_bounds = _pair(
        holdout.get("process_cost_activation_rate_bounds"),
        "process-cost bounds",
    )
    tradeoff_tasks = {str(item) for item in protocol.get("risk_performance_tradeoff_tasks", ())}
    minimum_tradeoff = float(protocol.get("minimum_tradeoff_spearman", math.nan))

    task_reports: dict[str, Any] = {}
    for task_id in SERIOUS_TASK_IDS:
        policy = RiskCostTaskPolicy.from_protocol(task_id, protocol)
        rows = rows_by_task.get(task_id, [])
        calibration_rows = [
            row
            for row in rows
            if row["method"] in calibration_methods and row["seed"] in calibration_seeds
        ]
        holdout_rows = [row for row in rows if row["seed"] in holdout_seeds]
        if not calibration_rows or not holdout_rows:
            raise ValueError(f"task {task_id!r} lacks calibration or holdout rows")
        recomputed_risk_limit = _quantile(
            calibration_rows,
            "max_risk",
            risk_quantile,
        )
        recomputed_process_limit = _quantile(
            calibration_rows,
            "process_cost",
            process_quantile,
        )
        risk_activation = _activation_rate(
            holdout_rows,
            "max_risk",
            policy.risk_limit,
        )
        cost_activation = _activation_rate(
            holdout_rows,
            "process_cost",
            policy.process_cost_limit,
        )
        correlation = _score_risk_spearman(holdout_rows)
        method_reports = {
            method: _method_summary(
                [row for row in holdout_rows if row["method"] == method],
                policy,
            )
            for method in formal_methods
        }
        measurement_costs = {round(float(row["measurement_cost"]), 12) for row in rows}
        task_reports[task_id] = {
            "policy": {
                "risk_limit": policy.risk_limit,
                "process_cost_limit": policy.process_cost_limit,
                "risk_semantics": policy.risk_semantics,
            },
            "experiment_count": len(rows),
            "calibration_experiment_count": len(calibration_rows),
            "holdout_experiment_count": len(holdout_rows),
            "recomputed_risk_limit": recomputed_risk_limit,
            "recomputed_process_cost_limit": recomputed_process_limit,
            "risk_limit_matches_calibration": math.isclose(
                policy.risk_limit,
                recomputed_risk_limit,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            ),
            "process_cost_limit_matches_calibration": math.isclose(
                policy.process_cost_limit,
                recomputed_process_limit,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            ),
            "holdout_risk_activation_rate": risk_activation,
            "holdout_process_cost_activation_rate": cost_activation,
            "holdout_score_risk_spearman": correlation,
            "risk_tradeoff_task": task_id in tradeoff_tasks,
            "tradeoff_direction_matches_scope": (
                correlation >= minimum_tradeoff
                if task_id in tradeoff_tasks
                else correlation < minimum_tradeoff
            ),
            "measurement_cost_unique_count": len(measurement_costs),
            "classic_measurement_policy_varies": len(measurement_costs) > 1,
            "method_reports": method_reports,
        }

    checks = {
        "schema": protocol.get("schema_version") == RISK_COST_PROTOCOL_VERSION,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "task_scope": tuple(protocol.get("tasks", {})) == tuple(SERIOUS_TASK_IDS),
        "formal_result_count": len(results) == 600,
        "formal_scope": {str(row["task_id"]) for row in results} == set(SERIOUS_TASK_IDS)
        and {str(row["baseline_agent"]) for row in results} == set(formal_methods)
        and {int(row["seed"]) for row in results} == calibration_seeds.union(holdout_seeds),
        "experiment_matrix_complete": all(
            report["experiment_count"] == 4_000
            and report["calibration_experiment_count"] == 400
            and report["holdout_experiment_count"] == 3_000
            for report in task_reports.values()
        ),
        "calibration_holdout_disjoint": not calibration_seeds.intersection(holdout_seeds),
        "thresholds_reproduce": all(
            report["risk_limit_matches_calibration"]
            and report["process_cost_limit_matches_calibration"]
            for report in task_reports.values()
        ),
        "risk_activation_nonzero_nonsaturated": all(
            risk_bounds[0] <= report["holdout_risk_activation_rate"] <= risk_bounds[1]
            for report in task_reports.values()
        ),
        "process_cost_activation_nonzero_nonsaturated": all(
            cost_bounds[0] <= report["holdout_process_cost_activation_rate"] <= cost_bounds[1]
            for report in task_reports.values()
        ),
        "risk_tradeoff_scope_empirically_separated": all(
            report["tradeoff_direction_matches_scope"] for report in task_reports.values()
        ),
        "cost_decomposition_nonnegative": all(
            row["process_cost"] >= 0.0 for rows in rows_by_task.values() for row in rows
        ),
    }
    controls_ready = all(checks.values())
    measurement_policy_identifiable = any(
        report["classic_measurement_policy_varies"] for report in task_reports.values()
    )
    return {
        "schema_version": RISK_COST_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": (
            "risk_process_controls_ready_method_rerun_pending"
            if controls_ready
            else "controls_failed"
        ),
        "controls_ready": controls_ready,
        "risk_process_signal_identifiable": controls_ready,
        "measurement_policy_identifiable": measurement_policy_identifiable,
        "formal_method_comparison_ready": False,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "tasks": task_reports,
        "limitations": [
            "The calibrated limit is a benchmark operational-risk budget, not a "
            "real-world safety threshold.",
            "The retained methods received the legacy 0.65 limit, so retrospective "
            "activation cannot rank safe methods.",
            "Classic recipes use fixed measurement schedules within each task, so "
            "measurement efficiency is not identified.",
            "Only flow, crystallization, and distillation exhibit a positive "
            "performance-risk tradeoff on the holdout slice.",
        ],
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _resolve_trajectory_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_file():
        return path
    root = Path(__file__).resolve().parents[3]
    parts = path.parts
    run_indices = [index for index, part in enumerate(parts) if part.lower() == "runs"]
    for index in reversed(run_indices):
        candidate = root.joinpath(*parts[index:])
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"trajectory does not exist: {raw_path}")


def _experiment_rows(
    result: dict[str, Any],
    trajectory_path: Path,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    risks: list[float] = []
    measurement_cost = 0.0
    with trajectory_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            observation = record.get("observation", {})
            if isinstance(observation, dict) and observation.get("safety_risk") is not None:
                risks.append(float(observation["safety_risk"]))
            measurement_cost += float(record.get("measurement_cost", 0.0))
            if record.get("leaderboard_score") is None:
                continue
            if not risks or not isinstance(observation, dict) or observation.get("cost") is None:
                raise ValueError(f"incomplete terminal evidence in {trajectory_path}")
            total_cost = float(observation["cost"])
            process_cost = total_cost - measurement_cost
            if process_cost < -1.0e-9:
                raise ValueError(f"measurement cost exceeds total cost in {trajectory_path}")
            rows.append(
                {
                    "task_id": str(result["task_id"]),
                    "method": str(result["baseline_agent"]),
                    "seed": int(result["seed"]),
                    "score": float(record["leaderboard_score"]),
                    "max_risk": max(risks),
                    "terminal_risk": risks[-1],
                    "total_cost": total_cost,
                    "measurement_cost": measurement_cost,
                    "process_cost": max(process_cost, 0.0),
                }
            )
            risks = []
            measurement_cost = 0.0
    if risks or measurement_cost:
        raise ValueError(f"trajectory ends with an incomplete experiment: {trajectory_path}")
    return rows


def _pair(payload: Any, name: str) -> tuple[float, float]:
    if not isinstance(payload, list) or len(payload) != 2:
        raise ValueError(f"{name} must contain [low, high]")
    low, high = float(payload[0]), float(payload[1])
    if not 0.0 <= low < high <= 1.0:
        raise ValueError(f"invalid {name}: {payload}")
    return low, high


def _quantile(rows: list[dict[str, Any]], field: str, quantile: float) -> float:
    if not 0.0 < quantile < 1.0:
        raise ValueError("calibration quantiles must be in (0, 1)")
    return float(np.quantile([float(row[field]) for row in rows], quantile, method="linear"))


def _activation_rate(
    rows: list[dict[str, Any]],
    field: str,
    limit: float,
) -> float:
    return sum(float(row[field]) >= limit for row in rows) / len(rows)


def _score_risk_spearman(rows: list[dict[str, Any]]) -> float:
    statistic = spearmanr(
        [float(row["score"]) for row in rows],
        [float(row["max_risk"]) for row in rows],
    ).statistic
    if not math.isfinite(float(statistic)):
        raise ValueError("score-risk Spearman correlation is not identifiable")
    return float(statistic)


def _method_summary(
    rows: list[dict[str, Any]],
    policy: RiskCostTaskPolicy,
) -> dict[str, Any]:
    if not rows:
        raise ValueError(f"missing holdout rows for method under {policy.task_id}")
    return {
        "experiment_count": len(rows),
        "mean_score": float(np.mean([row["score"] for row in rows])),
        "mean_max_risk": float(np.mean([row["max_risk"] for row in rows])),
        "risk_budget_exceedance_rate": _activation_rate(
            rows,
            "max_risk",
            policy.risk_limit,
        ),
        "process_cost_exceedance_rate": _activation_rate(
            rows,
            "process_cost",
            policy.process_cost_limit,
        ),
    }


__all__ = [
    "DEFAULT_FORMAL_RESULTS_PATH",
    "DEFAULT_RISK_COST_PROTOCOL_PATH",
    "RISK_COST_AUDIT_VERSION",
    "RISK_COST_PROTOCOL_VERSION",
    "RiskCostTaskPolicy",
    "audit_risk_cost_signal",
    "load_risk_cost_protocol",
]
