# 国际 SOTA 智能体交互化学环境 Gap Audit

更新日期：2026-07-08

这份审计用于回答一个实际问题：ChemWorld 如果要从“可运行的虚拟化工 benchmark”走向“专业级智能体交互化学世界”，还需要补哪些能力。结论不是把外部项目照搬进来，而是把它们体现出的设计压力转化为 ChemWorld 自己的架构要求。

## 参照对象

| 项目 | 关键定位 | 对 ChemWorld 的启发 |
| --- | --- | --- |
| [ChemGymRL](https://pubs.rsc.org/en/content/articlehtml/2024/dd/d3dd00183k) / [arXiv](https://arxiv.org/abs/2305.14177) | Gymnasium 风格的虚拟化学实验室，包含 reaction、distillation、extraction benches | 化学环境不应只有反应优化；bench 之间要能共享样品、容器、相态、分离和测量状态 |
| [DiscoveryWorld](https://arxiv.org/abs/2406.06769) | 面向完整科学发现循环的虚拟环境，包含多主题、多难度、多参数变化任务 | 任务要评价假设形成、实验设计、结果分析和解释性知识发现，而不是只看终点分数 |
| [ScienceWorld](https://arxiv.org/abs/2203.07540) | 交互式文本科学环境，强调概念在新情境中的可迁移推理 | ChemWorld 需要更强的 action feedback、state affordance、错误恢复和自然语言任务卡 |
| [SciAgentGym](https://arxiv.org/abs/2602.12984) | 多步科学 tool-use 环境，覆盖物理、化学、生物、材料等学科工具 | LLM agent 不能只调用 `env.step`，还应能使用 validator、recipe compiler、surrogate、仪器和数据工具 |
| [ChemCrow](https://www.nature.com/articles/s42256-024-00832-8) / [arXiv](https://arxiv.org/abs/2304.05376) | 将 LLM 与专家化学工具结合，服务合成、药物发现和材料设计 | ChemWorld 需要真正的 tool-using agent baseline，而不是只有在线 API adapter |
| [Coscientist](https://www.nature.com/articles/s41586-023-06792-0) | LLM 结合搜索、代码、文档和实验自动化执行复杂化学实验 | 长期应支持 planner → validator → instrument/simulator → analysis 的多工具闭环 |
| [A-Lab](https://www.nature.com/articles/s41586-023-06734-w) | 结合文献、计算、机器学习、主动学习和机器人执行的闭环材料实验室 | ChemWorld 的虚拟闭环需要更明确地区分 prediction、execution、diagnosis、active learning 和 failure recovery |
| [Matbench Discovery](https://www.nature.com/articles/s42256-025-01055-1) / [leaderboard](https://matbench-discovery.materialsproject.org/) | 任务式材料发现评测和公开 leaderboard | ChemWorld 的 leaderboard 应使用任务相关指标、public/private split、提交包和可复现实验记录 |

## 当前 ChemWorld 的优势

| 能力 | 当前状态 |
| --- | --- |
| 统一入口 | `gym.make("ChemWorld", task_id=...)` 已经成为主入口 |
| 共享世界规律 | reaction、phase、separation、observation 正在挂到同一套 `WorldLaw` |
| 事件驱动实验 | 支持 add、heat、wait、measure、terminate、separation 等 operation |
| 轨迹与提交 | JSONL trajectory、manifest、verify、submission bundle、local eval machine 已有基础 |
| 教学闭环 | Day 1-13 notebook 已覆盖入门、机制、观测、surrogate、BO、leaderboard、泛化和过程模块 |
| 专业底座开端 | `physchem` 已开始实现 properties、reaction networks、reactors、EOS、equilibrium、spectroscopy 等本地核心 |

## 主要差距

### 1. 科学发现循环还不够完整

DiscoveryWorld 的强项是把任务组织成完整循环：提出假设、设计实验、执行、分析、形成解释性知识。ChemWorld 现在已经有解释字段和反思问题，但自动评测仍偏向数值分数。

需要加强：

- `explanation_schema`：把 hypothesis、evidence、mechanism update、failure analysis、next experiment rationale 做成结构化对象。
- explanation rubric：先人工评分，后续再做半自动对齐评分。
- knowledge discovery metrics：记录 agent 是否发现了温度-副反应、溶剂-分配、催化剂失活、纯度-回收率等隐藏规律。

### 2. 交互环境 affordance 还不够强

ScienceWorld 和 DiscoveryWorld 会给 agent 明确的可操作对象、位置、状态和失败反馈。ChemWorld 目前已有 action mask 和 validator，但状态摘要仍偏工程字段。

需要加强：

- `visible_state_summary`：给 agent 一个可读的实验台状态，例如当前容器、相态、可用样品、已终止/未终止、可测量仪器。
- invalid action recovery：非法动作不只返回失败，还返回可修复建议。
- operation cards：每个 operation 需要 human-readable preconditions、payload ranges、typical use、failure modes。

### 3. Tool-using agent baseline 还偏弱

ChemCrow、Coscientist、SciAgentGym 的共同点是 agent 不只是直接给动作，而是编排工具。ChemWorld 当前有 `LLMReplayAgent` 和 stub，但还没有标准工具箱。

需要加强：

- `ChemWorldToolKit`：统一暴露 `validate_action`、`validate_recipe`、`compile_recipe`、`run_experiment`、`query_task_info`、`fit_surrogate`、`plot_trajectory`。
- `ToolUsingLLMStub`：不依赖在线模型，但必须走真实工具链。
- LLM replay trace：记录每次 tool call、输入、输出、修复过程和成本。

### 4. Bench 之间还缺真实样品流转

ChemGymRL 的 reaction、distillation、extraction benches 指向同一实验室直觉。ChemWorld 已经有 reaction-to-purification，但需要让反应、相分配、分离、纯化和最终 assay 的 ledger 更像真实样品账本。

需要加强：

- vessel inventory：多个容器、转移、废液、取样、损失、残留。
- phase ledger：每个相中的关键物种、体积、密度 proxy、溶解度限制和夹带损失。
- sample lineage：每次取样、分液、浓缩和最终检测能追溯来源。

### 5. 真实 grounding 和参考校准不足

Coscientist、A-Lab 和 Matbench Discovery 都强调真实工具、真实数据或任务式真实评价。ChemWorld 仍是半机理虚拟世界，科研可信度要靠透明假设、参考校准和任务化评测补强。

需要加强：

- reference cases：用公开文献或标准物性数据校准少量受控案例，而不是宣称通用预测。
- optional backend validation：对 CoolProp、Cantera、thermo、Reaktoro、pycalphad 等只做可选对照，不作为核心依赖。
- benchmark cards：每个 task 说明适用范围、隐藏机制、指标、失效模式和不该外推的地方。

### 6. Dataset 层还需要接近 Minari 风格

SOTA 环境越来越重视可复用数据集。ChemWorld 有 JSONL，但还需要更正式的 dataset card、Parquet export、trajectory validation 和 offline agent training split。

需要加强：

- `dataset_card.json`：记录 task、world law、agent、seed、license、隐私状态、已知局限。
- offline split：baseline trajectories、student trajectories、external submissions 分开。
- replay hash：每条 trajectory 的 action/observation/reward 可重放校验哈希。

## Notebook 与课程需要补的坡度

| 阶段 | 当前问题 | 本轮调整方向 |
| --- | --- | --- |
| Day 1-3 | 入门已经能跑，但学生容易不知道“今天只该学什么” | 增加难度、先修、核心产出、不要做什么、下一天如何复用 |
| Day 4-6 | 机制扫描、surrogate、baseline 之间衔接偏松 | 明确从 hypothesis → data → local model → next experiment 的证据链 |
| Day 7-9 | capstone、GPT planner、BO 难度跃迁较大 | 加入基础/进阶/挑战任务分层，先让学生修复 recipe，再进入自动优化 |
| Day 10-12 | leaderboard 和 private generalization 容易被理解为刷榜 | 明确 public/private gap、过拟合诊断、解释质量和可复现提交 |
| Day 13 | Year 2 过程模块容易像愿景展示 | 改成研究延展入口：每个模块说明共享 world law 下新增哪类物理账本 |

## 下一轮工程 TODO

1. 把 `visible_state_summary` 和 operation cards 暴露到 `env.task_info()` 与 wrapper info。
2. 建立 `ChemWorldToolKit`，让 LLM baseline 通过工具调用而不是直接拼动作。
3. 给 explanation 增加结构化 schema 和人工评分 rubric。
4. 给 reaction-to-purification 增加更完整的 sample lineage 和 vessel inventory。
5. 扩展 dataset export：Parquet + dataset card + replay hash。
6. 为 `physchem` 选择 3-5 个 reference calibration cases，优先 properties、reaction kinetics、phase equilibrium、spectroscopy。
7. 把 notebook 每日任务改成基础、进阶、挑战三层，并标注难度与交付物。

## 定位更新

ChemWorld 当前最适合的国际定位是：

> 面向 AI4Science 教育与 agent 研究的统一物理化学交互世界。它不是通用真实化学预测软件，而是在同一套可执行物理化学约束下，评测人类、LLM agent、BO 和 hybrid system 如何完成有限预算实验设计、局部 world model 学习、过程决策、解释和可复现提交。

