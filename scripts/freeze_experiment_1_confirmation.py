#!/usr/bin/env python3
"""Freeze sealed Experiment 1 confirmation commitments without revealing coordinates."""

from __future__ import annotations

import argparse
import json
import os
import secrets
from pathlib import Path

from chemworld.eval.experiment_1_confirmation import (
    ELIGIBLE_LOCI,
    build_public_contract,
    realize_secret_plan,
    validate_secret_plan,
    write_secret_once,
)
from chemworld.eval.provenance import file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--secret-dir", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    secret_dir = args.secret_dir.resolve()
    if secret_dir.is_relative_to(ROOT.resolve()):
        raise ValueError("secret directory must remain outside the Git repository")
    if secret_dir.exists():
        raise FileExistsError("refusing to reuse a confirmation secret directory")
    secret_dir.mkdir(parents=True, mode=0o700)
    os.chmod(secret_dir, 0o700)
    salt = secrets.token_bytes(32)
    salt_path = secret_dir / "salt.bin"
    plan_path = secret_dir / "realized-plan.json"
    write_secret_once(salt_path, salt)
    plan = realize_secret_plan(ROOT, salt, source_commit=args.source_commit)
    validate_secret_plan(ROOT, plan)
    serialized = (json.dumps(plan, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_secret_once(plan_path, serialized)
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError("refusing to overwrite a confirmation contract")
    contract = build_public_contract(
        ROOT,
        source_commit=args.source_commit,
        salt_file_sha256=file_sha256(salt_path),
        realized_plan_file_sha256=file_sha256(plan_path),
        realized_plan_sha256=plan["plan_sha256"],
        evidence_roots=[path.resolve() for path in args.evidence_root],
    )
    write_json_atomic(output, contract)
    print(
        json.dumps(
            {
                "status": "frozen-with-sealed-coordinates",
                "eligible_loci": len(ELIGIBLE_LOCI),
                "atomic_units": 35,
                "contract_sha256": contract["contract_sha256"],
                "salt_commitment_sha256": contract["generator"]["secret_salt_file_sha256"],
                "realized_plan_commitment_sha256": contract["generator"][
                    "realized_plan_file_sha256"
                ],
                "output": str(output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
