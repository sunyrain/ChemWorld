# LLM Agent Harness

ChemWorld 把 LLM 当作受资源约束的 tool agent，而不是直接询问一个最终配方。正式交互循环是：

```text
public task + history + spectra
  -> structured model decision
  -> action validator
  -> environment step
  -> public observation + experiment memory
  -> next decision
```

环境本身不依赖在线 API。没有凭据时，经典方法、学生端、stub 和 replay 仍可离线运行。

## 在线交互合同

每个 operation-level 逻辑决策只能提交一个最终 action，并同时返回：

- 支撑动作的公开 evidence；
- 对可见谱图或仪器结果的 interpretation；
- 当前 hypothesis；
- uncertainty；
- 简短 rationale。

模型只接收 public task view、合法动作、公开历史和经过披露策略处理的谱图，不接收 hidden state、
机理参数或 private salt。系统不请求、保存或向网页展示私有逐字思维链。

## 多轮与单次计划

- `adaptive`：每一步根据最新观测重新决策；这是闭环能力的主测试模式。
- `plan`：开始时生成整段动作，仅用于低调用成本对照。

两者必须分开报告。一次性计划成功不能证明模型读取了新观测；多轮调用次数本身也不能证明有效
适应，轨迹还需显示动作或假设随证据发生可解释变化。

## 谱图披露

| 模式 | 模型输入 | 用途 |
| --- | --- | --- |
| `raw` | 降采样曲线 | 原始信号读取下限 |
| `unassigned` | 曲线与未指认峰 | 默认研究候选设置 |
| `assigned` | 带标签峰表 | 教学与信息上限 |
| masked | 无该谱图通道 | 配对消融 |

如果声明模型会“读谱”，必须比较相同任务、seed、预算和模型下的可见/屏蔽运行，并保留模型引用的
峰、动作变化和最终效应。仅把曲线画在网页上不构成使用证据。

## 请求、重试与费用

一个 environment operation 对应一个最终逻辑决策。provider 超时、空响应、JSON 修复或重试都
作为实际请求计入资源账本。正式运行至少记录：

- provider 与请求模型 ID；
- prompt、工具 schema 和披露策略摘要；
- 输入 cache-hit/cache-miss token、输出 token；
- 请求、失败、重试和修复计数；
- 冻结价格快照与折算费用；
- 模型和客户端版本、运行时间与轨迹摘要。

本地配置示例：

```powershell
$env:DEEPSEEK_API_KEY = "<your-api-key>"
$env:DEEPSEEK_MODEL = "<provider-supported-model-id>"
python -m apps.task_lab.server --port 8876
```

密钥只通过进程环境变量传入，不进入浏览器、prompt artifact、trajectory 或结果文件。

## 离线测试 Agent

`ToolUsingLLMStubAgent` 用确定性规则生成符合 trace schema 的行为，检查 tool-use、validator、memory
和 replay 管线；`LLMReplayAgent` 读取固定 action trace，复现已经发生的交互。二者都不是在线 LLM
性能证据。

```bash
python examples/demo_llm_replay_harness.py
```

## 当前证据边界

在线客户端、结构化 trace、谱图披露、token/费用账本和失败重试规则已经实现。两个冻结 live-LLM
角色尚未在四任务新 cohort 上完成配对、回放验证的正式矩阵，因此当前不能发布 LLM 排名、模型
优劣或“LLM 学会化学机理”的结论。

界面使用见[Agent Observatory 与 Student Lab](interactive_task_lab.md)，统一资源规则见
[Benchmark 协议](benchmark_protocol.md)。
