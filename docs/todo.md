# 统一任务板摘要

活跃任务源只有仓库根目录的 `TODO.md`。本页只给站点读者提供状态摘要，不作为第二份任务板维护。

## 当前判断

公开预发布路线已经完成：P0、P1、P2、P4 均为 Done。当前工作进入 P3 专业物理化学深化。

D4 组已完成：

- D4B：LLE phase-split solver；
- D4C：aqueous acid-base equilibrium；
- D4D：Gibbs-minimization toy solver hardening。

接下来暂停，先讨论后续 P3 优先级。

## 当前统计

| 阶段 | 目标 | 总数 | Done | Claimed | Open | Blocked | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 | 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 | runtime 与环境自洽性 | 8 | 8 | 0 | 0 | 0 | 0 |
| P2 | agent-facing 交互与数据集 | 6 | 6 | 0 | 0 | 0 | 0 |
| P3 | 专业物理化学深化 | 27 | 3 | 3 | 21 | 0 | 24 |
| P4 | 文档、notebook、站点与发布包装 | 5 | 5 | 0 | 0 | 0 | 0 |
| **合计** |  | **58** | **34** | **3** | **21** | **0** | **24** |

## 下一执行队列

P3 剩余 24 项，其中 D1A/D1B/D1C 已由 `liyijun` 认领。Codex 后续应从未认领项中选择，但当前按照用户要求先停在 D4 完成点。

## Cutline

| Cutline | 还差 | 判定标准 |
| --- | ---: | --- |
| 最小可信 benchmark | 0 | P0/P1 全部完成。 |
| 可公开预发布包 | 0 | P2/P4 全部完成。 |
| 全部可见路线图 | 24 | 完成剩余 P3。 |

详细任务、owner、验收标准和状态以根目录 `TODO.md` 为准。
