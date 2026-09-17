#!/usr/bin/env python3
"""Build the immutable 15-row Experiment 1 PA qualification registry."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.experiment_1_ec_qualification import EXPECTED_COMMON_GATES
from chemworld.eval.experiment_1_pa_qualification import load_contract
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "configs/benchmark/experiment_1_pa_qualification_v1.0.1.json"
SUMMARY_VERSION = "chemworld-experiment-1-pa-qualification-summary-1.0.1"
REGISTRY_VERSION = "chemworld-experiment-1-pa-qualification-registry-1.0.1"
LOCI = ("entity", "parametric", "structural")


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


def build_registry(
    contract: Mapping[str, Any],
    *,
    canary_path: Path,
    locus_paths: Mapping[str, Path],
) -> tuple[dict[str, Any], dict[str, Any]]:
    contract_sha256 = canonical_json_sha256(contract)
    canary = _load(canary_path)
    _validate_self_hash(canary, "summary_sha256", "PA canary summary")
    if (
        canary.get("passed") is not True
        or canary.get("formal_denominator") is not False
        or canary.get("contract_sha256") != contract_sha256
    ):
        raise ValueError("PA-W00 canary did not pass with the frozen contract")

    rows: list[dict[str, Any]] = []
    locus_summaries: dict[str, dict[str, Any]] = {}
    truths: dict[str, set[str]] = {}
    for locus in LOCI:
        summary_path = locus_paths[locus]
        summary = _load(summary_path)
        _validate_self_hash(summary, "summary_sha256", f"{locus} summary")
        if summary.get("contract_sha256") != contract_sha256:
            raise ValueError(f"{locus} summary contract binding differs")
        if summary.get("provider_call_count") != 0:
            raise ValueError(f"{locus} qualification used provider calls")
        world_rows = summary.get("worlds")
        if not isinstance(world_rows, list) or len(world_rows) != 5:
            raise ValueError(f"{locus} summary must contain five worlds")
        keyed = {str(row["world_id"]): row for row in world_rows}
        for world in contract["worlds"]["qualification"]:
            world_id = str(world["world_id"])
            summary_row = keyed.get(world_id)
            if not isinstance(summary_row, Mapping):
                raise ValueError(f"{locus} summary lacks {world_id}")
            report_path = summary_path.parent / world_id / "world-report.json"
            report = _load(report_path)
            _validate_self_hash(report, "report_sha256", f"{world_id}/{locus} report")
            if (
                report.get("report_sha256") != summary_row.get("report_sha256")
                or report.get("world_seed") != world["world_seed"]
                or report.get("prior_locus") != locus
                or report.get("status") != summary_row.get("status")
            ):
                raise ValueError(f"{world_id}/{locus} report binding differs")
            gates = report.get("gates")
            if not isinstance(gates, Mapping) or tuple(gates) != EXPECTED_COMMON_GATES:
                raise ValueError(f"{world_id}/{locus} gate registry differs")
            truth_sha256 = report.get("truth_sha256")
            if not isinstance(truth_sha256, str):
                raise ValueError(f"{world_id}/{locus} truth binding is missing")
            truths.setdefault(world_id, set()).add(truth_sha256)
            rows.append(
                {
                    "unit_id": f"{world_id}:{locus}",
                    "system_id": "PA",
                    "world_id": world_id,
                    "world_seed": world["world_seed"],
                    "prior_locus": locus,
                    "status": report["status"],
                    "gates": dict(gates),
                    "failures": list(report["failures"]),
                    "denominators": dict(report["denominators"]),
                    "truth_sha256": truth_sha256,
                    "evidence": {
                        "path": _relative(report_path),
                        "sha256": file_sha256(report_path),
                        "report_sha256": report["report_sha256"],
                    },
                }
            )
        actual_all_qualified = all(
            row["status"] == "qualified" for row in rows if row["prior_locus"] == locus
        )
        if summary.get("five_world_qualified") is not actual_all_qualified:
            raise ValueError(f"{locus} five-world decision differs from reports")
        locus_summaries[locus] = {
            "status": "five_world_qualified" if actual_all_qualified else "completed_with_failures",
            "qualified_worlds": sum(
                row["status"] == "qualified" for row in rows if row["prior_locus"] == locus
            ),
            "worlds": 5,
            "summary": {
                "path": _relative(summary_path),
                "sha256": file_sha256(summary_path),
                "summary_sha256": summary["summary_sha256"],
            },
        }
    truth_match = {world_id: len(values) == 1 for world_id, values in truths.items()}
    if not all(truth_match.values()):
        failed = sorted(world_id for world_id, passed in truth_match.items() if not passed)
        raise ValueError(f"cross-locus PA truth mismatch: {failed}")
    registry: dict[str, Any] = {
        "schema_version": REGISTRY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "contract_sha256": contract_sha256,
        "denominator": 15,
        "rows": rows,
    }
    registry["registry_sha256"] = canonical_json_sha256(registry)
    all_qualified = all(row["status"] == "qualified" for row in rows)
    summary = {
        "schema_version": SUMMARY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "contract_sha256": contract_sha256,
        "canary": {
            "status": "passed",
            "formal_denominator": False,
            "path": _relative(canary_path),
            "sha256": file_sha256(canary_path),
            "summary_sha256": canary["summary_sha256"],
        },
        "truth_match_by_world": truth_match,
        "qualification_denominator": 15,
        "qualified_units": sum(row["status"] == "qualified" for row in rows),
        "failed_units": sum(row["status"] == "failed" for row in rows),
        "loci": locus_summaries,
        "all_pa_units_qualified": all_qualified,
        "pa_development_qualification_completed": True,
        "participant_execution_authorized": False,
        "formal_benchmark_execution_authorized": False,
        "campaign_action": "record_pa_result_and_continue_to_fl",
        "decision": (
            "pa_all_15_units_qualified"
            if all_qualified
            else "pa_completed_with_retained_scientific_failures"
        ),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    return registry, summary


def render_markdown(registry: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    by_unit = {row["unit_id"]: row for row in registry["rows"]}
    lines = [
        "# Experiment 1 PA qualification v1.0.1 — development result",
        "",
        "| World | Entity | Parametric | Structural |",
        "| --- | --- | --- | --- |",
    ]
    for world_index in range(1, 6):
        world_id = f"PA-W0{world_index}"
        statuses = [by_unit[f"{world_id}:{locus}"]["status"] for locus in LOCI]
        lines.append(f"| {world_id} | {statuses[0]} | {statuses[1]} | {statuses[2]} |")
    lines.extend(
        [
            "",
            f"Qualified units: `{summary['qualified_units']}/15`.",
            "",
            "Scientific failures are retained. Participant and formal benchmark execution "
            "remain unauthorized.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--canary", type=Path, required=True)
    parser.add_argument("--entity", type=Path, required=True)
    parser.add_argument("--parametric", type=Path, required=True)
    parser.add_argument("--structural", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    contract = load_contract(ROOT, args.contract.resolve())
    registry, summary = build_registry(
        contract,
        canary_path=args.canary.resolve(),
        locus_paths={
            "entity": args.entity.resolve(),
            "parametric": args.parametric.resolve(),
            "structural": args.structural.resolve(),
        },
    )
    args.output.mkdir(parents=True)
    write_json_atomic(args.output / "registry.json", registry)
    write_json_atomic(args.output / "summary.json", summary)
    (args.output / "summary.md").write_text(render_markdown(registry, summary), encoding="utf-8")
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

