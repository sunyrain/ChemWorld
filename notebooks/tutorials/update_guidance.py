# ruff: noqa: E501, I001, RUF001

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

GUIDANCE = {
    ROOT / "notebooks/tutorials/day_01_enter_virtual_lab.ipynb": {
        "stage": "A. 进入世界",
        "difficulty": "入门 1/3",
        "prereq": "会打开 Jupyter，能运行一个 Python 单元。",
        "today": "第一次运行 ChemWorld，看懂 action、observation、reward、info 和 trajectory 的关系。",
        "not_today": "不追求最高分，也不要求理解完整反应机理。",
        "deliverables": "一条可回放轨迹、一张实验图、一个下一轮实验假设。",
        "next_use": "Day 2 会用这条轨迹检查 ontology、单位和 physical constitution。",
        "basic": "按给定 recipe 跑通一次 reaction-to-assay，保存轨迹并指出每一步的 operation。",
        "advanced": "修改一个温度或时间参数，比较 score、risk 和 final assay 的变化。",
        "challenge": "写出一个“为什么下一轮该这样改条件”的化工假设。",
        "reflection": "今天你看到的是隐藏真实状态，还是仪器返回的观测？这两者为什么不能混淆？",
    },
    ROOT / "notebooks/tutorials/day_02_ontology_and_constitution.ipynb": {
        "stage": "A. 进入世界",
        "difficulty": "入门 2/3",
        "prereq": "已能执行一次完整实验，并能找到 trajectory 中的 action 和 observation。",
        "today": "理解物质、相、容器、操作、单位和 physical constitution 如何约束世界。",
        "not_today": "不新增物理模型，也不手改 simulator 内部参数。",
        "deliverables": "一个非法动作、constitution/validator 给出的原因、修复后的合法动作。",
        "next_use": "Day 3 会在这些约束下选择仪器并解释观测成本。",
        "basic": "找出当前 task 允许的 operation 和 instrument。",
        "advanced": "构造一个前置条件失败的动作，并解释为什么失败是合理的。",
        "challenge": "把失败动作改写成一个合法 recipe，并说明每一步满足了什么前置条件。",
        "reflection": "如果没有物料守恒、非负性和动作前置条件，agent 会学到什么错误策略？",
    },
    ROOT / "notebooks/tutorials/day_03_observation_and_instruments.ipynb": {
        "stage": "A. 进入世界",
        "difficulty": "入门到进阶",
        "prereq": "理解 action 合法性和隐藏状态/公开观测的区别。",
        "today": "比较 HPLC、GC、UV-vis、FinalAssay 的信息量、噪声、成本和样品消耗。",
        "not_today": "不把一次测量当作无噪声真值，也不默认所有仪器都可用。",
        "deliverables": "仪器比较表、一张 raw signal 或谱图、一段测量策略说明。",
        "next_use": "Day 4 会用观测数据扫描机理趋势。",
        "basic": "运行至少两种仪器测量，比较它们的 processed_estimate 和 uncertainty。",
        "advanced": "解释为什么 FinalAssay 适合评分，UV-vis 更适合快速探索。",
        "challenge": "设计一个低成本观测策略：先粗筛，再用高质量仪器确认。",
        "reflection": "如果仪器有成本和噪声，什么时候“少测一次”反而是好策略？",
    },
    ROOT / "notebooks/tutorials/day_04_mechanism_scans.ipynb": {
        "stage": "B. 认识规律",
        "difficulty": "进阶 1/3",
        "prereq": "能运行实验并解释仪器观测字段。",
        "today": "用温度、时间、催化剂、溶剂和浓度扫描建立第一版机制直觉。",
        "not_today": "不要求得到全局最优，只要求能发现趋势和 trade-off。",
        "deliverables": "至少一张机制扫描图、一个安全-性能权衡解释、下一轮实验建议。",
        "next_use": "Day 5 会把这些扫描数据变成 surrogate model 的训练样本。",
        "basic": "扫描单个变量并画出 score/risk 随变量变化的图。",
        "advanced": "比较两个变量或两个离散选择的交互效应。",
        "challenge": "指出一个“产率更高但不一定更好”的条件，并给出化工原因。",
        "reflection": "哪些结果支持主反应加快？哪些结果暗示副反应、降解或安全风险也在增加？",
    },
    ROOT / "notebooks/tutorials/day_05_surrogate_modeling.ipynb": {
        "stage": "B. 认识规律",
        "difficulty": "进阶 2/3",
        "prereq": "已有若干实验轨迹或扫描表，能把 action 转成特征。",
        "today": "从有限数据训练局部 surrogate，理解预测误差、不确定性和外推风险。",
        "not_today": "不把 surrogate 当真实机理模型，也不要求覆盖所有 hidden world。",
        "deliverables": "一个局部预测模型、误差/残差分析、候选实验排序。",
        "next_use": "Day 6 会把你的模型表现放进 baseline/leaderboard 对比。",
        "basic": "训练一个简单模型并报告验证误差。",
        "advanced": "找出模型最不确定或误差最大的区域。",
        "challenge": "提出一个兼顾 exploitation 和 exploration 的下一轮实验。",
        "reflection": "局部 world model 能解释什么？它在哪些区域最可能失效？",
    },
    ROOT / "notebooks/tutorials/day_06_baselines_and_leaderboard.ipynb": {
        "stage": "B. 认识规律",
        "difficulty": "进阶 3/3",
        "prereq": "知道 score、risk、sample efficiency 和 trajectory 的含义。",
        "today": "比较 random、LHS、scripted、BO、safe BO 等 baseline 的决策效率。",
        "not_today": "不把 leaderboard 当唯一目标，也不只看最终最高分。",
        "deliverables": "baseline 对比表、best-score 曲线、安全成本解释。",
        "next_use": "Day 7 会把你选定的策略整理成可复现 submission artifact。",
        "basic": "运行至少两个 baseline 并比较最终 score。",
        "advanced": "比较 area-under-best-score、invalid action 和 safety cost。",
        "challenge": "解释为什么某个策略在 public world 强，但可能泛化差。",
        "reflection": "一个好 benchmark 为什么要同时看性能、样本效率、安全和复现性？",
    },
    ROOT / "notebooks/tutorials/day_07_capstone_artifact.ipynb": {
        "stage": "C. 形成项目",
        "difficulty": "进阶到挑战",
        "prereq": "已能运行 baseline，理解 trajectory、manifest、results 的作用。",
        "today": "把前六天的实验、模型、策略和解释整理成可复现小项目。",
        "not_today": "不要求 private-eval，也不要求最终模型最强。",
        "deliverables": "小型 submission bundle：manifest、trajectory、results、explanation。",
        "next_use": "Day 8 会把 GPT-style planner 纳入同一套验证流程。",
        "basic": "生成并验证一份最小提交包。",
        "advanced": "补充策略说明和机制解释，使别人能复现实验。",
        "challenge": "把失败案例也写进 failure analysis，而不是只保留成功结果。",
        "reflection": "如果别人拿到你的提交包，能否不问你就复现实验结论？",
    },
    ROOT / "notebooks/tutorials/day_08_gpt_planner_and_validation.ipynb": {
        "stage": "C. 形成项目",
        "difficulty": "挑战 1/4",
        "prereq": "理解 operation schema、task policy 和前置条件。",
        "today": "把 GPT-style proposal 转成可验证、可修复、可执行的实验 recipe。",
        "not_today": "不依赖在线 GPT API；重点是 planner 输出必须受 schema 和 validator 约束。",
        "deliverables": "原始 plan、validator 反馈、修复后的 action sequence。",
        "next_use": "Day 9 会把自动规划与 BO/safe BO 的闭环选点连接起来。",
        "basic": "验证一个 GPT-style action，读懂 invalid reason。",
        "advanced": "修复一个非法 recipe，使其能在环境中执行。",
        "challenge": "设计一个 tool-using planner 流程：先查询 task_info，再 validate，再执行。",
        "reflection": "LLM 生成的“看起来合理”的实验，为什么仍必须经过 validator？",
    },
    ROOT / "notebooks/tutorials/day_09_bayesian_optimization.ipynb": {
        "stage": "C. 形成项目",
        "difficulty": "挑战 2/4",
        "prereq": "已了解 surrogate 和 baseline 指标。",
        "today": "理解 BO/safe BO 如何在 campaign 中利用历史实验推荐下一条 recipe。",
        "not_today": "不要求推导完整 GP 公式，重点是闭环决策和安全约束。",
        "deliverables": "BO 初始点、acquisition 阶段、best-score 与 safety-cost 曲线。",
        "next_use": "Day 10 会把策略作为 public leaderboard submission 运行。",
        "basic": "运行 BO 并确认它进入 acquisition 阶段。",
        "advanced": "比较普通 BO 与 safe BO 的分数和风险。",
        "challenge": "找一个 BO 可能被误导的区域，并提出改进采样策略。",
        "reflection": "有限预算下，探索未知区域和利用已知高分区域如何取舍？",
    },
    ROOT / "notebooks/tutorials/day_10_public_leaderboard_challenge.ipynb": {
        "stage": "D. 接近科研评测",
        "difficulty": "挑战 3/4",
        "prereq": "能生成提交包并理解 task-specific metrics。",
        "today": "在 public-test 上组织一次标准提交，体验本地 leaderboard 流程。",
        "not_today": "不鼓励人工刷榜；策略必须可解释、可复现。",
        "deliverables": "public-test 结果 JSON、验证日志、策略摘要。",
        "next_use": "Day 11 会用 private-like split 诊断泛化差距。",
        "basic": "运行一个 agent 的 public submission 并通过验证。",
        "advanced": "比较至少两个 agent 的 public leaderboard row。",
        "challenge": "指出一个可能过拟合 public world 的策略特征。",
        "reflection": "公开榜分数高，为什么不等于科研结论可靠？",
    },
    ROOT / "notebooks/tutorials/day_11_private_generalization.ipynb": {
        "stage": "D. 接近科研评测",
        "difficulty": "挑战 4/4",
        "prereq": "已理解 public-test 提交流程。",
        "today": "诊断 public/private gap，区分稳健策略和公开世界过拟合。",
        "not_today": "不尝试反推 hidden parameters，也不把 private split 当训练集。",
        "deliverables": "泛化差距表、失败模式分析、下一版策略修正。",
        "next_use": "Day 12 会把泛化、机理、复现性整合进最终展示。",
        "basic": "比较同一策略在两个 split 上的表现差异。",
        "advanced": "把差异拆成 performance、safety、sample efficiency 和 invalid action。",
        "challenge": "提出一个更稳健的探索策略并说明它如何降低 gap。",
        "reflection": "一个策略在 hidden world 上变差，可能是机理误判、采样不足，还是过拟合？",
    },
    ROOT / "notebooks/tutorials/day_12_demo_day_artifact.ipynb": {
        "stage": "D. 接近科研评测",
        "difficulty": "综合挑战",
        "prereq": "已有 public/private 结果、轨迹、解释和验证日志。",
        "today": "形成最终展示：性能、机理、安全、泛化和复现性并重。",
        "not_today": "不做营销式展示；每个结论都要有实验或日志证据。",
        "deliverables": "Demo Day 报告骨架、项目摘要、关键图表和可复现证据。",
        "next_use": "Day 13 会把同一套世界规律扩展到更多化工过程。",
        "basic": "整理一页项目摘要和关键结果表。",
        "advanced": "把机制解释、失败分析和下一步实验写成连贯故事。",
        "challenge": "设计一个对外评审也能复现的 paper artifact 清单。",
        "reflection": "你的结果最可信的证据是什么？最大的不确定性又是什么？",
    },
    ROOT / "notebooks/tutorials/day_13_year2_process_modules.ipynb": {
        "stage": "E. 研究延展",
        "difficulty": "研究延展",
        "prereq": "理解统一 world law、task slice 和 reaction-to-purification。",
        "today": "观察结晶、蒸馏、连续流、电化学如何作为同一世界下的过程模块扩展。",
        "not_today": "不宣称这些模块已经达到专业过程模拟器精度。",
        "deliverables": "一个跨过程 task 的最小闭环、一个需要新增的物理账本、一个后续开发计划。",
        "next_use": "这些产出会进入专业级 TODO 和后续环境设计。",
        "basic": "运行一个 Year 2 task 并记录新增观测字段。",
        "advanced": "比较不同过程模块的 score、risk、cost 和 mass-balance 字段。",
        "challenge": "为其中一个模块写出下一步要实现的专业物理模型清单。",
        "reflection": "为什么这些过程不应该做成独立小游戏，而应共享同一套 WorldLaw？",
    },
    ROOT / "notebooks/tutorials/project_leaderboard_blueprint.ipynb": {
        "stage": "E. 项目组织",
        "difficulty": "课程/项目设计",
        "prereq": "已经理解 submission bundle、local eval machine 和 leaderboard 指标。",
        "today": "设计本机教师端/学生端评测组织方式，明确如何提交、验证和排名。",
        "not_today": "不搭云端账号系统，也不把 leaderboard 变成唯一评分标准。",
        "deliverables": "评测机目录结构、榜单指标、项目 track、提交协议。",
        "next_use": "可直接作为课程项目说明或实验室内部 challenge 草案。",
        "basic": "画出教师端、学生端和 shared specs 的文件流。",
        "advanced": "设计 performance、sample efficiency、safety、explanation 多榜。",
        "challenge": "写出防止重复劳动和过拟合刷榜的项目管理规则。",
        "reflection": "怎样让 leaderboard 鼓励科学探索，而不只是鼓励刷最高分？",
    },
    ROOT / "notebooks/full_workflow_demo.ipynb": {
        "stage": "全流程演示",
        "difficulty": "综合入门",
        "prereq": "已安装 ChemWorld 并选择 Python (ChemWorld) 内核。",
        "today": "快速浏览环境检查、事件序列、trajectory、评测、verify、suite 和 LLM replay 接入。",
        "not_today": "不替代 Day 1-12 的逐步练习；它是总览，不是课程作业。",
        "deliverables": "一份端到端运行结果、一条可验证轨迹、一个 baseline/leaderboard 结果。",
        "next_use": "读完后回到 Day 1，从最小实验开始逐天加深。",
        "basic": "顺序运行 notebook，确认环境和评测链路都能工作。",
        "advanced": "定位每个输出对应到哪个 CLI 或 public API。",
        "challenge": "把其中一个步骤改成自己的 task 或 agent。",
        "reflection": "这个全流程里，哪些步骤属于实验执行，哪些属于评测和复现？",
    },
    ROOT / "notebooks/physics_sanity_check.ipynb": {
        "stage": "物理合理性检查",
        "difficulty": "进阶验证",
        "prereq": "理解 reactor task 中的温度、时间、浓度、催化剂和溶剂字段。",
        "today": "用扫描验证模型是否满足基本化工直觉：升温加速、过长降解、浓度提高风险。",
        "not_today": "不把 sanity check 当真实体系校准。",
        "deliverables": "四组扫描图、定性断言结果、一段模型局限说明。",
        "next_use": "把这些检查结果作为后续物理内核重构的回归证据。",
        "basic": "运行所有扫描并确认断言通过。",
        "advanced": "解释每张图对应的反应或风险机制。",
        "challenge": "提出一个目前 sanity check 没覆盖但应该加入的物理规律。",
        "reflection": "一个虚拟环境通过 sanity check，和它能预测真实实验之间差了什么？",
    },
}


def _markdown_cell(text: str) -> dict:
    if not text.endswith("\n"):
        text += "\n"
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def _text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def _is_existing_guidance(cell: dict) -> bool:
    if cell.get("cell_type") != "markdown":
        return False
    text = _text(cell).lstrip()
    return (
        text.startswith("## 学习路径定位")
        or text.startswith("## 本日任务梯度")
        or (text.startswith("## ??????") and "| ?? | ?? |" in text)
    )


def _path_cell(meta: dict[str, str]) -> dict:
    return _markdown_cell(
        f"""## 学习路径定位

| 项目 | 内容 |
| --- | --- |
| 阶段 | {meta["stage"]} |
| 难度 | {meta["difficulty"]} |
| 先修 | {meta["prereq"]} |
| 今天只解决 | {meta["today"]} |
| 今天不要求 | {meta["not_today"]} |
| 本日交付 | {meta["deliverables"]} |
| 下一步如何复用 | {meta["next_use"]} |

"""
    )


def _ladder_cell(meta: dict[str, str]) -> dict:
    return _markdown_cell(
        f"""## 本日任务梯度

| 层级 | 任务 |
| --- | --- |
| 基础任务 | {meta["basic"]} |
| 进阶任务 | {meta["advanced"]} |
| 挑战任务 | {meta["challenge"]} |
| 反思问题 | {meta["reflection"]} |

"""
    )


def update_notebook(path: Path, meta: dict[str, str]) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = [cell for cell in notebook["cells"] if not _is_existing_guidance(cell)]
    cells.insert(1 if cells else 0, _path_cell(meta))

    target = None
    for index, cell in enumerate(cells):
        text = _text(cell).lstrip()
        if text.startswith("## 准备工作") or text.startswith("## 学习目标"):
            target = index + 1
            break
    if target is None:
        for index, cell in enumerate(cells):
            if "课堂时间盒" in _text(cell):
                target = index + 1
                break
    if target is None:
        target = min(2, len(cells))
    cells.insert(target, _ladder_cell(meta))

    notebook["cells"] = cells
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> None:
    for path, meta in GUIDANCE.items():
        update_notebook(path, meta)


if __name__ == "__main__":
    main()
