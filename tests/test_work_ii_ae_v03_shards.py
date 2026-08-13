from __future__ import annotations

import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    RECEIPT_VERSION,
    AEPriorQualificationV03Error,
    _build_plan,
    validate_plan,
)
from chemworld.eval.work_ii_ae_v03_shards import (
    execute_shard,
    materialize_merged_output,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)
RUNNER_SCRIPT = ROOT / "scripts/run_work_ii_ae_v03_shards.py"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_scientific_rejection_is_a_successful_terminal_merge_status() -> None:
    spec = importlib.util.spec_from_file_location("ae_v03_shard_runner", RUNNER_SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert "scientifically_rejected" in module.MERGED_TERMINAL_STATUSES


def _two_cluster_plan() -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _load(CONTRACT_PATH)
    plan = _build_plan(ROOT, CONTRACT_PATH, contract, "classifier_fit")
    plan["executions"] = deepcopy(plan["executions"][:48])
    plan["task_locus_bindings"] = deepcopy(plan["task_locus_bindings"][:1])
    plan["denominators"] = {
        "included_loci": 1,
        "worlds": 2,
        "primary_executions": 48,
        "exact_replays": 48,
    }
    plan["plan_sha256"] = canonical_json_sha256(
        {key: value for key, value in plan.items() if key != "plan_sha256"}
    )
    assert validate_plan(plan) == []
    return contract, plan


def _fake_executor(
    _root: Path,
    plan: dict[str, Any],
    row: dict[str, Any],
    output_root: Path,
    *,
    execution_root: Path,
) -> dict[str, Any]:
    execution_root.mkdir(parents=True)
    trajectory = execution_root / "trajectory.jsonl"
    trajectory.write_text(
        json.dumps(
            {
                "execution_id": row["execution_id"],
                "world_seed": row["world_seed"],
                "observation_seed": row["observation_seed"],
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    metrics = dict.fromkeys(row["measured_metric_ids"], 0.5)
    receipt = {
        key: deepcopy(row[key])
        for key in (
            "execution_index",
            "execution_id",
            "phase",
            "task_id",
            "locus_id",
            "world_index",
            "world_seed",
            "anchor_id",
            "target_category",
            "replicate",
            "anchor_recipe",
            "measurement_stage_id",
        )
    }
    receipt.update(
        {
            "schema_version": RECEIPT_VERSION,
            "plan_sha256": plan["plan_sha256"],
            "provider_call_count": 0,
            "status": "completed",
            "measurement": {
                "measurement_stage_id": row["measurement_stage_id"],
                "metrics": metrics,
            },
            "classification_metrics": {
                name: metrics[name] for name in row["classification_metric_ids"]
            },
            "non_gating_secondary_metrics": {
                name: metrics[name] for name in row["non_gating_secondary_metric_ids"]
            },
            "exact_replay": {"verified": True},
            "trajectory": {
                "path": trajectory.relative_to(output_root).as_posix(),
                "sha256": file_sha256(trajectory),
            },
            "failure": None,
        }
    )
    receipt["receipt_sha256"] = canonical_json_sha256(receipt)
    return receipt


def _fake_report(
    _contract: dict[str, Any],
    plan: dict[str, Any],
    receipts: list[dict[str, Any]],
    *,
    fit_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    assert fit_report is None
    report = {
        "status": "completed",
        "phase": plan["phase"],
        "receipt_sha256s": [receipt["receipt_sha256"] for receipt in receipts],
    }
    report["report_sha256"] = canonical_json_sha256(report)
    return report


def _run_two_shards(plan: dict[str, Any], shard_root: Path) -> None:
    for shard_index in range(2):
        summary = execute_shard(
            ROOT,
            plan,
            shard_root,
            shard_index=shard_index,
            shard_count=2,
            executor=_fake_executor,
        )
        assert summary["status"] == "completed"


def test_sharded_merge_is_serial_equivalent_at_cluster_boundary(tmp_path: Path) -> None:
    contract, plan = _two_cluster_plan()
    shard_root = tmp_path / "shards"
    _run_two_shards(plan, shard_root)

    manifests = [
        _load(shard_root / f"shard-{index:05d}-of-00002" / "shard-manifest.json")
        for index in range(2)
    ]
    assert [manifest["execution_count"] for manifest in manifests] == [24, 24]
    assert all(len(manifest["cluster_keys"]) == 1 for manifest in manifests)

    serial_root = tmp_path / "serial"
    serial_receipts = [
        _fake_executor(
            ROOT,
            plan,
            row,
            serial_root,
            execution_root=serial_root / "executions" / str(row["execution_index"]),
        )
        for row in plan["executions"]
    ]
    merged_root = tmp_path / "merged"
    result = materialize_merged_output(
        contract,
        plan,
        shard_root,
        merged_root,
        shard_count=2,
        report_builder=_fake_report,
    )
    assert result["primary_executions"] == 48
    merged_receipts = [
        _load(merged_root / "receipts" / f"{index}.json") for index in range(48)
    ]
    assert merged_receipts == serial_receipts
    assert _load(merged_root / "report.json")["receipt_sha256s"] == [
        receipt["receipt_sha256"] for receipt in serial_receipts
    ]
    for index in range(48):
        assert (
            merged_root / "executions" / str(index) / "trajectory.jsonl"
        ).read_bytes() == (
            serial_root / "executions" / str(index) / "trajectory.jsonl"
        ).read_bytes()


@pytest.mark.parametrize("corruption", ["missing", "execution_index", "plan", "trajectory"])
def test_merge_rejects_incomplete_or_rebound_shard_set(
    tmp_path: Path, corruption: str
) -> None:
    contract, plan = _two_cluster_plan()
    shard_root = tmp_path / "shards"
    _run_two_shards(plan, shard_root)
    receipt_path = shard_root / "shard-00000-of-00002" / "receipts" / "0.json"
    if corruption == "missing":
        receipt_path.unlink()
    elif corruption == "trajectory":
        trajectory = shard_root / "shard-00000-of-00002/executions/0/trajectory.jsonl"
        trajectory.write_text("tampered\n", encoding="utf-8")
    else:
        receipt = _load(receipt_path)
        if corruption == "execution_index":
            receipt["execution_index"] = 1
        else:
            receipt["plan_sha256"] = "0" * 64
        receipt["receipt_sha256"] = canonical_json_sha256(
            {key: value for key, value in receipt.items() if key != "receipt_sha256"}
        )
        receipt_path.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    with pytest.raises(AEPriorQualificationV03Error):
        materialize_merged_output(
            contract,
            plan,
            shard_root,
            tmp_path / "merged",
            shard_count=2,
            report_builder=_fake_report,
        )
