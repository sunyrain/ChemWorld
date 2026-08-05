# LLM 实验智能体

> **LLM 的价值不只是拥有化学知识，而是能否把知识变成可检验假设，并在实验否定它时改变行动。**

在 ChemWorld 里，LLM 是一个反复使用实验工具的 Agent：它读取公开证据，选择一个合法操作，观察
结果，再决定下一步。

```text
任务 + 实验历史 + 可用谱图
  → 模型给出结构化决策
  → 校验 Action
  → 执行环境步骤
  → 返回公开观测与实验记忆
  → 下一次决策
```

环境本身不依赖在线 API。没有密钥时，经典算法、Student Lab、stub 和 replay 都可以离线运行。

## LLM 在实验循环中的角色

LLM 可以承担假设生成、计划、公开证据解释、工具调用和跨实验记忆。不同 scaffold 应被当作不同
方法条件，而不是笼统称为“同一个模型”：

| 条件 | 决策结构 |
| --- | --- |
| Direct | 只读取当前公开状态并选择 Action |
| Memory | 同时读取压缩实验历史 |
| Retrieval | 主动请求谱图、材料资料或历史记录 |
| Planner–Executor | 规划目标与单步执行分离 |
| World-model assisted | 使用显式局部模型或 belief 支持判断 |

## 一次模型决策包含什么

每次逻辑决策只执行一个最终 Action，并可以同时记录：

- 支撑动作的公开 evidence；
- 对当前仪器或谱图结果的 interpretation；
- 可被后续实验检验的 hypothesis；
- uncertainty；
- 一段简短、面向审计的 rationale。

模型只看到 task prompt、合法动作、公开历史和当前披露策略允许的谱图。隐藏状态、机理参数与
private salt 不进入 prompt。系统也不请求或保存私有逐字思维链。

## 逐步决策与整段计划

- **逐操作自适应**：每执行一个 operation 都重新读取最新结果，适合研究闭环调整。
- **整段计划**：开局生成完整 recipe，适合作为低调用成本或 open-loop 对照。

调用次数多不等于真的发生了适应。轨迹还要显示：新证据是否改变了假设、谱图解释或后续动作。

## 让模型按需读取谱图

| 披露模式 | 模型可以获得什么 | 适合回答的问题 |
| --- | --- | --- |
| `raw` | 降采样原始曲线 | 模型能否直接读取原始信号 |
| `unassigned` | 曲线与未指认峰 | 默认研究条件 |
| `assigned` | 曲线与允许披露的峰指认 | 教学或信息上限 |
| `masked` | 不提供谱图通道 | 配对因果消融 |

Agent Observatory 会先给模型一个谱图目录；只有模型明确请求某个 `spectrum_request_id`，下一次
调用才会携带对应曲线或峰表。这样可以区分“网页上显示了谱图”和“模型实际用到了谱图”。

若要主张模型从谱图中获益，应在相同任务、世界、预算和模型 seed 下比较可见/屏蔽条件，并保留
模型引用的峰、动作变化与最终效果。

## 材料信息也要形成对照条件

| 条件 | 模型知道什么 |
| --- | --- |
| `opaque` | 只看到稳定类别 ID |
| `descriptor` | 获得公开、可追溯的有限描述符 |
| `named/retrieval` | 可以读取材料名称或经批准的资料 |
| `oracle` | 研究上限条件；不属于正式公开 Agent 输入 |

材料名称可能带来强先验。若要证明模型使用了实验而非名称记忆，应在保持世界和预算一致时遮蔽、
重映射或冲突化公开信息，并观察假设、测量和 Action 是否相应改变。

## 用因果消融判断“是否真的使用了证据”

解释文本提到某个峰，不足以证明它影响决策。更可靠的设计是配对改变信息条件：

- assigned ↔ masked 谱图；
- 有记忆 ↔ 无记忆；
- named material ↔ opaque material；
- retrieval ↔ 相同 token 预算下的直接决策。

评价应检查后续 Action、测量选择、最终结果和失败类型，而不只给自然语言解释打分。

## 开放与闭源模型承担不同角色

Frontier API 可以作为能力上界探针，开放权重模型支持可复现实验，化学专用模型检验领域先验，未来
的 ChemWorld-trained 模型则检验交互预训练价值。正式比较需要分别报告模型身份、权重可得性、
scaffold、信息条件和资源，不能把它们合并成“LLM”一行。

## 技术配置：连接在线模型

这里有两条独立的模型接入路径：

| 路径 | 当前 provider | 用途 |
| --- | --- | --- |
| Task Lab / Agent Observatory | DeepSeek API | 本地交互、演示和自定义开发评测 |
| 冻结正式 campaign runner | Codex subscription | 当前双旗舰 S0 正式结果 |

下面的环境变量只配置 **Task Lab**，不会把正式 campaign 切换为 DeepSeek，也不会复现已经冻结的
Codex subscription 结果。正式 runner、模型与资源合同见[旗舰实验](flagship_experiments.md)。

=== "PowerShell"

    ```powershell
    $env:DEEPSEEK_API_KEY = "<your-api-key>"
    $env:DEEPSEEK_MODEL = "<provider-model-id>"
    python -m apps.task_lab.server --port 8876
    ```

=== "bash"

    ```bash
    export DEEPSEEK_API_KEY="..."
    export DEEPSEEK_MODEL="<provider-model-id>"
    python -m apps.task_lab.server --port 8876
    ```

模型 ID 与可用参数可能随 provider 变化，请使用 provider 当前支持的标识。密钥只通过进程环境变量
或本地忽略文件传入，不进入浏览器、prompt artifact、trajectory 或结果文件。

## 把请求成本算清楚

provider 超时、空响应、JSON 修复和重试都是真实消耗。正式运行至少记录：

- provider、模型 ID、客户端版本和请求参数；
- prompt、工具 schema 与披露策略摘要；
- 输入 cache-hit/cache-miss token 与输出 token；
- 请求、失败、重试和修复次数；
- 冻结价格快照与折算费用；
- 运行时间、轨迹摘要和 prompt hash。

一个 environment operation 最终只能对应一个逻辑决策，但为了得到这个决策产生的所有 provider
请求都应进入资源账本。

这一区分对当前 Codex 路径尤其重要：DeepSeek 的 `StructuredG2Agent` 是每个 primitive
operation 一次直接 JSON completion；原生 Codex 路径则是一个持久 `codex exec` experiment turn，
通过 host-owned STDIO MCP 连续调用 `material_information` 和 `step`。因此“一个 Codex session”
不是“一个底层模型 response”。若 CLI 没有逐 response usage 事件，报告必须把
`backend_model_response_count` 标为未知，同时分别报告 provider session、logical turn、MCP tool
calls、累计 input、cache hit/miss 和 output。

U05 的口径固定为：1 个 provider session、1 个 logical Codex turn、17 个 MCP tool calls（1 次
`material_information` 加 16 次 `step`），而不是 17 个底层模型响应。DeepSeek 对照臂则是每个
primitive operation 一个 provider completion；两者 transport/scaffold 不同，不能把 session 数
直接当作模型调用数。`cache_hit_tokens` 是被复用的历史输入上下文，`cache_miss_tokens` 是本次
新计入的输入；两者都属于 input，不是重复生成的 output。必须同时报告 cumulative input、cache
hit/miss 和 output，不能用 cache hit 数量推断“重复输出”。

## 不联网也能测试 Harness

`ToolUsingLLMStubAgent` 用确定性规则检查 tool use、validator、memory 与 replay 管线；
`LLMReplayAgent`（method id `llm_replay`）重放已经保存的 Action trace；
`LLMCompletionReplayAgent`（method id `llm_completion_replay`）则重放 recipe planner 的缓存 JSON completion。
两者处于不同抽象层，不共享方法身份。

```bash
python examples/demo_llm_replay_harness.py
```

它们适合测试工程链路，但不能代表在线 LLM 的性能。

## 当前做到哪一步

在线客户端、逐操作 trace、按需谱图、token/费用账本和失败保留规则已经实现。双旗舰静态
campaign 已留下真实 Codex subscription provider 轨迹；这支持冻结范围内的正式描述性结果，
不构成跨模型排名或“模型学会化学机理”的结论。机制适应的正式跨方法 provider 矩阵仍未执行。

界面操作见[打开可视化实验室](interactive_task_lab.md)，方法比较口径见
[设计公平评测](benchmark_protocol.md)。
