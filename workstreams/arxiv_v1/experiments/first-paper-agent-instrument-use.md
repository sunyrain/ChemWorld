# 第一篇完整 agent 仪器使用实验说明

状态：**FROZEN BEFORE DATA GENERATION**  
执行者：**Codex `/root`**  
任务：**U04、U05、E02**

## 问题与独立单位

问题：一个完整 agent 系统能否只读取公开 task contract，在构造器冻结后生成的未见
`reaction + thermal + distillation + observation` 世界中自主选择逐步操作、承担失败与资源后果，并在不修改
核心 runtime 的条件下闭合一次生命周期和通过 exact replay？U04 只复用既有受控 world-fork 正式证据，
不产生新数据。

唯一新实验单位是一个完整 agent 系统在一个冻结世界中的一次生命周期。世界固定为 current composition
qualification 中生成顺序第一项：composition
`qualification-reaction-distillation-observation-coverage-0001`、case
`qualification-reaction-distillation-observation-case-0001`、generation seed 105、generation index 0、world seed 0，
composition request SHA-256 为
`2c5ac886b1ed95eb2868aae285e8183510a34da1bd317b42ab6be131fb0d152e`；该请求在当前 runtime
编译得到的 task contract hash 固定为
`9b775c56b1cfe07dc75afc355d4815077913b27cbeedf20d32fb21d9dadf9f14`，composition qualification
保存的公开 compiled task subobject hash 固定为
`0ada08676d4b4afd20383619b4a1392639b4641ad26a15fb3b3e0f38c0b2de1e`。不得按结果改选其余七项。

## 冻结 agent、权限与预算

- 系统：`InteractiveCodexExperimentAgent`；method ID
  `first_paper_u05_interactive_codex_sol_medium_v1`；一个 `codex exec --ephemeral` 持久会话通过 host-owned
  `chemworld_lab` MCP 控制完整 experiment。model `gpt-5.6-sol`，reasoning effort `medium`，agent seed 0。
- provider/auth 使用 Codex CLI 的 cached ChatGPT subscription login；冻结 preflight 为 `codex-cli 0.145.0` 且
  login status 通过。pre-action restart limit 为 0；运行级不允许换模型、换 seed、换世界、resume 或重启后择优。
- 环境操作上限 16；完整生命周期上限 1；wall time 上限 3600 s；provider session/model-call 上限 1；输入
  token 上限 192000；输出 token 上限 64000；单次下一动作等待上限 600 s，session finalization 上限 300 s。
- agent 只见公开 composition/task contract、decision state、合法 action signatures、资源和明确的
  `terminate -> final_assay` 生命周期。host 不修复 action，不自动 terminate，不自动 final assay，也不把
  确定性参考轨迹放入 prompt；apps、subagents、web 和非 `chemworld_lab` 工具不参与实验决策。
- 原始 provider response、私有 reasoning、认证材料、临时 workspace 和模型笔记不进入 Git；只保留去敏
  session/tool receipt、usage、公开 action audit 和环境回执。ChatGPT subscription 没有可归因到单次运行的
  美元价格，因此只报告 token/session accounting，不把美元成本写成测得的零。

## 测量与通过规则

每个 submitted action 保存公开输入摘要、agent action、schema/transaction、constitution checks、world events、
资源 preflight/outcome、公开观测、method-resource 和 provider receipt 绑定。最终保存终止/评价、public/private
边界、trajectory bytes 和 tolerance 0 的 exact replay。

整体通过必须同时满足：

- current registry 对 composition qualification、U04 world-fork evidence 和冻结 U05 case 的路径与 SHA 绑定通过；
- 恰好一个生命周期闭合，至少一个 committed `terminate`，且恰好一个 committed `final_assay`；无右删失；
- 恰好一个完整 Codex session；所有 action 均由该 session 经 MCP 提交；无 restart、host fallback、自动
  action repair、自动 terminate 或自动 final assay；
- session、MCP tool-call 和 token accounting 完整且在冻结上限内；不可恢复的 provider、IPC、工具完整性
  或结构化决策错误使结果失败；
- 环境资源与 method-resource 对账通过，公开输出无私有状态泄漏，exact replay verified 且
  `max_abs_error == 0`；
- 1--16 个 actions 全部 schema-valid 且 transaction `committed`；零 rollback、零 resource rejection；MCP
  `step` 数、accepted action 数和 trajectory record 数完全一致；
- 任何缺失回执、无效 action、rollback、未闭合生命周期、资源不一致、泄漏或 replay 失败使整体状态为
  `FAILED`。终端分数只作描述，不设性能阈值，也不形成模型排名。

正式运行没有运行级重试。若实现阶段发现平台缺陷，可以修复后从唯一实验单位的第一个 decision 重新开始；
一旦正式 provider call 开始，失败结果必须保留，不得用后续更有利的运行替换。

## 预期输出

- `workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v1.json`
- 同路径 Markdown 摘要，列出唯一生命周期的完整分母、所有失败、provider accounting、资源、终止和 replay，
  并列出 U04 既有 fork evidence 的 current binding 摘要。
- 不新增 manifest，不保存 raw provider payload，不写入 `runs/`。
