"""Build the immutable public evidence bundle for chemworld-serious-v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from typing import Any

from chemworld import __version__  # type: ignore[import-untyped]
from chemworld.eval.baseline_report import SERIOUS_BASELINE_AGENTS  # type: ignore[import-untyped]
from chemworld.eval.benchmark_validation import (  # type: ignore[import-untyped]
    PRIMARY_METRIC_FIELDS,
    validate_serious_baseline_report,
)
from chemworld.eval.seed_suite import SERIOUS_SEED_SUITE_ID  # type: ignore[import-untyped]
from chemworld.tasks import (  # type: ignore[import-untyped]
    SERIOUS_TASK_IDS,
    TASK_CONTRACT_VERSION,
    get_task,
)
from chemworld.world.parameters import WORLD_FAMILY_VERSION  # type: ignore[import-untyped]

RELEASE_ID = "chemworld-serious-v1"
RELEASE_SCHEMA_VERSION = "chemworld-benchmark-release-0.1"


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _read_json_list(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise ValueError(f"{path} must contain a JSON object list")
    return payload


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_metadata(root: Path) -> tuple[str, bool]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return head, bool(status)


def _write_trajectory_archive(
    *,
    run_dir: Path,
    output_dir: Path,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    results_path = run_dir / "baseline_report" / "baseline_results.json"
    rows = _read_json_list(results_path)
    entries: list[dict[str, Any]] = []
    archive_path = output_dir / "trajectories.zip"
    with zipfile.ZipFile(
        archive_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for row in sorted(
            rows,
            key=lambda item: (
                str(item["task_id"]),
                str(item["agent_name"]),
                int(item["seed"]),
            ),
        ):
            source = Path(str(row["trajectory_path"]))
            if not source.is_file():
                raise ValueError(f"trajectory is unavailable: {source}")
            actual_digest = _sha256(source)
            declared_digest = str(row["trajectory_sha256"])
            if actual_digest != declared_digest:
                raise ValueError(f"trajectory digest mismatch: {source}")
            relative_name = (
                f"trajectories/{row['task_id']}/{row['agent_name']}/seed-{int(row['seed'])}.jsonl"
            )
            info = zipfile.ZipInfo(relative_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
            entries.append(
                {
                    "task_id": row["task_id"],
                    "agent_name": row["agent_name"],
                    "seed": int(row["seed"]),
                    "archive_member": relative_name,
                    "trajectory_sha256": actual_digest,
                    "verified": bool(row.get("verified")),
                }
            )
    if not all(entry["verified"] for entry in entries):
        raise ValueError("all archived trajectories must have verified results")
    index_path = output_dir / "trajectory_index.json"
    _write_json(
        index_path,
        {
            "schema_version": "chemworld-trajectory-index-0.1",
            "count": len(entries),
            "entries": entries,
        },
    )
    return {
        "count": len(entries),
        "index_path": index_path.name,
        "index_sha256": _sha256(index_path),
        "archive_path": archive_path.name,
        "archive_sha256": _sha256(archive_path),
    }


def _public_summary(report: dict[str, Any]) -> dict[str, Any]:
    rows = report.get("summary_rows")
    if not isinstance(rows, list):
        raise ValueError("baseline report must contain summary_rows")
    public_rows: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("baseline summary rows must be objects")
        task_id = str(row["task_id"])
        primary_field = PRIMARY_METRIC_FIELDS[task_id]
        stderr_field = primary_field.replace("mean_", "stderr_", 1)
        public_rows.append(
            {
                "task_id": task_id,
                "agent_name": row["agent_name"],
                "runs": row["runs"],
                "seeds": row["seeds"],
                "mean_total_score": row["mean_total_score"],
                "stderr_total_score": row["stderr_total_score"],
                "ci95_total_score": [
                    row["ci95_lower_total_score"],
                    row["ci95_upper_total_score"],
                ],
                "success_rate": row["success_rate"],
                "mean_final_assay_count": row["mean_final_assay_count"],
                "mean_invalid_action_rate": row["mean_invalid_action_rate"],
                "mean_bo_initial_recipe_count": row["mean_bo_initial_recipe_count"],
                "mean_bo_acquisition_recipe_count": row["mean_bo_acquisition_recipe_count"],
                "primary_metric_field": primary_field,
                "mean_primary_metric": row[primary_field],
                "stderr_primary_metric": row[stderr_field],
                "ci95_primary_metric": [
                    row[primary_field.replace("mean_", "ci95_lower_", 1)],
                    row[primary_field.replace("mean_", "ci95_upper_", 1)],
                ],
            }
        )
    return {
        "schema_version": "chemworld-public-baseline-summary-0.1",
        "suite_id": RELEASE_ID,
        "reporting_policy": "per-task; no cross-task aggregate score",
        "rows": public_rows,
    }


def _release_readme() -> str:
    return """# ChemWorld Serious Benchmark v1

This directory is the public evidence bundle for `chemworld-serious-v1`.

- `manifest.json` freezes versions, task hashes, seeds, agents, and evidence digests.
- `baseline_summary.json` reports all official baselines per task.
- `benchmark_validation.json` contains the machine-readable empirical gate.
- `response_surface_audit.json` records deterministic response-surface probes.

Validate an installed source tree with:

```bash
python scripts/check_frozen_benchmark.py
```

Scores compare experimental strategies inside ChemWorld. They are not predictions of
real chemical yields, material properties, or plant safety.

The strict command verifies task hashes, source commit, embedded evidence digests, and
the complete trajectory archive. `--allow-candidate` is only a development migration
mode and never authorizes a release claim.
"""


def build_release(*, run_dir: Path, output_dir: Path, official_path: Path) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parents[1]
    source_commit, source_tree_dirty = _git_metadata(project_root)
    if source_tree_dirty:
        raise ValueError("refusing to build a frozen release from a dirty tracked source tree")
    baseline_path = run_dir / "baseline_report" / "baseline_report.json"
    response_path = run_dir / "response_surface_audit.json"
    artifact_path = run_dir / "artifact" / "artifact_summary.json"
    report = _read_json(baseline_path)
    if report.get("commit_hash") != source_commit:
        raise ValueError("baseline report commit does not match the checked-out source commit")
    validation = validate_serious_baseline_report(report)
    response = _read_json(response_path)
    artifact = _read_json(artifact_path)

    if validation.get("validated") is not True:
        raise ValueError("baseline report does not pass the empirical benchmark gate")
    if response.get("passed") is not True:
        raise ValueError("response-surface audit did not pass")
    if response.get("task_ids") != list(SERIOUS_TASK_IDS):
        raise ValueError("response-surface audit has unexpected task coverage")
    if artifact.get("replay_verified") is not True:
        raise ValueError("paper artifact replay is not verified")

    output_dir.mkdir(parents=True, exist_ok=True)
    baseline_summary_path = output_dir / "baseline_summary.json"
    validation_path = output_dir / "benchmark_validation.json"
    release_response_path = output_dir / "response_surface_audit.json"
    _write_json(baseline_summary_path, _public_summary(report))
    _write_json(validation_path, validation)
    _write_json(release_response_path, response)
    _write_json(official_path, validation)
    (output_dir / "README.md").write_text(_release_readme(), encoding="utf-8")
    trajectory_evidence = _write_trajectory_archive(
        run_dir=run_dir,
        output_dir=output_dir,
    )

    manifest = {
        "schema_version": RELEASE_SCHEMA_VERSION,
        "release_id": RELEASE_ID,
        "release_status": "frozen",
        "source_commit": source_commit,
        "source_tree_dirty": False,
        "package_version": __version__,
        "world_law_version": WORLD_FAMILY_VERSION,
        "task_contract_version": TASK_CONTRACT_VERSION,
        "seed_suite_id": SERIOUS_SEED_SUITE_ID,
        "task_ids": list(SERIOUS_TASK_IDS),
        "task_contract_hashes": {
            task_id: get_task(task_id).contract_hash for task_id in SERIOUS_TASK_IDS
        },
        "seeds": list(get_task(SERIOUS_TASK_IDS[0]).seeds),
        "baseline_agents": list(SERIOUS_BASELINE_AGENTS),
        "baseline_result_count": report.get("result_count"),
        "artifact_replay_verified": True,
        "trajectory_evidence": trajectory_evidence,
        "reporting_policy": "per-task; no cross-task aggregate score",
        "evidence": {
            "baseline_report_sha256": _sha256(baseline_path),
            "baseline_report_canonical_sha256": validation["baseline_report_sha256"],
            "baseline_summary_sha256": _sha256(baseline_summary_path),
            "benchmark_validation_sha256": _sha256(validation_path),
            "response_surface_audit_sha256": _sha256(release_response_path),
            "paper_artifact_summary_sha256": _sha256(artifact_path),
            "trajectory_index_sha256": trajectory_evidence["index_sha256"],
            "trajectory_archive_sha256": trajectory_evidence["archive_sha256"],
        },
        "verification_commands": [
            "python scripts/check_frozen_benchmark.py",
            "python scripts/audit_serious_response_surfaces.py",
            "python scripts/run_serious_task_suite.py --output-dir runs/serious_release",
            "python scripts/run_release_gate.py",
        ],
    }
    manifest_path = output_dir / "manifest.json"
    _write_json(manifest_path, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", default="runs/benchmark_freeze/release_v1")
    parser.add_argument("--output-dir", default=f"benchmark/releases/{RELEASE_ID}")
    parser.add_argument(
        "--official-validation", default="configs/benchmark/serious_validation.json"
    )
    args = parser.parse_args()
    manifest = build_release(
        run_dir=Path(args.run_dir),
        output_dir=Path(args.output_dir),
        official_path=Path(args.official_validation),
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
