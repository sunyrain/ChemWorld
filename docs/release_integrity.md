# 验证结果可信度

一个结果之所以可信，不是因为 JSON 里写着 `verified=true`，而是因为它可以从明确源码和合同出发，
沿着原始轨迹重新得到同样的指标。

## 一条完整的信任链

```text
source commit + clean tree
  → wheel 与依赖环境
  → 版本化任务 / 场景 / 机理 / 评价合同
  → trajectory JSONL
  → schema + constitution + deterministic replay
  → 重算指标并绑定 trajectory SHA-256
  → 逐任务统计
  → public release 或签名 private aggregate
```

任何一环缺失，都应降低结果状态，而不是靠下游文件补一个“通过”字段。

## Evaluation Result 记录什么

`chemworld-evaluation-result-0.3` 将结果与来源绑定，包括：

- 完整任务指标与阈值；
- replay report 和 `verified` 状态；
- trajectory 路径与 SHA-256；
- score replay 版本、源记录数和 layered evaluation；
- 风险语义、完整实验数和资源账本。

验证器会重算轨迹摘要、回放状态、指标和 score binding。修改轨迹、结果字段、阈值或合同后，绑定
应失效。包内相对路径用于迁移后的重新绑定，绝对路径不是结果身份。

## 把资源也纳入完整性

不同方法要报告同一组资源：完整实验、操作、测量、墙钟、CPU/GPU、训练步、模型请求、token 与
费用。LLM 的失败请求和重试也要计数；RL 的训练过程与冻结评测必须分开。

## Private Eval 如何保密

私有评测由维护者持有高熵 secret，并只发布允许公开的签名聚合结果。仓库和网站中不应出现 secret、
salt 原值、隐藏 seeds、逐条私有轨迹或可逆世界参数。

## 第三方代码需要额外隔离

本地评测机使用 `trusted-local-subprocess`，适合课程与可信代码。面对未知提交时，还需要外部容器或
沙箱提供无网络、只读挂载、低权限以及 CPU、内存、PID 和时间限制。

## 发布候选必须公开什么

发布页应绑定 source commit、clean-tree 状态、backend/world-law/task-contract 版本、逐任务哈希、完整
trajectory archive、统计摘要、依赖快照和独立复现状态。使用者可以据此确认下载内容与结果表属于
同一候选版本，而不需要运行仓库维护脚本。

!!! warning "工程全绿不等于论文结论成立"
    软件门禁、科学证据和正式发布是三个层级。严格冻结发布必须绑定 source commit、clean tree、
    当前 task contract、完整 trajectory archive、统计摘要、私有签名与独立复现。
