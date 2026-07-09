# 架构

ChemWorld 的架构目标是提供一个统一的、可交互的虚拟化学世界。任务只是同一世界律的
不同切片；agent 面对的是连续的实验决策过程，而不是一组互不相干的 toy task。

## 基础层

基础层包含：

- ontology：物种、相、操作、仪器、任务和约束的概念定义；
- physical constitution：质量、电荷、相组成和 ledger 守恒；
- mechanism schema：反应网络和参数的机器可读描述；
- task registry：任务卡、maturity、预算、指标和可见接口；
- action/observation schema：agent 与环境交互的稳定合同。

这些模块共同定义 `world_law_id = chemworld-physical-chemistry`。

## Runtime V2 运行时

Runtime V2 把每个 step 拆成可追踪 transaction：

1. 校验 action schema。
2. 检查任务阶段和操作前置条件。
3. 调用 domain services 更新状态。
4. 写入 typed ledger 和 transaction record。
5. 生成 observation、instrument readout、reward 和 constraint flags。
6. 判断 termination/truncation。

这条链路让环境既能服务 RL，也能服务 audit、replay 和课程教学。

## 领域服务

Domain services 处理具体物理化学语义：

- reaction service；
- phase/partition service；
- separation service；
- spectroscopy/instrument service；
- safety/cost service；
- scoring service。

服务之间通过 typed state 和 ledger 交互，避免把所有逻辑塞进一个巨大的 `step()`。

## 任务注册表

Task registry 是 benchmark contract 的中心。每个任务应声明：

- `task_id`
- `world_law_id`
- maturity；
- allowed operations；
- observation channels；
- budget；
- metrics；
- hidden scenario policy。

任务卡应从 registry 生成或至少与 registry 保持一致。

## Gym API

正式入口：

```python
env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
obs, info = env.reset(seed=1)
obs, reward, terminated, truncated, info = env.step(action)
```

Gym API 是 agent 的公共面；内部 runtime 可以复杂，但对外合同必须稳定。

## 观测服务

Observation 不应泄露 hidden state。仪器读数、谱图、final assay 和 phase probe 都应通过
独立服务生成，并记录 noise、cost、unit 和 visibility boundary。

## Agent 类型

支持的 agent 类型包括：

- 固定 recipe；
- 规则 baseline；
- black-box optimizer；
- RL agent；
- tool-using LLM agent；
- world-model learner。

## 评测层

评测层负责 score、constraint summary、trajectory validation、baseline table 和
leaderboard artifact。它不应修改环境语义。

## 数据层

数据层保存 trajectory、task card、manifest、score 和 report。正式发布时，数据包必须
能说明生成命令、commit、seeds 和 maturity metadata。
