"""Import completed notebook campaigns as local, read-only workbench archives.

No simulator or provider calls. Original records stay untouched; only public events,
instrument packets, notebook revisions and sealed model reports are copied.
"""

# ruff: noqa: RUF001 -- Chinese workbench labels.
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from apps.research_workbench.workspace_lock import WorkspaceLock
from scripts.report_paper_case_notebooks import jsonl, readable_posttests
from scripts.run_paper_case_notebooks import CASES, case_folder, read

from chemworld.workbench.service import write_json
from chemworld.workbench.signals import chart_series

TITLES = {
    "EC-discovery": "电化学 · 发现",
    "EC-optimization": "电化学 · 优化",
    "EQ-Sol": "平衡外推 · Sol",
    "EQ-Astra": "平衡外推 · Astra",
    "C-12": "结晶热条件 · 12 批",
    "C-24": "结晶热条件 · 24 批",
}
STAGES = {"K1": "机理报告", "Q": "盲预测", "K2": "事后复盘", "EQS": "平衡补充问答"}


def import_case(
    root: Path, reports: Path, destination: Path, case: dict, *, repeat_label: str | None = None
) -> dict:
    row = read(reports / f"{case['id']}.json")
    if row["status"] != "completed":
        raise ValueError("This importer accepts completed chains only")
    source = case_folder(root, case)
    documents = list(source.glob("**/notebook/experiment_documents"))
    if len(documents) != 1:
        raise ValueError("Expected one notebook document directory")
    ledger = jsonl(documents[0] / "environment_authoritative_ledger.jsonl")
    trajectory = jsonl(source / "trajectory.jsonl")
    if len(ledger) != len(trajectory) or len(ledger) != row["operations"]:
        raise ValueError("Public events and executed operations differ")
    identity = f"chemworld:paper-case-notebooks:{root.resolve().as_posix()}:{case['id']}"
    run_id = uuid5(NAMESPACE_URL, identity).hex
    target = destination / run_id
    if (target / "run.json").exists():
        saved = read(target / "run.json")
        if saved.get("import_identity") != identity:
            raise ValueError("Existing record has a different import identity")
        return {"case": case["id"], "id": run_id, "status": "already_imported"}
    target.mkdir(parents=True, exist_ok=True)
    # Write run.json last, so interrupted imports never appear as complete archives.
    events = []
    for public, record in zip(ledger, trajectory, strict=True):
        if public["action"] != record["action"]:
            raise ValueError("Public action does not match its trajectory")
        view = record["agent_view"]["tool_json"]
        event = {
            "event_id": public["event_id"],
            "recorded_at": record["timestamp"],
            "batch": record["experiment_index"] + 1,
            "action": public["action"],
            "transaction_status": public["transaction_status"],
            "observation": public["observation"],
            "observed_mask": dict.fromkeys(public["observed_keys"], True),
            "report": view.get("lab_report", {}),
            "delta": public.get("state_delta_summary", {}),
            "validation": {"valid": public["ok"]},
        }
        raw = view.get("raw_signal")
        if raw and public["action"]["operation"] == "measure" and public["ok"]:
            event["measurement"] = public["event_id"]
            event["series"] = chart_series(raw, public["action"]["instrument"])
            write_json(target / "measurements" / f"{public['event_id']}.json", raw)
        events.append(event)
    # Preserve original texts, timestamps, cursors and revision numbers byte for byte.
    (target / "experiment_documents/notebook_history").mkdir(parents=True, exist_ok=True)
    for filename in ("environment_authoritative_ledger.jsonl", "model_owned_notebook.md"):
        shutil.copyfile(documents[0] / filename, target / "experiment_documents" / filename)
    for revision in (documents[0] / "notebook_history").glob("[0-9]*.json"):
        shutil.copyfile(revision, target / "experiment_documents/notebook_history" / revision.name)
    last = trajectory[-1]["agent_view"]["tool_json"]
    campaign = last["campaign_state"]
    usage = row["token_accounting"]
    metadata = {
        "id": run_id,
        "import_identity": identity,
        "archive_only": True,
        "case_id": case["id"],
        "name": TITLES[case["id"]] + (f" · {repeat_label}" if repeat_label else ""),
        "project": (
            "论文案例 · 同世界稳定性 · 2026-10-13"
            if repeat_label
            else "论文案例 · 同期笔记复跑 · 2026-10-13"
        ),
        "stability_repeat": repeat_label,
        "question": (
            "模型自主探索虚拟实验室；同期笔记与封闭后测分开保存。开发复跑，无新增无笔记对照。"
        ),
        "created_at": trajectory[0]["timestamp"],
        "updated_at": trajectory[-1]["timestamp"],
        "design": {
            "task_id": trajectory[0]["task_id"],
            "seed": trajectory[0]["seed"],
            "budget": trajectory[0]["budget"],
            "campaign_cell": case["cell"],
            "batches": case["batches"],
        },
        "status": "completed",
        "actor": case["model"],
        "provider": "native-campaign-archive",
        "model_configuration": {"requested_model": case["model"], "reasoning_effort": "medium"},
        "model_calls": None,
        "model_tool_calls": None,
        "usage": {**usage["total"], "complete": usage["complete"]},
        "wall_time_s": row["elapsed_s"],
        "cost_usd": None,
        "events": events,
        "submitted_steps": len(events),
        "executed_steps": len(trajectory),
        "rejected_steps": sum(e["transaction_status"] != "committed" for e in events),
        "final_assay_count": row["completed_batches"],
        "batch_count": case["batches"],
        "replay": row["exact_replay"],
        "message": (
            "已导入完整实验链。回放结果来自原执行；此档案只供阅览，不能直接续跑或复制为同条件实验。"
        ),
        "view": {
            "observation": last.get("observation", {}),
            "lab_report": last.get("lab_report", {}),
            "campaign_state": {
                key: campaign[key]
                for key in ("operation_count", "remaining_budget", "final_assay_count")
                if key in campaign
            },
        },
        "sealed_reports": [
            {
                "stage": stage,
                "title": STAGES[stage],
                "payload": row["posttests"][stage]["payload"],
                "text": readable_posttests(case, {stage: row["posttests"][stage]})
                .split(f"## {stage}\n", 1)[1]
                .strip(),
            }
            for stage in STAGES
            if stage in row["posttests"]
        ],
        "retained_failures": {
            "notebook_tool_errors": row["notebook"]["tool_failures"],
            "laboratory_tool_errors": row["source_usage"]["recovered_mcp_tool_failure_count"],
        },
    }
    write_json(target / "run.json", metadata)
    return {"case": case["id"], "id": run_id, "status": "imported", "batches": case["batches"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--repeat-label")
    args = parser.parse_args()
    lock = WorkspaceLock(args.data_dir)
    try:
        for case in CASES:
            print(
                import_case(
                    args.root.resolve(),
                    args.reports,
                    args.data_dir,
                    case,
                    repeat_label=args.repeat_label,
                ),
                flush=True,
            )
    finally:
        lock.close()


if __name__ == "__main__":
    main()
