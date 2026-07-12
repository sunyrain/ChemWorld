# 发布说明

这里记录用户可感知的接口、任务、世界律和证据状态变化。正在开发但尚未进入正式 runtime 的候选
能力不会被写成已经发布的功能。

## 2026-07-12 · Architecture, mechanism, RL and LLM evidence refresh

- 分层评价增加 recipe-search、operation-open-loop、operation-closed-loop 能力层，交互与资源诊断不进入端点总分；
- 六个研究任务均接入实际 provider 消费的机理/构成律族，9/9 任务—模式组合通过多世界、多配方校准；
- 机理干预版本和 opaque hash 进入轨迹，精确上下文缺失或篡改时回放失败关闭；
- SAC 单 seed 开发运行精确完成 100,000 步并保留五个 checkpoint；80k 明显优于 100k，正式矩阵继续关闭；
- 新 SafeGP β 诊断拒绝通过降低风险置信系数追逐确认阈值，原确认失败不变；
- live-LLM adapter 冻结 Pro/Flash 角色、费用账本和失败策略；assigned/masked 消融保持所有非谱图证据不变；
- 全局架构控制层一致，正式证据层仍有 11 项活动问题，完整 benchmark 与 publication 主张保持关闭；
- 公开文档改为用户旅程导航，删除维护者执行路径与内部认领信息。

## 2026-07-12 · Safe-GP development and untouched confirmation

- 修复风险代理误学 final-assay 末态风险的问题，改为实验内操作峰值风险；
- recipe space 升至 0.2，类别材料使用 one-hot，连续用量与类别选择解耦；
- Dev seeds 1100–1119 上完成 240 条策略选择运行和独立回放，开发证据不得用于 benchmark 主张；
- 在结果产生前绑定策略实现摘要、seeds 500–519、SESOI、安全/成本界限与统计规则；
- 完成 240/240 条确认运行和第二次独立 replay，失败 0、轨迹摘要 240 个且互不重复；
- Safe-GP 相对 random 的四项 safety/cost 规则与四项目标方向通过；
- 连续流平均目标效应 0.018752 低于 SESOI 0.020000，完整联合规则为 `false`；
- benchmark、publication 与方法优越性主张继续关闭，seeds 500–519 不得用于后续调参。

## 2026-07-12 · Constrained fresh-cohort evidence

- 归档 0.2 objective-only 协议与证据，不复用其 seeds 20–39；
- 0.3 在运行前冻结 seeds 300–319、安全/成本非劣界限和同时置信上界；
- 新 160-run cohort 与第二遍独立 replay 均为 160/160，失败 0；
- 四任务 objective 和 cost 非劣通过；分配 safety 通过，流动/结晶/蒸馏 safety 失败；
- 完整 classical primary rule 为 `false`，benchmark/publication claims 保持关闭。

## 2026-07-12 · Documentation and evaluation redesign

本次更新不发布正式 leaderboard，重点是让工程状态、实验结果和允许主张保持一致。

- 完成四核心任务的 vNext 经典诊断：2 methods × 20 paired seeds × 4 tasks；
- 160/160 个结果通过轨迹 digest、完整 replay、指标重算和资源账本检查；
- objective-only 规则在四任务通过；
- 审计发现 structured GP 在三任务具有更高风险预算超限率；
- 识别原协议未预注册安全/成本非劣界限，完整经典主比较保持未通过；
- 新增可搬移运行包审计和确定性统计复算；
- 文档重组为开始使用、运行评测、开发 Agent、理解环境、模型世界、数据部署和边界版本；
- 左侧目录支持一键折叠/展开并保存偏好。

该诊断直接触发了上面的 0.3 约束协议；旧 cohort 未被事后重新解释。

## World Law v0.4

当前 runtime 使用 `chemworld-physical-chemistry-v0.4` 与 task contract 0.6。它是可执行后端，不是
冻结 benchmark release。

- 干燥、浓缩、转移、LLE、洗涤、蒸馏、结晶、连续流和电化学使用显式 provider route；
- spent sorbent、condensate、vent、source heel 和 line hold-up 进入 typed ledger；
- 正式路由不使用旧通用 separation proxy/fallback；
- 15 个任务均为 `proxy_allowed=false`，整体成熟度仍按最弱必需模块聚合为 `lite`；
- 世界律、任务、场景、机理、观测和评分摘要进入轨迹。

无 proxy route 只说明运行时路径明确，不代表模型达到现实工业验证。

## 0.2.0 与历史 serious-v1

Python 包版本仍为 0.2.0。历史 `chemworld-serious-v1` 使用 World Law v0.3 与 task contract 0.5，
只适用于对应合同。历史 candidate bundle 被保留用于回归和证据溯源，不会被新结果静默改写，也
不能作为 v0.4 正式发布证据。
