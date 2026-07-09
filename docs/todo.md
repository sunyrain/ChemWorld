# 统一任务板摘要

活跃任务源只有仓库根目录的 `TODO.md`。本页只给站点读者提供当前状态摘要，避免维护两套任务板。

## 当前判断

ChemWorld 已完成 **最小可信 benchmark** 的 P0/P1 收束：核心任务、baseline、submission、replay、release gate、runtime boundary audit、ledger audit、public leakage audit 和环境自洽性审计已经闭环。

下一步分两条线：

- **公开预发布包**：先完成 P2 agent-facing 交互与数据集，再直接完成 P4 文档/notebook/站点。
- **长期专业化路线**：P3 专业物理化学模块深化暂缓，不阻塞当前公开预发布。

## 当前统计

| 阶段 | 目标 | 总数 | Done | Claimed | Open | Blocked | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 | 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 | runtime 与环境自洽性 | 8 | 8 | 0 | 0 | 0 | 0 |
| P2 | agent-facing 交互与数据集 | 6 | 6 | 0 | 0 | 0 | 0 |
| P3 | 专业物理化学深化 | 27 | 0 | 3 | 24 | 0 | 27 |
| P4 | 文档、notebook、站点与发布包装 | 5 | 0 | 0 | 5 | 0 | 5 |
| **合计** |  | **58** | **26** | **3** | **29** | **0** | **32** |

还需要完成 **32 项**：

- **5 项**用于公开预发布：P4 全部 5 项。
- **27 项**用于长期专业化深化：P3 全部 27 项，其中 3 项已由 `liyijun` 认领。

## 下一执行队列

1. `P4-DOCS-01`：reorganize docs around pre-release benchmark。
2. `P4-DOCS-02`：build concise architecture report from current code。
3. `P4-DOCS-03`：harden 12-day tutorial workload。
4. `P4-DOCS-04`：add three end-to-end notebooks。
5. `P4-DOCS-05`：finalize release checklist page。

## Cutline

| Cutline | 还差 | 判定标准 |
| --- | ---: | --- |
| 最小可信 benchmark | 0 | P0/P1 全部完成。 |
| 可公开预发布包 | 5 | 完成 P2/P4。 |
| 全部可见路线图 | 32 | 完成 P2/P3/P4。 |

详细任务、owner、验收标准和状态以根目录 `TODO.md` 为准。
