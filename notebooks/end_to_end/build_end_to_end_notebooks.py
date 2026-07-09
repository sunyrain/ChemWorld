# ruff: noqa: E501, RUF001
"""Build the three public end-to-end ChemWorld notebooks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

METADATA = {
    "kernelspec": {
        "display_name": "Python (ChemWorld)",
        "language": "python",
        "name": "chemworld",
    },
    "language_info": {
        "name": "python",
        "pygments_lexer": "ipython3",
    },
}


def md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def write_notebook(filename: str, cells: list[dict]) -> None:
    stem = Path(filename).stem.replace("_", "-")
    for index, cell in enumerate(cells, start=1):
        cell["id"] = f"{stem}-{index:02d}"
    payload = {
        "cells": cells,
        "metadata": METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (ROOT / filename).write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


COMMON_IMPORTS = """from __future__ import annotations

from pathlib import Path

import gymnasium as gym
import pandas as pd
from IPython.display import display

import chemworld  # noqa: F401 - registers ChemWorld

OUTPUT_DIR = Path("runs/end_to_end")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
pd.set_option("display.precision", 4)
"""


RUN_HELPER = """def run_recipe(task_id: str, recipe: list[dict], *, seed: int = 0) -> tuple[pd.DataFrame, dict]:
    env = gym.make("ChemWorld", task_id=task_id, seed=seed)
    _obs, info = env.reset(seed=seed)
    rows = []
    final_info = info
    try:
        for step, action in enumerate(recipe, start=1):
            validation = env.unwrapped.validate_action(action)
            _obs, reward, terminated, truncated, info = env.step(action)
            final_info = info
            rows.append(
                {
                    "step": step,
                    "operation": action["operation"],
                    "valid_before_step": validation["valid"],
                    "invalid_reasons": "; ".join(validation.get("invalid_reasons", [])),
                    "reward": float(reward),
                    "leaderboard_score": info.get("leaderboard_score"),
                    "precondition_failed": info.get("constraint_flags", {}).get("precondition_failed"),
                    "unsafe": info.get("constraint_flags", {}).get("unsafe"),
                    "cost": info.get("cost"),
                    "observed_keys": ", ".join(info.get("observed_keys", [])),
                    "has_raw_signal": bool(info.get("raw_signal")),
                    "terminated": terminated,
                    "truncated": truncated,
                }
            )
            if terminated or truncated:
                break
    finally:
        env.close()
    return pd.DataFrame(rows), final_info


def spectra_frame(final_info: dict, channel: str = "hplc") -> pd.DataFrame:
    packet = final_info.get("raw_signal", {})
    spectra = packet.get("spectra", {}) if isinstance(packet, dict) else {}
    signal = spectra.get(channel, {})
    if channel in {"hplc", "gc"}:
        return pd.DataFrame({"x": signal.get("time_min", []), "signal": signal.get("intensity", [])})
    if channel == "uvvis":
        return pd.DataFrame({"x": signal.get("wavelength_nm", []), "signal": signal.get("absorbance", [])})
    return pd.DataFrame()
"""


def build_reaction_to_assay() -> None:
    cells = [
        md(
            """# 端到端示例 1：Reaction-to-Assay

目标：从任务说明开始，规划一条合法反应实验，执行到 final assay，读取谱图和指标，并写出下一轮实验判断。

本 notebook 是完整流程模板，不是最高分策略。重点是可验证、可复现、可解释。"""
        ),
        md(
            """## 1. 任务规划

使用 `task_prompt()`、`available_actions()` 和 `action_schema()` 先读 public contract。不要直接猜 payload 字段名。"""
        ),
        code(
            COMMON_IMPORTS
            + """
env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
_obs, _info = env.reset(seed=0)
display(env.unwrapped.task_prompt())
display(pd.DataFrame(env.unwrapped.available_actions()).head(12))
display(env.unwrapped.action_schema("heat"))
env.close()
"""
        ),
        md(
            """## 2. 设计并验证 recipe

这条 recipe 先做中间 HPLC，再淬灭、终止并执行 final assay。"""
        ),
        code(
            """recipe = [
    {"operation": "add_solvent", "volume_L": 0.030, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.012},
    {"operation": "add_catalyst", "catalyst": 2, "catalyst_amount_mol": 0.0004},
    {"operation": "heat", "target_temperature_K": 350.0, "duration_s": 1200.0, "stirring_speed_rpm": 800.0},
    {"operation": "sample", "sample_volume_L": 0.0005},
    {"operation": "measure", "instrument": "hplc"},
    {"operation": "quench"},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]

validation_rows = []
env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
env.reset(seed=0)
for action in recipe:
    validation = env.unwrapped.validate_action(action)
    validation_rows.append({"operation": action["operation"], "valid": validation["valid"], "reasons": validation.get("invalid_reasons", [])})
    if validation["valid"]:
        _obs, _reward, terminated, truncated, _info = env.step(action)
        if terminated or truncated:
            break
env.close()
display(pd.DataFrame(validation_rows))
"""
        ),
        md(
            """## 3. 执行实验并保存轨迹表

`reward` 是在线观测分数；正式榜单看 final assay 的 `leaderboard_score`。"""
        ),
        code(
            RUN_HELPER
            + """
rows, final_info = run_recipe("reaction-to-assay", recipe, seed=0)
display(rows)
rows.to_csv(OUTPUT_DIR / "reaction_to_assay_trace.csv", index=False)
"""
        ),
        md(
            """## 4. 谱图与指标

final assay 返回多通道 packet。这里读取 HPLC 和 UV-vis，用于确认 processed metrics 是否有观测依据。"""
        ),
        code(
            """display(final_info.get("processed_estimate", {}))

hplc = spectra_frame(final_info, "hplc")
uvvis = spectra_frame(final_info, "uvvis")
if not hplc.empty:
    display(hplc.head())
    hplc.plot(x="x", y="signal", title="Final assay HPLC signal", xlabel="time / min")
if not uvvis.empty:
    uvvis.plot(x="x", y="signal", title="Final assay UV-vis signal", xlabel="wavelength / nm")
"""
        ),
        md(
            """## 5. 反思记录

请把下面字段填完整，再把 CSV、图和结论一起作为本次实验 artifact。"""
        ),
        code(
            """reflection = {
    "best_observed_step": rows.sort_values("reward", ascending=False).iloc[0].to_dict(),
    "chemical_hypothesis": "示例：当前温度产生了可测产物，但选择性仍有限，下一轮应比较更短反应时间。",
    "next_experiment": {"target_temperature_K": 340.0, "duration_s": 900.0, "reason": "降低副反应和风险"},
    "reproducibility_evidence": str(OUTPUT_DIR / "reaction_to_assay_trace.csv"),
}
reflection
"""
        ),
    ]
    write_notebook("reaction_to_assay_end_to_end.ipynb", cells)


def build_reaction_to_purification() -> None:
    cells = [
        md(
            """# 端到端示例 2：Reaction-to-Purification

目标：完成反应、建立相系统、萃取/分相、洗涤/干燥/浓缩，最后 final assay。

关键点：下游纯化不能在 `terminate` 之后进行；当前 schema 要先 `add_phase`，再 `add_extractant`。"""
        ),
        md(
            """## 1. 任务规划与动作空间

先检查 task contract，确认允许 separation operations。"""
        ),
        code(
            COMMON_IMPORTS
            + """
env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
_obs, _info = env.reset(seed=0)
display(env.unwrapped.task_prompt())
display(pd.DataFrame(env.unwrapped.available_actions()).head(16))
display(env.unwrapped.action_schema("add_extractant"))
display(env.unwrapped.action_schema("separate_phase"))
env.close()
"""
        ),
        md(
            """## 2. 合法 reaction-to-purification recipe

流程顺序：反应生成产物 -> 淬灭 -> 建立有机相 -> 萃取混合静置 -> 分相 -> 洗涤干燥浓缩 -> 终止 -> final assay。"""
        ),
        code(
            """recipe = [
    {"operation": "add_solvent", "volume_L": 0.030, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.012},
    {"operation": "add_catalyst", "catalyst": 2, "catalyst_amount_mol": 0.0004},
    {"operation": "heat", "target_temperature_K": 350.0, "duration_s": 1200.0, "stirring_speed_rpm": 800.0},
    {"operation": "quench"},
    {"operation": "add_phase", "phase": "organic", "volume_L": 0.020},
    {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.010},
    {"operation": "mix", "duration_s": 120.0, "stirring_speed_rpm": 600.0},
    {"operation": "settle", "duration_s": 300.0},
    {"operation": "separate_phase", "target_phase": "organic"},
    {"operation": "wash", "wash_volume_L": 0.010},
    {"operation": "dry"},
    {"operation": "concentrate", "duration_s": 300.0},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]
"""
        ),
        md(
            """## 3. 执行、验证和指标表

重点看 purification score、purity、recovery、process mass balance 和 precondition failure。"""
        ),
        code(
            RUN_HELPER
            + """
rows, final_info = run_recipe("reaction-to-purification", recipe, seed=0)
display(rows)
display(final_info.get("processed_estimate", {}))
rows.to_csv(OUTPUT_DIR / "reaction_to_purification_trace.csv", index=False)
assert not rows["precondition_failed"].any(), "recipe should be valid under current task contract"
"""
        ),
        md(
            """## 4. 谱图与纯化权衡

比较 HPLC 主峰、impurity signal、purity/recovery。高纯度但低 recovery 不是一定更好。"""
        ),
        code(
            """hplc = spectra_frame(final_info, "hplc")
if not hplc.empty:
    hplc.plot(x="x", y="signal", title="Purified final assay HPLC", xlabel="time / min")
metrics = final_info.get("processed_estimate", {})
tradeoff = pd.DataFrame([{
    "leaderboard_score": final_info.get("leaderboard_score"),
    "purity": metrics.get("purity"),
    "recovery": metrics.get("recovery"),
    "yield": metrics.get("yield"),
    "process_mass_balance_error": metrics.get("process_mass_balance_error"),
}])
display(tradeoff)
"""
        ),
        md(
            """## 5. 反思记录

请用化工语言解释：分相和浓缩提高了什么，牺牲了什么。"""
        ),
        code(
            """reflection = {
    "best_score": rows["leaderboard_score"].dropna().max(),
    "purification_hypothesis": "示例：有机相分离提高了可检测纯度，但 recovery 仍低，下一轮应比较相体积和 target_phase。",
    "next_experiment": {"add_phase_volume_L": 0.030, "target_phase": "organic", "reason": "提高分配和回收"},
    "evidence": str(OUTPUT_DIR / "reaction_to_purification_trace.csv"),
}
reflection
"""
        ),
    ]
    write_notebook("reaction_to_purification_end_to_end.ipynb", cells)


def build_partition_discovery() -> None:
    cells = [
        md(
            """# 端到端示例 3：Partition Discovery

目标：在 campaign task 中用多次实验学习分配趋势。每个 final assay 结束一个 experiment，但不结束整个 campaign。

重点：不要假设 hidden partition coefficient 可见；只能从公开仪器和 final assay 推断。"""
        ),
        md(
            """## 1. 任务规划

读取 campaign 状态、可用动作和任务提示。"""
        ),
        code(
            COMMON_IMPORTS
            + """
env = gym.make("ChemWorld", task_id="partition-discovery", seed=0)
_obs, _info = env.reset(seed=0)
display(env.unwrapped.task_prompt())
display(env.unwrapped.campaign_state())
display(pd.DataFrame(env.unwrapped.available_actions()).head(14))
env.close()
"""
        ),
        md(
            """## 2. 设计多轮 campaign recipes

这里比较两种 solvent 和两个 target phase。每轮 experiment 都要重新建立相系统。"""
        ),
        code(
            """experiment_recipes = [
    [
        {"operation": "add_solvent", "volume_L": 0.030, "solvent": 0},
        {"operation": "add_reagent", "amount_mol": 0.008},
        {"operation": "add_phase", "phase": "organic", "volume_L": 0.020},
        {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.010},
        {"operation": "mix", "duration_s": 120.0, "stirring_speed_rpm": 500.0},
        {"operation": "settle", "duration_s": 300.0},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ],
    [
        {"operation": "add_solvent", "volume_L": 0.030, "solvent": 3},
        {"operation": "add_reagent", "amount_mol": 0.008},
        {"operation": "add_phase", "phase": "organic", "volume_L": 0.020},
        {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.010},
        {"operation": "mix", "duration_s": 180.0, "stirring_speed_rpm": 600.0},
        {"operation": "settle", "duration_s": 300.0},
        {"operation": "separate_phase", "target_phase": "aqueous"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ],
]
"""
        ),
        md(
            """## 3. 执行 campaign 并提取每轮 final assay

在 campaign 模式下，`terminated` 通常不会在第一次 final assay 后变成 True；环境会准备下一轮 experiment。"""
        ),
        code(
            """env = gym.make("ChemWorld", task_id="partition-discovery", seed=0)
_obs, _info = env.reset(seed=0)
rows = []
final_packets = []
for experiment_index, recipe in enumerate(experiment_recipes):
    for action in recipe:
        validation = env.unwrapped.validate_action(action)
        _obs, reward, terminated, truncated, info = env.step(action)
        rows.append({
            "experiment": experiment_index,
            "operation": action["operation"],
            "valid_before_step": validation["valid"],
            "reward": float(reward),
            "leaderboard_score": info.get("leaderboard_score"),
            "precondition_failed": info.get("constraint_flags", {}).get("precondition_failed"),
            "phase_ratio": info.get("processed_estimate", {}).get("phase_ratio"),
            "product_in_organic": info.get("processed_estimate", {}).get("product_in_organic"),
            "product_in_aqueous": info.get("processed_estimate", {}).get("product_in_aqueous"),
            "terminated": terminated,
            "truncated": truncated,
        })
        if action["operation"] == "measure" and action.get("instrument") == "final_assay":
            final_packets.append({"experiment": experiment_index, "info": info})
        if terminated or truncated:
            break
    if terminated or truncated:
        break
df = pd.DataFrame(rows)
display(df)
display(env.unwrapped.campaign_state())
env.close()
df.to_csv(OUTPUT_DIR / "partition_discovery_campaign.csv", index=False)
"""
        ),
        md(
            """## 4. 谱图与分配趋势

比较每轮 final assay 的 processed estimates。若 raw spectra 与 processed estimate 冲突，应记录 warning，而不是强行解释。"""
        ),
        code(
            RUN_HELPER
            + """
summary_rows = []
for packet in final_packets:
    info = packet["info"]
    metrics = info.get("processed_estimate", {})
    summary_rows.append({
        "experiment": packet["experiment"],
        "leaderboard_score": info.get("leaderboard_score"),
        "phase_ratio": metrics.get("phase_ratio"),
        "product_in_organic": metrics.get("product_in_organic"),
        "product_in_aqueous": metrics.get("product_in_aqueous"),
        "has_spectra": bool(info.get("raw_signal", {}).get("spectra")),
    })
summary = pd.DataFrame(summary_rows)
display(summary)
if final_packets:
    hplc = spectra_frame(final_packets[0]["info"], "hplc")
    if not hplc.empty:
        hplc.plot(x="x", y="signal", title="Partition discovery final HPLC", xlabel="time / min")
"""
        ),
        md(
            """## 5. 反思记录

请写出你当前学到的局部分配模型，以及下一轮应该改哪个变量。"""
        ),
        code(
            """reflection = {
    "observed_pattern": summary.to_dict(orient="records"),
    "local_world_model": "示例：当前 public observations 只能支持相对分配趋势，不能直接给出 hidden partition coefficient。",
    "next_experiment": {"variable": "solvent / target_phase", "reason": "验证 organic 与 aqueous readout 的稳定差异"},
    "evidence": str(OUTPUT_DIR / "partition_discovery_campaign.csv"),
}
reflection
"""
        ),
    ]
    write_notebook("partition_discovery_end_to_end.ipynb", cells)


def write_readme() -> None:
    (ROOT / "README.md").write_text(
        """# ChemWorld 端到端 Notebook

这组 notebook 面向外部读者，展示从 task prompt 到执行、谱图、指标和反思的完整闭环。

| Notebook | 任务 | 覆盖内容 |
| --- | --- | --- |
| `reaction_to_assay_end_to_end.ipynb` | `reaction-to-assay` | 任务规划、HPLC 中间测量、final assay、谱图和下一轮实验 |
| `reaction_to_purification_end_to_end.ipynb` | `reaction-to-purification` | 反应、相系统、萃取、分相、洗涤、干燥、浓缩、final assay |
| `partition_discovery_end_to_end.ipynb` | `partition-discovery` | campaign 多轮实验、分配趋势、final assay packet 和局部 world model |

这些 notebooks 不是最高分策略，而是可验证流程模板。运行前请安装：

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
```
""",
        encoding="utf-8",
    )


def main() -> None:
    build_reaction_to_assay()
    build_reaction_to_purification()
    build_partition_discovery()
    write_readme()


if __name__ == "__main__":
    main()
