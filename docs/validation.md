# 验证安装与结果

验证分成三个尺度：检查单条轨迹、检查提交包、确认发布证据。使用者只需通过公开 CLI 完成前两层；
发布候选的工程与科学门禁由发布方在版本证据中声明。

## 我刚跑完一条轨迹

```bash
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

这会检查 schema、合同、状态守恒与 replay，并从轨迹重算指标。

## 我要检查提交包

```bash
chemworld submission validate runs/example_submission
chemworld submission summarize runs/example_submission
```

提交包验证会检查 manifest、轨迹、结果、解释和依赖说明是否互相绑定。摘要只读取公开证据，不会
暴露隐藏 world state。

## 我要判断一个发布候选是否可信

检查发布页是否同时给出 source commit、clean-tree 状态、backend/world-law/task-contract 版本、15 个任务
哈希、轨迹归档、统计摘要和独立复现状态。软件检查、科学证据和正式 benchmark 声明是三个不同层级；
缺少任一层时，都不应把“可运行”升级为“方法优越”。

## 物理与数值证据如何分层

1. 用解析解和守恒式检查简单极限。
2. 用单元测试固定模型行为和错误边界。
3. 用可选专业参考后端对照局部性质、动力学或传递切片。
4. 用 runtime integration 确认模型真的进入 Gym 状态转移。
5. 用冻结 trajectory 检查版本化世界律的端到端行为。

参考依赖缺失时，对应验证应显示为 skipped 或 unavailable，而不是被当作通过。

## 结果为什么能够复现

Trajectory、submission manifest 与 dataset card 会记录任务、场景、机理、世界律、runtime profile、
observation/scoring contract、依赖环境和源码摘要。`chemworld verify` 使用这些字段发现合同漂移或
轨迹修改。

发布 artifact 的完整要求见[验证结果可信度](release_integrity.md)。
