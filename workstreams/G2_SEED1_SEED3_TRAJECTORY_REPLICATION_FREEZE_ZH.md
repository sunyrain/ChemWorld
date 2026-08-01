# G2 seed 1 / seed 3 多轨迹复现实验冻结

更新日期：2026-08-01

协议：`g2-electrochemical-autonomous-material-information-seed1-seed3-r5-v0.5`

配置：`configs/benchmark/g2_autonomous_electrochemical_material_seed1_seed3_r5_v0.5_dev.json`

## 为什么下一步不是再扩 world seed

v0.4 已证明环境、逐操作接口、资源账本、provider session 和 exact replay 可以在 10 个 cell 中完整闭环。当前最大的不确定性不再是接口，而是每个 world/arm 只有一条 Codex 轨迹。

seed 1 与 seed 3 的 nominal-minus-opaque 结果方向相反：

| seed | Δbest | Δonline retention | Δmax drawdown | Δterminal/best |
|---:|---:|---:|---:|---:|
| 1 | -.2009 | 0 pp | -.0206 | +.034 |
| 3 | +.3217 | -60 pp | +.1059 | -.184 |

继续增加单轨迹 world 数会混合两种变异：世界机制异质性和模型单次采样异质性。本阶段固定两个已知方向相反的物理世界，每个世界获取五组**全新** arm 轨迹，直接估计“同一世界中轨迹结构是否可复现”。

这不是从两个世界推断总体先验效应，也不是显著性检验。两个 world 是基于开发结果有目的地选取，因此所有结论必须按 world 分层。

## 三个必须分离的实验轴

1. `world_seed` 决定物理机制、材料实例与 keyed observation stream；同一 seed 的所有 replicate 保持完全相同。
2. `replicate_id` 标识一次全新的 Codex provider 轨迹。原生 Codex CLI 不提供可冻结的模型采样 seed，因此 replicate 不是“可复现模型 RNG”，而是独立会话实现的随机轨迹样本。
3. `arm` 只改变材料信息是否提供；资源、模型、reasoning、物理世界、观测流和本地 `agent_seed` 在一个 pair 内保持一致。

`agent_seed` 只绑定本地方法 RNG 与 provenance；不能被误写为控制了 Codex provider 随机性。

## 冻结矩阵

- world：seed 1、seed 3；
- fresh trajectory replicates：每个 world 5 个，`r01`—`r05`；
- arm：opaque、anonymous nominal properties；
- 总计：10 个相邻 pair block，20 个 cell，120 个容器/session。

旧 v0.4 轨迹已经参与 seed 选择和指标设计，**不进入**这五个 fresh replicate 的复现估计量。

pair block 按 replicate 交替 world 顺序，并让两个 world 的 arm-first 顺序互为镜像。全局恰好 5 个 nominal-first 与 5 个 opaque-first；每个 arm pair 必须相邻运行，以降低慢 provider drift。

完整显式顺序保存在配置的 `trajectory_replication.pair_blocks`，runner 不允许按运行时状态重新排序。

## 单 cell 资源不改变

| 资源 | 每 cell | 20 cells 总上限 |
|---|---:|---:|
| fresh vessels / final assay | 6 | 120 |
| non-final instruments | 18 | 360 |
| reagent / solvent stock | .48 mol / .96 L | 各 cell 独立同额 |
| primitive operations | 144 | 2880 |
| Codex sessions | 6 | 120 |

primitive operation 仍是非主要绑定的安全护栏；材料、容器和仪器机会才是主要物理资源控制。

按 v0.4 seed 1/3 四个 cell 的实际用量外推，五组 fresh replication 预计约 1725 次操作、81.8M input tokens、0.368M output tokens。硬 token envelope 仍按每 cell 72M 保留，用于容纳 Codex 多轮累计 input/cache 记账，不代表预计消费。

## 已冻结指标

主要轨迹指标在 fresh run 前已经由 audit v0.3 固定：

- global-best discovery fraction；
- 90% online incumbent retention rate；
- maximum absolute drawdown from prior incumbent；
- terminal-to-global-best ratio；
- loss episode、recovery、recovery delay 与 terminal unresolved；
- batch 级 diagnostic-aligned control change 到下一 final score 的时间对齐。

共同报告而不可互相替代的资源/优化指标：生命周期完成、batch AUC、realized-attempt AUC、fixed-144 AUC、best final 和 mean final。

每个 world 单独报告五个 nominal-minus-opaque 值、median、range 和 sign consistency。禁止只选支持某个故事的 endpoint，也禁止将两个有目的选择的 world 合并为“总体 p 值”。

## 失败 attempt 与恢复规则

长运行必须区分 provider 基础设施 attempt 与统计 trajectory replicate：

1. 每次 attempt 落入不可覆盖的独立目录并进入 manifest。
2. 只有 `provider_infrastructure_failure` 且 `accepted_operation_count == 0` 时，才可自动创建新 attempt；每 cell 最多 3 次。
3. 一旦已有任何 accepted operation，失败即成为该 cell 的 terminal right-censor，不能替换、删除或挑选更好轨迹。
4. 非 provider 的代码、协议、账本或回放失败立即停止审计，不自动重试。
5. completed 或 right-censored cell 永不重跑；resume 只推进冻结 schedule 中尚未 finalise 的 cell。
6. 不允许根据 score、arm difference 或当前故事方向提前停止。

这套规则既避免瞬时 provider 故障浪费一个“零动作轨迹”，也避免在看到部分结果后重抽样造成选择偏差。

## 启动门槛

完整真实矩阵只能在以下条件全部通过后启动：

1. runner 的 manifest 中同时绑定 `world_seed`、`replicate_id`、`agent_seed` 和 arm；
2. dry run 对 10 个 pair block 全部证明物理/观测/资源 identity 一致；
3. resume 测试覆盖零动作 provider retry、动作后 terminal censor、不可覆盖 attempt 和冻结 schedule；
4. replication audit 能按 world/replicate 配对，并拒绝缺 cell、重复 replicate、身份不一致和选择性替换；
5. 一个 K1 或 K2 低成本真实 qualification 证明新 attempt/manifest 路径与原生 Codex MCP 协同正常；
6. 源码、协议和 qualification 证据提交到干净 commit 后，才启动 20-cell run。

## 预期可回答的问题

如果同一 world 的 fresh trajectories 保持相似方向，可以说某种轨迹结构在该物理世界内具有重复性；如果方向大幅翻转，应将原 v0.4 现象解释为单次 agent-world interaction，而不是稳定的先验效应。

无论结果如何，核心产出都不是“LLM 赢了谁”，而是明确区分：世界机制、信息条件与 agent 随机探索轨迹如何共同塑造发现、保留、回撤和恢复。

## 实现与启动状态（2026-08-01）

- 门槛 1 已通过：cell config、pair hash 与 manifest 分别绑定 `world_seed`、`trajectory_replicate_id`、`agent_seed` 和 arm。
- 门槛 2 已通过：10/10 pair block dry run 全部通过；schedule hash 为 `d8c75528c82ea0181b7da880088c3f0663a7f4d1026b9e03d93fe2cc7f0b13af`。
- 门槛 3 已通过：immutable attempt、零动作 provider retry、动作后 right censor、resume 身份验证均有自动化测试。
- 门槛 4 已通过：replication audit 拒绝缺失/重复 replicate、身份篡改和选择性替换；仅对两 arm 都完整的 replicate 计算配对差。
- 静态检查与相关回归已通过：Ruff 全绿；167 passed，1 个与本协议无关的既有测试显式 deselect。
- 门槛 5 尚待真实 K1 qualification；在它通过并随证据形成干净 commit 前，禁止启动 20-cell 正式矩阵。

可复现命令：

```powershell
# 只验证十个物理 pair，不调用 Codex
.\.venv\Scripts\python.exe -m scripts.run_g2_trajectory_replication --dry-run

# 单 cell、单实验的原生 Codex 资格实验（默认 seed 1 / r01 / nominal）
.\.venv\Scripts\python.exe -m scripts.run_g2_trajectory_replication_qualification `
  --allow-external-provider --pair-order 1 --condition nominal --experiments 1

# qualification 通过后才允许启动冻结的 20-cell 矩阵
.\.venv\Scripts\python.exe -m scripts.run_g2_trajectory_replication `
  --allow-external-provider

# 完成后生成 fail-closed JSON 与中文报告
.\.venv\Scripts\python.exe -m chemworld.eval.autonomous_material_replication_audit `
  runs/development/g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1/matrix_manifest.json `
  --json-output runs/development/g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1/audit.json `
  --markdown-output runs/development/g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1/audit_zh.md
```
