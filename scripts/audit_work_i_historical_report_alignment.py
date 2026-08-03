"""Audit two historical generated reports against the current evidence binding."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT_PATH = Path("configs/current.json")
RUNTIME_REPORT_PATH = Path(
    "workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json"
)
PUBLIC_BOUNDARY_REPORT_PATH = Path(
    "workstreams/world_foundation/reports/public-boundary-security-vnext.json"
)
REPORT_JSON_PATH = Path("workstreams/arxiv_v1/reports/work-i-historical-report-alignment-v0.1.json")
REPORT_MD_PATH = Path("workstreams/arxiv_v1/reports/work-i-historical-report-alignment-v0.1.md")


class HistoricalReportAlignmentError(RuntimeError):
    """Raised when a historical report or its current binding fails closed."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HistoricalReportAlignmentError(f"cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise HistoricalReportAlignmentError(f"JSON root must be an object: {path}")
    return payload


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise HistoricalReportAlignmentError(f"{key} must be an object")
    return value


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise HistoricalReportAlignmentError(f"cannot read bound file: {path}") from exc
    return digest.hexdigest()


def _canonical_sha256(payload: Any, hash_field: str | None = None) -> str:
    unhashed = deepcopy(payload)
    if hash_field is not None:
        if not isinstance(unhashed, dict):
            raise HistoricalReportAlignmentError("self-hashed payload must be an object")
        unhashed.pop(hash_field, None)
    return hashlib.sha256(
        json.dumps(
            unhashed,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def receipt_sha256(payload: Mapping[str, Any]) -> str:
    """Return the canonical receipt digest excluding its embedded self-hash."""

    return _canonical_sha256(payload, "receipt_sha256")


def _run_git(root: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise HistoricalReportAlignmentError(f"git inspection failed: {' '.join(args)}") from exc
    return completed.stdout.strip()


def _git_tracking_binding(root: Path, path: Path) -> dict[str, Any]:
    repository_path = path.as_posix()
    output = _run_git(root, "ls-files", "--stage", "--", repository_path)
    rows = [row for row in output.splitlines() if row]
    if len(rows) != 1 or "\t" not in rows[0]:
        raise HistoricalReportAlignmentError(f"report is not uniquely tracked: {repository_path}")
    metadata, tracked_path = rows[0].split("\t", 1)
    fields = metadata.split()
    if len(fields) != 3 or fields[2] != "0" or tracked_path != repository_path:
        raise HistoricalReportAlignmentError(f"invalid Git index entry: {repository_path}")
    mode, index_blob_oid, _stage = fields
    working_tree_blob_oid = _run_git(root, "hash-object", "--", repository_path)
    if working_tree_blob_oid != index_blob_oid:
        raise HistoricalReportAlignmentError(
            f"uncommitted generated-artifact drift: {repository_path}"
        )
    return {
        "git_file_mode": mode,
        "git_index_blob_oid": index_blob_oid,
        "tracked": True,
        "working_tree_blob_oid": working_tree_blob_oid,
        "working_tree_matches_index": True,
    }


def _validate_runtime_report(payload: Mapping[str, Any]) -> dict[str, Any]:
    summary = _mapping(payload, "summary")
    checks = _mapping(payload, "checks")
    findings = payload.get("findings")
    if (
        payload.get("schema_version") != "chemworld-runtime-domain-affordance-audit-0.4"
        or payload.get("status") != "passed"
        or payload.get("passed") is not True
        or payload.get("guarded_sources_match_source_commit") is not True
        or not isinstance(findings, list)
        or findings
        or not checks
        or any(value is not True for value in checks.values())
        or summary.get("candidate_count") != 237
        or summary.get("validator_valid_count") != 235
        or summary.get("runtime_committed_count") != 235
        or summary.get("finding_count") != 0
        or summary.get("task_count") != 6
    ):
        raise HistoricalReportAlignmentError("runtime-domain acceptance evidence changed")
    source_commit = payload.get("source_commit")
    if not isinstance(source_commit, str) or len(source_commit) != 40:
        raise HistoricalReportAlignmentError("runtime-domain source provenance is invalid")
    return {
        "all_checks_passed": True,
        "candidate_count": 237,
        "finding_count": 0,
        "guarded_sources_match_source_commit": True,
        "historical_source_commit": source_commit,
        "runtime_committed_count": 235,
        "task_count": 6,
        "validator_valid_count": 235,
    }


def _probe_leaf_counts(probe_groups: Mapping[str, Any]) -> tuple[int, int]:
    total = 0
    passed = 0
    for group_name, group_value in probe_groups.items():
        if not isinstance(group_value, Mapping) or not group_value:
            raise HistoricalReportAlignmentError(f"invalid probe group: {group_name}")
        for probe_name, probe_value in group_value.items():
            if not isinstance(probe_value, bool):
                raise HistoricalReportAlignmentError(
                    f"probe is not Boolean: {group_name}.{probe_name}"
                )
            total += 1
            passed += int(probe_value)
    return total, passed


def _validate_public_boundary_report(root: Path, payload: Mapping[str, Any]) -> dict[str, Any]:
    checks = _mapping(payload, "checks")
    dependencies = _mapping(payload, "dependency_bindings")
    details = _mapping(payload, "details")
    invariance = _mapping(details, "invariance")
    probe_groups = _mapping(payload, "probe_groups")
    probe_count, passed_probe_count = _probe_leaf_counts(probe_groups)
    if (
        payload.get("schema_version") != "chemworld-foundation-public-boundary-security-audit-0.1"
        or payload.get("status") != "controls_ready"
        or payload.get("controls_ready") is not True
        or payload.get("backend_freeze_allowed") is not True
        or payload.get("probe_count") != 35
        or probe_count != 35
        or passed_probe_count != 35
        or not checks
        or any(value is not True for value in checks.values())
        or invariance.get("controls_ready") is not True
        or invariance.get("paired_run_count") != 12
        or invariance.get("task_count") != 6
        or len(dependencies) != 4
    ):
        raise HistoricalReportAlignmentError("public-boundary acceptance evidence changed")

    dependency_rows: list[dict[str, Any]] = []
    for name in sorted(dependencies):
        binding = dependencies[name]
        if not isinstance(binding, Mapping):
            raise HistoricalReportAlignmentError(f"invalid dependency binding: {name}")
        path_value = binding.get("path")
        sha_value = binding.get("actual_sha256")
        if (
            not isinstance(path_value, str)
            or not isinstance(sha_value, str)
            or binding.get("passed") is not True
            or _file_sha256(root / path_value) != sha_value
        ):
            raise HistoricalReportAlignmentError(f"dependency binding changed: {name}")
        dependency_rows.append({"name": name, "path": path_value, "sha256": sha_value})
    return {
        "all_checks_passed": True,
        "dependency_binding_count": 4,
        "dependency_bindings": dependency_rows,
        "failed_probe_count": 0,
        "passed_probe_count": 35,
        "probe_count": 35,
        "semantic_invariance_controls_ready": True,
        "semantic_invariance_paired_run_count": 12,
        "task_count": 6,
    }


def _current_node(
    current: Mapping[str, Any], node_name: str, expected_path: Path, report_sha256: str
) -> dict[str, Any]:
    evidence_dag = _mapping(current, "evidence_dag")
    nodes = _mapping(evidence_dag, "nodes")
    node = _mapping(nodes, node_name)
    if (
        node.get("path") != expected_path.as_posix()
        or node.get("sha256") != report_sha256
        or node.get("role") != "generated_current"
        or node.get("lifecycle") != "generated"
        or node.get("artifact_state") != "current"
        or node.get("freshness") != "fresh"
        or node.get("gate_state") != "passed"
    ):
        raise HistoricalReportAlignmentError(f"current evidence binding changed: {node_name}")
    return {
        "artifact_state": "current",
        "freshness": "fresh",
        "gate_state": "passed",
        "lifecycle": "generated",
        "node": node_name,
        "path": expected_path.as_posix(),
        "producer": node.get("producer"),
        "role": "generated_current",
        "sha256": report_sha256,
    }


def build_alignment_receipt(root: Path = ROOT) -> dict[str, Any]:
    """Build a fail-closed receipt without rewriting either historical report."""

    resolved = root.resolve()
    runtime_payload = _read_json(resolved / RUNTIME_REPORT_PATH)
    public_payload = _read_json(resolved / PUBLIC_BOUNDARY_REPORT_PATH)
    current = _read_json(resolved / CURRENT_PATH)
    runtime_sha = _file_sha256(resolved / RUNTIME_REPORT_PATH)
    public_sha = _file_sha256(resolved / PUBLIC_BOUNDARY_REPORT_PATH)

    runtime_tracking = _git_tracking_binding(resolved, RUNTIME_REPORT_PATH)
    public_tracking = _git_tracking_binding(resolved, PUBLIC_BOUNDARY_REPORT_PATH)
    runtime_acceptance = _validate_runtime_report(runtime_payload)
    public_acceptance = _validate_public_boundary_report(resolved, public_payload)
    current_nodes = [
        _current_node(current, "runtime_affordance", RUNTIME_REPORT_PATH, runtime_sha),
        _current_node(current, "public_boundary", PUBLIC_BOUNDARY_REPORT_PATH, public_sha),
    ]

    receipt: dict[str, Any] = {
        "schema_id": "chemworld.work_i_historical_report_alignment_receipt",
        "schema_version": "0.1.0",
        "receipt_id": "work-i-w1-m03-historical-report-alignment-v0.1",
        "owner_task": "W1-M03",
        "status": "target_reports_aligned_global_refresh_queued",
        "source_reports": [
            {
                "bytes": (resolved / RUNTIME_REPORT_PATH).stat().st_size,
                "id": "runtime_affordance",
                "path": RUNTIME_REPORT_PATH.as_posix(),
                "sha256": runtime_sha,
                **runtime_tracking,
            },
            {
                "bytes": (resolved / PUBLIC_BOUNDARY_REPORT_PATH).stat().st_size,
                "id": "public_boundary",
                "path": PUBLIC_BOUNDARY_REPORT_PATH.as_posix(),
                "sha256": public_sha,
                **public_tracking,
            },
        ],
        "current_evidence_bindings": current_nodes,
        "acceptance_evidence": {
            "runtime_domain_affordance": runtime_acceptance,
            "public_boundary_security": public_acceptance,
        },
        "alignment_decision": {
            "registry_declared_node_hashes_match_report_bytes": True,
            "registry_declared_node_paths_match_report_paths": True,
            "registry_declared_target_nodes_current_fresh_and_passed": True,
            "historical_source_commit_is_provenance_not_current_selector": True,
            "report_worktree_bytes_match_git_index": True,
            "reports_are_tracked": True,
            "unexplained_target_report_drift": False,
        },
        "repository_integration_state": {
            "baseline_commit": "143c83a7",
            "baseline_evidence_pipeline_check_passed": False,
            "baseline_issue_existed_before_w1_m03_implementation": True,
            "baseline_errors": [
                "current registry executable source fingerprint is stale",
                "registry freshness state mismatch: runtime_affordance",
                "registry gate state mismatch: runtime_affordance",
                "repository stale binding count is inconsistent",
                "repository stale binding identities are inconsistent",
            ],
            "classification": "explained_repository_integration_drift",
            "global_refresh_owned_by": "coordinator integration (W1-M05/W1-M06)",
            "target_report_path_or_content_mismatch": False,
            "w1_m03_global_refresh_allowed": False,
        },
        "preservation_boundary": {
            "configs_current_rewritten_by_task": False,
            "evidence_dag_regenerated_by_task": False,
            "historical_report_bytes_rewritten_by_task": False,
            "historical_reports_selected_by_content_sha256": True,
            "silent_overwrite_allowed": False,
        },
        "claim_boundary": {
            "benchmark_performance_claim_allowed": False,
            "chemistry_safety_certification": False,
            "control_and_conformance_evidence_only": True,
        },
    }
    receipt["receipt_sha256"] = receipt_sha256(receipt)
    return receipt


def build_markdown_report(receipt: Mapping[str, Any]) -> str:
    """Render a concise human-readable alignment handoff."""

    acceptance = _mapping(receipt, "acceptance_evidence")
    runtime = _mapping(acceptance, "runtime_domain_affordance")
    public = _mapping(acceptance, "public_boundary_security")
    return "\n".join(
        [
            "# Work I historical report alignment",
            "",
            f"Status: **{receipt['status']}**",
            f"Receipt SHA-256: `{receipt['receipt_sha256']}`",
            "",
            "Both historical generated reports are tracked, byte-identical to their Git index",
            "entries, and selected by matching content hashes in the current evidence DAG.",
            "",
            "| Acceptance item | Verified value |",
            "| --- | ---: |",
            f"| Runtime-domain candidates | {runtime['candidate_count']} |",
            f"| Validator-valid candidates | {runtime['validator_valid_count']} |",
            f"| Runtime-committed executions | {runtime['runtime_committed_count']} |",
            f"| Runtime-domain findings | {runtime['finding_count']} |",
            f"| Public-boundary probes passed | {public['passed_probe_count']}/35 |",
            (
                "| Semantic-invariance paired runs | "
                f"{public['semantic_invariance_paired_run_count']}/12 |"
            ),
            "",
            "The runtime report's embedded source commit is retained as historical generation",
            "provenance. It is not used as the current selector; current identity is bound by the",
            "report path and SHA-256 in `configs/current.json`.",
            "",
            "No historical report, current registry, global evidence DAG, or release manifest was",
            "rewritten by W1-M03. The target reports have no unexplained byte or binding drift.",
            "",
            "The repository-wide evidence checker already reported a stale executable-source",
            "fingerprint on the claimed main baseline. That explained integration drift is queued",
            "for coordinator-owned W1-M05/W1-M06 work; it is not a target-report mismatch and is",
            "outside W1-M03's hot-file authority.",
            "",
        ]
    )


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt = build_alignment_receipt(ROOT)
    if args.check:
        committed = _read_json(ROOT / REPORT_JSON_PATH)
        if committed.get("receipt_sha256") != receipt_sha256(committed):
            raise SystemExit("committed alignment receipt self-hash mismatch")
        if committed != receipt:
            raise SystemExit("committed alignment receipt differs from deterministic rebuild")
        if (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") != build_markdown_report(receipt):
            raise SystemExit("committed Markdown report differs from deterministic rebuild")
    else:
        (ROOT / REPORT_JSON_PATH).write_text(_json_text(receipt), encoding="utf-8", newline="\n")
        (ROOT / REPORT_MD_PATH).write_text(
            build_markdown_report(receipt), encoding="utf-8", newline="\n"
        )
    print(
        json.dumps(
            {
                "check": bool(args.check),
                "public_boundary_probes": 35,
                "receipt_sha256": receipt["receipt_sha256"],
                "runtime_domain_candidates": 237,
                "status": receipt["status"],
                "unexplained_target_report_drift": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
