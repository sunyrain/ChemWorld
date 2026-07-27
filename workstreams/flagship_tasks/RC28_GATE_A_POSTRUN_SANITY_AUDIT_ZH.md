# RC28 Gate A 运行后 sanity audit

状态：`completed; interpretive audit only; frozen Gate A artifacts unchanged`

审计日期：2026-07-25

本审计回答正式 RC28 A2/A3 结束后的两个问题：

1. 4,896 个 A2 receipts 和 2,016 个 A3 receipts 分别对应多少真正独立的物理
   world cluster；
2. A2 主预算 `k=5` 下 active oracle 与 fixed decoder 恰好得到相同
   98.26% top-1，是否来自实现上的预测复制或动作选择复用。

本审计不修改协议、世界、动作、预算、阈值、scorer、cohort、正式报告或联合决策。

## 1. 绑定对象

- 冻结环境标签：`mechanism-adaptation-v0.3.0-rc28-gate-a-passed`
- 公开联合决策：
  `workstreams/flagship_tasks/reports/mechanism-adaptation-public-decision-v0.1-rc28.json`
- A2 trial store：
  `runs/mechanism-adaptation-v0.3.0-rc28/confirmatory-trials/a2`
- A3 trial store：
  `runs/mechanism-adaptation-v0.3.0-rc28/confirmatory-trials/a3`
- A2 执行实现：
  `src/chemworld/eval/mechanism_adaptation_execution.py`

trial 唯一键为：

```text
task × truth_family × world_cluster × changepoint × arm
```

receipt 是执行和恢复单元，不自动等于统计独立样本。

## 2. Receipt、trial 与独立 cluster 的口径

### A2

| 组成 | Receipts | task × truth × world 单元 | 独立 task × world clusters |
| --- | ---: | ---: | ---: |
| predictive fit | 576 | 96 | 24 |
| budget 2 certificate | 1,440 | 1,440 | 360 |
| budget 4 certificate | 1,440 | 1,440 | 360 |
| budget 5 certificate | 1,440 | 1,440 | 360 |
| 合计 | 4,896 | — | 384 个 namespace-disjoint fit/certificate clusters |

三个 certificate budget 使用同一组 360 个 held-out task × world clusters，只改变
诊断动作预算；不得把三组 receipt 相加称为 1,080 个独立 held-out worlds。每个 task ×
world cluster 又配对生成四个 truth twins，因此每个 budget 有 1,440 个 trial 单元，但
仍只有 360 个独立物理 clusters。

### A3

| 组成 | Receipts | task × truth × world 单元 | 独立 task × world clusters |
| --- | ---: | ---: | ---: |
| predictive fit | 576 | 96 | 24 |
| online reference-policy certificate | 1,440 | 1,440 | 360 |
| 合计 | 2,016 | 1,536 | 384 个 namespace-disjoint fit/certificate clusters |

A2 与 A3 的 predictive-fit clusters、certificate clusters 两两交集均为 0。正式结果
报告应同时给出 receipt 数、trial 单元数和独立 world-cluster 数，主统计置信区间继续以
world cluster 为重采样单位。

## 3. `k=5` oracle/decoder 重合审计

在 1,440 个 `k=5` certificate trials 中：

| 检查 | 结果 |
| --- | ---: |
| Active oracle errors | 25 |
| Fixed decoder errors | 25 |
| 错误交集 | 25 |
| 错误并集 | 25 |
| Error-set Jaccard | 1.0 |
| Prediction disagreement | 0/1,440 |
| 完全相同的动作列表 | 720/1,440 |
| 完全相同的 pre/post observation seed 对 | 720/1,440 |

25 个共同错误全部来自反应–结晶：

| Truth | 共同预测 | 数量 |
| --- | --- | ---: |
| material mapping | no change | 19 |
| material mapping | rate law | 1 |
| rate law | material mapping | 3 |
| topology | material mapping | 2 |

### 3.1 调用链结论

没有发现 decoder 读取 active-oracle prediction、posterior 或 selection output 的代码路径：

- active batch 由所有合格 batch 的冻结 expected information gain 排名选择；
- decoder batch 固定为公共动作序列的前 `k` 个动作；
- 两个角色分别 reset posterior 后执行同一冻结 Gaussian decoder；
- 当 batch ID 不同时，各自使用由 batch ID 派生的独立 observation seed；
- 当 batch ID 相同时，执行器有意复用同一个 paired contrast，避免把同一证据重复采样后
  制造虚假的方法差异。

### 3.2 为什么有 720 条完全相同

- 电化学：active 使用 `design-00+02+03+04+05`，fixed decoder 使用
  `design-00+01+02+03+04`；720 条 trial 的动作、种子和 posterior 均不同。
- 反应–结晶：active information maximum 恰好也是
  `design-00+01+02+03+04`；因此 720 条 trial 的 active 与 decoder 实际上观察同一个
  witness batch，动作、种子、posterior 和 prediction 必然相同。

所以 98.26% 的完全一致不是预测字段被复制，但 fixed decoder 在反应–结晶 `k=5` 上也
不是独立轨迹复现。它只能被解释为辅助一致性检查。

## 4. 对 Gate A 解释等级的影响

此发现不改变 RC28 Gate A 决策，理由是：

1. A2 的 gate-controlling 证书始终是 active oracle；
2. `fixed_trajectory_decoder.controls_gate=false` 已在正式报告中冻结；
3. A3 是独立 cohort 上的冻结在线 reference policy 证书；
4. A2 与 A3 的正式 cohort 无交集。

允许的表述是：

> 在 `k=5` 的受控预算下，active oracle 通过 A2；固定 decoder 提供辅助一致性结果。
> 电化学的两个 batch 不同，反应–结晶的两个角色在该预算下收敛到同一 witness batch。

不再使用以下过强表述：

> active oracle 与 fixed decoder 构成两个完全独立的 A2 复现证书。

## 5. 软件运行资格边界

正式执行前，冻结 commit 已在 clean detached worktree 中完成针对 A2/A3 生产路径的
qualification、零作业入口检查和 61 项定向集成测试。正式 trial manifests、hash、schema、
stderr 和 joint-decision binding 均已核对。

尚未在正式结果标签上执行的额外 reviewer-assurance 项包括：

- 全仓测试；
- 从 wheel 安装后的完整 smoke；
- 从抽样 raw receipts 重建并逐位比较正式表。

这些项目列为 post-run software qualification，不得修改或选择性重跑 A2/A3 科学 trial。
遵循当前仓库测试策略，日常改动只运行相关定向测试；如论文提交前决定执行全仓资格测试，
应在 detached checkout 中单独运行并生成 attestation。

## 6. 最终判断

- Gate A 结果不需要作废或重跑。
- A2/A3 的独立 cluster 口径需要在论文表格中显式报告。
- fixed decoder 的证据角色需要降格为非控制性的辅助一致性检查。
- 不再改动 Gate A；下一阶段只冻结 participant-Agent 方法、runner、统计和成本合同。
