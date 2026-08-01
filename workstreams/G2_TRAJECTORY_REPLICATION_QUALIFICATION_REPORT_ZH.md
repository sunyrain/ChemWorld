# G2 fresh-trajectory replication 资格实验报告

日期：2026-08-01

物质源码 commit：`f02fdd2a862cb081b6c2c88dc2b1cf28a8091253`

物质源码 tree hash：`33992882cf928d88edb29dd8a31e0b5cd0d951e30ebb2a852a5335bcb6e0ffb3`

协议：`g2-electrochemical-autonomous-material-information-seed1-seed3-r5-v0.5`

模型：原生 Codex CLI 0.145.0，`gpt-5.6-sol`，`medium`

## 结论

资格门槛通过。一个全新的 opaque K1 cell 在没有 WellAU、notebook、自动动作修复、自动 terminate 或自动 final assay 的条件下，完成了 17 个 agent 自选原始操作、一个完整容器生命周期和一次 final assay。completed 结果随后通过同一 runner 的只读 `--resume` 身份、资源、provider-session 与 exact-replay 复核。

本资格实验不进入 replication 统计，也不能作为 opaque/nominal 效应证据。它只回答：冻结的 native Codex + stdio MCP + campaign resource ledger + immutable attempt + manifest 路径能否端到端闭环。

## Q1：nominal K1，外层启动器截止导致右删失

- cell：`qualification-seed1-r01-nominal`
- 结果：`right_censored`
- 有效操作：11
- provider receipt：`interrupted_before_next_action / agent_closed`
- provider errors：0；stderr bytes：0
- trajectory SHA-256：`77c789d7a4c74c9567bf78ea3610644cf31cbf470a5ab0a9191f9a912da4f026`
- manifest SHA-256：`e73c4f9c731e2f80cea54b9212571e86fbd76398403430d7f4b68e4712aa58b2`

该 attempt 的唯一外层执行上限被误设为 120 秒；关闭时点与该限制一致，且 11 个 MCP step 均已成功、provider 没有返回错误。因此将它归因于 qualification 启动器截止，而不是 ChemWorld 接口拒绝。按照预注册规则，它仍然是一个不可替换的动作后 terminal right-censor：不删除、不覆盖、不对同一 cell 重跑。

## Q2：opaque K1，成功闭环

- cell：`qualification-seed1-r01-opaque`
- 结果：`completed`
- 原始操作：17；invalid：0；resource rejection：0
- 操作构成：add reagent 1、add solvent 1、set potential 3、electrolyze 7、非终点表征 3、terminate 1、final assay 1
- 容器：started 1、closed 1、discarded 0
- 资源：reagent 0.025 mol、solvent 0.06 L、non-final instruments 3/3、final assay 1/1
- final score：0.668462（仅用于验证结果完整性，不作科学比较）
- provider session：1/1 completed，input tokens 480,483，output tokens 3,107
- provider-session audit：passed
- exact replay：17/17 steps，maximum absolute error 0，verified
- trajectory SHA-256：`1a8cf71194e5d569f371fdcaee0decd581b582d78977944b6756599b2f01de84`
- resource ledger file SHA-256：`62dea221612a17da5347d6031ea83b0cb8e351b6c718e4d1518d449dfee6ff4b`
- run summary file SHA-256：`f810cddb4c6d17ce335bc5be53c1b3c8587af9e5fb343a2c9bb158c53bf907fb`
- manifest SHA-256：`0c9d6ce49f76dac4d457fe36bc095b2f789e39844a5d4145523beefc6c509db2`

## 对正式矩阵的操作约束

1. 不再使用 120 秒外层命令截止。单 Codex session 由协议内 900 秒 request timeout 控制；整个 cell 由方法账本和 6 小时上限控制。
2. 20-cell 矩阵必须以持久后台进程运行并独立写 stdout/stderr；交互式工具调用只负责读取 manifest 和审计，不负责维持进程生命。
3. Q1/Q2 都是 qualification-only cell，不复用为正式 r01 轨迹；正式矩阵仍从冻结 schedule 的 20 个新 cell 开始。
4. 正式运行保持原有 attempt policy：只有零动作 provider infrastructure failure 可重试；任何动作后的失败都永久右删失。

## 启动判断

接口、资源账本、模型自主逐操作、finalization、provider usage、exact replay 与 immutable recovery 均已得到真实证据。可以进入冻结的 20-cell replication；当前不需要修改科学协议或 agent prompt。需要修改的只是运行部署方式：使用持久后台 launcher 和只读监控，避免外部会话截止干扰实验。
