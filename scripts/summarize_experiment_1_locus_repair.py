#!/usr/bin/env python3
"""Bind one five-World locus repair into a versioned composite registry."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_c_qualification import load_contract as load_c_contract
from chemworld.eval.experiment_1_ec_qualification import EXPECTED_COMMON_GATES
from chemworld.eval.experiment_1_pa_qualification import load_contract as load_pa_contract
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
LOADERS: dict[str, Callable[[Path, Path], dict[str, Any]]] = {
    "C": load_c_contract,
    "PA": load_pa_contract,
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
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


def build(
    *,
    system_id: str,
    locus: str,
    version: str,
    contract_path: Path,
    baseline_registry_path: Path,
    repair_summary_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if system_id not in LOADERS:
        raise ValueError(f"unsupported system: {system_id}")
    if locus not in {"entity", "parametric", "structural"}:
        raise ValueError(f"unsupported locus: {locus}")
    contract = LOADERS[system_id](ROOT, contract_path)
    contract_sha256 = canonical_json_sha256(contract)
    repair_summary = _load(repair_summary_path)
    _validate_self_hash(repair_summary, "summary_sha256", "repair summary")
    if repair_summary.get("contract_sha256") != contract_sha256:
        raise ValueError("repair summary does not bind the resolved repair contract")
    if repair_summary.get("provider_call_count") != 0:
        raise ValueError("repair evidence used provider calls")
    if repair_summary.get("prior_locus") != locus:
        raise ValueError("repair evidence locus differs")

    baseline = _load(baseline_registry_path)
    _validate_self_hash(baseline, "registry_sha256", "baseline registry")
    baseline_rows = baseline.get("rows")
    if not isinstance(baseline_rows, list) or len(baseline_rows) != 15:
        raise ValueError("baseline registry must contain 15 rows")
    keyed = {str(row["unit_id"]): row for row in baseline_rows}

    world_rows = repair_summary.get("worlds")
    if not isinstance(world_rows, list) or len(world_rows) != 5:
        raise ValueError("repair summary must contain five Worlds")
    repair_by_world = {str(row["world_id"]): row for row in world_rows}
    delta_rows: list[dict[str, Any]] = []
    replacements: dict[str, dict[str, Any]] = {}
    for world in contract["worlds"]["qualification"]:
        world_id = str(world["world_id"])
        unit_id = f"{world_id}:{locus}"
        old = keyed.get(unit_id)
        if not isinstance(old, Mapping):
            raise ValueError(f"baseline registry lacks {unit_id}")
        summary_row = repair_by_world.get(world_id)
        if not isinstance(summary_row, Mapping):
            raise ValueError(f"repair summary lacks {world_id}")
        report_path = repair_summary_path.parent / world_id / "world-report.json"
        report = _load(report_path)
        _validate_self_hash(report, "report_sha256", f"{unit_id} repair report")
        gates = report.get("gates")
        if not isinstance(gates, Mapping) or tuple(gates) != EXPECTED_COMMON_GATES:
            raise ValueError(f"{unit_id} gate registry differs")
        if (
            report.get("world_seed") != world["world_seed"]
            or report.get("world_id") != world_id
            or report.get("prior_locus") != locus
            or report.get("status") != summary_row.get("status")
            or report.get("report_sha256") != summary_row.get("report_sha256")
        ):
            raise ValueError(f"{unit_id} report binding differs")
        if report.get("truth_sha256") != old.get("truth_sha256"):
            raise ValueError(f"{unit_id} repair changed shared World truth")
        new_row = {
            "unit_id": unit_id,
            "system_id": system_id,
            "world_id": world_id,
            "world_seed": world["world_seed"],
            "prior_locus": locus,
            "status": report["status"],
            "qualification_stage": "development",
            "version": version,
            "gates": dict(gates),
            "failures": list(report["failures"]),
            "denominators": dict(report["denominators"]),
            "truth_sha256": report["truth_sha256"],
            "evidence": {
                "path": _relative(report_path),
                "sha256": file_sha256(report_path),
                "report_sha256": report["report_sha256"],
            },
            "supersedes": {
                "version": "v1.0.1",
                "status": old["status"],
                "evidence": dict(old["evidence"]),
            },
        }
        replacements[unit_id] = new_row
        delta_rows.append(new_row)

    composite_rows = []
    for row in baseline_rows:
        unit_id = str(row["unit_id"])
        if unit_id in replacements:
            composite_rows.append(replacements[unit_id])
        else:
            carried = dict(row)
            carried.setdefault("version", "v1.0.1")
            carried.setdefault("qualification_stage", "development")
            composite_rows.append(carried)

    delta: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-locus-repair-delta-1.0",
        "formal_result": False,
        "provider_call_count": 0,
        "system_id": system_id,
        "locus": locus,
        "version": version,
        "resolved_contract_sha256": contract_sha256,
        "contract_file": {
            "path": _relative(contract_path),
            "sha256": file_sha256(contract_path),
        },
        "repair_summary": {
            "path": _relative(repair_summary_path),
            "sha256": file_sha256(repair_summary_path),
            "summary_sha256": repair_summary["summary_sha256"],
        },
        "rows": delta_rows,
    }
    delta["registry_sha256"] = canonical_json_sha256(delta)
    composite: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-composite-registry-1.0.2",
        "formal_result": False,
        "provider_call_count": 0,
        "system_id": system_id,
        "version": version,
        "denominator": 15,
        "baseline_registry": {
            "path": _relative(baseline_registry_path),
            "sha256": file_sha256(baseline_registry_path),
            "registry_sha256": baseline["registry_sha256"],
        },
        "repair_delta_sha256": delta["registry_sha256"],
        "rows": composite_rows,
    }
    composite["registry_sha256"] = canonical_json_sha256(composite)
    qualified = sum(row["status"] == "qualified" for row in composite_rows)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-locus-repair-summary-1.0",
        "formal_result": False,
        "provider_call_count": 0,
        "system_id": system_id,
        "locus": locus,
        "version": version,
        "qualification_stage": "development",
        "qualification_denominator": 15,
        "qualified_units": qualified,
        "failed_units": 15 - qualified,
        "repaired_locus_qualified_worlds": sum(row["status"] == "qualified" for row in delta_rows),
        "repaired_locus_five_world_qualified": all(
            row["status"] == "qualified" for row in delta_rows
        ),
        "participant_execution_authorized": False,
        "formal_benchmark_execution_authorized": False,
        "composite_registry_sha256": composite["registry_sha256"],
        "repair_delta_sha256": delta["registry_sha256"],
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    return delta, composite, summary


def render_markdown(composite: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    rows = {str(row["unit_id"]): row for row in composite["rows"]}
    system_id = str(summary["system_id"])
    lines = [
        f"# Experiment 1 {system_id} {summary['version']} — development composite",
        "",
        "| World | Entity | Parametric | Structural |",
        "| --- | --- | --- | --- |",
    ]
    for index in range(1, 6):
        world_id = f"{system_id}-W0{index}"
        status = [
            rows[f"{world_id}:{locus}"]["status"]
            for locus in ("entity", "parametric", "structural")
        ]
        lines.append(f"| {world_id} | {status[0]} | {status[1]} | {status[2]} |")
    lines.extend(
        [
            "",
            f"Qualified units: `{summary['qualified_units']}/15`.",
            "",
            "This is development qualification. Superseded evidence remains bound in the registry; "
            "Participant and formal benchmark execution remain unauthorized.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system", choices=tuple(sorted(LOADERS)), required=True)
    parser.add_argument("--locus", choices=("entity", "parametric", "structural"), required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--baseline-registry", type=Path, required=True)
    parser.add_argument("--repair-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    delta, composite, summary = build(
        system_id=args.system,
        locus=args.locus,
        version=args.version,
        contract_path=args.contract.resolve(),
        baseline_registry_path=args.baseline_registry.resolve(),
        repair_summary_path=args.repair_summary.resolve(),
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
