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
`2c5ac886b1ed95eb2868aae285e8183510a34da1bd317b42ab6be131fb0d152e`。不得按结果改选其余七项。

## 冻结 agent、权限与预算

- 系统：`LiveLLMAgent` + WellAU JSON client；model `gpt-5.6-sol`，reasoning effort `high`，agent seed 0，
  assigned spectrum disclosure。
- 每次操作恰有一个逻辑 provider decision；每个 decision 最多 2 次传输尝试、180 s timeout、最多 4000
  输出 tokens。运行级不允许换模型、换 seed、换世界或重启后择优。
- 环境操作上限 16；完整生命周期上限 1；wall time 上限 3600 s；provider model-call 上限 32；输入 token
  上限 192000；输出 token 上限 64000。
- agent 只见公开 decision state、合法 action signatures、资源和生命周期合同。host 不修复 action，不自动
  terminate，不自动 final assay，也不把确定性参考轨迹放入 prompt。
- 原始 provider response、私有 reasoning、密钥和本地 payload 不进入 Git；只保留去敏 provider/session
  receipt、usage、公开 decision audit 和环境回执。WellAU 没有可核验的冻结价格表，因此不报告美元成本为零。

## 测量与通过规则

每个 submitted action 保存公开输入摘要、agent action、schema/transaction、constitution checks、world events、
资源 preflight/outcome、公开观测、method-resource 和 provider receipt 绑定。最终保存终止/评价、public/private
边界、trajectory bytes 和 tolerance 0 的 exact replay。

整体通过必须同时满足：

- current registry 对 composition qualification、U04 world-fork evidence 和冻结 U05 case 的路径与 SHA 绑定通过；
- 恰好一个生命周期闭合，至少一个 committed `terminate`，且恰好一个 committed `final_assay`；无右删失；
- 所有 agent 决定来自 provider；无 host fallback、自动 action repair、自动 terminate 或自动 final assay；
- provider/session 和 token accounting 完整且在冻结上限内；不可恢复的 provider 或结构化决策错误使结果失败；
- 环境资源与 method-resource 对账通过，公开输出无私有状态泄漏，exact replay verified 且
  `max_abs_error == 0`；
- agent 自选的无效或 rolled-back action 必须原样保留并计入分母，但只要生命周期最终闭合，不单独把行为失误
  改写成平台失败；任何缺失回执、未闭合生命周期、资源不一致、泄漏或 replay 失败使整体状态为 `FAILED`。

正式运行没有运行级重试。若实现阶段发现平台缺陷，可以修复后从唯一实验单位的第一个 decision 重新开始；
一旦正式 provider call 开始，失败结果必须保留，不得用后续更有利的运行替换。

## 预期输出

- `workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v1.json`
- 同路径 Markdown 摘要，列出唯一生命周期的完整分母、所有失败、provider accounting、资源、终止和 replay，
  并列出 U04 既有 fork evidence 的 current binding 摘要。
- 不新增 manifest，不保存 raw provider payload，不写入 `runs/`。
