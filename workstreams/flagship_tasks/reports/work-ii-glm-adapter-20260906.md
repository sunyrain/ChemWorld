# GLM Codex适配开发资格结果

2026-09-06；模型 `zai-org/GLM-5.3`；development evidence。

第三模型采用：**否**。真实工具闭环通过 0/3 次工程尝试；六会话校准完成 0/6，未启动 6/6。

| 尝试 | schema传输 | 尝试轮数/计划 | 实际MCP调用 | 完整通过 | wall秒 |
| --- | --- | --- | --- | --- | --- |
| smoke-01 | json_schema | 1/2 | 0 | False | 0.62 |
| smoke-02 | json_schema | 2/2 | 0 | False | 12.06 |
| smoke-03 | json_object | 1/2 | 0 | False | 7.64 |

## 每次失败

- smoke-01: 终答或thread检查未通过; 没有真实MCP调用; 本地适配器不支持当时的工具声明, 请求未到上游。
- smoke-02: 没有真实MCP调用。
- smoke-03: 终答或thread检查未通过; 没有真实MCP调用。

## 资源与边界

本块记录 4 次本地请求，3 次到达上游HTTP；报告输入 12,476、输出 221 tokens，其中reasoning 135。1 条请求无usage，原记录保留null。

未取得六会话吞吐，60会话正式复核ETA保持未知；不能用短算术调用外推。

- Development transport qualification only; historical two-model evidence is unchanged.
- Provider-default reasoning; Codex medium is not mapped to equivalent GLM effort.
- Upstream output is buffered before Responses output-item SSE events are emitted.
- Freeform tools use a JSON input string; grammar constraints are conveyed as text.
- Missing provider usage remains null in request records.
- Short smoke latency does not estimate the unstarted six-session calibration.

实验与停止规则见[实验说明](../WORK_II_GLM_ADAPTER_DEVELOPMENT_NOTE.md)。
原始请求、输出和凭据不进入Git；同名JSON保留全部尝试与固定分母。
