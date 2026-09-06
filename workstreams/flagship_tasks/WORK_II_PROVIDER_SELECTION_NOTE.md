# Kimi/Qwen逐一接入与有限开发校准

2026-09-06；W2-85；Codex /root，main，单executor，development mode。用户授权逐一测试
上一轮推荐的两个候选。本块独立于已终止的GLM开发块，不补跑GLM、不替换历史失败。

**问题与固定名单。** 按顺序测试`Pro/moonshotai/Kimi-K2.6`、
`Qwen/Qwen3.5-397B-A17B`。测量协议兼容性，不按科学答案、恢复率或收益选择模型。
原生Responses直连和Chat工具能力分别记录，不能用模型清单或HTTP成功代替harness通过。

**覆盖与通过。** 每个模型先做1次原生Responses短探针和2次Chat工具调用/返回探针，
后者首请求明确指定calculate工具，host仅执行固定的19+23并回传42，最终须返回42。
共6个直接HTTP机会；第二次Chat请求依赖首请求产生合法调用，否则保留未启动。
随后每模型按`json_schema`、`prompt_schema`各运行1个fresh Codex会话，两轮沿用W2-84
公开标记和42/43算术任务，共4会话、8计划轮。工具选择保持auto，要求两轮合法JSON、
相同thread、真实MCP审计值42/43、无越权或协议错误。两个模式都测，不因先前结果取消。

`prompt_schema`把完整原schema放入system提示，省略上游response_format；Codex的原始
output-schema与host校验保留。它只限制最终答案语义，不声称服务端strict decoding。
不把普通文本中的工具描述转成调用，不修正模型答案，不强制harness的工具选择。
两种模式预先固定，用于区分当前适配方式的可用性；每模式仅一次，不推断可靠性比例。

**选择与校准。** 两模型、两模式全部结束后，选择预定顺序中首个harness通过者；同模型
优先json_schema。随后该候选运行原B3 development seed0的3prior×tool off/on共6个fresh
会话、12轮，原提示/schema/validate/score及公开私有隔离保持。6/6合法两轮完成且无工具/
thread/传输问题，才登记为有限开发校准通过的第三模型。科学结果不控制选用，不重试科学
负结果；候选校准失败时不顺位换模型。本块不生成新物理或replay，不追加旧正式分母。

**预算与停止。** 直接HTTP超时60秒、输出1024tokens、自动重试0；每个harness冒烟最多
12次上游请求，每次输出8192tokens/120秒，Codex每轮240秒。校准按既有480秒/session、
2700秒/块、最多48次上游请求。每30秒报告当前阶段、事件/工具计数；阶段末给完成分母、
耗时和ETA。单元失败保留，继续其他预定单元；共享平台缺陷则停止并保留全部未启动项，
修复不在本块内追加尝试。未通过者不得作为正式第三模型科学证据。

**输出。** 原始请求/响应/回执留ignored runs；凭据仅在内存及非回显终端输入。单份脱敏
JSON/Markdown报告保留6个HTTP机会、4个harness会话、6个条件性校准会话的完整分母、
全部失败、真实工具/thread计数、实报usage及wall。没有usage时保持null。上游默认thinking，
Codex的medium标签不映射成跨模型等效算力；SSE输出项仍采用缓冲方式。实测六会话耗时
只能粗估相同开发输入的运行量级，不能据此承诺正式60会话的耗时或费用。

## 执行终态与后续工程修复

固定两模型、四个harness会话已全部尝试：7/8轮到达，Kimi的prompt_schema通过，
两轮同thread、真实MCP值42/43、合法终答，耗时17.08秒。两模型的strict模式都能回答
算术题，但实际工具调用0，不算通过。原生Responses均404；直接HTTP为5/6尝试、
2通过、3失败、1依赖未启动。Qwen明确不支持指定function的tool_choice；其prompt_schema
又因多个system消息被服务拒绝。这些是当前请求格式的兼容性结果，不证明Qwen不会用工具。

按预定顺序选择Kimi进入开发校准，终态为**0/6完成、1失败、1中止、4未启动；2/12轮尝试**。
首会话pre在180.406秒出现Codex SSE idle timeout，上游仍未返回；执行器随后进入第二会话，
造成未完成上游请求重叠。发现后停止本块专属进程树，保留所有落盘请求、首个失败回执、
第二会话已启动事件与未启动分母。没有补写模型输出，也没有把中止记为成功或换候选校准。

该事故暴露了平台缺陷：原socket超时没有约束整个stream的总时长，调用方断开后上游未取消，
而原始chunks直到请求结束才落盘。因此两个未完成上游请求的响应、usage和总wall未知；
已落盘证据复原的终态明确标注reconstructed，不伪造缺失资源。实报输入32,173、输出917，
只覆盖返回usage的请求；六会话吞吐和正式ETA仍未知。

停止后完成工程修复：总时限watchdog、取消未完成请求、禁止同适配器的上游请求重叠、
增量保存流式chunks，并在失败后停止校准块。Qwen所需的开头system消息合并也已完成，
保留原schema与公开合同的完整文字和顺序。42项定向与相关回归通过，包括持续keepalive
不能延长deadline、主动取消与usage保留、模型身份/凭据隔离及中止分母恢复。
这些修复**尚未进行新的线上资格复核**，不能将修复后的实现回填为本块通过。

结论：Kimi登记为**短工具闭环通过的优先候选**；完整第三模型开发资格尚未取得。
后续若推进，先在修复后的传输上重新校准科学会话预算并另立完整6会话块；
不追加本块第3个会话来补满分母。Qwen可在修复后的格式上另做有限接入复核。
MiniMax/Kimi-Code不在本次预定两模型范围内，未调用。

当前记录由`configs/current.json`的`w2_85_provider_selection`解析：
[机器摘要](reports/work-ii-provider-selection-20260906.json)、
[可读摘要](reports/work-ii-provider-selection-20260906.md)。本块没有新增正式科学或物理实验。
