# ruff: noqa: E501, RUF001
"""Refresh 30-minute teaching timeboxes in tutorial notebooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


TIMEBOXES: dict[str, tuple[tuple[str, str, str, str], ...]] = {
    "day_01_enter_virtual_lab.ipynb": (
        ("0:00-0:30", "确认环境入口", "运行导入单元，检查 kernel、项目根目录和输出目录。", "能解释 `gym.make(\"ChemWorld\")` 返回什么。"),
        ("0:30-1:00", "读懂事件动作", "逐条阅读 add/heat/terminate/measure 的操作含义。", "写下一个完整实验 recipe。"),
        ("1:00-1:30", "执行第一条实验", "运行手工事件序列，观察 reward、terminated、info。", "得到第一张轨迹表。"),
        ("1:30-2:00", "保存可复现证据", "导出 JSONL，定位 action、observation、raw_signal 字段。", "留下可回放轨迹文件。"),
        ("2:00-2:30", "画第一张图", "从轨迹中选择 score、risk 或 cost 生成图。", "得到一张能解释的实验图。"),
        ("2:30-3:00", "形成下一轮假设", "根据结果写机制假设和下一轮实验建议。", "提交 3 句话反思。"),
    ),
    "day_02_ontology_and_constitution.ipynb": (
        ("0:00-0:30", "定位世界对象", "查看 substance、phase、vessel、instrument、operation。", "画出 ChemWorld 的对象清单。"),
        ("0:30-1:00", "理解单位和账本", "检查单位、体积、温度、成本、风险和样品消耗。", "能说明每个 ledger 字段的含义。"),
        ("1:00-1:30", "触发前置条件", "故意提交一个非法动作并读取 invalid reasons。", "记录一个失败动作和失败原因。"),
        ("1:30-2:00", "修复非法动作", "用 validator 修改 payload 或操作顺序。", "得到合法动作版本。"),
        ("2:00-2:30", "检查物理宪法", "阅读 constitution checks，区分守恒、非负性和安全边界。", "写出 3 条可执行物理约束。"),
        ("2:30-3:00", "连接到 task", "比较不同 task 的 allowed operations 和 instruments。", "说明 task 是世界切片而不是新游戏。"),
    ),
    "day_03_observation_and_instruments.ipynb": (
        ("0:00-0:30", "区分真值和观测", "查看 observed_mask、observed_keys 和缺失值。", "解释为什么 agent 不能看 hidden state。"),
        ("0:30-1:00", "比较仪器合同", "阅读 HPLC、GC、UV-vis、final assay 的成本和噪声。", "完成仪器信息量对比表。"),
        ("1:00-1:30", "运行低成本测量", "使用 UV-vis 或 HPLC 获取部分观测。", "得到一条带成本的观测记录。"),
        ("1:30-2:00", "解析虚拟谱图", "读取 raw_signal 中的色谱或光谱坐标轴。", "画出一张 HPLC/UV-vis 信号图。"),
        ("2:00-2:30", "设计测量策略", "讨论什么时候值得做 final assay。", "写一个仪器选择策略。"),
        ("2:30-3:00", "总结非全知性", "比较 processed_estimate、uncertainty 和 raw_signal。", "形成观测核说明卡。"),
    ),
    "day_04_mechanism_scans.ipynb": (
        ("0:00-0:30", "建立扫描变量", "固定 seed，只改变温度、时间或催化剂。", "得到单因素扫描表。"),
        ("0:30-1:00", "温度扫描", "运行温度梯度并观察 conversion、risk、degradation。", "画温度-性能曲线。"),
        ("1:00-1:30", "时间扫描", "比较短时、中时、长时反应。", "指出过短和过长的失败模式。"),
        ("1:30-2:00", "催化剂/溶剂交互", "运行组合扫描或读取已有结果。", "找到一个交互证据。"),
        ("2:00-2:30", "安全约束分析", "把 score 与 safety_risk 放在一起比较。", "提出安全边界。"),
        ("2:30-3:00", "机制解释", "把扫描结果整理成反应-副反应-降解叙事。", "写下一轮实验条件。"),
    ),
    "day_05_surrogate_modeling.ipynb": (
        ("0:00-0:30", "整理训练数据", "从轨迹中抽取 temperature、time、solvent、catalyst 等特征。", "得到特征表。"),
        ("0:30-1:00", "训练基线模型", "拟合一个简单 surrogate model。", "记录训练误差或交叉验证误差。"),
        ("1:00-1:30", "检查残差", "找出预测偏差最大的实验。", "解释一个模型失败点。"),
        ("1:30-2:00", "候选点预测", "生成候选条件并预测 score/risk。", "得到候选排序表。"),
        ("2:00-2:30", "考虑不确定性", "标记外推点、稀疏区域或高风险候选。", "保留 2-3 个可信候选。"),
        ("2:30-3:00", "推荐下一轮实验", "用化工理由筛选最终候选。", "写出推荐条件和模型局限。"),
    ),
    "day_06_baselines_and_leaderboard.ipynb": (
        ("0:00-0:30", "理解评测合同", "查看 task、budget、seeds、metrics。", "说明为什么不能只看一次最高分。"),
        ("0:30-1:00", "运行 random/scripted", "执行快速 baseline 并读取结果。", "得到第一张 baseline 表。"),
        ("1:00-1:30", "运行 LHS/greedy", "比较系统探索和局部搜索。", "指出两者优缺点。"),
        ("1:30-2:00", "理解 BO 预算", "检查 campaign、final assay count 和 acquisition 阶段。", "确认 BO 是否真正闭环。"),
        ("2:00-2:30", "聚合 leaderboard", "按 task 输出 performance、safety、sample efficiency。", "得到榜单摘要。"),
        ("2:30-3:00", "写评测结论", "解释哪个 baseline 强、哪个风险高、哪里还不公平。", "形成评测备注。"),
    ),
    "day_07_capstone_artifact.ipynb": (
        ("0:00-0:30", "选择最佳策略", "回顾前 6 天结果，确定一个候选 recipe 或 agent。", "写出策略说明。"),
        ("0:30-1:00", "复现实验运行", "固定 seed 重新运行策略。", "得到复现轨迹。"),
        ("1:00-1:30", "验证轨迹", "运行 verify 或检查 replay 字段。", "确认可回放。"),
        ("1:30-2:00", "评估指标", "计算 score、risk、cost、sample efficiency。", "得到评价 JSON。"),
        ("2:00-2:30", "机制解释", "写温度、时间、副反应、安全的证据链。", "得到 explanation 草稿。"),
        ("2:30-3:00", "打包 artifact", "整理 trajectory、manifest、results、explanation。", "形成小型提交包。"),
    ),
    "day_08_gpt_planner_and_validation.ipynb": (
        ("0:00-0:30", "把 GPT 当 planner", "把自然语言计划改写成结构化 action。", "得到候选动作列表。"),
        ("0:30-1:00", "schema 检查", "运行 validate_action_schema 或 validate_recipe。", "找出格式错误。"),
        ("1:00-1:30", "物理前置检查", "用 validator 检查状态依赖和 task policy。", "找出不可执行动作。"),
        ("1:30-2:00", "修复计划", "修改操作顺序、payload 或 instrument。", "得到可执行 recipe。"),
        ("2:00-2:30", "执行并记录", "运行修复后的计划。", "保存轨迹和失败/成功说明。"),
        ("2:30-3:00", "反思 LLM 使用", "区分 GPT 的提议能力和验证器的约束能力。", "写一条 agent 设计原则。"),
    ),
    "day_09_bayesian_optimization.ipynb": (
        ("0:00-0:30", "定义 recipe 空间", "确认温度、时间、浓度、催化剂、溶剂等搜索变量。", "得到参数边界表。"),
        ("0:30-1:00", "初始设计", "运行少量随机/LHS 初始实验。", "得到初始观测点。"),
        ("1:00-1:30", "训练 GP/RF surrogate", "拟合模型并检查预测。", "得到 surrogate 状态。"),
        ("1:30-2:00", "acquisition 选择", "计算或读取下一轮候选。", "说明为什么选这个点。"),
        ("2:00-2:30", "安全 BO 对比", "比较普通 BO 与 safe BO 的风险。", "得到风险差异表。"),
        ("2:30-3:00", "收敛分析", "画 best-score 曲线和 final assay count。", "写 sample efficiency 结论。"),
    ),
    "day_10_public_leaderboard_challenge.ipynb": (
        ("0:00-0:30", "明确 public-test 规则", "读取 task card、allowed operations、seeds。", "写出提交约束。"),
        ("0:30-1:00", "生成提交轨迹", "运行选定 agent 或 recipe。", "得到 JSONL。"),
        ("1:00-1:30", "本地验证", "运行 validate 和 verify。", "修复所有格式/回放问题。"),
        ("1:30-2:00", "计算 public 指标", "运行 evaluate 并查看 leaderboard score。", "得到结果 JSON。"),
        ("2:00-2:30", "准备 manifest", "记录 agent、依赖、命令、seed。", "得到提交 manifest。"),
        ("2:30-3:00", "提交说明", "写清策略、风险控制、失败模式。", "形成 public submission 说明。"),
    ),
    "day_11_private_generalization.ipynb": (
        ("0:00-0:30", "区分 public/private", "读取 split 设计和 hidden salt 思路。", "说明什么是过拟合。"),
        ("0:30-1:00", "运行 public-test", "用固定策略获得 public 结果。", "得到 public 指标。"),
        ("1:00-1:30", "运行 private-eval", "在隐藏参数 split 上重跑。", "得到 private 指标。"),
        ("1:30-2:00", "计算 gap", "比较均值、方差和 public-private gap。", "得到泛化表。"),
        ("2:00-2:30", "诊断失败原因", "判断是安全、成本、机制还是搜索空间过拟合。", "写失败诊断。"),
        ("2:30-3:00", "改进策略", "提出更稳健的探索或安全约束。", "得到下一版计划。"),
    ),
    "day_12_demo_day_artifact.ipynb": (
        ("0:00-0:30", "整理故事线", "确定问题、策略、证据、结果、局限。", "形成展示大纲。"),
        ("0:30-1:00", "复查数据链", "确认 trajectory、results、figures、explanation 都存在。", "补齐缺失文件。"),
        ("1:00-1:30", "制作性能页", "展示 score、risk、cost、efficiency。", "得到性能图表。"),
        ("1:30-2:00", "制作机制页", "展示扫描、谱图或 surrogate 证据。", "得到机制解释页。"),
        ("2:00-2:30", "制作可复现页", "展示命令、manifest、verify 结果。", "得到复现说明。"),
        ("2:30-3:00", "演示排练", "用 3 分钟讲完科学闭环。", "形成最终 demo script。"),
    ),
    "day_13_year2_process_modules.ipynb": (
        ("0:00-0:30", "查看扩展模块", "读取 WorldLawSpec 中的结晶、蒸馏、连续流、电化学模块。", "确认它们共享同一 world law。"),
        ("0:30-1:00", "运行结晶任务", "执行 scripted task 并读取 crystal 指标。", "解释纯度/收率权衡。"),
        ("1:00-1:30", "运行蒸馏任务", "执行蒸馏 task 并读取 distillate 指标。", "解释能耗/回收权衡。"),
        ("1:30-2:00", "运行连续流/电化学", "比较 flow_conversion、selectivity、energy_efficiency。", "得到跨过程对比表。"),
        ("2:00-2:30", "检查前置条件", "用 validator 暴露状态依赖动作。", "说明为什么不是小游戏拼接。"),
        ("2:30-3:00", "设计新 task", "基于共享操作语言提出一个跨过程 task。", "写出 task card 草案。"),
    ),
    "project_leaderboard_blueprint.ipynb": (
        ("0:00-0:30", "确定课程赛道", "选择 reaction、purification、generalization 或 tool-agent 赛道。", "得到赛道清单。"),
        ("0:30-1:00", "定义评分指标", "设置 performance、safety、efficiency、explanation 权重。", "得到 rubric 表。"),
        ("1:00-1:30", "设计提交包", "明确 manifest、trajectory、results、explanation。", "得到 submission spec。"),
        ("1:30-2:00", "组织教师端", "规划 inbox、validate、verify、evaluate、leaderboard 流程。", "得到评测机流程图。"),
        ("2:00-2:30", "组织学生端", "设计 sandbox、public task cards、schema 和示例。", "得到学生端工作说明。"),
        ("2:30-3:00", "发布项目说明", "把赛道、时间线、评分和诚信规则写成项目 brief。", "得到可发给学生的项目说明。"),
    ),
}


def markdown_cell(source: str, cell_id: str) -> dict[str, Any]:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": [line + "\n" for line in source.splitlines()],
    }


def make_timebox_source(rows: tuple[tuple[str, str, str, str], ...]) -> str:
    lines = [
        "## 课堂时间盒：每 30 分钟都有产出",
        "",
        "建议按 3 小时工作坊使用。每一段都要留下一个小证据，不要只运行代码看到结果就继续往下翻。",
        "",
        "| 时间 | 阶段目标 | 具体动作 | 当段产出 |",
        "| --- | --- | --- | --- |",
    ]
    for time_range, goal, action, output in rows:
        lines.append(f"| {time_range} | {goal} | {action} | {output} |")
    lines.extend(
        [
            "",
            "教师提示：如果课堂时间少于 3 小时，可以把最后两个时间盒改成课后提交；但前四个时间盒建议现场完成。",
        ]
    )
    return "\n".join(lines)


def refresh_notebook(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = [
        cell
        for cell in nb["cells"]
        if not (
            cell.get("cell_type") == "markdown"
            and "".join(cell.get("source", [])).startswith("## 课堂时间盒：每 30 分钟都有产出")
        )
    ]
    rows = TIMEBOXES[path.name]
    cell = markdown_cell(make_timebox_source(rows), f"timebox-{path.stem}")
    insert_at = 1 if cells and cells[0].get("cell_type") == "markdown" else 0
    cells.insert(insert_at, cell)
    nb["cells"] = cells
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> None:
    for filename in TIMEBOXES:
        refresh_notebook(ROOT / filename)


if __name__ == "__main__":
    main()
