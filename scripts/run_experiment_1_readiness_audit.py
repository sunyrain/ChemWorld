#!/usr/bin/env python3
"""Run fail-closed Experiment 1 readiness audits for P or D."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

if __package__:
    from scripts.audit_environment_consistency import run_smoke_audit
else:
    from audit_environment_consistency import run_smoke_audit

from chemworld.eval.experiment_1_ec_qualification import EXPECTED_COMMON_GATES
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_VERSION = "chemworld-experiment-1-readiness-audit-contract-1.0.1"
REGISTRY_VERSION = "chemworld-experiment-1-readiness-audit-registry-1.0.1"
SUMMARY_VERSION = "chemworld-experiment-1-readiness-audit-summary-1.0.1"
EXPECTED = {
    "P": {
        "task_id": "reaction-to-purification",
        "world_ids": tuple(f"P-W0{index}" for index in range(1, 6)),
    },
    "D": {
        "task_id": "reaction-to-distillation",
        "world_ids": tuple(f"D-W0{index}" for index in range(1, 6)),
    },
}
LOCI = ("entity", "parametric", "structural")
REQUIRED_HASH_KEYS = (
    "task_contract_hash",
    "mechanism_hash",
    "score_contract_hash",
    "profile_hash",
    "observation_contract_hash",
)


class ReadinessAuditError(ValueError):
    """Raised when a frozen readiness contract is malformed."""


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReadinessAuditError(f"{path} must contain an object")
    return value


def _validate_binding(value: object, label: str) -> None:
    if not isinstance(value, Mapping):
        raise ReadinessAuditError(f"{label} binding is missing")
    path = ROOT / str(value.get("path", ""))
    if not path.is_file() or file_sha256(path) != value.get("sha256"):
        raise ReadinessAuditError(f"{label} hash binding changed")


def load_contract(path: Path) -> dict[str, Any]:
    contract = _load(path)
    if contract.get("schema_version") != CONTRACT_VERSION:
        raise ReadinessAuditError("contract schema version changed")
    if contract.get("status") != "development_frozen_before_execution":
        raise ReadinessAuditError("contract is not frozen before execution")
    if contract.get("development_only") is not True:
        raise ReadinessAuditError("contract must remain development-only")
    if contract.get("participant_provider_calls") != 0:
        raise ReadinessAuditError("provider calls must remain zero")
    if contract.get("participant_execution_authorized") is not False:
        raise ReadinessAuditError("participant execution must remain disabled")
    if contract.get("formal_benchmark_execution_authorized") is not False:
        raise ReadinessAuditError("formal benchmark execution must remain disabled")
    system = str(contract.get("system_id"))
    expected = EXPECTED.get(system)
    if expected is None or contract.get("task_id") != expected["task_id"]:
        raise ReadinessAuditError("system/task binding changed")
    _validate_binding(contract.get("specification"), "minimum specification")
    _validate_binding(contract.get("system_specification"), "system specification")
    _validate_binding(contract.get("smoke_runner"), "smoke runner")
    _validate_binding(contract.get("readiness_runner"), "readiness runner")
    worlds = contract.get("worlds")
    if not isinstance(worlds, list) or len(worlds) != 5:
        raise ReadinessAuditError("five smoke World rows are required")
    if tuple(str(row.get("world_id")) for row in worlds) != expected["world_ids"]:
        raise ReadinessAuditError("World IDs changed")
    if tuple(int(row.get("world_seed", -1)) for row in worlds) != tuple(range(5)):
        raise ReadinessAuditError("World smoke seeds changed")
    if tuple(contract.get("common_gates", ())) != EXPECTED_COMMON_GATES:
        raise ReadinessAuditError("Q1-Q8 registry changed")
    loci = contract.get("loci")
    if not isinstance(loci, Mapping) or set(loci) != set(LOCI):
        raise ReadinessAuditError("prior locus roster changed")
    for locus in LOCI:
        blockers = loci[locus].get("frozen_blockers")
        if not isinstance(blockers, list) or not blockers:
            raise ReadinessAuditError(f"{locus} must freeze at least one blocker")
    execution = contract.get("execution")
    if not isinstance(execution, Mapping):
        raise ReadinessAuditError("execution policy is missing")
    if execution.get("qualification_denominator_authorized") is not False:
        raise ReadinessAuditError("qualification denominator must remain unauthorized")
    if execution.get("fail_closed_on_missing_prerequisite") is not True:
        raise ReadinessAuditError("missing prerequisites must fail closed")
    if execution.get("overwrite_forbidden") is not True:
        raise ReadinessAuditError("write-once policy changed")
    return contract


def _relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def _smoke_gates(row: Mapping[str, Any]) -> tuple[bool, bool]:
    q2 = bool(
        row.get("verify_status") == "pass"
        and int(row.get("invalid_count", 0)) == 0
        and int(row.get("constitution_failure_count", 0)) == 0
        and int(row.get("ledger_single_source_failures", 0)) == 0
    )
    q3 = bool(
        all(row.get(key) for key in REQUIRED_HASH_KEYS)
        and int(row.get("public_leakage_failures", 0)) == 0
    )
    return q2, q3


def _unit_gates(system: str, locus: str, *, q2: bool, q3: bool) -> dict[str, bool]:
    return {
        "Q1_world_integrity": False,
        "Q2_task_accessibility": q2,
        "Q3_public_contract_invariance": q3,
        "Q4_prior_symmetry": system == "D" and locus == "entity",
        "Q5_identifiability": False,
        "Q6_budgeted_falsifiability": False,
        "Q7_behavioral_relevance": False,
        "Q8_noise_robustness": False,
    }


def _render_summary(summary: Mapping[str, Any]) -> str:
    lines = [
        f"# Experiment 1 {summary['system_id']} readiness audit v1.0.1",
        "",
        "This is a fail-closed development audit. Smoke runs prove environment reachability; "
        "they do not authorize a qualification denominator or Participant execution.",
        "",
        "| World | Entity | Parametric | Structural | Smoke |",
        "| --- | --- | --- | --- | --- |",
    ]
    for world in summary["worlds"]:
        lines.append(
            f"| {world['world_id']} | failed | failed | failed | "
            f"{'passed' if world['smoke_passed'] else 'failed'} |"
        )
    lines.extend(
        [
            "",
            f"Atomic units: `0 qualified`, `{summary['failed_units']} failed`.",
            f"Smoke runs: `{summary['smoke_passed_worlds']}/5 passed`.",
            "",
            "The repair campaign must create a new frozen version; this audit remains immutable.",
        ]
    )
    return "\n".join(lines) + "\n"


def run(contract_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise ReadinessAuditError(f"output already exists: {output}")
    contract = load_contract(contract_path)
    output.mkdir(parents=True)
    system = str(contract["system_id"])
    task_id = str(contract["task_id"])
    max_steps = int(contract["smoke_runner"]["max_steps"])
    smoke_root = output / "smoke"
    smoke_rows: list[dict[str, Any]] = []
    registry_rows: list[dict[str, Any]] = []
    summary_worlds: list[dict[str, Any]] = []
    for world in contract["worlds"]:
        world_id = str(world["world_id"])
        world_seed = int(world["world_seed"])
        row = run_smoke_audit(
            task_id=task_id,
            seed=world_seed,
            output_dir=smoke_root,
            max_steps=max_steps,
        )
        smoke_rows.append(row)
        q2, q3 = _smoke_gates(row)
        smoke_passed = q2 and q3 and row.get("spectra_metric_consistency") != "fail"
        summary_worlds.append({"world_id": world_id, "smoke_passed": smoke_passed})
        diagnostic_truth = {
            "system_id": system,
            "world_id": world_id,
            "world_seed": world_seed,
            "task_id": task_id,
            **{key: row.get(key) for key in REQUIRED_HASH_KEYS},
            "distinct_private_world_certified": False,
        }
        truth_sha256 = canonical_json_sha256(diagnostic_truth)
        for locus in LOCI:
            gates = _unit_gates(system, locus, q2=q2, q3=q3)
            failures = [gate for gate in EXPECTED_COMMON_GATES if not gates[gate]]
            report = {
                "schema_version": "chemworld-experiment-1-readiness-unit-report-1.0.1",
                "unit_id": f"{world_id}:{locus}",
                "system_id": system,
                "world_id": world_id,
                "world_seed": world_seed,
                "prior_locus": locus,
                "status": "failed",
                "diagnostic_only": True,
                "qualification_denominator_authorized": False,
                "gates": gates,
                "failures": failures,
                "frozen_blockers": list(contract["loci"][locus]["frozen_blockers"]),
                "diagnostic_truth": diagnostic_truth,
                "truth_sha256": truth_sha256,
                "smoke": row,
            }
            report_path = output / world_id / locus / "world-report.json"
            write_json_atomic(report_path, report)
            registry_rows.append(
                {
                    "unit_id": report["unit_id"],
                    "system_id": system,
                    "world_id": world_id,
                    "world_seed": world_seed,
                    "prior_locus": locus,
                    "status": "failed",
                    "diagnostic_only": True,
                    "gates": gates,
                    "failures": failures,
                    "denominators": {
                        "planned": 1,
                        "attempted": 1,
                        "completed": int(q2),
                        "exact_replay": int(row.get("verify_status") == "pass"),
                        "platform_failures": int(not q2),
                        "physical_failures": int(row.get("constitution_failure_count", 0)),
                    },
                    "truth_sha256": truth_sha256,
                    "evidence": {
                        "path": _relative(report_path),
                        "sha256": file_sha256(report_path),
                        "report_sha256": canonical_json_sha256(report),
                    },
                }
            )
    smoke_summary = {
        "schema_version": "chemworld-experiment-1-readiness-smoke-summary-1.0.1",
        "system_id": system,
        "task_id": task_id,
        "rows": smoke_rows,
    }
    smoke_summary["summary_sha256"] = canonical_json_sha256(smoke_summary)
    write_json_atomic(output / "smoke-summary.json", smoke_summary)
    registry: dict[str, Any] = {
        "schema_version": REGISTRY_VERSION,
        "contract_sha256": file_sha256(contract_path),
        "denominator": 15,
        "formal_result": False,
        "provider_call_count": 0,
        "qualification_denominator_authorized": False,
        "rows": registry_rows,
    }
    registry["registry_sha256"] = canonical_json_sha256(registry)
    write_json_atomic(output / "composite-registry.json", registry)
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "system_id": system,
        "formal_result": False,
        "qualified_units": 0,
        "failed_units": 15,
        "smoke_passed_worlds": sum(row["smoke_passed"] for row in summary_worlds),
        "worlds": summary_worlds,
        "registry_sha256": registry["registry_sha256"],
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    (output / "summary.md").write_text(_render_summary(summary), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args.contract.resolve(), args.output.resolve())
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
