# GLM / SiliconFlow Codex harness 接入测试

2026-09-06；W2-83；Codex /root，单executor，development mode。

**问题。** 用户提供的SiliconFlow凭据能否访问GLM，并支持当前Codex harness所需的
Responses传输、结构化输出、工具返回及同thread继续？示例中的DeepSeek模型名仅作调用方式参考。

**覆盖与顺序。** 一次`GET /v1/models`发现可用GLM标识，选定一个文本GLM后固定记录。
发现请求成功后、首次推理前选定`zai-org/GLM-5.3`；本块不按推理结果更换模型。
依次测试一次简短Chat Completions、一次无害整数加法工具调用及其返回（最多两次请求）、
一次原生Responses调用。原生Responses可达时，再测试实际Codex harness命令构造、
结构化终答、一个只读本地MCP工具和同thread继续；不可达时仅做一次CLI路径诊断。
每个测试单元执行一次，保留全部错误；协议或本地启动修复用独立attempt记录，最多两次修复尝试，
不替换旧结果。最多12次付费推理请求，每请求最多2048输出tokens（服务未支持时注明未受控），
直连超时60秒、Codex单turn180秒、整块20分钟；每20秒报告阶段、完成数和elapsed。

**通过规则。** API连接、文本响应、工具闭环、原生Responses和实际harness分别判定。
仅HTTP 200或普通聊天成功不等于harness接通；harness通过须收到正确工具结果、合法JSON终答、
同thread第二轮保留先前信息。若原生Responses不支持，记录协议障碍，不报告正式接入成功。
不访问论文world、评分truth或Core，不产生科学能力结果，也不启动第三模型正式实验。

**测量与输出。** 保留model id、接口状态、finish reason、tool计数、可得usage、耗时、
CLI版本与失败原因。脚本从环境或不回显的stdin读取密钥，脱敏摘要进入reports；原始响应、
CLI输出和隔离工作目录仅进入ignored runs。密钥不写入文件、CLI参数或输出。
报告缺失usage，不以未报告用量当作零消费；不修改全局Codex配置或原冻结执行面。

**终态。** 6/6接入探针执行，4通过/2失败；原生Responses和实际Codex路径返回404，
尚未直接接通harness。未继续原生MCP/终答/续接验证或开发适配器。首次本地启动因stdin关闭
在网络请求前退出，改用getpass无回显输入后完成同一次发现请求。完整结果见
[脱敏报告](reports/work-ii-glm-harness-20260906.md)，原始输出位于ignored开发目录。

探针入口为`scripts/probe_work_ii_siliconflow_glm.py`，通过`uv run --no-sync python`启动。
使用环境变量`SILICONFLOW_API_KEY`，或在交互终端传入`--key-stdin`后无回显输入；
`discover`、`probe --model zai-org/GLM-5.3`、`codex --model zai-org/GLM-5.3`分别需要
独立的`--output runs/development/<new-path>`。结果合并不调用provider。
