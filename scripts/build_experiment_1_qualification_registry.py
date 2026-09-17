#!/usr/bin/env python3
"""Build the 105-unit Experiment 1 continuous qualification registry."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "chemworld-experiment-1-continuous-qualification-registry-1.0.1"
SYSTEMS = ("EC", "RX", "PA", "FL", "C", "P", "D")
LOCI = ("entity", "parametric", "structural")
READINESS = {
    "EC": {"entity": "A", "parametric": "A", "structural": "A"},
    "RX": {"entity": "A", "parametric": "A", "structural": "A"},
    "PA": {"entity": "A", "parametric": "B", "structural": "A"},
    "FL": {"entity": "B", "parametric": "B", "structural": "A"},
    "C": {"entity": "A", "parametric": "B", "structural": "A"},
    "P": {"entity": "B", "parametric": "B", "structural": "C"},
    "D": {"entity": "A", "parametric": "B", "structural": "C"},
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _relative(path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"registry path escapes repository: {resolved}")
    return resolved.relative_to(ROOT).as_posix()


def _parse_binding(value: str) -> tuple[str, Path]:
    system, separator, raw_path = value.partition("=")
    if separator != "=" or system not in SYSTEMS or not raw_path:
        raise ValueError(f"invalid --system-registry binding: {value}")
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    return system, path.resolve()


def _load_system_registry(system: str, path: Path) -> dict[str, Any]:
    registry = _load(path)
    expected = canonical_json_sha256(
        {key: value for key, value in registry.items() if key != "registry_sha256"}
    )
    if registry.get("registry_sha256") != expected:
        raise ValueError(f"{system} registry self-hash mismatch")
    rows = registry.get("rows")
    if not isinstance(rows, list) or len(rows) != 15:
        raise ValueError(f"{system} registry must contain 15 rows")
    expected_units = {
        f"{system}-W0{world_index}:{locus}" for world_index in range(1, 6) for locus in LOCI
    }
    actual_units = {str(row.get("unit_id")) for row in rows}
    if actual_units != expected_units:
        raise ValueError(f"{system} registry unit coverage differs")
    if any(row.get("system_id") != system for row in rows):
        raise ValueError(f"{system} registry contains another system")
    if registry.get("formal_result") is not False:
        raise ValueError(f"{system} registry is not a development result")
    if registry.get("provider_call_count", 0) != 0:
        raise ValueError(f"{system} registry used provider calls")
    return registry


def build_registry(bindings: Mapping[str, Path]) -> dict[str, Any]:
    source_registries = {
        system: _load_system_registry(system, path) for system, path in bindings.items()
    }
    source_rows = {
        system: {str(row["unit_id"]): row for row in registry["rows"]}
        for system, registry in source_registries.items()
    }
    rows: list[dict[str, Any]] = []
    for system in SYSTEMS:
        for world_index in range(1, 6):
            world_id = f"{system}-W0{world_index}"
            for locus in LOCI:
                unit_id = f"{world_id}:{locus}"
                source = source_rows.get(system, {}).get(unit_id)
                if source is None:
                    rows.append(
                        {
                            "unit_id": unit_id,
                            "system_id": system,
                            "world_id": world_id,
                            "world_seed": world_index - 1,
                            "prior_locus": locus,
                            "implementation_readiness": READINESS[system][locus],
                            "implementation_status": "proposed",
                            "qualification_status": "pending",
                            "participant_ready_candidate": False,
                            "participant_execution_authorized": False,
                            "blocker": (
                                "system-specific world/prior/qualification contract not yet frozen"
                            ),
                        }
                    )
                    continue
                status = str(source["status"])
                if status not in {"qualified", "failed", "N/A"}:
                    raise ValueError(f"{unit_id} has unsupported source status {status}")
                rows.append(
                    {
                        "unit_id": unit_id,
                        "system_id": system,
                        "world_id": world_id,
                        "world_seed": source["world_seed"],
                        "prior_locus": locus,
                        "implementation_readiness": READINESS[system][locus],
                        "implementation_status": "frozen",
                        "qualification_status": status,
                        "participant_ready_candidate": status == "qualified",
                        "participant_execution_authorized": False,
                        "gates": source.get("gates"),
                        "failures": source.get("failures", []),
                        "denominators": source.get("denominators"),
                        "truth_sha256": source.get("truth_sha256"),
                        "evidence": source.get("evidence"),
                        "source_system_registry": {
                            "path": _relative(bindings[system]),
                            "sha256": file_sha256(bindings[system]),
                            "registry_sha256": source_registries[system]["registry_sha256"],
                        },
                    }
                )

    status_counts = {
        status: sum(row["qualification_status"] == status for row in rows)
        for status in ("qualified", "failed", "pending", "N/A")
    }
    systems: dict[str, Any] = {}
    for system in SYSTEMS:
        system_rows = [row for row in rows if row["system_id"] == system]
        locus_decisions = {}
        for locus in LOCI:
            locus_rows = [row for row in system_rows if row["prior_locus"] == locus]
            statuses = [row["qualification_status"] for row in locus_rows]
            locus_decisions[locus] = (
                "five_world_qualified"
                if statuses == ["qualified"] * 5
                else "completed_with_failures"
                if "pending" not in statuses
                else "pending"
            )
        systems[system] = {
            "qualified_units": sum(
                row["qualification_status"] == "qualified" for row in system_rows
            ),
            "failed_units": sum(row["qualification_status"] == "failed" for row in system_rows),
            "pending_units": sum(row["qualification_status"] == "pending" for row in system_rows),
            "loci": locus_decisions,
            "participant_ready_candidate": all(
                row["qualification_status"] == "qualified" for row in system_rows
            ),
            "participant_execution_authorized": False,
        }
    registry: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "campaign_status": "active",
        "formal_result": False,
        "provider_call_count": 0,
        "participant_execution_authorized": False,
        "denominator": 105,
        "status_counts": status_counts,
        "systems": systems,
        "rows": rows,
    }
    registry["registry_sha256"] = canonical_json_sha256(registry)
    return registry


def render_markdown(registry: Mapping[str, Any]) -> str:
    lines = [
        "# Experiment 1 continuous qualification campaign",
        "",
        "This is a provider-free development qualification registry. Participant and "
        "formal benchmark execution remain unauthorized.",
        "",
        "| System | Qualified | Failed | Pending | Entity | Parametric | Structural |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for system in SYSTEMS:
        value = registry["systems"][system]
        lines.append(
            f"| {system} | {value['qualified_units']} | {value['failed_units']} | "
            f"{value['pending_units']} | {value['loci']['entity']} | "
            f"{value['loci']['parametric']} | {value['loci']['structural']} |"
        )
    counts = registry["status_counts"]
    lines.extend(
        [
            "",
            f"Atomic units: `{counts['qualified']} qualified`, `{counts['failed']} failed`, "
            f"`{counts['pending']} pending`, `{counts['N/A']} N/A` out of `105`.",
            "",
            "A system may be a participant-ready candidate only when all 15 units "
            "qualify; this registry never authorizes Participant execution.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--system-registry",
        action="append",
        default=[],
        metavar="SYSTEM=PATH",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    bindings = dict(_parse_binding(value) for value in args.system_registry)
    if len(bindings) != len(args.system_registry):
        raise ValueError("duplicate --system-registry system binding")
    registry = build_registry(bindings)
    write_json_atomic(args.output.resolve(), registry)
    args.markdown.resolve().write_text(render_markdown(registry), encoding="utf-8")
    print(json.dumps(registry["status_counts"], sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
