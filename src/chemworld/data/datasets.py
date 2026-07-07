"""Dataset export utilities for ChemWorld trajectories."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from chemworld.data.logging import load_jsonl, to_builtin
from chemworld.data.submission import git_commit
from chemworld.data.validation import validate_records


@dataclass(frozen=True)
class DatasetExportResult:
    output_path: str
    record_count: int
    format: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_path": self.output_path,
            "record_count": self.record_count,
            "format": self.format,
        }


def _trajectory_paths(path: str | Path) -> list[Path]:
    root = Path(path)
    if root.is_file():
        return [root]
    trajectory_dir = root / "trajectories"
    if trajectory_dir.exists():
        return sorted(trajectory_dir.glob("*.jsonl"))
    return sorted(root.glob("*.jsonl"))


def load_dataset_records(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for trajectory_path in _trajectory_paths(path):
        trajectory_records = load_jsonl(trajectory_path)
        validate_records(trajectory_records)
        records.extend(trajectory_records)
    if not records:
        raise ValueError(f"No trajectory JSONL files found under {path}")
    return records


def flatten_record(record: dict[str, Any]) -> dict[str, Any]:
    observation = record.get("observation", {})
    flags = record.get("constraint_flags", {})
    return {
        "campaign_id": record.get("campaign_id"),
        "experiment_index": record.get("experiment_index"),
        "operation_id": record.get("operation_id"),
        "benchmark_task_id": record.get("benchmark_task_id"),
        "scenario_id": record.get("scenario_id"),
        "world_split": record.get("world_split"),
        "seed": record.get("seed"),
        "step": record.get("step"),
        "operation_type": record.get("operation_type"),
        "instrument": record.get("instrument"),
        "reward": record.get("reward"),
        "leaderboard_score": record.get("leaderboard_score"),
        "yield": observation.get("yield"),
        "selectivity": observation.get("selectivity"),
        "conversion": observation.get("conversion"),
        "score": observation.get("score"),
        "purity": observation.get("purity"),
        "recovery": observation.get("recovery"),
        "safety_risk": observation.get("safety_risk"),
        "cost": observation.get("cost"),
        "unsafe": flags.get("unsafe"),
        "precondition_failed": flags.get("precondition_failed"),
        "constitution_failed": flags.get("constitution_failed"),
        "action": json.dumps(to_builtin(record.get("action", {})), sort_keys=True),
    }


def export_dataset(
    path: str | Path,
    *,
    output: str | Path,
    format: str,
) -> DatasetExportResult:
    records = load_dataset_records(path)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if format == "jsonl":
        if len(_trajectory_paths(path)) == 1 and Path(path).is_file():
            shutil.copyfile(Path(path), output_path)
        else:
            with output_path.open("w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(to_builtin(record), sort_keys=True) + "\n")
    elif format == "parquet":
        frame = pd.DataFrame(flatten_record(record) for record in records)
        try:
            frame.to_parquet(output_path, index=False)
        except ImportError as exc:
            raise RuntimeError(
                "Parquet export requires pyarrow or fastparquet. "
                "Install one of them or export with --format jsonl."
            ) from exc
    else:
        raise ValueError("format must be 'jsonl' or 'parquet'")
    return DatasetExportResult(str(output_path), len(records), format)


def dataset_card(path: str | Path) -> dict[str, Any]:
    records = load_dataset_records(path)
    task_ids = sorted({str(record.get("benchmark_task_id")) for record in records})
    seeds = sorted({int(record["seed"]) for record in records})
    world_law_versions = sorted({str(record.get("world_family_version")) for record in records})
    env_versions = sorted({str(record.get("env_version")) for record in records})
    return {
        "dataset_id": f"chemworld-dataset-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
        "task_ids": task_ids,
        "world_law_version": world_law_versions,
        "env_version": env_versions,
        "commit_hash": git_commit(),
        "seeds": seeds,
        "record_count": len(records),
        "agent_manifests": sorted(
            {
                str(record.get("agent_metadata", {}).get("agent_name", "unknown"))
                for record in records
            }
        ),
        "license": "MIT for generated benchmark traces unless submission declares otherwise",
        "privacy_anonymization_status": "synthetic or submission-provided; review before release",
        "known_limitations": [
            "virtual semi-mechanistic world",
            "not calibrated to a specific real reaction",
            "private-eval parameters are not included in public datasets",
        ],
        "created_at": datetime.now(UTC).isoformat(),
    }


__all__ = ["DatasetExportResult", "dataset_card", "export_dataset", "load_dataset_records"]
