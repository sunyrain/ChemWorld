# Work II 催化剂失活双真实-provider campaign 分析

日期：2026-08-12

## 1. 执行定义与完整性

本轮按澄清后的定义执行两个独立 campaign，而不是一个 session 内的两次实验：

- reaction-safety world seed 0；
- `deactivating_baseline` 与 `stable_catalyst` 各一个独立 WellAU `gpt-5.6-sol` medium
  持久 Codex session；
- 每个 session 自主完成 8 次完整实验，共 `2/2` sessions、`16/16` experiments、`112/112`
  committed operations；
- 两边公共任务、opaque 材料信息、模型、reasoning、资源、checkpoint、agent seed 与 keyed-noise
  namespace 完全一致；唯一设计差异是 host-owned 固定物理定律；
- 两边均完成 `5/5` typed checkpoints、最终 recommendation 与 `56/56` exact replay；
- 失活侧为 8 个 unique recipes、0 exact repeat；稳定侧为 7 个 unique recipes、1 exact repeat；
- 0 provider error、0 resource rejection、0 platform failure。稳定侧曾有一次 checkpoint schema 错误：
  模型在线性 law term 中多写了 `category_value`，随后在同一 session 内修正并完成；这不是物理或 provider
  故障。

真实 provider 合计耗时 `783.927 s`。资源收据为：

- input `2,028,593` tokens；
- cached input `1,778,176`，uncached input `250,417`，合计 cache hit ratio 约 `87.66%`；
- output `19,986` tokens；
- 两个 Codex campaign 各只有一个完整 provider turn/session。缓存 token 是重复上下文的复用输入，
  不是重复生成的模型输出。

此前 source commit `5d6da7f5` 下完成的 `1 session x 2 experiments` 是需求范围误解产生的 development
pilot。它永久保留，但不进入本轮任何分母、效应计算或结论。

## 2. 两个自主 campaign 的描述性闭环差异

失活侧 8 轮 mean/best score 为 `0.05208/0.08629`；稳定侧为 `0.08534/0.13191`，稳定侧的
mean/best 差分别为 `+0.03326/+0.04562`。稳定侧前四轮 mean score 为 `0.04148`，后四轮为
`0.12920`，development gain 为 `+0.08772`；失活侧对应为 `0.05273 -> 0.05143`，gain
`-0.00130`。

若仅按相同轮次比较两个独立 session 的公开终点，`5/8` 轮至少一个 yield/conversion/selectivity
绝对差超过 W2-33 reference gate，`4/8` 轮至少两个指标超过；最大 round-wise gaps 为：

| 指标 | 最大绝对闭环 gap | Reference gate | 最大值所在轮次 |
|---|---:|---:|---:|
| yield | `0.15301` | `0.050` | 5 |
| conversion | `0.23939` | `0.050` | 5 |
| selectivity | `0.12313` | `0.054` | 6 |

因此，如果“真实 provider 差异”指两个完整 agent-system 的自主行为—结果轨迹，观察值确实可以明显超过
gate；后四轮尤其出现稳定侧更高 score 的持续分岔。

但这不是纯物理因果证明。两个 session 在第 1 轮、尚未获得任何物理结果前就选择了不同配方，且 `8/8`
同轮 recipe pairs 均不相同。上述 gap 同时混入 provider 随机性、早期探索选择、后续路径依赖和固定物理定律，
不能全部归因于催化剂失活。

## 3. 16 个真实-provider 配方的严格成对物理重放

为隔离固定物理定律效应， evaluator 将两个 session 产生的全部 16 个 recipes 分别在失活与稳定世界中
重放，共 `16 x 2 = 32/32` provider-free executions：

- 32/32 completed；
- 32/32 intervention-aware exact replay；
- 0 platform/physical failures；
- 每一对使用完全相同 action plan、world seed 与 keyed-noise binding；
- 16/16 pairs 的 mechanism hash 均随稳定拓扑 intervention 改变。

稳定减失活的 yield、conversion、selectivity 在全部 16 个配方中均为正，说明失活通道的因果方向真实且
稳定。但效应仍显著低于冻结 gate：

| 指标 | 16 个 provider-selected recipes 中最大 gap | Gate | Gate ratio | 超过 gate |
|---|---:|---:|---:|---:|
| yield | `0.010257` | `0.050` | `0.205x` | `0/16` |
| conversion | `0.012261` | `0.050` | `0.245x` | `0/16` |
| selectivity | `0.008993` | `0.054` | `0.167x` | `0/16` |

因此：

- `at_least_one_primary_metric_exceeds_frozen_gate = false`；
- `w2_33_two_metrics_same_recipe_effect_gate = false`；
- 没有任何真实-provider 选择的配方在固定动作的纯物理比较中超过任一 primary gate；
- 本轮不能证明“真实 provider 找到一个让 stable-vs-deactivating 纯物理差异超过 gate 的区域”，也不推翻
  W2-33 的科学拒绝。

## 4. 科学含义

本轮得到的不是预期的简单正结论，而是一个更明确的层次分离：

1. **固定动作的机制效应小。** 在真实 provider 选择的 16 个点上，stable catalyst 始终改善公开终点，
   但最大效应只有冻结 gate 的 `16.7%–24.5%`。
2. **闭环轨迹可以大幅分岔。** 两个自主 session 的 later-round behavior 和 score 出现明显差异，部分终点
   gap 超过 reference gate；这表明微小观测差异与 agent 自适应、路径依赖和 provider 随机性共同作用时，
   system-level divergence 可以远大于 fixed-action physics effect。
3. **当前设计不能把闭环放大归因于物理定律。** 因为两边从首轮配方即不同，缺少 within-law provider
   repeats 或同一随机决策流的可控分支。闭环差异是有价值的观察，但不是稳定催化剂优于失活催化剂的因果
   effect estimate。
4. **W2-33 gate 没有被证明过高。** 新结果重复说明当前失活机制在公开终点上的直接效应约为百分之一量级；
   若论文要研究“agent 是否因微弱世界差异发生行为分岔”，应将 estimand 改为 trajectory sensitivity/path
   dependence，而不是把 system-level 分岔冒充同配方 mechanism identifiability。

若后续要因果识别闭环放大，需要在新 experiment note 中预先冻结每种 law 的多个 provider repeats，或实现
common-prefix branching，使两个 session 在首个不同物理 observation 之前共享相同决策前缀；不能用本轮单个
session/law 事后消除 provider 随机性。本轮不追加运行。

机器摘要：`workstreams/flagship_tasks/reports/work-ii-catalyst-deactivation-paired-provider-seed0-20260812.json`。
