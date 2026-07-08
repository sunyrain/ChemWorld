# ChemWorld-Bench 总览

更新日期：2026-07-08

## 项目定位

ChemWorld-Bench 是一个面向 AI4Science、化工教育和闭环科学决策研究的虚拟物理化学实验 benchmark。它的目标不是立即模拟真实世界中所有化学现象，也不是构建一个通用反应预测软件；它首先要建立一个可交互、可复现、可评测、可扩展的化学实验世界，使学生、人类研究者、LLM agent、贝叶斯优化器和混合系统能够在同一套隐藏环境中进行有限预算实验。

更准确地说，ChemWorld 当前研究的是：

> 在受限但可执行的虚拟物理化学世界中，agent 如何通过实验动作、仪器观测、局部建模、过程决策和机制解释，形成可复现、可泛化的闭环实验策略。

## 距离 Chemical World Model 还有多远

如果把 chemical world model 理解为“能够覆盖真实化学空间、真实反应体系、真实仪器、真实工艺和真实机器人实验的通用世界模型”，ChemWorld 还处在很早期。它距离这种意义上的完整 chemical world model 仍然很远。

如果把目标收缩为“可交互、可评测、可教学的局部物理化学世界模型底座”，ChemWorld 已经形成了一个可运行的 alpha benchmark。它已经有统一环境入口、共享世界规律、隐藏状态、物理约束、事件动作、仪器观测、任务注册、轨迹日志、baseline、leaderboard 和教程体系。

当前成熟度可以这样判断：

| 层面 | 当前成熟度 | 判断 |
| --- | --- | --- |
| 交互环境 | 较成熟 | 已能执行多步实验、测量、分离、提交和回放 |
| Benchmark 骨架 | 较成熟 | task、trajectory、verify、metrics、baseline 和本机评测链路已经建立 |
| 教学平台 | 较成熟 | 已有多天 notebook、工作量要求和课程评测思路 |
| 物理化学底座 | 中等 | 已有自研 physchem 核心，但仍需持续校准和拆分 |
| 真实化学预测 | 早期 | 当前主要是半机理虚拟世界，不应宣称真实预测 |
| LLM agent 生态 | 早期 | 有 adapter/replay/stub，但还缺真正 tool-using agent 基线 |
| 国际级 benchmark 可信度 | 中期起步 | 需要更强 hidden eval、reference calibration、official baseline matrix 和数据集发布 |

## 核心思想

ChemWorld 的核心不是把多个小游戏堆在一起，而是在同一套物理化学世界规律下定义不同任务切片。反应优化、仪器表征、后处理分离、安全约束、机制解释、public/private 泛化和 tool-agent planning 都应共享同一套 ontology、constitution、state ledger、transition kernel、observation kernel 和 evaluation protocol。

这意味着：

- task 不是独立环境，而是同一世界的不同目标、预算和权限设置；
- agent 不能直接读取真实状态，只能通过仪器和日志建立自己的局部 world model；
- benchmark 不只评价最高分，还评价样本效率、安全性、泛化、解释和复现性；
- 教学不再围绕 Python 语法，而围绕未知环境中的实验决策和证据链。

## 当前平台形态

当前正式入口是：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
```

平台由几层组成：

- foundation：定义化学本体、单位、物理宪法、状态账本和 kernel 协议。
- world：定义世界规律、scenario、operation、instrument、recipe、scoring 和过程模块。
- envs：提供统一 Gymnasium 环境。
- tasks：把同一世界切成不同 benchmark 任务。
- agents：提供 random、LHS、scripted、BO、safe BO 和 LLM 相关 agent。
- eval：负责运行、验证、指标、排行榜和 benchmark artifact。
- data：负责 trajectory、submission、dataset export 和匿名化。
- physchem：逐步实现自研物理化学和化工计算核心。
- notebooks/docs：提供教程、课程地图、评测说明和项目文档。

## 当前能做什么

ChemWorld 当前已经可以完成以下闭环：

1. 运行多步虚拟实验。
2. 设计自定义 reaction recipe。
3. 执行反应、采样、测量、终止和 final assay。
4. 进行萃取、分相、洗涤、干燥、浓缩等后处理。
5. 读取 HPLC、GC、UV-vis、FinalAssay 等带噪观测。
6. 生成可绘图的虚拟 raw signal。
7. 在有限预算下运行 random、LHS、scripted、BO、safe BO 等 baseline。
8. 保存 JSONL trajectory。
9. 通过 verifier 回放实验轨迹。
10. 生成 leaderboard metrics。
11. 组织本机教师端/学生端评测。
12. 使用 notebook 进行多天课程训练。

更重要的是，这些能力不是孤立存在的。一次实验可以从投料开始，经过反应、表征、分离、纯化和最终检测，形成一条完整可回放轨迹。

## 当前任务主线

当前任务可以归纳为五条主线：

| 主线 | 代表任务 | 核心问题 |
| --- | --- | --- |
| 反应优化 | `reaction-optimization-standard`、`reaction-safety-constrained` | 如何在有限预算下找到高分且安全的反应条件 |
| 反应到纯化 | `reaction-to-purification`、`purity-yield-tradeoff` | 如何在产率、纯度、回收率、成本和风险之间权衡 |
| 科学发现 | `low-budget-characterization`、`reaction-mechanism-explanation` | agent 是否能从少量观测中发现隐藏规律 |
| 泛化评测 | `public-private-generalization` | public 表现是否能迁移到 hidden world |
| 工具型 agent | `tool-agent-planning` | LLM agent 是否能使用 validator、recipe、instrument 和 analysis 工具闭环 |

Year 2 扩展任务包括结晶、蒸馏、连续流和电化学。它们目前更适合作为后续过程模块的研究入口，而不是第一阶段 benchmark 的唯一核心。

## Ground Truth 形态

ChemWorld 当前的 ground truth 不是现实世界的全部化学真值，而是一套隐藏、可执行、可复现、受物理化学约束的虚拟世界真值。

它包括：

- hidden parameters；
- reaction and process mechanisms；
- phase and partition behavior；
- instrument noise and raw signal generation；
- hidden state ledger；
- task objective and scoring rules。

agent 默认不能看到这些真值，只能通过实验动作和仪器观测形成自己的 belief state。维护者使用 ground truth 生成世界、校验守恒、回放轨迹、评分解释和组织 private evaluation。

后续要继续增强的，是把更多模块与公开参考数据、教科书例题、专业库对照和真实实验锚点连接起来，使虚拟 ground truth 更有物理可信度。

## Benchmark 形态

一个正式 ChemWorld benchmark 应当包含：

- public-dev：用于教学、调试和开发。
- public-test：用于开源复现实验和官方 baseline。
- private-eval：用于正式榜单和抗过拟合。

每个任务都需要明确 task card、scenario card、允许操作、允许仪器、预算、成功指标和评测方式。提交应包含 manifest、trajectory、results 和 explanation。评测方不应信任提交中的最终分数，而应通过 replay verifier 重新计算关键结果。

理想评分不应只看最高分，而应同时考虑：

- final assay performance；
- sample efficiency；
- safety and cost；
- invalid action rate；
- purity and recovery；
- public/private generalization；
- explanation quality；
- reproducibility。

## 当前优势

ChemWorld 当前最有价值的地方在于：

- 已经建立统一的交互环境，而不是一组离散脚本。
- 已经把任务从单步黑箱优化推进到多步实验决策。
- 已经把反应、测量、分离、风险、成本和提交评测放进同一链路。
- 已经具备课程、benchmark、agent 研究三种使用场景。
- 已经开始建设自研物理化学底座，而不是完全依赖外部黑箱。
- 已经有本机评测机和提交协议，可以支持学生项目和内部 challenge。

## 当前短板

ChemWorld 仍然存在清晰短板：

- 物理模型仍是受限半机理模型，不能宣称真实反应预测软件。
- 部分过程模块仍处于 proxy 或 lite 阶段。
- hidden eval 还需要更正式的 maintainer-side registry。
- official baseline matrix 还需要冻结并系统运行。
- explanation scoring 还需要结构化 rubric。
- LLM agent 还需要真正 tool-using baseline。
- physchem 核心需要继续拆分、校准和专业化。
- 数据集层需要进一步接近可公开发布的 offline benchmark。

## 下一阶段最重要的方向

下一阶段不宜盲目增加更多任务，而应优先提升可信度：

1. 冻结少量 flagship tasks。
2. 为每个 flagship task 建立 task card 和 scenario card。
3. 生成 reference oracle envelope，用于校准任务难度。
4. 系统运行 official baseline matrix。
5. 建立 private-eval 维护者侧流程。
6. 增强 reaction-to-purification、low-budget-characterization 和 mechanism-explanation。
7. 将 physchem 核心继续专业化，并加入参考校准案例。
8. 建立 tool-using LLM agent 基线。
9. 发布 baseline trajectories 和 dataset cards。
10. 准备 benchmark paper artifact。

## 总体判断

ChemWorld 目前距离“通用化学世界模型”还很远，但已经接近一个有研究价值的“局部化学世界模型 benchmark”。它最现实、最有价值的路线不是宣称模拟整个真实化学世界，而是持续把化学直觉、物理约束、实验操作、仪器观测、agent 决策和可复现评测写成一个共享的、可执行的虚拟世界。

如果继续沿这个方向推进，ChemWorld 可以成为一个面向 AI 原生化工教育和智能体实验决策研究的正式 benchmark：它不替代真实实验室，但能在低成本、可控、可重复的环境中训练和评测“如何认识一个隐藏化学世界”。
