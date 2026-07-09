# 场景生成

Scenario generation 定义环境在 reset 时如何采样隐藏条件和可见条件。它决定任务是否能
测试泛化，而不是让 agent 记住单个固定实例。

## 合同

一个 scenario generator 应说明：

- 可见参数；
- 隐藏参数；
- seed 使用规则；
- train/eval split；
- 参数范围和物理约束；
- 与 scoring 的关系。

公开 observation 不应泄露隐藏答案。任务卡可以描述采样范围，但不应暴露 private eval
的具体 scenario。

## CLI

未来可提供：

```bash
chemworld scenario sample --task reaction-to-purification --seed 1
chemworld scenario inspect --task reaction-to-purification --public-only
```

## 质量要求

Scenario 应可复现、可序列化、可审计。若一个任务的 scenario 只是一组硬编码常数，它
仍可用于 smoke test，但不应作为正式泛化 benchmark。
