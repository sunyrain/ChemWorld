# GLM Responses适配与第三模型开发校准

2026-09-06；W2-84；Codex /root，单executor，development mode。用户授权尝试适配，
可用时采用GLM为第三模型；原W2-83的原生404失败和既有双模型正式结果保留。

**固定问题和模型。** `zai-org/GLM-5.3`通过SiliconFlow Chat Completions能否保留当前
Codex harness的消息、MCP工具返回、结构化提交、usage和同thread语义？只增加传输适配，
不修改原harness执行器、科学提示或评价器，不修正模型答案。适配器只监听loopback，以临时
本地token鉴权；上游凭据仅在适配器内存，原始请求/响应仅保留ignored runs。

**固定覆盖。** A：一条Codex thread、两轮。首轮通过public_numerics算19+23并提交JSON，
同时保存公开标记`LANTERN-47`；续轮从前文恢复标记并用同一工具计算上一结果+1。
检查42/43、标记、至少两次真实MCP调用、合法JSON与相同thread。B：A通过后复用原B3
开发seed0全部三prior，工具off/on各一次，共6个fresh sessions、12轮；使用原pre/post提示、
schema和validate，只向模型发送公开包。旧开发truth仅在回答后评分，不生成新物理或重放。
本块不改公开信息包，不能填补F2同信息充分性缺口。

**通过与停止。** A的所有检查通过，B的6/6完成两轮合法提交，无工具越权、协议错误或thread
替换，即把GLM登记为已通过有限开发校准的第三模型；结构恢复率、预测误差或收益不影响选用。
失败和未启动项留在固定分母，不因模型答案不好重试。A工程调试最多3个独立attempt；
B开始后如发现适配器缺陷，停止原块并在修复后完整重跑一次，旧结果独立保留。
科学能力复核另立正式块，不将本次开发数据追加进旧主分析。

**资源。** 单次上游输出最多8192 tokens、超时120秒、自动重试0；A/B各自最多48次上游请求，
Codex每turn240秒，B每session480秒、整块45分钟。20–30秒输出当前session/turn、完成数、
上游请求数与elapsed。上游默认thinking保持，Codex的medium配置标签不当作GLM等效算力。
记录schema的实际传输方式；若json_schema被服务拒绝，开发期可改为json_object加原schema
明文，答案仍由原host验证，不声称服务端strict decoding等价。

**输出。** 可复用本地适配器、独立启动/校准脚本、相关协议测试、单份可读JSON/Markdown报告，
候选配置和当前TODO/矩阵状态。记录全部失败、请求/输出tokens、实际模型、工具与thread计数；
缺失usage保持缺失。Codex所需SSE事件可由上游流式输出完整收集后生成，须明确记录缓冲策略，
不把本地生成的传输事件解释为额外模型推理或科学证据。

## 执行终态

A已用完3次工程尝试，完整通过0/3；计划最多6轮中尝试4轮，2轮终答和thread检查通过，
但真实MCP执行为0。B未启动6/6，正式科学会话0；GLM尚未采用为第三模型。

- smoke-01：本地namespace/custom工具翻译缺失，未到上游；修复后，离线模拟上游驱动
  真实Codex两轮、两次真实MCP成功。模拟结果仅验证本地协议，不算GLM资格。
- smoke-02：上游HTTP 200，严格schema下42/43与同thread均正确，但零工具调用。
- smoke-03：json_object下返回含`pending_tool_calls`的普通JSON，未生成原生tool call，
  缺少必需sum字段。没有把这段文本改写成工具调用，也没有修正答案。

第三次fallback的触发与原预设有偏离：服务并未HTTP拒绝json_schema，而是在实际调用中
未执行MCP。因此第三次仅作为另一种已列明传输方式的工程排查；不据此宣称定位了服务端
根因或完成预设资格。所有失败及未启动项保留，达到三次上限后停止。

后续若继续，候选方向是把工具调用阶段与最终结构化提交分开，先独立验证该协议语义；
不能从答案文本中的“待调用”字段执行工具，不能用自动纠错补齐schema。需要新开发设计，
不续跑本块第四次尝试、不将本块推广为GLM科学能力结论。

机器摘要及可读结果：[JSON](reports/work-ii-glm-adapter-20260906.json)、
[Markdown](reports/work-ii-glm-adapter-20260906.md)。本块实报输入12,476、输出221 tokens，
其中reasoning135；三次尝试wall合计约20.33秒，不含开发调试。6会话和60会话ETA未知。
上游凭据仅驻留适配器内存；子Codex仅收到临时本地token，未将凭据写入文件或命令行。
当前报告由`configs/current.json`的`w2_84_glm_adapter_development`解析。
33项适配/原生探针/既有诊断相关测试通过，Ruff通过；开发资格失败不改变这些工程测试的含义。

复算报告（不发起provider请求）：

```powershell
uv run --no-sync python scripts/check_work_ii_glm_bridge.py report `
  --output workstreams/flagship_tasks/reports/work-ii-glm-adapter-20260906 `
  --attempts runs/development/work-ii-glm-adapter-20260906/smoke-01 `
    runs/development/work-ii-glm-adapter-20260906/smoke-02 `
    runs/development/work-ii-glm-adapter-20260906/smoke-03
```
