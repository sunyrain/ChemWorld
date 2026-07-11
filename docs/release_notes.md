# 发布说明

## 2026-07-12 · Evidence and documentation update

本次更新不发布正式 leaderboard，重点是让工程状态、实验结果和允许主张保持一致。

- 完成四核心任务的 vNext 经典诊断：2 methods × 20 paired seeds × 4 tasks；
- 160/160 个结果通过轨迹 digest、完整 replay、指标重算和资源账本检查；
- objective-only 规则在四任务通过；
- 审计发现 structured GP 在三任务具有更高风险预算超限率；
- 因原协议未预注册安全/成本非劣界限，完整经典主比较保持未通过；
- 新增可搬移运行包审计和确定性统计复算；
- 文档重组为开始使用、运行评测、开发 Agent、理解环境、模型世界、数据部署和边界版本；
- 左侧目录支持一键折叠/展开并保存偏好。

下一次确认运行将升级约束决策规则并使用未触碰的新 seed cohort。

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
