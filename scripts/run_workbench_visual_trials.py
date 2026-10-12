"""Five fixed development trials in a running local workbench; no provider calls."""

# ruff: noqa: RUF001 -- Chinese user-facing notebook text.

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://127.0.0.1:8892")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)

    def request(path: str, body: dict | None = None) -> dict:
        req = urllib.request.Request(
            args.base + path,
            data=json.dumps(body).encode("utf-8") if body is not None else None,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)

    units = [
        ("加热时间对照 · 4 min", "reaction-to-assay", 240),
        ("加热时间对照 · 8 min", "reaction-to-assay", 480),
        ("加热时间对照 · 12 min", "reaction-to-assay", 720),
        ("结晶过程试跑", "reaction-to-crystallization", None),
        ("连续流过程试跑", "flow-reaction-optimization", None),
    ]
    results = []
    started = time.monotonic()
    for index, (name, task, duration) in enumerate(units, 1):
        result = {"name": name, "task_id": task, "duration_s": duration, "failures": []}
        results.append(result)
        run = None
        try:
            question = (
                "80 °C 下，加热时长如何影响虚拟环境的转化率、产率与选择性？"
                if duration
                else "观察虚拟环境的完整过程、仪器信号与终检。"
            )
            run = request(
                "/api/runs",
                {
                    "name": name,
                    "project": "工作台开发试跑 · 2026-10-12",
                    "question": question,
                    "design": {"task_id": task, "seed": 7, "budget": 32},
                },
            )
            result["id"] = run["id"]
            path = "/api/runs/" + run["id"]
            recipe = run["recipe"]
            if duration is not None:
                for action in recipe:
                    if action["operation"] == "heat":
                        action.update(target_temperature_K=353.15, duration_s=duration)
            result["planned_actions"] = recipe
            before = (
                "开发脚本记录（人工笔记区；不是模型自主研究记录）。\n"
                + question
                + "\n假设：加热时长可能改变转化与产物分布，方向待观测。\n"
                + "固定条件：seed 7，预算 32；"
                + (f"本单元加热时长 {duration} s。\n" if duration else "时长沿用参考步骤。\n")
                + "按事前固定步骤执行；拒绝即停止该单元，保留结果，不追加重跑。"
            )
            request(
                path + "/notebook",
                {
                    "author": "human",
                    "operation": "write",
                    "arguments": {"text": before, "message": "执行前的固定设计"},
                },
            )
            for count, action in enumerate(recipe, 1):
                run = request(
                    path + "/step", {"action": action, "expected_step": run["submitted_steps"]}
                )
                elapsed = time.monotonic() - started
                print(
                    f"unit {index}/5; action {count}/{len(recipe)}; {action['operation']}; "
                    f"elapsed {elapsed:.1f}s",
                    flush=True,
                )
                if run["events"][-1]["transaction_status"] != "committed":
                    result["failures"].append(
                        {"reason": "action rejected", "event": run["events"][-1]}
                    )
                    break
                if run["status"] != "ready":
                    break
            result.update(
                submitted=run["submitted_steps"],
                rejected=run["rejected_steps"],
                final_assays=run["final_assay_count"],
                status=run["status"],
                signal_channels=sum(len(event.get("series", [])) for event in run["events"]),
                simulated_time_s=sum(
                    event.get("delta", {}).get("delta_time_s", 0) for event in run["events"]
                ),
                public_metrics=run["view"].get("lab_report", {}).get("visible_metrics", {}),
            )
            if run["submitted_steps"]:
                result["replay"] = request(path + "/replay", {})
            if result["final_assays"] != 1 or not result.get("replay", {}).get("verified"):
                result["failures"].append({"reason": "terminal assay or exact replay missing"})
            report = (
                before
                + "\n\n实测公开结果：\n"
                + json.dumps(
                    {
                        key: value
                        for key, value in result.items()
                        if key not in {"planned_actions", "failures"}
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n范围：开发单次试跑，不支持普遍规律或模型能力结论。"
            )
            request(
                path + "/notebook",
                {
                    "author": "human",
                    "operation": "write",
                    "arguments": {"text": report, "message": "真实观测与回放结果"},
                },
            )
        except Exception as exc:
            result["failures"].append({"reason": f"{type(exc).__name__}: {exc}"})
        finally:
            if run:
                path = "/api/runs/" + run["id"]
                if run["status"] == "ready":
                    request(path + "/cancel", {})
                snapshot = request(path)
                result["status"] = snapshot["status"]
                (args.output / f"unit-{index}.json").write_text(
                    json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            summary = {
                "development_only": True,
                "planned_units": 5,
                "executed_units": index,
                "passed_units": sum(not item["failures"] for item in results),
                "real_provider_requests": 0,
                "units": results,
            }
            (args.output / "summary.json").write_text(
                json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
            )
    print(json.dumps({key: value for key, value in summary.items() if key != "units"}), flush=True)
    return int(any(item["failures"] for item in results))


if __name__ == "__main__":
    raise SystemExit(main())
