#!/usr/bin/env python3
"""Build the reader-facing data layer for the first-paper figure set."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "configs/current.json"
DEFAULT_OUTPUT = (
    ROOT / "paper/figures/first-paper-world-instrument-v1" / "first-paper-figure-data-v1.json"
)
SCHEMA = "chemworld-first-paper-figure-data-0.1"


class FigureDataError(RuntimeError):
    """Raised when current evidence cannot support the reader-facing data layer."""


def canonical_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise FigureDataError(f"JSON object required: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FigureDataError(message)


def _source_binding(current: Mapping[str, Any], *, role: str, relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    require(path.is_file(), f"current source is missing: {relative_path}")
    nodes = current.get("evidence_dag", {}).get("nodes", {})
    matches = [
        (node_id, node)
        for node_id, node in nodes.items()
        if isinstance(node, Mapping) and node.get("path") == relative_path
    ]
    require(len(matches) == 1, f"current source is not uniquely registered: {relative_path}")
    node_id, node = matches[0]
    actual_sha = file_sha256(path)
    require(node.get("sha256") == actual_sha, f"current source hash is stale: {relative_path}")
    require(node.get("freshness") == "fresh", f"current source is stale: {relative_path}")
    require(
        node.get("gate_state") in {"passed", "not_applicable"},
        f"current source gate is not usable: {relative_path}",
    )
    return {
        "role": role,
        "node_id": node_id,
        "path": relative_path,
        "sha256": actual_sha,
    }


def _pattern_components(pattern: str) -> list[str]:
    lookup = {
        "phase-observation": ["phase", "observation"],
        "reaction-thermal-observation": ["reaction", "thermal", "observation"],
        "phase-separation-observation": ["phase", "separation", "observation"],
        "reaction-crystallization-observation": [
            "reaction",
            "thermal",
            "crystallization",
            "observation",
        ],
        "reaction-distillation-observation": [
            "reaction",
            "thermal",
            "distillation",
            "observation",
        ],
        "reaction-continuous-flow-observation": [
            "reaction",
            "thermal",
            "continuous flow",
            "observation",
        ],
        "reaction-electrochemistry-observation": [
            "reaction",
            "electrochemistry",
            "observation",
        ],
        "reaction-phase-separation-observation": [
            "reaction",
            "thermal",
            "phase",
            "separation",
            "observation",
        ],
    }
    require(pattern in lookup, f"unregistered composition pattern: {pattern}")
    return lookup[pattern]


def build_figure_data(root: Path = ROOT) -> dict[str, Any]:
    global ROOT
    previous_root = ROOT
    ROOT = root.resolve()
    try:
        current = load_object(ROOT / "configs/current.json")
        publication = current.get("publication", {})
        work_i = current.get("work_i_fvl", {})
        paths = {
            "composition": publication.get("composition_qualification_report"),
            "deterministic": publication.get("deterministic_use_case_qualification_report"),
            "agent": publication.get("agent_instrument_use_report"),
            "forks": work_i.get("world_fork_report"),
            "endpoint_process": publication.get("derived_data"),
        }
        require(
            all(isinstance(path, str) for path in paths.values()),
            "current figure sources are incomplete",
        )
        bindings = [
            _source_binding(current, role=role, relative_path=str(path))
            for role, path in paths.items()
        ]
        composition = load_object(ROOT / str(paths["composition"]))
        deterministic = load_object(ROOT / str(paths["deterministic"]))
        agent = load_object(ROOT / str(paths["agent"]))
        forks = load_object(ROOT / str(paths["forks"]))
        derived = load_object(ROOT / str(paths["endpoint_process"]))

        require(composition.get("status") == "passed", "composition qualification did not pass")
        require(deterministic.get("status") == "passed", "deterministic qualification did not pass")
        require(agent.get("status") == "passed", "agent qualification did not pass")
        require(forks.get("passed") is True, "world-fork qualification did not pass")
        require(derived.get("status") == "frozen_complete", "derived endpoint data is not frozen")

        task_structure = composition["task_structure"]
        coverage = task_structure["coverage"]
        generated = composition["generated_qualification"]
        summary = composition["summary"]
        require(task_structure["registered_task_count"] == 15, "registered task count changed")
        require(len(coverage["operations"]) == 28, "typed operation count changed")
        require(len(coverage["instruments"]) == 5, "instrument count changed")
        require(generated["denominator"] == generated["passed"] == 52, "generated census changed")

        patterns: list[dict[str, Any]] = []
        aggregate_coverage: Counter[str] = Counter()
        reference_topologies = {
            tuple(sorted(str(component).replace("_", " ") for component in task["components"]))
            for task in task_structure["tasks"]
        }
        for row in generated["pattern_matrix"]:
            report = row["coverage_report"]
            denominators = report["denominators"]
            covered = report["covered"]
            require(covered == denominators, f"coverage is incomplete: {row['pattern']}")
            aggregate_coverage.update({key: int(value) for key, value in denominators.items()})
            components = _pattern_components(row["pattern"])
            reference_topology_overlap = tuple(sorted(components)) in reference_topologies
            patterns.append(
                {
                    "pattern": row["pattern"],
                    "components": components,
                    "generated": row["denominator"],
                    "passed": row["passed"],
                    "reference_topology_overlap": reference_topology_overlap,
                    "unseen_reference_identity": row["pattern"] == generated["unseen_pattern"],
                    "discrete_rows": report["discrete_row_count"],
                    "continuous_samples": report["continuous_sample_count"],
                    "workflow_templates": report["workflow_template_count"],
                    "coverage_denominators": denominators,
                }
            )
        require(len(patterns) == 8, "composition pattern count changed")
        new_topology_patterns = [row for row in patterns if not row["reference_topology_overlap"]]
        require(len(new_topology_patterns) == 3, "new-topology pattern count changed")
        require(
            sum(int(row["generated"]) for row in new_topology_patterns) == 18,
            "new-topology case count changed",
        )

        case_names = {
            "U01": "rxn to crystal",
            "U02": "resource eq.",
            "U03/E01": "failure + recovery",
            "U06-flow": "flow",
            "U06-electro": "electrochem.",
            "U06-distillation": "distillation",
            "U06-partition": "partition",
            "U06-crystallization": "crystallization",
        }
        cases: list[dict[str, Any]] = []
        for case in deterministic["cases"]:
            case_id = case["case_id"]
            require(case_id in case_names, f"unregistered deterministic case: {case_id}")
            cases.append(
                {
                    "case_id": case_id,
                    "label": case_names[case_id],
                    "submitted": case["submitted_action_count"],
                    "committed": case["committed_action_count"],
                    "rolled_back": case["rollback_count"],
                    "final_assays": case["committed_final_assay_count"],
                    "exact_replay": case["exact_replay"]["verified"],
                    "resource_reconciled": case["resource_receipt"]["resource_reconciled"],
                    "operations": [action["operation"] for action in case["actions"]],
                }
            )
        recovery_case = next(row for row in deterministic["cases"] if row["case_id"] == "U03/E01")
        recovery = recovery_case["recovery_receipt"]
        rollback = recovery["rollback_recovery_receipt"]
        require(recovery["passed"] is True, "failure-recovery path did not pass")

        fork_rows: list[dict[str, Any]] = []
        class_counts: Counter[str] = Counter()
        public_contract_component_counts: set[int] = set()
        for row in forks["rows"]:
            audit = row["audit"]
            public_contract_component_counts.add(
                audit["public_contract_certificate"]["invariant_component_count"]
            )
            expectations = audit["divergence_evaluation"]["expectation_results"]
            by_channel = {item["channel"]: item for item in expectations}
            require(
                audit["passed"] is True and all(audit["gates"].values()), "world-fork gate failed"
            )
            require(
                set(by_channel) == {"physical_state", "public_observation"},
                "fork divergence channels changed",
            )
            class_counts[audit["intervention_class"]] += 1
            fork_rows.append(
                {
                    "case_id": row["case_id"],
                    "seed": row["seed"],
                    "intervention_class": audit["intervention_class"],
                    "target": audit["target_component_id"],
                    "gates": audit["gates"],
                    "physical_relative_delta": by_channel["physical_state"]["relative_delta"],
                    "observation_relative_delta": by_channel["public_observation"][
                        "relative_delta"
                    ],
                }
            )
        require(len(fork_rows) == 6 and forks["trace_count"] == 24, "world-fork census changed")
        require(
            public_contract_component_counts == {9},
            "world-fork public contract census changed",
        )

        provider = agent["provider_accounting"]
        declared = agent["declared_resource_budget"]
        require(provider["mcp_tool_call_count"] == 17, "agent MCP census changed")
        require(agent["summary"]["submitted_action_count"] == 15, "agent action census changed")
        deterministic_reference = next(row for row in cases if row["case_id"] == "U06-distillation")

        endpoint_pair = next(
            (
                row
                for row in derived["g2_v0_5"]["paired_trajectories"]
                if row["world_seed"] == 1 and row["trajectory_replicate_id"] == "r03"
            ),
            None,
        )
        require(
            endpoint_pair is not None and endpoint_pair["pair_complete"] is True,
            "endpoint-near pair is unavailable",
        )
        endpoint_delta = endpoint_pair["nominal_minus_opaque"]

        data: dict[str, Any] = {
            "schema_version": SCHEMA,
            "status": "current_bound_complete",
            "current_graph_sha256": current["evidence_dag"]["graph_sha256"],
            "source_bindings": bindings,
            "figure_1": {
                "components": coverage["components"],
                "contract_surfaces": [
                    "initial state",
                    "actions",
                    "instruments",
                    "observations",
                    "resources",
                    "termination",
                    "evaluation",
                    "private-law boundary",
                ],
                "hierarchy": ["world", "task contract", "scenario", "trajectory"],
                "reference_counts": {
                    "reference_tasks": task_structure["registered_task_count"],
                    "typed_operations": len(coverage["operations"]),
                    "instruments": len(coverage["instruments"]),
                    "task_metric_bindings": task_structure["task_design_binding"][
                        "bound_success_metric_count"
                    ],
                },
                "construction_counts": {
                    "generated_compositions": generated["denominator"],
                    "controlled_fork_pairs": forks["pair_count"],
                    "fork_traces": forks["trace_count"],
                },
            },
            "figure_2": {
                "patterns": patterns,
                "aggregate_coverage_denominators": dict(sorted(aggregate_coverage.items())),
                "new_topology_pattern_count": len(new_topology_patterns),
                "new_topology_case_count": sum(
                    int(row["generated"]) for row in new_topology_patterns
                ),
                "reference_task_count": task_structure["registered_task_count"],
                "generated_composition_count": generated["denominator"],
                "unseen_composition_count": generated["unseen_denominator"],
                "unseen_passed": generated["unseen_passed"],
                "unseen_pattern": generated["unseen_pattern"],
                "unseen_reference_identity_overlap": len(
                    generated["unseen_reference_task_id_overlap"]
                ),
                "exhaustive_enumeration_claim": False,
            },
            "figure_3": {
                "execution_censuses": [
                    {"label": "reference units", **summary["reference_units"]},
                    {"label": "reference recipes", **summary["reference_recipes"]},
                    {"label": "generated", **summary["generated_compositions"]},
                    {"label": "unseen distillation", **summary["unseen_distillation_compositions"]},
                ],
                "qualification_censuses": [
                    {"label": "module probes", **summary["module_probes"]},
                    {"label": "interface paths", **summary["interface_paths"]},
                    {"label": "invalid declarations", **summary["compile_mutants"]},
                    {"label": "invalid actions", **summary["negative_probes"]},
                ],
                "zero_findings": {
                    "failure_classes": sum(summary["failure_class_counts"].values()),
                    "missing_receipts": summary["missing_receipt_count"],
                    "public_private_leakage": summary["public_private_leakage_count"],
                },
            },
            "figure_4": {
                "cases": cases,
                "totals": deterministic["summary"],
                "recovery": {
                    "rollback_step": recovery["expected_rollback_step"],
                    "rolled_back_operation": recovery_case["actions"][0]["operation"],
                    "subsequent_commits": recovery["subsequent_observed_commit_count"],
                    "physical_state_preserved": rollback["physical"]["preserved"],
                    "observation_rng_preserved": rollback["observation_rng"]["preserved"],
                    "ghost_state_preserved": rollback["ghost_state_preserved"],
                    "declared_penalty_reconciled": rollback["ledger"][
                        "declared_penalty_reconciled"
                    ],
                },
            },
            "figure_5": {
                "pair_count": forks["pair_count"],
                "trace_count": forks["trace_count"],
                "provider_call_count": forks["provider_call_count"],
                "selected_seeds": forks["selected_seeds"],
                "gate_pass_counts": forks["gate_pass_counts"],
                "intervention_class_counts": dict(sorted(class_counts.items())),
                "public_contract_component_count": next(iter(public_contract_component_counts)),
                "rows": fork_rows,
            },
            "figure_6": {
                "deterministic_reference": deterministic_reference,
                "complete_agent": {
                    "submitted": agent["summary"]["submitted_action_count"],
                    "committed": agent["summary"]["committed_action_count"],
                    "rolled_back": agent["summary"]["rollback_count"],
                    "terminate": agent["summary"]["committed_terminate_count"],
                    "final_assay": agent["summary"]["committed_final_assay_count"],
                    "exact_replay": agent["exact_replay"]["verified"],
                    "operations": [row["action"]["operation"] for row in agent["actions"]],
                    "resource_limits": declared["declared_limits"],
                    "resource_usage": declared["observed_usage"],
                    "provider": {
                        "sessions": provider["provider_session_count"],
                        "logical_turns": provider["logical_codex_turn_count"],
                        "mcp_calls": provider["mcp_tool_call_count"],
                        "mcp_steps": provider["mcp_step_count"],
                        "input_tokens": provider["usage"]["prompt_tokens"],
                        "cache_hit_tokens": provider["usage"]["prompt_cache_hit_tokens"],
                        "cache_miss_tokens": provider["usage"]["prompt_cache_miss_tokens"],
                        "output_tokens": provider["usage"]["completion_tokens"],
                    },
                },
                "endpoint_near_example": {
                    "world_seed": endpoint_pair["world_seed"],
                    "trajectory_replicate_id": endpoint_pair["trajectory_replicate_id"],
                    "raw_terminal_score": endpoint_delta["terminal_final_score"],
                    "best_discovery_fraction": endpoint_delta["global_best_discovery_fraction"],
                    "online_retention_rate": endpoint_delta["online_incumbent_retention_rate"],
                    "maximum_drawdown": endpoint_delta["maximum_absolute_incumbent_drawdown"],
                    "terminal_to_best_ratio": endpoint_delta["terminal_to_global_best_ratio"],
                    "claim": "descriptive process-record example only; no model ranking",
                },
            },
            "claim_boundary": {
                "full_census_not_statistical_sample": True,
                "unseen_not_unbounded": True,
                "virtual_instrument_not_physical_lab_validation": True,
                "complete_agent_not_model_ranking": True,
                "endpoint_example_not_provider_effect": True,
            },
        }
        data["figure_data_sha256"] = canonical_sha256(data)
        return data
    finally:
        ROOT = previous_root


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    data = build_figure_data(ROOT)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": data["status"],
                "source_count": len(data["source_bindings"]),
                "figure_data_sha256": data["figure_data_sha256"],
                "output": str(output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
