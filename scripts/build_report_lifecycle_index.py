"""Classify every retained workstream JSON report without deleting evidence."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.eval.provenance import (  # noqa: E402
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)

DEFAULT_POLICY = ROOT / "configs/foundation/report_lifecycle_v0.1.json"
DEFAULT_CURRENT = ROOT / "configs/current.json"
DEFAULT_OUTPUT = ROOT / "workstreams/report-lifecycle-index-v0.1.json"


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def workstream_report_inventory(
    root: Path,
    policy: Mapping[str, Any],
) -> list[dict[str, Any]]:
    paths = sorted(root.glob(str(policy["report_glob"])))
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": file_sha256(path),
        }
        for path in paths
        if path.is_file()
    ]


def current_workstream_report_paths(current: Mapping[str, Any]) -> set[str]:
    nodes = current.get("evidence_dag", {}).get("nodes", {})
    if not isinstance(nodes, Mapping):
        raise ValueError("current evidence DAG nodes must be an object")
    paths = {
        str(node.get("path"))
        for node_id, node in nodes.items()
        if str(node_id) != "report_lifecycle_index"
        if isinstance(node, Mapping)
        and isinstance(node.get("path"), str)
        and str(node["path"]).startswith("workstreams/")
        and str(node["path"]).endswith(".json")
    }
    mechanism = current.get("mechanism_adaptation", {})
    if isinstance(mechanism, Mapping):
        for key in ("gate_a_report", "design_audit_report", "preflight_report"):
            value = mechanism.get(key)
            if isinstance(value, str) and value.startswith("workstreams/"):
                paths.add(value)
    return paths


def build_report_lifecycle_index(
    *,
    root: Path,
    policy: Mapping[str, Any],
    current: Mapping[str, Any],
    source_commit: str | None = None,
    source_tree_dirty: bool | None = None,
) -> dict[str, Any]:
    if policy.get("schema_version") != "chemworld-report-lifecycle-policy-0.1":
        raise ValueError("unsupported report lifecycle policy")
    allowed = set(policy["categories"])
    if allowed != {"current", "historical", "superseded", "external"}:
        raise ValueError("report lifecycle categories must be exact")

    inventory = workstream_report_inventory(root, policy)
    inventory_paths = {item["path"] for item in inventory}
    current_paths = current_workstream_report_paths(current)
    explicit_external = {str(path) for path in policy.get("external_paths", [])}
    explicit_superseded = {str(path) for path in policy.get("superseded_paths", [])}
    missing_explicit = sorted(
        (explicit_external | explicit_superseded | current_paths) - inventory_paths
    )
    if missing_explicit:
        raise ValueError(f"classified workstream report paths are missing: {missing_explicit}")
    overlap = explicit_external & explicit_superseded
    if overlap:
        raise ValueError(f"report paths have conflicting explicit categories: {sorted(overlap)}")

    entries: list[dict[str, Any]] = []
    for item in inventory:
        path = str(item["path"])
        if "/archive/" in f"/{path}":
            category = "historical"
            reason = "archive_directory"
        elif path in explicit_superseded:
            category = "superseded"
            reason = "explicit_superseded_path"
        elif path in explicit_external:
            category = "external"
            reason = "explicit_external_evidence"
        elif path in current_paths:
            category = "current"
            reason = "current_evidence_dag_reference"
        else:
            category = str(policy["default_noncurrent_category"])
            reason = "retained_noncurrent_default"
        entries.append(
            {
                **item,
                "category": category,
                "classification_reason": reason,
                "current_surface": path in current_paths,
                "deletion_authorized": False,
            }
        )

    counts = {
        category: sum(item["category"] == category for item in entries)
        for category in sorted(allowed)
    }
    return {
        "schema_version": "chemworld-report-lifecycle-index-0.1",
        "status": "complete",
        "policy_sha256": canonical_json_sha256(policy),
        "source_commit": git_source_commit(root) if source_commit is None else source_commit,
        "source_tree_dirty": (
            git_worktree_dirty(
                root,
                excluded_paths={DEFAULT_OUTPUT.relative_to(ROOT).as_posix()}
                if root.resolve() == ROOT.resolve()
                else (),
            )
            if source_tree_dirty is None
            else source_tree_dirty
        ),
        "report_corpus_sha256": canonical_json_sha256(inventory),
        "report_count": len(entries),
        "category_counts": counts,
        "all_reports_classified_exactly_once": sum(counts.values()) == len(entries),
        "deletion_authorized": False,
        "reports": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--current", type=Path, default=DEFAULT_CURRENT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = build_report_lifecycle_index(
        root=ROOT,
        policy=_load_object(args.policy),
        current=_load_object(args.current),
    )
    if args.check:
        existing = _load_object(args.output)
        if existing != report:
            raise RuntimeError("report lifecycle index is stale")
    else:
        write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "report_count": report["report_count"],
                "category_counts": report["category_counts"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
