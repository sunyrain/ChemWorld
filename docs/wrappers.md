# Wrapper 与合法性信号

Wrappers 用于增强 agent 训练和调试体验，但不改变底层任务语义。

## ActionMaskWrapper：动作掩码

提供当前状态下可能合法的 operation mask。它适合 RL 或搜索 agent 使用，但正式评测
需要声明是否允许 agent 读取该 mask。

## SafetyCostWrapper：安全与成本

把 safety 和 cost 信号整理成更直接的 observation 或 reward component。用于训练时很
方便，但不要掩盖原始 `constraint_flags`。

## NaNObservationWrapper：观测检查

检查 observation 中的 NaN、inf 或形状异常。发现异常时应给出明确错误或诊断信息。

## 事件合法性校验 Helper

事件验证 helper 可用于检查 recipe 中每一步是否满足前置条件。它适合教程、baseline
开发和调试，不应成为 agent 绕过环境交互的 oracle。
