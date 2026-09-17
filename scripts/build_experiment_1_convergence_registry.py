#!/usr/bin/env python3
"""Build the audit-facing 105-unit Experiment 1 convergence registry."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
SYSTEMS = ("EC", "RX", "PA", "FL", "C", "P", "D")
LOCI = ("entity", "parametric", "structural")
READINESS_SYSTEMS = {"P", "D"}
READINESS_CONTRACTS = {
    "P": ROOT / "configs/benchmark/experiment_1_p_readiness_v1.0.1.json",
    "D": ROOT / "configs/benchmark/experiment_1_d_readiness_v1.0.1.json",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _relative(path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"path escapes repository: {resolved}")
    return resolved.relative_to(ROOT).as_posix()


def _binding(value: str, *, choices: tuple[str, ...] = SYSTEMS) -> tuple[str, str]:
    key, separator, raw = value.partition("=")
    if separator != "=" or key not in choices or not raw:
        raise ValueError(f"invalid binding: {value}")
    return key, raw


def _registry_binding(value: str) -> tuple[str, Path]:
    system, raw = _binding(value)
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return system, path.resolve()


def _self_hash(registry: Mapping[str, Any]) -> str:
    return canonical_json_sha256(
        {key: value for key, value in registry.items() if key != "registry_sha256"}
    )


def _validate_system_registry(system: str, path: Path) -> dict[str, Any]:
    registry = _load(path)
    if registry.get("registry_sha256") != _self_hash(registry):
        raise ValueError(f"{system} registry self-hash mismatch")
    rows = registry.get("rows")
    if not isinstance(rows, list) or len(rows) != 15:
        raise ValueError(f"{system} registry must contain 15 rows")
    expected = {f"{system}-W0{world}:{locus}" for world in range(1, 6) for locus in LOCI}
    if {str(row.get("unit_id")) for row in rows} != expected:
        raise ValueError(f"{system} registry does not cover the expected 15 units")
    return registry


def _prior_hashes(row: Mapping[str, Any]) -> dict[str, str] | None:
    evidence = row.get("evidence")
    if not isinstance(evidence, Mapping) or not isinstance(evidence.get("path"), str):
        return None
    report_path = ROOT / str(evidence["path"])
    if not report_path.is_file():
        return None
    report = _load(report_path)
    prior = report.get("prior_audit")
    if not isinstance(prior, Mapping):
        return None
    arm_hashes = prior.get("arm_sha256")
    if isinstance(arm_hashes, Mapping):
        return {str(key): str(value) for key, value in arm_hashes.items()}
    result = {
        key.removesuffix("_sha256"): str(value)
        for key, value in prior.items()
        if key.endswith("_sha256") and isinstance(value, str)
    }
    return result or None


def _readiness_blockers(system: str) -> dict[str, list[str]]:
    contract = _load(READINESS_CONTRACTS[system])
    return {
        locus: [str(value) for value in contract["loci"][locus]["frozen_blockers"]]
        for locus in LOCI
    }


def build_registry(
    *,
    bindings: Mapping[str, Path],
    versions: Mapping[str, str],
    repair_ledger: Path,
) -> dict[str, Any]:
    if set(bindings) != set(SYSTEMS):
        raise ValueError("all seven system registries are required")
    if set(versions) != set(SYSTEMS):
        raise ValueError("all seven system versions are required")
    registries = {
        system: _validate_system_registry(system, path) for system, path in bindings.items()
    }
    ledger = _load(repair_ledger)
    block_by_id = {str(block["block"]): block for block in ledger.get("blocks", [])}
    readiness = {system: _readiness_blockers(system) for system in READINESS_SYSTEMS}
    rows: list[dict[str, Any]] = []
    for system in SYSTEMS:
        source_rows = {str(row["unit_id"]): row for row in registries[system]["rows"]}
        for world_index in range(1, 6):
            world_id = f"{system}-W0{world_index}"
            for locus in LOCI:
                unit_id = f"{world_id}:{locus}"
                source = source_rows[unit_id]
                block = block_by_id.get(f"{system}-{locus[0].upper()}", {})
                if system in READINESS_SYSTEMS:
                    current_status = "readiness-blocked"
                    blocker: Any = readiness[system][locus]
                    version = str(block.get("baseline_version", versions[system]))
                    qualification_run_type = "diagnostic-readiness-audit"
                elif source.get("status") == "qualified":
                    # A locus-level ledger decision diagnoses or repairs the failed rows; it
                    # does not retroactively invalidate sibling Worlds whose frozen evidence
                    # still passes Q1-Q8. Scope invalidation is represented by a superseding
                    # system registry, not by painting every row with the block headline.
                    current_status = "qualified-development"
                    blocker = None
                    version = str(
                        source.get("version", block.get("target_version", versions[system]))
                    )
                    qualification_run_type = "development-qualification"
                elif source.get("status") == "N/A":
                    current_status = "N/A"
                    blocker = block.get("decision")
                    version = str(
                        source.get("version", block.get("target_version", versions[system]))
                    )
                    qualification_run_type = "development-qualification"
                else:
                    current_status = str(block.get("current_status", "failed-development"))
                    blocker = block.get("decision", source.get("failures", []))
                    version = str(
                        block.get("target_version", source.get("version", versions[system]))
                    )
                    qualification_run_type = "development-qualification"
                evidence = source.get("evidence")
                row = {
                    "unit_id": unit_id,
                    "system_id": system,
                    "world_id": world_id,
                    "world_seed": source.get("world_seed"),
                    "prior_locus": locus,
                    "current_status": current_status,
                    "version": version,
                    "truth_sha256": source.get("truth_sha256"),
                    "prior_hashes": _prior_hashes(source),
                    "qualification_run": {
                        "type": qualification_run_type,
                        "source_registry": {
                            "path": _relative(bindings[system]),
                            "file_sha256": file_sha256(bindings[system]),
                            "registry_sha256": registries[system]["registry_sha256"],
                        },
                        "evidence": evidence,
                        "denominators": source.get("denominators"),
                        "gates": source.get("gates"),
                        "failures": source.get("failures", []),
                    },
                    "confirmation_run": None,
                    "supersedes": source.get("supersedes"),
                    "superseded_by": None,
                    "blocker": blocker,
                    "participant_ready": current_status == "qualified-confirmed",
                    "participant_execution_authorized": False,
                }
                rows.append(row)
    counts = dict(sorted(Counter(str(row["current_status"]) for row in rows).items()))
    systems = {}
    for system in SYSTEMS:
        selected = [row for row in rows if row["system_id"] == system]
        systems[system] = {
            "version": versions[system],
            "status_counts": dict(
                sorted(Counter(str(row["current_status"]) for row in selected).items())
            ),
            "participant_ready_units": sum(bool(row["participant_ready"]) for row in selected),
            "participant_execution_authorized": False,
        }
    registry: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-convergence-registry-1.0",
        "campaign_status": "development_evidence_complete_confirmation_pending",
        "formal_result": False,
        "provider_call_count": 0,
        "participant_execution_authorized": False,
        "denominator": 105,
        "status_counts": counts,
        "systems": systems,
        "repair_ledger": {
            "path": _relative(repair_ledger),
            "sha256": file_sha256(repair_ledger),
        },
        "rows": rows,
    }
    registry["registry_sha256"] = canonical_json_sha256(registry)
    return registry


def render_markdown(registry: Mapping[str, Any]) -> str:
    statuses = sorted(registry["status_counts"])
    lines = [
        "# Experiment 1 benchmark convergence registry",
        "",
        "This registry distinguishes development qualification, readiness blocking, and "
        "confirmation. It does not authorize Participant execution.",
        "",
        "| System | " + " | ".join(statuses) + " | Participant-ready |",
        "| --- | " + " | ".join("---:" for _ in statuses) + " | ---: |",
    ]
    for system in SYSTEMS:
        values = registry["systems"][system]
        counts = values["status_counts"]
        lines.append(
            f"| {system} | "
            + " | ".join(str(counts.get(status, 0)) for status in statuses)
            + f" | {values['participant_ready_units']} |"
        )
    lines.extend(
        [
            "",
            "Current status counts: `"
            + ", ".join(f"{status}={count}" for status, count in registry["status_counts"].items())
            + "`.",
            "",
            "A development PASS is not a confirmation PASS. Participant execution remains "
            "unauthorized.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system-registry", action="append", default=[])
    parser.add_argument("--system-version", action="append", default=[])
    parser.add_argument("--repair-ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    bindings = dict(_registry_binding(value) for value in args.system_registry)
    versions = dict(_binding(value) for value in args.system_version)
    repair_ledger = args.repair_ledger.resolve()
    registry = build_registry(
        bindings=bindings,
        versions=versions,
        repair_ledger=repair_ledger,
    )
    write_json_atomic(args.output.resolve(), registry)
    args.markdown.resolve().write_text(render_markdown(registry), encoding="utf-8")
    print(json.dumps(registry["status_counts"], sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
