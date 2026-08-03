"""Build and check the frozen W1-D01 cross-track data contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.work_i_data_contract import (
    CONTRACT_PATH,
    REPORT_PATH,
    build_work_i_data_contract,
    validate_work_i_data_contract,
)

ROOT = Path(__file__).resolve().parents[1]


def _json_text(payload: dict[str, Any]) -> str:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def build_markdown(contract: dict[str, Any]) -> str:
    tracks = contract["track_contracts"]
    sources = contract["source_bindings"]
    units = contract["unit_registry"]
    lines = [
        "# Work I Incremental Data Contract",
        "",
        "Status: **FROZEN**",
        "",
        f"Contract SHA-256: `{contract['contract_sha256']}`",
        "",
        "## Frozen populations",
        "",
        "| Track | Primary unit | Formal counts | Excluded verification evidence |",
        "| --- | --- | --- | --- |",
        (
            "| F | one parent-child fork pair | 6 pairs; 24 total traces | "
            "exact replay traces are verification, not extra pairs |"
        ),
        (
            "| V | one original campaign profile | 30 campaigns; 180 closed "
            "lifecycles | 30 campaigns / 180 lifecycles of deterministic retest |"
        ),
        (
            "| L | one frozen discarded lifecycle | 36 discards in 10 cells; "
            "60 terminal lifecycles total | evaluator shadows are not original "
            "agent decisions or experiments |"
        ),
        "",
        "The L campaign-oracle estimand has exactly nine opportunity cells; "
        "`cell-02` has no discard opportunity and remains null rather than zero.",
        "",
        "## Counting invariants",
        "",
    ]
    lines.extend(
        [
            "- Never pool the distinct F-pair, V-campaign, and L-discard primary units.",
            "- Primitive operations and lifecycle rows are repeated events, not "
            "independent samples.",
            "- Exact replay, deterministic retest, and synthetic qualification "
            "never inflate a primary denominator.",
            "- Every summary discloses its numerator, denominator, and unit.",
            "- Duplicate `(track, record_type, record_id)` keys are fatal.",
            "- Missing numeric values use JSON `null`; NaN, infinity, and string "
            "sentinels are forbidden.",
            "- Failed or unresolved units retain identity, denominator membership, "
            "and failure reasons.",
            "- Complete-case substitution is forbidden for registered primary L estimands.",
        ]
    )
    lines.extend(
        [
            "",
            "## Record schemas",
            "",
            "| Track | Record type | Expected rows | Analysis role |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for track_id in ("F", "V", "L"):
        for record_type, schema in tracks[track_id]["record_schemas"].items():
            count = schema.get("expected_row_count", schema.get("expected_primary_row_count"))
            lines.append(
                f"| {track_id} | `{record_type}` | {count} | `{schema['analysis_role']}` |"
            )
    lines.extend(
        [
            "",
            "## Unit registry",
            "",
            "| Unit ID | Canonical unit | JSON type |",
            "| --- | --- | --- |",
        ]
    )
    for unit_id, definition in units.items():
        lines.append(
            f"| `{unit_id}` | `{definition['canonical_unit']}` | `{definition['json_type']}` |"
        )
    lines.extend(
        [
            "",
            "## Immutable source bindings",
            "",
            "| Artifact | Role | Embedded SHA-256 | File SHA-256 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for source in sources:
        lines.append(
            f"| `{source['artifact_id']}` | `{source['role']}` | "
            f"`{source['embedded_sha256']}` | `{source['file_sha256']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "W1-D01 freezes interfaces and counting semantics only. It executes no "
            "world, agent, provider, or formal shadow assay; reads no formal latent "
            "outcome; and does not regenerate the global derived-data layer, evidence "
            "DAG, ledger, manuscript, figure manifest, or release manifest. W1-D03 "
            "must bind its output to this contract hash.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract-output", type=Path, default=ROOT / CONTRACT_PATH)
    parser.add_argument("--report-output", type=Path, default=ROOT / REPORT_PATH)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract = build_work_i_data_contract(ROOT)
    errors = validate_work_i_data_contract(contract, root=ROOT)
    if errors:
        raise SystemExit("Work I data contract invalid: " + "; ".join(errors))
    json_text = _json_text(contract)
    markdown_text = build_markdown(contract)
    if args.check:
        if args.contract_output.read_text(encoding="utf-8") != json_text:
            raise SystemExit("committed contract differs from deterministic rebuild")
        if args.report_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("committed report differs from deterministic rebuild")
    else:
        args.contract_output.parent.mkdir(parents=True, exist_ok=True)
        args.contract_output.write_text(json_text, encoding="utf-8", newline="\n")
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(markdown_text, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": contract["status"],
                "contract_sha256": contract["contract_sha256"],
                "source_binding_count": len(contract["source_bindings"]),
                "unit_count": len(contract["unit_registry"]),
                "check": bool(args.check),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
