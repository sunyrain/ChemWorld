# GLM / SiliconFlow Codex harness 接入结果

模型：`zai-org/GLM-5.3`；Codex：`codex-cli 0.145.0`。开发接入测试，无科学会话。

结论：聊天与工具闭环成功；原生Responses及实际Codex路径均返回404，未直接接通harness。

| 探针 | 结果 | HTTP / CLI退出码 | 耗时（秒） |
| --- | --- | ---: | ---: |
| models | 通过 | 200 | 0.172 |
| chat_text | 通过 | 200 | 1.844 |
| chat_tool_call | 通过 | 200 | 1.797 |
| chat_tool_return | 通过 | 200 | 0.875 |
| native_responses | 失败 | 404 | 0.125 |
| native_codex | 失败 | 1 | 0.641 |

6/6探针已执行，4通过、2失败；两条CLI错误事件属于同一次失败会话。
工具API调用19+23后收到42，并正确使用工具结果完成回答。
MCP执行、合法结构化终答、同thread续接因传输失败未到达，不能报告通过。

三次成功推理报告输入518、输出112 tokens；失败请求未返回usage，不将其消费写成零。普通短调用耗时不能外推科学实验ETA。

当前harness的wire_api=responses；该入口仅验证了Chat Completions能力。
后续可开发Responses→Chat Completions适配器，再单独验证流式事件、工具返回、usage与会话续接。本块未实现适配器，也未启动第三模型科学实验。

首次本地启动因stdin关闭在网络调用前终止；已改用PTY无回显输入。凭据未写入文件、参数或日志；原始响应仅保留在ignored runs。

Codex协议依据：[官方配置文档](https://learn.chatgpt.com/docs/config-file/config-reference)。
