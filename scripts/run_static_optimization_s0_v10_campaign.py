"""Plan or execute the frozen two-flagship S0 v1.0 campaign."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256 as canonical_sha256,
)
from chemworld.eval.provenance import (
    write_json_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = (
    ROOT
    / "configs"
    / "benchmark"
    / "scientific_optimization_s0_v1.0_freeze_manifest.json"
)


@dataclass(frozen=True)
class CampaignCell:
    kind: str
    track_id: str
    world_seed: int
    protocol_path: Path
    method_path: Path | None
    method_id: str | None
    output: Path


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _repo_path(value: object) -> Path:
    path = (ROOT / str(value)).resolve()
    path.relative_to(ROOT)
    return path


def _git_output(*arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("status") != "owner_authorized_frozen_formal_pending_execution":
        raise ValueError("campaign manifest is not an owner-authorized frozen candidate")
    if manifest.get("world_seeds") != list(range(10)):
        raise ValueError("campaign world seeds must be exactly 0 through 9")
    for collection in ("participant_tracks", "baseline_tracks"):
        tracks = manifest.get(collection)
        if not isinstance(tracks, list) or len(tracks) != 2:
            raise ValueError(f"{collection} must contain exactly two flagship tracks")
        for track in tracks:
            protocol_path = _repo_path(track["protocol_path"])
            protocol = _load_json(protocol_path)
            if canonical_sha256(protocol) != track["protocol_sha256"]:
                raise ValueError(f"frozen protocol hash mismatch: {protocol_path}")
            if protocol["world_policy"]["formal_world_seeds"] != list(range(10)):
                raise ValueError(f"protocol world suite changed: {protocol_path}")
            if int(protocol["horizon"]) != 20:
                raise ValueError(f"protocol horizon changed: {protocol_path}")
            if collection == "participant_tracks":
                method_path = _repo_path(track["method_path"])
                methods = _load_json(method_path)
                if canonical_sha256(methods) != track["method_sha256"]:
                    raise ValueError(f"frozen method hash mismatch: {method_path}")
                reference_path = _repo_path(track["world_understanding_reference_path"])
                reference = _load_json(reference_path)
                if (
                    canonical_sha256(reference)
                    != track["world_understanding_reference_sha256"]
                ):
                    raise ValueError(
                        f"frozen world-understanding hash mismatch: {reference_path}"
                    )
                if protocol["method_config_path"] != track["method_path"]:
                    raise ValueError(f"protocol method binding changed: {protocol_path}")
                if protocol["method_ids"] != [track["method_id"]]:
                    raise ValueError(f"protocol method ID changed: {protocol_path}")


def _seeded_protocol(path: Path, world_seed: int) -> dict[str, Any]:
    protocol = _load_json(path)
    protocol["world_policy"] = dict(protocol["world_policy"])
    protocol["world_policy"]["world_seed"] = int(world_seed)
    return protocol


def _participant_complete(cell: CampaignCell) -> bool:
    report_path = cell.output / "report.json"
    if not report_path.is_file() or cell.method_path is None:
        return False
    report = _load_json(report_path)
    protocol_hash = canonical_sha256(
        _seeded_protocol(cell.protocol_path, cell.world_seed)
    )
    method_hash = canonical_sha256(_load_json(cell.method_path))
    return bool(
        report.get("protocol_sha256") == protocol_hash
        and report.get("method_config_sha256") == method_hash
        and report.get("completed_cell_count") == report.get("cell_count") == 1
        and report.get("method_failure_cell_count") == 0
        and report.get("completed_experiment_count")
        == report.get("planned_experiment_count")
        == 20
        and all(
            item.get("cell_status") == "completed"
            and int(item["cell"]["world_seed"]) == cell.world_seed
            for item in report.get("cells", [])
        )
    )


def _run_process(
    command: list[str],
    *,
    output: Path,
    log_name: str,
) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    log = {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    write_json_atomic(output / log_name, log)
    if result.returncode != 0:
        raise RuntimeError(
            f"campaign subprocess failed ({result.returncode}): {' '.join(command)}"
        )
    return log


def _audit_command(cell: CampaignCell) -> list[str]:
    return [
        sys.executable,
        "scripts/audit_static_optimization_s0.py",
        "--protocol",
        str(cell.protocol_path),
        "--run-root",
        str(cell.output),
        "--output",
        str(cell.output / "postrun_audit.json"),
        "--world-seed",
        str(cell.world_seed),
    ]


def _run_participant(cell: CampaignCell, provider: str) -> dict[str, Any]:
    if cell.method_path is None or cell.method_id is None:
        raise ValueError("participant cell lacks a method binding")
    reused = _participant_complete(cell)
    if not reused:
        if (cell.output / "receipts").exists() or (cell.output / "report.json").exists():
            raise RuntimeError(
                "incomplete participant output exists; use the explicit continuation "
                f"workflow before retrying: {cell.output}"
            )
        protocol_hash = canonical_sha256(
            _seeded_protocol(cell.protocol_path, cell.world_seed)
        )
        method_hash = canonical_sha256(_load_json(cell.method_path))
        command = [
            sys.executable,
            "scripts/run_static_optimization_s0.py",
            "--protocol",
            str(cell.protocol_path),
            "--llm-methods",
            str(cell.method_path),
            "--output",
            str(cell.output),
            "--provider",
            provider,
            "--world-seed",
            str(cell.world_seed),
            "--method-id",
            cell.method_id,
        ]
        if provider == "codex_subscription":
            command.extend(
                [
                    "--allow-external-provider",
                    "--confirm-protocol-sha256",
                    protocol_hash,
                    "--confirm-method-sha256",
                    method_hash,
                ]
            )
        _run_process(
            command,
            output=cell.output,
            log_name="execution_run_log.json",
        )
    _run_process(
        _audit_command(cell),
        output=cell.output,
        log_name="execution_audit_log.json",
    )
    audit = _load_json(cell.output / "postrun_audit.json")
    if audit.get("replay", {}).get("all_verified") is not True:
        raise RuntimeError(f"participant exact replay failed: {cell.output}")
    return {
        "kind": cell.kind,
        "track_id": cell.track_id,
        "world_seed": cell.world_seed,
        "output": str(cell.output),
        "reused": reused,
        "exact_replay": True,
    }


def _run_baselines(cell: CampaignCell) -> dict[str, Any]:
    command = [
        sys.executable,
        "scripts/run_static_optimization_s0_baselines.py",
        "--protocol",
        str(cell.protocol_path),
        "--output",
        str(cell.output),
        "--world-seed",
        str(cell.world_seed),
        "--resume-missing",
    ]
    _run_process(
        command,
        output=cell.output,
        log_name="execution_run_log.json",
    )
    _run_process(
        _audit_command(cell),
        output=cell.output,
        log_name="execution_audit_log.json",
    )
    report = _load_json(cell.output / "report.json")
    audit = _load_json(cell.output / "postrun_audit.json")
    if report.get("completed_cell_count") != report.get("cell_count"):
        raise RuntimeError(f"baseline cells are incomplete: {cell.output}")
    if audit.get("replay", {}).get("all_verified") is not True:
        raise RuntimeError(f"baseline exact replay failed: {cell.output}")
    return {
        "kind": cell.kind,
        "track_id": cell.track_id,
        "world_seed": cell.world_seed,
        "output": str(cell.output),
        "reused": False,
        "cell_count": int(report["cell_count"]),
        "exact_replay": True,
    }


def _campaign_cells(
    manifest: dict[str, Any],
    *,
    output_root: Path,
    selection: str,
    track_ids: set[str],
    world_seeds: set[int],
) -> list[CampaignCell]:
    cells: list[CampaignCell] = []
    if selection in {"participants", "all"}:
        for track in manifest["participant_tracks"]:
            if track_ids and track["track_id"] not in track_ids:
                continue
            for seed in manifest["world_seeds"]:
                if world_seeds and seed not in world_seeds:
                    continue
                cells.append(
                    CampaignCell(
                        kind="participant",
                        track_id=str(track["track_id"]),
                        world_seed=int(seed),
                        protocol_path=_repo_path(track["protocol_path"]),
                        method_path=_repo_path(track["method_path"]),
                        method_id=str(track["method_id"]),
                        output=(
                            output_root
                            / "participants"
                            / str(track["track_id"])
                            / f"world-{seed:02d}"
                        ),
                    )
                )
    if selection in {"baselines", "all"}:
        for track in manifest["baseline_tracks"]:
            if track_ids and track["track_id"] not in track_ids:
                continue
            for seed in manifest["world_seeds"]:
                if world_seeds and seed not in world_seeds:
                    continue
                cells.append(
                    CampaignCell(
                        kind="baseline",
                        track_id=str(track["track_id"]),
                        world_seed=int(seed),
                        protocol_path=_repo_path(track["protocol_path"]),
                        method_path=None,
                        method_id=None,
                        output=(
                            output_root
                            / "baselines"
                            / str(track["track_id"])
                            / f"world-{seed:02d}"
                        ),
                    )
                )
    return cells


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--selection",
        choices=("participants", "baselines", "all"),
        default="all",
    )
    parser.add_argument("--track-id", action="append")
    parser.add_argument("--world-seed", type=int, action="append")
    parser.add_argument(
        "--participant-provider",
        choices=("mock", "codex_subscription"),
        default="codex_subscription",
    )
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-freeze-sha256")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest = _load_json(manifest_path)
    _validate_manifest(manifest)
    freeze_hash = canonical_sha256(manifest)
    world_seeds = set(args.world_seed or [])
    if world_seeds - set(manifest["world_seeds"]):
        raise ValueError("requested world seed is outside the frozen suite")
    cells = _campaign_cells(
        manifest,
        output_root=args.output_root.resolve(),
        selection=args.selection,
        track_ids=set(args.track_id or []),
        world_seeds=world_seeds,
    )
    plan = {
        "freeze_id": manifest["freeze_id"],
        "freeze_sha256": freeze_hash,
        "selection": args.selection,
        "participant_provider": args.participant_provider,
        "cell_count": len(cells),
        "cells": [
            {
                "kind": cell.kind,
                "track_id": cell.track_id,
                "world_seed": cell.world_seed,
                "output": str(cell.output),
            }
            for cell in cells
        ],
    }
    if not args.execute:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return
    if args.confirm_freeze_sha256 != freeze_hash:
        raise RuntimeError(
            "execution requires the exact canonical freeze-manifest SHA-256"
        )
    if args.max_workers <= 0:
        raise ValueError("--max-workers must be positive")
    dirty = _git_output("status", "--porcelain")
    if dirty:
        raise RuntimeError("formal campaign execution requires a clean source tree")
    source_commit = _git_output("rev-parse", "HEAD")

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(
                _run_participant,
                cell,
                args.participant_provider,
            )
            if cell.kind == "participant"
            else executor.submit(_run_baselines, cell): cell
            for cell in cells
        }
        for future in as_completed(futures):
            cell = futures[future]
            result = future.result()
            results.append(result)
            print(
                json.dumps(
                    {
                        "completed": (
                            f"{cell.kind}:{cell.track_id}:world-{cell.world_seed:02d}"
                        ),
                        "exact_replay": result["exact_replay"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    results.sort(key=lambda item: (item["kind"], item["track_id"], item["world_seed"]))
    execution_index = {
        "schema_version": "chemworld-static-s0-v10-campaign-execution-index-1.0",
        "freeze_id": manifest["freeze_id"],
        "freeze_sha256": freeze_hash,
        "source_commit": source_commit,
        "source_tree_clean_at_launch": True,
        "participant_provider": args.participant_provider,
        "all_requested_cells_completed": len(results) == len(cells),
        "all_exact_replay_verified": all(item["exact_replay"] for item in results),
        "results": results,
    }
    write_json_atomic(args.output_root / "campaign_execution_index.json", execution_index)
    print(
        json.dumps(
            {
                "output": str(
                    args.output_root / "campaign_execution_index.json"
                ),
                "completed_cells": len(results),
                "all_exact_replay_verified": execution_index[
                    "all_exact_replay_verified"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
