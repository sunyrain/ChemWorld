# LLM Agent Harness

ChemWorld 当前不依赖在线 LLM API。首版 harness 采用可复现的离线协议：

```text
Planner -> Action Validator -> Env Step -> Observation Summarizer -> Memory -> Next Action
```

这样可以先把 tool-use、validator-use、observation-use 和 replay 评测打牢，再接入在线模型。

## ToolUsingLLMStubAgent

`ToolUsingLLMStubAgent` 是确定性的 tool-using LLM stub。它不调用模型，但会模拟一个 LLM/tool agent 应该留下的行为记录：

- prompt input 摘要；
- selected action；
- reasoning summary；
- hypothesis note；
- validator result；
- observation summary；
- short memory summary。

运行示例：

```bash
python examples/demo_llm_replay_harness.py
```

在 trajectory JSONL 中，相关字段写入：

- `agent_view`
- `agent_trace`

## LLMReplayAgent

`LLMReplayAgent` 从 JSONL 读取固定 action trace：

```json
{"action": {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}}
{"action": {"operation": "add_reagent", "amount_mol": 0.010}}
{"action": {"operation": "terminate"}}
{"action": {"operation": "measure", "instrument": "final_assay"}}
```

它用于复现实验、教学展示和之后对真实 LLM trace 的离线评测。

## Why Offline First

离线 harness 有三个好处：

- 结果可复现，不受模型版本、API 波动和 temperature 影响；
- 可以先验证 action schema、validator、lab report、trajectory 和 replay；
- 后续接入真实 LLM 时，只需要替换 planner，不需要改变 benchmark contract。

## Trace Policy

`agent_trace` 只保存行为摘要，不强制保存完整 chain-of-thought。建议记录：

- prompt/task 摘要；
- validator 结果；
- selected action；
- observation-use 摘要；
- hypothesis or next-step rationale。
