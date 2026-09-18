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


def _verify_self_hash(payload: Mapping[str, Any], key: str) -> str:
    declared = payload.get(key)
    if not isinstance(declared, str):
        raise ValueError(f"{key} is missing")
    unhashed = dict(payload)
    unhashed.pop(key, None)
    if canonical_json_sha256(unhashed) != declared:
        raise ValueError(f"{key} canonical self-hash mismatch")
    return declared


def _bound_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("bound artifact path escapes the repository")
    return path


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


def build_audit(registry_path: Path, probes_path: Path) -> dict[str, Any]:
    registry = _load(registry_path)
    probes = _load(probes_path)
    registry_self_hash = _verify_self_hash(registry, "registry_sha256")
    probe_self_hash = _verify_self_hash(probes, "challenge_probe_sha256")
    registry_binding = probes.get("source_registry")
    if not isinstance(registry_binding, Mapping):
        raise ValueError("challenge probes lack the exact registry binding")
    if registry_path.resolve() != _bound_path(str(registry_binding.get("path", ""))):
        raise ValueError("audit registry path differs from the probe binding")
    if file_sha256(registry_path) != registry_binding.get("file_sha256"):
        raise ValueError("audit registry file digest differs from the probe binding")
    if registry_self_hash != registry_binding.get("registry_sha256"):
        raise ValueError("audit registry self-hash differs from the probe binding")
    manifest_binding = probes.get("raw_evidence_manifest")
    if not isinstance(manifest_binding, Mapping):
        raise ValueError("challenge probes lack a raw manifest binding")
    manifest_path = _bound_path(str(manifest_binding.get("path", "")))
    if not manifest_path.is_file() or file_sha256(manifest_path) != manifest_binding.get(
        "file_sha256"
    ):
        raise ValueError("raw evidence manifest file binding mismatch")
    manifest = _load(manifest_path)
    manifest_self_hash = _verify_self_hash(manifest, "manifest_sha256")
    if manifest_self_hash != manifest_binding.get("manifest_sha256"):
        raise ValueError("raw evidence manifest self-hash binding mismatch")
    if manifest.get("source_registry_sha256") != registry_self_hash:
        raise ValueError("raw evidence manifest is stale for the audit registry")
    rows = registry.get("rows")
    if not isinstance(rows, list) or len(rows) != 105:
        raise ValueError("challenge audit requires the complete 105-unit registry")
    if probes.get("schema_version") not in {
        "chemworld-experiment-1-challenge-probes-1.0",
        "chemworld-experiment-1-challenge-probes-1.1",
        "chemworld-experiment-1-challenge-probes-1.2",
    }:
        raise ValueError("unexpected challenge probe schema")
    probe_denominators = probes.get("denominators")
    if not isinstance(probe_denominators, Mapping) or any(
        probe_denominators.get(key) != value
        for key, value in {
            "planned_world_probe_rows": 50,
            "attempted_world_probe_rows": 50,
            "completed_world_probe_rows": 50,
            "candidate_loci": 10,
        }.items()
    ):
        raise ValueError("challenge probe denominator is incomplete")
    if probes.get("source_registry_sha256") != registry_self_hash:
        raise ValueError("challenge probes are bound to a different convergence registry")
    probe_loci = probes.get("loci")
    if not isinstance(probe_loci, list) or len(probe_loci) != 10:
        raise ValueError("challenge probes must contain ten locus decisions")
    probes_by_block = {str(row.get("block")): row for row in probe_loci if isinstance(row, Mapping)}
    if len(probes_by_block) != 10:
        raise ValueError("challenge probe block identifiers are incomplete or duplicated")
    loci: list[dict[str, Any]] = []
    locus_name = {"E": "entity", "P": "parametric", "S": "structural"}
    expected_blocks = tuple(probes_by_block)
    for block in expected_blocks:
        system, short_locus = block.split("-")
        locus = locus_name[short_locus]
        selected = [
            row
            for row in rows
            if row.get("system_id") == system and row.get("prior_locus") == locus
        ]
        if len(selected) != 5:
            raise ValueError(f"{block} registry denominator must contain exactly five Worlds")
        if len({str(row.get("unit_id")) for row in selected}) != 5:
            raise ValueError(f"{block} registry rows are duplicated")
        if any(row.get("current_status") != "qualified-development" for row in selected):
            raise ValueError(f"{block} contains stale or non-qualified registry rows")
        probe = probes_by_block.get(block)
        if not isinstance(probe, Mapping) or probe.get("world_probe_rows") != 5:
            raise ValueError(f"missing five-World challenge probe for {block}")
        probe_checks = probe.get("checks")
        if not isinstance(probe_checks, Mapping):
            raise ValueError(f"missing challenge checks for {block}")

        def probe_check(
            name: str, frozen_checks: Mapping[str, Any] = probe_checks
        ) -> dict[str, str]:
            passed = frozen_checks.get(name) is True
            return {
                "status": "passed" if passed else "failed",
                "evidence": (
                    f"five-World frozen challenge probe {probes['challenge_probe_sha256']}"
                ),
            }

        checks = {
            "schema_symmetry": {
                "status": "passed" if _gate(selected, "Q4_prior_symmetry") else "failed",
                "evidence": "all five development Q4 gates",
            },
            "plausibility": probe_check("plausibility"),
            "non_triviality": probe_check("non_triviality"),
            "information_choice": probe_check("information_choice"),
            "budget_window": probe_check("budget_window"),
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
                "block": block,
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
        "schema_version": "chemworld-experiment-1-challenge-audit-1.2",
        "formal_result": False,
        "provider_call_count": 0,
        "participant_execution_authorized": False,
        "source_registry": {
            "path": _relative(registry_path),
            "file_sha256": file_sha256(registry_path),
            "registry_sha256": registry_self_hash,
        },
        "source_probes": {
            "path": _relative(probes_path),
            "file_sha256": file_sha256(probes_path),
            "challenge_probe_sha256": probe_self_hash,
            "source_commit": probes.get("source_commit"),
        },
        "source_manifest": {
            "path": _relative(manifest_path),
            "file_sha256": file_sha256(manifest_path),
            "manifest_sha256": manifest_self_hash,
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
        "Status: **challenge complete; locus-wise fail-closed**",
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
            "Challenge decisions are locus-wise. A failed locus remains blocked while passing "
            "loci may proceed to a separately frozen process-isolated confirmation contract. "
            "This audit does not itself generate or consume confirmation secret material.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--probes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    audit = build_audit(args.registry.resolve(), args.probes.resolve())
    write_json_atomic(args.output.resolve(), audit)
    written = _load(args.output.resolve())
    if _verify_self_hash(written, "audit_sha256") != audit["audit_sha256"]:
        raise ValueError("written audit self-hash mismatch")
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
