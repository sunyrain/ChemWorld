# G2 直接 Codex + 文档记忆单世界试跑

## 结论

直接调用 `codex exec -m gpt-5.6-sol` 已经能够完成严格的逐操作实验。seed 0
中，Agent 用 12 次自主决策完成了从配料到 final assay 的完整实验；12 个动作全部合法并
成功提交，环境没有修复动作，也没有替 Agent terminate 或执行 final assay。

这次试跑同时说明：把完整账本移出 prompt 是正确的，但“账本可访问”不等于“上下文自动
保持紧凑”。Agent 没有写自己的 notebook，而 Codex 总输入在多数中间步骤随账本增长，说明
下一版需要明确区分热记忆与冷历史，而不是仅仅把 JSONL 放在工作目录中。

## 冻结配置

- task：`reaction-to-assay`
- world seed / agent seed：`0 / 0`
- model：`gpt-5.6-sol`
- reasoning effort：`high`
- 调用方式：每个实验操作一次独立、ephemeral 的 `codex exec`
- 当前 public state：直接进入短 prompt
- 环境账本：宿主追加、Agent 只读
- Agent notebook：Agent 可读写
- 完整账本正文进入 prompt：否
- 自动 action repair / terminate / final assay：均为否
- 正式结果：否；仅为单世界、单 seed 开发试跑

## 行为结果

| 指标 | 结果 |
|---|---:|
| 完成实验数 | 1 |
| 总操作数 | 12 |
| 合法并提交 | 12 / 12 |
| 无效操作 | 0 |
| final assay score | 0.2207577082 |
| provider calls | 12 |
| provider input tokens | 188,776 |
| provider output tokens | 8,221 |

操作序列为：

1. `add_reagent(0.02 mol)`
2. `add_solvent(solvent=2, 0.02 L)`
3. `add_solvent(solvent=2, 0.02 L)`
4. `add_solvent(solvent=2, 0.01 L)`
5. `add_solvent(solvent=2, 0.0005 L)`
6. `add_solvent(solvent=2, 0.0495 L)`
7. `add_catalyst(catalyst=2, 0.002 mol)`
8. `heat(350 K, 1800 s, 600 rpm)`
9. `measure(hplc)`
10. `quench`
11. `terminate`
12. `measure(final_assay)`

HPLC 时可见结果为 conversion 0.83684、yield 0.39886、selectivity 0.49091；
Agent 随后明确以这些测量值为依据选择 quench，再完成 closeout。final assay 的 yield 为
0.39793、selectivity 为 0.46520。

## 账本与 prompt 膨胀审计

环境权威账本从 1 行、1,387 bytes 增长到 12 行、18,356 bytes。与此同时：

| 口径 | 第一步 | 最后一步 | 最大值 |
|---|---:|---:|---:|
| 直接 prompt 启发式估算 | 992 | 1,209 | 1,598 |
| Codex 报告的总 input tokens | 7,252 | 7,330 | 19,610 |
| notebook 大小 | 23 bytes | 23 bytes | 23 bytes |

因此可以确定：

- 完整账本没有被宿主逐轮拼接进 prompt。账本增加约 17 KB，但直接 prompt 没有与之等比例
  增长；其变化主要来自合法动作集合、测量结果和生命周期状态。
- Codex 总输入不能当成“直接 prompt 大小”。它还包括系统指令、动态输出 schema、工具
  上下文以及模型主动读取文件后产生的内容。
- 第 2–10 步总输入大体随账本增长，第 12 步又降至 7,330；这与“模型在需要规划时读取
  历史、在唯一 final-assay 动作时不读取”的解释一致，但本次没有保存逐工具调用事件，
  因而只能作为强迹象，不能作为已直接观测的文件读取次数。
- notebook 始终保持初始 23 bytes，说明仅赋予写权限并不会让 Agent 自发形成压缩记忆。

## 这次真正暴露的 Agent 特点

接口已不再是主要问题。更值得研究的是：

1. **局部约束追逐。** Agent 把反应前持续出现的 `low_selectivity` 当成可通过继续稀释即时
   修复的信号，连续进行了五次 solvent addition。
2. **缺少前置资源规划。** 它没有先形成“原料—溶剂—催化剂—反应—表征—closeout”的
   有限操作计划；加入 catalyst 后 cost 立即饱和到 1.0。
3. **测量后的认知更新较合理。** 得到 HPLC 后，它能引用 yield、byproduct 和 conversion
   选择 quench，并正确完成 terminate → final assay 生命周期。
4. **结构正确不保证语义审计正确。** 第 6 步虽然动作合法，但部分声明字段退化成通用占位
   文本，说明严格 JSON schema 解决了接口形状，尚未保证科学解释质量。

这正好把研究问题从“模型能否发出合法动作”推进到“它如何分配操作、材料、测量和认知
资源”。

## 下一步：仍然保持直接 Codex

无需新增一套复杂 Agent 框架。下一次只调整文档使用协议：

- 保留完整 JSONL 作为冷历史，仍可按需访问；
- 每轮默认只读取 notebook 和账本最后一条事件；
- 要求 Agent 在做出下一动作前，把 notebook 更新为固定上限的科学状态：当前假设、关键
  证据、资源余量、下一测试；
- 只有提出明确历史问题时才搜索完整账本；
- 保存 Codex 的文件读取/写入工具事件，以区分 prompt、工具读取和输出各自的 token。

一个更稳妥的最小实现是由环境额外维护 `latest_event.json`。它不是新的认知脚手架，只是
权威账本的最新一行视图；Agent 日常读取 `latest_event.json + notebook.md`，完整账本继续
作为可查询档案。这样能检验 notebook 是否真正承载跨步认知，而不是每轮重读全部历史。

## 证据位置

- 运行摘要：`runs/development/g2-reaction-to-assay-w0-a0-codex-sol-high-doc-v1/run_summary.json`
- 完整轨迹：`runs/development/g2-reaction-to-assay-w0-a0-codex-sol-high-doc-v1/trajectory.jsonl`
- 环境权威账本：`runs/development/g2-reaction-to-assay-w0-a0-codex-sol-high-doc-v1/codex_workspace/experiment_documents/environment_authoritative_ledger.jsonl`
- Agent notebook：`runs/development/g2-reaction-to-assay-w0-a0-codex-sol-high-doc-v1/codex_workspace/experiment_documents/model_owned_notebook.md`

轨迹回放校验通过：12 步、最大绝对误差 0、无 mismatch。
