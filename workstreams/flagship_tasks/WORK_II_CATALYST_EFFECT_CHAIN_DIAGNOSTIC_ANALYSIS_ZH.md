# Work II 催化剂效应链诊断分析

日期：2026-08-12

## 结论

本次 provider-free seed-0 诊断完成 `63/63` 主执行、`63/63` 确定性投影复现和
`63/63` 官方 exact replay，0 execution failure。所有运行时门禁均通过：催化剂加料、库存守恒、
稳定拓扑、破坏性采样、HPLC 采样时点、fresh-batch reset 与 replay 均未发现实现缺陷。

旧 W2-33/W2-34 的弱效应不能归因于平台错误。催化剂相对无催化剂的最大 noiseless yield
效应为 `0.36470`，证明催化功能真实存在；但 stable 相对 deactivating 的最大 yield 差仅
`0.00620`，0 个 public cells 达到既定 W2-33 effect gate。9 个高温比较中没有一个达到冻结的
deactivation-specific difference-in-differences 门槛，且 deactivating law 在所有剂量下仍保留至少
约 `83.28%` active catalyst。

## 归因

- **实验设计遮蔽**：每次 complete experiment 从 fresh batch 开始，催化剂老化不能跨轮累积；
  现有 participant lifecycle 因而只暴露单批次内的部分失活。
- **endpoint compression**：5 个 cell 的 integrated target-formation gap 明显大于终点 yield gap，
  说明终点压缩了中间过程差异。
- **任务/机制可辨识性不足**：stable-vs-deactivating 差异远低于冻结 public gate，不能支撑 A-S。
- **参数校准不足**：冻结的高温失活 tradeoff 在 9 个 cell 中均不稳健。

因此保留 W2-33/W2-34 的科学拒绝，不调整既有阈值，不扩展五 worlds，也不生成 participant
配置。后续 A-S 应转向独立预先冻结、能够在单批次公开测量中直接产生可辨识效应的候选。

机器证据：`workstreams/flagship_tasks/reports/work-ii-catalyst-effect-chain-diagnostic-20260812.json`。
