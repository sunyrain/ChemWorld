# 第一篇确定性使用案例实验说明

状态：**FROZEN BEFORE DATA GENERATION**  
执行者：**Codex `/root`**  
任务：**U01、U02、U03/E01、U06**

## 问题与独立单位

问题：在不修改核心 runtime、不调用模型 provider 的前提下，预先选定的多阶段、资源受限、失败恢复和
参考案例路径，能否只通过公开任务/组合契约完成事务执行、资源对账、生命周期闭合和精确 replay？

独立单位是下列 8 个确定性案例，不把动作、测量或 replay 当作独立样本：

| Case | 公开身份 | Seed | 冻结路径 | Submitted actions |
| --- | --- | ---: | --- | ---: |
| U01 | `reaction-to-crystallization` | 0 | 公开 task-recipe 全维 0.5 中点 | 12 |
| U02 | `composed-equilibrium-characterization-demo` | 0 | `use-case-reference-paths-v0.1.json` 的 U02 actions | 5 |
| U03/E01 | `composed-reaction-purification-demo` | 0 | 同一 sidecar 的 U03 actions；首步为预期失败 | 19 |
| U06-flow | `flow-reaction-optimization` | 0 | 公开 task-recipe 全维 0.5 中点 | 8 |
| U06-electro | `electrochemical-conversion` | 0 | 公开 task-recipe 全维 0.5 中点 | 11 |
| U06-distillation | `reaction-to-distillation` | 0 | 公开 task-recipe 全维 0.5 中点 | 12 |
| U06-partition | `partition-discovery` | 0 | 公开 task-recipe 全维 0.5 中点 | 10 |
| U06-crystallization | `reaction-to-crystallization` | 1 | 公开 task-recipe 全维 0.5 中点 | 12 |

总分母固定为 8 cases、89 submitted actions、88 expected commits、1 expected rollback 和 8 final assays。
U04 只复用既有 single-private-component fork 正式证据；U05 的确定性参考部分只复用 C03 正式报告中生成顺序
第一项，不在本实验替换或重跑。U05/E02 的完整 agent 生命周期另写实验说明。

## 测量与通过规则

每个案例保存规范化公开请求或任务合同、seed、冻结动作列表、逐步 schema/validate 判定、事务状态、公开观测
摘要、constitution checks、world events、资源 preflight/outcome、终止/评价回执、公开/私有泄漏检查、耗时、
轨迹字节数和 exact replay 结论。

通过要求：

- 8/8 案例完成；submitted/committed/rollback/final-assay 分母精确为 89/88/1/8；
- U03 第 1 步必须因 `precondition_failed` 回滚，物理状态不变，失败 penalty、process/ledger 和资源回执对账；
- U03 后续 18 步及其余 7 个案例的全部动作均提交，无额外失败；
- 每个案例恰有一个 committed final assay，生命周期闭合，资源声明与实际结果一致；
- 公共输出无私有状态泄漏，8/8 trajectory exact replay 通过；
- 任何缺失回执、非有限测量、意外 rollback/commit、分母漂移或 replay 失败使总体状态为 `FAILED`。

一旦执行开始，不得改变 case、seed、中点向量、sidecar actions、预期失败位置或 pass/failure 规则。平台缺陷修复
后必须从 U01 开始整批重跑，旧失败报告保留。

## 预期输出

- `workstreams/arxiv_v1/reports/first-paper-deterministic-use-cases-v1.json`；
- 同路径 Markdown 摘要，列出精确分母、全部失败、逐案例资源/终止/replay 状态和 U04/U05 既有证据引用；
- 不创建额外 manifest，不保存 raw provider payload，因为本实验没有 provider 调用。
