# 统一任务板摘要

活跃任务源只有仓库根目录的 `TODO.md`。本页只给站点读者一个当前状态摘要，避免维护两套任务板。

## 当前结论

ChemWorld 当前已经进入 benchmark trust hardening 阶段。短期重点不是继续扩展新任务，而是收束任务合同、ledger、观测泄漏、runtime 边界、agent 交互和公开预发布文档。

当前剩余工作：

- 总任务 58 项。
- 已完成 17 项。
- 进行中 1 项。
- 已认领 3 项。
- 待开始 37 项。
- 剩余 41 项。

## 当前统计

| 范围 | 总数 | 已完成 | 进行中 | 已认领 | 待开始 | 剩余 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 runtime 与环境自洽性 | 8 | 5 | 1 | 0 | 2 | 3 |
| P2 agent-facing 交互与数据集 | 6 | 0 | 0 | 0 | 6 | 6 |
| P3 专业物理化学深化 | 27 | 0 | 0 | 3 | 24 | 27 |
| P4 文档、notebook、站点与发布包装 | 5 | 0 | 0 | 0 | 5 | 5 |
| Total | 58 | 17 | 1 | 3 | 37 | 41 |

## Cutline

| Cutline | 剩余 | 含义 |
| --- | ---: | --- |
| 最小可信 benchmark | 3 | 完成全部 P0/P1 |
| 可公开预发布包 | 14 | 完成 P0/P1/P2/P4 |
| 全部可见路线图 | 41 | 包含长期 P3 专业物化深化 |

## 下一轮优先级

1. `P1-CONSIST-06`：ledger single-source-of-truth audit。
2. `P1-CONSIST-07`：public observation leakage audit。
3. `P1-CONSIST-08`：runtime boundary scan。

## 协作规则

- 从 `main` 开发，开始任务前先拉取远端。
- 每次只把一个任务标记为 `Active`。
- 完成任务后立即更新根目录 `TODO.md`、提交并推送。
- 不维护第二份活跃 TODO。
- 不把 `proxy`、`lite` 或 `professional-candidate` 模型写成 `professional`。

详细任务、owner、验收标准和状态以根目录 `TODO.md` 为准。
