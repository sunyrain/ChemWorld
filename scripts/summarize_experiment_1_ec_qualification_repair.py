#!/usr/bin/env python3
"""Build the EC v1.0.2 repair delta and 15-unit composite registry."""

from __future__ import annotations

import argparse
import copy
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_ec_qualification import EXPECTED_COMMON_GATES
from chemworld.eval.experiment_1_ec_qualification_repair import (
    EXPECTED_WORLD_IDS,
    load_repair_contract,
    validate_parent_parametric_evidence,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_ec_qualification_repair_v1.0.2.json"
DELTA_REGISTRY_VERSION = "chemworld-experiment-1-ec-repair-delta-registry-1.0.2"
COMPOSITE_REGISTRY_VERSION = "chemworld-experiment-1-ec-composite-registry-1.0.2"
SUMMARY_VERSION = "chemworld-experiment-1-ec-repair-summary-1.0.2"
REPAIR_LOCI = ("entity", "structural")
ALL_LOCI = ("entity", "parametric", "structural")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _validate_self_hash(value: Mapping[str, Any], field: str, label: str) -> None:
    expected = canonical_json_sha256({key: item for key, item in value.items() if key != field})
    if value.get(field) != expected:
        raise ValueError(f"{label} self-hash mismatch")


def _relative(path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"evidence path escapes repository: {resolved}")
    return resolved.relative_to(ROOT).as_posix()


def _truth_sha256(report: Mapping[str, Any], locus: str) -> str:
    value = (
        report.get("private_world_audit", {}).get("truth_sha256")
        if locus == "entity"
        else report.get("truth_sha256")
    )
    if not isinstance(value, str):
        raise ValueError(f"{locus} report lacks a truth hash")
    return value


def _load_repair_rows(
    contract: Mapping[str, Any],
    *,
    locus: str,
    summary_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    contract_sha256 = canonical_json_sha256(contract)
    summary = _load(summary_path)
    _validate_self_hash(summary, "summary_sha256", f"{locus} summary")
    if summary.get("contract_sha256") != contract_sha256:
        raise ValueError(f"{locus} summary contract binding differs")
    if summary.get("provider_call_count") != 0:
        raise ValueError(f"{locus} repair used provider calls")
    if summary.get("prior_locus") != locus:
        raise ValueError(f"{locus} summary prior-locus binding differs")
    world_rows = summary.get("worlds")
    if not isinstance(world_rows, list) or len(world_rows) != 5:
        raise ValueError(f"{locus} summary must contain five worlds")
    keyed = {str(row["world_id"]): row for row in world_rows}
    result: list[dict[str, Any]] = []
    for world in contract["worlds"]["qualification"]:
        world_id = str(world["world_id"])
        summary_row = keyed.get(world_id)
        if not isinstance(summary_row, Mapping):
            raise ValueError(f"{locus} summary lacks {world_id}")
        report_path = summary_path.parent / world_id / "world-report.json"
        report = _load(report_path)
        _validate_self_hash(report, "report_sha256", f"{world_id}/{locus} report")
        if (
            report.get("repair_contract_sha256") != contract_sha256
            or report.get("report_sha256") != summary_row.get("report_sha256")
            or report.get("world_seed") != world["world_seed"]
            or report.get("prior_locus") != locus
            or report.get("status") != summary_row.get("status")
        ):
            raise ValueError(f"{world_id}/{locus} report binding differs")
        gates = report.get("gates")
        if not isinstance(gates, Mapping) or tuple(gates) != EXPECTED_COMMON_GATES:
            raise ValueError(f"{world_id}/{locus} gate registry differs")
        result.append(
            {
                "unit_id": f"{world_id}:{locus}",
                "system_id": "EC",
                "world_id": world_id,
                "world_seed": world["world_seed"],
                "prior_locus": locus,
                "status": report["status"],
                "gates": dict(gates),
                "failures": list(report["failures"]),
                "denominators": dict(report["denominators"]),
                "truth_sha256": _truth_sha256(report, locus),
                "supersedes": {
                    "unit_id": f"{world_id}:{locus}",
                    "registry": contract["parent_result"]["registry"]["path"],
                },
                "evidence": {
                    "path": _relative(report_path),
                    "sha256": file_sha256(report_path),
                    "report_sha256": report["report_sha256"],
                },
            }
        )
    actual_all_qualified = all(row["status"] == "qualified" for row in result)
    if summary.get("five_world_qualified") is not actual_all_qualified:
        raise ValueError(f"{locus} five-world decision differs from reports")
    return result, summary


def build_composite(
    contract: Mapping[str, Any],
    *,
    canary_path: Path,
    locus_paths: Mapping[str, Path],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract_sha256 = canonical_json_sha256(contract)
    canary = _load(canary_path)
    _validate_self_hash(canary, "summary_sha256", "repair canary summary")
    if (
        canary.get("passed") is not True
        or canary.get("formal_denominator") is not False
        or canary.get("contract_sha256") != contract_sha256
    ):
        raise ValueError("EC-W00 repair canary did not pass with the frozen contract")

    repair_rows: list[dict[str, Any]] = []
    repair_summaries: dict[str, dict[str, Any]] = {}
    for locus in REPAIR_LOCI:
        rows, summary = _load_repair_rows(
            contract,
            locus=locus,
            summary_path=locus_paths[locus],
        )
        repair_rows.extend(rows)
        repair_summaries[locus] = summary

    parent = validate_parent_parametric_evidence(ROOT, contract)
    if parent["passed"] is not True:
        failures = sorted(key for key, value in parent["checks"].items() if not value)
        raise ValueError(f"parametric carry-forward compatibility failed: {failures}")
    parent_parametric = {
        str(row["world_id"]): copy.deepcopy(dict(row)) for row in parent["parametric_rows"]
    }
    repair_by_unit = {str(row["unit_id"]): row for row in repair_rows}
    truth_checks: dict[str, bool] = {}
    for world_id in EXPECTED_WORLD_IDS:
        truth_values = {
            repair_by_unit[f"{world_id}:entity"]["truth_sha256"],
            repair_by_unit[f"{world_id}:structural"]["truth_sha256"],
            parent_parametric[world_id]["truth_sha256"],
        }
        truth_checks[world_id] = len(truth_values) == 1
    if not all(truth_checks.values()):
        failed = sorted(world_id for world_id, passed in truth_checks.items() if not passed)
        raise ValueError(f"repair/parent truth compatibility failed for {failed}")

    parametric_rows: list[dict[str, Any]] = []
    for world_id in EXPECTED_WORLD_IDS:
        row = parent_parametric[world_id]
        row["carried_forward_from"] = {
            "registry": contract["parent_result"]["registry"]["path"],
            "registry_sha256": contract["parent_result"]["registry"]["self_sha256"],
            "compatibility_audit": "passed",
        }
        parametric_rows.append(row)

    composite_rows: list[dict[str, Any]] = []
    for world_id in EXPECTED_WORLD_IDS:
        for locus in ALL_LOCI:
            composite_rows.append(
                parent_parametric[world_id]
                if locus == "parametric"
                else repair_by_unit[f"{world_id}:{locus}"]
            )
    delta: dict[str, Any] = {
        "schema_version": DELTA_REGISTRY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "repair_contract_sha256": contract_sha256,
        "denominator": 10,
        "rows": repair_rows,
    }
    delta["registry_sha256"] = canonical_json_sha256(delta)
    composite: dict[str, Any] = {
        "schema_version": COMPOSITE_REGISTRY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "repair_contract_sha256": contract_sha256,
        "parent_registry_sha256": contract["parent_result"]["registry"]["self_sha256"],
        "denominator": 15,
        "rows": composite_rows,
    }
    composite["registry_sha256"] = canonical_json_sha256(composite)

    loci: dict[str, dict[str, Any]] = {}
    for locus in ALL_LOCI:
        rows = [row for row in composite_rows if row["prior_locus"] == locus]
        qualified = sum(row["status"] == "qualified" for row in rows)
        loci[locus] = {
            "status": "five_world_qualified" if qualified == 5 else "completed_with_failures",
            "qualified_worlds": qualified,
            "failed_worlds": 5 - qualified,
            "worlds": 5,
            "evidence_origin": "carried_forward_v1.0.1"
            if locus == "parametric"
            else "repair_v1.0.2",
        }
    all_qualified = all(row["status"] == "qualified" for row in composite_rows)
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "repair_contract_sha256": contract_sha256,
        "canary": {
            "status": "passed",
            "formal_denominator": False,
            "path": _relative(canary_path),
            "sha256": file_sha256(canary_path),
            "summary_sha256": canary["summary_sha256"],
        },
        "parametric_carry_forward_compatibility": {
            "passed": True,
            "checks": parent["checks"],
            "truth_match_by_world": truth_checks,
            "parent_registry": parent["registry_path"],
            "parent_summary": parent["summary_path"],
        },
        "qualification_denominator": 15,
        "qualified_units": sum(row["status"] == "qualified" for row in composite_rows),
        "failed_units": sum(row["status"] == "failed" for row in composite_rows),
        "loci": loci,
        "all_ec_units_qualified": all_qualified,
        "ec_development_qualification_completed": True,
        "participant_execution_authorized": False,
        "formal_benchmark_execution_authorized": False,
        "campaign_action": "record_ec_result_and_continue_to_rx",
        "decision": (
            "ec_all_15_units_qualified"
            if all_qualified
            else "ec_completed_with_retained_scientific_failures"
        ),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    return delta, composite, summary


def render_markdown(registry: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    by_unit = {row["unit_id"]: row for row in registry["rows"]}
    lines = [
        "# Experiment 1 EC qualification v1.0.2 — composite development result",
        "",
        "This result combines newly executed entity/structural repair evidence with a "
        "machine-audited carry-forward of the unchanged v1.0.1 parametric block.",
        "",
        "| World | Entity | Parametric | Structural |",
        "| --- | --- | --- | --- |",
    ]
    for world_id in EXPECTED_WORLD_IDS:
        statuses = [by_unit[f"{world_id}:{locus}"]["status"] for locus in ALL_LOCI]
        lines.append(f"| {world_id} | {statuses[0]} | {statuses[1]} | {statuses[2]} |")
    lines.extend(
        [
            "",
            f"Qualified units: `{summary['qualified_units']}/15`.",
            "",
            "Parametric carry-forward compatibility: `passed`.",
            "",
            "Participant and formal benchmark execution remain unauthorized. The continuous "
            "development campaign proceeds to RX whether scientific failures are present "
            "or absent.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--canary", type=Path, required=True)
    parser.add_argument("--entity", type=Path, required=True)
    parser.add_argument("--structural", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    contract = load_repair_contract(ROOT, args.contract.resolve())
    delta, composite, summary = build_composite(
        contract,
        canary_path=args.canary.resolve(),
        locus_paths={
            "entity": args.entity.resolve(),
            "structural": args.structural.resolve(),
        },
    )
    args.output.mkdir(parents=True)
    write_json_atomic(args.output / "repair-delta-registry.json", delta)
    write_json_atomic(args.output / "composite-registry.json", composite)
    write_json_atomic(args.output / "summary.json", summary)
    (args.output / "summary.md").write_text(render_markdown(composite, summary), encoding="utf-8")
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
