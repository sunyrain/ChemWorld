"""Create, inspect, validate, and complete non-overlapping task claims."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

CLAIM_SCHEMA_VERSION = "chemworld-task-claim-0.1"
TASK_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
REQUIRED_FIELDS = {
    "schema_version",
    "task_id",
    "owner",
    "branch",
    "status",
    "scope",
    "owned_paths",
    "claimed_at",
    "expires_at",
    "notes",
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _normalize_owned_path(value: str) -> str:
    normalized = value.strip().replace("\\", "/").strip("/")
    if not normalized or normalized.startswith("../") or "/../" in normalized:
        raise ValueError(f"invalid owned path: {value!r}")
    return normalized


def _read_claim(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _write_claim(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _claim_files(root: Path, status: str) -> list[Path]:
    return sorted((root / "claims" / status).glob("*.json"))


def validate_claim(path: Path, payload: dict[str, Any], *, active: bool) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(payload))
    if missing:
        errors.append(f"missing fields: {missing}")
    if payload.get("schema_version") != CLAIM_SCHEMA_VERSION:
        errors.append("unsupported schema_version")
    task_id = str(payload.get("task_id", ""))
    if not TASK_ID_PATTERN.fullmatch(task_id):
        errors.append("task_id must use lowercase letters, digits, dot, underscore, or dash")
    if path.stem != task_id and active:
        errors.append("active claim filename must equal task_id")
    for field in ("owner", "branch", "scope"):
        if not str(payload.get(field, "")).strip():
            errors.append(f"{field} cannot be empty")
    expected_status = "active" if active else "completed"
    if payload.get("status") != expected_status:
        errors.append(f"status must be {expected_status!r}")
    owned_paths = payload.get("owned_paths")
    if not isinstance(owned_paths, list) or not owned_paths:
        errors.append("owned_paths must be a non-empty list")
    else:
        try:
            normalized = [_normalize_owned_path(str(value)) for value in owned_paths]
            if len(normalized) != len(set(normalized)):
                errors.append("owned_paths contains duplicates")
        except ValueError as error:
            errors.append(str(error))
    for field in ("claimed_at", "expires_at"):
        try:
            datetime.fromisoformat(str(payload.get(field, "")))
        except ValueError:
            errors.append(f"{field} must be ISO-8601")
    if active and not errors:
        expires_at = datetime.fromisoformat(str(payload["expires_at"]))
        if expires_at.tzinfo is None:
            errors.append("expires_at must include a timezone")
        elif expires_at <= datetime.now(UTC):
            errors.append("claim has expired")
    return errors


def _paths_overlap(left: str, right: str) -> bool:
    left_parts = _normalize_owned_path(left).split("/")
    right_parts = _normalize_owned_path(right).split("/")
    shared = min(len(left_parts), len(right_parts))
    return left_parts[:shared] == right_parts[:shared]


def check_claims(root: Path) -> dict[str, Any]:
    active_items: list[tuple[Path, dict[str, Any]]] = []
    completed_items: list[tuple[Path, dict[str, Any]]] = []
    errors: list[str] = []
    for active, status in ((True, "active"), (False, "completed")):
        target = active_items if active else completed_items
        for path in _claim_files(root, status):
            try:
                payload = _read_claim(path)
            except (ValueError, json.JSONDecodeError) as error:
                errors.append(f"{path}: {error}")
                continue
            target.append((path, payload))
            errors.extend(
                f"{path}: {message}"
                for message in validate_claim(path, payload, active=active)
            )
    task_ids: dict[str, Path] = {}
    owned: list[tuple[str, str, Path]] = []
    for path, payload in active_items:
        task_id = str(payload.get("task_id", ""))
        if task_id in task_ids:
            errors.append(f"duplicate active task_id {task_id!r}: {task_ids[task_id]} and {path}")
        task_ids[task_id] = path
        for owned_path in payload.get("owned_paths", []):
            try:
                normalized = _normalize_owned_path(str(owned_path))
            except ValueError as error:
                errors.append(f"{path}: {error}")
                continue
            for other_task, other_path, other_file in owned:
                if _paths_overlap(normalized, other_path):
                    errors.append(
                        f"owned path overlap: {task_id}:{normalized} and "
                        f"{other_task}:{other_path} ({other_file})"
                    )
            owned.append((task_id, normalized, path))
    return {
        "schema_version": "chemworld-task-claim-check-0.1",
        "passed": not errors,
        "active_claim_count": len(active_items),
        "completed_claim_count": len(completed_items),
        "errors": errors,
        "active_claims": [payload for _, payload in active_items],
    }


def create_claim(
    root: Path,
    *,
    task_id: str,
    owner: str,
    branch: str,
    scope: str,
    owned_paths: list[str],
    days: int = 7,
    notes: str = "",
) -> Path:
    if not TASK_ID_PATTERN.fullmatch(task_id):
        raise ValueError("invalid task_id")
    if days < 1 or days > 30:
        raise ValueError("days must be between 1 and 30")
    destination = root / "claims" / "active" / f"{task_id}.json"
    if destination.exists():
        raise ValueError(f"task {task_id!r} is already claimed")
    normalized_paths = [_normalize_owned_path(path) for path in owned_paths]
    current = check_claims(root)
    if not current["passed"]:
        raise ValueError("existing claim registry is invalid: " + "; ".join(current["errors"]))
    for claim in current["active_claims"]:
        for new_path in normalized_paths:
            for active_path in claim["owned_paths"]:
                if _paths_overlap(new_path, str(active_path)):
                    raise ValueError(
                        f"owned path {new_path!r} overlaps active task "
                        f"{claim['task_id']!r} path {active_path!r}"
                    )
    now = datetime.now(UTC)
    payload = {
        "schema_version": CLAIM_SCHEMA_VERSION,
        "task_id": task_id,
        "owner": owner.strip(),
        "branch": branch.strip(),
        "status": "active",
        "scope": scope.strip(),
        "owned_paths": normalized_paths,
        "claimed_at": now.isoformat(),
        "expires_at": (now + timedelta(days=days)).isoformat(),
        "notes": notes.strip(),
    }
    errors = validate_claim(destination, payload, active=True)
    if errors:
        raise ValueError("invalid claim: " + "; ".join(errors))
    _write_claim(destination, payload)
    return destination


def complete_claim(root: Path, *, task_id: str, owner: str, summary: str) -> Path:
    source = root / "claims" / "active" / f"{task_id}.json"
    if not source.is_file():
        raise ValueError(f"active claim {task_id!r} does not exist")
    payload = _read_claim(source)
    if payload.get("owner") != owner:
        raise ValueError("only the recorded owner can complete a claim")
    now = datetime.now(UTC)
    payload.update(
        {
            "status": "completed",
            "completed_at": now.isoformat(),
            "completion_summary": summary.strip(),
        }
    )
    destination = (
        root
        / "claims"
        / "completed"
        / f"{task_id}--{now.strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    _write_claim(destination, payload)
    source.unlink()
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repository_root())
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    subparsers.add_parser("check")
    claim = subparsers.add_parser("claim")
    claim.add_argument("--task-id", required=True)
    claim.add_argument("--owner", required=True)
    claim.add_argument("--branch", required=True)
    claim.add_argument("--scope", required=True)
    claim.add_argument("--paths", nargs="+", required=True)
    claim.add_argument("--days", type=int, default=7)
    claim.add_argument("--notes", default="")
    complete = subparsers.add_parser("complete")
    complete.add_argument("--task-id", required=True)
    complete.add_argument("--owner", required=True)
    complete.add_argument("--summary", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.command in {"list", "check"}:
        report = check_claims(root)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["passed"] else 1
    if args.command == "claim":
        path = create_claim(
            root,
            task_id=args.task_id,
            owner=args.owner,
            branch=args.branch,
            scope=args.scope,
            owned_paths=args.paths,
            days=args.days,
            notes=args.notes,
        )
    else:
        path = complete_claim(
            root,
            task_id=args.task_id,
            owner=args.owner,
            summary=args.summary,
        )
    print(json.dumps({"path": str(path), "status": args.command}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
