#!/usr/bin/env python3
"""Validate and integrate one completed Work II A-S development qualification.

The long-running qualification deliberately writes everything below ``runs/development``.
This tool is the explicit bridge to the small canonical inputs consumed by W2-26.  It does
not change evidence status, authorize provider execution, or turn a development run into a
formal result.
"""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import file_sha256, write_json_atomic
from chemworld.eval.work_ii_constitutive_structural_qualification import (
    CANDIDATE_IDS,
    materialize_d1_resource_design,
    summary_sha256,
    validate_summary,
)

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SUMMARY = Path(
    "workstreams/flagship_tasks/reports/"
    "work-ii-as-paired-law-q1-q2-five-world-20260812.json"
)
CANONICAL_PACKAGE = Path(
    "configs/benchmark/work_ii_as_paired_law_q2_package_v0.1.json"
)
CANONICAL_D1 = {
    "partition_power_response": Path(
        "configs/benchmark/work_ii_as_partition_d1_v0.1.json"
    ),
    "crystallization_reversible_topology": Path(
        "configs/benchmark/work_ii_as_crystallization_d1_v0.1.json"
    ),
}


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _inside(root: Path, path: Path, *, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{label} escapes its repository root") from error
    return resolved


def _bound_source_path(
    root: Path,
    binding: Mapping[str, Any],
    *,
    label: str,
) -> Path:
    relative = binding.get("path")
    digest = binding.get("sha256")
    if not isinstance(relative, str) or not isinstance(digest, str):
        raise ValueError(f"{label} lacks a path/file binding")
    path = _inside(root, root / relative, label=label)
    if not path.is_file() or file_sha256(path) != digest:
        raise ValueError(f"{label} file binding is stale")
    return path


def integrate_development_result(
    *,
    source_root: Path,
    source_summary: Path,
    destination_root: Path = ROOT,
    evidence_progress: Callable[[str, int, int], None] | None = None,
    reuse_source_deep_validation: bool = False,
) -> dict[str, Any]:
    """Deep-validate a complete run and publish only its canonical development inputs.

    Raw receipts and trajectories remain ignored under their original relative run path.
    All destinations are write-once.  A scientifically failed complete run is retained, but
    it cannot produce D1 configs and is reported as ineligible for W2-26.
    """

    source_root = source_root.resolve()
    destination_root = destination_root.resolve()
    source_summary = _inside(
        source_root, source_summary, label="A-S source summary"
    )
    if not source_summary.is_file():
        raise FileNotFoundError(f"A-S source summary is missing: {source_summary}")
    source_run = source_summary.parent
    source_run_relative = source_run.relative_to(source_root)
    if source_run_relative.parts[:2] != ("runs", "development"):
        raise ValueError("A-S integration accepts only runs/development source evidence")

    summary = _load_object(source_summary)
    source_errors = validate_summary(
        source_root,
        summary,
        evidence_progress=evidence_progress,
        # The accelerated closeout validates every receipt before it can publish
        # summary.json.  Its binding/roster/aggregate checks still run here, but
        # callers may reuse that completed deep pass instead of replaying all ten
        # worlds a second time during the mechanical repository integration.
        deep_validate_world_reports=not reuse_source_deep_validation,
    )
    if source_errors:
        raise ValueError(
            "A-S source qualification failed deep validation: "
            + "; ".join(source_errors)
        )

    generated_package = summary.get("generated_package")
    if not isinstance(generated_package, Mapping):
        raise ValueError("A-S source summary lacks its generated Q2 package")
    source_package = _bound_source_path(
        source_root, generated_package, label="A-S source Q2 package"
    )

    passed = summary.get("all_candidates_passed") is True
    generated_d1 = summary.get("participant_d1_configs_generated")
    generated_d1 = generated_d1 if isinstance(generated_d1, Mapping) else {}
    if passed and set(generated_d1) != set(CANDIDATE_IDS):
        raise ValueError("passing A-S source summary lacks both generated D1 configs")
    if not passed and generated_d1:
        raise ValueError("failed A-S source summary unexpectedly generated D1 configs")
    source_d1: dict[str, Path] = {}
    for candidate_id, binding in generated_d1.items():
        if candidate_id not in CANONICAL_D1 or not isinstance(binding, Mapping):
            raise ValueError("A-S source summary has an invalid D1 roster")
        source_d1[candidate_id] = _bound_source_path(
            source_root,
            binding,
            label=f"A-S source D1 config {candidate_id}",
        )

    destination_run = destination_root / source_run_relative
    canonical_summary = destination_root / CANONICAL_SUMMARY
    canonical_package = destination_root / CANONICAL_PACKAGE
    canonical_d1 = {
        candidate_id: destination_root / relative
        for candidate_id, relative in CANONICAL_D1.items()
    }
    protected = [canonical_summary, canonical_package, *canonical_d1.values()]
    if source_root != destination_root and destination_run.exists():
        raise FileExistsError(
            f"refusing to overwrite integrated A-S raw run: {destination_run}"
        )
    existing = [path for path in protected if path.exists()]
    if existing:
        raise FileExistsError(
            "refusing to overwrite canonical A-S artifacts: "
            + ", ".join(str(path) for path in existing)
        )

    # Materialize the complete destination view first, then publish and validate it
    # inside one rollback scope. Otherwise a destination-side contract error would
    # strand a partial raw run/package and make a corrected retry impossible.
    destination_root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".work-ii-as-integration-", dir=destination_root.parent
    ) as staging_directory:
        staging_root = Path(staging_directory).resolve()
        staged_run = staging_root / source_run_relative
        shutil.copytree(source_run, staged_run)
        staged_package = staging_root / CANONICAL_PACKAGE
        staged_package.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_package, staged_package)
        staged_d1: dict[str, Path] = {}
        for candidate_id, source_path in source_d1.items():
            target = staging_root / CANONICAL_D1[candidate_id]
            target.parent.mkdir(parents=True, exist_ok=True)
            config = _load_object(source_path)
            qualification = config.get("qualification")
            if not isinstance(qualification, dict) or qualification.get(
                "q0_q1_q2_passed"
            ) is not True:
                raise ValueError(
                    f"A-S source D1 {candidate_id} lacks its complete Q0-Q2 gate"
                )
            if qualification.get("q2_passed") not in {None, True}:
                raise ValueError(f"A-S source D1 {candidate_id} contradicts its Q2 pass")
            # The frozen qualification may predate the current downstream resource
            # semantics.  Re-materialize only the outcome-independent 12-round D1
            # envelope; Q1/Q2 evidence and the participant design are unchanged.
            config = materialize_d1_resource_design(config, candidate_id)
            write_json_atomic(target, config)
            staged_d1[candidate_id] = target

        integrated = json.loads(json.dumps(summary))
        integrated["generated_package"] = {
            "path": CANONICAL_PACKAGE.as_posix(),
            "sha256": file_sha256(staged_package),
            "package_sha256": generated_package["package_sha256"],
        }
        integrated["participant_d1_configs_generated"] = {
            candidate_id: {
                "path": CANONICAL_D1[candidate_id].as_posix(),
                "sha256": file_sha256(staged_d1[candidate_id]),
                "execution_authorized": False,
            }
            for candidate_id in source_d1
        }
        integrated["summary_sha256"] = summary_sha256(integrated)

        staged_summary = staging_root / CANONICAL_SUMMARY
        staged_summary.parent.mkdir(parents=True, exist_ok=True)
        write_json_atomic(staged_summary, integrated)

        published: list[Path] = []
        try:
            if source_root != destination_root:
                destination_run.parent.mkdir(parents=True, exist_ok=True)
                staged_run.replace(destination_run)
                published.append(destination_run)
            canonical_package.parent.mkdir(parents=True, exist_ok=True)
            staged_package.replace(canonical_package)
            published.append(canonical_package)
            for candidate_id, source_path in staged_d1.items():
                target = canonical_d1[candidate_id]
                target.parent.mkdir(parents=True, exist_ok=True)
                source_path.replace(target)
                published.append(target)
            canonical_summary.parent.mkdir(parents=True, exist_ok=True)
            staged_summary.replace(canonical_summary)
            published.append(canonical_summary)
            destination_errors = validate_summary(
                destination_root,
                integrated,
                evidence_progress=evidence_progress,
                # Receipt/trajectory replay was already rebuilt against the source
                # root. This pass verifies the rewritten canonical bindings against
                # the complete destination repository, including plan and Q0 inputs.
                deep_validate_world_reports=False,
            )
            if destination_errors:
                raise ValueError(
                    "integrated A-S qualification failed deep validation: "
                    + "; ".join(destination_errors)
                )
        except Exception:
            for path in reversed(published):
                if path.is_dir():
                    shutil.rmtree(path)
                elif path.exists():
                    path.unlink()
            raise

    return {
        "status": (
            "integrated_w2_26_input_ready"
            if passed
            else "integrated_scientific_rejection_w2_26_blocked"
        ),
        "all_candidates_passed": passed,
        "resource_calibration_candidate_ready": passed,
        "provider_execution_authorized": False,
        "formal_r5_authorized": False,
        "raw_run": source_run_relative.as_posix(),
        "canonical_summary": CANONICAL_SUMMARY.as_posix(),
        "canonical_package": CANONICAL_PACKAGE.as_posix(),
        "canonical_d1_configs": {
            candidate_id: CANONICAL_D1[candidate_id].as_posix()
            for candidate_id in source_d1
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-summary", type=Path, required=True)
    parser.add_argument(
        "--reuse-source-deep-validation",
        action="store_true",
        help=(
            "reuse the receipt-level deep validation completed by the source "
            "closeout while retaining all summary, binding, roster, and aggregate checks"
        ),
    )
    args = parser.parse_args()

    def progress(label: str, completed: int, total: int) -> None:
        print(
            json.dumps(
                {
                    "event": "work_ii_as_integration_validation_progress",
                    "candidate_world": label,
                    "completed_receipts": completed,
                    "total_receipts": total,
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )

    result = integrate_development_result(
        source_root=args.source_root,
        source_summary=args.source_summary,
        evidence_progress=progress,
        reuse_source_deep_validation=bool(args.reuse_source_deep_validation),
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
    return 0 if result["resource_calibration_candidate_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
