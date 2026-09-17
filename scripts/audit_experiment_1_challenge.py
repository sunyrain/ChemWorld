#!/usr/bin/env python3
"""Fail-closed challenge audit for Experiment 1 development-qualified loci."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]


def _relative(path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"path escapes repository: {resolved}")
    return resolved.relative_to(ROOT).as_posix()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _gate(rows: list[Mapping[str, Any]], gate: str) -> bool:
    return bool(
        rows
        and all(
            isinstance(row.get("qualification_run"), Mapping)
            and isinstance(row["qualification_run"].get("gates"), Mapping)
            and row["qualification_run"]["gates"].get(gate) is True
            for row in rows
        )
    )


def build_audit(registry_path: Path) -> dict[str, Any]:
    registry = _load(registry_path)
    rows = registry.get("rows")
    if not isinstance(rows, list) or len(rows) != 105:
        raise ValueError("challenge audit requires the complete 105-unit registry")
    loci: list[dict[str, Any]] = []
    systems = ("EC", "RX", "PA", "FL", "C", "P", "D")
    locus_ids = ("entity", "parametric", "structural")
    for system in systems:
        for locus in locus_ids:
            selected = [
                row
                for row in rows
                if row.get("system_id") == system and row.get("prior_locus") == locus
            ]
            if not selected or any(
                row.get("current_status") != "qualified-development" for row in selected
            ):
                continue
            checks = {
                "schema_symmetry": {
                    "status": "passed" if _gate(selected, "Q4_prior_symmetry") else "failed",
                    "evidence": "all five development Q4 gates",
                },
                "plausibility": {
                    "status": "blocked-evidence",
                    "evidence": "no frozen system-specific false-claim envelope audit is bound",
                },
                "non_triviality": {
                    "status": "blocked-evidence",
                    "evidence": (
                        "no frozen default/one-shot cross-World discriminator audit is bound"
                    ),
                },
                "information_choice": {
                    "status": "blocked-evidence",
                    "evidence": (
                        "Q5/Q6 do not by themselves prove that an active choice adds information"
                    ),
                },
                "budget_window": {
                    "status": "blocked-evidence",
                    "evidence": (
                        "all five Q6 gates pass, but the frozen trivial_lower_bound cost is absent"
                        if _gate(selected, "Q6_budgeted_falsifiability")
                        else "one or more development Q6 gates fail"
                    ),
                },
                "consequence": {
                    "status": "passed" if _gate(selected, "Q7_behavioral_relevance") else "failed",
                    "evidence": "all five development Q7 gates",
                },
                "leakage": {
                    "status": "passed"
                    if _gate(selected, "Q3_public_contract_invariance")
                    else "failed",
                    "evidence": "all five development Q3 gates",
                },
            }
            eligible = all(value["status"] == "passed" for value in checks.values())
            loci.append(
                {
                    "block": f"{system}-{locus[0].upper()}",
                    "system_id": system,
                    "prior_locus": locus,
                    "development_qualified_worlds": 5,
                    "checks": checks,
                    "confirmation_eligible": eligible,
                    "decision": (
                        "eligible-for-process-isolated-confirmation"
                        if eligible
                        else "confirmation-blocked-fail-closed"
                    ),
                }
            )
    audit: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-challenge-audit-1.0",
        "formal_result": False,
        "provider_call_count": 0,
        "participant_execution_authorized": False,
        "source_registry": {
            "path": _relative(registry_path),
            "file_sha256": file_sha256(registry_path),
            "registry_sha256": registry.get("registry_sha256"),
        },
        "candidate_loci": len(loci),
        "confirmation_eligible_loci": sum(row["confirmation_eligible"] for row in loci),
        "confirmation_blocked_loci": sum(not row["confirmation_eligible"] for row in loci),
        "loci": loci,
    }
    audit["audit_sha256"] = canonical_json_sha256(audit)
    return audit


def render_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Experiment 1 challenge audit",
        "",
        "Status: **fail-closed before confirmation**",
        "",
        "The audit covers every locus whose five Worlds are currently "
        "`qualified-development`. A development gate is not silently promoted into "
        "challenge evidence.",
        "",
        "| Block | Symmetry | Plausibility | Non-triviality | Information choice | "
        "Budget window | Consequence | Leakage | Confirmation |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    labels = (
        "schema_symmetry",
        "plausibility",
        "non_triviality",
        "information_choice",
        "budget_window",
        "consequence",
        "leakage",
    )
    for row in audit["loci"]:
        values = [row["checks"][label]["status"] for label in labels]
        lines.append(f"| {row['block']} | " + " | ".join(values) + f" | {row['decision']} |")
    lines.extend(
        [
            "",
            f"Candidate loci: `{audit['candidate_loci']}`; confirmation eligible: "
            f"`{audit['confirmation_eligible_loci']}`; blocked: "
            f"`{audit['confirmation_blocked_loci']}`.",
            "",
            "The common blockers are missing frozen evidence for false-prior plausibility, "
            "default/one-shot non-triviality, active information choice, and the lower edge "
            "of the budget window. Confirmation was therefore not started. This is an "
            "evidence-readiness result, not proof that all ten scientific questions are bad.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    audit = build_audit(args.registry.resolve())
    write_json_atomic(args.output.resolve(), audit)
    args.markdown.resolve().write_text(render_markdown(audit), encoding="utf-8")
    print(
        json.dumps(
            {
                "candidate_loci": audit["candidate_loci"],
                "confirmation_eligible_loci": audit["confirmation_eligible_loci"],
                "confirmation_blocked_loci": audit["confirmation_blocked_loci"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
