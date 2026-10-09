# R17 / R18：持久笔记与完整公开历史

开发说明，Codex /root。问题：笔记是否可自由写且不会变成环境事实；最近缓存淘汰后模型能否查回最早的公开动作？

复用 ExperimentDocumentWorkspace 的 host append 与 notebook API、Codex public cache 和既有 artifact reader。保留现有最近缓存，另保留可分页的完整公开动作流；它是 host 事实的公开投影，不是评价器完整私有 trajectory，也不授权 agent 修改世界。history 默认仍取最近条目，offset 从 0 开始定位历史；明确总条数、窗口省略数量及下一页。无新检索索引或恢复状态机。

执行前固定：无 provider 的文档适配示例执行 seed 0 的 reaction-to-assay，0.025 L 溶剂、0.012 mol 试剂、HPLC、terminate、final assay；故意先提交一次缺物料 HPLC 并保留失败。Notebook 写一个假设/观察/后续问题，host ledger 不因笔记变化；新进程读取并验证完整轨迹。另用 80 条明确标成合成的公开事件穿过实际 workspace append，最近缓存限制 64，经 MCP 和生成的 lab_tool 子进程读取 offset=0 首条及分页到最后一条。测试页边界、重启读取、限额及事实账本篡改拒绝。

验收：6/6 操作记录保留（包括 1 次预期拒绝）；轨迹零容差回放；笔记写入前后事实账本相同；80/80 公开事件可定位，缓存确实淘汰首条，两个工具一致，输出不含 evaluator/private state。错误完整保存，不改覆盖以追求通过。输出根 `D:/Projects/ChemWorld-local-research/20261009-r17-r18/`。本块不声称 LLM 压缩恢复成功。

结果：2/2 开发块通过。6/6 真实操作保留（5 committed、1 预期拒绝），终检与零容差 replay 通过；新 Python 进程重读笔记并校验同一事实账本/轨迹。80/80 合成公开事件经 MCP 与独立 lab_tool 子进程一致返回，缓存只剩 64 条且首条变为 operation-0016，完整历史仍从 operation-0000 查到 operation-0079。机器摘要在上述输出根的 `attempt-01/summary.json`，六步明细在其文档块子目录的 `demo/summary.json`，失败列表为空。

相关测试 88 passed（文档/长历史/IPC/MCP 45，交互 agent 43）。Ruff 通过；新增 reader、IPC 与 demo 的 mypy 通过。MCP 原文件已有 4 个类型错误（重定义 context、三个 Optional 用法），从 HEAD 原文件副本复核相同错误，未借本项重写 Work II。未做真实 LLM 压缩恢复或 provider 调用。

交接 LYJ R16：`scripts/run_research_documents_demo.py` 提供 `run(Path)` 与 `--output`，输出目录必须全新，避免覆盖结果；模型适配只暴露 read_notebook/write_notebook，append_operation 由宿主调用。示例的假设、执行前预测、观察与证据引用、解释/不确定性、下一步模板同时覆盖 R22。API 所有权不等于本地同进程任意代码的 OS 沙箱。

history 新增零起点 offset 和 next_offset；默认最近 5 条、最多 10 条，并按现有工具字节预算缩页。返回 source、总数、省略数和 cache_truncated；单条过大时返回 oversized_event 的精确 offset 与持久 source，不跳过、不丢记录，可直接读该公开文件。缺少完整 archive 会明确报错，不把旧缓存伪装成完整空历史。生成的 stdlib-only lab_tool 与 MCP 共用同一 reader；最近缓存仍供现有轻量消费者使用。公开动作流与 evaluator trajectory 分开，前者不授予改写环境事实的权限。
