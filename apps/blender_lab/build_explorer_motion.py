"""Author presentation choreography; never run Core or submit environment commands.

Routes reuse the scene navigator against catalog geometry. The reaction handoff below
exists only in this illustration, not in the service's sample custody contract.
"""

from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

from .catalog import ASSETS
from .navigation import Navigator

ROOT = Path(__file__).resolve().parent


def build_motion():
    definition = json.loads((ROOT / "environment.json").read_text(encoding="utf-8"))
    demo = json.loads((ROOT / "static/demo.json").read_text(encoding="utf-8"))
    stations = deepcopy(definition["stations"])
    stations["reaction"]["sample_position_m"] = [-2.25, 1.98, 0.94]
    nav = Navigator(
        SimpleNamespace(poses={a["id"]: list(a["location"]) for a in ASSETS}), definition
    )
    pose = {
        "position": stations["home"]["dock_m"],
        "yaw": 0,
        "extension": 0,
        "target": [-2.25, 1.98, 1.11],
        "gripperOpen": True,
        "sampleVisible": False,
        "holder": "reaction",
        "samplePosition": stations["reaction"]["sample_position_m"],
    }
    segments, starts, ends = [], [0], [0]
    elapsed, step = 0.0, 0

    def add(duration, label, asset=None, effect=None, **changes):
        nonlocal elapsed, pose
        end = {**deepcopy(pose), **deepcopy(changes)}
        segments.append(
            {
                "start": round(elapsed, 6),
                "end": round(elapsed + duration, 6),
                "step": step,
                "label": label,
                "asset": asset,
                "effect": effect,
                "from": deepcopy(pose),
                "to": end,
            }
        )
        elapsed += duration
        pose = end

    def navigate(station):
        target = stations[station]
        for point in nav.path(pose["position"], target["dock_m"]):
            delta = [point[i] - pose["position"][i] for i in range(3)]
            distance = math.dist(point, pose["position"])
            if distance < 1e-6:
                continue
            yaw = math.degrees(math.atan2(-delta[0], delta[1]))
            add(0.4, "转向 · " + target["name"], "robot_01", yaw=yaw)
            add(distance / 0.75, "前往" + target["name"], "robot_01", position=point)
        add(0.5, "停靠 · " + target["name"], "robot_01", yaw=target["yaw_deg"])

    def reach(station, label, asset):
        point = stations[station]["sample_position_m"]
        add(0.15, label, asset, target=[point[0], point[1], point[2] + 0.17])
        add(1.0, label, asset, extension=1)

    def gesture(label, station, asset):
        reach(station, label, asset)
        add(0.8, label, asset, effect="operation")
        add(1.0, "收臂", asset, extension=0)

    add(1.2, "准备开始 · 小车待命", "robot_01")
    for step, action in enumerate(demo["actions"], 1):
        starts.append(round(elapsed, 6))
        operation = action["operation"]
        if operation in {"add_solvent", "add_reagent", "add_catalyst"}:
            if step == 1:
                navigate("preparation")
            label = {
                "add_solvent": "加入溶剂 · 配液动作示意",
                "add_reagent": "加入反应物 · 配液动作示意",
                "add_catalyst": "加入催化剂 · 配液动作示意",
            }[operation]
            gesture(label, "preparation", "bench_preparation")
        elif operation == "heat":
            navigate("reaction")
            gesture("启动反应 · 操作示意", "reaction", "reactor_01")
            add(
                5,
                f"加热与搅拌 · 模拟 {action['duration_s']:g} 秒压缩为 5 秒",
                "reactor_01",
                effect="heat",
            )
        elif operation == "sample":
            reach("reaction", "取样 · 反应区交接动作示意", "reactor_01")
            add(0.7, "封闭样品管就位 · 动作示意", "sample_tube_01", sampleVisible=True)
            add(1, "收臂 · 等待转运", "sample_tube_01", extension=0)
        elif operation == "measure" and action["instrument"] == "uvvis":
            reach("reaction", "伸臂 · 抓取样品管", "sample_tube_01")
            add(0.35, "夹爪闭合", "sample_tube_01", gripperOpen=False, holder="robot_01")
            add(1.0, "提起样品 · 收臂", "sample_tube_01", extension=0)
            navigate("analysis")
            reach("analysis", "伸臂 · 放置到表征台", "sample_tube_01")
            add(
                0.35,
                "松开夹爪 · 样品已交接",
                "sample_tube_01",
                gripperOpen=True,
                holder="analysis",
                samplePosition=stations["analysis"]["sample_position_m"],
            )
            add(1.0, "收臂 · 等待仪器测量", "uvvis_01", extension=0)
            add(3.0, "UV–Vis 测量 · 样品留在交接位", "uvvis_01", effect="measure")
        elif operation == "terminate":
            navigate("reaction")
            gesture("终止反应 · 操作示意", "reaction", "reactor_01")
        elif operation == "measure" and action["instrument"] == "final_assay":
            add(2.0, "终点检测 · 仅展示报告，无对应仪器模型")
            navigate("home")
            add(1.0, "回放完成 · 小车归位，样品留在表征台")
        else:
            raise ValueError(f"No illustration defined for action {action}")
        ends.append(round(elapsed, 6))
    return {
        "source": "authored_illustration",
        "research_evidence": False,
        "description": "公开实验观测配合动作示意；并非历史机器人轨迹，样品管未绑定 Core 样本。",
        "actions": demo["actions"],
        "duration": round(elapsed, 6),
        "stepStarts": starts,
        "stepEnds": ends,
        "stations": stations,
        "segments": segments,
    }


def main():
    motion = build_motion()
    (ROOT / "static/replay-motion.json").write_text(
        json.dumps(motion, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    print(
        f"Authored {len(motion['segments'])} motion segments; "
        f"{motion['duration']:.1f}s; no Core calls"
    )


if __name__ == "__main__":
    main()
