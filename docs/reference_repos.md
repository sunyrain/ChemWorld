# 本地参考仓库

本页记录可用于 ChemWorld 物理化学深化的外部开源项目。它们不是当前 benchmark 的硬
依赖，而是 future backend、reference validation 和专业化路线的参考。

## 本地快照

建议在 `references/` 或外部工作区维护只读快照，并记录 commit、license 和用途。不要
把大体积第三方仓库直接混入 ChemWorld 主包。

## 重建快照

```bash
git clone <repo-url> references/<name>
git -C references/<name> rev-parse HEAD
```

把 commit 写入文档或 manifest，确保以后能复现阅读和校准上下文。

## 阅读地图

- RMG-Py：反应网络、动力学、机理生成。
- IDAES：过程系统工程、单元操作、优化。
- teqp：热力学性质和 equation of state。
- thermopack：相平衡和物性。

## 贡献者规则

- 不直接复制第三方代码进核心包，除非 license 和维护策略明确。
- 先写 adapter/interface，再接具体 backend。
- 引入参考模型时必须增加测试和 maturity 标注。

## 可选验证层

参考仓库可用于抽样校准，不要求每个 step 都调用外部重型模拟器。核心 benchmark 仍应
保持轻量、可复现、可离线运行。
