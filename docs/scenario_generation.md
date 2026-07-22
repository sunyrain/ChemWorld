# 场景如何生成

Scenario 是一个 Task 与隐藏 World 的具体组合，再加入初态、干预计划、reset/反馈条件和 seed。一次
reset 实例化该 Scenario；它决定 Agent 是在适应新规律，还是只面对同一世界中的随机变化。

## Scenario 合同应说明

- 哪些参数对 Agent 可见，哪些保持隐藏；
- seed 如何映射到可复现实例；
- Train、Dev、Bench 与 Private 如何划分；
- 参数范围、物理约束与评分关系；
- mechanism/world family 如何分配。

换 seed 主要测试实例随机性；切换 mechanism family 才能测试预先定义的机制轴变化。Private eval
还需要独立 salt，不能把隐藏答案泄露到 observation、错误文本或公开任务卡。

## 什么样的 Scenario 才适合研究

它应当可复现、可序列化、可审计，并让合理策略产生可辨识差异。只有一组硬编码常数的场景仍可用于
smoke test，但不应被包装成泛化 benchmark。

命令行查看 seed 计划：

```bash
chemworld seeds show --all-tasks
```

数据划分细节见[管理 Seed 与数据划分](seed_suite.md)。
