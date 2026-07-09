# 统一任务板摘要

活跃任务源只有仓库根目录的 `TODO.md`。本页只给站点读者一个当前状态摘要，避免维护两套任务板。

## 当前阶段

ChemWorld 当前处在 **benchmark trust hardening** 收束阶段。P0 预发布 benchmark hardening 和 P1 runtime / environment self-consistency 已完成；下一步重点转入 P2 agent-facing 交互和 P4 站点、notebook、发布包装。

## 当前统计

| 阶段 | 目标 | 总数 | 已完成 | 已认领 | 待开始 | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| P0 | 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 |
| P1 | runtime 与环境自洽性 | 8 | 8 | 0 | 0 | 0 |
| P2 | agent-facing 交互与数据集 | 6 | 0 | 0 | 6 | 6 |
| P3 | 专业物理化学深化 | 27 | 0 | 3 | 24 | 27 |
| P4 | 文档、notebook、站点与发布包装 | 5 | 0 | 0 | 5 | 5 |
| **合计** |  | **58** | **20** | **3** | **35** | **38** |

还需要完成 **38 项**。其中 **35 项尚未开始**，**3 项已由 liyijun 认领但未完成**。

## 下一执行队列

1. `P2-AGENT-01`：polish `task_prompt()` for the three pre-release tasks。
2. `P2-AGENT-02`：improve lab-report summaries。
3. `P2-AGENT-03`：stabilize RL observation view。
4. `P2-AGENT-04`：add agent trace to dataset export examples。
5. `P4-DOCS-01`：reorganize docs around pre-release benchmark。

## Cutline

| Cutline | 剩余 | 定义 |
| --- | ---: | --- |
| 最小可信 benchmark | 0 | 完成全部 P0/P1。 |
| 可公开预发布包 | 11 | 完成 P0/P1/P2/P4。 |
| 全部可见路线图 | 38 | 包含长期 P3 专业物理化学深化。 |

详细任务、owner、验收标准和状态以根目录 `TODO.md` 为准。
