<section class="cw-home-hero" markdown>

<span class="cw-eyebrow">A causal world engine for experimental intelligence</span>

# 让实验智能拥有自己的世界引擎

**静态基准问模型知道什么；ChemWorld 问它在不知道答案时会怎样做实验。**

<p class="cw-lead">ChemWorld 构造可回放、因果可干预的虚拟化学与化工世界。Agent 在部分观测、
有限预算和安全约束下选择操作与测量、形成假设并更新策略；世界规律可以改变，因此记住一个最佳
配方并不足以成功。</p>

它不是通用真实反应预测器，而是训练和检验实验决策能力的研究环境。

<div class="cw-button-row" markdown>

[走进一次未知世界](one_experiment.md){ .md-button .md-button--primary }
[阅读研究主线](vision.md){ .md-button }
[构建一个 Agent](agent_tracks.md){ .md-button }

</div>

<div class="cw-pill-row">
  <span class="cw-pill">Gymnasium API</span>
  <span class="cw-pill">Replay-verified trajectories</span>
  <span class="cw-pill">Causal world shifts</span>
  <span class="cw-pill">BO · RL · LLM · World Models</span>
</div>

</section>

## 当前证据

两个旗舰任务已完成无材料 dossier 的正式描述性 campaign，以及
`opaque / nominal / misindexed` 三臂匿名材料信息实验。正确信息对电化学有确认的正价值，
对结晶仍不确定；错误先验会影响两个任务的早期行动，但没有一个任务通过整体恢复联合规则。

当前还完成了五任务、五世界的 development-only 扩展：共享 Codex 策略在电化学和新
反应—蒸馏任务上高于最佳经典方法均值，在结晶、分配和连续流上落后。15 个任务的完整实验合同
均可执行；两个任务有正式结果，另外三个任务新增了开发比较。历史 Gate A 的当前源码绑定已过期，
Participant Gates B–E 尚未执行，因此当前
`benchmark_ready=false`：这是候选研究环境，不是完整排名 release。

[查看精确结果与当前状态 →](benchmark_release.md){ .md-button }

## 为什么需要 World Engine

真实化学实验慢、贵并带有风险，无法像文本或游戏那样无限生成交互数据。静态数据集可以测试知识和
预测，却不能直接检验 Agent 是否会选择信息量高的实验、处理失败、管理资源，或在旧模型失效时恢复。

| 静态化学 Benchmark | ChemWorld |
| --- | --- |
| 给定问题，生成答案 | 给定目标，决定下一次实验 |
| 一次性输入输出 | 多轮观测、行动与更新 |
| 数据和规律固定 | 隐藏世界规律可以变化 |
| 错误主要表现为分数下降 | 错误会消耗预算、触发风险或改变状态 |

[为什么需要 ChemWorld →](vision.md)

## 核心实验

```text
隐藏世界 + 公开任务
        ↓
Agent 选择操作与测量
        ↓
虚拟物理执行完整实验
        ↓
公开反馈 + 成本 + 约束
        ↓
Agent 更新判断并选择下一次实验
        ↓
盲测、回放与证据审计
```

同一个任务可以运行在不同的隐藏材料、动力学、相行为或设备参数下。严格评测不仅问最终分数，还问：

- **静态搜索：**有限预算能否找到可靠方案？
- **先验纠错：**正确或错误的材料信息怎样改变行动，反馈能否纠偏？
- **机制适应：**规律中途变化后，Agent 能否检测、归因并恢复？

当前正式证据已经覆盖前两项的两个旗舰任务，五任务开发比较进一步检验了静态搜索的任务异质性；
第三项仍缺 Participant Gates B–E。

[了解因果世界 →](causal_worlds.md) · [查看旗舰实验 →](flagship_experiments.md)

## 三种交互层级

<div class="grid cards" markdown>

- **Campaign Design**

  Agent 每轮提交一个完整实验方案。适合配方搜索、主动学习和 Bayesian optimization。

- **Procedure Execution**

  Agent 逐步投料、控温、测量、后处理和终检。适合 LLM 工具使用与实验程序规划。

- **Process Control**

  Agent 在反应器或分离流程运行期间持续测量和控制。适合 RL、MPC 和 world model。

</div>

三种 Track 可以作系统级并列展示；算法归因必须固定相同交互层级、信息和资源合同。

[选择 Agent Track →](agent_tracks.md)

## 结果为什么可核查

一次高分不会自动成为科学结论。ChemWorld 把结果拆成任务终点、风险、成本、信息效率、适应、
资源和自治，并保留失败与未完成实验。

```text
submission
  → trajectory validation
  → deterministic replay
  → metric recomputation
  → constraint and resource audit
  → verified result
```

环境验证不等于模型能力，历史证书不等于当前源码证书，描述性结果也不等于预注册 superiority。

[阅读 Benchmark 设计 →](benchmark_overview.md) · [了解证据边界 →](limitations.md)

## 不直接迁移配方，而是迁移适应能力

ChemWorld 使用受控的虚拟规律，不承诺匿名催化剂或虚拟最优条件对应现实体系。现实相关性需要逐级
连接独立 backend、真实数据和 shadow-mode 物理实验，最后才讨论窄域闭环。

[查看现实桥接路线 →](real_world_bridge.md)

## 从这里开始

<div class="grid cards" markdown>

- **体验一次实验**

  从公开任务、合法操作、测量反馈到 final assay。

  [走进一次闭环实验 →](one_experiment.md)

- **观察 Agent**

  在本地 Task Lab 中查看模型逐轮决策或运行经典方法。

  [打开可视化界面 →](interactive_task_lab.md)

- **构建 Agent**

  使用 Gymnasium、Typed Action、Wrapper 与回放接口。

  [五分钟开始 →](getting_started.md)

- **复现与评测**

  阅读冻结合同、seed、提交和结果可信链。

  [设计公平评测 →](benchmark_protocol.md)

</div>

完整低层规范见[技术参考索引](reference_index.md)。
