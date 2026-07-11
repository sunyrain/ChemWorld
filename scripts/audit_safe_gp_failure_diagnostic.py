"""Audit the fresh-seed SafeGP confidence-beta failure diagnostic."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any

from chemworld.physchem.mechanism_library import configuration_root  # type: ignore[import-untyped]

PROTOCOL_VERSION = "chemworld-safe-gp-failure-diagnostic-protocol-0.1"
REPORT_VERSION = "chemworld-safe-gp-failure-diagnostic-report-0.1"
DEFAULT_PROTOCOL = configuration_root() / "benchmark" / "safe_gp_failure_diagnostic.json"
DEFAULT_RESULTS_ROOT = Path("runs/benchmark-vnext/safe-gp-beta-pilot")
DEFAULT_OUTPUT = Path(
    "workstreams/benchmark_v1/reports/safe-gp-failure-diagnostic.json"
)


def load_protocol(path: str | Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SafeGP diagnostic protocol must be an object")
    if payload.get("schema_version") != PROTOCOL_VERSION:
        raise ValueError("unsupported SafeGP diagnostic protocol")
    if payload.get("benchmark_claim_allowed") is not False:
        raise ValueError("SafeGP failure diagnostic must remain nonclaiming")
    return payload


def build_diagnostic_report(
    results_by_method: dict[str, list[dict[str, Any]]],
    *,
    protocol: dict[str, Any],
    source_sha256: dict[str, str] | None = None,
) -> dict[str, Any]:
    seeds = tuple(int(seed) for seed in protocol["dev_seeds"])
    incumbent = str(protocol["incumbent"])
    comparator = str(protocol["comparator"])
    methods = (comparator, *tuple(str(key) for key in protocol["variants"]))
    summaries: dict[str, Any] = {}
    indexed: dict[str, dict[int, dict[str, Any]]] = {}
    for method in methods:
        rows = results_by_method.get(method)
        if rows is None:
            raise ValueError(f"missing diagnostic results for {method}")
        by_seed = {int(row["seed"]): row for row in rows}
        if tuple(sorted(by_seed)) != seeds:
            raise ValueError(f"{method} does not contain the exact frozen Dev seeds")
        indexed[method] = by_seed
        cards = [_result_card(by_seed[seed], protocol=protocol) for seed in seeds]
        summaries[method] = {
            "run_count": len(cards),
            "mean_flow_conversion": statistics.fmean(card["flow_conversion"] for card in cards),
            "mean_risk_exceedance_rate": statistics.fmean(
                card["risk_exceedance_rate"] for card in cards
            ),
            "mean_cost_per_experiment": statistics.fmean(
                card["cost_per_experiment"] for card in cards
            ),
            "mean_decision_wall_time_s": statistics.fmean(
                card["decision_wall_time_s"] for card in cards
            ),
            "mean_process_cpu_time_s": statistics.fmean(
                card["process_cpu_time_s"] for card in cards
            ),
            "mean_total_wall_time_s": statistics.fmean(
                card["total_wall_time_s"] for card in cards
            ),
            "all_replay_verified": all(card["verified"] for card in cards),
            "all_method_resource_ledgers_complete": all(
                card["accounting_complete"] for card in cards
            ),
        }

    comparator_effects = {
        method: _paired_effects(indexed, method, comparator, seeds)
        for method in protocol["variants"]
    }
    rule = protocol["joint_revision_rule"]
    incumbent_summary = summaries[incumbent]
    revision_decisions: dict[str, Any] = {}
    for method in protocol["variants"]:
        if method == incumbent:
            continue
        effects = _paired_effects(indexed, method, incumbent, seeds)
        candidate = summaries[method]
        objective_improved = effects["mean_paired_flow_conversion_effect"] > 0.0
        risk_noninferior = (
            candidate["mean_risk_exceedance_rate"]
            - incumbent_summary["mean_risk_exceedance_rate"]
            <= float(rule["maximum_absolute_risk_rate_regression"])
        )
        cost_noninferior = (
            candidate["mean_cost_per_experiment"]
            / incumbent_summary["mean_cost_per_experiment"]
            - 1.0
            <= float(rule["maximum_relative_cost_regression"])
        )
        revision_decisions[method] = {
            **effects,
            "objective_improved": objective_improved,
            "risk_noninferior": risk_noninferior,
            "cost_noninferior": cost_noninferior,
            "joint_revision_rule_passed": (
                objective_improved and risk_noninferior and cost_noninferior
            ),
        }
    selected_revisions = [
        method
        for method, decision in revision_decisions.items()
        if decision["joint_revision_rule_passed"]
    ]
    controls_passed = all(
        card["all_replay_verified"] and card["all_method_resource_ledgers_complete"]
        for card in summaries.values()
    )
    return {
        "schema_version": REPORT_VERSION,
        "protocol_id": protocol["protocol_id"],
        "status": (
            "development_diagnostic_complete" if controls_passed else "controls_failed"
        ),
        "controls_passed": controls_passed,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "task_id": protocol["task_id"],
        "dev_seeds": list(seeds),
        "method_summaries": summaries,
        "paired_effects_vs_random": comparator_effects,
        "revision_decisions_vs_incumbent": revision_decisions,
        "incumbent": incumbent,
        "selected_revision": selected_revisions[0] if len(selected_revisions) == 1 else None,
        "incumbent_retained": not selected_revisions,
        "interpretation": (
            "Lowering the SafeGP confidence beta did not jointly improve objective, risk, "
            "and cost on the fresh five-seed Dev diagnostic; retain beta=2.0 and do not "
            "reinterpret the prior confirmatory failure."
        ),
        "evidence_boundary": protocol["evidence_boundary"],
        "compute_accounting_note": (
            "Environment experiment count alone understates classical optimizer cost; "
            "decision wall time, process CPU time, and total wall time are reported separately."
        ),
        "source_suite_sha256": source_sha256 or {},
    }


def load_result_suites(
    root: str | Path,
    *,
    protocol: dict[str, Any],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
    methods = (str(protocol["comparator"]), *tuple(str(key) for key in protocol["variants"]))
    results: dict[str, list[dict[str, Any]]] = {}
    digests: dict[str, str] = {}
    for method in methods:
        path = Path(root) / method / "suite_results.json"
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            raise ValueError(f"{path} must contain a result list")
        results[method] = rows
        digests[method] = hashlib.sha256(path.read_bytes()).hexdigest()
    return results, digests


def _result_card(result: dict[str, Any], *, protocol: dict[str, Any]) -> dict[str, Any]:
    layered = result["score_replay"]["layered_evaluation"]
    resources = layered["resources"]
    usage = result["resource_usage"]
    complete = int(resources["complete_experiment_count"])
    if complete != int(protocol["complete_experiments_per_run"]):
        raise ValueError("diagnostic result has an incomplete experiment budget")
    return {
        "flow_conversion": float(result["mean_flow_conversion"]),
        "risk_exceedance_rate": float(
            layered["constraints"]["risk_budget_exceedance_rate"]
        ),
        "cost_per_experiment": float(resources["campaign_total_cost"]) / complete,
        "decision_wall_time_s": float(
            usage["method_ledger"]["decision_wall_time_s"]
        ),
        "process_cpu_time_s": float(usage["process_cpu_time_s"]),
        "total_wall_time_s": float(usage["total_wall_time_s"]),
        "verified": result.get("verified") is True,
        "accounting_complete": (
            usage["method_ledger"].get("accounting_complete") is True
        ),
    }


def _paired_effects(
    indexed: dict[str, dict[int, dict[str, Any]]],
    candidate: str,
    comparator: str,
    seeds: tuple[int, ...],
) -> dict[str, Any]:
    effects = [
        float(indexed[candidate][seed]["mean_flow_conversion"])
        - float(indexed[comparator][seed]["mean_flow_conversion"])
        for seed in seeds
    ]
    return {
        "comparator": comparator,
        "paired_flow_conversion_effects": effects,
        "mean_paired_flow_conversion_effect": statistics.fmean(effects),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--results-root", type=Path, default=DEFAULT_RESULTS_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    protocol = load_protocol(args.protocol)
    results, digests = load_result_suites(args.results_root, protocol=protocol)
    report = build_diagnostic_report(
        results,
        protocol=protocol,
        source_sha256=digests,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), "status": report["status"]}, indent=2))
    return 0 if report["controls_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
