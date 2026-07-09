# 当前进展

ChemWorld 当前已经从单一任务原型推进到统一世界律下的多任务 benchmark 雏形。核心问题
不再是“能否创建环境”，而是如何把 public contract、环境自洽性、任务成熟度和发布站点
一起收束。

## 阶段总结

- 正式 Gymnasium 入口为 `ChemWorld`。
- 任务通过 `task_id` 选择，共享 `world_law_id`。
- Runtime V2、typed ledger、transaction record 和 instrument observation 已形成主线。
- 文档站已经改为中文优先，并保留英文首页入口。
- 环境自洽性审计脚本已加入发布流程。

## 已实现能力

- 反应、分离、表征、安全、机理、连续流、电化学和 tool-agent planning 任务切片。
- Action schema 和 recipe 运行。
- 约束 flags：安全、成本、选择性、前置条件、constitution 等。
- 虚拟仪器和虚拟光谱。
- replay 和 smoke trajectory 检查。
- 任务卡与 maturity metadata。

## 已注册任务族

详见 [任务卡](task_cards.md) 和 [任务](tasks.md)。当前任务覆盖从单步优化到反应-纯化
闭环流程的多种能力。

## 验证状态

推荐当前 gate：

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

## 成熟度边界

当前系统仍应被称为 research benchmark / virtual chemical world model gym，而不是
真实反应预测器、DFT wrapper、流程模拟器或机器人控制器。所有公开 claim 都要携带
maturity。

## 已知风险

- 部分物理模块仍是 proxy/lite。
- 任务奖励和 measurement timing 需要继续用强 baseline 压测。
- 文档仍有历史审计页偏长，需要后续迁移到 archive 或 audits。
- 英文完整镜像尚未逐页维护，目前中文站点是发布主入口。

## 建议下一步

1. 增加三个端到端 notebook：`reaction-to-assay`、`reaction-to-purification`、`partition-discovery`。
2. 最后冻结发布检查表、已知限制、citation 和 private-eval 政策。
