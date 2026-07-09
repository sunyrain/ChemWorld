# 操作语言

操作语言定义 agent 在 ChemWorld 中能做什么。它处在“真实化学语义”和“可计算 Gym
action”之间：足够接近实验流程，便于人类理解；又足够结构化，便于校验、回放和评分。

## Action 抽象层

每个操作由 `operation` 字段标识，并携带参数。环境会根据当前 task stage 和 state
ledger 检查前置条件。

常见字段：

- `volume_L`：体积。
- `amount_mol`：物质的量。
- `temperature_K`：温度。
- `duration_s`：持续时间。
- `stirring_rpm`：搅拌速率。
- `phase`：相，例如 `organic` 或 `aqueous`。
- `instrument`：测量工具。

字段保持英文，以保证 API 稳定。

## 反应操作

- `add_solvent`
- `add_reagent`
- `add_catalyst`
- `heat`
- `cool`
- `stir`
- `terminate`
- `measure`

这些操作会影响反应进程、成本、安全、选择性和观测结果。

## 分离操作

- `add_extractant`
- `mix`
- `settle`
- `separate_phase`
- `wash`
- `dry`
- `concentrate`
- `crystallize`
- `distill`

分离操作通常依赖前序状态。例如没有形成可分离相时调用 `separate_phase`，应返回
`precondition_failed`，而不是静默成功。

## 设计原则

操作语言不追求覆盖真实实验室全部 SOP，而是优先服务 benchmark：合法性清楚、反馈可
学习、失败可解释、trajectory 可回放。
