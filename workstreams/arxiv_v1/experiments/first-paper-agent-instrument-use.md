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
`687007fb2fe9e7cb7bde1eff10219469fecc73903648d2fa34fec17c10694b4f`；该请求在当前 runtime
编译得到的 task contract hash 固定为
`9b775c56b1cfe07dc75afc355d4815077913b27cbeedf20d32fb21d9dadf9f14`，composition qualification
保存的公开 compiled task subobject hash 固定为
`2d89a69f68d910dc8593a6ccfad698b108114a5295d18a4c362aad59155c497d`。不得按结果改选其余七项。

## 冻结 agent、权限与预算

- 系统：`InteractiveCodexExperimentAgent`；method ID
  `first_paper_u05_interactive_codex_sol_medium_v1`；一个 `codex exec --ephemeral` 持久会话通过 host-owned
  `chemworld_lab` MCP 控制完整 experiment。model `gpt-5.6-sol`，reasoning effort `medium`，agent seed 0。
- provider/auth 使用 Codex CLI 的 cached ChatGPT subscription login；冻结 preflight 为 `codex-cli 0.145.0` 且
  login status 通过。pre-action restart limit 为 0；运行级不允许换模型、换 seed、换世界、resume 或重启后择优。
- 环境操作上限 16；完整生命周期上限 1；provider session 与 logical Codex turn 上限各 1；MCP `step`
  上限与已提交环境操作数一致。单次下一动作等待上限 600 s，session finalization 上限 300 s，另加
  600 s runner/IPC 余量，因此 method wall time 上限按 `16 × 600 + 300 + 600 = 10500 s` 冻结，而非
  与分项 timeout 矛盾的统一 3600 s。
- cumulative input token 上限 640000，其中 517000 是旧正式 session 的已审计累计 input 基线，另留
  123000 headroom；uncached input token 仍独立硬限制为 192000，输出 token 上限 64000。cache hit 只
  表示被后续 backend response 再次使用的历史 input context，不是重复 output，也不能用来绕过
  cumulative input 上限。
- U05 专用 MCP 单次返回上限 16384 bytes，history 最多 16 条且总计 65536 bytes。新冻结 12-step
  unseen 路径的实测最大 step response 约 6.2 kB，故该 cap 保留超过 2 倍余量，同时限制意外上下文膨胀。
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

## 2026-08-05 调用路径与 provider accounting amendment

U05 在 2026-08-05 正式 provider 调用前，从原计划的 `LiveLLMAgent`/WellAU 逐操作 JSON decision
改为已经在 G2 v0.4 资格化的原生 Codex CLI 路径：一个 `codex exec --ephemeral` 完整实验 session，
通过 host-owned `chemworld_lab` STDIO MCP 逐步提交动作。该变更的目标是验证完整 agent 生命周期，不是
把 MCP session 误当作一次底层模型请求；DeepSeek 对比臂仍是每个 primitive operation 一次直接 JSON
decision，两个系统的 transport/scaffold 不同，不能当作同构单次调用比较。

原 amendment 没有同步重估累计 token 和流程时间预算。后续版本必须同时报告
`provider_session_count`、`logical_codex_turn_count`、`mcp_tool_call_count` 和（只有 provider 暴露时）
`backend_model_response_count`。`input_token_count` 是完整 Codex turn 的累计 input；其中 cache hit 是
复用的历史 input context，不是重复生成的 output，必须与 cache miss 分栏报告。当前 v1 的 517,000 input
tokens、439,040 cache-hit 和 77,960 cache-miss 失败结果不可覆盖；修复后须以新版本预算从唯一 decision
重新运行，并保留该失败。

旧 U05 回执中的 21,658.454 s 也不是“重复 output”造成的，而是开放动作没有 process-time preflight：
agent 连续提交了 3 次 heat（3,600/7,200/3,600 s）和 2 次 distill（各 3,600 s），另有 quench 与
fraction collection 的隐含耗时，超过原手工 `time_s=14,400`。修复后的 pattern envelope 会在提交前
同时拒绝超出累计时间或 operation repeat 上限的动作；method wall time（agent 运行耗时）仍与世界
process time（物理账本秒数）分开记录，不能互相替代。

修复后未见 composition 的 request SHA-256 为
`687007fb2fe9e7cb7bde1eff10219469fecc73903648d2fa34fec17c10694b4f`，公开 compiled task subobject
SHA-256 为 `2d89a69f68d910dc8593a6ccfad698b108114a5295d18a4c362aad59155c497d`；runtime task contract
hash 保持 `9b775c56b1cfe07dc75afc355d4815077913b27cbeedf20d32fb21d9dadf9f14`。变化来自新增公开
`process_time_policy`，不是世界、seed 或生成顺序改选。新 provider run 开始前必须重新冻结并核对这三个
binding；旧 design-v1 请求和旧失败结果继续保留为历史，不得覆盖。

## 2026-08-05 正式 v2 失败与 design-v3 平台修复

经用户明确授权，正式 v2 provider 单元在一个 session / 一个 logical Codex turn 中提交 16 个动作。前 15 步
全部 committed，process time 为 8,435.453 s（低于 10,440 s），token、MCP、资源、公开边界和 exact replay
均对账；第 16 步 final assay 被 `declared_process_resource:operation_repeat_limit` 拒绝，因此生命周期右删失并
判定 FAILED。该结果固定保存在 v2 报告中，不得覆盖或解释为成功。

根因是 design v2 将 `measure` repeat limit 从冻结参考 workflow 推导为 3，同时任务资源允许 3 次非终检测量
加 1 次 final assay，总 instrument-use 上限为 4。Design v3 只修复这一平台合同矛盾：所有 composition 的
`measure` repeat limit 必须等于其声明的总 `instrument_uses`；process-time 上限和其他 operation repeat limit
不变。修复后先从首个 case 重跑受影响的离线资格并冻结新 request/task bindings，随后才可从第一个 decision
执行一个新的正式 provider 单元；v2 失败永久保留，且新单元仍不得运行级重试、择优或结果替换。
