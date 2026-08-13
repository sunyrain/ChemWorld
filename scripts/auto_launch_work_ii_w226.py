#!/usr/bin/env python3
"""Launch the full W2-26 provider calibration as soon as all nine tasks resolve."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_resource_calibration_v02 import (
    build_authorization,
    build_execution_manifest,
    validate_authorization,
    validate_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_resource_calibration_manifest_v0.2.json"
)
DEFAULT_MANIFEST = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-26-execution-manifest-v0.2.json"
)
DEFAULT_AUTHORIZATION = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-26-calibration-authorization-v0.2.json"
)
DEFAULT_EXECUTION_ROOT = (
    ROOT / "runs/development/work-ii-w2-26-nine-task-calibration-20260813"
)
RUNNER = ROOT / "scripts/run_work_ii_resource_calibration.py"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _inside_root(path: Path, *, label: str) -> Path:
    path = path.resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"{label} must remain inside the repository")
    return path


def _emit(**payload: object) -> None:
    payload = {
        "observed_at": datetime.now().astimezone().isoformat(),
        **payload,
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True), flush=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--authorization", type=Path, default=DEFAULT_AUTHORIZATION)
    parser.add_argument("--execution-root", type=Path, default=DEFAULT_EXECUTION_ROOT)
    parser.add_argument("--poll-interval-s", type=float, default=60.0)
    parser.add_argument("--provider-contract-confirmed-by-user", action="store_true")
    parser.add_argument("--credential-confirmed-by-user", action="store_true")
    parser.add_argument("--unlimited-spend-authorized", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if not (
        args.provider_contract_confirmed_by_user
        and args.credential_confirmed_by_user
        and args.unlimited_spend_authorized
    ):
        raise RuntimeError(
            "automatic W2-26 launch requires explicit provider, credential, and "
            "unlimited-spend confirmations"
        )
    if args.poll_interval_s < 10.0:
        raise ValueError("poll interval must be at least 10 seconds")
    protocol_path = _inside_root(args.protocol, label="protocol")
    manifest_path = _inside_root(args.manifest, label="manifest")
    authorization_path = _inside_root(args.authorization, label="authorization")
    execution_root = _inside_root(args.execution_root, label="execution root")
    protocol = _load(protocol_path)
    started = time.monotonic()
    attempt = 0
    while True:
        attempt += 1
        try:
            manifest = build_execution_manifest(ROOT, protocol)
        except (OSError, TypeError, ValueError) as error:
            _emit(
                event="work_ii_w226_auto_launch_waiting",
                stage="nine_task_manifest_resolution",
                liveness_counter=attempt,
                elapsed_s=round(time.monotonic() - started, 1),
                detail=str(error)[:1000],
            )
            time.sleep(args.poll_interval_s)
            continue
        if manifest.get("status") != "ready_authorization_blocked":
            _emit(
                event="work_ii_w226_auto_launch_waiting",
                stage="nine_task_manifest_resolution",
                liveness_counter=attempt,
                elapsed_s=round(time.monotonic() - started, 1),
                resolved_task_triplets=sum(
                    row.get("campaign_config_binding") is not None
                    for row in manifest.get("patterns", [])
                    if isinstance(row, dict)
                ),
                total_task_triplets=9,
                blockers=manifest.get("blocking_requirements", []),
            )
            time.sleep(args.poll_interval_s)
            continue
        manifest_errors = validate_manifest(ROOT, manifest)
        if manifest_errors:
            raise RuntimeError("resolved W2-26 manifest failed: " + "; ".join(manifest_errors))
        if manifest_path.exists():
            if _load(manifest_path) != manifest:
                raise RuntimeError("existing W2-26 execution manifest differs")
        else:
            write_json_atomic(manifest_path, manifest)
        approved_at = datetime.now().astimezone().isoformat()
        authorization = build_authorization(
            ROOT,
            manifest_path,
            currency_ceiling_usd=None,
            approved_at=approved_at,
            pricing_source=None,
            pricing_observed_at=None,
            cache_hit_input_usd_per_million=None,
            cache_miss_input_usd_per_million=None,
            output_usd_per_million=None,
            unlimited_spend_authorized=True,
        )
        authorization_errors = validate_authorization(
            ROOT, authorization, manifest_path
        )
        if authorization_errors:
            raise RuntimeError(
                "W2-26 unlimited authorization failed: "
                + "; ".join(authorization_errors)
            )
        if authorization_path.exists():
            if _load(authorization_path) != authorization:
                raise RuntimeError("existing W2-26 authorization differs")
        else:
            write_json_atomic(authorization_path, authorization)
        _emit(
            event="work_ii_w226_provider_launching",
            stage="provider_task_triplets",
            resolved_task_triplets=9,
            total_task_triplets=9,
            total_cells=27,
            total_complete_experiments=252,
            provider="wellau",
            model="gpt-5.6-sol",
            reasoning_effort="medium",
            unlimited_spend_authorized=True,
            attributable_pricing_available=False,
        )
        command = [
            sys.executable,
            str(RUNNER),
            "--execute",
            "--manifest",
            str(manifest_path),
            "--authorization",
            str(authorization_path),
            "--output",
            str(execution_root),
            "--allow-provider-execution",
        ]
        completed = subprocess.run(command, cwd=ROOT, check=False)
        _emit(
            event="work_ii_w226_provider_process_terminal",
            stage="provider_task_triplets",
            return_code=completed.returncode,
            execution_root=str(execution_root),
        )
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
