# 统一任务板

活跃任务源只有仓库根目录的 `TODO.md`。本页只给站点读者一个当前状态摘要，避免站点和仓库根目录维护两套任务板。

## 当前剩余工作

| 范围 | 总数 | 已完成 | 已认领 | 待做 | 剩余 |
| --- | ---: | ---: | ---: | ---: | ---: |
| P0 Pre-release benchmark hardening | 12 | 8 | 0 | 4 | 4 |
| P1 Runtime and environment consistency | 8 | 4 | 0 | 4 | 4 |
| P2 Agent-facing interaction and datasets | 6 | 0 | 0 | 6 | 6 |
| P3 Professional physchem deepening | 27 | 0 | 3 | 24 | 27 |
| P4 Docs, notebooks, site, release packaging | 5 | 0 | 0 | 5 | 5 |
| Total | 58 | 12 | 3 | 43 | 46 |

## 当前优先级

1. `P0-BENCH-09`: build local teacher/student evaluation smoke.
2. `P1-CONSIST-05`: audit campaign vs single-experiment semantics.
3. `P0-BENCH-10`: produce benchmark paper artifact skeleton.
4. `P0-BENCH-11`: add CI-like local release command.
5. `P0-BENCH-12`: write pre-release limitations statement.

## 协作规则

- 开始任务前先拉取 `main`。
- 只认领一个任务，并在根目录 `TODO.md` 中把 owner 和 status 写清楚。
- 完成任务后立即更新 `TODO.md`、提交并推送。
- 不维护第二份活跃 TODO。
- 不把 proxy/lite 工作标记为 professional。

## 发布判断

第一阶段公开预发布不要求完成全部 58 项。真正阻塞发布的是 P0/P1：

- P0/P1 剩余 8 项，是 benchmark trust 的核心。
- P2/P4 剩余 11 项，是可用性和文档包装。
- P3 剩余 27 项，是长期专业物理化学深化。

详细任务、owner、验收标准和状态以根目录 `TODO.md` 为准。
