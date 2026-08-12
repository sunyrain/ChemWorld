#!/usr/bin/env python3
"""Authorize or execute the sealed Work II private matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_private_execution import (
    build_private_execution_authorization,
    execute_private_manifest,
    validate_private_execution_authorization,
    validate_private_execution_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
CELL_RUNNER = ROOT / "scripts/run_work_ii_campaign_pilot.py"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _inside_private(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to((ROOT / "runs/private").resolve()):
        raise ValueError(f"{label} must remain under runs/private")
    return resolved


def _write_once(path: Path, payload: dict[str, object]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite private artifact: {path}")
    write_json_atomic(path, payload)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--authorize", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--allow-private-execution", action="store_true")
    parser.add_argument("--clean-release-receipt", type=Path)
    parser.add_argument("--approved-at")
    parser.add_argument("--pricing-source")
    parser.add_argument("--pricing-observed-at")
    parser.add_argument("--cache-hit-input-usd-per-million", type=float)
    parser.add_argument("--cache-miss-input-usd-per-million", type=float)
    parser.add_argument("--output-usd-per-million", type=float)
    parser.add_argument("--private-currency-ceiling-usd", type=float)
    parser.add_argument("--provider-contract-confirmed-by-user", action="store_true")
    parser.add_argument("--credential-rotation-confirmed-by-user", action="store_true")
    parser.add_argument("--private-one-shot-execution-confirmed-by-user", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    preflight_path = _inside_private(args.preflight, "private preflight")
    preflight = _load(preflight_path)
    errors = validate_private_execution_preflight(ROOT, preflight)
    if errors:
        raise RuntimeError("private preflight failed: " + "; ".join(errors))
    if args.authorize:
        required = {
            "--clean-release-receipt": args.clean_release_receipt,
            "--approved-at": args.approved_at,
            "--pricing-source": args.pricing_source,
            "--pricing-observed-at": args.pricing_observed_at,
            "--cache-hit-input-usd-per-million": args.cache_hit_input_usd_per_million,
            "--cache-miss-input-usd-per-million": args.cache_miss_input_usd_per_million,
            "--output-usd-per-million": args.output_usd_per_million,
            "--private-currency-ceiling-usd": args.private_currency_ceiling_usd,
        }
        missing = [name for name, value in required.items() if value is None]
        if not args.provider_contract_confirmed_by_user:
            missing.append("--provider-contract-confirmed-by-user")
        if not args.credential_rotation_confirmed_by_user:
            missing.append("--credential-rotation-confirmed-by-user")
        if not args.private_one_shot_execution_confirmed_by_user:
            missing.append("--private-one-shot-execution-confirmed-by-user")
        if missing:
            raise RuntimeError("private authorization lacks explicit inputs: " + ", ".join(missing))
        authorization = build_private_execution_authorization(
            ROOT,
            preflight,
            args.clean_release_receipt,
            approved_at=args.approved_at,
            pricing_source=args.pricing_source,
            pricing_observed_at=args.pricing_observed_at,
            cache_hit_input_usd_per_million=args.cache_hit_input_usd_per_million,
            cache_miss_input_usd_per_million=args.cache_miss_input_usd_per_million,
            output_usd_per_million=args.output_usd_per_million,
            private_currency_ceiling_usd=args.private_currency_ceiling_usd,
            provider_contract_confirmed_by_user=True,
            credential_rotation_confirmed_by_user=True,
            private_one_shot_execution_confirmed_by_user=True,
        )
        output = _inside_private(args.output, "private authorization")
        output.parent.mkdir(parents=True, exist_ok=True)
        _write_once(output, authorization)
        print(
            json.dumps(
                {
                    "status": authorization["status"],
                    "provider_process_attempts": authorization["initial_schedule"][
                        "provider_process_attempts"
                    ],
                    "authorization_sha256": authorization["authorization_sha256"],
                    "output": str(output),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        return 0
    if not args.allow_private_execution:
        raise RuntimeError("private execution requires --allow-private-execution")
    if args.authorization is None or args.progress_file is None:
        raise RuntimeError("private execution requires --authorization and --progress-file")
    authorization_path = _inside_private(args.authorization, "private authorization")
    authorization = _load(authorization_path)
    authorization_errors = validate_private_execution_authorization(
        ROOT, authorization, preflight
    )
    if authorization_errors:
        raise RuntimeError("private authorization failed: " + "; ".join(authorization_errors))
    report = execute_private_manifest(
        ROOT,
        preflight=preflight,
        authorization=authorization,
        output_root=_inside_private(args.output, "private execution output"),
        progress_path=_inside_private(args.progress_file, "private progress"),
        resume=bool(args.resume),
        cell_runner=CELL_RUNNER,
    )
    print(json.dumps(report, sort_keys=True), flush=True)
    return 0 if report["status"] == "all_private_cells_terminal" else 1


if __name__ == "__main__":
    raise SystemExit(main())
