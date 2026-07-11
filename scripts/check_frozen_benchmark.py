"""Verify the public serious benchmark bundle instead of trusting status flags."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from chemworld.eval.baseline_report import SERIOUS_BASELINE_AGENTS  # type: ignore[import-untyped]
from chemworld.tasks import SERIOUS_TASK_IDS, get_task  # type: ignore[import-untyped]

RELEASE_SCHEMA_VERSION = "chemworld-benchmark-release-0.1"
RELEASE_ID = "chemworld-serious-v1"
DEFAULT_RELEASE_DIR = Path("benchmark/releases/chemworld-serious-v1")


@dataclass(frozen=True)
class IntegrityCheck:
    check_id: str
    passed: bool
    level: str
    observed: Any
    required: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read JSON object {path}: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_value(root: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip()


def _add(
    checks: list[IntegrityCheck],
    check_id: str,
    passed: bool,
    level: str,
    observed: Any,
    required: str,
) -> None:
    checks.append(IntegrityCheck(check_id, bool(passed), level, observed, required))


def verify_release_bundle(
    root: Path,
    release_dir: Path,
    *,
    allow_candidate: bool = False,
) -> dict[str, Any]:
    """Return structural and strict-freshness checks for one public bundle."""

    root = root.resolve()
    release_dir = release_dir.resolve()
    checks: list[IntegrityCheck] = []
    required_files = {
        "manifest": release_dir / "manifest.json",
        "baseline_summary": release_dir / "baseline_summary.json",
        "benchmark_validation": release_dir / "benchmark_validation.json",
        "response_surface_audit": release_dir / "response_surface_audit.json",
        "readme": release_dir / "README.md",
    }
    missing = sorted(name for name, path in required_files.items() if not path.is_file())
    _add(
        checks,
        "required_files",
        not missing,
        "structural",
        missing,
        "The public bundle must contain manifest, summary, validation, response audit, and README.",
    )
    if missing:
        return _finish(checks, allow_candidate=allow_candidate)

    try:
        manifest = _read_json(required_files["manifest"])
        baseline = _read_json(required_files["baseline_summary"])
        validation = _read_json(required_files["benchmark_validation"])
        response = _read_json(required_files["response_surface_audit"])
    except ValueError as error:
        _add(
            checks,
            "json_parse",
            False,
            "structural",
            str(error),
            "Every release JSON document must parse as an object.",
        )
        return _finish(checks, allow_candidate=allow_candidate)

    task_ids = list(SERIOUS_TASK_IDS)
    agent_ids = list(SERIOUS_BASELINE_AGENTS)
    _add(
        checks,
        "manifest_identity",
        manifest.get("schema_version") == RELEASE_SCHEMA_VERSION
        and manifest.get("release_id") == RELEASE_ID,
        "structural",
        {
            "schema_version": manifest.get("schema_version"),
            "release_id": manifest.get("release_id"),
        },
        f"Manifest identity must be {RELEASE_SCHEMA_VERSION}/{RELEASE_ID}.",
    )
    _add(
        checks,
        "task_set",
        manifest.get("task_ids") == task_ids,
        "structural",
        manifest.get("task_ids"),
        "Manifest task ids must exactly match the runtime serious suite.",
    )
    _add(
        checks,
        "agent_set",
        manifest.get("baseline_agents") == agent_ids,
        "structural",
        manifest.get("baseline_agents"),
        "Manifest agents must exactly match the official baseline matrix.",
    )
    expected_rows = len(task_ids) * len(agent_ids)
    rows = baseline.get("rows")
    row_list = rows if isinstance(rows, list) else []
    pairs = {
        (str(row.get("task_id")), str(row.get("agent_name")))
        for row in row_list
        if isinstance(row, dict)
    }
    expected_pairs = {(task, agent) for task in task_ids for agent in agent_ids}
    _add(
        checks,
        "baseline_matrix",
        len(row_list) == expected_rows and pairs == expected_pairs,
        "structural",
        {"row_count": len(row_list), "unique_pairs": len(pairs)},
        f"The public summary must contain all {expected_rows} task-agent rows exactly once.",
    )
    seeds = manifest.get("seeds")
    seed_list = seeds if isinstance(seeds, list) else []
    expected_results = expected_rows * len(seed_list)
    _add(
        checks,
        "result_count",
        len(seed_list) >= 1 and manifest.get("baseline_result_count") == expected_results,
        "structural",
        {
            "seeds": seed_list,
            "baseline_result_count": manifest.get("baseline_result_count"),
            "expected": expected_results,
        },
        "Result count must equal tasks x agents x frozen seeds.",
    )
    _add(
        checks,
        "validation_coverage",
        validation.get("validated") is True
        and validation.get("validated_task_count") == len(task_ids)
        and validation.get("task_ids") == task_ids,
        "structural",
        {
            "validated": validation.get("validated"),
            "validated_task_count": validation.get("validated_task_count"),
            "task_ids": validation.get("task_ids"),
        },
        "Validation must cover and accept the exact task set.",
    )
    response_tasks = response.get("tasks")
    response_ids = sorted(response_tasks) if isinstance(response_tasks, dict) else []
    _add(
        checks,
        "response_surface_coverage",
        response.get("passed") is True
        and response.get("task_ids") == task_ids
        and response_ids == sorted(task_ids),
        "structural",
        {"passed": response.get("passed"), "task_ids": response_ids},
        "Response-surface evidence must cover the exact task set.",
    )

    evidence = manifest.get("evidence")
    evidence_map = evidence if isinstance(evidence, dict) else {}
    embedded = {
        "baseline_summary_sha256": required_files["baseline_summary"],
        "benchmark_validation_sha256": required_files["benchmark_validation"],
        "response_surface_audit_sha256": required_files["response_surface_audit"],
    }
    digest_results = {
        key: {
            "declared": evidence_map.get(key),
            "actual": _sha256(path),
            "matches": evidence_map.get(key) == _sha256(path),
        }
        for key, path in embedded.items()
    }
    _add(
        checks,
        "embedded_evidence_digests",
        all(item["matches"] for item in digest_results.values()),
        "structural",
        digest_results,
        "Every embedded evidence file must match the SHA-256 declared by the manifest.",
    )

    release_hashes = manifest.get("task_contract_hashes")
    release_hash_map = release_hashes if isinstance(release_hashes, dict) else {}
    current_hashes = {task_id: get_task(task_id).contract_hash for task_id in task_ids}
    hash_drift = {
        task_id: {
            "release": release_hash_map.get(task_id),
            "current": current_hashes[task_id],
        }
        for task_id in task_ids
        if release_hash_map.get(task_id) != current_hashes[task_id]
    }
    _add(
        checks,
        "task_contract_freshness",
        not hash_drift,
        "freshness",
        hash_drift,
        "Released task hashes must equal the current source contracts.",
    )
    head = _git_value(root, "rev-parse", "HEAD")
    source_commit = manifest.get("source_commit") or manifest.get("commit_hash")
    resolved_source = (
        _git_value(root, "rev-parse", "--verify", f"{source_commit}^{{commit}}")
        if isinstance(source_commit, str) and source_commit
        else None
    )
    _add(
        checks,
        "source_commit_binding",
        bool(resolved_source) and resolved_source == source_commit,
        "freshness",
        {
            "evaluated_source_commit": source_commit,
            "resolved_source_commit": resolved_source,
            "current_release_commit": head,
        },
        (
            "The manifest must bind an existing evaluated source commit; current "
            "task hashes independently prevent post-evaluation semantic drift."
        ),
    )
    tracked_status = _git_value(root, "status", "--porcelain", "--untracked-files=no")
    tree_clean = tracked_status == ""
    _add(
        checks,
        "clean_source_tree",
        tree_clean and manifest.get("source_tree_dirty") is False,
        "freshness",
        {
            "current_tracked_dirty": not tree_clean,
            "manifest_source_tree_dirty": manifest.get("source_tree_dirty"),
        },
        "A frozen release must be built from and checked against a clean tracked source tree.",
    )
    _add(
        checks,
        "frozen_release_status",
        manifest.get("release_status") == "frozen",
        "freshness",
        manifest.get("release_status"),
        "The manifest must explicitly declare release_status=frozen.",
    )

    trajectory = manifest.get("trajectory_evidence")
    trajectory_map = trajectory if isinstance(trajectory, dict) else {}
    index_name = trajectory_map.get("index_path")
    archive_name = trajectory_map.get("archive_path")
    index_path = release_dir / str(index_name) if index_name else None
    archive_path = release_dir / str(archive_name) if archive_name else None
    trajectory_observed: dict[str, Any] = {
        "declared_count": trajectory_map.get("count"),
        "index_path": index_name,
        "archive_path": archive_name,
    }
    trajectory_passed = bool(
        trajectory_map.get("count") == expected_results
        and index_path is not None
        and index_path.is_file()
        and archive_path is not None
        and archive_path.is_file()
        and trajectory_map.get("index_sha256") == _sha256(index_path)
        and trajectory_map.get("archive_sha256") == _sha256(archive_path)
    )
    _add(
        checks,
        "trajectory_archive_binding",
        trajectory_passed,
        "freshness",
        trajectory_observed,
        "Every official result must be represented by a hashed trajectory index and archive.",
    )
    return _finish(checks, allow_candidate=allow_candidate)


def _finish(checks: list[IntegrityCheck], *, allow_candidate: bool) -> dict[str, Any]:
    structural_failures = [
        check.check_id for check in checks if check.level == "structural" and not check.passed
    ]
    freshness_failures = [
        check.check_id for check in checks if check.level == "freshness" and not check.passed
    ]
    structural_passed = not structural_failures
    strict_ready = structural_passed and not freshness_failures
    passed = structural_passed and (strict_ready or allow_candidate)
    return {
        "schema_version": "chemworld-release-integrity-report-0.1",
        "release_id": RELEASE_ID,
        "mode": "candidate" if allow_candidate else "strict_frozen",
        "passed": passed,
        "structural_integrity_passed": structural_passed,
        "strict_release_ready": strict_ready,
        "release_claim_allowed": strict_ready,
        "structural_failures": structural_failures,
        "candidate_waivers": freshness_failures if allow_candidate else [],
        "freshness_failures": freshness_failures,
        "checks": [check.to_dict() for check in checks],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--release-dir", type=Path, default=DEFAULT_RELEASE_DIR)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--allow-candidate",
        action="store_true",
        help="Allow structurally intact but explicitly non-claiming stale evidence.",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    release_dir = args.release_dir
    if not release_dir.is_absolute():
        release_dir = root / release_dir
    report = verify_release_bundle(
        root,
        release_dir,
        allow_candidate=args.allow_candidate,
    )
    if args.output is not None:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
