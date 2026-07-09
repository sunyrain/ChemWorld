# 统一任务板摘要

活跃任务源只有仓库根目录的 `TODO.md`。本页只给站点读者一个当前状态摘要，避免维护两套任务板。

## 当前结论

ChemWorld 当前不是功能数量不足，而是需要继续提高 benchmark trust：任务合同、评分、回放、提交包、文档和成熟度边界还要收束。

当前剩余工作：

- 总任务 58 项，已完成 16 项，剩余 42 项。
- 公开预发布最关键的是 P0/P1，剩余 4 项。
- 可用的公开预发布包需要完成 P0/P1/P2/P4，剩余 15 项。
- P3 是长期专业物理化学深化，剩余 27 项，不应阻塞第一版公开预发布。

## 当前统计

| 范围 | 总数 | 已完成 | 进行中 | 已认领 | 待做 | 剩余 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 Pre-release benchmark hardening | 12 | 11 | 0 | 0 | 1 | 1 |
| P1 Runtime and environment consistency | 8 | 5 | 0 | 0 | 3 | 3 |
| P2 Agent-facing interaction and datasets | 6 | 0 | 0 | 0 | 6 | 6 |
| P3 Professional physchem deepening | 27 | 0 | 0 | 3 | 24 | 27 |
| P4 Docs, notebooks, site, release packaging | 5 | 0 | 0 | 0 | 5 | 5 |
| Total | 58 | 16 | 0 | 3 | 39 | 42 |

## 下一轮优先级

1. `P0-BENCH-12`: write pre-release limitations statement.
2. `P1-CONSIST-06`: audit ledger single-source-of-truth.
3. `P1-CONSIST-07`: audit public observation leakage.
4. `P1-CONSIST-08`: scan runtime boundaries.

## 协作规则

- 开始任务前先拉取 `main`。
- 每次只认领一个任务，并在根目录 `TODO.md` 写清 owner 和 status。
- 完成任务后立即更新 `TODO.md`、提交并推送。
- 不维护第二份活跃 TODO。
- 不把 proxy/lite 工作标记为 professional。

详细任务、owner、验收标准和状态以根目录 `TODO.md` 为准。
