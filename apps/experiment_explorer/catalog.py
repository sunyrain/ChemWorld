"""Discover bound evidence and local trajectories without running experiments."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import threading
import time
from pathlib import Path
from typing import Any

from .categories import CATEGORIES, categories_in, ordered_categories, recorded_categories

MAX_FILE_BYTES = 128 * 1024 * 1024
SKIP_DIRS = {".git", "__pycache__", "provider", "provider_calls", "raw", "node_modules"}
ROOT_KEYS = {"run_root", "output_root", "root", "source_directory", "trajectory_path"}


def disk_path(path: Path) -> Path:
    """Keep Windows archive paths beyond MAX_PATH readable without renaming data."""
    if os.name == "nt" and path.is_absolute() and not str(path).startswith("\\\\?\\"):
        if str(path).startswith("\\\\"):
            return Path("\\\\?\\UNC\\" + str(path)[2:])
        return Path("\\\\?\\" + str(path))
    return path


def identity(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:24]


def read_json(path: Path) -> Any:
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("File exceeds the 128 MiB display limit")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def walk_values(value: Any, trail: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_values(child, (*trail, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_values(child, (*trail, str(index)))
    else:
        yield trail, value


def title(value: str) -> str:
    value = re.sub(r"\.jsonl?$", "", value)
    return value.replace("_", " ").replace("-", " ")


def evidence_mode(binding: dict, path: str) -> str:
    explicit = binding.get("evidence_mode")
    if explicit:
        return str(explicit)
    if binding.get("formal_result") is False:
        return "development"
    if binding.get("formal_result") is True:
        return "formal"
    status = str(binding.get("status", "")).lower()
    if any(x in status for x in ("historical", "superseded", "retired", "withdrawn")):
        return "historical"
    if "development" in status or "/development/" in path or "/dev/" in path:
        return "development"
    # A directory named 'formal' is a location, not proof of formal qualification.
    return "unspecified"


def metric_leaves(value: Any, trail: str = "") -> list[dict]:
    result = []
    if isinstance(value, dict):
        for key, child in value.items():
            name = f"{trail}.{key}" if trail else key
            if isinstance(child, dict):
                result.extend(metric_leaves(child, name))
            elif isinstance(child, (int, float)) and not isinstance(child, bool):
                result.append({"key": name, "value": child})
    return result


def report_metrics(report: dict) -> list[dict]:
    metrics = []
    for key in ("counts", "denominators", "physical_runs", "model_calls"):
        if isinstance(report.get(key), dict):
            metrics.extend(metric_leaves(report[key], key))
    for key, value in report.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            metrics.append({"key": key, "value": value})
    return metrics


class Catalog:
    def __init__(self, root: Path, run_roots: list[Path] | None = None):
        self.root = root.resolve()
        self.run_roots = [p.resolve() for p in (run_roots or [self.root / "runs"])]
        self.lock = threading.RLock()
        self.entries: dict[str, dict] = {}
        self.files: dict[str, Path] = {}
        self.reports: dict[str, Path] = {}
        self.errors: list[dict] = []
        self.indexed_at = 0.0
        self.summary_cache: dict[str, tuple[tuple, dict]] = {}

    def display_path(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    def safe_report(self, name: str) -> Path:
        path = (self.root / name).resolve()
        allowed = [self.root / "workstreams", *self.run_roots]
        if not any(path.is_relative_to(r) for r in allowed) or path.suffix != ".json":
            raise ValueError("Report must be under workstreams or a configured run root")
        return path

    def refresh(self) -> dict:
        """Atomically replace an in-memory index; never read provider payloads."""
        with self.lock:
            entries, reports, files, errors = {}, {}, {}, []
            report_categories, referenced_roots = {}, {}
            registry_path = self.root / "configs/current.json"
            try:
                registry = read_json(registry_path)
            except (OSError, ValueError) as exc:
                registry = {}
                errors.append({"path": "configs/current.json", "error": str(exc)})
            for trail, value in walk_values(registry):
                if not isinstance(value, str):
                    continue
                is_report = value.startswith("workstreams/") and "/reports/" in value
                is_summary = value.startswith("runs/") and trail[-1] in {
                    "report",
                    "summary",
                    "results",
                }
                if not (is_report or is_summary):
                    continue
                if not value.endswith(".json"):
                    continue
                entry_id = identity("report:" + value)
                if entry_id in entries:
                    entries[entry_id]["bindings"].append(".".join(trail))
                    continue
                binding = registry
                for part in trail[:-1]:
                    binding = binding[int(part)] if isinstance(binding, list) else binding[part]
                binding = binding if isinstance(binding, dict) else {}
                try:
                    path = self.safe_report(value)
                except ValueError as exc:
                    errors.append({"path": value, "error": str(exc)})
                    continue
                reports[entry_id] = path
                report_header = {}
                if path.is_file():
                    try:
                        source = read_json(path)
                        if isinstance(source, dict):
                            report_header = source
                    except (OSError, ValueError) as exc:
                        errors.append({"path": value, "error": str(exc)})
                entries[entry_id] = {
                    "id": entry_id,
                    "kind": "report",
                    "title": title(path.parent.name if is_summary else path.stem),
                    "path": value,
                    "bindings": [".".join(trail)],
                    "workstream": "Work I"
                    if "/arxiv_v1/" in value
                    else "Work II"
                    if "/flagship_tasks/" in value or "work-ii-" in value
                    else "Platform",
                    "mode": evidence_mode({**report_header, **binding}, value),
                    "status": binding.get("status", "bound"),
                    "available": path.is_file(),
                    "metrics": report_metrics(binding),
                    "modified": path.stat().st_mtime if path.is_file() else 0,
                    "roots": [
                        v
                        for t, v in walk_values(binding)
                        if t and t[-1] in ROOT_KEYS and isinstance(v, str)
                    ],
                }
                report_categories[entry_id] = categories_in(report_header)
                entry = entries[entry_id]
                entry["roots"].extend(
                    v
                    for t, v in walk_values(report_header)
                    if t and t[-1] in ROOT_KEYS and isinstance(v, str)
                )
                for source in entry["roots"]:
                    referenced_roots.setdefault((self.root / source).resolve(), set()).add(entry_id)
                for _, source in walk_values(report_header):
                    if isinstance(source, str) and source.endswith(".jsonl"):
                        referenced_roots.setdefault((self.root / source).resolve(), set()).add(
                            entry_id
                        )
            scanned = 0
            started = last_progress = time.monotonic()
            for run_root in self.run_roots:
                if not run_root.is_dir():
                    errors.append(
                        {
                            "path": self.display_path(run_root),
                            "error": "Local run directory is unavailable",
                        }
                    )
                    continue

                def scan_error(exc):
                    errors.append({"path": str(exc.filename), "error": str(exc)})

                for directory, subdirs, names in os.walk(disk_path(run_root), onerror=scan_error):
                    subdirs[:] = [
                        d
                        for d in subdirs
                        if d not in SKIP_DIRS
                        and not Path(directory, d).is_symlink()
                        and not getattr(Path(directory, d), "is_junction", lambda: False)()
                    ]
                    for name in names:
                        if not name.endswith(".jsonl"):
                            continue
                        path = run_root / Path(directory).relative_to(disk_path(run_root)) / name
                        try:
                            metadata = disk_path(path).lstat()
                            if stat.S_ISLNK(metadata.st_mode):
                                continue
                            if not ("trajectory" in name or name.startswith("episode")):
                                # Older runs use task/condition names. Inspect only their
                                # first record; avoid known provider and event log files.
                                if name in {
                                    "stdout.jsonl",
                                    "progress.jsonl",
                                    "tool_audit.jsonl",
                                    "history.jsonl",
                                    "numerics.jsonl",
                                    "transport.jsonl",
                                    "events.jsonl",
                                    "environment_events.jsonl",
                                }:
                                    continue
                                with disk_path(path).open(encoding="utf-8-sig") as handle:
                                    first = json.loads(handle.readline(2 * 1024 * 1024))
                                if not isinstance(first, dict) or not isinstance(
                                    first.get("action"), dict
                                ):
                                    continue
                        except OSError as exc:
                            scan_error(exc)
                            continue
                        except (ValueError, UnicodeError):
                            continue
                        file_id = identity(str(path))
                        if file_id in files:
                            continue
                        files[file_id] = path
                        parts = path.relative_to(run_root).parts
                        depth = 2 if parts[0] in {"development", "dev", "formal"} else 1
                        group_path = run_root.joinpath(*parts[: min(depth, len(parts) - 1)])
                        group_id = identity("run:" + str(group_path))
                        if group_id not in entries:
                            display = self.display_path(group_path)
                            entries[group_id] = {
                                "id": group_id,
                                "kind": "run",
                                "title": title(group_path.name),
                                "path": display,
                                "bindings": [],
                                "mode": evidence_mode({}, display),
                                "workstream": "Work II"
                                if "work-ii" in display
                                else "Work I"
                                if "work-i-" in display
                                else "Platform",
                                "status": "local",
                                "available": True,
                                "metrics": [],
                                "trajectory_count": 0,
                                "modified": 0,
                                "roots": [str(group_path)],
                            }
                        entry = entries[group_id]
                        categories = categories_in(path.as_posix())
                        if not categories:
                            try:
                                with disk_path(path).open(encoding="utf-8-sig") as handle:
                                    categories = recorded_categories(
                                        json.loads(handle.readline(2 * 1024 * 1024))
                                    )
                            except (OSError, ValueError, UnicodeError):
                                pass
                        entry["categories"] = sorted(set(entry.get("categories", [])) | categories)
                        for source in (path, *path.parents):
                            for report_id in referenced_roots.get(source, ()):
                                report_categories[report_id].update(categories)
                        entry["trajectory_count"] += 1
                        entry["modified"] = max(entry["modified"], metadata.st_mtime)
                        scanned += 1
                        if time.monotonic() - last_progress >= 30:
                            elapsed = time.monotonic() - started
                            print(
                                f"Indexing: {scanned} files, {scanned / elapsed:.0f} files/s",
                                flush=True,
                            )
                            last_progress = time.monotonic()
            for entry_id, entry in entries.items():
                entry["categories"] = ordered_categories(
                    report_categories.get(entry_id, entry.get("categories", []))
                )
            self.entries, self.reports, self.files, self.errors = entries, reports, files, errors
            self.summary_cache.clear()
            self.indexed_at = time.time()
            return self.snapshot()

    def snapshot(self) -> dict:
        with self.lock:
            entries = sorted(self.entries.values(), key=lambda e: e["modified"], reverse=True)
            return {
                "categories": CATEGORIES,
                "entries": [{k: v for k, v in e.items() if k != "roots"} for e in entries],
                "counts": {
                    "reports": len(self.reports),
                    "runs": len(entries) - len(self.reports),
                    "trajectories": len(self.files),
                },
                "indexed_at": self.indexed_at,
                "errors": self.errors,
            }

    def report(self, entry_id: str) -> dict:
        with self.lock:
            path = self.reports[entry_id]
        value = read_json(self.safe_report(str(path)))
        return value if isinstance(value, dict) else {"data": value}

    def detail(self, entry_id: str) -> dict:
        with self.lock:
            entry = dict(self.entries[entry_id])
            files = list(self.files.items())
        report, error = {}, None
        if entry["kind"] == "report":
            try:
                report = self.report(entry_id)
            except (OSError, ValueError) as exc:
                error = str(exc)
        elif entry["kind"] == "run":
            # Fixed conventional names, never a guessed 'latest' version. If several
            # exist, display each under its own filename without mixing statistics.
            local_reports = {}
            group = (self.root / entry["path"]).resolve()
            for name in ("summary.json", "report.json", "results.json", "result.json"):
                candidate = group / name
                if not candidate.is_file():
                    continue
                try:
                    checked = self.safe_report(str(candidate))
                    local_reports[name] = read_json(checked)
                except (OSError, ValueError) as exc:
                    local_reports[name] = {"read_error": str(exc)}
            if len(local_reports) == 1:
                source_name, source_data = next(iter(local_reports.items()))
                report = (
                    source_data if isinstance(source_data, dict) else {source_name: source_data}
                )
            else:
                report = local_reports
        roots = list(entry.pop("roots"))
        direct_paths = set()
        for trail, value in walk_values(report):
            if not isinstance(value, str):
                continue
            if value.endswith(".jsonl"):
                direct_paths.add((self.root / value).resolve())
            elif trail and trail[-1] in ROOT_KEYS:
                roots.append(value)
        resolved = set()
        for value in roots:
            path = (self.root / value).resolve()
            if any(path.is_relative_to(r) for r in self.run_roots):
                resolved.add(path)
        trajectories = []
        for file_id, path in files:
            if path in direct_paths or resolved.intersection(path.parents):
                trajectories.append(
                    {
                        "id": file_id,
                        "path": self.display_path(path),
                        "name": "/".join(path.parts[-3:]),
                    }
                )
        trajectories.sort(key=lambda t: t["path"])
        mode = evidence_mode(report, entry["path"])
        if mode != "unspecified":
            entry["mode"] = mode
        return {
            "entry": entry,
            "report": report,
            "metrics": report_metrics(report),
            "trajectories": trajectories,
            "error": error,
        }

    def trajectory(self, file_id: str) -> dict:
        with self.lock:
            path = self.files[file_id]
        if not any(path.resolve().is_relative_to(r) for r in self.run_roots):
            raise ValueError("Trajectory is outside the configured run roots")
        path = disk_path(path)
        if path.stat().st_size > MAX_FILE_BYTES:
            raise ValueError("File exceeds the 128 MiB display limit")
        records, errors = [], []
        with path.open(encoding="utf-8-sig") as handle:
            for number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if not isinstance(row, dict) or not isinstance(row.get("action"), dict):
                        raise ValueError("Expected a ChemWorld record with an action object")
                    records.append(row)
                except ValueError as exc:
                    # Only the contiguous valid prefix is playable. Never silently
                    # jump over a corrupt action and pretend the sequence is complete.
                    errors.append({"line": number, "error": str(exc)})
                    break
        if not records:
            raise ValueError(f"No playable trajectory records. {errors}")
        return {
            "id": file_id,
            "name": path.name,
            "path": self.display_path(self.files[file_id]),
            "records": records,
            "errors": errors,
            "record_count": len(records),
            "context": self.recording_context(file_id),
        }

    def planning_context(self, file_id: str) -> dict:
        """Label a separately executed recipe without merging different matrix cells."""
        path = self.files[file_id]
        parts = path.parts
        for i in range(len(parts) - 5):
            if parts[i : i + 2] != ("physical", "source"):
                continue
            source, round_id, member = parts[i + 2 : i + 5]
            if not round_id.isdigit() or parts[i + 5] != "trajectory.jsonl":
                continue
            name = f"acquire_{source}_{round_id}"
            try:
                plan_path = self.safe_report(str(Path(*parts[:i]) / "model" / name / "result.json"))
                saved = read_json(disk_path(plan_path))
                plans = saved.get("payload")
                if saved.get("name") != name or not isinstance(plans, dict) or member not in plans:
                    continue
                return {
                    "kind": "one_shot_plan",
                    "model": saved.get("model"),
                    "planning_call": name,
                    "source": source,
                    "round": int(round_id),
                    "member": member,
                    "planned": len(plans),
                    "plan": plans[member],
                    "path": self.display_path(plan_path),
                }
            except (OSError, ValueError, AttributeError):
                continue
        return {}

    def recording_context(self, file_id: str) -> dict:
        """Read only known adjacent receipts. Never reconstruct a retired prompt."""
        parent = self.files[file_id].parent
        planning = self.planning_context(file_id)
        context = {"planning": planning} if planning else {}
        keys = {
            "completed",
            "failure",
            "status",
            "arm",
            "analysis",
            "provider_receipts",
            "provider_final",
            "final_payload",
            "model",
            "kind",
            "task",
        }
        for name in ("summary.json", "result.json", "receipts.json"):
            path = parent / name
            if not disk_path(path).is_file():
                continue
            try:
                resolved = path.resolve()
                if not any(resolved.is_relative_to(r) for r in self.run_roots):
                    continue
                value = read_json(disk_path(resolved))
                if isinstance(value, dict):
                    context[name] = {k: v for k, v in value.items() if k in keys}
                elif name == "receipts.json" and isinstance(value, list):
                    context[name] = [
                        {k: v for k, v in r.items() if k in keys}
                        for r in value
                        if isinstance(r, dict)
                    ]
            except (ValueError, OSError) as exc:
                context[name] = {"read_error": str(exc)}
        return context

    def recording_summaries(self, file_ids: list[str]) -> dict:
        from .recording import recording_summary

        if len(file_ids) > 16:
            raise ValueError("Request up to 16 recording summaries at a time")
        results = {}
        for file_id in file_ids:
            try:
                with self.lock:
                    path = self.files[file_id]
                resolved = path.resolve()
                if not any(resolved.is_relative_to(r) for r in self.run_roots):
                    raise ValueError("File is outside configured run roots")
                native = disk_path(path)
                info = native.stat()
                signature = (info.st_mtime_ns, info.st_size)
                if info.st_size > MAX_FILE_BYTES:
                    raise ValueError("File exceeds 128 MiB display limit")
                cached = self.summary_cache.get(file_id)
                if cached and cached[0] == signature:
                    results[file_id] = cached[1]
                    continue
                result = recording_summary(native)
                planning = self.planning_context(file_id)
                if planning:
                    result["planning"] = {k: v for k, v in planning.items() if k != "plan"}
                self.summary_cache[file_id] = (signature, result)
                results[file_id] = result
            except (KeyError, OSError, ValueError) as exc:
                results[file_id] = {"error": str(exc)}
        return results
