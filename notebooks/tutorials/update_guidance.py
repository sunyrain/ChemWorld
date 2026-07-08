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

WORK_ORDERS = {
    "day_01_enter_virtual_lab.ipynb": (
        "至少新增 6 条不同 recipe，覆盖 2 个温度、2 个时间和 2 个溶剂/催化剂选择。",
        "把每条实验的 action、observation、reward、risk、cost 保存成一张表。",
        "至少画 2 张图：score/risk 随条件变化图，以及最终 best experiment 摘要图。",
        "写 300 字实验日志：你认为哪一步最影响结果，下一轮为什么这样改。",
    ),
    "day_02_ontology_and_constitution.ipynb": (
        "至少构造 4 个非法动作：缺少前置物料、非法仪器、越界温度/体积、错误操作顺序。",
        "把每个非法动作的 validator/constitution 原因记录成表。",
        "把其中 2 个非法动作修复为合法 recipe，并证明修复后可执行。",
        "写 300 字解释：这些约束对应哪些真实化工安全或物料账本问题。",
    ),
    "day_03_observation_and_instruments.ipynb": (
        "至少比较 HPLC、GC、UV-vis、FinalAssay 中 3 类仪器；每类至少做 3 次重复测量。",
        "计算每类仪器的平均成本、平均 uncertainty、样品消耗和可观测字段数量。",
        "至少画 2 张 raw signal/processed estimate 图，解释噪声如何影响判断。",
        "设计一个低成本测量策略：先筛选，再确认，并说明何时升级到 FinalAssay。",
    ),
    "day_04_mechanism_scans.ipynb": (
        "至少完成 20 个扫描实验：温度 5 点、时间 5 点、浓度 4 点、催化剂/溶剂组合至少 6 点。",
        "画出 score、yield、selectivity、risk 至少 4 个指标的趋势图。",
        "找出一个高产率但低综合 score 的条件，并解释 trade-off。",
        "写出 3 条机制假设，并为每条假设设计下一轮验证实验。",
    ),
    "day_05_surrogate_modeling.ipynb": (
        "至少使用 30 条实验样本；如果数据不足，先补做实验再建模。",
        "训练至少 2 个模型或 2 组特征方案，并比较验证误差。",
        "列出模型最不确定的 5 个候选条件和最可能高分的 5 个候选条件。",
        "写 400 字模型局限：哪些区域是外推，哪些结论只能当局部 world model。",
    ),
    "day_06_baselines_and_leaderboard.ipynb": (
        "至少运行 5 类策略：random、LHS、scripted、BO、safe BO；每类至少 3 个 seed。",
        "输出 performance、sample efficiency、safety cost、invalid action count 四类指标。",
        "画 best-score 曲线和 safety-cost 曲线，解释两条曲线是否一致。",
        "写 400 字 baseline 诊断：哪个策略最稳，哪个策略最容易刷榜但不安全。",
    ),
    "day_07_capstone_artifact.ipynb": (
        "整理至少 1 个完整 submission bundle：manifest、trajectory、results、explanation。",
        "至少 replay/verify 2 条轨迹：一条成功轨迹，一条失败或低分轨迹。",
        "补齐 failure analysis：至少解释 2 个失败原因和对应修复方案。",
        "写 500 字项目摘要，让别人不问你也能复现实验结论。",
    ),
    "day_08_gpt_planner_and_validation.ipynb": (
        "至少写 3 个 GPT-style plan：保守、激进、安全约束三种风格。",
        "每个 plan 至少包含 8 个 operation，并全部经过 validate/repair。",
        "记录每次 invalid reason 和修复动作，形成 tool-call 日志表。",
        "写 400 字讨论：LLM planner 在哪里帮了忙，在哪里必须被工具约束。",
    ),
    "day_09_bayesian_optimization.ipynb": (
        "使用足够 budget 让 BO 至少进入 3 次 acquisition 决策，而不是停在初始点。",
        "比较普通 BO 与 safe BO：至少各跑 3 个 seed。",
        "画 best-score、risk、constraint violation 随实验轮次变化的曲线。",
        "写 400 字分析：BO 被哪些观测误差或安全约束影响，下一版 acquisition 如何改。",
    ),
    "day_10_public_leaderboard_challenge.ipynb": (
        "至少提交 2 个 agent，每个 agent 至少 3 个 seed。",
        "每个提交都必须包含 manifest、trajectory、results 和一段 strategy note。",
        "比较 public leaderboard 的 performance、sample efficiency、safety-aware score。",
        "写 400 字说明：哪些改动是稳健策略，哪些可能只是 public-test 过拟合。",
    ),
    "day_11_private_generalization.ipynb": (
        "至少比较 2 个策略在 public-test 与 private-like split 上的表现。",
        "每个策略至少 3 个 seed，报告均值、标准误和 public/private gap。",
        "把 gap 拆成 performance、safety、sample efficiency、invalid operation 四部分。",
        "写 500 字泛化诊断：失败来自机理误判、采样不足、噪声，还是公开榜过拟合。",
    ),
    "day_12_demo_day_artifact.ipynb": (
        "整理最终 6 类证据：轨迹、榜单、图表、机理解释、失败分析、复现命令。",
        "形成 8-10 页展示稿或等价 markdown 报告。",
        "至少选择 1 条最佳轨迹和 1 条失败轨迹进行并排解释。",
        "写 800 字最终结论：你发现了什么局部 world model，下一步如何验证。",
    ),
    "day_13_year2_process_modules.ipynb": (
        "至少运行 4 个过程 task：结晶、蒸馏、连续流、电化学各一次。",
        "为每个过程记录新增 ledger 字段、观测字段、风险来源和失效模式。",
        "选择 1 个过程做深挖，写出需要新增的专业物理模型和测试清单。",
        "写 500 字论证：为什么它应挂在同一套 WorldLaw 下，而不是独立小游戏。",
    ),
    "project_leaderboard_blueprint.ipynb": (
        "模拟至少 2 个学生提交、2 个 task、2 个 seed 的本机评测流程。",
        "输出教师端 inbox、验证日志、结果表、leaderboard 四类文件结构。",
        "设计至少 4 个榜：performance、sample efficiency、safety、explanation。",
        "写出双人/小组协作规则：如何声明任务、如何提交、如何避免重复劳动和刷榜。",
    ),
    "full_workflow_demo.ipynb": (
        "完整跑通一次全流程，并把每个输出映射到对应 API 或 CLI。",
        "修改一个 task 或 agent 参数，重新生成一条不同轨迹。",
        "至少对比 2 个 agent 的结果，并运行 verify。",
        "写 400 字总结：哪些步骤是实验执行，哪些步骤是评测复现。",
    ),
    "physics_sanity_check.ipynb": (
        "每类扫描至少 10 个点：温度、时间、催化剂-溶剂、浓度-风险。",
        "对每张图写出预期趋势、实际趋势和不一致原因。",
        "至少新增 2 条 sanity assertion，作为后续物理内核重构的回归测试候选。",
        "写 400 字说明：通过 sanity check 与真实校准之间还差什么。",
    ),
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
        or text.startswith("## 三小时实验工单")
        or text.startswith("## 学生工作区")
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


def _work_order_cell(path: Path, meta: dict[str, str]) -> dict:
    orders = WORK_ORDERS[path.name]
    rows = "\n".join(f"| {index} | {item} |" for index, item in enumerate(orders, start=1))
    return _markdown_cell(
        f"""## 三小时实验工单（必须自己完成）

这一节不是演示输出，而是当天真正的工作量。请不要只从上到下运行已有单元；必须在后面的学生工作区新增自己的实验、图表、表格和文字结论。

| 序号 | 最小完成量 |
| --- | --- |
{rows}

验收口径：本日交付至少应包含数据表、图或谱图、验证/评测结果、机制解释和下一步实验建议。低于这些证据量，视为只完成了演示浏览。

"""
    )


def _workspace_markdown_cell() -> dict:
    return _markdown_cell(
        """## 学生工作区

请从这里开始写自己的实验扩展。建议保留上方演示单元作为参考，不要直接覆盖；把你新增的实验条件、图、模型、验证结果和文字结论放在下面。

建议你在本节下面新增自己的代码单元。可从这个记录模板开始：

```python
student_work = {
    "hypothesis": "",
    "experiments_added": 0,
    "figures_created": 0,
    "verification_or_metric": "",
    "next_experiment": "",
}
```

"""
    )


def _is_existing_workspace_code(cell: dict) -> bool:
    return cell.get("cell_type") == "code" and _text(cell).lstrip().startswith("# 学生工作区")


def update_notebook(path: Path, meta: dict[str, str]) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = [
        cell
        for cell in notebook["cells"]
        if not _is_existing_guidance(cell) and not _is_existing_workspace_code(cell)
    ]
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
    cells.insert(target + 1, _work_order_cell(path, meta))
    cells.insert(target + 2, _workspace_markdown_cell())

    notebook["cells"] = cells
    path.write_text(json.dumps(notebook, ensure_ascii=True, indent=1) + "\n", encoding="ascii")


def main() -> None:
    for path, meta in GUIDANCE.items():
        update_notebook(path, meta)


if __name__ == "__main__":
    main()
