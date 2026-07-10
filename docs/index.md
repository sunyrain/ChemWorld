# ChemWorld-Bench

<p class="cw-site-version">发布文档 · World Law v0.2 · 2026-07-10</p>

ChemWorld-Bench 是一个机制驱动、可回放的闭环虚拟化学实验 benchmark。智能体通过统一的
Gymnasium 环境执行投料、反应、分离、测量和终止操作，在有限预算、部分可观测、带成本与
安全约束的世界中学习并决策。

<div class="cw-hero-grid" markdown>

<div class="cw-hero-card" markdown>

### 运行任务

安装环境、完成第一次 episode，并理解 observation 与 `info`。

[五分钟开始 →](getting_started.md)

</div>

<div class="cw-hero-card" markdown>

### 评测 Agent

使用冻结任务合同、official seeds、replay verifier 和提交清单。

[查看评测协议 →](benchmark_protocol.md)

</div>

<div class="cw-hero-card" markdown>

### 接入工具或模型

了解操作协议、Action Schema、wrapper 与 LLM tool adapter。

[阅读 Agent 接口 →](agent_interface.md)

</div>

<div class="cw-hero-card" markdown>

### 理解物理边界

查看世界律、物化模型、成熟度和明确限制。

[查看模型成熟度 →](model_maturity.md)

</div>

</div>

## 你将获得什么

- 一个稳定入口：`gym.make("ChemWorld", task_id=..., seed=...)`；
- 15 个共享 `chemworld-physical-chemistry-v0.2` 世界律的任务切片；
- 事务化运行时、typed ledgers、physical constitution checks 与可重放轨迹；
- 受预算约束的 HPLC、GC、UV-vis、IR、NMR、MS 和 final assay 等虚拟仪器；
- 任务级成熟度元数据，明确区分 `proxy`、`lite`、`reference_validated` 与
  `professional_candidate`；
- 从 baseline、suite、verify、evaluate 到 leaderboard artifact 的完整本地评测链路。

## 最短路径

=== "第一次使用"

    1. 按[安装与首次运行](getting_started.md)创建环境。
    2. 从[任务列表](tasks.md)选择任务。
    3. 运行[演示](demos.md)，检查 trajectory 和 final assay。

=== "提交 Benchmark"

    1. 阅读[评测协议](benchmark_protocol.md)和[任务卡](task_cards.md)。
    2. 使用[Official Seed Suite](seed_suite.md)运行 agent。
    3. 按[提交与验证](submission.md)生成并验证提交包。

=== "开发 Agent"

    1. 阅读[Agent 交互接口](agent_interface.md)。
    2. 对照[操作协议](operations.md)和[Action Schema](action_schema.md)。
    3. 选用[Wrapper](wrappers.md)或[LLM Agent Harness](llm_agent_harness.md)。

## 当前可信边界

ChemWorld 是虚拟研究环境，不是现实反应预测器、商业流程模拟器、DFT/分子动力学 wrapper
或实验机器人控制器。`reaction-to-purification` 等任务仍包含没有专业等价模块的干燥、浓缩、
转移降级模型；这些表面继续公开标为 proxy。结晶、连续流和萃取运行时已升级为专业候选模型，
但 `professional_candidate` 仍不代表工业验证。

在引用结果前，请阅读[适用范围与限制](pre_release_limitations.md)和
[模型成熟度](model_maturity.md)。

## 发布质量

发布版本通过统一门禁检查 lint、类型、测试、文档、冻结轨迹、参考后端和环境自洽性。验证
方法与可复现命令见[验证与质量保证](validation.md)，本次模型与合同变更见
[发布说明](release_notes.md)。
