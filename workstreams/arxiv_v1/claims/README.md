# Work I 声明认领登记册（历史归档）

> **RETIRED 2026-08-04.** 本目录仅保留旧 Work I 的认领与验收记录。禁止创建新 claim、续租、
> 接管或根据这里的 owner 分配当前工作。当前入口为
> [`../FIRST_PAPER_TODOLIST.md`](../FIRST_PAPER_TODOLIST.md)，当前负责人为 `codex-1`。

本目录记录 `WORK_I_TODOLIST.md` 中任务的认领、心跳、阻塞、交接和验收状态。任务执行者只修改自己的 claim 文件；主 TODO 的汇总状态由 coordinator 更新。

## 认领流程

1. 从 `TEMPLATE.md` 复制一份声明，命名为 `<TASK-ID>--<owner>.md`。
2. 填写 owner、UTC 时间、48 小时租约、base commit、branch/worktree、写集、交付物和验证命令。
3. 单独提交 claim 文件。竞争认领以最早进入 `main` 的有效 claim commit 为准。
4. 开始实现后将状态改为 `ACTIVE`；至少每 24 小时更新一次 heartbeat。
5. 交付后改为 `REVIEW`，附最终 commit、产物路径和验证结果。
6. 独立验收通过并合并后，由 coordinator 将状态改为 `DONE`。

## 租约与接管

- 默认租约为 48 小时；每次有效 heartbeat 可续期。
- 超过 24 小时没有 heartbeat 的 claim 会进入协调检查。
- 租约到期且无法联系 owner 时，coordinator 可释放任务。
- 接管者创建新的 claim 文件，并在 `supersedes` 中引用原声明；原文件保留，不覆盖历史。
- `BLOCKED` 必须记录证据、解除条件、责任方和下一次检查时间。

## 写集纪律

- 声明中列出的 `declared_write_set` 是默认可写边界。
- 修改共享热文件前，必须填写 `shared_hot_file_requests` 并由 coordinator 分配集成窗口。
- 不在自己的任务分支重生成全局 evidence DAG、总 ledger、主论文或 release manifest，除非该任务本身拥有对应热文件。
- raw runs、derived data、报告和代码分别提交，避免将大规模产物混入实现 commit。
- 完成后的 claim 文件构成审计记录，不删除、不重写历史时间线。

以下流程和状态只用于解释历史记录；旧任务矩阵归档于
[`../archive/coordination/WORK_I_TODOLIST_RETIRED_2026-08-04.md`](../archive/coordination/WORK_I_TODOLIST_RETIRED_2026-08-04.md)。
