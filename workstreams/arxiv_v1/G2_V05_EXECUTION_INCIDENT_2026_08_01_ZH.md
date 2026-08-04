# G2 v0.5 第一次正式启动：基础设施中断记录

> **LEGACY INCIDENT — 非当前任务。** 仅为历史运行事件记录，不得据此重启旧矩阵或创建新的
> G2 工作。当前入口为 [`FIRST_PAPER_TODOLIST.md`](FIRST_PAPER_TODOLIST.md)。

状态：`excluded infrastructure incident; retained immutably`

## 结论

2026-08-01 23:30（Asia/Shanghai）启动的第一次 G2 v0.5 矩阵不能进入确认性分析。冻结协议本身没有失败：`cell-001` 已完成 6 个容器并生成完整摘要、账本和精确回放；但外层 detached Python 进程随后在 `cell-002` 的第 4 个已接受操作后消失。该单元没有 `run_summary.json`，标准状态机因此只能把它判为 `audit_required`。

整个第一次启动均被排除，不从中提取科学结果，也不把已经完成的 6 个容器计入论文实验总数。原始目录保持不可修改，作为运行基础设施事件证据。

## 冻结身份

- source commit：`f539bfa7af5e3846ef56a842fd56b990cdd8bd07`
- protocol SHA-256：`2d2685b67c47a276c9b7eb7e3575313fe264dfc6ba65d708d60e0a98e8127cbf`
- schedule SHA-256：`d8c75528c82ea0181b7da880088c3f0663a7f4d1026b9e03d93fe2cc7f0b13af`
- material source tree SHA-256：`9a7fc95c8a46bb0d094adf57bdfe381c4b41115cbb60aa18caff601bec7e12e9`
- launch receipt SHA-256：`d317b7089193ac12f67a6ca545344c9cef97fbcf803224149e7c1ab4e5f20259`
- detached PID：`15984`

## 可观察事实

1. `cell-001/attempt-01` 终态为 `completed`，61 个已接受原子操作、6 个 final assays，完整写出 `run_summary.json`。
2. `cell-002/attempt-01` 仅有 `run_config.json`、`environment_contract.json` 和轨迹记录；最后一个持久事件发生于 `2026-08-01T15:44:02.8410346Z`，已接受操作数为 4。
3. detached PID 随后不存在；系统中没有相同命令行的 Python/Codex 子进程。
4. launcher `stderr.log` 为空，Windows Application 日志中没有对应的 Python、Codex 或 PID 15984 崩溃事件。
5. 由于没有失败摘要，不能把中断追溯性地改写为 provider failure、method-limit failure 或成功单元。

## 排除与重启规则

- 不覆盖、不删除、不补写第一次启动中的任何实验目录。
- 不把 `cell-001` 的完成结果与第二次启动拼接。
- 不基于第一次启动的 endpoint、best score 或条件差异修改协议、顺序、世界、arm、预算或分析。
- 第二次启动使用同一协议和同一 20-cell schedule，但写入新的输出根目录。
- 执行改为由当前任务前台托管并持续等待，避免 detached 子进程被宿主回收。
- 只有第二次启动的 20 个单元全部终态化、通过身份验证、资源账本审计和精确回放后，才能进入论文。

## 对实验缺口的影响

确认性缺口仍是完整的 20 cells / 120 fresh-vessel experiments / 120 provider sessions。第一次启动产生的 6 个完成容器和 1 个未完成容器均属于排除数据，不减少该缺口。
