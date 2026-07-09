# 统一任务板摘要

活跃任务源只有仓库根目录的 `TODO.md`。本页只给站点读者提供当前状态摘要，避免维护两套任务板。

## 当前判断

ChemWorld 已完成 **最小可信 benchmark** 的 P0/P1 收束：核心任务、baseline、submission、replay、release gate、runtime boundary audit、ledger audit、public leakage audit 和环境自洽性审计已经闭环。

下一步分两条线：

- **公开预发布包**：完成 P2 agent-facing 交互与数据集、P4 文档/notebook/站点。
- **长期专业化路线**：推进 P3 专业物理化学模块深化，每个模块必须有 maturity、适用范围、验证算例和失败边界。

## 当前统计

| 阶段 | 目标 | 总数 | Done | Claimed | Open | Blocked | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 | 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 | runtime 与环境自洽性 | 8 | 8 | 0 | 0 | 0 | 0 |
| P2 | agent-facing 交互与数据集 | 6 | 4 | 0 | 2 | 0 | 2 |
| P3 | 专业物理化学深化 | 27 | 0 | 3 | 24 | 0 | 27 |
| P4 | 文档、notebook、站点与发布包装 | 5 | 0 | 0 | 5 | 0 | 5 |
| **合计** |  | **58** | **24** | **3** | **31** | **0** | **34** |

还需要完成 **34 项**：

- **7 项**用于公开预发布：P2 剩余 2 项 + P4 全部 5 项。
- **27 项**用于长期专业化深化：P3 全部 27 项，其中 3 项已由 `liyijun` 认领。

## 下一执行队列

1. `P2-AGENT-05`：multi-round ToolUsingLLMStub probe。
2. `P2-AGENT-06`：LLMReplay benchmark fixture。
3. `P4-DOCS-01`：reorganize docs around pre-release benchmark。
4. `P4-DOCS-02`：build concise architecture report from current code。
5. `P4-DOCS-03`：harden 12-day tutorial workload。

## Cutline

| Cutline | 还差 | 判定标准 |
| --- | ---: | --- |
| 最小可信 benchmark | 0 | P0/P1 全部完成。 |
| 可公开预发布包 | 7 | 完成 P2/P4。 |
| 全部可见路线图 | 34 | 完成 P2/P3/P4。 |

详细任务、owner、验收标准和状态以根目录 `TODO.md` 为准。
